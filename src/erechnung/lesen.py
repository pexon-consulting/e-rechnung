"""E-Rechnungen lesen: XRechnung UBL, XRechnung CII, ZUGFeRD/Factur-X (XML oder PDF).

``lesen(pfad_oder_bytes)`` erkennt das Format selbst und liefert eine
:class:`~erechnung.modell.Rechnung`. Beträge werden übernommen, wie sie in der
Datei stehen, nicht neu berechnet. So sieht man, was der Absender geschickt hat.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from lxml import etree

from .codelisten import KEINE_E_RECHNUNG, ZUGFERD_PROFILE
from .modell import (
    Adresse,
    Kontakt,
    Lieferung,
    NachlassZuschlag,
    Partei,
    Position,
    Rechnung,
    Steuer,
    Summen,
    Zahlung,
)

PARSER = etree.XMLParser(resolve_entities=False, no_network=True, remove_comments=True)


class KeineERechnung(ValueError):
    """Die Datei enthält kein strukturiertes Rechnungs-XML."""


@dataclass
class Format:
    syntax: str  # UBL-Invoice, UBL-CreditNote, CII
    spezifikation: str  # BT-24
    bezeichnung: str  # z.B. "XRechnung 3.0 (UBL)", "ZUGFeRD EN 16931"
    ist_e_rechnung: bool  # strukturiert nach EN 16931 im Sinne von § 14 UStG
    pdf: bool = False
    anhang: str = ""  # Dateiname des eingebetteten XML


def _d(text: str | None) -> Decimal | None:
    if text is None or not text.strip():
        return None
    try:
        return Decimal(text.strip())
    except InvalidOperation:
        return None


def _datum(text: str | None) -> date | None:
    if not text:
        return None
    t = text.strip()
    for muster in ("%Y-%m-%d", "%Y%m%d"):
        try:
            return datetime.strptime(t[:10] if "-" in t else t[:8], muster).date()
        except ValueError:
            continue
    return None


def xml_aus_eingabe(quelle: str | Path | bytes) -> tuple[bytes, bool, str]:
    """XML-Bytes, ob es aus einem PDF kam, und der Anhangname."""
    if isinstance(quelle, (str, Path)):
        daten = Path(quelle).read_bytes()
    else:
        daten = quelle
    if daten[:5] == b"%PDF-":
        from .pdf import xml_auslesen

        name, xml = xml_auslesen(daten)
        return xml, True, name
    return daten, False, ""


def format_erkennen(xml: bytes, pdf: bool = False, anhang: str = "") -> Format:
    try:
        wurzel = etree.fromstring(xml, PARSER)
    except etree.XMLSyntaxError as e:
        raise KeineERechnung(f"Kein wohlgeformtes XML: {e}") from e
    tag = etree.QName(wurzel).localname
    if tag == "CrossIndustryInvoice":
        spez = (wurzel.findtext(".//{*}GuidelineSpecifiedDocumentContextParameter/{*}ID") or "").strip()
        syntax = "CII"
    elif tag in ("Invoice", "CreditNote"):
        spez = (wurzel.findtext("{*}CustomizationID") or "").strip()
        syntax = f"UBL-{tag}"
    else:
        raise KeineERechnung(f"Unbekanntes Wurzelelement {tag}. Erwartet: Invoice, CreditNote oder CrossIndustryInvoice.")

    if "xrechnung" in spez:
        art = "XRechnung " + ("3.0" if "xrechnung_3.0" in spez else spez.rsplit("_", 1)[-1])
        if "extension" in spez:
            art += " Extension"
        bezeichnung = f"{art} ({'CII' if syntax == 'CII' else 'UBL'})"
        if pdf:
            bezeichnung = f"ZUGFeRD-Profil XRECHNUNG, {bezeichnung}"
        return Format(syntax, spez, bezeichnung, True, pdf, anhang)

    profil = ZUGFERD_PROFILE.get(spez)
    if syntax == "CII" and profil:
        ist = profil not in KEINE_E_RECHNUNG
        return Format(syntax, spez, f"{'ZUGFeRD/Factur-X' if pdf else 'CII'} Profil {profil}", ist, pdf, anhang)
    if spez.startswith("urn:cen.eu:en16931:2017"):
        return Format(syntax, spez, f"EN 16931 ({'CII' if syntax == 'CII' else 'UBL'})", True, pdf, anhang)
    return Format(syntax, spez, f"Unbekannte Spezifikation {spez or '(leer)'}", False, pdf, anhang)


# --- UBL -------------------------------------------------------------------

def _t(e, pfad: str) -> str:
    if e is None:
        return ""
    return (e.findtext(pfad) or "").strip()


def _ubl_adresse(e) -> Adresse:
    if e is None:
        return Adresse(land="")
    return Adresse(
        strasse=_t(e, "{*}StreetName"),
        zusatz=_t(e, "{*}AdditionalStreetName"),
        plz=_t(e, "{*}PostalZone"),
        ort=_t(e, "{*}CityName"),
        land=_t(e, "{*}Country/{*}IdentificationCode"),
        region=_t(e, "{*}CountrySubentity"),
    )


def _ubl_partei(e) -> Partei:
    p = e.find("{*}Party") if e is not None else None
    if p is None:
        return Partei(name="")
    ust = steuernr = ""
    for ts in p.iterfind("{*}PartyTaxScheme"):
        if _t(ts, "{*}TaxScheme/{*}ID") == "VAT":
            ust = _t(ts, "{*}CompanyID")
        else:
            steuernr = _t(ts, "{*}CompanyID")
    endpunkt = p.find("{*}EndpointID")
    kennungen = [i for i in p.iterfind("{*}PartyIdentification/{*}ID") if i.get("schemeID") != "SEPA"]
    return Partei(
        name=_t(p, "{*}PartyLegalEntity/{*}RegistrationName") or _t(p, "{*}PartyName/{*}Name"),
        handelsname=_t(p, "{*}PartyName/{*}Name"),
        kennung=(kennungen[0].text or "").strip() if kennungen else "",
        adresse=_ubl_adresse(p.find("{*}PostalAddress")),
        ust_id=ust,
        steuernummer=steuernr,
        register=_t(p, "{*}PartyLegalEntity/{*}CompanyID"),
        rechtliches=_t(p, "{*}PartyLegalEntity/{*}CompanyLegalForm"),
        elektronische_adresse=(endpunkt.text or "").strip() if endpunkt is not None else "",
        elektronische_adresse_schema=endpunkt.get("schemeID", "") if endpunkt is not None else "",
        kontakt=Kontakt(_t(p, "{*}Contact/{*}Name"), _t(p, "{*}Contact/{*}Telephone"), _t(p, "{*}Contact/{*}ElectronicMail")),
    )


def _ubl_nachlass(e, belegebene: bool) -> NachlassZuschlag:
    return NachlassZuschlag(
        betrag=_d(_t(e, "{*}Amount")) or Decimal("0"),
        grund=_t(e, "{*}AllowanceChargeReason"),
        grund_code=_t(e, "{*}AllowanceChargeReasonCode"),
        zuschlag=_t(e, "{*}ChargeIndicator").lower() == "true",
        kategorie=_t(e, "{*}TaxCategory/{*}ID") if belegebene else "",
        satz=_d(_t(e, "{*}TaxCategory/{*}Percent")) if belegebene else None,
        prozent=_d(_t(e, "{*}MultiplierFactorNumeric")),
        basis=_d(_t(e, "{*}BaseAmount")),
    )


def _ubl(w) -> Rechnung:
    gutschrift = etree.QName(w).localname == "CreditNote"
    r = Rechnung(
        nummer=_t(w, "{*}ID"),
        datum=_datum(_t(w, "{*}IssueDate")),
        verkaeufer=_ubl_partei(w.find("{*}AccountingSupplierParty")),
        kaeufer=_ubl_partei(w.find("{*}AccountingCustomerParty")),
        art=_t(w, "{*}CreditNoteTypeCode" if gutschrift else "{*}InvoiceTypeCode"),
        waehrung=_t(w, "{*}DocumentCurrencyCode"),
        faellig=_datum(_t(w, "{*}DueDate") or _t(w, "{*}PaymentMeans/{*}PaymentDueDate")),
        leitweg_id=_t(w, "{*}BuyerReference"),
        bestellnummer=_t(w, "{*}OrderReference/{*}ID"),
        auftragsnummer=_t(w, "{*}OrderReference/{*}SalesOrderID"),
        vertragsnummer=_t(w, "{*}ContractDocumentReference/{*}ID"),
        projekt=_t(w, "{*}ProjectReference/{*}ID"),
        vorgaenger_nummer=_t(w, "{*}BillingReference/{*}InvoiceDocumentReference/{*}ID"),
        vorgaenger_datum=_datum(_t(w, "{*}BillingReference/{*}InvoiceDocumentReference/{*}IssueDate")),
        leistung_von=_datum(_t(w, "{*}InvoicePeriod/{*}StartDate")),
        leistung_bis=_datum(_t(w, "{*}InvoicePeriod/{*}EndDate")),
        notizen=[(n.text or "").strip() for n in w.iterfind("{*}Note")],
        spezifikation=_t(w, "{*}CustomizationID"),
        prozess=_t(w, "{*}ProfileID"),
        syntax="UBL",
    )
    d = w.find("{*}Delivery")
    if d is not None:
        adr = d.find("{*}DeliveryLocation/{*}Address")
        r.lieferung = Lieferung(_t(d, "{*}DeliveryParty/{*}PartyName/{*}Name"),
                                _ubl_adresse(adr) if adr is not None else None,
                                _datum(_t(d, "{*}ActualDeliveryDate")))
    pm = w.find("{*}PaymentMeans")
    glaeubiger = ""
    for i in w.iterfind("{*}AccountingSupplierParty/{*}Party/{*}PartyIdentification/{*}ID"):
        if i.get("schemeID") == "SEPA":
            glaeubiger = (i.text or "").strip()
    r.zahlung = Zahlung(
        art=_t(pm, "{*}PaymentMeansCode"),
        iban=_t(pm, "{*}PayeeFinancialAccount/{*}ID"),
        bic=_t(pm, "{*}PayeeFinancialAccount/{*}FinancialInstitutionBranch/{*}ID"),
        kontoinhaber=_t(pm, "{*}PayeeFinancialAccount/{*}Name"),
        verwendungszweck=_t(pm, "{*}PaymentID"),
        bedingungen=_t(w, "{*}PaymentTerms/{*}Note"),
        mandatsreferenz=_t(pm, "{*}PaymentMandate/{*}ID"),
        zahler_iban=_t(pm, "{*}PaymentMandate/{*}PayerFinancialAccount/{*}ID"),
        glaeubiger_id=glaeubiger,
    )
    r.nachlaesse = [_ubl_nachlass(e, True) for e in w.iterfind("{*}AllowanceCharge")]
    for sub in w.iterfind("{*}TaxTotal/{*}TaxSubtotal"):
        r.steuern.append(Steuer(
            kategorie=_t(sub, "{*}TaxCategory/{*}ID"),
            satz=_d(_t(sub, "{*}TaxCategory/{*}Percent")),
            basis=_d(_t(sub, "{*}TaxableAmount")) or Decimal("0"),
            betrag=_d(_t(sub, "{*}TaxAmount")) or Decimal("0"),
            befreiungsgrund=_t(sub, "{*}TaxCategory/{*}TaxExemptionReason"),
            befreiungsgrund_code=_t(sub, "{*}TaxCategory/{*}TaxExemptionReasonCode"),
        ))
    mt = w.find("{*}LegalMonetaryTotal")
    steuer_gesamt = Decimal("0")
    for tt in w.iterfind("{*}TaxTotal"):
        betrag = tt.find("{*}TaxAmount")
        if betrag is not None and betrag.get("currencyID", r.waehrung) == r.waehrung:
            steuer_gesamt = _d(betrag.text) or Decimal("0")
    r.summen = Summen(
        positionen=_d(_t(mt, "{*}LineExtensionAmount")) or Decimal("0"),
        nachlaesse=_d(_t(mt, "{*}AllowanceTotalAmount")) or Decimal("0"),
        zuschlaege=_d(_t(mt, "{*}ChargeTotalAmount")) or Decimal("0"),
        netto=_d(_t(mt, "{*}TaxExclusiveAmount")) or Decimal("0"),
        steuer=steuer_gesamt,
        brutto=_d(_t(mt, "{*}TaxInclusiveAmount")) or Decimal("0"),
        vorauszahlung=_d(_t(mt, "{*}PrepaidAmount")) or Decimal("0"),
        rundung=_d(_t(mt, "{*}PayableRoundingAmount")) or Decimal("0"),
        zahlbetrag=_d(_t(mt, "{*}PayableAmount")) or Decimal("0"),
    )
    for line in w.iterfind("{*}CreditNoteLine" if gutschrift else "{*}InvoiceLine"):
        menge = line.find("{*}CreditedQuantity" if gutschrift else "{*}InvoicedQuantity")
        r.positionen.append(Position(
            id=_t(line, "{*}ID"),
            name=_t(line, "{*}Item/{*}Name"),
            menge=_d(menge.text if menge is not None else None) or Decimal("0"),
            einheit=menge.get("unitCode", "") if menge is not None else "",
            preis=_d(_t(line, "{*}Price/{*}PriceAmount")) or Decimal("0"),
            basismenge=_d(_t(line, "{*}Price/{*}BaseQuantity")),
            kategorie=_t(line, "{*}Item/{*}ClassifiedTaxCategory/{*}ID"),
            satz=_d(_t(line, "{*}Item/{*}ClassifiedTaxCategory/{*}Percent")),
            beschreibung=_t(line, "{*}Item/{*}Description"),
            artikelnummer=_t(line, "{*}Item/{*}SellersItemIdentification/{*}ID"),
            notiz=_t(line, "{*}Note"),
            bestellposition=_t(line, "{*}OrderLineReference/{*}LineID"),
            zeitraum_von=_datum(_t(line, "{*}InvoicePeriod/{*}StartDate")),
            zeitraum_bis=_datum(_t(line, "{*}InvoicePeriod/{*}EndDate")),
            nachlaesse=[_ubl_nachlass(e, False) for e in line.iterfind("{*}AllowanceCharge")],
            nettobetrag=_d(_t(line, "{*}LineExtensionAmount")),
        ))
    return r


# --- CII -------------------------------------------------------------------

def _cii_datum(e, pfad: str) -> date | None:
    return _datum(_t(e, pfad + "/{*}DateTimeString"))


def _cii_adresse(e) -> Adresse:
    if e is None:
        return Adresse(land="")
    return Adresse(
        strasse=_t(e, "{*}LineOne"),
        zusatz=_t(e, "{*}LineTwo"),
        plz=_t(e, "{*}PostcodeCode"),
        ort=_t(e, "{*}CityName"),
        land=_t(e, "{*}CountryID"),
        region=_t(e, "{*}CountrySubDivisionName"),
    )


def _cii_partei(p) -> Partei:
    if p is None:
        return Partei(name="")
    ust = steuernr = ""
    for reg in p.iterfind("{*}SpecifiedTaxRegistration/{*}ID"):
        if reg.get("schemeID") == "VA":
            ust = (reg.text or "").strip()
        elif reg.get("schemeID") == "FC":
            steuernr = (reg.text or "").strip()
    uri = p.find("{*}URIUniversalCommunication/{*}URIID")
    return Partei(
        name=_t(p, "{*}Name"),
        handelsname=_t(p, "{*}SpecifiedLegalOrganization/{*}TradingBusinessName"),
        kennung=_t(p, "{*}ID") or _t(p, "{*}GlobalID"),
        adresse=_cii_adresse(p.find("{*}PostalTradeAddress")),
        ust_id=ust,
        steuernummer=steuernr,
        register=_t(p, "{*}SpecifiedLegalOrganization/{*}ID"),
        rechtliches=_t(p, "{*}Description"),
        elektronische_adresse=(uri.text or "").strip() if uri is not None else "",
        elektronische_adresse_schema=uri.get("schemeID", "") if uri is not None else "",
        kontakt=Kontakt(
            _t(p, "{*}DefinedTradeContact/{*}PersonName") or _t(p, "{*}DefinedTradeContact/{*}DepartmentName"),
            _t(p, "{*}DefinedTradeContact/{*}TelephoneUniversalCommunication/{*}CompleteNumber"),
            _t(p, "{*}DefinedTradeContact/{*}EmailURIUniversalCommunication/{*}URIID"),
        ),
    )


def _cii_nachlass(e, belegebene: bool) -> NachlassZuschlag:
    return NachlassZuschlag(
        betrag=_d(_t(e, "{*}ActualAmount")) or Decimal("0"),
        grund=_t(e, "{*}Reason"),
        grund_code=_t(e, "{*}ReasonCode"),
        zuschlag=_t(e, "{*}ChargeIndicator/{*}Indicator").lower() == "true",
        kategorie=_t(e, "{*}CategoryTradeTax/{*}CategoryCode") if belegebene else "",
        satz=_d(_t(e, "{*}CategoryTradeTax/{*}RateApplicablePercent")) if belegebene else None,
        prozent=_d(_t(e, "{*}CalculationPercent")),
        basis=_d(_t(e, "{*}BasisAmount")),
    )


def _cii(w) -> Rechnung:
    dok = w.find("{*}ExchangedDocument")
    tx = w.find("{*}SupplyChainTradeTransaction")
    ag = tx.find("{*}ApplicableHeaderTradeAgreement") if tx is not None else None
    lf = tx.find("{*}ApplicableHeaderTradeDelivery") if tx is not None else None
    st = tx.find("{*}ApplicableHeaderTradeSettlement") if tx is not None else None
    pt = st.find("{*}SpecifiedTradePaymentTerms") if st is not None else None
    r = Rechnung(
        nummer=_t(dok, "{*}ID"),
        datum=_cii_datum(dok, "{*}IssueDateTime"),
        verkaeufer=_cii_partei(ag.find("{*}SellerTradeParty") if ag is not None else None),
        kaeufer=_cii_partei(ag.find("{*}BuyerTradeParty") if ag is not None else None),
        art=_t(dok, "{*}TypeCode"),
        waehrung=_t(st, "{*}InvoiceCurrencyCode"),
        faellig=_cii_datum(pt, "{*}DueDateDateTime") if pt is not None else None,
        leitweg_id=_t(ag, "{*}BuyerReference"),
        bestellnummer=_t(ag, "{*}BuyerOrderReferencedDocument/{*}IssuerAssignedID"),
        auftragsnummer=_t(ag, "{*}SellerOrderReferencedDocument/{*}IssuerAssignedID"),
        vertragsnummer=_t(ag, "{*}ContractReferencedDocument/{*}IssuerAssignedID"),
        projekt=_t(ag, "{*}SpecifiedProcuringProject/{*}ID"),
        vorgaenger_nummer=_t(st, "{*}InvoiceReferencedDocument/{*}IssuerAssignedID"),
        vorgaenger_datum=_datum(_t(st, "{*}InvoiceReferencedDocument/{*}FormattedIssueDateTime/{*}DateTimeString")),
        leistung_von=_cii_datum(st, "{*}BillingSpecifiedPeriod/{*}StartDateTime") if st is not None else None,
        leistung_bis=_cii_datum(st, "{*}BillingSpecifiedPeriod/{*}EndDateTime") if st is not None else None,
        notizen=[_t(n, "{*}Content") for n in dok.iterfind("{*}IncludedNote")] if dok is not None else [],
        spezifikation=_t(w, "{*}ExchangedDocumentContext/{*}GuidelineSpecifiedDocumentContextParameter/{*}ID"),
        prozess=_t(w, "{*}ExchangedDocumentContext/{*}BusinessProcessSpecifiedDocumentContextParameter/{*}ID"),
        syntax="CII",
    )
    if lf is not None and len(lf):
        ship = lf.find("{*}ShipToTradeParty")
        adr = ship.find("{*}PostalTradeAddress") if ship is not None else None
        r.lieferung = Lieferung(_t(ship, "{*}Name"), _cii_adresse(adr) if adr is not None else None,
                                _cii_datum(lf, "{*}ActualDeliverySupplyChainEvent/{*}OccurrenceDateTime"))
    pm = st.find("{*}SpecifiedTradeSettlementPaymentMeans") if st is not None else None
    r.zahlung = Zahlung(
        art=_t(pm, "{*}TypeCode"),
        iban=_t(pm, "{*}PayeePartyCreditorFinancialAccount/{*}IBANID"),
        bic=_t(pm, "{*}PayeeSpecifiedCreditorFinancialInstitution/{*}BICID"),
        kontoinhaber=_t(pm, "{*}PayeePartyCreditorFinancialAccount/{*}AccountName"),
        verwendungszweck=_t(st, "{*}PaymentReference"),
        bedingungen=_t(pt, "{*}Description"),
        mandatsreferenz=_t(pt, "{*}DirectDebitMandateID"),
        glaeubiger_id=_t(st, "{*}CreditorReferenceID"),
        zahler_iban=_t(pm, "{*}PayerPartyDebtorFinancialAccount/{*}IBANID"),
    )
    if st is not None:
        r.nachlaesse = [_cii_nachlass(e, True) for e in st.iterfind("{*}SpecifiedTradeAllowanceCharge")]
        for t in st.iterfind("{*}ApplicableTradeTax"):
            r.steuern.append(Steuer(
                kategorie=_t(t, "{*}CategoryCode"),
                satz=_d(_t(t, "{*}RateApplicablePercent")),
                basis=_d(_t(t, "{*}BasisAmount")) or Decimal("0"),
                betrag=_d(_t(t, "{*}CalculatedAmount")) or Decimal("0"),
                befreiungsgrund=_t(t, "{*}ExemptionReason"),
                befreiungsgrund_code=_t(t, "{*}ExemptionReasonCode"),
            ))
        ms = st.find("{*}SpecifiedTradeSettlementHeaderMonetarySummation")
        steuer = Decimal("0")
        for e in (ms.iterfind("{*}TaxTotalAmount") if ms is not None else []):
            if e.get("currencyID", r.waehrung) == r.waehrung:
                steuer = _d(e.text) or Decimal("0")
        r.summen = Summen(
            positionen=_d(_t(ms, "{*}LineTotalAmount")) or Decimal("0"),
            nachlaesse=_d(_t(ms, "{*}AllowanceTotalAmount")) or Decimal("0"),
            zuschlaege=_d(_t(ms, "{*}ChargeTotalAmount")) or Decimal("0"),
            netto=_d(_t(ms, "{*}TaxBasisTotalAmount")) or Decimal("0"),
            steuer=steuer,
            brutto=_d(_t(ms, "{*}GrandTotalAmount")) or Decimal("0"),
            vorauszahlung=_d(_t(ms, "{*}TotalPrepaidAmount")) or Decimal("0"),
            rundung=_d(_t(ms, "{*}RoundingAmount")) or Decimal("0"),
            zahlbetrag=_d(_t(ms, "{*}DuePayableAmount")) or Decimal("0"),
        )
    for li in (tx.iterfind("{*}IncludedSupplyChainTradeLineItem") if tx is not None else []):
        menge = li.find("{*}SpecifiedLineTradeDelivery/{*}BilledQuantity")
        ls = li.find("{*}SpecifiedLineTradeSettlement")
        netto = li.find("{*}SpecifiedLineTradeAgreement/{*}NetPriceProductTradePrice")
        r.positionen.append(Position(
            id=_t(li, "{*}AssociatedDocumentLineDocument/{*}LineID"),
            name=_t(li, "{*}SpecifiedTradeProduct/{*}Name"),
            menge=_d(menge.text if menge is not None else None) or Decimal("0"),
            einheit=menge.get("unitCode", "") if menge is not None else "",
            preis=_d(_t(netto, "{*}ChargeAmount")) or Decimal("0"),
            basismenge=_d(_t(netto, "{*}BasisQuantity")),
            kategorie=_t(ls, "{*}ApplicableTradeTax/{*}CategoryCode"),
            satz=_d(_t(ls, "{*}ApplicableTradeTax/{*}RateApplicablePercent")),
            beschreibung=_t(li, "{*}SpecifiedTradeProduct/{*}Description"),
            artikelnummer=_t(li, "{*}SpecifiedTradeProduct/{*}SellerAssignedID"),
            notiz=_t(li, "{*}AssociatedDocumentLineDocument/{*}IncludedNote/{*}Content"),
            bestellposition=_t(li, "{*}SpecifiedLineTradeAgreement/{*}BuyerOrderReferencedDocument/{*}LineID"),
            zeitraum_von=_cii_datum(ls, "{*}BillingSpecifiedPeriod/{*}StartDateTime") if ls is not None else None,
            zeitraum_bis=_cii_datum(ls, "{*}BillingSpecifiedPeriod/{*}EndDateTime") if ls is not None else None,
            nachlaesse=[_cii_nachlass(e, False) for e in (ls.iterfind("{*}SpecifiedTradeAllowanceCharge") if ls is not None else [])],
            nettobetrag=_d(_t(ls, "{*}SpecifiedTradeSettlementLineMonetarySummation/{*}LineTotalAmount")),
        ))
    return r


def lesen(quelle: str | Path | bytes) -> Rechnung:
    """Liest XRechnung (UBL/CII) oder ZUGFeRD/Factur-X (XML oder PDF)."""
    xml, aus_pdf, anhang = xml_aus_eingabe(quelle)
    fmt = format_erkennen(xml, aus_pdf, anhang)
    wurzel = etree.fromstring(xml, PARSER)
    r = _cii(wurzel) if fmt.syntax == "CII" else _ubl(wurzel)
    r.quelle = fmt.bezeichnung
    return r


def erkennen(quelle: str | Path | bytes) -> Format:
    xml, aus_pdf, anhang = xml_aus_eingabe(quelle)
    return format_erkennen(xml, aus_pdf, anhang)
