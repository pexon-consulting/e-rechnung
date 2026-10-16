# E-Rechnung Software kostenlos: Open-Source-Werkzeuge im Überblick

Kostenlose E-Rechnung-Software gibt es für jede Teilaufgabe: Den KoSIT-Validator und die KoSIT-Visualisierung zum Prüfen und Anzeigen von XRechnungen, Mustang und den Quba-Viewer für ZUGFeRD, Python-Bibliotheken wie drafthorse und factur-x für Entwickler und das Kommandozeilen-Werkzeug `erechnung`, das lesen, prüfen, erstellen und DATEV-Export ohne Java verbindet. Alle sind Open Source und laufen lokal. Was kostenlose Werkzeuge nicht leisten, sind Versand über Peppol, Mahnwesen und ein revisionssicheres Archiv; dafür ist eine Buchhaltungssoftware gedacht.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil von [E-Rechnung in Python](../../README.md).

## Das Wichtigste in Kürze

- Für den Empfang reicht laut BMF-Schreiben vom 15.10.2025 (UStAE 14.1) ein E-Mail-Postfach; zum Lesen und Prüfen genügen kostenlose Werkzeuge.
- Der KoSIT-Validator (Apache-2.0, Java 11+) ist die Referenz für die XRechnung-Prüfung; `erechnung` führt dieselben KoSIT-Regeln ohne Java aus.
- Mustang (Apache-2.0, Java) prüft zusätzlich PDF/A-3 bei ZUGFeRD-PDFs, was weder der KoSIT-Validator noch `erechnung` können.
- Der Quba-Viewer (Apache-2.0) zeigt XRechnung und ZUGFeRD als Programm für Windows, macOS und Linux an, ohne Kommandozeile.
- Online-Validatoren sind bequem, dafür laden Sie Rechnungsdaten auf einen fremden Server; lokale Prüfung ist datenschutzfreundlicher.
- Wer viele Ausgangsrechnungen schreibt, Rechnungen per Peppol versenden oder revisionssicher archivieren muss, braucht eine Buchhaltungssoftware.

## Welche kostenlose E-Rechnung-Software gibt es?

Ein E-Rechnung-Programm muss vier Dinge können: die Datei lesbar machen, sie gegen die Regeln prüfen, eigene E-Rechnungen erzeugen und die Daten an die Buchhaltung weitergeben. Kostenlose Werkzeuge decken meist ein oder zwei davon ab.

| Werkzeug | Lesen | Prüfen | Erstellen | ZUGFeRD | DATEV | Java nötig | Lizenz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| KoSIT-Validator 1.6.3 | Prüfbericht als HTML | ja, XRechnung und EN 16931 | nein | nur das XML, kein PDF/A-3 | nein | ja, Java 11+ | Apache-2.0 |
| KoSIT-Visualisierung 2026-10-13 | ja, HTML und PDF | nein | nein | CII-XML, nicht das PDF | nein | XSLT 2.0, braucht Saxon | Apache-2.0 |
| Mustang 2.26.0 | ja (`visualize`, `extract`) | ja, XML und PDF/A-3 | ja (`combine`, `ubl`) | ja | nein | ja | Apache-2.0 |
| Quba-Viewer 1.5.1 | ja | optional über den Online-Dienst Mustangserver | nein | ja | nein | nein | Apache-2.0 |
| drafthorse 2025.2.0 | CII parsen | nur XML-Schema | CII/ZUGFeRD | ja | nein | nein (Python) | Apache-2.0 |
| factur-x 7.7 | CII und UBL parsen | XML-Schema, Schematron über externen Saxon-Server | CII und UBL, kein XRechnung-Profil | ja | nein | nein (Python) | BSD |
| pycheval 0.3.3 | Factur-X lesen | nicht angegeben | MINIMUM bis EN 16931 | ja, ohne EXTENDED und XRechnung | nein | nein (Python 3.11+) | Apache-2.0 |
| `erechnung` 0.1.0 | ja, Text, JSON, HTML | ja, KoSIT-Regeln plus Vorprüfung | XRechnung UBL/CII, ZUGFeRD | ja, ohne PDF/A-Prüfung | ja, Buchungsstapel | nein (Python 3.10+) | MIT |

Quellen: GitHub-Releases und PyPI der Projekte, abgefragt am 15.10.2026 (Links unter [Weiterlesen](#weiterlesen)). Funktionen laut Projektdokumentation; bei `erechnung` selbst ausprobiert.

## KoSIT-Validator: die Referenz für XRechnung

Der KoSIT-Validator ist das Prüfprogramm der Koordinierungsstelle für IT-Standards (KoSIT), die die XRechnung herausgibt. Er ist ein Java-Programm und braucht Java 11 oder neuer. Die Prüfregeln stecken nicht im Programm, sondern in einer eigenen Konfiguration, aktuell `xrechnung-3.0.2-validator-configuration-2026-08-31.zip` vom 02.09.2026.

Der Aufruf laut [Dokumentation der Konfiguration](https://github.com/itplr-kosit/validator-configuration-xrechnung) lautet `java -jar validator-1.6.3-standalone.jar -s scenarios.xml -r ${PWD} -h rechnung.xml`. Das Ergebnis ist `rechnung-report.xml` und mit `-h` zusätzlich `rechnung-report.html`. Version 1.6.3 vom 20.08.2026 enthält einen Sicherheitsfix; ältere Versionen sollten Sie nicht mehr nutzen.

Wann er passt: Wenn Java ohnehin installiert ist oder Sie einen Prüfdienst im Hintergrund brauchen (Daemon-Modus mit `-D`). Grenzen: Er prüft das XML, keine PDF/A-3-Hülle, und für ZUGFeRD BASIC und EXTENDED hat die Konfiguration kein eigenes Szenario.

## KoSIT-Visualisierung: XRechnung lesbar machen

Die KoSIT-Visualisierung wandelt eine XRechnung (UBL oder CII) in HTML oder, über Apache FOP, in PDF um. Sie besteht aus XSLT-2.0-Stylesheets und braucht deshalb einen Prozessor wie Saxon. Nehmen Sie die Version 2026-10-13: Sie behebt eine JavaScript-Injection über die Dateinamen von Anhängen (BT-122, BT-125).

Die KoSIT weist darauf hin, dass eine Visualisierung keine gültige XRechnung ist und nicht zur Archivierung dient. Das Original ist das XML. `erechnung anzeigen --offiziell` nutzt genau diese Stylesheets ohne Java:

```text
$ erechnung anzeigen beispiele/01_standard/xrechnung_cii.xml --offiziell -o ansicht.html
Ansicht geschrieben: ansicht.html
```

## Mustang und Quba: ZUGFeRD prüfen und anzeigen

Mustang ist eine Java-Bibliothek mit Kommandozeile für ZUGFeRD, Factur-X und XRechnung. Laut [Mustang-Dokumentation](https://www.mustangproject.org/commandline/) prüft `--action validate` das PDF (mit eingebautem veraPDF auf PDF/A-3) und das XML (Schema und Schematron). Weitere Aktionen sind `extract`, `combine` (PDF und XML zusammenführen), `visualize`, `pdf`, `a3only`, `ubl` (Factur-X nach UBL), `upgrade` und `metrics`. Mustang ist das passende Werkzeug, wenn Sie wissen müssen, ob ein ZUGFeRD-PDF formal PDF/A-3 ist.

Der Quba-Viewer ist ein Programm für Windows, macOS und Linux, das XRechnung (UBL und CII), ZUGFeRD/Factur-X und Order-X offline anzeigt. Er basiert auf den KoSIT-Stylesheets. Prüfen kann er optional über den Mustangserver; das ist ein Online-Dienst, die Rechnung verlässt dann den Rechner. Quba 2.0 mit Anzeigen, Prüfen und Erstellen ist laut Projekt angekündigt.

## Python-Bibliotheken für Entwickler

Für eigene Programme gibt es mehrere freie Python-Pakete. Sie erzeugen und lesen ZUGFeRD gut, prüfen aber die XRechnung-Regeln (BR-DE) nicht selbst:

- **drafthorse** (Apache-2.0): CII/ZUGFeRD erzeugen und parsen, XSD-Prüfung, XML in PDF einbetten. Kein UBL, keine Schematron-Prüfung.
- **factur-x** (BSD): Factur-X-PDF erzeugen und auslesen, CII und UBL aus einem Dict erzeugen, Schematron nur über einen externen Saxon-Server. Kein XRechnung-Profil.
- **pycheval** (Apache-2.0): Factur-X 1.08 lesen und schreiben bis Profil EN 16931, EXTENDED und XRechnung noch nicht.

Die offiziellen Regeln liegen nur als XSLT 2.0 vor, das lxml nicht ausführen kann. Wie `erechnung` das mit saxonche löst und welche API es hat, steht in [E-Rechnung mit Python](./e-rechnung-python.md).

## `erechnung`: lesen, prüfen, erstellen und DATEV in einem Werkzeug

`erechnung` ist eine Kommandozeile und Python-Bibliothek. Installation mit pipx (Python 3.10+, kein Java):

```bash
pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
```

Beim ersten Prüfen lädt es die KoSIT-Konfiguration von GitHub, prüft die SHA-256-Summe und legt sie in `~/.cache/erechnung` ab. Danach läuft alles offline, Rechnungsdaten verlassen den Rechner nicht.

| Aufgabe | Befehl |
| --- | --- |
| Rechnung lesen | `erechnung lesen DATEI` |
| Prüfen mit KoSIT-Regeln | `erechnung validieren DATEI...` (Exit-Code 0 gültig, 1 ungültig, 2 Prüfung nicht möglich) |
| Prüfbericht aufbewahren | `erechnung validieren DATEI --bericht ORDNER` |
| HTML-Ansicht | `erechnung anzeigen DATEI [--offiziell]` |
| E-Rechnung erstellen | `erechnung erstellen EINGABE.json --format xrechnung-ubl` |
| PDF zu ZUGFeRD | `erechnung zugferd XML --pdf RECHNUNG.pdf` |
| XML aus ZUGFeRD holen | `erechnung extrahieren PDF` |
| DATEV-Buchungsstapel | `erechnung datev DATEI... -o EXTF.csv` |
| Leitweg-ID prüfen | `erechnung leitweg-id ID` |

Grenzen: kein Versand (kein Peppol-Zugangspunkt, kein E-Mail-Versand), kein Archiv, keine PDF/A-Prüfung, keine Belegbilder für DATEV. ZUGFeRD BASIC und EXTENDED prüft es gegen die EN 16931 mit Hinweis. XRechnung 4.0 kommt laut KoSIT voraussichtlich im Frühjahr 2027 und wird noch nicht unterstützt.

## Online-Validatoren: bequem, aber mit Datenschutz-Abwägung

Viele private Anbieter bieten eine Upload-Seite zum Prüfen an, meist auf Basis des KoSIT-Validators oder von Mustang. Einen offiziellen öffentlichen Upload-Validator der KoSIT haben wir bei der Recherche nicht gefunden.

| Frage | Online-Validator | Lokales Werkzeug |
| --- | --- | --- |
| Installation | keine | einmal |
| Wo liegt die Rechnung? | auf dem Server des Anbieters | auf Ihrem Rechner |
| Welche Regelversion? | steht nicht immer dabei | im Prüfbericht (`regeln`) |
| Viele Dateien auf einmal | meist einzeln | ja |
| Prüfbericht zum Aufbewahren | je nach Anbieter | ja, mit SHA-256 der Datei |

Rechnungen enthalten Namen, Anschriften, Preise und Bankdaten Ihrer Geschäftspartner. Ob Sie sie bei einem Dritten hochladen dürfen, klären Sie mit Ihrer Datenschutzstelle. Für einzelne Testdateien ohne echte Daten ist ein Online-Validator unproblematisch.

## Staatliche Angebote

Für Rechnungen an die unmittelbare Bundesverwaltung ist die Plattform OZG-RE der Eingangskanal. Laut [FAQ von e-rechnung-bund.de](https://www.e-rechnung-bund.de/faq/) ist die Registrierung kostenlos, auch über "Mein Unternehmenskonto" (ELSTER). Kanäle sind Peppol, E-Mail, Upload und Weberfassung, die Grenzen liegen bei 10 MB per E-Mail und 11 MB in der Weberfassung. Rechnungen werden 28 Tage nach Bereitstellung gelöscht. Länder setzen die EU-Richtlinie 2014/55/EU in eigener Kompetenz um und haben eigene Regeln und Portale. Für Rechnungen zwischen Unternehmen ist OZG-RE nicht gedacht.

## Wann reicht ein kostenloses Werkzeug, wann eine Buchhaltungssoftware?

Ein kostenloses Werkzeug reicht, wenn Ihre Aufgabe klar umrissen ist. Eine Buchhaltungssoftware lohnt sich, wenn Rechnungen in Prozesse eingebunden sein müssen.

| Situation | Kostenloses Werkzeug reicht | Buchhaltungssoftware sinnvoll |
| --- | --- | --- |
| Eingangsrechnungen lesen und prüfen | ja | bei großem Volumen mit Freigabe-Workflow |
| Wenige Ausgangsrechnungen im Monat | ja, zum Beispiel aus einer JSON-Vorlage | bei vielen Rechnungen, Nummernkreisen und Kundenstamm |
| Versand an Behörden über Peppol | nein, ein Peppol-Zugang fehlt | ja, wenn sie Peppol anbietet |
| Offene Posten, Mahnwesen, Zahlungsabgleich | nein | ja |
| Aufbewahrung 8 Jahre (§ 14b Abs. 1 UStG) | Dateien selbst ablegen, Prüfbericht dazu | revisionssicheres Archiv |
| Übergabe an die Steuerberatung | Buchungsstapel als Vorschlag | direkte Schnittstelle mit Belegen |
| Eigene Software oder Shop anbinden | ja, Bibliothek oder Kommandozeile | je nach Schnittstelle |

Laut BMF-Schreiben vom 15.10.2025 (Rn. 60) ist die Speicherung außerhalb eines GoBD-konformen Systems allein umsatzsteuerlich kein Verstoß gegen § 14b UStG; die GoBD gelten trotzdem. Wie Sie archivieren, klären Sie mit der Steuerberatung. Mehr in [E-Rechnung archivieren](./e-rechnung-archivieren.md).

## Beispiele

Alle Befehle laufen in einem Ordner mit den Beispieldateien (`erechnung beispiele` schreibt sie, die ZUGFeRD-PDFs liegen im Repo unter `beispiele/`).

### Beispiel 1: Eingangsrechnung prüfen

```text
$ erechnung validieren beispiele/01_standard/xrechnung_ubl.xml beispiele/07_kleinunternehmer/zugferd_en16931.pdf
beispiele/01_standard/xrechnung_ubl.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
beispiele/07_kleinunternehmer/zugferd_en16931.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
```

Für jede eingehende E-Rechnung, bevor sie in die Buchhaltung geht.

### Beispiel 2: Erkennen, dass ein PDF keine E-Rechnung ist

```text
$ erechnung validieren scan.pdf
scan.pdf: unbekannt
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-LESEN: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
```

Für PDF-Rechnungen, bei denen unklar ist, ob ein XML enthalten ist. Der Exit-Code ist 2.

### Beispiel 3: ZUGFeRD-Rechnung kostenlos erstellen

```text
$ erechnung erstellen rechnung.json --format zugferd -o rechnung.pdf --validieren
rechnung.pdf: zugferd, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
  KoSIT: GÜLTIG (EN16931 (CII))
```

Für Ausgangsrechnungen ohne Rechnungsprogramm. `rechnung.json` ist eine Kopie von `beispiele/01_standard/eingabe.json`. Ohne `--pdf VORLAGE.pdf` erzeugt Ghostscript eine einfache PDF/A-3-Lesefassung; Ghostscript muss dafür installiert sein. Mehr in [E-Rechnung erstellen](./e-rechnung-erstellen.md).

### Beispiel 4: Prüfbericht zum Aufbewahren ablegen

```text
$ erechnung validieren rechnung.xml --bericht berichte
rechnung.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
  Prüfbericht: berichte/rechnung.xml.1e0e5c550373.validierungsbericht.json
```

Für die Ablage neben der Rechnung. Das BMF-Schreiben vom 15.10.2025 (Rn. 35a) empfiehlt, den Validierungsbericht aufzubewahren.

### Beispiel 5: Eingangsrechnungen als DATEV-Buchungsstapel

```text
$ erechnung datev beispiele/01_standard/xrechnung_ubl.xml beispiele/05_reverse_charge_13b/xrechnung_ubl.xml -o EXTF_Buchungsstapel.csv
EXTF_Buchungsstapel.csv: 2 Rechnungen, 2 Buchungszeilen (EXTF 700, SKR 03)
  Hinweis: RE-2026-0004: Kategorie AE: Steuer auf Eingangsseite selbst berechnen (BU-Schlüssel mit Steuerberatung festlegen).
```

Für die Übergabe an die Steuerberatung. Konten und BU-Schlüssel sind ein Vorschlag (Sammelkreditor 70000, Aufwandskonto SKR03 4980), Belegbilder enthält der Stapel nicht. Details in [DATEV und E-Rechnung](./datev-e-rechnung.md).

### Beispiel 6: XML aus einem ZUGFeRD-PDF holen

```text
$ erechnung extrahieren rechnung.pdf -o aus_pdf.xml
factur-x.xml aus rechnung.pdf gespeichert als aus_pdf.xml
```

Für Programme, die nur XML verarbeiten, oder für den Blick ins strukturierte Original.

## Schritt für Schritt: kostenlos E-Rechnungen prüfen und lesen

1. Python 3.10 oder neuer installieren (python.org oder Paketverwaltung), dazu `pipx`.
2. Im Terminal installieren: `pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"`.
3. Einmal die Prüfregeln laden: `erechnung konfiguration`. Die Ausgabe zeigt den Cache-Ordner.
4. Eingangsrechnung prüfen: `erechnung validieren rechnung.xml`. "GÜLTIG" heißt von den KoSIT-Regeln angenommen.
5. Rechnung lesbar machen: `erechnung anzeigen rechnung.xml -o rechnung.html` und die HTML-Datei im Browser öffnen.
6. Bei ZUGFeRD-PDFs funktionieren dieselben Befehle direkt mit der PDF-Datei.
7. Wer lieber ein Programm mit Fenster will, nimmt den Quba-Viewer zum Anzeigen und `erechnung` oder Mustang zum Prüfen.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| XRechnung per Doppelklick öffnen | Browser oder Editor zeigt nur XML-Code | Viewer nutzen: `erechnung anzeigen`, KoSIT-Visualisierung oder Quba |
| Ein PDF für eine E-Rechnung halten | `VP-LESEN`: kein eingebettetes Rechnungs-XML | Beim Absender XRechnung oder ZUGFeRD anfordern |
| Alte Version der KoSIT-Visualisierung | Sicherheitslücke über Anhang-Dateinamen | Version 2026-10-13 oder neuer verwenden |
| KoSIT-Validator ohne Java | Programm startet nicht | Java 11+ installieren oder `erechnung` ohne Java nutzen |
| Echte Rechnungen in Online-Validator laden | Daten liegen beim Anbieter | Lokal prüfen oder vorher mit der Datenschutzstelle klären |
| ZUGFeRD MINIMUM oder BASIC WL verschicken | Vorprüfung `VP-FORMAT`, keine E-Rechnung | Mindestens Profil BASIC, besser EN 16931 |

## Häufige Fragen

### Gibt es eine kostenlose Software für E-Rechnungen?

Ja. Zum Prüfen und Anzeigen gibt es den KoSIT-Validator, die KoSIT-Visualisierung, Mustang und den Quba-Viewer, zum Erstellen Mustang, Python-Bibliotheken und `erechnung`. Alle sind Open Source und kostenlos.

### Welches kostenlose Programm zeigt eine XRechnung an?

Der Quba-Viewer für Windows, macOS und Linux zeigt XRechnung und ZUGFeRD offline an. Auf der Kommandozeile macht `erechnung anzeigen rechnung.xml` eine HTML-Ansicht, mit `--offiziell` die der KoSIT.

### Brauche ich Java für die E-Rechnung?

Für den KoSIT-Validator und Mustang ja, Java 11 oder neuer. `erechnung` führt dieselben KoSIT-Regeln mit saxonche in Python aus und braucht kein Java.

### Ist eine kostenlose ZUGFeRD-Software genauso gültig wie eine gekaufte?

Ja, wenn die erzeugte Datei die Regeln erfüllt. Ob eine E-Rechnung gültig ist, hängt am Inhalt der Datei, nicht am Preis des Programms; prüfen Sie jede erzeugte Rechnung mit einem Validator.

### Darf ich E-Rechnungen mit einem Online-Validator prüfen?

Technisch ja. Weil Sie dabei Daten Ihrer Geschäftspartner an einen Dritten übermitteln, klären Sie das vorher mit Ihrer Datenschutzstelle. Lokale Werkzeuge vermeiden die Frage.

### Kann ich mit kostenloser Software E-Rechnungen an Behörden schicken?

Erstellen ja, zum Beispiel eine XRechnung mit Leitweg-ID. Für den Versand an die Bundesverwaltung ist OZG-RE kostenlos nutzbar (Upload, E-Mail, Weberfassung oder Peppol). Einen eigenen Peppol-Zugang bieten die hier genannten Werkzeuge nicht.

> **Hinweis:** Diese Anleitung erklärt Gesetz, BMF-Schreiben und technische Standards nach dem Stand vom 15.10.2026. Sie ist keine Steuer- oder Rechtsberatung, die Autoren sind keine Steuerberater. Für die Beurteilung eines konkreten Falls wenden Sie sich an Ihre Steuerberatung oder Ihr Finanzamt. Alle Angaben ohne Gewähr.

## Weiterlesen

- [E-Rechnung prüfen: XRechnung- und ZUGFeRD-Validator](./e-rechnung-validator.md)
- [E-Rechnung erstellen](./e-rechnung-erstellen.md)
- [E-Rechnung empfangen und lesen](./e-rechnung-empfangen.md)
- [E-Rechnung mit Python](./e-rechnung-python.md)
- [E-Rechnung aus Lexware, sevdesk, SAP und anderen Programmen prüfen](./e-rechnung-buchhaltungssoftware.md)
- [Beispiele im Repo](../../beispiele/README.md)
- Projekte: [KoSIT-Validator](https://github.com/itplr-kosit/validator), [KoSIT-Konfiguration XRechnung](https://github.com/itplr-kosit/validator-configuration-xrechnung), [KoSIT-Visualisierung](https://github.com/itplr-kosit/xrechnung-visualization), [Mustang](https://github.com/ZUGFeRD/mustangproject), [Quba-Viewer](https://github.com/ZUGFeRD/quba-viewer), [drafthorse](https://github.com/pretix/python-drafthorse), [factur-x](https://github.com/akretion/factur-x), [pycheval](https://github.com/zfutura/pycheval)
