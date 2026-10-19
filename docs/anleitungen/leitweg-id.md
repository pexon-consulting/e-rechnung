# Leitweg-ID: Aufbau, Prüfziffer und E-Rechnung an Behörden

Die Leitweg-ID ist die Adresse einer öffentlichen Verwaltungseinheit für E-Rechnungen: Sie steht in der XRechnung im Feld BT-10 (Buyer reference) und sorgt dafür, dass die Rechnung bei der richtigen Stelle der Behörde ankommt. Sie bekommen die Leitweg-ID vom Auftraggeber, meist mit dem Auftrag, und schicken die XRechnung dann über das Portal oder den Kanal, den die Behörde nennt, beim Bund über die OZG-RE. Ob die Leitweg-ID richtig abgetippt ist, verrät ihre zweistellige Prüfziffer.

> Stand: 15.10.2026. Rechtsstand BMF-Schreiben vom 15.10.2025, XRechnung 3.0.2, ZUGFeRD 2.5.2. Keine Steuerberatung. Teil der Sammlung [E-Rechnung: Anleitungen und kostenloses Prüfwerkzeug](../../README.md).

Für: Unternehmen, die Rechnungen an Behörden schicken, und ihre Buchhaltung.

## Das Wichtigste in Kürze

- Eine Leitweg-ID besteht aus Grobadressierung (2-12 Ziffern), optionaler Feinadressierung (bis 30 Buchstaben oder Ziffern) und einer zweistelligen Prüfziffer, getrennt durch Bindestriche, zum Beispiel `04011000-1234512345-06`.
- Die Prüfziffer wird nach ISO/IEC 7064 Mod 97-10 berechnet, dem gleichen Verfahren wie bei der IBAN.
- In der XRechnung steht die Leitweg-ID in BT-10 und, wenn die Behörde das so vorgibt, auch als elektronische Adresse des Käufers (BT-49) mit dem Schema `0204`.
- Die Leitweg-ID vergibt der öffentliche Auftraggeber. Sie können sie nicht selbst bilden, nur auf Tippfehler prüfen.
- Im B2B-Geschäft brauchen Sie keine Leitweg-ID. BT-10 muss in einer XRechnung trotzdem gefüllt sein, laut BMF-FAQ genügt umsatzsteuerlich ein Platzhalter wie `-`.
- `erechnung leitweg-id` prüft Format und Prüfziffer und berechnet eine fehlende Prüfziffer, ohne dass Daten den Rechner verlassen.

## Was ist eine Leitweg-ID?

Eine Leitweg-ID ist eine zwischen Bund, Ländern und Kommunen abgestimmte Kennung, mit der eine E-Rechnung an eine bestimmte Verwaltungseinheit adressiert wird. So beschreibt es die [Leitweg-ID-Formatspezifikation 2.0.2](https://xeinkauf.de/app/uploads/2022/11/Leitweg-ID-Formatspezifikation-v2-0-2-1.pdf) (Fassung vom 28.07.2021) der KoSIT. Die Rechnungseingangsplattform der Behörde liest die Leitweg-ID und leitet die Rechnung an das zuständige Rechnungsbearbeitungssystem weiter.

Die Spezifikation regelt nur das Format. Welche Stelle welche Leitweg-ID bekommt, regeln Bund und Länder jeweils selbst. Deshalb können Sie eine Leitweg-ID nicht aus Name oder Anschrift der Behörde ableiten.

Seit dem 30.09.2019 ist die Leitweg-ID als Identifikationsschema in der ISO/IEC-6523-Liste registriert, mit dem Code `0204` (laut Formatspezifikation, Kapitel 1.5). Diesen Code sehen Sie in der XRechnung im Attribut `schemeID`.

## Wie ist die Leitweg-ID aufgebaut?

Die Leitweg-ID hat drei Bestandteile. Grobadressierung und Prüfziffer sind Pflicht, die Feinadressierung ist optional.

| Bestandteil | Länge | Zeichen | Pflicht | Beispiel |
| --- | --- | --- | --- | --- |
| Grobadressierung | 2-12 Stellen | Ziffern | ja | `04011000` |
| Bindestrich | 1 | `-` (U+002D) | nur wenn Feinadressierung folgt | `-` |
| Feinadressierung | bis 30 Stellen | Buchstaben A-Z und Ziffern 0-9 | nein | `1234512345` |
| Bindestrich | 1 | `-` (U+002D) | ja | `-` |
| Prüfziffer | 2 Stellen | Ziffern | ja | `06` |

Daraus ergibt sich laut Spezifikation eine Gesamtlänge von 5 bis 46 Zeichen. Buchstaben in der Feinadressierung sind nicht case-sensitiv, `abc` und `ABC` ergeben die gleiche Prüfziffer.

### Grobadressierung

Die Grobadressierung folgt dem Regionalschlüssel. Die ersten zwei Ziffern sind die Kennzahl des Bundeslandes oder des Bundes:

| Kennzahl | Bereich | Kennzahl | Bereich |
| --- | --- | --- | --- |
| 01 | Schleswig-Holstein | 09 | Bayern |
| 02 | Hamburg | 10 | Saarland |
| 03 | Niedersachsen | 11 | Berlin |
| 04 | Bremen | 12 | Brandenburg |
| 05 | Nordrhein-Westfalen | 13 | Mecklenburg-Vorpommern |
| 06 | Hessen | 14 | Sachsen |
| 07 | Rheinland-Pfalz | 15 | Sachsen-Anhalt |
| 08 | Baden-Württemberg | 16 | Thüringen |
| 99 | Bund | | |

Danach können folgen: Regierungsbezirk (1 Ziffer, beim Bund eine Ordnungskennzahl 0-9), Landkreis (2 Ziffern) und Gemeindeverband oder Gemeindekennzahl (3, 4 oder 7 Ziffern). Jede Stufe ist nur Pflicht, wenn die nächste angegeben ist.

### Feinadressierung

Die Feinadressierung legt jede Verwaltung selbst fest. Sie ist eindeutig nur zusammen mit der Grobadressierung, gleiche Feinadressierungen in verschiedenen Kommunen sind also erlaubt.

Die Spezifikation empfiehlt, die Feinadressierung mit einem Buchstaben beginnen zu lassen. Der Grund: Der Bindestrich zählt bei der Prüfziffer nicht mit. Ein verrutschter Bindestrich fällt deshalb nicht auf, solange die Ziffern gleich bleiben:

```bash
erechnung leitweg-id 04011000-12345-03 0401100-012345-03 040110001-2345-03
```

```text
04011000-12345-03: gültig
0401100-012345-03: gültig
040110001-2345-03: gültig
```

Alle drei haben eine korrekte Prüfziffer, aber nur eine davon ist die echte Adresse. Beginnt die Feinadressierung mit einem Buchstaben, kann so ein Fehler nicht entstehen.

### Prüfziffer

Die Prüfziffer erkennt Tippfehler. Sie wird aus Grob- und Feinadressierung ohne Bindestriche nach ISO/IEC 7064:2003, Verfahren Mod 97-10, berechnet. Das Rechenbeispiel aus der Formatspezifikation 2.0.2, Kapitel 2.4:

| Schritt | Was passiert | Ergebnis |
| --- | --- | --- |
| 1 | Grobadressierung übernehmen | `04011000` |
| 2 | Feinadressierung ohne Bindestrich anhängen, Buchstaben durch Zahlen ersetzen (A = 10, B = 11 bis Z = 35) | `040110001234512345` |
| 3 | Zwei Nullen anhängen | `04011000123451234500` |
| 4 | Rest bei Division durch 97 | `92` |
| 5 | 98 minus Rest, zweistellig | `98 - 92 = 06` |

Ergebnis: `04011000-1234512345-06`. Zur Kontrolle hängt man die Prüfziffer statt der zwei Nullen an: `04011000123451234506` geteilt durch 97 lässt den Rest 1. Rest 1 heißt gültig.

Mit Buchstaben sieht das so aus: In `991-33333TEST` wird `TEST` zu `29 14 28 29`. Die Zahl `991333332914282900` lässt bei Division durch 97 den Rest 65, die Prüfziffer ist also 98 - 65 = 33, die Leitweg-ID lautet `991-33333TEST-33`.

Mit 20-stelligen Zahlen rechnet man von Hand ungern. Lassen Sie das deshalb das Werkzeug erledigen (siehe Beispiele 1-3).

## Wo steht die Leitweg-ID in der XRechnung?

Die Leitweg-ID gehört in BT-10 (Buyer reference). In XRechnung ist BT-10 Pflicht, die Regel BR-DE-15 meldet sonst einen Fehler. Als elektronische Adresse des Käufers (BT-49) kann ebenfalls die Leitweg-ID stehen, mit dem Schema `0204`. Welche Adresse eine Behörde dort erwartet, nennt sie selbst. Die elektronische Adresse ist in XRechnung 3.0 Pflicht (Regel PEPPOL-EN16931-R010).

| Feld | Bedeutung | UBL | CII |
| --- | --- | --- | --- |
| BT-10 | Buyer reference, bei Behörden die Leitweg-ID | `cbc:BuyerReference` | `ram:BuyerReference` |
| BT-49 | Elektronische Adresse des Käufers | `cac:AccountingCustomerParty/cac:Party/cbc:EndpointID` | `ram:BuyerTradeParty/ram:URIUniversalCommunication/ram:URIID` |
| BT-49-1 | Schema der Adresse, `0204` = Leitweg-ID | Attribut `schemeID` | Attribut `schemeID` |

Die Beispielrechnung [08_b2g_leitweg_id](../../beispiele/08_b2g_leitweg_id/) zeigt beides. Aus [`xrechnung_ubl.xml`](../../beispiele/08_b2g_leitweg_id/xrechnung_ubl.xml):

```xml
<cbc:BuyerReference>04011000-12345-03</cbc:BuyerReference>
<!-- ... -->
<cac:AccountingCustomerParty>
  <cac:Party>
    <cbc:EndpointID schemeID="0204">04011000-12345-03</cbc:EndpointID>
  </cac:Party>
</cac:AccountingCustomerParty>
```

Und aus [`xrechnung_cii.xml`](../../beispiele/08_b2g_leitweg_id/xrechnung_cii.xml):

```xml
<ram:BuyerReference>04011000-12345-03</ram:BuyerReference>
<!-- ... -->
<ram:URIUniversalCommunication>
  <ram:URIID schemeID="0204">04011000-12345-03</ram:URIID>
</ram:URIUniversalCommunication>
```

Wichtig: Die offiziellen KoSIT-Regeln prüfen nur, ob BT-10 vorhanden ist. Die Prüfziffer der Leitweg-ID prüfen sie nicht (siehe Beispiel 5). Eine XRechnung mit falscher Leitweg-ID kann also offiziell gültig sein und trotzdem bei der Behörde nicht zugeordnet werden. Deshalb prüft `erechnung validieren` die Prüfziffer zusätzlich in der Vorprüfung (Code `VP-LEITWEG`).

## Woher bekomme ich die Leitweg-ID?

Sie bekommen die Leitweg-ID vom öffentlichen Auftraggeber. Laut Formatspezifikation (Kapitel 1.3) wird sie "in der Regel im konkreten Auftrag an den Rechnungssteller" übermittelt. Steht sie nicht im Auftrag, in der Bestellung oder im Vertrag, fragen Sie bei der Vergabestelle oder der Rechnungsstelle nach.

Was Sie nicht tun sollten:

- Eine Leitweg-ID aus einer anderen Rechnung an dieselbe Behörde übernehmen, ohne nachzufragen. Die Feinadressierung kann je Amt oder Abteilung verschieden sein.
- Eine Leitweg-ID aus dem Gemeindeschlüssel selbst bilden. Die Prüfziffer wäre dann zwar richtig, die Adresse aber vermutlich falsch.
- Die Peppol-ID mit der Leitweg-ID gleichsetzen. Laut Spezifikation (Kapitel 1.4) muss die Peppol-ID nicht identisch mit der Leitweg-ID sein. Die Behörde teilt sie Ihnen mit, wenn sie Peppol nutzt.

## E-Rechnung an Behörden: ERechV, OZG-RE und Peppol

Für Rechnungen an öffentliche Auftraggeber (B2G) gelten eigene Regeln neben dem Umsatzsteuergesetz.

- **Bund:** Die E-Rechnungsverordnung des Bundes (ERechV) verpflichtet Auftragnehmer des Bundes seit dem 27.11.2020 zur E-Rechnung (laut [BMF-FAQ](https://www.bundesfinanzministerium.de/Content/DE/FAQ/e-rechnung.html)). Ausgenommen sind unter anderem Direktaufträge bis 1.000 EUR Auftragswert (laut [FAQ auf e-rechnung-bund.de](https://www.e-rechnung-bund.de/faq/)).
- **Länder und Kommunen:** Die Länder setzen die Richtlinie 2014/55/EU in eigener Kompetenz um, mit eigenen Regeln und Portalen (laut e-rechnung-bund.de). Ob und ab welchem Betrag ein Land oder eine Kommune die E-Rechnung verlangt, klären Sie mit dem jeweiligen Auftraggeber.
- **Verhältnis zum UStG:** B2G fällt nicht unter die umsatzsteuerliche E-Rechnungspflicht, wenn die Verwaltung nicht als Unternehmer handelt. Zwischen UStG und ERechV gibt es laut BMF-FAQ kein Rangverhältnis.

### OZG-RE: das Portal des Bundes

Laut [e-rechnung-bund.de](https://www.e-rechnung-bund.de/faq/) nimmt die unmittelbare Bundesverwaltung E-Rechnungen ausschließlich über die OZG-konforme Rechnungseingangsplattform (OZG-RE) an. Mittelbare Bundesverwaltung und kooperierende Länder können sie ebenfalls nutzen.

| Merkmal | OZG-RE laut e-rechnung-bund.de |
| --- | --- |
| Kanäle | Peppol, E-Mail, Upload, Weberfassung |
| Registrierung | kostenlos, auch über "Mein Unternehmenskonto" (ELSTER) |
| Größe | höchstens 10 MB per E-Mail, 11 MB in der Weberfassung |
| Speicherdauer | Rechnungen werden 28 Tage nach Bereitstellung bzw. nach der letzten Statusänderung gelöscht |

Die Löschung nach 28 Tagen ersetzt nicht Ihre eigene Aufbewahrung. Heben Sie die XRechnung selbst auf, siehe [E-Rechnung archivieren](./e-rechnung-archivieren.md).

### Peppol

Peppol ist ein europäisches Netz für den Austausch von E-Rechnungen. Die KoSIT ist seit Juni 2018 die deutsche Peppol Authority. Laut [Peppol-Länderprofil Deutschland](https://peppol.org/learn-more/country-profiles/germany/) müssen öffentliche Stellen mit E-Rechnungsdienst über Peppol erreichbar sein (IT-Planungsrat, Oktober 2018). Adressiert wird mit Peppol-ID plus Leitweg-ID. Seit Peppol BIS Billing 3.0.18 sind die XRechnung-Regeln dort als deutsches National Ruleset eingebaut (laut [xeinkauf.de](https://xeinkauf.de/aktuelles/peppol/zusammenhang-xrechnung-peppol/)).

Für den Versand über Peppol brauchen Sie einen Peppol-Zugangspunkt (Access Point). Dieses Werkzeug ist keiner: Es erzeugt und prüft die XRechnung, verschickt sie aber nicht.

## Brauche ich im B2B eine Leitweg-ID?

Nein. Die Leitweg-ID ist nur für Rechnungen an öffentliche Auftraggeber gedacht. Laut BMF-FAQ (Frage 6) ist sie im B2B nicht nötig, umsatzsteuerlich genügt in BT-10 ein Platzhalter wie `-`. Viele Unternehmen tragen dort stattdessen eine Bestell- oder Kundennummer ein, wie die Beispielrechnung [01_standard](../../beispiele/01_standard/) mit `BH-2026-0815`.

Fehlt BT-10 ganz, ist das ein Geschäftsregelfehler (BR-DE-15). Laut BMF-Schreiben vom 15.10.2025, Rn. 35a, ist ein fehlendes BT-10 umsatzsteuerlich unbeachtlich. Die Prüfung meldet die XRechnung trotzdem als ungültig, und eine Behörde braucht BT-10 für die Zuordnung.

## Leitweg-ID prüfen und eintragen: Beispiele

### Beispiel 1: Gültige Leitweg-ID prüfen

```bash
erechnung leitweg-id 04011000-1234512345-06
```

```text
04011000-1234512345-06: gültig
```

Exit-Code 0. Das brauchen Sie, bevor Sie eine neue Leitweg-ID im Kundenstamm speichern.

### Beispiel 2: Falsche Prüfziffer erkennen

```bash
erechnung leitweg-id 04011000-1234512345-07
```

```text
04011000-1234512345-07: Prüfziffer falsch, richtig wäre 04011000-1234512345-06
```

Exit-Code 1. Der Vorschlag ist nur die rechnerisch passende Prüfziffer. Oft steckt der Tippfehler aber in der Grob- oder Feinadressierung. Fragen Sie daher bei der Behörde nach, statt die Prüfziffer einfach zu ersetzen.

### Beispiel 3: Fehlende Prüfziffer berechnen

```bash
erechnung leitweg-id 04011000-1234512345 991-33333TEST
```

```text
04011000-1234512345: ohne Prüfziffer, vollständig: 04011000-1234512345-06
991-33333TEST: ohne Prüfziffer, vollständig: 991-33333TEST-33
```

Exit-Code 1, weil die Eingabe so noch keine vollständige Leitweg-ID ist. Das hilft, wenn Sie als Behörde eine eigene Leitweg-ID-Systematik testen.

### Beispiel 4: Falsches Format erkennen

```bash
erechnung leitweg-id 04011000_12345 1-12345-03 04011000-12345-3
```

```text
04011000_12345: kein gültiges Format (Grobadressierung 2-12 Ziffern, optional Feinadressierung bis 30 Zeichen, Prüfziffer 2 Ziffern, getrennt durch Bindestriche)
1-12345-03: kein gültiges Format (Grobadressierung 2-12 Ziffern, optional Feinadressierung bis 30 Zeichen, Prüfziffer 2 Ziffern, getrennt durch Bindestriche)
04011000-12345-3: kein gültiges Format (Grobadressierung 2-12 Ziffern, optional Feinadressierung bis 30 Zeichen, Prüfziffer 2 Ziffern, getrennt durch Bindestriche)
```

Typische Ursachen: Unterstrich statt Bindestrich, nur eine Ziffer in der Grobadressierung, einstellige Prüfziffer.

### Beispiel 5: Leitweg-ID in einer fertigen XRechnung prüfen

```bash
erechnung validieren rechnung-falsche-ziffer.xml
```

```text
rechnung-falsche-ziffer.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): GÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 0 Fehler, 0 Warnungen
  Vorprüfung (Erklärungen, nicht maßgeblich):
  WARNUNG VP-LEITWEG: Leitweg-ID 04011000-12345-04 hat ein falsches Format oder eine falsche Prüfziffer (Formatspezifikation 2.0.2). Die Behörde kann die Rechnung dann nicht zuordnen.
```

Die Datei ist Beispiel 08 mit absichtlich falscher Prüfziffer. Die KoSIT-Regeln melden nichts, erst die Vorprüfung findet den Fehler. Der Exit-Code ist trotzdem 0, weil die Vorprüfung nur Hinweise gibt. Lesen Sie die Ausgabe also immer ganz, nicht nur das Wort "GÜLTIG".

### Beispiel 6: XRechnung ohne BT-10

```bash
erechnung validieren rechnung-ohne-bt10.xml
```

```text
rechnung-ohne-bt10.xml: XRechnung 3.0 (UBL)
  KoSIT-Regeln (xrechnung-3.0.2-validator-configuration-2026-08-31): UNGÜLTIG, Szenario EN16931 XRechnung (UBL Invoice), 1 Fehler, 0 Warnungen
  FEHLER  BR-DE-15: [BR-DE-15] Das Element "Buyer reference" (BT-10) muss übermittelt werden.
  Vorprüfung (Erklärungen, nicht maßgeblich):
  FEHLER  VP-BR-DE-15: Käuferreferenz (BT-10) fehlt. In XRechnung Pflicht, bei Behörden die Leitweg-ID.
```

Exit-Code 1. Mehr zu dieser Meldung in [E-Rechnung Fehlermeldungen](./e-rechnung-fehlermeldungen.md).

### Beispiel 7: XRechnung an eine Behörde erzeugen

Die Eingabe [`eingabe.json`](../../beispiele/08_b2g_leitweg_id/eingabe.json) aus Beispiel 08 enthält die Leitweg-ID an zwei Stellen (Ausschnitt):

```json
{
  "nummer": "RE-2026-0006",
  "leitweg_id": "04011000-12345-03",
  "kaeufer": {
    "name": "Stadt Musterstadt, Amt für Digitalisierung",
    "elektronische_adresse": "04011000-12345-03",
    "elektronische_adresse_schema": "0204"
  }
}
```

```bash
erechnung erstellen beispiele/08_b2g_leitweg_id/eingabe.json -o rechnung-stadt.xml --validieren
```

```text
rechnung-stadt.xml: xrechnung-ubl, Rechnung RE-2026-0006, Zahlbetrag 3.590,83 EUR
  KoSIT-Regeln: GÜLTIG (EN16931 XRechnung (UBL Invoice))
```

Ist die Leitweg-ID in der Eingabe falsch, erscheint beim Erstellen auf stderr die Warnung `VP-LEITWEG`. Die Datei wird trotzdem geschrieben.

### Beispiel 8: Leitweg-ID in Python prüfen

```python
from erechnung import leitweg_id_gueltig

for wert in ["04011000-1234512345-06", "04011000-1234512345-07", "04011000-1234512345"]:
    print(wert, leitweg_id_gueltig(wert))
```

```text
04011000-1234512345-06 True
04011000-1234512345-07 False
04011000-1234512345 False
```

Ohne das Paket genügt für die Prüfziffer diese Funktion (Python erlaubt Umlaute in Namen):

```python
def prüfziffer(grob: str, fein: str = "") -> str:
    """Prüfziffer nach ISO/IEC 7064 Mod 97-10, Buchstaben A=10 bis Z=35."""
    zahl = "".join(str(int(z, 36)) for z in (grob + fein).upper()) + "00"
    return f"{98 - int(zahl) % 97:02d}"


print(prüfziffer("04011000", "1234512345"))  # 06
print(prüfziffer("991", "33333TEST"))        # 33
```

Für KI-Assistenten gibt es das gleiche als MCP-Werkzeug `erechnung_leitweg_id`, siehe [E-Rechnung mit KI prüfen](./e-rechnung-ki-mcp.md).

## Schritt für Schritt: XRechnung an eine Behörde schicken

1. **Leitweg-ID beschaffen.** Sie steht meist im Auftrag oder in der Bestellung. Fehlt sie, fragen Sie die Vergabestelle. Notieren Sie auch, über welches Portal oder welchen Kanal die Behörde Rechnungen annimmt.
2. **Leitweg-ID prüfen.** Geben Sie `erechnung leitweg-id <ID>` ein. Bei "Prüfziffer falsch" oder "kein gültiges Format" fragen Sie nach, bevor Sie die Rechnung schreiben.
3. **Leitweg-ID im Rechnungsprogramm eintragen.** Sie gehört in BT-10, in Programmen oft als "Käuferreferenz", "Kundenreferenz" oder "Leitweg-ID" bezeichnet. Wenn die Behörde es verlangt, auch als elektronische Adresse des Käufers mit Schema `0204`.
4. **XRechnung erzeugen.** Mit diesem Werkzeug: `erechnung erstellen eingabe.json -o rechnung.xml`, siehe [E-Rechnung erstellen](./e-rechnung-erstellen.md). Welches Format die Behörde annimmt, steht in ihren Vorgaben.
5. **XRechnung prüfen.** `erechnung validieren rechnung.xml` muss "GÜLTIG" zeigen und darf keine Warnung `VP-LEITWEG` enthalten. Mit `--bericht prüfberichte` legen Sie einen Prüfbericht zum Aufbewahren ab.
6. **Einreichen.** Beim Bund über die OZG-RE (Peppol, E-Mail, Upload oder Weberfassung), bei Ländern und Kommunen über den Kanal, den der Auftraggeber nennt.
7. **Aufbewahren.** Heben Sie die XRechnung im Ursprungsformat auf. Die OZG-RE löscht sie 28 Tage nach Bereitstellung bzw. letzter Statusänderung.

## Häufige Fehler

| Fehler | Symptom | Lösung |
| --- | --- | --- |
| BT-10 leer | `BR-DE-15` "Das Element "Buyer reference" (BT-10) muss übermittelt werden." | Leitweg-ID eintragen, im B2B eine Referenz oder `-` |
| Prüfziffer vertippt | Vorprüfung `VP-LEITWEG`, KoSIT meldet nichts | Leitweg-ID beim Auftraggeber bestätigen lassen |
| Bindestrich verrutscht | Prüfziffer stimmt, Behörde kann die Rechnung nicht zuordnen | Ziffernfolge und Bindestriche mit dem Auftrag vergleichen |
| Unterstrich, Leerzeichen oder Punkt statt Bindestrich | "kein gültiges Format" | Nur `-` (U+002D) verwenden |
| Leitweg-ID nur in BT-49, nicht in BT-10 | `BR-DE-15` | Leitweg-ID in BT-10 eintragen |
| Elektronische Adresse des Käufers fehlt | `PEPPOL-EN16931-R010` "Buyer electronic address MUST be provided" | BT-49 füllen, bei Behörden die Adresse nach deren Vorgabe, zum Beispiel die Leitweg-ID mit Schema `0204` |
| ZUGFeRD EN 16931, obwohl die Behörde XRechnung verlangt | Prüfung "GÜLTIG" im Szenario EN16931, nicht im Szenario XRechnung | Format nach Vorgabe der Behörde wählen; beim Bund ZUGFeRD XRECHNUNG nur als reine XML-Datei, nicht als PDF |
| Leitweg-ID einer anderen Abteilung | Rechnung landet bei der falschen Stelle | Für jeden Auftrag die Leitweg-ID aus dem Auftrag nehmen |

## Häufige Fragen

### Was ist die Leitweg-ID bei einer E-Rechnung?

Die Leitweg-ID ist die Empfängeradresse einer öffentlichen Verwaltungseinheit in der XRechnung. Sie steht in BT-10 (Buyer reference) und leitet die Rechnung innerhalb der Behörde an die richtige Stelle weiter.

### Wo finde ich die Leitweg-ID meines Auftraggebers?

Die Leitweg-ID steht in der Regel im Auftrag, in der Bestellung oder im Vertrag der Behörde. Steht sie dort nicht, fragen Sie bei der Vergabe- oder Rechnungsstelle nach.

### Wie wird die Prüfziffer der Leitweg-ID berechnet?

Die Prüfziffer wird nach ISO/IEC 7064 Mod 97-10 berechnet: Grob- und Feinadressierung ohne Bindestriche aneinanderhängen, Buchstaben durch 10 bis 35 ersetzen, `00` anhängen, den Rest bei Division durch 97 von 98 abziehen. Aus `04011000-1234512345` wird so `04011000-1234512345-06`.

### Prüft der KoSIT-Validator die Leitweg-ID?

Nein, die KoSIT-Regeln prüfen nur, ob BT-10 vorhanden ist. Eine falsche Prüfziffer blieb im Test offiziell gültig. `erechnung validieren` meldet sie zusätzlich in der Vorprüfung als `VP-LEITWEG`.

### Brauche ich eine Leitweg-ID für Rechnungen an Unternehmen?

Nein, im B2B brauchen Sie keine Leitweg-ID. BT-10 muss in einer XRechnung aber gefüllt sein, laut BMF-FAQ genügt umsatzsteuerlich ein Platzhalter wie `-`.

### Muss ich Rechnungen an den Bund über die OZG-RE schicken?

Ja, die unmittelbare Bundesverwaltung nimmt E-Rechnungen laut e-rechnung-bund.de ausschließlich über die OZG-RE an. Dort können Sie per Peppol, E-Mail, Upload oder Weberfassung einreichen. Für Länder und Kommunen gelten deren eigene Portale und Regeln.

### Gilt die E-Rechnungspflicht gegenüber Behörden auch für kleine Beträge?

Beim Bund sind laut e-rechnung-bund.de unter anderem Direktaufträge bis 1.000 EUR Auftragswert von der ERechV ausgenommen. Länder und Kommunen regeln das selbst. Fragen Sie im Zweifel den Auftraggeber.

> **Hinweis:** Diese Anleitung erklärt Technik und Rechtslage allgemein, Stand siehe oben. Sie ist keine Steuer- oder Rechtsberatung. Die Autoren sind weder Steuerberater noch Rechtsanwälte. Die Autoren erbringen keine Hilfeleistung in Steuersachen. Für Ihren Einzelfall wenden Sie sich an Ihre Steuerberatung. Alle Angaben ohne Gewähr.
>
> DATEV, Lexware, sevdesk, SAP, ELSTER, ZUGFeRD, Factur-X und XRechnung sind Marken oder Bezeichnungen ihrer jeweiligen Inhaber. Dieses Projekt ist mit keinem dieser Anbieter, mit der KoSIT oder dem FeRD verbunden.

## Weiterlesen

- [XRechnung: Format, Aufbau und Pflichtfelder](./xrechnung.md)
- [E-Rechnung prüfen: Validator mit den offiziellen Regeln](./e-rechnung-validator.md)
- [E-Rechnung Fehlermeldungen: BR-DE-15 und andere](./e-rechnung-fehlermeldungen.md)
- [E-Rechnung erstellen](./e-rechnung-erstellen.md)
- [XRechnung oder ZUGFeRD](./xrechnung-oder-zugferd.md)
- Beispiel: [Rechnung an eine Behörde (08_b2g_leitweg_id)](../../beispiele/08_b2g_leitweg_id/), [KoSIT-Ansicht](../../beispiele/08_b2g_leitweg_id/ansicht_kosit.html), [Übersicht aller Beispiele](../../beispiele/README.md)
