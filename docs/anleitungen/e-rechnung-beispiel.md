# E-Rechnung Beispiel: XRechnung und ZUGFeRD Beispieldateien zum Herunterladen

Ein E-Rechnung Beispiel ist eine XML-Datei (XRechnung in UBL oder CII) oder ein PDF/A-3 mit eingebettetem XML (ZUGFeRD), in der alle Rechnungsangaben als strukturierte Daten nach EN 16931 stehen. Im Ordner [`beispiele/`](../../beispiele/README.md) dieses Repos liegen neun gültige Fälle, von der Standardrechnung über Reverse Charge bis zur Rechnung an eine Behörde, jeweils als XRechnung UBL und CII, mit HTML-Ansicht, Eingabedatei und dem Ergebnis der offiziellen KoSIT-Prüfung.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil von [E-Rechnung in Python](../../README.md).

## Das Wichtigste in Kürze

- Das Repo enthält 9 Beispielfälle mit 18 XRechnung-Dateien (je UBL und CII) und 3 ZUGFeRD-PDFs im Profil EN 16931.
- Alle 21 Dateien sind mit den KoSIT-Regeln `xrechnung-3.0.2-validator-configuration-2026-08-31` geprüft: angenommen, 0 Fehler, 0 Warnungen.
- Jeder Fall zeigt eine typische Besonderheit, etwa Steuerkategorie AE mit Befreiungsgrund, die Vorgängerrechnung (BG-3) bei Rechnungsart 384 oder die Leitweg-ID mit dem Schema `0204`.
- Sie können die Dateien direkt von GitHub laden oder mit `erechnung beispiele` lokal erzeugen und als Vorlage für eigene Rechnungen nutzen.
- Namen, Adressen, IBAN `DE79000000001234567890` und Gläubiger-ID `DE98ZZZ09999999999` sind Testwerte und gehören keiner echten Firma.
- Die offizielle Sammlung von Testrechnungen pflegt die KoSIT in der [xrechnung-testsuite](https://github.com/itplr-kosit/xrechnung-testsuite).

## Welche Beispiel-E-Rechnungen gibt es?

| Fall | Was er zeigt | XRechnung | PDF | Ansicht | Eingabe | Prüfergebnis |
| --- | --- | --- | --- | --- | --- | --- |
| 01 Standardrechnung | 19 %, Leistungszeitraum, Skonto, SEPA-Überweisung | [UBL](../../beispiele/01_standard/xrechnung_ubl.xml), [CII](../../beispiele/01_standard/xrechnung_cii.xml) | [ZUGFeRD](../../beispiele/01_standard/zugferd_en16931.pdf) | [HTML](../../beispiele/01_standard/ansicht.html) | [JSON](../../beispiele/01_standard/eingabe.json) | [UBL](../../beispiele/01_standard/validierung_ubl.txt), [CII](../../beispiele/01_standard/validierung_cii.txt) |
| 02 Gemischte Steuersätze | 7 % und 19 %, Nachlass auf Belegebene | [UBL](../../beispiele/02_gemischte_steuersaetze/xrechnung_ubl.xml), [CII](../../beispiele/02_gemischte_steuersaetze/xrechnung_cii.xml) | [ZUGFeRD](../../beispiele/02_gemischte_steuersaetze/zugferd_en16931.pdf) | [HTML](../../beispiele/02_gemischte_steuersaetze/ansicht.html) | [JSON](../../beispiele/02_gemischte_steuersaetze/eingabe.json) | [UBL](../../beispiele/02_gemischte_steuersaetze/validierung_ubl.txt), [CII](../../beispiele/02_gemischte_steuersaetze/validierung_cii.txt) |
| 03 Gutschrift (381) | Rechnungskorrektur mit Minderung, in UBL als CreditNote | [UBL](../../beispiele/03_gutschrift/xrechnung_ubl.xml), [CII](../../beispiele/03_gutschrift/xrechnung_cii.xml) | - | [HTML](../../beispiele/03_gutschrift/ansicht.html) | [JSON](../../beispiele/03_gutschrift/eingabe.json) | [UBL](../../beispiele/03_gutschrift/validierung_ubl.txt), [CII](../../beispiele/03_gutschrift/validierung_cii.txt) |
| 04 Rechnungskorrektur (384) | Bezug auf die ursprüngliche Rechnung (BG-3) | [UBL](../../beispiele/04_rechnungskorrektur/xrechnung_ubl.xml), [CII](../../beispiele/04_rechnungskorrektur/xrechnung_cii.xml) | - | [HTML](../../beispiele/04_rechnungskorrektur/ansicht.html) | [JSON](../../beispiele/04_rechnungskorrektur/eingabe.json) | [UBL](../../beispiele/04_rechnungskorrektur/validierung_ubl.txt), [CII](../../beispiele/04_rechnungskorrektur/validierung_cii.txt) |
| 05 Reverse Charge | Steuerkategorie AE, § 13b UStG | [UBL](../../beispiele/05_reverse_charge_13b/xrechnung_ubl.xml), [CII](../../beispiele/05_reverse_charge_13b/xrechnung_cii.xml) | - | [HTML](../../beispiele/05_reverse_charge_13b/ansicht.html) | [JSON](../../beispiele/05_reverse_charge_13b/eingabe.json) | [UBL](../../beispiele/05_reverse_charge_13b/validierung_ubl.txt), [CII](../../beispiele/05_reverse_charge_13b/validierung_cii.txt) |
| 06 Innergemeinschaftliche Lieferung | Steuerkategorie K, Käufer in Österreich | [UBL](../../beispiele/06_innergemeinschaftlich/xrechnung_ubl.xml), [CII](../../beispiele/06_innergemeinschaftlich/xrechnung_cii.xml) | - | [HTML](../../beispiele/06_innergemeinschaftlich/ansicht.html) | [JSON](../../beispiele/06_innergemeinschaftlich/eingabe.json) | [UBL](../../beispiele/06_innergemeinschaftlich/validierung_ubl.txt), [CII](../../beispiele/06_innergemeinschaftlich/validierung_cii.txt) |
| 07 Kleinunternehmer | Steuerkategorie E, Steuernummer statt USt-IdNr. | [UBL](../../beispiele/07_kleinunternehmer/xrechnung_ubl.xml), [CII](../../beispiele/07_kleinunternehmer/xrechnung_cii.xml) | [ZUGFeRD](../../beispiele/07_kleinunternehmer/zugferd_en16931.pdf) | [HTML](../../beispiele/07_kleinunternehmer/ansicht.html) | [JSON](../../beispiele/07_kleinunternehmer/eingabe.json) | [UBL](../../beispiele/07_kleinunternehmer/validierung_ubl.txt), [CII](../../beispiele/07_kleinunternehmer/validierung_cii.txt) |
| 08 Rechnung an eine Behörde | Leitweg-ID in BT-10 und als elektronische Adresse (0204) | [UBL](../../beispiele/08_b2g_leitweg_id/xrechnung_ubl.xml), [CII](../../beispiele/08_b2g_leitweg_id/xrechnung_cii.xml) | - | [HTML](../../beispiele/08_b2g_leitweg_id/ansicht.html), [KoSIT](../../beispiele/08_b2g_leitweg_id/ansicht_kosit.html) | [JSON](../../beispiele/08_b2g_leitweg_id/eingabe.json) | [UBL](../../beispiele/08_b2g_leitweg_id/validierung_ubl.txt), [CII](../../beispiele/08_b2g_leitweg_id/validierung_cii.txt) |
| 09 SEPA-Lastschrift | Zahlungsart 59, Mandatsreferenz, Gläubiger-ID | [UBL](../../beispiele/09_sepa_lastschrift/xrechnung_ubl.xml), [CII](../../beispiele/09_sepa_lastschrift/xrechnung_cii.xml) | - | [HTML](../../beispiele/09_sepa_lastschrift/ansicht.html) | [JSON](../../beispiele/09_sepa_lastschrift/eingabe.json) | [UBL](../../beispiele/09_sepa_lastschrift/validierung_ubl.txt), [CII](../../beispiele/09_sepa_lastschrift/validierung_cii.txt) |

Dazu kommt ein DATEV-Buchungsstapel über alle Fälle: [`datev/EXTF_Buchungsstapel.csv`](../../beispiele/datev/EXTF_Buchungsstapel.csv), siehe [DATEV und E-Rechnung](./datev-e-rechnung.md).

## Wie sieht eine XRechnung als Datei aus?

Eine XRechnung ist eine XML-Datei. Sie beginnt mit der Kennung der Spezifikation (BT-24) und dem Geschäftsprozess (BT-23), dann folgen Rechnungsnummer, Datum, Rechnungsart, Käuferreferenz, die beiden Parteien, Zahlungsangaben, Steueraufschlüsselung, Summen und die Positionen. So beginnt die Standardrechnung in UBL:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0</cbc:CustomizationID>
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
  <cbc:ID>RE-2026-0001</cbc:ID>
  <cbc:IssueDate>2026-10-15</cbc:IssueDate>
  <cbc:DueDate>2026-11-14</cbc:DueDate>
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <cbc:Note>Vielen Dank für Ihren Auftrag.</cbc:Note>
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
  <cbc:BuyerReference>BH-2026-0815</cbc:BuyerReference>
  ...
</Invoice>
```

Dieselbe Rechnung in CII hat andere Elementnamen und schreibt Datumsangaben als JJJJMMTT mit `format="102"`:

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
  ...
</rsm:ExchangedDocument>
```

| Angabe | BT | UBL | CII |
| --- | --- | --- | --- |
| Rechnungsnummer | BT-1 | `cbc:ID` | `ram:ID` in `rsm:ExchangedDocument` |
| Rechnungsdatum | BT-2 | `cbc:IssueDate` (JJJJ-MM-TT) | `ram:IssueDateTime` (JJJJMMTT) |
| Rechnungsart | BT-3 | `cbc:InvoiceTypeCode` | `ram:TypeCode` |
| Käuferreferenz | BT-10 | `cbc:BuyerReference` | `ram:BuyerReference` |
| Kennung | BT-24 | `cbc:CustomizationID` | `ram:GuidelineSpecifiedDocumentContextParameter` |
| Zahlbetrag | BT-115 | `cbc:PayableAmount` | `ram:DuePayableAmount` |

Eine ZUGFeRD-Rechnung ist ein PDF/A-3, in dem genau so ein CII-XML als Anhang steckt, beim Profil EN 16931 unter dem Namen `factur-x.xml`. Mehr zum Aufbau: [XRechnung](./xrechnung.md) und [ZUGFeRD](./zugferd.md).

## Beispieldateien herunterladen

Jede Datei im Ordner `beispiele/` hat eine direkte Download-Adresse nach dem Muster:

```text
https://raw.githubusercontent.com/pexon-consulting/e-rechnung/main/beispiele/<Fall>/<Datei>
```

| Datei | Download-Adresse |
| --- | --- |
| Standardrechnung, XRechnung UBL | `https://raw.githubusercontent.com/pexon-consulting/e-rechnung/main/beispiele/01_standard/xrechnung_ubl.xml` |
| Standardrechnung, XRechnung CII | `https://raw.githubusercontent.com/pexon-consulting/e-rechnung/main/beispiele/01_standard/xrechnung_cii.xml` |
| Standardrechnung, ZUGFeRD-PDF | `https://raw.githubusercontent.com/pexon-consulting/e-rechnung/main/beispiele/01_standard/zugferd_en16931.pdf` |
| Behörde mit Leitweg-ID, UBL | `https://raw.githubusercontent.com/pexon-consulting/e-rechnung/main/beispiele/08_b2g_leitweg_id/xrechnung_ubl.xml` |
| Kleinunternehmer, ZUGFeRD-PDF | `https://raw.githubusercontent.com/pexon-consulting/e-rechnung/main/beispiele/07_kleinunternehmer/zugferd_en16931.pdf` |

Im Terminal laden Sie eine Datei so:

```bash
curl -LO https://raw.githubusercontent.com/pexon-consulting/e-rechnung/main/beispiele/01_standard/xrechnung_ubl.xml
```

Im Browser öffnen Sie die Datei auf GitHub und klicken auf "Raw" oder das Download-Symbol. Die HTML-Ansichten (`ansicht.html`) laden Sie herunter und öffnen sie lokal im Browser.

## Beispiele lokal erzeugen mit `erechnung beispiele`

Wer das Werkzeug installiert hat, braucht keinen Download. `erechnung beispiele` schreibt alle neun Eingaben und die XRechnungen in UBL und CII in einen Ordner:

```console
$ erechnung beispiele meine-beispiele
meine-beispiele/01_standard: JSON, XRechnung UBL, XRechnung CII
meine-beispiele/02_gemischte_steuersaetze: JSON, XRechnung UBL, XRechnung CII
meine-beispiele/03_gutschrift: JSON, XRechnung UBL, XRechnung CII
...
meine-beispiele/09_sepa_lastschrift: JSON, XRechnung UBL, XRechnung CII
```

Die Dateien heißen dann `01_standard.json`, `01_standard_xrechnung_ubl.xml` und `01_standard_xrechnung_cii.xml`. Sie sind inhaltlich gleich mit den Dateien im Repo. Ein ZUGFeRD-PDF erzeugen Sie aus jeder Eingabe selbst:

```console
$ erechnung erstellen meine-beispiele/01_standard.json --format zugferd -o rechnung.pdf --validieren
rechnung.pdf: zugferd, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
  KoSIT: GÜLTIG (EN16931 (CII))
```

Ohne eigene PDF-Vorlage braucht das Ghostscript. Wie Sie eine Eingabe an Ihre Rechnung anpassen, beschreibt [E-Rechnung erstellen](./e-rechnung-erstellen.md).

## Warum sind die Beispiele gültig?

Alle Dateien sind mit `python scripts/beispiele_bauen.py` aus den Eingaben erzeugt und gegen die offiziellen KoSIT-Regeln geprüft; die CI prüft, dass der Ordner zum Code passt (laut [`beispiele/README.md`](../../beispiele/README.md)). Das Ergebnis liegt je Datei als Text daneben. So sieht `04_rechnungskorrektur/validierung_ubl.txt` aus, die anderen 17 Dateien zeigen dasselbe Ergebnis mit ihrem Szenario:

```text
Regeln: xrechnung-3.0.2-validator-configuration-2026-08-31
Szenario: EN16931 XRechnung (UBL Invoice)
Ergebnis: angenommen
Fehler: 0, Warnungen: 0
```

| Szenario in `validierung_*.txt` | Dateien |
| --- | --- |
| `EN16931 XRechnung (UBL Invoice)` | UBL von 01, 02, 04 bis 09 |
| `EN16931 XRechnung (UBL CreditNote)` | UBL von 03 (Rechnungsart 381) |
| `EN16931 XRechnung (CII)` | alle neun CII-Dateien |

Sie müssen den Textdateien nicht glauben, sondern können selbst prüfen:

```console
$ erechnung validieren beispiele/05_reverse_charge_13b/xrechnung_ubl.xml beispiele/05_reverse_charge_13b/xrechnung_cii.xml
beispiele/05_reverse_charge_13b/xrechnung_ubl.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
beispiele/05_reverse_charge_13b/xrechnung_cii.xml: XRechnung 3.0 (CII)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (CII), 0 Fehler, 0 Warnungen
```

Die Prüfung arbeitet wie der KoSIT-Validator: erst das XML-Schema, dann die Schematron-Regeln der EN 16931 und der XRechnung (BR-DE). Bei den ZUGFeRD-PDFs prüft sie das eingebettete XML, Szenario `EN16931 (CII)`; eine Prüfung der PDF/A-3-Konformität leistet der KoSIT-Validator nicht. Eine Prüfung mit anderen Validatoren beschreibt [E-Rechnung prüfen](./e-rechnung-validator.md).

## Offizielle Testrechnungen der KoSIT

Die KoSIT pflegt eine eigene Sammlung von Testrechnungen: die [xrechnung-testsuite](https://github.com/itplr-kosit/xrechnung-testsuite), aktuell Version v2026-08-31, Lizenz Apache-2.0. Sie eignet sich als Testmaterial für Software, etwa die Datei `src/test/business-cases/standard/01.01a-INVOICE_ubl.xml` mit dem Geschäftsprozess `urn:fdc:peppol.eu:2017:poacc:billing:01:1.0`. Die Beispiele in diesem Repo sind kleiner, deutsch beschriftet und je auf einen Fall zugeschnitten. Für Softwaretests lohnt sich beides.

## Beispiele

### Beispiel 1: Standardrechnung mit Skonto (01)

```xml
<cac:PaymentMeans>
  <cbc:PaymentMeansCode>58</cbc:PaymentMeansCode>
  <cbc:PaymentID>RE-2026-0001</cbc:PaymentID>
  <cac:PayeeFinancialAccount>
    <cbc:ID>DE79000000001234567890</cbc:ID>
    <cbc:Name>Nordlicht Software GmbH</cbc:Name>
  </cac:PayeeFinancialAccount>
</cac:PaymentMeans>
<cac:PaymentTerms>
  <cbc:Note>#SKONTO#TAGE=10#PROZENT=2.00#
Zahlbar innerhalb von 30 Tagen ohne Abzug.</cbc:Note>
</cac:PaymentTerms>
```

Brauchen Sie als Vorlage für die normale Dienstleistungsrechnung. Code 58 ist die SEPA-Überweisung, die Skonto-Zeile folgt der Syntax nach BR-DE-18, der Leistungszeitraum steht in `cac:InvoicePeriod`.

### Beispiel 2: Gemischte Steuersätze und Nachlass (02)

```xml
<cac:AllowanceCharge>
  <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
  <cbc:AllowanceChargeReasonCode>95</cbc:AllowanceChargeReasonCode>
  <cbc:AllowanceChargeReason>Treuerabatt</cbc:AllowanceChargeReason>
  <cbc:Amount currencyID="EUR">5.00</cbc:Amount>
  <cac:TaxCategory>
    <cbc:ID>S</cbc:ID>
    <cbc:Percent>19</cbc:Percent>
    ...
  </cac:TaxCategory>
</cac:AllowanceCharge>
```

Brauchen Sie, wenn eine Rechnung 7 % und 19 % enthält. Die Steueraufschlüsselung hat dann zwei `cac:TaxSubtotal`: 10,48 EUR auf 149,70 EUR und 7,58 EUR auf 39,88 EUR. Der Nachlass mindert die 19-%-Gruppe.

### Beispiel 3: Gutschrift als CreditNote (03)

```xml
<CreditNote xmlns="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2">
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0</cbc:CustomizationID>
  ...
  <cbc:CreditNoteTypeCode>381</cbc:CreditNoteTypeCode>
  ...
  <cac:BillingReference>
    <cac:InvoiceDocumentReference>
      <cbc:ID>RE-2026-0001</cbc:ID>
      <cbc:IssueDate>2026-10-15</cbc:IssueDate>
    </cac:InvoiceDocumentReference>
  </cac:BillingReference>
  ...
</CreditNote>
```

Brauchen Sie, wenn Sie einen Betrag gutschreiben, etwa doppelt berechnete Stunden. In UBL wird Rechnungsart 381 (Credit note) zum eigenen Dokumenttyp `CreditNote`, in CII bleibt es `ram:TypeCode` 381. Achtung: Umsatzsteuerlich ist eine Gutschrift nach § 14 Abs. 2 Satz 5 UStG die Abrechnung durch den Leistungsempfänger, dafür steht Code 389. Mehr in [Gutschrift, Rechnungskorrektur und Reverse Charge](./e-rechnung-gutschrift-korrektur.md).

### Beispiel 4: Rechnungskorrektur mit Vorgängerrechnung, BG-3 (04)

```xml
<cbc:InvoiceTypeCode>384</cbc:InvoiceTypeCode>
<cbc:Note>Diese Rechnung ersetzt Rechnung RE-2026-0002 (falsche Anschrift).</cbc:Note>
<cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
<cbc:BuyerReference>BH-2026-0815</cbc:BuyerReference>
<cac:BillingReference>
  <cac:InvoiceDocumentReference>
    <cbc:ID>RE-2026-0002</cbc:ID>
    <cbc:IssueDate>2026-10-15</cbc:IssueDate>
  </cac:InvoiceDocumentReference>
</cac:BillingReference>
```

Brauchen Sie, wenn eine Rechnung ersetzt wird. Bei Code 384 soll die Vorgängerrechnung (BG-3) mit Nummer BT-25 und Datum BT-26 angegeben sein (Regel BR-DE-26). In CII steht sie in `ram:InvoiceReferencedDocument`.

### Beispiel 5: Reverse Charge mit Steuerkategorie AE (05)

```xml
<cac:TaxSubtotal>
  <cbc:TaxableAmount currencyID="EUR">18500.00</cbc:TaxableAmount>
  <cbc:TaxAmount currencyID="EUR">0.00</cbc:TaxAmount>
  <cac:TaxCategory>
    <cbc:ID>AE</cbc:ID>
    <cbc:Percent>0</cbc:Percent>
    <cbc:TaxExemptionReason>Steuerschuldnerschaft des Leistungsempfängers (§ 13b UStG)</cbc:TaxExemptionReason>
    <cac:TaxScheme>
      <cbc:ID>VAT</cbc:ID>
    </cac:TaxScheme>
  </cac:TaxCategory>
</cac:TaxSubtotal>
```

Brauchen Sie bei Bauleistungen und anderen Fällen nach § 13b UStG, wenn der Leistungsempfänger die Steuer schuldet. Kategorie AE braucht einen Befreiungsgrund (BT-120) und die USt-IdNr. des Käufers. Auch § 13b-Fälle zwischen inländischen Unternehmern fallen unter die E-Rechnungspflicht (BMF-Schreiben vom 15.10.2025, Rn. 17).

### Beispiel 6: Innergemeinschaftliche Lieferung, Kategorie K (06)

```xml
<cac:TaxCategory>
  <cbc:ID>K</cbc:ID>
  <cbc:Percent>0</cbc:Percent>
  <cbc:TaxExemptionReason>Steuerfreie innergemeinschaftliche Lieferung (§ 4 Nr. 1b UStG)</cbc:TaxExemptionReason>
  ...
</cac:TaxCategory>
```

Brauchen Sie bei Lieferungen in einen anderen EU-Staat. Das Beispiel hat einen Käufer in Wien mit USt-IdNr. `ATU12345678` und eine Lieferadresse in `cac:Delivery`. Ob die Voraussetzungen der Steuerbefreiung erfüllt sind, klären Sie mit der Steuerberatung.

### Beispiel 7: Kleinunternehmer mit Steuernummer, Kategorie E (07)

```xml
<ram:SpecifiedTaxRegistration>
  <ram:ID schemeID="FC">214/5678/1234</ram:ID>
</ram:SpecifiedTaxRegistration>
...
<ram:ApplicableTradeTax>
  <ram:CalculatedAmount>0.00</ram:CalculatedAmount>
  <ram:TypeCode>VAT</ram:TypeCode>
  <ram:ExemptionReason>Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.</ram:ExemptionReason>
  <ram:BasisAmount>850.00</ram:BasisAmount>
  <ram:CategoryCode>E</ram:CategoryCode>
  <ram:RateApplicablePercent>0</ram:RateApplicablePercent>
</ram:ApplicableTradeTax>
```

Brauchen Sie als Kleinunternehmer, der freiwillig E-Rechnungen schickt. `schemeID="FC"` kennzeichnet die Steuernummer (BT-32) statt einer USt-IdNr. Pflicht ist die E-Rechnung für Kleinunternehmer nicht (§ 34a UStDV), siehe [E-Rechnung für Kleinunternehmer](./e-rechnung-kleinunternehmer.md).

### Beispiel 8: Rechnung an eine Behörde mit Leitweg-ID 0204 (08)

```xml
<cbc:BuyerReference>04011000-12345-03</cbc:BuyerReference>
...
<cac:AccountingCustomerParty>
  <cac:Party>
    <cbc:EndpointID schemeID="0204">04011000-12345-03</cbc:EndpointID>
    ...
  </cac:Party>
</cac:AccountingCustomerParty>
```

Brauchen Sie für Rechnungen an öffentliche Auftraggeber. Die Leitweg-ID steht in BT-10 und als elektronische Adresse des Käufers (BT-49) mit dem Schema `0204`. Die Prüfziffer bestätigt `erechnung leitweg-id`:

```console
$ erechnung leitweg-id 04011000-12345-03
04011000-12345-03: gültig
```

Zu diesem Fall gibt es zusätzlich die [KoSIT-Ansicht](../../beispiele/08_b2g_leitweg_id/ansicht_kosit.html), erzeugt mit der offiziellen KoSIT-Visualisierung. Mehr in [Leitweg-ID](./leitweg-id.md).

### Beispiel 9: SEPA-Lastschrift mit PaymentMandate (09)

```xml
<cac:PartyIdentification>
  <cbc:ID schemeID="SEPA">DE98ZZZ09999999999</cbc:ID>
</cac:PartyIdentification>
...
<cac:PaymentMeans>
  <cbc:PaymentMeansCode>59</cbc:PaymentMeansCode>
  <cac:PaymentMandate>
    <cbc:ID>MANDAT-2026-001</cbc:ID>
    <cac:PayerFinancialAccount>
      <cbc:ID>DE79000000001234567890</cbc:ID>
    </cac:PayerFinancialAccount>
  </cac:PaymentMandate>
</cac:PaymentMeans>
```

Brauchen Sie, wenn Sie den Betrag per Lastschrift einziehen. Bei Code 59 verlangt XRechnung die Gruppe DIRECT DEBIT (BG-19, Regel BR-DE-25) mit Gläubiger-ID (BT-90) und belastetem Konto (BT-91); die Mandatsreferenz (BT-89) verlangt PEPPOL-EN16931-R061. In CII heißen die Elemente `ram:CreditorReferenceID`, `ram:DirectDebitMandateID` und `ram:PayerPartyDebtorFinancialAccount`.

### Beispiel 10: Das XML aus einem ZUGFeRD-Beispiel holen

```console
$ erechnung extrahieren beispiele/01_standard/zugferd_en16931.pdf -o 01_standard_factur-x.xml
factur-x.xml aus beispiele/01_standard/zugferd_en16931.pdf gespeichert als 01_standard_factur-x.xml
```

Brauchen Sie, um zu sehen, was im PDF steckt. Das XML entspricht `01_standard/xrechnung_cii.xml`, nur die Kennung BT-24 ist `urn:cen.eu:en16931:2017` (Profil EN 16931) statt der XRechnung-Kennung.

## Schritt für Schritt

1. In der Tabelle oben den Fall wählen, der Ihrer Rechnung am nächsten kommt.
2. Die XML-Datei oder das PDF herunterladen (Download-Adresse oder "Raw" auf GitHub).
3. Die Datei lesbar machen: `ansicht.html` im Browser öffnen oder mit dem Werkzeug `erechnung anzeigen beispiele/08_b2g_leitweg_id/xrechnung_ubl.xml -o ansicht.html` eine eigene Ansicht erzeugen.
4. Mit `erechnung lesen` eine Zusammenfassung im Terminal ansehen, etwa für das ZUGFeRD-Beispiel 02:

   ```bash
   erechnung lesen beispiele/02_gemischte_steuersaetze/zugferd_en16931.pdf
   ```

   ```text
   Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
   E-Rechnung:   ja, strukturiert nach EN 16931
   ...
   USt:          S (Regelsteuersatz oder ermäßigter Satz) 7 %: 10,48 EUR auf 149,70 EUR
   USt:          S (Regelsteuersatz oder ermäßigter Satz) 19 %: 7,58 EUR auf 39,88 EUR
   Zahlbetrag:   207,64 EUR, fällig 14.11.2026
   ```

5. Mit `erechnung validieren` selbst prüfen, dass die Datei gültig ist.
6. Für eine eigene Rechnung die passende `eingabe.json` kopieren, Ihre Daten eintragen und mit `erechnung erstellen ... --validieren` eine neue E-Rechnung erzeugen.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Beispiel-XML direkt an Kunden schicken | Testdaten (Musterfirmen, Test-IBAN) beim Empfänger | Immer eine eigene Rechnung aus der Eingabe erzeugen |
| Datei über "Speichern unter" der GitHub-Seite geladen | Datei enthält HTML statt XML, Prüfung schlägt fehl | "Raw" verwenden oder die Download-Adresse nach dem Muster oben |
| `ansicht.html` für die Rechnung halten | Ansicht wird weitergeleitet oder archiviert | Maßgeblich ist das XML; die Ansicht dient nur zum Lesen |
| Nur die Bildseite eines ZUGFeRD-PDFs ändern | Bildteil und XML passen nicht zusammen | Eingabe ändern und PDF neu erzeugen; bei Abweichungen gilt laut BMF-FAQ das XML |
| Gutschrift 381 und 389 verwechseln | Falsche Rechnungsart für den Vorgang | 381 für Korrektur mit Minderung, 389 für Abrechnung durch den Leistungsempfänger |
| Leitweg-ID aus Beispiel 08 übernehmen | Behörde kann die Rechnung nicht zuordnen | Die Leitweg-ID des eigenen Auftraggebers eintragen und prüfen |

## Häufige Fragen

### Wo finde ich eine XRechnung als Beispiel zum Herunterladen?

Im Ordner [`beispiele/`](../../beispiele/README.md) dieses Repos liegen 18 XRechnungen in UBL und CII, jede mit dem Ergebnis der KoSIT-Prüfung. Die direkte Adresse folgt dem Muster `https://raw.githubusercontent.com/pexon-consulting/e-rechnung/main/beispiele/<Fall>/<Datei>`. Weitere offizielle Testdateien enthält die [xrechnung-testsuite](https://github.com/itplr-kosit/xrechnung-testsuite) der KoSIT.

### Gibt es eine ZUGFeRD-Beispielrechnung als PDF?

Ja, drei: [Standardrechnung](../../beispiele/01_standard/zugferd_en16931.pdf), [gemischte Steuersätze](../../beispiele/02_gemischte_steuersaetze/zugferd_en16931.pdf) und [Kleinunternehmer](../../beispiele/07_kleinunternehmer/zugferd_en16931.pdf), jeweils im Profil EN 16931 mit eingebettetem `factur-x.xml`. Aus jeder anderen Eingabe erzeugen Sie mit `erechnung erstellen ... --format zugferd` ein eigenes PDF.

### Sind die Beispiele wirklich gültige E-Rechnungen?

Ja, alle 21 Dateien sind mit den KoSIT-Regeln für XRechnung 3.0.2 (Konfiguration 2026-08-31) geprüft: angenommen, 0 Fehler, 0 Warnungen. Das Ergebnis steht in den Dateien `validierung_ubl.txt` und `validierung_cii.txt`, und Sie können es mit `erechnung validieren` jederzeit selbst nachprüfen.

### Wie sieht eine E-Rechnung aus, wenn ich sie öffne?

Eine E-Rechnung ist eine XML-Datei mit Elementen wie `cbc:ID` für die Rechnungsnummer und `cbc:PayableAmount` für den Zahlbetrag. Im Texteditor sehen Sie diesen Quelltext, für eine lesbare Ansicht brauchen Sie einen Viewer. Dafür liegt neben jedem Beispiel eine `ansicht.html`; wie Sie eigene Rechnungen öffnen, steht in [E-Rechnung empfangen und lesen](./e-rechnung-empfangen.md).

### Was ist der Unterschied zwischen den UBL- und CII-Dateien?

Beide Dateien eines Falls enthalten dieselbe Rechnung in zwei zulässigen Syntaxen der XRechnung: UBL 2.1 und UN/CEFACT CII D16B. Die Elementnamen und das Datumsformat unterscheiden sich, der Inhalt nicht. ZUGFeRD verwendet immer CII.

### Darf ich die Beispiele für eigene Software-Tests verwenden?

Ja, die Dateien enthalten nur Testwerte und stehen wie das ganze Repo unter der MIT-Lizenz ([LICENSE](../../LICENSE)). Für Tests eignen sich zusätzlich die Testrechnungen der [KoSIT-Testsuite](https://github.com/itplr-kosit/xrechnung-testsuite) (Apache-2.0).

> **Hinweis:** Diese Anleitung erklärt Gesetz, BMF-Schreiben und technische Standards nach dem Stand vom 15.10.2026. Sie ist keine Steuer- oder Rechtsberatung, die Autoren sind keine Steuerberater. Für die Beurteilung eines konkreten Falls wenden Sie sich an Ihre Steuerberatung oder Ihr Finanzamt. Alle Angaben ohne Gewähr.

## Weiterlesen

- [E-Rechnung erstellen: XRechnung und ZUGFeRD kostenlos erzeugen](./e-rechnung-erstellen.md)
- [E-Rechnung prüfen: Validator mit den offiziellen Regeln](./e-rechnung-validator.md)
- [Gutschrift, Rechnungskorrektur und Reverse Charge als E-Rechnung](./e-rechnung-gutschrift-korrektur.md)
- [XRechnung: Format, Aufbau und Pflichtfelder](./xrechnung.md)
- [ZUGFeRD: Format, Profile und Versionen](./zugferd.md)
- Beispiele im Repo: [Übersicht](../../beispiele/README.md), [Behörde mit Leitweg-ID](../../beispiele/08_b2g_leitweg_id/xrechnung_ubl.xml), [SEPA-Lastschrift](../../beispiele/09_sepa_lastschrift/xrechnung_ubl.xml)
