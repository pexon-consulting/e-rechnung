# XRechnung oder ZUGFeRD: Unterschied und welches Format Sie brauchen

XRechnung oder ZUGFeRD: An Behörden schicken Sie eine XRechnung mit Leitweg-ID, im B2B sind beide Formate zulässig, ZUGFeRD ab Version 2.0.1 in jedem Profil außer MINIMUM und BASIC WL. Der Unterschied liegt im Aufbau: Eine XRechnung ist eine reine XML-Datei, eine ZUGFeRD-Rechnung ist ein PDF/A-3, in das ein XML eingebettet ist, so dass Menschen sie ohne Zusatzprogramm lesen können.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil von [E-Rechnung in Python](../../README.md).

## Das Wichtigste in Kürze

- Eine XRechnung ist eine XML-Datei nach dem deutschen Standard der KoSIT, in UBL 2.1 oder CII D16B.
- Eine ZUGFeRD-Rechnung ist eine Hybridrechnung: strukturierter XML-Teil und lesbarer PDF-Teil in einer Datei (UStAE 14.1 Abs. 14).
- Laut UStAE 14.1 Abs. 14 ist ZUGFeRD ab Version 2.0.1 eine zulässige E-Rechnung, ausgenommen die Profile MINIMUM und BASIC WL.
- Bei einer ZUGFeRD-Rechnung ist der XML-Teil maßgebend, nicht das PDF (BMF-FAQ).
- Das ZUGFeRD-Profil XRECHNUNG verbindet beides: ein PDF, in dem eine vollständige XRechnung als `xrechnung.xml` steckt.
- Mit `erechnung erstellen` entstehen XRechnung UBL, XRechnung CII, ZUGFeRD und ZUGFeRD-XRECHNUNG aus derselben Eingabedatei.

## Unterschied zwischen XRechnung und ZUGFeRD

Eine XRechnung ist eine Rechnung als XML-Datei nach dem Standard XRechnung, einer deutschen Spezialisierung (CIUS) der EN 16931. Eine ZUGFeRD-Rechnung ist ein PDF/A-3 mit einer eingebetteten XML-Datei in der Syntax CII. Factur-X ist der französische Name desselben Formats; ZUGFeRD 2.5.2 und Factur-X 1.09.2 sind technisch identisch.

| Merkmal | XRechnung | ZUGFeRD |
| --- | --- | --- |
| Aufbau | reine XML-Datei | PDF/A-3 mit eingebettetem XML (Hybrid) |
| Lesbarkeit für Menschen | nur mit Viewer | PDF in jedem PDF-Programm lesbar |
| Maßgeblicher Teil | das XML | das XML, nicht das PDF (BMF-FAQ) |
| Herausgeber | KoSIT | FeRD (Factur-X: gleiche Spezifikation für Frankreich) |
| Aktuelle Version | 3.0.2 | 2.5.2 = Factur-X 1.09.2, gültig ab 01.09.2026 |
| Syntax | UBL 2.1 oder UN/CEFACT CII D16B | CII (ab ZUGFeRD 2.4 auf Basis D22B, rückwärtskompatibel zu D16B) |
| Profile | CIUS, dazu Extension und CVD | MINIMUM, BASIC WL, BASIC, EN 16931, EXTENDED, XRECHNUNG |
| Kennung in BT-24 | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` | je Profil, zum Beispiel `urn:cen.eu:en16931:2017` für EN 16931 |
| Käuferreferenz BT-10 | Pflicht (BR-DE-15) | im Profil EN 16931 nicht Pflicht |
| B2G (Behörden) | Standard, Leitweg-ID in BT-10 | Annahme mit der Rechnungseingangsplattform klären |
| B2B | zulässig | zulässig ab 2.0.1, außer MINIMUM und BASIC WL |
| Dateigröße (Beispiel 01) | 5.643 Byte (UBL), 8.065 Byte (CII) | 28.164 Byte (PDF mit Lesefassung) |
| Name des XML im PDF | - | `factur-x.xml`, beim Profil XRECHNUNG `xrechnung.xml` |
| Offizielle Prüfung | KoSIT-Validator (Java), `erechnung validieren` | XML wie bei XRechnung, PDF/A-3 zum Beispiel mit Mustang (veraPDF) |

Die Dateigrößen stammen aus Beispiel 5 unten. Das PDF ist größer, weil es neben dem XML eine Seite mit Schriften und Layout enthält. Für die Bundesportale ist das unkritisch: Die OZG-RE nimmt laut [e-rechnung-bund.de](https://www.e-rechnung-bund.de/faq/) bis 10 MB per E-Mail und bis 11 MB in der Weberfassung an.

## Welche ZUGFeRD-Profile sind E-Rechnungen?

Ein ZUGFeRD-Profil legt fest, wie viele Felder das XML enthält. Nicht jedes Profil reicht für eine E-Rechnung nach § 14 UStG.

| Profil | BT-24 im XML | E-Rechnung laut BMF? |
| --- | --- | --- |
| MINIMUM | `urn:factur-x.eu:1p0:minimum` | nein |
| BASIC WL | `urn:factur-x.eu:1p0:basicwl` | nein |
| BASIC | `urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic` | ja |
| EN 16931 (COMFORT) | `urn:cen.eu:en16931:2017` | ja |
| EXTENDED | `urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended` | ja |
| XRECHNUNG | `urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0` | ja |

Wörtlich heißt es im UStAE 14.1 Abs. 14 in der Fassung des BMF-Schreibens vom 15.10.2025: "ZUGFeRD ab der Version 2.0.1 - ausgenommen die Profile MINIMUM und BASIC-WL - beruht auf der Normenreihe EN 16931 und fällt somit unter die zulässigen E-Rechnungs-Formate." Mehr zu den Profilen steht in [ZUGFeRD: Format, Profile und Versionen](./zugferd.md).

## ZUGFeRD-Profil XRECHNUNG: die Mischform

Das Profil XRECHNUNG ist ein ZUGFeRD-PDF, dessen XML eine vollständige XRechnung in CII ist. Es trägt in BT-24 dieselbe Kennung wie eine XRechnung und muss deshalb auch alle BR-DE-Regeln erfüllen, also zum Beispiel BT-10. Das eingebettete XML heißt `xrechnung.xml` statt `factur-x.xml`.

Mit diesem Werkzeug lässt sich das direkt nachprüfen. Das aus dem PDF geholte XML ist Byte für Byte gleich mit der XRechnung CII aus derselben Eingabe:

```bash
erechnung extrahieren rechnung_zugferd_xr.pdf -o aus_xr.xml
diff aus_xr.xml rechnung_cii.xml && echo gleich
```

```text
xrechnung.xml aus rechnung_zugferd_xr.pdf gespeichert als aus_xr.xml
gleich
```

Beim normalen ZUGFeRD-Profil EN 16931 unterscheidet sich das XML in diesem Beispiel nur in BT-24:

```bash
erechnung extrahieren rechnung_zugferd.pdf -o aus_zf.xml
diff aus_zf.xml rechnung_cii.xml
```

```text
factur-x.xml aus rechnung_zugferd.pdf gespeichert als aus_zf.xml
8c8
<       <ram:ID>urn:cen.eu:en16931:2017</ram:ID>
---
>       <ram:ID>urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0</ram:ID>
```

Das Profil XRECHNUNG passt, wenn ein Empfänger eine XRechnung verlangt, Sie aber auch eine lesbare Fassung in derselben Datei mitschicken wollen. Ob eine bestimmte Behörde oder Plattform dieses Profil annimmt, klären Sie vorher mit der Rechnungsempfangsstelle.

## XRechnung oder ZUGFeRD: Entscheidungshilfe

| Ihre Situation | Empfehlung | Grund |
| --- | --- | --- |
| Rechnung an eine Behörde des Bundes | XRechnung mit Leitweg-ID in BT-10 | E-Rechnungsverordnung des Bundes (ERechV), Leitweg-ID ist im B2G Pflicht |
| Rechnung an eine Landes- oder Kommunalbehörde | XRechnung mit Leitweg-ID, Vorgaben der Stelle prüfen | Die Länder setzen die Richtlinie 2014/55/EU mit eigenen Regeln um |
| Rechnung an ein Unternehmen, das nichts vorgibt | ZUGFeRD (Profil EN 16931) oder XRechnung | Beide sind zulässig; ZUGFeRD ist auch ohne Software lesbar |
| Kunde verlangt ausdrücklich XRechnung | XRechnung oder ZUGFeRD-Profil XRECHNUNG | Das Profil XRECHNUNG enthält eine vollständige XRechnung |
| Kunde arbeitet mit Peppol | XRechnung | XRechnung 3.0 und Peppol BIS Billing 3.0 sind laut [xeinkauf.de](https://xeinkauf.de/aktuelles/peppol/zusammenhang-xrechnung-peppol/) in Deutschland inhaltlich gleichbedeutend |
| Ihre Software kann nur MINIMUM oder BASIC WL | wechseln auf BASIC, EN 16931 oder XRechnung | Diese beiden Profile sind keine E-Rechnung |
| Rechnung an Privatkunden (B2C) | keine Pflicht zur E-Rechnung | B2C ist laut BMF-FAQ nicht betroffen |

Ab wann Sie im B2B E-Rechnungen ausstellen müssen, steht in [E-Rechnung Pflicht](./e-rechnung-pflicht.md).

## Was darf der Empfänger verlangen?

Welches Format verwendet wird, ist laut UStAE 14.1 Abs. 12 zivilrechtlich zwischen den Vertragsparteien zu klären. Andere Formate nach EN 16931 sind ebenfalls zulässig. Umsatzsteuerlich gilt nur: Das Format muss der EN 16931 entsprechen oder vereinbart sein und die richtige und vollständige Extraktion der Angaben ermöglichen (§ 14 Abs. 1 Satz 6 UStG).

Daraus folgt für die Praxis:

- Ein Unternehmen muss E-Rechnungen seit 01.01.2025 empfangen können. Der Empfang per E-Mail genügt, ein eigenes Postfach ist laut BMF-Schreiben vom 15.10.2025 (UStAE 14.1) nicht nötig.
- Bei einer Pflicht-E-Rechnung im B2B braucht der Aussteller keine Zustimmung des Empfängers (§ 14 Abs. 1 Satz 5 UStG).
- Ein bestimmtes Format, zum Beispiel XRechnung statt ZUGFeRD, kann der Kunde über den Vertrag vereinbaren. Ob eine solche Vorgabe in Ihrem Fall bindet, klären Sie mit der Steuerberatung oder rechtlich.
- Auftragnehmer des Bundes müssen seit 27.11.2020 nach der ERechV elektronisch abrechnen, über die OZG-RE und mit Leitweg-ID. Direktaufträge bis 1.000 EUR sind laut [e-rechnung-bund.de](https://www.e-rechnung-bund.de/faq/) ausgenommen.

## Beispiele

Alle Befehle laufen mit der Eingabe aus [`beispiele/01_standard/eingabe.json`](../../beispiele/01_standard/eingabe.json), kopiert als `rechnung.json`.

### Beispiel 1: XRechnung UBL und CII aus derselben Eingabe

Das brauchen Sie für Behörden, Peppol oder Kunden, die XRechnung verlangen.

```bash
erechnung erstellen rechnung.json --format xrechnung-ubl -o rechnung_ubl.xml
erechnung erstellen rechnung.json --format xrechnung-cii -o rechnung_cii.xml
```

```text
rechnung_ubl.xml: xrechnung-ubl, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
rechnung_cii.xml: xrechnung-cii, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
```

### Beispiel 2: ZUGFeRD-PDF im Profil EN 16931

Das ist die übliche Wahl im B2B, wenn der Kunde nichts vorgibt. Ohne `--pdf` erzeugt das Werkzeug über Ghostscript eine einfache PDF/A-3-Lesefassung.

```bash
erechnung erstellen rechnung.json --format zugferd -o rechnung_zugferd.pdf
```

```text
rechnung_zugferd.pdf: zugferd, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
```

Mit `--pdf IHRE_RECHNUNG.pdf` nimmt das Werkzeug stattdessen Ihr eigenes Rechnungslayout als PDF-Teil.

### Beispiel 3: ZUGFeRD-PDF im Profil XRECHNUNG

Das brauchen Sie, wenn eine XRechnung verlangt ist und Sie trotzdem ein lesbares PDF mitliefern wollen.

```bash
erechnung erstellen rechnung.json --format zugferd-xrechnung -o rechnung_zugferd_xr.pdf
```

```text
rechnung_zugferd_xr.pdf: zugferd-xrechnung, Rechnung RE-2026-0001, Zahlbetrag 2.009,91 EUR
```

### Beispiel 4: Alle vier Dateien offiziell prüfen

Die Prüfung erkennt das Format selbst und wählt das passende KoSIT-Szenario. Beim ZUGFeRD-Profil EN 16931 ist das das reine EN-16931-Szenario, beim Profil XRECHNUNG das XRechnung-Szenario mit allen BR-DE-Regeln.

```bash
erechnung validieren rechnung_ubl.xml rechnung_cii.xml rechnung_zugferd.pdf rechnung_zugferd_xr.pdf
```

```text
rechnung_ubl.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
rechnung_cii.xml: XRechnung 3.0 (CII)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (CII), 0 Fehler, 0 Warnungen
rechnung_zugferd.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
rechnung_zugferd_xr.pdf: ZUGFeRD-Profil XRECHNUNG, XRechnung 3.0 (CII)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (CII), 0 Fehler, 0 Warnungen
```

Der Exit-Code ist 0, wenn alle Dateien gültig sind. Die PDF/A-3-Konformität des PDF-Teils prüft `erechnung` nicht, nur das eingebettete XML.

### Beispiel 5: Dateigrößen vergleichen

Das hilft, wenn ein Portal oder Postfach eine Größengrenze hat.

```bash
ls -go rechnung_ubl.xml rechnung_cii.xml rechnung_zugferd.pdf rechnung_zugferd_xr.pdf
```

```text
-rw-r--r--  1    8065 Oct 16 00:17 rechnung_cii.xml
-rw-r--r--  1    5643 Oct 16 00:17 rechnung_ubl.xml
-rw-r--r--  1   28164 Oct 16 00:17 rechnung_zugferd.pdf
-rw-r--r--  1   28206 Oct 16 00:17 rechnung_zugferd_xr.pdf
```

UBL ist in diesem Beispiel bei gleichem Inhalt kleiner als CII. Die PDFs sind rund dreieinhalbmal so groß wie das CII-XML, das in ihnen steckt.

### Beispiel 6: Profil und eingebettete Datei erkennen

Mit `erechnung lesen` sehen Sie bei einer empfangenen Rechnung sofort, ob es ZUGFeRD EN 16931 oder das Profil XRECHNUNG ist und ob sie als E-Rechnung zählt.

```bash
erechnung lesen rechnung_zugferd.pdf rechnung_zugferd_xr.pdf
```

```text
Datei:        rechnung_zugferd.pdf
Format:       ZUGFeRD/Factur-X Profil EN 16931 (COMFORT) (eingebettet als factur-x.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
Art:          380 (Rechnung)
Nummer:       RE-2026-0001 vom 15.10.2026
...
Zahlbetrag:   2.009,91 EUR, fällig 14.11.2026
Zahlung:      58 (SEPA-Überweisung) DE79000000001234567890

Datei:        rechnung_zugferd_xr.pdf
Format:       ZUGFeRD-Profil XRECHNUNG, XRechnung 3.0 (CII) (eingebettet als xrechnung.xml)
E-Rechnung:   ja, strukturiert nach EN 16931
...
```

### Beispiel 7: Ohne BT-10 ist ZUGFeRD gültig, XRechnung nicht

Hier zeigt sich der wichtigste praktische Unterschied. Für den Test wurde `leitweg_id` (BT-10) aus der Eingabe gelöscht und beide Formate erzeugt:

```bash
erechnung validieren ohne_bt10.xml
erechnung validieren ohne_bt10_zf.pdf
```

```text
ohne_bt10.xml: XRechnung 3.0 (UBL)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-DE-15: [BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BR-DE-15: Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.
ohne_bt10_zf.pdf: ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)
  KoSIT (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 (CII), 0 Fehler, 0 Warnungen
```

Ein fehlendes BT-10 ist laut BMF-Schreiben vom 15.10.2025, Rn. 35a, umsatzsteuerlich unbeachtlich. Eine Behörde braucht die Leitweg-ID aber, um die Rechnung zuzuordnen.

## Schritt für Schritt: beide Formate aus einer Eingabe erzeugen und prüfen

1. Klären Sie mit dem Empfänger, welches Format er erwartet. Bei Behörden fragen Sie nach der Leitweg-ID.
2. Installieren Sie das Werkzeug (Python 3.10 oder neuer, kein Java):

   ```bash
   pipx install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
   ```

3. Legen Sie die Rechnungsdaten als JSON an. Vorlage ist [`beispiele/01_standard/eingabe.json`](../../beispiele/01_standard/eingabe.json). Tragen Sie die Leitweg-ID oder die Referenz des Kunden in `leitweg_id` ein, dann passt dieselbe Datei für XRechnung und ZUGFeRD.
4. Erzeugen Sie das gewünschte Format, zum Beispiel `--format xrechnung-ubl` für eine Behörde oder `--format zugferd` für ein Unternehmen. Mit `--validieren` prüft das Werkzeug das Ergebnis gleich mit.
5. Prüfen Sie die Datei mit `erechnung validieren DATEI`. Gültig ist sie, wenn `GÜLTIG` und Exit-Code 0 erscheinen.
6. Bewahren Sie Rechnung und Prüfbericht auf (`erechnung validieren --bericht berichte DATEI`), wie es das BMF-Schreiben vom 15.10.2025, Rn. 35a, empfiehlt.
7. Versenden Sie die Datei über den vereinbarten Weg, etwa per E-Mail oder über das Portal des Empfängers. Einen Versand oder Peppol-Zugang bietet das Werkzeug nicht.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| ZUGFeRD MINIMUM oder BASIC WL als E-Rechnung verschickt | Vorprüfung meldet `VP-FORMAT`, die Datei gilt nicht als E-Rechnung | Profil BASIC, EN 16931 oder XRECHNUNG verwenden |
| ZUGFeRD EN 16931 an eine Behörde, die XRechnung verlangt | Ablehnung, häufig mit `[BR-DE-15]` bei Prüfung als XRechnung | XRechnung oder ZUGFeRD-Profil XRECHNUNG mit Leitweg-ID schicken |
| Profil XRECHNUNG ohne BT-10 oder Verkäuferkontakt | `UNGÜLTIG` mit BR-DE-15 oder BR-DE-2 | Dieselben Pflichtfelder wie bei einer XRechnung füllen |
| PDF und XML zeigen unterschiedliche Beträge | Der Empfänger sieht im PDF etwas anderes, als seine Software einliest | XML und PDF aus denselben Daten erzeugen; maßgebend ist das XML |
| Normales PDF ohne XML verschickt | `erechnung lesen` meldet: "Das PDF enthält kein eingebettetes Rechnungs-XML." | XML erzeugen und mit `erechnung zugferd XML --pdf RECHNUNG.pdf` einbetten |
| XRechnung lässt sich nicht öffnen | Doppelklick zeigt nur XML-Code | Mit `erechnung anzeigen rechnung.xml` eine HTML-Ansicht erzeugen |

## Häufige Fragen

### Was ist der Unterschied zwischen XRechnung und ZUGFeRD?

Eine XRechnung ist eine reine XML-Datei, eine ZUGFeRD-Rechnung ist ein PDF mit eingebettetem XML. Beide beruhen auf der EN 16931. Die XRechnung verlangt mehr Pflichtfelder, zum Beispiel BT-10 und einen Verkäuferkontakt.

### Ist ZUGFeRD eine E-Rechnung?

Ja, ZUGFeRD ab Version 2.0.1 ist eine E-Rechnung, außer in den Profilen MINIMUM und BASIC WL (UStAE 14.1 Abs. 14). Maßgebend ist dabei der XML-Teil, nicht das PDF.

### Muss ich an Behörden eine XRechnung schicken?

Für Behörden ist die XRechnung mit Leitweg-ID in BT-10 der Standard. Auftragnehmer des Bundes rechnen nach der ERechV über die OZG-RE ab. Länder und Kommunen haben eigene Regeln; fragen Sie im Zweifel bei der Rechnungsempfangsstelle nach.

### Kann ich im B2B statt ZUGFeRD auch XRechnung schicken?

Ja, beide Formate sind im B2B zulässig. Welches verwendet wird, klären die Vertragspartner laut UStAE 14.1 Abs. 12 untereinander. Eine XRechnung ist für Empfänger ohne Viewer allerdings schwerer zu lesen.

### Was ist ZUGFeRD XRechnung?

ZUGFeRD XRechnung ist das ZUGFeRD-Profil XRECHNUNG: ein PDF/A-3, in dem eine vollständige XRechnung in CII als `xrechnung.xml` eingebettet ist. Es gelten alle Regeln der XRechnung, dazu ist die Rechnung als PDF lesbar.

### Welches Format ist kleiner, XRechnung oder ZUGFeRD?

Die XRechnung ist kleiner. In Beispiel 01 hat die XRechnung UBL 5.643 Byte, die XRechnung CII 8.065 Byte und das ZUGFeRD-PDF 28.164 Byte. Für die Grenzen der OZG-RE (10 MB per E-Mail) spielt das keine Rolle.

### Kann ich eine XRechnung in ZUGFeRD umwandeln?

Ja, eine XRechnung in CII können Sie mit `erechnung zugferd rechnung_cii.xml --pdf RECHNUNG.pdf` in ein vorhandenes PDF einbetten. Das Werkzeug erkennt die XRechnung-Kennung und bettet die Datei als `xrechnung.xml` im Profil XRECHNUNG ein. Eine XRechnung in UBL lässt sich so nicht einbetten, weil ZUGFeRD auf CII beruht. Einfacher ist es, beide Formate wie oben aus derselben JSON-Eingabe zu erzeugen. Details stehen in [PDF in ZUGFeRD umwandeln](./pdf-in-zugferd-umwandeln.md).

> **Hinweis:** Diese Anleitung erklärt Gesetz, BMF-Schreiben und technische Standards nach dem Stand vom 15.10.2026. Sie ist keine Steuer- oder Rechtsberatung, die Autoren sind keine Steuerberater. Für die Beurteilung eines konkreten Falls wenden Sie sich an Ihre Steuerberatung oder Ihr Finanzamt. Alle Angaben ohne Gewähr.

## Weiterlesen

- [XRechnung: Format, Aufbau und Pflichtfelder](./xrechnung.md)
- [ZUGFeRD: Format, Profile und Versionen](./zugferd.md)
- [E-Rechnung erstellen](./e-rechnung-erstellen.md)
- [E-Rechnung prüfen mit dem Validator](./e-rechnung-validator.md)
- [Leitweg-ID und E-Rechnung an Behörden](./leitweg-id.md)
- Beispieldateien: [Übersicht](../../beispiele/README.md), [ZUGFeRD-PDF Standardrechnung](../../beispiele/01_standard/zugferd_en16931.pdf), [XRechnung UBL](../../beispiele/01_standard/xrechnung_ubl.xml)
