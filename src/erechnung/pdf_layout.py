"""Einfache Lesefassung einer Rechnung als PDF/A-3b, gebaut über PostScript und Ghostscript.

Das ist bewusst schlicht: eine Seite pro 25 Positionen, Helvetica, keine
Logos. Wer ein eigenes Layout hat, nimmt dessen PDF als Vorlage und bettet
nur das XML ein (``erechnung zugferd --pdf``).
"""

from __future__ import annotations

import tempfile
from decimal import Decimal
from pathlib import Path

from .codelisten import EINHEITEN, RECHNUNGSARTEN, STEUERKATEGORIEN, ZAHLUNGSARTEN
from .modell import Rechnung
from .rechnen import bedingungen_lesbar, berechnen, zahlungsbedingungen


def _de(betrag: Decimal | None, stellen: int = 2) -> str:
    if betrag is None:
        return ""
    text = f"{Decimal(betrag):,.{stellen}f}"
    return text.replace(",", "X").replace(".", ",").replace("X", ".")


def _menge(wert: Decimal) -> str:
    text = format(Decimal(wert).normalize(), "f")
    return text.replace(".", ",")


def _ps(text: str) -> str:
    roh = text.encode("latin-1", "replace").decode("latin-1")
    return "(" + roh.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") + ")"


class _Seite:
    def __init__(self):
        self.befehle: list[str] = []

    def text(self, x: float, y: float, s: str, groesse: int = 9, fett: bool = False, rechts: bool = False):
        schrift = "/HB" if fett else "/HR"
        self.befehle.append(f"{schrift} {groesse} selectfont")
        if rechts:
            self.befehle.append(f"{_ps(s)} dup stringwidth pop {x} exch sub {y} moveto show")
        else:
            self.befehle.append(f"{x} {y} moveto {_ps(s)} show")

    def linie(self, x1: float, y1: float, x2: float, y2: float):
        self.befehle.append(f"0.5 setlinewidth {x1} {y1} moveto {x2} {y2} lineto stroke")


def postscript(r: Rechnung) -> str:
    berechnen(r) if not r.steuern else None
    seiten: list[_Seite] = []
    s = _Seite()
    seiten.append(s)
    v, k = r.verkaeufer, r.kaeufer
    s.text(50, 800, v.name, 13, fett=True)
    s.text(50, 786, f"{v.adresse.strasse}, {v.adresse.plz} {v.adresse.ort}")
    if v.ust_id or v.steuernummer:
        s.text(50, 774, f"USt-IdNr.: {v.ust_id}" if v.ust_id else f"Steuernummer: {v.steuernummer}")
    s.text(50, 735, v.name + " - " + v.adresse.strasse + " - " + v.adresse.plz + " " + v.adresse.ort, 7)
    y = 720
    for zeile in [k.name, k.adresse.strasse, f"{k.adresse.plz} {k.adresse.ort}", k.adresse.land if k.adresse.land != "DE" else ""]:
        if zeile.strip():
            s.text(50, y, zeile, 10)
            y -= 13
    titel = RECHNUNGSARTEN.get(r.art, "Rechnung").split(" (")[0]
    s.text(50, 640, f"{titel} {r.nummer}", 14, fett=True)
    meta = [("Rechnungsdatum", r.datum.strftime("%d.%m.%Y"))]
    if r.lieferung and r.lieferung.datum:
        meta.append(("Leistungsdatum", r.lieferung.datum.strftime("%d.%m.%Y")))
    if r.leistung_von and r.leistung_bis:
        meta.append(("Leistungszeitraum", f"{r.leistung_von:%d.%m.%Y} - {r.leistung_bis:%d.%m.%Y}"))
    if r.leitweg_id:
        meta.append(("Käuferreferenz", r.leitweg_id))
    if r.bestellnummer:
        meta.append(("Bestellnummer", r.bestellnummer))
    if r.vorgaenger_nummer:
        meta.append(("Bezug auf Rechnung", r.vorgaenger_nummer))
    y = 690
    for name, wert in meta:
        s.text(380, y, name, 8)
        s.text(545, y, wert, 8, rechts=True)
        y -= 11

    y = 610
    def kopf(seite: _Seite, y: float):
        for x, t, rechts in [(50, "Pos.", False), (80, "Bezeichnung", False), (360, "Menge", True), (410, "Einheit", False),
                             (490, "Einzelpreis", True), (545, "Betrag", True)]:
            seite.text(x, y, t, 8, fett=True, rechts=rechts)
        seite.linie(50, y - 4, 545, y - 4)
        return y - 16

    y = kopf(s, y)
    for i, pos in enumerate(r.positionen):
        if y < 150:
            s = _Seite()
            seiten.append(s)
            y = kopf(s, 800)
        s.text(50, y, pos.id, 8)
        s.text(80, y, pos.name[:55], 8)
        s.text(360, y, _menge(pos.menge), 8, rechts=True)
        s.text(410, y, EINHEITEN.get(pos.einheit, pos.einheit), 8)
        s.text(490, y, _de(pos.preis), 8, rechts=True)
        s.text(545, y, _de(pos.nettobetrag), 8, rechts=True)
        y -= 12
        if pos.beschreibung:
            s.text(80, y, pos.beschreibung[:70], 7)
            y -= 11
    s.linie(50, y + 4, 545, y + 4)
    y -= 8
    zeilen = [("Summe Positionen", r.summen.positionen)]
    if r.summen.nachlaesse:
        zeilen.append(("Nachlässe", -r.summen.nachlaesse))
    if r.summen.zuschlaege:
        zeilen.append(("Zuschläge", r.summen.zuschlaege))
    zeilen.append(("Nettobetrag", r.summen.netto))
    for st in r.steuern:
        satz = f" {_menge(st.satz)} %" if st.satz is not None else ""
        zeilen.append((f"USt {st.kategorie}{satz} auf {_de(st.basis)}", st.betrag))
    for name, wert in zeilen:
        s.text(440, y, name, 8, rechts=True)
        s.text(545, y, f"{_de(wert)} {r.waehrung}", 8, rechts=True)
        y -= 11
    s.text(440, y - 2, "Zahlbetrag", 10, fett=True, rechts=True)
    s.text(545, y - 2, f"{_de(r.summen.zahlbetrag)} {r.waehrung}", 10, fett=True, rechts=True)
    y -= 30
    for st in r.steuern:
        if st.befreiungsgrund:
            s.text(50, y, f"{STEUERKATEGORIEN.get(st.kategorie, st.kategorie).split(' (')[0]}: {st.befreiungsgrund}", 8)
            y -= 11
    for notiz in r.notizen:
        s.text(50, y, notiz[:110], 8)
        y -= 11
    z = r.zahlung
    zahlung = ZAHLUNGSARTEN.get(z.art, z.art)
    if z.iban:
        zahlung += f", IBAN {z.iban}"
    if z.mandatsreferenz:
        zahlung += f", Mandat {z.mandatsreferenz}"
    s.text(50, y - 6, f"Zahlung: {zahlung}", 8)
    bedingungen = bedingungen_lesbar(zahlungsbedingungen(r)).replace("\n", ". ")
    if r.faellig:
        bedingungen = f"Fällig am {r.faellig:%d.%m.%Y}. {bedingungen}"
    if bedingungen:
        s.text(50, y - 17, bedingungen[:120], 8)
    s.text(50, 40, "Diese PDF-Datei enthält die Rechnungsdaten zusätzlich als strukturiertes XML (ZUGFeRD).", 7)

    kopfzeilen = [
        "%!PS-Adobe-3.0",
        "%%Pages: " + str(len(seiten)),
        "/reenc { findfont dup length dict begin { 1 index /FID ne { def } { pop pop } ifelse } forall "
        "/Encoding ISOLatin1Encoding 256 array copy dup 45 /hyphen put def currentdict end definefont pop } bind def",
        "/HR /Helvetica reenc /HB /Helvetica-Bold reenc",
    ]
    rumpf = []
    for n, seite in enumerate(seiten, 1):
        rumpf.append(f"%%Page: {n} {n}")
        rumpf.append("<< /PageSize [595 842] >> setpagedevice")
        rumpf.extend(seite.befehle)
        rumpf.append("showpage")
    return "\n".join(kopfzeilen + rumpf) + "\n%%EOF\n"


def pdf(r: Rechnung) -> bytes:
    """Lesefassung als PDF/A-3b. Braucht Ghostscript."""
    from .pdf import ghostscript_pdfa3

    with tempfile.TemporaryDirectory() as tmp:
        ein = Path(tmp) / "rechnung.ps"
        ein.write_text(postscript(r), encoding="latin-1", errors="replace")
        return ghostscript_pdfa3(ein)
