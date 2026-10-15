"""MCP-Server: E-Rechnungen aus Claude, Cursor oder anderen MCP-Clients lesen, prüfen und erstellen.

Start (stdio)::

    erechnung-mcp

Die Werkzeuge arbeiten nur mit lokalen Dateien. Rechnungsdaten verlassen den
Rechner nicht; einzig die KoSIT-Prüfregeln werden beim ersten Prüfen von
GitHub geladen.
"""

from __future__ import annotations

import json
from pathlib import Path

try:  # mcp 2.x
    from mcp.server.mcpserver import MCPServer as _Server
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server  # type: ignore[no-redef]

from . import offiziell
from .anzeigen import html
from .eingabe import aus_dict
from .lesen import erkennen, lesen
from .validieren import validieren

server = _Server(
    "e-rechnung",
    instructions=(
        "Werkzeuge für deutsche E-Rechnungen (XRechnung, ZUGFeRD, Factur-X). "
        "erechnung_validieren nutzt die offiziellen KoSIT-Regeln. Maßgeblich ist immer das XML."
    ),
)


def _pfad(datei: str) -> Path:
    p = Path(datei).expanduser().resolve()
    if not p.is_file():
        raise ValueError(f"Datei nicht gefunden: {p}")
    return p


@server.tool()
def erechnung_lesen(datei: str) -> str:
    """Liest eine E-Rechnung (XRechnung UBL/CII oder ZUGFeRD-PDF) und gibt Format und Inhalt als JSON zurück."""
    p = _pfad(datei)
    fmt = erkennen(p)
    daten = lesen(p).als_dict()
    daten["_format"] = fmt.__dict__
    return json.dumps(daten, ensure_ascii=False, indent=2)


@server.tool()
def erechnung_validieren(datei: str, offiziell_pruefen: bool = True) -> str:
    """Prüft eine E-Rechnung mit den offiziellen KoSIT-Regeln (XRechnung 3.0.2, EN 16931) und einer Vorprüfung."""
    return json.dumps(validieren(_pfad(datei), offiziell_pruefen=offiziell_pruefen).als_dict(), ensure_ascii=False, indent=2)


@server.tool()
def erechnung_anzeigen(datei: str, ziel: str = "", kosit: bool = False) -> str:
    """Schreibt eine HTML-Ansicht der Rechnung neben die Datei (oder nach ziel) und gibt den Pfad zurück."""
    p = _pfad(datei)
    if kosit:
        from .lesen import xml_aus_eingabe

        inhalt = offiziell.html_ansicht(xml_aus_eingabe(p)[0])
    else:
        fmt = erkennen(p)
        inhalt = html(lesen(p), fmt.ist_e_rechnung, fmt.bezeichnung)
    ausgabe = Path(ziel).expanduser() if ziel else p.with_suffix(".html")
    ausgabe.write_text(inhalt, encoding="utf-8")
    return str(ausgabe)


@server.tool()
def erechnung_erstellen(rechnung_json: str, ziel: str, format: str = "xrechnung-ubl") -> str:
    """Erzeugt eine E-Rechnung aus JSON (Felder wie in den Beispielen) und prüft sie offiziell.

    format: xrechnung-ubl, xrechnung-cii, en16931-ubl, en16931-cii, zugferd, zugferd-xrechnung
    """
    from .cli import _erzeugen

    r = aus_dict(json.loads(rechnung_json))
    daten, _ = _erzeugen(r, format, None, False)
    ausgabe = Path(ziel).expanduser()
    ausgabe.write_bytes(daten)
    e = validieren(ausgabe)
    return json.dumps({"datei": str(ausgabe), "zahlbetrag": str(r.summen.zahlbetrag),
                       "validierung": e.als_dict()}, ensure_ascii=False, indent=2)


@server.tool()
def erechnung_datev(dateien: list[str], ziel: str, skr: str = "03", kreditor: int = 70000) -> str:
    """Exportiert Eingangsrechnungen als DATEV-Buchungsstapel (EXTF, cp1252) und gibt Hinweise zurück."""
    from . import datev

    rechnungen = [lesen(_pfad(d)) for d in dateien]
    daten, hinweise = datev.stapel(rechnungen, datev.Einstellungen(skr=skr, kreditor=kreditor))
    ausgabe = Path(ziel).expanduser()
    ausgabe.write_bytes(daten)
    return json.dumps({"datei": str(ausgabe), "buchungen": daten.count(b"\r\n") - 2, "hinweise": hinweise},
                      ensure_ascii=False, indent=2)


@server.tool()
def erechnung_leitweg_id(leitweg_id: str) -> str:
    """Prüft Format und Prüfziffer einer Leitweg-ID (Formatspezifikation 2.0.2)."""
    from .validieren import LEITWEG_MUSTER, leitweg_id_gueltig, leitweg_pruefziffer

    m = LEITWEG_MUSTER.fullmatch(leitweg_id.strip())
    richtig = None
    if m:
        richtig = "-".join(t for t in (m.group(1), m.group(2)) if t) + "-" + leitweg_pruefziffer(m.group(1), m.group(2) or "")
    return json.dumps({"leitweg_id": leitweg_id, "gueltig": leitweg_id_gueltig(leitweg_id), "richtig": richtig},
                      ensure_ascii=False)


def main() -> None:
    server.run()


if __name__ == "__main__":
    main()
