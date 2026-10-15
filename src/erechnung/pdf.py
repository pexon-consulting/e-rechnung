"""ZUGFeRD und Factur-X: XML aus einem PDF lesen und XML in ein PDF einbetten.

Eine ZUGFeRD-Rechnung ist ein PDF/A-3 mit eingebettetem CII-XML. Für die
Einbettung braucht es vier Dinge:

1. das XML als eingebettete Datei (``factur-x.xml``, Profil XRECHNUNG: ``xrechnung.xml``)
2. ``/AFRelationship`` an der Datei (``/Alternative``, bei MINIMUM und BASIC WL ``/Data``)
3. einen Eintrag im ``/AF``-Array des Dokumentkatalogs
4. XMP-Metadaten mit PDF/A-Kennung und dem Factur-X-Schema

Ob das Ergebnis ein gültiges PDF/A-3 ist, hängt am Ausgangs-PDF (Schriften
eingebettet, Farbprofil). Mit ``pdfa=True`` wandelt Ghostscript das
Ausgangs-PDF vorher nach PDF/A-3b um.
"""

from __future__ import annotations

import io
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from lxml import etree
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject, NumberObject, TextStringObject

from .codelisten import ZUGFERD_PROFILE

BEKANNTE_NAMEN = ("factur-x.xml", "xrechnung.xml", "zugferd-invoice.xml", "ZUGFeRD-invoice.xml", "order-x.xml")

# Profil -> (ConformanceLevel im XMP, AFRelationship)
PROFIL_XMP = {
    "MINIMUM": ("MINIMUM", "/Data"),
    "BASIC WL": ("BASIC WL", "/Data"),
    "BASIC": ("BASIC", "/Alternative"),
    "EN 16931 (COMFORT)": ("EN 16931", "/Alternative"),
    "EXTENDED": ("EXTENDED", "/Alternative"),
    "XRECHNUNG": ("XRECHNUNG", "/Alternative"),
}


class KeinXmlImPdf(ValueError):
    pass


def xml_auslesen(pdf: bytes | str | Path) -> tuple[str, bytes]:
    """Name und Inhalt des eingebetteten Rechnungs-XML."""
    daten = Path(pdf).read_bytes() if isinstance(pdf, (str, Path)) else pdf
    leser = PdfReader(io.BytesIO(daten))
    anhaenge = leser.attachments
    for name in BEKANNTE_NAMEN:
        for vorhanden, inhalte in anhaenge.items():
            if vorhanden.lower() == name.lower() and inhalte:
                return vorhanden, inhalte[0]
    for vorhanden, inhalte in anhaenge.items():
        if vorhanden.lower().endswith(".xml") and inhalte:
            kopf = inhalte[0][:2000]
            if b"CrossIndustryInvoice" in kopf or b"Invoice" in kopf:
                return vorhanden, inhalte[0]
    raise KeinXmlImPdf(
        "Das PDF enthält kein eingebettetes Rechnungs-XML. Ein reines PDF ist nach § 14 UStG "
        "eine sonstige Rechnung, keine E-Rechnung."
    )


def _profil(xml: bytes) -> str:
    wurzel = etree.fromstring(xml, etree.XMLParser(resolve_entities=False, no_network=True))
    gid = (wurzel.findtext(".//{*}GuidelineSpecifiedDocumentContextParameter/{*}ID") or "").strip()
    profil = ZUGFERD_PROFILE.get(gid)
    if not profil:
        raise ValueError(f"Unbekannte Guideline-ID für ZUGFeRD: {gid!r}. Erwartet wird CII mit einem ZUGFeRD-Profil.")
    return profil


def _xmp(dateiname: str, stufe: str, titel: str, jetzt: str) -> bytes:
    return f"""<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="" xmlns:pdfaid="http://www.aiim.org/pdfa/ns/id/">
   <pdfaid:part>3</pdfaid:part>
   <pdfaid:conformance>B</pdfaid:conformance>
  </rdf:Description>
  <rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/">
   <dc:title><rdf:Alt><rdf:li xml:lang="x-default">{titel}</rdf:li></rdf:Alt></dc:title>
   <dc:format>application/pdf</dc:format>
  </rdf:Description>
  <rdf:Description rdf:about="" xmlns:xmp="http://ns.adobe.com/xap/1.0/">
   <xmp:CreateDate>{jetzt}</xmp:CreateDate>
   <xmp:ModifyDate>{jetzt}</xmp:ModifyDate>
   <xmp:MetadataDate>{jetzt}</xmp:MetadataDate>
   <xmp:CreatorTool>e-rechnung (Python)</xmp:CreatorTool>
  </rdf:Description>
  <rdf:Description rdf:about="" xmlns:pdf="http://ns.adobe.com/pdf/1.3/">
   <pdf:Producer>e-rechnung (Python) mit pypdf</pdf:Producer>
  </rdf:Description>
  <rdf:Description rdf:about="" xmlns:fx="urn:factur-x:pdfa:CrossIndustryDocument:invoice:1p0#">
   <fx:DocumentType>INVOICE</fx:DocumentType>
   <fx:DocumentFileName>{dateiname}</fx:DocumentFileName>
   <fx:Version>1.0</fx:Version>
   <fx:ConformanceLevel>{stufe}</fx:ConformanceLevel>
  </rdf:Description>
  <rdf:Description rdf:about="" xmlns:pdfaExtension="http://www.aiim.org/pdfa/ns/extension/"
    xmlns:pdfaSchema="http://www.aiim.org/pdfa/ns/schema#" xmlns:pdfaProperty="http://www.aiim.org/pdfa/ns/property#">
   <pdfaExtension:schemas>
    <rdf:Bag>
     <rdf:li rdf:parseType="Resource">
      <pdfaSchema:schema>Factur-X PDFA Extension Schema</pdfaSchema:schema>
      <pdfaSchema:namespaceURI>urn:factur-x:pdfa:CrossIndustryDocument:invoice:1p0#</pdfaSchema:namespaceURI>
      <pdfaSchema:prefix>fx</pdfaSchema:prefix>
      <pdfaSchema:property>
       <rdf:Seq>
        <rdf:li rdf:parseType="Resource">
         <pdfaProperty:name>DocumentFileName</pdfaProperty:name>
         <pdfaProperty:valueType>Text</pdfaProperty:valueType>
         <pdfaProperty:category>external</pdfaProperty:category>
         <pdfaProperty:description>The name of the embedded XML document</pdfaProperty:description>
        </rdf:li>
        <rdf:li rdf:parseType="Resource">
         <pdfaProperty:name>DocumentType</pdfaProperty:name>
         <pdfaProperty:valueType>Text</pdfaProperty:valueType>
         <pdfaProperty:category>external</pdfaProperty:category>
         <pdfaProperty:description>The type of the hybrid document in capital letters, e.g. INVOICE or ORDER</pdfaProperty:description>
        </rdf:li>
        <rdf:li rdf:parseType="Resource">
         <pdfaProperty:name>Version</pdfaProperty:name>
         <pdfaProperty:valueType>Text</pdfaProperty:valueType>
         <pdfaProperty:category>external</pdfaProperty:category>
         <pdfaProperty:description>The actual version of the standard applying to the embedded XML document</pdfaProperty:description>
        </rdf:li>
        <rdf:li rdf:parseType="Resource">
         <pdfaProperty:name>ConformanceLevel</pdfaProperty:name>
         <pdfaProperty:valueType>Text</pdfaProperty:valueType>
         <pdfaProperty:category>external</pdfaProperty:category>
         <pdfaProperty:description>The conformance level of the embedded XML document</pdfaProperty:description>
        </rdf:li>
       </rdf:Seq>
      </pdfaSchema:property>
     </rdf:li>
    </rdf:Bag>
   </pdfaExtension:schemas>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>""".encode("utf-8")


def _icc_profil() -> Path:
    """sRGB-Profil für den PDF/A-OutputIntent. Ghostscript bringt eines mit."""
    eigen = os.environ.get("ERECHNUNG_ICC")
    if eigen:
        return Path(eigen)
    gs = shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")
    kandidaten: list[Path] = []
    if gs:
        basis = Path(gs).resolve().parent.parent
        kandidaten += list(basis.glob("share/ghostscript/iccprofiles/srgb.icc"))
        kandidaten += list(basis.glob("share/ghostscript/*/iccprofiles/srgb.icc"))
        kandidaten += list(basis.glob("iccprofiles/srgb.icc"))
    kandidaten += [Path("/usr/share/color/icc/ghostscript/srgb.icc"), Path("/usr/share/ghostscript/iccprofiles/srgb.icc")]
    kandidaten += list(Path("/usr/share/ghostscript").glob("*/iccprofiles/srgb.icc"))
    for k in kandidaten:
        if k.is_file():
            return k
    raise RuntimeError("Kein sRGB-ICC-Profil gefunden. ERECHNUNG_ICC auf eine .icc-Datei setzen.")


def ghostscript_pdfa3(eingabe: Path) -> bytes:
    """PDF oder PostScript mit Ghostscript nach PDF/A-3b (Schriften eingebettet, sRGB-OutputIntent)."""
    gs = shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")
    if not gs:
        raise RuntimeError("Ghostscript (gs) nicht gefunden. Installieren oder ein PDF/A-3 als Vorlage verwenden.")
    icc = _icc_profil()
    with tempfile.TemporaryDirectory() as tmp:
        definition = Path(tmp) / "pdfa_def.ps"
        aus = Path(tmp) / "aus.pdf"
        icc_ps = str(icc).replace("\\", "/").replace("(", "\\(").replace(")", "\\)")
        definition.write_text(
            "%!\n"
            "[/_objdef {icc_PDFA} /type /stream /OBJ pdfmark\n"
            "[{icc_PDFA} << /N 3 >> /PUT pdfmark\n"
            f"[{{icc_PDFA}} ({icc_ps}) (r) file /PUT pdfmark\n"
            "[/_objdef {OutputIntent_PDFA} /type /dict /OBJ pdfmark\n"
            "[{OutputIntent_PDFA} << /Type /OutputIntent /S /GTS_PDFA1 /DestOutputProfile {icc_PDFA} "
            "/OutputConditionIdentifier (sRGB IEC61966-2.1) /Info (sRGB) >> /PUT pdfmark\n"
            "[{Catalog} << /OutputIntents [ {OutputIntent_PDFA} ] >> /PUT pdfmark\n",
            encoding="latin-1",
        )
        befehl = [gs, "-dPDFA=3", "-dBATCH", "-dNOPAUSE", "-dQUIET", "-dNOOUTERSAVE", "-dPDFACompatibilityPolicy=1",
                  "-sColorConversionStrategy=RGB", "-sProcessColorModel=DeviceRGB", "-sDEVICE=pdfwrite",
                  "-dEmbedAllFonts=true", f"--permit-file-read={icc}", f"-sOutputFile={aus}",
                  str(definition), str(eingabe)]
        lauf = subprocess.run(befehl, capture_output=True, text=True)
        if lauf.returncode != 0 or not aus.exists():
            raise RuntimeError(f"Ghostscript-Fehler: {(lauf.stderr or lauf.stdout).strip()[:500]}")
        return aus.read_bytes()


def nach_pdfa3(pdf: bytes) -> bytes:
    """Wandelt ein beliebiges PDF mit Ghostscript nach PDF/A-3b."""
    with tempfile.TemporaryDirectory() as tmp:
        ein = Path(tmp) / "ein.pdf"
        ein.write_bytes(pdf)
        return ghostscript_pdfa3(ein)


def einbetten(pdf: bytes, xml: bytes, dateiname: str | None = None, pdfa: bool = False) -> bytes:
    """Bettet CII-XML als ZUGFeRD/Factur-X in ein PDF ein und gibt das neue PDF zurück."""
    profil = _profil(xml)
    stufe, beziehung = PROFIL_XMP[profil]
    if dateiname is None:
        dateiname = "xrechnung.xml" if profil == "XRECHNUNG" else "factur-x.xml"
    if pdfa:
        pdf = nach_pdfa3(pdf)

    schreiber = PdfWriter(clone_from=PdfReader(io.BytesIO(pdf)))
    for name in list(schreiber.attachments):
        if name.lower() in {n.lower() for n in BEKANNTE_NAMEN}:
            raise ValueError(f"Das PDF enthält bereits {name}. Erst das Original-PDF ohne XML verwenden.")

    jetzt = datetime.now(timezone.utc).replace(microsecond=0)
    anhang = schreiber.add_attachment(dateiname, xml)
    anhang.subtype = NameObject("/text/xml")
    anhang.associated_file_relationship = NameObject(beziehung)
    anhang.modification_date = jetzt
    anhang.size = NumberObject(len(xml))
    spec = anhang.pdf_object
    spec[NameObject("/UF")] = TextStringObject(dateiname)
    spec[NameObject("/Desc")] = TextStringObject("Rechnungsdaten nach EN 16931 (ZUGFeRD/Factur-X)")

    katalog = schreiber.root_object
    af = katalog.get("/AF")
    if af is None:
        af = ArrayObject()
        katalog[NameObject("/AF")] = af
    af.append(spec.indirect_reference)

    titel = "Rechnung"
    try:
        wurzel = etree.fromstring(xml, etree.XMLParser(resolve_entities=False, no_network=True))
        nummer = wurzel.findtext(".//{*}ExchangedDocument/{*}ID")
        if nummer:
            titel = f"Rechnung {nummer}".replace("&", "&amp;").replace("<", "&lt;")
    except etree.XMLSyntaxError:
        pass
    schreiber.xmp_metadata = _xmp(dateiname, stufe, titel, jetzt.isoformat())
    if "/Title" not in (schreiber.metadata or {}):
        schreiber.add_metadata({"/Title": titel.replace("&amp;", "&").replace("&lt;", "<")})

    puffer = io.BytesIO()
    schreiber.write(puffer)
    return puffer.getvalue()
