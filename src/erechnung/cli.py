"""Kommandozeile ``erechnung``.

Beispiele::

    erechnung lesen rechnung.xml
    erechnung validieren rechnung.xml rechnung.pdf
    erechnung anzeigen rechnung.xml -o rechnung.html
    erechnung erstellen rechnung.json --format xrechnung-ubl -o rechnung.xml
    erechnung erstellen rechnung.json --format zugferd -o rechnung.pdf
    erechnung datev eingang/*.xml -o EXTF_Buchungsstapel.csv --skr 04
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from importlib import resources
from pathlib import Path

from . import __version__, offiziell
from .codelisten import RECHNUNGSARTEN, STEUERKATEGORIEN, ZAHLUNGSARTEN, text
from .modell import EN16931, XRECHNUNG_3

FORMATE = {
    "xrechnung-ubl": ("ubl", XRECHNUNG_3),
    "xrechnung-cii": ("cii", XRECHNUNG_3),
    "en16931-ubl": ("ubl", "urn:cen.eu:en16931:2017"),
    "en16931-cii": ("cii", "urn:cen.eu:en16931:2017"),
    "zugferd": ("pdf", EN16931),
    "zugferd-xrechnung": ("pdf", XRECHNUNG_3),
}


def _geld(wert, waehrung="EUR") -> str:
    s = f"{wert:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} {waehrung}"


def _ausgabe(text_: str = "", datei=None):
    print(text_, file=datei or sys.stdout)


def befehl_lesen(a) -> int:
    from .lesen import erkennen, lesen

    code = 0
    for pfad in a.dateien:
        try:
            fmt = erkennen(pfad)
            r = lesen(pfad)
        except (ValueError, OSError) as e:
            _ausgabe(f"{pfad}: {e}", sys.stderr)
            code = 1
            continue
        if a.json:
            d = r.als_dict()
            d["_format"] = fmt.__dict__
            _ausgabe(json.dumps(d, ensure_ascii=False, indent=2))
            continue
        v, k = r.verkaeufer, r.kaeufer
        _ausgabe(f"Datei:        {pfad}")
        _ausgabe(f"Format:       {fmt.bezeichnung}" + (f" (eingebettet als {fmt.anhang})" if fmt.anhang else ""))
        _ausgabe(f"E-Rechnung:   {'ja, strukturiert nach EN 16931' if fmt.ist_e_rechnung else 'nein'}")
        _ausgabe(f"Art:          {text(RECHNUNGSARTEN, r.art)}")
        _ausgabe(f"Nummer:       {r.nummer} vom {r.datum:%d.%m.%Y}" if r.datum else f"Nummer:       {r.nummer}")
        kennung = f", USt-IdNr. {v.ust_id}" if v.ust_id else (f", Steuernummer {v.steuernummer}" if v.steuernummer else "")
        _ausgabe(f"Verkäufer:    {v.name}, {v.adresse.plz} {v.adresse.ort}{kennung}")
        _ausgabe(f"Käufer:       {k.name}, {k.adresse.plz} {k.adresse.ort}")
        if r.leitweg_id:
            _ausgabe(f"Käuferref.:   {r.leitweg_id}")
        _ausgabe(f"Positionen:   {len(r.positionen)}")
        for p in r.positionen[: a.positionen]:
            _ausgabe(f"  {p.id:>4}  {p.menge.normalize():>8} {p.einheit:<4} {p.name[:46]:<46} {_geld(p.nettobetrag or 0, r.waehrung):>16}")
        if len(r.positionen) > a.positionen:
            _ausgabe(f"  ... {len(r.positionen) - a.positionen} weitere")
        for st in r.steuern:
            satz = f"{st.satz.normalize()} %" if st.satz is not None else ""
            _ausgabe(f"USt:          {text(STEUERKATEGORIEN, st.kategorie)} {satz}: {_geld(st.betrag, r.waehrung)} auf {_geld(st.basis, r.waehrung)}")
        _ausgabe(f"Netto:        {_geld(r.summen.netto, r.waehrung)}")
        _ausgabe(f"Brutto:       {_geld(r.summen.brutto, r.waehrung)}")
        _ausgabe(f"Zahlbetrag:   {_geld(r.summen.zahlbetrag, r.waehrung)}" + (f", fällig {r.faellig:%d.%m.%Y}" if r.faellig else ""))
        if r.zahlung.art:
            _ausgabe(f"Zahlung:      {text(ZAHLUNGSARTEN, r.zahlung.art)} {r.zahlung.iban}".rstrip())
        if len(a.dateien) > 1:
            _ausgabe()
    return code


def _befund_zeile(b) -> str:
    stufe = {"error": "FEHLER ", "warning": "WARNUNG", "information": "INFO   "}.get(b.stufe, b.stufe)
    return f"  {stufe} {b.code}: {b.text}"


def befehl_validieren(a) -> int:
    from .validieren import validieren

    gesamt = 0
    ergebnisse = []
    for pfad in a.dateien:
        e = validieren(pfad, offiziell_pruefen=not a.ohne_offiziell, offline=a.offline)
        ergebnisse.append(e)
        gespeichert = None
        if a.bericht:
            from .validieren import bericht_speichern

            gespeichert = bericht_speichern(e, Path(pfad).read_bytes(), a.bericht)
        if e.offiziell is not None:
            ok = e.offiziell.akzeptiert and not (a.streng and e.offiziell.warnungen)
        elif a.ohne_offiziell:
            ok = e.vorpruefung_ok
        else:
            ok = False
            gesamt = max(gesamt, 2)
        if not ok:
            gesamt = max(gesamt, 1)
        if a.json:
            continue
        fmt = e.format.bezeichnung if e.format else "unbekannt"
        _ausgabe(f"{pfad}: {fmt}")
        if e.offiziell is not None:
            o = e.offiziell
            urteil = "GÜLTIG" if o.akzeptiert else "UNGÜLTIG"
            _ausgabe(f"  KoSIT-Regeln ({o.konfiguration}): {urteil}, Szenario {o.szenario}, "
                     f"{len(o.fehler)} Fehler, {len(o.warnungen)} Warnungen")
            if o.hinweis:
                _ausgabe(f"  Hinweis: {o.hinweis}")
            for b in o.befunde:
                if b.stufe != "information" or a.alle:
                    _ausgabe(_befund_zeile(b))
        elif e.offiziell_fehler:
            _ausgabe(f"  Offizielle Prüfung nicht möglich: {e.offiziell_fehler}")
        eigene = [b for b in e.vorpruefung if b.stufe != "information" or a.alle]
        if eigene:
            _ausgabe("  Vorprüfung (Erklärungen, nicht maßgeblich):")
            for b in eigene:
                _ausgabe(_befund_zeile(b))
        elif e.offiziell is None:
            _ausgabe("  Vorprüfung ohne Befund.")
        if gespeichert:
            _ausgabe(f"  Prüfbericht: {gespeichert}")
    if a.json:
        daten = [e.als_dict() for e in ergebnisse]
        _ausgabe(json.dumps(daten if len(daten) > 1 else daten[0], ensure_ascii=False, indent=2))
    return gesamt


def befehl_anzeigen(a) -> int:
    from .anzeigen import html
    from .lesen import erkennen, lesen, xml_aus_eingabe

    fmt = erkennen(a.datei)
    if a.offiziell:
        xml, _, _ = xml_aus_eingabe(a.datei)
        inhalt = offiziell.html_ansicht(xml, offline=a.offline)
    else:
        inhalt = html(lesen(a.datei), fmt.ist_e_rechnung, fmt.bezeichnung)
    ziel = Path(a.ausgabe) if a.ausgabe else Path(a.datei).with_suffix(".html")
    if str(ziel) == "-":
        sys.stdout.write(inhalt)
    else:
        ziel.write_text(inhalt, encoding="utf-8")
        _ausgabe(f"Ansicht geschrieben: {ziel}")
    return 0


def _erzeugen(r, fmt: str, vorlage: str | None, pdfa: bool) -> tuple[bytes, str]:
    from .codelisten import XRECHNUNG_ARTEN
    from .schreiben_cii import cii
    from .schreiben_ubl import ubl

    if fmt.startswith(("xrechnung", "zugferd-xrechnung")) and r.art not in XRECHNUNG_ARTEN:
        raise ValueError(f"Rechnungsart {r.art} ist in XRechnung nicht erlaubt (BR-DE-17). Erlaubt: "
                         f"{', '.join(sorted(XRECHNUNG_ARTEN))}.")
    syntax, spezifikation = FORMATE[fmt]
    r.spezifikation = spezifikation
    if syntax == "ubl":
        return ubl(r), ".xml"
    xml = cii(r)
    if syntax == "cii":
        return xml, ".xml"
    from .pdf import einbetten

    if vorlage:
        basis = Path(vorlage).read_bytes()
    else:
        from .pdf_layout import pdf as lesefassung

        basis = lesefassung(r)
    return einbetten(basis, xml, pdfa=pdfa), ".pdf"


def befehl_erstellen(a) -> int:
    from .eingabe import Eingabefehler, laden

    try:
        r = laden(a.eingabe)
    except (Eingabefehler, ValueError, OSError) as e:
        _ausgabe(f"Eingabe fehlerhaft: {e}", sys.stderr)
        return 1
    from .validieren import validieren

    try:
        daten, endung = _erzeugen(r, a.format, a.pdf, a.pdfa)
    except ValueError as e:
        _ausgabe(str(e), sys.stderr)
        return 1
    except RuntimeError as e:
        _ausgabe(str(e), sys.stderr)
        return 2
    ziel = Path(a.ausgabe) if a.ausgabe else Path(a.eingabe).with_suffix(endung)
    ziel.write_bytes(daten)
    _ausgabe(f"{ziel}: {a.format}, Rechnung {r.nummer}, Zahlbetrag {_geld(r.summen.zahlbetrag, r.waehrung)}")
    if not a.validieren:
        hinweise = [b for b in validieren(daten, offiziell_pruefen=False).vorpruefung if b.stufe != "information"]
        for b in hinweise:
            _ausgabe(_befund_zeile(b), sys.stderr)
        if any(b.stufe == "error" for b in hinweise):
            _ausgabe("  Nicht mit den KoSIT-Regeln geprüft. Prüfen mit: erechnung validieren " + str(ziel), sys.stderr)
    if a.validieren:
        e = validieren(ziel, offline=a.offline)
        if e.offiziell:
            _ausgabe(f"  KoSIT-Regeln: {'GÜLTIG' if e.offiziell.akzeptiert else 'UNGÜLTIG'} ({e.offiziell.szenario})")
            for b in e.offiziell.befunde:
                if b.stufe != "information":
                    _ausgabe(_befund_zeile(b))
            return 0 if e.offiziell.akzeptiert else 1
        _ausgabe(f"  Offizielle Prüfung nicht möglich: {e.offiziell_fehler}")
        return 2
    return 0


def befehl_leitweg_id(a) -> int:
    from .validieren import LEITWEG_MUSTER, leitweg_id_gueltig, leitweg_pruefziffer

    ok = True
    for wert in a.leitweg_id:
        wert = wert.strip()
        if leitweg_id_gueltig(wert):
            _ausgabe(f"{wert}: gültig")
            continue
        ok = False
        m = LEITWEG_MUSTER.fullmatch(wert)
        if m:
            richtig = "-".join(t for t in (m.group(1), m.group(2)) if t) + "-" + leitweg_pruefziffer(m.group(1), m.group(2) or "")
            _ausgabe(f"{wert}: Prüfziffer falsch, richtig wäre {richtig}")
        elif re.fullmatch(r"\d{2,12}(-[A-Za-z0-9]{1,30})?", wert):
            grob, _, fein = wert.partition("-")
            _ausgabe(f"{wert}: ohne Prüfziffer, vollständig: {wert}-{leitweg_pruefziffer(grob, fein)}")
        else:
            _ausgabe(f"{wert}: kein gültiges Format (Grobadressierung 2-12 Ziffern, optional Feinadressierung "
                     "bis 30 Zeichen, Prüfziffer 2 Ziffern, getrennt durch Bindestriche)")
    return 0 if ok else 1


def befehl_zugferd(a) -> int:
    from .pdf import einbetten

    xml = Path(a.xml).read_bytes()
    daten = einbetten(Path(a.pdf).read_bytes(), xml, pdfa=a.pdfa)
    ziel = Path(a.ausgabe) if a.ausgabe else Path(a.pdf).with_name(Path(a.pdf).stem + "_zugferd.pdf")
    ziel.write_bytes(daten)
    _ausgabe(f"ZUGFeRD-PDF geschrieben: {ziel}")
    return 0


def befehl_extrahieren(a) -> int:
    from .pdf import xml_auslesen

    name, xml = xml_auslesen(a.pdf)
    ziel = Path(a.ausgabe) if a.ausgabe else Path(a.pdf).with_suffix(".xml")
    if str(ziel) == "-":
        sys.stdout.buffer.write(xml)
    else:
        ziel.write_bytes(xml)
        _ausgabe(f"{name} aus {a.pdf} gespeichert als {ziel}")
    return 0


def befehl_datev(a) -> int:
    from .datev import DatevFehler, Einstellungen, stapel
    from .lesen import lesen

    kreditoren = json.loads(Path(a.kreditoren).read_text(encoding="utf-8")) if a.kreditoren else {}
    e = Einstellungen(berater=a.berater, mandant=a.mandant, skr=a.skr, kreditor=a.kreditor,
                      kreditoren=kreditoren, aufwandskonto=a.konto)
    rechnungen = []
    for pfad in a.dateien:
        try:
            rechnungen.append(lesen(pfad))
        except (ValueError, OSError) as fehler:
            _ausgabe(f"{pfad}: übersprungen, {fehler}", sys.stderr)
    try:
        daten, hinweise = stapel(rechnungen, e)
    except DatevFehler as fehler:
        _ausgabe(str(fehler), sys.stderr)
        return 1
    Path(a.ausgabe).write_bytes(daten)
    zeilen = daten.count(b"\r\n") - 2
    _ausgabe(f"{a.ausgabe}: {len(rechnungen)} Rechnungen, {zeilen} Buchungszeilen (EXTF 700, SKR {a.skr})")
    for h in hinweise:
        _ausgabe(f"  Hinweis: {h}")
    return 0


def befehl_beispiele(a) -> int:
    from .eingabe import aus_dict
    from .schreiben_cii import cii
    from .schreiben_ubl import ubl

    ziel = Path(a.ziel)
    ziel.mkdir(parents=True, exist_ok=True)
    quellen = sorted(resources.files("erechnung").joinpath("beispiele").iterdir(), key=lambda p: p.name)
    for q in quellen:
        if not q.name.endswith(".json"):
            continue
        daten = json.loads(q.read_text(encoding="utf-8"))
        stamm = q.name[:-5]
        (ziel / q.name).write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ziel / f"{stamm}_xrechnung_ubl.xml").write_bytes(ubl(aus_dict(daten)))
        (ziel / f"{stamm}_xrechnung_cii.xml").write_bytes(cii(aus_dict(daten)))
        _ausgabe(f"{ziel / stamm}: JSON, XRechnung UBL, XRechnung CII")
    return 0


def befehl_konfiguration(a) -> int:
    pfad = offiziell.konfiguration(offline=a.offline)
    _ausgabe(f"KoSIT-Prüfkonfiguration: {offiziell.KONFIG_VERSION}")
    _ausgabe(f"Ordner: {pfad}")
    if a.visualisierung:
        _ausgabe(f"Visualisierung: {offiziell.visualisierung(offline=a.offline)}")
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="erechnung", description="E-Rechnung: XRechnung und ZUGFeRD lesen, prüfen, erstellen, anzeigen, nach DATEV exportieren.")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    u = p.add_subparsers(dest="befehl", required=True)

    s = u.add_parser("lesen", help="Rechnung lesen und zusammenfassen (XML oder ZUGFeRD-PDF)")
    s.add_argument("dateien", nargs="+")
    s.add_argument("--json", action="store_true", help="vollständiges Modell als JSON")
    s.add_argument("--positionen", type=int, default=20, help="maximal so viele Positionen zeigen")
    s.set_defaults(f=befehl_lesen)

    s = u.add_parser("validieren", aliases=["check", "prüfen"], help="E-Rechnung mit den offiziellen KoSIT-Regeln prüfen, plus Vorprüfung")
    s.add_argument("dateien", nargs="+")
    s.add_argument("--json", action="store_true")
    s.add_argument("--ohne-offiziell", action="store_true", help="nur Vorprüfung, ohne Download und saxonche")
    s.add_argument("--offline", action="store_true", help="nichts herunterladen, nur Cache oder ERECHNUNG_KOSIT_KONFIG")
    s.add_argument("--streng", action="store_true", help="Warnungen zählen als Fehler (Exit-Code 1)")
    s.add_argument("--alle", action="store_true", help="auch Informationen ausgeben")
    s.add_argument("--bericht", metavar="ORDNER", help="Prüfbericht je Datei als JSON ablegen (zum Aufbewahren)")
    s.set_defaults(f=befehl_validieren)

    s = u.add_parser("anzeigen", help="Rechnung als HTML anzeigen (Viewer)")
    s.add_argument("datei")
    s.add_argument("-o", "--ausgabe", help="Zieldatei, - für stdout")
    s.add_argument("--offiziell", action="store_true", help="KoSIT-Visualisierung statt eigener Ansicht")
    s.add_argument("--offline", action="store_true")
    s.set_defaults(f=befehl_anzeigen)

    s = u.add_parser("erstellen", help="E-Rechnung aus JSON oder TOML erzeugen")
    s.add_argument("eingabe")
    s.add_argument("--format", choices=sorted(FORMATE), default="xrechnung-ubl")
    s.add_argument("-o", "--ausgabe")
    s.add_argument("--pdf", help="vorhandenes PDF als Vorlage für ZUGFeRD (sonst einfache Lesefassung über Ghostscript)")
    s.add_argument("--pdfa", action="store_true", help="Vorlage vorher mit Ghostscript nach PDF/A-3b wandeln")
    s.add_argument("--validieren", action="store_true", help="Ergebnis sofort offiziell prüfen")
    s.add_argument("--offline", action="store_true")
    s.set_defaults(f=befehl_erstellen)

    s = u.add_parser("zugferd", help="CII-XML in ein vorhandenes PDF einbetten (PDF zu ZUGFeRD)")
    s.add_argument("xml")
    s.add_argument("--pdf", required=True)
    s.add_argument("-o", "--ausgabe")
    s.add_argument("--pdfa", action="store_true", help="PDF vorher mit Ghostscript nach PDF/A-3b wandeln")
    s.set_defaults(f=befehl_zugferd)

    s = u.add_parser("extrahieren", help="XML aus einem ZUGFeRD-/Factur-X-PDF holen")
    s.add_argument("pdf")
    s.add_argument("-o", "--ausgabe", help="Zieldatei, - für stdout")
    s.set_defaults(f=befehl_extrahieren)

    s = u.add_parser("datev", help="Eingangsrechnungen als DATEV-Buchungsstapel (EXTF) exportieren")
    s.add_argument("dateien", nargs="+")
    s.add_argument("-o", "--ausgabe", default="EXTF_Buchungsstapel.csv")
    s.add_argument("--berater", type=int, default=1001)
    s.add_argument("--mandant", type=int, default=1)
    s.add_argument("--skr", choices=["03", "04"], default="03")
    s.add_argument("--kreditor", type=int, default=70000, help="Sammelkreditor")
    s.add_argument("--kreditoren", help="JSON: USt-IdNr. oder Name -> Kreditorennummer")
    s.add_argument("--konto", type=int, help="Aufwandskonto (Standard SKR03 4980, SKR04 6850)")
    s.set_defaults(f=befehl_datev)

    s = u.add_parser("leitweg-id", help="Leitweg-ID prüfen oder die Prüfziffer berechnen")
    s.add_argument("leitweg_id", nargs="+", help="z. B. 04011000-1234512345-06 oder ohne Prüfziffer 04011000-1234512345")
    s.set_defaults(f=befehl_leitweg_id)

    s = u.add_parser("beispiele", help="Beispielrechnungen (JSON, XRechnung UBL und CII) in einen Ordner schreiben")
    s.add_argument("ziel", nargs="?", default="beispiele")
    s.set_defaults(f=befehl_beispiele)

    s = u.add_parser("konfiguration", help="KoSIT-Prüfregeln laden und Cache-Ordner zeigen")
    s.add_argument("--offline", action="store_true")
    s.add_argument("--visualisierung", action="store_true", help="auch die KoSIT-Visualisierung laden")
    s.set_defaults(f=befehl_konfiguration)
    return p


def main(argv: list[str] | None = None) -> int:
    a = parser().parse_args(argv)
    try:
        return a.f(a)
    except offiziell.NichtVerfuegbar as e:
        _ausgabe(str(e), sys.stderr)
        return 2
    except (ValueError, OSError, RuntimeError) as e:
        _ausgabe(f"Fehler: {e}", sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
