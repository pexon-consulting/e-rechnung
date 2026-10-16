# E-Rechnung empfangen und lesen: XRechnung öffnen und anzeigen

Eine E-Rechnung empfangen heißt: Sie nehmen eine strukturierte Rechnungsdatei (XRechnung als XML oder ZUGFeRD als PDF mit eingebettetem XML) entgegen, zum Beispiel per E-Mail, und machen sie mit einem Viewer lesbar. Eine XRechnung ist reines XML, deshalb zeigt ein Doppelklick nur Code; lesbar wird sie erst durch eine Visualisierung wie die offizielle KoSIT-Ansicht oder `erechnung anzeigen rechnung.xml`. Seit dem 01.01.2025 müssen alle inländischen Unternehmer E-Rechnungen empfangen können, ein normales E-Mail-Postfach genügt dafür.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil von [E-Rechnung in Python](../../README.md).

## Das Wichtigste in Kürze

- Seit dem 01.01.2025 müssen alle inländischen Unternehmer E-Rechnungen empfangen können, ohne Ausnahme, auch Kleinunternehmer nach § 19 UStG.
- Für den Empfang reicht laut BMF-Schreiben vom 15.10.2025 (UStAE 14.1) ein E-Mail-Postfach, ein gesondertes Postfach ist nicht nötig.
- Eine XRechnung ist eine XML-Datei; ein Viewer macht daraus eine lesbare Rechnung, rechtlich maßgeblich bleibt das XML.
- Bei ZUGFeRD steckt das XML im PDF; weichen PDF-Bild und XML voneinander ab, gilt laut BMF-FAQ der strukturierte Teil.
- `erechnung anzeigen`, `erechnung lesen` und `erechnung validieren` öffnen, lesen und prüfen Eingangsrechnungen lokal, ohne Java und ohne Upload.
- Bei einer ungültigen E-Rechnung bitten Sie den Lieferanten um eine korrigierte Rechnung; die umsatzsteuerlichen Folgen klären Sie mit der Steuerberatung.

## Was bedeutet "E-Rechnung empfangen"?

Eine E-Rechnung ist laut § 14 Abs. 1 Satz 3 UStG eine Rechnung, die in einem strukturierten elektronischen Format ausgestellt, übermittelt und empfangen wird und eine elektronische Verarbeitung ermöglicht. Empfangen heißt also nicht, eine besondere Software zu kaufen. Es heißt, die Datei anzunehmen, aufzubewahren und lesen zu können.

Die Empfangspflicht gilt seit dem 01.01.2025 für alle inländischen Unternehmer. Laut BMF-FAQ und BMF-Schreiben vom 15.10.2025 (UStAE 14.1) gibt es keine Ausnahme, auch nicht für Kleinunternehmer, Land- und Forstwirte oder Unternehmer mit ausschließlich steuerfreien Umsätzen wie Wohnungsvermieter.

| Frage | Antwort laut BMF | Quelle |
| --- | --- | --- |
| Brauche ich ein eigenes E-Rechnungs-Postfach? | Nein, Empfang per E-Mail genügt. | BMF-Schreiben vom 15.10.2025 (UStAE 14.1) |
| Ist ein Übermittlungsweg vorgeschrieben? | Nein, zum Beispiel E-Mail, Schnittstelle, Portal-Download oder USB-Stick. | BMF-FAQ |
| Müssen Kleinunternehmer empfangen können? | Ja, auch bei der Sonderregelung nach § 19 UStG. | BMF-Schreiben vom 15.10.2025 (UStAE 14.1) |
| Ab wann? | Seit dem 01.01.2025. | BMF-FAQ |

E-Rechnung empfangen kostenlos geht also mit dem vorhandenen Postfach. Was Sie zusätzlich brauchen, ist ein Weg, die Datei lesbar zu machen und zu prüfen. Dafür reicht ein kostenloser Viewer.

Bis Ende 2027 dürfen Ihre Lieferanten unter bestimmten Bedingungen noch Papier- oder PDF-Rechnungen schicken (§ 27 Abs. 38 UStG). Sie bekommen deshalb vorerst eine Mischung aus E-Rechnungen und sonstigen Rechnungen. Details stehen in [E-Rechnung Pflicht](./e-rechnung-pflicht.md).

## Was kann ich mit einer XRechnung anfangen?

Eine XRechnung ist das deutsche E-Rechnungsformat für EN 16931, als XML in der Syntax UBL oder CII. Mit der Datei können Sie vier Dinge tun:

| Aufgabe | Wozu | Befehl |
| --- | --- | --- |
| Anzeigen | Rechnung wie gewohnt lesen, Positionen und Beträge kontrollieren | `erechnung anzeigen rechnung.xml` |
| Lesen | Kerndaten als Text oder JSON für Tabellen und Skripte | `erechnung lesen rechnung.xml --json` |
| Prüfen | Feststellen, ob die Datei den offiziellen KoSIT-Regeln entspricht | `erechnung validieren rechnung.xml` |
| Weiterverarbeiten | Als DATEV-Buchungsstapel an die Buchhaltung geben | `erechnung datev rechnung.xml` |

Die XML-Datei selbst bewahren Sie unverändert auf. Wie, steht in [E-Rechnung archivieren](./e-rechnung-archivieren.md).

## Warum zeigt ein Doppelklick auf die XRechnung nur Code?

Eine XRechnung enthält kein Layout. Sie besteht nur aus Datenfeldern mit festen Namen, den Business Terms der EN 16931 (zum Beispiel BT-1 Rechnungsnummer, BT-10 Käuferreferenz). Ein Browser oder Texteditor zeigt deshalb die Rohdaten. So beginnt die Beispielrechnung [`01_standard/xrechnung_ubl.xml`](../../beispiele/01_standard/xrechnung_ubl.xml):

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

Alles Nötige ist da: Rechnungsnummer (`cbc:ID`), Datum, Fälligkeit, Rechnungsart 380 und Käuferreferenz. Damit ein Mensch es bequem lesen kann, braucht es eine Visualisierung. Das BMF empfiehlt laut BMF-FAQ, den XML-Teil selbst zu visualisieren, statt sich auf ein mitgeliefertes Bild zu verlassen.

## XRechnung Viewer: welche Möglichkeiten gibt es?

Ein E-Rechnung-Viewer wandelt das XML in eine lesbare Ansicht um. Die Ansicht ist keine Rechnung im rechtlichen Sinn. Laut KoSIT sind Visualisierungen keine gültigen XRechnungen und nicht zur Archivierung gedacht; das Original bleibt das XML.

| Viewer | Was er ist | Läuft offline | Formate |
| --- | --- | --- | --- |
| [KoSIT xrechnung-visualization](https://github.com/itplr-kosit/xrechnung-visualization) | Offizielle XSLT-Stylesheets der KoSIT (Apache-2.0), aktuell v2026-10-13, erzeugen HTML oder PDF | ja | XRechnung UBL und CII |
| [Quba-Viewer](https://github.com/ZUGFeRD/quba-viewer) | Desktop-App (Apache-2.0) für Windows, macOS und Linux, aktuell v1.5.1, basiert auf den KoSIT-XSLTs | ja, Prüfung optional über Mustangserver | XRechnung, ZUGFeRD/Factur-X, Order-X |
| `erechnung anzeigen` | Eigene schlichte HTML-Ansicht aus diesem Paket | ja | XRechnung UBL und CII, ZUGFeRD-PDF |
| `erechnung anzeigen --offiziell` | Ruft die KoSIT-Visualisierung v2026-10-13 aus Python auf (mit saxonche, ohne Java) | ja, nach einmaligem Download | XRechnung UBL und CII, ZUGFeRD-PDF (das eingebettete CII) |

Die KoSIT-Stylesheets sind XSLT 2.0. Ohne Saxon lassen sie sich in Python nicht ausführen, deshalb nutzt das Paket saxonche.

**Sicherheitshinweis:** Die KoSIT-Visualisierung v2026-10-13 behebt eine JavaScript-Injection über die Dateinamen in BT-122 und BT-125 (Anhänge). Ältere Versionen sollten Sie meiden, gerade bei Rechnungen von unbekannten Absendern. `erechnung` lädt genau die Version 2026-10-13 und prüft ihre SHA-256-Summe. Bei anderen Programmen, die die KoSIT-Stylesheets mitbringen, lohnt ein Blick, welche Version enthalten ist.

## E-Rechnung anzeigen mit `erechnung anzeigen`

`erechnung anzeigen DATEI` schreibt eine HTML-Datei neben die Rechnung. Sie öffnen sie mit jedem Browser.

```bash
erechnung anzeigen rechnung.xml
```

```text
Ansicht geschrieben: rechnung.html
```

Die eigene Ansicht zeigt oben, ob es eine E-Rechnung nach EN 16931 ist, und darunter Parteien, Positionen, Summen, Steuer und Zahlung. Auszug aus dem Textinhalt der erzeugten HTML-Datei:

```text
380 (Rechnung)
RE-2026-0001
E-Rechnung nach EN 16931
XRechnung 3.0 (UBL)
Verkäufer
Nordlicht Software GmbH
...
Positionen
Pos.  Bezeichnung                               Menge  Einheit  Preis   USt     Netto
1     Beratung Einführung E-Rechnung            12     Stunde   120,00  S 19 %  1.440,00
2     Softwarelizenz Rechnungseingang (Monat)   1      Monat    249,00  S 19 %  249,00
Umsatzsteuer      320,91 EUR
Zahlbetrag      2.009,91 EUR
...
Zahlungsbedingungen
2,00 % Skonto bei Zahlung innerhalb von 10 Tagen
Zahlbar innerhalb von 30 Tagen ohne Abzug.
Ansicht erzeugt mit e-rechnung (Python). Rechtlich maßgeblich ist der XML-Inhalt der E-Rechnung.
```

Die Positionstabelle ist hier für die Lesbarkeit in Spalten gesetzt. Die Skonto-Angabe `#SKONTO#TAGE=10#PROZENT=2.00#` aus dem XML übersetzt die Ansicht in einen Satz.

Mit `--offiziell` nutzt der Befehl die KoSIT-Visualisierung. Beim ersten Aufruf lädt das Paket sie von GitHub und legt sie im Cache ab; danach läuft es offline.

```bash
erechnung anzeigen rechnung.xml --offiziell -o rechnung_kosit.html
```

```text
Ansicht geschrieben: rechnung_kosit.html
```

Die KoSIT-Ansicht hat Reiter (Übersicht, Details, Zusätze, Anlagen, Laufzettel) und zeigt alle Felder, auch leere. Auszug aus dem Textinhalt:

```text
XRechnung
...
Inhalte auf dieser Seite sind ohne JavaScript nur eingeschränkt darstellbar.
Wir übernehmen keine Haftung für die Richtigkeit der Daten.
Informationen zum Käufer
Käuferreferenz:
BH-2026-0815
...
Rechnungsnummer:
RE-2026-0001
Rechnungsart:
380
...
Skonto; weitere Zahlungsbedingungen:
#SKONTO#TAGE=10#PROZENT=2.00#
Code für das Zahlungsmittel:
58
```

Die KoSIT-Ansicht zeigt Codes wie `380` und `58` roh, die eigene Ansicht übersetzt sie ("380 (Rechnung)", "58 (SEPA-Überweisung)"). Für die Freigabe im Alltag reicht meist die eigene Ansicht. Wer jedes Feld in der Darstellung der KoSIT sehen will, nimmt `--offiziell`.

Für Rechner ohne Internet laden Sie die Visualisierung vorher einmal mit `erechnung konfiguration --visualisierung`. Der Befehl zeigt danach den Cache-Ordner, zum Beispiel `~/.cache/erechnung/xrechnung-3.0.2-visualization-2026-10-13`.

## E-Rechnung lesen auf der Kommandozeile

`erechnung lesen` erkennt das Format und fasst die Rechnung als Text zusammen. Das ist der schnellste Blick in eine Eingangsrechnung.

```bash
erechnung lesen rechnung.xml
```

```text
Datei:        rechnung.xml
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

Mit `--json` gibt der Befehl das vollständige Modell aus. Das eignet sich für Tabellen, eigene Skripte oder eine Übergabe an andere Programme. Beträge stehen als Text mit Punkt, zum Beispiel `"2009.91"`.

```bash
erechnung lesen rechnung.xml --json
```

```json
{
  "nummer": "RE-2026-0001",
  "datum": "2026-10-15",
  "verkaeufer": {
    "name": "Nordlicht Software GmbH",
    "ust_id": "DE123456789"
  },
  "summen": {
    "netto": "1689.00",
    "steuer": "320.91",
    "zahlbetrag": "2009.91"
  },
  "_format": {
    "bezeichnung": "XRechnung 3.0 (UBL)",
    "ist_e_rechnung": true
  }
}
```

Der Auszug ist gekürzt; die echte Ausgabe enthält zusätzlich Adressen, Positionen, Steuern und Zahlungsdaten.

## ZUGFeRD-PDF: das XML herausholen

Eine ZUGFeRD-Rechnung ist ein PDF/A-3 mit eingebettetem XML. Das PDF öffnen Sie wie jedes PDF. Für Prüfung und Buchung zählt aber das XML, denn laut BMF-FAQ ist bei Abweichungen der strukturierte Teil maßgebend. `erechnung lesen`, `anzeigen` und `validieren` arbeiten direkt mit dem PDF. Wenn Sie das XML als eigene Datei brauchen, holen Sie es mit `erechnung extrahieren`:

```bash
erechnung extrahieren kleinunternehmer.pdf
```

```text
factur-x.xml aus kleinunternehmer.pdf gespeichert als kleinunternehmer.xml
```

Die herausgeholte Datei ist CII. Darin steht in BT-24 (`ram:GuidelineSpecifiedDocumentContextParameter/ram:ID`) die Kennung `urn:cen.eu:en16931:2017`, also das ZUGFeRD-Profil EN 16931 (COMFORT). Aufbewahrt wird trotzdem das ganze PDF, so wie es angekommen ist.

Enthält ein PDF kein XML, ist es keine E-Rechnung:

```bash
erechnung lesen nur_pdf.pdf
```

```text
nur_pdf.pdf: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
```

## Viele Eingangsrechnungen auf einmal lesen, prüfen und anzeigen

`erechnung lesen` und `erechnung validieren` nehmen mehrere Dateien auf einmal, zum Beispiel `erechnung validieren eingang/*`. Der Exit-Code ist dann 1, sobald eine Datei ungültig ist. Eine kurze Eingangsliste für einen Ordner `eingang/` mit drei gültigen Rechnungen und einer fehlerhaften:

```bash
erechnung lesen eingang/* | grep -E "^(Datei|Zahlbetrag)"
```

```text
Datei:        eingang/2026-017.pdf
Zahlbetrag:   850,00 EUR, fällig 14.11.2026
Datei:        eingang/RE-2026-0001.xml
Zahlbetrag:   2.009,91 EUR, fällig 14.11.2026
...
```

`erechnung anzeigen` nimmt nur eine Datei. Für den ganzen Ordner hilft eine Schleife, die prüft, einen Prüfbericht ablegt und eine Ansicht schreibt (Bash, zsh, macOS, Linux, Git Bash):

```bash
mkdir -p ansicht berichte
for f in eingang/*; do
  if erechnung validieren "$f" --bericht berichte > /dev/null; then
    echo "gültig    $f"
  else
    echo "Exit $?    $f"
  fi
  erechnung anzeigen "$f" -o "ansicht/$(basename "$f").html" > /dev/null
done
```

```text
gültig    eingang/2026-017.pdf
gültig    eingang/RE-2026-0001.xml
gültig    eingang/RE-2026-0002.xml
Exit 1    eingang/fehlerhaft.xml
```

Die Ansichten landen in `ansicht/`, damit der Eingangsordner nur die Originale enthält. Exit-Code 1 heißt ungültig, 2 heißt, die Prüfung war nicht möglich.

Dieselbe Schleife in PowerShell unter Windows:

```powershell
New-Item -ItemType Directory -Force ansicht, berichte | Out-Null
foreach ($f in Get-ChildItem eingang -File) {
    erechnung validieren $f.FullName --bericht berichte | Out-Null
    if ($LASTEXITCODE -eq 0) { "gültig    $($f.Name)" } else { "Exit $LASTEXITCODE    $($f.Name)" }
    erechnung anzeigen $f.FullName -o "ansicht\$($f.Name).html" | Out-Null
}
```

## Eingang prüfen: ist die E-Rechnung gültig?

`erechnung validieren` prüft mit den offiziellen KoSIT-Regeln (XML-Schema und Schematron für EN 16931 und XRechnung) und zusätzlich mit einer eigenen Vorprüfung. Die Rechnungsdaten verlassen dabei den Rechner nicht.

```bash
erechnung validieren eingang/fehlerhaft.xml
```

```text
eingang/fehlerhaft.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-DE-15: [BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BR-DE-15: Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.
```

Laut BMF-Schreiben vom 15.10.2025 (Rn. 35a) ersetzt eine Validierung die Prüfpflicht des Empfängers nicht. Sie dürfen sich aber bei der Sorgfalt eines ordentlichen Kaufmanns auf das Ergebnis einer geeigneten Validierungsanwendung verlassen. Das BMF empfiehlt, den Validierungsbericht aufzubewahren; dafür gibt es `--bericht`. Mehr zur Prüfung steht in [E-Rechnung prüfen](./e-rechnung-validator.md).

## Was tun bei einer ungültigen E-Rechnung?

Nicht jeder Fehler wiegt gleich. Das BMF-Schreiben vom 15.10.2025 unterscheidet drei Arten:

| Art | Was es ist | Folge laut BMF-Schreiben vom 15.10.2025 |
| --- | --- | --- |
| Formatfehler (Rn. 6a) | Die Datei entspricht nicht der Syntax oder deren technischen Vorgaben | Keine E-Rechnung, sondern eine sonstige Rechnung |
| Geschäftsregelfehler (Rn. 6b) | Verstoß gegen Regeln des Formats, zum Beispiel fehlendes BT-10 in einer XRechnung | Betrifft er keine Pflichtangabe, ist er laut Rn. 35a umsatzsteuerlich unbeachtlich |
| Inhaltsfehler (Rn. 35a) | Pflichtangaben nach §§ 14 Abs. 4, 14a UStG fehlen oder sind falsch | Keine ordnungsmäßige Rechnung |

So gehen Sie vor:

1. Prüfbericht ablegen: `erechnung validieren rechnung.xml --bericht berichte`.
2. Den Lieferanten um eine korrigierte E-Rechnung bitten und den Fehlercode nennen, zum Beispiel "BR-DE-15: Käuferreferenz (BT-10) fehlt".
3. Die Originaldatei und den Bericht aufbewahren, auch wenn eine korrigierte Fassung kommt.
4. Bei Inhaltsfehlern oder Unsicherheit die Folgen für den Vorsteuerabzug mit der Steuerberatung klären.

Für die Fehlercodes selbst gibt es [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md).

## Beispiele

### Beispiel 1: XRechnung im Browser lesbar machen

```bash
erechnung anzeigen rechnung.xml
```

```text
Ansicht geschrieben: rechnung.html
```

Brauchen Sie, wenn eine XRechnung per E-Mail kommt und jemand sie freigeben soll.

### Beispiel 2: Offizielle KoSIT-Ansicht einer ZUGFeRD-Rechnung

```bash
erechnung anzeigen kleinunternehmer.pdf --offiziell -o kleinunternehmer_kosit.html
```

```text
Ansicht geschrieben: kleinunternehmer_kosit.html
```

Brauchen Sie, wenn Sie prüfen wollen, ob das XML im PDF dasselbe zeigt wie das PDF-Bild.

### Beispiel 3: ZUGFeRD-Rechnung lesen, ohne das XML herauszuholen

```bash
erechnung lesen kleinunternehmer.pdf
```

```text
Datei:        kleinunternehmer.pdf
Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
...
Zahlbetrag:   850,00 EUR, fällig 14.11.2026
```

Brauchen Sie, um bei einem PDF schnell zu sehen, ob es eine E-Rechnung ist und welches Profil es hat.

### Beispiel 4: Zahlbetrag und IBAN als JSON für ein Skript

```bash
erechnung lesen rechnung.xml --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['nummer'], d['summen']['zahlbetrag'], d['zahlung']['iban'])"
```

```text
RE-2026-0001 2009.91 DE79000000001234567890
```

Brauchen Sie, wenn Sie Zahlungsvorschläge oder eine Eingangsliste aus vielen Rechnungen bauen.

### Beispiel 5: XML aus einem ZUGFeRD-PDF direkt ausgeben

```bash
erechnung extrahieren zugferd_en16931.pdf -o - | head -3
```

```text
<?xml version='1.0' encoding='UTF-8'?>
<rsm:CrossIndustryInvoice xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100" ...>
  <rsm:ExchangedDocumentContext>
```

Brauchen Sie, wenn ein anderes Programm nur das XML annimmt.

## Schritt für Schritt: eine E-Rechnung empfangen und lesen

1. Legen Sie fest, wohin E-Rechnungen kommen, zum Beispiel ein E-Mail-Postfach wie `rechnungseingang@example.com`, und teilen Sie es Ihren Lieferanten mit.
2. Speichern Sie jeden Anhang (`.xml` oder `.pdf`) unverändert in einen Eingangsordner. Den Inhalt der Datei bearbeiten Sie nie.
3. Installieren Sie das Werkzeug einmal: `pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"`.
4. Prüfen Sie die Datei: `erechnung validieren rechnung.xml --bericht berichte`. "GÜLTIG" heißt: die offiziellen KoSIT-Regeln sind erfüllt.
5. Machen Sie sie lesbar: `erechnung anzeigen rechnung.xml` und öffnen Sie die HTML-Datei im Browser.
6. Kontrollieren Sie fachlich: Ist die Leistung erbracht, stimmen Menge, Preis und Bankverbindung? Das kann keine Software für Sie entscheiden.
7. Bei "UNGÜLTIG": Lieferanten mit dem Fehlercode um Korrektur bitten, Original und Bericht aufbewahren.
8. Geben Sie die Rechnung zur Buchung weiter, zum Beispiel als DATEV-Buchungsstapel mit `erechnung datev`.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| XML per Doppelklick geöffnet | Browser oder Editor zeigt nur Tags | `erechnung anzeigen rechnung.xml` oder einen anderen Viewer nutzen |
| Nur das PDF-Bild einer ZUGFeRD-Rechnung geprüft | Abweichungen zum XML fallen nicht auf | `erechnung anzeigen rechnung.pdf --offiziell` zeigt das XML; das XML ist maßgebend |
| Ansicht statt Original abgelegt | Archiv enthält nur HTML oder Ausdruck | Immer die empfangene Datei unverändert aufbewahren |
| Reines PDF für eine E-Rechnung gehalten | `lesen` meldet "kein eingebettetes Rechnungs-XML" | Es ist eine sonstige Rechnung; bei Bedarf beim Lieferanten eine E-Rechnung anfordern |
| `--offiziell` auf einem Rechner ohne Internet | Erster Aufruf kann die Visualisierung nicht laden | Vorher `erechnung konfiguration --visualisierung` mit Internet ausführen |
| Ansichten im Eingangsordner erzeugt | Originale und HTML-Dateien gemischt | In der Schleife `-o ansicht/...` verwenden |

## Häufige Fragen

### Brauche ich eine Software, um E-Rechnungen zu empfangen?

Nein, für den Empfang reicht laut BMF-Schreiben vom 15.10.2025 (UStAE 14.1) ein E-Mail-Postfach. Zum Lesen brauchen Sie einen Viewer; kostenlose Viewer sind die KoSIT-Visualisierung, der Quba-Viewer oder `erechnung anzeigen`.

### Wie öffne ich eine XRechnung?

Mit einem XRechnung-Viewer, nicht per Doppelklick. Auf der Kommandozeile reicht `erechnung anzeigen rechnung.xml`; danach öffnen Sie die erzeugte HTML-Datei im Browser.

### Muss ich als Kleinunternehmer E-Rechnungen empfangen können?

Ja, seit dem 01.01.2025 gilt die Empfangspflicht ohne Ausnahme, auch bei der Sonderregelung nach § 19 UStG. Mehr dazu in [E-Rechnung für Kleinunternehmer](./e-rechnung-kleinunternehmer.md).

### Was ist bei einer ZUGFeRD-Rechnung maßgeblich, das PDF oder das XML?

Das XML. Laut BMF-FAQ ist bei Abweichungen zwischen Bildteil und XML der strukturierte Teil maßgebend; das BMF empfiehlt, den XML-Teil selbst zu visualisieren.

### Werden meine Rechnungen bei `erechnung` irgendwohin hochgeladen?

Nein, Lesen, Prüfen und Anzeigen laufen lokal. Das Paket lädt nur einmal die öffentlichen KoSIT-Regeln und die KoSIT-Visualisierung von GitHub und prüft deren SHA-256-Summe.

### Darf ich eine ungültige E-Rechnung einfach zurückweisen?

Ob Sie zahlen oder zurückweisen, ist eine kaufmännische Entscheidung; die Prüfung liefert nur den Befund. Üblich ist, den Lieferanten mit dem Fehlercode um eine korrigierte Rechnung zu bitten. Ob der Fehler umsatzsteuerlich zählt, hängt laut BMF-Schreiben vom 15.10.2025 (Rn. 35a) davon ab, ob eine Pflichtangabe betroffen ist; im Zweifel mit der Steuerberatung klären.

### Kann `erechnung` E-Rechnungen über Peppol empfangen?

Nein, das Werkzeug ist kein Peppol-Zugangspunkt und holt keine E-Mails ab. Es verarbeitet Dateien, die schon auf Ihrem Rechner liegen.

> **Hinweis:** Diese Anleitung erklärt Gesetz, BMF-Schreiben und technische Standards nach dem Stand vom 15.10.2026. Sie ist keine Steuer- oder Rechtsberatung, die Autoren sind keine Steuerberater. Für die Beurteilung eines konkreten Falls wenden Sie sich an Ihre Steuerberatung oder Ihr Finanzamt. Alle Angaben ohne Gewähr.

## Weiterlesen

- [Was ist eine E-Rechnung?](./was-ist-eine-e-rechnung.md)
- [E-Rechnung prüfen: XRechnung- und ZUGFeRD-Validator](./e-rechnung-validator.md)
- [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md)
- [E-Rechnung archivieren](./e-rechnung-archivieren.md)
- [DATEV und E-Rechnung](./datev-e-rechnung.md)
- Beispiele: [Standardrechnung UBL](../../beispiele/01_standard/xrechnung_ubl.xml), [ZUGFeRD-PDF](../../beispiele/01_standard/zugferd_en16931.pdf), [KoSIT-Ansicht](../../beispiele/08_b2g_leitweg_id/ansicht_kosit.html), [Übersicht](../../beispiele/README.md)
