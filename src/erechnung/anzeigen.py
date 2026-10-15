"""E-Rechnung als lesbares HTML, ohne Internet und ohne Java.

``html(rechnung)`` baut eine schlichte Ansicht aus dem Modell. Die offizielle
KoSIT-Visualisierung gibt es über :func:`erechnung.offiziell.html_ansicht`.
"""

from __future__ import annotations

from decimal import Decimal
from html import escape

from .codelisten import (
    ADRESS_SCHEMATA,
    EINHEITEN,
    RECHNUNGSARTEN,
    STEUERKATEGORIEN,
    ZAHLUNGSARTEN,
    text,
)
from .modell import Partei, Rechnung
from .rechnen import bedingungen_lesbar


def _geld(wert: Decimal | None, waehrung: str = "") -> str:
    if wert is None:
        return ""
    s = f"{Decimal(wert):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} {waehrung}".strip()


def _zahl(wert: Decimal | None) -> str:
    if wert is None:
        return ""
    return format(Decimal(wert).normalize(), "f").replace(".", ",")


def _datum(d) -> str:
    return d.strftime("%d.%m.%Y") if d else ""


def _partei(titel: str, p: Partei) -> str:
    a = p.adresse
    zeilen = [f"<strong>{escape(p.name)}</strong>"]
    if p.handelsname and p.handelsname != p.name:
        zeilen.append(escape(p.handelsname))
    for z in (a.strasse, a.zusatz, f"{a.plz} {a.ort}".strip(), a.land):
        if z:
            zeilen.append(escape(z))
    details = []
    for name, wert in (("USt-IdNr.", p.ust_id), ("Steuernummer", p.steuernummer), ("Register", p.register),
                       ("Kennung", p.kennung)):
        if wert:
            details.append(f"<dt>{name}</dt><dd>{escape(wert)}</dd>")
    if p.elektronische_adresse:
        schema = ADRESS_SCHEMATA.get(p.elektronische_adresse_schema, p.elektronische_adresse_schema)
        details.append(f"<dt>Elektronische Adresse</dt><dd>{escape(p.elektronische_adresse)} <small>({escape(schema)})</small></dd>")
    k = p.kontakt
    kontakt = ", ".join(escape(x) for x in (k.name, k.telefon, k.email) if x)
    if kontakt:
        details.append(f"<dt>Kontakt</dt><dd>{kontakt}</dd>")
    if p.rechtliches:
        details.append(f"<dt>Rechtliches</dt><dd>{escape(p.rechtliches)}</dd>")
    return (f'<section class="partei"><h2>{titel}</h2><p>{"<br>".join(zeilen)}</p>'
            f'<dl>{"".join(details)}</dl></section>')


STIL = """
body{font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1a1a;max-width:960px;margin:2rem auto;padding:0 1rem}
h1{font-size:1.5rem;margin:.2rem 0}h2{font-size:1rem;margin:1.2rem 0 .4rem;color:#444;text-transform:uppercase;letter-spacing:.04em}
.kopf{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;border-bottom:2px solid #1a1a1a;padding-bottom:.6rem}
.status{padding:.5rem .8rem;border-radius:6px;font-weight:600}.ja{background:#e6f4ea;color:#0f5132}.nein{background:#fdecea;color:#842029}
.parteien{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}@media(max-width:700px){.parteien{grid-template-columns:1fr}}
dl{display:grid;grid-template-columns:max-content 1fr;gap:.1rem .8rem;margin:0}dt{color:#555}dd{margin:0}
table{width:100%;border-collapse:collapse;margin:.4rem 0}th,td{padding:.35rem .5rem;border-bottom:1px solid #ddd;vertical-align:top}
th{text-align:left;background:#f4f4f4}td.z,th.z{text-align:right;white-space:nowrap}small{color:#666}
.summen{margin-left:auto;max-width:420px}.summen td{border:0}.gesamt td{font-weight:700;border-top:2px solid #1a1a1a}
.hinweis{font-size:.85rem;color:#555;margin-top:2rem}
"""


def html(r: Rechnung, ist_e_rechnung: bool | None = None, format_text: str = "") -> str:
    art = text(RECHNUNGSARTEN, r.art)
    status = ""
    if ist_e_rechnung is not None:
        klasse = "ja" if ist_e_rechnung else "nein"
        wort = "E-Rechnung nach EN 16931" if ist_e_rechnung else "Keine E-Rechnung im Sinne von § 14 UStG"
        status = f'<div class="status {klasse}">{escape(wort)}<br><small>{escape(format_text or r.quelle)}</small></div>'

    meta = [("Rechnungsart", art), ("Rechnungsdatum", _datum(r.datum)), ("Fällig", _datum(r.faellig)),
            ("Währung", r.waehrung), ("Käuferreferenz / Leitweg-ID", r.leitweg_id), ("Bestellnummer", r.bestellnummer),
            ("Vertrag", r.vertragsnummer), ("Projekt", r.projekt)]
    if r.vorgaenger_nummer:
        meta.append(("Bezug auf Rechnung", f"{r.vorgaenger_nummer} {_datum(r.vorgaenger_datum)}".strip()))
    if r.leistung_von or r.leistung_bis:
        meta.append(("Leistungszeitraum", f"{_datum(r.leistung_von)} - {_datum(r.leistung_bis)}"))
    if r.lieferung and r.lieferung.datum:
        meta.append(("Liefer-/Leistungsdatum", _datum(r.lieferung.datum)))
    meta_html = "".join(f"<dt>{escape(k)}</dt><dd>{escape(v)}</dd>" for k, v in meta if v)

    zeilen = []
    for p in r.positionen:
        satz = f"{_zahl(p.satz)} %" if p.satz is not None else ""
        beschreibung = f"<br><small>{escape(p.beschreibung)}</small>" if p.beschreibung else ""
        artikel = f"<br><small>Art.-Nr. {escape(p.artikelnummer)}</small>" if p.artikelnummer else ""
        zeitraum = f"<br><small>{_datum(p.zeitraum_von)} - {_datum(p.zeitraum_bis)}</small>" if p.zeitraum_von else ""
        nachlass = "".join(
            f"<br><small>{'Zuschlag' if n.zuschlag else 'Nachlass'} {escape(n.grund)}: {_geld(n.betrag)}</small>"
            for n in p.nachlaesse)
        zeilen.append(
            f"<tr><td>{escape(p.id)}</td><td>{escape(p.name)}{beschreibung}{artikel}{zeitraum}{nachlass}</td>"
            f'<td class="z">{_zahl(p.menge)}</td><td>{escape(EINHEITEN.get(p.einheit, p.einheit))}</td>'
            f'<td class="z">{_geld(p.preis)}</td><td>{escape(p.kategorie)} {satz}</td>'
            f'<td class="z">{_geld(p.nettobetrag)}</td></tr>')

    s = r.summen
    summen = [("Summe Positionen", s.positionen)]
    if s.nachlaesse:
        summen.append(("Nachlässe", -s.nachlaesse))
    if s.zuschlaege:
        summen.append(("Zuschläge", s.zuschlaege))
    summen += [("Nettobetrag", s.netto), ("Umsatzsteuer", s.steuer), ("Bruttobetrag", s.brutto)]
    if s.vorauszahlung:
        summen.append(("Bereits gezahlt", -s.vorauszahlung))
    summen_html = "".join(f"<tr><td>{k}</td><td class='z'>{_geld(v, r.waehrung)}</td></tr>" for k, v in summen)
    summen_html += f"<tr class='gesamt'><td>Zahlbetrag</td><td class='z'>{_geld(s.zahlbetrag, r.waehrung)}</td></tr>"

    nachlaesse = "".join(
        f"<tr><td>{'Zuschlag' if n.zuschlag else 'Nachlass'}</td><td>{escape(n.grund)}</td>"
        f"<td>{escape(n.kategorie)} {_zahl(n.satz)} %</td><td class='z'>{_geld(n.betrag, r.waehrung)}</td></tr>"
        for n in r.nachlaesse)
    nachlass_html = (f"<h2>Nachlässe und Zuschläge auf Belegebene</h2><table>{nachlaesse}</table>" if nachlaesse else "")

    steuern = "".join(
        f"<tr><td>{escape(text(STEUERKATEGORIEN, st.kategorie))}</td>"
        f"<td class='z'>{_zahl(st.satz) + ' %' if st.satz is not None else ''}</td>"
        f"<td class='z'>{_geld(st.basis, r.waehrung)}</td><td class='z'>{_geld(st.betrag, r.waehrung)}</td>"
        f"<td>{escape(st.befreiungsgrund)}</td></tr>"
        for st in r.steuern)

    z = r.zahlung
    zahlung = [("Zahlungsart", text(ZAHLUNGSARTEN, z.art)), ("IBAN", z.iban), ("BIC", z.bic), ("Kontoinhaber", z.kontoinhaber),
               ("Verwendungszweck", z.verwendungszweck), ("Mandatsreferenz", z.mandatsreferenz),
               ("Gläubiger-ID", z.glaeubiger_id), ("IBAN des Zahlers", z.zahler_iban),
               ("Zahlungsbedingungen", bedingungen_lesbar(z.bedingungen))]
    zahlung_html = "".join(f"<dt>{k}</dt><dd>{escape(v).replace(chr(10), '<br>')}</dd>" for k, v in zahlung if v)
    notizen = "".join(f"<p>{escape(n)}</p>" for n in r.notizen if n)

    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(art.split(' (')[0])} {escape(r.nummer)}</title><style>{STIL}</style></head>
<body>
<div class="kopf"><div><small>{escape(art)}</small><h1>{escape(r.nummer)}</h1></div>{status}</div>
<div class="parteien">{_partei("Verkäufer", r.verkaeufer)}{_partei("Käufer", r.kaeufer)}</div>
<h2>Rechnungsdaten</h2><dl>{meta_html}</dl>
{f"<h2>Hinweise</h2>{notizen}" if notizen else ""}
<h2>Positionen</h2>
<table><thead><tr><th>Pos.</th><th>Bezeichnung</th><th class="z">Menge</th><th>Einheit</th><th class="z">Preis</th><th>USt</th><th class="z">Netto</th></tr></thead>
<tbody>{"".join(zeilen)}</tbody></table>
{nachlass_html}
<table class="summen">{summen_html}</table>
<h2>Umsatzsteuer</h2>
<table><thead><tr><th>Kategorie</th><th class="z">Satz</th><th class="z">Basis</th><th class="z">Steuer</th><th>Befreiungsgrund</th></tr></thead><tbody>{steuern}</tbody></table>
<h2>Zahlung</h2><dl>{zahlung_html}</dl>
<p class="hinweis">Ansicht erzeugt mit e-rechnung (Python). Rechtlich maßgeblich ist der XML-Inhalt der E-Rechnung.</p>
</body></html>
"""
