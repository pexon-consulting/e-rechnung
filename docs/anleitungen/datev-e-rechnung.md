# DATEV und E-Rechnung: XRechnung und ZUGFeRD als Buchungsstapel übernehmen

Für DATEV und E-Rechnung gibt es zwei Wege: Die E-Rechnung kommt als Beleg in DATEV Unternehmen online bzw. Belege online (dort wird sie geprüft, visualisiert und abgelegt), oder ein Fremdprogramm liest die XML-Daten und übergibt sie als Buchungsstapel im DATEV-Format (EXTF). Den zweiten Weg erledigt `erechnung datev`: Er macht aus XRechnung- und ZUGFeRD-Dateien eine EXTF-Datei mit einer Buchungszeile je Steuersatz, die die Buchhaltung prüft und importiert.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil von [E-Rechnung in Python](../../README.md).

## Das Wichtigste in Kürze

- DATEV arbeitet laut eigener FAQ mit den XML-Daten einer E-Rechnung, nicht mit dem PDF.
- Belege online übernimmt empfangene ZUGFeRD- und XRechnung-Dateien, prüft sie auf EN-16931-Konformität und zeigt die XML-Daten lesbar an.
- Ein Buchungsstapel im DATEV-Format ist eine CSV-Datei mit Kopfzeile (`EXTF;700;21;Buchungsstapel;13;...`), Spaltenzeile und einer Zeile je Buchung.
- `erechnung datev` schreibt diese Datei aus Eingangsrechnungen: Bruttobetrag je Steuersatz, Kreditor, Aufwandskonto nach SKR03 oder SKR04 und BU-Schlüssel 9 (19 %) oder 8 (7 %).
- Der Export ist ein Importvorschlag: Konten, BU-Schlüssel und Sonderfälle wie Reverse Charge legt die Buchhaltung bzw. die Steuerberatung fest.
- Das Belegbild wird nicht übertragen; die Spalte Beleglink bleibt leer.

## Wie kommen E-Rechnungen in DATEV?

Eine E-Rechnung ist laut § 14 Abs. 1 Satz 3 UStG eine Rechnung in einem strukturierten elektronischen Format, das eine elektronische Verarbeitung ermöglicht. Für DATEV heißt das: Entscheidend sind die XML-Daten, das PDF ist nur eine Lesefassung.

| Weg | Was passiert | Quelle |
| --- | --- | --- |
| DATEV Unternehmen online / Belege online | Empfangene E-Rechnungen (ZUGFeRD, XRechnung) und PDF-Rechnungen übernehmen, Validierung auf EN-16931-Konformität, Datenvisualisierung, revisionssichere Ablage, Zugriff aus DATEV-Rechnungswesen über Schnittstelle und Beleglink. Bereitstellung per DATEV Upload Mail oder Upload online. | [DATEV Belege online](https://www.datev.de/web/de/shop/produkt-details/belege-online-95157) |
| DATEV E-Rechnungsplattform / E-Rechnungspostfach | Kostenpflichtige Erweiterung, automatische Anmeldung im TRAFFIQX- und Peppol-Netzwerk, Weiterleitung an Unternehmen online. | [DATEV Hilfe-Center](https://apps.datev.de/help-center/documents/1038006?product=datev-e-rechnungsplattform&topic=e-rechnungsplattform) |
| Buchungsstapel im DATEV-Format | Ein Fremdprogramm liest die E-Rechnung und schreibt eine EXTF-Datei, die in DATEV-Rechnungswesen importiert wird. Hier setzt `erechnung datev` an. | [DATEV Developer Portal](https://developer.datev.de/de/file-format/details/datev-format/getting-started) |

Welchen Weg Ihre Kanzlei nutzt, hängt von deren DATEV-Ausstattung ab. Der Buchungsstapel ist sinnvoll, wenn die E-Rechnungen schon bei Ihnen liegen (Postfach, Ordner, eigenes Programm) und die Buchungsvorschläge ohne Abtippen in DATEV ankommen sollen.

Prüfen Sie Eingangsrechnungen vor dem Export: `erechnung validieren eingang/*.xml` prüft mit den offiziellen KoSIT-Regeln. Das BMF-Schreiben vom 15.10.2025, Rn. 35a, empfiehlt, den Validierungsbericht aufzubewahren; dafür gibt es `--bericht`.

## Was ist ein DATEV-Buchungsstapel (EXTF)?

Ein DATEV-Buchungsstapel ist eine Textdatei im öffentlich beschriebenen DATEV-Format, mit der Fremdprogramme Buchungen an DATEV-Rechnungswesen übergeben. Die Formatbeschreibung steht im [DATEV Developer Portal](https://developer.datev.de/de/file-format/details/datev-format/format-description/header).

Die Datei hat drei Teile:

1. Kopfzeile: beginnt mit `EXTF` (Kennzeichen für Fremdprogramme, DATEV-Programme schreiben `DTVF`), dann Versionsnummer 700, Datenkategorie 21 (Buchungsstapel), Formatname und Formatversion 13.
2. Spaltenzeile: die Namen aller Spalten in fester Reihenfolge.
3. Datenzeilen: eine Buchung je Zeile, Felder durch Semikolon getrennt, Texte in Anführungszeichen.

Laut dem Funktionsumfang DATEV-Format im [DATEV-Marktplatz](https://www.datev.de/content/dam/markenassets/marktplatz/schnittstellen-funktionsumfang/DATEV-Format_betzemeier.pdf) sind Umsatz, Soll/Haben-Kennzeichen, Konto, Gegenkonto und Belegdatum Mussfelder.

`erechnung datev` schreibt die Datei in Windows-1252 (cp1252) mit Zeilenende CRLF, wie es das Format vorsieht. Zeichen, die Windows-1252 nicht kennt, werden zu `?`.

## erechnung datev: Eingangsrechnungen als Buchungsstapel exportieren

Der Befehl liest XRechnung (UBL und CII) und ZUGFeRD-PDFs und schreibt eine EXTF-Datei. Alle Beispielrechnungen aus dem Repo mit SKR04:

```bash
erechnung datev beispiele/0*/xrechnung_ubl.xml --skr 04 -o EXTF_Buchungsstapel.csv
```

```text
EXTF_Buchungsstapel.csv: 9 Rechnungen, 10 Buchungszeilen (EXTF 700, SKR 04)
  Hinweis: RE-2026-0004: Kategorie AE: Steuer auf Eingangsseite selbst berechnen (BU-Schlüssel mit Steuerberatung festlegen).
  Hinweis: RE-2026-0005: Kategorie K: Steuer auf Eingangsseite selbst berechnen (BU-Schlüssel mit Steuerberatung festlegen).
```

Neun Rechnungen ergeben zehn Zeilen, weil Rechnung RE-2026-0002 zwei Steuersätze hat. Die Hinweise gehen an die Buchhaltung: Bei Reverse Charge und innergemeinschaftlichen Fällen setzt der Export keinen BU-Schlüssel.

Die Optionen laut `erechnung datev --help`:

| Option | Bedeutung | Standard |
| --- | --- | --- |
| `-o`, `--ausgabe` | Zieldatei | `EXTF_Buchungsstapel.csv` |
| `--berater` | Beraternummer in der Kopfzeile | 1001 |
| `--mandant` | Mandantennummer in der Kopfzeile | 1 |
| `--skr` | Kontenrahmen `03` oder `04` | `03` |
| `--kreditor` | Sammelkreditor | 70000 |
| `--kreditoren` | JSON-Datei: USt-IdNr. oder Name zu Kreditorennummer | keine |
| `--konto` | Aufwandskonto | SKR03 4980, SKR04 6850 |

Ersetzen Sie Berater- und Mandantennummer durch die Werte Ihrer Kanzlei, sonst passt der Stapel nicht zum Mandanten.

## Die Kopfzeile: 31 Felder

Die erste Zeile der Beispieldatei [`beispiele/datev/EXTF_Buchungsstapel.csv`](../../beispiele/datev/EXTF_Buchungsstapel.csv):

```text
"EXTF";700;21;"Buchungsstapel";13;20261015120000000;;"RE";"e-rechnung";;1001;1;20260101;4;20261015;20261015;"E-Rechnungen Eingang";;1;0;0;"EUR";;;;;"04";;;;
```

| Feld | Wert | Herkunft im Export |
| --- | --- | --- |
| 1 | `"EXTF"` | Kennzeichen für Fremdprogramme |
| 2 | `700` | Versionsnummer |
| 3 | `21` | Datenkategorie Buchungsstapel |
| 4 | `"Buchungsstapel"` | Formatname |
| 5 | `13` | Formatversion |
| 6 | `20261015120000000` | Zeitpunkt der Erzeugung (Jahr bis Millisekunde) |
| 8 | `"RE"` | fester Wert im Code |
| 9 | `"e-rechnung"` | exportierendes Programm |
| 11 | `1001` | Beraternummer (`--berater`) |
| 12 | `1` | Mandantennummer (`--mandant`) |
| 13 | `20260101` | Beginn des Wirtschaftsjahres (1.1. des Rechnungsjahres) |
| 14 | `4` | Sachkontenlänge |
| 15 und 16 | `20261015` | ältestes und jüngstes Rechnungsdatum im Stapel |
| 17 | `"E-Rechnungen Eingang"` | Bezeichnung des Stapels |
| 22 | `"EUR"` | Währung |
| 27 | `"04"` | Kontenrahmen (`--skr`) |

Die übrigen Felder sind leer oder feste Werte aus dem Code (`1;0;0` in den Feldern 19 bis 21).

## Die Spaltenzeile: 125 Spalten und welche befüllt werden

Die zweite Zeile nennt 125 Spalten der Formatversion 13. Die ersten 20 davon:

```text
Umsatz (ohne Soll/Haben-Kz);Soll/Haben-Kennzeichen;WKZ Umsatz;Kurs;Basisumsatz;WKZ Basisumsatz;Konto;Gegenkonto (ohne BU-Schlüssel);BU-Schlüssel;Belegdatum;Belegfeld 1;Belegfeld 2;Skonto;Buchungstext;Postensperre;Diverse Adressnummer;Geschäftspartnerbank;Sachverhalt;Zinssperre;Beleglink
```

Danach folgen unter anderem Beleginfo, Kostenstellen, Zusatzinformationen und am Ende Leistungsdatum, Fälligkeit und Steuersatz. In den Originalnamen von DATEV stehen bei Beleginfo, KOST und Zusatzinformation lange Striche; der Export schreibt sie genau so.

Diese Spalten füllt `erechnung datev`, alle anderen bleiben leer:

| Nr. | Spalte | Inhalt aus der E-Rechnung | Beispiel |
| --- | --- | --- | --- |
| 1 | Umsatz (ohne Soll/Haben-Kz) | Bruttobetrag je Steuersatz (BT-116 plus BT-117), Komma als Dezimalzeichen | `2009,91` |
| 2 | Soll/Haben-Kennzeichen | `H` bei Rechnungen, `S` bei Gutschriften (bezogen auf das Konto, also den Kreditor) | `"H"` |
| 3 | WKZ Umsatz | immer EUR | `"EUR"` |
| 7 | Konto | Kreditor: Sammelkreditor oder Treffer aus `--kreditoren` | `70000` |
| 8 | Gegenkonto (ohne BU-Schlüssel) | Aufwandskonto 4980 (SKR03), 6850 (SKR04) oder `--konto` | `6850` |
| 9 | BU-Schlüssel | 9 bei 19 %, 8 bei 7 %, sonst leer | `"9"` |
| 10 | Belegdatum | Rechnungsdatum BT-2 als TTMM | `1510` |
| 11 | Belegfeld 1 | Rechnungsnummer BT-1, höchstens 36 Zeichen, nur Buchstaben, Ziffern und `$ & % * + - /` | `"RE-2026-0001"` |
| 14 | Buchungstext | Name des Verkäufers (BT-27) und Rechnungsnummer, höchstens 60 Zeichen | `"Nordlicht Software GmbH RE-2026-0001"` |
| 20 | Beleglink | bleibt leer | |
| 21 und 22 | Beleginfo Art 1 und Inhalt 1 | `E-Rechnung` und das erkannte Format | `"XRechnung 3.0 (UBL)"` |
| 40 | EU-Land u. USt-IdNr. | USt-IdNr. des Verkäufers (BT-31), nur bei Kategorie AE und K | `"DE123456789"` |
| 105 | SEPA-Mandatsreferenz | BT-89 bei Lastschrift | `"MANDAT-2026-001"` |
| 115 | Leistungsdatum | Lieferdatum BT-72, sonst Ende des Leistungszeitraums BT-74, als TTMMJJJJ | `30092026` |
| 117 | Fälligkeit | Fälligkeitsdatum BT-9 als TTMMJJJJ | `14112026` |
| 119 | Steuersatz | 19 oder 7, nur bei Kategorie S | `19` |

Die erste Datenzeile der Beispieldatei, Felder 1 bis 22:

```text
2009,91;"H";"EUR";;;;70000;6850;"9";1510;"RE-2026-0001";;;"Nordlicht Software GmbH RE-2026-0001";;;;;;;"E-Rechnung";"XRechnung 3.0 (UBL)"
```

In Worten: 2.009,91 EUR brutto, Kreditor 70000 im Haben, Aufwandskonto 6850 im Soll, BU-Schlüssel 9 zieht 19 % Vorsteuer heraus, Belegdatum 15.10., Belegfeld 1 ist die Rechnungsnummer.

## Eine Buchungszeile je Steuersatz

Enthält eine Rechnung mehrere Steuersätze, schreibt der Export je Zeile der Umsatzsteuer-Aufschlüsselung (BG-23) eine Buchung. Beispiel 02 hat 7 % und 19 %:

```text
160,18;"H";"EUR";;;;70000;6850;"8";1510;"RE-2026-0002";;;"Buchhandlung am Markt GmbH RE-2026-0002"
47,46;"H";"EUR";;;;70000;6850;"9";1510;"RE-2026-0002";;;"Buchhandlung am Markt GmbH RE-2026-0002"
```

Beide Zeilen tragen dieselbe Rechnungsnummer in Belegfeld 1, damit der offene Posten zusammenpasst. Ein Betrag von 0,00 EUR je Steuersatz wird übersprungen.

## Kreditoren: Sammelkreditor oder Zuordnung per JSON

Ohne weitere Angabe bucht der Export alle Rechnungen auf den Sammelkreditor 70000 (änderbar mit `--kreditor`). Für eigene Kreditorennummern je Lieferant gibt es `--kreditoren` mit einer JSON-Datei. Der Export sucht in dieser Reihenfolge: USt-IdNr. des Verkäufers (BT-31), Steuernummer (BT-32), Name (BT-27). Der Schlüssel muss genau so geschrieben sein wie in der Rechnung.

```json
{
  "Nordlicht Software GmbH": 70010,
  "Buchhandlung am Markt GmbH": 70020,
  "Elektro Schmidt GmbH": 70030
}
```

```bash
erechnung datev beispiele/0*/xrechnung_ubl.xml --skr 03 --kreditoren kreditoren.json -o EXTF_Buchungsstapel.csv
```

```text
EXTF_Buchungsstapel.csv: 9 Rechnungen, 10 Buchungszeilen (EXTF 700, SKR 03)
  Hinweis: RE-2026-0004: Kategorie AE: Steuer auf Eingangsseite selbst berechnen (BU-Schlüssel mit Steuerberatung festlegen).
  Hinweis: RE-2026-0005: Kategorie K: Steuer auf Eingangsseite selbst berechnen (BU-Schlüssel mit Steuerberatung festlegen).
  Hinweis: 2026-017: Grafikdesign Lena Beispiel hat keine eigene Kreditorennummer, Sammelkreditor 70000.
```

Ergebnis (Auszug, Felder 1 bis 11):

```text
2009,91;"H";"EUR";;;;70010;4980;"9";1510;"RE-2026-0001"
160,18;"H";"EUR";;;;70020;4980;"8";1510;"RE-2026-0002"
18500,00;"H";"EUR";;;;70030;4980;;1510;"RE-2026-0004"
850,00;"H";"EUR";;;;70000;4980;;1510;"2026-017"
```

Lieferanten ohne Eintrag landen auf dem Sammelkreditor, der Hinweis sagt welche. Die Kreditorennummern selbst müssen in DATEV angelegt sein; der Export legt keine Stammdaten an.

## Konten und BU-Schlüssel nach SKR03 und SKR04

| Kontenrahmen | Aufwandskonto (Gegenkonto) | BU-Schlüssel 19 % | BU-Schlüssel 7 % | Sammelkreditor |
| --- | --- | --- | --- | --- |
| SKR03 (`--skr 03`, Standard) | 4980 Sonstiger Betriebsbedarf | 9 | 8 | 70000 |
| SKR04 (`--skr 04`) | 6850 Sonstiger Betriebsbedarf | 9 | 8 | 70000 |

Ein einziges Aufwandskonto für alle Rechnungen ist ein Platzhalter. Die richtige Kontierung (Wareneingang, Fremdleistungen, Software, Miete) entscheidet die Buchhaltung beim Import oder danach. Ein anderes Konto für den ganzen Stapel setzt `--konto`:

```bash
erechnung datev beispiele/01_standard/xrechnung_ubl.xml --konto 4900 -o EXTF_Buchungsstapel.csv
```

```text
EXTF_Buchungsstapel.csv: 1 Rechnungen, 1 Buchungszeilen (EXTF 700, SKR 03)
```

## Gutschriften, Reverse Charge und innergemeinschaftliche Fälle

Gutschriften mit Rechnungsart 381 bucht der Export mit Soll-Kennzeichen auf dem Kreditor, also umgekehrt zur Rechnung:

```text
285,60;"S";"EUR";;;;70000;6850;"9";1510;"GS-2026-0001";;;"Nordlicht Software GmbH GS-2026-0001"
```

Bei Reverse Charge nach § 13b UStG (Steuerkategorie AE) und innergemeinschaftlichen Fällen (Kategorie K) weist die Rechnung keine Steuer aus. Der Export setzt deshalb keinen BU-Schlüssel, trägt die USt-IdNr. des Verkäufers in Spalte 40 ein und gibt einen Hinweis aus:

```text
18500,00;"H";"EUR";;;;70000;6850;;1510;"RE-2026-0004";;;"Elektro Schmidt GmbH RE-2026-0004"
```

Welcher BU-Schlüssel in diesen Fällen richtig ist, klären Sie mit der Steuerberatung. Rechnungen von Kleinunternehmern (Kategorie E) bekommen ebenfalls keinen BU-Schlüssel, weil sie keine Umsatzsteuer ausweisen.

Andere Rechnungsarten bucht der Export wie eine normale Rechnung. Das betrifft auch die Rechnungskorrektur 384 und die Schlussrechnung 877: Sie erscheinen mit ihrem vollen Betrag. Ob die ursprüngliche Rechnung oder die Abschläge storniert bzw. verrechnet werden, entscheidet die Buchhaltung. Mehr zu diesen Arten in [Gutschrift, Rechnungskorrektur und Reverse Charge](./e-rechnung-gutschrift-korrektur.md).

## Wirtschaftsjahr und Fremdwährung

Ein Buchungsstapel gehört zu genau einem Wirtschaftsjahr. Der Export setzt den Beginn auf den 1.1. des ältesten Rechnungsjahres und bricht ab, wenn eine Rechnung außerhalb liegt:

```bash
erechnung datev beispiele/01_standard/xrechnung_ubl.xml rechnung_januar_2027.xml -o EXTF_Buchungsstapel.csv
```

```text
RE-2027-0001 vom 2027-01-05 liegt nicht im Wirtschaftsjahr ab 2026-01-01. Pro Wirtschaftsjahr einen Stapel bauen.
```

Der Exit-Code ist dann 1 und es entsteht keine Datei. Bauen Sie je Wirtschaftsjahr einen eigenen Stapel. Ein abweichendes Wirtschaftsjahr kennt die Kommandozeile nicht; in Python geht es über `Einstellungen(wj_beginn=...)` (Beispiel 6).

Rechnungen in anderer Währung als Euro lehnt der Export ab:

```text
RE-2026-0100: Währung USD. Dieser Export kann nur EUR.
```

Fremdwährungsrechnungen (Kurs, Basisumsatz) erfassen Sie in DATEV von Hand.

## Import in DATEV-Rechnungswesen

Die EXTF-Datei wird in DATEV-Rechnungswesen als Buchungsstapel im DATEV-Format importiert. Den genauen Menüweg Ihrer DATEV-Version beschreibt die DATEV-Hilfe, die Feldbeschreibung steht im [DATEV Developer Portal](https://developer.datev.de/de/file-format/details/datev-format/getting-started). Prüfen Sie den Stapel nach dem Import, bevor er festgeschrieben wird; der Export setzt in der Kopfzeile keine Festschreibung (Feld 21 ist 0).

## Grenzen: was der Export nicht macht

- Kein Belegbild: Die Spalte Beleglink (Feld 20) bleibt leer. Im DATEV-Format verweist sie für Unternehmen online auf einen Beleg mit dem Programmkürzel `BEDI` und einer GUID; dafür muss der Beleg vorher an DATEV übertragen sein. Das leistet dieses Werkzeug nicht.
- Keine Stammdaten: Kreditoren und Konten müssen in DATEV bestehen.
- Keine Dublettenprüfung: Dieselbe Datei zweimal übergeben ergibt zwei Buchungen.
- Nur Euro und nur ein Wirtschaftsjahr je Stapel.
- Kein Versand und keine Archivierung. Die E-Rechnung selbst bewahren Sie im Ursprungsformat auf, laut BMF-Schreiben vom 15.10.2025, Rn. 60, acht Jahre.

## Beispiele

### Beispiel 1: Einen Ordner mit Eingangsrechnungen exportieren

```bash
erechnung datev eingang/*.xml -o EXTF_Buchungsstapel.csv --skr 04
```

Für den monatlichen Export, wenn alle E-Rechnungen eines Zeitraums in einem Ordner liegen.

### Beispiel 2: ZUGFeRD-PDF und XRechnung gemischt

```bash
erechnung datev beispiele/02_gemischte_steuersaetze/zugferd_en16931.pdf beispiele/02_gemischte_steuersaetze/xrechnung_cii.xml -o EXTF_Buchungsstapel.csv
```

```text
EXTF_Buchungsstapel.csv: 2 Rechnungen, 4 Buchungszeilen (EXTF 700, SKR 03)
```

Die Spalte Beleginfo Inhalt 1 zeigt danach das Format, `"ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)"` bzw. `"XRechnung 3.0 (CII)"`. Das braucht man, wenn Lieferanten unterschiedliche Formate schicken. Hier steckt dieselbe Rechnung in beiden Dateien; im echten Einsatz übergeben Sie jede Rechnung nur einmal.

### Beispiel 3: Eigene Berater- und Mandantennummer

```bash
erechnung datev eingang/*.xml --berater 1001 --mandant 1 --skr 03 -o EXTF_Buchungsstapel.csv
```

Setzen Sie hier die Nummern aus Ihrer DATEV-Kanzlei ein, damit der Stapel dem richtigen Mandanten zugeordnet wird.

### Beispiel 4: Lieferanten auf eigene Kreditoren buchen

```bash
erechnung datev eingang/*.xml --kreditoren kreditoren.json -o EXTF_Buchungsstapel.csv
```

Die JSON-Datei ordnet USt-IdNr., Steuernummer oder Namen einer Kreditorennummer zu (siehe oben). Sinnvoll, sobald Sie offene Posten je Lieferant führen.

### Beispiel 5: Zeile mit SEPA-Lastschrift

Aus Beispiel 09 übernimmt der Export die Mandatsreferenz in Spalte 105 (Auszug, Felder 1 bis 11, dann Spalte 105):

```text
714,00;"H";"EUR";;;;70000;6850;"9";1510;"RE-2026-0007" ... "MANDAT-2026-001"
```

Hilfreich, wenn der Lieferant per Lastschrift einzieht und der Zahlungsabgleich die Mandatsreferenz braucht.

### Beispiel 6: Abweichendes Wirtschaftsjahr in Python

```python
from datetime import date
from pathlib import Path

from erechnung import lesen
from erechnung.datev import Einstellungen, stapel

rechnungen = [lesen("beispiele/01_standard/xrechnung_ubl.xml"),
              lesen("rechnung_januar_2027.xml")]
e = Einstellungen(berater=1001, mandant=1, skr="04", wj_beginn=date(2026, 7, 1))
daten, hinweise = stapel(rechnungen, e)
Path("EXTF_Buchungsstapel.csv").write_bytes(daten)
print(daten.decode("cp1252").splitlines()[0])
```

```text
"EXTF";700;21;"Buchungsstapel";13;20261016002043675;;"RE";"e-rechnung";;1001;1;20260701;4;20261015;20270105;"E-Rechnungen Eingang";;1;0;0;"EUR";;;;;"04";;;;
```

Für Firmen, deren Wirtschaftsjahr nicht am 1.1. beginnt: Rechnungen vom Oktober 2026 und Januar 2027 liegen dann im selben Stapel (Wirtschaftsjahr ab 1.7.2026).

## Schritt für Schritt

1. Sammeln Sie die Eingangsrechnungen eines Zeitraums als Dateien (XRechnung als `.xml`, ZUGFeRD als `.pdf`) in einem Ordner. Dateien, die keine E-Rechnung enthalten, werden mit Hinweis übersprungen.
2. Installieren Sie das Werkzeug (Python 3.10 oder neuer, kein Java):
   ```bash
   pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
   ```
3. Prüfen Sie die Rechnungen mit den offiziellen Regeln und legen Sie die Prüfberichte ab:
   ```bash
   erechnung validieren eingang/* --bericht berichte/
   ```
4. Fragen Sie die Kanzlei nach Beraternummer, Mandantennummer, Kontenrahmen und, falls gewünscht, Kreditorennummern. Legen Sie die Kreditoren als JSON-Datei an.
5. Exportieren Sie den Stapel, je Wirtschaftsjahr einen:
   ```bash
   erechnung datev eingang/* --berater 1001 --mandant 1 --skr 04 --kreditoren kreditoren.json -o EXTF_Buchungsstapel.csv
   ```
6. Lesen Sie die Hinweise in der Ausgabe. Rechnungen mit Reverse Charge oder innergemeinschaftlichem Bezug und Lieferanten auf dem Sammelkreditor gehören vor dem Import geklärt.
7. Übergeben Sie die CSV-Datei an die Buchhaltung bzw. importieren Sie sie in DATEV-Rechnungswesen. Kontrollieren Sie Konten und BU-Schlüssel, bevor der Stapel festgeschrieben wird.
8. Bewahren Sie die E-Rechnungen im Ursprungsformat und die Prüfberichte auf.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Rechnungen aus zwei Wirtschaftsjahren in einem Aufruf | `... liegt nicht im Wirtschaftsjahr ab 2026-01-01. Pro Wirtschaftsjahr einen Stapel bauen.`, keine Datei | Je Wirtschaftsjahr einen Aufruf, bei abweichendem Wirtschaftsjahr die Python-API mit `wj_beginn` |
| Rechnung in USD oder einer anderen Währung | `Währung USD. Dieser Export kann nur EUR.`, Exit-Code 1 | Rechnung aus dem Stapel nehmen und in DATEV von Hand erfassen |
| Reines PDF ohne eingebettetes XML | `...: übersprungen, Das PDF enthält kein eingebettetes Rechnungs-XML. ...`, der Export läuft trotzdem weiter (Exit-Code 0) | Ausgabe auf "übersprungen" prüfen; die Rechnung von Hand buchen oder beim Lieferanten eine E-Rechnung anfordern |
| Andere Datei im Ordner (zum Beispiel HTML) | `...: übersprungen, Kein wohlgeformtes XML ...` | Nur `.xml` und `.pdf` übergeben und die Zahl der Rechnungen in der Ausgabe vergleichen |
| Gleiche Rechnung zweimal übergeben | zwei identische Buchungen, keine Warnung | Ordner vorher bereinigen, z. B. bereits exportierte Dateien verschieben |
| Kreditor wird nicht gefunden | Hinweis `hat keine eigene Kreditorennummer, Sammelkreditor 70000` | Schlüssel in der JSON-Datei genau wie BT-31, BT-32 oder BT-27 der Rechnung schreiben |
| Reverse Charge ohne BU-Schlüssel importiert | Steuer nach § 13b fehlt in der Auswertung | BU-Schlüssel mit der Steuerberatung festlegen und in DATEV nachtragen |
| Rechnungskorrektur oder Schlussrechnung doppelt im Aufwand | Ursprungsrechnung bzw. Abschläge und Korrektur stehen beide voll im Stapel | Ursprungsbuchung oder Abschläge in DATEV stornieren bzw. verrechnen |
| Sonderzeichen außerhalb von Windows-1252 | `?` im Buchungstext, etwa bei polnischen Namen | Buchungstext in DATEV korrigieren; die Rechnung selbst bleibt unverändert |

## Häufige Fragen

### Kann DATEV XRechnung und ZUGFeRD lesen?

Ja, laut DATEV übernimmt Belege online empfangene ZUGFeRD- und XRechnung-Dateien, prüft sie auf EN-16931-Konformität und visualisiert die XML-Daten. Details stehen auf der Seite [DATEV Belege online](https://www.datev.de/web/de/shop/produkt-details/belege-online-95157). Dieses Werkzeug ist ein zusätzlicher Weg über den Buchungsstapel.

### Was bedeutet EXTF im DATEV-Format?

EXTF ist das Kennzeichen in der Kopfzeile für Dateien, die ein Fremdprogramm erzeugt hat. DATEV-eigene Programme schreiben `DTVF`. Danach folgen Versionsnummer 700, Datenkategorie 21 (Buchungsstapel) und Formatversion 13.

### Welche Konten und BU-Schlüssel nutzt erechnung datev?

Standard sind Sammelkreditor 70000, Aufwandskonto 4980 (SKR03) bzw. 6850 (SKR04) und BU-Schlüssel 9 für 19 % sowie 8 für 7 % Vorsteuer. Das sind Vorschläge; Kreditor und Aufwandskonto lassen sich mit `--kreditor`, `--kreditoren` und `--konto` ändern.

### Wird die Rechnung als Beleg an DATEV übertragen?

Nein, der Export überträgt nur Buchungsdaten, kein Belegbild und keinen Beleglink. Die E-Rechnung bewahren Sie selbst auf oder laden sie über einen DATEV-Weg wie Belege online hoch.

### Kann ich ZUGFeRD-PDFs direkt nach DATEV exportieren?

Ja, `erechnung datev` liest das eingebettete XML aus ZUGFeRD-PDFs und behandelt es wie eine XRechnung. Dateien, die keine E-Rechnung enthalten, werden mit einem Hinweis übersprungen.

### Warum entstehen mehr Buchungszeilen als Rechnungen?

Je Steuersatz einer Rechnung entsteht eine eigene Zeile. Eine Rechnung mit 7 % und 19 % ergibt zwei Zeilen mit derselben Rechnungsnummer in Belegfeld 1.

### Wie buche ich Reverse-Charge-Rechnungen aus E-Rechnungen?

Der Export übernimmt den Nettobetrag ohne BU-Schlüssel und gibt einen Hinweis aus. Den passenden Schlüssel für die Steuerschuldnerschaft des Leistungsempfängers legen Sie mit der Steuerberatung fest.

> **Hinweis:** Diese Anleitung erklärt Gesetz, BMF-Schreiben und technische Standards nach dem Stand vom 15.10.2026. Sie ist keine Steuer- oder Rechtsberatung, die Autoren sind keine Steuerberater. Für die Beurteilung eines konkreten Falls wenden Sie sich an Ihre Steuerberatung oder Ihr Finanzamt. Alle Angaben ohne Gewähr.

## Weiterlesen

- [E-Rechnung empfangen und lesen](./e-rechnung-empfangen.md)
- [E-Rechnung prüfen: Validator mit den offiziellen Regeln](./e-rechnung-validator.md)
- [Gutschrift, Rechnungskorrektur und Reverse Charge als E-Rechnung](./e-rechnung-gutschrift-korrektur.md)
- [E-Rechnung archivieren](./e-rechnung-archivieren.md)
- [E-Rechnung mit Python](./e-rechnung-python.md)
- Beispieldatei: [`beispiele/datev/EXTF_Buchungsstapel.csv`](../../beispiele/datev/EXTF_Buchungsstapel.csv), Übersicht aller Fälle: [`beispiele/README.md`](../../beispiele/README.md)
