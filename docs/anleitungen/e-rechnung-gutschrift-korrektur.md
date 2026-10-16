# Gutschrift, Rechnungskorrektur und Reverse Charge als E-Rechnung

Eine Gutschrift als E-Rechnung, eine Rechnungskorrektur oder ein Reverse-Charge-Fall unterscheidet sich von einer normalen E-Rechnung in wenigen Feldern: der Rechnungsart BT-3, dem Bezug auf die Vorgängerrechnung BG-3 und der Steuerkategorie BT-118/BT-151 mit Befreiungsgrund BT-120. XRechnung erlaubt laut Geschäftsregel BR-DE-17 nur acht Rechnungsarten (326, 380, 381, 384, 389, 875, 876, 877); Reverse Charge nach § 13b UStG läuft über die Steuerkategorie AE, die innergemeinschaftliche Lieferung über K. Diese Anleitung zeigt jeden Fall mit echtem XML und den Befehlen `erechnung erstellen` und `erechnung validieren`.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil von [E-Rechnung in Python](../../README.md).

## Das Wichtigste in Kürze

- Die Rechnungsart steht in BT-3 als Code der Liste UNTDID 1001; XRechnung lässt nur 326, 380, 381, 384, 389, 875, 876 und 877 zu (BR-DE-17).
- "Gutschrift" meint zwei verschiedene Dinge: die Abrechnung durch den Leistungsempfänger (389, Gutschrift im Sinne des UStG) und die Minderung einer Rechnung durch den Leistenden (381, Credit Note).
- Eine Rechnungskorrektur (384) soll laut BR-DE-26 auf die ursprüngliche Rechnung verweisen (BG-3 mit BT-25 und BT-26).
- In UBL wird die Rechnungsart 381 als eigenes Dokument `CreditNote` geschrieben, in CII bleibt es eine `CrossIndustryInvoice` mit `TypeCode` 381.
- Reverse Charge (Kategorie AE) und innergemeinschaftliche Lieferung (Kategorie K) brauchen Steuersatz 0, einen Befreiungsgrund und die USt-IdNr. des Käufers (BT-48).
- Welche Rechnungsart und welche Steuerkategorie im Einzelfall richtig ist, ist eine steuerliche Frage; klären Sie das mit der Steuerberatung.

## Welche Rechnungsarten erlaubt die XRechnung?

Die Rechnungsart ist ein Pflichtfeld (BT-3, Geschäftsregel BR-04). Für XRechnung schränkt BR-DE-17 die Codes ein. Die deutschen Bezeichnungen stammen aus `src/erechnung/codelisten.py`, die englischen aus der Codeliste UNTDID 1001:

| Code | Bedeutung | Englisch (UNTDID 1001) | UBL-Dokument |
| --- | --- | --- | --- |
| 326 | Teilrechnung | Partial invoice | Invoice |
| 380 | Rechnung | Commercial invoice | Invoice |
| 381 | Rechnungskorrektur mit Minderung (Credit Note) | Credit note | CreditNote |
| 384 | Korrigierte Rechnung | Corrected invoice | Invoice |
| 389 | Gutschrift im Sinne des UStG (Abrechnung durch den Leistungsempfänger) | Self-billed invoice | Invoice |
| 875 | Teilrechnung Bau | Partial construction invoice | Invoice |
| 876 | Teilschlussrechnung Bau | Partial final construction invoice | Invoice |
| 877 | Schlussrechnung Bau | Final construction invoice | Invoice |

Andere Codes lehnt `erechnung erstellen` für XRechnung schon vor dem Schreiben ab:

```bash
erechnung erstellen rechnung_383.json -o rechnung.xml
```

```text
Rechnungsart 383 ist in XRechnung nicht erlaubt (BR-DE-17). Erlaubt: 326, 380, 381, 384, 389, 875, 876, 877.
```

Der Exit-Code ist dann 1, es entsteht keine Datei. In der Eingabe-JSON steht die Rechnungsart im Feld `art`, Standard ist 380.

## Gutschrift ist nicht gleich Gutschrift: 389 oder 381

Im Alltag heißt vieles "Gutschrift". Für die E-Rechnung müssen Sie zwei Fälle trennen:

| | Gutschrift im Sinne des UStG | Kaufmännische Gutschrift |
| --- | --- | --- |
| Code | 389 (Self-billed invoice) | 381 (Credit note) |
| Wer stellt aus? | der Leistungsempfänger, er rechnet über die Leistung ab, die er bekommen hat | der Leistende, er mindert eine eigene Rechnung |
| Einordnung | Gutschrift nach § 14 Abs. 2 Satz 5 UStG | Minderung einer bereits gestellten Rechnung |
| Typischer Anlass | Provisionsabrechnung, Abrechnung von Lieferungen durch den Abnehmer | doppelt berechnete Stunden, Rücksendung, nachträglicher Nachlass |
| UBL-Dokument | Invoice | CreditNote |

Eine Gutschrift im Sinne des UStG ist eine Rechnung, die der Leistungsempfänger ausstellt. Auch dann steht in der Datei der leistende Unternehmer als Verkäufer (BG-4) und der Aussteller als Käufer (BG-7); nur die Rechnungsart 389 zeigt, wer abgerechnet hat. Ob eine solche Abrechnung vereinbart ist und welche Angaben zusätzlich nötig sind, klären Sie mit der Steuerberatung.

Auch Gutschriften fallen unter die E-Rechnungspflicht, wenn beide Unternehmer im Inland ansässig sind (laut [BMF-FAQ](https://www.bundesfinanzministerium.de/Content/DE/FAQ/e-rechnung.html) und BMF-Schreiben vom 15.10.2025).

## Gutschrift als E-Rechnung (381): Beispiel 03

Beispiel [`03_gutschrift`](../../beispiele/03_gutschrift/eingabe.json) mindert Rechnung RE-2026-0001 um zwei doppelt berechnete Stunden. Die wichtigen Felder der Eingabe:

```json
{
  "nummer": "GS-2026-0001",
  "art": "381",
  "vorgaenger_nummer": "RE-2026-0001",
  "vorgaenger_datum": "2026-10-15",
  "notizen": [
    "Gutschrift zu Rechnung RE-2026-0001: zwei Stunden wurden doppelt berechnet."
  ]
}
```

Die Beträge stehen positiv in der Datei. Dass es eine Minderung ist, sagt der Code 381. In UBL wird daraus ein Dokument mit dem Wurzelelement `CreditNote` (Namensraum `urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2`), Auszug aus [`xrechnung_ubl.xml`](../../beispiele/03_gutschrift/xrechnung_ubl.xml):

```xml
<cbc:CreditNoteTypeCode>381</cbc:CreditNoteTypeCode>
<cbc:Note>Gutschrift zu Rechnung RE-2026-0001: zwei Stunden wurden doppelt berechnet.</cbc:Note>
<cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
<cbc:BuyerReference>BH-2026-0815</cbc:BuyerReference>
<cac:BillingReference>
  <cac:InvoiceDocumentReference>
    <cbc:ID>RE-2026-0001</cbc:ID>
    <cbc:IssueDate>2026-10-15</cbc:IssueDate>
  </cac:InvoiceDocumentReference>
</cac:BillingReference>
```

Auch die Positionen heißen anders: `CreditNoteLine` statt `InvoiceLine` und `CreditedQuantity` statt `InvoicedQuantity`, die Menge bleibt positiv:

```xml
<cbc:CreditedQuantity unitCode="HUR">2</cbc:CreditedQuantity>
```

In CII gibt es kein eigenes Gutschrift-Dokument. Der Code steht als `<ram:TypeCode>381</ram:TypeCode>` im Kopf (`ExchangedDocument`), der Bezug auf die Vorgängerrechnung in `ram:InvoiceReferencedDocument` mit `ram:IssuerAssignedID` RE-2026-0001.

Erstellen und prüfen:

```bash
erechnung erstellen beispiele/03_gutschrift/eingabe.json -o gutschrift.xml
erechnung validieren gutschrift.xml
```

```text
gutschrift.xml: xrechnung-ubl, Rechnung GS-2026-0001, Zahlbetrag 285,60 EUR
gutschrift.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL CreditNote), 0 Fehler, 0 Warnungen
```

## Rechnungskorrektur als E-Rechnung (384) mit Bezug BG-3

Eine Rechnungskorrektur ersetzt eine fehlerhafte Rechnung. Sie trägt den Code 384 und verweist in BG-3 (PRECEDING INVOICE REFERENCE) auf die Vorgängerrechnung: BT-25 ist deren Nummer, BT-26 deren Datum. In der Eingabe heißen die Felder `vorgaenger_nummer` und `vorgaenger_datum`. Auszug aus [`04_rechnungskorrektur/xrechnung_ubl.xml`](../../beispiele/04_rechnungskorrektur/xrechnung_ubl.xml):

```xml
<cbc:ID>RE-2026-0003</cbc:ID>
<cbc:InvoiceTypeCode>384</cbc:InvoiceTypeCode>
<cbc:Note>Diese Rechnung ersetzt Rechnung RE-2026-0002 (falsche Anschrift).</cbc:Note>
<cac:BillingReference>
  <cac:InvoiceDocumentReference>
    <cbc:ID>RE-2026-0002</cbc:ID>
    <cbc:IssueDate>2026-10-15</cbc:IssueDate>
  </cac:InvoiceDocumentReference>
</cac:BillingReference>
```

Die Korrektur bekommt eine eigene, neue Rechnungsnummer. Fehlt der Bezug, meldet die offizielle Prüfung eine Warnung (die Datei bleibt gültig):

```bash
erechnung validieren korrektur_ohne_bezug.xml
```

```text
korrektur_ohne_bezug.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 1 Warnungen
  WARNUNG BR-DE-26: [BR-DE-26] Wenn im Element "Invoice type code" (BT-3) der Code 384 (Corrected invoice) übergeben wird, soll PRECEDING INVOICE REFERENCE BG-3 mind. einmal vorhanden sein.
```

Laut BMF-Schreiben vom 15.10.2025, Rn. 51a und 51b, braucht eine Minderung der Bemessungsgrundlage nach § 17 UStG (zum Beispiel Skonto oder Nachlass) keine Rechnungsberichtigung; Änderungen im Leistungsumfang dagegen schon. Ob Sie berichtigen, mindern oder neu ausstellen, klären Sie im Einzelfall mit der Steuerberatung.

## Storno einer E-Rechnung

Für einen Storno gibt es in der Liste der XRechnung keinen eigenen Code. Technisch lässt sich eine fehlerhafte Rechnung auf zwei Arten aufheben: mit einer Gutschrift 381 über den vollen Betrag und BG-3 auf die ursprüngliche Rechnung (danach bei Bedarf eine neue Rechnung 380) oder mit einer korrigierten Rechnung 384, die die ursprüngliche ersetzt.

Welcher Weg steuerlich passt, entscheidet nicht das Format; stimmen Sie das mit der Steuerberatung und dem Empfänger ab. Wichtig für den Empfänger: Er muss erkennen können, welche Rechnung aufgehoben ist. Deshalb gehört die Nummer der ursprünglichen Rechnung immer in BG-3 und gern zusätzlich in eine Notiz (BT-22).

## Abschlagsrechnung, Teilrechnung und Schlussrechnung (326, 875-877)

Für Teil- und Abschlagsrechnungen sieht die Codeliste 326 (Teilrechnung) vor, für Bauleistungen 875 (Teilrechnung Bau), 876 (Teilschlussrechnung Bau) und 877 (Schlussrechnung Bau). Welche Art Ihr Auftraggeber erwartet, stimmen Sie mit ihm ab.

In einer Schlussrechnung stehen alle Leistungen, bereits gezahlte Abschläge zieht man als Vorauszahlung (BT-113, Feld `vorauszahlung`) ab. Der Bezug auf die Teilrechnung kommt in BG-3. Beispiel: Schlussrechnung über 18.500,00 EUR mit 10.000,00 EUR Abschlag, als Bauleistung mit Reverse Charge:

```json
{
  "nummer": "SR-2026-0001",
  "art": "877",
  "vorauszahlung": "10000.00",
  "vorgaenger_nummer": "TR-2026-0001",
  "vorgaenger_datum": "2026-09-15"
}
```

```bash
erechnung erstellen schlussrechnung.json -o schlussrechnung.xml --validieren
```

```text
schlussrechnung.xml: xrechnung-ubl, Rechnung SR-2026-0001, Zahlbetrag 8.500,00 EUR
  KoSIT: GÜLTIG (EN16931 XRechnung (UBL Invoice))
```

Im XML stehen `<cbc:InvoiceTypeCode>877</cbc:InvoiceTypeCode>`, Vorauszahlung und Zahlbetrag:

```xml
<cbc:PrepaidAmount currencyID="EUR">10000.00</cbc:PrepaidAmount>
<cbc:PayableAmount currencyID="EUR">8500.00</cbc:PayableAmount>
```

## Reverse Charge in der XRechnung (§ 13b UStG, Kategorie AE)

Bei Reverse Charge schuldet der Leistungsempfänger die Umsatzsteuer (§ 13b UStG). In der E-Rechnung heißt das Steuerkategorie AE ("Steuerschuldnerschaft des Leistungsempfängers"). Auch § 13b-Fälle fallen unter die E-Rechnungspflicht, wenn beide Unternehmer im Inland ansässig sind (BMF-Schreiben vom 15.10.2025, Rn. 17).

Was in der Datei stehen muss:

| Angabe | Feld | Geprüft durch |
| --- | --- | --- |
| Steuerkategorie AE an Position und in der Aufschlüsselung | BT-151, BT-118 | Codeliste UNCL 5305 (BR-CL-18) |
| Steuersatz 0 an der Position, Steuerbetrag 0 | BT-152, BT-117 | BR-AE-05, BR-AE-09 |
| Befreiungsgrund als Text oder Code | BT-120 bzw. BT-121 | BR-AE-10 |
| USt-IdNr. oder Steuernummer des Verkäufers | BT-31, BT-32 | BR-AE-02, BR-DE-16 |
| USt-IdNr. des Käufers (oder seine Registernummer) | BT-48 bzw. BT-47 | BR-AE-02 |

Beispiel [`05_reverse_charge_13b`](../../beispiele/05_reverse_charge_13b/eingabe.json) ist eine Elektroinstallation an einen Bauträger. In der Eingabe stehen an der Position `"kategorie": "AE"` und `"satz": "0"`, beim Käufer `"ust_id": "DE987654321"`. Fehlt der Befreiungsgrund, setzt das Werkzeug den Standardtext "Steuerschuldnerschaft des Leistungsempfängers (§ 13b UStG)". In UBL steht die USt-IdNr. des Käufers in `cac:AccountingCustomerParty` unter `cac:PartyTaxScheme/cbc:CompanyID`. Die Steueraufschlüsselung aus [`xrechnung_ubl.xml`](../../beispiele/05_reverse_charge_13b/xrechnung_ubl.xml):

```xml
<cac:TaxTotal>
  <cbc:TaxAmount currencyID="EUR">0.00</cbc:TaxAmount>
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
</cac:TaxTotal>
```

In CII steht dasselbe in `ram:ApplicableTradeTax` mit `ram:CategoryCode` AE, `ram:RateApplicablePercent` 0 und `ram:ExemptionReason`; die USt-IdNr. des Käufers steht in `ram:SpecifiedTaxRegistration` mit `schemeID="VA"`.

Erstellen und prüfen:

```bash
erechnung erstellen beispiele/05_reverse_charge_13b/eingabe.json -o reverse_charge.xml
erechnung validieren reverse_charge.xml
```

```text
reverse_charge.xml: xrechnung-ubl, Rechnung RE-2026-0004, Zahlbetrag 18.500,00 EUR
reverse_charge.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
```

Ob eine Leistung unter § 13b UStG fällt, prüft das Werkzeug nicht. Das ist eine steuerliche Einordnung für die Steuerberatung.

## Innergemeinschaftliche Lieferung als E-Rechnung (Kategorie K)

Eine innergemeinschaftliche Lieferung geht an einen Unternehmer in einem anderen EU-Staat und wird mit Steuerkategorie K ausgewiesen. Die deutsche E-Rechnungspflicht gilt nach § 14 Abs. 2 Satz 2 Nr. 1 UStG nur, wenn beide Unternehmer im Inland ansässig sind. Für eine Lieferung nach Österreich ist die XRechnung also eine Möglichkeit, keine Pflicht aus dem UStG; das Format stimmen Sie mit dem Kunden ab.

| Angabe | Feld | Geprüft durch |
| --- | --- | --- |
| Steuerkategorie K | BT-151, BT-118 | Codeliste UNCL 5305 (BR-CL-18) |
| Steuersatz 0 an der Position, Steuerbetrag 0 | BT-152, BT-117 | BR-IC-05, BR-IC-09 |
| Befreiungsgrund | BT-120 bzw. BT-121 | BR-IC-10 |
| USt-IdNr. des Verkäufers | BT-31 | BR-IC-02 |
| USt-IdNr. des Käufers | BT-48 | BR-IC-02 |
| Lieferdatum und Lieferort | BT-72, BG-15 | in Beispiel 06 gesetzt |

Beispiel [`06_innergemeinschaftlich`](../../beispiele/06_innergemeinschaftlich/eingabe.json) liefert vier Gateways nach Wien. Der Käufer trägt die USt-IdNr. `ATU12345678` (gleiches Element `cac:PartyTaxScheme` wie oben). In `cac:Delivery` stehen Lieferdatum (`cbc:ActualDeliveryDate` 2026-10-12) und Lieferort in Wien mit Ländercode AT. Die Steuerkategorie aus [`xrechnung_ubl.xml`](../../beispiele/06_innergemeinschaftlich/xrechnung_ubl.xml):

```xml
<cac:TaxCategory>
  <cbc:ID>K</cbc:ID>
  <cbc:Percent>0</cbc:Percent>
  <cbc:TaxExemptionReason>Steuerfreie innergemeinschaftliche Lieferung (§ 4 Nr. 1b UStG)</cbc:TaxExemptionReason>
  <cac:TaxScheme>
    <cbc:ID>VAT</cbc:ID>
  </cac:TaxScheme>
</cac:TaxCategory>
```

```bash
erechnung erstellen beispiele/06_innergemeinschaftlich/eingabe.json -o eu_lieferung.xml
erechnung validieren eu_lieferung.xml
```

```text
eu_lieferung.xml: xrechnung-ubl, Rechnung RE-2026-0005, Zahlbetrag 3.560,00 EUR
eu_lieferung.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
```

## Steuerkategorien im Überblick

Die Steuerkategorie (BT-118 in der Aufschlüsselung, BT-151 an der Position) kommt aus der Codeliste UNCL 5305. Die deutschen Texte stehen in `src/erechnung/codelisten.py`:

| Code | Bedeutung | Befreiungsgrund in der Vorprüfung Pflicht |
| --- | --- | --- |
| S | Regelsteuersatz oder ermäßigter Satz | nein |
| Z | Nullsatz (Umsatzsteuer 0 %) | nein |
| E | Steuerbefreit (z. B. § 4 UStG, Kleinunternehmer § 19 UStG) | ja |
| AE | Steuerschuldnerschaft des Leistungsempfängers (Reverse Charge, § 13b UStG) | ja |
| K | Innergemeinschaftliche Lieferung oder Leistung | ja |
| G | Ausfuhrlieferung außerhalb der EU | ja |
| O | Nicht steuerbar | ja |
| L | Kanarische Inseln (IGIC) | nein |
| M | Ceuta und Melilla (IPSI) | nein |

Die letzte Spalte zeigt, wo die Vorprüfung des Werkzeugs einen Befreiungsgrund (BT-120 oder BT-121) verlangt; sie stützt sich auf die Regeln BR-E-10, BR-AE-10, BR-IC-10, BR-G-10 und BR-O-10. Fehlt der Grund bei AE, K, G oder O, setzt `erechnung erstellen` einen Standardtext ein.

## Beispiele

### Beispiel 1: Gutschrift in CII statt UBL

```bash
erechnung erstellen beispiele/03_gutschrift/eingabe.json --format xrechnung-cii -o gutschrift_cii.xml
erechnung validieren gutschrift_cii.xml
```

```text
gutschrift_cii.xml: xrechnung-cii, Rechnung GS-2026-0001, Zahlbetrag 285,60 EUR
gutschrift_cii.xml: XRechnung 3.0 (CII)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (CII), 0 Fehler, 0 Warnungen
```

Wenn der Empfänger CII verlangt; die Rechnungsart 381 steht dann in `ram:TypeCode`.

### Beispiel 2: Eingegangene Gutschrift lesen

```bash
erechnung lesen beispiele/03_gutschrift/xrechnung_ubl.xml
```

```text
Datei:        beispiele/03_gutschrift/xrechnung_ubl.xml
Format:       XRechnung 3.0 (UBL)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          381 (Rechnungskorrektur mit Minderung (Credit Note))
Nummer:       GS-2026-0001 vom 15.10.2026
...
Brutto:       285,60 EUR
```

Für die Buchhaltung, um auf einen Blick zu sehen, ob eine Rechnung oder eine Gutschrift vorliegt.

### Beispiel 3: Gutschrift im Sinne des UStG (389)

Die Eingabe ist Beispiel 01 mit `"nummer": "GS-2026-0100"` und `"art": "389"`.

```bash
erechnung erstellen gutschrift_389.json -o gutschrift_389.xml
erechnung validieren gutschrift_389.xml
```

```text
gutschrift_389.xml: xrechnung-ubl, Rechnung GS-2026-0100, Zahlbetrag 2.009,91 EUR
gutschrift_389.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
```

Der Code 389 bleibt ein UBL-Invoice. Das braucht man, wenn der Leistungsempfänger vereinbarungsgemäß selbst abrechnet.

### Beispiel 4: Reverse Charge ohne USt-IdNr. des Käufers

```bash
erechnung erstellen reverse_charge_ohne_ustid.json -o rc.xml
erechnung validieren rc.xml
```

```text
  FEHLER  VP-13B: Reverse Charge (AE) ohne USt-IdNr. des Käufers (BT-48).
rc.xml: xrechnung-ubl, Rechnung RE-2026-0004, Zahlbetrag 18.500,00 EUR
rc.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-AE-02: [BR-AE-02]-An Invoice that contains an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is "Reverse charge" shall contain the Seller VAT Identifier (BT-31), the Seller Tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63) and the Buyer VAT identifier (BT-48) and/or the Buyer legal registration identifier (BT-47).
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-13B: Reverse Charge (AE) ohne USt-IdNr. des Käufers (BT-48).
```

`erechnung erstellen` meldet den Fehler der Vorprüfung, schreibt die Datei aber trotzdem. Erst `erechnung validieren` liefert Exit-Code 1. Prüfen Sie deshalb jede erzeugte Datei.

### Beispiel 5: Innergemeinschaftliche Lieferung ohne USt-IdNr. des Käufers

```bash
erechnung validieren eu_ohne_ustid.xml
```

```text
eu_ohne_ustid.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-IC-02: [BR-IC-02]-An Invoice that contains an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is "Intra-community supply" shall contain the Seller VAT Identifier (BT-31) or the Seller tax representative VAT identifier (BT-63) and the Buyer VAT identifier (BT-48).
  ...
```

Die Datei ist Beispiel 06 ohne `ust_id` beim Käufer. Tragen Sie die USt-IdNr. des Kunden in `kaeufer.ust_id` ein.

### Beispiel 6: Teilrechnung (326)

```bash
erechnung erstellen teilrechnung.json -o teilrechnung.xml --validieren
```

```text
teilrechnung.xml: xrechnung-ubl, Rechnung TR-2026-0001, Zahlbetrag 2.009,91 EUR
  KoSIT: GÜLTIG (EN16931 XRechnung (UBL Invoice))
```

Die Eingabe ist Beispiel 01 mit `"art": "326"`. Für Abschläge bei längeren Projekten.

## Schritt für Schritt

1. Klären Sie mit der Steuerberatung, welcher Fall vorliegt: Minderung (381), Ersatz einer fehlerhaften Rechnung (384), Abrechnung durch den Leistungsempfänger (389), Teil- oder Schlussrechnung (326, 875-877), Reverse Charge (AE) oder innergemeinschaftliche Lieferung (K).
2. Holen Sie sich die Beispiele als Vorlage:
   ```bash
   erechnung beispiele ./meine-beispiele
   ```
3. Kopieren Sie die passende Eingabe (`03_gutschrift.json`, `04_rechnungskorrektur.json`, `05_reverse_charge_13b.json` oder `06_innergemeinschaftlich.json`) und tragen Sie Ihre Daten ein.
4. Setzen Sie die Rechnungsart im Feld `art`. Bei 381 und 384 tragen Sie Nummer und Datum der ursprünglichen Rechnung in `vorgaenger_nummer` und `vorgaenger_datum` ein.
5. Bei AE oder K setzen Sie an jeder betroffenen Position `kategorie` und `"satz": "0"`, tragen die USt-IdNr. des Käufers ein und, falls gewünscht, einen eigenen Befreiungsgrund in `befreiungsgruende`.
6. Erstellen Sie die Datei und prüfen Sie sie in einem Schritt:
   ```bash
   erechnung erstellen gutschrift.json -o gutschrift.xml --validieren
   ```
7. Lesen Sie die Ausgabe. Nur "GÜLTIG" ohne Fehler heißt: Die Datei erfüllt die KoSIT-Regeln. Ob die steuerliche Einordnung stimmt, prüft keine Validierung.
8. Versenden Sie die Datei und bewahren Sie sie auf, laut BMF-Schreiben vom 15.10.2025, Rn. 60, acht Jahre.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Rechnungsart außerhalb von BR-DE-17 | `Rechnungsart 383 ist in XRechnung nicht erlaubt (BR-DE-17).` | Einen der acht erlaubten Codes nehmen |
| Korrektur ohne Bezug | Warnung BR-DE-26 bei Code 384 | `vorgaenger_nummer` und `vorgaenger_datum` setzen |
| 389 und 381 verwechselt | Empfänger bucht Abrechnung und Minderung falsch | Tabelle oben prüfen: Wer stellt aus? |
| Reverse Charge ohne USt-IdNr. des Käufers | `BR-AE-02` und `VP-13B` | `kaeufer.ust_id` eintragen |
| Innergemeinschaftliche Lieferung ohne USt-IdNr. des Käufers | `BR-IC-02` und `VP-IG` | USt-IdNr. des Kunden eintragen |
| Steuersatz größer 0 bei AE oder K | `erechnung erstellen` rechnet Steuer aus, die Prüfung meldet `BR-AE-05` und `BR-AE-09` bzw. `BR-IC-05` und `BR-IC-09` | `"satz": "0"` an der Position setzen |
| Datei trotz Vorprüfungsfehler verschickt | `erechnung erstellen` endet mit Exit-Code 0 | Immer mit `--validieren` erstellen oder danach `erechnung validieren` aufrufen |

## Häufige Fragen

### Wie erstelle ich eine Gutschrift als E-Rechnung?

Setzen Sie die Rechnungsart 381, tragen Sie die Beträge positiv ein und verweisen Sie in BG-3 auf die ursprüngliche Rechnung. `erechnung erstellen` schreibt daraus in UBL ein `CreditNote`-Dokument, das die KoSIT-Prüfung im Szenario "UBL CreditNote" bestätigt.

### Was ist der Unterschied zwischen 381 und 389?

381 mindert eine Rechnung des Leistenden (Credit Note), 389 ist eine Rechnung, die der Leistungsempfänger ausstellt (Self-billed invoice, Gutschrift nach § 14 Abs. 2 Satz 5 UStG). Welche Variante vorliegt, klären Sie mit der Steuerberatung.

### Muss eine Rechnungskorrektur die alte Rechnungsnummer enthalten?

Laut XRechnung-Regel BR-DE-26 soll eine Rechnung mit Code 384 mindestens einen Verweis BG-3 auf die Vorgängerrechnung enthalten. Fehlt er, gibt die KoSIT-Prüfung eine Warnung aus, die Datei bleibt formal gültig.

### Wie storniere ich eine E-Rechnung?

Einen eigenen Storno-Code kennt die XRechnung nicht. Technisch möglich sind eine Gutschrift 381 über den vollen Betrag mit Bezug BG-3 oder eine korrigierte Rechnung 384; den passenden Weg stimmen Sie mit der Steuerberatung ab.

### Wie sieht Reverse Charge in der XRechnung aus?

Position und Steueraufschlüsselung tragen Steuerkategorie AE mit Steuersatz 0, dazu kommen ein Befreiungsgrund (BT-120) und die USt-IdNr. des Käufers (BT-48); Beispiel 05 im Repo ist eine gültige Datei.

### Brauche ich für eine innergemeinschaftliche Lieferung eine E-Rechnung?

Die deutsche E-Rechnungspflicht gilt nach § 14 Abs. 2 Satz 2 Nr. 1 UStG nur, wenn beide Unternehmer im Inland ansässig sind. Für Kunden in anderen EU-Staaten ist eine XRechnung mit Kategorie K möglich; das Format vereinbaren Sie mit dem Kunden.

### Welche Rechnungsart nehme ich für eine Abschlagsrechnung?

Die XRechnung kennt 326 (Teilrechnung) und für Bauleistungen 875, 876 und 877. Abschläge in der Schlussrechnung ziehen Sie über die Vorauszahlung BT-113 ab.

> **Hinweis:** Diese Anleitung erklärt Gesetz, BMF-Schreiben und technische Standards nach dem Stand vom 15.10.2026. Sie ist keine Steuer- oder Rechtsberatung, die Autoren sind keine Steuerberater. Für die Beurteilung eines konkreten Falls wenden Sie sich an Ihre Steuerberatung oder Ihr Finanzamt. Alle Angaben ohne Gewähr.

## Weiterlesen

- [E-Rechnung erstellen](./e-rechnung-erstellen.md)
- [E-Rechnung prüfen: Validator mit den offiziellen Regeln](./e-rechnung-validator.md)
- [E-Rechnung Fehlermeldungen beheben](./e-rechnung-fehlermeldungen.md)
- [XRechnung: Format, Aufbau und Pflichtfelder](./xrechnung.md)
- [DATEV und E-Rechnung](./datev-e-rechnung.md)
- Beispiele: [`03_gutschrift`](../../beispiele/03_gutschrift/xrechnung_ubl.xml), [`04_rechnungskorrektur`](../../beispiele/04_rechnungskorrektur/xrechnung_ubl.xml), [`05_reverse_charge_13b`](../../beispiele/05_reverse_charge_13b/xrechnung_ubl.xml), [`06_innergemeinschaftlich`](../../beispiele/06_innergemeinschaftlich/xrechnung_ubl.xml), Übersicht: [`beispiele/README.md`](../../beispiele/README.md)
