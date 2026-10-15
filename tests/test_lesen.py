from decimal import Decimal

import pytest

from erechnung.lesen import KeineERechnung, erkennen, format_erkennen, lesen
from erechnung.rechnen import berechnen
from erechnung.schreiben_cii import cii
from erechnung.schreiben_ubl import ubl

from conftest import beispiel, beispiel_namen


@pytest.mark.parametrize("name", beispiel_namen())
@pytest.mark.parametrize("f", [ubl, cii])
def test_rundlauf(name, f):
    original = berechnen(beispiel(name))
    gelesen = lesen(f(beispiel(name)))
    assert gelesen.nummer == original.nummer
    assert gelesen.art == original.art
    assert gelesen.datum == original.datum
    assert gelesen.leitweg_id == original.leitweg_id
    assert gelesen.summen.zahlbetrag == original.summen.zahlbetrag
    assert gelesen.summen.steuer == original.summen.steuer
    assert len(gelesen.positionen) == len(original.positionen)
    assert [p.nettobetrag for p in gelesen.positionen] == [p.nettobetrag for p in original.positionen]
    assert gelesen.verkaeufer.name == original.verkaeufer.name
    assert gelesen.verkaeufer.ust_id == original.verkaeufer.ust_id
    assert gelesen.kaeufer.adresse.ort == original.kaeufer.adresse.ort
    assert gelesen.zahlung.iban == original.zahlung.iban
    assert gelesen.zahlung.glaeubiger_id == original.zahlung.glaeubiger_id
    assert {(s.kategorie, s.basis) for s in gelesen.steuern} == {(s.kategorie, s.basis) for s in original.steuern}


def test_format_erkennung():
    assert erkennen(ubl(beispiel("01_standard"))).bezeichnung == "XRechnung 3.0 (UBL)"
    assert erkennen(cii(beispiel("01_standard"))).bezeichnung == "XRechnung 3.0 (CII)"


def test_minimum_ist_keine_e_rechnung():
    xml = cii(beispiel("01_standard")).replace(
        b"urn:cen.eu:en16931:2017#compliant#urn:xeinkauf.de:kosit:xrechnung_3.0", b"urn:factur-x.eu:1p0:minimum")
    fmt = format_erkennen(xml)
    assert fmt.bezeichnung == "CII Profil MINIMUM"
    assert fmt.ist_e_rechnung is False


def test_kein_xml():
    with pytest.raises(KeineERechnung):
        format_erkennen(b"Hallo")
    with pytest.raises(KeineERechnung):
        format_erkennen(b"<Bestellung/>")


def test_entities_werden_nicht_aufgeloest(tmp_path):
    geheim = tmp_path / "geheim.txt"
    geheim.write_text("GEHEIM")
    xml = (f'<?xml version="1.0"?><!DOCTYPE x [<!ENTITY e SYSTEM "file://{geheim}">]>'
           '<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" '
           'xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">'
           '<cbc:CustomizationID>urn:cen.eu:en16931:2017</cbc:CustomizationID><cbc:ID>&e;</cbc:ID></Invoice>').encode()
    with pytest.raises(KeineERechnung, match="DOCTYPE") as fehler:
        lesen(xml)
    assert "GEHEIM" not in str(fehler.value)


def test_menge_mit_nachkommastellen():
    r = lesen(cii(beispiel("08_b2g_leitweg_id")))
    assert r.positionen[1].menge == Decimal("6.5")
    assert r.kaeufer.elektronische_adresse_schema == "0204"
