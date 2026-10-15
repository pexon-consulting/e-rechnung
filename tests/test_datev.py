from datetime import datetime
from decimal import Decimal

import pytest

from erechnung import datev
from erechnung.lesen import lesen
from erechnung.schreiben_ubl import ubl

from conftest import beispiel, beispiel_namen

JETZT = datetime(2026, 10, 15, 12, 0, 0)


def _stapel(namen, **kw):
    rechnungen = [lesen(ubl(beispiel(n))) for n in namen]
    return datev.stapel(rechnungen, datev.Einstellungen(**kw), jetzt=JETZT)


def test_kopf_und_spalten():
    daten, _ = _stapel(["01_standard"])
    zeilen = daten.decode("cp1252").split("\r\n")
    kopf = zeilen[0].split(";")
    assert kopf[:6] == ['"EXTF"', "700", "21", '"Buchungsstapel"', "13", "20261015120000000"]
    assert len(kopf) == 31
    assert len(zeilen[1].split(";")) == 125
    assert all(len(z.split(";")) == 125 for z in zeilen[2:] if z)
    assert daten.endswith(b"\r\n")


def test_buchung_standardrechnung():
    daten, _ = _stapel(["01_standard"], skr="04")
    werte = dict(zip(datev.SPALTEN, daten.decode("cp1252").split("\r\n")[2].split(";")))
    assert werte["Umsatz (ohne Soll/Haben-Kz)"] == "2009,91"
    assert werte["Soll/Haben-Kennzeichen"] == '"H"'
    assert werte["Konto"] == "70000"
    assert werte["Gegenkonto (ohne BU-Schlüssel)"] == "6850"
    assert werte["BU-Schlüssel"] == '"9"'
    assert werte["Belegdatum"] == "1510"
    assert werte["Belegfeld 1"] == '"RE-2026-0001"'
    assert werte["Leistungsdatum"] == "30092026"


def test_je_steuersatz_eine_zeile():
    daten, _ = _stapel(["02_gemischte_steuersaetze"])
    zeilen = [z for z in daten.decode("cp1252").split("\r\n")[2:] if z]
    assert len(zeilen) == 2
    betraege = sorted(Decimal(z.split(";")[0].replace(",", ".")) for z in zeilen)
    assert sum(betraege) == Decimal("207.64")


def test_gutschrift_im_soll():
    daten, _ = _stapel(["03_gutschrift"])
    assert daten.decode("cp1252").split("\r\n")[2].split(";")[1] == '"S"'


def test_kreditor_zuordnung_ueber_ust_id():
    daten, hinweise = _stapel(["01_standard", "07_kleinunternehmer"], kreditoren={"DE123456789": 70123})
    zeilen = daten.decode("cp1252").split("\r\n")[2:]
    assert zeilen[0].split(";")[6] == "70123"
    assert zeilen[1].split(";")[6] == "70000"
    assert any("Sammelkreditor" in h for h in hinweise)


def test_reverse_charge_gibt_hinweis():
    _, hinweise = _stapel(["05_reverse_charge_13b"])
    assert any("AE" in h for h in hinweise)


def test_alle_beispiele_exportierbar():
    daten, _ = _stapel(beispiel_namen())
    assert daten.count(b"\r\n") >= len(beispiel_namen()) + 2


def test_fremdwaehrung_abgelehnt():
    r = lesen(ubl(beispiel("01_standard")))
    r.waehrung = "USD"
    with pytest.raises(datev.DatevFehler):
        datev.stapel([r])


def test_wirtschaftsjahr_grenze():
    a = lesen(ubl(beispiel("01_standard")))
    b = lesen(ubl(beispiel("01_standard")))
    b.datum = b.datum.replace(year=2027)
    with pytest.raises(datev.DatevFehler, match="Wirtschaftsjahr"):
        datev.stapel([a, b])


def test_belegfeld_ohne_unerlaubte_zeichen():
    r = lesen(ubl(beispiel("01_standard")))
    r.nummer = "RE 2026_0001 (neu)"
    daten, _ = datev.stapel([r], jetzt=JETZT)
    assert daten.decode("cp1252").split("\r\n")[2].split(";")[10] == '"RE20260001neu"'
