---
name: e-rechnung-erstellen
description: Erzeugt aus strukturierten Rechnungsdaten (JSON/TOML) eine gültige XRechnung (UBL oder CII) oder ein ZUGFeRD-PDF und validiert sie sofort. Verwenden, wenn eine Ausgangsrechnung als E-Rechnung gebaut, eine Rechnung für eine Behörde mit Leitweg-ID erstellt oder ein vorhandenes PDF in ZUGFeRD umgewandelt werden soll.
---

# E-Rechnung erstellen

Werkzeug: `erechnung` aus https://github.com/pexon-consulting/e-rechnung.

## Ablauf

1. Eingabedatei anlegen. Vorlage: `beispiele/01_standard/eingabe.json` im Repository. Mindestens nötig: Nummer, Datum, Verkäufer mit Anschrift, Kontakt und USt-IdNr. oder Steuernummer, Käufer mit Anschrift, Positionen mit Menge, Einheit, Preis und Steuersatz, Zahlungsart.
2. Format wählen:
   - Behörde (B2G): `xrechnung-ubl` oder `xrechnung-cii`, Käuferreferenz = Leitweg-ID, elektronische Adresse des Käufers mit Schema `0204`.
   - Unternehmen (B2B), das ein lesbares PDF erwartet: `zugferd` (Profil EN 16931).
   - Unternehmen ohne Vorgabe: `xrechnung-ubl` oder `zugferd`, beides ist eine E-Rechnung nach § 14 UStG.
3. Erzeugen und sofort validieren (`--pdfa` wandelt eine eigene Vorlage vorher nach PDF/A-3b):
   ```bash
   erechnung erstellen rechnung.json --format xrechnung-ubl -o RE-2026-0100.xml --validieren
   erechnung erstellen rechnung.json --format zugferd --pdf vorlage.pdf --pdfa -o RE-2026-0100.pdf --validieren
   ```
   Ohne `--pdf` baut das Werkzeug über Ghostscript eine einfache PDF/A-3-Ansicht. Mit eigener Vorlage `--pdfa` setzen, wenn die Vorlage nicht schon PDF/A-3 ist; `--validieren` prüft nur das XML, strenge PDF-Prüfer wie Mustang lehnen eine Vorlage ohne PDF/A-3 sonst ab.
4. Bei Behörden vorher die Leitweg-ID kontrollieren: `erechnung leitweg-id 04011000-1234512345-06`.

## Regeln, die beim Bauen oft schiefgehen

- Rechnungsart: XRechnung erlaubt nur 326, 380, 381, 384, 389 und 875-877 (BR-DE-17). Das Werkzeug lehnt andere Codes ab.
- Eine Rechnungskorrektur mit Minderung (umgangssprachlich oft "Gutschrift") ist Art 381 mit positiven Beträgen, nicht 380 mit negativen. Eine Gutschrift im Sinne des UStG, also die Abrechnung durch den Leistungsempfänger, ist Art 389.
- Steuerbefreiung braucht Kategorie und Befreiungsgrund, z. B. `AE` mit "Steuerschuldnerschaft des Leistungsempfängers (§ 13b UStG)" oder `E` mit "Gemäß § 19 UStG wird keine Umsatzsteuer berechnet." Vorlagen: `beispiele/05_reverse_charge_13b` und `beispiele/07_kleinunternehmer`.
- Skonto steht in den Zahlungsbedingungen (BT-20) im Format `#SKONTO#TAGE=10#PROZENT=2.00#`. Das Werkzeug erzeugt es aus den Feldern `skonto_tage` und `skonto_prozent` unter `zahlung`.

## Ergebnis übergeben

Nach erfolgreicher Validierung die Datei ausgeben und kurz nennen: Format, Rechnungsnummer, Zahlbetrag, und ob Warnungen offen sind. Keine Rechnung als gültig melden, deren Validierung nicht gelaufen ist.

## Hinweis an den Nutzer

Schließe jede Antwort, die umsatzsteuerliche Folgen, Fristen, Aufbewahrung oder Buchungen betrifft, mit diesem Satz ab: "Hinweis: Das ist eine technische Auswertung, keine Steuer- oder Rechtsberatung. Klären Sie die Folgen mit Ihrer Steuerberatung."
