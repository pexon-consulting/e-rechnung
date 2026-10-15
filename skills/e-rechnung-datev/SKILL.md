---
name: e-rechnung-datev
description: Wandelt eingegangene E-Rechnungen (XRechnung, ZUGFeRD) in einen DATEV-Buchungsstapel (EXTF, SKR03 oder SKR04) für den Import in DATEV Rechnungswesen oder die Weitergabe an die Steuerberatung. Verwenden, wenn Eingangsrechnungen gesammelt an DATEV übergeben, Konten vorgeschlagen oder ein Buchungsstapel kontrolliert werden soll.
---

# E-Rechnungen an DATEV übergeben

Werkzeug: `erechnung` aus https://github.com/pexon-consulting/e-rechnung.

## Ablauf

1. Alle Rechnungen zuerst validieren. Nur gültige Dateien übernehmen:
   `erechnung validieren eingang/*.xml eingang/*.pdf`
2. Buchungsstapel erzeugen:
   ```bash
   erechnung datev eingang/*.xml eingang/*.pdf -o EXTF_Buchungsstapel.csv --skr 03 --kreditor 70000
   ```
   Für SKR04 `--skr 04`. Berater- und Mandantennummer mit `--berater` und `--mandant`, sie müssen zum Mandanten in DATEV passen.
3. Datei in DATEV Rechnungswesen über "Stapelverarbeitung" importieren oder der Steuerberatung schicken. Die Original-XML gehört zum Beleg und muss mit archiviert werden.

## Was im Stapel steht

- Eine Buchungszeile je Rechnung und Steuersatz mit dem Bruttobetrag. Konto ist der Kreditor, Gegenkonto das Aufwandskonto.
- Kreditor: Sammelkreditor aus `--kreditor` oder je Lieferant über `--kreditoren zuordnung.json` (USt-IdNr., Steuernummer oder Name auf Kreditorennummer).
- Aufwandskonto: `--konto`, sonst SKR03 4980 bzw. SKR04 6850 (sonstiger Betriebsbedarf). BU-Schlüssel 9 für 19 % und 8 für 7 % Vorsteuer. Konten und Schlüssel sind Vorschläge, die mit der Steuerberatung abgestimmt gehören.
- Belegfeld 1 = Rechnungsnummer, Belegdatum = Rechnungsdatum, Buchungstext = Lieferant und Nummer, dazu Leistungsdatum, Fälligkeit und SEPA-Mandatsreferenz, falls vorhanden. Rechnungskorrekturen (Art 381) werden mit umgekehrtem Soll/Haben gebucht.
- Format: EXTF 700, Kategorie 21, Formatversion 13, Windows-1252, CRLF, 125 Spalten.

## Grenzen

- Nur Rechnungen in EUR.
- Kein Upload in DATEV Unternehmen online und keine Belegbilder.
- Reverse Charge (`AE`) und innergemeinschaftlicher Erwerb (`K`): Das Werkzeug setzt die USt-IdNr. des Lieferanten und gibt einen Hinweis aus, den BU-Schlüssel legt die Buchhaltung fest.
- Die Hinweise am Ende der Ausgabe immer weitergeben, nicht verschlucken.
