# E-Rechnung für Kleinunternehmer: was nach § 19 UStG gilt

Für die E-Rechnung gilt bei Kleinunternehmern: Seit dem 01.01.2025 müssen auch Kleinunternehmer nach § 19 UStG E-Rechnungen empfangen können, eine Ausnahme gibt es dafür nicht. Eigene Rechnungen dürfen Kleinunternehmer dagegen weiter als sonstige Rechnung ausstellen, also auf Papier oder mit Zustimmung des Empfängers zum Beispiel als PDF (§ 34a UStDV). Wer freiwillig E-Rechnungen schreibt, braucht die Steuerkategorie E, einen Befreiungsgrund mit Hinweis auf § 19 UStG und die Steuernummer oder USt-IdNr.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Kleinunternehmer, Selbstständige und ihre Steuerkanzleien. Technische Beispiele stehen weiter unten und sind optional.

## Das Wichtigste in Kürze

- Kleinunternehmer müssen seit dem 01.01.2025 E-Rechnungen empfangen können, genau wie alle anderen inländischen Unternehmer.
- Für den Empfang genügt ein E-Mail-Postfach; ein besonderes Postfach oder eine bestimmte Software ist nicht vorgeschrieben.
- Rechnungen von Kleinunternehmern sind von der Pflicht zur Ausstellung einer E-Rechnung ausgenommen (§ 34a UStDV).
- Eine freiwillige E-Rechnung eines Kleinunternehmers nutzt die Steuerkategorie E (steuerbefreit) mit 0 % und einem Befreiungsgrund in BT-120.
- Ohne Steuernummer (BT-32) oder USt-IdNr. (BT-31) lehnen die offiziellen Prüfregeln eine solche Rechnung ab (BR-DE-16, BR-E-02).
- Das Beispiel [`beispiele/07_kleinunternehmer`](../../beispiele/07_kleinunternehmer/) zeigt eine gültige Kleinunternehmer-Rechnung als XRechnung und als ZUGFeRD-PDF.

## Muss ein Kleinunternehmer E-Rechnungen empfangen?

Ja. Seit dem 01.01.2025 müssen alle inländischen Unternehmer E-Rechnungen empfangen können, ohne Ausnahme. Das BMF-Schreiben vom 15.10.2025 (UStAE 14.1) sagt ausdrücklich, dass das gilt, "auch, wenn der Rechnungsempfänger der Sonderregelung nach § 19 UStG unterliegt". Die BMF-FAQ nennt neben Kleinunternehmern auch Land- und Forstwirte und Unternehmer mit ausschließlich steuerfreien Umsätzen.

Empfangen können heißt nicht, dass Sie teure Software brauchen:

- Der Empfang per E-Mail genügt, ein gesondertes Postfach ist nicht nötig (BMF-Schreiben vom 15.10.2025, UStAE 14.1).
- Ein Übermittlungsweg ist nicht vorgeschrieben: E-Mail, Schnittstelle, Portal-Download oder USB-Stick sind möglich (BMF-FAQ).
- Sie müssen die Rechnung lesen können. Dafür reicht ein kostenloser Viewer, der das XML als lesbare Ansicht darstellt (siehe Beispiel 6).
- Sie müssen die E-Rechnung im empfangenen Format aufbewahren, den strukturierten Teil unversehrt (UStAE 14b.1 neu). Die Aufbewahrungsfrist beträgt acht Jahre (§ 14b Abs. 1 UStG, BMF-Schreiben vom 15.10.2025, Rn. 60).

Ihr Lieferant entscheidet, ob er Ihnen eine E-Rechnung schickt. Ist er selbst zur E-Rechnung verpflichtet, braucht er Ihre Zustimmung nicht (§ 14 Abs. 1 Satz 5 UStG). Ein PDF anzunehmen statt einer E-Rechnung ist in der Übergangszeit nur möglich, wenn Sie zustimmen.

## Muss ein Kleinunternehmer E-Rechnungen schreiben?

Nein. Rechnungen von Kleinunternehmern gehören zu den Ausnahmen von der Ausstellungspflicht (§ 34a UStDV, BMF-FAQ, BMF-Schreiben vom 15.10.2025, UStAE 14.7a). Sie dürfen weiter als sonstige Rechnung ausgestellt werden: auf Papier oder, wenn der Empfänger zustimmt, in einem anderen elektronischen Format wie PDF.

| Frage | Kleinunternehmer nach § 19 UStG | Quelle |
| --- | --- | --- |
| E-Rechnungen empfangen können | ja, seit 01.01.2025 | BMF-Schreiben vom 15.10.2025, UStAE 14.1 |
| Eigene Rechnungen als E-Rechnung ausstellen | nicht verpflichtet | § 34a UStDV |
| Papierrechnung ausstellen | zulässig | § 34a UStDV, BMF-FAQ |
| PDF-Rechnung ausstellen | zulässig mit Zustimmung des Empfängers | § 34a UStDV, BMF-FAQ |
| Freiwillig E-Rechnung ausstellen | zulässig | § 14 Abs. 1 UStG |
| Empfangene E-Rechnung aufbewahren | acht Jahre, im Ursprungsformat | § 14b Abs. 1 UStG, BMF-Schreiben vom 15.10.2025, Rn. 60 |

Kleinunternehmer ist nach § 19 Abs. 1 UStG (Fassung ab 01.01.2025), wessen Gesamtumsatz im Vorjahr 25.000 EUR nicht überschritten hat und im laufenden Jahr 100.000 EUR nicht überschreitet. Wird die Grenze von 100.000 EUR im laufenden Jahr überschritten, unterliegt laut BMF schon der Umsatz, mit dem das passiert, der Regelbesteuerung (UStAE 19.1 Abs. 2 in der Fassung des BMF-Schreibens vom 18.03.2025). Ob die Regelung in Ihrem Fall greift, klärt Ihre Steuerberatung.

## Warum freiwillig E-Rechnungen schreiben?

Viele Kunden von Kleinunternehmern sind selbst Unternehmen. Ab dem 01.01.2028 ist die E-Rechnung für inländische B2B-Umsätze verpflichtend (§ 27 Abs. 38 UStG), mit Ausnahmen wie Kleinbetragsrechnungen bis 250 EUR brutto und Rechnungen von Kleinunternehmern. Ihre Kunden stellen deshalb ihren Rechnungseingang auf XML um. Eine E-Rechnung von Ihnen lässt sich dort ohne Abtippen buchen.

Gründe, die für eine freiwillige E-Rechnung sprechen können:

- Der Kunde bittet darum, zum Beispiel weil sein Rechnungseingang nur noch XML verarbeitet.
- Sie wollen nicht zwei Wege pflegen, wenn Sie später die Kleinunternehmerregelung verlassen.

Getrennt davon: Ist der Kunde eine Bundesbehörde, verlangt die E-Rechnungsverordnung des Bundes (ERechV) die E-Rechnung unabhängig von § 34a UStDV, auch von Kleinunternehmern; ausgenommen sind Direktaufträge bis 1.000 EUR. Länder und Kommunen haben eigene Regeln. Mehr in [Leitweg-ID](./leitweg-id.md).

Eine E-Rechnung zu erstellen kostet mit Open-Source-Werkzeugen nichts. Das Werkzeug aus diesem Repo erzeugt eine XRechnung oder ein ZUGFeRD-PDF aus einer JSON-Datei (siehe Schritt für Schritt).

## Was muss auf einer Kleinunternehmer-Rechnung stehen?

Für Rechnungen von Kleinunternehmern gelten die verringerten Angaben nach § 34a UStDV: Name und Anschrift von Ihnen und Ihrem Kunden, Ihre Steuernummer, USt-IdNr. oder Kleinunternehmer-Identifikationsnummer, das Ausstellungsdatum, Menge und Art der Leistung, das Entgelt und ein Hinweis auf die Steuerbefreiung nach § 19 UStG. Rechnungsnummer und Leistungsdatum verlangt § 34a UStDV nicht; in einer XRechnung sind BT-1 (Rechnungsnummer) und weitere Felder technisch trotzdem Pflicht. Laut BMF-Schreiben vom 15.10.2025 (UStAE 14.5 Abs. 14) brauchen Rechnungen von Kleinunternehmern auch keine fortlaufende Nummer. Welche Angaben Ihre Rechnung im Einzelfall braucht, klärt Ihre Steuerberatung.

Kurz gesagt: Auf Ihrer E-Rechnung steht keine Umsatzsteuer, der Satz ist 0 %, und es steht ein Hinweis wie "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet." darauf. Dazu kommt Ihre Steuernummer oder USt-IdNr. Wenn Ihr Rechnungsprogramm E-Rechnungen erstellt, setzt es diese Felder in der Regel selbst. Wie sie in der Datei aussehen, zeigen die folgenden Ausschnitte.

In einer E-Rechnung landen diese Angaben in festen Feldern. Für Kleinunternehmer sind drei Stellen entscheidend:

| Angabe | Feld | Wert im Beispiel 07 | Regel |
| --- | --- | --- | --- |
| Steuerkategorie der Position | BT-151 | `E` (steuerbefreit) | UNCL 5305 |
| Steuerkategorie in der Aufschlüsselung | BT-118 | `E` mit Satz `0` (BT-119) | UNCL 5305 |
| Befreiungsgrund | BT-120 | "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet." | BR-E-10 |
| Steuernummer des Verkäufers | BT-32 | `214/5678/1234` | BR-DE-16, BR-E-02 |

Zusätzlich steht der Hinweis im Beispiel als Bemerkung (BT-22); die Ansicht zeigt ihn unter "Hinweise".

### Steuerkategorie E statt S

Eine normale Rechnung nutzt die Steuerkategorie S mit 19 % oder 7 %. Ein Kleinunternehmer berechnet keine Umsatzsteuer. Im Beispiel 07 hat die Position deshalb die Kategorie `E` mit dem Satz `0`. In der UBL-Datei [`beispiele/07_kleinunternehmer/xrechnung_ubl.xml`](../../beispiele/07_kleinunternehmer/xrechnung_ubl.xml) sieht die Position so aus:

<details><summary>XML ansehen</summary>

```xml
  <cac:InvoiceLine>
    <cbc:ID>1</cbc:ID>
    <cbc:InvoicedQuantity unitCode="LS">1</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">850.00</cbc:LineExtensionAmount>
    <cac:Item>
      <cbc:Name>Logo-Entwicklung inkl. drei Entwürfe</cbc:Name>
      <cac:ClassifiedTaxCategory>
        <cbc:ID>E</cbc:ID>
        <cbc:Percent>0</cbc:Percent>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:ClassifiedTaxCategory>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="EUR">850</cbc:PriceAmount>
    </cac:Price>
  </cac:InvoiceLine>
```

</details>

### Befreiungsgrund mit Hinweis auf § 19 UStG

Bei Kategorie E verlangt die EN 16931 einen Befreiungsgrund als Text (BT-120) oder Code (BT-121), sonst meldet die Prüfung BR-E-10. Im Beispiel steht der Grund in der Steueraufschlüsselung:

<details><summary>XML ansehen</summary>

```xml
  <cac:TaxTotal>
    <cbc:TaxAmount currencyID="EUR">0.00</cbc:TaxAmount>
    <cac:TaxSubtotal>
      <cbc:TaxableAmount currencyID="EUR">850.00</cbc:TaxableAmount>
      <cbc:TaxAmount currencyID="EUR">0.00</cbc:TaxAmount>
      <cac:TaxCategory>
        <cbc:ID>E</cbc:ID>
        <cbc:Percent>0</cbc:Percent>
        <cbc:TaxExemptionReason>Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.</cbc:TaxExemptionReason>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:TaxCategory>
    </cac:TaxSubtotal>
  </cac:TaxTotal>
```

</details>

In der CII-Datei [`beispiele/07_kleinunternehmer/xrechnung_cii.xml`](../../beispiele/07_kleinunternehmer/xrechnung_cii.xml) heißt das Element `ExemptionReason`:

<details><summary>XML ansehen</summary>

```xml
      <ram:ApplicableTradeTax>
        <ram:CalculatedAmount>0.00</ram:CalculatedAmount>
        <ram:TypeCode>VAT</ram:TypeCode>
        <ram:ExemptionReason>Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.</ram:ExemptionReason>
        <ram:BasisAmount>850.00</ram:BasisAmount>
        <ram:CategoryCode>E</ram:CategoryCode>
        <ram:RateApplicablePercent>0</ram:RateApplicablePercent>
      </ram:ApplicableTradeTax>
```

</details>

### Steuernummer statt USt-IdNr.

§ 34a Satz 1 Nr. 2 UStDV verlangt die Steuernummer, die USt-IdNr. oder die Kleinunternehmer-Identifikationsnummer des Verkäufers. Im Beispiel 07 hat die Verkäuferin nur eine Steuernummer. Sie steht in BT-32 mit dem Schema `FC`, nicht mit `VAT` wie eine USt-IdNr.:

<details><summary>XML ansehen</summary>

```xml
      <cac:PartyTaxScheme>
        <cbc:CompanyID>214/5678/1234</cbc:CompanyID>
        <cac:TaxScheme>
          <cbc:ID>FC</cbc:ID>
        </cac:TaxScheme>
      </cac:PartyTaxScheme>
```

</details>

In CII steht dieselbe Angabe als `<ram:ID schemeID="FC">214/5678/1234</ram:ID>` unter `SpecifiedTaxRegistration`. Fehlen beide Angaben, lehnt die KoSIT-Prüfung die Rechnung ab (Beispiel 5).

## Kleinunternehmer-Rechnung als E-Rechnung: Beispiele

Alle Befehle laufen im Ordner mit den Dateien aus [`beispiele/`](../../beispiele/README.md). Die Werte stammen aus dem Beispiel 07, einer Rechnung über 850,00 EUR für eine Logo-Entwicklung.

### Beispiel 1: die Eingabe als JSON

Das ist [`beispiele/07_kleinunternehmer/eingabe.json`](../../beispiele/07_kleinunternehmer/eingabe.json). Daraus erzeugt das Werkzeug die XRechnung und das ZUGFeRD-PDF.

```json
{
  "nummer": "2026-017",
  "datum": "2026-10-15",
  "faellig": "2026-11-14",
  "leitweg_id": "BH-2026-0815",
  "verkaeufer": {
    "name": "Grafikdesign Lena Beispiel",
    "adresse": {
      "strasse": "Gartenweg 3",
      "plz": "50667",
      "ort": "Köln",
      "land": "DE"
    },
    "steuernummer": "214/5678/1234",
    "elektronische_adresse": "lena@grafik-beispiel.example",
    "kontakt": {
      "name": "Lena Beispiel",
      "telefon": "+49 221 4710123",
      "email": "lena@grafik-beispiel.example"
    },
    "kennung": "LIEF-0815"
  },
  "kaeufer": {
    "name": "Beispiel Handel AG",
    "adresse": {
      "strasse": "Hauptstraße 5",
      "plz": "80331",
      "ort": "München",
      "land": "DE"
    },
    "kennung": "K-10023",
    "elektronische_adresse": "eingangsrechnung@beispiel-handel.example"
  },
  "zahlung": {
    "art": "58",
    "iban": "DE79000000001234567890",
    "bic": "",
    "kontoinhaber": "Lena Beispiel"
  },
  "notizen": [
    "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.",
    "Lieferantennummer beim Kunden: LIEF-0815."
  ],
  "leistung_von": "2026-10-01",
  "leistung_bis": "2026-10-10",
  "positionen": [
    {
      "id": "1",
      "name": "Logo-Entwicklung inkl. drei Entwürfe",
      "menge": "1",
      "einheit": "LS",
      "preis": "850.00",
      "kategorie": "E",
      "satz": "0"
    }
  ],
  "befreiungsgruende": {
    "E": "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet."
  }
}
```

Die wichtigen Felder für Kleinunternehmer sind `steuernummer`, `kategorie: "E"` mit `satz: "0"` und `befreiungsgruende`. Das Feld `leitweg_id` füllt BT-10, das in einer XRechnung Pflicht ist; im B2B genügt dort eine Referenz des Kunden.

### Beispiel 2: ZUGFeRD-PDF erstellen und gleich prüfen

Die JSON-Datei holen Sie mit `erechnung beispiele bsp`; sie liegt dann als `bsp/07_kleinunternehmer.json` vor.

```bash
erechnung erstellen bsp/07_kleinunternehmer.json --format zugferd -o ku.pdf --validieren
```

```text
ku.pdf: zugferd, Rechnung 2026-017, Zahlbetrag 850,00 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 (CII))
```

Das brauchen Sie, wenn Ihr Kunde ein PDF zum Ansehen und ein XML zum Buchen in einer Datei möchte. Die sichtbare Seite zeigt die Steuernummer und die Zeile "Steuerbefreit: Gemäß § 19 UStG wird keine Umsatzsteuer berechnet."

### Beispiel 3: XRechnung erstellen

```bash
erechnung erstellen bsp/07_kleinunternehmer.json -o ku.xml
```

```text
ku.xml: xrechnung-ubl, Rechnung 2026-017, Zahlbetrag 850,00 EUR
```

Ohne `--format` entsteht eine XRechnung in UBL. Das brauchen Sie, wenn der Kunde ausdrücklich eine XRechnung verlangt, etwa eine Behörde.

### Beispiel 4: das ZUGFeRD-PDF lesen

```bash
erechnung lesen beispiele/07_kleinunternehmer/zugferd_en16931.pdf
```

```text
Datei:        beispiele/07_kleinunternehmer/zugferd_en16931.pdf
Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
Nummer:       2026-017 vom 15.10.2026
Verkäufer:    Grafikdesign Lena Beispiel, 50667 Köln, Steuernummer 214/5678/1234
Käufer:       Beispiel Handel AG, 80331 München
Käuferref.:   BH-2026-0815
Positionen:   1
     1         1 LS   Logo-Entwicklung inkl. drei Entwürfe                 850,00 EUR
USt:          E (Steuerbefreit, z. B. § 4 UStG oder Kleinunternehmer § 19 UStG) 0 %: 0,00 EUR auf 850,00 EUR
Netto:        850,00 EUR
Brutto:       850,00 EUR
Zahlbetrag:   850,00 EUR, fällig 14.11.2026
Zahlung:      58 (SEPA-Überweisung) DE79000000001234567890
```

Netto und Brutto sind gleich, die Steuer beträgt 0,00 EUR. Die Beschreibung der Kategorie E wird in dieser Kurzansicht abgeschnitten; vollständig zeigt sie `erechnung anzeigen`.

### Beispiel 5: Rechnung ohne Steuernummer

Zum Ausprobieren wurde in einer Kopie der JSON-Datei die `steuernummer` gelöscht (`ku_ohne_stnr.json`). Schon beim Erstellen meldet die Vorprüfung den Fehler:

```bash
erechnung erstellen ku_ohne_stnr.json -o ku_ohne_stnr.xml
```

```text
  FEHLER  VP-14-4-2: Weder USt-IdNr. (BT-31) noch Steuernummer (BT-32) des Verkäufers angegeben (§ 14 Abs. 4 Nr. 2 UStG).
  Nicht mit den KoSIT-Regeln geprüft. Prüfen mit: erechnung validieren ku_ohne_stnr.xml
ku_ohne_stnr.xml: xrechnung-ubl, Rechnung 2026-017, Zahlbetrag 850,00 EUR
```

Die offizielle Prüfung lehnt die Datei ab:

```bash
erechnung validieren ku_ohne_stnr.xml
```

```text
ku_ohne_stnr.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 2 Fehler, 0 Warnungen
  FEHLER  BR-E-02: [BR-E-02]-An Invoice that contains an Invoice line (BG-25) where the Invoiced item VAT category code (BT-151) is "Exempt from VAT" shall contain the Seller VAT Identifier (BT-31), the Seller tax registration identifier (BT-32) and/or the Seller tax representative VAT identifier (BT-63).
  FEHLER  BR-DE-16: [BR-DE-16] Wenn in einer Rechnung die Steuercodes S, Z, E, AE, K, G, L oder M verwendet werden, muss mindestens eines der Elemente "Seller VAT identifier" (BT-31), "Seller tax registration identifier" (BT-32) oder "SELLER TAX REPRESENTATIVE PARTY" (BG-11) übermittelt werden.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-14-4-2: Weder USt-IdNr. (BT-31) noch Steuernummer (BT-32) des Verkäufers angegeben (§ 14 Abs. 4 Nr. 2 UStG).
```

Das Werkzeug schreibt die Datei trotz Vorprüfungsfehler. Prüfen Sie deshalb immer, bevor Sie verschicken.

### Beispiel 6: Befreiungsgrund vergessen

In einer zweiten Kopie fehlt der Block `befreiungsgruende` (`ku_ohne_grund.json`):

```bash
erechnung validieren ku_ohne_grund.xml
```

```text
ku_ohne_grund.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-E-10: [BR-E-10]-A VAT breakdown (BG-23) with VAT Category code (BT-118) "Exempt from VAT" shall have a VAT exemption reason code (BT-121) or a VAT exemption reason text (BT-120).
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-14-4-8: Steuerkategorie E ohne Befreiungsgrund (BT-120/121). Hinweis auf Steuerbefreiung oder Reverse Charge ist Pflicht (§ 14 Abs. 4 Nr. 8, § 14a UStG).
```

Ein Hinweis nur in den Notizen (BT-22) reicht der Prüfung nicht. Der Grund muss in der Steueraufschlüsselung stehen.

### Beispiel 7: empfangene E-Rechnung kostenlos ansehen

```bash
erechnung anzeigen beispiele/07_kleinunternehmer/zugferd_en16931.pdf -o ku.html
```

```text
Ansicht geschrieben: ku.html
```

Die HTML-Datei öffnen Sie im Browser. Sie zeigt Verkäufer mit Steuernummer, Positionen, die Umsatzsteuer-Tabelle mit Befreiungsgrund und die Zahlungsdaten. Unten steht: "Rechtlich maßgeblich ist der XML-Inhalt der E-Rechnung." Für eine XRechnung geht es genauso, mit `--offiziell` auch über die KoSIT-Visualisierung:

```bash
erechnung anzeigen beispiele/07_kleinunternehmer/xrechnung_ubl.xml --offiziell -o ku_kosit.html
```

```text
Ansicht geschrieben: ku_kosit.html
```

Das brauchen Sie als Kleinunternehmer jedes Mal, wenn ein Lieferant eine XRechnung schickt, die Ihr PDF-Programm nicht öffnet.

## Schritt für Schritt: als Kleinunternehmer eine E-Rechnung schreiben

### E-Rechnungen empfangen

1. **Postfach festlegen.** Eine E-Mail-Adresse für Rechnungen genügt. Nennen Sie sie Ihren Lieferanten.
2. **Werkzeug installieren.** Python 3.10 oder neuer, kein Java:
   ```bash
   pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
   ```
3. **Rechnung lesen.** Speichern Sie den Anhang und rufen Sie `erechnung lesen rechnung.xml` auf. Die Zeile `E-Rechnung:` zeigt, ob es eine E-Rechnung ist.
4. **Ansicht erzeugen.** `erechnung anzeigen rechnung.xml -o rechnung.html` und die Datei im Browser öffnen.
5. **Inhalt prüfen.** Prüfen Sie wie bei jeder Rechnung, ob Leistung, Betrag und Ihre Anschrift stimmen. Formal prüft `erechnung validieren rechnung.xml`.
6. **Original aufbewahren.** Legen Sie die empfangene XML- oder PDF-Datei unverändert ab, acht Jahre lang (§ 14b Abs. 1 UStG). Die HTML-Ansicht ist nur eine Lesehilfe.

### Freiwillig eine E-Rechnung schreiben

1. **Vorlage holen.** `erechnung beispiele bsp` schreibt die Beispiel-Eingaben in den Ordner `bsp`. Kopieren Sie `bsp/07_kleinunternehmer.json`.
2. **Eigene Daten eintragen.** Name, Anschrift, `steuernummer`, Kontakt, elektronische Adresse, IBAN, Kunde, Rechnungsnummer, Datum, Leistungszeitraum und Positionen. Jede Position bekommt `"kategorie": "E"` und `"satz": "0"`.
3. **Befreiungsgrund stehen lassen.** Der Block `befreiungsgruende` mit dem Hinweis auf § 19 UStG muss bleiben. Ob diese Regel für Ihr Unternehmen gilt, klärt Ihre Steuerberatung.
4. **Format wählen.** Will der Kunde ein PDF mit XML, nehmen Sie `--format zugferd`. Will er eine XRechnung, lassen Sie `--format` weg.
5. **Erstellen und prüfen.** `erechnung erstellen meine-rechnung.json --format zugferd -o rechnung.pdf --validieren`. Achten Sie auf `KoSIT-Regeln: GÜLTIG`.
6. **Verschicken.** Das Werkzeug versendet nicht. Schicken Sie die Datei per E-Mail oder laden Sie sie im Portal des Kunden hoch.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Position mit Kategorie S und 19 % statt E | Rechnung weist Umsatzsteuer aus, obwohl Sie nach § 19 UStG keine berechnen | `"kategorie": "E"` und `"satz": "0"` in jeder Position |
| Befreiungsgrund fehlt | KoSIT meldet BR-E-10, Vorprüfung VP-14-4-8 | Block `befreiungsgruende` mit `"E": "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet."` |
| Hinweis nur in den Notizen | Gleicher Fehler BR-E-10 | Hinweis in BT-120 setzen; die Notiz darf zusätzlich bleiben |
| Weder Steuernummer noch USt-IdNr. | KoSIT meldet BR-E-02 und BR-DE-16 | `steuernummer` beim Verkäufer eintragen |
| Empfangene XRechnung nur ausgedruckt abgelegt | Original fehlt bei einer Prüfung | Die XML-Datei unverändert aufbewahren (BMF-Schreiben vom 15.10.2025, Rn. 60) |
| Käuferreferenz fehlt in der XRechnung | KoSIT meldet BR-DE-15 | Feld `leitweg_id` füllen; im B2B genügt eine Referenz des Kunden |

## Häufige Fragen

### Muss ich als Kleinunternehmer E-Rechnungen schreiben?

Nein, Rechnungen von Kleinunternehmern sind von der Pflicht zur E-Rechnung ausgenommen (§ 34a UStDV). Sie dürfen weiter Papierrechnungen ausstellen oder, wenn der Empfänger zustimmt, zum Beispiel PDF-Rechnungen. Eine freiwillige E-Rechnung ist erlaubt.

### Muss ich als Kleinunternehmer E-Rechnungen empfangen können?

Ja, seit dem 01.01.2025 müssen alle inländischen Unternehmer E-Rechnungen empfangen können, auch Kleinunternehmer nach § 19 UStG (BMF-Schreiben vom 15.10.2025, UStAE 14.1). Ein E-Mail-Postfach genügt. Zum Lesen reicht ein kostenloser Viewer.

### Brauche ich als Kleinunternehmer eine USt-IdNr. für die E-Rechnung?

Nein, die Steuernummer genügt. § 14 Abs. 4 UStG verlangt die Steuernummer oder die USt-IdNr. In der E-Rechnung steht die Steuernummer in BT-32. Mindestens eine der beiden Angaben muss vorhanden sein, sonst meldet die Prüfung BR-DE-16.

### Welche Steuerkategorie nutze ich als Kleinunternehmer?

Die Steuerkategorie ist `E` (steuerbefreit) mit 0 %. Dazu gehört ein Befreiungsgrund in BT-120, zum Beispiel "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet." So ist es in [`beispiele/07_kleinunternehmer`](../../beispiele/07_kleinunternehmer/) umgesetzt und von den KoSIT-Regeln als gültig geprüft.

### Welche Software brauche ich als Kleinunternehmer für E-Rechnungen?

Zum Empfangen reichen ein E-Mail-Postfach und ein kostenloser Viewer. Dieses Repo bietet mit `erechnung anzeigen` und `erechnung lesen` einen solchen Viewer für die Kommandozeile. Daneben gibt es den Open-Source-Viewer [Quba](https://github.com/ZUGFeRD/quba-viewer) (Apache-2.0) für Windows, macOS und Linux, der offline arbeitet. Mehr in [E-Rechnung Software kostenlos](./e-rechnung-software-kostenlos.md).

### Brauche ich als Kleinunternehmer eine fortlaufende Rechnungsnummer?

Laut BMF-Schreiben vom 15.10.2025 (UStAE 14.5 Abs. 14) brauchen Rechnungen von Kleinunternehmern keine fortlaufende Nummer. In einer E-Rechnung ist eine Rechnungsnummer (BT-1) trotzdem Pflicht (BR-02). Eine eindeutige Nummer hilft außerdem bei Zahlung und Mahnung.

### Was passiert, wenn ich die Kleinunternehmerregelung verlasse?

Dann gelten für Ihre Rechnungen an andere inländische Unternehmer die allgemeinen Fristen zur E-Rechnung aus § 27 Abs. 38 UStG. Ab dem 01.01.2028 ist die E-Rechnung im B2B für alle verpflichtend. Die Übergangsregeln stehen in [E-Rechnung Pflicht](./e-rechnung-pflicht.md); den Zeitpunkt klären Sie mit der Steuerberatung.

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [E-Rechnung Pflicht: ab wann, für wen und welche Übergangsfristen gelten](./e-rechnung-pflicht.md)
- [Was ist eine E-Rechnung?](./was-ist-eine-e-rechnung.md)
- [E-Rechnung empfangen und lesen](./e-rechnung-empfangen.md)
- [E-Rechnung erstellen](./e-rechnung-erstellen.md)
- [E-Rechnung archivieren](./e-rechnung-archivieren.md)
- [Lexware, sevdesk, SAP: E-Rechnung aus dem eigenen Programm testen](./e-rechnung-buchhaltungssoftware.md)
- Beispiel Kleinunternehmer: [Eingabe](../../beispiele/07_kleinunternehmer/eingabe.json), [UBL](../../beispiele/07_kleinunternehmer/xrechnung_ubl.xml), [CII](../../beispiele/07_kleinunternehmer/xrechnung_cii.xml), [Ansicht](../../beispiele/07_kleinunternehmer/ansicht.html), [ZUGFeRD-PDF](../../beispiele/07_kleinunternehmer/zugferd_en16931.pdf)
