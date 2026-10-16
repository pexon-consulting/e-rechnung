# Mitmachen

Danke für Ihre Hilfe. Am meisten hilft uns eine Rechnung, die dieses Werkzeug anders bewertet als der KoSIT-Validator, oder ein Fall, den es noch nicht abbildet.

## Entwicklungsumgebung

```bash
git clone https://github.com/pexon-consulting/e-rechnung
cd e-rechnung
python3 -m venv .venv
.venv/bin/pip install -e ".[dev,mcp]"
.venv/bin/pytest -q
```

Mit `ERECHNUNG_TESTSUITE_LADEN=1` laufen zusätzlich alle Dateien der KoSIT-Testsuite durch Lesen und Vorprüfung.

## Abgleich mit dem KoSIT-Validator und Mustang

Die offizielle Prüfung muss immer dasselbe Ergebnis liefern wie der Java-Validator. Das prüft:

```bash
python scripts/abgleich_kosit.py                 # braucht Java 11+
python scripts/mustang_check.py beispiele/*/zugferd_en16931.pdf
```

Beide Skripte laden ihre Java-Programme mit fester Version und SHA-256-Summe. Die CI führt sie bei jedem Pull Request aus.

## Beispiele

Der Ordner `beispiele/` wird erzeugt, nicht von Hand bearbeitet. Neue Fälle kommen als JSON nach `src/erechnung/beispiele/` und in die Liste in `scripts/beispiele_bauen.py`. Danach:

```bash
python scripts/beispiele_bauen.py
python scripts/beispiele_bauen.py --check
```

## Stil

- Code und Kommentare auf Deutsch, Bezeichner ohne Umlaute.
- Texte mit echten Umlauten und ohne Gedankenstriche.
- Keine echten Personen- oder Bankdaten in Tests und Beispielen. Für IBANs `DE79000000001234567890` (KoSIT-Testwert), für Gläubiger-IDs `DE98ZZZ09999999999`.
- Jede neue Prüfregel bekommt einen Test, der sie auslöst, und einen, der sie nicht auslöst.

## Rechtliche Aussagen

Anleitungen zitieren Gesetz, BMF-Schreiben (mit Datum und Randnummer) oder die Spezifikation. Bitte keine eigenen steuerlichen Auslegungen. Wo es auf den Einzelfall ankommt, verweisen wir auf die Steuerberatung.
