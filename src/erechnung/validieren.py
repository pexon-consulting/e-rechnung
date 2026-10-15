"""Prüfen einer E-Rechnung: schnelle Vorprüfung plus offizielle KoSIT-Regeln.

Die Vorprüfung braucht keinen Download und erklärt die häufigsten Fehler auf
Deutsch (Pflichtangaben nach § 14 Abs. 4 UStG, Rechenfehler, IBAN). Sie
ersetzt die offizielle Prüfung nicht. Maßgeblich ist das Ergebnis der
KoSIT-Regeln in :mod:`erechnung.offiziell`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

from . import offiziell
from .codelisten import BEFREIUNGSGRUND_PFLICHT, EINHEITEN, KEINE_E_RECHNUNG
from .lesen import Format, KeineERechnung, format_erkennen, xml_aus_eingabe
from .lesen import lesen as _lesen
from .modell import Rechnung
from .offiziell import Befund, Bericht
from .rechnen import runden

KLEINBETRAG = Decimal("250")
TOLERANZ = Decimal("0.01")


def iban_gueltig(iban: str) -> bool:
    s = re.sub(r"\s", "", iban).upper()
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{10,30}", s):
        return False
    umgestellt = s[4:] + s[:4]
    zahl = "".join(str(int(c, 36)) for c in umgestellt)
    return int(zahl) % 97 == 1


def _f(liste: list[Befund], stufe: str, code: str, text: str):
    liste.append(Befund(stufe, code, text, quelle="Vorprüfung"))


LEITWEG_MUSTER = re.compile(r"(\d{2,12})(?:-([A-Za-z0-9]{1,30}))?-(\d{2})")


def leitweg_pruefziffer(grob: str, fein: str = "") -> str:
    """Prüfziffer nach Leitweg-ID-Formatspezifikation 2.0.2 (ISO/IEC 7064 Mod 97-10)."""
    zahl = "".join(str(int(z, 36)) for z in (grob + fein).upper()) + "00"
    return f"{98 - int(zahl) % 97:02d}"


def leitweg_id_gueltig(leitweg_id: str) -> bool:
    """Format und Prüfziffer einer Leitweg-ID prüfen, z.B. 04011000-1234512345-06."""
    m = LEITWEG_MUSTER.fullmatch((leitweg_id or "").strip())
    return bool(m) and leitweg_pruefziffer(m.group(1), m.group(2) or "") == m.group(3)


def vorpruefung(r: Rechnung, fmt: Format) -> list[Befund]:
    b: list[Befund] = []
    xrechnung = "xrechnung" in (r.spezifikation or "")

    if not fmt.ist_e_rechnung:
        profil = fmt.bezeichnung
        if any(p in profil for p in KEINE_E_RECHNUNG):
            _f(b, "error", "VP-FORMAT", f"{profil}: Dieses ZUGFeRD-Profil enthält nicht alle Pflichtangaben und gilt "
               "nicht als E-Rechnung nach § 14 UStG. Mindestens Profil BASIC, besser EN 16931 verwenden.")
        else:
            _f(b, "error", "VP-FORMAT", f"{profil}: keine bekannte Spezifikation nach EN 16931.")

    # Pflichtangaben § 14 Abs. 4 UStG
    if not r.nummer:
        _f(b, "error", "VP-14-4-4", "Rechnungsnummer fehlt (BT-1, § 14 Abs. 4 Nr. 4 UStG).")
    if not r.datum:
        _f(b, "error", "VP-14-4-3", "Rechnungsdatum fehlt (BT-2, § 14 Abs. 4 Nr. 3 UStG).")
    for rolle, p in (("Verkäufer", r.verkaeufer), ("Käufer", r.kaeufer)):
        if not p.name:
            _f(b, "error", "VP-14-4-1", f"Name des {rolle}s fehlt (§ 14 Abs. 4 Nr. 1 UStG).")
        if not (p.adresse.ort and p.adresse.plz) and p.adresse.land == "DE":
            _f(b, "error", "VP-14-4-1", f"Anschrift des {rolle}s unvollständig, Ort oder PLZ fehlen (§ 14 Abs. 4 Nr. 1 UStG).")
    v = r.verkaeufer
    if not (v.ust_id or v.steuernummer):
        kleinbetrag = r.summen.brutto and r.summen.brutto <= KLEINBETRAG
        _f(b, "warning" if kleinbetrag else "error", "VP-14-4-2", "Weder USt-IdNr. (BT-31) noch Steuernummer (BT-32) des Verkäufers angegeben "
           "(§ 14 Abs. 4 Nr. 2 UStG)." + (" Bei Kleinbetragsrechnungen bis 250 EUR nicht nötig (§ 33 UStDV)." if kleinbetrag else ""))
    if v.ust_id and v.ust_id.replace(" ", "").upper().startswith("DE") and not re.fullmatch(r"DE\d{9}", v.ust_id.replace(" ", "").upper()):
        _f(b, "warning", "VP-USTID", f"USt-IdNr. {v.ust_id} hat nicht das Format DE + 9 Ziffern.")
    hat_datum = (r.lieferung and r.lieferung.datum) or r.leistung_von or r.leistung_bis or (
        r.positionen and all(p.zeitraum_von or p.zeitraum_bis for p in r.positionen))
    if not hat_datum:
        _f(b, "warning", "VP-14-4-6", "Kein Liefer- oder Leistungsdatum (BT-72, BG-14 oder BG-26). Pflichtangabe nach "
           "§ 14 Abs. 4 Nr. 6 UStG, außer es entspricht dem Rechnungsdatum und das ist vermerkt.")
    if not r.positionen:
        _f(b, "error", "VP-14-4-5", "Keine Rechnungspositionen (BG-25).")
    for p in r.positionen:
        if not p.name:
            _f(b, "error", "VP-14-4-5", f"Position {p.id}: Bezeichnung fehlt (BT-153).")
        if p.einheit and p.einheit not in EINHEITEN and not re.fullmatch(r"[A-Z0-9]{2,3}", p.einheit):
            _f(b, "error", "VP-EINHEIT", f"Position {p.id}: Einheit {p.einheit!r} ist kein UN/ECE-Code (z.B. C62, HUR, DAY).")
    for st in r.steuern:
        if st.kategorie in BEFREIUNGSGRUND_PFLICHT and not (st.befreiungsgrund or st.befreiungsgrund_code):
            _f(b, "error", "VP-14-4-8", f"Steuerkategorie {st.kategorie} ohne Befreiungsgrund (BT-120/121). "
               "Hinweis auf Steuerbefreiung oder Reverse Charge ist Pflicht (§ 14 Abs. 4 Nr. 8, § 14a UStG).")
        if st.kategorie == "AE" and not r.kaeufer.ust_id:
            _f(b, "error", "VP-13B", "Reverse Charge (AE) ohne USt-IdNr. des Käufers (BT-48).")
        if st.kategorie == "K" and not r.kaeufer.ust_id:
            _f(b, "error", "VP-IG", "Innergemeinschaftliche Lieferung (K) ohne USt-IdNr. des Käufers (BT-48).")

    # XRechnung
    if xrechnung:
        if not r.leitweg_id:
            _f(b, "error", "VP-BR-DE-15", "Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.")
        elif (LEITWEG_MUSTER.fullmatch(r.leitweg_id.strip()) or r.kaeufer.elektronische_adresse_schema == "0204") \
                and not leitweg_id_gueltig(r.leitweg_id):
            _f(b, "warning", "VP-LEITWEG", f"Leitweg-ID {r.leitweg_id} hat ein falsches Format oder eine falsche "
               "Prüfziffer (Formatspezifikation 2.0.2). Die Behörde kann die Rechnung dann nicht zuordnen.")
        k = v.kontakt
        if not (k.name and k.telefon and k.email):
            _f(b, "error", "VP-BR-DE-2", "Kontakt des Verkäufers unvollständig: XRechnung verlangt Name, Telefon und E-Mail "
               "(BT-41, BT-42, BT-43).")
        if not v.elektronische_adresse:
            _f(b, "error", "VP-BR-DE-ADR", "Elektronische Adresse des Verkäufers (BT-34) fehlt.")
        if not r.kaeufer.elektronische_adresse:
            _f(b, "error", "VP-BR-DE-ADR", "Elektronische Adresse des Käufers (BT-49) fehlt.")
        if not r.zahlung.art:
            _f(b, "error", "VP-BR-DE-1", "Zahlungsart (BT-81) fehlt.")

    if r.zahlung.iban and not iban_gueltig(r.zahlung.iban):
        _f(b, "warning", "VP-IBAN", f"IBAN {r.zahlung.iban} hat eine falsche Prüfziffer.")
    if r.faellig and r.datum and r.faellig < r.datum:
        _f(b, "warning", "VP-FAELLIG", "Fälligkeitsdatum liegt vor dem Rechnungsdatum.")

    # Rechnen
    s = r.summen
    summe = sum((p.nettobetrag or Decimal("0") for p in r.positionen), Decimal("0"))
    if abs(summe - s.positionen) > TOLERANZ:
        _f(b, "error", "VP-SUMME", f"Summe der Positionen {runden(summe)} weicht von BT-106 {s.positionen} ab.")
    netto = s.positionen - s.nachlaesse + s.zuschlaege
    if abs(netto - s.netto) > TOLERANZ:
        _f(b, "error", "VP-NETTO", f"Nettobetrag BT-109 {s.netto} passt nicht zu Positionen - Nachlässe + Zuschläge = {netto}.")
    steuer = sum((st.betrag for st in r.steuern), Decimal("0"))
    if abs(steuer - s.steuer) > TOLERANZ:
        _f(b, "error", "VP-STEUER", f"Steuersumme BT-110 {s.steuer} passt nicht zur Aufschlüsselung {steuer}.")
    for st in r.steuern:
        if st.satz is not None and abs(runden(st.basis * st.satz / 100) - st.betrag) > TOLERANZ:
            _f(b, "error", "VP-STEUERSATZ", f"{st.kategorie} {st.satz} %: Steuer {st.betrag} auf Basis {st.basis} "
               f"ergibt nicht {runden(st.basis * st.satz / 100)}.")
    if abs(s.netto + s.steuer - s.brutto) > TOLERANZ:
        _f(b, "error", "VP-BRUTTO", f"Bruttobetrag BT-112 {s.brutto} ist nicht Netto + Steuer = {s.netto + s.steuer}.")
    # Die XRechnung-Extension kennt Zahlungen Dritter (BG-DEX-09), die den Zahlbetrag erhöhen.
    if abs(s.brutto - s.vorauszahlung + s.rundung - s.zahlbetrag) > TOLERANZ and "extension" not in fmt.spezifikation:
        _f(b, "error", "VP-ZAHLBETRAG", f"Zahlbetrag BT-115 {s.zahlbetrag} passt nicht zu Brutto - Vorauszahlung + Rundung.")
    return b


@dataclass
class Ergebnis:
    datei: str
    format: Format | None
    vorpruefung: list[Befund] = field(default_factory=list)
    offiziell: Bericht | None = None
    offiziell_fehler: str = ""

    @property
    def gueltig(self) -> bool | None:
        """True/False nach KoSIT. None, wenn die offizielle Prüfung nicht lief."""
        if self.offiziell is None:
            return None
        return self.offiziell.akzeptiert

    @property
    def vorpruefung_ok(self) -> bool:
        return not any(b.stufe == "error" for b in self.vorpruefung)

    def als_dict(self) -> dict:
        return {
            "datei": self.datei,
            "format": self.format.__dict__ if self.format else None,
            "gueltig": self.gueltig,
            "vorpruefung_ok": self.vorpruefung_ok,
            "vorpruefung": [b.als_dict() for b in self.vorpruefung],
            "offiziell": self.offiziell.als_dict() if self.offiziell else None,
            "offiziell_fehler": self.offiziell_fehler,
        }


def bericht_speichern(e: Ergebnis, quelle: bytes, ordner: str | Path) -> Path:
    """Prüfbericht als JSON ablegen, mit Zeitpunkt, Regelversion und SHA-256 der geprüften Datei.

    Das BMF-Schreiben vom 15.10.2025 (Rn. 35a) empfiehlt, das Ergebnis der Validierung aufzubewahren.
    """
    import hashlib
    import json
    from datetime import datetime, timezone

    from . import __version__

    ziel = Path(ordner)
    ziel.mkdir(parents=True, exist_ok=True)
    pruefsumme = hashlib.sha256(quelle).hexdigest()
    daten = {
        "validiert_am": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "werkzeug": f"e-rechnung {__version__}",
        "regeln": offiziell.KONFIG_VERSION,
        "sha256": pruefsumme,
        **e.als_dict(),
    }
    datei = ziel / f"{Path(e.datei).name}.{pruefsumme[:12]}.validierungsbericht.json"
    datei.write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return datei


def validieren(quelle: str | Path | bytes, offiziell_pruefen: bool = True, offline: bool = False) -> Ergebnis:
    name = str(quelle) if isinstance(quelle, (str, Path)) else "(Daten)"
    try:
        xml, aus_pdf, anhang = xml_aus_eingabe(quelle)
        fmt = format_erkennen(xml, aus_pdf, anhang)
    except (KeineERechnung, ValueError) as e:
        return Ergebnis(name, None, [Befund("error", "VP-LESEN", str(e), quelle="Vorprüfung")])
    erg = Ergebnis(name, fmt)
    try:
        erg.vorpruefung = vorpruefung(_lesen(xml), fmt)
    except Exception as e:  # noqa: BLE001 - kaputte Dateien sollen einen Befund ergeben, keinen Absturz
        erg.vorpruefung = [Befund("error", "VP-LESEN", f"Rechnung konnte nicht gelesen werden: {e}", quelle="Vorprüfung")]
    if offiziell_pruefen:
        try:
            erg.offiziell = offiziell.validieren(xml, offline=offline)
        except (offiziell.NichtVerfuegbar, RuntimeError) as e:
            erg.offiziell_fehler = str(e)
    return erg
