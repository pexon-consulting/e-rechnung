import json

from erechnung.cli import main

from conftest import braucht_saxon


def test_beispiele_und_lesen(tmp_path, capsys):
    assert main(["beispiele", str(tmp_path)]) == 0
    dateien = sorted(p.name for p in tmp_path.iterdir())
    assert "01_standard.json" in dateien and "01_standard_xrechnung_ubl.xml" in dateien
    assert main(["lesen", str(tmp_path / "01_standard_xrechnung_cii.xml")]) == 0
    aus = capsys.readouterr().out
    assert "XRechnung 3.0 (CII)" in aus and "2.009,91 EUR" in aus


def test_lesen_json(tmp_path, capsys):
    main(["beispiele", str(tmp_path)])
    capsys.readouterr()
    assert main(["lesen", "--json", str(tmp_path / "02_gemischte_steuersaetze_xrechnung_ubl.xml")]) == 0
    daten = json.loads(capsys.readouterr().out)
    assert daten["summen"]["zahlbetrag"] == "207.64"


def test_erstellen_und_anzeigen(tmp_path, capsys):
    main(["beispiele", str(tmp_path)])
    ziel = tmp_path / "neu.xml"
    assert main(["erstellen", str(tmp_path / "08_b2g_leitweg_id.json"), "--format", "xrechnung-cii", "-o", str(ziel)]) == 0
    assert main(["anzeigen", str(ziel), "-o", str(tmp_path / "neu.html")]) == 0
    html = (tmp_path / "neu.html").read_text(encoding="utf-8")
    assert "04011000-12345-03" in html and "E-Rechnung nach EN 16931" in html


def test_erstellen_mit_falscher_eingabe(tmp_path, capsys):
    (tmp_path / "x.json").write_text('{"nummer": "1", "farbe": "rot"}')
    assert main(["erstellen", str(tmp_path / "x.json")]) == 1
    assert "unbekannte Felder" in capsys.readouterr().err


def test_pruefen_ohne_offiziell(tmp_path, capsys):
    main(["beispiele", str(tmp_path)])
    assert main(["validieren", "--ohne-offiziell", str(tmp_path / "01_standard_xrechnung_ubl.xml")]) == 0


@braucht_saxon
def test_pruefen_exit_codes(tmp_path, capsys):
    main(["beispiele", str(tmp_path)])
    gut = tmp_path / "01_standard_xrechnung_ubl.xml"
    assert main(["validieren", str(gut)]) == 0
    schlecht = tmp_path / "schlecht.xml"
    schlecht.write_bytes(gut.read_bytes().replace(b"<cbc:BuyerReference>BH-2026-0815</cbc:BuyerReference>", b""))
    assert main(["validieren", str(schlecht)]) == 1
    assert "BR-DE-15" in capsys.readouterr().out


def test_datev(tmp_path, capsys):
    main(["beispiele", str(tmp_path)])
    dateien = [str(p) for p in sorted(tmp_path.glob("*_ubl.xml"))]
    ziel = tmp_path / "EXTF.csv"
    assert main(["datev", *dateien, "-o", str(ziel), "--skr", "04"]) == 0
    assert ziel.read_bytes().startswith(b'"EXTF";700;21;')


def test_zugferd_und_extrahieren(tmp_path, capsys):
    import io

    from pypdf import PdfWriter

    main(["beispiele", str(tmp_path)])
    w = PdfWriter()
    w.add_blank_page(595, 842)
    puffer = io.BytesIO()
    w.write(puffer)
    (tmp_path / "vorlage.pdf").write_bytes(puffer.getvalue())
    xml = tmp_path / "01_standard_xrechnung_cii.xml"
    assert main(["zugferd", str(xml), "--pdf", str(tmp_path / "vorlage.pdf"), "-o", str(tmp_path / "z.pdf")]) == 0
    assert main(["extrahieren", str(tmp_path / "z.pdf"), "-o", str(tmp_path / "x.xml")]) == 0
    assert (tmp_path / "x.xml").read_bytes() == xml.read_bytes()


def test_erstellen_lehnt_unerlaubte_art_ab(tmp_path, capsys):
    main(["beispiele", str(tmp_path)])
    eingabe = tmp_path / "01_standard.json"
    eingabe.write_text(eingabe.read_text(encoding="utf-8").replace('"nummer"', '"art": "386",\n  "nummer"', 1), encoding="utf-8")
    assert main(["erstellen", str(eingabe), "-o", str(tmp_path / "x.xml")]) == 1
    assert "BR-DE-17" in capsys.readouterr().err
    assert main(["erstellen", str(eingabe), "--format", "en16931-ubl", "-o", str(tmp_path / "x.xml")]) == 0


def test_erstellen_meldet_vorpruefung(tmp_path, capsys):
    main(["beispiele", str(tmp_path)])
    eingabe = tmp_path / "01_standard.json"
    eingabe.write_text(eingabe.read_text(encoding="utf-8").replace('"leitweg_id": "BH-2026-0815",', ""), encoding="utf-8")
    main(["erstellen", str(eingabe), "-o", str(tmp_path / "x.xml")])
    assert "VP-BR-DE-15" in capsys.readouterr().err


def test_leitweg_id_befehl(capsys):
    assert main(["leitweg-id", "04011000-1234512345-06"]) == 0
    assert main(["leitweg-id", "04011000-1234512345-07"]) == 1
    assert "richtig wäre 04011000-1234512345-06" in capsys.readouterr().out
    assert main(["leitweg-id", "04011000-1234512345"]) == 1
    assert "04011000-1234512345-06" in capsys.readouterr().out
