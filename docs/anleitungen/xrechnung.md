# XRechnung: Format, Aufbau und Pflichtfelder einfach erklärt

Die XRechnung ist das deutsche XML-Format für E-Rechnungen: eine von der KoSIT herausgegebene Spezialisierung (CIUS) der europäischen Norm EN 16931, aktuell in Version 3.0.2. Eine XRechnung ist eine reine XML-Datei ohne Bildteil, wahlweise in der Syntax UBL 2.1 oder UN/CEFACT CII D16B. Jede Rechnungsangabe steht darin in einem festen, nummerierten Feld (zum Beispiel BT-1 für die Rechnungsnummer), deshalb kann ein Buchhaltungsprogramm sie ohne Abtippen übernehmen. Lesbar wird die Datei erst mit einem Viewer.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Buchhaltung, Geschäftsführung und Entwickler, die das Format verstehen wollen. Die XML-Ausschnitte sind zum Nachschlagen.

## Das Wichtigste in Kürze

- Die XRechnung ist eine CIUS (Core Invoice Usage Specification) der EN 16931: Sie nimmt das europäische Datenmodell und ergänzt deutsche Regeln mit dem Kürzel BR-DE.
- Gültig ist XRechnung 3.0.2; die Hauptversion 3.0 bleibt laut KoSIT mindestens bis 31.07.2027 in Kraft.
- Es gibt zwei gleichwertige Syntaxen: UBL 2.1 (Wurzelelement `Invoice` oder `CreditNote`) und CII D16B (Wurzelelement `CrossIndustryInvoice`).
- Erkennbar ist eine XRechnung an der Kennung `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` in BT-24.
- Pflicht sind unter anderem die Käuferreferenz BT-10, ein Verkäuferkontakt mit Name, Telefon und E-Mail (BT-41 bis BT-43), elektronische Adressen von Verkäufer und Käufer (BT-34, BT-49) und Zahlungsangaben (BG-16).
- XRechnung 4.0 gibt es seit 15.09.2026 nur als Vorversion, die finale Fassung erscheint laut KoSIT voraussichtlich im Frühjahr 2027.

## Was ist eine XRechnung?

Eine XRechnung ist eine Rechnung als strukturierte XML-Datei nach dem Standard XRechnung der KoSIT. Sie ist eine E-Rechnung im Sinne von § 14 Abs. 1 Satz 3 UStG, weil sie "in einem strukturierten elektronischen Format ausgestellt, übermittelt und empfangen wird und eine elektronische Verarbeitung ermöglicht".

Die Grundlage ist die EN 16931. Die Norm legt fest, welche Angaben eine Rechnung haben kann, und gibt jeder Angabe eine Nummer: BT-1 ist die Rechnungsnummer, BT-112 der Bruttobetrag. Eine CIUS schränkt diese Norm für einen Einsatzzweck ein und macht zusätzliche Felder zur Pflicht. Die XRechnung ist die deutsche CIUS. Ihre Zusatzregeln heißen BR-DE-1, BR-DE-2 und so weiter.

Seit Peppol BIS Billing 3.0.18 (ab Februar 2025) sind die XRechnung-Regeln als German National Ruleset in Peppol enthalten. Laut [xeinkauf.de](https://xeinkauf.de/aktuelles/peppol/zusammenhang-xrechnung-peppol/) sind XRechnung 3.0 und Peppol BIS Billing 3.0 innerhalb Deutschlands inhaltlich gleichbedeutend.

Eine XRechnung hat keinen eingebauten Bildteil. Menschen lesen sie mit einem Viewer, der das XML in eine Ansicht umwandelt. Das ist der wichtigste Unterschied zu ZUGFeRD, das XML und PDF in einer Datei verbindet (siehe [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md)).

## XRechnung 3.0: Version, CustomizationID und ProfileID

Jede XRechnung sagt in zwei Feldern, nach welchen Regeln sie gebaut ist. BT-24 (Specification identifier) nennt den Standard, BT-23 (Business process type) den Geschäftsprozess. Beide prüft der Validator.

| Feld | UBL-Element | CII-Element | Wert für XRechnung 3.0 |
| --- | --- | --- | --- |
| BT-24 | `cbc:CustomizationID` | `ram:GuidelineSpecifiedDocumentContextParameter/ram:ID` | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` |
| BT-23 | `cbc:ProfileID` | `ram:BusinessProcessSpecifiedDocumentContextParameter/ram:ID` | `urn:fdc:peppol.eu:2017:poacc:billing:01:1.0` |

Die Kennung `xrechnung_3.0` gilt für alle Unterversionen 3.0.x. Neben der normalen CIUS kennt die Prüfkonfiguration der KoSIT (Fassung 2026-08-31) zwei Varianten:

| Variante | BT-24 |
| --- | --- |
| CIUS XRechnung (Normalfall) | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` |
| Extension XRechnung | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0#conformant#urn:xeinkauf.de:kosit:extension:xrechnung_3.0` |
| XRechnung CVD | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0#compliant#urn:xeinkauf.de:kosit:xrechnung:cvd_0.9` |

BT-23 ist in XRechnung über die Regel PEPPOL-EN16931-R001 ("Business process MUST be provided") Pflicht. Ältere Versionen (XRechnung 1.x und 2.x) nutzten Kennungen der Form `urn:xoev-de:kosit:standard:xrechnung_X.Y`.

Zu den Versionen: Die Hauptversion 3.0 ist seit 01.02.2024 in Kraft (mit 3.0.1), die Version 2.3 seitdem außer Kraft. Die Spezifikation 3.0.2 stammt vom 20.06.2024, das aktuelle Bundle "XRechnung Bundle 3.0.2 Summer 2026 Bugfix" vom 31.08.2026.

## XRechnung Format: UBL oder CII?

Beide Syntaxen tragen denselben Inhalt und sind gleichwertig. Die KoSIT-Prüfkonfiguration enthält eigene Szenarien für XRechnung UBL Invoice, XRechnung UBL CreditNote und XRechnung CII.

| Merkmal | UBL 2.1 | UN/CEFACT CII D16B |
| --- | --- | --- |
| Wurzelelement | `Invoice` oder `CreditNote` | `rsm:CrossIndustryInvoice` |
| Präfixe | `cbc:` für Werte, `cac:` für Gruppen | `ram:`, `rsm:`, `udt:`, `qdt:` |
| Datumsformat | `2026-10-15` | `<udt:DateTimeString format="102">20261015</udt:DateTimeString>` |
| Minderung (381) | eigenes Dokument `CreditNote` | dasselbe Wurzelelement, `ram:TypeCode` 381 |
| Reihenfolge | Kopf, Parteien, Zahlung, Summen, Positionen | Kopf, Positionen, dann Vereinbarung, Lieferung, Abrechnung |
| Beispiel 01 im Repo | 5.644 Byte, 139 Zeilen | 8.066 Byte, 165 Zeilen |
| Grundlage auch für | - | ZUGFeRD und Factur-X |

Welche Syntax Sie nehmen, hängt meist an der Software beim Empfänger. Wer zusätzlich ZUGFeRD erzeugt, hat mit CII in beiden Fällen dieselbe XML-Struktur, weil ZUGFeRD ein CII-XML in ein PDF einbettet.

## Aufbau einer XRechnung: die wichtigsten BT-Felder

Die Tabelle zeigt die Felder der [Standardrechnung](../../beispiele/01_standard/) mit dem Element in beiden Syntaxen. Die Pfade sind gekürzt, die vollständigen Dateien liegen unter [`xrechnung_ubl.xml`](../../beispiele/01_standard/xrechnung_ubl.xml) und [`xrechnung_cii.xml`](../../beispiele/01_standard/xrechnung_cii.xml).

| BT | Bedeutung | UBL 2.1 | CII D16B | Wert im Beispiel |
| --- | --- | --- | --- | --- |
| BT-1 | Rechnungsnummer | `cbc:ID` | `rsm:ExchangedDocument/ram:ID` | RE-2026-0001 |
| BT-2 | Rechnungsdatum | `cbc:IssueDate` | `ram:IssueDateTime/udt:DateTimeString` | 2026-10-15 |
| BT-3 | Rechnungsart | `cbc:InvoiceTypeCode` | `ram:TypeCode` | 380 |
| BT-5 | Währung | `cbc:DocumentCurrencyCode` | `ram:InvoiceCurrencyCode` | EUR |
| BT-9 | Fälligkeitsdatum | `cbc:DueDate` | `ram:SpecifiedTradePaymentTerms/ram:DueDateDateTime` | 2026-11-14 |
| BT-10 | Käuferreferenz (Buyer reference) | `cbc:BuyerReference` | `ram:ApplicableHeaderTradeAgreement/ram:BuyerReference` | BH-2026-0815 |
| BT-13 | Bestellnummer | `cac:OrderReference/cbc:ID` | `ram:BuyerOrderReferencedDocument/ram:IssuerAssignedID` | PO-4711 |
| BT-20 | Zahlungsbedingungen | `cac:PaymentTerms/cbc:Note` | `ram:SpecifiedTradePaymentTerms/ram:Description` | #SKONTO#... |
| BT-27 | Name des Verkäufers | `cac:PartyLegalEntity/cbc:RegistrationName` | `ram:SellerTradeParty/ram:Name` | Nordlicht Beispiel GmbH |
| BT-31 | USt-IdNr. des Verkäufers | `cac:PartyTaxScheme/cbc:CompanyID` (TaxScheme `VAT`) | `ram:SpecifiedTaxRegistration/ram:ID schemeID="VA"` | DE123456789 |
| BT-32 | Steuernummer des Verkäufers | `cac:PartyTaxScheme/cbc:CompanyID` (TaxScheme `FC`) | `ram:SpecifiedTaxRegistration/ram:ID schemeID="FC"` | nur in Beispiel 07 |
| BT-34 | Elektronische Adresse Verkäufer | `cbc:EndpointID schemeID="EM"` | `ram:URIUniversalCommunication/ram:URIID schemeID="EM"` | rechnung@nordlicht.example |
| BT-37 | Ort | `cbc:CityName` | `ram:CityName` | Hamburg |
| BT-38 | Postleitzahl | `cbc:PostalZone` | `ram:PostcodeCode` | 20095 |
| BT-41 | Kontaktname Verkäufer | `cac:Contact/cbc:Name` | `ram:DefinedTradeContact/ram:PersonName` | Erika Mustermann |
| BT-42 | Telefon Verkäufer | `cac:Contact/cbc:Telephone` | `ram:TelephoneUniversalCommunication/ram:CompleteNumber` | +49 40 66969123 |
| BT-43 | E-Mail Verkäufer | `cac:Contact/cbc:ElectronicMail` | `ram:EmailURIUniversalCommunication/ram:URIID` | buchhaltung@nordlicht.example |
| BT-44 | Name des Käufers | `cac:PartyLegalEntity/cbc:RegistrationName` | `ram:BuyerTradeParty/ram:Name` | Beispiel Handel AG |
| BT-49 | Elektronische Adresse Käufer | `cbc:EndpointID schemeID="EM"` | `ram:URIUniversalCommunication/ram:URIID schemeID="EM"` | eingangsrechnung@... |
| BT-73, BT-74 | Leistungszeitraum | `cac:InvoicePeriod/cbc:StartDate`, `cbc:EndDate` | `ram:BillingSpecifiedPeriod/ram:StartDateTime`, `ram:EndDateTime` | 01.-30.09.2026 |
| BT-81 | Zahlungsart | `cac:PaymentMeans/cbc:PaymentMeansCode` | `ram:SpecifiedTradeSettlementPaymentMeans/ram:TypeCode` | 58 |
| BT-83 | Verwendungszweck | `cbc:PaymentID` | `ram:PaymentReference` | RE-2026-0001 |
| BT-84 | IBAN | `cac:PayeeFinancialAccount/cbc:ID` | `ram:PayeePartyCreditorFinancialAccount/ram:IBANID` | DE79000000001234567890 |
| BT-106 | Summe der Positionen | `cac:LegalMonetaryTotal/cbc:LineExtensionAmount` | `ram:SpecifiedTradeSettlementHeaderMonetarySummation/ram:LineTotalAmount` | 1689.00 |
| BT-109 | Nettobetrag | `cbc:TaxExclusiveAmount` | `ram:TaxBasisTotalAmount` | 1689.00 |
| BT-110 | Umsatzsteuer gesamt | `cac:TaxTotal/cbc:TaxAmount` | `ram:TaxTotalAmount` | 320.91 |
| BT-112 | Bruttobetrag | `cbc:TaxInclusiveAmount` | `ram:GrandTotalAmount` | 2009.91 |
| BT-115 | Zahlbetrag | `cbc:PayableAmount` | `ram:DuePayableAmount` | 2009.91 |
| BT-118, BT-119 | Steuerkategorie und Steuersatz | `cac:TaxCategory/cbc:ID`, `cbc:Percent` | `ram:ApplicableTradeTax/ram:CategoryCode`, `ram:RateApplicablePercent` | S, 19 |
| BT-129, BT-130 | Menge und Einheit je Position | `cbc:InvoicedQuantity unitCode` | `ram:BilledQuantity unitCode` | 12 HUR |
| BT-131 | Nettobetrag der Position | `cac:InvoiceLine/cbc:LineExtensionAmount` | `ram:SpecifiedTradeSettlementLineMonetarySummation/ram:LineTotalAmount` | 1440.00 |
| BT-146 | Nettopreis | `cac:Price/cbc:PriceAmount` | `ram:NetPriceProductTradePrice/ram:ChargeAmount` | 120 |
| BT-153 | Artikelbezeichnung | `cac:Item/cbc:Name` | `ram:SpecifiedTradeProduct/ram:Name` | Beratung Einführung E-Rechnung |

Gruppen von Feldern heißen Business Groups (BG). BG-4 ist der Verkäufer, BG-7 der Käufer, BG-16 die Zahlungsanweisung, BG-22 die Summen, BG-23 die Steueraufschlüsselung und BG-25 eine Rechnungsposition.

## XRechnung Pflichtfelder: die wichtigsten BR-DE-Regeln

Die EN 16931 macht nur wenige Felder zur Pflicht (zum Beispiel BT-1 über BR-02, BT-2 über BR-03, BT-5 über BR-05). Die XRechnung legt mehr fest. Die Regeln stammen aus der XRechnung-Schematron 2.6.0, Texte in Anführungszeichen stehen dort wörtlich so.

| Regel | Was sie verlangt |
| --- | --- |
| BR-DE-1 | "Eine Rechnung (INVOICE) muss Angaben zu "PAYMENT INSTRUCTIONS" (BG-16) enthalten." |
| BR-DE-2 | "Die Gruppe "SELLER CONTACT" (BG-6) muss übermittelt werden." |
| BR-DE-3, BR-DE-4 | Ort (BT-37) und Postleitzahl (BT-38) des Verkäufers |
| BR-DE-5, BR-DE-6, BR-DE-7 | Kontaktname (BT-41), Telefon (BT-42) und E-Mail (BT-43) des Verkäufers |
| BR-DE-8, BR-DE-9 | Ort (BT-52) und Postleitzahl (BT-53) des Käufers |
| BR-DE-14 | Steuersatz (BT-119) in jeder Steueraufschlüsselung |
| BR-DE-15 | "Das Element "Buyer reference" (BT-10) muss übermittelt werden." |
| BR-DE-16 | Bei Steuerkategorie S, Z, E, AE, K, G, L oder M muss BT-31, BT-32 oder eine Steuervertreter-Angabe vorhanden sein. |
| BR-DE-17 | Nur bestimmte Rechnungsarten in BT-3 (Tabelle unten) |
| BR-DE-18 | Skonto in BT-20 in fester Syntax (`#SKONTO#TAGE=10#PROZENT=2.00#`) |
| BR-DE-19 | Bei Zahlungsart 58 soll BT-84 eine korrekte IBAN sein. |
| BR-DE-21 | BT-24 soll der Kennung des Standards XRechnung entsprechen. |
| BR-DE-23 | Bei Zahlungsart 30 oder 58 ist BG-17 (Überweisung) Pflicht. |
| BR-DE-24 | Bei Zahlungsart 48, 54 oder 55 ist BG-18 (Zahlungskarte) Pflicht. |
| BR-DE-25 | Bei Zahlungsart 59 ist BG-19 (Lastschrift) Pflicht, dazu BT-90 und BT-91 (BR-DE-30, BR-DE-31). |
| BR-DE-26 | Bei Rechnungsart 384 soll BG-3 (Vorgängerrechnung) vorhanden sein. |
| BR-DE-27, BR-DE-28 | Telefon mit mindestens 3 Ziffern, E-Mail in gültiger Syntax |

Dazu kommen Regeln aus Peppol, die mit XRechnung 3.0 übernommen wurden: PEPPOL-EN16931-R020 ("Seller electronic address MUST be provided") für BT-34 und PEPPOL-EN16931-R010 ("Buyer electronic address MUST be provided") für BT-49. Als elektronische Adresse dient meist eine E-Mail-Adresse mit dem Schema `EM`, bei Behörden die Leitweg-ID mit dem Schema `0204`.

Nicht jeder Regelverstoß macht eine Rechnung steuerlich unbrauchbar. Laut BMF-Schreiben vom 15.10.2025, Rn. 35a, sind Geschäftsregelfehler zu Inhalten außerhalb der Pflichtangaben nach § 14 Abs. 4 UStG, zum Beispiel ein fehlendes BT-10, umsatzsteuerlich unbeachtlich. Die Behörde oder Software des Empfängers kann die Datei trotzdem ablehnen. Was das im Einzelfall bedeutet, klären Sie mit der Steuerberatung.

## Erlaubte Rechnungsarten in XRechnung (BR-DE-17)

BT-3 enthält einen Code aus der Liste UNTDID 1001. XRechnung lässt laut BR-DE-17 nur diese Codes zu:

| Code | Bedeutung | UBL-Dokument |
| --- | --- | --- |
| 326 | Teilrechnung | `Invoice` |
| 380 | Rechnung | `Invoice` |
| 381 | Credit note (Rechnungskorrektur mit Minderung) | `CreditNote` |
| 384 | Korrigierte Rechnung (Rechnungskorrektur) | `Invoice` |
| 389 | Gutschrift nach § 14 Abs. 2 Satz 5 UStG (Abrechnung durch den Leistungsempfänger) | `Invoice` |
| 875 | Teilrechnung Bau | `Invoice` |
| 876 | Teilschlussrechnung Bau | `Invoice` |
| 877 | Schlussrechnung Bau | `Invoice` |

Andere Codes sind in der reinen EN 16931 möglich, in XRechnung aber nicht. `erechnung erstellen` lehnt sie bei den XRechnung-Formaten ab (Beispiel 8 unten). Mehr zu Gutschrift und Korrektur steht in [Gutschrift, Rechnungskorrektur und Reverse Charge](./e-rechnung-gutschrift-korrektur.md).

## XRechnung 4.0: was sich ändert

Laut [xeinkauf.de](https://xeinkauf.de/aktuelles/xse/vorversion-xrechnung-4-0/) gibt es seit 15.09.2026 eine Vorversion XRechnung 4.0.0. Sie ist nicht für den produktiven Einsatz gedacht. Die finale Version 4.0 erscheint voraussichtlich im Frühjahr 2027 und beruht auf der neuen Norm EN 16931-1:2026.

Geplante Neuerungen laut KoSIT:

- BT-10 darf mehrfach vorkommen, mit optionalem Scheme Identifier.
- XML-Anhänge sind in der Kernrechnung möglich.
- BG-35 "Early Payment Discount" ersetzt die bisherige Skonto-Konvention in BT-20.
- BG-34 "Charges on Behalf of a Third Party" kommt hinzu.
- Mehrere Bestellungen und Lieferungen je Rechnung werden möglich.

Bis dahin bleibt XRechnung 3.0 in Kraft, laut KoSIT mindestens bis 31.07.2027. Für die alte und die neue Normfassung ist ein Parallelbetrieb bis 2029 vorgesehen. Das Werkzeug `erechnung` prüft und erzeugt derzeit XRechnung 3.0.2, nicht 4.0.

## XRechnung Beispiel: Aufbau an echten Dateien

Alle Ausschnitte stammen aus den Dateien in [`beispiele/`](../../beispiele/README.md). Sie sind mit den offiziellen KoSIT-Regeln geprüft.

### Beispiel 1: Kopfdaten in UBL und CII

Dieselben Angaben (BT-24, BT-23, BT-1, BT-2, BT-3) in beiden Syntaxen. So erkennen Sie auf einen Blick, ob eine Datei eine XRechnung ist. UBL aus `01_standard/xrechnung_ubl.xml`:

```xml
<cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0</cbc:CustomizationID>
<cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
<cbc:ID>RE-2026-0001</cbc:ID>
<cbc:IssueDate>2026-10-15</cbc:IssueDate>
<cbc:DueDate>2026-11-14</cbc:DueDate>
<cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
```

CII aus `01_standard/xrechnung_cii.xml`:

```xml
<rsm:ExchangedDocumentContext>
  <ram:BusinessProcessSpecifiedDocumentContextParameter>
    <ram:ID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</ram:ID>
  </ram:BusinessProcessSpecifiedDocumentContextParameter>
  <ram:GuidelineSpecifiedDocumentContextParameter>
    <ram:ID>urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0</ram:ID>
  </ram:GuidelineSpecifiedDocumentContextParameter>
</rsm:ExchangedDocumentContext>
<rsm:ExchangedDocument>
  <ram:ID>RE-2026-0001</ram:ID>
  <ram:TypeCode>380</ram:TypeCode>
  <ram:IssueDateTime>
    <udt:DateTimeString format="102">20261015</udt:DateTimeString>
  </ram:IssueDateTime>
</rsm:ExchangedDocument>
```

### Beispiel 2: Verkäufer mit Kontakt und elektronischer Adresse

Hier stecken BT-34 und die Pflichtgruppe BG-6 (BR-DE-2). Das brauchen Sie, wenn der Validator BR-DE-2 oder PEPPOL-EN16931-R020 meldet. UBL:

```xml
<cbc:EndpointID schemeID="EM">rechnung@nordlicht.example</cbc:EndpointID>
...
<cac:Contact>
  <cbc:Name>Erika Mustermann</cbc:Name>
  <cbc:Telephone>+49 40 66969123</cbc:Telephone>
  <cbc:ElectronicMail>buchhaltung@nordlicht.example</cbc:ElectronicMail>
</cac:Contact>
```

CII:

```xml
<ram:DefinedTradeContact>
  <ram:PersonName>Erika Mustermann</ram:PersonName>
  <ram:TelephoneUniversalCommunication>
    <ram:CompleteNumber>+49 40 66969123</ram:CompleteNumber>
  </ram:TelephoneUniversalCommunication>
  <ram:EmailURIUniversalCommunication>
    <ram:URIID>buchhaltung@nordlicht.example</ram:URIID>
  </ram:EmailURIUniversalCommunication>
</ram:DefinedTradeContact>
...
<ram:URIUniversalCommunication>
  <ram:URIID schemeID="EM">rechnung@nordlicht.example</ram:URIID>
</ram:URIUniversalCommunication>
```

### Beispiel 3: Summen BT-106 bis BT-115

Die Summen müssen rechnerisch zusammenpassen (BR-CO-15: BT-112 = BT-109 + BT-110). Das brauchen Sie, wenn ein Validator einen Rechenfehler meldet. UBL:

```xml
<cac:LegalMonetaryTotal>
  <cbc:LineExtensionAmount currencyID="EUR">1689.00</cbc:LineExtensionAmount>
  <cbc:TaxExclusiveAmount currencyID="EUR">1689.00</cbc:TaxExclusiveAmount>
  <cbc:TaxInclusiveAmount currencyID="EUR">2009.91</cbc:TaxInclusiveAmount>
  <cbc:PayableAmount currencyID="EUR">2009.91</cbc:PayableAmount>
</cac:LegalMonetaryTotal>
```

CII (BT-110 steht hier mit Währungsattribut in der Summengruppe):

```xml
<ram:SpecifiedTradeSettlementHeaderMonetarySummation>
  <ram:LineTotalAmount>1689.00</ram:LineTotalAmount>
  <ram:TaxBasisTotalAmount>1689.00</ram:TaxBasisTotalAmount>
  <ram:TaxTotalAmount currencyID="EUR">320.91</ram:TaxTotalAmount>
  <ram:GrandTotalAmount>2009.91</ram:GrandTotalAmount>
  <ram:DuePayableAmount>2009.91</ram:DuePayableAmount>
</ram:SpecifiedTradeSettlementHeaderMonetarySummation>
```

### Beispiel 4: Zahlung per SEPA-Überweisung mit Skonto

Zahlungsart 58 (BT-81), IBAN (BT-84) und Skonto in der Syntax nach BR-DE-18. UBL:

```xml
<cac:PaymentMeans>
  <cbc:PaymentMeansCode>58</cbc:PaymentMeansCode>
  <cbc:PaymentID>RE-2026-0001</cbc:PaymentID>
  <cac:PayeeFinancialAccount>
    <cbc:ID>DE79000000001234567890</cbc:ID>
    <cbc:Name>Nordlicht Beispiel GmbH</cbc:Name>
  </cac:PayeeFinancialAccount>
</cac:PaymentMeans>
<cac:PaymentTerms>
  <cbc:Note>#SKONTO#TAGE=10#PROZENT=2.00#
Zahlbar innerhalb von 30 Tagen ohne Abzug.</cbc:Note>
</cac:PaymentTerms>
```

CII:

```xml
<ram:SpecifiedTradeSettlementPaymentMeans>
  <ram:TypeCode>58</ram:TypeCode>
  <ram:PayeePartyCreditorFinancialAccount>
    <ram:IBANID>DE79000000001234567890</ram:IBANID>
    <ram:AccountName>Nordlicht Beispiel GmbH</ram:AccountName>
  </ram:PayeePartyCreditorFinancialAccount>
</ram:SpecifiedTradeSettlementPaymentMeans>
```

### Beispiel 5: Minderung 381 als UBL-CreditNote

In UBL ist eine Minderung (381, kaufmännische Gutschrift) ein eigenes Dokument mit eigenem Wurzelelement, in CII nur ein anderer TypeCode. Das brauchen Sie, wenn Ihre Software Gutschriften falsch als `Invoice` schreibt. Aus `03_gutschrift/xrechnung_ubl.xml`:

```xml
<CreditNote xmlns="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2" ...>
  ...
  <cbc:ID>GS-2026-0001</cbc:ID>
  <cbc:IssueDate>2026-10-15</cbc:IssueDate>
  <cbc:CreditNoteTypeCode>381</cbc:CreditNoteTypeCode>
  ...
  <cac:BillingReference>
    <cac:InvoiceDocumentReference>
      <cbc:ID>RE-2026-0001</cbc:ID>
      <cbc:IssueDate>2026-10-15</cbc:IssueDate>
    </cac:InvoiceDocumentReference>
  </cac:BillingReference>
```

`erechnung validieren` prüft diese Datei im KoSIT-Szenario "EN16931 XRechnung (UBL CreditNote)", die CII-Fassung im Szenario "EN16931 XRechnung (CII)". Beide sind gültig.

### Beispiel 6: Rechnung an eine Behörde mit Leitweg-ID

Bei öffentlichen Auftraggebern steht die Leitweg-ID in BT-10 und meist auch als elektronische Adresse des Käufers mit dem Schema `0204`. Aus `08_b2g_leitweg_id/xrechnung_ubl.xml` und `xrechnung_cii.xml`:

```xml
<!-- UBL -->
<cbc:BuyerReference>04011000-12345-03</cbc:BuyerReference>
<cbc:EndpointID schemeID="0204">04011000-12345-03</cbc:EndpointID>
<!-- CII -->
<ram:BuyerReference>04011000-12345-03</ram:BuyerReference>
<ram:URIID schemeID="0204">04011000-12345-03</ram:URIID>
```

Details zu Aufbau und Prüfziffer stehen in [Leitweg-ID](./leitweg-id.md).

### Beispiel 7: Fehlende Käuferreferenz (BR-DE-15)

Ohne BT-10 ist eine XRechnung nach den KoSIT-Regeln ungültig. Für den Test wurde `leitweg_id` aus der Eingabe gelöscht:

```bash
erechnung validieren ohne_bt10.xml
```

```text
ohne_bt10.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-DE-15: [BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BR-DE-15: Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.
```

Im B2B genügt laut BMF-FAQ umsatzsteuerlich ein Platzhalter wie "-" in BT-10. Mit `"leitweg_id": "-"` ist dieselbe Rechnung nach KoSIT gültig. Weitere Meldungen erklärt [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md).

### Beispiel 8: Nicht erlaubte Rechnungsart (BR-DE-17)

Code 386 steht nicht in der Liste von BR-DE-17. `erechnung erstellen` bricht deshalb mit Exit-Code 1 ab, bevor eine Datei entsteht:

```bash
erechnung erstellen vorauszahlung.json --format xrechnung-ubl -o v.xml
```

```text
Rechnungsart 386 ist in XRechnung nicht erlaubt (BR-DE-17). Erlaubt: 326, 380, 381, 384, 389, 875, 876, 877.
```

## Schritt für Schritt: eine XRechnung erstellen und prüfen

So erzeugen Sie aus einer JSON-Datei eine XRechnung in beiden Syntaxen und prüfen sie mit den offiziellen KoSIT-Regeln. Ein Konto oder ein Upload ist nicht nötig, die Rechnungsdaten bleiben auf Ihrem Rechner.

1. Installieren Sie das Werkzeug (Python 3.10 oder neuer, kein Java):

   ```bash
   pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
   ```

2. Legen Sie eine Eingabedatei an. Am einfachsten kopieren Sie [`beispiele/01_standard/eingabe.json`](../../beispiele/01_standard/eingabe.json) und ändern Nummer, Datum, Parteien und Positionen. Summen und Steuern rechnet das Werkzeug selbst.

3. Erzeugen Sie die XRechnung in UBL und, falls gewünscht, in CII:

   ```bash
   erechnung erstellen rechnung.json --format xrechnung-ubl -o rechnung_ubl.xml
   erechnung erstellen rechnung.json --format xrechnung-cii -o rechnung_cii.xml
   ```

   ```text
   rechnung_ubl.xml: xrechnung-ubl, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
   rechnung_cii.xml: xrechnung-cii, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
   ```

4. Prüfen Sie beide Dateien. Beim ersten Aufruf lädt das Werkzeug die KoSIT-Konfiguration, danach läuft es offline:

   ```bash
   erechnung validieren rechnung_ubl.xml rechnung_cii.xml
   ```

   ```text
   rechnung_ubl.xml: XRechnung 3.0 (UBL)
     KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
   rechnung_cii.xml: XRechnung 3.0 (CII)
     KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (CII), 0 Fehler, 0 Warnungen
   ```

5. Kontrollieren Sie den Inhalt: `erechnung lesen rechnung_cii.xml` zeigt Parteien, Positionen und Beträge als Text, `erechnung anzeigen rechnung_ubl.xml -o rechnung_ubl.html` schreibt eine HTML-Ansicht zum Öffnen im Browser.

6. Heben Sie zusammen mit der Rechnung einen Prüfbericht auf, wie es das BMF-Schreiben vom 15.10.2025, Rn. 35a, zum Nachweis nahelegt: `erechnung validieren --bericht berichte rechnung_ubl.xml`.

Versenden müssen Sie die Datei selbst, zum Beispiel per E-Mail oder über das Portal des Empfängers. Das Werkzeug hat keinen Versand und keinen Peppol-Zugangspunkt.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| BT-10 fehlt | `[BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.` | Bei Behörden die Leitweg-ID eintragen, im B2B die Referenz des Kunden oder einen Platzhalter wie "-" |
| Verkäuferkontakt fehlt | `[BR-DE-2] Die Gruppe "SELLER CONTACT" (BG-6) muss übermittelt werden.` | Name, Telefon und E-Mail (BT-41 bis BT-43) ergänzen |
| Elektronische Adresse fehlt | `[PEPPOL-EN16931-R020]` oder `[PEPPOL-EN16931-R010]` | BT-34 und BT-49 setzen, zum Beispiel E-Mail mit Schema `EM` |
| Falsche Kennung in BT-24 | `[BR-DE-21]`, oder die Datei wird nur nach EN 16931 geprüft | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` verwenden |
| Rechnungsart nicht erlaubt | Ablehnung nach BR-DE-17 | Einen der Codes 326, 380, 381, 384, 389, 875, 876, 877 nehmen |
| Summen passen nicht | `[BR-CO-15]` oder `[BR-CO-10]` | BT-106, BT-109, BT-110 und BT-112 nachrechnen, Rundung je Steuersatz prüfen |
| Skonto als Freitext | Meldung zu BR-DE-18 | Syntax `#SKONTO#TAGE=10#PROZENT=2.00#` in BT-20 nutzen |
| Zahlungsart 58 ohne gültige IBAN | Meldung zu BR-DE-19, Vorprüfung `VP-IBAN` | IBAN in BT-84 prüfen |

## Häufige Fragen

### Was ist eine XRechnung einfach erklärt?

Eine XRechnung ist eine Rechnung als XML-Datei, in der jede Angabe ein festes, nummeriertes Feld hat. Software kann sie ohne Abtippen einlesen. Sie folgt der EN 16931 mit deutschen Zusatzregeln der KoSIT.

### Welche XRechnung-Version gilt aktuell?

Aktuell gilt XRechnung 3.0.2. Die Hauptversion 3.0 ist seit 01.02.2024 in Kraft und bleibt laut KoSIT mindestens bis 31.07.2027 gültig. XRechnung 4.0 gibt es bisher nur als Vorversion.

### Ist eine XRechnung eine PDF-Datei?

Nein, eine XRechnung ist eine reine XML-Datei. Eine PDF-Ansicht oder HTML-Ansicht daraus ist nur eine Lesehilfe. Laut KoSIT sind Visualisierungen keine gültigen XRechnungen, das Original ist das XML. Wer XML und PDF in einer Datei braucht, nimmt ZUGFeRD, auf Wunsch mit dem Profil XRECHNUNG.

### Muss ich im B2B eine XRechnung schicken?

Nein, im B2B ist jedes Format nach EN 16931 zulässig, also auch ZUGFeRD ab Version 2.0.1 außer den Profilen MINIMUM und BASIC WL (UStAE 14.1 Abs. 14). Die Formatwahl klären die Vertragspartner laut UStAE 14.1 Abs. 12 untereinander. Der Vergleich steht in [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md).

### Was muss in BT-10 stehen, wenn mein Kunde keine Behörde ist?

BT-10 muss in einer XRechnung vorhanden sein, eine Leitweg-ID ist im B2B aber nicht nötig. Laut BMF-FAQ genügt umsatzsteuerlich ein Platzhalter wie "-". Nennt Ihr Kunde eine eigene Referenz, tragen Sie diese ein.

### Was ist der Unterschied zwischen XRechnung UBL und XRechnung CII?

Es ist dieselbe Rechnung in zwei XML-Sprachen. UBL nutzt Elemente wie `cbc:IssueDate`, CII Elemente wie `ram:IssueDateTime`. Beide prüft die KoSIT mit denselben Geschäftsregeln.

### Wie öffne ich eine XRechnung?

Mit einem Viewer, der das XML lesbar darstellt. Mit diesem Werkzeug geht das über `erechnung anzeigen rechnung.xml`, mit `--offiziell` über die KoSIT-Visualisierung. Mehr dazu in [E-Rechnung empfangen und lesen](./e-rechnung-empfangen.md).

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [XRechnung oder ZUGFeRD: Unterschied und welches Format Sie brauchen](./xrechnung-oder-zugferd.md)
- [E-Rechnung erstellen](./e-rechnung-erstellen.md)
- [E-Rechnung prüfen mit dem Validator](./e-rechnung-validator.md)
- [E-Rechnung Fehlermeldungen beheben](./e-rechnung-fehlermeldungen.md)
- [Leitweg-ID und E-Rechnung an Behörden](./leitweg-id.md)
- [Was ist eine E-Rechnung? Definition, Formate und wie sie aussieht](./was-ist-eine-e-rechnung.md)
- [E-Rechnung Pflicht: ab wann, für wen und welche Übergangsfristen gelten](./e-rechnung-pflicht.md)
- [E-Rechnung Beispiel: XRechnung und ZUGFeRD Beispieldateien zum Herunterladen](./e-rechnung-beispiel.md)
- Beispieldateien: [Übersicht](../../beispiele/README.md), [Standardrechnung UBL](../../beispiele/01_standard/xrechnung_ubl.xml), [Standardrechnung CII](../../beispiele/01_standard/xrechnung_cii.xml)
