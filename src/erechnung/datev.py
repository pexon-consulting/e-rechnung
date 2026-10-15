"""Eingangsrechnungen als DATEV-Buchungsstapel (EXTF, Format 700, Kategorie 21, Version 13).

Je Rechnung und Steuersatz entsteht eine Buchungszeile:
Kreditor (Konto) an Aufwandskonto (Gegenkonto), Bruttobetrag, BU-Schlüssel
für die Vorsteuer. Konten und BU-Schlüssel sind Vorschläge und gehören mit
der Steuerberatung abgestimmt. Der Stapel wird in DATEV über
"Stapelverarbeitung" bzw. "Import Buchungsstapel" eingelesen.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal

from .codelisten import GUTSCHRIFT_ARTEN
from .modell import Rechnung

# Die Spaltennamen von DATEV enthalten einen Gedankenstrich (U+2013).
S = "\u2013"

# 125 Spalten des Buchungsstapels, Formatversion 13
SPALTEN = [
    "Umsatz (ohne Soll/Haben-Kz)", "Soll/Haben-Kennzeichen", "WKZ Umsatz", "Kurs", "Basisumsatz", "WKZ Basisumsatz",
    "Konto", "Gegenkonto (ohne BU-Schlüssel)", "BU-Schlüssel", "Belegdatum", "Belegfeld 1", "Belegfeld 2", "Skonto",
    "Buchungstext", "Postensperre", "Diverse Adressnummer", "Geschäftspartnerbank", "Sachverhalt", "Zinssperre",
    "Beleglink",
    *[f"Beleginfo {S} {teil} {i}" for i in range(1, 9) for teil in ("Art", "Inhalt")],
    f"KOST1 {S} Kostenstelle", f"KOST2 {S} Kostenstelle", "Kost Menge", "EU-Land u. USt-IdNr.", "EU-Steuersatz",
    "Abw. Versteuerungsart", "Sachverhalt L+L", "Funktionsergänzung L+L", "BU 49 Hauptfunktionstyp",
    "BU 49 Hauptfunktionsnummer", "BU 49 Funktionsergänzung",
    *[f"Zusatzinformation {S} {teil} {i}" for i in range(1, 21) for teil in ("Art", "Inhalt")],
    "Stück", "Gewicht", "Zahlweise", "Forderungsart", "Veranlagungsjahr", "Zugeordnete Fälligkeit", "Skontotyp",
    "Auftragsnummer", "Buchungstyp", "USt-Schlüssel (Anzahlungen)", "EU-Mitgliedstaat (Anzahlungen)",
    "Sachverhalt L+L (Anzahlungen)", "EU-Steuersatz (Anzahlungen)", "Erlöskonto (Anzahlungen)", "Herkunft-Kz",
    "Leerfeld", "KOST-Datum", "SEPA-Mandatsreferenz", "Skontosperre", "Gesellschaftername", "Beteiligtennummer",
    "Identifikationsnummer", "Zeichnernummer", "Postensperre bis", "Bezeichnung", "Kennzeichen", "Festschreibung",
    "Leistungsdatum", "Datum Zuord.", "Fälligkeit", "Generalumkehr", "Steuersatz", "Land", "Abrechnungsreferent",
    "BVV-Position", "EU-Mitgliedstaat u. UStID (Ursprung)", "EU-Steuersatz (Ursprung)", "Abw. Skontokonto",
]
assert len(SPALTEN) == 125

# Vorschläge für nicht automatische Aufwandskonten
AUFWANDSKONTO = {"03": 4980, "04": 6850}  # Sonstiger Betriebsbedarf
# BU-Schlüssel für Vorsteuer bei nicht automatischen Konten (klassische zweistellige Schlüssel)
BU_SCHLUESSEL = {("S", "19"): "9", ("S", "7"): "8"}

ERLAUBT_BELEGFELD = re.compile(r"[^A-Za-z0-9$&%*+\-/]")


class DatevFehler(ValueError):
    pass


@dataclass
class Einstellungen:
    berater: int = 1001
    mandant: int = 1
    wj_beginn: date | None = None  # Standard: 1.1. des Rechnungsjahres
    skr: str = "03"
    sachkontenlaenge: int = 4
    kreditor: int = 70000  # Sammelkreditor, wenn keine Zuordnung passt
    kreditoren: dict[str, int] = field(default_factory=dict)  # USt-IdNr. oder Name -> Kreditorennummer
    aufwandskonto: int | None = None
    bu_schluessel: dict[tuple[str, str], str] = field(default_factory=lambda: dict(BU_SCHLUESSEL))
    bezeichnung: str = "E-Rechnungen Eingang"
    exportiert_von: str = "e-rechnung"


def _text(wert: str, laenge: int) -> str:
    wert = (wert or "").replace('"', '""')[:laenge]
    return f'"{wert}"' if wert else ""


def _betrag(wert: Decimal) -> str:
    return format(Decimal(wert).quantize(Decimal("0.01")), "f").replace(".", ",")


def _satz(wert: Decimal | None) -> str:
    if wert is None:
        return ""
    return format(Decimal(wert).normalize(), "f")


def kreditor_fuer(r: Rechnung, e: Einstellungen) -> int:
    for schluessel in (r.verkaeufer.ust_id, r.verkaeufer.steuernummer, r.verkaeufer.name):
        if schluessel and schluessel in e.kreditoren:
            return int(e.kreditoren[schluessel])
    return e.kreditor


@dataclass
class Buchung:
    werte: dict[str, str]
    hinweise: list[str] = field(default_factory=list)


def buchungen(r: Rechnung, e: Einstellungen) -> list[Buchung]:
    if r.waehrung and r.waehrung != "EUR":
        raise DatevFehler(f"{r.nummer}: Währung {r.waehrung}. Dieser Export kann nur EUR.")
    gutschrift = r.art in GUTSCHRIFT_ARTEN
    konto = kreditor_fuer(r, e)
    gegenkonto = e.aufwandskonto or AUFWANDSKONTO.get(e.skr, 4980)
    belegfeld = ERLAUBT_BELEGFELD.sub("", r.nummer)[:36]
    liste = []
    for st in r.steuern:
        hinweise = []
        brutto = st.basis + st.betrag
        if brutto == 0:
            continue
        satz = _satz(st.satz) if st.satz is not None else ""
        bu = e.bu_schluessel.get((st.kategorie, satz), "")
        if st.kategorie == "S" and not bu:
            hinweise.append(f"Kein BU-Schlüssel für {satz} %. Bitte zuordnen.")
        if st.kategorie in {"AE", "K"}:
            hinweise.append(f"Kategorie {st.kategorie}: Steuer auf Eingangsseite selbst berechnen (BU-Schlüssel mit Steuerberatung festlegen).")
        soll_haben = "S" if (gutschrift ^ (brutto < 0)) else "H"
        z = {
            "Umsatz (ohne Soll/Haben-Kz)": _betrag(abs(brutto)),
            "Soll/Haben-Kennzeichen": f'"{soll_haben}"',
            "WKZ Umsatz": '"EUR"',
            "Konto": str(konto),
            "Gegenkonto (ohne BU-Schlüssel)": str(gegenkonto),
            "BU-Schlüssel": _text(bu, 4),
            "Belegdatum": r.datum.strftime("%d%m"),
            "Belegfeld 1": _text(belegfeld, 36),
            "Buchungstext": _text(f"{r.verkaeufer.name} {r.nummer}".strip(), 60),
            "EU-Land u. USt-IdNr.": _text(r.verkaeufer.ust_id.replace(" ", "") if st.kategorie in {"K", "AE"} else "", 15),
            f"Beleginfo {S} Art 1": _text("E-Rechnung", 20),
            f"Beleginfo {S} Inhalt 1": _text(r.quelle or r.syntax, 210),
        }
        leistung = (r.lieferung.datum if r.lieferung and r.lieferung.datum else None) or r.leistung_bis
        if leistung:
            z["Leistungsdatum"] = leistung.strftime("%d%m%Y")
        if r.faellig:
            z["Fälligkeit"] = r.faellig.strftime("%d%m%Y")
        if r.zahlung.mandatsreferenz:
            z["SEPA-Mandatsreferenz"] = _text(r.zahlung.mandatsreferenz, 35)
        if satz and st.kategorie == "S":
            z["Steuersatz"] = satz.replace(".", ",")
        liste.append(Buchung(z, hinweise))
    return liste


def stapel(rechnungen: list[Rechnung], e: Einstellungen | None = None, jetzt: datetime | None = None) -> tuple[bytes, list[str]]:
    """Buchungsstapel als Bytes (Windows-1252, CRLF) und Hinweise für die Prüfung."""
    e = e or Einstellungen()
    if not rechnungen:
        raise DatevFehler("Keine Rechnungen übergeben.")
    jahre = {r.datum.year for r in rechnungen}
    wj = e.wj_beginn or date(min(jahre), 1, 1)
    for r in rechnungen:
        if not (wj <= r.datum < date(wj.year + 1, wj.month, wj.day)):
            raise DatevFehler(f"{r.nummer} vom {r.datum} liegt nicht im Wirtschaftsjahr ab {wj}. Pro Wirtschaftsjahr einen Stapel bauen.")
    vom = min(r.datum for r in rechnungen)
    bis = max(r.datum for r in rechnungen)
    jetzt = jetzt or datetime.now()
    kopf = [
        '"EXTF"', "700", "21", '"Buchungsstapel"', "13", jetzt.strftime("%Y%m%d%H%M%S") + f"{jetzt.microsecond // 1000:03d}",
        "", '"RE"', _text(e.exportiert_von, 25), "", str(e.berater), str(e.mandant), wj.strftime("%Y%m%d"),
        str(e.sachkontenlaenge), vom.strftime("%Y%m%d"), bis.strftime("%Y%m%d"), _text(e.bezeichnung, 30), "",
        "1", "0", "0", '"EUR"', "", "", "", "", _text(e.skr, 2), "", "", "", "",
    ]
    zeilen = [";".join(kopf), ";".join(SPALTEN)]
    hinweise: list[str] = []
    for r in rechnungen:
        for b in buchungen(r, e):
            zeilen.append(";".join(b.werte.get(s, "") for s in SPALTEN))
            hinweise += [f"{r.nummer}: {h}" for h in b.hinweise]
        if kreditor_fuer(r, e) == e.kreditor and e.kreditoren:
            hinweise.append(f"{r.nummer}: {r.verkaeufer.name} hat keine eigene Kreditorennummer, Sammelkreditor {e.kreditor}.")
    text = "\r\n".join(zeilen) + "\r\n"
    return text.encode("cp1252", errors="replace"), hinweise
