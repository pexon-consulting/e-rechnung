# Sicherheit

## Lücke melden

Bitte keine öffentlichen Issues für Sicherheitslücken. Nutzen Sie [GitHub Private Vulnerability Reporting](https://github.com/pexon-consulting/e-rechnung/security/advisories/new). Wir bemühen uns, innerhalb von fünf Werktagen zu antworten. Ein Anspruch auf eine Antwort oder eine Behebung besteht nicht.

Besonders interessiert uns:

- eine Rechnungsdatei, mit der beim Lesen, Prüfen oder Anzeigen lokale Dateien gelesen, Netzwerkzugriffe ausgelöst oder Code ausgeführt werden (XXE, XSLT-Erweiterungen, Skripte in der HTML-Ansicht),
- ein ZIP oder PDF, das beim Entpacken oder Einbetten außerhalb des Zielordners schreibt,
- eine Datei, die als gültig gemeldet wird, obwohl der KoSIT-Validator sie ablehnt,
- ein Weg, über den der MCP-Server außerhalb seines Ordners liest oder schreibt.

## Was das Werkzeug dagegen tut

- XML wird ohne Entitäten, ohne DTD-Laden und ohne Netzwerkzugriff geparst.
- Die KoSIT-Dateien werden nur über HTTPS von festen URLs geladen und vor dem Entpacken gegen eine SHA-256-Summe geprüft. Eine lokal angegebene ZIP (`ERECHNUNG_KOSIT_KONFIG`) mit dem Originalnamen der festen Version wird ebenfalls gegen die Prüfsumme geprüft; eigene Regeln erlaubt erst `ERECHNUNG_KOSIT_KONFIG_OHNE_HASH=1`. ZIP-Einträge mit absoluten Pfaden oder `..` werden abgelehnt.
- Die eigene HTML-Ansicht escaped alle Werte aus der Rechnung. Die KoSIT-Visualisierung ist in der Version 2026-10-13 eingebunden, die eine JavaScript-Injection über Dateinamen von Anhängen behebt.
- Zeilenumbrüche in einzeiligen Feldern (Namen, Straße, Ort, Rechnungsnummer) werden beim Einlesen entfernt. Der DATEV-Export entschärft Werte, die eine Tabellenkalkulation als Formel lesen würde.
- Der MCP-Server lädt nichts hoch. Er liest und schreibt nur Dateien im Ordner aus `ERECHNUNG_MCP_ORDNER` (Standard: das Arbeitsverzeichnis) und überschreibt keine vorhandenen Dateien. Rechnungen stammen von Dritten und können Anweisungen an das Modell enthalten (Prompt-Injection). Setzen Sie die schreibenden Werkzeuge `erechnung_erstellen`, `erechnung_anzeigen` und `erechnung_datev` deshalb nicht auf eine Allow-Liste.

## Unterstützte Versionen

Sicherheitskorrekturen gibt es für die jeweils neueste Version.
