# E-Rechnung Fehlermeldungen: BR-DE-15, BR-CO-26 und andere Validierungsfehler beheben

Die Fehlermeldung BR-DE-15 bedeutet, dass in einer XRechnung die Käuferreferenz BT-10 fehlt; behoben wird sie mit einem Element `cbc:BuyerReference` (UBL) bzw. `ram:BuyerReference` (CII). Jede Validierungsmeldung besteht aus einem Regel-Code (BR-DE-... für deutsche XRechnung-Regeln, BR-CO-... für Rechenregeln der EN 16931, PEPPOL-... für übernommene Peppol-Regeln), einer Stufe und einem Text, der das betroffene BT-Feld nennt. Diese Referenz zeigt die häufigen Meldungen wörtlich, mit Ursache, Lösung als XML vorher und nachher und einer vorsichtigen umsatzsteuerlichen Einordnung.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil von [E-Rechnung in Python](../../README.md).

## Das Wichtigste in Kürze

- Alle Meldungen unten sind echt: Sie stammen aus `erechnung validieren` mit der KoSIT-Prüfkonfiguration `xrechnung-3.0.2-validator-configuration-2026-08-31`, angewendet auf absichtlich veränderte Dateien aus `beispiele/`.
- Stufe `FEHLER` macht die Rechnung ungültig, `WARNUNG` nicht; welche Stufe gilt, legt das Prüfszenario fest.
- Schemafehler (`XSD`) zuerst beheben: Solange das XML-Schema verletzt ist, laufen die Geschäftsregeln nicht, und weitere Fehler bleiben unsichtbar.
- Laut BMF-Schreiben vom 15.10.2025 sind Formatfehler (Rn. 6a) keine E-Rechnung, Fehler bei Pflichtangaben nach § 14 Abs. 4 UStG machen die Rechnung nicht ordnungsmäßig, andere Geschäftsregelfehler wie ein fehlendes BT-10 sind umsatzsteuerlich unbeachtlich (Rn. 35a).
- Die Zeilen mit `VP-` stammen aus der eigenen Vorprüfung des Werkzeugs; sie erklären auf Deutsch, maßgeblich ist die KoSIT-Meldung.

## Übersicht: alle Codes auf dieser Seite

| Code | Stufe | Worum es geht | Felder |
| --- | --- | --- | --- |
| [BR-DE-15](#br-de-15) | Fehler | Käuferreferenz fehlt | BT-10 |
| [BR-DE-2, BR-DE-6, BR-DE-7](#br-de-2-br-de-6-und-br-de-7) | Fehler | Kontakt des Verkäufers fehlt oder unvollständig | BG-6, BT-41 bis BT-43 |
| [BR-DE-27, BR-DE-28](#br-de-27-und-br-de-28) | Warnung | Telefon oder E-Mail falsch geschrieben | BT-42, BT-43 |
| [BR-DE-4](#br-de-4) | Fehler | Postleitzahl des Verkäufers fehlt | BT-38 |
| [PEPPOL-EN16931-R020, R010](#peppol-en16931-r020-und-r010) | Fehler | elektronische Adresse fehlt | BT-34, BT-49 |
| [PEPPOL-EN16931-R001](#peppol-en16931-r001) | Fehler | Geschäftsprozess fehlt | BT-23 |
| [BR-CO-26, BR-S-02, BR-DE-16](#br-co-26-br-s-02-und-br-de-16) | Fehler | Kennung oder USt-IdNr. des Verkäufers fehlt | BT-29 bis BT-32 |
| [BR-DE-1](#br-de-1) | Fehler | Zahlungsangaben fehlen | BG-16, BT-81 |
| [BR-DE-23-a, BR-61](#br-de-23-a-und-br-61) | Fehler | IBAN fehlt bei Überweisung (58) | BG-17, BT-84 |
| [BR-DE-19](#br-de-19) | Warnung | IBAN hat falsche Prüfziffer | BT-84 |
| [BR-DE-30, BR-DE-31](#br-de-30-und-br-de-31) | Fehler | Gläubiger-ID oder Konto fehlt bei Lastschrift (59) | BT-90, BT-91 |
| [BR-DE-18](#br-de-18) | Fehler | Skonto-Zeile falsch aufgebaut | BT-20 |
| [BR-CO-16](#br-co-16) | Fehler | Zahlbetrag stimmt nicht | BT-115 |
| [BR-CO-15](#br-co-15) | Fehler | Bruttobetrag stimmt nicht | BT-112 |
| [BR-CO-10, BR-CO-13](#br-co-10-und-br-co-13) | Fehler | Summe der Positionen stimmt nicht | BT-106, BT-109, BT-131 |
| [BR-CO-14](#br-co-14) | Fehler | Steuersumme stimmt nicht | BT-110, BT-117 |
| [BR-CO-17, BR-S-08, BR-S-09](#br-co-17-br-s-08-und-br-s-09) | Fehler | Steuersatz passt nicht zu Betrag oder Positionen | BT-117, BT-119 |
| [BR-AE-10](#br-ae-10) | Fehler | Reverse Charge ohne Hinweistext | BT-120, BT-121 |
| [BR-DE-17, BR-CL-01](#br-de-17-und-br-cl-01) | Warnung, Fehler | Rechnungsart nicht erlaubt | BT-3 |
| [BR-DE-26](#br-de-26) | Warnung | Rechnungskorrektur ohne Bezug | BG-3 |
| [BR-CL-23](#br-cl-23) | Warnung | Einheitencode unbekannt | BT-130 |
| [XSD](#xsd) | Fehler | Schemafehler: Datum, Reihenfolge, Elementname | alle |
| [CII-DT-097, BR-TMP-7](#cii-dt-097-und-br-tmp-7) | Fehler, Warnung | Datum in CII falsch formatiert | BT-2 |
| [SZENARIO, VP-LESEN](#szenario-und-vp-lesen) | Fehler | Datei nicht prüfbar | BT-24 |
| [BR-DE-TMP-32](#br-de-tmp-32) | Information | Liefer- oder Leistungsdatum fehlt | BT-72, BG-14, BG-26 |

## So entsteht eine Fehlermeldung

Ein Validator wählt anhand von BT-24 das Prüfszenario, prüft das XML-Schema und dann die Schematron-Regeln der EN 16931 und der XRechnung. Jede verletzte Regel ergibt eine Zeile wie `FEHLER  BR-DE-15: [BR-DE-15] ...`, darunter folgen die Erklärungen der Vorprüfung (Ablauf und Optionen in [E-Rechnung prüfen](./e-rechnung-validator.md)). Die Texte der EN-16931-Regeln sind englisch, die der BR-DE-Regeln deutsch. Die XML-Ausschnitte unten sind UBL aus `beispiele/01_standard/xrechnung_ubl.xml`, wenn nicht anders angegeben.

## Pflichtangaben und Adressen

### BR-DE-15

`[BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.`

Ursache: Die Käuferreferenz fehlt. In der XRechnung ist BT-10 Pflicht, in UBL und CII gleich. Bei Behörden steht hier die Leitweg-ID, im B2B eine Referenz des Kunden. Vorprüfung: `VP-BR-DE-15`. Umsatzsteuer: Das BMF-Schreiben vom 15.10.2025 nennt genau diesen Fall (Rn. 6b) und stuft ihn als umsatzsteuerlich unbeachtlich ein (Rn. 35a). Laut BMF-FAQ genügt im B2B ein Platzhalter wie "-". Der Empfänger kann die Datei trotzdem technisch ablehnen.

```xml
<!-- vorher -->
<cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
<cac:InvoicePeriod>
<!-- nachher, UBL -->
<cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
<cbc:BuyerReference>BH-2026-0815</cbc:BuyerReference>
<cac:InvoicePeriod>
<!-- nachher, CII: erstes Element in ram:ApplicableHeaderTradeAgreement -->
<ram:ApplicableHeaderTradeAgreement>
  <ram:BuyerReference>BH-2026-0815</ram:BuyerReference>
```

### BR-DE-2, BR-DE-6 und BR-DE-7

`[BR-DE-2] Die Gruppe "SELLER CONTACT" (BG-6) muss übermittelt werden.`
`[BR-DE-6] Das Element "Seller contact telephone number" (BT-42) muss übermittelt werden.`
`[BR-DE-7] Das Element "Seller contact email address" (BT-43) muss übermittelt werden.`

Ursache: Der Kontakt des Verkäufers fehlt ganz (BR-DE-2) oder ihm fehlt Telefon (BR-DE-6) bzw. E-Mail (BR-DE-7). Fehlt nur ein Element, kommt zusätzlich BR-DE-27 bzw. BR-DE-28 als Warnung. Vorprüfung: `VP-BR-DE-2`. Umsatzsteuer: kein Pflichtfeld nach § 14 Abs. 4 UStG, nach Rn. 35a voraussichtlich unbeachtlich.

```xml
<!-- nachher: in cac:AccountingSupplierParty/cac:Party, nach cac:PartyLegalEntity -->
<cac:Contact>
  <cbc:Name>Erika Mustermann</cbc:Name>
  <cbc:Telephone>+49 40 1234567</cbc:Telephone>
  <cbc:ElectronicMail>buchhaltung@nordlicht.example</cbc:ElectronicMail>
</cac:Contact>
```

### BR-DE-27 und BR-DE-28

`[BR-DE-27] In BT-42 sollen mindestens drei Ziffern enthalten sein.`
`[BR-DE-28] In BT-43 soll genau ein @-Zeichen enthalten sein, welches nicht von einem Leerzeichen, einem Punkt, aber mindestens zwei Zeichen auf beiden Seiten flankiert werden soll. Ein Punkt sollte nicht am Anfang oder am Ende stehen.`

Ursache: Telefon wie `-` oder E-Mail wie `buchhaltung(at)nordlicht.example`. Nur Warnungen, die Rechnung bleibt gültig. Lösung: `<cbc:Telephone>+49 40 1234567</cbc:Telephone>` und `<cbc:ElectronicMail>buchhaltung@nordlicht.example</cbc:ElectronicMail>`. Umsatzsteuer: unbeachtlich (keine Pflichtangabe).

### BR-DE-4

`[BR-DE-4] Das Element "Seller post code" (BT-38) muss übermittelt werden.`

Ursache: Die Postleitzahl des Verkäufers fehlt. Fehlt der Ort, kommt BR-DE-3; beim Käufer BR-DE-8 (Ort) und BR-DE-9 (PLZ). Vorprüfung: `VP-14-4-1`. Umsatzsteuer: Die Anschrift ist Pflichtangabe nach § 14 Abs. 4 Nr. 1 UStG; laut Rn. 35a kann eine unvollständige Anschrift die Rechnung nicht ordnungsmäßig machen. Mit der Steuerberatung klären. Lösung: nach `<cbc:CityName>Hamburg</cbc:CityName>` die Zeile `<cbc:PostalZone>20095</cbc:PostalZone>` ergänzen.

### PEPPOL-EN16931-R020 und R010

`[PEPPOL-EN16931-R020]-Seller electronic address MUST be provided`
`[PEPPOL-EN16931-R010]-Buyer electronic address MUST be provided`

Ursache: `cbc:EndpointID` fehlt beim Verkäufer (BT-34) oder Käufer (BT-49). In XRechnung 3.0 ist beides über die übernommenen Peppol-Regeln Pflicht. `schemeID="EM"` steht für E-Mail, `0204` für die Leitweg-ID (siehe `beispiele/08_b2g_leitweg_id`). Vorprüfung: `VP-BR-DE-ADR`. Umsatzsteuer: keine Pflichtangabe, nach Rn. 35a voraussichtlich unbeachtlich.

```xml
<!-- nachher: erstes Element in cac:Party -->
<cbc:EndpointID schemeID="EM">rechnung@nordlicht.example</cbc:EndpointID>
```

### PEPPOL-EN16931-R001

`[PEPPOL-EN16931-R001]-Business process MUST be provided.`

Ursache: `cbc:ProfileID` (BT-23) fehlt. Die Vorprüfung meldet das nicht. Lösung: direkt nach `cbc:CustomizationID` die Zeile `<cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>` einfügen. Umsatzsteuer: unbeachtlich (technische Angabe).

### BR-CO-26, BR-S-02 und BR-DE-16

`[BR-CO-26]-In order for the buyer to automatically identify a supplier, the Seller identifier (BT-29), the Seller legal registration identifier (BT-30) and/or the Seller VAT identifier (BT-31) shall be present.`
`[BR-S-02]-An Invoice that contains an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is "Standard rated" shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).`
`[BR-DE-16] Wenn in einer Rechnung die Steuercodes S, Z, E, AE, K, G, L oder M verwendet werden, muss mindestens eines der Elemente "Seller VAT identifier" (BT-31), "Seller tax registration identifier" (BT-32) oder "SELLER TAX REPRESENTATIVE PARTY" (BG-11) übermittelt werden.`

Ursache, Fall 1: USt-IdNr. und Handelsregisternummer entfernt, dann kommen alle drei Meldungen, Vorprüfung `VP-14-4-2`. Fall 2: Ein Kleinunternehmer gibt nur die Steuernummer an (BT-32) und keine Lieferantennummer (BT-29). Dann kommt BR-CO-26 allein, weil die Steuernummer für BR-CO-26 nicht zählt. Umsatzsteuer: Fall 1 betrifft die Pflichtangabe nach § 14 Abs. 4 Nr. 2 UStG, laut Rn. 35a kann die Rechnung dann nicht ordnungsmäßig sein. Fall 2 betrifft keine Pflichtangabe, voraussichtlich unbeachtlich.

Lösung Fall 1: `cac:PartyTaxScheme` mit `<cbc:CompanyID>DE123456789</cbc:CompanyID>` und `<cbc:ID>VAT</cbc:ID>` wieder einfügen (wie in `beispiele/01_standard`). Lösung Fall 2:

```xml
<!-- beispiele/07_kleinunternehmer: Kennung BT-29 in cac:Party vor cac:PostalAddress -->
<cac:PartyIdentification>
  <cbc:ID>LIEF-0815</cbc:ID>
</cac:PartyIdentification>
```

## Zahlungsangaben

### BR-DE-1

`[BR-DE-1] Eine Rechnung (INVOICE) muss Angaben zu "PAYMENT INSTRUCTIONS" (BG-16) enthalten.`

Ursache: `cac:PaymentMeans` fehlt ganz, also auch die Zahlungsart BT-81. Vorprüfung: `VP-BR-DE-1`. Umsatzsteuer: keine Pflichtangabe, nach Rn. 35a voraussichtlich unbeachtlich.

```xml
<cac:PaymentMeans>
  <cbc:PaymentMeansCode>58</cbc:PaymentMeansCode>
  <cbc:PaymentID>RE-2026-0001</cbc:PaymentID>
  <cac:PayeeFinancialAccount>
    <cbc:ID>DE79000000001234567890</cbc:ID>
    <cbc:Name>Nordlicht Software GmbH</cbc:Name>
  </cac:PayeeFinancialAccount>
</cac:PaymentMeans>
```

### BR-DE-23-a und BR-61

`[BR-61]-If the Payment means type code (BT-81) means SEPA credit transfer, Local credit transfer or Non-SEPA international credit transfer, the Payment account identifier (BT-84) shall be present.`
`[BR-DE-23-a] Wenn BT-81 "Payment means type code" einen Schlüssel für Überweisungen enthält (30, 58), muss BG-17 "CREDIT TRANSFER" übermittelt werden.`

Ursache: Zahlungsart 58 (SEPA-Überweisung), aber `cac:PayeeFinancialAccount` mit der IBAN fehlt. Dazu kommt BR-DE-19 als Warnung. Die Vorprüfung meldet das nicht. Lösung: den Block `cac:PayeeFinancialAccount` aus dem Abschnitt BR-DE-1 einfügen. Umsatzsteuer: keine Pflichtangabe, voraussichtlich unbeachtlich.

### BR-DE-19

`[BR-DE-19] "Payment account identifier" (BT-84) soll eine korrekte IBAN enthalten, wenn in "Payment means type code" (BT-81) mit dem Code 58 SEPA als Zahlungsmittel gefordert wird.`

Ursache: IBAN mit falscher Prüfziffer, z.B. `DE79000000001234567891`. Nur Warnung. Vorprüfung: `VP-IBAN: IBAN DE79000000001234567891 hat eine falsche Prüfziffer.` Lösung: IBAN korrigieren. Bei Lastschrift (59) heißt die entsprechende Warnung BR-DE-20 und betrifft BT-91. Umsatzsteuer: unbeachtlich, aber der Kunde kann nicht zahlen.

### BR-DE-30 und BR-DE-31

`[BR-DE-30] Wenn "DIRECT DEBIT" BG-19 vorhanden ist, dann muss "Bank assigned creditor identifier" BT-90 übermittelt werden.`
`[BR-DE-31] Wenn "DIRECT DEBIT" BG-19 vorhanden ist, dann muss "Debited account identifier" BT-91 übermittelt werden.`

Ursache: SEPA-Lastschrift (Code 59) ohne Gläubiger-ID bzw. ohne IBAN des Zahlers. Die Vorprüfung meldet das nicht. Umsatzsteuer: keine Pflichtangabe, voraussichtlich unbeachtlich. XML aus `beispiele/09_sepa_lastschrift`:

```xml
<!-- BT-90: in cac:AccountingSupplierParty/cac:Party -->
<cac:PartyIdentification>
  <cbc:ID schemeID="SEPA">DE98ZZZ09999999999</cbc:ID>
</cac:PartyIdentification>
<!-- BT-91: im Mandat -->
<cac:PaymentMandate>
  <cbc:ID>MANDAT-2026-001</cbc:ID>
  <cac:PayerFinancialAccount>
    <cbc:ID>DE79000000001234567890</cbc:ID>
  </cac:PayerFinancialAccount>
</cac:PaymentMandate>
```

### BR-DE-18

`[BR-DE-18] Skonto Zeilen in Invoice müssen diesem regulärem Ausdruck entsprechen: (^|\r?\n)#(SKONTO)#TAGE=([0-9]+#PROZENT=[0-9]+\.[0-9]{2})(#BASISBETRAG=-?[0-9]+\.[0-9]{2})?#$. Die Informationen zur Gewährung von Skonto müssen wie folgt im Element "Payment terms" (BT-20) übermittelt werden: ...` (gekürzt)

Ursache: Skonto als freier Text in der Skonto-Syntax, z.B. `#SKONTO#10 Tage 2 %#`. Umsatzsteuer: keine Pflichtangabe, voraussichtlich unbeachtlich.

```xml
<!-- vorher -->
<cbc:Note>#SKONTO#10 Tage 2 %#
<!-- nachher: Großbuchstaben, zwei Nachkommastellen, Zeilenumbruch danach -->
<cbc:Note>#SKONTO#TAGE=10#PROZENT=2.00#
Zahlbar innerhalb von 30 Tagen ohne Abzug.</cbc:Note>
```

## Beträge und Steuern

### BR-CO-16

`[BR-CO-16]-Amount due for payment (BT-115) = Invoice total amount with VAT (BT-112) -Paid amount (BT-113) +Rounding amount (BT-114).`

Ursache: Der Zahlbetrag passt nicht zu Brutto, Vorauszahlung und Rundung. Kommt auch als Folgefehler von BR-CO-15. Vorprüfung: `VP-ZAHLBETRAG`. Umsatzsteuer: Der Zahlbetrag ist keine eigene Pflichtangabe nach § 14 Abs. 4 UStG; die Einordnung mit der Steuerberatung klären. Lösung: vorher `<cbc:PayableAmount currencyID="EUR">2010.91</cbc:PayableAmount>`, nachher `2009.91` wie `cbc:TaxInclusiveAmount`.

### BR-CO-15

`[BR-CO-15]-Invoice total amount with VAT (BT-112) = Invoice total amount without VAT (BT-109) + Invoice total VAT amount (BT-110).`

Ursache: Brutto ist nicht Netto plus Steuer. Hier `2019.91` statt `1689.00 + 320.91 = 2009.91`; dazu kommt BR-CO-16. Vorprüfung: `VP-BRUTTO`. Lösung: `<cbc:TaxInclusiveAmount currencyID="EUR">2009.91</cbc:TaxInclusiveAmount>`. Umsatzsteuer: Rechenfehler in den Summen mit der Steuerberatung klären.

### BR-CO-10 und BR-CO-13

`[BR-CO-10]-Sum of Invoice line net amount (BT-106) = Σ Invoice line net amount (BT-131).`
`[BR-CO-13]-Invoice total amount without VAT (BT-109) = Σ Invoice line net amount (BT-131) - Sum of allowances on document level (BT-107) + Sum of charges on document level (BT-108).`

Ursache: Die Positionssumme BT-106 (`1698.00`) passt nicht zu den Positionen (`1440.00 + 249.00 = 1689.00`). Vorprüfung: `VP-SUMME`, `VP-NETTO`. Lösung: `<cbc:LineExtensionAmount currencyID="EUR">1689.00</cbc:LineExtensionAmount>` in `cac:LegalMonetaryTotal`. Umsatzsteuer: betrifft das Entgelt, eine Pflichtangabe nach § 14 Abs. 4 UStG; mit der Steuerberatung klären.

### BR-CO-14

`[BR-CO-14]-Invoice total VAT amount (BT-110) = Σ VAT category tax amount (BT-117).`

Ursache: Die Steuersumme im Kopf (`320.91`) passt nicht zur Aufschlüsselung (`320.19`). Vorprüfung: `VP-STEUER`, `VP-STEUERSATZ`. Umsatzsteuer: Steuerbetrag ist Pflichtangabe nach § 14 Abs. 4 Nr. 8 UStG; laut Rn. 35a kann die Rechnung dann nicht ordnungsmäßig sein. Lösung: in `cac:TaxSubtotal` vorher `<cbc:TaxAmount currencyID="EUR">320.19</cbc:TaxAmount>`, nachher `320.91` (19 % von 1689.00).

### BR-CO-17, BR-S-08 und BR-S-09

`[BR-CO-17]-VAT category tax amount (BT-117) = VAT category taxable amount (BT-116) x (VAT category rate (BT-119) / 100), rounded to two decimals.`
`[BR-S-08]-For each different value of VAT category rate (BT-119) where the VAT category code (BT-118) is "Standard rated", the VAT category taxable amount (BT-116) in a VAT breakdown (BG-23) shall equal the sum of Invoice line net amounts (BT-131) ...` (gekürzt)
`[BR-S-09]-The VAT category tax amount (BT-117) in a VAT breakdown (BG-23) where VAT category code (BT-118) is "Standard rated" shall equal the VAT category taxable amount (BT-116) multiplied by the VAT category rate (BT-119).`

Ursache: In der Steueraufschlüsselung steht 16 %, die Positionen haben 19 %, und der Betrag 320.91 passt nicht zu 16 % von 1689.00. Vorprüfung: `VP-STEUERSATZ: S 16 %: Steuer 320.91 auf Basis 1689.00 ergibt nicht 270.24.` Umsatzsteuer: Steuersatz und Steuerbetrag sind Pflichtangaben nach § 14 Abs. 4 Nr. 8 UStG; das BMF nennt "Steuerbetrag passt rechnerisch nicht zum Steuersatz" ausdrücklich als Beispiel (Rn. 6b). Mit der Steuerberatung klären.

```xml
<cac:TaxCategory>
  <cbc:ID>S</cbc:ID>
  <cbc:Percent>19</cbc:Percent>  <!-- vorher 16, gleich wie in den Positionen -->
```

### BR-AE-10

`[BR-AE-10]-A VAT breakdown (BG-23) with VAT Category code (BT-118) "Reverse charge" shall have a VAT exemption reason code (BT-121), meaning "Reverse charge" or the VAT exemption reason text (BT-120) "Reverse charge" (or the equivalent standard text in another language).`

Ursache: Steuerkategorie AE (§ 13b UStG) ohne Hinweistext. Vorprüfung: `VP-14-4-8`. Umsatzsteuer: Der Hinweis auf die Steuerschuldnerschaft des Leistungsempfängers ist Pflichtangabe (§ 14a UStG); laut Rn. 35a kann die Rechnung dann nicht ordnungsmäßig sein. XML aus `beispiele/05_reverse_charge_13b`:

```xml
<cbc:ID>AE</cbc:ID>
<cbc:Percent>0</cbc:Percent>
<cbc:TaxExemptionReason>Steuerschuldnerschaft des Leistungsempfängers (§ 13b UStG)</cbc:TaxExemptionReason>
```

## Codes und Codelisten

### BR-DE-17 und BR-CL-01

`[BR-DE-17] Mit dem Element "Invoice type code" (BT-3) sollen ausschließlich folgende Codes aus der Codeliste UNTDID 1001 übermittelt werden: 326 (Partial invoice), 380 (Commercial invoice), 384 (Corrected invoice), 389 (Self-billed invoice) und 381 (Credit note),875 (Partial construction invoice), 876 (Partial final construction invoice), 877 (Final construction invoice).`
`[BR-CL-01]-The document type code MUST be coded by the invoice and credit note related code lists of UNTDID 1001.`

Ursache: Ein Code, den XRechnung nicht vorsieht (z.B. 382), ergibt nur BR-DE-17 als Warnung; die Rechnung bleibt gültig. Ein Code, den es in UNTDID 1001 nicht gibt (z.B. 999), ergibt zusätzlich BR-CL-01 als Fehler. `erechnung erstellen` lehnt solche Codes schon beim Erzeugen ab (siehe Beispiel 4). Lösung: `<cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>`. Umsatzsteuer: keine Pflichtangabe, voraussichtlich unbeachtlich.

### BR-DE-26

`[BR-DE-26] Wenn im Element "Invoice type code" (BT-3) der Code 384 (Corrected invoice) übergeben wird, soll PRECEDING INVOICE REFERENCE BG-3 mind. einmal vorhanden sein.`

Ursache: Rechnungskorrektur ohne Verweis auf die ursprüngliche Rechnung. Warnung. XML aus `beispiele/04_rechnungskorrektur` (nach `cbc:BuyerReference`). Umsatzsteuer: Ob eine Berichtigung wirksam ist, mit der Steuerberatung klären.

```xml
<cac:BillingReference>
  <cac:InvoiceDocumentReference>
    <cbc:ID>RE-2026-0002</cbc:ID>
    <cbc:IssueDate>2026-10-15</cbc:IssueDate>
  </cac:InvoiceDocumentReference>
</cac:BillingReference>
```

### BR-CL-23

`[BR-CL-23]-Unit code MUST be coded according to the UN/ECE Recommendation 20 with Rec 21 extension`

Ursache: Einheit wie `Std`, `STD` oder `Stück` statt eines UN/ECE-Codes. Im XRechnung-Szenario ist das nur eine Warnung (Umstufung, ursprünglich Fehler), in einem reinen EN-16931-Szenario wie bei ZUGFeRD ein Fehler. Vorprüfung: `VP-EINHEIT`, aber nur bei Schreibweisen wie `Std` oder `Stück`, nicht bei `STD`. Gängige Codes: C62 (one), H87 (Stück), HUR (Stunde), DAY (Tag), MON (Monat), LS (Pauschale). Umsatzsteuer: Menge und Art der Leistung sind Pflichtangaben, ein falscher Code macht die Angabe aber nicht unbedingt unvollständig; im Zweifel mit der Steuerberatung klären.

```xml
<cbc:InvoicedQuantity unitCode="HUR">12</cbc:InvoicedQuantity>  <!-- vorher unitCode="Std" -->
```

## Schema, Datum und nicht prüfbare Dateien

### XSD

`Element '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueDate': '15.10.2026' is not a valid value of the atomic type 'xs:date'.`
`Element '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}DueDate': This element is not expected. Expected is one of ( {...}CopyIndicator, {...}UUID, {...}IssueDate ).`

Ursache: Die erste Meldung kommt bei einem deutschen Datum (UBL verlangt `JJJJ-MM-TT`), die zweite bei falscher Reihenfolge: `cbc:DueDate` steht vor `cbc:IssueDate`. UBL schreibt die Reihenfolge der Elemente fest vor. Stecken beide Fehler in einer Datei, meldet das Werkzeug nur den ersten (die Reihenfolge). Nach einem Schemafehler laufen keine Geschäftsregeln (siehe Beispiel 2). Die Vorprüfung meldet beim deutschen Datum `VP-14-4-3: Rechnungsdatum fehlt`, weil sie das Datum nicht lesen kann. Umsatzsteuer: Formatfehler nach Rn. 6a; laut BMF ist die Datei keine E-Rechnung, sondern eine sonstige Rechnung.

```xml
<!-- vorher: beide Fehler -->
<cbc:DueDate>2026-11-14</cbc:DueDate>
<cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
<cbc:IssueDate>15.10.2026</cbc:IssueDate>
<!-- nachher -->
<cbc:IssueDate>2026-10-15</cbc:IssueDate>
<cbc:DueDate>2026-11-14</cbc:DueDate>
<cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
```

### CII-DT-097 und BR-TMP-7

`[CII-DT-097] - Date time string with format attribute 102 shall be YYYYMMDD.`
`[BR-TMP-7] Datumsangaben in UNCEFACT/CII müssen das Attribut format="102" tragen und im Format JJJJMMTT (YYYYMMDD) übermittelt werden.`

Ursache: In CII steht ein Datum mit Bindestrichen. Das ist kein Schemafehler, sondern ein Geschäftsregelfehler. Umsatzsteuer: Das Datum ist vorhanden, nur falsch formatiert; die Einordnung mit der Steuerberatung klären.

```xml
<ram:IssueDateTime>
  <udt:DateTimeString format="102">20261015</udt:DateTimeString>  <!-- vorher 2026-10-15 -->
</ram:IssueDateTime>
```

### SZENARIO und VP-LESEN

`SZENARIO: Kein passendes Prüfszenario. Erwartet wird UBL Invoice/CreditNote oder CII mit einer Spezifikationskennung (BT-24) für XRechnung 3.0 oder EN 16931.`
`VP-LESEN: Kein wohlgeformtes XML: Opening and ending tag mismatch: Note line 9 and Notiz, line 9, column 55 (<string>, line 9)`
`VP-LESEN: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.`

Ursache: `SZENARIO` kommt bei einer Kennung ohne Prüfszenario, z.B. ZUGFeRD MINIMUM (`urn:factur-x.eu:1p0:minimum`, dazu `VP-FORMAT`). `VP-LESEN` kommt bei kaputtem XML oder einem PDF ohne XML; der Exit-Code ist dann 2. Umsatzsteuer: MINIMUM und BASIC WL sind laut UStAE 14.1 Abs. 14 keine E-Rechnung, ein reines PDF ist eine sonstige Rechnung, kaputtes XML ein Formatfehler (Rn. 6a).

### BR-DE-TMP-32

`[BR-DE-TMP-32] Eine Rechnung sollte zur Angabe des Liefer-/Leistungsdatums entweder BT-72 "Actual delivery date", BG-14 "Invoicing period" oder in jeder Rechnungsposition BG-26 "Invoice line period" enthalten.`

Ursache: kein Liefer- oder Leistungsdatum. Nur Information, sichtbar mit `--alle`; die Vorprüfung meldet `VP-14-4-6` als Warnung. Umsatzsteuer: Pflichtangabe nach § 14 Abs. 4 Nr. 6 UStG, außer es entspricht dem Rechnungsdatum und das ist vermerkt.

```xml
<cac:InvoicePeriod>
  <cbc:StartDate>2026-09-01</cbc:StartDate>
  <cbc:EndDate>2026-09-30</cbc:EndDate>
</cac:InvoicePeriod>
```

## Beispiele

### Beispiel 1: Nur die Fehlercodes einer Datei ausgeben

```console
$ erechnung validieren --json ohne_bt10.xml > ergebnis.json
$ python3 -c 'import json; e = json.load(open("ergebnis.json")); print([b["code"] for b in e["offiziell"]["befunde"]])'
['BR-DE-15']
```

Nützlich, um viele Dateien nach Fehlerart zu sortieren.

### Beispiel 2: Ein Schemafehler verdeckt BR-DE-15

```console
$ erechnung validieren zwei_fehler.xml
zwei_fehler.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  XSD: Element '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}DueDate': This element is not expected. Expected is one of ( ... ).
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BR-DE-15: Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.
```

Die Datei hat zwei Fehler. Die KoSIT-Regeln zeigen nur den Schemafehler, die Vorprüfung verrät schon den zweiten.

### Beispiel 3: Folgefehler erkennen

```console
$ erechnung validieren --ohne-offiziell brutto_falsch.xml
brutto_falsch.xml: XRechnung 3.0 (UBL)
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BRUTTO: Bruttobetrag BT-112 2019.91 ist nicht Netto + Steuer = 2009.91.
  FEHLER  VP-ZAHLBETRAG: Zahlbetrag BT-115 2009.91 passt nicht zu Brutto - Vorauszahlung + Rundung.
```

Ein falscher Bruttobetrag ergibt zwei Meldungen (offiziell BR-CO-15 und BR-CO-16). Den ersten Rechenfehler beheben, dann neu prüfen.

### Beispiel 4: Unerlaubte Rechnungsart schon beim Erstellen abfangen

```console
$ erechnung erstellen art_382.json -o art_382.xml
Rechnungsart 382 ist in XRechnung nicht erlaubt (BR-DE-17). Erlaubt: 326, 380, 381, 384, 389, 875, 876, 877.
$ echo $?
1
```

### Beispiel 5: BR-CO-26 bei einer Kleinunternehmer-Rechnung

```console
$ erechnung validieren nur_steuernummer.xml
nur_steuernummer.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-CO-26: [BR-CO-26]-In order for the buyer to automatically identify a supplier, the Seller identifier (BT-29), the Seller legal registration identifier (BT-30) and/or the Seller VAT identifier (BT-31) shall be present.
```

Hier schweigt die Vorprüfung, weil die Steuernummer für § 14 Abs. 4 UStG genügt. Die Lieferantennummer BT-29 ergänzen.

## Schritt für Schritt: eine Fehlermeldung beheben

1. Datei prüfen: `erechnung validieren rechnung.xml` (oder das ZUGFeRD-PDF).
2. Zuerst Zeilen mit `XSD` oder `VP-LESEN` beheben, dann neu prüfen.
3. Den Code in der Übersicht oben suchen (Strg+F, z.B. "BR-DE-15").
4. Das genannte BT-Feld in der Datei suchen oder ergänzen; die Ausschnitte oben zeigen Element und Position.
5. Kommt die Rechnung aus einem Programm, den Fehler dort beheben, nicht nur in der Datei, sonst kommt er bei der nächsten Rechnung wieder.
6. Neu prüfen, bis `GÜLTIG` dasteht. Warnungen mit `--streng` sichtbar machen.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Element an falscher Stelle eingefügt | Neuer `XSD`-Fehler "This element is not expected" | Reihenfolge wie im Beispiel einhalten, z.B. `cbc:BuyerReference` nach `cbc:DocumentCurrencyCode` |
| Nur die Summe korrigiert | BR-CO-16 bleibt | Brutto und Zahlbetrag zusammen anpassen |
| Steuersatz nur im Kopf geändert | BR-S-08 bleibt | Satz in Positionen (`ClassifiedTaxCategory`) und Aufschlüsselung (`TaxCategory`) gleich setzen |
| Platzhalter-Telefon `-` | Warnung BR-DE-27 | echte Nummer mit mindestens drei Ziffern |
| ZUGFeRD EN 16931 mit BR-DE-15 abgelehnt | Prüfung lief gegen XRechnung | BT-24 entscheidet; als XRechnung nur Profil XRECHNUNG versenden |

## Häufige Fragen

### Was bedeutet BR-DE-15?

BR-DE-15 bedeutet, dass die Käuferreferenz BT-10 fehlt. Bei Behörden gehört dort die Leitweg-ID hinein, im B2B eine Referenz des Kunden oder laut BMF-FAQ ein Platzhalter wie "-".

### Was bedeutet BR-CO-26?

BR-CO-26 bedeutet, dass der Verkäufer nicht eindeutig gekennzeichnet ist: Es fehlen Lieferantennummer (BT-29), Registernummer (BT-30) und USt-IdNr. (BT-31). Eine Steuernummer allein reicht für diese Regel nicht.

### Ist eine E-Rechnung mit Validierungsfehler ungültig im Sinne des UStG?

Nicht automatisch. Laut BMF-Schreiben vom 15.10.2025 ist eine Datei mit Formatfehlern keine E-Rechnung (Rn. 6a); Fehler bei Pflichtangaben machen sie nicht ordnungsmäßig, andere Geschäftsregelfehler sind umsatzsteuerlich unbeachtlich (Rn. 35a). Den Einzelfall mit der Steuerberatung klären.

### Darf ich eine Rechnung mit Warnungen annehmen?

Ja, Warnungen machen eine Rechnung technisch nicht ungültig. Ob die Angabe inhaltlich stimmt, prüft der Empfänger trotzdem selbst.

### Was bedeutet BR-DE-17?

BR-DE-17 bedeutet, dass die Rechnungsart BT-3 nicht in der Liste der XRechnung steht (326, 380, 381, 384, 389, 875, 876, 877). Es ist nur eine Warnung, die Rechnung bleibt gültig.

> **Hinweis:** Diese Anleitung erklärt Gesetz, BMF-Schreiben und technische Standards nach dem Stand vom 15.10.2026. Sie ist keine Steuer- oder Rechtsberatung, die Autoren sind keine Steuerberater. Für die Beurteilung eines konkreten Falls wenden Sie sich an Ihre Steuerberatung oder Ihr Finanzamt. Alle Angaben ohne Gewähr.

## Weiterlesen

- [E-Rechnung prüfen](./e-rechnung-validator.md): wie die Prüfung abläuft und alle Optionen von `erechnung validieren`
- [XRechnung](./xrechnung.md): Pflichtfelder und BT-Nummern
- [ZUGFeRD](./zugferd.md): Profile MINIMUM bis EXTENDED
- [Gutschrift, Korrektur und Reverse Charge](./e-rechnung-gutschrift-korrektur.md)
- [Leitweg-ID](./leitweg-id.md) und die gültigen [Beispiele](../../beispiele/README.md) zum Vergleichen
