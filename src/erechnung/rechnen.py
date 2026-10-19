"""Rechenregeln der EN 16931 (BR-CO-*), damit erzeugte Rechnungen aufgehen.

Jede Position wird auf zwei Nachkommastellen gerundet, die Steuer je
Kategorie und Satz aus der gerundeten Basis berechnet. So rechnen auch die
Schematron-Regeln der KoSIT nach.
"""

from __future__ import annotations

from collections import OrderedDict
from decimal import ROUND_HALF_UP, Decimal

from .codelisten import BEFREIUNGSGRUND_PFLICHT, STANDARD_BEFREIUNGSGRUND
from .modell import NachlassZuschlag, Position, Rechnung, Steuer, Summen

CENT = Decimal("0.01")
NULL = Decimal("0")


def runden(wert: Decimal) -> Decimal:
    return wert.quantize(CENT, rounding=ROUND_HALF_UP)


def _betrag(nz: NachlassZuschlag, basis: Decimal) -> Decimal:
    if nz.prozent is not None and not nz.betrag:
        nz.basis = runden(nz.basis if nz.basis is not None else basis)
        nz.betrag = runden(nz.basis * nz.prozent / 100)
    return runden(nz.betrag)


def positionsbetrag(pos: Position) -> Decimal:
    """BT-131 = Menge x (Preis / Basismenge) - Nachlässe + Zuschläge (BR-LIN-04)."""
    basismenge = pos.basismenge or Decimal("1")
    brutto = runden(pos.menge * pos.preis / basismenge)
    for nz in pos.nachlaesse:
        betrag = _betrag(nz, brutto)
        brutto += betrag if nz.zuschlag else -betrag
    return runden(brutto)


def _schluessel(kategorie: str, satz: Decimal | None) -> tuple[str, Decimal | None]:
    if kategorie == "O":
        return ("O", None)
    return (kategorie, NULL if satz is None else Decimal(satz).normalize())


def berechnen(r: Rechnung) -> Rechnung:
    """Füllt BT-131, BG-23 und BG-22. Gibt die Rechnung zurück."""
    for pos in r.positionen:
        pos.nettobetrag = positionsbetrag(pos)
        if pos.kategorie in {"E", "Z", "AE", "K", "G"} and pos.satz is None:
            pos.satz = NULL

    summe_positionen = sum((p.nettobetrag for p in r.positionen), NULL)

    gruppen: OrderedDict[tuple[str, Decimal | None], Decimal] = OrderedDict()
    for pos in r.positionen:
        k = _schluessel(pos.kategorie, pos.satz)
        gruppen[k] = gruppen.get(k, NULL) + pos.nettobetrag

    nachlaesse = zuschlaege = NULL
    for nz in r.nachlaesse:
        betrag = _betrag(nz, summe_positionen)
        k = _schluessel(nz.kategorie, nz.satz)
        if nz.zuschlag:
            zuschlaege += betrag
            gruppen[k] = gruppen.get(k, NULL) + betrag
        else:
            nachlaesse += betrag
            gruppen[k] = gruppen.get(k, NULL) - betrag

    r.steuern = []
    for (kategorie, satz), basis in gruppen.items():
        basis = runden(basis)
        betrag = NULL if satz is None else runden(basis * satz / 100)
        grund = r.befreiungsgruende.get(kategorie, "")
        if not grund and kategorie in BEFREIUNGSGRUND_PFLICHT:
            grund = STANDARD_BEFREIUNGSGRUND.get(kategorie, "")
        r.steuern.append(Steuer(kategorie=kategorie, satz=satz, basis=basis, betrag=betrag, befreiungsgrund=grund))

    netto = runden(summe_positionen - nachlaesse + zuschlaege)
    steuer = runden(sum((s.betrag for s in r.steuern), NULL))
    brutto = netto + steuer
    vorauszahlung = runden(r.vorauszahlung or NULL)
    r.summen = Summen(
        positionen=runden(summe_positionen),
        nachlaesse=runden(nachlaesse),
        zuschlaege=runden(zuschlaege),
        netto=netto,
        steuer=steuer,
        brutto=brutto,
        vorauszahlung=vorauszahlung,
        zahlbetrag=brutto - vorauszahlung,
    )
    return r


def skonto_zeile(tage: int, prozent: Decimal, basis: Decimal | None = None) -> str:
    """Skonto im XRechnung-Format für BT-20, z. B. ``#SKONTO#TAGE=14#PROZENT=2.00#``."""
    zeile = f"#SKONTO#TAGE={int(tage)}#PROZENT={Decimal(prozent).quantize(CENT)}#"
    if basis is not None:
        zeile += f"BASISBETRAG={runden(basis)}#"
    return zeile


def zahlungsbedingungen(r: Rechnung) -> str:
    """BT-20 inklusive Skonto-Zeile. XRechnung verlangt einen Zeilenumbruch nach jeder Skonto-Angabe."""
    teile = []
    z = r.zahlung
    if z.skonto_tage and z.skonto_prozent:
        teile.append(skonto_zeile(z.skonto_tage, z.skonto_prozent) + "\n")
    if z.bedingungen:
        teile.append(z.bedingungen)
    return "".join(teile)



def bedingungen_lesbar(text: str) -> str:
    """#SKONTO#-Zeilen nach XRechnung in Klartext übersetzen, übrigen Text unverändert lassen."""
    zeilen = []
    for zeile in (text or "").splitlines():
        zeile = zeile.strip()
        werte = dict(t.split("=", 1) for t in zeile.strip("#").split("#") if "=" in t)
        if zeile.startswith("#SKONTO#") and "TAGE" in werte and "PROZENT" in werte:
            satz = f"{werte['PROZENT'].replace('.', ',')} % Skonto bei Zahlung innerhalb von {werte['TAGE']} Tagen"
            if "BASISBETRAG" in werte:
                satz += f" auf {werte['BASISBETRAG'].replace('.', ',')} EUR"
            zeilen.append(satz)
        elif zeile:
            zeilen.append(zeile)
    return "\n".join(zeilen)
