"""Offizielle Prüfung mit den Regeln der KoSIT, ohne Java.

Die KoSIT veröffentlicht die Prüfregeln für XRechnung als Konfiguration für
ihren Java-Validator. Darin liegen XML-Schemas und die Schematron-Regeln
bereits als kompiliertes XSLT. Dieses Modul führt genau diese Dateien aus:
XSD über lxml, XSLT 3.0 über saxonche (Saxon-HE als Python-Paket).

Ablauf wie beim KoSIT-Validator:
1. Szenario über ``<match>`` aus ``scenarios.xml`` wählen
2. XML-Schema prüfen
3. Alle Schematron-Stufen des Szenarios ausführen
4. ``customLevel`` des Szenarios anwenden (z.B. BR-CL-21 nur Warnung)
5. Annehmen, wenn es weder Schemafehler noch Befunde der Stufe ``error`` gibt

Die Konfiguration wird beim ersten Aufruf von GitHub geladen, per SHA-256
geprüft und im Cache abgelegt. Offline: ``ERECHNUNG_KOSIT_KONFIG`` auf einen
entpackten Ordner oder die ZIP-Datei setzen.
"""

from __future__ import annotations

import hashlib
import io
import os
import sys
import urllib.request
import gc
import queue
import threading
import zipfile
from concurrent.futures import Future
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from lxml import etree

KONFIG_VERSION = "xrechnung-3.0.2-validator-configuration-2026-08-31"
KONFIG_URL = (
    "https://github.com/itplr-kosit/validator-configuration-xrechnung/releases/download/"
    "v2026-08-31/xrechnung-3.0.2-validator-configuration-2026-08-31.zip"
)
KONFIG_SHA256 = "2530cd107c414511c5d0462ec10f886910395abfca820db82e83d70bf01221a8"

VISUALISIERUNG_VERSION = "xrechnung-3.0.2-visualization-2026-10-13"
VISUALISIERUNG_URL = (
    "https://github.com/itplr-kosit/xrechnung-visualization/releases/download/"
    "v2026-10-13/xrechnung-3.0.2-visualization-2026-10-13.zip"
)
VISUALISIERUNG_SHA256 = "ecf3913029218822ee4c90a86a3e23689768bf3568a061cf9bc742115e52264e"

NS_SCENARIO = "http://www.xoev.de/de/validator/framework/1/scenarios"
SVRL = "http://purl.oclc.org/dsdl/svrl"

STUFEN = {"fatal": "error", "error": "error", "warning": "warning", "warn": "warning",
          "information": "information", "info": "information"}


class NichtVerfuegbar(RuntimeError):
    """saxonche fehlt oder die KoSIT-Konfiguration ist nicht erreichbar."""


@dataclass
class Befund:
    stufe: str  # error, warning, information
    code: str  # z.B. BR-DE-15, XSD
    text: str
    ort: str = ""
    quelle: str = ""
    stufe_original: str = ""  # Stufe laut Schematron, bevor das Szenario sie umstuft

    def als_dict(self) -> dict:
        d = {"stufe": self.stufe, "code": self.code, "text": self.text, "ort": self.ort, "quelle": self.quelle}
        if self.stufe_original and self.stufe_original != self.stufe:
            d["stufe_original"] = self.stufe_original
        return d


@dataclass
class Bericht:
    szenario: str
    akzeptiert: bool
    befunde: list[Befund] = field(default_factory=list)
    hinweis: str = ""
    konfiguration: str = KONFIG_VERSION

    @property
    def fehler(self) -> list[Befund]:
        return [b for b in self.befunde if b.stufe == "error"]

    @property
    def warnungen(self) -> list[Befund]:
        return [b for b in self.befunde if b.stufe == "warning"]

    def als_dict(self) -> dict:
        return {
            "szenario": self.szenario,
            "akzeptiert": self.akzeptiert,
            "konfiguration": self.konfiguration,
            "hinweis": self.hinweis,
            "befunde": [b.als_dict() for b in self.befunde],
        }


@dataclass
class Szenario:
    name: str
    match: str
    namespaces: dict[str, str]
    xsd: str
    schematron: list[tuple[str, str]]
    stufen: dict[str, str]


def cache_ordner() -> Path:
    eigen = os.environ.get("ERECHNUNG_CACHE")
    if eigen:
        return Path(eigen)
    if sys.platform == "win32" and os.environ.get("LOCALAPPDATA"):
        return Path(os.environ["LOCALAPPDATA"]) / "erechnung"
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "erechnung"


def _entpacken(quelle: bytes, ziel: Path) -> None:
    tmp = ziel.with_suffix(".tmp")
    with zipfile.ZipFile(io.BytesIO(quelle)) as z:
        for name in z.namelist():
            if name.startswith("/") or ".." in Path(name).parts:
                raise ValueError(f"Unsicherer Pfad im ZIP: {name}")
        z.extractall(tmp)
    tmp.rename(ziel)


def bereitstellen(url: str, sha256: str, name: str, umgebung: str, offline: bool = False) -> Path:
    """Ordner mit entpackten KoSIT-Dateien, notfalls frisch geladen."""
    eigen = os.environ.get(umgebung)
    if eigen:
        pfad = Path(eigen)
        if pfad.is_file():
            ziel = cache_ordner() / (pfad.stem + "-lokal")
            if not ziel.exists():
                ziel.parent.mkdir(parents=True, exist_ok=True)
                _entpacken(pfad.read_bytes(), ziel)
            return ziel
        return pfad
    ziel = cache_ordner() / name
    if ziel.exists():
        return ziel
    if offline:
        raise NichtVerfuegbar(f"{name} liegt nicht im Cache ({ziel}) und offline ist gesetzt.")
    try:
        with urllib.request.urlopen(url, timeout=60) as antwort:
            daten = antwort.read()
    except OSError as e:
        raise NichtVerfuegbar(f"Download fehlgeschlagen: {url} ({e}). Offline: {umgebung} setzen.") from e
    if hashlib.sha256(daten).hexdigest() != sha256:
        raise NichtVerfuegbar(f"Prüfsumme stimmt nicht für {url}")
    ziel.parent.mkdir(parents=True, exist_ok=True)
    _entpacken(daten, ziel)
    return ziel


def konfiguration(offline: bool = False) -> Path:
    return bereitstellen(KONFIG_URL, KONFIG_SHA256, KONFIG_VERSION, "ERECHNUNG_KOSIT_KONFIG", offline)


def visualisierung(offline: bool = False) -> Path:
    return bereitstellen(VISUALISIERUNG_URL, VISUALISIERUNG_SHA256, VISUALISIERUNG_VERSION,
                         "ERECHNUNG_KOSIT_VISUALISIERUNG", offline)


# saxonche läuft in einem GraalVM-Isolate, das an den erzeugenden Thread gebunden ist.
# Alle Saxon-Aufrufe laufen deshalb auf genau einem Thread, auch wenn der Aufrufer
# (z.B. ein MCP-Server) Worker-Threads benutzt. Beim Beenden gibt derselbe Thread
# die Saxon-Objekte frei, sonst bricht das Isolate beim Herunterfahren ab.
class _SaxonThread:
    def __init__(self):
        self._auftraege: queue.Queue = queue.Queue()
        self._thread: threading.Thread | None = None
        self._sperre = threading.Lock()

    def _schleife(self):
        while True:
            auftrag = self._auftraege.get()
            if auftrag is None:
                _stylesheet.cache_clear()
                _saxon.cache_clear()
                gc.collect()
                return
            funktion, args, kwargs, ergebnis = auftrag
            try:
                ergebnis.set_result(funktion(*args, **kwargs))
            except BaseException as e:  # noqa: BLE001 - Fehler an den Aufrufer weiterreichen
                ergebnis.set_exception(e)

    def ausfuehren(self, funktion, *args, **kwargs):
        if self._thread is not None and threading.current_thread() is self._thread:
            return funktion(*args, **kwargs)
        with self._sperre:
            if self._thread is None:
                self._thread = threading.Thread(target=self._schleife, name="saxon", daemon=True)
                self._thread.start()
                threading._register_atexit(self.beenden)  # vor dem Aufräumen des Interpreters
        ergebnis: Future = Future()
        self._auftraege.put((funktion, args, kwargs, ergebnis))
        return ergebnis.result()

    def beenden(self):
        if self._thread is not None and self._thread.is_alive():
            self._auftraege.put(None)
            self._thread.join(timeout=10)


_SAXON = _SaxonThread()


def _im_saxon_thread(funktion, *args, **kwargs):
    return _SAXON.ausfuehren(funktion, *args, **kwargs)


@lru_cache(maxsize=1)
def _saxon():
    try:
        from saxonche import PySaxonProcessor
    except ImportError as e:
        raise NichtVerfuegbar("saxonche fehlt: pip install 'e-rechnung[offiziell]'") from e
    return PySaxonProcessor(license=False)


@lru_cache(maxsize=32)
def _stylesheet(pfad: str):
    xslt = _saxon().new_xslt30_processor()
    return xslt.compile_stylesheet(stylesheet_file=pfad)


@lru_cache(maxsize=8)
def _schema(pfad: str) -> etree.XMLSchema:
    return etree.XMLSchema(etree.parse(pfad))


@lru_cache(maxsize=2)
def szenarien(ordner: str) -> list[Szenario]:
    baum = etree.parse(str(Path(ordner) / "scenarios.xml"))
    ns = {"s": NS_SCENARIO}
    liste = []
    for sz in baum.iterfind("s:scenario", ns):
        namespaces = {n.get("prefix"): n.text.strip() for n in sz.iterfind("s:namespace", ns)}
        xsd = sz.findtext("s:validateWithXmlSchema/s:resource/s:location", namespaces=ns).strip()
        schematron = [(r.findtext("s:name", namespaces=ns).strip(), r.findtext("s:location", namespaces=ns).strip())
                      for r in sz.iterfind("s:validateWithSchematron/s:resource", ns)]
        stufen = {c.text.strip(): c.get("level") for c in sz.iterfind("s:createReport/s:customLevel", ns)}
        liste.append(Szenario(sz.findtext("s:name", namespaces=ns).strip(), sz.findtext("s:match", namespaces=ns).strip(),
                              namespaces, xsd, schematron, stufen))
    return liste


def _passt(sz: Szenario, xml_text: str) -> bool:
    saxon = _saxon()
    knoten = saxon.parse_xml(xml_text=xml_text)
    xp = saxon.new_xpath_processor()
    for prefix, uri in sz.namespaces.items():
        xp.declare_namespace(prefix, uri)
    xp.set_context(xdm_item=knoten)
    return bool(xp.effective_boolean_value(sz.match))


def _ersatzszenario(alle: list[Szenario], wurzel: etree._Element) -> tuple[Szenario | None, str]:
    """ZUGFeRD BASIC oder EXTENDED: kein eigenes KoSIT-Szenario, aber EN 16931 als Kern."""
    if wurzel.tag.endswith("CrossIndustryInvoice"):
        gid = wurzel.findtext(".//{*}GuidelineSpecifiedDocumentContextParameter/{*}ID") or ""
        name = "EN16931 (CII)"
    elif wurzel.tag.endswith("Invoice"):
        gid = wurzel.findtext("{*}CustomizationID") or ""
        name = "EN16931 (UBL Invoice)"
    elif wurzel.tag.endswith("CreditNote"):
        gid = wurzel.findtext("{*}CustomizationID") or ""
        name = "EN16931 (UBL CreditNote)"
    else:
        return None, ""
    if not gid.strip().startswith("urn:cen.eu:en16931:2017"):
        return None, ""
    for sz in alle:
        if sz.name == name:
            return sz, (f"Für die Spezifikation {gid.strip()} hat die KoSIT kein eigenes Szenario. "
                        f"Geprüft wurde der Kern nach EN 16931. Profilregeln von ZUGFeRD prüft z.B. Mustang.")
    return None, ""


def validieren(xml: bytes, offline: bool = False) -> Bericht:
    """Prüft ein Rechnungs-XML wie der KoSIT-Validator."""
    ordner = konfiguration(offline)
    return _im_saxon_thread(_validieren, xml, ordner)


def _validieren(xml: bytes, ordner: Path) -> Bericht:
    alle = szenarien(str(ordner))
    try:
        wurzel = etree.fromstring(xml, etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=False))
    except etree.XMLSyntaxError as e:
        return Bericht("kein Szenario", False, [Befund("error", "XML", f"Kein wohlgeformtes XML: {e}")])
    xml_text = etree.tostring(wurzel, encoding="unicode")

    szenario = next((sz for sz in alle if _passt(sz, xml_text)), None)
    hinweis = ""
    if szenario is None:
        szenario, hinweis = _ersatzszenario(alle, wurzel)
    if szenario is None:
        return Bericht("kein Szenario", False, [Befund(
            "error", "SZENARIO",
            "Kein passendes Prüfszenario. Erwartet wird UBL Invoice/CreditNote oder CII mit einer "
            "Spezifikationskennung (BT-24) für XRechnung 3.0 oder EN 16931.")])

    befunde: list[Befund] = []
    schema = _schema(str(ordner / szenario.xsd))
    if not schema.validate(wurzel):
        for f in schema.error_log:
            befunde.append(Befund("error", "XSD", f.message, f"Zeile {f.line}", "XML-Schema"))
        return Bericht(szenario.name, False, befunde, hinweis)

    knoten = _saxon().parse_xml(xml_text=xml_text)
    for name, ort in szenario.schematron:
        ergebnis = _stylesheet(str(ordner / ort)).transform_to_string(xdm_node=knoten)
        svrl = etree.fromstring(ergebnis.encode("utf-8"))
        for e in svrl.iter(f"{{{SVRL}}}failed-assert", f"{{{SVRL}}}successful-report"):
            code = e.get("id") or ""
            original = STUFEN.get((e.get("flag") or e.get("role") or "error").lower(), "error")
            stufe = szenario.stufen.get(code, original)
            textknoten = e.find(f"{{{SVRL}}}text")
            text = " ".join("".join(textknoten.itertext()).split()) if textknoten is not None else ""
            befunde.append(Befund(stufe, code, text, e.get("location") or "", name, original))

    akzeptiert = not any(b.stufe == "error" for b in befunde)
    return Bericht(szenario.name, akzeptiert, befunde, hinweis)


def html_ansicht(xml: bytes, offline: bool = False) -> str:
    """Offizielle Lesefassung der KoSIT (xrechnung-visualization) als HTML."""
    ordner = visualisierung(offline) / "xsl"
    return _im_saxon_thread(_html_ansicht, xml, ordner)


def _html_ansicht(xml: bytes, ordner: Path) -> str:
    wurzel = etree.fromstring(xml, etree.XMLParser(resolve_entities=False, no_network=True))
    if wurzel.tag.endswith("CrossIndustryInvoice"):
        erster = "cii-xr.xsl"
    elif wurzel.tag.endswith("CreditNote"):
        erster = "ubl-creditnote-xr.xsl"
    else:
        erster = "ubl-invoice-xr.xsl"
    saxon = _saxon()
    knoten = saxon.parse_xml(xml_text=etree.tostring(wurzel, encoding="unicode"))
    zwischen = _stylesheet(str(ordner / erster)).transform_to_string(xdm_node=knoten)
    zk = saxon.parse_xml(xml_text=zwischen)
    return _stylesheet(str(ordner / "xrechnung-html.xsl")).transform_to_string(xdm_node=zk)
