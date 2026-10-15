"""Alle Dateien der KoSIT-Testsuite lesen und vorprüfen (läuft, wenn die Testsuite verfügbar ist)."""
import os
import sys
from pathlib import Path

import pytest

from erechnung.lesen import format_erkennen, lesen
from erechnung.pruefen import vorpruefung

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))


def _instanzen():
    if not (os.environ.get("ERECHNUNG_KOSIT_TESTSUITE") or os.environ.get("ERECHNUNG_TESTSUITE_LADEN")):
        return []
    from _werkzeuge import testsuite

    return sorted((testsuite() / "instances").rglob("*.xml"))


# Technische Testfälle ohne Steuernummer: nach UStG ein Mangel, für KoSIT kein Fehler.
OHNE_STEUERNUMMER = {"01.05_minimal_test_ubl.xml", "01.05_minimal_test_uncefact.xml"}


@pytest.mark.parametrize("datei", _instanzen(), ids=lambda p: p.name)
def test_testsuite_lesen_und_vorpruefen(datei):
    xml = datei.read_bytes()
    r = lesen(xml)
    assert r.nummer and r.summen.zahlbetrag is not None
    fehler = {b.code for b in vorpruefung(r, format_erkennen(xml)) if b.stufe == "error"}
    if datei.name in OHNE_STEUERNUMMER:
        fehler.discard("VP-14-4-2")
    assert not fehler
