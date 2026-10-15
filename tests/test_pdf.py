import io

import pytest
from pypdf import PdfReader

from erechnung import pdf
from erechnung.lesen import erkennen, lesen
from erechnung.modell import EN16931
from erechnung.schreiben_cii import cii

from conftest import beispiel, braucht_gs


def _leeres_pdf() -> bytes:
    from pypdf import PdfWriter

    w = PdfWriter()
    w.add_blank_page(595, 842)
    puffer = io.BytesIO()
    w.write(puffer)
    return puffer.getvalue()


def _cii(spezifikation=EN16931):
    r = beispiel("01_standard")
    r.spezifikation = spezifikation
    return cii(r)


def test_einbetten_und_auslesen():
    xml = _cii()
    ergebnis = pdf.einbetten(_leeres_pdf(), xml)
    name, inhalt = pdf.xml_auslesen(ergebnis)
    assert name == "factur-x.xml"
    assert inhalt == xml
    assert erkennen(ergebnis).bezeichnung == "ZUGFeRD/Factur-X Profil EN 16931 (COMFORT)"
    assert lesen(ergebnis).nummer == "RE-2026-0001"


def test_metadaten_fuer_zugferd():
    ergebnis = pdf.einbetten(_leeres_pdf(), _cii())
    leser = PdfReader(io.BytesIO(ergebnis))
    katalog = leser.trailer["/Root"]
    af = katalog["/AF"]
    spec = af[0].get_object()
    assert spec["/AFRelationship"] == "/Alternative"
    assert spec["/UF"] == "factur-x.xml"
    datei = spec["/EF"]["/F"].get_object()
    assert datei["/Subtype"] == "/text/xml"
    xmp = katalog["/Metadata"].get_object().get_data()
    assert b"<fx:ConformanceLevel>EN 16931</fx:ConformanceLevel>" in xmp
    assert b"<pdfaid:part>3</pdfaid:part>" in xmp


def test_xrechnung_profil_heisst_xrechnung_xml():
    ergebnis = pdf.einbetten(_leeres_pdf(), cii(beispiel("01_standard")))
    assert pdf.xml_auslesen(ergebnis)[0] == "xrechnung.xml"


def test_doppelt_einbetten_wird_abgelehnt():
    einmal = pdf.einbetten(_leeres_pdf(), _cii())
    with pytest.raises(ValueError, match="bereits"):
        pdf.einbetten(einmal, _cii())


def test_pdf_ohne_xml_ist_keine_e_rechnung():
    with pytest.raises(pdf.KeinXmlImPdf, match="sonstige Rechnung"):
        pdf.xml_auslesen(_leeres_pdf())


def test_ubl_laesst_sich_nicht_als_zugferd_einbetten():
    from erechnung.schreiben_ubl import ubl

    with pytest.raises(ValueError):
        pdf.einbetten(_leeres_pdf(), ubl(beispiel("01_standard")))


@braucht_gs
def test_lesefassung_ist_pdfa3():
    from erechnung.pdf_layout import pdf as lesefassung

    r = beispiel("02_gemischte_steuersaetze")
    daten = lesefassung(r)
    leser = PdfReader(io.BytesIO(daten))
    katalog = leser.trailer["/Root"]
    assert "/OutputIntents" in katalog
    text = leser.pages[0].extract_text()
    assert "RE-2026-0002" in text
    assert "Zahlbetrag" in text
