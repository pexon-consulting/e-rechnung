# Was ist eine E-Rechnung? Definition, Formate und wie sie aussieht

Eine E-Rechnung ist nach § 14 Abs. 1 UStG eine Rechnung, die in einem strukturierten elektronischen Format ausgestellt, übermittelt und empfangen wird und eine elektronische Verarbeitung ermöglicht. In Deutschland heißt das praktisch: eine XML-Datei nach der europäischen Norm EN 16931, also eine XRechnung (UBL oder CII) oder eine ZUGFeRD/Factur-X-Rechnung ab Profil BASIC. Ein PDF ohne eingebettete Daten ist keine E-Rechnung, sondern eine "sonstige Rechnung".

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil von [E-Rechnung in Python](../../README.md).

## Das Wichtigste in Kürze

- Eine E-Rechnung ist ein Datensatz, den ein Programm ohne Abtippen lesen kann; das regelt § 14 Abs. 1 Satz 3 UStG für Umsätze ab dem 01.01.2025.
- Das Format muss der EN 16931 entsprechen oder zwischen Aussteller und Empfänger vereinbart sein (§ 14 Abs. 1 Satz 6 UStG).
- Ein normales PDF per E-Mail ist eine sonstige Rechnung, genau wie eine Papierrechnung (§ 14 Abs. 1 Satz 4 UStG).
- Zulässige Formate in Deutschland sind vor allem XRechnung (Syntax UBL oder CII) und ZUGFeRD/Factur-X ab Profil BASIC; MINIMUM und BASIC WL sind keine E-Rechnung.
- Bei einer ZUGFeRD-Rechnung zählt das eingebettete XML, nicht das sichtbare PDF.
- Mit `erechnung lesen` sehen Sie in Sekunden, ob eine Datei eine E-Rechnung ist und was drinsteht.

## Was ist eine E-Rechnung laut § 14 UStG?

Seit der Neufassung von § 14 UStG durch das Wachstumschancengesetz gibt es zwei Arten von Rechnungen:

| Rechnungsart | Definition im Gesetz | Beispiele |
| --- | --- | --- |
| E-Rechnung | "eine Rechnung, die in einem strukturierten elektronischen Format ausgestellt, übermittelt und empfangen wird und eine elektronische Verarbeitung ermöglicht" (§ 14 Abs. 1 Satz 3 UStG) | XRechnung (UBL, CII), ZUGFeRD ab BASIC, Factur-X ab BASIC |
| Sonstige Rechnung | "eine Rechnung, die in einem anderen elektronischen Format oder auf Papier übermittelt wird" (§ 14 Abs. 1 Satz 4 UStG) | Papier, PDF ohne XML, Word-Datei, Scan |

Strukturiert heißt: Jede Angabe steht in einem festen Feld mit fester Bedeutung. Die Rechnungsnummer steht im Feld BT-1, das Rechnungsdatum in BT-2, der Zahlbetrag in BT-115. Ein Buchhaltungsprogramm muss nichts erraten.

Welche Formate zulässig sind, regelt § 14 Abs. 1 Satz 6 UStG. Das Format muss entweder

1. der europäischen Norm EN 16931 und der Liste der Syntaxen nach Richtlinie 2014/55/EU entsprechen, oder
2. zwischen Aussteller und Empfänger vereinbart sein, wenn es die richtige und vollständige Extraktion der umsatzsteuerlichen Angaben in ein EN-16931-konformes oder interoperables Format ermöglicht (zum Beispiel EDI-Verfahren wie EDIFACT).

Die Pflichtangaben einer Rechnung ändern sich dadurch nicht. Sie stehen weiter in § 14 Abs. 4 UStG: Name und Anschrift, Steuernummer oder USt-IdNr., Ausstellungsdatum, fortlaufende Nummer, Menge und Art der Leistung, Leistungszeitpunkt, Entgelt nach Steuersätzen, Steuersatz und Steuerbetrag oder ein Hinweis auf die Steuerbefreiung. Neu ist, dass sie im strukturierten Teil stehen müssen. Ein Verweis auf eine unstrukturierte Anlage genügt nicht, ein Link auf ein externes Ziel auch nicht (BMF-Schreiben vom 15.10.2025, Rn. 35).

## Warum ist ein PDF keine E-Rechnung?

Ein PDF ohne eingebettetes XML ist für ein Programm nur ein Bild mit Text. Es kann die Rechnungsnummer nicht sicher finden. Deshalb zählen laut BMF-Schreiben vom 15.10.2025 (UStAE 14.1 Abs. 2) "alle nicht strukturierten elektronischen Dateien, zum Beispiel PDF-Dateien ohne integrierte Datensätze" zu den sonstigen Rechnungen.

Auch eine fehlerhafte XML-Datei kann eine sonstige Rechnung sein. Das BMF-Schreiben vom 15.10.2025 unterscheidet zwei Fehlerarten:

| Fehlerart | Was gemeint ist | Folge |
| --- | --- | --- |
| Formatfehler (Rn. 6a) | Die Datei entspricht nicht der Syntax oder deren technischen Vorgaben | keine E-Rechnung, sondern sonstige Rechnung |
| Geschäftsregelfehler (Rn. 6b) | Ein Verstoß gegen die Regeln des Formats, zum Beispiel fehlendes BT-10 in einer XRechnung | umsatzsteuerlich unbeachtlich, wenn keine Pflichtangabe nach §§ 14 Abs. 4, 14a UStG betroffen ist (Rn. 35a) |

So sieht es aus, wenn Sie ein reines PDF mit dem Werkzeug lesen:

```bash
erechnung lesen rechnung.pdf
```

```text
rechnung.pdf: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
```

Ob Sie ein solches PDF noch verschicken dürfen, hängt von den Übergangsfristen in § 27 Abs. 38 UStG ab. Bis 31.12.2026 geht das mit Zustimmung des Empfängers. Details stehen in der Anleitung [E-Rechnung Pflicht](./e-rechnung-pflicht.md).

## Welche E-Rechnung-Formate gibt es?

In Deutschland sind zwei Formatfamilien verbreitet. Beide bilden dasselbe Datenmodell der EN 16931 ab, nur in unterschiedlicher Form.

| Format | Datei | Syntax | Kennung in BT-24 | Typischer Einsatz |
| --- | --- | --- | --- | --- |
| XRechnung (UBL) | reines XML | UBL 2.1 Invoice oder CreditNote | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` | Rechnungen an Behörden, Peppol, B2B |
| XRechnung (CII) | reines XML | UN/CEFACT CII D16B | wie oben | wie oben |
| ZUGFeRD / Factur-X | PDF/A-3 mit eingebettetem XML | CII | je nach Profil, siehe unten | B2B, wenn der Empfänger auch ein lesbares PDF möchte |

XRechnung ist der deutsche Standard der KoSIT. Aktuell ist XRechnung 3.0.2. Die Version 3.0 bleibt laut xeinkauf.de bis mindestens 31.07.2027 in Kraft, XRechnung 4.0 erscheint voraussichtlich im Frühjahr 2027.

ZUGFeRD heißt in Frankreich Factur-X. Beide sind technisch identisch. Aktuell ist laut FeRD ZUGFeRD 2.5.2 (Factur-X 1.09.2), gültig ab 01.09.2026. Eine ZUGFeRD-Rechnung ist ein Hybridformat: ein PDF für Menschen und ein XML für Programme in einer Datei (UStAE 14.1 Abs. 14).

Mehr zum Vergleich steht in [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md).

### Welche ZUGFeRD-Profile sind eine E-Rechnung?

ZUGFeRD gibt es in mehreren Profilen, die unterschiedlich viele Angaben enthalten. Laut BMF-Schreiben vom 15.10.2025 (UStAE 14.1 Abs. 14) fällt "ZUGFeRD ab der Version 2.0.1 - ausgenommen die Profile MINIMUM und BASIC-WL" unter die zulässigen E-Rechnungs-Formate.

| Profil | Kennung in BT-24 | E-Rechnung nach BMF? |
| --- | --- | --- |
| MINIMUM | `urn:factur-x.eu:1p0:minimum` | nein |
| BASIC WL | `urn:factur-x.eu:1p0:basicwl` | nein |
| BASIC | `urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic` | ja |
| EN 16931 (COMFORT) | `urn:cen.eu:en16931:2017` | ja |
| EXTENDED | `urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended` | ja |
| XRECHNUNG | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` | ja |

MINIMUM und BASIC WL enthalten nicht alle Pflichtangaben einer Rechnung. Das Werkzeug erkennt die Kennung und sagt es deutlich (siehe Beispiel 6).

## Wie sieht eine E-Rechnung aus?

Eine E-Rechnung sieht zuerst aus wie eine Textdatei voller spitzer Klammern. Das ist der Anfang der XRechnung in [`beispiele/01_standard/xrechnung_ubl.xml`](../../beispiele/01_standard/xrechnung_ubl.xml):

```xml
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

Jedes Element entspricht einem Business Term (BT) der EN 16931. Die Felder aus diesem Ausschnitt:

| BT | Bedeutung | Element in UBL | Wert im Beispiel |
| --- | --- | --- | --- |
| BT-24 | Spezifikationskennung (welcher Standard) | `cbc:CustomizationID` | XRechnung 3.0 |
| BT-23 | Geschäftsprozess | `cbc:ProfileID` | Peppol Billing |
| BT-1 | Rechnungsnummer | `cbc:ID` | RE-2026-0001 |
| BT-2 | Rechnungsdatum | `cbc:IssueDate` | 2026-10-15 |
| BT-9 | Fälligkeitsdatum | `cbc:DueDate` | 2026-11-14 |
| BT-3 | Rechnungsart (UNTDID 1001) | `cbc:InvoiceTypeCode` | 380 (Rechnung) |
| BT-22 | Bemerkung | `cbc:Note` | Vielen Dank für Ihren Auftrag. |
| BT-5 | Währung | `cbc:DocumentCurrencyCode` | EUR |
| BT-10 | Käuferreferenz, bei Behörden die Leitweg-ID | `cbc:BuyerReference` | BH-2026-0815 |

Die Umsatzsteuer steht in einer eigenen Aufschlüsselung (BG-23) mit Kategorie, Satz, Basis und Betrag. Im selben Beispiel:

```xml
  <cac:TaxTotal>
    <cbc:TaxAmount currencyID="EUR">320.91</cbc:TaxAmount>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">1689.00</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">320.91</cbc:TaxAmount>
      <cac:TaxCategory>
        <cbc:ID>S</cbc:ID>
        <cbc:Percent>19</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:TaxCategory>
    </cac:TaxSubtotal>
  </cac:TaxTotal>
```

Das erste `TaxAmount` ist die Steuersumme der Rechnung (BT-110). In `TaxSubtotal` stehen die Basis (`TaxableAmount`, BT-116), die Steuer dieser Zeile (`TaxAmount`, BT-117), die Steuerkategorie (`S`, BT-118, Regelsteuersatz) und der Satz (`19`, BT-119).

Dieselbe Rechnung gibt es im Beispielordner noch zweimal:

- **Lesefassung als HTML:** [`beispiele/01_standard/ansicht.html`](../../beispiele/01_standard/ansicht.html) zeigt die Daten als Tabellen mit Verkäufer, Käufer, Positionen, Umsatzsteuer und Zahlung. Am Ende steht: "Rechtlich maßgeblich ist der XML-Inhalt der E-Rechnung."
- **ZUGFeRD-PDF:** [`beispiele/01_standard/zugferd_en16931.pdf`](../../beispiele/01_standard/zugferd_en16931.pdf) sieht aus wie eine normale PDF-Rechnung. Darin steckt als Anhang die Datei `factur-x.xml` mit denselben Daten in CII-Syntax. Der Fußtext im PDF sagt: "Diese PDF-Datei enthält die Rechnungsdaten zusätzlich als strukturiertes XML (ZUGFeRD)."

### Was gilt, wenn PDF und XML nicht übereinstimmen?

Bei einer ZUGFeRD-Rechnung ist das XML maßgebend. Laut BMF-FAQ hat bei Abweichungen zwischen XML und Bildteil der strukturierte Teil Vorrang; früher war es umgekehrt. Das BMF empfiehlt, den XML-Teil selbst zu visualisieren, statt sich auf das mitgelieferte PDF zu verlassen. Genau das macht `erechnung anzeigen`: Es baut die Ansicht aus dem XML, nicht aus dem PDF.

## Beispiele

Alle Befehle laufen im Ordner mit den Dateien aus [`beispiele/`](../../beispiele/README.md). Die Installation steht im [README](../../README.md) und unten in Schritt 2.

### Beispiel 1: XRechnung in UBL lesen

```bash
erechnung lesen beispiele/01_standard/xrechnung_ubl.xml
```

```text
Datei:        beispiele/01_standard/xrechnung_ubl.xml
Format:       XRechnung 3.0 (UBL)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
Nummer:       RE-2026-0001 vom 15.10.2026
Verkäufer:    Nordlicht Software GmbH, 20095 Hamburg, USt-IdNr. DE123456789
Käufer:       Beispiel Handel AG, 80331 München
Käuferref.:   BH-2026-0815
Positionen:   2
     1        12 HUR  Beratung Einführung E-Rechnung                     1.440,00 EUR
     2         1 MON  Softwarelizenz Rechnungseingang (Monat)              249,00 EUR
USt:          S (Regelsteuersatz oder ermäßigter Satz) 19 %: 320,91 EUR auf 1.689,00 EUR
Netto:        1.689,00 EUR
Brutto:       2.009,91 EUR
Zahlbetrag:   2.009,91 EUR, fällig 14.11.2026
Zahlung:      58 (SEPA-Überweisung) DE79000000001234567890
```

Das brauchen Sie, wenn eine XML-Datei per Mail kommt und Sie schnell wissen wollen, was drinsteht.

### Beispiel 2: dieselbe Rechnung in CII lesen

```bash
erechnung lesen beispiele/01_standard/xrechnung_cii.xml
```

```text
Datei:        beispiele/01_standard/xrechnung_cii.xml
Format:       XRechnung 3.0 (CII)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
Nummer:       RE-2026-0001 vom 15.10.2026
...
Zahlbetrag:   2.009,91 EUR, fällig 14.11.2026
Zahlung:      58 (SEPA-Überweisung) DE79000000001234567890
```

Der Inhalt ist identisch mit Beispiel 1, nur die Syntax ist eine andere. UBL und CII sind zwei Schreibweisen desselben Datenmodells.

### Beispiel 3: ZUGFeRD-PDF lesen

```bash
erechnung lesen beispiele/01_standard/zugferd_en16931.pdf
```

```text
Datei:        beispiele/01_standard/zugferd_en16931.pdf
Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
Nummer:       RE-2026-0001 vom 15.10.2026
...
Zahlbetrag:   2.009,91 EUR, fällig 14.11.2026
```

Das brauchen Sie, wenn Sie prüfen wollen, ob ein PDF wirklich ein XML enthält und welches Profil es hat.

### Beispiel 4: XML aus dem ZUGFeRD-PDF holen

```bash
erechnung extrahieren beispiele/01_standard/zugferd_en16931.pdf -o factur-x.xml
```

```text
factur-x.xml aus beispiele/01_standard/zugferd_en16931.pdf gespeichert als factur-x.xml
```

Der Anfang der Datei zeigt das Profil EN 16931 in BT-24 (`GuidelineSpecifiedDocumentContextParameter`):

```xml
<rsm:CrossIndustryInvoice xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100" xmlns:ram="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100" xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100" xmlns:qdt="urn:un:unece:uncefact:data:standard:QualifiedDataType:100">
  <rsm:ExchangedDocumentContext>
    <ram:BusinessProcessSpecifiedDocumentContextParameter>
      <ram:ID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</ram:ID>
    </ram:BusinessProcessSpecifiedDocumentContextParameter>
    <ram:GuidelineSpecifiedDocumentContextParameter>
      <ram:ID>urn:cen.eu:en16931:2017</ram:ID>
    </ram:GuidelineSpecifiedDocumentContextParameter>
  </rsm:ExchangedDocumentContext>
  <rsm:ExchangedDocument>
    <ram:ID>RE-2026-0001</ram:ID>
    ...
  </rsm:ExchangedDocument>
  ...
</rsm:CrossIndustryInvoice>
```

Das brauchen Sie, wenn ein Programm nur XML annimmt oder wenn Sie den strukturierten Teil getrennt ansehen wollen.

### Beispiel 5: Lesefassung aus dem XML erzeugen

```bash
erechnung anzeigen beispiele/01_standard/xrechnung_ubl.xml -o ansicht.html
```

```text
Ansicht geschrieben: ansicht.html
```

Die HTML-Datei öffnen Sie im Browser. Mit `--offiziell` nutzt das Werkzeug stattdessen die KoSIT-Visualisierung. Das brauchen Sie, um eine XRechnung ohne Spezialprogramm zu lesen.

### Beispiel 6: ZUGFeRD MINIMUM erkennen

Zum Ausprobieren wurde in der Datei aus Beispiel 4 die Kennung in BT-24 auf `urn:factur-x.eu:1p0:minimum` gesetzt und als `minimum.xml` gespeichert:

```bash
erechnung lesen minimum.xml
```

```text
Datei:        minimum.xml
Format:       CII Profil MINIMUM
E-Rechnung:   nein
...
```

```bash
erechnung validieren minimum.xml
```

```text
minimum.xml: CII Profil MINIMUM
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario kein Szenario, 1 Fehler, 0 Warnungen
  FEHLER  SZENARIO: Kein passendes Prüfszenario. Erwartet wird UBL Invoice/CreditNote oder CII mit einer Spezifikationskennung (BT-24) für XRechnung 3.0 oder EN 16931.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-FORMAT: CII Profil MINIMUM: Dieses ZUGFeRD-Profil enthält nicht alle Pflichtangaben und gilt nicht als E-Rechnung nach § 14 UStG. Mindestens Profil BASIC, besser EN 16931 verwenden.
```

Das brauchen Sie, wenn ein Lieferant "ZUGFeRD" schickt und Sie wissen wollen, ob das Profil reicht.

### Beispiel 7: prüfen, ob eine E-Rechnung gültig ist

```bash
erechnung validieren beispiele/01_standard/xrechnung_ubl.xml --bericht berichte/
```

```text
beispiele/01_standard/xrechnung_ubl.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
  Prüfbericht: berichte/xrechnung_ubl.xml.1e0e5c550373.validierungsbericht.json
```

Lesen zeigt den Inhalt, Validieren prüft die offiziellen KoSIT-Regeln. Der Prüfbericht enthält Zeitpunkt, Regelversion und SHA-256 der Datei. Mehr dazu in [E-Rechnung prüfen](./e-rechnung-validator.md).

## Schritt für Schritt: herausfinden, ob eine Datei eine E-Rechnung ist

1. **Dateityp ansehen.** Eine `.xml`-Datei ist ein Kandidat für XRechnung. Ein `.pdf` kann eine ZUGFeRD-Rechnung sein oder nur eine sonstige Rechnung.
2. **Werkzeug installieren.** Sie brauchen Python 3.10 oder neuer, Java ist nicht nötig:
   ```bash
   pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
   ```
3. **Datei lesen.** `erechnung lesen rechnung.pdf` oder `erechnung lesen rechnung.xml`. Die Zeile `E-Rechnung:` sagt "ja" oder "nein", die Zeile `Format:` nennt Format und Profil.
4. **Bei "nein" nachsehen, warum.** Ein PDF ohne XML ist eine sonstige Rechnung. Ein ZUGFeRD-Profil MINIMUM oder BASIC WL reicht nicht. Bitten Sie den Lieferanten um eine XRechnung oder ein ZUGFeRD-PDF ab Profil BASIC.
5. **Bei "ja" prüfen.** `erechnung validieren rechnung.xml` prüft mit den offiziellen KoSIT-Regeln. Die Rechnungsdaten verlassen dabei Ihren Rechner nicht.
6. **Inhalt ansehen.** `erechnung anzeigen rechnung.xml -o ansicht.html` erzeugt eine Lesefassung aus dem XML.
7. **Original aufbewahren.** Bewahren Sie die empfangene Datei im Ursprungsformat auf, nicht nur die Lesefassung (BMF-Schreiben vom 15.10.2025, Rn. 60). Mehr dazu in [E-Rechnung archivieren](./e-rechnung-archivieren.md).

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| PDF aus Word oder Buchhaltung gilt als E-Rechnung | `erechnung lesen` meldet: "Das PDF enthält kein eingebettetes Rechnungs-XML." | XRechnung oder ZUGFeRD-PDF erzeugen, siehe [E-Rechnung erstellen](./e-rechnung-erstellen.md) |
| ZUGFeRD im Profil MINIMUM oder BASIC WL | `E-Rechnung:   nein`, Hinweis `VP-FORMAT` | Profil BASIC oder besser EN 16931 verwenden |
| Nur die Lesefassung (HTML oder PDF) wird gebucht oder archiviert | Beträge im PDF weichen vom XML ab, niemand merkt es | Das XML ist maßgeblich; Ansicht immer aus dem XML erzeugen und das Original aufbewahren |
| Pflichtangabe steht nur im angehängten PDF | Validierung meldet fehlende BT-Felder | Alle Pflichtangaben gehören in den strukturierten Teil (BMF-Schreiben vom 15.10.2025, Rn. 35) |
| Link auf ein Kundenportal statt Anhang | Ergänzende Unterlagen fehlen in der Datei | Unterlagen einbetten; ein Link auf ein externes Ziel genügt nicht (Rn. 35) |
| XML-Datei im Texteditor von Hand geändert | Validierung meldet Schema- oder Rechenfehler | Datei neu aus der Quelle erzeugen, nicht von Hand ändern |

## Häufige Fragen

### Ist ein PDF eine E-Rechnung?

Nein, ein PDF ohne eingebettetes XML ist eine sonstige Rechnung nach § 14 Abs. 1 Satz 4 UStG. Nur ein PDF mit eingebettetem XML nach ZUGFeRD oder Factur-X ab Profil BASIC ist eine E-Rechnung. Ob ein PDF ein XML enthält, zeigt `erechnung lesen rechnung.pdf`.

### Was ist der Unterschied zwischen XRechnung und ZUGFeRD?

Eine XRechnung ist eine reine XML-Datei, eine ZUGFeRD-Rechnung ist ein PDF/A-3 mit eingebettetem XML. Beide beruhen auf der EN 16931. Die XRechnung hat zusätzliche deutsche Regeln (BR-DE), zum Beispiel ist die Käuferreferenz BT-10 Pflicht (BR-DE-15). Ausführlich: [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md).

### Was ist UBL und was ist CII?

UBL und CII sind zwei XML-Syntaxen für dieselben Rechnungsdaten: UBL 2.1 und UN/CEFACT CII D16B. Eine XRechnung darf in beiden Syntaxen kommen, ZUGFeRD nutzt CII. Für den Inhalt macht das keinen Unterschied, wie Beispiel 1 und 2 zeigen.

### Wie öffne ich eine E-Rechnung?

Eine E-Rechnung öffnen Sie mit einem Viewer, der das XML in eine Lesefassung umwandelt. Mit dem Werkzeug geht das über `erechnung anzeigen rechnung.xml -o ansicht.html`; die HTML-Datei öffnet jeder Browser. Ein ZUGFeRD-PDF können Sie zusätzlich mit jedem PDF-Programm öffnen, maßgeblich bleibt aber das XML. Mehr in [E-Rechnung empfangen](./e-rechnung-empfangen.md).

### Ist eine XRechnung mit einem Fehler trotzdem eine E-Rechnung?

Das hängt von der Art des Fehlers ab. Formatfehler machen die Datei zur sonstigen Rechnung (BMF-Schreiben vom 15.10.2025, Rn. 6a). Geschäftsregelfehler, die keine Pflichtangabe nach §§ 14 Abs. 4, 14a UStG betreffen, sind umsatzsteuerlich unbeachtlich (Rn. 35a). Im Einzelfall mit der Steuerberatung klären. Was einzelne Meldungen bedeuten, steht in [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md).

### Ist eine EDI-Rechnung eine E-Rechnung?

Ja, wenn Aussteller und Empfänger das Format vereinbart haben und es die richtige und vollständige Extraktion der umsatzsteuerlichen Angaben in ein EN-16931-konformes oder interoperables Format ermöglicht (§ 14 Abs. 1 Satz 6 Nr. 2 UStG). Laut BMF-FAQ können dadurch EDI-Verfahren wie EDIFACT weiter genutzt werden. Dieses Werkzeug liest EDIFACT nicht.

### Muss ich jede E-Rechnung prüfen?

Sie müssen eingehende Rechnungen weiterhin selbst prüfen; eine Validierung ersetzt diese Prüfpflicht nicht (BMF-Schreiben vom 15.10.2025, Rn. 35a). Sie dürfen sich aber bei Sorgfalt eines ordentlichen Kaufmanns auf das Ergebnis einer geeigneten Validierungsanwendung verlassen. Das BMF empfiehlt, den Validierungsbericht aufzubewahren, zum Beispiel mit `erechnung validieren rechnung.xml --bericht berichte/`.

> **Hinweis:** Diese Anleitung erklärt Gesetz, BMF-Schreiben und technische Standards nach dem Stand vom 15.10.2026. Sie ist keine Steuer- oder Rechtsberatung, die Autoren sind keine Steuerberater. Für die Beurteilung eines konkreten Falls wenden Sie sich an Ihre Steuerberatung oder Ihr Finanzamt. Alle Angaben ohne Gewähr.

## Weiterlesen

- [E-Rechnung Pflicht: ab wann, für wen und welche Übergangsfristen gelten](./e-rechnung-pflicht.md)
- [E-Rechnung für Kleinunternehmer](./e-rechnung-kleinunternehmer.md)
- [XRechnung: Format, Aufbau und Pflichtfelder](./xrechnung.md)
- [ZUGFeRD: Format, Profile und Versionen](./zugferd.md)
- [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md)
- [E-Rechnung Beispiel: Beispieldateien zum Herunterladen](./e-rechnung-beispiel.md)
- Beispielrechnung: [UBL](../../beispiele/01_standard/xrechnung_ubl.xml), [CII](../../beispiele/01_standard/xrechnung_cii.xml), [Ansicht](../../beispiele/01_standard/ansicht.html), [ZUGFeRD-PDF](../../beispiele/01_standard/zugferd_en16931.pdf), [alle Beispiele](../../beispiele/README.md)
