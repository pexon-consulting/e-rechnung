# BMF-Schreiben zur E-Rechnung: die wichtigen Randnummern erklärt

Das BMF-Schreiben zur E-Rechnung gibt es in zwei Fassungen: Das erste Schreiben vom 15.10.2024 regelt die Einführung der Pflicht, das zweite vom 15.10.2025 ändert und ergänzt es um Formatfehler (Rn. 6a), Geschäftsregelfehler (Rn. 6b), Rechtsfolgen und Validierung (Rn. 35a) und die Aufbewahrung von acht Jahren (Rn. 60). Praktisch heißt das: Eine Datei mit Formatfehler ist keine E-Rechnung, ein fehlendes BT-10 ist umsatzsteuerlich unbeachtlich, bei Hybridformaten wie ZUGFeRD gilt das XML, und den Validierungsbericht sollten Sie aufbewahren.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Geschäftsführung, Buchhaltung und Steuerkanzleien. Technische Beispiele stehen weiter unten und sind optional.

## Das Wichtigste in Kürze

- Das BMF-Schreiben vom 15.10.2025 (GZ III C 2 - S 7287-a/00019/007/243) ändert Randnummern des Schreibens vom 15.10.2024 und den Umsatzsteuer-Anwendungserlass (UStAE); es gilt für alle Umsätze nach dem 31.12.2024.
- Eine Datei mit Formatfehlern ist laut Rn. 6a keine E-Rechnung, sondern eine sonstige Rechnung, egal welcher Art der Fehler ist.
- Geschäftsregelfehler (Rn. 6b) zu Inhalten außerhalb der Pflichtangaben, etwa ein fehlendes BT-10, sind laut Rn. 35a umsatzsteuerlich unbeachtlich.
- Alle umsatzsteuerlichen Pflichtangaben müssen im strukturierten Teil stehen (Rn. 35); bei Hybridformaten gehen die Daten des XML dem Bildteil vor (UStAE 14.4 Abs. 3).
- Auf das technische Ergebnis einer Validierung hinsichtlich Format und Geschäftsregeln durch eine geeignete Validierungsanwendung darf man sich bei Beachtung der Sorgfalt eines ordentlichen Kaufmanns verlassen; den Validierungsbericht aufzubewahren, bietet sich laut Rn. 35a zum Nachweis an.
- Rechnungen sind acht Jahre aufzubewahren, bei E-Rechnungen zumindest der strukturierte Teil unversehrt in seiner ursprünglichen Form (Rn. 60).

## Welche BMF-Schreiben zur E-Rechnung gibt es?

Ein BMF-Schreiben ist eine Verwaltungsanweisung des Bundesministeriums der Finanzen. Es richtet sich an die obersten Finanzbehörden der Länder und zeigt, wie die Finanzverwaltung das Gesetz auslegt. Für die E-Rechnung gibt es zwei:

| Schreiben | Fundstelle | Inhalt |
| --- | --- | --- |
| BMF-Schreiben vom 15.10.2024 | BStBl 2024 I S. 1320 | Einführung der obligatorischen E-Rechnung bei Umsätzen zwischen inländischen Unternehmern ab 01.01.2025, Übergangsregelungen in Rn. 62 bis 65 |
| BMF-Schreiben vom 15.10.2025 | GZ III C 2 - S 7287-a/00019/007/243, Entwurf vorab am 25.06.2025 | ändert und ergänzt Randnummern des ersten Schreibens, passt den UStAE an |

Das zweite Schreiben ersetzt das erste nicht. Es ändert einzelne Randnummern (Rn.) und Zwischenüberschriften, die Änderungen sind im Original fett gedruckt. Laut seiner Anwendungsregelung gilt es für alle Umsätze, die nach dem 31.12.2024 ausgeführt werden; die Übergangsregelungen bis zum 31.12.2027 aus Rn. 62 bis 65 des Schreibens von 2024 bleiben zu beachten.

Das Schreiben vom 15.10.2025 steht als PDF auf der Seite des BMF: [BMF-Schreiben vom 15.10.2025 (PDF)](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/Umsatzsteuer-Anwendungserlass/2025-10-15-einfuehrung-obligatorische-e-rechnung.pdf?__blob=publicationFile). Eine Zusammenfassung in Frage-Antwort-Form bietet die [BMF-FAQ zur E-Rechnung](https://www.bundesfinanzministerium.de/Content/DE/FAQ/e-rechnung.html).

## Die wichtigen Randnummern im Überblick

Die Tabelle nennt die Randnummern in der Fassung des BMF-Schreibens vom 15.10.2025 und was sie im Alltag bedeuten.

| Rn. | Thema | Was es praktisch heißt |
| --- | --- | --- |
| 6a | Formatfehler | Entspricht die Datei nicht der zulässigen Syntax oder deren technischen Vorgaben, ist sie keine E-Rechnung, sondern eine sonstige Rechnung. Prüfbar mit einer geeigneten Validierungsanwendung. |
| 6b | Geschäftsregelfehler | Verstöße gegen die Geschäftsregeln des Formats, z. B. fehlendes BT-10 in einer XRechnung oder ein Steuerbetrag, der rechnerisch nicht zum Steuersatz passt. Erkennbar als "critical Error" bei der Validierung. |
| 17 | Geltungsbereich | Die Pflicht gilt auch für Gutschriften und für § 13b-Fälle, wenn beide Seiten im Inland ansässig sind, und auch, wenn der Empfänger Kleinunternehmer ist. |
| 22 | Kleinbeträge, Kleinunternehmer, Fahrausweise | Diese Rechnungen dürfen immer sonstige Rechnungen sein; für ein anderes elektronisches Format braucht es die Zustimmung des Empfängers. |
| 35 | Pflichtangaben im strukturierten Teil | Alle umsatzsteuerlichen Pflichtangaben gehören in das XML. Ergänzende Angaben dürfen in einem eingebetteten Anhang stehen (z. B. Stundennachweis als PDF), ein Link auf ein externes Ziel genügt nicht. |
| 35a | Rechtsfolgen und Validierung | Fehlende Pflichtangaben machen die Rechnung nicht ordnungsmäßig. Geschäftsregelfehler zu anderen Inhalten (z. B. BT-10) sind umsatzsteuerlich unbeachtlich. Validierung ersetzt die Prüfpflicht des Empfängers nicht. Validierungsbericht aufbewahren. |
| 51a | Minderung der Bemessungsgrundlage | Skonti und Nachlässe nach § 17 UStG erfordern keine Rechnungsberichtigung. |
| 51b | Änderung des Leistungsumfangs | Ändert sich die Leistung selbst, ist grundsätzlich eine Rechnungsberichtigung nötig, mindestens bei der Leistungsbeschreibung. |
| 60 | Aufbewahrung | Acht Jahre (§ 14b Abs. 1 UStG). Bei der E-Rechnung zumindest der strukturierte Teil unversehrt in seiner ursprünglichen Form. Speicherung außerhalb eines GoBD-konformen Systems ist allein umsatzsteuerlich kein Verstoß. |
| 61 | GoBD | Für andere als umsatzsteuerliche Zwecke gelten die GoBD (BMF-Schreiben vom 28.11.2019, zuletzt geändert am 14.07.2025). |
| 62 bis 65 (Schreiben 2024) | Übergangsregelungen | Versand von sonstigen Rechnungen bis Ende 2026, 2027 bis 800.000 EUR Vorjahresumsatz, EDI bis Ende 2027. Details in [E-Rechnung Pflicht](./e-rechnung-pflicht.md). |

Neben den Randnummern ändert das Schreiben den UStAE. Die für die Praxis wichtigsten Stellen:

| UStAE (neu gefasst) | Inhalt |
| --- | --- |
| 14.1 Abs. 2 | Sonstige Rechnungen sind auch "alle nicht strukturierten elektronischen Dateien, zum Beispiel PDF-Dateien ohne integrierte Datensätze". |
| 14.1 Abs. 5 | Alle inländischen Unternehmer müssen E-Rechnungen empfangen können, auch Kleinunternehmer; ein normales E-Mail-Postfach genügt. |
| 14.1 Abs. 12 | Die Formatwahl klären die Parteien zivilrechtlich; andere EN-16931-konforme europäische Formate sind zulässig. |
| 14.1 Abs. 14 | ZUGFeRD ab Version 2.0.1 ist zulässig, ausgenommen die Profile MINIMUM und BASIC-WL. |
| 14.4 Abs. 3 | Bei hybriden Formaten bilden die strukturierten Daten den führenden Teil und gehen dem Bildteil vor. |
| 14b.1 | Aufbewahrung im empfangenen Format, strukturierter Teil unversehrt, maschinelle Auswertbarkeit für die Finanzverwaltung. |
| 15.2a | Eine sonstige Rechnung trotz Pflicht nach Ablauf der Übergangsfrist ist keine ordnungsmäßige Rechnung; Berichtigung durch nachträgliche E-Rechnung möglich. |

## Formatfehler und Geschäftsregelfehler: der Unterschied

Das BMF-Schreiben vom 15.10.2025 unterscheidet drei Arten von Fehlern. Der Unterschied entscheidet, ob überhaupt eine E-Rechnung vorliegt.

Ein Formatfehler liegt laut Rn. 6a vor, wenn die Rechnungsdatei nicht den zulässigen Syntaxen oder deren technischen Vorgaben entspricht. Bei vereinbarten Formaten (etwa EDI) liegt er vor, wenn sie keine richtige und vollständige Extraktion zulässt. Die Art des Formatfehlers ist unerheblich: Die Datei ist dann eine sonstige Rechnung.

Ein Geschäftsregelfehler liegt laut Rn. 6b vor, wenn die Datei gegen die Geschäftsregeln des Formats verstößt. Geschäftsregeln prüfen die logischen Abhängigkeiten der Angaben, etwa ob ein Pflichtfeld gefüllt ist oder ob Beträge zusammenpassen. In XRechnung sind das die Regeln mit Codes wie `BR-DE-15` oder `BR-CO-15`.

Ein Inhaltsfehler liegt laut Rn. 35a vor, wenn Pflichtangaben nach § 14 Abs. 4 oder § 14a UStG fehlen oder falsch sind. Er kann als Geschäftsregelfehler auffallen, muss es aber nicht.

| Fehlerart | Beispiel | Wie das Werkzeug ihn meldet | Folge laut BMF-Schreiben vom 15.10.2025 |
| --- | --- | --- | --- |
| Formatfehler (Rn. 6a) | kein wohlgeformtes XML, Datum im falschen Format | `VP-LESEN` oder `XSD`, Exit-Code 2 bzw. 1 | keine E-Rechnung, sondern sonstige Rechnung |
| Geschäftsregelfehler ohne Bezug zu Pflichtangaben (Rn. 6b, 35a) | fehlendes BT-10 (`BR-DE-15`) | `UNGÜLTIG` mit Regelcode | umsatzsteuerlich unbeachtlich, technisch bleibt die Datei nach den KoSIT-Regeln ungültig |
| Geschäftsregelfehler mit Bezug zu Pflichtangaben (Rn. 6b, 35a) | Steuerbetrag passt nicht zum Steuersatz (`BR-S-09`, `BR-CO-17`) | `UNGÜLTIG` mit Regelcode | Inhaltsfehler, keine ordnungsmäßige Rechnung |
| Inhaltsfehler ohne Regelverstoß (Rn. 35a) | falscher Steuersatz, aber rechnerisch stimmig | `GÜLTIG` | trotzdem keine ordnungsmäßige Rechnung, fällt nur bei fachlicher Prüfung auf |

Die Zuordnung der Werkzeug-Meldungen zu Rn. 6a und 6b ist eine Faustregel: Schemafehler (`XSD`) betreffen die Syntax, Schematron-Regeln (`BR-...`) die Geschäftsregeln. Ob ein Fehler im Einzelfall eine Pflichtangabe berührt, klären Sie mit der Steuerberatung.

## Was Rn. 35a für Validierung und Prüfbericht heißt

Rn. 35a ist die Randnummer mit den meisten praktischen Folgen. Sie sagt vier Dinge:

1. Verstöße gegen die Pflichtangaben der §§ 14 Abs. 4 und 14a UStG führen zu einer nicht ordnungsmäßigen Rechnung (Inhaltsfehler).
2. Geschäftsregelfehler zu anderen Inhalten, zum Beispiel das fehlende Feld BT-10 Buyer reference, sind umsatzsteuerlich unbeachtlich.
3. Eine Validierung ersetzt nicht die Pflicht des Empfängers, die Rechnung auf Vollständigkeit und Richtigkeit zu prüfen, sie unterstützt ihn dabei. Inhaltsfehler können auch vorliegen, wenn die Validierung keinen Fehler findet, zum Beispiel bei einem fehlerhaften Steuersatz.
4. Ein Unternehmer kann sich bei Sorgfalt eines ordentlichen Kaufmanns auf das technische Ergebnis einer geeigneten Validierungsanwendung verlassen, hinsichtlich Format und Geschäftsregeln. Zum Nachweis bietet es sich an, den Validierungsbericht aufzubewahren.

Die beiden letzten Sätze der Rn. 35a im Wortlaut:

> "Ein Unternehmer kann sich bei Beachtung der Sorgfaltspflichten eines ordentlichen Kaufmanns auf das technische Ergebnis einer Validierung (hinsichtlich des Formats und der Geschäftsregeln) durch eine geeignete Validierungsanwendung verlassen. Zum Nachweis bietet es sich an, den Validierungsbericht aufzubewahren."

Ein Validierungsbericht ist ein Protokoll, das festhält, welche Datei wann mit welchen Regeln geprüft wurde und mit welchem Ergebnis. Genau das legt `erechnung validieren --bericht ORDNER` an: je geprüfter Datei eine JSON-Datei mit Zeitpunkt (UTC), Werkzeugversion, Regelversion der KoSIT-Konfiguration, SHA-256-Prüfsumme der Datei und allen Befunden.

```bash
erechnung validieren rechnung.pdf --bericht prüfberichte
```

```text
rechnung.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
  Prüfbericht: prüfberichte/rechnung.pdf.fff3d8c9aba4.validierungsbericht.json
```

Der Bericht (gekürzt):

```json
{
  "validiert_am": "2026-10-15T22:24:17+00:00",
  "werkzeug": "e-rechnung 0.1.0",
  "regeln": "xrechnung-3.0.2-validator-configuration-2026-08-31",
  "sha256": "fff3d8c9aba4e7589d8f582d84425a1c1580e26729ea61ee30f5387f54e39436",
  "datei": "rechnung.pdf",
  "gueltig": true,
  "offiziell": {
    "szenario": "EN16931 (CII)",
    "akzeptiert": true,
    "konfiguration": "xrechnung-3.0.2-validator-configuration-2026-08-31",
    "hinweis": "",
    "befunde": []
  }
}
```

Die Prüfsumme verbindet den Bericht mit genau dieser Datei. Die ersten zwölf Zeichen stehen auch im Dateinamen des Berichts. Wird die Rechnung später verändert, passt die Prüfsumme nicht mehr. Nachrechnen lässt sie sich unter macOS und Linux so:

```bash
shasum -a 256 rechnung.pdf
```

```text
fff3d8c9aba4e7589d8f582d84425a1c1580e26729ea61ee30f5387f54e39436  rechnung.pdf
```

Ob das Werkzeug im Sinne der Rn. 35a eine "geeignete Validierungsanwendung" ist, entscheidet nicht das Werkzeug selbst. Es nutzt die offiziellen KoSIT-Regeln (XRechnung 3.0.2, Konfiguration 2026-08-31) und kommt bei allen 222 Testdateien zum selben Ergebnis wie der KoSIT-Validator 1.6.3. Die eigene Vorprüfung (Codes mit `VP-`) erklärt Fehler auf Deutsch, ist aber nicht maßgeblich.

## Vorrang des XML bei Hybridformaten

Ein Hybridformat ist eine Datei, die einen strukturierten Teil (XML) und einen menschenlesbaren Teil (PDF) vereint, wie ZUGFeRD oder Factur-X (UStAE 14.1 Abs. 14). Früher ging bei Abweichungen der Bildteil vor. Seit der Einführung der E-Rechnung ist es umgekehrt: Laut UStAE 14.4 Abs. 3 in der Fassung des BMF-Schreibens vom 15.10.2025 bilden die strukturierten Daten den führenden Teil, bei Abweichungen gehen sie dem Bildteil vor.

Daraus folgt für die Praxis:

- Prüfen und buchen Sie die Daten aus dem XML, nicht aus dem PDF-Bild.
- Die BMF-FAQ empfiehlt, den XML-Teil selbst zu visualisieren.
- Enthält der Bildteil abweichende Rechnungsangaben, ist er laut UStAE 14c.1 Abs. 4a gegebenenfalls eine weitere (sonstige) Rechnung, für die § 14c UStG zu prüfen ist. Geringfügige technische Abweichungen wie Rundungsdifferenzen werden nicht beanstandet. Der Vorsteuerabzug ist nur aus dem strukturierten Teil möglich.

`erechnung anzeigen` zeigt bei einem ZUGFeRD-PDF immer den Inhalt des eingebetteten XML, nicht das Bild. Mit `erechnung extrahieren` holen Sie das XML als eigene Datei heraus.

## Aufbewahrung nach Rn. 60

Laut Rn. 60 des BMF-Schreibens vom 15.10.2025 muss ein Unternehmer ein Doppel jeder ein- und ausgehenden Rechnung acht Jahre aufbewahren (§ 14b Abs. 1 UStG). Die Frist beginnt mit dem Ende des Jahres, in dem die Rechnung ausgestellt wurde.

| Frage | Antwort laut BMF-Schreiben vom 15.10.2025 |
| --- | --- |
| Wie lange? | acht Jahre (Rn. 60, § 14b Abs. 1 UStG, § 147 Abs. 3 AO in der Fassung des Bürokratieentlastungsgesetzes IV) |
| In welcher Form? | im empfangenen Format, zumindest der strukturierte Teil unversehrt in seiner ursprünglichen Form (Rn. 60, UStAE 14b.1) |
| Muss es maschinell auswertbar bleiben? | ja, für die Finanzverwaltung (UStAE 14b.1) |
| Reicht ein Ausdruck oder eine HTML-Ansicht? | nein, sie ersetzt das Original nicht |
| Muss das Archiv GoBD-konform sein? | umsatzsteuerlich ist eine Speicherung außerhalb eines GoBD-konformen Systems allein kein Verstoß (Rn. 60); für andere Zwecke gelten die GoBD (Rn. 61) |

Die FAQ auf e-rechnung-bund.de nennt an einer Stelle noch "10 Jahre". Das ist durch das Bürokratieentlastungsgesetz IV überholt; nach § 27 Abs. 40 UStG gilt die Frist von acht Jahren für alle Rechnungen, deren Frist am 31.12.2024 noch nicht abgelaufen war. Für Bücher und Jahresabschlüsse bleiben es zehn Jahre.

Das Werkzeug ist keine Archivlösung. Es liefert mit `--bericht` den Prüfbericht, den Sie zusammen mit der Originaldatei ablegen. Mehr in [E-Rechnung archivieren](./e-rechnung-archivieren.md).

## BMF-Schreiben in der Praxis: Beispiele aus dem Rechnungseingang

Die Beispiele nutzen die Standardrechnung aus [beispiele/01_standard](../../beispiele/01_standard/xrechnung_ubl.xml) und daraus abgeleitete, absichtlich fehlerhafte Fassungen.

### Beispiel 1: Geschäftsregelfehler nach Rn. 6b, fehlendes BT-10

In dieser XRechnung fehlt die Zeile mit der Käuferreferenz:

```xml
<cbc:BuyerReference>BH-2026-0815</cbc:BuyerReference>
```

```bash
erechnung validieren ohne_bt10.xml
```

```text
ohne_bt10.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-DE-15: [BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BR-DE-15: Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.
```

Das ist genau das Beispiel aus Rn. 6b. Laut Rn. 35a ist dieser Fehler umsatzsteuerlich unbeachtlich, weil BT-10 keine Pflichtangabe nach § 14 Abs. 4 UStG ist. Im B2B genügt laut BMF-FAQ ein Platzhalter wie "-". Behörden brauchen dagegen die Leitweg-ID in BT-10, siehe [Leitweg-ID](./leitweg-id.md).

### Beispiel 2: Dieselbe Rechnung als EN 16931 ohne BT-10

```bash
erechnung validieren en16931_ohne_bt10.xml
```

```text
en16931_ohne_bt10.xml: EN 16931 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (UBL Invoice), 0 Fehler, 0 Warnungen
```

Hier ist nur die Kennung in BT-24 auf `urn:cen.eu:en16931:2017` geändert. Die Pflicht für BT-10 kommt aus der XRechnung (Regel BR-DE-15), nicht aus der EN 16931. Das zeigt, warum das BMF solche Fehler von den Pflichtangaben trennt.

### Beispiel 3: Formatfehler nach Rn. 6a, Datum im falschen Format

```bash
erechnung validieren datum_falsch.xml
```

```text
datum_falsch.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  XSD: Element '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueDate': '15.10.2026' is not a valid value of the atomic type 'xs:date'.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-14-4-3: Rechnungsdatum fehlt (BT-2, § 14 Abs. 4 Nr. 3 UStG).
```

UBL verlangt das Datum als `2026-10-15`. Die Datei verletzt das XML-Schema, also die technischen Vorgaben der Syntax. Nach der Faustregel oben ist das ein Formatfehler im Sinne von Rn. 6a, die Datei wäre damit keine E-Rechnung.

### Beispiel 4: Formatfehler nach Rn. 6a, kein wohlgeformtes XML

```bash
erechnung validieren abgeschnitten.xml
```

```text
abgeschnitten.xml: unbekannt
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-LESEN: Kein wohlgeformtes XML: Couldn't find end of Start Tag CompanyID line 31, line 31, column 23 (<string>, line 31)
```

Die Datei ist mitten im XML abgeschnitten, etwa durch einen fehlerhaften Download. Die offizielle Prüfung kann gar nicht erst starten, der Exit-Code ist 2. Bitten Sie den Absender, die Datei neu zu schicken.

### Beispiel 5: Geschäftsregelfehler mit Bezug zur Pflichtangabe Steuerbetrag

```bash
erechnung validieren steuer_falsch.xml
```

```text
steuer_falsch.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 3 Fehler, 0 Warnungen
  FEHLER  BR-CO-15: [BR-CO-15]-Invoice total amount with VAT (BT-112) = Invoice total amount without VAT (BT-109) + Invoice total VAT amount (BT-110).
  FEHLER  BR-CO-17: [BR-CO-17]-VAT category tax amount (BT-117) = VAT category taxable amount (BT-116) x (VAT category rate (BT-119) / 100), rounded to two decimals.
  FEHLER  BR-S-09: [BR-S-09]-The VAT category tax amount (BT-117) in a VAT breakdown (BG-23) where VAT category code (BT-118) is "Standard rated" shall equal the VAT category taxable amount (BT-116) multiplied by the VAT category rate (BT-119).
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-STEUERSATZ: S 19 %: Steuer 302.91 auf Basis 1689.00 ergibt nicht 320.91.
  FEHLER  VP-BRUTTO: Bruttobetrag BT-112 2009.91 ist nicht Netto + Steuer = 1991.91.
```

Der Steuerbetrag wurde von 320,91 EUR auf 302,91 EUR geändert. Das ist das zweite Beispiel aus Rn. 6b: Der Steuerbetrag stimmt rechnerisch nicht mit dem Steuersatz überein. Weil der Steuerbetrag eine Pflichtangabe ist, ist das ein Inhaltsfehler nach Rn. 35a.

### Beispiel 6: Inhaltsfehler, den keine Validierung findet

```bash
erechnung validieren steuersatz_7.xml
```

```text
steuersatz_7.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
```

```bash
erechnung lesen steuersatz_7.xml
```

```text
...
     1        12 HUR  Beratung Einführung E-Rechnung                     1.440,00 EUR
     2         1 MON  Softwarelizenz Rechnungseingang (Monat)              249,00 EUR
USt:          S (Regelsteuersatz oder ermäßigter Satz) 7 %: 118,23 EUR auf 1.689,00 EUR
...
```

Die Beratungsleistung ist hier mit 7 % statt 19 % abgerechnet, die Beträge passen aber zusammen. Technisch ist die Datei gültig. Ob der Steuersatz stimmt, prüft keine Geschäftsregel; genau diesen Fall nennt Rn. 35a. Die fachliche Prüfung bleibt Ihre Aufgabe.

### Beispiel 7: Bei einer ZUGFeRD-Rechnung das maßgebliche XML ansehen

```bash
erechnung extrahieren rechnung.pdf -o rechnung_aus_pdf.xml
erechnung anzeigen rechnung.pdf -o rechnung.html
```

```text
factur-x.xml aus rechnung.pdf gespeichert als rechnung_aus_pdf.xml
Ansicht geschrieben: rechnung.html
```

Ausschnitt aus dem extrahierten XML, BT-24 mit der Kennung des Profils EN 16931:

```xml
<ram:GuidelineSpecifiedDocumentContextParameter>
  <ram:ID>urn:cen.eu:en16931:2017</ram:ID>
</ram:GuidelineSpecifiedDocumentContextParameter>
```

Die HTML-Ansicht zeigt die Daten aus diesem XML. Das brauchen Sie, um nach UStAE 14.4 Abs. 3 den maßgeblichen Teil zu prüfen, statt dem PDF-Bild zu vertrauen.

### Beispiel 8: Prüfbericht für eine ungültige Rechnung

```bash
erechnung validieren ohne_bt10.xml --bericht prüfberichte
```

Auszug aus dem abgelegten Bericht:

```json
{
  "offiziell": {
    "szenario": "EN16931 XRechnung (UBL Invoice)",
    "akzeptiert": false,
    "konfiguration": "xrechnung-3.0.2-validator-configuration-2026-08-31",
    "hinweis": "",
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

Auch ein negativer Bericht ist nützlich: Er belegt, wann Sie einen Fehler festgestellt haben, etwa bevor Sie den Lieferanten um Korrektur bitten.

## Schritt für Schritt: Eingangsrechnungen nach dem BMF-Schreiben prüfen

1. Speichern Sie jede eingehende Rechnung unverändert in einem Ordner, zum Beispiel `eingang/2026-10/`.
2. Prüfen Sie den Ordner und legen Sie Berichte ab: `erechnung validieren eingang/2026-10/* --bericht prüfberichte/2026-10`.
3. Bei Exit-Code 0 sind alle Dateien technisch gültig. Bei 1 ist mindestens eine ungültig, bei 2 war mindestens eine nicht prüfbar (etwa ein reines PDF oder kaputtes XML).
4. Ordnen Sie Fehler ein: Formatfehler bedeuten "keine E-Rechnung" (Rn. 6a). Ein `BR-DE-15` allein ist umsatzsteuerlich unbeachtlich (Rn. 35a). Fehler bei Beträgen und Steuern betreffen Pflichtangaben.
5. Öffnen Sie jede Rechnung mit `erechnung anzeigen DATEI -o DATEI.html` und prüfen Sie fachlich: Leistung, Zeitraum, Steuersatz, Beträge. Bei ZUGFeRD gilt das XML, nicht das PDF-Bild.
6. Bitten Sie bei Format- und Inhaltsfehlern den Lieferanten um eine korrigierte E-Rechnung.
7. Legen Sie Original und Prüfbericht gemeinsam ab und bewahren Sie beide acht Jahre auf (Rn. 60).

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Jeden Validierungsfehler als "keine E-Rechnung" werten | Rechnungen mit nur `BR-DE-15` werden abgelehnt oder nicht gebucht | Rn. 6a und 6b unterscheiden; Geschäftsregelfehler zu BT-10 sind laut Rn. 35a umsatzsteuerlich unbeachtlich |
| "GÜLTIG" als fachliche Freigabe verstehen | falscher Steuersatz wird gebucht | Validierung ersetzt die Prüfpflicht nicht (Rn. 35a), Inhalt fachlich prüfen |
| ZUGFeRD-PDF nach dem Bild prüfen | Betrag im PDF weicht vom XML ab | XML mit `erechnung anzeigen` oder `erechnung extrahieren` ansehen (UStAE 14.4 Abs. 3) |
| Pflichtangaben nur im PDF-Anhang oder per Link | Validierung meldet fehlende Felder, oder Angaben fehlen im XML | alle Pflichtangaben in den strukturierten Teil, Anhänge nur ergänzend (Rn. 35) |
| Validierungsbericht nicht aufheben | kein Nachweis, wann und womit geprüft wurde | `--bericht ORDNER` verwenden und neben dem Original ablegen |
| Mit zehn Jahren Aufbewahrung rechnen | unnötig lange Speicherung von Rechnungen | acht Jahre nach § 14b Abs. 1 UStG und Rn. 60; Bücher und Jahresabschlüsse weiter zehn Jahre |
| Original nach der Prüfung umbenennen oder neu speichern | Prüfsumme im Bericht passt nicht mehr | Original unverändert lassen; umbenennen ändert die Prüfsumme nicht, neu speichern schon |

## Häufige Fragen

### Was steht im BMF-Schreiben zur E-Rechnung?

Das BMF-Schreiben vom 15.10.2024 regelt die Einführung der E-Rechnung ab 01.01.2025 mit Definitionen, Formaten und Übergangsregelungen. Das Schreiben vom 15.10.2025 ändert es und ergänzt vor allem Formatfehler (Rn. 6a), Geschäftsregelfehler (Rn. 6b), Rechtsfolgen und Validierung (Rn. 35a) sowie die Aufbewahrung von acht Jahren (Rn. 60).

### Welches BMF-Schreiben zur E-Rechnung ist aktuell?

Maßgeblich ist das BMF-Schreiben vom 15.10.2024 in der Fassung, die das BMF-Schreiben vom 15.10.2025 ergänzt und geändert hat. Beide gelten zusammen für Umsätze nach dem 31.12.2024.

### Ist eine Rechnung ohne BT-10 eine gültige E-Rechnung?

Umsatzsteuerlich ja, solange alle Pflichtangaben stimmen: Laut Rn. 35a ist ein fehlendes BT-10 umsatzsteuerlich unbeachtlich. Technisch ist eine XRechnung ohne BT-10 aber ungültig (BR-DE-15). Bei Rechnungen an Behörden ist BT-10 zwingend, weil dort die Leitweg-ID steht.

### Was ist der Unterschied zwischen Formatfehler und Geschäftsregelfehler?

Ein Formatfehler verletzt die Syntax oder deren technische Vorgaben, die Datei ist dann laut Rn. 6a keine E-Rechnung. Ein Geschäftsregelfehler verletzt eine inhaltliche Regel des Formats (Rn. 6b) und ist nur dann umsatzsteuerlich relevant, wenn er eine Pflichtangabe betrifft (Rn. 35a).

### Muss ich den Validierungsbericht aufbewahren?

Eine ausdrückliche Pflicht nennt das BMF-Schreiben nicht, laut Rn. 35a bietet es sich aber zum Nachweis an. Mit `erechnung validieren --bericht ORDNER` entsteht je Datei ein Bericht mit Zeitpunkt, Regelversion und SHA-256-Prüfsumme.

### Was gilt, wenn PDF und XML einer ZUGFeRD-Rechnung abweichen?

Dann gehen die Daten des XML vor (UStAE 14.4 Abs. 3). Weicht der Bildteil bei Rechnungsangaben ab, kann er laut UStAE 14c.1 Abs. 4a eine weitere Rechnung sein, für die § 14c UStG zu prüfen ist; den Einzelfall klären Sie mit der Steuerberatung.

### Wie lange muss ich E-Rechnungen aufbewahren?

Acht Jahre, laut Rn. 60 und § 14b Abs. 1 UStG, gerechnet ab dem Ende des Ausstellungsjahres. Aufzubewahren ist mindestens der strukturierte Teil unversehrt in seiner ursprünglichen Form.

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [E-Rechnung Pflicht: Fristen und Ausnahmen](./e-rechnung-pflicht.md)
- [E-Rechnung prüfen: Validator mit den offiziellen Regeln](./e-rechnung-validator.md)
- [E-Rechnung Fehlermeldungen beheben](./e-rechnung-fehlermeldungen.md)
- [E-Rechnung archivieren](./e-rechnung-archivieren.md)
- [ZUGFeRD: Format und Profile](./zugferd.md)
- Beispieldateien: [Standardrechnung UBL](../../beispiele/01_standard/xrechnung_ubl.xml), [Prüfergebnis](../../beispiele/01_standard/validierung_ubl.txt), [Übersicht](../../beispiele/README.md)

Quellen: [BMF-Schreiben vom 15.10.2025 (PDF)](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/Umsatzsteuer-Anwendungserlass/2025-10-15-einfuehrung-obligatorische-e-rechnung.pdf?__blob=publicationFile), [BMF-FAQ zur E-Rechnung](https://www.bundesfinanzministerium.de/Content/DE/FAQ/e-rechnung.html), [§ 14 UStG](https://www.gesetze-im-internet.de/ustg_1980/__14.html), [§ 14b UStG](https://www.gesetze-im-internet.de/ustg_1980/__14b.html), [§ 27 UStG](https://www.gesetze-im-internet.de/ustg_1980/__27.html), [§ 147 AO](https://www.gesetze-im-internet.de/ao_1977/__147.html).
