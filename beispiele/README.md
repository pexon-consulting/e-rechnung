# Beispieldateien für XRechnung und ZUGFeRD

Neun gültige E-Rechnungen zum Herunterladen, von der Standardrechnung bis zur Rechnung an eine
Behörde, jeweils als XRechnung UBL und CII, mit lesbarer HTML-Ansicht und dem Ergebnis der
offiziellen KoSIT-Prüfregeln (`xrechnung-3.0.2-validator-configuration-2026-08-31`). Was jeder Fall zeigt, erklärt die
Anleitung [E-Rechnung Beispiel](../docs/anleitungen/e-rechnung-beispiel.md). Erzeugt werden die
Dateien mit `python scripts/beispiele_bauen.py` aus den Eingaben in `src/erechnung/beispiele/`,
die CI prüft, dass sie zum Code passen.

Firmen, Namen, Anschriften, Telefonnummern (aus den Bereichen der Bundesnetzagentur für Film und
Fernsehen), IBAN (`DE79000000001234567890`), Gläubiger-ID (`DE98ZZZ09999999999`) und
USt-IdNr. sind Testwerte und gehören keiner echten Firma oder Person.

| Fall | Was er zeigt | Dateien |
| --- | --- | --- |
| Standardrechnung | Dienstleistung mit Leistungszeitraum, 19 % USt, Skonto, Überweisung | [UBL](01_standard/xrechnung_ubl.xml), [CII](01_standard/xrechnung_cii.xml), [Ansicht](01_standard/ansicht.html), [Eingabe](01_standard/eingabe.json), [ZUGFeRD-PDF](01_standard/zugferd_en16931.pdf) |
| Gemischte Steuersätze | 7 % und 19 % in einer Rechnung, Nachlass auf Belegebene | [UBL](02_gemischte_steuersaetze/xrechnung_ubl.xml), [CII](02_gemischte_steuersaetze/xrechnung_cii.xml), [Ansicht](02_gemischte_steuersaetze/ansicht.html), [Eingabe](02_gemischte_steuersaetze/eingabe.json), [ZUGFeRD-PDF](02_gemischte_steuersaetze/zugferd_en16931.pdf) |
| Minderung (381, kaufmännische Gutschrift) | Minderung einer früheren Rechnung, in UBL als CreditNote; keine Gutschrift nach § 14 Abs. 2 Satz 5 UStG (das wäre Rechnungsart 389) | [UBL](03_gutschrift/xrechnung_ubl.xml), [CII](03_gutschrift/xrechnung_cii.xml), [Ansicht](03_gutschrift/ansicht.html), [Eingabe](03_gutschrift/eingabe.json) |
| Rechnungskorrektur (384) | Korrektur mit Bezug auf die ursprüngliche Rechnung (BG-3) | [UBL](04_rechnungskorrektur/xrechnung_ubl.xml), [CII](04_rechnungskorrektur/xrechnung_cii.xml), [Ansicht](04_rechnungskorrektur/ansicht.html), [Eingabe](04_rechnungskorrektur/eingabe.json) |
| Reverse Charge § 13b UStG | Steuerkategorie AE, Steuerschuldnerschaft des Leistungsempfängers | [UBL](05_reverse_charge_13b/xrechnung_ubl.xml), [CII](05_reverse_charge_13b/xrechnung_cii.xml), [Ansicht](05_reverse_charge_13b/ansicht.html), [Eingabe](05_reverse_charge_13b/eingabe.json) |
| Innergemeinschaftliche Lieferung | Steuerkategorie K, Käufer in Österreich | [UBL](06_innergemeinschaftlich/xrechnung_ubl.xml), [CII](06_innergemeinschaftlich/xrechnung_cii.xml), [Ansicht](06_innergemeinschaftlich/ansicht.html), [Eingabe](06_innergemeinschaftlich/eingabe.json) |
| Kleinunternehmer § 19 UStG | Steuerkategorie E, Steuernummer statt USt-IdNr. | [UBL](07_kleinunternehmer/xrechnung_ubl.xml), [CII](07_kleinunternehmer/xrechnung_cii.xml), [Ansicht](07_kleinunternehmer/ansicht.html), [Eingabe](07_kleinunternehmer/eingabe.json), [ZUGFeRD-PDF](07_kleinunternehmer/zugferd_en16931.pdf) |
| Rechnung an eine Behörde | Leitweg-ID in BT-10 und als elektronische Adresse (0204) | [UBL](08_b2g_leitweg_id/xrechnung_ubl.xml), [CII](08_b2g_leitweg_id/xrechnung_cii.xml), [Ansicht](08_b2g_leitweg_id/ansicht.html), [Eingabe](08_b2g_leitweg_id/eingabe.json), [KoSIT-Ansicht](08_b2g_leitweg_id/ansicht_kosit.html) |
| SEPA-Lastschrift | Zahlungsart 59 mit Mandatsreferenz und Gläubiger-ID | [UBL](09_sepa_lastschrift/xrechnung_ubl.xml), [CII](09_sepa_lastschrift/xrechnung_cii.xml), [Ansicht](09_sepa_lastschrift/ansicht.html), [Eingabe](09_sepa_lastschrift/eingabe.json) |

Der DATEV-Buchungsstapel über alle Fälle (SKR04, Sammelkreditor 70000) liegt in
[`datev/EXTF_Buchungsstapel.csv`](datev/EXTF_Buchungsstapel.csv).

Selbst erzeugen:

```bash
erechnung beispiele ./meine-beispiele
erechnung erstellen ./meine-beispiele/01_standard.json --format zugferd -o rechnung.pdf
```
