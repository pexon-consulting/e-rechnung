"""Die Codes, die in deutschen Rechnungen am häufigsten vorkommen, mit deutschem Text.

Die vollständigen Listen pflegt die KoSIT bzw. die CEF (EN 16931 Codelisten).
Hier steht nur, was für Lesen, Anzeigen und Erstellen gebraucht wird.
"""

# UNTDID 1001, BT-3. XRechnung erlaubt nur 326, 380, 381, 384, 389, 875, 876, 877 (BR-DE-17).
RECHNUNGSARTEN = {
    "380": "Rechnung",
    "381": "Rechnungskorrektur mit Minderung (Credit Note)",
    "384": "Korrigierte Rechnung",
    "389": "Gutschrift im Sinne des UStG (Abrechnung durch den Leistungsempfänger)",
    "326": "Teilrechnung",
    "875": "Teilrechnung Bau",
    "876": "Teilschlussrechnung Bau",
    "877": "Schlussrechnung Bau",
}

XRECHNUNG_ARTEN = {"326", "380", "381", "384", "389", "875", "876", "877"}

# In UBL werden diese Arten als CreditNote-Dokument geschrieben.
GUTSCHRIFT_ARTEN = {"381", "261", "262", "296", "308", "396", "420", "458", "532"}

# UNTDID 5305, BT-95/102/118/151
STEUERKATEGORIEN = {
    "S": "Regelsteuersatz oder ermäßigter Satz",
    "Z": "Nullsatz (Umsatzsteuer 0 %)",
    "E": "Steuerbefreit, z. B. § 4 UStG oder Kleinunternehmer § 19 UStG",
    "AE": "Steuerschuldnerschaft des Leistungsempfängers, Reverse Charge § 13b UStG",
    "K": "Innergemeinschaftliche Lieferung oder Leistung",
    "G": "Ausfuhrlieferung außerhalb der EU",
    "O": "Nicht steuerbar",
    "L": "Kanarische Inseln (IGIC)",
    "M": "Ceuta und Melilla (IPSI)",
}

# Kategorien, bei denen BT-120 oder BT-121 Pflicht ist (BR-E-10, BR-AE-10, BR-IC-10, BR-G-10, BR-O-10)
BEFREIUNGSGRUND_PFLICHT = {"E", "AE", "K", "G", "O"}

STANDARD_BEFREIUNGSGRUND = {
    "AE": "Steuerschuldnerschaft des Leistungsempfängers (§ 13b UStG)",
    "K": "Steuerfreie innergemeinschaftliche Lieferung (§ 4 Nr. 1b UStG)",
    "G": "Steuerfreie Ausfuhrlieferung (§ 4 Nr. 1a UStG)",
    "O": "Nicht im Inland steuerbare Leistung",
}

KLEINUNTERNEHMER_GRUND = "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet."

# UNTDID 4461, BT-81
ZAHLUNGSARTEN = {
    "10": "Bargeld",
    "20": "Scheck",
    "30": "Überweisung (ohne SEPA)",
    "31": "Auslandsüberweisung",
    "42": "Zahlung auf Bankkonto",
    "48": "Bankkarte",
    "49": "Lastschrift",
    "54": "Kreditkarte",
    "55": "Debitkarte",
    "57": "Dauerauftrag",
    "58": "SEPA-Überweisung",
    "59": "SEPA-Lastschrift",
    "97": "Verrechnung",
    "ZZZ": "Sonstige",
}

# UNECE Recommendation 20/21, BT-130
EINHEITEN = {
    "C62": "Stück",
    "H87": "Stück",
    "XPP": "Packung",
    "HUR": "Stunde",
    "MIN": "Minute",
    "DAY": "Tag",
    "WEE": "Woche",
    "MON": "Monat",
    "ANN": "Jahr",
    "KGM": "Kilogramm",
    "GRM": "Gramm",
    "TNE": "Tonne",
    "MTR": "Meter",
    "KMT": "Kilometer",
    "MTK": "Quadratmeter",
    "MTQ": "Kubikmeter",
    "LTR": "Liter",
    "KWH": "Kilowattstunde",
    "LS": "Pauschale",
    "SET": "Satz",
    "E48": "Leistungseinheit",
    "P1": "Prozent",
}

# EAS (Electronic Address Scheme), BT-34-1 / BT-49-1
ADRESS_SCHEMATA = {
    "EM": "E-Mail-Adresse",
    "0204": "Leitweg-ID (deutsche öffentliche Auftraggeber)",
    "9930": "Deutsche Umsatzsteuer-Identifikationsnummer",
    "0088": "GLN (Global Location Number)",
    "0060": "DUNS-Nummer",
    "0009": "SIRET (Frankreich)",
}

# ZUGFeRD / Factur-X: Guideline-ID (BT-24) -> Profil
ZUGFERD_PROFILE = {
    "urn:factur-x.eu:1p0:minimum": "MINIMUM",
    "urn:factur-x.eu:1p0:basicwl": "BASIC WL",
    "urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic": "BASIC",
    "urn:cen.eu:en16931:2017": "EN 16931 (COMFORT)",
    "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended": "EXTENDED",
    "urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0": "XRECHNUNG",
}

# MINIMUM und BASIC WL enthalten nicht alle Pflichtangaben einer Rechnung.
KEINE_E_RECHNUNG = {"MINIMUM", "BASIC WL"}


def text(liste: dict[str, str], code: str) -> str:
    """Code mit deutschem Text, z. B. ``58 (SEPA-Überweisung)``."""
    if not code:
        return ""
    beschreibung = liste.get(code)
    return f"{code} ({beschreibung})" if beschreibung else code
