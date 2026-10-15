from decimal import Decimal

import pytest

from erechnung.eingabe import Eingabefehler, aus_dict, laden


def test_minimal():
    r = aus_dict({"nummer": "1", "datum": "2026-10-15", "verkaeufer": {"name": "V"}, "kaeufer": {"name": "K"},
                  "positionen": [{"id": "1", "name": "x", "menge": "2", "einheit": "C62", "preis": "1,50"}]})
    assert r.positionen[0].preis == Decimal("1.50")
    assert r.datum.isoformat() == "2026-10-15"


def test_unbekanntes_feld():
    with pytest.raises(Eingabefehler, match="unbekannte Felder"):
        aus_dict({"nummer": "1", "datum": "2026-10-15", "verkaeufer": {"name": "V", "fax": "1"}, "kaeufer": {"name": "K"}})


def test_falsches_datum():
    with pytest.raises(Eingabefehler, match="JJJJ-MM-TT"):
        aus_dict({"nummer": "1", "datum": "15.10.2026", "verkaeufer": {"name": "V"}, "kaeufer": {"name": "K"}})


def test_pflichtfeld_fehlt():
    with pytest.raises(Eingabefehler, match="Pflichtfelder"):
        aus_dict({"nummer": "1", "verkaeufer": {"name": "V"}, "kaeufer": {"name": "K"}})


def test_toml(tmp_path):
    (tmp_path / "r.toml").write_text('''nummer = "T-1"
datum = 2026-10-15
[verkaeufer]
name = "V"
[kaeufer]
name = "K"
[[positionen]]
id = "1"
name = "Beratung"
menge = 2
einheit = "HUR"
preis = 100
''')
    r = laden(tmp_path / "r.toml")
    assert r.nummer == "T-1" and r.positionen[0].menge == Decimal("2")
