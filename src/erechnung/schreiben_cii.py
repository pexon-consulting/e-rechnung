"""XRechnung, EN 16931 und ZUGFeRD-XML in UN/CEFACT CII D16B schreiben.

ZUGFeRD 2.x und Factur-X verwenden genau diese Syntax. Welches Profil gilt,
steht nur in der Guideline-ID (BT-24).
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from lxml import etree

from .modell import Adresse, NachlassZuschlag, Partei, Position, Rechnung
from .rechnen import berechnen, zahlungsbedingungen
from .schreiben_ubl import betrag, zahl

RSM = "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"
RAM = "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"
UDT = "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100"
QDT = "urn:un:unece:uncefact:data:standard:QualifiedDataType:100"


def _e(eltern, ns: str, name: str, text=None, **attr):
    e = etree.SubElement(eltern, f"{{{ns}}}{name}", {k: v for k, v in attr.items() if v})
    if text is not None:
        e.text = str(text)
    return e


def ram(eltern, name: str, text=None, **attr):
    if text == "":
        return None
    return _e(eltern, RAM, name, text, **attr)


def _datum(eltern, name: str, d: date | None):
    if d is None:
        return
    container = ram(eltern, name)
    _e(container, UDT, "DateTimeString", d.strftime("%Y%m%d"), format="102")


def _adresse(eltern, a: Adresse, name: str = "PostalTradeAddress"):
    pa = ram(eltern, name)
    ram(pa, "PostcodeCode", a.plz)
    ram(pa, "LineOne", a.strasse)
    ram(pa, "LineTwo", a.zusatz)
    ram(pa, "CityName", a.ort)
    ram(pa, "CountryID", a.land or "DE")
    ram(pa, "CountrySubDivisionName", a.region)


def _partei(eltern, name: str, p: Partei, verkaeufer: bool):
    tp = ram(eltern, name)
    ram(tp, "ID", p.kennung)
    ram(tp, "Name", p.name)
    if verkaeufer:
        ram(tp, "Description", p.rechtliches)
    if p.register or p.handelsname:
        lo = ram(tp, "SpecifiedLegalOrganization")
        ram(lo, "ID", p.register)
        ram(lo, "TradingBusinessName", p.handelsname)
    k = p.kontakt
    if k.name or k.telefon or k.email:
        c = ram(tp, "DefinedTradeContact")
        ram(c, "PersonName", k.name)
        if k.telefon:
            ram(ram(c, "TelephoneUniversalCommunication"), "CompleteNumber", k.telefon)
        if k.email:
            ram(ram(c, "EmailURIUniversalCommunication"), "URIID", k.email)
    _adresse(tp, p.adresse)
    if p.elektronische_adresse:
        ram(ram(tp, "URIUniversalCommunication"), "URIID", p.elektronische_adresse,
            schemeID=p.elektronische_adresse_schema or "EM")
    if p.ust_id:
        ram(ram(tp, "SpecifiedTaxRegistration"), "ID", p.ust_id, schemeID="VA")
    if verkaeufer and p.steuernummer:
        ram(ram(tp, "SpecifiedTaxRegistration"), "ID", p.steuernummer, schemeID="FC")


def _steuer(eltern, kategorie: str, satz: Decimal | None, basis=None, steuer=None, grund="", code=""):
    t = ram(eltern, "ApplicableTradeTax")
    if steuer is not None:
        ram(t, "CalculatedAmount", betrag(steuer))
    ram(t, "TypeCode", "VAT")
    ram(t, "ExemptionReason", grund)
    if basis is not None:
        ram(t, "BasisAmount", betrag(basis))
    ram(t, "CategoryCode", kategorie)
    ram(t, "ExemptionReasonCode", code)
    if kategorie != "O" and satz is not None:
        ram(t, "RateApplicablePercent", zahl(satz))
    return t


def _nachlass(eltern, nz: NachlassZuschlag, belegebene: bool):
    ac = ram(eltern, "SpecifiedTradeAllowanceCharge")
    _e(ram(ac, "ChargeIndicator"), UDT, "Indicator", "true" if nz.zuschlag else "false")
    if nz.prozent is not None:
        ram(ac, "CalculationPercent", zahl(nz.prozent))
    if nz.basis is not None:
        ram(ac, "BasisAmount", betrag(nz.basis))
    ram(ac, "ActualAmount", betrag(nz.betrag))
    ram(ac, "ReasonCode", nz.grund_code)
    ram(ac, "Reason", nz.grund)
    if belegebene:
        ct = ram(ac, "CategoryTradeTax")
        ram(ct, "TypeCode", "VAT")
        ram(ct, "CategoryCode", nz.kategorie)
        if nz.kategorie != "O" and nz.satz is not None:
            ram(ct, "RateApplicablePercent", zahl(nz.satz))


def _position(eltern, pos: Position):
    li = ram(eltern, "IncludedSupplyChainTradeLineItem")
    doc = ram(li, "AssociatedDocumentLineDocument")
    ram(doc, "LineID", pos.id)
    if pos.notiz:
        ram(ram(doc, "IncludedNote"), "Content", pos.notiz)
    prod = ram(li, "SpecifiedTradeProduct")
    ram(prod, "SellerAssignedID", pos.artikelnummer)
    ram(prod, "Name", pos.name)
    ram(prod, "Description", pos.beschreibung)
    ag = ram(li, "SpecifiedLineTradeAgreement")
    if pos.bestellposition:
        ram(ram(ag, "BuyerOrderReferencedDocument"), "LineID", pos.bestellposition)
    netto = ram(ag, "NetPriceProductTradePrice")
    ram(netto, "ChargeAmount", zahl(pos.preis))
    if pos.basismenge:
        ram(netto, "BasisQuantity", zahl(pos.basismenge), unitCode=pos.einheit)
    ram(ram(li, "SpecifiedLineTradeDelivery"), "BilledQuantity", zahl(pos.menge), unitCode=pos.einheit)
    st = ram(li, "SpecifiedLineTradeSettlement")
    t = ram(st, "ApplicableTradeTax")
    ram(t, "TypeCode", "VAT")
    ram(t, "CategoryCode", pos.kategorie)
    if pos.kategorie != "O" and pos.satz is not None:
        ram(t, "RateApplicablePercent", zahl(pos.satz))
    if pos.zeitraum_von or pos.zeitraum_bis:
        bp = ram(st, "BillingSpecifiedPeriod")
        _datum(bp, "StartDateTime", pos.zeitraum_von)
        _datum(bp, "EndDateTime", pos.zeitraum_bis)
    for nz in pos.nachlaesse:
        _nachlass(st, nz, belegebene=False)
    ram(ram(st, "SpecifiedTradeSettlementLineMonetarySummation"), "LineTotalAmount", betrag(pos.nettobetrag))


def cii(r: Rechnung) -> bytes:
    """Rechnung als CII-XML. Für ZUGFeRD die passende ``r.spezifikation`` setzen."""
    berechnen(r)
    wurzel = etree.Element(f"{{{RSM}}}CrossIndustryInvoice", nsmap={"rsm": RSM, "ram": RAM, "udt": UDT, "qdt": QDT})

    kontext = _e(wurzel, RSM, "ExchangedDocumentContext")
    if r.prozess:
        ram(ram(kontext, "BusinessProcessSpecifiedDocumentContextParameter"), "ID", r.prozess)
    ram(ram(kontext, "GuidelineSpecifiedDocumentContextParameter"), "ID", r.spezifikation)

    dok = _e(wurzel, RSM, "ExchangedDocument")
    ram(dok, "ID", r.nummer)
    ram(dok, "TypeCode", r.art)
    _datum(dok, "IssueDateTime", r.datum)
    for notiz in r.notizen:
        ram(ram(dok, "IncludedNote"), "Content", notiz)

    tx = _e(wurzel, RSM, "SupplyChainTradeTransaction")
    for pos in r.positionen:
        _position(tx, pos)

    ag = ram(tx, "ApplicableHeaderTradeAgreement")
    ram(ag, "BuyerReference", r.leitweg_id)
    _partei(ag, "SellerTradeParty", r.verkaeufer, verkaeufer=True)
    _partei(ag, "BuyerTradeParty", r.kaeufer, verkaeufer=False)
    if r.auftragsnummer:
        ram(ram(ag, "SellerOrderReferencedDocument"), "IssuerAssignedID", r.auftragsnummer)
    if r.bestellnummer:
        ram(ram(ag, "BuyerOrderReferencedDocument"), "IssuerAssignedID", r.bestellnummer)
    if r.vertragsnummer:
        ram(ram(ag, "ContractReferencedDocument"), "IssuerAssignedID", r.vertragsnummer)
    if r.projekt:
        pr = ram(ag, "SpecifiedProcuringProject")
        ram(pr, "ID", r.projekt)
        ram(pr, "Name", "Projekt")

    lief = ram(tx, "ApplicableHeaderTradeDelivery")
    if r.lieferung:
        if r.lieferung.name or r.lieferung.adresse:
            ship = ram(lief, "ShipToTradeParty")
            ram(ship, "Name", r.lieferung.name)
            if r.lieferung.adresse:
                _adresse(ship, r.lieferung.adresse)
        if r.lieferung.datum:
            ev = ram(lief, "ActualDeliverySupplyChainEvent")
            _datum(ev, "OccurrenceDateTime", r.lieferung.datum)

    st = ram(tx, "ApplicableHeaderTradeSettlement")
    z = r.zahlung
    ram(st, "CreditorReferenceID", z.glaeubiger_id)
    ram(st, "PaymentReference", z.verwendungszweck)
    ram(st, "InvoiceCurrencyCode", r.waehrung)
    pm = ram(st, "SpecifiedTradeSettlementPaymentMeans")
    ram(pm, "TypeCode", z.art)
    if z.zahler_iban:
        ram(ram(pm, "PayerPartyDebtorFinancialAccount"), "IBANID", z.zahler_iban)
    if z.iban:
        konto = ram(pm, "PayeePartyCreditorFinancialAccount")
        ram(konto, "IBANID", z.iban)
        ram(konto, "AccountName", z.kontoinhaber)
        if z.bic:
            ram(ram(pm, "PayeeSpecifiedCreditorFinancialInstitution"), "BICID", z.bic)

    for s in r.steuern:
        _steuer(st, s.kategorie, s.satz, basis=s.basis, steuer=s.betrag, grund=s.befreiungsgrund, code=s.befreiungsgrund_code)

    if r.leistung_von or r.leistung_bis:
        bp = ram(st, "BillingSpecifiedPeriod")
        _datum(bp, "StartDateTime", r.leistung_von)
        _datum(bp, "EndDateTime", r.leistung_bis)

    for nz in r.nachlaesse:
        _nachlass(st, nz, belegebene=True)

    bedingungen = zahlungsbedingungen(r)
    if bedingungen or r.faellig or z.mandatsreferenz:
        pt = ram(st, "SpecifiedTradePaymentTerms")
        ram(pt, "Description", bedingungen)
        if r.faellig:
            due = ram(pt, "DueDateDateTime")
            _e(due, UDT, "DateTimeString", r.faellig.strftime("%Y%m%d"), format="102")
        ram(pt, "DirectDebitMandateID", z.mandatsreferenz)

    s = r.summen
    ms = ram(st, "SpecifiedTradeSettlementHeaderMonetarySummation")
    ram(ms, "LineTotalAmount", betrag(s.positionen))
    if s.zuschlaege:
        ram(ms, "ChargeTotalAmount", betrag(s.zuschlaege))
    if s.nachlaesse:
        ram(ms, "AllowanceTotalAmount", betrag(s.nachlaesse))
    ram(ms, "TaxBasisTotalAmount", betrag(s.netto))
    ram(ms, "TaxTotalAmount", betrag(s.steuer), currencyID=r.waehrung)
    ram(ms, "GrandTotalAmount", betrag(s.brutto))
    if s.vorauszahlung:
        ram(ms, "TotalPrepaidAmount", betrag(s.vorauszahlung))
    ram(ms, "DuePayableAmount", betrag(s.zahlbetrag))

    if r.vorgaenger_nummer:
        ref = ram(st, "InvoiceReferencedDocument")
        ram(ref, "IssuerAssignedID", r.vorgaenger_nummer)
        if r.vorgaenger_datum:
            fd = ram(ref, "FormattedIssueDateTime")
            _e(fd, QDT, "DateTimeString", r.vorgaenger_datum.strftime("%Y%m%d"), format="102")

    return etree.tostring(wurzel, xml_declaration=True, encoding="UTF-8", pretty_print=True)
