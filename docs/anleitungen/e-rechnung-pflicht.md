# E-Rechnung Pflicht: ab wann, für wen und welche Übergangsfristen gelten

Die E-Rechnung-Pflicht gilt in Deutschland in zwei Stufen: Seit dem 01.01.2025 müssen alle inländischen Unternehmer E-Rechnungen empfangen können, ohne Ausnahme und auch als Kleinunternehmer. Für den Versand gelten nach § 27 Abs. 38 UStG Übergangsfristen: Für Umsätze aus 2025 und 2026 sind Papier und (mit Zustimmung des Empfängers) PDF noch erlaubt, wenn die Rechnung bis Ende 2026 übermittelt wird, 2027 nur noch bei einem Vorjahresumsatz bis 800.000 EUR oder für EDI-Verfahren, und ab dem 01.01.2028 ist die E-Rechnung für alle inländischen B2B-Umsätze Pflicht.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Geschäftsführung, Buchhaltung und Steuerkanzleien. Technische Beispiele stehen weiter unten und sind optional.

## Das Wichtigste in Kürze

- Seit dem 01.01.2025 muss jeder inländische Unternehmer E-Rechnungen empfangen können, ein normales E-Mail-Postfach genügt dafür.
- Beim Versand dürfen Sie Umsätze aus 2025 und 2026 noch mit Papierrechnung oder (mit Zustimmung des Empfängers) als PDF abrechnen, wenn die Rechnung bis zum 31.12.2026 übermittelt wird.
- Für Umsätze aus 2027 gilt diese Erleichterung nur noch, wenn Ihr Gesamtumsatz im Vorjahr nicht mehr als 800.000 EUR betrug und die Rechnung bis zum 31.12.2027 übermittelt wird; EDI-Verfahren bleiben mit Zustimmung unabhängig vom Umsatz bis Ende 2027 zulässig.
- Ab dem 01.01.2028 ist die E-Rechnung für alle Umsätze zwischen inländischen Unternehmern Pflicht.
- Kleinbetragsrechnungen bis 250 EUR, Fahrausweise und Rechnungen von Kleinunternehmern dürfen dauerhaft sonstige Rechnungen sein; Rechnungen an Privatpersonen (B2C) sind nicht betroffen.
- Mit `erechnung validieren` und `erechnung anzeigen` prüfen und lesen Sie eingehende XRechnung- und ZUGFeRD-Dateien lokal, ohne Java und ohne Upload.

## Ab wann gilt die E-Rechnung-Pflicht? Der Zeitstrahl

Maßgeblich sind zwei Zeitpunkte: wann der Umsatz ausgeführt wurde und wann die Rechnung übermittelt wird. Eine sonstige Rechnung für einen Umsatz aus 2025 oder 2026 muss bis zum 31.12.2026 beim Empfänger sein, eine für einen Umsatz aus 2027 bis zum 31.12.2027 (§ 27 Abs. 38 UStG). Wer einen Dezember-Umsatz erst im Januar abrechnet, braucht dafür unter Umständen schon eine E-Rechnung. Die Tabelle fasst die Fristen nach § 27 Abs. 38 UStG und die BMF-FAQ zusammen.

| Zeitraum | Empfang | Versand an inländische Unternehmer | Rechtsgrundlage |
| --- | --- | --- | --- |
| seit 27.11.2020 | - | Auftragnehmer des Bundes schicken E-Rechnungen an Bundesbehörden (B2G) | E-Rechnungsverordnung des Bundes (ERechV) |
| ab 01.01.2025 | Pflicht für alle inländischen Unternehmer | neue Definition der E-Rechnung gilt, Übergangsfristen beginnen | § 14 UStG (Wachstumschancengesetz) |
| 01.01.2025 - 31.12.2026 | Pflicht | Papierrechnung immer zulässig, sonstiges elektronisches Format (z. B. PDF) nur mit Zustimmung des Empfängers; Rechnung bis 31.12.2026 übermittelt | § 27 Abs. 38 UStG |
| 01.01.2027 - 31.12.2027 | Pflicht | E-Rechnung Pflicht, außer der Gesamtumsatz (§ 19 Abs. 2 UStG) im Vorjahr lag bei höchstens 800.000 EUR und die Rechnung wird bis 31.12.2027 übermittelt; EDI nach Empfehlung 94/820/EG mit Zustimmung unabhängig vom Umsatz | § 27 Abs. 38 UStG |
| ab 01.01.2028 | Pflicht | E-Rechnung für alle inländischen B2B-Umsätze | § 14 Abs. 2 UStG |

Hinweis zur 800.000-EUR-Grenze: Das Gesetz stellt auf den Gesamtumsatz nach § 19 Abs. 2 UStG des Rechnungsausstellers im Vorjahr ab. Die BMF-FAQ spricht vereinfacht vom "Vorjahresumsatz". Für 2027 zählt also der Gesamtumsatz 2026.

## E-Rechnung Pflicht 2025: Empfangen müssen alle

Eine E-Rechnung ist eine Rechnung als strukturierter Datensatz nach § 14 Abs. 1 Satz 3 UStG, Details in [Was ist eine E-Rechnung?](./was-ist-eine-e-rechnung.md). Praktisch heißt das: Die Rechnung kommt als XML-Datei (XRechnung) oder als PDF mit eingebettetem XML (ZUGFeRD, Factur-X).

Die Empfangspflicht gilt seit dem 01.01.2025 für alle inländischen Unternehmer, auch für:

- Kleinunternehmer nach § 19 UStG,
- Land- und Forstwirte,
- Unternehmer mit ausschließlich steuerfreien Umsätzen, zum Beispiel Wohnungsvermieter.

Was Sie dafür brauchen, ist wenig. Laut BMF-Schreiben vom 15.10.2025 (UStAE 14.1) genügt der Empfang per E-Mail, ein gesondertes Postfach ist nicht nötig. Die BMF-FAQ schreibt keinen Übermittlungsweg vor: E-Mail, Schnittstelle, Download aus einem Portal oder sogar ein USB-Stick sind möglich.

Empfangen allein reicht im Alltag aber nicht. Eine XRechnung ist eine reine XML-Datei, die man ohne Hilfsmittel kaum lesen kann. Sie brauchen also ein Programm, das die Datei anzeigt, und idealerweise eines, das sie prüft. Wie das mit diesem Repo geht, zeigt der Abschnitt [Empfangspflicht praktisch erfüllen](#empfangspflicht-praktisch-erfüllen-lesen-prüfen-anzeigen).

## E-Rechnung Pflicht 2026 und 2027: die Übergangsfristen beim Versand

Beim Versand ist der Übergang gestaffelt. Die Übergangsfristen nach § 27 Abs. 38 UStG erlauben für eine begrenzte Zeit noch sonstige Rechnungen, also Papier oder PDF.

| Umsatz ausgeführt / Rechnung übermittelt bis | Zulässig statt E-Rechnung |
| --- | --- |
| 01.01.2025 - 31.12.2026 / bis 31.12.2026 | Papierrechnung immer; sonstige elektronische Formate (z. B. PDF) nur mit Zustimmung des Empfängers |
| 01.01.2027 - 31.12.2027 / bis 31.12.2027 | Papier oder (mit Zustimmung) sonstiges elektronisches Format, wenn der Gesamtumsatz (§ 19 Abs. 2 UStG) des Ausstellers im Vorjahr nicht mehr als 800.000 EUR betrug |
| 01.01.2027 - 31.12.2027 / ausgestellt bis 31.12.2027 | EDI-Verfahren (Empfehlung 94/820/EG), das nicht EN-16931-konform ist, mit Zustimmung des Empfängers, unabhängig vom Umsatz |
| ab 01.01.2028 | keine Erleichterung mehr: E-Rechnung für alle inländischen B2B-Umsätze |

Zwei Rechenbeispiele für 2027:

- Ein Handwerksbetrieb hatte 2026 einen Gesamtumsatz von 750.000 EUR. Er darf Umsätze aus 2027 noch als Papierrechnung oder (mit Zustimmung) als PDF abrechnen, wenn er die Rechnung bis zum 31.12.2027 übermittelt.
- Eine Agentur hatte 2026 einen Gesamtumsatz von 900.000 EUR. Für Umsätze ab dem 01.01.2027 muss sie E-Rechnungen ausstellen, außer sie nutzt mit Zustimmung ein EDI-Verfahren.

Wichtig: Die Übergangsfristen betreffen nur den Versand. Freiwillig E-Rechnungen zu schicken, ist schon heute erlaubt und braucht bei Pflichtumsätzen keine Zustimmung des Empfängers (§ 14 Abs. 1 Satz 5 UStG).

## EDI-Sonderregel: was nach 2027 gilt

EDI steht für elektronischen Datenaustausch, etwa im Format EDIFACT. Für EDI gibt es zwei Regeln:

1. Bis zum 31.12.2027 darf ein EDI-Verfahren nach Empfehlung 94/820/EG weiterverwendet werden, auch wenn es nicht EN-16931-konform ist. Voraussetzung ist die Zustimmung des Empfängers. Auf den Umsatz kommt es nicht an.
2. Dauerhaft, also auch nach 2027, bleiben vereinbarte Formate wie EDIFACT zulässig, wenn sie die richtige und vollständige Extraktion der umsatzsteuerlichen Angaben in ein EN-16931-konformes oder interoperables Format ermöglichen (§ 14 Abs. 1 Satz 6 Nr. 2 UStG).

Ob Ihr konkretes EDI-Verfahren die zweite Bedingung erfüllt, klären Sie mit Ihrem EDI-Dienstleister und der Steuerberatung.

## E-Rechnung ab 2028: Pflicht für alle B2B-Umsätze

Ab dem 01.01.2028 enden alle Übergangsfristen. Jede Rechnung über einen Umsatz an einen anderen inländischen Unternehmer für dessen Unternehmen muss dann eine E-Rechnung sein (§ 14 Abs. 2 Satz 2 Nr. 1 UStG), außer es greift eine der dauerhaften Ausnahmen.

Wer nach Ablauf der Übergangsfrist trotz Pflicht eine sonstige Rechnung ausstellt, stellt laut BMF-Schreiben vom 15.10.2025 (UStAE 15.2a Abs. 1) keine ordnungsmäßige Rechnung aus. Die Rechnung lässt sich durch eine nachträgliche E-Rechnung berichtigen (UStAE 15.2a Abs. 7). Für den Vorsteuerabzug des Kunden reicht nach UStAE 15.2a Abs. 1a in der Regel trotzdem eine inhaltlich richtige und vollständige sonstige Rechnung; ob das im Einzelfall genügt, klären Sie mit der Steuerberatung.

## E-Rechnung Pflicht Ausnahmen: wann keine E-Rechnung nötig ist

Für einige Rechnungen gilt die Ausstellungspflicht nie. Die Empfangspflicht bleibt davon unberührt.

| Fall | E-Rechnung beim Versand nötig? | Grundlage |
| --- | --- | --- |
| Kleinbetragsrechnung bis 250 EUR brutto | nein, sonstige Rechnung immer zulässig | § 33 UStDV |
| Fahrausweis | nein, sonstige Rechnung immer zulässig | § 34 UStDV |
| Rechnung eines Kleinunternehmers | nein, sonstige Rechnung immer zulässig | § 34a UStDV |
| Rechnung an Privatpersonen (B2C) | nein, nicht betroffen | BMF-FAQ |
| Leistung an juristische Personen, die nicht Unternehmer sind (z. B. viele Vereine, staatliche Einrichtungen) | nein, nicht erfasst | BMF-FAQ |
| bestimmte Leistungen an Endverbraucher im Zusammenhang mit einem Grundstück | nein, nicht erfasst | BMF-FAQ |
| steuerfreie Umsätze nach § 4 Nr. 8 bis 29 UStG | nein, keine Rechnungspflicht, außer bei Option zur Steuerpflicht nach § 9 UStG | BMF-FAQ, BMF-Schreiben vom 15.10.2025, Rn. 17 |
| Leistender ohne Ansässigkeit im Inland | nein, nicht erfasst | BMF-FAQ |

Bei Kleinbetragsrechnungen, Fahrausweisen und Rechnungen von Kleinunternehmern ist laut BMF-Schreiben vom 15.10.2025 (UStAE 14.5 Abs. 14) auch keine fortlaufende Rechnungsnummer nötig. Wer will, darf trotzdem eine E-Rechnung schicken.

Keine Ausnahme sind dagegen:

- Gutschriften (Abrechnung durch den Leistungsempfänger),
- Fälle des § 13b UStG (Reverse Charge), wenn beide Seiten im Inland ansässig sind (BMF-Schreiben vom 15.10.2025, Rn. 17),
- Barzahlungen über 250 EUR, zum Beispiel ein Geschäftsessen oder ein Einkauf im Baumarkt.

## Was ist eine sonstige Rechnung?

Eine sonstige Rechnung ist nach § 14 Abs. 1 Satz 4 UStG "eine Rechnung, die in einem anderen elektronischen Format oder auf Papier übermittelt wird". Dazu zählen laut BMF-Schreiben vom 15.10.2025 (UStAE 14.1 Abs. 2) "auch alle nicht strukturierten elektronischen Dateien, zum Beispiel PDF-Dateien ohne integrierte Datensätze".

Drei Fälle sind in der Praxis wichtig:

- Ein PDF ohne eingebettetes XML ist eine sonstige Rechnung, auch wenn es am Bildschirm wie eine E-Rechnung aussieht.
- Eine Datei mit Formatfehlern, die nicht den zulässigen Syntaxen entspricht, ist laut BMF-Schreiben vom 15.10.2025, Rn. 6a, ebenfalls eine sonstige Rechnung.
- ZUGFeRD in den Profilen MINIMUM und BASIC WL gilt nicht als E-Rechnung, obwohl die Datei XML enthält (UStAE 14.1 Abs. 14).

Welche Formate als E-Rechnung zählen:

| Format | E-Rechnung nach § 14 UStG? |
| --- | --- |
| XRechnung (UBL oder CII) | ja |
| ZUGFeRD ab 2.0.1, Profile BASIC, EN 16931 (COMFORT), EXTENDED, XRECHNUNG | ja |
| ZUGFeRD MINIMUM und BASIC WL | nein |
| andere EN-16931-konforme europäische Formate | ja (UStAE 14.1 Abs. 12) |
| PDF ohne XML, Word-Datei, Scan, Papier | nein, sonstige Rechnung |

Mehr dazu in [Was ist eine E-Rechnung?](./was-ist-eine-e-rechnung.md) und [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md).

## Was muss ich wann tun? Entscheidungshilfe nach Unternehmensart

Die Tabelle zeigt, was für typische Unternehmensarten beim Empfang und beim Versand an inländische Unternehmer gilt. Sie ersetzt keine Prüfung im Einzelfall; Grenzfälle klären Sie mit der Steuerberatung.

| Unternehmensart | Empfang | Versand 2025-2026 | Versand 2027 | Versand ab 2028 |
| --- | --- | --- | --- | --- |
| Gesamtumsatz im Vorjahr über 800.000 EUR | E-Rechnungen seit 01.01.2025 empfangen können | Papier oder (mit Zustimmung) PDF erlaubt | E-Rechnung, außer EDI mit Zustimmung | E-Rechnung |
| Gesamtumsatz im Vorjahr bis 800.000 EUR | E-Rechnungen seit 01.01.2025 empfangen können | Papier oder (mit Zustimmung) PDF erlaubt | Papier oder (mit Zustimmung) PDF weiter erlaubt | E-Rechnung |
| Kleinunternehmer (§ 19 UStG) | E-Rechnungen seit 01.01.2025 empfangen können | sonstige Rechnung erlaubt (§ 34a UStDV) | sonstige Rechnung erlaubt | sonstige Rechnung weiter erlaubt, E-Rechnung freiwillig |
| nur Kunden, die Privatpersonen sind (B2C) | Eingangsrechnungen von Lieferanten als E-Rechnung empfangen können | keine E-Rechnung nötig | keine E-Rechnung nötig | keine E-Rechnung nötig |
| nur steuerfreie Umsätze nach § 4 Nr. 8 bis 29 UStG (z. B. Wohnungsvermietung) | E-Rechnungen seit 01.01.2025 empfangen können | keine Rechnungspflicht für diese Umsätze, außer bei Option zur Steuerpflicht nach § 9 UStG | wie 2025-2026 | wie 2025-2026 |
| Unternehmen mit EDI (z. B. EDIFACT) | E-Rechnungen seit 01.01.2025 empfangen können | EDI mit Zustimmung | EDI mit Zustimmung, unabhängig vom Umsatz | nur EDI, das die vollständige Extraktion nach EN 16931 erlaubt |
| Auftragnehmer von Bundesbehörden (B2G) | wie oben | E-Rechnung nach ERechV seit 27.11.2020, grundsätzlich XRechnung mit Leitweg-ID; Direktaufträge bis 1.000 EUR ausgenommen | wie 2025-2026 | wie 2025-2026 |

Zum B2G-Fall: Die ERechV gilt neben dem UStG, ein Rangverhältnis gibt es nicht. Direktaufträge bis 1.000 EUR Auftragswert sind laut e-rechnung-bund.de ausgenommen. Die Länder haben eigene Regeln und Portale. Details stehen in [Leitweg-ID](./leitweg-id.md).

Was alle Unternehmen jetzt tun sollten:

1. Eine Adresse für den Empfang festlegen und Lieferanten mitteilen, zum Beispiel `rechnungseingang@example.com`.
2. Ein Programm einrichten, das XRechnung und ZUGFeRD anzeigt und prüft.
3. E-Rechnungen im Ursprungsformat aufbewahren, laut BMF-Schreiben vom 15.10.2025, Rn. 60, acht Jahre.
4. Den eigenen Gesamtumsatz des Vorjahres prüfen, um zu wissen, ob 2027 oder 2028 der Stichtag für den Versand ist. Ob diese Regel für Ihr Unternehmen gilt, klärt Ihre Steuerberatung.

## Empfangspflicht praktisch erfüllen: lesen, prüfen, anzeigen

Dieses Repo enthält das Kommandozeilen-Werkzeug `erechnung`. Es liest XRechnung (UBL und CII) und ZUGFeRD/Factur-X, prüft sie mit den offiziellen KoSIT-Regeln und zeigt sie als HTML an. Es braucht Python 3.10 oder neuer, aber kein Java. Rechnungsdaten verlassen Ihren Rechner nicht.

Installation (einmalig):

```bash
pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
```

Beim ersten Prüfen lädt das Paket die KoSIT-Prüfregeln von GitHub, prüft deren SHA-256-Summe und legt sie in `~/.cache/erechnung` ab. Danach läuft alles offline. Welche Regelversion aktiv ist, zeigt:

```bash
erechnung konfiguration
```

```text
KoSIT-Prüfkonfiguration: xrechnung-3.0.2-validator-configuration-2026-08-31
Ordner: /Users/.../.cache/erechnung/xrechnung-3.0.2-validator-configuration-2026-08-31
```

Der Ablauf im Rechnungseingang hat drei Schritte: Datei lesen, prüfen, für Menschen anzeigen. Die folgenden Beispiele nutzen einen Ordner `eingang/` mit vier Dateien: einer ZUGFeRD-Rechnung, einer XRechnung, einer Kleinunternehmer-Rechnung und einem eingescannten PDF.

Was der Exit-Code von `erechnung validieren` bedeutet:

| Exit-Code | Bedeutung |
| --- | --- |
| 0 | alle Dateien gültig nach den KoSIT-Regeln |
| 1 | mindestens eine Datei ungültig |
| 2 | Prüfung nicht möglich, z. B. kein Rechnungs-XML gefunden oder Regeln nicht verfügbar |

Grenzen des Werkzeugs: Es ist kein Postfach und kein Peppol-Zugangspunkt, es holt also keine Rechnungen ab und verschickt keine. Es ist auch keine Archivlösung. Den Empfangsweg (E-Mail, Portal) und die Ablage organisieren Sie selbst.

## Rechnungseingang prüfen: Beispiele mit dem Werkzeug erechnung

### Beispiel 1: Eine ZUGFeRD-Rechnung vom Lieferanten lesen

```bash
erechnung lesen eingang/2026-10-15_nordlicht.pdf
```

```text
Datei:        eingang/2026-10-15_nordlicht.pdf
Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
Nummer:       RE-2026-0001 vom 15.10.2026
Verkäufer:    Nordlicht Beispiel GmbH, 20095 Hamburg, USt-IdNr. DE123456789
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

Das brauchen Sie, wenn Sie schnell sehen wollen, ob eine Datei überhaupt eine E-Rechnung ist und was drinsteht. Die Zeile `E-Rechnung:` beantwortet genau die Frage aus § 14 UStG.

### Beispiel 2: Den ganzen Rechnungseingang prüfen

```bash
erechnung validieren eingang/*
```

```text
eingang/2026-10-15_buchhandlung.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
eingang/2026-10-15_nordlicht.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
eingang/2026-10-16_grafikdesign.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
eingang/2026-10-16_scan.pdf: unbekannt
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-LESEN: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
```

Das brauchen Sie einmal am Tag oder vor dem Buchen. Drei Dateien sind gültige E-Rechnungen. Das Scan-PDF ist eine sonstige Rechnung; der Exit-Code ist hier 2, weil es nichts zu prüfen gab. Bis Ende 2026 darf Ihr Lieferant mit Ihrer Zustimmung so abrechnen, danach je nach seinem Umsatz und der Art der Rechnung nicht mehr.

### Beispiel 3: Prüfberichte zum Aufbewahren ablegen

```bash
erechnung validieren eingang/* --bericht prüfberichte/2026-10
```

```text
eingang/2026-10-15_buchhandlung.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
  Prüfbericht: prüfberichte/2026-10/2026-10-15_buchhandlung.xml.7fba94710c3a.validierungsbericht.json
eingang/2026-10-15_nordlicht.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
  Prüfbericht: prüfberichte/2026-10/2026-10-15_nordlicht.pdf.fff3d8c9aba4.validierungsbericht.json
...
```

Je Datei entsteht eine JSON-Datei mit Zeitpunkt, Regelversion und SHA-256-Prüfsumme der geprüften Rechnung. Laut BMF-Schreiben vom 15.10.2025, Rn. 35a, bietet es sich zum Nachweis an, den Validierungsbericht aufzubewahren. Mehr dazu in [BMF-Schreiben zur E-Rechnung](./bmf-schreiben-e-rechnung.md).

### Beispiel 4: Eine E-Rechnung für Menschen anzeigen

```bash
erechnung anzeigen eingang/2026-10-15_nordlicht.pdf -o ansichten/2026-10-15_nordlicht.html
```

```text
Ansicht geschrieben: ansichten/2026-10-15_nordlicht.html
```

Die HTML-Datei öffnen Sie im Browser. Sie zeigt den Inhalt des XML, nicht das Bild im PDF. Das ist Absicht: Bei Abweichungen zwischen XML und Bildteil ist laut BMF-Schreiben vom 15.10.2025 (UStAE 14.4 Abs. 3) der strukturierte Teil maßgebend, und das BMF empfiehlt, den XML-Teil selbst zu visualisieren. Der Zielordner muss vorher existieren.

### Beispiel 5: Eine XRechnung mit der offiziellen KoSIT-Ansicht anzeigen

```bash
erechnung anzeigen eingang/2026-10-15_buchhandlung.xml --offiziell -o ansichten/2026-10-15_buchhandlung.html
```

```text
Ansicht geschrieben: ansichten/2026-10-15_buchhandlung.html
```

Das brauchen Sie, wenn Sie die Darstellung der KoSIT-Visualisierung bevorzugen, die viele Behörden und Programme verwenden. Ohne `--offiziell` nutzt das Werkzeug eine eigene, schlankere Ansicht.

### Beispiel 6: Erkennen, dass ein PDF keine E-Rechnung ist

```bash
erechnung lesen eingang/2026-10-16_scan.pdf
```

```text
eingang/2026-10-16_scan.pdf: Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
```

Das brauchen Sie, wenn ein Lieferant behauptet, er schicke schon E-Rechnungen. Ein PDF ohne eingebettetes XML ist eine sonstige Rechnung (UStAE 14.1 Abs. 2).

### Beispiel 7: Rechnung eines Kleinunternehmers erkennen

```bash
erechnung lesen eingang/2026-10-16_grafikdesign.pdf
```

```text
Datei:        eingang/2026-10-16_grafikdesign.pdf
Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
...
Verkäufer:    Grafikdesign Lena Beispiel, 50667 Köln, Steuernummer 214/5678/1234
...
USt:          E (Steuerbefreit, z. B. § 4 UStG oder Kleinunternehmer § 19 UStG) 0 %: 0,00 EUR auf 850,00 EUR
Brutto:       850,00 EUR
```

Kleinunternehmer dürfen sonstige Rechnungen schicken (§ 34a UStDV), hier hat die Absenderin freiwillig eine E-Rechnung erstellt. Im XML steht der Hinweis in BT-120:

```xml
<cbc:TaxExemptionReason>Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.</cbc:TaxExemptionReason>
```

Die Datei stammt aus [beispiele/07_kleinunternehmer](../../beispiele/07_kleinunternehmer/xrechnung_ubl.xml). Mehr in [E-Rechnung für Kleinunternehmer](./e-rechnung-kleinunternehmer.md).

## Schritt für Schritt: Rechnungseingang für die E-Rechnung-Pflicht einrichten

Für die Schritte 2 bis 5 brauchen Sie ein Terminal (macOS: Terminal, Windows: PowerShell), Programmierkenntnisse aber nicht. Wer kein Terminal nutzen möchte, zeigt E-Rechnungen mit dem kostenlosen [Quba-Viewer](https://github.com/ZUGFeRD/quba-viewer) an (Programm mit Fenster für Windows, macOS und Linux) und lässt die Prüfung von der Buchhaltungssoftware oder der Steuerkanzlei erledigen; die Schritte 1, 6, 7 und 8 gelten trotzdem.

1. Legen Sie fest, wie E-Rechnungen ankommen. Eine bestehende E-Mail-Adresse genügt; teilen Sie sie Ihren Lieferanten mit.
2. Installieren Sie Python 3.10 oder neuer und `pipx`, dann das Werkzeug mit dem Befehl aus dem Abschnitt oben.
3. Speichern Sie eingehende Rechnungen (XML- und PDF-Anhänge) in einen Ordner, zum Beispiel `eingang/`.
4. Prüfen Sie den Ordner mit `erechnung validieren eingang/* --bericht prüfberichte/2026-10`. Gültige Dateien sind E-Rechnungen nach den offiziellen Regeln.
5. Öffnen Sie jede Rechnung zum fachlichen Prüfen mit `erechnung anzeigen DATEI -o ansichten/DATEI.html` im Browser. Prüfen Sie wie bisher, ob Leistung, Betrag und Steuer stimmen; die technische Prüfung ersetzt das nicht (BMF-Schreiben vom 15.10.2025, Rn. 35a).
6. Bei ungültigen Dateien bitten Sie den Lieferanten um eine korrigierte E-Rechnung. Was einzelne Fehlermeldungen bedeuten, steht in [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md).
7. Bewahren Sie die Originaldatei unverändert und den Prüfbericht acht Jahre auf (§ 14b Abs. 1 UStG). Die Ansicht als HTML ist keine Rechnung und ersetzt das Original nicht.
8. Prüfen Sie Ihren Gesamtumsatz 2026 (§ 19 Abs. 2 UStG): Lag er über 800.000 EUR, müssen Sie Umsätze ab 01.01.2027 als E-Rechnung abrechnen, sonst ab 01.01.2028. Ob diese Regel für Ihr Unternehmen gilt, klärt Ihre Steuerberatung. Wie Sie dann selbst E-Rechnungen erzeugen, zeigt [E-Rechnung erstellen](./e-rechnung-erstellen.md).

## Ausblick: XRechnung 4.0, Meldesystem und ViDA

Diese Punkte ändern an den Fristen oben nichts, kommen aber auf Unternehmen zu.

| Thema | Stand laut Quellen | Sicherheit |
| --- | --- | --- |
| XRechnung 3.0 | bleibt laut xeinkauf.de mindestens bis 31.07.2027 in Kraft | offiziell |
| XRechnung 4.0 | Vorversion 4.0.0 seit 15.09.2026, nicht für den Produktivbetrieb; finale Fassung laut xeinkauf.de voraussichtlich Frühjahr 2027, auf Basis EN 16931-1:2026 | Termin voraussichtlich |
| ViDA (VAT in the Digital Age) | in Kraft seit 14.04.2025; Meldepflichten für grenzüberschreitende B2B-Umsätze ab 01.07.2030 laut EU-Kommission | offiziell |
| deutsches Meldesystem | die BMF-FAQ kündigt ein transaktionsbezogenes Meldesystem an, das Gesetz kommt "zu gegebener Zeit" | offiziell, ohne Termin |
| Zeitplan Meldesystem | laut Fachpresse am 22.09.2026 vorgestellt: Gesetzgebung 2027, freiwillige Pilotphase Anfang 2029, Pflicht ab 01.07.2030 | unsicher, noch keine BMF-Veröffentlichung und kein Gesetzentwurf |

Das Werkzeug prüft derzeit gegen XRechnung 3.0.2. XRechnung 4.0 unterstützt es noch nicht.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| PDF für eine E-Rechnung halten | `erechnung lesen` meldet "kein eingebettetes Rechnungs-XML" | Lieferanten um XRechnung oder ZUGFeRD (mindestens Profil BASIC) bitten |
| ZUGFeRD MINIMUM oder BASIC WL akzeptieren | Vorprüfung meldet `VP-FORMAT`, Profil enthält nicht alle Pflichtangaben | Lieferanten um Profil EN 16931 oder XRECHNUNG bitten |
| Nur das PDF-Bild einer ZUGFeRD-Rechnung prüfen | Beträge im Bild und im XML weichen ab, gebucht wird das Falsche | XML mit `erechnung anzeigen` darstellen, maßgebend ist der strukturierte Teil |
| 800.000-EUR-Grenze am Umsatz des laufenden Jahres messen | falscher Stichtag für den Versand | Gesamtumsatz nach § 19 Abs. 2 UStG des Vorjahres zugrunde legen, im Zweifel mit der Steuerberatung klären |
| Empfangspflicht mit Versandpflicht verwechseln | Kleinunternehmer glauben, sie seien nicht betroffen | Empfangen müssen alle seit 01.01.2025, nur der Versand hat Ausnahmen |
| Nur die HTML-Ansicht archivieren | Original fehlt bei einer Prüfung durch das Finanzamt | Originaldatei unverändert aufbewahren, die Ansicht ersetzt das Original nicht |
| Zielordner für `anzeigen -o` fehlt | `Fehler: [Errno 2] No such file or directory` | Ordner vorher anlegen, z. B. `mkdir ansichten` |

## Häufige Fragen

### Ab wann ist die E-Rechnung Pflicht?

Der Empfang ist seit dem 01.01.2025 Pflicht für alle inländischen Unternehmer. Der Versand wird schrittweise Pflicht: ab 01.01.2027 für Unternehmen mit mehr als 800.000 EUR Gesamtumsatz im Vorjahr, ab 01.01.2028 für alle (§ 27 Abs. 38 UStG). Für die Übergangsfrist zählt auch, wann die Rechnung übermittelt wird: Eine sonstige Rechnung über einen Umsatz aus 2026 muss bis zum 31.12.2026 beim Empfänger sein.

### Was gilt bei der E-Rechnung Pflicht 2026?

Im Jahr 2026 müssen Sie E-Rechnungen empfangen können, dürfen aber selbst noch Papierrechnungen oder, mit Zustimmung des Empfängers, PDF-Rechnungen schicken. Das gilt für alle Umsätze, die bis zum 31.12.2026 ausgeführt werden, wenn die Rechnung ebenfalls bis zum 31.12.2026 übermittelt wird.

### Was ändert sich bei der E-Rechnung ab 2027?

Ab dem 01.01.2027 müssen Unternehmen mit einem Gesamtumsatz von mehr als 800.000 EUR im Vorjahr E-Rechnungen verschicken. Kleinere Unternehmen dürfen 2027 noch Papier oder (mit Zustimmung) PDF nutzen, und EDI-Verfahren bleiben mit Zustimmung bis Ende 2027 erlaubt.

### Müssen Kleinunternehmer E-Rechnungen schreiben?

Nein, Kleinunternehmer dürfen dauerhaft sonstige Rechnungen ausstellen (§ 34a UStDV). Empfangen müssen sie E-Rechnungen aber seit dem 01.01.2025 wie alle anderen Unternehmer. Details in [E-Rechnung für Kleinunternehmer](./e-rechnung-kleinunternehmer.md).

### Brauche ich für den Empfang ein spezielles Postfach oder Peppol?

Nein, laut BMF-Schreiben vom 15.10.2025 genügt der Empfang per E-Mail, ein eigenes Postfach ist nicht nötig. Einen bestimmten Übermittlungsweg schreibt die BMF-FAQ nicht vor. Sie brauchen aber ein Programm, das die Datei lesbar anzeigt.

### Gilt die E-Rechnung-Pflicht auch für Rechnungen an Privatkunden?

Nein, Rechnungen an Privatpersonen (B2C) sind von der Pflicht nicht erfasst. Die Pflicht betrifft Umsätze zwischen inländischen Unternehmern für deren Unternehmen.

### Was passiert, wenn ich nach der Übergangsfrist noch PDF-Rechnungen schicke?

Dann stellen Sie laut BMF-Schreiben vom 15.10.2025 (UStAE 15.2a Abs. 1) keine ordnungsmäßige Rechnung aus. Sie können die Rechnung durch eine nachträgliche E-Rechnung berichtigen. Nach UStAE 15.2a Abs. 1a bleibt der Vorsteuerabzug Ihres Kunden bei einer inhaltlich richtigen und vollständigen sonstigen Rechnung in der Regel möglich. Welche Folgen das im Einzelfall für den Vorsteuerabzug Ihres Kunden hat, klären Sie mit der Steuerberatung.

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [Was ist eine E-Rechnung?](./was-ist-eine-e-rechnung.md)
- [E-Rechnung empfangen und lesen](./e-rechnung-empfangen.md)
- [E-Rechnung prüfen: Validator mit den offiziellen Regeln](./e-rechnung-validator.md)
- [BMF-Schreiben zur E-Rechnung: die wichtigen Randnummern](./bmf-schreiben-e-rechnung.md)
- [E-Rechnung für Kleinunternehmer](./e-rechnung-kleinunternehmer.md)
- [E-Rechnung archivieren](./e-rechnung-archivieren.md)
- Beispieldateien: [Übersicht](../../beispiele/README.md), [Standardrechnung als ZUGFeRD-PDF](../../beispiele/01_standard/zugferd_en16931.pdf)

Quellen: [§ 14 UStG](https://www.gesetze-im-internet.de/ustg_1980/__14.html), [§ 27 UStG](https://www.gesetze-im-internet.de/ustg_1980/__27.html), [BMF-FAQ zur E-Rechnung](https://www.bundesfinanzministerium.de/Content/DE/FAQ/e-rechnung.html), [BMF-Schreiben vom 15.10.2025 (PDF)](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/Umsatzsteuer-Anwendungserlass/2025-10-15-einfuehrung-obligatorische-e-rechnung.pdf?__blob=publicationFile), [XRechnung Versionen (xeinkauf.de)](https://xeinkauf.de/xrechnung/versionen-und-bundles/), [ViDA (EU-Kommission)](https://taxation-customs.ec.europa.eu/taxation/vat/vat-digital-age-vida_en).
