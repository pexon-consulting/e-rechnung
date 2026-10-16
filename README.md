# E-Rechnung in Python: XRechnung und ZUGFeRD lesen, prüfen, erstellen und an DATEV übergeben

`e-rechnung` ist ein Open-Source-Werkzeug für die deutsche E-Rechnung: Es liest XRechnung (UBL und CII) und ZUGFeRD-PDFs, prüft sie mit den offiziellen KoSIT-Regeln ohne Java, erstellt gültige E-Rechnungen aus einer JSON-Datei, zeigt sie als lesbare HTML-Ansicht an und exportiert Eingangsrechnungen als DATEV-Buchungsstapel. Es läuft als Kommandozeile `erechnung`, als Python-Bibliothek und als MCP-Server für KI-Assistenten, und Rechnungsdaten verlassen dabei nie den eigenen Rechner. Dazu kommen 21 Anleitungen auf Deutsch, von der E-Rechnungspflicht bis zu den Fehlermeldungen der Validierung.

> Stand: 15.10.2026. XRechnung 3.0.2 (KoSIT-Konfiguration 2026-08-31), EN 16931, ZUGFeRD 2.5.2 / Factur-X 1.09.2, BMF-Schreiben vom 15.10.2025. MIT-Lizenz. Keine Steuerberatung. [English summary below](#english).

```bash
pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
erechnung validieren rechnung.xml
```

## Inhalt

- [Was ist eine E-Rechnung?](#was-ist-eine-e-rechnung)
- [E-Rechnung Pflicht: die Fristen auf einen Blick](#e-rechnung-pflicht-die-fristen-auf-einen-blick)
- [XRechnung oder ZUGFeRD?](#xrechnung-oder-zugferd)
- [Installation](#installation)
- [Schnellstart in sechs Befehlen](#schnellstart-in-sechs-befehlen)
- [E-Rechnung prüfen: offizielle KoSIT-Regeln ohne Java](#e-rechnung-prüfen-offizielle-kosit-regeln-ohne-java)
- [E-Rechnung erstellen: XRechnung und ZUGFeRD aus JSON](#e-rechnung-erstellen-xrechnung-und-zugferd-aus-json)
- [E-Rechnung lesen und anzeigen (Viewer)](#e-rechnung-lesen-und-anzeigen-viewer)
- [DATEV: Eingangsrechnungen als Buchungsstapel](#datev-eingangsrechnungen-als-buchungsstapel)
- [Leitweg-ID prüfen](#leitweg-id-prüfen)
- [Python-API](#python-api)
- [MCP-Server für Claude, Cursor und andere KI-Assistenten](#mcp-server-für-claude-cursor-und-andere-ki-assistenten)
- [Beispieldateien](#beispieldateien)
- [Alle Anleitungen](#alle-anleitungen)
- [Vergleich mit anderen Werkzeugen](#vergleich-mit-anderen-werkzeugen)
- [Was das Werkzeug nicht macht](#was-das-werkzeug-nicht-macht)
- [Häufige Fragen zur E-Rechnung (FAQ)](#häufige-fragen-zur-e-rechnung-faq)
- [E-Rechnung tools for Python (English)](#english)
- [Mitmachen, Lizenz und Quellen](#mitmachen-lizenz-und-quellen)

## Was ist eine E-Rechnung?

Eine E-Rechnung ist nach § 14 Abs. 1 UStG eine Rechnung, die in einem strukturierten elektronischen Format ausgestellt, übermittelt und empfangen wird und eine elektronische Verarbeitung ermöglicht. In Deutschland heißt das praktisch: ein XML-Datensatz nach der europäischen Norm EN 16931, also eine XRechnung oder eine ZUGFeRD-Rechnung ab Version 2.0.1 mit einem der Profile BASIC, EN 16931, EXTENDED oder XRECHNUNG.

Ein PDF, das per Mail kommt, ist keine E-Rechnung, sondern eine "sonstige Rechnung". Das gilt auch für ZUGFeRD-PDFs mit den Profilen MINIMUM und BASIC WL (UStAE 14.1 Abs. 14). Bei einer Hybridrechnung (PDF mit eingebettetem XML) gilt der strukturierte Teil: Weichen PDF und XML voneinander ab, ist das XML maßgeblich.

Mehr dazu: [Was ist eine E-Rechnung?](docs/anleitungen/was-ist-eine-e-rechnung.md)

## E-Rechnung Pflicht: die Fristen auf einen Blick

Seit dem 01.01.2025 müssen alle inländischen Unternehmen E-Rechnungen empfangen können, ohne Ausnahme, also auch Kleinunternehmer und Vermieter. Ein normales E-Mail-Postfach reicht dafür. Für das Ausstellen gelten Übergangsfristen nach § 27 Abs. 38 UStG:

| Umsatz ausgeführt | Was statt einer E-Rechnung noch zulässig ist |
| --- | --- |
| 01.01.2025 - 31.12.2026 | Papierrechnung immer, PDF und andere elektronische Formate mit Zustimmung des Empfängers |
| 01.01.2027 - 31.12.2027 | Papier oder (mit Zustimmung) PDF nur, wenn der Gesamtumsatz des Ausstellers im Vorjahr höchstens 800.000 EUR betrug; EDI-Verfahren mit Zustimmung unabhängig vom Umsatz |
| ab 01.01.2028 | E-Rechnung für alle inländischen B2B-Umsätze |

Ausgenommen bleiben Kleinbetragsrechnungen bis 250 EUR brutto, Fahrausweise und Rechnungen von Kleinunternehmern. Rechnungen an Privatpersonen (B2C) sind nicht betroffen. Für Rechnungen an Bundesbehörden gilt schon seit dem 27.11.2020 die E-Rechnungsverordnung (XRechnung mit Leitweg-ID).

Mehr dazu: [E-Rechnung Pflicht](docs/anleitungen/e-rechnung-pflicht.md), [Kleinunternehmer](docs/anleitungen/e-rechnung-kleinunternehmer.md), [BMF-Schreiben erklärt](docs/anleitungen/bmf-schreiben-e-rechnung.md)

## XRechnung oder ZUGFeRD?

| | XRechnung | ZUGFeRD / Factur-X |
| --- | --- | --- |
| Was es ist | reines XML, deutscher Standard (CIUS der EN 16931) der KoSIT | PDF/A-3 mit eingebettetem XML (CII), deutsch-französischer Standard |
| Syntax | UBL 2.1 oder UN/CEFACT CII D16B | CII |
| Für Menschen lesbar | nur mit Viewer | ja, das PDF |
| E-Rechnung nach UStG | ja | ab 2.0.1 mit BASIC, EN 16931, EXTENDED, XRECHNUNG |
| An Behörden | Standard (mit Leitweg-ID in BT-10) | nur mit Profil XRECHNUNG, wenn die Stelle es annimmt |
| Mit diesem Werkzeug | `erechnung erstellen --format xrechnung-ubl` | `erechnung erstellen --format zugferd` |

Mehr dazu: [XRechnung oder ZUGFeRD](docs/anleitungen/xrechnung-oder-zugferd.md), [XRechnung erklärt](docs/anleitungen/xrechnung.md), [ZUGFeRD erklärt](docs/anleitungen/zugferd.md)

## Installation

Python 3.10 oder neuer, kein Java. Das Paket liegt auf GitHub:

```bash
# als eigenständiges Programm
pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"

# ohne Installation, einmalig
uvx --from "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0" erechnung validieren rechnung.xml

# in einem Python-Projekt
pip install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
```

| Extra | Was es dazu bringt |
| --- | --- |
| `offiziell` | saxonche (MPL-2.0) für die offiziellen KoSIT-Regeln und die KoSIT-Ansicht. Ohne läuft nur die Vorprüfung. |
| `mcp` | den MCP-Server `erechnung-mcp` (enthält `offiziell`) |
| `toml` | TOML-Eingabe unter Python 3.10 |

Für ZUGFeRD-PDFs ohne eigene Vorlage braucht `erechnung erstellen` zusätzlich [Ghostscript](https://www.ghostscript.com/) (`brew install ghostscript`, `apt install ghostscript`). Wer ein eigenes Rechnungs-PDF hat, braucht es nicht.

## Schnellstart in sechs Befehlen

```bash
erechnung beispiele bsp                                   # 9 Beispielrechnungen als JSON, UBL und CII
erechnung lesen bsp/02_gemischte_steuersaetze_xrechnung_cii.xml
erechnung validieren bsp/08_b2g_leitweg_id_xrechnung_ubl.xml
erechnung erstellen bsp/01_standard.json --format zugferd -o rechnung.pdf
erechnung anzeigen rechnung.pdf -o rechnung.html
erechnung datev bsp/*_ubl.xml --skr 04 -o EXTF_Buchungsstapel.csv
```

So sieht `erechnung lesen` aus:

```text
Datei:        bsp/02_gemischte_steuersaetze_xrechnung_cii.xml
Format:       XRechnung 3.0 (CII)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
Nummer:       RE-2026-0002 vom 15.10.2026
Verkäufer:    Buchhandlung am Markt GmbH, 20095 Hamburg, USt-IdNr. DE123456789
Käufer:       Beispiel Handel AG, 80331 München
Käuferref.:   BH-2026-0815
Positionen:   3
     1         3 C62  Fachbuch Umsatzsteuer 2026                           149,70 EUR
     2         2 C62  E-Book Reader Hülle                                   39,98 EUR
     3         1 LS   Versandkostenpauschale                                 4,90 EUR
USt:          S (Regelsteuersatz oder ermäßigter Satz) 7 %: 10,48 EUR auf 149,70 EUR
USt:          S (Regelsteuersatz oder ermäßigter Satz) 19 %: 7,58 EUR auf 39,88 EUR
Netto:        189,58 EUR
Brutto:       207,64 EUR
Zahlbetrag:   207,64 EUR, fällig 14.11.2026
Zahlung:      58 (SEPA-Überweisung) DE79000000001234567890
```

## E-Rechnung prüfen: offizielle KoSIT-Regeln ohne Java

`erechnung validieren` prüft eine XRechnung oder ZUGFeRD-Rechnung mit denselben Regeln wie der offizielle KoSIT-Validator: erst gegen das XML-Schema (UBL 2.1 oder CII D16B), dann gegen die Schematron-Regeln der EN 16931 und der XRechnung (BR-DE). Szenario-Auswahl und Umstufungen von Fehlern zu Warnungen übernimmt es aus der KoSIT-Konfiguration. Auf 222 Dateien (alle 86 der KoSIT-Testsuite, alle 18 Beispiele und 118 absichtlich kaputte Varianten, von denen KoSIT 100 ablehnt) kommt es zum selben Ergebnis wie der Java-Validator 1.6.3, Regel für Regel. Der Abgleich läuft in der CI mit ([scripts/abgleich_kosit.py](scripts/abgleich_kosit.py)).

```text
$ erechnung validieren rechnung.xml
rechnung.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-DE-15: [BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BR-DE-15: Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.
```

| Option | Wirkung |
| --- | --- |
| `--json` | Ergebnis als JSON, für Skripte und CI |
| `--bericht ORDNER` | Prüfbericht je Datei als JSON mit Zeitpunkt, Regelversion und SHA-256 der Datei ablegen |
| `--streng` | Warnungen zählen als Fehler |
| `--offline` | nur den lokalen Cache der Prüfregeln nutzen |
| `--ohne-offiziell` | nur die Vorprüfung, ohne KoSIT-Regeln |
| `--alle` | auch Informationen ausgeben |

Exit-Code 0 heißt gültig, 1 ungültig, 2 Prüfung nicht möglich. Die Prüfregeln (Apache-2.0) lädt das Werkzeug beim ersten Aufruf von GitHub, prüft die SHA-256-Summe und speichert sie in `~/.cache/erechnung`. Danach läuft alles offline. Rechner ohne Internet bekommen die Datei über `ERECHNUNG_KOSIT_KONFIG=/pfad/xrechnung-3.0.2-validator-configuration-2026-08-31.zip`.

Der Prüfbericht hat einen umsatzsteuerlichen Zweck: Laut BMF-Schreiben vom 15.10.2025 (Rn. 35a) darf sich ein Unternehmen mit der Sorgfalt eines ordentlichen Kaufmanns auf das Ergebnis einer geeigneten Validierung verlassen, und das BMF empfiehlt, den Validierungsbericht aufzubewahren.

Mehr dazu: [E-Rechnung prüfen](docs/anleitungen/e-rechnung-validator.md), [Fehlermeldungen beheben](docs/anleitungen/e-rechnung-fehlermeldungen.md)

## E-Rechnung erstellen: XRechnung und ZUGFeRD aus JSON

Die Eingabe ist eine JSON- oder TOML-Datei mit den Rechnungsdaten. Summen, Steuern je Steuersatz und Zahlbetrag rechnet das Werkzeug selbst (kaufmännisch gerundet je Steuergruppe).

```json
{
  "nummer": "RE-2026-0100",
  "datum": "2026-10-15",
  "leitweg_id": "BH-2026-0815",
  "verkaeufer": {
    "name": "Muster IT GmbH",
    "adresse": {"strasse": "Musterstraße 1", "plz": "20095", "ort": "Hamburg", "land": "DE"},
    "ust_id": "DE123456789",
    "elektronische_adresse": "rechnung@example.com",
    "kontakt": {"name": "Erika Muster", "telefon": "+49 40 123456", "email": "erika@example.com"}
  },
  "kaeufer": {
    "name": "Beispiel Handel AG",
    "adresse": {"strasse": "Hauptstraße 5", "plz": "80331", "ort": "München", "land": "DE"},
    "elektronische_adresse": "eingang@example.com"
  },
  "lieferung": {"datum": "2026-10-10"},
  "zahlung": {"art": "58", "iban": "DE79000000001234567890"},
  "positionen": [
    {"id": "1", "name": "Beratung", "menge": "8", "einheit": "HUR", "preis": "120.00"}
  ]
}
```

```bash
erechnung erstellen rechnung.json --validieren                         # XRechnung UBL
erechnung erstellen rechnung.json --format xrechnung-cii -o rechnung.xml
erechnung erstellen rechnung.json --format zugferd -o rechnung.pdf     # PDF/A-3 mit factur-x.xml
erechnung erstellen rechnung.json --format zugferd --pdf mein_layout.pdf -o rechnung.pdf
erechnung zugferd rechnung_cii.xml --pdf vorhandene_rechnung.pdf       # PDF zu ZUGFeRD
```

Formate: `xrechnung-ubl`, `xrechnung-cii`, `en16931-ubl`, `en16931-cii`, `zugferd` (Profil EN 16931) und `zugferd-xrechnung` (Profil XRECHNUNG, eingebettet als `xrechnung.xml`). Die erzeugten ZUGFeRD-PDFs bestehen die Prüfung mit [Mustang](https://www.mustangproject.org/) (PDF/A-3b und XML), auch das läuft in der CI.

Mehr dazu: [E-Rechnung erstellen](docs/anleitungen/e-rechnung-erstellen.md), [PDF in ZUGFeRD umwandeln](docs/anleitungen/pdf-in-zugferd-umwandeln.md), [Gutschrift, Korrektur und Reverse Charge](docs/anleitungen/e-rechnung-gutschrift-korrektur.md)

## E-Rechnung lesen und anzeigen (Viewer)

Eine XRechnung ist reines XML. Mit einem Doppelklick sieht man nur Code. `erechnung anzeigen` macht daraus eine HTML-Seite mit Parteien, Positionen, Steuern und Zahlungsdaten, `--offiziell` nutzt stattdessen die offizielle KoSIT-Visualisierung (Version 2026-10-13). Bei ZUGFeRD-PDFs liest das Werkzeug das eingebettete XML, denn das ist der maßgebliche Teil.

```bash
erechnung anzeigen eingang.xml                    # schreibt eingang.html
erechnung anzeigen eingang.xml --offiziell -o kosit.html
erechnung lesen eingang.pdf --json                # alle Felder als JSON
erechnung extrahieren eingang.pdf -o eingang.xml  # XML aus dem ZUGFeRD-PDF holen
```

Mehr dazu: [E-Rechnung empfangen und lesen](docs/anleitungen/e-rechnung-empfangen.md), [E-Rechnung archivieren](docs/anleitungen/e-rechnung-archivieren.md)

## DATEV: Eingangsrechnungen als Buchungsstapel

`erechnung datev` schreibt aus beliebig vielen E-Rechnungen einen DATEV-Buchungsstapel im Format EXTF (Version 700, Kategorie 21, Formatversion 13, Windows-1252, 125 Spalten). Je Rechnung und Steuersatz entsteht eine Zeile mit Bruttobetrag, Kreditor, Aufwandskonto, BU-Schlüssel, Belegdatum, Rechnungsnummer und Leistungsdatum.

```text
$ erechnung datev eingang/*.xml --skr 04 --kreditoren kreditoren.json -o EXTF_Buchungsstapel.csv
EXTF_Buchungsstapel.csv: 2 Rechnungen, 3 Buchungszeilen (EXTF 700, SKR 04)
```

Standard: Sammelkreditor 70000, Aufwandskonto 4980 (SKR03) bzw. 6850 (SKR04), BU-Schlüssel 9 für 19 % und 8 für 7 %. Kreditoren ordnet `--kreditoren` über USt-IdNr. oder Namen zu. Der Stapel ist ein Importvorschlag: Konten und Steuerschlüssel prüft die Buchhaltung, bei Reverse Charge und innergemeinschaftlichem Erwerb gibt das Werkzeug einen Hinweis aus.

Mehr dazu: [DATEV und E-Rechnung](docs/anleitungen/datev-e-rechnung.md)

## Leitweg-ID prüfen

Rechnungen an Behörden brauchen die Leitweg-ID des Auftraggebers in BT-10. Ihre letzten zwei Ziffern sind eine Prüfziffer nach ISO/IEC 7064 Mod 97-10 (Leitweg-ID-Formatspezifikation 2.0.2).

```text
$ erechnung leitweg-id 04011000-1234512345-07 04011000-1234512345
04011000-1234512345-07: Prüfziffer falsch, richtig wäre 04011000-1234512345-06
04011000-1234512345: ohne Prüfziffer, vollständig: 04011000-1234512345-06
```

Mehr dazu: [Leitweg-ID und E-Rechnung an Behörden](docs/anleitungen/leitweg-id.md)

## Python-API

```python
from erechnung import laden, lesen, ubl, cii, validieren

rechnung = laden("rechnung.json")         # JSON oder TOML
xml = ubl(rechnung)                        # oder cii(rechnung)
ergebnis = validieren(xml)                 # Pfad, Datei oder Bytes
print(ergebnis.gueltig)                    # True
print([b.code for b in ergebnis.offiziell.fehler])

eingang = lesen("eingang.pdf")             # XRechnung oder ZUGFeRD-PDF
print(eingang.nummer, eingang.summen.zahlbetrag)
```

Weitere Module: `erechnung.pdf` (einbetten und auslesen), `erechnung.datev` (Buchungsstapel), `erechnung.anzeigen` (HTML), `erechnung.offiziell` (KoSIT-Regeln und KoSIT-Ansicht). Die Saxon-Aufrufe laufen auf einem eigenen Thread, damit ist die Bibliothek auch aus Web-Servern und Worker-Threads heraus nutzbar.

Mehr dazu: [E-Rechnung mit Python](docs/anleitungen/e-rechnung-python.md)

## MCP-Server für Claude, Cursor und andere KI-Assistenten

`erechnung-mcp` stellt die Funktionen als MCP-Werkzeuge bereit: `erechnung_lesen`, `erechnung_validieren`, `erechnung_anzeigen`, `erechnung_erstellen`, `erechnung_datev` und `erechnung_leitweg_id`. Der Server läuft lokal und arbeitet mit lokalen Dateien. Was das Sprachmodell zu sehen bekommt, sind die Antworten der Werkzeuge.

```json
{
  "mcpServers": {
    "e-rechnung": {
      "command": "uvx",
      "args": ["--from", "e-rechnung[mcp] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0", "erechnung-mcp"]
    }
  }
}
```

Mehr dazu: [E-Rechnung mit KI prüfen](docs/anleitungen/e-rechnung-ki-mcp.md)

### Skills für Claude Code und Codex

Im Ordner [`skills/`](skills/) liegen drei Skills, die einem Coding-Agenten den Ablauf beibringen: [E-Rechnung validieren](skills/e-rechnung-validieren/SKILL.md), [E-Rechnung erstellen](skills/e-rechnung-erstellen/SKILL.md) und [E-Rechnungen an DATEV übergeben](skills/e-rechnung-datev/SKILL.md). Für Claude Code kopieren Sie einen Ordner nach `~/.claude/skills/` oder `.claude/skills/` im Projekt.

## Beispieldateien

Im Ordner [beispiele/](beispiele/README.md) liegen neun Fälle, je als JSON-Eingabe, XRechnung UBL, XRechnung CII, HTML-Ansicht und mit dem Ergebnis der offiziellen Prüfung. Drei Fälle gibt es zusätzlich als ZUGFeRD-PDF, dazu einen DATEV-Buchungsstapel über alle Fälle. Alle sind gegen die KoSIT-Regeln geprüft, und die CI stellt sicher, dass sie zum Code passen.

| Fall | Was er zeigt |
| --- | --- |
| [01 Standardrechnung](beispiele/01_standard/) | Leistungszeitraum, 19 %, Skonto, SEPA-Überweisung |
| [02 Gemischte Steuersätze](beispiele/02_gemischte_steuersaetze/) | 7 % und 19 % in einer Rechnung, Nachlass |
| [03 Gutschrift](beispiele/03_gutschrift/) | Rechnungsart 381, in UBL als CreditNote |
| [04 Rechnungskorrektur](beispiele/04_rechnungskorrektur/) | Rechnungsart 384 mit Bezug auf die Ursprungsrechnung |
| [05 Reverse Charge](beispiele/05_reverse_charge_13b/) | § 13b UStG, Steuerkategorie AE |
| [06 Innergemeinschaftliche Lieferung](beispiele/06_innergemeinschaftlich/) | Steuerkategorie K, Käufer in Österreich |
| [07 Kleinunternehmer](beispiele/07_kleinunternehmer/) | § 19 UStG, Steuerkategorie E |
| [08 Rechnung an eine Behörde](beispiele/08_b2g_leitweg_id/) | Leitweg-ID in BT-10 und als elektronische Adresse |
| [09 SEPA-Lastschrift](beispiele/09_sepa_lastschrift/) | Zahlungsart 59 mit Mandat und Gläubiger-ID |

Mehr dazu: [E-Rechnung Beispiel](docs/anleitungen/e-rechnung-beispiel.md)

## Alle Anleitungen

| Thema | Anleitung |
| --- | --- |
| Grundlagen | [Was ist eine E-Rechnung?](docs/anleitungen/was-ist-eine-e-rechnung.md) |
| Recht | [E-Rechnung Pflicht: ab wann, für wen, Übergangsfristen](docs/anleitungen/e-rechnung-pflicht.md) |
| Recht | [BMF-Schreiben zur E-Rechnung erklärt](docs/anleitungen/bmf-schreiben-e-rechnung.md) |
| Recht | [E-Rechnung für Kleinunternehmer](docs/anleitungen/e-rechnung-kleinunternehmer.md) |
| Recht | [E-Rechnung archivieren: Aufbewahrung, GoBD, Prüfbericht](docs/anleitungen/e-rechnung-archivieren.md) |
| Formate | [XRechnung: Format, Aufbau, Pflichtfelder](docs/anleitungen/xrechnung.md) |
| Formate | [ZUGFeRD: Format, Profile, Versionen](docs/anleitungen/zugferd.md) |
| Formate | [XRechnung oder ZUGFeRD](docs/anleitungen/xrechnung-oder-zugferd.md) |
| Formate | [E-Rechnung Beispiel: Beispieldateien](docs/anleitungen/e-rechnung-beispiel.md) |
| Erstellen | [E-Rechnung erstellen (kostenlos)](docs/anleitungen/e-rechnung-erstellen.md) |
| Erstellen | [PDF in ZUGFeRD umwandeln](docs/anleitungen/pdf-in-zugferd-umwandeln.md) |
| Erstellen | [Gutschrift, Rechnungskorrektur und Reverse Charge](docs/anleitungen/e-rechnung-gutschrift-korrektur.md) |
| Erstellen | [Leitweg-ID und E-Rechnung an Behörden](docs/anleitungen/leitweg-id.md) |
| Prüfen | [E-Rechnung prüfen: XRechnung- und ZUGFeRD-Validator](docs/anleitungen/e-rechnung-validator.md) |
| Prüfen | [Fehlermeldungen: BR-DE-15, BR-CO-26 und andere](docs/anleitungen/e-rechnung-fehlermeldungen.md) |
| Prüfen | [E-Rechnung aus Lexware, sevdesk, SAP prüfen](docs/anleitungen/e-rechnung-buchhaltungssoftware.md) |
| Empfangen | [E-Rechnung empfangen und lesen (Viewer)](docs/anleitungen/e-rechnung-empfangen.md) |
| Buchhaltung | [DATEV und E-Rechnung](docs/anleitungen/datev-e-rechnung.md) |
| Werkzeuge | [E-Rechnung Software kostenlos (Open Source)](docs/anleitungen/e-rechnung-software-kostenlos.md) |
| Werkzeuge | [E-Rechnung mit Python](docs/anleitungen/e-rechnung-python.md) |
| Werkzeuge | [E-Rechnung mit KI prüfen (MCP)](docs/anleitungen/e-rechnung-ki-mcp.md) |

## Vergleich mit anderen Werkzeugen

| | e-rechnung | KoSIT-Validator | Mustang | factur-x (Python) | drafthorse (Python) |
| --- | --- | --- | --- | --- | --- |
| XRechnung UBL erzeugen | ja | nein | über Umwandlung aus Factur-X | nur als EN 16931 | nein |
| XRechnung CII erzeugen | ja | nein | ja | nur als EN 16931 | ja |
| ZUGFeRD-PDF erzeugen | ja | nein | ja | ja | ja |
| Offizielle XRechnung-Regeln (BR-DE) | ja, ohne Java | ja | ja | nein | nein |
| PDF/A-3 prüfen | nein | nein | ja | nein | nein |
| HTML-Ansicht | ja, auch KoSIT | nein | ja | nein | nein |
| DATEV-Buchungsstapel | ja | nein | nein | nein | nein |
| MCP-Server | ja | nein | nein | nein | nein |
| Sprache | Python | Java | Java | Python | Python |

Stand der anderen Projekte: Herstellerangaben und Code vom 15.10.2026. Details in [E-Rechnung Software kostenlos](docs/anleitungen/e-rechnung-software-kostenlos.md).

## Was das Werkzeug nicht macht

- **Kein Versand.** Kein Peppol-Zugangspunkt, kein Mailversand, keine Anbindung an OZG-RE.
- **Kein Archiv.** Es legt Prüfberichte ab, ein revisionssicheres Archiv ersetzt es nicht.
- **Keine PDF/A-Prüfung.** Ob ein fremdes PDF PDF/A-3 erfüllt, prüft Mustang oder veraPDF.
- **ZUGFeRD BASIC und EXTENDED** prüft es gegen die EN-16931-Regeln (mit Hinweis), weil die KoSIT-Konfiguration dafür kein eigenes Szenario hat.
- **XRechnung 4.0** kommt laut KoSIT im Frühjahr 2027. Bis dahin gilt 3.0.2.
- **Keine Steuerberatung.** Das Werkzeug prüft Format und Regeln, nicht, ob ein Vorgang steuerlich richtig behandelt ist.

## Häufige Fragen zur E-Rechnung (FAQ)

### Ist eine PDF-Rechnung eine E-Rechnung?

Nein. Ein PDF ohne eingebettete strukturierte Daten ist eine sonstige Rechnung (UStAE 14.1 Abs. 2). Bis Ende 2026 darf man sie mit Zustimmung des Empfängers weiter verschicken, 2027 nur noch bei höchstens 800.000 EUR Vorjahresumsatz, ab 2028 nicht mehr im inländischen B2B.

### Ab wann muss ich E-Rechnungen empfangen können?

Seit dem 01.01.2025, und zwar jedes inländische Unternehmen, auch Kleinunternehmer. Eine E-Mail-Adresse reicht, um E-Rechnungen zu empfangen. Zum Lesen braucht man einen Viewer, etwa `erechnung anzeigen`.

### Wie prüfe ich kostenlos, ob eine XRechnung gültig ist?

Mit `erechnung validieren rechnung.xml`. Das Werkzeug wendet die offiziellen KoSIT-Regeln lokal an, ohne die Rechnung hochzuladen. Exit-Code 0 heißt gültig.

### Was bedeutet die Fehlermeldung BR-DE-15?

Die Käuferreferenz BT-10 fehlt. In einer XRechnung ist sie Pflicht, bei Behörden steht dort die Leitweg-ID, im B2B genügt laut BMF auch ein Platzhalter wie "-". Laut BMF-Schreiben vom 15.10.2025 (Rn. 35a) ist dieser Geschäftsregelfehler umsatzsteuerlich unbeachtlich, die Datei ist aber keine gültige XRechnung. Weitere Codes: [Fehlermeldungen](docs/anleitungen/e-rechnung-fehlermeldungen.md).

### Brauche ich Java für die XRechnung-Validierung?

Nein. Die KoSIT-Regeln liegen als XSLT 2.0 vor, das Werkzeug führt sie mit saxonche direkt in Python aus und kommt dabei zu denselben Ergebnissen wie der Java-Validator.

### Kann ich mit dem Werkzeug E-Rechnungen verschicken?

Nein, es erzeugt die Datei. Verschicken kann man sie per E-Mail, über ein Portal oder über Peppol. Die unmittelbare Bundesverwaltung nimmt sie ausschließlich über die OZG-RE an.

### Wie lange muss ich E-Rechnungen aufbewahren?

Acht Jahre (§ 14b Abs. 1 UStG, BMF-Schreiben vom 15.10.2025, Rn. 60), mindestens den strukturierten Teil unverändert im empfangenen Format. Der Prüfbericht von `--bericht` gehört sinnvollerweise dazu.

### Funktioniert der DATEV-Export mit DATEV Unternehmen online?

Der Buchungsstapel ist eine EXTF-Datei für den Import in DATEV Rechnungswesen. Belegbilder überträgt das Werkzeug nicht. Wer Belege in Unternehmen online hat, verknüpft sie dort. Siehe [DATEV und E-Rechnung](docs/anleitungen/datev-e-rechnung.md).

<a id="english"></a>

## E-Rechnung tools for Python (English)

`e-rechnung` is an open-source Python package and CLI for German e-invoicing. It reads XRechnung (UBL 2.1 and UN/CEFACT CII D16B) and ZUGFeRD/Factur-X PDFs, validates them against the official KoSIT rules **without Java** (identical results to the KoSIT validator 1.6.3 on all 222 test files), generates valid XRechnung and ZUGFeRD invoices (PDF/A-3, checked with Mustang), renders them as HTML (own viewer or the official KoSIT visualization), exports incoming invoices as a DATEV booking batch (EXTF) and checks Leitweg-IDs. It ships an MCP server for AI assistants. Invoice data never leaves your machine; only the KoSIT rule files are downloaded once (SHA-256 pinned).

```bash
pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
erechnung validieren invoice.xml        # alias: erechnung check
erechnung erstellen invoice.json --format zugferd -o invoice.pdf
```

Commands are German: `lesen` (read), `validieren` (validate), `anzeigen` (view), `erstellen` (create), `extrahieren` (extract), `datev`, `leitweg-id`, `beispiele` (examples). The Python API: `from erechnung import laden, lesen, ubl, cii, validieren`. Covered standards: EN 16931, XRechnung 3.0.2 (UBL and CII), ZUGFeRD 2.x / Factur-X in CII D16B (profiles EN 16931 and XRECHNUNG for output, all profiles for reading).

## Mitmachen, Lizenz und Quellen

Fehler in einer Anleitung, eine Rechnung, die anders geprüft wird als vom KoSIT-Validator, ein neuer Sonderfall: Issues und Pull Requests sind willkommen. Wie Tests und der Abgleich mit Java laufen, steht in [CONTRIBUTING.md](CONTRIBUTING.md). Sicherheitslücken bitte wie in [SECURITY.md](SECURITY.md) beschrieben melden.

```bash
git clone https://github.com/pexon-consulting/e-rechnung
cd e-rechnung
python3 -m venv .venv && .venv/bin/pip install -e ".[dev,mcp]"
.venv/bin/pytest -q
```

Lizenz: [MIT](LICENSE). Die KoSIT-Prüfregeln, die KoSIT-Visualisierung und die Testsuite stehen unter Apache-2.0, die enthaltenen CEN-Schematron-Regeln unter EUPL-1.2. Sie werden nicht mitgeliefert, sondern beim ersten Aufruf geladen, siehe [NOTICE](NOTICE). Änderungen: [CHANGELOG.md](CHANGELOG.md).

Primärquellen: [§ 14 UStG](https://www.gesetze-im-internet.de/ustg_1980/__14.html), [§ 27 UStG](https://www.gesetze-im-internet.de/ustg_1980/__27.html), [BMF-FAQ zur E-Rechnung](https://www.bundesfinanzministerium.de/Content/DE/FAQ/e-rechnung.html), [XRechnung bei xeinkauf.de](https://xeinkauf.de/xrechnung/), [KoSIT-Validator](https://github.com/itplr-kosit/validator), [ZUGFeRD bei FeRD](https://www.ferd-net.de/standards/zugferd).

### Haftungsausschluss

- **Keine Steuer- oder Rechtsberatung.** Die Anleitungen und das Werkzeug erklären Gesetz, BMF-Schreiben und technische Standards nach dem genannten Stand. Die Autoren sind keine Steuerberater und keine Rechtsanwälte. Ob ein Vorgang steuerlich richtig behandelt ist, klären Sie mit Ihrer Steuerberatung oder Ihrem Finanzamt.
- **Keine Gewähr.** Die Software steht unter der MIT-Lizenz und wird ohne jede Gewährleistung bereitgestellt. Ein Ergebnis "gültig" bedeutet, dass die Datei die offiziellen Formatregeln erfüllt, nicht, dass die Rechnung inhaltlich oder steuerlich richtig ist.
- **Kein Ersatz für die Prüfung beim Empfänger.** Rechnungsplattformen von Bund und Ländern und die Systeme Ihrer Kunden können zusätzliche Regeln anwenden.
- **DATEV-Buchungsvorschläge** (Konten, BU-Schlüssel) sind Vorschläge und müssen vor dem Import von der Buchhaltung oder Steuerberatung freigegeben werden.
- **Rechtsstand und Versionen ändern sich.** Prüfen Sie bei wichtigen Entscheidungen die verlinkten Primärquellen.

Dieses Projekt ist unabhängig und nicht mit der KoSIT, dem FeRD oder der DATEV eG verbunden. XRechnung, ZUGFeRD und DATEV sind Marken ihrer jeweiligen Inhaber.

Gepflegt von Pexon Consulting. Wer den Rechnungseingang von der E-Rechnung bis zur Buchung automatisieren will, findet bei uns [Rechnungseingang automatisieren mit KI](https://pexon-consulting.de/ki-beratung/ai-workflows/n8n-rechnungseingang-automatisierung-ki/).
