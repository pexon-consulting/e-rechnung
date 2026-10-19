# ZUGFeRD: Format, Profile und Versionen der ZUGFeRD-Rechnung erklärt

ZUGFeRD ist ein hybrides Rechnungsformat: eine PDF/A-3-Datei, die man wie jede PDF-Rechnung lesen kann, mit einem eingebetteten XML nach UN/CEFACT CII, das Programme automatisch verarbeiten. Für Deutschland relevant sind sechs Profile; MINIMUM und BASIC WL sind keine E-Rechnung, BASIC, EN 16931, EXTENDED und XRECHNUNG sind es (BMF-Schreiben vom 15.10.2025, UStAE 14.1 Abs. 14). Dazu kommt seit ZUGFeRD 2.5 das französische Profil EXTENDED-CTC-FR. Aktuell ist ZUGFeRD 2.5.2, technisch identisch mit Factur-X 1.09.2 und gültig ab 01.09.2026.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Buchhaltung, Geschäftsführung und Entwickler, die das Format verstehen wollen. Die XML-Ausschnitte sind zum Nachschlagen.

## Das Wichtigste in Kürze

- Eine ZUGFeRD-Rechnung ist ein PDF/A-3 mit einer eingebetteten XML-Datei, meist `factur-x.xml`, beim Profil XRECHNUNG `xrechnung.xml`.
- Maßgeblich ist das XML: Weichen Bildteil und XML voneinander ab, gilt laut BMF-Schreiben vom 15.10.2025 (UStAE 14.4 Abs. 3) der strukturierte Teil.
- ZUGFeRD ab Version 2.0.1 ist eine zulässige E-Rechnung, ausgenommen die Profile MINIMUM und BASIC WL (UStAE 14.1 Abs. 14).
- ZUGFeRD und Factur-X sind dieselbe Spezifikation: ZUGFeRD 2.5.2 entspricht Factur-X 1.09.2.
- Welches Profil eine Datei hat, steht im XML im Feld BT-24 (`GuidelineSpecifiedDocumentContextParameter/ID`).
- Mit `erechnung lesen`, `erechnung extrahieren`, `erechnung validieren` und `erechnung erstellen --format zugferd` lesen, prüfen und erzeugen Sie ZUGFeRD-Dateien lokal und ohne Java.

## Was ist ZUGFeRD? Abkürzung und Herausgeber

ZUGFeRD steht für "Zentraler User Guide des Forums elektronische Rechnung Deutschland". Herausgeber ist das Forum elektronische Rechnung Deutschland (FeRD). Die Spezifikation, die Schemas und Musterrechnungen gibt es als Infopaket bei [ferd-net.de](https://www.ferd-net.de/standards/zugferd).

Eine ZUGFeRD-Rechnung ist eine Rechnung in einer einzigen Datei, die zwei Teile hat:

- den Bildteil: ein PDF, das Menschen am Bildschirm oder ausgedruckt lesen,
- den strukturierten Teil: ein XML nach UN/CEFACT Cross Industry Invoice (CII), das Buchhaltungsprogramme ohne Abtippen übernehmen.

Das Umsatzsteuerrecht nennt so etwas ein Hybridformat (UStAE 14.1 Abs. 14 in der Fassung des BMF-Schreibens vom 15.10.2025). Alle umsatzsteuerlichen Pflichtangaben müssen im strukturierten Teil stehen (BMF-Schreiben vom 15.10.2025, Rn. 35). Ein PDF ohne eingebettetes XML ist dagegen eine sonstige Rechnung, keine E-Rechnung (UStAE 14.1 Abs. 2).

### ZUGFeRD und Factur-X: derselbe Standard

Factur-X ist der Name derselben Spezifikation in Frankreich ([fnfe-mpe.org](https://fnfe-mpe.org/factur-x/)). ZUGFeRD 2.5.2 und Factur-X 1.09.2 sind technisch identisch. Deshalb heißt die eingebettete Datei auch bei deutschen Rechnungen `factur-x.xml`, und die Profil-Kennungen beginnen mit `urn:factur-x.eu`.

## ZUGFeRD-Format: PDF/A-3 plus eingebettetes XML

Seit ZUGFeRD 2.0 ist PDF/A-3 (ISO 19005-3:2012) die Grundlage ([ferd-net.de](https://www.ferd-net.de/standards/zugferd)). PDF/A-3 ist die Archivvariante von PDF, die eingebettete Dateien erlaubt. Ein ZUGFeRD-PDF besteht technisch aus vier Bausteinen, so beschreibt es auch der Code in `src/erechnung/pdf.py`:

| Baustein | Inhalt | Wert im Werkzeug |
| --- | --- | --- |
| Eingebettete Datei | das CII-XML | `factur-x.xml`, beim Profil XRECHNUNG `xrechnung.xml` |
| AFRelationship | Beziehung der Datei zum PDF | `/Alternative`, bei MINIMUM und BASIC WL `/Data` |
| `/AF`-Eintrag | Verweis im Dokumentkatalog auf die Datei | ein Eintrag je Rechnungs-XML |
| XMP-Metadaten | PDF/A-Kennung und Factur-X-Schema | `pdfaid:part` 3, `fx:ConformanceLevel` je Profil |

### Dateiname des eingebetteten XML

Der Dateiname hängt von Version und Profil ab (laut Mustang-Quellcode, Faktenbasis Abschnitt 2.2):

| Version | Profil | Dateiname im PDF |
| --- | --- | --- |
| ZUGFeRD 2.1 und neuer, Factur-X | alle außer XRECHNUNG | `factur-x.xml` |
| ZUGFeRD 2.1 und neuer | XRECHNUNG | `xrechnung.xml` |
| ZUGFeRD 2.0 | alle | `zugferd-invoice.xml` |
| ZUGFeRD 1.0 | alle | `ZUGFeRD-invoice.xml` |

`erechnung lesen` und `erechnung extrahieren` finden alle diese Namen. Steht im PDF eine andere XML-Datei, nimmt das Werkzeug die erste, die nach `CrossIndustryInvoice` oder `Invoice` aussieht.

### XMP-Metadaten: so steht das Profil im PDF

Die XMP-Metadaten sind ein XML-Block im PDF, den Programme ohne Auspacken des Anhangs lesen. Für ZUGFeRD 2 und Factur-X gilt der Namensraum `urn:factur-x:pdfa:CrossIndustryDocument:invoice:1p0#` mit dem Präfix `fx`. ZUGFeRD 2.0 nutzte `urn:zugferd:pdfa:CrossIndustryDocument:invoice:2p0#`, ZUGFeRD 1.0 `urn:ferd:pdfa:CrossIndustryDocument:invoice:1p0#`.

So lesen Sie die Metadaten aus dem Beispiel `beispiele/01_standard/zugferd_en16931.pdf` mit pypdf aus:

```python
from pypdf import PdfReader

pdf = PdfReader("beispiele/01_standard/zugferd_en16931.pdf")
print(pdf.xmp_metadata.stream.get_data().decode("utf-8"))

katalog = pdf.trailer["/Root"]
for ref in katalog["/AF"]:
    datei = ref.get_object()
    print(datei["/F"], datei["/AFRelationship"], datei["/EF"]["/F"].get_object()["/Subtype"])
```

Echte Ausgabe (gekürzt):

```xml
<rdf:Description rdf:about="" xmlns:pdfaid="http://www.aiim.org/pdfa/ns/id/">
 <pdfaid:part>3</pdfaid:part>
 <pdfaid:conformance>B</pdfaid:conformance>
</rdf:Description>
...
<rdf:Description rdf:about="" xmlns:fx="urn:factur-x:pdfa:CrossIndustryDocument:invoice:1p0#">
 <fx:DocumentType>INVOICE</fx:DocumentType>
 <fx:DocumentFileName>factur-x.xml</fx:DocumentFileName>
 <fx:Version>1.0</fx:Version>
 <fx:ConformanceLevel>EN 16931</fx:ConformanceLevel>
</rdf:Description>
...
<pdfaSchema:schema>Factur-X PDFA Extension Schema</pdfaSchema:schema>
<pdfaSchema:namespaceURI>urn:factur-x:pdfa:CrossIndustryDocument:invoice:1p0#</pdfaSchema:namespaceURI>
<pdfaSchema:prefix>fx</pdfaSchema:prefix>
...
```

```text
factur-x.xml /Alternative /text/xml
```

Die Felder bedeuten:

- `pdfaid:part` 3 und `pdfaid:conformance` B: die Datei erklärt sich als PDF/A-3b.
- `fx:DocumentType`: Art des Dokuments, hier `INVOICE`.
- `fx:DocumentFileName`: Name des eingebetteten XML.
- `fx:Version`: Version des Metadaten-Schemas. Der Wert `1.0` passt zur Kennung `1p0` im Namensraum und ist nicht die ZUGFeRD-Versionsnummer.
- `fx:ConformanceLevel`: das Profil (MINIMUM, BASIC WL, BASIC, EN 16931, EXTENDED, XRECHNUNG).
- Der Block `pdfaExtension:schemas` beschreibt die `fx`-Felder, weil PDF/A eigene Metadaten nur mit dieser Beschreibung erlaubt.

## ZUGFeRD-Profile: welche sind E-Rechnungen?

Ein Profil legt fest, wie viele Angaben das XML enthält. Das Profil steht im XML im Feld BT-24 (Specification identifier), in CII unter `ram:GuidelineSpecifiedDocumentContextParameter/ram:ID`. Laut BMF-Schreiben vom 15.10.2025 (UStAE 14.1 Abs. 14) gilt: "ZUGFeRD ab der Version 2.0.1 - ausgenommen die Profile MINIMUM und BASIC-WL - beruht auf der Normenreihe EN 16931 und fällt somit unter die zulässigen E-Rechnungs-Formate."

| Profil | Kennung in BT-24 (GuidelineID) | `fx:ConformanceLevel` | AFRelationship | E-Rechnung nach BMF |
| --- | --- | --- | --- | --- |
| MINIMUM | `urn:factur-x.eu:1p0:minimum` | MINIMUM | Data | nein |
| BASIC WL | `urn:factur-x.eu:1p0:basicwl` | BASIC WL | Data | nein |
| BASIC | `urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic` | BASIC | Alternative | ja |
| EN 16931 (COMFORT) | `urn:cen.eu:en16931:2017` | EN 16931 | Alternative | ja |
| EXTENDED | `urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended` | EXTENDED | Alternative | ja |
| XRECHNUNG | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` | XRECHNUNG | Alternative | ja |

Kurz erklärt:

- MINIMUM und BASIC WL enthalten nicht alle Pflichtangaben einer Rechnung. Deshalb zählen sie nicht als E-Rechnung.
- BASIC ist das kleinste Profil, das als E-Rechnung zählt. Seine Kennung trägt den Zusatz `#compliant` zur EN 16931.
- EN 16931, auch COMFORT genannt, entspricht der Norm EN 16931 ohne Zusatz. Für Rechnungen zwischen Unternehmen ist das die übliche Wahl.
- EXTENDED geht mit dem Zusatz `#conformant` über EN 16931 hinaus und bietet zusätzliche Felder. In ZUGFeRD 2.5.2 kamen Elemente für die französische B2B-Reform und das überarbeitete Datenmodell EN 16931-1:2026 hinzu.
- XRECHNUNG ist ein ZUGFeRD-PDF, dessen XML die Regeln der XRechnung erfüllt (zum Beispiel BT-10 und elektronische Adressen). Mehr dazu unter [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md).

Das neue französische Profil EXTENDED-CTC-FR nennt das BMF-Schreiben nicht. Ob es in Deutschland als E-Rechnung gilt, ist offen; klären Sie das im Einzelfall mit der Steuerberatung.

## ZUGFeRD-Versionen: welche ist aktuell?

Die aktuelle Version ist ZUGFeRD 2.5.2, identisch mit Factur-X 1.09.2. FeRD hat das Infopaket am 04.08.2026 veröffentlicht, gültig ist es ab 01.09.2026 ([ferd-net.de](https://www.ferd-net.de/aktuelles-veranstaltungen/aktuelles/news/zugferd-252-veroeffentlicht)). Die Versionen sind rückwärtskompatibel.

| Version | Veröffentlicht | Hinweis |
| --- | --- | --- |
| 2.0.1 | 15.10.2019 | ab hier zulässige E-Rechnung (außer MINIMUM, BASIC WL) |
| 2.1 | 24.03.2020 | |
| 2.1.1 | 01.07.2020 | |
| 2.2 | 01.03.2022 | |
| 2.3 | 18.09.2024 | |
| 2.3.2 | 13.11.2024 | |
| 2.3.3 | 07.05.2025 | |
| 2.4 (Factur-X 1.08) | 04.12.2025 | in Kraft 15.01.2026, CII D22B, rückwärtskompatibel zu D16B |
| 2.5 | 10.06.2026 | |
| 2.5.2 (Factur-X 1.09.2) | 04.08.2026 | gültig ab 01.09.2026 |

Quelle: [ZUGFeRD-Versionsarchiv bei FeRD](https://www.ferd-net.de/standards/zugferd-versionsarchiv). Ältere Versionen lassen sich dort nicht mehr herunterladen. Ein nächstes Release ist laut FeRD für Herbst 2026 angekündigt.

Wichtig für die Praxis: Die Profil-Kennung in BT-24 nennt keine Versionsnummer. Eine Datei mit `urn:cen.eu:en16931:2017` kann aus einem Programm mit ZUGFeRD 2.1 oder 2.5.2 stammen. Die KoSIT-Prüfregeln, die `erechnung validieren` nutzt, prüfen CII gegen das Schema D16B.

## ZUGFeRD-Datei erkennen und das XML herausholen

Ob ein PDF eine ZUGFeRD-Rechnung ist, sehen Sie im PDF-Viewer meist nur an der Büroklammer für Anhänge. Sicherer ist es, das PDF zu lesen:

```bash
erechnung lesen beispiele/01_standard/zugferd_en16931.pdf
```

```text
Datei:        beispiele/01_standard/zugferd_en16931.pdf
Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
Nummer:       RE-2026-0001 vom 15.10.2026
Verkäufer:    Nordlicht Beispiel GmbH, 20095 Hamburg, USt-IdNr. DE123456789
Käufer:       Beispiel Handel AG, 80331 München
Käuferref.:   BH-2026-0815
...
Brutto:       2.009,91 EUR
Zahlbetrag:   2.009,91 EUR, fällig 14.11.2026
Zahlung:      58 (SEPA-Überweisung) DE79000000001234567890
```

Das XML holen Sie mit `erechnung extrahieren` heraus. Ohne `-o` landet es neben dem PDF mit der Endung `.xml`, mit `-o -` auf der Standardausgabe:

```bash
erechnung extrahieren beispiele/01_standard/zugferd_en16931.pdf -o factur-x.xml
```

```text
factur-x.xml aus beispiele/01_standard/zugferd_en16931.pdf gespeichert als factur-x.xml
```

Die ersten Zeilen des XML zeigen das Profil:

```xml
<rsm:CrossIndustryInvoice xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100" ...>
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
    <ram:TypeCode>380</ram:TypeCode>
    ...
```

## ZUGFeRD-Rechnung prüfen

`erechnung validieren` holt das XML aus dem PDF und prüft es mit den offiziellen KoSIT-Regeln, dazu kommt eine eigene Vorprüfung:

```bash
erechnung validieren beispiele/01_standard/zugferd_en16931.pdf
```

```text
beispiele/01_standard/zugferd_en16931.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
```

Was geprüft wird und was nicht:

| Profil | Prüfung im Werkzeug |
| --- | --- |
| EN 16931 | KoSIT-Szenario EN16931 (CII) |
| XRECHNUNG | KoSIT-Szenario XRechnung (CII) mit BR-DE-Regeln |
| BASIC, EXTENDED | Kern nach EN 16931, mit Hinweis; die KoSIT hat dafür kein eigenes Szenario |
| MINIMUM, BASIC WL | kein Szenario, Vorprüfung meldet `VP-FORMAT` (keine E-Rechnung) |

Die PDF/A-3-Konformität des Bildteils prüft weder der KoSIT-Validator noch dieses Werkzeug. Das Java-Werkzeug Mustang prüft laut eigener Dokumentation auch PDF/A-3 ([mustangproject.org](https://www.mustangproject.org/commandline/)). Alle Fehlermeldungen erklärt die Anleitung [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md).

## ZUGFeRD-Rechnung erstellen

Aus Rechnungsdaten im JSON- oder TOML-Format erzeugt `erechnung erstellen` ein fertiges ZUGFeRD-PDF. Es gibt zwei ZUGFeRD-Formate:

| `--format` | Profil | Dateiname im PDF | Wann |
| --- | --- | --- | --- |
| `zugferd` | EN 16931 | `factur-x.xml` | Rechnungen zwischen Unternehmen |
| `zugferd-xrechnung` | XRECHNUNG | `xrechnung.xml` | Empfänger verlangt XRechnung-Regeln, aber auch ein PDF |

Ohne `--pdf` baut das Werkzeug mit Ghostscript eine schlichte PDF/A-3-Ansicht. Mit `--pdf rechnung.pdf` nimmt es Ihr eigenes Layout als Bildteil, siehe [PDF in ZUGFeRD umwandeln](./pdf-in-zugferd-umwandeln.md).

```bash
erechnung erstellen beispiele/01_standard/eingabe.json --format zugferd -o rechnung_zugferd.pdf
```

```text
rechnung_zugferd.pdf: zugferd, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
```

Summen und Steuern rechnet das Werkzeug selbst aus den Positionen aus. Hinweise der Vorprüfung erscheinen auf der Fehlerausgabe (stderr).

## ZUGFeRD-Rechnung lesen und prüfen: Beispiele

### Beispiel 1: Profil und Inhalt einer eingegangenen ZUGFeRD-Rechnung ansehen

```bash
erechnung lesen beispiele/01_standard/zugferd_en16931.pdf
```

```text
Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
...
```

Das brauchen Sie im Rechnungseingang, um zu sehen, ob ein PDF überhaupt eine E-Rechnung ist.

### Beispiel 2: ZUGFeRD-Rechnung mit Profil XRECHNUNG erzeugen und gleich prüfen

```bash
erechnung erstellen beispiele/01_standard/eingabe.json --format zugferd-xrechnung -o rechnung_xr.pdf --validieren
```

```text
rechnung_xr.pdf: zugferd-xrechnung, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 XRechnung (CII))
```

```bash
erechnung lesen rechnung_xr.pdf
```

```text
Datei:        rechnung_xr.pdf
Format:       ZUGFeRD-Profil XRECHNUNG, XRechnung 3.0 (CII) (eingebettet als xrechnung.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
```

Das brauchen Sie, wenn ein Kunde XRechnung-Regeln verlangt und trotzdem ein lesbares PDF haben möchte.

### Beispiel 3: Dieselben Daten, zwei Profile, zwei Ergebnisse

Die Datei `ohne_bt10.json` ist `beispiele/01_standard/eingabe.json` ohne die Felder `leitweg_id` (BT-10) und `kaeufer.elektronische_adresse` (BT-49). Mit dem Profil EN 16931 ist das Ergebnis gültig, mit dem Profil XRECHNUNG nicht:

```bash
erechnung erstellen ohne_bt10.json --format zugferd -o ohne_bt10.pdf
erechnung validieren ohne_bt10.pdf
```

```text
ohne_bt10.pdf: zugferd, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
ohne_bt10.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
```

```bash
erechnung erstellen ohne_bt10.json --format zugferd-xrechnung -o ohne_bt10_xr.pdf --validieren
```

```text
ohne_bt10_xr.pdf: zugferd-xrechnung, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
  KoSIT-Regeln: UNGÜLTIG (EN16931 XRechnung (CII))
  FEHLER  PEPPOL-EN16931-R010: [PEPPOL-EN16931-R010]-Buyer electronic address MUST be provided
  FEHLER  BR-DE-15: [BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.
```

Das zeigt, warum Sie das Profil kennen müssen: Die XRechnung-Regeln verlangen mehr als EN 16931.

### Beispiel 4: Profil BASIC WL erkennen

Für dieses Beispiel ist in der oben extrahierten `factur-x.xml` nur die Kennung in BT-24 durch `urn:factur-x.eu:1p0:basicwl` ersetzt.

```bash
erechnung validieren basicwl.xml
```

```text
basicwl.xml: CII Profil BASIC WL
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario kein Szenario, 1 Fehler, 0 Warnungen
  FEHLER  SZENARIO: Kein passendes Prüfszenario. Erwartet wird UBL Invoice/CreditNote oder CII mit einer Spezifikationskennung (BT-24) für XRechnung 3.0 oder EN 16931.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-FORMAT: CII Profil BASIC WL: Dieses ZUGFeRD-Profil enthält nicht alle Pflichtangaben und gilt nicht als E-Rechnung nach § 14 UStG. Mindestens Profil BASIC, besser EN 16931 verwenden.
```

Das brauchen Sie, wenn ein Lieferant ZUGFeRD schickt und Sie wissen wollen, ob es als E-Rechnung zählt. Exit-Code ist 1.

### Beispiel 5: Ein PDF ohne XML

```bash
erechnung lesen leer.pdf
```

```text
leer.pdf: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
```

So erkennen Sie, dass eine "PDF-Rechnung" keine ZUGFeRD-Rechnung ist.

### Beispiel 6: Das XML direkt weiterverarbeiten

Mit `-o -` schreibt `erechnung extrahieren` das XML auf die Standardausgabe:

```bash
erechnung extrahieren beispiele/01_standard/zugferd_en16931.pdf -o - | head -3
```

```text
<?xml version='1.0' encoding='UTF-8'?>
<rsm:CrossIndustryInvoice xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100" ...>
  <rsm:ExchangedDocumentContext>
```

Das brauchen Sie in Skripten, die das XML ohne Zwischendatei weitergeben.

## Schritt für Schritt: eine ZUGFeRD-Rechnung prüfen und auslesen

1. Installieren Sie das Werkzeug (Python 3.10 oder neuer, kein Java nötig):

   ```bash
   pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
   ```

2. Öffnen Sie ein Terminal im Ordner mit der Rechnung.
3. Lesen Sie die Rechnung: `erechnung lesen rechnung.pdf`. In der Zeile "Format" steht das Profil, in der Zeile "E-Rechnung" ja oder nein.
4. Prüfen Sie die Rechnung: `erechnung validieren rechnung.pdf`. Beim ersten Aufruf lädt das Werkzeug die KoSIT-Regeln, danach läuft es offline. Die Rechnung verlässt Ihren Rechner nicht.
5. Bewahren Sie bei Bedarf einen Prüfbericht auf: `erechnung validieren rechnung.pdf --bericht prüfberichte`. Laut BMF-Schreiben vom 15.10.2025, Rn. 35a, bietet es sich zum Nachweis an, den Validierungsbericht aufzubewahren.
6. Holen Sie das XML heraus, wenn ein anderes Programm es braucht: `erechnung extrahieren rechnung.pdf`.
7. Sehen Sie sich den Inhalt des XML als HTML an: `erechnung anzeigen rechnung.pdf`. So sehen Sie den maßgeblichen strukturierten Teil, nicht nur das PDF-Bild.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| PDF ohne eingebettetes XML | "Das PDF enthält kein eingebettetes Rechnungs-XML" | Beim Absender eine ZUGFeRD-Datei oder XRechnung anfordern, ein reines PDF ist eine sonstige Rechnung. |
| Profil MINIMUM oder BASIC WL | `VP-FORMAT`, "gilt nicht als E-Rechnung" | Absender um Profil BASIC, besser EN 16931, bitten. |
| EN-16931-Datei als XRechnung erwartet | `BR-DE-15`, `PEPPOL-EN16931-R010` bei Prüfung als XRechnung | Mit `--format zugferd-xrechnung` erzeugen und BT-10 sowie elektronische Adressen angeben. |
| Bildteil und XML stimmen nicht überein | PDF zeigt andere Beträge als `erechnung lesen` | Das XML ist maßgeblich (BMF-Schreiben vom 15.10.2025, UStAE 14.4 Abs. 3). Absender um eine berichtigte Rechnung bitten. |
| Datei als PDF/A-3 gekennzeichnet, aber nicht konform | andere Prüfprogramme melden PDF/A-Fehler | Beim Erstellen `--pdfa` nutzen; PDF/A-3 separat prüfen, zum Beispiel mit Mustang. |
| UBL-XML statt CII eingebettet | "Unbekannte Guideline-ID für ZUGFeRD" beim Einbetten | ZUGFeRD verlangt CII: mit `--format en16931-cii` oder `xrechnung-cii` erzeugen. |

## Häufige Fragen

### Was ist eine ZUGFeRD-Rechnung?

Eine ZUGFeRD-Rechnung ist ein PDF/A-3 mit eingebettetem CII-XML, das alle Rechnungsdaten strukturiert enthält. Menschen lesen das PDF, Programme das XML. Ab ZUGFeRD 2.0.1 und mit einem Profil ab BASIC ist sie eine E-Rechnung nach § 14 UStG.

### Ist ZUGFeRD eine E-Rechnung?

Ja, wenn die Version mindestens 2.0.1 ist und das Profil BASIC, EN 16931, EXTENDED oder XRECHNUNG lautet (BMF-Schreiben vom 15.10.2025, UStAE 14.1 Abs. 14). MINIMUM und BASIC WL sind keine E-Rechnung.

### Was ist der Unterschied zwischen ZUGFeRD und Factur-X?

Es gibt keinen technischen Unterschied. ZUGFeRD 2.5.2 und Factur-X 1.09.2 sind identisch; Factur-X ist der Name in Frankreich, ZUGFeRD der Name in Deutschland.

### Welche ZUGFeRD-Version ist aktuell?

Aktuell ist ZUGFeRD 2.5.2 (Factur-X 1.09.2), veröffentlicht am 04.08.2026 und gültig ab 01.09.2026. Die Versionen sind rückwärtskompatibel, ältere Dateien ab 2.0.1 bleiben zulässig.

### Welches ZUGFeRD-Profil soll ich verwenden?

Für Rechnungen zwischen Unternehmen ist EN 16931 (COMFORT) die übliche Wahl. Verlangt ein Empfänger die XRechnung-Regeln, nehmen Sie das Profil XRECHNUNG oder gleich eine reine XRechnung. Welches Format Ihr Empfänger braucht, klären Sie mit ihm; die Formatwahl ist laut UStAE 14.1 Abs. 12 zivilrechtlich zwischen den Parteien zu regeln.

### Woran erkenne ich eine ZUGFeRD-Datei?

An einem eingebetteten Anhang `factur-x.xml`, `xrechnung.xml` oder `zugferd-invoice.xml` und an den `fx`-Feldern in den XMP-Metadaten. Am einfachsten zeigt es `erechnung lesen datei.pdf` in der Zeile "Format".

### Was gilt, wenn PDF und XML unterschiedliche Beträge zeigen?

Dann gilt das XML. Laut BMF-Schreiben vom 15.10.2025 (UStAE 14.4 Abs. 3) ist bei Abweichungen der strukturierte Teil maßgebend. Prüfen Sie deshalb das XML, zum Beispiel mit `erechnung anzeigen`, und nicht nur das PDF-Bild.

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [XRechnung oder ZUGFeRD: Unterschied und welches Format Sie brauchen](./xrechnung-oder-zugferd.md)
- [PDF in ZUGFeRD umwandeln](./pdf-in-zugferd-umwandeln.md)
- [E-Rechnung erstellen](./e-rechnung-erstellen.md)
- [E-Rechnung prüfen: Validator mit den offiziellen Regeln](./e-rechnung-validator.md)
- [XRechnung: Format, Aufbau und Pflichtfelder](./xrechnung.md)
- [Was ist eine E-Rechnung? Definition, Formate und wie sie aussieht](./was-ist-eine-e-rechnung.md)
- [E-Rechnung Pflicht: ab wann, für wen und welche Übergangsfristen gelten](./e-rechnung-pflicht.md)
- [E-Rechnung Beispiel: XRechnung und ZUGFeRD Beispieldateien zum Herunterladen](./e-rechnung-beispiel.md)
- Beispiel-PDF: [`beispiele/01_standard/zugferd_en16931.pdf`](../../beispiele/01_standard/zugferd_en16931.pdf), Übersicht aller Beispiele: [`beispiele/README.md`](../../beispiele/README.md)
