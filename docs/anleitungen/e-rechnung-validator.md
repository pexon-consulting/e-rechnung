# E-Rechnung prüfen: XRechnung- und ZUGFeRD-Validator mit den offiziellen Regeln

Ob eine E-Rechnung gültig ist, prüfen Sie mit einem Validator, der die offiziellen Regeln der KoSIT anwendet: Er meldet jeden Verstoß mit einem Code wie BR-DE-15, und gültig ist die Datei, wenn keine Meldung der Stufe "Fehler" übrig bleibt. Kostenlos, lokal und ohne Upload geht das für XRechnung und ZUGFeRD mit `erechnung validieren rechnung.xml`. Technisch prüft der Validator zuerst den Aufbau der Datei (XML-Schema für UBL oder CII) und danach die Geschäftsregeln der EN 16931 und der XRechnung.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Buchhaltung, Steuerkanzleien und IT, die E-Rechnungen auf Gültigkeit prüfen.

## Das Wichtigste in Kürze

- Eine Validierung prüft Wohlgeformtheit, XML-Schema und Schematron-Regeln, in dieser Reihenfolge; nach Schemafehlern laufen die Schematron-Regeln nicht mehr.
- Welche Regeln gelten, entscheidet die Kennung in BT-24: XRechnung 3.0 bekommt EN 16931 plus BR-DE-Regeln, ZUGFeRD EN 16931 nur die EN-16931-Regeln.
- Das offizielle Werkzeug ist der KoSIT-Validator (Java, Version 1.6.3) mit der Prüfkonfiguration XRechnung 3.0.2 vom 31.08.2026; `erechnung validieren` führt genau diese Regeldateien in Python aus.
- Laut BMF-Schreiben vom 15.10.2025 (Rn. 35a) darf sich ein Unternehmen bei Beachtung der Sorgfalt eines ordentlichen Kaufmanns auf das technische Ergebnis einer Validierung hinsichtlich Format und Geschäftsregeln verlassen. Inhaltliche Fehler wie ein falscher Steuersatz erkennt eine Validierung nicht immer; die eigene Prüfpflicht bleibt. Zum Nachweis bietet es sich laut BMF an, den Validierungsbericht aufzubewahren. Ob `e-rechnung` in Ihrem Fall als geeignete Validierungsanwendung gilt, entscheidet nicht das Werkzeug, sondern Sie mit Ihrer Steuerberatung.
- Die PDF/A-3-Konformität einer ZUGFeRD-Datei prüft `erechnung` nicht; dafür gibt es Mustang mit eingebautem veraPDF.

## Was prüft ein E-Rechnung-Validator?

Ein E-Rechnung-Validator ist ein Programm, das eine Rechnungsdatei gegen die technischen Vorgaben ihres Formats prüft und jeden Verstoß mit Regel-Code und Stufe meldet. Die Prüfung läuft wie beim KoSIT-Validator in festen Schritten:

| Schritt | Was geprüft wird | Typischer Code bei Fehler |
| --- | --- | --- |
| 1. Wohlgeformtheit | Ist die Datei überhaupt lesbares XML? | `VP-LESEN` |
| 2. Szenario | Welche Regeln gelten? Auswahl über BT-24 (`cbc:CustomizationID` bzw. `ram:GuidelineSpecifiedDocumentContextParameter/ram:ID`) | `SZENARIO` |
| 3. XML-Schema | Stimmen Elementnamen, Reihenfolge und Datentypen (UBL 2.1 oder CII D16B)? | `XSD` |
| 4. Schematron EN 16931 | Rechenregeln, Pflichtfelder, Codelisten der Norm | `BR-CO-16`, `BR-S-08`, `BR-CL-23` |
| 5. Schematron XRechnung | Deutsche Zusatzregeln und übernommene Peppol-Regeln | `BR-DE-15`, `PEPPOL-EN16931-R010` |
| 6. Umstufung | Das Szenario stuft einzelne Regeln hoch oder herunter (`customLevel`) | z. B. `BR-CL-23` nur Warnung |

Wichtig für die Fehlersuche: Findet das XML-Schema einen Fehler, bricht die Prüfung dort ab. Die Schematron-Regeln laufen dann nicht, so wie beim KoSIT-Validator. Nach dem Beheben eines Schemafehlers können also neue Meldungen auftauchen.

Jeder Befund hat eine von drei Stufen:

| Stufe | Ausgabe | Bedeutung | Folge für das Ergebnis |
| --- | --- | --- | --- |
| error | `FEHLER` | Regel verletzt ("muss") | Rechnung ungültig |
| warning | `WARNUNG` | Empfehlung verletzt ("soll") | Rechnung bleibt gültig, außer mit `--streng` |
| information | `INFO` | Hinweis | nur mit `--alle` sichtbar |

## Gültig, ungültig und was das BMF dazu sagt

Das BMF-Schreiben vom 15.10.2025 unterscheidet zwei Arten von Fehlern:

| Art | Quelle | Beispiel | Folge laut BMF |
| --- | --- | --- | --- |
| Formatfehler | Rn. 6a | Datei entspricht nicht der Syntax, z. B. Schemafehler | keine E-Rechnung, sondern sonstige Rechnung |
| Geschäftsregelfehler | Rn. 6b | fehlendes BT-10, Steuerbetrag passt nicht zum Steuersatz | hängt vom Inhalt ab (Rn. 35a) |

Laut Rn. 35a sind Verstöße gegen Pflichtangaben nach §§ 14 Abs. 4, 14a UStG Inhaltsfehler, die Rechnung ist dann nicht ordnungsmäßig. Geschäftsregelfehler zu anderen Inhalten, zum Beispiel ein fehlendes BT-10, sind umsatzsteuerlich unbeachtlich. Die Validierung ersetzt die Prüfpflicht des Empfängers nicht. Wie eine einzelne Meldung einzuordnen ist, steht in der Anleitung [Fehlermeldungen](./e-rechnung-fehlermeldungen.md); im Einzelfall mit der Steuerberatung klären.

## Offizielle Validatoren: KoSIT-Validator und Mustang

Der KoSIT-Validator ist das Referenzwerkzeug für XRechnung. Er ist Open Source (Apache-2.0), braucht Java 11 oder neuer und liegt aktuell in Version 1.6.3 vom 20.08.2026 vor ([GitHub](https://github.com/itplr-kosit/validator)). Die Regeln kommen als eigene Prüfkonfiguration, aktuell `xrechnung-3.0.2-validator-configuration-2026-08-31.zip` ([GitHub](https://github.com/itplr-kosit/validator-configuration-xrechnung)). Der Aufruf laut Dokumentation der Konfiguration:

```bash
java -jar validator-1.6.3-standalone.jar -s scenarios.xml -r ${PWD} -h rechnung.xml
```

Das Ergebnis steht in `rechnung-report.xml`, mit `-h` zusätzlich in `rechnung-report.html`. Eine PDF/A-3-Prüfung leistet der KoSIT-Validator nicht, und für ZUGFeRD BASIC oder EXTENDED gibt es in der Konfiguration kein eigenes Szenario.

Mustang ist ein Java-Werkzeug für ZUGFeRD und XRechnung (Apache-2.0, aktuell core-2.26.0). Es prüft das PDF mit eingebautem veraPDF auf PDF/A-3 und das XML gegen Schema und Schematron ([mustangproject.org](https://www.mustangproject.org/commandline/)):

```bash
java -Xmx1G -Dfile.encoding=UTF-8 -jar Mustang-CLI-2.26.0.jar --no-notices --action validate --source invoice.pdf
```

Laut Mustang-Dokumentation werden EN-16931-Dateien zusätzlich auf Hinweis-Ebene gegen XRechnung geprüft. Daher kommt die häufige Meldung BR-DE-15 bei ZUGFeRD-Dateien, die gar keine XRechnung sein sollen.

## Online-Validatoren und Datenschutz

Es gibt zahlreiche private Online-Validatoren, meist auf Basis von KoSIT oder Mustang. Dort lädt man die Rechnung hoch, also Namen, Anschriften, Bankverbindung, Beträge und Leistungen von Kunden oder Lieferanten. Ob das zulässig ist, hängt von Vertrag und Datenschutzregeln des Anbieters ab. Wer echte Rechnungen prüft, ist mit einer lokalen Prüfung auf der sicheren Seite: `erechnung validieren` lädt nur einmal die öffentliche Regelkonfiguration herunter, die Rechnungsdaten verlassen den Rechner nicht.

## XRechnung validieren mit `erechnung validieren`

Installation einmalig (Python 3.10 oder neuer, kein Java):

```bash
pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
```

Der Befehl hat zwei Aliase: `erechnung check` und `erechnung prüfen` tun dasselbe. Er nimmt XML-Dateien (UBL, CII) und ZUGFeRD-PDFs, auch viele auf einmal.

| Option | Wirkung |
| --- | --- |
| `--json` | Ergebnis als JSON: bei einer Datei ein einzelnes Objekt, bei mehreren eine Liste |
| `--ohne-offiziell` | nur Vorprüfung, ohne Download und ohne saxonche |
| `--offline` | nichts herunterladen, nur Cache oder `ERECHNUNG_KOSIT_KONFIG` |
| `--streng` | Warnungen zählen als Fehler (Exit-Code 1) |
| `--alle` | auch Befunde der Stufe information ausgeben |
| `--bericht ORDNER` | je Datei einen JSON-Prüfbericht ablegen |

| Exit-Code | Bedeutung |
| --- | --- |
| 0 | alle Dateien gültig |
| 1 | mindestens eine Datei ungültig (mit `--streng` auch bei Warnungen) |
| 2 | Prüfung nicht möglich, z. B. Regeln nicht im Cache, kein lesbares XML oder PDF ohne eingebettetes XML |

Eine gültige XRechnung aus den Beispielen:

```console
$ erechnung validieren beispiele/01_standard/xrechnung_ubl.xml
beispiele/01_standard/xrechnung_ubl.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
$ echo $?
0
```

Die erste Zeile nennt das erkannte Format, die zweite das Urteil, die Regelversion und das Szenario. Darunter folgen die offiziellen Befunde der KoSIT-Regeln. Danach kommt getrennt die Vorprüfung: eine zusätzliche Prüfung dieses Werkzeugs, die Fehler in einfachem Deutsch erklärt und an dem Kürzel VP- erkennbar ist. Ob eine Rechnung gültig ist, entscheiden allein die KoSIT-Regeln.

### Umstufungen: warum BR-CL-23 nur eine Warnung ist

Die Prüfkonfiguration der KoSIT legt je Szenario fest, dass einzelne Regeln eine andere Stufe bekommen (`customLevel` in `scenarios.xml`). Ein Beispiel: BR-CL-23 (Einheitencode nicht nach UN/ECE Recommendation 20) ist im Schematron der EN 16931 ein Fehler, im XRechnung-Szenario aber nur eine Warnung. Eine XRechnung mit der Einheit `Std` statt `HUR` ist daher gültig. In der JSON-Ausgabe steht die ursprüngliche Stufe als `stufe_original`:

```console
$ erechnung validieren --json einheit_std.xml
{
  "datei": "einheit_std.xml",
  ...
  "gueltig": true,
  "vorpruefung_ok": false,
  "vorpruefung": [
    {
      "stufe": "error",
      "code": "VP-EINHEIT",
      "text": "Position 1: Einheit 'Std' ist kein UN/ECE-Code (z. B. C62, HUR, DAY).",
      "ort": "",
      "quelle": "Vorprüfung"
    }
  ],
  "offiziell": {
    "szenario": "EN16931 XRechnung (UBL Invoice)",
    "akzeptiert": true,
    "konfiguration": "xrechnung-3.0.2-validator-configuration-2026-08-31",
    "hinweis": "",
    "befunde": [
      {
        "stufe": "warning",
        "code": "BR-CL-23",
        "text": "[BR-CL-23]-Unit code MUST be coded according to the UN/ECE Recommendation 20 with Rec 21 extension",
        "ort": "/Q{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice[1]/Q{...}InvoiceLine[1]/Q{...}InvoicedQuantity[1]",
        "quelle": "Schematron rules for EN16931 (UBL)",
        "stufe_original": "error"
      }
    ]
  },
  "offiziell_fehler": ""
}
```

`gueltig` folgt dem KoSIT-Urteil (`akzeptiert`). Die Vorprüfung meldet `VP-EINHEIT` zwar als Fehler, das ändert das Urteil und den Exit-Code (hier 0) aber nicht.

### Szenario und Hinweis lesen

Für eine Kennung in BT-24, für die die KoSIT kein eigenes Szenario hat, die aber mit `urn:cen.eu:en16931:2017` beginnt (etwa ZUGFeRD BASIC oder EXTENDED), prüft das Werkzeug den Kern nach EN 16931 und schreibt eine Zeile `Hinweis:`. Das gilt auch für vertippte oder veraltete XRechnung-Kennungen wie `xrechnung_2.3`. Die BR-DE-Regeln laufen dann nicht. Steht bei einer XRechnung im Szenario nicht `XRechnung`, die Kennung in BT-24 prüfen.

### Vorprüfung: die VP-Codes

Zusätzlich zur offiziellen Prüfung läuft eine eigene Vorprüfung. Sie erklärt häufige Fehler auf Deutsch und rechnet nach. Sie ersetzt die offizielle Prüfung nicht und ändert den Exit-Code nicht, solange die offizielle Prüfung läuft. Nur mit `--ohne-offiziell` entscheidet sie allein.

| Code | Prüft | Stufe |
| --- | --- | --- |
| `VP-LESEN` | Datei lesbar, PDF enthält ein Rechnungs-XML | error |
| `VP-FORMAT` | ZUGFeRD MINIMUM oder BASIC WL (keine E-Rechnung) oder unbekannte Spezifikation | error |
| `VP-14-4-1` | Name und Anschrift (Ort, PLZ) von Verkäufer und Käufer | error |
| `VP-14-4-2` | USt-IdNr. (BT-31) oder Steuernummer (BT-32) des Verkäufers | error, bis 250 EUR brutto warning |
| `VP-14-4-3` | Rechnungsdatum (BT-2) | error |
| `VP-14-4-4` | Rechnungsnummer (BT-1) | error |
| `VP-14-4-5` | Positionen und Bezeichnung (BT-153) | error |
| `VP-14-4-6` | Liefer- oder Leistungsdatum (BT-72, BG-14, BG-26) | warning |
| `VP-14-4-8` | Befreiungsgrund (BT-120/121) bei E, AE, K, G, O | error |
| `VP-USTID` | deutsche USt-IdNr. im Format DE plus 9 Ziffern | warning |
| `VP-EINHEIT` | Einheit sieht wie ein UN/ECE-Code aus | error |
| `VP-13B` | Reverse Charge (AE) mit USt-IdNr. (BT-48) oder Registernummer (BT-47) des Käufers | error |
| `VP-IG` | Innergemeinschaftliche Lieferung (K) mit USt-IdNr. des Käufers | error |
| `VP-BR-DE-15` | Käuferreferenz BT-10 (nur XRechnung) | error |
| `VP-LEITWEG` | Format und Prüfziffer der Leitweg-ID (nur XRechnung) | warning |
| `VP-BR-DE-2` | Kontakt mit Name, Telefon, E-Mail (BT-41 bis BT-43, nur XRechnung) | error |
| `VP-BR-DE-ADR` | elektronische Adressen BT-34 und BT-49 (nur XRechnung) | error |
| `VP-BR-DE-1` | Zahlungsart BT-81 (nur XRechnung) | error |
| `VP-IBAN` | Prüfziffer der IBAN | warning |
| `VP-FAELLIG` | Fälligkeitsdatum nicht vor dem Rechnungsdatum | warning |
| `VP-SUMME`, `VP-NETTO`, `VP-STEUER`, `VP-STEUERSATZ`, `VP-BRUTTO`, `VP-ZAHLBETRAG` | Rechenprüfung der Summen und Steuern | error |

`VP-EINHEIT` ist eine grobe Prüfung: Sie meldet Schreibweisen wie `Std` oder `Stück`, aber keine drei Großbuchstaben wie `STD`, auch wenn die Liste sie nicht kennt. Für Einheiten zählt BR-CL-23.

Ein Fall, den nur die Vorprüfung findet: eine Leitweg-ID mit falscher Prüfziffer. Die KoSIT-Regeln prüfen die Prüfziffer nicht, die Rechnung ist offiziell gültig.

```console
$ erechnung validieren leitweg_pruefziffer.xml
leitweg_pruefziffer.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
  Vorprüfung (Erklärungen, nicht maßgeblich):
  WARNUNG VP-LEITWEG: Leitweg-ID 04011000-12345-04 hat ein falsches Format oder eine falsche Prüfziffer (Formatspezifikation 2.0.2). Die Behörde kann die Rechnung dann nicht zuordnen.
```

## ZUGFeRD prüfen: PDF rein, XML wird geprüft

Ein ZUGFeRD-Validator muss zwei Dinge prüfen: das eingebettete XML und das PDF/A-3 drumherum. `erechnung validieren` nimmt das PDF, holt das XML heraus (`factur-x.xml` oder `xrechnung.xml`) und prüft es mit den KoSIT-Regeln. Profil EN 16931 läuft im Szenario `EN16931 (CII)`, Profil XRECHNUNG im XRechnung-Szenario.

```console
$ erechnung validieren beispiele/01_standard/zugferd_en16931.pdf
beispiele/01_standard/zugferd_en16931.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
```

Ein PDF ohne eingebettetes XML ist keine E-Rechnung:

```console
$ erechnung validieren nur_pdf.pdf
nur_pdf.pdf: unbekannt
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-LESEN: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
$ echo $?
2
```

Grenzen: Ob das PDF wirklich PDF/A-3 ist und die XMP-Metadaten stimmen, prüft `erechnung` nicht. Dafür Mustang verwenden (siehe oben). Profile MINIMUM und BASIC WL meldet die Vorprüfung als `VP-FORMAT`, weil sie laut UStAE 14.1 Abs. 14 keine E-Rechnung sind. BASIC und EXTENDED werden gegen EN 16931 geprüft, mit Hinweis.

## Wie genau ist die Prüfung? Abgleich mit dem KoSIT-Validator

Das Skript `scripts/abgleich_kosit.py` im Repo prüft 222 Dateien mit beiden Werkzeugen: 136 eigene (die 9 Beispiele in UBL und CII plus absichtlich kaputte Varianten wie fehlendes BT-10, falscher Steuersatz, Schemafehler) und 86 Dateien der KoSIT-Testsuite. Verglichen wird je Datei, ob sie angenommen wird, und die Menge der Regel-Codes mit ihrer Stufe. Ergebnis: 222 von 222 gleich wie der KoSIT-Validator 1.6.3. Die CI des Repos lässt diesen Abgleich mit Java laufen.

## E-Rechnungen in der CI prüfen (GitHub Actions)

Wer Rechnungen aus einem eigenen Programm erzeugt, kann jede Änderung automatisch prüfen lassen. Mit `uvx` braucht es keine Installation. Ein Schritt in einem GitHub-Actions-Workflow:

```yaml
- uses: astral-sh/setup-uv@v6
- name: E-Rechnungen prüfen
  run: >
    uvx --from "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
    erechnung validieren --streng --bericht berichte ausgabe/*.xml
```

Der Schritt schlägt mit Exit-Code 1 fehl, sobald eine Datei einen Fehler oder (wegen `--streng`) eine Warnung hat. Damit die Regeln nicht bei jedem Lauf neu geladen werden, `ERECHNUNG_CACHE` auf einen Ordner setzen und ihn mit `actions/cache` sichern, so wie es die CI des Repos tut.

## XRechnung validieren: Beispiele mit Ausgabe

### Beispiel 1: Eine ungültige XRechnung finden

```console
$ erechnung validieren ohne_bt10.xml
ohne_bt10.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-DE-15: [BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BR-DE-15: Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.
$ echo $?
1
```

Der Normalfall: Code nachschlagen in [Fehlermeldungen](./e-rechnung-fehlermeldungen.md#br-de-15), Feld ergänzen, neu prüfen.

### Beispiel 2: Einen Ordner prüfen und Prüfberichte ablegen

```console
$ erechnung validieren --bericht berichte eingang/*
eingang/01_standard.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
  Prüfbericht: berichte/01_standard.xml.29ccd409852b.validierungsbericht.json
...
eingang/zugferd_falsch.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 (CII), 1 Fehler, 0 Warnungen
  FEHLER  BR-CO-16: [BR-CO-16]-Amount due for payment (BT-115) = Invoice total amount with VAT (BT-112) -Paid amount (BT-113) +Rounding amount (BT-114).
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-ZAHLBETRAG: Zahlbetrag BT-115 2010.91 passt nicht zu Brutto - Vorauszahlung + Rundung.
  Prüfbericht: berichte/zugferd_falsch.pdf.c5f4d32aa126.validierungsbericht.json
```

Für den Rechnungseingang: XML und PDF gemischt, ein Bericht je Datei. Der Bericht enthält Zeitpunkt, Werkzeug, Regelversion und SHA-256 der Datei (gekürzt, der Rest entspricht der Ausgabe von `--json`):

```json
{
  "validiert_am": "2026-10-15T22:23:58+00:00",
  "werkzeug": "e-rechnung 0.1.0",
  "regeln": "xrechnung-3.0.2-validator-configuration-2026-08-31",
  "sha256": "29ccd409852be59511072ff301dced03d7d8c2c8988f3477a1df75997bbe65fb",
  "datei": "eingang/01_standard.xml",
  "gueltig": true,
  "vorpruefung_ok": true
}
```

### Beispiel 3: Warnungen als Fehler werten

```console
$ erechnung validieren --streng einheit_std.xml
einheit_std.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 1 Warnungen
  WARNUNG BR-CL-23: [BR-CL-23]-Unit code MUST be coded according to the UN/ECE Recommendation 20 with Rec 21 extension
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-EINHEIT: Position 1: Einheit 'Std' ist kein UN/ECE-Code (z. B. C62, HUR, DAY).
$ echo $?
1
```

Ohne `--streng` endet derselbe Aufruf mit 0. Für eigene Rechnungsausgänge `--streng` nehmen, damit auch Warnungen auffallen.

### Beispiel 4: Hinweise mit `--alle` sehen

```console
$ erechnung validieren --alle ohne_leistungsdatum.xml
ohne_leistungsdatum.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
  INFO    BR-DE-TMP-32: [BR-DE-TMP-32] Eine Rechnung sollte zur Angabe des Liefer-/Leistungsdatums entweder BT-72 "Actual delivery date", BG-14 "Invoicing period" oder in jeder Rechnungsposition BG-26 "Invoice line period" enthalten.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  WARNUNG VP-14-4-6: Kein Liefer- oder Leistungsdatum (BT-72, BG-14 oder BG-26). Pflichtangabe nach § 14 Abs. 4 Nr. 6 UStG, außer es entspricht dem Rechnungsdatum und das ist vermerkt.
```

Die Rechnung ist technisch gültig, das Leistungsdatum ist aber eine Pflichtangabe nach § 14 Abs. 4 Nr. 6 UStG.

### Beispiel 5: Offline prüfen

```console
$ erechnung konfiguration
KoSIT-Prüfkonfiguration: xrechnung-3.0.2-validator-configuration-2026-08-31
Ordner: /Users/.../.cache/erechnung/xrechnung-3.0.2-validator-configuration-2026-08-31
$ erechnung validieren --offline ohne_bt10.xml
ohne_bt10.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  ...
```

`erechnung konfiguration` lädt die Regeln einmal in den Cache (`~/.cache/erechnung`, änderbar mit `ERECHNUNG_CACHE`). Danach läuft `--offline` ohne Netz. Fehlt der Cache, endet der Aufruf mit Exit-Code 2:

```console
$ ERECHNUNG_CACHE=leer erechnung validieren --offline ohne_bt10.xml
ohne_bt10.xml: XRechnung 3.0 (UBL)
  Offizielle Prüfung nicht möglich: xrechnung-3.0.2-validator-configuration-2026-08-31 liegt nicht im Cache (.../leer/xrechnung-3.0.2-validator-configuration-2026-08-31) und offline ist gesetzt.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BR-DE-15: Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.
$ echo $?
2
```

Auf Rechnern ganz ohne Internet `ERECHNUNG_KOSIT_KONFIG=/pfad/zur/konfiguration.zip` setzen, mit der ZIP-Datei von der GitHub-Seite der KoSIT. Trägt die ZIP-Datei den Originalnamen der festen Version, prüft das Werkzeug ihre SHA-256-Summe und bricht bei einer Abweichung ab; eigene, bewusst geänderte Regeln erlauben Sie mit `ERECHNUNG_KOSIT_KONFIG_OHNE_HASH=1`. Jede ZIP wird in einen eigenen Cache-Ordner mit ihrer Prüfsumme im Namen entpackt.

### Beispiel 6: Ergebnisse auswerten mit `--json`

```console
$ erechnung validieren --json eingang/* > ergebnis.json
$ python3 -c '
import json
for e in json.load(open("ergebnis.json")):
    befunde = (e["offiziell"] or {}).get("befunde", [])
    print(e["datei"], e["gueltig"], ",".join(b["code"] for b in befunde if b["stufe"] == "error"))
'
eingang/01_standard.xml True
eingang/02_gemischte_steuersaetze.xml True
eingang/08_b2g_leitweg_id.xml True
eingang/ohne_bt10.xml False BR-DE-15
eingang/zugferd_falsch.pdf False BR-CO-16
```

Für Tabellen, Tickets oder ein Dashboard im Rechnungseingang. `gueltig` ist `null`, wenn die offizielle Prüfung nicht laufen konnte. Bei genau einer Datei ist die Ausgabe ein einzelnes Objekt statt einer Liste; ein Skript, das beides verarbeiten soll, prüft das vorher (in Python etwa mit `isinstance(daten, dict)`).

### Beispiel 7: Aus Python prüfen

```python
from erechnung import validieren

e = validieren("ohne_bt10.xml")
print(e.gueltig, [b.code for b in e.offiziell.fehler], [b.code for b in e.vorpruefung])
# False ['BR-DE-15'] ['VP-BR-DE-15']
```

## Schritt für Schritt: eine E-Rechnung prüfen

1. Installieren: `pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"`. Python 3.10 oder neuer genügt, Java ist nicht nötig.
2. Regeln laden: `erechnung konfiguration`. Das passiert sonst automatisch beim ersten Prüfen.
3. Prüfen: `erechnung validieren rechnung.xml` oder `erechnung validieren rechnung.pdf` für ZUGFeRD.
4. Urteil lesen: `GÜLTIG` oder `UNGÜLTIG` in der zweiten Zeile, dahinter das Szenario. Bei einer XRechnung muss dort `XRechnung` stehen.
5. Jede Zeile mit `FEHLER` beheben. Den Code in der Anleitung [Fehlermeldungen](./e-rechnung-fehlermeldungen.md) nachschlagen. Nach Schemafehlern (`XSD`) neu prüfen, weil erst dann die Geschäftsregeln laufen.
6. Warnungen ansehen. Für eigene Rechnungen mit `--streng` prüfen.
7. Für die Ablage mit `--bericht berichte` prüfen und den Bericht mit der Rechnung aufbewahren (BMF-Schreiben vom 15.10.2025, Rn. 35a).

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Nur das PDF geprüft, nicht das XML | PDF/A-Prüfung ok, Rechnung trotzdem abgelehnt | ZUGFeRD-PDF mit `erechnung validieren` prüfen, es prüft das eingebettete XML |
| ZUGFeRD EN 16931 gegen XRechnung geprüft | `BR-DE-15` bei einer Rechnung ohne Behördenbezug | Szenario richtet sich nach BT-24; nur Profil XRECHNUNG braucht BR-DE-Regeln |
| Vertippte Kennung in BT-24 | Szenario `EN16931 (UBL Invoice)` und `Hinweis:` statt XRechnung | Kennung auf `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` setzen |
| Vorprüfung für maßgeblich gehalten | `FEHLER VP-...`, aber Urteil `GÜLTIG` | Maßgeblich ist das KoSIT-Urteil; die Vorprüfung erklärt nur |
| Warnungen übersehen | Exit-Code 0, später Rückfrage vom Empfänger | `--streng` verwenden |
| Nach Schemafehler aufgehört | Nach der Korrektur plötzlich neue Fehler | Normal: Schematron läuft erst ohne Schemafehler |
| Prüfung in der CI ohne Netz | Exit-Code 2, "liegt nicht im Cache" | `ERECHNUNG_CACHE` cachen oder `ERECHNUNG_KOSIT_KONFIG` setzen |

## Häufige Fragen

### Wie prüfe ich, ob eine E-Rechnung gültig ist?

Mit einem Validator, der die offiziellen KoSIT-Regeln anwendet, zum Beispiel `erechnung validieren rechnung.xml` oder dem KoSIT-Validator in Java. Gültig ist die Rechnung, wenn das Urteil `GÜLTIG` lautet, also weder Schemafehler noch Befunde der Stufe error vorliegen.

### Gibt es einen kostenlosen XRechnung-Validator?

Ja. Der KoSIT-Validator, Mustang und `erechnung` sind Open Source und kostenlos. `erechnung` braucht kein Java und lädt keine Rechnungsdaten hoch.

### Ist ein ZUGFeRD-Validator dasselbe wie ein XRechnung-Validator?

Teilweise. Beide prüfen das XML gegen EN 16931; ein ZUGFeRD-Validator prüft zusätzlich das PDF/A-3. `erechnung validieren` prüft das XML aus dem PDF, für PDF/A-3 ist Mustang zuständig.

### Ist meine Rechnung ungültig, wenn eine Warnung kommt?

Nein. Warnungen (Stufe warning) machen eine Rechnung nicht ungültig, das Urteil bleibt `GÜLTIG`. Sie zeigen Empfehlungen ("soll"), die der Empfänger trotzdem bemängeln kann.

### Muss ich eingehende E-Rechnungen validieren?

Das BMF-Schreiben vom 15.10.2025 schreibt keine Validierung vor. Laut Rn. 35a darf sich ein Unternehmen bei Beachtung der Sorgfalt eines ordentlichen Kaufmanns auf das technische Ergebnis einer Validierung hinsichtlich Format und Geschäftsregeln verlassen. Inhaltliche Fehler wie ein falscher Steuersatz erkennt eine Validierung nicht immer; die eigene Prüfpflicht bleibt. Zum Nachweis bietet es sich laut BMF an, den Validierungsbericht aufzubewahren. Ob `e-rechnung` in Ihrem Fall als geeignete Validierungsanwendung gilt, entscheidet nicht das Werkzeug, sondern Sie mit Ihrer Steuerberatung.

### Warum findet `erechnung` andere Fehler als ein Online-Validator?

Meist wurde ein anderes Szenario oder eine andere Regelversion verwendet. `erechnung` nennt beides in jeder Ausgabe (`xrechnung-3.0.2-validator-configuration-2026-08-31`, Szenario). Bei gleicher Konfiguration ist das Ergebnis laut Abgleich gleich wie beim KoSIT-Validator.

### Prüft der Validator auch, ob die Leitweg-ID stimmt?

Die KoSIT-Regeln prüfen nur, dass BT-10 vorhanden ist. Format und Prüfziffer der Leitweg-ID prüft die Vorprüfung (`VP-LEITWEG`) und der Befehl `erechnung leitweg-id`.

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md): jede Meldung mit Ursache und Lösung
- [XRechnung](./xrechnung.md): Aufbau und Pflichtfelder
- [ZUGFeRD](./zugferd.md): Profile und welche davon E-Rechnungen sind
- [E-Rechnung empfangen](./e-rechnung-empfangen.md): öffnen und anzeigen
- [E-Rechnung archivieren](./e-rechnung-archivieren.md): Prüfbericht aufbewahren
- [Leitweg-ID](./leitweg-id.md) und die [Beispiele](../../beispiele/README.md) mit ihren Prüfergebnissen
- [E-Rechnung Pflicht: ab wann, für wen und welche Übergangsfristen gelten](./e-rechnung-pflicht.md)
- [BMF-Schreiben zur E-Rechnung: was Formatfehler und Geschäftsregelfehler bedeuten](./bmf-schreiben-e-rechnung.md)
- [E-Rechnung Beispiel: XRechnung und ZUGFeRD Beispieldateien zum Herunterladen](./e-rechnung-beispiel.md)
- [Lexware, sevdesk, SAP: E-Rechnung aus dem eigenen Programm testen](./e-rechnung-buchhaltungssoftware.md)
- [E-Rechnung mit KI prüfen: MCP-Server für Claude, Cursor und Co.](./e-rechnung-ki-mcp.md)
