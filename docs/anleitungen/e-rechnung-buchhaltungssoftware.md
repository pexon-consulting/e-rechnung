# Lexware, sevdesk, SAP: E-Rechnung aus der Buchhaltungssoftware testen

Ob Lexware, sevdesk, SAP, DATEV oder ein anderes Programm wirklich gültige E-Rechnungen erzeugt, prüfen Sie mit einer Testrechnung: exportieren Sie sie als XML oder ZUGFeRD-PDF, lassen Sie mit `erechnung lesen` Format und Profil erkennen und prüfen Sie sie mit `erechnung validieren` gegen die offiziellen KoSIT-Regeln. Zeigt die Prüfung "GÜLTIG" und ist das Format eine XRechnung oder ein ZUGFeRD-Profil ab BASIC, erzeugt das Programm für diesen Fall eine E-Rechnung. Wiederholen Sie den Test für jede Rechnungsart, die Sie wirklich verschicken.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Buchhaltung und Geschäftsführung, die ihr Rechnungsprogramm testen wollen.

## Das Wichtigste in Kürze

- Eine E-Rechnung ist eine XRechnung oder ein ZUGFeRD-PDF ab Profil BASIC ([Was ist eine E-Rechnung?](./was-ist-eine-e-rechnung.md)). Ein PDF ohne eingebettetes XML ist keine E-Rechnung.
- Ein Hinweis "E-Rechnung" im Programm sagt nicht, welches Format und Profil herauskommt. Das sehen Sie erst an der exportierten Datei.
- `erechnung lesen` zeigt Format, Profil und Inhalt, `erechnung validieren` prüft mit den offiziellen KoSIT-Regeln. Beides läuft lokal, die Rechnungsdaten verlassen den Rechner nicht.
- ZUGFeRD MINIMUM und BASIC WL sind laut BMF keine E-Rechnungen. BASIC, EN 16931, EXTENDED und XRECHNUNG sind es.
- Laut BMF-Schreiben vom 15.10.2025 (Rn. 35a) darf sich ein Unternehmen bei Beachtung der Sorgfalt eines ordentlichen Kaufmanns auf das technische Ergebnis einer Validierung hinsichtlich Format und Geschäftsregeln verlassen. Inhaltliche Fehler wie ein falscher Steuersatz erkennt eine Validierung nicht immer; die eigene Prüfpflicht bleibt. Zum Nachweis bietet es sich laut BMF an, den Validierungsbericht aufzubewahren. `--bericht` legt ihn ab. Ob `e-rechnung` in Ihrem Fall als geeignete Validierungsanwendung gilt, entscheidet nicht das Werkzeug, sondern Sie mit Ihrer Steuerberatung.
- Die Angaben der Hersteller unten sind Zusammenfassungen ihrer Hilfeseiten, keine Bewertung. Sie ersetzen den Test mit einer eigenen Testrechnung nicht.

## Woran erkenne ich, ob mein Programm eine echte E-Rechnung erzeugt?

Entscheidend ist die Datei, nicht das Programm. Eine Rechnung ist eine E-Rechnung, wenn sie in einem strukturierten Format nach EN 16931 vorliegt. In Deutschland sind das vor allem XRechnung (reines XML) und ZUGFeRD (PDF/A-3 mit eingebettetem XML). Ein PDF, das nur gut aussieht, ist eine sonstige Rechnung.

Zwei Dinge müssen zusammenkommen:

1. **Das richtige Format und Profil.** Bei ZUGFeRD zählt das Profil:

| Format oder Profil | Datei | E-Rechnung nach BMF? |
| --- | --- | --- |
| XRechnung (UBL oder CII) | XML | ja |
| ZUGFeRD XRECHNUNG | PDF/A-3 mit XML | ja |
| ZUGFeRD EN 16931 (COMFORT) | PDF/A-3 mit XML | ja |
| ZUGFeRD EXTENDED | PDF/A-3 mit XML | ja |
| ZUGFeRD BASIC | PDF/A-3 mit XML | ja |
| ZUGFeRD BASIC WL | PDF/A-3 mit XML | nein |
| ZUGFeRD MINIMUM | PDF/A-3 mit XML | nein |
| PDF ohne XML | PDF | nein, sonstige Rechnung |

Quelle: UStAE 14.1 Abs. 14 in der Fassung des BMF-Schreibens vom 15.10.2025 ("ausgenommen die Profile MINIMUM und BASIC-WL").

2. **Keine Formatfehler.** Laut BMF-Schreiben vom 15.10.2025, Rn. 6a, ist eine Datei mit Formatfehlern keine E-Rechnung, sondern eine sonstige Rechnung. Geprüft wird das "mit einer geeigneten Validierungsanwendung". Verstöße gegen Geschäftsregeln (Rn. 6b), etwa ein fehlendes BT-10 in einer XRechnung, sind nach Rn. 35a umsatzsteuerlich unbeachtlich, solange die Pflichtangaben nach § 14 Abs. 4 UStG stimmen. Ein Empfänger, vor allem eine Behörde, kann so eine Rechnung trotzdem ablehnen. Was das im Einzelfall bedeutet, klären Sie mit der Steuerberatung.

## Welche Datei muss ich aus dem Programm exportieren?

Exportieren Sie genau die Datei, die Ihr Kunde bekommt. Nicht die Druckvorschau, nicht ein Screenshot, nicht ein PDF aus "Drucken als PDF".

| Sie verschicken | Exportieren Sie | Prüfen mit |
| --- | --- | --- |
| ZUGFeRD | das PDF aus dem E-Rechnungs-Versand oder -Download | `erechnung lesen RE-123.pdf` |
| XRechnung | die XML-Datei | `erechnung lesen RE-123.xml` |
| Upload in ein Behördenportal | die Datei, die Sie hochladen | `erechnung validieren RE-123.xml` |

Wenn Sie nicht wissen, ob das PDF ein XML enthält: `erechnung lesen` sagt es Ihnen. Mit `erechnung extrahieren` holen Sie das XML heraus, um es anzusehen oder weiterzugeben.

Tipp: Legen Sie für den Test einen Musterkunden an und schreiben Sie je Fall eine Testrechnung: Standardrechnung, gemischte Steuersätze, Gutschrift oder Rechnungskorrektur, Reverse Charge, Rechnung an eine Behörde. Jeder Fall nutzt andere Felder, und Fehler zeigen sich oft erst in einem davon. Fertige Vergleichsdateien liegen in [`beispiele/`](../../beispiele/README.md).

## Format und Profil erkennen mit `erechnung lesen`

`erechnung lesen` öffnet XML-Dateien und ZUGFeRD-PDFs und zeigt in der Zeile "Format", was die Datei ist, und in der Zeile "E-Rechnung", ob sie als E-Rechnung zählt.

```bash
erechnung lesen export/RE-2026-0001.pdf
```

```text
Datei:        export/RE-2026-0001.pdf
Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
Nummer:       RE-2026-0001 vom 15.10.2026
...
Brutto:       2.009,91 EUR
Zahlbetrag:   2.009,91 EUR, fällig 14.11.2026
Zahlung:      58 (SEPA-Überweisung) DE79000000001234567890
```

So lesen Sie die Zeile "Format":

| Ausgabe | Bedeutung |
| --- | --- |
| `XRechnung 3.0 (UBL)` oder `XRechnung 3.0 (CII)` | reine XRechnung |
| `ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)` | ZUGFeRD-PDF im Profil EN 16931 |
| `ZUGFeRD-Profil XRECHNUNG, XRechnung 3.0 (CII) (eingebettet als xrechnung.xml)` | ZUGFeRD-PDF mit XRechnung im Inneren |
| `CII Profil MINIMUM`, dazu `E-Rechnung: nein` | Profil ohne vollständige Pflichtangaben |
| "Das PDF enthält kein eingebettetes Rechnungs-XML." | reines PDF, keine E-Rechnung |

Vergleichen Sie danach die übrigen Zeilen mit der Rechnung im Programm: Nummer, Datum, Käufer, Steuersätze, Summen und IBAN. Bei Abweichungen zwischen PDF-Bild und XML ist laut BMF-Schreiben vom 15.10.2025 (UStAE 14.4 Abs. 3) der strukturierte Teil maßgebend.

## Gültigkeit prüfen mit `erechnung validieren`

`erechnung validieren` prüft erst das XML-Schema, dann die Schematron-Regeln der KoSIT für EN 16931 und XRechnung, so wie der KoSIT-Validator. Dazu kommt eine Vorprüfung mit eigenen Hinweisen (Codes mit `VP-`), etwa zu Pflichtangaben nach § 14 Abs. 4 UStG, Summen, IBAN und Leitweg-ID. Die Vorprüfung erklärt, sie ersetzt die offizielle Prüfung nicht.

| Exit-Code | Bedeutung |
| --- | --- |
| 0 | alle Dateien gültig |
| 1 | mindestens eine Datei ungültig |
| 2 | mindestens eine Datei ließ sich nicht prüfen, zum Beispiel ein PDF ohne XML |

Achten Sie in der Ausgabe auf das Szenario. "EN16931 XRechnung" heißt, die Datei wurde als XRechnung geprüft. "EN16931 (CII)" heißt, sie wurde gegen EN 16931 geprüft, ohne die zusätzlichen XRechnung-Regeln. Für B2B genügt ein EN-16931-konformes Format. Welche Formate eine Behörde annimmt, steht in ihren Vorgaben.

Grenzen: Das Werkzeug prüft das XML. Ob das PDF selbst PDF/A-3-konform ist, prüfen die KoSIT-Regeln nicht. ZUGFeRD BASIC und EXTENDED werden gegen EN 16931 geprüft, mit Hinweis. XRechnung 4.0 wird noch nicht unterstützt.

## Was die Hersteller zur E-Rechnung sagen

Die folgenden Angaben fassen die verlinkten Hilfeseiten und Ankündigungen der Hersteller zusammen, laut Hersteller (Stand Oktober 2026). Funktionen ändern sich mit Updates. Prüfen Sie Ihre eigene Version immer mit einer Testrechnung.

### Lexware Office

Laut Hersteller (Stand Oktober 2026) erstellt Lexware Office nach Aktivierung der E-Rechnungsfunktion für Kontakte, die als Firma angelegt sind, automatisch eine ZUGFeRD-Rechnung (PDF mit eingebetteter XML-Datei). Eine XRechnung (reine XML-Datei) entsteht nur, wenn der Kunde eine Behörde ist und Leitweg-ID und Lieferantennummer hinterlegt sind ([E-Rechnungsfunktion aktivieren](https://help.lexware.de/de-form/articles/547939-die-e-rechnungsfunktion-aktivieren)). Eine Checkliste in der Vorschau zeigt fehlende Angaben, laut Hersteller unterstützt die E-Rechnung dort nur das Netto-Rechenverfahren ([Checkliste](https://help.lexware.de/de-form/articles/548939-checkliste-bei-der-erstellung-von-e-rechnungen)).

Welches ZUGFeRD-Profil herauskommt, nennen diese Seiten nicht. Das zeigt Ihnen `erechnung lesen`.

### Lexware faktura+auftrag

Laut Hersteller (Stand Oktober 2026) versendet Lexware faktura+auftrag Belege per E-Mail "im XRechnungs- sowie den ZUGFeRD-Formaten Basic, EN16931 und Extended (eingeschränkt)" und zeigt und validiert empfangene E-Rechnungen ([Produktvergleich 2026](https://partner.haufe-lexware.com/fileadmin/user_upload/Lexware-faktura-auftrag-2026_Produktvergleich.pdf)).

### sevdesk

Laut Hersteller (Stand Oktober 2026) aktivieren Sie die E-Rechnung in sevdesk in der Rechnung oder im Kontakt. Beim Versand übermittelt "Per E-Mail versenden" das Dokument im ZUGFeRD-Format, "Nur XML senden" im XRechnung-Format. Ohne Leitweg-ID setzt sevdesk als Kundenreferenz die `0`, die USt-IdNr. muss in den Unternehmenseinstellungen hinterlegt sein ([E-Rechnung versenden](https://hilfe.sevdesk.de/de/articles/10079526-e-rechnung-versenden)).

Ein ZUGFeRD-Profil nennt die Seite nicht. Prüfen Sie es mit `erechnung lesen`.

### DATEV

Laut Hersteller (Stand Oktober 2026) behandelt das Lernvideo zu DATEV Auftragswesen next das "Versenden von E-Rechnungen im Format ZUGFeRD2.x und X-Rechnung" ([DATEV Auftragswesen next](https://www.datev.de/web/de/datev-shop/wissensvermittlung/lernvideos/78770-datev-auftragswesen-next-verkaufsbelege-einfach-und-effizient-erstellen/)). Für den Eingang beschreibt DATEV in Unternehmen online / Belege online die Übernahme von ZUGFeRD und XRechnung mit Validierung auf EN-16931-Konformität und Visualisierung der XML-Daten ([Belege online](https://www.datev.de/web/de/shop/produkt-details/belege-online-95157)).

Wie Sie geprüfte Eingangsrechnungen als Buchungsstapel nach DATEV bringen, steht in [DATEV und E-Rechnung](./datev-e-rechnung.md).

### SAP

Laut Hersteller (Stand Oktober 2026) erzeugt SAP S/4HANA im Prozess "Germany eInvoice (E-Mail)" im eDocument Cockpit elektronische Dokumente im Standard XRechnung/CII, der auch die Grundlage für das ZUGFeRD-Profil XRECHNUNG ist. Sie werden über einen Cloud-Service validiert und als XML-Datei oder als PDF/A-3 per E-Mail verschickt; dafür sind Einrichtung und Konfiguration nötig ([What's New in SAP S/4HANA 1909 SPS08](https://help.sap.com/doc/b870b6ebcd2e4b5890f16f4b06827064/1909.008/en-US)). Für empfangene Rechnungen nennt SAP die Validierung von XRechnung in CII und UBL mit SAP Document and Reporting Compliance ([What's New in SAP S/4HANA Cloud 2408.4](https://help.sap.com/doc/ce01d82756b947a1a043a5d5a3204226/2408.10/en-US/WN_CE2408.4_EN.pdf)).

Welche Funktionen in Ihrem System aktiv sind, hängt von Produkt, Release und Konfiguration ab. Lassen Sie sich aus dem Testsystem eine XML-Datei geben und prüfen Sie sie wie unten beschrieben.

### ELSTER

ELSTER ist das Portal der Steuerverwaltung. In den offiziellen Quellen, auf die sich diese Anleitung stützt, kommt ELSTER bei der E-Rechnung an einer Stelle vor: Für die Rechnungseingangsplattform des Bundes (OZG-RE) können Sie sich laut [e-rechnung-bund.de](https://www.e-rechnung-bund.de/faq/) kostenlos registrieren, auch über "Mein Unternehmenskonto" (ELSTER). Mehr dazu in [Leitweg-ID und E-Rechnung an Behörden](./leitweg-id.md).

### Andere Programme

Für Warenwirtschaft, Branchensoftware, Rechnungs-Apps und eigene Exporte gilt dieselbe Methode: Testrechnung exportieren, `erechnung lesen`, `erechnung validieren`. Eine Herstellerangabe ersetzt diesen Test nicht.

## Testrechnung aus Lexware, sevdesk oder SAP prüfen: Beispiele

Die Dateien unten liegen in einem Ordner `export/`. RE-2026-0001 und RE-2026-0002 stammen aus den Beispielen des Repos, die übrigen sind daraus abgeleitet und absichtlich fehlerhaft, so wie man es bei Exporten antrifft.

### Beispiel 1: Prüfen, ob ein PDF überhaupt eine E-Rechnung ist

```bash
erechnung lesen export/RE-2026-0003.pdf
```

```text
export/RE-2026-0003.pdf: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
```

Exit-Code 1. Das passiert, wenn das PDF über die normale Druckfunktion statt über den E-Rechnungs-Export entstanden ist oder die E-Rechnungsfunktion nicht aktiv war.

### Beispiel 2: ZUGFeRD-Profil erkennen

```bash
erechnung lesen export/RE-2026-0007.pdf
```

```text
Datei:        export/RE-2026-0007.pdf
Format:       ZUGFeRD-Profil XRECHNUNG, XRechnung 3.0 (CII) (eingebettet als xrechnung.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
...
```

Brauchen Sie, wenn eine Behörde ZUGFeRD im Profil XRECHNUNG verlangt und Sie wissen wollen, ob Ihr Programm genau das liefert.

### Beispiel 3: Profil MINIMUM erkennen

```bash
erechnung validieren export/RE-2026-0004.xml
```

```text
export/RE-2026-0004.xml: CII Profil MINIMUM
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario kein Szenario, 1 Fehler, 0 Warnungen
  FEHLER  SZENARIO: Kein passendes Prüfszenario. Erwartet wird UBL Invoice/CreditNote oder CII mit einer Spezifikationskennung (BT-24) für XRechnung 3.0 oder EN 16931.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-FORMAT: CII Profil MINIMUM: Dieses ZUGFeRD-Profil enthält nicht alle Pflichtangaben und gilt nicht als E-Rechnung nach § 14 UStG. Mindestens Profil BASIC, besser EN 16931 verwenden.
```

Exit-Code 1. Stellen Sie im Programm ein höheres Profil ein, falls es die Wahl anbietet.

### Beispiel 4: Fehlender Kontakt in einer XRechnung

```bash
erechnung validieren export/RE-2026-0005.xml
```

```text
export/RE-2026-0005.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-DE-2: [BR-DE-2] Die Gruppe "SELLER CONTACT" (BG-6) muss übermittelt werden.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BR-DE-2: Kontakt des Verkäufers unvollständig: XRechnung verlangt Name, Telefon und E-Mail (BT-41, BT-42, BT-43).
```

Ein häufiger Fall: Die Firmenstammdaten im Programm enthalten keinen Ansprechpartner mit Telefon und E-Mail. Tragen Sie ihn einmal nach und exportieren Sie neu.

### Beispiel 5: Rechenfehler in den Summen

```bash
erechnung validieren export/RE-2026-0006.xml
```

```text
export/RE-2026-0006.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-CO-15: [BR-CO-15]-Invoice total amount with VAT (BT-112) = Invoice total amount without VAT (BT-109) + Invoice total VAT amount (BT-110).
```

Hier weicht der Bruttobetrag um 1 Cent von Netto plus Steuer ab. Prüfen Sie dann die Einstellungen zu Rundung und Rechenverfahren. Lexware Office verlangt laut eigener Hilfe für E-Rechnungen das Netto-Rechenverfahren, um solche Abweichungen zu vermeiden (siehe unten).

### Beispiel 6: Den ganzen Testexport auf einmal prüfen und Prüfberichte ablegen

```bash
erechnung validieren export/* --bericht prüfberichte
```

```text
export/RE-2026-0001.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
  Prüfbericht: prüfberichte/RE-2026-0001.pdf.fff3d8c9aba4.validierungsbericht.json
export/RE-2026-0002.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
  Prüfbericht: prüfberichte/RE-2026-0002.xml.29ccd409852b.validierungsbericht.json
export/RE-2026-0003.pdf: unbekannt
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-LESEN: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
  Prüfbericht: prüfberichte/RE-2026-0003.pdf.b3e44df802e4.validierungsbericht.json
...
export/RE-2026-0007.pdf: ZUGFeRD-Profil XRECHNUNG, XRechnung 3.0 (CII)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (CII), 0 Fehler, 0 Warnungen
  Prüfbericht: prüfberichte/RE-2026-0007.pdf.cd43a857fe0f.validierungsbericht.json
```

Exit-Code 2, weil RE-2026-0003 sich nicht prüfen ließ. Jeder Prüfbericht enthält Zeitpunkt, Regelversion und SHA-256 der Datei. Bei Ihren eigenen Dateien weichen die Prüfsummen im Dateinamen der Berichte ab. Ein Ausschnitt:

```json
{
  "validiert_am": "2026-10-15T22:25:53+00:00",
  "werkzeug": "e-rechnung 0.1.0",
  "regeln": "xrechnung-3.0.2-validator-configuration-2026-08-31",
  "sha256": "fff3d8c9aba4e7589d8f582d84425a1c1580e26729ea61ee30f5387f54e39436",
  "datei": "export/RE-2026-0001.pdf",
  "gueltig": true
}
```

### Beispiel 7: XML aus dem PDF holen und als Ansicht öffnen

```bash
erechnung extrahieren export/RE-2026-0001.pdf -o RE-2026-0001.xml
erechnung anzeigen export/RE-2026-0001.pdf -o RE-2026-0001.html
```

```text
factur-x.xml aus export/RE-2026-0001.pdf gespeichert als RE-2026-0001.xml
Ansicht geschrieben: RE-2026-0001.html
```

Öffnen Sie die HTML-Ansicht neben dem PDF. So sehen Sie, ob das XML dieselben Beträge enthält wie das Bild, das Ihr Kunde sieht.

### Beispiel 8: Ergebnis maschinell auswerten

```bash
erechnung validieren --json export/RE-2026-0005.xml
```

```text
{
  "datei": "export/RE-2026-0005.xml",
  "format": {
    "syntax": "UBL-Invoice",
    "spezifikation": "urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0",
    "bezeichnung": "XRechnung 3.0 (UBL)",
    "ist_e_rechnung": true,
    ...
  },
  "gueltig": false,
  ...
}
```

Nützlich, wenn Ihre IT jeden Export automatisch prüfen soll, bevor er rausgeht.

## Schritt für Schritt: Ihr Programm testen

1. **Werkzeug installieren.** Mit Python 3.10 oder neuer, kein Java nötig:
   `pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"`.
   Beim ersten Prüfen lädt das Werkzeug einmal die KoSIT-Regeln, danach läuft alles offline.
2. **E-Rechnungsfunktion im Programm einschalten.** Wo das geht, steht in der Hilfe des Herstellers (Links oben).
3. **Stammdaten vervollständigen.** Eigene Anschrift, USt-IdNr. oder Steuernummer, Bankverbindung, Ansprechpartner mit Telefon und E-Mail, eine elektronische Adresse (zum Beispiel eine E-Mail-Adresse).
4. **Testkunden anlegen.** Einen Firmenkunden mit Anschrift und E-Mail. Für den Behördenfall zusätzlich eine Leitweg-ID, zum Beispiel den Testwert `04011000-12345-03`.
5. **Testrechnungen schreiben und exportieren.** Je Fall eine Rechnung, als XML oder ZUGFeRD-PDF, in einen Ordner `export/`.
6. **Format prüfen.** `erechnung lesen export/<datei>`: Steht bei "E-Rechnung" ein "ja" und ist das Profil das, was Ihr Kunde erwartet?
7. **Gültigkeit prüfen.** `erechnung validieren export/* --bericht prüfberichte`. Jede Datei sollte "GÜLTIG" zeigen. Lesen Sie auch die Zeilen der Vorprüfung.
8. **Inhalt vergleichen.** Beträge, Steuersätze, Datum und IBAN aus `erechnung lesen` mit der Rechnung im Programm vergleichen.
9. **Fehler beheben.** Mit der Tabelle unten und der Anleitung [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md). Bleibt ein Fehler, obwohl alle Daten gepflegt sind, schicken Sie die Datei und die Fehlermeldung an den Support des Herstellers.
10. **Nach Updates wiederholen.** Ein Programm-Update kann den Export ändern. Prüfen Sie dann wieder eine Testrechnung je Fall.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| PDF ohne XML exportiert | `lesen`: "Das PDF enthält kein eingebettetes Rechnungs-XML." | E-Rechnungsfunktion aktivieren und den E-Rechnungs-Export statt "Drucken" nutzen |
| Profil MINIMUM oder BASIC WL | `VP-FORMAT`, "E-Rechnung: nein" | Profil BASIC oder besser EN 16931 einstellen |
| Kontakt des Verkäufers fehlt | `BR-DE-2` "Die Gruppe "SELLER CONTACT" (BG-6) muss übermittelt werden." | Ansprechpartner mit Telefon und E-Mail in den Firmenstammdaten |
| BT-10 leer in XRechnung | `BR-DE-15` | Leitweg-ID bei Behörden, sonst Bestellnummer, Referenz oder `-` |
| Elektronische Adresse fehlt | `PEPPOL-EN16931-R020` (Verkäufer) oder `PEPPOL-EN16931-R010` (Käufer) | E-Mail-Adresse im Firmen- und Kundenstamm |
| Zahlungsangaben fehlen | `BR-DE-1`, Gruppe "PAYMENT INSTRUCTIONS" (BG-16) | Zahlungsart und Bankverbindung hinterlegen |
| Rundungsdifferenz | `BR-CO-15` oder andere `BR-CO`-Regeln | Rechenverfahren und Rundung im Programm prüfen |
| Unbekannte Spezifikationskennung | `SZENARIO`: "Kein passendes Prüfszenario." | Exporteinstellung auf XRechnung oder ZUGFeRD ab BASIC ändern |
| ZUGFeRD EN 16931 an eine Behörde, die XRechnung verlangt | Szenario "EN16931 (CII)" statt "EN16931 XRechnung" | XRechnung oder ZUGFeRD XRECHNUNG exportieren |

## Häufige Fragen

### Wie prüfe ich, ob Lexware gültige E-Rechnungen erstellt?

Exportieren Sie eine Testrechnung aus Lexware und prüfen Sie sie mit `erechnung lesen` und `erechnung validieren`. Laut Hersteller erstellt Lexware Office für Firmenkontakte ZUGFeRD und für Behörden mit Leitweg-ID XRechnung. Welches Profil Ihre Version wirklich schreibt, zeigt erst die Datei.

### Ist eine Rechnung aus sevdesk automatisch eine E-Rechnung?

Nein, nur wenn die E-Rechnung aktiviert ist und das Ergebnis ein strukturiertes Format ist. Laut Hersteller wird beim Versand "Per E-Mail versenden" ZUGFeRD und bei "Nur XML senden" XRechnung übermittelt. Prüfen Sie die exportierte Datei mit `erechnung lesen`.

### Kann SAP XRechnung erzeugen?

Laut SAP-Dokumentation erzeugt SAP S/4HANA im eDocument Cockpit XRechnung im CII-Format und verschickt sie als XML oder PDF/A-3, nach Einrichtung. Ob das in Ihrem System aktiv ist, hängt von Release und Konfiguration ab. Prüfen Sie eine Datei aus dem Testsystem.

### Kann ich mit ELSTER E-Rechnungen schreiben?

Dafür nennen die offiziellen Quellen dieser Anleitung keine Funktion. ELSTER kommt dort bei der E-Rechnung nur als Anmeldeweg vor: Für die OZG-RE des Bundes können Sie sich laut e-rechnung-bund.de auch über "Mein Unternehmenskonto" registrieren.

### Reicht die Prüfung im Programm selbst?

Manche Programme prüfen Pflichtangaben vor dem Export, Lexware Office beschreibt dafür zum Beispiel eine Checkliste. Eine zweite Prüfung mit den offiziellen KoSIT-Regeln zeigt, ob die Datei auch beim Empfänger als gültig erkannt wird, und liefert einen Prüfbericht zum Aufbewahren.

### Was mache ich, wenn mein Programm nur PDF kann?

Ein PDF ohne XML ist keine E-Rechnung. Sie können aus den Rechnungsdaten mit `erechnung erstellen` eine XRechnung oder ein ZUGFeRD-PDF erzeugen oder ein XML mit `erechnung zugferd` in Ihr PDF einbetten. Wie, steht in [PDF in ZUGFeRD umwandeln](./pdf-in-zugferd-umwandeln.md) und [E-Rechnung erstellen](./e-rechnung-erstellen.md).

### Muss ich jede Rechnung prüfen oder reicht ein Test?

Ein Test je Rechnungsart zeigt, ob das Programm grundsätzlich richtig exportiert. Weil Fehler oft an einzelnen Stammdaten hängen, lohnt sich eine Stichprobe nach Updates und bei neuen Kunden. Mit `erechnung validieren export/*` prüfen Sie viele Dateien in einem Lauf.

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [E-Rechnung prüfen: Validator mit den offiziellen Regeln](./e-rechnung-validator.md)
- [E-Rechnung Fehlermeldungen: BR-DE-15, BR-CO-26 und andere](./e-rechnung-fehlermeldungen.md)
- [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md)
- [ZUGFeRD: Format, Profile und Versionen](./zugferd.md)
- [DATEV und E-Rechnung](./datev-e-rechnung.md)
- [Leitweg-ID und E-Rechnung an Behörden](./leitweg-id.md)
- Beispiele zum Vergleichen: [Übersicht](../../beispiele/README.md), [ZUGFeRD-PDF Standardrechnung](../../beispiele/01_standard/zugferd_en16931.pdf), [XRechnung UBL](../../beispiele/01_standard/xrechnung_ubl.xml)
