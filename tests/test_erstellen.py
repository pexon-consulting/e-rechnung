import pytest
from lxml import etree

from erechnung import offiziell
from erechnung.modell import EN16931
from erechnung.schreiben_cii import cii
from erechnung.schreiben_ubl import ubl

from conftest import beispiel, beispiel_namen, braucht_saxon


@braucht_saxon
@pytest.mark.parametrize("name", beispiel_namen())
@pytest.mark.parametrize("syntax", ["ubl", "cii"])
def test_beispiele_sind_offiziell_gueltig(name, syntax):
    xml = (ubl if syntax == "ubl" else cii)(beispiel(name))
    bericht = offiziell.validieren(xml)
    assert bericht.szenario.startswith("EN16931 XRechnung")
    assert bericht.akzeptiert, [(b.code, b.text) for b in bericht.fehler]
    assert not bericht.warnungen, [(b.code, b.text) for b in bericht.warnungen]


@braucht_saxon
@pytest.mark.parametrize("syntax", ["ubl", "cii"])
def test_en16931_ohne_xrechnung(syntax):
    r = beispiel("01_standard")
    r.spezifikation = EN16931
    bericht = offiziell.validieren((ubl if syntax == "ubl" else cii)(r))
    assert bericht.szenario.startswith("EN16931 (")
    assert bericht.akzeptiert


def test_gutschrift_wird_creditnote():
    wurzel = etree.fromstring(ubl(beispiel("03_gutschrift")))
    assert etree.QName(wurzel).localname == "CreditNote"
    assert wurzel.find("{*}CreditNoteLine") is not None


def test_ubl_elementreihenfolge_passt_zum_schema():
    """Ohne saxonche: nur XSD, aber für alle Beispiele."""
    try:
        ordner = offiziell.konfiguration()
    except offiziell.NichtVerfuegbar:
        pytest.skip("KoSIT-Konfiguration nicht verfügbar")
    schemas = {
        "Invoice": etree.XMLSchema(etree.parse(str(ordner / "resources/ubl/2.1/xsd/maindoc/UBL-Invoice-2.1.xsd"))),
        "CreditNote": etree.XMLSchema(etree.parse(str(ordner / "resources/ubl/2.1/xsd/maindoc/UBL-CreditNote-2.1.xsd"))),
        "CrossIndustryInvoice": etree.XMLSchema(etree.parse(str(ordner / "resources/cii/16b/xsd/CrossIndustryInvoice_100pD16B.xsd"))),
    }
    for name in beispiel_namen():
        for f in (ubl, cii):
            wurzel = etree.fromstring(f(beispiel(name)))
            schema = schemas[etree.QName(wurzel).localname]
            assert schema.validate(wurzel), (name, f.__name__, str(schema.error_log))


def test_keine_leeren_elemente():
    for name in beispiel_namen():
        for f in (ubl, cii):
            wurzel = etree.fromstring(f(beispiel(name)))
            for e in wurzel.iter():
                if e.tag.endswith("ApplicableHeaderTradeDelivery"):
                    continue
                assert len(e) or (e.text or "").strip(), (name, e.tag)


@braucht_saxon
def test_kosit_ansicht():
    html = offiziell.html_ansicht(ubl(beispiel("08_b2g_leitweg_id")))
    assert "04011000-12345-03" in html
    assert "<html" in html.lower()
