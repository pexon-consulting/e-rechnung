# E-Rechnung mit Python: XRechnung und ZUGFeRD lesen, prüfen und erzeugen

XRechnung und ZUGFeRD in Python verarbeiten Sie ohne Java, indem Sie die offiziellen KoSIT-Prüfregeln (kompiliertes XSLT) mit saxonche ausführen, statt den Java-Validator aufzurufen. Das Paket `e-rechnung` macht genau das: Es liest XRechnung (UBL und CII) und ZUGFeRD-PDFs, baut Rechnungen aus Python-Dataclasses, prüft sie mit den KoSIT-Regeln und schreibt DATEV-Buchungsstapel. Die bekannten Python-Bibliotheken drafthorse, factur-x und pycheval decken jeweils nur einen Teil davon ab.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Entwickler und IT-Teams.

## Das Wichtigste in Kürze

- Die offiziellen Prüfregeln für XRechnung liegen nur als XSLT 2.0 vor; lxml kann nur XSLT 1.0, deshalb braucht Python dafür Saxon (saxonche) oder einen Java-Prozess.
- `e-rechnung` führt die KoSIT-Konfiguration 2026-08-31 mit saxonche aus und liefert dieselben Ergebnisse wie der KoSIT-Validator 1.6.3 (222 von 222 Testdateien).
- Eine Rechnung entsteht als Dataclass `Rechnung` mit `Partei`, `Adresse`, `Kontakt`, `Position` und `Zahlung`; Beträge sind immer `Decimal`.
- `ubl()` und `cii()` rechnen Summen und Steuern selbst und geben XML-Bytes zurück, `validieren()` gibt ein Ergebnis-Objekt mit `gueltig`, `offiziell` und `vorpruefung` zurück.
- Alle Saxon-Aufrufe laufen auf einem eigenen Thread, deshalb dürfen Web-Server und Thread-Pools `validieren()` parallel aufrufen.
- Rechnungsdaten bleiben auf dem Rechner; nur die KoSIT-Regeln werden einmal von GitHub geladen, offline geht es mit `ERECHNUNG_KOSIT_KONFIG`.

## Welche Python-Bibliotheken gibt es für die E-Rechnung?

Eine Python-Bibliothek für XRechnung, die UBL und CII mit der Kennung `xrechnung_3.0` erzeugt und die XRechnung-Regeln (BR-DE, Peppol) ohne Java prüft, gab es laut Recherche vom 15.10.2026 auf PyPI nicht. Die vorhandenen Pakete sind gut, aber für andere Zwecke gebaut.

| Paket | Version (Datum) | Lizenz | Kann | Kann nicht |
| --- | --- | --- | --- | --- |
| drafthorse (pretix) | 2025.2.0 (15.09.2025) | Apache-2.0 | ZUGFeRD/CII-XML erzeugen und parsen, XSD-Prüfung, XML in PDF einbetten | kein UBL, keine Schematron-Prüfung, kein PDF-Parsing, Dateiname immer `factur-x.xml` |
| factur-x (akretion) | 7.7 (14.10.2026) | BSD | Factur-X-PDF erzeugen, XML aus PDF holen, XSD-Prüfung, CII und UBL 2.1 aus einem Dict erzeugen (seit 5.0), UBL/CII parsen (seit 7.0) | kein XRechnung-Profil, Schematron nur über externen Saxon-Server per HTTP, Fokus Frankreich |
| pycheval (zfutura) | 0.3.3 (20.02.2026) | Apache-2.0 | Factur-X 1.08 / ZUGFeRD 2.4 lesen und schreiben (MINIMUM bis EN 16931) | EXTENDED und XRechnung laut Projekt "not yet supported", Alpha, Python 3.11+ |
| saxonche (Saxonica) | 13.1.0 (15.10.2026) | MPL-2.0 | XSLT 3.0, XPath 3.1, XSD; damit laufen die KoSIT-XSLT | keine E-Rechnungs-Logik; factur-x hat es wegen Abstürzen im GraalVM-Isolate wieder entfernt |
| lxml | 6.1.3 (02.09.2026) | BSD-3-Clause | XML, XSD, XSLT 1.0 | kein XSLT 2.0, KoSIT-Regeln nicht direkt ausführbar |
| pypdf | 6.20.1 (12.10.2026) | BSD-3-Clause | PDF-Anhänge lesen und schreiben | erzeugt selbst kein geprüftes PDF/A-3 |
| invoice2data | 1.0.1 (01.08.2026) | MIT | Daten aus PDF-Rechnungen per Vorlage herauslesen | kein E-Rechnungsformat, keine EN-16931-Ausgabe |
| e-rechnung | 0.1.0 | MIT | XRechnung UBL/CII und ZUGFeRD lesen, erzeugen, mit KoSIT-Regeln prüfen, HTML-Ansicht, DATEV-Buchungsstapel, MCP-Server | kein Versand, kein Archiv, keine PDF/A-Prüfung, noch kein XRechnung 4.0 |

Quellen: PyPI und GitHub der jeweiligen Projekte, abgefragt am 15.10.2026 (Links unter [Weiterlesen](#weiterlesen)). Auf PyPI gibt es keine Pakete namens `xrechnung`, `python-xrechnung`, `zugferd` oder `facturx`.

Der Grund für die Lücke ist technisch: Die Schematron-Regeln von KoSIT und CEN sind als XSLT 2.0 kompiliert. Wer in Python prüfen will, muss Saxon einbinden. `e-rechnung` nutzt dafür saxonche und kapselt das Thread-Problem, an dem factur-x gescheitert ist (siehe [Thread-Sicherheit](#ist-validieren-thread-sicher)).

## Installation für Python-Projekte

Das Paket liegt auf GitHub, nicht auf PyPI. Python 3.10 oder neuer, kein Java.

```bash
pip install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"
```

Das Extra `offiziell` bringt saxonche für die KoSIT-Regeln mit. Ohne das Extra läuft nur die Vorprüfung. `mcp` installiert zusätzlich den MCP-Server, `toml` die TOML-Eingabe unter Python 3.10.

Alle Beispiele unten laufen im geklonten Repo, weil sie Dateien aus `beispiele/` lesen. Die Ausgaben sind echt.

## Rechnung im Code bauen: Dataclasses und Decimal

Eine Rechnung ist ein `Rechnung`-Objekt. Die Felder tragen deutsche Namen, der Kommentar in `src/erechnung/modell.py` nennt jeweils die BT-Nummer der EN 16931. Pflicht beim Erzeugen sind `nummer` (BT-1), `datum` (BT-2), `verkaeufer` und `kaeufer`; für eine Position `id`, `name`, `menge`, `einheit` und `preis`.

| Klasse | Wichtige Felder | BT/BG |
| --- | --- | --- |
| `Rechnung` | `nummer`, `datum`, `art="380"`, `waehrung="EUR"`, `faellig`, `leitweg_id`, `leistung_von`, `leistung_bis`, `positionen`, `zahlung`, `nachlaesse`, `spezifikation` | BT-1, BT-2, BT-3, BT-5, BT-9, BT-10, BT-73, BT-74, BG-25, BG-16, BG-20, BT-24 |
| `Partei` | `name`, `adresse`, `ust_id`, `steuernummer`, `elektronische_adresse`, `elektronische_adresse_schema="EM"`, `kontakt` | BT-27/BT-44, BT-31, BT-32, BT-34/BT-49, BG-6 |
| `Adresse` | `strasse`, `plz`, `ort`, `land="DE"` | BT-35, BT-38, BT-37, BT-40 |
| `Kontakt` | `name`, `telefon`, `email` | BT-41, BT-42, BT-43 |
| `Position` | `id`, `name`, `menge`, `einheit`, `preis`, `kategorie="S"`, `satz=Decimal("19")` | BT-126, BT-153, BT-129, BT-130, BT-146, BT-151, BT-152 |
| `Zahlung` | `art="58"`, `iban`, `bic`, `verwendungszweck`, `skonto_tage`, `skonto_prozent`, `mandatsreferenz`, `glaeubiger_id` | BT-81, BT-84, BT-86, BT-83, BT-20, BT-89, BT-90 |

Das Feld `leitweg_id` ist BT-10 (Buyer reference). Bei Behörden steht dort die Leitweg-ID, im B2B eine Referenz des Käufers, zum Beispiel die Bestellnummer.

Datei `bauen.py`:

```python
from datetime import date
from decimal import Decimal

from erechnung import Adresse, Kontakt, Partei, Position, Rechnung, Zahlung, berechnen

rechnung = Rechnung(
    nummer="RE-2026-0042",
    datum=date(2026, 10, 15),
    faellig=date(2026, 11, 14),
    leitweg_id="PO-4711",
    leistung_von=date(2026, 9, 1),
    leistung_bis=date(2026, 9, 30),
    verkaeufer=Partei(
        name="Nordlicht Beispiel GmbH",
        adresse=Adresse(strasse="Musterstraße 1", plz="20095", ort="Hamburg"),
        ust_id="DE123456789",
        elektronische_adresse="rechnung@nordlicht.example",
        kontakt=Kontakt(name="Erika Mustermann", telefon="+49 40 66969123",
                        email="buchhaltung@nordlicht.example"),
    ),
    kaeufer=Partei(
        name="Beispiel Handel AG",
        adresse=Adresse(strasse="Hauptstraße 5", plz="80331", ort="München"),
        elektronische_adresse="eingangsrechnung@beispiel-handel.example",
    ),
    zahlung=Zahlung(art="58", iban="DE79000000001234567890",
                    verwendungszweck="RE-2026-0042"),
    positionen=[
        Position(id="1", name="Beratung", menge=Decimal("12"), einheit="HUR",
                 preis=Decimal("120.00")),
        Position(id="2", name="Fachbuch", menge=Decimal("2"), einheit="C62",
                 preis=Decimal("39.90"), satz=Decimal("7")),
    ],
)

if __name__ == "__main__":
    berechnen(rechnung)
    for st in rechnung.steuern:
        print(st.kategorie, st.satz, st.basis, st.betrag)
    print("Netto", rechnung.summen.netto, "Steuer", rechnung.summen.steuer,
          "Zahlbetrag", rechnung.summen.zahlbetrag)
```

```text
$ python bauen.py
S 19 1440.00 273.60
S 7 79.80 5.59
Netto 1519.80 Steuer 279.19 Zahlbetrag 1798.99
```

`berechnen(r)` füllt die Positionsbeträge (BT-131), die Umsatzsteuer-Aufschlüsselung je Kategorie und Satz (BG-23) und die Summen (BG-22) und gibt dieselbe Rechnung zurück. Beträge immer als `Decimal("120.00")` aus einem String übergeben. Ein `float` wie `preis=39.9` bricht mit `TypeError: unsupported operand type(s) for *: 'decimal.Decimal' and 'float'` ab, und `Decimal(0.1)` ohne Anführungszeichen ergibt `0.1000000000000000055511151231257827021181583404541015625`.

Statt Python-Code geht auch JSON oder TOML mit denselben Feldnamen: `laden("eingabe.json")` oder `aus_dict(daten)` liefern ein `Rechnung`-Objekt. Vorlagen dafür stehen in [`beispiele/`](../../beispiele/README.md).

## XRechnung erzeugen mit `ubl()` und `cii()`

`ubl(r)` und `cii(r)` rufen intern `berechnen(r)` auf und geben das XML als Bytes zurück. Welche Kennung (BT-24) im XML steht, bestimmt `r.spezifikation`. Standard ist XRechnung 3.0.

| `r.spezifikation` | Ergebnis mit `ubl()` | Ergebnis mit `cii()` |
| --- | --- | --- |
| `erechnung.modell.XRECHNUNG_3` (Standard) | XRechnung 3.0 UBL | XRechnung 3.0 CII, ZUGFeRD-Profil XRECHNUNG |
| `erechnung.modell.EN16931` | EN 16931 UBL | ZUGFeRD-Profil EN 16931 (COMFORT) |

Minderungen mit Rechnungsart 381 (kaufmännische Gutschrift) schreibt `ubl()` automatisch als UBL `CreditNote`.

```python
from erechnung import cii, ubl
from bauen import rechnung

print("\n".join(ubl(rechnung).decode().splitlines()[2:10]))
```

```xml
  <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0</cbc:CustomizationID>
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
  <cbc:ID>RE-2026-0042</cbc:ID>
  <cbc:IssueDate>2026-10-15</cbc:IssueDate>
  <cbc:DueDate>2026-11-14</cbc:DueDate>
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
  <cbc:BuyerReference>PO-4711</cbc:BuyerReference>
```

## XRechnung validieren in Python: `validieren()` und das Ergebnis

`validieren(quelle, offiziell_pruefen=True, offline=False)` nimmt einen Pfad, einen `str` oder Bytes, XML oder ZUGFeRD-PDF. Zurück kommt ein `Ergebnis`:

| Attribut | Typ | Bedeutung |
| --- | --- | --- |
| `gueltig` | `bool` oder `None` | Ergebnis der KoSIT-Regeln; `None`, wenn die offizielle Prüfung nicht lief |
| `format` | `Format` | Syntax, Kennung (BT-24), Bezeichnung, `ist_e_rechnung`, `pdf`, `anhang` |
| `offiziell` | `Bericht` oder `None` | `szenario`, `akzeptiert`, `befunde`, `fehler`, `warnungen`, `konfiguration`, `hinweis` |
| `vorpruefung` | `list[Befund]` | eigene Regeln mit Codes `VP-...` (Pflichtangaben, Rechnen, IBAN, Leitweg-ID) |
| `vorpruefung_ok` | `bool` | keine Vorprüfung der Stufe `error` |
| `offiziell_fehler` | `str` | Grund, falls die offizielle Prüfung nicht möglich war |
| `als_dict()` | `dict` | alles als JSON-fähiges Dict |

Ein `Befund` hat `stufe` (`error`, `warning`, `information`), `code` (zum Beispiel `BR-DE-15`), `text`, `ort` (XPath) und `quelle`. Maßgeblich ist `gueltig`. Die Vorprüfung erklärt Fehler auf Deutsch, ersetzt die KoSIT-Regeln aber nicht.

```python
from erechnung import cii, ubl, validieren
from bauen import rechnung

ergebnis = validieren(ubl(rechnung))
print("gültig:", ergebnis.gueltig)
print("Szenario:", ergebnis.offiziell.szenario)
print("Fehler:", [b.code for b in ergebnis.offiziell.fehler])
print("Warnungen:", [b.code for b in ergebnis.offiziell.warnungen])
print("Vorprüfung:", [(b.stufe, b.code) for b in ergebnis.vorpruefung])
print("CII gültig:", validieren(cii(rechnung)).gueltig)
```

```text
gültig: True
Szenario: EN16931 XRechnung (UBL Invoice)
Fehler: []
Warnungen: []
Vorprüfung: []
CII gültig: True
```

Fehlen BT-10 und der Verkäuferkontakt, meldet die KoSIT-Prüfung die Regeln BR-DE-15 und BR-DE-2:

```python
from erechnung import Kontakt, ubl, validieren
from bauen import rechnung

rechnung.leitweg_id = ""
rechnung.verkaeufer.kontakt = Kontakt()
ergebnis = validieren(ubl(rechnung))
print("gültig:", ergebnis.gueltig)
for b in ergebnis.offiziell.fehler + ergebnis.vorpruefung:
    print(b.code, "|", b.text)
```

```text
gültig: False
BR-DE-15 | [BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.
BR-DE-2 | [BR-DE-2] Die Gruppe "SELLER CONTACT" (BG-6) muss übermittelt werden.
VP-BR-DE-15 | Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.
VP-BR-DE-2 | Kontakt des Verkäufers unvollständig: XRechnung verlangt Name, Telefon und E-Mail (BT-41, BT-42, BT-43).
```

`ergebnis.als_dict()` liefert dasselbe als Dict mit den Schlüsseln `datei`, `format`, `gueltig`, `vorpruefung_ok`, `vorpruefung`, `offiziell` und `offiziell_fehler`.

Laut BMF-Schreiben vom 15.10.2025 (Rn. 35a) ist ein fehlendes BT-10 umsatzsteuerlich unbeachtlich, die Rechnung fällt in der XRechnung-Prüfung aber durch. Für die Aufbewahrung des Ergebnisses gibt es auf der Kommandozeile `erechnung validieren --bericht ORDNER` (JSON mit Zeitpunkt, Regelversion und SHA-256 der Datei).

## E-Rechnung lesen: `lesen()` und `erkennen()`

`erkennen(quelle)` sagt, was in der Datei steckt, ohne sie ganz zu lesen. `lesen(quelle)` gibt ein `Rechnung`-Objekt mit den Beträgen genau so zurück, wie sie in der Datei stehen; es rechnet nichts nach. Beide nehmen Pfad oder Bytes, XML oder ZUGFeRD-PDF.

```python
from erechnung import erkennen, lesen

pfad = "beispiele/01_standard/zugferd_en16931.pdf"
print(erkennen(pfad))
r = lesen(pfad)
print(r.nummer, r.datum, r.verkaeufer.name, r.summen.zahlbetrag, r.syntax)
for p in r.positionen:
    print(p.id, p.name, p.menge, p.einheit, p.nettobetrag)
print(erkennen("beispiele/08_b2g_leitweg_id/xrechnung_ubl.xml").bezeichnung)
```

```text
Format(syntax='CII', spezifikation='urn:cen.eu:en16931:2017', bezeichnung='ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)', ist_e_rechnung=True, pdf=True, anhang='factur-x.xml')
RE-2026-0001 2026-10-15 Nordlicht Beispiel GmbH 2009.91 CII
1 Beratung Einführung E-Rechnung 12 HUR 1440.00
2 Softwarelizenz Rechnungseingang (Monat) 1 MON 249.00
XRechnung 3.0 (UBL)
```

`ist_e_rechnung` ist `False` bei den ZUGFeRD-Profilen MINIMUM und BASIC WL, die laut BMF-Schreiben vom 15.10.2025 (UStAE 14.1 Abs. 14) keine E-Rechnung sind. Ein PDF ohne eingebettetes XML löst `erechnung.pdf.KeinXmlImPdf` aus:

```text
KeinXmlImPdf Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG eine sonstige Rechnung, keine E-Rechnung.
```

## ZUGFeRD in Python: `einbetten()` und `xml_auslesen()`

`erechnung.pdf.xml_auslesen(pdf)` gibt Dateiname und Inhalt des eingebetteten XML zurück. `erechnung.pdf.einbetten(pdf, xml, dateiname=None, pdfa=False)` bettet CII-XML in ein vorhandenes PDF ein und setzt AFRelationship, den `/AF`-Eintrag und die XMP-Metadaten. Der Dateiname ergibt sich aus dem Profil: `xrechnung.xml` beim Profil XRECHNUNG, sonst `factur-x.xml`. Mit `pdfa=True` wandelt Ghostscript das PDF vorher nach PDF/A-3b um (Ghostscript muss installiert sein).

```python
from pathlib import Path

from erechnung import cii
from erechnung.modell import EN16931
from erechnung.pdf import einbetten, xml_auslesen
from bauen import rechnung

name, xml = xml_auslesen("beispiele/01_standard/zugferd_en16931.pdf")
print(name, len(xml), "Bytes")

rechnung.spezifikation = EN16931
neu = einbetten(Path("vorlage.pdf").read_bytes(), cii(rechnung))
Path("RE-2026-0042.pdf").write_bytes(neu)
print(xml_auslesen(neu)[0])
```

```text
factur-x.xml 8020 Bytes
factur-x.xml
```

`erechnung validieren RE-2026-0042.pdf` meldet danach "GÜLTIG, Szenario EN16931 (CII)". Enthält das PDF schon ein `factur-x.xml` oder `xrechnung.xml`, bricht `einbetten()` mit `ValueError` ab. Ob das Ergebnis ein gültiges PDF/A-3 ist, hängt am Ausgangs-PDF; eine PDF/A-Prüfung macht das Paket nicht (dafür Mustang oder veraPDF). Mehr in [PDF in ZUGFeRD umwandeln](./pdf-in-zugferd-umwandeln.md).

## DATEV-Buchungsstapel aus Python: `stapel()` und `Einstellungen`

`erechnung.datev.stapel(rechnungen, einstellungen=None)` gibt den Buchungsstapel als Bytes (Windows-1252, CRLF) und eine Liste von Hinweisen zurück. `Einstellungen` hat unter anderem `berater=1001`, `mandant=1`, `skr="03"`, `kreditor=70000` (Sammelkreditor), `kreditoren` (USt-IdNr., Steuernummer oder Name auf Kreditorennummer), `aufwandskonto` und `wj_beginn`. Je Rechnung und Steuersatz entsteht eine Zeile mit dem Bruttobetrag.

```python
from pathlib import Path

from erechnung import lesen
from erechnung.datev import Einstellungen, stapel

dateien = ["beispiele/01_standard/xrechnung_ubl.xml",
           "beispiele/02_gemischte_steuersaetze/xrechnung_cii.xml"]
rechnungen = [lesen(d) for d in dateien]
einstellungen = Einstellungen(berater=1001, mandant=1, skr="04",
                              kreditoren={"DE123456789": 70010})
daten, hinweise = stapel(rechnungen, einstellungen)
Path("EXTF_Buchungsstapel.csv").write_bytes(daten)
for z in daten.decode("cp1252").splitlines()[2:]:
    print(";".join(z.split(";")[:11]))
print(hinweise)
```

```text
2009,91;"H";"EUR";;;;70010;6850;"9";1510;"RE-2026-0001"
160,18;"H";"EUR";;;;70010;6850;"8";1510;"RE-2026-0002"
47,46;"H";"EUR";;;;70010;6850;"9";1510;"RE-2026-0002"
[]
```

Die Spalten sind Umsatz, Soll/Haben, Währung, Kurs, Basisumsatz, Währung Basisumsatz, Konto (Kreditor), Gegenkonto (SKR04 6850), BU-Schlüssel (9 für 19 %, 8 für 7 %), Belegdatum (TTMM) und Belegfeld 1. Rechnungen aus verschiedenen Wirtschaftsjahren lehnt `stapel()` mit `DatevFehler` ab, ebenso Fremdwährungen. Konten und BU-Schlüssel sind ein Vorschlag; stimmen Sie sie mit der Steuerberatung ab. Details in [DATEV und E-Rechnung](./datev-e-rechnung.md).

## HTML-Ansicht: `anzeigen.html()` und `offiziell.html_ansicht()`

`erechnung.anzeigen.html(r, ist_e_rechnung=None, format_text="")` baut aus einem `Rechnung`-Objekt eine schlichte HTML-Seite, ohne Internet. `erechnung.offiziell.html_ansicht(xml, offline=False)` nimmt XML-Bytes und erzeugt die offizielle KoSIT-Visualisierung (Version 2026-10-13, wird beim ersten Aufruf geladen).

```python
from pathlib import Path

from erechnung import erkennen, lesen
from erechnung.anzeigen import html
from erechnung.offiziell import html_ansicht

pfad = "beispiele/08_b2g_leitweg_id/xrechnung_ubl.xml"
fmt = erkennen(pfad)
Path("ansicht.html").write_text(html(lesen(pfad), fmt.ist_e_rechnung, fmt.bezeichnung), encoding="utf-8")
Path("ansicht_kosit.html").write_text(html_ansicht(Path(pfad).read_bytes()), encoding="utf-8")
```

Für ZUGFeRD-PDFs holen Sie vorher das XML mit `xml_auslesen()`, weil `html_ansicht()` nur XML nimmt. Die KoSIT weist darauf hin, dass eine Visualisierung keine gültige XRechnung ist und nicht zur Archivierung dient; das Original ist das XML.

## Ist `validieren()` thread-sicher?

Ja. saxonche läuft in einem GraalVM-Isolate, das an den Thread gebunden ist, der es erzeugt hat. Genau daran sind andere Projekte gescheitert (factur-x hat saxonche deshalb entfernt). `e-rechnung` schickt deshalb alle Saxon-Aufrufe an einen eigenen Thread namens `saxon` und gibt die Ergebnisse an den Aufrufer zurück. Sie können `validieren()` und `html_ansicht()` aus beliebigen Threads aufrufen.

```python
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from erechnung import validieren

dateien = sorted(Path("beispiele").glob("*/xrechnung_*.xml"))
with ThreadPoolExecutor(max_workers=8) as pool:
    ergebnisse = list(pool.map(validieren, dateien))
print(len(ergebnisse), "Dateien,", sum(e.gueltig for e in ergebnisse), "gültig")
print([t.name for t in threading.enumerate() if t.name == "saxon"])
```

```text
18 Dateien, 18 gültig
['saxon']
```

Weil es nur einen Saxon-Thread je Prozess gibt, laufen die Schematron-Prüfungen nacheinander. Für mehr Durchsatz nehmen Sie mehrere Prozesse, zum Beispiel `concurrent.futures.ProcessPoolExecutor`; jeder Prozess hat seinen eigenen Saxon-Thread.

## Offline-Betrieb: `ERECHNUNG_KOSIT_KONFIG` und `ERECHNUNG_CACHE`

Beim ersten Prüfen lädt das Paket die KoSIT-Konfiguration `xrechnung-3.0.2-validator-configuration-2026-08-31.zip` von GitHub, prüft die SHA-256-Summe und entpackt sie nach `~/.cache/erechnung`. Danach läuft alles ohne Netz.

| Variable | Wirkung |
| --- | --- |
| `ERECHNUNG_CACHE` | anderer Cache-Ordner statt `~/.cache/erechnung` |
| `ERECHNUNG_KOSIT_KONFIG` | Pfad zur ZIP-Datei oder zum entpackten Ordner der KoSIT-Konfiguration, kein Download. Eine ZIP mit dem Originalnamen wird gegen die SHA-256-Summe geprüft |
| `ERECHNUNG_KOSIT_KONFIG_OHNE_HASH` | `1` erlaubt eine ZIP mit Originalnamen, deren Prüfsumme abweicht (bewusst geänderte Regeln) |
| `ERECHNUNG_KOSIT_VISUALISIERUNG` | dasselbe für die KoSIT-Visualisierung (`html_ansicht()`) |

Für Rechner ohne Internet laden Sie die ZIP einmal woanders herunter und legen sie ab. Mit `offline=True` in `validieren()` (oder `--offline` auf der Kommandozeile) lädt das Paket nie etwas nach:

```text
$ ERECHNUNG_CACHE=/tmp/leer erechnung validieren --offline beispiele/01_standard/xrechnung_ubl.xml
beispiele/01_standard/xrechnung_ubl.xml: XRechnung 3.0 (UBL)
  Offizielle Prüfung nicht möglich: xrechnung-3.0.2-validator-configuration-2026-08-31 liegt nicht im Cache (/tmp/leer/xrechnung-3.0.2-validator-configuration-2026-08-31) und offline ist gesetzt.
  Vorprüfung ohne Befund.

$ export ERECHNUNG_KOSIT_KONFIG=/pfad/xrechnung-3.0.2-validator-configuration-2026-08-31.zip
$ erechnung validieren --offline beispiele/01_standard/xrechnung_ubl.xml
beispiele/01_standard/xrechnung_ubl.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
```

Im ersten Fall ist der Exit-Code 2 (Prüfung nicht möglich), in Python steht der Grund in `ergebnis.offiziell_fehler` und `gueltig` ist `None`.

## E-Rechnung in Django oder FastAPI prüfen

Für einen Web-Dienst reicht eine Funktion, die Bytes nimmt. In Django kommen die Bytes aus `request.FILES["datei"].read()`, in FastAPI aus `await datei.read()` eines `UploadFile`. `validieren()` blockiert für die Dauer der Prüfung; in async-Code rufen Sie es deshalb in einem Thread auf, was dank des Saxon-Threads sicher ist.

```python
import asyncio
from pathlib import Path

from erechnung import validieren


def rechnung_pruefen(daten: bytes) -> dict:
    """Prüft hochgeladene Bytes (XML oder ZUGFeRD-PDF) und gibt eine kurze Antwort zurück."""
    e = validieren(daten)
    return {
        "format": e.format.bezeichnung if e.format else None,
        "gueltig": e.gueltig,
        "fehler": [f"{b.code}: {b.text}" for b in (e.offiziell.fehler if e.offiziell else [])],
        "hinweis": e.offiziell_fehler,
    }


if __name__ == "__main__":
    daten = Path("beispiele/07_kleinunternehmer/zugferd_en16931.pdf").read_bytes()
    print(rechnung_pruefen(daten))
    print(asyncio.run(asyncio.to_thread(rechnung_pruefen, b"<Invoice/>")))
```

```text
{'format': 'ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)', 'gueltig': True, 'fehler': [], 'hinweis': ''}
{'format': 'Unbekannte Spezifikation (leer)', 'gueltig': False, 'fehler': ['SZENARIO: Kein passendes Prüfszenario. Erwartet wird UBL Invoice/CreditNote oder CII mit einer Spezifikationskennung (BT-24) für XRechnung 3.0 oder EN 16931.'], 'hinweis': ''}
```

Laden Sie die KoSIT-Konfiguration beim Deployment vor (`erechnung konfiguration`) oder setzen Sie `ERECHNUNG_KOSIT_KONFIG`, damit der erste Aufruf im Betrieb nicht auf GitHub wartet.

## Eigene Rechnungsvorlagen mit pytest absichern

Wer Rechnungen aus eigenen Vorlagen erzeugt, sollte jede Vorlage im Test durch die KoSIT-Regeln schicken. Dann fällt eine geänderte Vorlage auf, bevor eine ungültige Rechnung beim Kunden landet. Datei `test_vorlagen.py` neben den JSON-Vorlagen:

```python
from pathlib import Path

import pytest

from erechnung import cii, laden, ubl, validieren

VORLAGEN = sorted(Path(__file__).parent.glob("*.json"))


@pytest.mark.parametrize("vorlage", VORLAGEN, ids=lambda p: p.stem)
@pytest.mark.parametrize("erzeuger", [ubl, cii], ids=["ubl", "cii"])
def test_vorlage_besteht_kosit(vorlage, erzeuger):
    e = validieren(erzeuger(laden(vorlage)))
    assert e.offiziell is not None, e.offiziell_fehler
    assert e.gueltig, [f"{b.code}: {b.text}" for b in e.offiziell.fehler]
    assert not e.offiziell.warnungen
    assert e.vorpruefung_ok, [b.code for b in e.vorpruefung]
```

```text
$ python -m pytest -v
test_vorlagen.py::test_vorlage_besteht_kosit[ubl-reverse_charge] PASSED  [ 25%]
test_vorlagen.py::test_vorlage_besteht_kosit[ubl-standard] PASSED        [ 50%]
test_vorlagen.py::test_vorlage_besteht_kosit[cii-reverse_charge] PASSED  [ 75%]
test_vorlagen.py::test_vorlage_besteht_kosit[cii-standard] PASSED        [100%]
============================== 4 passed in 0.69s ===============================
```

Die Vorlagen `standard.json` und `reverse_charge.json` sind Kopien von `beispiele/01_standard/eingabe.json` und `beispiele/05_reverse_charge_13b/eingabe.json`. In CI setzen Sie `ERECHNUNG_KOSIT_KONFIG` oder cachen `~/.cache/erechnung`.

## XRechnung und ZUGFeRD in Python: Codebeispiele

### Beispiel 1: Minderung (381) als UBL CreditNote

```python
from erechnung import laden, ubl

xml = ubl(laden("beispiele/03_gutschrift/eingabe.json"))
print(xml.splitlines()[1][:60].decode())
```

```text
<CreditNote xmlns="urn:oasis:names:specification:ubl:schema:
```

Für Minderungen mit Rechnungsart 381: `ubl()` wählt das Wurzelelement `CreditNote` selbst.

### Beispiel 2: Rechnung aus JSON laden und als ZUGFeRD-XML mit Profil XRECHNUNG schreiben

```python
from erechnung import cii, laden

r = laden("beispiele/08_b2g_leitweg_id/eingabe.json")
xml = cii(r)
print(r.leitweg_id, r.summen.zahlbetrag, len(xml), "Bytes")
```

```text
04011000-12345-03 3590.83 7676 Bytes
```

Für Rechnungen an Behörden, die CII erwarten. `r.spezifikation` bleibt auf XRechnung 3.0, BT-10 enthält die Leitweg-ID aus der Vorlage.

### Beispiel 3: Leitweg-ID vor dem Versand prüfen

```python
from erechnung import leitweg_id_gueltig

print(leitweg_id_gueltig("04011000-1234512345-06"), leitweg_id_gueltig("04011000-1234512345-07"))
```

```text
True False
```

Für Formulare, in denen Kunden ihre Leitweg-ID eintragen. Die Prüfziffer folgt der Formatspezifikation 2.0.2 (ISO/IEC 7064 Mod 97-10).

### Beispiel 4: Eingangsrechnung als JSON für ein anderes System

```python
import json

from erechnung import lesen

r = lesen("beispiele/02_gemischte_steuersaetze/zugferd_en16931.pdf")
d = r.als_dict()
print(json.dumps({k: d[k] for k in ("nummer", "datum", "faellig")} | {"zahlbetrag": d["summen"]["zahlbetrag"]}))
```

```text
{"nummer": "RE-2026-0002", "datum": "2026-10-15", "faellig": "2026-11-14", "zahlbetrag": "207.64"}
```

Für die Übergabe an eine Datenbank oder eine Freigabe-Strecke. `als_dict()` wandelt `Decimal` und `date` in Strings.

### Beispiel 5: Vorprüfung ohne saxonche

```python
from erechnung import validieren

e = validieren("beispiele/09_sepa_lastschrift/xrechnung_ubl.xml", offiziell_pruefen=False)
print(e.gueltig, e.vorpruefung_ok)
```

```text
None True
```

Für schnelle Prüfungen in einer Umgebung ohne das Extra `offiziell`. `gueltig` ist dann `None`, weil die KoSIT-Regeln nicht liefen.

## Schritt für Schritt: E-Rechnung in Python prüfen

1. Python 3.10 oder neuer installieren und eine virtuelle Umgebung anlegen: `python3 -m venv .venv`.
2. Paket mit Prüfregeln installieren: `.venv/bin/pip install "e-rechnung[offiziell] @ git+https://github.com/pexon-consulting/e-rechnung@v0.1.0"`.
3. Prüfregeln einmal laden: `.venv/bin/erechnung konfiguration`. Ohne Internet stattdessen `ERECHNUNG_KOSIT_KONFIG` auf die ZIP-Datei setzen.
4. In Python `from erechnung import validieren` und `ergebnis = validieren("rechnung.xml")` aufrufen.
5. `ergebnis.gueltig` auswerten: `True` heißt von den KoSIT-Regeln angenommen, `False` heißt Fehler in `ergebnis.offiziell.fehler`, `None` heißt Prüfung nicht möglich (Grund in `ergebnis.offiziell_fehler`).
6. Für eigene Rechnungen `Rechnung(...)` bauen, mit `ubl()` oder `cii()` schreiben und das Ergebnis vor dem Versand mit `validieren()` prüfen.
7. Eigene Vorlagen mit dem pytest-Test oben in die CI aufnehmen.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| Beträge als `float` | `TypeError` beim Rechnen mit `Decimal` | Immer `Decimal("12.34")` aus einem String bauen |
| Extra `offiziell` fehlt | `gueltig` ist `None`, `offiziell_fehler` nennt saxonche | `pip install "e-rechnung[offiziell] @ git+..."` |
| BT-10 leer | BR-DE-15 in XRechnung | `leitweg_id` setzen, im B2B eine Käuferreferenz |
| `lesen()` auf ein reines PDF | `KeinXmlImPdf` | Das PDF ist keine E-Rechnung; beim Absender die E-Rechnung anfordern |
| `einbetten()` mit UBL-XML | `ValueError` "Unbekannte Guideline-ID" | ZUGFeRD braucht CII, also `cii()` statt `ubl()` |
| Kein Netz beim ersten Aufruf | `offiziell_fehler`: Download fehlgeschlagen | `ERECHNUNG_KOSIT_KONFIG` setzen oder `erechnung konfiguration` vorher ausführen |

## Häufige Fragen

### Kann ich XRechnung in Python ohne Java prüfen?

Ja, mit `e-rechnung` und saxonche. Das Paket führt die kompilierten Schematron-Regeln der KoSIT-Konfiguration aus und kam auf allen 222 Testdateien zum selben Ergebnis wie der KoSIT-Validator 1.6.3.

### Gibt es einen KoSIT-Validator für Python?

Einen Python-Wrapper der KoSIT selbst gibt es nicht; der KoSIT-Validator ist ein Java-Programm (Java 11+). `e-rechnung` nutzt dieselbe Prüfkonfiguration der KoSIT und braucht kein Java.

### Werden Rechnungsdaten irgendwohin geschickt?

Nein. Geladen werden nur die KoSIT-Konfiguration und bei Bedarf die KoSIT-Visualisierung, beide mit fester SHA-256-Prüfsumme. Die Prüfung selbst läuft lokal.

### Unterstützt das Paket XRechnung 4.0?

Noch nicht. Laut KoSIT gibt es seit 15.09.2026 eine Vorversion 4.0.0, die finale 4.0 soll im Frühjahr 2027 kommen. XRechnung 3.0 bleibt bis mindestens 31.07.2027 in Kraft.

### Kann ich ZUGFeRD BASIC oder EXTENDED prüfen?

Ja, aber nur gegen die Regeln der EN 16931. Die KoSIT-Konfiguration hat für diese Profile kein eigenes Szenario; das Ergebnis enthält dann einen `hinweis`. Profilregeln von ZUGFeRD prüft zum Beispiel Mustang.

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [E-Rechnung prüfen: XRechnung- und ZUGFeRD-Validator](./e-rechnung-validator.md)
- [E-Rechnung erstellen](./e-rechnung-erstellen.md)
- [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md)
- [E-Rechnung mit KI prüfen: MCP-Server](./e-rechnung-ki-mcp.md)
- [E-Rechnung Software kostenlos](./e-rechnung-software-kostenlos.md)
- [Beispiele im Repo](../../beispiele/README.md) und [Standardrechnung als XRechnung UBL](../../beispiele/01_standard/xrechnung_ubl.xml)
- Andere Python-Projekte: [drafthorse](https://github.com/pretix/python-drafthorse), [factur-x](https://github.com/akretion/factur-x), [pycheval](https://github.com/zfutura/pycheval), [saxonche](https://pypi.org/project/saxonche/)
