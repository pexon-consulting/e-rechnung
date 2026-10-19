"""XRechnung bzw. EN 16931 in UBL 2.1 schreiben (Invoice und CreditNote).

Die Reihenfolge der Elemente folgt dem UBL-2.1-Schema. Wer hier etwas
umsortiert, bricht die XSD-Prüfung.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from lxml import etree

from .codelisten import GUTSCHRIFT_ARTEN
from .modell import Adresse, NachlassZuschlag, Partei, Position, Rechnung
from .rechnen import berechnen, zahlungsbedingungen

NS_INVOICE = "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
NS_CREDITNOTE = "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2"
CAC = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
CBC = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"


def zahl(wert: Decimal | int | str) -> str:
    """Decimal ohne Exponent und ohne überflüssige Nullen, z. B. 19, 2.5, 0.125."""
    d = Decimal(wert)
    text = format(d.normalize(), "f")
    return text if text != "-0" else "0"


def betrag(wert: Decimal) -> str:
    return format(Decimal(wert).quantize(Decimal("0.01")), "f")


class _Bau:
    def __init__(self, wurzel: etree._Element, waehrung: str):
        self.wurzel = wurzel
        self.waehrung = waehrung

    def cbc(self, eltern, name: str, text, **attr):
        if text is None or text == "":
            return None
        e = etree.SubElement(eltern, f"{{{CBC}}}{name}", {k: v for k, v in attr.items() if v})
        e.text = text.isoformat() if isinstance(text, date) else str(text)
        return e

    def geld(self, eltern, name: str, wert: Decimal):
        return self.cbc(eltern, name, betrag(wert), currencyID=self.waehrung)

    def cac(self, eltern, name: str):
        return etree.SubElement(eltern, f"{{{CAC}}}{name}")


def _adresse(b: _Bau, eltern, a: Adresse, name: str = "PostalAddress"):
    pa = b.cac(eltern, name)
    b.cbc(pa, "StreetName", a.strasse)
    b.cbc(pa, "AdditionalStreetName", a.zusatz)
    b.cbc(pa, "CityName", a.ort)
    b.cbc(pa, "PostalZone", a.plz)
    b.cbc(pa, "CountrySubentity", a.region)
    land = b.cac(pa, "Country")
    b.cbc(land, "IdentificationCode", a.land or "DE")


def _partei(b: _Bau, eltern, p: Partei, verkaeufer: bool, glaeubiger_id: str = ""):
    party = b.cac(eltern, "Party")
    if p.elektronische_adresse:
        b.cbc(party, "EndpointID", p.elektronische_adresse, schemeID=p.elektronische_adresse_schema or "EM")
    if p.kennung:
        pid = b.cac(party, "PartyIdentification")
        b.cbc(pid, "ID", p.kennung)
    if glaeubiger_id:
        b.cbc(b.cac(party, "PartyIdentification"), "ID", glaeubiger_id, schemeID="SEPA")
    if p.handelsname:
        pn = b.cac(party, "PartyName")
        b.cbc(pn, "Name", p.handelsname)
    _adresse(b, party, p.adresse)
    if p.ust_id:
        ts = b.cac(party, "PartyTaxScheme")
        b.cbc(ts, "CompanyID", p.ust_id)
        b.cbc(b.cac(ts, "TaxScheme"), "ID", "VAT")
    if verkaeufer and p.steuernummer:
        ts = b.cac(party, "PartyTaxScheme")
        b.cbc(ts, "CompanyID", p.steuernummer)
        b.cbc(b.cac(ts, "TaxScheme"), "ID", "FC")
    le = b.cac(party, "PartyLegalEntity")
    b.cbc(le, "RegistrationName", p.name)
    b.cbc(le, "CompanyID", p.register)
    if verkaeufer:
        b.cbc(le, "CompanyLegalForm", p.rechtliches)
    k = p.kontakt
    if k.name or k.telefon or k.email:
        c = b.cac(party, "Contact")
        b.cbc(c, "Name", k.name)
        b.cbc(c, "Telephone", k.telefon)
        b.cbc(c, "ElectronicMail", k.email)


def _steuerkategorie(b: _Bau, eltern, kategorie: str, satz: Decimal | None, name="TaxCategory", grund: str = "", code: str = ""):
    tc = b.cac(eltern, name)
    b.cbc(tc, "ID", kategorie)
    if kategorie != "O" and satz is not None:
        b.cbc(tc, "Percent", zahl(satz))
    b.cbc(tc, "TaxExemptionReasonCode", code)
    b.cbc(tc, "TaxExemptionReason", grund)
    b.cbc(b.cac(tc, "TaxScheme"), "ID", "VAT")


def _nachlass(b: _Bau, eltern, nz: NachlassZuschlag, belegebene: bool):
    ac = b.cac(eltern, "AllowanceCharge")
    b.cbc(ac, "ChargeIndicator", "true" if nz.zuschlag else "false")
    b.cbc(ac, "AllowanceChargeReasonCode", nz.grund_code)
    b.cbc(ac, "AllowanceChargeReason", nz.grund)
    if nz.prozent is not None:
        b.cbc(ac, "MultiplierFactorNumeric", zahl(nz.prozent))
    b.geld(ac, "Amount", nz.betrag)
    if nz.basis is not None:
        b.geld(ac, "BaseAmount", nz.basis)
    if belegebene:
        _steuerkategorie(b, ac, nz.kategorie, nz.satz)


def _position(b: _Bau, eltern, pos: Position, gutschrift: bool):
    line = b.cac(eltern, "CreditNoteLine" if gutschrift else "InvoiceLine")
    b.cbc(line, "ID", pos.id)
    b.cbc(line, "Note", pos.notiz)
    b.cbc(line, "CreditedQuantity" if gutschrift else "InvoicedQuantity", zahl(pos.menge), unitCode=pos.einheit)
    b.geld(line, "LineExtensionAmount", pos.nettobetrag)
    if pos.zeitraum_von or pos.zeitraum_bis:
        ip = b.cac(line, "InvoicePeriod")
        b.cbc(ip, "StartDate", pos.zeitraum_von)
        b.cbc(ip, "EndDate", pos.zeitraum_bis)
    if pos.bestellposition:
        b.cbc(b.cac(line, "OrderLineReference"), "LineID", pos.bestellposition)
    if not gutschrift:
        for nz in pos.nachlaesse:
            _nachlass(b, line, nz, belegebene=False)
    item = b.cac(line, "Item")
    b.cbc(item, "Description", pos.beschreibung)
    b.cbc(item, "Name", pos.name)
    if pos.artikelnummer:
        b.cbc(b.cac(item, "SellersItemIdentification"), "ID", pos.artikelnummer)
    _steuerkategorie(b, item, pos.kategorie, pos.satz, name="ClassifiedTaxCategory")
    preis = b.cac(line, "Price")
    b.cbc(preis, "PriceAmount", zahl(pos.preis), currencyID=b.waehrung)
    if pos.basismenge:
        b.cbc(preis, "BaseQuantity", zahl(pos.basismenge), unitCode=pos.einheit)


def ubl(r: Rechnung) -> bytes:
    """Rechnung als UBL-XML. Minderungen wie 381 werden zur CreditNote."""
    berechnen(r)
    gutschrift = r.art in GUTSCHRIFT_ARTEN
    ns = NS_CREDITNOTE if gutschrift else NS_INVOICE
    wurzel = etree.Element(f"{{{ns}}}{'CreditNote' if gutschrift else 'Invoice'}",
                           nsmap={None: ns, "cac": CAC, "cbc": CBC})
    b = _Bau(wurzel, r.waehrung)

    b.cbc(wurzel, "CustomizationID", r.spezifikation)
    b.cbc(wurzel, "ProfileID", r.prozess)
    b.cbc(wurzel, "ID", r.nummer)
    b.cbc(wurzel, "IssueDate", r.datum)
    if not gutschrift:
        b.cbc(wurzel, "DueDate", r.faellig)
    b.cbc(wurzel, "CreditNoteTypeCode" if gutschrift else "InvoiceTypeCode", r.art)
    for notiz in r.notizen:
        b.cbc(wurzel, "Note", notiz)
    b.cbc(wurzel, "DocumentCurrencyCode", r.waehrung)
    b.cbc(wurzel, "BuyerReference", r.leitweg_id)
    if r.leistung_von or r.leistung_bis:
        ip = b.cac(wurzel, "InvoicePeriod")
        b.cbc(ip, "StartDate", r.leistung_von)
        b.cbc(ip, "EndDate", r.leistung_bis)
    if r.bestellnummer or r.auftragsnummer:
        orf = b.cac(wurzel, "OrderReference")
        b.cbc(orf, "ID", r.bestellnummer or "NA")
        b.cbc(orf, "SalesOrderID", r.auftragsnummer)
    if r.vorgaenger_nummer:
        idr = b.cac(b.cac(wurzel, "BillingReference"), "InvoiceDocumentReference")
        b.cbc(idr, "ID", r.vorgaenger_nummer)
        b.cbc(idr, "IssueDate", r.vorgaenger_datum)
    if r.vertragsnummer:
        b.cbc(b.cac(wurzel, "ContractDocumentReference"), "ID", r.vertragsnummer)
    if r.projekt:
        b.cbc(b.cac(wurzel, "ProjectReference"), "ID", r.projekt)

    _partei(b, b.cac(wurzel, "AccountingSupplierParty"), r.verkaeufer, verkaeufer=True,
           glaeubiger_id=r.zahlung.glaeubiger_id)
    _partei(b, b.cac(wurzel, "AccountingCustomerParty"), r.kaeufer, verkaeufer=False)

    if r.lieferung:
        d = b.cac(wurzel, "Delivery")
        b.cbc(d, "ActualDeliveryDate", r.lieferung.datum)
        if r.lieferung.adresse:
            _adresse(b, b.cac(d, "DeliveryLocation"), r.lieferung.adresse, name="Address")
        if r.lieferung.name:
            b.cbc(b.cac(b.cac(d, "DeliveryParty"), "PartyName"), "Name", r.lieferung.name)

    z = r.zahlung
    pm = b.cac(wurzel, "PaymentMeans")
    b.cbc(pm, "PaymentMeansCode", z.art)
    if gutschrift:
        b.cbc(pm, "PaymentDueDate", r.faellig)
    b.cbc(pm, "PaymentID", z.verwendungszweck)
    if z.iban:
        konto = b.cac(pm, "PayeeFinancialAccount")
        b.cbc(konto, "ID", z.iban)
        b.cbc(konto, "Name", z.kontoinhaber)
        if z.bic:
            b.cbc(b.cac(konto, "FinancialInstitutionBranch"), "ID", z.bic)
    if z.mandatsreferenz or z.zahler_iban:
        mandat = b.cac(pm, "PaymentMandate")
        b.cbc(mandat, "ID", z.mandatsreferenz)
        if z.zahler_iban:
            b.cbc(b.cac(mandat, "PayerFinancialAccount"), "ID", z.zahler_iban)
    bedingungen = zahlungsbedingungen(r)
    if bedingungen:
        b.cbc(b.cac(wurzel, "PaymentTerms"), "Note", bedingungen)

    for nz in r.nachlaesse:
        _nachlass(b, wurzel, nz, belegebene=True)

    tt = b.cac(wurzel, "TaxTotal")
    b.geld(tt, "TaxAmount", r.summen.steuer)
    for s in r.steuern:
        sub = b.cac(tt, "TaxSubtotal")
        b.geld(sub, "TaxableAmount", s.basis)
        b.geld(sub, "TaxAmount", s.betrag)
        _steuerkategorie(b, sub, s.kategorie, s.satz, grund=s.befreiungsgrund, code=s.befreiungsgrund_code)

    s = r.summen
    mt = b.cac(wurzel, "LegalMonetaryTotal")
    b.geld(mt, "LineExtensionAmount", s.positionen)
    b.geld(mt, "TaxExclusiveAmount", s.netto)
    b.geld(mt, "TaxInclusiveAmount", s.brutto)
    if s.nachlaesse:
        b.geld(mt, "AllowanceTotalAmount", s.nachlaesse)
    if s.zuschlaege:
        b.geld(mt, "ChargeTotalAmount", s.zuschlaege)
    if s.vorauszahlung:
        b.geld(mt, "PrepaidAmount", s.vorauszahlung)
    b.geld(mt, "PayableAmount", s.zahlbetrag)

    for pos in r.positionen:
        _position(b, wurzel, pos, gutschrift)

    return etree.tostring(wurzel, xml_declaration=True, encoding="UTF-8", pretty_print=True)
