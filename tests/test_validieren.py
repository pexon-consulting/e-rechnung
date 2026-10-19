import re

import pytest

from erechnung import offiziell
from erechnung.lesen import KeineERechnung, lesen
from erechnung.validieren import iban_gueltig, leitweg_id_gueltig, leitweg_pruefziffer, validieren
from erechnung.schreiben_cii import cii
from erechnung.schreiben_ubl import ubl

from conftest import beispiel, braucht_saxon


def _codes(befunde):
    return {b.code for b in befunde if b.stufe == "error"}


def test_iban():
    assert iban_gueltig("DE79000000001234567890")
    assert iban_gueltig("DE79 0000 0000 1234 5678 90")
    assert not iban_gueltig("DE80000000001234567890")
    assert not iban_gueltig("kein iban")


def test_vorpruefung_sauber_bei_beispiel():
    e = validieren(ubl(beispiel("01_standard")), offiziell_pruefen=False)
    assert e.vorpruefung_ok, e.vorpruefung
    assert e.gueltig is None


def test_vorpruefung_findet_fehlende_leitweg_id():
    xml = re.sub(rb"<cbc:BuyerReference>[^<]*</cbc:BuyerReference>", b"", ubl(beispiel("01_standard")))
    assert "VP-BR-DE-15" in _codes(validieren(xml, offiziell_pruefen=False).vorpruefung)


def test_vorpruefung_findet_rechenfehler():
    xml = ubl(beispiel("01_standard")).replace(b">2009.91<", b">2010.91<")
    codes = _codes(validieren(xml, offiziell_pruefen=False).vorpruefung)
    assert "VP-BRUTTO" in codes or "VP-ZAHLBETRAG" in codes


def test_vorpruefung_kleinunternehmer_ohne_grund():
    r = beispiel("07_kleinunternehmer")
    r.befreiungsgruende = {}
    xml = ubl(r).replace("Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.".encode(), b"")
    assert "VP-14-4-8" in _codes(validieren(xml, offiziell_pruefen=False).vorpruefung)


def test_vorpruefung_reverse_charge_mit_registernummer_statt_ust_id():
    r = beispiel("05_reverse_charge_13b")
    r.kaeufer.ust_id = ""
    r.kaeufer.register = "HRB 000000"
    assert "VP-13B" not in _codes(validieren(ubl(r), offiziell_pruefen=False).vorpruefung)
    r.kaeufer.register = ""
    assert "VP-13B" in _codes(validieren(ubl(r), offiziell_pruefen=False).vorpruefung)


@braucht_saxon
def test_offiziell_reverse_charge_mit_registernummer_statt_ust_id():
    r = beispiel("05_reverse_charge_13b")
    r.kaeufer.ust_id = ""
    r.kaeufer.register = "HRB 000000"
    assert "BR-AE-02" not in _codes(offiziell.validieren(ubl(r)).befunde)


def test_kaputte_datei_ergibt_befund():
    e = validieren(b"<kaputt", offiziell_pruefen=False)
    assert not e.vorpruefung_ok


@braucht_saxon
def test_offiziell_lehnt_fehlende_leitweg_id_ab():
    xml = re.sub(rb"<ram:BuyerReference>[^<]*</ram:BuyerReference>", b"", cii(beispiel("01_standard")))
    bericht = offiziell.validieren(xml)
    assert not bericht.akzeptiert
    assert "BR-DE-15" in _codes(bericht.befunde)


@braucht_saxon
def test_offiziell_schemafehler():
    xml = ubl(beispiel("01_standard")).replace(b"<cbc:IssueDate>", b"<cbc:Falsch>x</cbc:Falsch><cbc:IssueDate>", 1)
    bericht = offiziell.validieren(xml)
    assert not bericht.akzeptiert
    assert bericht.befunde[0].code == "XSD"


@braucht_saxon
def test_offiziell_falscher_steuersatz():
    xml = ubl(beispiel("01_standard")).replace(b"<cbc:Percent>19</cbc:Percent>", b"<cbc:Percent>16</cbc:Percent>", 1)
    bericht = offiziell.validieren(xml)
    assert not bericht.akzeptiert


@braucht_saxon
def test_offiziell_kein_szenario():
    bericht = offiziell.validieren(b"<Invoice xmlns='urn:oasis:names:specification:ubl:schema:xsd:Invoice-2'/>")
    assert not bericht.akzeptiert
    assert bericht.szenario == "kein Szenario"


@braucht_saxon
def test_umstufung_wird_angewendet():
    """BR-CL-23 (Einheitencode) ist im XRechnung-Szenario nur eine Warnung."""
    xml = ubl(beispiel("01_standard")).replace(b'unitCode="HUR"', b'unitCode="QQQ"')
    assert b'unitCode="QQQ"' in xml
    bericht = offiziell.validieren(xml)
    treffer = [b for b in bericht.befunde if b.code == "BR-CL-23"]
    assert treffer and treffer[0].stufe == "warning" and treffer[0].stufe_original == "error"
    assert bericht.akzeptiert


@braucht_saxon
def test_bericht_wird_gespeichert(tmp_path):
    from erechnung.validieren import bericht_speichern

    xml = ubl(beispiel("01_standard"))
    datei = bericht_speichern(validieren(xml), xml, tmp_path)
    inhalt = datei.read_text(encoding="utf-8")
    assert '"akzeptiert": true' in inhalt
    assert offiziell.KONFIG_VERSION in inhalt


def test_leitweg_id_beispiel_aus_der_spezifikation():
    assert leitweg_pruefziffer("04011000", "1234512345") == "06"
    assert leitweg_id_gueltig("04011000-1234512345-06")
    assert leitweg_id_gueltig("04011000-12345-03")
    assert not leitweg_id_gueltig("04011000-1234512345-07")
    assert not leitweg_id_gueltig("BH-2026-0815")


def test_leitweg_id_mit_buchstaben():
    pz = leitweg_pruefziffer("991", "ABC12")
    assert leitweg_id_gueltig(f"991-ABC12-{pz}")
    assert leitweg_id_gueltig(f"991-abc12-{pz}")


def test_vorpruefung_falsche_leitweg_id():
    r = beispiel("08_b2g_leitweg_id")
    r.leitweg_id = "04011000-12345-04"
    r.kaeufer.elektronische_adresse = "04011000-12345-04"
    codes = {b.code for b in validieren(ubl(r), offiziell_pruefen=False).vorpruefung}
    assert "VP-LEITWEG" in codes


def test_doctype_mit_externer_entitaet_wird_abgelehnt(tmp_path):
    geheim = tmp_path / "geheim.txt"
    geheim.write_text("GEHEIMNIS123")
    xml = ubl(beispiel("01_standard")).decode()
    kopf, rest = xml.split("?>", 1)
    xml = f'{kopf}?>\n<!DOCTYPE Invoice [<!ENTITY e SYSTEM "{geheim.as_uri()}">]>{rest}'
    xml = xml.replace("<cbc:ID>RE-", "<cbc:ID>&e;RE-", 1)
    assert "&e;" in xml
    with pytest.raises(KeineERechnung, match="DOCTYPE"):
        lesen(xml.encode())
    e = validieren(xml.encode(), offiziell_pruefen=False)
    assert not e.vorpruefung_ok
    assert "DOCTYPE" in e.vorpruefung[0].text
    assert "GEHEIMNIS" not in repr(e.als_dict())


@braucht_saxon
def test_doctype_offiziell_abgelehnt_ohne_absturz():
    from erechnung import offiziell

    xml = ubl(beispiel("01_standard")).decode()
    kopf, rest = xml.split("?>", 1)
    xml = f"{kopf}?>\n<!DOCTYPE Invoice [<!ENTITY e \"x\">]>{rest}"
    b = offiziell.validieren(xml.encode(), offline=True)
    assert not b.akzeptiert
    assert "DOCTYPE" in b.befunde[0].text
