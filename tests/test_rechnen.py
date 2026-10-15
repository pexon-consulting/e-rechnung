from decimal import Decimal

from erechnung.modell import NachlassZuschlag, Partei, Position, Rechnung
from erechnung.rechnen import bedingungen_lesbar, berechnen, positionsbetrag, skonto_zeile, zahlungsbedingungen

from conftest import beispiel

D = Decimal


def _r(positionen, nachlaesse=()):
    from datetime import date

    return Rechnung("1", date(2026, 10, 15), Partei("V"), Partei("K"), positionen=list(positionen), nachlaesse=list(nachlaesse))


def test_positionsbetrag_rundet_kaufmaennisch():
    assert positionsbetrag(Position("1", "x", D("3"), "C62", D("0.3333"))) == D("1.00")
    assert positionsbetrag(Position("1", "x", D("1"), "C62", D("0.125"))) == D("0.13")


def test_basismenge_teilt_den_preis():
    p = Position("1", "Schrauben", D("250"), "C62", D("4.50"), basismenge=D("100"))
    assert positionsbetrag(p) == D("11.25")


def test_positionsnachlass_in_prozent():
    p = Position("1", "x", D("10"), "C62", D("20"), nachlaesse=[NachlassZuschlag(D("0"), "Rabatt", prozent=D("10"))])
    assert positionsbetrag(p) == D("180.00")


def test_gemischte_saetze_und_belegnachlass():
    r = berechnen(beispiel("02_gemischte_steuersaetze"))
    saetze = {(s.kategorie, s.satz): (s.basis, s.betrag) for s in r.steuern}
    assert saetze[("S", D("7"))] == (D("149.70"), D("10.48"))
    assert saetze[("S", D("19"))] == (D("39.88"), D("7.58"))
    assert r.summen.netto == D("189.58")
    assert r.summen.zahlbetrag == D("207.64")


def test_steuer_je_gruppe_nicht_je_position():
    # 3 x 0,10 EUR zu 19 %: je Position gerundet waeren es 0,06, je Gruppe 0,06 (0,057)
    r = berechnen(_r([Position(str(i), "x", D("1"), "C62", D("0.10")) for i in range(3)]))
    assert r.steuern[0].basis == D("0.30")
    assert r.steuern[0].betrag == D("0.06")


def test_zuschlag_erhoeht_basis():
    r = berechnen(_r([Position("1", "x", D("1"), "C62", D("100"))],
                     [NachlassZuschlag(D("10"), "Fracht", zuschlag=True, kategorie="S", satz=D("19"))]))
    assert r.summen.zuschlaege == D("10.00")
    assert r.summen.netto == D("110.00")
    assert r.summen.steuer == D("20.90")


def test_nicht_steuerbar_ohne_satz():
    r = berechnen(_r([Position("1", "x", D("1"), "C62", D("50"), kategorie="O", satz=None)]))
    assert r.steuern[0].satz is None
    assert r.steuern[0].betrag == D("0")
    assert r.steuern[0].befreiungsgrund


def test_kleinunternehmer_null_steuer():
    r = berechnen(beispiel("07_kleinunternehmer"))
    assert r.summen.steuer == D("0.00")
    assert r.steuern[0].kategorie == "E"
    assert "19 UStG" in r.steuern[0].befreiungsgrund


def test_vorauszahlung_mindert_zahlbetrag():
    r = _r([Position("1", "x", D("1"), "C62", D("100"))])
    r.vorauszahlung = D("50")
    berechnen(r)
    assert r.summen.brutto == D("119.00")
    assert r.summen.zahlbetrag == D("69.00")


def test_skonto_format_xrechnung():
    assert skonto_zeile(14, D("2")) == "#SKONTO#TAGE=14#PROZENT=2.00#"
    assert skonto_zeile(10, D("3"), D("100")) == "#SKONTO#TAGE=10#PROZENT=3.00#BASISBETRAG=100.00#"


def test_zahlungsbedingungen_mit_zeilenumbruch():
    r = beispiel("01_standard")
    text = zahlungsbedingungen(r)
    assert text.startswith("#SKONTO#TAGE=10#PROZENT=2.00#\n")
    assert "30 Tagen" in text


def test_skonto_lesbar():
    text = "#SKONTO#TAGE=10#PROZENT=2.00#\n#SKONTO#TAGE=20#PROZENT=1.00#BASISBETRAG=100.00#\nZahlbar in 30 Tagen."
    assert bedingungen_lesbar(text) == ("2,00 % Skonto bei Zahlung innerhalb von 10 Tagen\n"
                                        "1,00 % Skonto bei Zahlung innerhalb von 20 Tagen auf 100,00 EUR\n"
                                        "Zahlbar in 30 Tagen.")
