"""Rechnungsdaten aus JSON, TOML oder einem dict ins Modell übernehmen."""

from __future__ import annotations

import dataclasses
import json
import typing
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from . import modell
from .modell import Rechnung


class Eingabefehler(ValueError):
    pass


# Freitextfelder, in denen Zeilenumbrüche erlaubt sind (BT-20 braucht sie für #SKONTO#).
MEHRZEILIG = {"notizen", "notiz", "beschreibung", "bedingungen"}


def _einzeilig(wert: str) -> str:
    """Zeilenumbrüche und Steuerzeichen durch Leerzeichen ersetzen.

    Namen, Anschriften und Nummern landen in Dateinamen, CSV-Zeilen und
    Ansichten; ein Umbruch darin kann dort eine eigene Zeile erzeugen.
    """
    if any(z in wert for z in "\r\n\t\v\f\x85\u2028\u2029"):
        return " ".join(wert.split())
    return wert


def _typ(feld_typ: Any) -> tuple[Any, bool]:
    """Kern-Typ und ob es eine Liste ist. ``str | None`` -> (str, False)."""
    herkunft = typing.get_origin(feld_typ)
    if herkunft is list:
        return typing.get_args(feld_typ)[0], True
    if herkunft in (typing.Union, getattr(__import__("types"), "UnionType", None)):
        argumente = [a for a in typing.get_args(feld_typ) if a is not type(None)]
        return _typ(argumente[0])
    return feld_typ, False


def _wert(typ: Any, wert: Any, pfad: str) -> Any:
    if wert is None:
        return None
    if typ is Decimal:
        try:
            return Decimal(str(wert).replace(",", ".")) if not isinstance(wert, Decimal) else wert
        except InvalidOperation as e:
            raise Eingabefehler(f"{pfad}: keine Zahl: {wert!r}") from e
    if typ is date:
        if isinstance(wert, date):
            return wert
        try:
            return date.fromisoformat(str(wert))
        except ValueError as e:
            raise Eingabefehler(f"{pfad}: Datum im Format JJJJ-MM-TT erwartet, nicht {wert!r}") from e
    if typ is int:
        return int(wert)
    if typ is str:
        return str(wert)
    if typ is dict or typing.get_origin(typ) is dict:
        return dict(wert)
    if dataclasses.is_dataclass(typ):
        return _objekt(typ, wert, pfad)
    return wert


def _objekt(klasse: type, daten: Any, pfad: str) -> Any:
    if not isinstance(daten, dict):
        raise Eingabefehler(f"{pfad}: Objekt erwartet")
    hinweise = typing.get_type_hints(klasse, vars(modell))
    felder = {f.name: f for f in dataclasses.fields(klasse)}
    unbekannt = set(daten) - set(felder)
    if unbekannt:
        raise Eingabefehler(f"{pfad}: unbekannte Felder {sorted(unbekannt)}. Erlaubt: {sorted(felder)}")
    werte = {}
    for name, inhalt in daten.items():
        typ, liste = _typ(hinweise[name])
        if liste:
            if not isinstance(inhalt, list):
                raise Eingabefehler(f"{pfad}.{name}: Liste erwartet")
            werte[name] = [_wert(typ, x, f"{pfad}.{name}[{i}]") for i, x in enumerate(inhalt)]
        else:
            werte[name] = _wert(typ, inhalt, f"{pfad}.{name}")
            if typ is str and isinstance(werte[name], str) and name not in MEHRZEILIG:
                werte[name] = _einzeilig(werte[name])
    try:
        return klasse(**werte)
    except TypeError as e:
        fehlend = [f.name for f in felder.values()
                   if f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING and f.name not in werte]
        raise Eingabefehler(f"{pfad}: Pflichtfelder fehlen: {fehlend}") from e


def aus_dict(daten: dict) -> Rechnung:
    return _objekt(Rechnung, daten, "rechnung")


def laden(pfad: str | Path) -> Rechnung:
    pfad = Path(pfad)
    text = pfad.read_text(encoding="utf-8")
    if pfad.suffix.lower() == ".toml":
        try:
            import tomllib
        except ImportError:  # Python 3.10
            try:
                import tomli as tomllib  # type: ignore[no-redef]
            except ImportError as e:
                raise Eingabefehler('TOML braucht unter Python 3.10 das Extra toml: pip install "e-rechnung[toml]"') from e
        daten = tomllib.loads(text)
    else:
        daten = json.loads(text)
    return aus_dict(daten)
