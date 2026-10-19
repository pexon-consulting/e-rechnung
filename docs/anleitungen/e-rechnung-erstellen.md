# E-Rechnung erstellen: XRechnung und ZUGFeRD kostenlos erzeugen

Eine E-Rechnung erstellen Sie, indem Sie die Rechnungsdaten in einem strukturierten Format nach EN 16931 ausgeben, also als XRechnung (UBL oder CII) oder als ZUGFeRD-PDF mit eingebettetem XML, und das Ergebnis mit den offiziellen KoSIT-Regeln prüfen. Kostenlos geht das mit dem Open-Source-Werkzeug `erechnung`: Sie schreiben die Rechnungsdaten in eine JSON- oder TOML-Datei, `erechnung erstellen rechnung.json --validieren` rechnet Summen und Steuern selbst aus, schreibt die Datei und prüft sie sofort.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Selbstständige, Buchhaltung und Entwickler, die Rechnungen aus einer Datei erzeugen wollen. Wer ein Rechnungsprogramm nutzt, erstellt E-Rechnungen meist direkt dort.

## Das Wichtigste in Kürze

- Eine E-Rechnung muss als XRechnung oder als ZUGFeRD ab Version 2.0.1 im Profil BASIC oder höher vorliegen, ein reines PDF reicht nicht (Details: [Was ist eine E-Rechnung?](./was-ist-eine-e-rechnung.md)).
- Es gibt drei Wege: das eigene Buchhaltungsprogramm, ein Portal wie die Weberfassung der OZG-RE für Rechnungen an den Bund, oder ein Open-Source-Werkzeug.
- Mit `erechnung erstellen` erzeugen Sie aus einer JSON- oder TOML-Datei sechs Formate: XRechnung UBL, XRechnung CII, EN 16931 UBL und CII sowie ZUGFeRD-PDF in den Profilen EN 16931 und XRECHNUNG.
- Summen, Steuerbeträge und die Umsatzsteuer-Aufschlüsselung rechnet das Werkzeug selbst, kaufmännisch gerundet je Steuersatz, so wie die KoSIT-Regeln nachrechnen.
- Mit `--validieren` prüft das Werkzeug das Ergebnis sofort mit den offiziellen KoSIT-Regeln (XRechnung 3.0.2); ohne die Option zeigt es zumindest die Hinweise der Vorprüfung.
- Laut BMF-Schreiben vom 15.10.2025, Rn. 35a, bietet es sich zum Nachweis an, den Validierungsbericht aufzubewahren; dafür gibt es `erechnung validieren --bericht`.

## Was bedeutet es, eine E-Rechnung zu erstellen?

Was eine E-Rechnung ist, erklärt [Was ist eine E-Rechnung?](./was-ist-eine-e-rechnung.md) ausführlich. Für das Erstellen zählt: Das Format muss der EN 16931 entsprechen oder zwischen den Parteien vereinbart sein (§ 14 Abs. 1 Satz 6 UStG). Ein PDF ohne integrierte Datensätze ist eine sonstige Rechnung (UStAE 14.1 Abs. 2 in der Fassung des BMF-Schreibens vom 15.10.2025).

E-Rechnung schreiben heißt also: Die Pflichtangaben nach § 14 Abs. 4 UStG stehen im XML, nicht nur auf einem Bild. Laut BMF-Schreiben vom 15.10.2025, Rn. 35, müssen alle umsatzsteuerlichen Pflichtangaben im strukturierten Teil stehen. Bei ZUGFeRD ist bei Abweichungen der XML-Teil maßgebend (BMF-Schreiben vom 15.10.2025, UStAE 14.4 Abs. 3). Eine XRechnung ist eine reine XML-Datei, eine ZUGFeRD-Rechnung ein PDF/A-3 mit eingebettetem XML. ZUGFeRD ab Version 2.0.1 ist laut UStAE 14.1 Abs. 14 ein zulässiges E-Rechnungsformat, ausgenommen die Profile MINIMUM und BASIC-WL. Mehr dazu in [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md).

## Wie erstelle ich eine E-Rechnung? Die drei Wege

| Weg | Wie es funktioniert | Gut für |
| --- | --- | --- |
| Buchhaltungs- oder Rechnungsprogramm | Das Programm erzeugt XRechnung oder ZUGFeRD aus den erfassten Daten | Wer ohnehin ein Programm nutzt |
| Portal | Rechnung im Browser erfassen; die OZG-RE des Bundes bietet laut [e-rechnung-bund.de](https://www.e-rechnung-bund.de/faq/) eine Weberfassung, die Registrierung ist kostenlos | Einzelne Rechnungen an den Bund |
| Open-Source-Werkzeug | Daten als Datei, ein Befehl erzeugt und prüft die E-Rechnung | Selbstständige, Entwickler, Steuerkanzleien, Massenverarbeitung |

Ob Ihr Programm gültige Dateien erzeugt, können Sie unabhängig davon prüfen: [E-Rechnung aus Lexware, sevdesk, SAP und anderen Programmen prüfen](./e-rechnung-buchhaltungssoftware.md). Andere Open-Source-Bibliotheken stellt [E-Rechnung Software kostenlos](./e-rechnung-software-kostenlos.md) vor.

## E-Rechnung kostenlos erstellen mit `erechnung`

Das Werkzeug braucht Python 3.10 oder neuer, aber kein Java. Es liegt auf GitHub, nicht auf PyPI:

```bash
pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
```

Das Extra `offiziell` installiert saxonche für die KoSIT-Regeln. Beim ersten Prüfen lädt das Werkzeug die KoSIT-Konfiguration einmal von GitHub, prüft die SHA-256-Summe und arbeitet danach offline. Rechnungsdaten verlassen den Rechner nicht. Für ZUGFeRD ohne eigene PDF-Vorlage und für `--pdfa` muss Ghostscript (`gs`) installiert sein. TOML-Dateien unter Python 3.10 brauchen das Extra `toml`.

Der kürzeste Weg von der Datei zur geprüften XRechnung ist `erechnung erstellen rechnung.json --validieren` (Ausgabe in Beispiel 1). Ohne `-o` heißt die Ausgabe wie die Eingabe, mit `.xml` oder `.pdf` als Endung. Der Exit-Code ist 0 bei gültig, 1 bei ungültig oder fehlerhafter Eingabe und 2, wenn die offizielle Prüfung nicht laufen konnte.

## Die Eingabedatei: Aufbau und Pflichtfelder

Die Eingabedatei beschreibt eine Rechnung mit deutschen Feldnamen. Die Felder entsprechen dem Datenmodell der EN 16931 in `src/erechnung/modell.py`. Fünf Regeln gelten für jede Eingabe:

1. Dezimalzahlen als Text schreiben, also `"120.00"` statt `120.00`. Text wird exakt als Dezimalzahl übernommen, ohne Rundungsfehler einer Gleitkommazahl. Ein Komma als Dezimaltrenner wird akzeptiert (`"1,5"`), ein Tausenderpunkt nicht (`"1.234,50"` ergibt einen Fehler).
2. Datumsangaben im Format JJJJ-MM-TT, also `"2026-10-15"`.
3. Unbekannte Feldnamen lehnt das Werkzeug ab und nennt die erlaubten Felder. Tippfehler fallen so sofort auf.
4. Summen, Steuerbeträge und die Aufschlüsselung (`summen`, `steuern`) nicht angeben. Das Werkzeug berechnet sie bei jedem Lauf neu.
5. Die Kennung BT-24 setzt `--format`. Ein Feld `spezifikation` in der Eingabe wird dabei überschrieben.

Ohne diese Felder bricht `erechnung erstellen` mit "Pflichtfelder fehlen" ab: `nummer`, `datum`, `verkaeufer.name`, `kaeufer.name` und je Position `id`, `name`, `menge`, `einheit`, `preis`. Bei Nachlässen und Zuschlägen ist `betrag` Pflicht.

Damit die Datei als XRechnung gültig ist, braucht sie zusätzlich:

| Angabe | Eingabefeld | Regel |
| --- | --- | --- |
| Käuferreferenz | `leitweg_id` (bei Behörden die Leitweg-ID, sonst z. B. `"-"`) | BR-DE-15 |
| Kontakt des Verkäufers mit Name, Telefon, E-Mail | `verkaeufer.kontakt` | BR-DE-2, BR-DE-5 bis BR-DE-7 |
| Elektronische Adresse beider Seiten | `verkaeufer.elektronische_adresse`, `kaeufer.elektronische_adresse` | PEPPOL-EN16931-R020, -R010 |
| Ort und PLZ beider Seiten | `adresse.ort`, `adresse.plz` | BR-DE-3, -4, -8, -9 |
| USt-IdNr. oder Steuernummer des Verkäufers | `verkaeufer.ust_id` oder `verkaeufer.steuernummer` | BR-DE-16, § 14 Abs. 4 Nr. 2 UStG |
| Zahlungsart und passende Daten | `zahlung.art`, bei 58 die `iban` | BR-DE-1, BR-DE-23 |
| Liefer- oder Leistungsdatum | `lieferung.datum` oder `leistung_von`/`leistung_bis` | § 14 Abs. 4 Nr. 6 UStG (Hinweis der Vorprüfung) |

Laut BMF-FAQ genügt im B2B als BT-10 ein Platzhalter wie "-"; eine Leitweg-ID braucht nur, wer an Behörden schreibt.

### Minimale, gültige Eingabe

Diese Eingabe enthält nur, was für eine gültige XRechnung nötig ist. Sie wurde mit `erechnung erstellen rechnung.json --validieren` geprüft: KoSIT gültig, 0 Fehler, 0 Warnungen.

```json
{
  "nummer": "RE-2026-0100",
  "datum": "2026-10-15",
  "leitweg_id": "-",
  "verkaeufer": {
    "name": "Nordlicht Beispiel GmbH",
    "adresse": {"strasse": "Musterstraße 1", "plz": "20095", "ort": "Hamburg"},
    "ust_id": "DE123456789",
    "elektronische_adresse": "rechnung@example.com",
    "kontakt": {"name": "Erika Mustermann", "telefon": "+49 40 66969123", "email": "buchhaltung@example.com"}
  },
  "kaeufer": {
    "name": "Beispiel Handel AG",
    "adresse": {"strasse": "Hauptstraße 5", "plz": "80331", "ort": "München"},
    "elektronische_adresse": "eingang@example.com"
  },
  "zahlung": {"art": "58", "iban": "DE79000000001234567890"},
  "lieferung": {"datum": "2026-10-14"},
  "positionen": [
    {"id": "1", "name": "Beratung", "menge": "3", "einheit": "HUR", "preis": "100.00"}
  ]
}
```

Alles andere hat Standardwerte: Rechnungsart `380`, Währung `EUR`, Land `DE`, Steuerkategorie `S` mit 19 %, Zahlungsart `58` (SEPA-Überweisung), elektronische Adressen als E-Mail (`EM`).

## Feldreferenz: Eingabefeld, BT-Nummer, Bedeutung

BT steht für Business Term, BG für Business Group der EN 16931. Bei Parteien gilt die erste Nummer für den Verkäufer, die zweite für den Käufer.

| Eingabefeld | BT/BG | Bedeutung |
| --- | --- | --- |
| `nummer` | BT-1 | Rechnungsnummer |
| `datum` | BT-2 | Rechnungsdatum |
| `art` | BT-3 | Rechnungsart (UNTDID 1001), Standard `380` |
| `waehrung` | BT-5 | Währung, Standard `EUR` |
| `faellig` | BT-9 | Fälligkeitsdatum |
| `leitweg_id` | BT-10 | Käuferreferenz, bei Behörden die Leitweg-ID |
| `projekt`, `vertragsnummer` | BT-11, BT-12 | Projekt- und Vertragsreferenz |
| `bestellnummer`, `auftragsnummer` | BT-13, BT-14 | Bestellnummer des Käufers, Auftragsnummer des Verkäufers |
| `notizen` | BT-22 | Liste freier Bemerkungen |
| `prozess` | BT-23 | Geschäftsprozess, Standard `urn:fdc:peppol.eu:2017:poacc:billing:01:1.0` |
| `vorgaenger_nummer`, `vorgaenger_datum` | BT-25, BT-26 | Vorgängerrechnung (BG-3), etwa bei Rechnungsart 384 |
| `leistung_von`, `leistung_bis` | BT-73, BT-74 | Leistungszeitraum der ganzen Rechnung |
| `vorauszahlung` | BT-113 | Bereits gezahlter Betrag |
| `befreiungsgruende` | BT-120 | Befreiungsgrund je Steuerkategorie, z. B. `{"AE": "..."}` |
| `verkaeufer` / `kaeufer` | BG-4 / BG-7 | Die beiden Parteien |
| `.name` | BT-27 / BT-44 | Name laut Register |
| `.handelsname` | BT-28 / BT-45 | Abweichender Handelsname |
| `.kennung` | BT-29 / BT-46 | Kennung, etwa Kunden- oder Lieferantennummer |
| `.register` | BT-30 / BT-47 | Registernummer, z. B. HRB 000000 |
| `.ust_id` | BT-31 / BT-48 | USt-IdNr. |
| `.steuernummer` | BT-32 | Steuernummer des Verkäufers |
| `.rechtliches` | BT-33 | Weitere rechtliche Angaben des Verkäufers |
| `.elektronische_adresse` | BT-34 / BT-49 | Elektronische Adresse |
| `.elektronische_adresse_schema` | - | EAS-Code: `EM` E-Mail, `0204` Leitweg-ID, `9930` USt-IdNr. |
| `.adresse.strasse`, `.zusatz` | BT-35, BT-36 / BT-50, BT-51 | Straße und Zusatz |
| `.adresse.ort`, `.plz` | BT-37, BT-38 / BT-52, BT-53 | Ort und PLZ |
| `.adresse.region`, `.land` | BT-39, BT-40 / BT-54, BT-55 | Region und Land (ISO 3166-1, Standard `DE`) |
| `.kontakt.name`, `.telefon`, `.email` | BT-41 bis BT-43 / BT-56 bis BT-58 | Ansprechpartner |
| `lieferung.name`, `.adresse`, `.datum` | BT-70, BG-15, BT-72 | Empfänger, Lieferadresse, Lieferdatum |
| `zahlung.art`, `.verwendungszweck` | BT-81, BT-83 | Zahlungsart (UNTDID 4461, Standard `58`), Verwendungszweck |
| `zahlung.iban`, `.kontoinhaber`, `.bic` | BT-84, BT-85, BT-86 | Empfängerkonto |
| `zahlung.mandatsreferenz`, `.glaeubiger_id`, `.zahler_iban` | BT-89, BT-90, BT-91 | Lastschrift: Mandatsreferenz, Gläubiger-ID, belastetes Konto |
| `zahlung.bedingungen`, `.skonto_tage`, `.skonto_prozent` | BT-20 | Zahlungsbedingungen; Skonto wird als `#SKONTO#`-Zeile geschrieben |
| `positionen[]` | BG-25 | Rechnungspositionen |
| `.id`, `.notiz` | BT-126, BT-127 | Positionsnummer und Bemerkung |
| `.menge`, `.einheit` | BT-129, BT-130 | Menge und Einheit (UN/ECE Rec 20, z. B. `C62`, `HUR`) |
| `.bestellposition` | BT-132 | Position in der Bestellung |
| `.zeitraum_von`, `.zeitraum_bis` | BT-134, BT-135 | Leistungszeitraum der Position |
| `.preis`, `.basismenge` | BT-146, BT-149 | Nettopreis und Preisbasismenge |
| `.kategorie`, `.satz` | BT-151, BT-152 | Steuerkategorie (Standard `S`) und Steuersatz (Standard 19) |
| `.name`, `.beschreibung`, `.artikelnummer` | BT-153, BT-154, BT-155 | Bezeichnung, Beschreibung, Artikelnummer |
| `nachlaesse[]` (Rechnung / Position) | BG-20, BG-21 / BG-27, BG-28 | Nachlässe und Zuschläge |
| `.grund`, `.grund_code` | BT-97, BT-98 / BT-104, BT-105 | Grund als Text und Code (Belegebene) |
| `.kategorie`, `.satz` | BT-95, BT-96 / BT-102, BT-103 | Steuer des Nachlasses, nur auf Belegebene |
| `.betrag`, `.prozent`, `.basis`, `.zuschlag` | - | Betrag, Prozentsatz, Basis, `true` für Zuschlag |

## XRechnung oder ZUGFeRD erstellen: alle Formate

`--format` bestimmt Syntax und Kennung (BT-24). Ohne Angabe entsteht eine XRechnung in UBL.

| `--format` | Ergebnis | BT-24 |
| --- | --- | --- |
| `xrechnung-ubl` (Standard) | XRechnung 3.0, UBL 2.1 | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` |
| `xrechnung-cii` | XRechnung 3.0, CII | wie oben |
| `en16931-ubl` | EN 16931, UBL 2.1 | `urn:cen.eu:en16931:2017` |
| `en16931-cii` | EN 16931, CII | `urn:cen.eu:en16931:2017` |
| `zugferd` | PDF, ZUGFeRD-Profil EN 16931, Anhang `factur-x.xml` | `urn:cen.eu:en16931:2017` |
| `zugferd-xrechnung` | PDF, ZUGFeRD-Profil XRECHNUNG, Anhang `xrechnung.xml` | XRechnung-Kennung |

```console
$ erechnung erstellen rechnung.json --format xrechnung-cii -o rechnung_cii.xml --validieren
rechnung_cii.xml: xrechnung-cii, Rechnung RE-2026-0100, Zahlbetrag 357,00 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 XRechnung (CII))
$ erechnung erstellen rechnung.json --format zugferd -o rechnung.pdf --validieren
rechnung.pdf: zugferd, Rechnung RE-2026-0100, Zahlbetrag 357,00 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 (CII))
```

Ohne `--pdf` erzeugt Ghostscript eine einfache PDF/A-3-Ansicht. Mit `--pdf layout.pdf` nimmt das Werkzeug Ihr eigenes Rechnungslayout als Vorlage; `--pdfa` wandelt die Vorlage vorher nach PDF/A-3b. Bei PDFs prüft `--validieren` das eingebettete XML mit den KoSIT-Regeln, nicht die PDF/A-3-Konformität. Rechnungsarten, die XRechnung nicht kennt, lehnt das Werkzeug bei den XRechnung-Formaten ab (BR-DE-17); erlaubt sind 326, 380, 381, 384, 389, 875, 876 und 877.

## Eingabe als TOML

TOML ist für Menschen oft leichter zu lesen als JSON. Die Feldnamen sind dieselben, Unterobjekte werden zu Abschnitten oder Inline-Tabellen, Listen zu `[[positionen]]`.

```toml
nummer = "RE-2026-0101"
datum = "2026-10-15"
faellig = "2026-11-14"
leitweg_id = "-"
leistung_von = "2026-09-01"
leistung_bis = "2026-09-30"

[verkaeufer]
name = "Nordlicht Beispiel GmbH"
ust_id = "DE123456789"
elektronische_adresse = "rechnung@example.com"
adresse = { strasse = "Musterstraße 1", plz = "20095", ort = "Hamburg" }
kontakt = { name = "Erika Mustermann", telefon = "+49 40 66969123", email = "buchhaltung@example.com" }

[kaeufer]
name = "Beispiel Handel AG"
elektronische_adresse = "eingang@example.com"
adresse = { strasse = "Hauptstraße 5", plz = "80331", ort = "München" }

[zahlung]
art = "58"
iban = "DE79000000001234567890"
skonto_tage = 10
skonto_prozent = "2"
bedingungen = "Zahlbar innerhalb von 30 Tagen ohne Abzug."

[[positionen]]
id = "1"
name = "Wartung Server"
menge = "12"
einheit = "HUR"
preis = "95.00"
```

```console
$ erechnung erstellen rechnung.toml --validieren
rechnung.xml: xrechnung-ubl, Rechnung RE-2026-0101, Zahlbetrag 1.356,60 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 XRechnung (UBL Invoice))
```

## Skonto in der XRechnung: die #SKONTO#-Syntax

XRechnung verlangt Skonto in einer festen Syntax im Feld BT-20 (Regel BR-DE-18): `#SKONTO#TAGE=10#PROZENT=2.00#`, optional mit `BASISBETRAG=...#`, wenn nur ein Teil des Betrags skontofähig ist. Prozentwerte haben genau zwei Nachkommastellen mit Punkt, alles in Großbuchstaben, nach jeder Skonto-Zeile folgt ein Zeilenumbruch.

Sie müssen die Syntax nicht selbst schreiben. Aus `"skonto_tage": 10` und `"skonto_prozent": "2"` erzeugt das Werkzeug die Zeile `#SKONTO#TAGE=10#PROZENT=2.00#` samt Zeilenumbruch und hängt `bedingungen` dahinter (XML in Beispiel 3). Eine zweite Skontostufe schreiben Sie selbst an den Anfang von `bedingungen`, mit `\n` als Zeilenumbruch: `"#SKONTO#TAGE=20#PROZENT=1.00#\nZahlbar innerhalb von 30 Tagen ohne Abzug."`. Steht dort `PROZENT=1` statt `PROZENT=1.00`, meldet die KoSIT-Prüfung `BR-DE-18`. Die Ansicht (`erechnung anzeigen`) übersetzt die Zeilen in Klartext, etwa "2,00 % Skonto bei Zahlung innerhalb von 10 Tagen".

## Leistungszeitraum und Lieferdatum angeben

Das Liefer- oder Leistungsdatum ist eine Pflichtangabe nach § 14 Abs. 4 Nr. 6 UStG. Drei Möglichkeiten:

- `"lieferung": {"datum": "2026-10-14"}` für einen Liefertag (BT-72).
- `"leistung_von"` und `"leistung_bis"` für einen Zeitraum der ganzen Rechnung (BT-73, BT-74), in UBL als `cac:InvoicePeriod`.
- `"zeitraum_von"` und `"zeitraum_bis"` je Position (BT-134, BT-135), wenn Positionen verschiedene Zeiträume haben.

Fehlt alles, gibt die Vorprüfung den Hinweis `VP-14-4-6` aus. Die KoSIT-Regeln verlangen das Datum nicht, das Umsatzsteuergesetz schon.

## Nachlässe und Zuschläge

Nachlässe und Zuschläge gibt es auf Belegebene (`nachlaesse` der Rechnung, BG-20 und BG-21) und je Position (`nachlaesse` in der Position, BG-27 und BG-28). `"zuschlag": true` macht aus einem Nachlass einen Zuschlag. Belegnachlässe brauchen `kategorie` und `satz`, damit sie der richtigen Steuergruppe zugeordnet werden.

Für einen Prozent-Nachlass setzen Sie `"betrag": "0"` und `"prozent": "10"`. Das Werkzeug rechnet dann Betrag und Basis aus. Die Basis ist bei Positionen der Positionsbetrag, auf Belegebene die Summe aller Positionen. Bei gemischten Steuersätzen geben Sie auf Belegebene besser einen festen `betrag` je Steuersatz an oder setzen `basis` ausdrücklich.

## Zahlungsarten: die Codes für BT-81

| Code | Text, den das Werkzeug anzeigt | Was XRechnung zusätzlich verlangt |
| --- | --- | --- |
| `58` | SEPA-Überweisung | Konto (BG-17) mit `iban`; BT-84 soll eine korrekte IBAN sein (BR-DE-19) |
| `59` | SEPA-Lastschrift | `mandatsreferenz`, `glaeubiger_id`, `zahler_iban` (BR-DE-25, BR-DE-30, BR-DE-31) |
| `30` | Überweisung (ohne SEPA) | Konto (BG-17), BR-DE-23 |
| `48`, `54`, `55` | Bankkarte, Kreditkarte, Debitkarte | Kartenangaben (BG-18), BR-DE-24 |
| `10` | Bargeld | - |
| `20`, `31`, `42`, `49`, `57`, `97`, `ZZZ` | Scheck, Auslandsüberweisung, Zahlung auf Bankkonto, Lastschrift, Dauerauftrag, Verrechnung, Sonstige | - |

Kartendaten (BG-18) kann die Eingabe nicht abbilden. Für Kartenzahlungen ist das Werkzeug deshalb nicht geeignet. Eine IBAN mit falscher Prüfziffer meldet die Vorprüfung als `VP-IBAN`.

## Steuerkategorien und Befreiungsgründe

Jede Position hat eine Steuerkategorie (`kategorie`, UNTDID 5305) und einen Satz (`satz`). Bei `E`, `Z`, `AE`, `K` und `G` ohne Satz setzt das Werkzeug 0 %.

| Kategorie | Bedeutung | Befreiungsgrund |
| --- | --- | --- |
| `S`, `Z` | Regelsteuersatz oder ermäßigter Satz; Nullsatz | nicht nötig |
| `E` | Steuerbefreit, z. B. Kleinunternehmer nach § 19 UStG | Pflicht, selbst angeben |
| `AE` | Reverse Charge, § 13b UStG | Pflicht, Standardtext vorhanden |
| `K` | Innergemeinschaftliche Lieferung | Pflicht, Standardtext vorhanden |
| `G`, `O` | Ausfuhr außerhalb der EU; nicht steuerbar | Pflicht, Standardtext vorhanden |

Den Befreiungsgrund (BT-120) geben Sie über `befreiungsgruende` an, etwa `{"E": "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet."}`. Fehlt er bei `E`, meldet die Vorprüfung `VP-14-4-8` und die KoSIT-Prüfung `BR-E-10`. Bei `AE` braucht der Käufer eine `ust_id` oder eine Registernummer (`register`), bei `K` eine `ust_id`, sonst meldet die Vorprüfung `VP-13B` bzw. `VP-IG`; vollständige Eingaben zeigen [Beispiel 05](../../beispiele/05_reverse_charge_13b/eingabe.json) und [Beispiel 06](../../beispiele/06_innergemeinschaftlich/eingabe.json). Ob eine Steuerbefreiung im Einzelfall greift, klären Sie mit der Steuerberatung.

## Wie das Werkzeug Summen und Steuern berechnet

Die Rechenlogik steht in `src/erechnung/rechnen.py` und folgt den Rechenregeln der EN 16931 (BR-CO-*):

1. Positionsbetrag (BT-131) = Menge mal Preis durch Basismenge, auf Cent gerundet, minus Nachlässe, plus Zuschläge der Position.
2. Die Positionen werden nach Steuerkategorie und Steuersatz gruppiert. Belegnachlässe und -zuschläge kommen in ihre Gruppe.
3. Je Gruppe wird die Basis auf Cent gerundet, die Steuer aus der gerundeten Basis berechnet und ebenfalls auf Cent gerundet. Gerundet wird kaufmännisch (`ROUND_HALF_UP`: ab 0,5 Cent wird aufgerundet).
4. Nettobetrag (BT-109) = Summe der Positionen minus Nachlässe plus Zuschläge; Steuersumme (BT-110) = Summe der Gruppen; Brutto (BT-112) = Netto plus Steuer; Zahlbetrag (BT-115) = Brutto minus Vorauszahlung.

[Beispiel 02](../../beispiele/02_gemischte_steuersaetze/xrechnung_ubl.xml) zeigt das: 3 Fachbücher zu 49,90 EUR ergeben 149,70 EUR, davon 7 % sind 10,479 EUR, gerundet 10,48 EUR. Die 19-%-Gruppe hat 39,98 EUR plus 4,90 EUR minus 5,00 EUR Treuerabatt, also 39,88 EUR; 19 % davon sind 7,5772 EUR, gerundet 7,58 EUR. Genau diese Werte stehen in den beiden `cac:TaxSubtotal` der Datei. So rechnen auch die Schematron-Regeln der KoSIT nach (etwa BR-CO-15 für Brutto = Netto + Steuer). Rechenfehler wie in Rn. 6b des BMF-Schreibens vom 15.10.2025 beschrieben (Steuerbetrag passt nicht zum Steuersatz) entstehen dadurch nicht.

## Prüfen beim Erstellen: `--validieren` und die Vorprüfung

Ohne `--validieren` läuft nach dem Schreiben nur die Vorprüfung. Ihre Hinweise erscheinen auf stderr, die Datei wird trotzdem geschrieben und der Exit-Code ist 0. Bei einem Fehler weist eine Zeile darauf hin, dass die KoSIT-Regeln noch nicht geprüft haben:

```console
$ erechnung erstellen ohne_kontakt.json
  FEHLER  VP-BR-DE-2: Kontakt des Verkäufers unvollständig: XRechnung verlangt Name, Telefon und E-Mail (BT-41, BT-42, BT-43).
  Nicht mit den KoSIT-Regeln geprüft. Prüfen mit: erechnung validieren ohne_kontakt.xml
ohne_kontakt.xml: xrechnung-ubl, Rechnung RE-2026-0100, Zahlbetrag 357,00 EUR
```

Mit `--validieren` prüft das Werkzeug die fertige Datei mit den KoSIT-Regeln und zeigt deren Befunde. Das Ergebnis ist maßgeblich, die Vorprüfung ersetzt es nicht:

```console
$ erechnung erstellen ohne_kontakt.json --validieren
ohne_kontakt.xml: xrechnung-ubl, Rechnung RE-2026-0100, Zahlbetrag 357,00 EUR
  KoSIT-Regeln: UNGÜLTIG (EN16931 XRechnung (UBL Invoice))
  FEHLER  BR-DE-2: [BR-DE-2] Die Gruppe "SELLER CONTACT" (BG-6) muss übermittelt werden.
```

Bei `--validieren` zeigt das Werkzeug nur die KoSIT-Befunde. Die Vorprüfungs-Hinweise, etwa zum fehlenden Leistungsdatum, sehen Sie dann mit `erechnung validieren rechnung.xml`. Mit `--bericht berichte` legt dieser Befehl zusätzlich einen Prüfbericht als JSON ab, mit Zeitpunkt, Regelversion und SHA-256 der Datei, etwa `berichte/rechnung.xml.bd53628ed806.validierungsbericht.json`. Die Bedeutung einzelner Meldungen erklärt [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md).

## E-Rechnung erstellen: Beispiele für XRechnung und ZUGFeRD

### Beispiel 1: Minimale XRechnung erzeugen und prüfen

```console
$ erechnung erstellen rechnung.json --validieren
rechnung.xml: xrechnung-ubl, Rechnung RE-2026-0100, Zahlbetrag 357,00 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 XRechnung (UBL Invoice))
```

Brauchen Sie, wenn Sie eine einzelne Rechnung ohne Rechnungsprogramm schreiben. Die Eingabe steht oben im Abschnitt "Minimale, gültige Eingabe".

### Beispiel 2: ZUGFeRD-PDF mit eigenem Rechnungslayout

```console
$ erechnung erstellen rechnung.json --format zugferd --pdf layout.pdf --pdfa -o rechnung_zugferd.pdf --validieren
rechnung_zugferd.pdf: zugferd, Rechnung RE-2026-0100, Zahlbetrag 357,00 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 (CII))
```

Brauchen Sie, wenn Ihre Kunden weiter Ihr gewohntes PDF sehen sollen. Das PDF darf noch kein XML enthalten. Wer ein fertiges CII-XML hat, nimmt `erechnung zugferd`, siehe [PDF in ZUGFeRD umwandeln](./pdf-in-zugferd-umwandeln.md).

### Beispiel 3: Zwei Skontostufen

```json
{"zahlung": {"art": "58", "iban": "DE79000000001234567890", "skonto_tage": 10, "skonto_prozent": "2",
             "bedingungen": "#SKONTO#TAGE=20#PROZENT=1.00#\nZahlbar innerhalb von 30 Tagen ohne Abzug."}}
```

```xml
<cbc:Note>#SKONTO#TAGE=10#PROZENT=2.00#
#SKONTO#TAGE=20#PROZENT=1.00#
Zahlbar innerhalb von 30 Tagen ohne Abzug.</cbc:Note>
```

Brauchen Sie bei gestaffeltem Skonto. Der Ausschnitt zeigt nur den Teil `zahlung` der Eingabe. Die Datei ist laut `erechnung erstellen skonto.json --validieren` gültig.

### Beispiel 4: Rabatt auf eine Position, Zuschlag und Vorauszahlung

```json
{
  "positionen": [
    {"id": "1", "name": "Beratung", "menge": "10", "einheit": "HUR", "preis": "120.00",
     "nachlaesse": [{"betrag": "0", "prozent": "10", "grund": "Projektrabatt", "grund_code": "95"}]},
    {"id": "2", "name": "Fachbuch", "menge": "2", "einheit": "C62", "preis": "39.90", "satz": "7"}
  ],
  "nachlaesse": [{"betrag": "25.00", "zuschlag": true, "grund": "Anfahrt", "kategorie": "S", "satz": "19"}],
  "vorauszahlung": "500.00"
}
```

```xml
<cac:LegalMonetaryTotal>
  <cbc:LineExtensionAmount currencyID="EUR">1159.80</cbc:LineExtensionAmount>
  <cbc:TaxExclusiveAmount currencyID="EUR">1184.80</cbc:TaxExclusiveAmount>
  ...
  <cbc:PrepaidAmount currencyID="EUR">500.00</cbc:PrepaidAmount>
  <cbc:PayableAmount currencyID="EUR">900.34</cbc:PayableAmount>
</cac:LegalMonetaryTotal>
```

Brauchen Sie bei Rabatten, Pauschalen und Abschlägen. Die Position 1 kostet nach 10 % Rabatt 1.080,00 EUR, die 19-%-Gruppe hat mit Anfahrt 1.105,00 EUR Basis und 209,95 EUR Steuer. Laut `erechnung erstellen rabatt.json --validieren` ist die Datei gültig.

### Beispiel 5: Rechnung an eine Behörde mit Leitweg-ID

```json
{
  "leitweg_id": "04011000-12345-03",
  "kaeufer": {"name": "Stadt Musterstadt, Amt für Digitalisierung",
              "adresse": {"strasse": "Rathausplatz 1", "plz": "12345", "ort": "Musterstadt"},
              "elektronische_adresse": "04011000-12345-03", "elektronische_adresse_schema": "0204"}
}
```

Brauchen Sie für Rechnungen an öffentliche Auftraggeber. Die Leitweg-ID steht in BT-10 und als elektronische Adresse mit dem Schema `0204`. Die vollständige Datei ist [Beispiel 08](../../beispiele/08_b2g_leitweg_id/eingabe.json); die Prüfziffer prüfen Sie mit `erechnung leitweg-id`, siehe [Leitweg-ID](./leitweg-id.md).

### Beispiel 6: Fehler in der Eingabe finden

```console
$ erechnung erstellen datum_falsch.json
Eingabe fehlerhaft: rechnung.datum: Datum im Format JJJJ-MM-TT erwartet, nicht '15.10.2026'
```

Brauchen Sie beim ersten Ausfüllen. Die Meldung nennt den Pfad zum Feld, bei Positionen etwa `rechnung.positionen[0].preis: keine Zahl: 'abc'`.

## Schritt für Schritt: die erste eigene E-Rechnung erstellen

1. Werkzeug installieren (siehe oben) und mit `erechnung --version` testen.
2. Eine Vorlage holen: `erechnung beispiele meine-beispiele` schreibt neun fertige Eingaben, etwa `meine-beispiele/01_standard.json`. Die Fälle erklärt [E-Rechnung Beispiel](./e-rechnung-beispiel.md).
3. Die passende Vorlage kopieren und mit einem Texteditor Ihre Daten eintragen: Rechnungsnummer, Datum, Ihre Firma, den Kunden, die Positionen. Beträge in Anführungszeichen, Datum als JJJJ-MM-TT.
4. Für Kunden ohne Leitweg-ID `"leitweg_id": "-"` setzen, für Behörden die Leitweg-ID des Auftraggebers.
5. Format wählen: XRechnung (Standard) oder `--format zugferd` für ein PDF.
6. `erechnung erstellen meine-rechnung.json --validieren` ausführen.
7. Bei "UNGÜLTIG" die gemeldeten Regeln nachschlagen, die Eingabe korrigieren und Schritt 6 wiederholen.
8. Mit `erechnung validieren meine-rechnung.xml --bericht berichte` auch die Hinweise der Vorprüfung ansehen und einen Prüfbericht mit SHA-256 ablegen.
9. Die Datei an den Kunden schicken. Den Versand übernimmt das Werkzeug nicht, es hat keinen Peppol-Zugangspunkt und keinen E-Mail-Versand.
10. Die Rechnung aufbewahren: acht Jahre nach § 14b Abs. 1 UStG, siehe [E-Rechnung archivieren](./e-rechnung-archivieren.md).

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Datum als TT.MM.JJJJ | "Datum im Format JJJJ-MM-TT erwartet" | `"2026-10-15"` schreiben |
| Feldname falsch geschrieben | "unbekannte Felder [...]" mit Liste der erlaubten Felder | Namen aus der Feldreferenz übernehmen |
| Kein `leitweg_id` | KoSIT `BR-DE-15` | Leitweg-ID oder `"-"` eintragen |
| Kontakt fehlt | KoSIT `BR-DE-2`, Vorprüfung `VP-BR-DE-2` | `verkaeufer.kontakt` mit Name, Telefon, E-Mail |
| Steuerkategorie `E` ohne Grund | KoSIT `BR-E-10`, Vorprüfung `VP-14-4-8` | `befreiungsgruende` setzen |
| Zahlungsart `59` ohne Mandat | KoSIT `PEPPOL-EN16931-R061`, `BR-DE-25-a` | `mandatsreferenz`, `glaeubiger_id`, `zahler_iban` angeben |
| Skonto als `PROZENT=1` | KoSIT `BR-DE-18` | zwei Nachkommastellen: `PROZENT=1.00` |
| `--format zugferd` ohne Ghostscript | Meldung "Ghostscript (gs) nicht gefunden" | Ghostscript installieren oder `--pdf` mit eigener PDF/A-3-Vorlage |

## Häufige Fragen

### Kann ich eine E-Rechnung kostenlos erstellen?

Ja, mit `erechnung erstellen` erzeugen Sie XRechnung und ZUGFeRD kostenlos und prüfen sie mit den offiziellen KoSIT-Regeln. Das Werkzeug ist Open Source, die KoSIT-Prüfkonfiguration steht unter Apache-2.0. Für einzelne Rechnungen an den Bund gibt es außerdem die Weberfassung der OZG-RE; die Registrierung dort ist kostenlos.

### Wie erstelle ich eine XRechnung aus Word oder Excel?

Aus einem Word- oder Excel-Dokument entsteht keine XRechnung durch Speichern als PDF. Sie übertragen die Angaben in eine Eingabedatei (JSON oder TOML) und erzeugen daraus mit `erechnung erstellen` die XRechnung. Ein vorhandenes PDF-Layout können Sie für ZUGFeRD mit `--pdf` weiterverwenden.

### Wie erstelle ich eine ZUGFeRD-Rechnung?

Mit `erechnung erstellen rechnung.json --format zugferd -o rechnung.pdf` entsteht ein PDF/A-3 mit eingebettetem `factur-x.xml` im Profil EN 16931. Mit `--pdf` nutzen Sie Ihr eigenes Layout. Das Profil EN 16931 gilt laut UStAE 14.1 Abs. 14 als E-Rechnung.

### Muss ich Summen und Umsatzsteuer selbst ausrechnen?

Nein, das Werkzeug rechnet Positionsbeträge, Steuer je Steuersatz, Netto, Brutto und Zahlbetrag selbst. Felder wie `summen` und `steuern` in der Eingabe überschreibt es. Gerundet wird kaufmännisch je Steuergruppe, so wie die KoSIT-Regeln nachrechnen.

### Was trage ich als Leitweg-ID ein, wenn mein Kunde keine Behörde ist?

Tragen Sie die Bestellnummer des Kunden oder einen Platzhalter wie "-" ein. Laut BMF-FAQ genügt im B2B ein Platzhalter, und ein fehlendes BT-10 ist nach BMF-Schreiben vom 15.10.2025, Rn. 35a, umsatzsteuerlich unbeachtlich. Für eine gültige XRechnung verlangt BR-DE-15 das Feld trotzdem.

### Müssen Kleinunternehmer E-Rechnungen erstellen?

Nein, Rechnungen von Kleinunternehmern dürfen laut BMF-FAQ immer als sonstige Rechnung ausgestellt werden (§ 34a UStDV). Wer trotzdem eine E-Rechnung schickt, nutzt Steuerkategorie `E` mit Befreiungsgrund wie in [Beispiel 07](../../beispiele/07_kleinunternehmer/eingabe.json). Details in [E-Rechnung für Kleinunternehmer](./e-rechnung-kleinunternehmer.md).

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [XRechnung: Format, Aufbau und Pflichtfelder](./xrechnung.md)
- [ZUGFeRD: Format, Profile und Versionen](./zugferd.md)
- [E-Rechnung prüfen: Validator mit den offiziellen Regeln](./e-rechnung-validator.md)
- [E-Rechnung Beispiel: Beispieldateien zum Herunterladen](./e-rechnung-beispiel.md)
- [E-Rechnung mit Python](./e-rechnung-python.md)
- [Was ist eine E-Rechnung? Definition, Formate und wie sie aussieht](./was-ist-eine-e-rechnung.md)
- [E-Rechnung Pflicht: ab wann, für wen und welche Übergangsfristen gelten](./e-rechnung-pflicht.md)
- Beispiele im Repo: [Übersicht](../../beispiele/README.md), [Standardrechnung als Eingabe](../../beispiele/01_standard/eingabe.json), [als XRechnung UBL](../../beispiele/01_standard/xrechnung_ubl.xml)
