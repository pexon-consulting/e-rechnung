# E-Rechnung archivieren: Aufbewahrung, GoBD und Prüfbericht

E-Rechnungen archivieren heißt: Sie bewahren jede ein- und ausgehende E-Rechnung acht Jahre lang auf (§ 14b Abs. 1 UStG, BMF-Schreiben vom 15.10.2025, Rn. 60), und zwar im empfangenen Format mit unversehrtem strukturiertem Teil. Bei einer XRechnung ist das die XML-Datei, bei ZUGFeRD das PDF mit dem eingebetteten XML; eine Ansicht oder ein Ausdruck ersetzt das Original nicht. Den Prüfbericht der Validierung sollten Sie laut BMF-Schreiben vom 15.10.2025 (Rn. 35a) ebenfalls aufbewahren.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Geschäftsführung, Buchhaltung und Steuerkanzleien. Technische Beispiele stehen weiter unten und sind optional.

## Das Wichtigste in Kürze

- Die Aufbewahrungsfrist für Rechnungen beträgt acht Jahre (§ 14b Abs. 1 UStG, § 147 Abs. 3 AO), sie beginnt mit dem Ende des Jahres, in dem die Rechnung ausgestellt wurde. Sie endet nicht, solange die Rechnung für eine noch offene Steuerfestsetzung von Bedeutung ist (§ 147 Abs. 3 Satz 5 AO).
- Aufbewahrt wird im empfangenen Format, der strukturierte Teil muss unversehrt und maschinell auswertbar bleiben (UStAE 14b.1, BMF-Schreiben vom 15.10.2025).
- Bei ZUGFeRD bewahren Sie das ganze PDF auf, bei XRechnung die XML-Datei; eine Visualisierung ist laut KoSIT nicht zur Archivierung gedacht.
- `erechnung validieren --bericht ORDNER` legt je Datei einen JSON-Prüfbericht mit Zeitpunkt, Regelversion und SHA-256 der Datei ab.
- Eine SHA-256-Summe zeigt später, ob eine Datei seit der Prüfung verändert wurde; sie ersetzt kein revisionssicheres Archiv.
- Wie Ihr Archiv konkret aussehen muss, beschreiben Sie in Ihrer Verfahrensdokumentation und klären Sie mit der Steuerberatung.

## Wie lange muss ich E-Rechnungen aufbewahren?

Die Aufbewahrungsfrist für E-Rechnungen beträgt acht Jahre. Das gilt für die Doppel ausgehender Rechnungen und für alle eingehenden Rechnungen (§ 14b Abs. 1 UStG). Das BMF-Schreiben vom 15.10.2025 bestätigt die acht Jahre in Rn. 60. Früher waren es zehn Jahre; geändert hat das das Bürokratieentlastungsgesetz IV.

| Unterlage | Frist | Rechtsgrundlage |
| --- | --- | --- |
| Rechnungen (ein- und ausgehend) | acht Jahre | § 14b Abs. 1 UStG |
| Buchungsbelege | acht Jahre (vorher zehn) | § 147 Abs. 3 AO |
| Bücher und Jahresabschlüsse | zehn Jahre | § 147 Abs. 3 AO |
| Sonstige Unterlagen | sechs Jahre | § 147 Abs. 3 AO |

Die Frist beginnt mit dem Ende des Jahres, in dem die Rechnung ausgestellt wurde. Eine Rechnung vom 15.10.2026 bewahren Sie also mindestens bis zum 31.12.2034 auf. Die Frist endet nicht, solange die Rechnung für eine noch offene Steuerfestsetzung von Bedeutung ist (§ 147 Abs. 3 Satz 5 AO). Ob diese Regel für Ihr Unternehmen gilt, klärt Ihre Steuerberatung.

Die acht Jahre gelten laut § 27 Abs. 40 UStG für alle Rechnungen, deren Frist am 31.12.2024 noch nicht abgelaufen war. Für einige Branchen, etwa Kreditinstitute, gibt es Sonderregeln; klären Sie solche Fälle mit der Steuerberatung.

Hinweis: Die FAQ auf [e-rechnung-bund.de](https://www.e-rechnung-bund.de/faq/) nennt noch zehn Jahre nach § 14b UStG. Das ist durch das Bürokratieentlastungsgesetz IV überholt; maßgeblich ist der aktuelle [§ 14b UStG](https://www.gesetze-im-internet.de/ustg_1980/__14b.html).

## In welcher Form muss ich E-Rechnungen aufbewahren?

Eine E-Rechnung bewahren Sie in dem Format auf, in dem Sie sie empfangen haben. Laut BMF-Schreiben vom 15.10.2025 (Rn. 60 und UStAE 14b.1) muss zumindest der strukturierte Teil unversehrt im Ursprungsformat erhalten bleiben, und die Finanzverwaltung muss ihn maschinell auswerten können.

| Sie haben empfangen | Das ist das Original | Das ist nur eine Hilfe |
| --- | --- | --- |
| XRechnung (UBL oder CII) | die `.xml`-Datei, unverändert | HTML-Ansicht, Ausdruck, PDF aus einem Viewer |
| ZUGFeRD/Factur-X | das ganze `.pdf` mit eingebettetem XML | das herausgeholte XML, ein Ausdruck |
| Prüfung der Datei | der Prüfbericht (`*.validierungsbericht.json`) | die Bildschirmausgabe |

Die KoSIT schreibt zu ihrer eigenen Visualisierung: Visualisierungen sind keine gültigen XRechnungen und nicht zur Archivierung gedacht; nur das XML ist das Original. Das gilt genauso für die Ansicht von `erechnung anzeigen`. Sie dürfen eine Ansicht zusätzlich ablegen, sie ersetzt das Original aber nicht.

Unversehrt heißt nach § 14 Abs. 3 UStG: Die Rechnungsangaben werden nicht verändert. Am einfachsten weisen Sie das nach, wenn Sie die Originaldatei unverändert ablegen, nicht neu speichern, nicht umformatieren und nicht umwandeln. Eine Prüfsumme (SHA-256) zeigt dann, dass sich kein Byte geändert hat.

## ZUGFeRD archivieren: warum das ganze PDF?

Eine ZUGFeRD-Rechnung ist eine einzige Datei: ein PDF/A-3 mit eingebettetem XML. Das empfangene Format ist also das PDF. Wenn Sie das PDF unverändert aufbewahren, bleibt der strukturierte Teil darin automatisch erhalten.

Das XML herauszuholen ist für die Verarbeitung nützlich, zum Beispiel für ein Programm, das nur XML annimmt:

```bash
erechnung extrahieren archiv/2026/eingang/2026-017.pdf -o arbeit/2026-017.xml
```

```text
factur-x.xml aus archiv/2026/eingang/2026-017.pdf gespeichert als arbeit/2026-017.xml
```

Ohne `-o` legt der Befehl die XML-Datei neben das PDF; im Archivordner ist ein eigener Zielordner übersichtlicher. Die herausgeholte Datei ist eine Kopie. Bewahren Sie trotzdem das PDF auf, so wie es angekommen ist. Auch der Prüfbericht bezieht sich auf das ganze PDF: Die SHA-256-Summe im Bericht ist die Summe der PDF-Datei, nicht die des eingebetteten XML.

## E-Rechnung und GoBD: was gilt?

Die GoBD sind die Grundsätze der Finanzverwaltung zur ordnungsmäßigen Führung und Aufbewahrung von Büchern und Unterlagen in elektronischer Form. Maßgeblich ist das BMF-Schreiben vom 28.11.2019, zuletzt geändert durch das BMF-Schreiben vom 14.07.2025 (BStBl I S. 1502). Darauf verweist das BMF-Schreiben vom 15.10.2025 in Rn. 61.

Für die Umsatzsteuer stellt das BMF-Schreiben vom 15.10.2025 in Rn. 60 klar: Wird eine E-Rechnung außerhalb eines GoBD-konformen Systems gespeichert, ist das allein umsatzsteuerlich kein Verstoß gegen § 14b UStG. Das heißt nicht, dass die GoBD für Sie keine Rolle spielen. Sie gelten für Ihre Buchführung weiter.

Was das praktisch heißt, hängt von Ihrem Betrieb ab:

- Beschreiben Sie in Ihrer Verfahrensdokumentation, wie E-Rechnungen eingehen, geprüft, abgelegt und gefunden werden.
- Legen Sie fest, wer Dateien im Archiv ändern oder löschen darf.
- Klären Sie mit der Steuerberatung, ob Ihre Ablage den Anforderungen genügt oder ob Sie ein Archivsystem brauchen.

## Prüfbericht aufbewahren mit `erechnung validieren --bericht`

Laut BMF-Schreiben vom 15.10.2025 (Rn. 35a) darf sich ein Unternehmen bei Beachtung der Sorgfalt eines ordentlichen Kaufmanns auf das technische Ergebnis einer Validierung hinsichtlich Format und Geschäftsregeln verlassen. Inhaltliche Fehler wie ein falscher Steuersatz erkennt eine Validierung nicht immer; die eigene Prüfpflicht bleibt. Zum Nachweis bietet es sich laut BMF an, den Validierungsbericht aufzubewahren. Ob `e-rechnung` in Ihrem Fall als geeignete Validierungsanwendung gilt, entscheidet nicht das Werkzeug, sondern Sie mit Ihrer Steuerberatung.

`erechnung validieren --bericht ORDNER` legt je geprüfter Datei einen JSON-Bericht ab:

```bash
cd archiv/2026
erechnung validieren eingang/* --bericht berichte
```

```text
eingang/2026-017.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
  Prüfbericht: berichte/2026-017.pdf.3f88a74f3189.validierungsbericht.json
eingang/RE-2026-0001.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
  Prüfbericht: berichte/RE-2026-0001.xml.29ccd409852b.validierungsbericht.json
eingang/RE-2026-0002.xml: XRechnung 3.0 (CII)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (CII), 0 Fehler, 0 Warnungen
  Prüfbericht: berichte/RE-2026-0002.xml.8228f8899659.validierungsbericht.json
```

Der Dateiname des Berichts enthält den Namen der Rechnung und die ersten 12 Zeichen ihrer SHA-256-Summe. Eine geänderte Fassung mit gleichem Dateinamen bekommt deshalb einen eigenen Bericht. Prüfen Sie dagegen dieselbe Datei ein zweites Mal, überschreibt der neue Bericht den alten; wer den ersten Prüfzeitpunkt behalten will, prüft jede Datei nur einmal in den Archivordner. Das ist der vollständige Bericht für die XRechnung:

```json
{
  "validiert_am": "2026-10-15T22:24:55+00:00",
  "werkzeug": "e-rechnung 0.1.0",
  "regeln": "xrechnung-3.0.2-validator-configuration-2026-08-31",
  "sha256": "29ccd409852be59511072ff301dced03d7d8c2c8988f3477a1df75997bbe65fb",
  "datei": "eingang/RE-2026-0001.xml",
  "format": {
    "syntax": "UBL-Invoice",
    "spezifikation": "urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0",
    "bezeichnung": "XRechnung 3.0 (UBL)",
    "ist_e_rechnung": true,
    "pdf": false,
    "anhang": ""
  },
  "gueltig": true,
  "vorpruefung_ok": true,
  "vorpruefung": [],
  "offiziell": {
    "szenario": "EN16931 XRechnung (UBL Invoice)",
    "akzeptiert": true,
    "konfiguration": "xrechnung-3.0.2-validator-configuration-2026-08-31",
    "hinweis": "",
    "befunde": []
  },
  "offiziell_fehler": ""
}
```

| Feld | Bedeutung |
| --- | --- |
| `validiert_am` | Zeitpunkt der Prüfung in UTC (`+00:00`); 22:24 Uhr UTC am 15.10. ist 00:24 Uhr am 16.10. deutscher Sommerzeit |
| `werkzeug` | Name und Version des Prüfwerkzeugs |
| `regeln` | Version der KoSIT-Prüfkonfiguration, mit der geprüft wurde |
| `sha256` | Prüfsumme der geprüften Datei, bei ZUGFeRD des ganzen PDF |
| `datei` | Pfad, so wie er beim Aufruf angegeben wurde |
| `gueltig` | Gesamturteil |
| `offiziell` | Ergebnis der KoSIT-Regeln mit Szenario und allen Befunden |
| `vorpruefung` | Befunde der eigenen Vorprüfung (Codes mit `VP-`), nicht maßgeblich |

Bei einer ungültigen Rechnung stehen die Befunde im Bericht. Auszug aus dem Bericht einer XRechnung ohne BT-10:

```json
{
  "gueltig": false,
  "offiziell": {
    "szenario": "EN16931 XRechnung (UBL Invoice)",
    "akzeptiert": false,
    "befunde": [
      {
        "stufe": "error",
        "code": "BR-DE-15",
        "text": "[BR-DE-15] Das Element \"Buyer reference\" (BT-10) muss übermittelt werden.",
        "ort": "/Q{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice[1]",
        "quelle": "Schematron rules for Invoice - CIUS XRechnung (UBL)"
      }
    ]
  }
}
```

Auch solche Berichte bewahren Sie auf, zusammen mit der ursprünglichen Datei und der Bitte an den Lieferanten um Korrektur.

## SHA-256: Nachweis, dass die E-Rechnung unverändert ist

Eine SHA-256-Summe ist ein 64-stelliger Fingerabdruck einer Datei. Ändert sich auch nur ein Zeichen, ändert sich die ganze Summe. Weil der Prüfbericht die Summe enthält, können Sie Jahre später zeigen: Diese Datei ist genau die, die zum Zeitpunkt in `validiert_am` geprüft wurde.

Die Summe berechnen Sie mit Bordmitteln:

| System | Befehl |
| --- | --- |
| Linux | `sha256sum eingang/RE-2026-0001.xml` |
| macOS | `shasum -a 256 eingang/RE-2026-0001.xml` |
| Windows (PowerShell) | `Get-FileHash -Algorithm SHA256 eingang\RE-2026-0001.xml` |

```bash
shasum -a 256 eingang/RE-2026-0001.xml
```

```text
29ccd409852be59511072ff301dced03d7d8c2c8988f3477a1df75997bbe65fb  eingang/RE-2026-0001.xml
```

Die Summe stimmt mit dem Feld `sha256` im Prüfbericht überein. `Get-FileHash` unter Windows gibt dieselbe Summe in Großbuchstaben aus; PowerShell vergleicht Zeichenketten mit `-eq` ohne Rücksicht auf Groß- und Kleinschreibung:

```powershell
(Get-FileHash -Algorithm SHA256 eingang\RE-2026-0001.xml).Hash -eq "29ccd409852be59511072ff301dced03d7d8c2c8988f3477a1df75997bbe65fb"
```

Für einen ganzen Ordner schreiben Sie eine Liste der Summen und prüfen sie später:

```bash
sha256sum eingang/* > sha256summen.txt
cat sha256summen.txt
```

```text
3f88a74f3189f91f4707261aaf044b7653c9bebb8576ea1b7a8b22177466e8c6  eingang/2026-017.pdf
29ccd409852be59511072ff301dced03d7d8c2c8988f3477a1df75997bbe65fb  eingang/RE-2026-0001.xml
8228f889965938ccdab6fef6c7a709a338caf01ad305f2150312abd5aa359c74  eingang/RE-2026-0002.xml
```

```bash
shasum -a 256 -c sha256summen.txt
```

```text
eingang/2026-017.pdf: OK
eingang/RE-2026-0001.xml: OK
eingang/RE-2026-0002.xml: OK
```

Wurde eine Datei verändert, hier ein Betrag in `RE-2026-0002.xml`, meldet die Prüfung das und endet mit Exit-Code 1:

```text
eingang/2026-017.pdf: OK
eingang/RE-2026-0001.xml: OK
eingang/RE-2026-0002.xml: FAILED
shasum: WARNING: 1 computed checksum did NOT match
```

Grenze: Wer Dateien und Summenliste gleichzeitig ändern kann, kann beides fälschen. Die Summe belegt Unverändertheit nur so gut, wie die Summenliste und die Berichte geschützt sind, zum Beispiel durch Schreibschutz, getrennte Ablage oder eine Kopie bei der Steuerberatung.

## Ordnerstruktur für E-Rechnungen: ein einfacher Vorschlag

Eine einfache Ablage nach Jahr hält Originale, Berichte und Ansichten getrennt. Ein Ordner je Jahr erleichtert es, nach Ablauf der Frist zu entscheiden, was gelöscht werden darf. Vorher fragen Sie die Steuerberatung: Läuft für das Jahr noch eine Außenprüfung, ein Einspruch oder eine andere offene Festsetzung, verlängert sich die Frist (§ 147 Abs. 3 Satz 5 AO).

Liegt das Archiv bei einem Cloud-Anbieter, achten Sie auf den Speicherort: § 14b Abs. 2 UStG erlaubt elektronische Aufbewahrung im Inland und, mit vollständigem Online-Zugriff für das Finanzamt, im übrigen Gemeinschaftsgebiet; dann ist dem Finanzamt der Aufbewahrungsort mitzuteilen. Für Drittländer braucht es eine Bewilligung (§ 146 Abs. 2b AO). Ob diese Regel für Ihr Unternehmen gilt, klärt Ihre Steuerberatung.

```text
archiv/
  2026/
    eingang/            Originale, so wie empfangen (XML, ZUGFeRD-PDF)
    ausgang/            eigene Rechnungen, so wie versendet
    berichte/           *.validierungsbericht.json aus erechnung validieren --bericht
    ansicht/            HTML-Ansichten, nur zum Lesen, jederzeit neu erzeugbar
    sha256summen.txt    Liste der Prüfsummen aller Originale
  2027/
    ...
```

Den Dateinamen der Originale wählen Sie so, dass Sie Rechnungen wiederfinden, zum Beispiel mit Rechnungsnummer. Der Prüfbericht nennt in `datei` den Pfad beim Aufruf. Prüfen Sie deshalb aus dem Jahresordner heraus mit relativen Pfaden, wie oben gezeigt, damit der Bericht auch nach einem Umzug des Archivs passt.

## Was `erechnung` beim Archivieren nicht ist

`erechnung` ist kein Archivsystem und kein revisionssicheres Archiv. Das Werkzeug liest, prüft und zeigt E-Rechnungen an und schreibt Prüfberichte. Es verwaltet keine Zugriffsrechte, schützt keine Dateien vor Änderung oder Löschung, sichert nichts und überwacht keine Fristen. Diese Aufgaben übernimmt Ihre Ablage, Ihr Dokumentenmanagement oder Ihr Buchhaltungssystem.

| Aufgabe | `erechnung` | Ihre Ablage oder Ihr Archivsystem |
| --- | --- | --- |
| Datei prüfen und Bericht schreiben | ja | - |
| SHA-256 der Datei festhalten | ja, im Bericht | Summenliste schützen |
| Original unveränderbar speichern | nein | ja |
| Zugriffsrechte und Protokoll | nein | ja |
| Datensicherung | nein | ja |
| Fristen überwachen und löschen | nein | ja |

## E-Rechnungen archivieren: Beispiele mit Prüfbericht

### Beispiel 1: Prüfbericht für eine einzelne Eingangsrechnung

```bash
erechnung validieren eingang/RE-2026-0001.xml --bericht berichte
```

```text
eingang/RE-2026-0001.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
  Prüfbericht: berichte/RE-2026-0001.xml.29ccd409852b.validierungsbericht.json
```

Brauchen Sie bei jedem Rechnungseingang, bevor die Rechnung gebucht wird.

### Beispiel 2: Prüfsumme im Bericht mit der Datei vergleichen

```bash
grep '"sha256"' berichte/2026-017.pdf.*.json
sha256sum eingang/2026-017.pdf
```

```text
  "sha256": "3f88a74f3189f91f4707261aaf044b7653c9bebb8576ea1b7a8b22177466e8c6",
3f88a74f3189f91f4707261aaf044b7653c9bebb8576ea1b7a8b22177466e8c6  eingang/2026-017.pdf
```

Brauchen Sie, wenn Sie bei einer Prüfung zeigen wollen, dass die Datei seit der Validierung unverändert ist.

### Beispiel 3: Ganzen Jahresordner auf Änderungen prüfen

```bash
shasum -a 256 -c sha256summen.txt
```

```text
eingang/2026-017.pdf: OK
eingang/RE-2026-0001.xml: OK
eingang/RE-2026-0002.xml: OK
```

Brauchen Sie nach einem Umzug des Archivs, nach einer Wiederherstellung aus der Datensicherung oder einmal im Jahr.

### Beispiel 4: XML aus einem ZUGFeRD-PDF holen, ohne das PDF anzufassen

Aufruf aus dem Ordner über `archiv/`, mit einem Arbeitsordner `arbeit/` daneben:

```bash
erechnung extrahieren archiv/2026/eingang/2026-017.pdf -o arbeit/2026-017.xml
```

```text
factur-x.xml aus archiv/2026/eingang/2026-017.pdf gespeichert als arbeit/2026-017.xml
```

Brauchen Sie, wenn ein anderes Programm das XML braucht. Die Kopie landet außerhalb des Archivs, das PDF bleibt das Original.

### Beispiel 5: Lesbare Ansicht neben das Archiv legen

```bash
mkdir -p ansicht
erechnung anzeigen eingang/RE-2026-0001.xml -o ansicht/RE-2026-0001.html
```

```text
Ansicht geschrieben: ansicht/RE-2026-0001.html
```

Brauchen Sie, damit Kolleginnen und Kollegen Rechnungen ohne Werkzeug lesen können. Die Ansicht ist kein Original und kann jederzeit neu erzeugt werden.

## Schritt für Schritt: E-Rechnungen archivieren

1. Legen Sie einen Jahresordner an, zum Beispiel `archiv/2026/eingang/`.
2. Speichern Sie jede empfangene E-Rechnung unverändert dort, bei XRechnung die XML-Datei, bei ZUGFeRD das ganze PDF.
3. Wechseln Sie in den Jahresordner: `cd archiv/2026`.
4. Prüfen Sie neue Dateien und legen Sie die Berichte ab: `erechnung validieren eingang/* --bericht berichte`.
5. Schreiben Sie die Prüfsummen: unter Linux `sha256sum eingang/* > sha256summen.txt`, unter macOS `shasum -a 256 eingang/* > sha256summen.txt`.
6. Schützen Sie Originale, Berichte und Summenliste vor Änderung, zum Beispiel mit Schreibschutz und einer Datensicherung an einem zweiten Ort.
7. Bei ungültigen Rechnungen bitten Sie den Lieferanten um Korrektur und legen die korrigierte Fassung zusätzlich ab; die alte Datei und ihren Bericht löschen Sie nicht.
8. Halten Sie den Ablauf in Ihrer Verfahrensdokumentation fest und stimmen Sie ihn mit der Steuerberatung ab.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Nur den Ausdruck oder die HTML-Ansicht aufbewahrt | Kein strukturierter Teil im Archiv | Immer die empfangene Datei aufbewahren, die Ansicht nur zusätzlich |
| Bei ZUGFeRD nur das herausgeholte XML archiviert | Empfangenes Format fehlt, Bericht-Summe passt nicht zum XML | Das ganze PDF aufbewahren |
| XML im Editor geöffnet und gespeichert | Prüfsumme stimmt nicht mehr (`FAILED`) | Originale nur lesen, nie speichern; Datei aus der Sicherung wiederherstellen |
| Frist nach alter FAQ mit 10 Jahren angesetzt | Unklar, wann Rechnungen gelöscht werden dürfen | § 14b Abs. 1 UStG nennt acht Jahre; vor dem Löschen mit der Steuerberatung klären, ob andere Fristen greifen |
| Dieselbe Datei mehrfach mit `--bericht` geprüft | Erster Prüfzeitpunkt im Bericht ist überschrieben | Jede Datei nur einmal in den Archivordner prüfen, spätere Prüfungen in einen anderen Ordner |
| Berichte mit absoluten Pfaden erzeugt | `datei` im Bericht zeigt auf einen alten Ort | Aus dem Jahresordner mit relativen Pfaden prüfen |
| Prüfbericht nur am Bildschirm gelesen | Kein Nachweis der Prüfung | `--bericht berichte` verwenden |

## Häufige Fragen

### Wie lange muss ich E-Rechnungen aufbewahren?

Acht Jahre, laut § 14b Abs. 1 UStG und BMF-Schreiben vom 15.10.2025 (Rn. 60). Die Frist beginnt mit dem Ende des Jahres, in dem die Rechnung ausgestellt wurde. Solange die Rechnung für eine noch offene Steuerfestsetzung von Bedeutung ist, läuft die Frist nicht ab (§ 147 Abs. 3 Satz 5 AO).

### Reicht es, eine E-Rechnung auszudrucken?

Nein. Laut BMF-Schreiben vom 15.10.2025 (Rn. 60) muss zumindest der strukturierte Teil unversehrt im Ursprungsformat aufbewahrt werden, also die XML-Datei oder das ZUGFeRD-PDF.

### Muss ich bei ZUGFeRD das PDF oder das XML aufbewahren?

Das ganze PDF, so wie Sie es empfangen haben. Darin steckt das XML; das empfangene Format ist das PDF.

### Brauche ich ein GoBD-konformes Archivsystem für E-Rechnungen?

Umsatzsteuerlich ist die Speicherung außerhalb eines GoBD-konformen Systems allein kein Verstoß gegen § 14b UStG (BMF-Schreiben vom 15.10.2025, Rn. 60). Die GoBD gelten für Ihre Buchführung trotzdem; ob Ihre Ablage genügt, klären Sie mit der Steuerberatung.

### Warum soll ich den Prüfbericht aufbewahren?

Weil Rn. 35a des BMF-Schreibens vom 15.10.2025 die Aufbewahrung des Validierungsberichts nahelegt. Der Bericht dokumentiert, wann und mit welchen Regeln die Datei geprüft wurde. Ob dieses Werkzeug eine "geeignete Validierungsanwendung" im Sinne der Rn. 35a ist, entscheidet nicht das Werkzeug selbst; klären Sie das mit Ihrer Steuerberatung.

### Ist `erechnung` ein revisionssicheres Archiv?

Nein. Das Werkzeug prüft Dateien und schreibt Berichte mit Prüfsumme; Speicherung, Schutz vor Änderung, Zugriffsrechte und Datensicherung übernimmt Ihre Ablage oder Ihr Archivsystem.

### Darf ich eine E-Rechnung umbenennen?

Der Inhalt muss unverändert bleiben; die SHA-256-Summe hängt nur vom Inhalt ab, nicht vom Dateinamen. Ob Ihre Verfahrensdokumentation feste Dateinamen vorsieht, entscheiden Sie selbst oder mit der Steuerberatung.

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [E-Rechnung empfangen und lesen](./e-rechnung-empfangen.md)
- [E-Rechnung prüfen: XRechnung- und ZUGFeRD-Validator](./e-rechnung-validator.md)
- [BMF-Schreiben zur E-Rechnung](./bmf-schreiben-e-rechnung.md)
- [ZUGFeRD: Format, Profile und Versionen](./zugferd.md)
- [DATEV und E-Rechnung](./datev-e-rechnung.md)
- Beispiele: [Standardrechnung UBL](../../beispiele/01_standard/xrechnung_ubl.xml), [ZUGFeRD-PDF](../../beispiele/01_standard/zugferd_en16931.pdf), [Übersicht](../../beispiele/README.md)
