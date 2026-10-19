"""Datenmodell einer Rechnung nach EN 16931.

Die Felder tragen deutsche Namen, im Kommentar steht die Business-Term-Nummer
(BT) bzw. Business-Group (BG) aus der Norm. Beträge sind immer ``Decimal``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any

XRECHNUNG_3 = "urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0"
EN16931 = "urn:cen.eu:en16931:2017"
PEPPOL_BILLING = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"


@dataclass
class Adresse:
    strasse: str = ""  # BT-35 / BT-50
    zusatz: str = ""  # BT-36 / BT-51
    plz: str = ""  # BT-38 / BT-53
    ort: str = ""  # BT-37 / BT-52
    land: str = "DE"  # BT-40 / BT-55, ISO 3166-1 alpha-2
    region: str = ""  # BT-39 / BT-54


@dataclass
class Kontakt:
    name: str = ""  # BT-41 / BT-56
    telefon: str = ""  # BT-42 / BT-57
    email: str = ""  # BT-43 / BT-58


@dataclass
class Partei:
    name: str  # BT-27 / BT-44
    adresse: Adresse = field(default_factory=Adresse)
    handelsname: str = ""  # BT-28 / BT-45
    kennung: str = ""  # BT-29 / BT-46
    ust_id: str = ""  # BT-31 / BT-48
    steuernummer: str = ""  # BT-32
    register: str = ""  # BT-30 / BT-47, z. B. HRB 12345
    rechtliches: str = ""  # BT-33
    elektronische_adresse: str = ""  # BT-34 / BT-49
    elektronische_adresse_schema: str = "EM"  # EAS-Code, EM = E-Mail, 0204 = Leitweg-ID
    kontakt: Kontakt = field(default_factory=Kontakt)


@dataclass
class Lieferung:
    name: str = ""  # BT-70
    adresse: Adresse | None = None  # BG-15
    datum: date | None = None  # BT-72


@dataclass
class Zahlung:
    art: str = "58"  # BT-81, UNTDID 4461: 58 SEPA-Überweisung, 59 SEPA-Lastschrift, 30 Überweisung, 10 bar
    iban: str = ""  # BT-84
    bic: str = ""  # BT-86
    kontoinhaber: str = ""  # BT-85
    verwendungszweck: str = ""  # BT-83
    bedingungen: str = ""  # BT-20, Freitext
    skonto_tage: int | None = None  # XRechnung: #SKONTO#TAGE=..#PROZENT=..# in BT-20
    skonto_prozent: Decimal | None = None
    mandatsreferenz: str = ""  # BT-89
    glaeubiger_id: str = ""  # BT-90
    zahler_iban: str = ""  # BT-91


@dataclass
class NachlassZuschlag:
    """Nachlass (BG-20/BG-27) oder Zuschlag (BG-21/BG-28)."""

    betrag: Decimal
    grund: str = ""  # BT-97 / BT-104 / BT-139 / BT-144
    grund_code: str = ""  # BT-98 / BT-105 (UNTDID 5189 bzw. 7161)
    zuschlag: bool = False
    kategorie: str = "S"  # BT-95 / BT-102, nur auf Belegebene
    satz: Decimal | None = None  # BT-96 / BT-103
    prozent: Decimal | None = None
    basis: Decimal | None = None


@dataclass
class Position:
    id: str  # BT-126
    name: str  # BT-153
    menge: Decimal  # BT-129
    einheit: str  # BT-130, UNECE Rec 20, z. B. C62 Stück, HUR Stunde
    preis: Decimal  # BT-146, Nettopreis
    kategorie: str = "S"  # BT-151, UNTDID 5305
    satz: Decimal | None = Decimal("19")  # BT-152
    beschreibung: str = ""  # BT-154
    artikelnummer: str = ""  # BT-155
    basismenge: Decimal | None = None  # BT-149
    notiz: str = ""  # BT-127
    bestellposition: str = ""  # BT-132
    zeitraum_von: date | None = None  # BT-134
    zeitraum_bis: date | None = None  # BT-135
    nachlaesse: list[NachlassZuschlag] = field(default_factory=list)  # BG-27/BG-28
    nettobetrag: Decimal | None = None  # BT-131, wird berechnet


@dataclass
class Steuer:
    """Eine Zeile der Umsatzsteuer-Aufschlüsselung (BG-23)."""

    kategorie: str  # BT-118
    satz: Decimal | None  # BT-119
    basis: Decimal  # BT-116
    betrag: Decimal  # BT-117
    befreiungsgrund: str = ""  # BT-120
    befreiungsgrund_code: str = ""  # BT-121, VATEX


@dataclass
class Summen:
    positionen: Decimal = Decimal("0")  # BT-106
    nachlaesse: Decimal = Decimal("0")  # BT-107
    zuschlaege: Decimal = Decimal("0")  # BT-108
    netto: Decimal = Decimal("0")  # BT-109
    steuer: Decimal = Decimal("0")  # BT-110
    brutto: Decimal = Decimal("0")  # BT-112
    vorauszahlung: Decimal = Decimal("0")  # BT-113
    rundung: Decimal = Decimal("0")  # BT-114
    zahlbetrag: Decimal = Decimal("0")  # BT-115


@dataclass
class Rechnung:
    nummer: str  # BT-1
    datum: date  # BT-2
    verkaeufer: Partei  # BG-4
    kaeufer: Partei  # BG-7
    positionen: list[Position] = field(default_factory=list)  # BG-25
    art: str = "380"  # BT-3, UNTDID 1001
    waehrung: str = "EUR"  # BT-5
    faellig: date | None = None  # BT-9
    leitweg_id: str = ""  # BT-10 Buyer reference, in XRechnung Pflicht
    bestellnummer: str = ""  # BT-13
    auftragsnummer: str = ""  # BT-14
    vertragsnummer: str = ""  # BT-12
    projekt: str = ""  # BT-11
    vorgaenger_nummer: str = ""  # BT-25
    vorgaenger_datum: date | None = None  # BT-26
    leistung_von: date | None = None  # BT-73
    leistung_bis: date | None = None  # BT-74
    notizen: list[str] = field(default_factory=list)  # BT-22
    lieferung: Lieferung | None = None  # BG-13
    zahlung: Zahlung = field(default_factory=Zahlung)  # BG-16
    nachlaesse: list[NachlassZuschlag] = field(default_factory=list)  # BG-20/BG-21
    steuern: list[Steuer] = field(default_factory=list)  # BG-23, wird berechnet
    befreiungsgruende: dict[str, str] = field(default_factory=dict)  # Kategorie -> BT-120
    summen: Summen = field(default_factory=Summen)  # BG-22
    vorauszahlung: Decimal = Decimal("0")  # BT-113
    spezifikation: str = XRECHNUNG_3  # BT-24
    prozess: str = PEPPOL_BILLING  # BT-23
    # Nur beim Lesen gefüllt:
    syntax: str = ""  # UBL, CII
    quelle: str = ""

    def als_dict(self) -> dict[str, Any]:
        """Für JSON-Ausgabe: Decimal und date werden zu Strings."""
        return _jsonfaehig(asdict(self))


def _jsonfaehig(wert: Any) -> Any:
    if isinstance(wert, dict):
        return {k: _jsonfaehig(v) for k, v in wert.items()}
    if isinstance(wert, list):
        return [_jsonfaehig(v) for v in wert]
    if isinstance(wert, Decimal):
        return format(wert, "f")
    if isinstance(wert, date):
        return wert.isoformat()
    return wert
