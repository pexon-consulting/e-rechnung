"""Ordner beispiele/ aus den eingebauten Beispielen erzeugen.

Je Fall: Eingabe (JSON), XRechnung in UBL und CII, ZUGFeRD-PDF, HTML-Ansicht und das
Ergebnis der offiziellen Prüfung. Dazu ein DATEV-Buchungsstapel über alle Fälle.

    python scripts/beispiele_bauen.py           # neu schreiben
    python scripts/beispiele_bauen.py --check   # nur vergleichen (CI), Exit-Code 1 bei Abweichung

PDF-Dateien enthalten Zeitstempel und werden beim Vergleich nur auf Vorhandensein geprüft.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from importlib import resources
from pathlib import Path

from erechnung import datev, offiziell
from erechnung.anzeigen import html
from erechnung.eingabe import aus_dict
from erechnung.lesen import erkennen, lesen
from erechnung.modell import EN16931
from erechnung.rechnen import berechnen
from erechnung.schreiben_cii import cii
from erechnung.schreiben_ubl import ubl

ZIEL = Path(__file__).resolve().parents[1] / "beispiele"
JETZT = datetime(2026, 10, 15, 12, 0, 0)

FAELLE = {
    "01_standard": ("Standardrechnung", "Dienstleistung mit Leistungszeitraum, 19 % USt, Skonto, Überweisung"),
    "02_gemischte_steuersaetze": ("Gemischte Steuersätze", "7 % und 19 % in einer Rechnung, Nachlass auf Belegebene"),
    "03_gutschrift": ("Minderung (381, kaufmännische Gutschrift)",
                      "Minderung einer früheren Rechnung, in UBL als CreditNote; keine Gutschrift nach "
                      "§ 14 Abs. 2 Satz 5 UStG (das wäre Rechnungsart 389)"),
    "04_rechnungskorrektur": ("Rechnungskorrektur (384)", "Korrektur mit Bezug auf die ursprüngliche Rechnung (BG-3)"),
    "05_reverse_charge_13b": ("Reverse Charge § 13b UStG", "Steuerkategorie AE, Steuerschuldnerschaft des Leistungsempfängers"),
    "06_innergemeinschaftlich": ("Innergemeinschaftliche Lieferung", "Steuerkategorie K, Käufer in Österreich"),
    "07_kleinunternehmer": ("Kleinunternehmer § 19 UStG", "Steuerkategorie E, Steuernummer statt USt-IdNr."),
    "08_b2g_leitweg_id": ("Rechnung an eine Behörde", "Leitweg-ID in BT-10 und als elektronische Adresse (0204)"),
    "09_sepa_lastschrift": ("SEPA-Lastschrift", "Zahlungsart 59 mit Mandatsreferenz und Gläubiger-ID"),
}

# Diese Fälle bekommen zusätzlich ein ZUGFeRD-PDF (Profil EN 16931).
MIT_PDF = {"01_standard", "02_gemischte_steuersaetze", "07_kleinunternehmer"}


def _eingaben() -> dict[str, tuple[str, object]]:
    ergebnis = {}
    for name in FAELLE:
        text = resources.files("erechnung").joinpath("beispiele", f"{name}.json").read_text(encoding="utf-8")
        ergebnis[name] = (text, aus_dict(json.loads(text)))
    return ergebnis


def _validierungsergebnis(xml: bytes) -> str:
    b = offiziell.validieren(xml)
    zeilen = [
        f"Regeln: {offiziell.KONFIG_VERSION}",
        f"Szenario: {b.szenario}",
        f"Ergebnis: {'angenommen' if b.akzeptiert else 'abgelehnt'}",
        f"Fehler: {len(b.fehler)}, Warnungen: {len(b.warnungen)}",
    ]
    zeilen += [f"{x.stufe} {x.code}: {x.text}" for x in b.befunde]
    return "\n".join(zeilen) + "\n"


def bauen(ordner: Path, mit_pdf: bool) -> dict[str, bytes]:
    dateien: dict[str, bytes] = {}
    rechnungen = []
    for name, (text, r) in _eingaben().items():
        xml_ubl, xml_cii = ubl(r), cii(r)
        dateien[f"{name}/eingabe.json"] = text.encode()
        dateien[f"{name}/xrechnung_ubl.xml"] = xml_ubl
        dateien[f"{name}/xrechnung_cii.xml"] = xml_cii
        fmt = erkennen(xml_cii)
        dateien[f"{name}/ansicht.html"] = html(lesen(xml_cii), fmt.ist_e_rechnung, fmt.bezeichnung).encode()
        dateien[f"{name}/validierung_ubl.txt"] = _validierungsergebnis(xml_ubl).encode()
        dateien[f"{name}/validierung_cii.txt"] = _validierungsergebnis(xml_cii).encode()
        if name == "08_b2g_leitweg_id":
            dateien[f"{name}/ansicht_kosit.html"] = offiziell.html_ansicht(xml_ubl).encode()
        if mit_pdf and name in MIT_PDF:
            from erechnung.pdf import einbetten
            from erechnung.pdf_layout import pdf

            r_pdf = aus_dict(json.loads(text))
            r_pdf.spezifikation = EN16931
            berechnen(r_pdf)
            dateien[f"{name}/zugferd_en16931.pdf"] = einbetten(pdf(r_pdf), cii(r_pdf), pdfa=False)
        rechnungen.append(lesen(xml_ubl))
    stapel, _ = datev.stapel(rechnungen, datev.Einstellungen(skr="04"), jetzt=JETZT)
    dateien["datev/EXTF_Buchungsstapel.csv"] = stapel
    dateien["README.md"] = _index().encode()
    return dateien


def _index() -> str:
    zeilen = [
        "# Beispieldateien für XRechnung und ZUGFeRD",
        "",
        "Neun gültige E-Rechnungen zum Herunterladen, von der Standardrechnung bis zur Rechnung an eine",
        "Behörde, jeweils als XRechnung UBL und CII, mit lesbarer HTML-Ansicht und dem Ergebnis der",
        f"offiziellen KoSIT-Prüfregeln (`{offiziell.KONFIG_VERSION}`). Was jeder Fall zeigt, erklärt die",
        "Anleitung [E-Rechnung Beispiel](../docs/anleitungen/e-rechnung-beispiel.md). Erzeugt werden die",
        "Dateien mit `python scripts/beispiele_bauen.py` aus den Eingaben in `src/erechnung/beispiele/`,",
        "die CI prüft, dass sie zum Code passen.",
        "",
        "Firmen, Namen, Anschriften, Telefonnummern (aus den Bereichen der Bundesnetzagentur für Film und",
        "Fernsehen), IBAN (`DE79000000001234567890`), Gläubiger-ID (`DE98ZZZ09999999999`) und",
        "USt-IdNr. sind Testwerte und gehören keiner echten Firma oder Person.",
        "",
        "| Fall | Was er zeigt | Dateien |",
        "| --- | --- | --- |",
    ]
    for name, (titel, text) in FAELLE.items():
        teile = [f"[UBL]({name}/xrechnung_ubl.xml)", f"[CII]({name}/xrechnung_cii.xml)",
                 f"[Ansicht]({name}/ansicht.html)", f"[Eingabe]({name}/eingabe.json)"]
        if name in MIT_PDF:
            teile.append(f"[ZUGFeRD-PDF]({name}/zugferd_en16931.pdf)")
        if name == "08_b2g_leitweg_id":
            teile.append(f"[KoSIT-Ansicht]({name}/ansicht_kosit.html)")
        zeilen.append(f"| {titel} | {text} | {', '.join(teile)} |")
    zeilen += [
        "",
        "Der DATEV-Buchungsstapel über alle Fälle (SKR04, Sammelkreditor 70000) liegt in",
        "[`datev/EXTF_Buchungsstapel.csv`](datev/EXTF_Buchungsstapel.csv).",
        "",
        "Selbst erzeugen:",
        "",
        "```bash",
        "erechnung beispiele ./meine-beispiele",
        "erechnung erstellen ./meine-beispiele/01_standard.json --format zugferd -o rechnung.pdf",
        "```",
        "",
    ]
    return "\n".join(zeilen)


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--check", action="store_true", help="nur vergleichen, nichts schreiben")
    a.add_argument("--ohne-pdf", action="store_true", help="keine PDFs (ohne Ghostscript)")
    args = a.parse_args()
    mit_pdf = not args.ohne_pdf and shutil.which("gs") is not None
    neu = bauen(ZIEL, mit_pdf)

    if args.check:
        abweichungen = []
        for rel, inhalt in neu.items():
            pfad = ZIEL / rel
            if not pfad.exists():
                abweichungen.append(f"fehlt: {rel}")
            elif not rel.endswith(".pdf") and pfad.read_bytes() != inhalt:
                abweichungen.append(f"veraltet: {rel}")
        bekannt = set(neu) | ({rel for rel in (str(p.relative_to(ZIEL)) for p in ZIEL.rglob("*.pdf"))} if not mit_pdf else set())
        abweichungen += [f"überzählig: {p.relative_to(ZIEL)}" for p in ZIEL.rglob("*")
                         if p.is_file() and str(p.relative_to(ZIEL)) not in bekannt]
        for z in abweichungen:
            print(z)
        if abweichungen:
            print("beispiele/ passt nicht zum Code. Neu erzeugen: python scripts/beispiele_bauen.py")
            return 1
        print(f"beispiele/ aktuell ({len(neu)} Dateien)")
        return 0

    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    for rel, inhalt in neu.items():
        pfad = ZIEL / rel
        pfad.parent.mkdir(parents=True, exist_ok=True)
        pfad.write_bytes(inhalt)
    print(f"{len(neu)} Dateien nach {ZIEL} geschrieben")
    return 0


if __name__ == "__main__":
    sys.exit(main())
