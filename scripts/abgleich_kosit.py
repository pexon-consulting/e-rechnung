"""Eigene offizielle Prüfung gegen den KoSIT-Validator (Java) abgleichen.

Geprüft werden die KoSIT-Testsuite, alle Beispiele in UBL und CII sowie absichtlich
kaputte Varianten davon. Verglichen wird je Datei: angenommen oder abgelehnt, und
die Menge der Regel-Codes mit ihrer Original-Stufe.

    python scripts/abgleich_kosit.py [--java java]

Exit-Code 0, wenn alle Dateien übereinstimmen.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from importlib import resources
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).parent))
from _werkzeuge import VALIDATOR_SHA256, VALIDATOR_URL, datei, testsuite  # noqa: E402

from erechnung import offiziell  # noqa: E402
from erechnung.eingabe import laden  # noqa: E402
from erechnung.schreiben_cii import cii  # noqa: E402
from erechnung.schreiben_ubl import ubl  # noqa: E402

VARL = "{http://www.xoev.de/de/validator/varl/1}"


def varianten(xml: bytes) -> dict[str, bytes]:
    s = xml.decode()
    v = {
        "ohne_leitweg": re.sub(r"<(cbc|ram):BuyerReference>[^<]*</(cbc|ram):BuyerReference>\s*", "", s, count=1),
        "summe_falsch": re.sub(r"(<(cbc:PayableAmount|ram:DuePayableAmount)[^>]*>)([0-9.]+)",
                               lambda m: m.group(1) + f"{float(m.group(3)) + 1:.2f}", s, count=1),
        "satz_falsch": s.replace("<cbc:Percent>19</cbc:Percent>", "<cbc:Percent>16</cbc:Percent>", 1)
                        .replace("<ram:RateApplicablePercent>19</", "<ram:RateApplicablePercent>16</", 1),
        "einheit_falsch": re.sub(r'unitCode="[A-Z0-9]+"', 'unitCode="STK"', s, count=1),
        "ohne_kontakt": re.sub(r"<cac:Contact>.*?</cac:Contact>|<ram:DefinedTradeContact>.*?</ram:DefinedTradeContact>",
                               "", s, count=1, flags=re.S),
        "schema_kaputt": s.replace("<cbc:IssueDate>", "<cbc:Ausgestellt>x</cbc:Ausgestellt><cbc:IssueDate>", 1)
                          .replace("<ram:TypeCode>", "<ram:Typ>x</ram:Typ><ram:TypeCode>", 1),
        "datum_falsch": re.sub(r"(<cbc:IssueDate>)[^<]+", r"\g<1>2026-13-45", s, count=1)
                         .replace('format="102">2026', 'format="102">2026-', 1),
    }
    return {k: w.encode() for k, w in v.items() if w != s}


def kosit_ergebnis(bericht: Path) -> tuple[bool, list[tuple[str, str]]]:
    text = bericht.read_bytes()
    angenommen = b"<rep:accept" in text.split(b"<rep:assessment>")[1][:30]
    codes = set()
    for m in etree.fromstring(text).iter(f"{VARL}message"):
        code = m.get("code") or ""
        if not code or code.startswith(("cvc-", "s4s", "src-")):
            code = "XSD"
        codes.add((m.get("level"), code))
    return angenommen, sorted(codes)


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--java", default="java")
    args = a.parse_args()

    arbeit = Path(tempfile.mkdtemp(prefix="abgleich-"))
    ein = arbeit / "ein"
    ein.mkdir()
    dateien: list[Path] = []
    for j in sorted(resources.files("erechnung").joinpath("beispiele").iterdir()):
        if not j.name.endswith(".json"):
            continue
        for syntax, f in (("ubl", ubl), ("cii", cii)):
            xml = f(laden(Path(str(j))))
            name = f"{j.name[:-5]}_{syntax}"
            for zusatz, inhalt in {"": xml, **{f"__{k}": w for k, w in varianten(xml).items()}}.items():
                ziel = ein / f"{name}{zusatz}.xml"
                ziel.write_bytes(inhalt)
                dateien.append(ziel)
    dateien += sorted((testsuite() / "instances").rglob("*.xml"))

    konfig = offiziell.konfiguration()
    jar = datei(VALIDATOR_URL, VALIDATOR_SHA256)
    aus = arbeit / "berichte"
    lauf = subprocess.run([args.java, "-jar", str(jar), "-s", str(konfig / "scenarios.xml"), "-r", str(konfig),
                           "-o", str(aus), *map(str, dateien)], capture_output=True, text=True)
    if not aus.exists():
        print(lauf.stdout[-2000:], lauf.stderr[-2000:], file=sys.stderr)
        return 2

    gleich = abgelehnt = 0
    for d in dateien:
        k_ok, k_codes = kosit_ergebnis(aus / f"{d.stem}-report.xml")
        u = offiziell.pruefen(d.read_bytes())
        u_codes = sorted({(b.stufe_original or b.stufe, b.code) for b in u.befunde})
        abgelehnt += not k_ok
        if k_ok == u.akzeptiert and k_codes == u_codes:
            gleich += 1
        else:
            print(f"ABWEICHUNG {d.name}: KoSIT {k_ok} {k_codes} | e-rechnung {u.akzeptiert} {u_codes}")
    print(f"{len(dateien)} Dateien, {gleich} gleich, {len(dateien) - gleich} Abweichungen, KoSIT lehnt {abgelehnt} ab")
    return 0 if gleich == len(dateien) else 1


if __name__ == "__main__":
    sys.exit(main())
