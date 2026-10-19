---
name: e-rechnung-validieren
description: Liest und validiert eingehende E-Rechnungen (XRechnung UBL/CII, ZUGFeRD/Factur-X-PDF) mit den offiziellen KoSIT-Regeln und erklärt die Fehlermeldungen auf Deutsch. Verwenden, wenn eine Rechnungsdatei geprüft, eine BR-DE- oder BR-Fehlermeldung erklärt oder geprüft werden soll, ob eine Datei technisch dem Format einer E-Rechnung entspricht (XRechnung oder ZUGFeRD ab Profil EN 16931).
---

# E-Rechnung validieren

Werkzeug: `erechnung` aus https://github.com/pexon-consulting/e-rechnung. Falls nicht installiert:

```bash
uvx --from "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0" erechnung --help
```

## Ablauf

1. Datei lesen, um Format, Profil, Beträge und Parteien zu sehen:
   `erechnung lesen rechnung.xml` (oder `.pdf`).
2. Validieren mit JSON-Ausgabe:
   `erechnung validieren rechnung.xml --json`
   Exit-Code 0 heißt gültig, 1 heißt Fehler, 2 heißt Werkzeugproblem.
3. Für die Ablage einen Bericht schreiben:
   `erechnung validieren rechnung.xml --bericht berichte/`

## Ergebnis einordnen

- `gueltig: true`: Die Datei besteht XSD und alle KoSIT-Schematron-Regeln. Inhaltlich richtig (Preis, Leistung) ist sie damit noch nicht.
- Ergebnis `kein Szenario`: Die Datei ist kein XRechnung- oder EN-16931-Dokument. Bei ZUGFeRD MINIMUM und BASIC WL meldet `erechnung lesen` "keine E-Rechnung": Diese Profile gelten seit 1.1.2025 als sonstige Rechnung.
- Fehler beginnen mit `BR-` (EN 16931), `BR-DE-` (XRechnung), `BR-CL-` (Codelisten) oder `VP-` (Vorprüfung dieses Werkzeugs, keine offizielle Regel).
- Laut BMF-Schreiben vom 15.10.2025 (Rn. 35a) sind Geschäftsregelfehler zu Inhalten außerhalb der Pflichtangaben nach §§ 14 Abs. 4 und 14a UStG umsatzsteuerlich unbeachtlich, etwa ein fehlendes BT-10 (BR-DE-15). Betrifft die Regel eine Pflichtangabe, etwa Anschrift (BR-DE-3, BR-DE-4, BR-DE-8, BR-DE-9), Steuernummer oder USt-IdNr. (BR-DE-16) oder Steuersatz (BR-DE-14), ist die Rechnung nicht ordnungsmäßig. Ob das im Einzelfall zutrifft, beurteilt die Steuerberatung; gib keine pauschale Entwarnung. Bei Behörden als Empfänger lehnt die Rechnungsplattform fehlerhafte Dateien ohnehin ab.

## Häufige Fehler kurz erklärt

| Code | Bedeutung | Abhilfe |
| --- | --- | --- |
| BR-DE-15 | Käuferreferenz BT-10 fehlt | Leitweg-ID oder bei B2B eine Referenz bzw. `-` eintragen |
| BR-CO-15 | Gesamtbetrag ungleich Netto plus Steuer | Rundung je Steuersatz prüfen, nicht je Position |
| BR-DE-5 / BR-DE-7 | Kontaktname oder E-Mail des Verkäufers fehlt | BG-6 Verkäuferkontakt ergänzen |
| BR-CL-23 | Unbekannter Mengeneinheitscode | UN/ECE Rec. 20 verwenden, z. B. `C62`, `HUR`, `DAY` |
| VP-LEITWEG | Leitweg-ID mit falscher Prüfziffer | `erechnung leitweg-id <ID>` zeigt die richtige |

Die vollständige Liste steht in `docs/anleitungen/e-rechnung-fehlermeldungen.md` im Repository.

## Grenzen

- Kein Ersatz für die Prüfung durch die Steuerberatung bei Grenzfällen wie Kleinbetragsrechnungen, Gutschriften im umsatzsteuerlichen Sinn oder Reverse Charge.
- PDF/A-Konformität eines ZUGFeRD-PDFs prüft das Werkzeug nicht. Dafür Mustang oder veraPDF verwenden.

## Hinweis an den Nutzer

Schließe jede Antwort, die umsatzsteuerliche Folgen, Fristen, Aufbewahrung oder Buchungen betrifft, mit diesem Satz ab: "Hinweis: Das ist eine technische Auswertung, keine Steuer- oder Rechtsberatung. Klären Sie die Folgen mit Ihrer Steuerberatung."
