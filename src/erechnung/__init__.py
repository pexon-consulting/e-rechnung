"""E-Rechnung in Python: XRechnung und ZUGFeRD lesen, prüfen, erstellen, anzeigen, nach DATEV exportieren.

    from erechnung import lesen, validieren, laden, ubl, cii

    ergebnis = validieren("rechnung.xml")
    print(ergebnis.gueltig)
"""

__version__ = "0.1.0"

from .eingabe import aus_dict, laden  # noqa: E402
from .lesen import erkennen, lesen  # noqa: E402
from .modell import Adresse, Kontakt, Lieferung, NachlassZuschlag, Partei, Position, Rechnung, Zahlung  # noqa: E402
from .rechnen import berechnen  # noqa: E402
from .schreiben_cii import cii  # noqa: E402
from .schreiben_ubl import ubl  # noqa: E402
from .validieren import leitweg_id_gueltig, validieren  # noqa: E402

__all__ = [
    "Adresse", "Kontakt", "Lieferung", "NachlassZuschlag", "Partei", "Position", "Rechnung", "Zahlung",
    "aus_dict", "berechnen", "cii", "erkennen", "laden", "leitweg_id_gueltig", "lesen", "ubl", "validieren",
]
