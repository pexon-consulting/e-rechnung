# Sicherheit

## Lücke melden

Bitte keine öffentlichen Issues für Sicherheitslücken. Nutze [GitHub Private Vulnerability Reporting](https://github.com/pexon-consulting/e-rechnung/security/advisories/new). Wir antworten innerhalb von fünf Werktagen.

Besonders interessiert uns:

- eine Rechnungsdatei, mit der beim Lesen, Prüfen oder Anzeigen lokale Dateien gelesen, Netzwerkzugriffe ausgelöst oder Code ausgeführt werden (XXE, XSLT-Erweiterungen, Skripte in der HTML-Ansicht),
- ein ZIP oder PDF, das beim Entpacken oder Einbetten außerhalb des Zielordners schreibt,
- eine Datei, die als gültig gemeldet wird, obwohl der KoSIT-Validator sie ablehnt.

## Was das Werkzeug dagegen tut

- XML wird ohne Entitäten, ohne DTD-Laden und ohne Netzwerkzugriff geparst.
- Die KoSIT-Dateien werden nur über HTTPS von festen URLs geladen und vor dem Entpacken gegen eine SHA-256-Summe geprüft. ZIP-Einträge mit absoluten Pfaden oder `..` werden abgelehnt.
- Die eigene HTML-Ansicht escaped alle Werte aus der Rechnung. Die KoSIT-Visualisierung ist in der Version 2026-10-13 eingebunden, die eine JavaScript-Injection über Dateinamen von Anhängen behebt.
- Der MCP-Server arbeitet nur mit lokalen Dateien und lädt nichts hoch.

## Unterstützte Versionen

Sicherheitskorrekturen gibt es für die jeweils neueste Version.
