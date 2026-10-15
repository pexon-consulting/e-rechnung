"""Gepinnte Java-Werkzeuge für die Vergleichsprüfungen (nur Entwicklung und CI)."""
from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

from erechnung import offiziell

VALIDATOR_URL = "https://github.com/itplr-kosit/validator/releases/download/v1.6.3/validator-1.6.3-standalone.jar"
VALIDATOR_SHA256 = "799e64befca97d4080e03608c80b85dd5a5ecc5f4ae4f35d1116ec2855b9a7c9"
TESTSUITE_URL = ("https://github.com/itplr-kosit/xrechnung-testsuite/releases/download/v2026-08-31/"
                 "xrechnung-3.0.2-testsuite-2026-08-31.zip")
TESTSUITE_SHA256 = "1e81ef7563e0fa04c0e0b0631318a7e0843a3c0beb57d83ef95ac0c4a095e3d7"
MUSTANG_URL = "https://repo1.maven.org/maven2/org/mustangproject/Mustang-CLI/2.26.0/Mustang-CLI-2.26.0.jar"
MUSTANG_SHA256 = "42d7868cb68264874a7b8cab4c3587b03b23ccc7cd72373da917f66758bb9736"


def datei(url: str, sha256: str) -> Path:
    ziel = offiziell.cache_ordner() / url.rsplit("/", 1)[1]
    if ziel.exists() and hashlib.sha256(ziel.read_bytes()).hexdigest() == sha256:
        return ziel
    with urllib.request.urlopen(url, timeout=120) as antwort:
        daten = antwort.read()
    if hashlib.sha256(daten).hexdigest() != sha256:
        raise SystemExit(f"Prüfsumme stimmt nicht: {url}")
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_bytes(daten)
    return ziel


def testsuite() -> Path:
    return offiziell.bereitstellen(TESTSUITE_URL, TESTSUITE_SHA256, "xrechnung-3.0.2-testsuite-2026-08-31",
                                   "ERECHNUNG_KOSIT_TESTSUITE")
