# PDF in ZUGFeRD umwandeln: aus einer PDF-Rechnung eine E-Rechnung machen

Ein PDF lässt sich nicht per Knopfdruck in ZUGFeRD umwandeln: Für eine ZUGFeRD-Rechnung müssen die Rechnungsdaten als strukturiertes XML vorliegen, das in das PDF eingebettet wird. Sie erfassen die Daten also einmal als JSON oder TOML und betten das daraus erzeugte XML kostenlos mit `erechnung erstellen ... --format zugferd --pdf rechnung.pdf` oder `erechnung zugferd rechnung.xml --pdf rechnung.pdf` in Ihr vorhandenes PDF ein. Mit `--pdfa` macht Ghostscript aus dem PDF vorher ein PDF/A-3.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Selbstständige, Buchhaltung und Entwickler, die Rechnungen aus einer Datei erzeugen wollen. Wer ein Rechnungsprogramm nutzt, erstellt E-Rechnungen meist direkt dort.

## Das Wichtigste in Kürze

- Ein PDF ohne eingebettetes XML ist eine sonstige Rechnung, keine E-Rechnung (UStAE 14.1 Abs. 2 in der Fassung des BMF-Schreibens vom 15.10.2025).
- "Umwandeln" heißt: Rechnungsdaten strukturiert erfassen, daraus CII-XML erzeugen und dieses XML in Ihr PDF einbetten.
- Das Werkzeug liest kein PDF-Layout aus und erkennt keinen Text auf gescannten Rechnungen; die Daten kommen aus einer JSON- oder TOML-Datei.
- Das Ergebnis ist ein PDF mit `factur-x.xml` (Profil EN 16931) oder `xrechnung.xml` (Profil XRECHNUNG), das Sie mit `erechnung validieren` prüfen.
- Weichen PDF-Inhalt und XML voneinander ab, ist laut BMF-Schreiben vom 15.10.2025 (UStAE 14.4 Abs. 3) der strukturierte Teil maßgebend; das Werkzeug vergleicht beide nicht.
- Für eine reine XRechnung brauchen Sie kein PDF, sondern nur das XML aus `erechnung erstellen`.

## Kann man ein PDF in eine E-Rechnung umwandeln?

Nicht automatisch. Eine E-Rechnung ist nach § 14 Abs. 1 Satz 3 UStG "eine Rechnung, die in einem strukturierten elektronischen Format ausgestellt, übermittelt und empfangen wird und eine elektronische Verarbeitung ermöglicht". Ein PDF enthält Text und Grafik für das Auge, aber keine Felder, die ein Programm sicher zuordnen kann. Welche Zahl der Nettobetrag ist und welche die Steuer, weiß nur, wer die Rechnung geschrieben hat.

Darum geht es in drei Schritten:

1. Rechnungsdaten strukturiert erfassen (JSON oder TOML).
2. Daraus das XML nach EN 16931 erzeugen lassen.
3. Das XML in Ihr PDF einbetten. Das PDF bleibt der Bildteil, das XML ist der maßgebliche strukturierte Teil.

Das Ergebnis ist ein Hybridformat nach UStAE 14.1 Abs. 14: eine Datei mit PDF und XML. Alle umsatzsteuerlichen Pflichtangaben müssen im XML stehen (BMF-Schreiben vom 15.10.2025, Rn. 35).

Bis zum 31.12.2026 dürfen Sie PDF-Rechnungen an Unternehmen noch mit Zustimmung des Empfängers verschicken, danach gelten die Übergangsregeln nach § 27 Abs. 38 UStG. Details stehen in [E-Rechnung Pflicht](./e-rechnung-pflicht.md).

## Was Sie brauchen: Rechnungsdaten als JSON oder TOML

Das Werkzeug erwartet die Angaben der Rechnung in einer Eingabedatei. Summen und Steuern rechnet es selbst aus den Positionen aus. Diese Datei `rechnung.json` reicht für eine gültige ZUGFeRD-Rechnung im Profil EN 16931 und für eine XRechnung:

```json
{
  "nummer": "RE-2026-0001",
  "datum": "2026-10-15",
  "faellig": "2026-11-14",
  "leitweg_id": "BH-2026-0815",
  "verkaeufer": {
    "name": "Nordlicht Beispiel GmbH",
    "adresse": {"strasse": "Musterstraße 1", "plz": "20095", "ort": "Hamburg", "land": "DE"},
    "ust_id": "DE123456789",
    "elektronische_adresse": "rechnung@nordlicht.example",
    "kontakt": {"name": "Erika Mustermann", "telefon": "+49 40 66969123", "email": "buchhaltung@nordlicht.example"}
  },
  "kaeufer": {
    "name": "Beispiel Handel AG",
    "adresse": {"strasse": "Hauptstraße 5", "plz": "80331", "ort": "München", "land": "DE"},
    "elektronische_adresse": "eingangsrechnung@beispiel-handel.example"
  },
  "zahlung": {"art": "58", "iban": "DE79000000001234567890"},
  "leistung_von": "2026-09-01",
  "leistung_bis": "2026-09-30",
  "positionen": [
    {"id": "1", "name": "Beratung Einführung E-Rechnung", "menge": "12", "einheit": "HUR", "preis": "120.00", "satz": "19"},
    {"id": "2", "name": "Softwarelizenz Rechnungseingang (Monat)", "menge": "1", "einheit": "MON", "preis": "249.00", "satz": "19"}
  ]
}
```

Das Feld `leitweg_id` füllt die Käuferreferenz BT-10. Im B2B ist das nicht die Leitweg-ID einer Behörde, sondern eine Referenz des Käufers; für XRechnung ist BT-10 Pflicht (BR-DE-15). Weitere Felder wie Bestellnummer, Skonto oder Notizen zeigt die vollständige Vorlage [`beispiele/01_standard/eingabe.json`](../../beispiele/01_standard/eingabe.json). Mit `erechnung beispiele` schreiben Sie alle 9 Beispiel-Eingaben in einen Ordner.

Die Vorlage-PDF in dieser Anleitung heißt `rechnung.pdf`. Sie ist eine einseitige Rechnung mit denselben Angaben, erzeugt mit Ghostscript, mit nicht eingebetteten Schriften und ohne Farbprofil. So ein PDF ist noch keine E-Rechnung:

```bash
erechnung lesen rechnung.pdf
```

```text
rechnung.pdf: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
```

## Weg 1: XML erzeugen und einbetten in einem Schritt

`erechnung erstellen` liest die Eingabedatei, erzeugt das CII-XML und bettet es in die Vorlage ein:

```bash
erechnung erstellen rechnung.json --format zugferd --pdf rechnung.pdf --pdfa -o RE-2026-0001_pdfa.pdf --validieren
```

```text
RE-2026-0001_pdfa.pdf: zugferd, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 (CII))
```

| Option | Wirkung |
| --- | --- |
| `--format zugferd` | Profil EN 16931, eingebettet als `factur-x.xml` |
| `--format zugferd-xrechnung` | Profil XRECHNUNG, eingebettet als `xrechnung.xml` |
| `--pdf rechnung.pdf` | Ihr PDF wird der Bildteil; ohne diese Option baut Ghostscript eine schlichte Ansicht |
| `--pdfa` | Ghostscript wandelt die Vorlage vorher nach PDF/A-3b |
| `--validieren` | Ergebnis sofort mit den KoSIT-Regeln prüfen |
| `-o` | Name der Zieldatei |

## Weg 2: vorhandenes XML in ein PDF einbetten

Haben Sie schon ein CII-XML, etwa aus einem anderen Programm oder aus `erechnung erstellen --format en16931-cii`, bettet `erechnung zugferd` es in das PDF ein:

```bash
erechnung erstellen rechnung.json --format en16931-cii -o rechnung.xml
erechnung zugferd rechnung.xml --pdf rechnung.pdf --pdfa
```

```text
rechnung.xml: en16931-cii, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
ZUGFeRD-PDF geschrieben: rechnung_zugferd.pdf
```

Ohne `-o` heißt das Ergebnis wie die Vorlage mit dem Zusatz `_zugferd.pdf`. Das Profil liest das Werkzeug aus BT-24 im XML:

| XML aus | Profil im PDF | Dateiname im PDF |
| --- | --- | --- |
| `--format en16931-cii` | EN 16931 | `factur-x.xml` |
| `--format xrechnung-cii` | XRECHNUNG | `xrechnung.xml` |
| UBL (`xrechnung-ubl`, `en16931-ubl`) | nicht möglich | ZUGFeRD verlangt CII |

## PDF/A-3: was die Option --pdfa macht

ZUGFeRD baut seit Version 2.0 auf PDF/A-3 (ISO 19005-3:2012) auf ([ferd-net.de](https://www.ferd-net.de/standards/zugferd)). PDF/A ist für die Langzeitarchivierung gedacht: Schriften müssen eingebettet sein, und ein Farbprofil (OutputIntent) legt fest, wie Farben aussehen.

Das Werkzeug schreibt in jedes ZUGFeRD-PDF die XMP-Kennung PDF/A-3b. Ob die Datei die Anforderungen wirklich erfüllt, hängt aber an der Vorlage. Mit `--pdfa` schreibt Ghostscript die Vorlage vorher neu, bettet die Schriften ein und setzt ein sRGB-Farbprofil. Der Unterschied lässt sich mit pypdf sichtbar machen (`schriften.py`):

```python
from pypdf import PdfReader


def eingebettet(schrift):
    fd = schrift.get("/FontDescriptor")
    return fd is not None and any(k in fd for k in ("/FontFile", "/FontFile2", "/FontFile3"))


for name in ["rechnung.pdf", "RE-2026-0001.pdf", "RE-2026-0001_pdfa.pdf"]:
    pdf = PdfReader(name)
    schriften = [
        f"{s['/BaseFont']}={'ja' if eingebettet(s) else 'nein'}"
        for seite in pdf.pages
        for s in (v.get_object() for v in seite["/Resources"]["/Font"].values())
    ]
    print(name, "| OutputIntent:", "/OutputIntents" in pdf.trailer["/Root"], "|", ", ".join(schriften))
```

```text
rechnung.pdf | OutputIntent: False | /Helvetica=nein, /Helvetica-Bold=nein
RE-2026-0001.pdf | OutputIntent: False | /Helvetica=nein, /Helvetica-Bold=nein
RE-2026-0001_pdfa.pdf | OutputIntent: True | /YRLELF+Helvetica-Bold=ja, /ESVAAE+Helvetica=ja
```

`RE-2026-0001.pdf` ist ohne `--pdfa` entstanden und übernimmt die Schwächen der Vorlage. Nehmen Sie `--pdfa`, wenn Ihre Vorlage nicht sicher PDF/A-3 ist. Ghostscript muss dafür installiert sein; fehlt es, meldet das Werkzeug "Ghostscript (gs) nicht gefunden". Eine vollständige PDF/A-3-Prüfung leisten weder das Werkzeug noch der KoSIT-Validator; das Java-Werkzeug Mustang prüft laut eigener Dokumentation auch PDF/A-3 ([mustangproject.org](https://www.mustangproject.org/commandline/)).

## Was passiert, wenn PDF-Inhalt und XML abweichen?

Dann gilt das XML. Laut BMF-Schreiben vom 15.10.2025 (UStAE 14.4 Abs. 3) ist bei Abweichungen zwischen strukturiertem Teil und Bildteil der strukturierte Teil maßgebend; das BMF empfiehlt, den XML-Teil selbst zu visualisieren.

Das Werkzeug liest den Text Ihres PDFs nicht und vergleicht ihn nicht mit dem XML. Wenn im PDF 2.009,91 EUR stehen und in der JSON-Datei ein Tippfehler steckt, enthält die E-Rechnung den Tippfehler. Prüfen Sie deshalb vor dem Versand den strukturierten Teil:

```bash
erechnung lesen rechnung_zugferd.pdf
```

```text
Datei:        rechnung_zugferd.pdf
Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
Nummer:       RE-2026-0001 vom 15.10.2026
...
Netto:        1.689,00 EUR
Brutto:       2.009,91 EUR
Zahlbetrag:   2.009,91 EUR, fällig 14.11.2026
Zahlung:      58 (SEPA-Überweisung) DE79000000001234567890
```

Oder als HTML-Ansicht: `erechnung anzeigen rechnung_zugferd.pdf`. Vergleichen Sie Nummer, Datum, Beträge und Steuersätze mit dem PDF.

## PDF in ZUGFeRD umwandeln: Beispiele

### Beispiel 1: Eigenes PDF zur ZUGFeRD-Rechnung machen (Profil EN 16931)

```bash
erechnung erstellen rechnung.json --format zugferd --pdf rechnung.pdf --pdfa -o RE-2026-0001_pdfa.pdf --validieren
```

```text
RE-2026-0001_pdfa.pdf: zugferd, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 (CII))
```

Das ist der übliche Weg, wenn Sie Ihr Layout behalten und eine E-Rechnung an ein Unternehmen schicken wollen.

### Beispiel 2: PDF mit Profil XRECHNUNG

```bash
erechnung erstellen rechnung.json --format xrechnung-cii -o rechnung_xr_cii.xml
erechnung zugferd rechnung_xr_cii.xml --pdf rechnung.pdf --pdfa -o rechnung_xr.pdf
erechnung lesen rechnung_xr.pdf
```

```text
rechnung_xr_cii.xml: xrechnung-cii, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
ZUGFeRD-PDF geschrieben: rechnung_xr.pdf
Datei:        rechnung_xr.pdf
Format:       ZUGFeRD-Profil XRECHNUNG, XRechnung 3.0 (CII) (eingebettet als xrechnung.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
...
```

Das brauchen Sie, wenn der Empfänger XRechnung-Regeln verlangt, aber zusätzlich ein lesbares PDF möchte. Kürzer geht es mit `erechnung erstellen rechnung.json --format zugferd-xrechnung --pdf rechnung.pdf --pdfa`.

### Beispiel 3: Das eingebettete XML wieder herausholen

```bash
erechnung extrahieren rechnung_zugferd.pdf
```

```text
factur-x.xml aus rechnung_zugferd.pdf gespeichert als rechnung_zugferd.xml
```

Damit kontrollieren Sie, was wirklich im PDF steckt, oder geben das XML an ein anderes Programm weiter.

### Beispiel 4: Ergebnis prüfen und den Prüfbericht aufbewahren

```bash
erechnung validieren RE-2026-0001_pdfa.pdf rechnung_zugferd.pdf --bericht prüfberichte
```

```text
RE-2026-0001_pdfa.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
  Prüfbericht: prüfberichte/RE-2026-0001_pdfa.pdf.593ce775f06b.validierungsbericht.json
rechnung_zugferd.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
  Prüfbericht: prüfberichte/rechnung_zugferd.pdf.a6c093f01a7b.validierungsbericht.json
```

Der Bericht enthält Zeitpunkt, Regelversion und die SHA-256-Summe der Datei. Die Prüfsumme im Dateinamen des Berichts gehört zu der Datei aus diesem Beispiel; bei Ihrer eigenen Datei weicht der Wert ab. Laut BMF-Schreiben vom 15.10.2025, Rn. 35a, bietet es sich zum Nachweis an, den Validierungsbericht aufzubewahren.

### Beispiel 5: Versehentlich ein schon fertiges ZUGFeRD-PDF als Vorlage

```bash
erechnung zugferd rechnung.xml --pdf rechnung_zugferd.pdf -o doppelt.pdf
```

```text
Fehler: Das PDF enthält bereits factur-x.xml. Erst das Original-PDF ohne XML verwenden.
```

Das Werkzeug verhindert zwei Rechnungs-XML in einer Datei. Nehmen Sie das ursprüngliche PDF ohne XML.

### Beispiel 6: UBL-XML lässt sich nicht einbetten

```bash
erechnung erstellen rechnung.json -o rechnung_ubl.xml
erechnung zugferd rechnung_ubl.xml --pdf rechnung.pdf -o ubl.pdf
```

```text
rechnung_ubl.xml: xrechnung-ubl, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
Fehler: Unbekannte Guideline-ID für ZUGFeRD: ''. Erwartet wird CII mit einem ZUGFeRD-Profil.
```

ZUGFeRD verlangt CII. Das Standardformat von `erechnung erstellen` ist XRechnung UBL; für ZUGFeRD wählen Sie `--format en16931-cii` oder `xrechnung-cii`.

### Beispiel 7: Leere Testvorlage selbst anlegen

Zum Ausprobieren reicht eine leere A4-Seite, erzeugt mit pypdf:

```python
from pypdf import PdfWriter

w = PdfWriter()
w.add_blank_page(595, 842)
w.write("leer.pdf")
```

Für echte Rechnungen nehmen Sie das PDF aus Ihrem Rechnungsprogramm, denn der Bildteil soll dieselben Angaben zeigen wie das XML.

## Schritt für Schritt: PDF-Rechnung in ZUGFeRD umwandeln

1. Installieren Sie das Werkzeug (Python 3.10 oder neuer, kein Java nötig) und Ghostscript für die Option `--pdfa`:

   ```bash
   pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
   ```

2. Exportieren Sie die Rechnung aus Ihrem Programm als PDF, zum Beispiel `rechnung.pdf`. Das PDF darf noch kein Rechnungs-XML enthalten.
3. Legen Sie eine Eingabedatei `rechnung.json` mit denselben Angaben an. Vorlage: das Beispiel oben oder [`beispiele/01_standard/eingabe.json`](../../beispiele/01_standard/eingabe.json).
4. Erzeugen Sie die ZUGFeRD-Rechnung:

   ```bash
   erechnung erstellen rechnung.json --format zugferd --pdf rechnung.pdf --pdfa -o RE-2026-0001.pdf --validieren
   ```

5. Achten Sie auf die Zeile "KoSIT-Regeln: GÜLTIG". Steht dort UNGÜLTIG, korrigieren Sie die Eingabedatei anhand der Meldungen und wiederholen Schritt 4. Erklärungen stehen in [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md).
6. Vergleichen Sie den strukturierten Teil mit dem PDF: `erechnung lesen RE-2026-0001.pdf`. Beträge, Nummer und Datum müssen übereinstimmen.
7. Bewahren Sie den Prüfbericht auf: `erechnung validieren RE-2026-0001.pdf --bericht prüfberichte`.
8. Versenden Sie die Datei. Das Werkzeug versendet selbst nichts. Einen bestimmten Übermittlungsweg schreibt das Gesetz laut BMF-FAQ nicht vor; E-Mail ist einer der möglichen Wege.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Erwartung, das Werkzeug lese das PDF aus | keine Option für "PDF rein, E-Rechnung raus" | Daten als JSON oder TOML erfassen, dann einbetten. |
| Vorlage enthält schon ein Rechnungs-XML | "Das PDF enthält bereits factur-x.xml" | Das Original-PDF ohne XML als Vorlage nehmen. |
| UBL statt CII eingebettet | "Unbekannte Guideline-ID für ZUGFeRD" | `--format en16931-cii` oder `xrechnung-cii` verwenden. |
| PDF und JSON passen nicht zusammen | `erechnung lesen` zeigt andere Beträge als das PDF | Das XML ist maßgeblich; Eingabedatei oder PDF korrigieren und neu erzeugen. |
| Vorlage ist kein PDF/A | Schriften nicht eingebettet, kein Farbprofil | Mit `--pdfa` erzeugen; Ghostscript installieren. |
| Profil XRECHNUNG ohne BT-10 | `BR-DE-15` bei `--validieren` | `leitweg_id` in der Eingabedatei setzen. |
| Rechnungsart, die XRechnung nicht kennt | "Rechnungsart 386 ist in XRechnung nicht erlaubt (BR-DE-17)" | Erlaubte Arten: 326, 380, 381, 384, 389, 875, 876, 877; oder Profil EN 16931 (`--format zugferd`). |

## Häufige Fragen

### Kann ich ein PDF kostenlos in ZUGFeRD umwandeln?

Ja, mit dem Open-Source-Werkzeug `erechnung` und Ghostscript, beide kostenlos. Sie müssen die Rechnungsdaten aber einmal strukturiert als JSON oder TOML angeben; aus dem PDF allein entsteht keine E-Rechnung.

### Ist eine PDF-Rechnung eine E-Rechnung?

Nein. Ein PDF ohne eingebettete Datensätze ist eine sonstige Rechnung (UStAE 14.1 Abs. 2 in der Fassung des BMF-Schreibens vom 15.10.2025). Erst mit eingebettetem XML in einem zulässigen Profil wird daraus eine E-Rechnung.

### Muss das PDF für ZUGFeRD ein PDF/A-3 sein?

Ja, ZUGFeRD baut seit Version 2.0 auf PDF/A-3 auf. Ist Ihre Vorlage kein PDF/A-3, wandelt die Option `--pdfa` sie mit Ghostscript nach PDF/A-3b um.

### Wie wandle ich ein PDF in eine XRechnung um?

Für eine XRechnung brauchen Sie kein PDF, sondern nur das XML. Aus derselben Eingabedatei erzeugt `erechnung erstellen` eine XRechnung in UBL:

```bash
erechnung erstellen rechnung.json -o rechnung_xrechnung.xml --validieren
```

```text
rechnung_xrechnung.xml: xrechnung-ubl, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 XRechnung (UBL Invoice))
```

Mit `--format xrechnung-cii` bekommen Sie dieselbe Rechnung in CII. Mehr dazu in [XRechnung](./xrechnung.md).

### Was gilt, wenn im PDF etwas anderes steht als im XML?

Das XML. Laut BMF-Schreiben vom 15.10.2025 (UStAE 14.4 Abs. 3) ist bei Abweichungen der strukturierte Teil maßgebend. Kontrollieren Sie deshalb vor dem Versand mit `erechnung lesen` oder `erechnung anzeigen`, was im XML steht.

### Kann ich eine eingescannte Papierrechnung in ZUGFeRD umwandeln?

Nicht automatisch. Das Werkzeug erkennt keinen Text auf Bildern. Sie können die Angaben abtippen und als JSON erfassen; ob eine nachträglich erstellte E-Rechnung für Ihren Fall die richtige Lösung ist, klären Sie mit der Steuerberatung.

### Welches Profil entsteht bei der Umwandlung?

Mit `--format zugferd` entsteht das Profil EN 16931, mit `--format zugferd-xrechnung` das Profil XRECHNUNG. Beide sind E-Rechnungen nach UStAE 14.1 Abs. 14. Eine Übersicht aller Profile steht in [ZUGFeRD](./zugferd.md).

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [ZUGFeRD: Format, Profile und Versionen](./zugferd.md)
- [E-Rechnung erstellen: XRechnung und ZUGFeRD kostenlos erzeugen](./e-rechnung-erstellen.md)
- [E-Rechnung prüfen: Validator mit den offiziellen Regeln](./e-rechnung-validator.md)
- [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md)
- [Was ist eine E-Rechnung?](./was-ist-eine-e-rechnung.md)
- Beispiele: [`beispiele/01_standard/zugferd_en16931.pdf`](../../beispiele/01_standard/zugferd_en16931.pdf), [`beispiele/README.md`](../../beispiele/README.md)
