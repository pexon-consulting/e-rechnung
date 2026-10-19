# Änderungen

Alle nennenswerten Änderungen an diesem Projekt. Versionen nach [Semantic Versioning](https://semver.org/lang/de/).

## 0.1.0 - 2026-10-15

Erste Version.

- `erechnung lesen`: XRechnung UBL (Invoice, CreditNote), XRechnung CII und ZUGFeRD/Factur-X-PDF lesen, Format und Profil erkennen, MINIMUM und BASIC WL als "keine E-Rechnung" kennzeichnen.
- `erechnung validieren` (Aliase `check`, `prüfen`): offizielle KoSIT-Regeln für XRechnung 3.0.2 (Konfiguration 2026-08-31) in Python mit saxonche, ohne Java. Gleiche Annahme oder Ablehnung und dieselben verletzten Regeln wie der KoSIT-Validator 1.6.3 auf 222 Testdateien. Dazu eine Vorprüfung mit Pflichtangaben nach § 14 Abs. 4 UStG, Rechenprüfung, IBAN und Leitweg-ID. Prüfbericht mit `--bericht`.
- `erechnung erstellen`: XRechnung UBL und CII, EN 16931 und ZUGFeRD (Profile EN 16931 und XRECHNUNG) aus JSON oder TOML, mit eigener PDF-Vorlage oder einer PDF/A-3-Ansicht über Ghostscript. Geprüft mit Mustang 2.26.0.
- `erechnung zugferd` und `erechnung extrahieren`: XML in PDF einbetten und wieder auslesen.
- `erechnung anzeigen`: eigene HTML-Ansicht und KoSIT-Visualisierung 2026-10-13.
- `erechnung datev`: DATEV-Buchungsstapel EXTF 700, Formatversion 13, SKR03 und SKR04.
- `erechnung leitweg-id`: Prüfziffer nach Formatspezifikation 2.0.2.
- MCP-Server `erechnung-mcp` mit sechs Werkzeugen. Er liest und schreibt nur im Ordner aus `ERECHNUNG_MCP_ORDNER` und überschreibt keine Dateien.
- Neun Beispielrechnungen, 21 Anleitungen.
