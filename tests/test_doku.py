"""Befehle und Formate in README, Anleitungen und Skills müssen zur Kommandozeile passen."""

import re
from pathlib import Path

import pytest

from erechnung.cli import FORMATE, parser

WURZEL = Path(__file__).resolve().parents[1]
DATEIEN = sorted([WURZEL / "README.md", *WURZEL.glob("docs/**/*.md"), *WURZEL.glob("skills/*/SKILL.md")])
BEFEHLE = set(parser()._subparsers._group_actions[0].choices)  # noqa: SLF001


@pytest.mark.parametrize("datei", DATEIEN, ids=lambda p: str(p.relative_to(WURZEL)))
def test_formate_gibt_es(datei):
    falsch = [f for f in re.findall(r"--format[ =]([a-z0-9-]+)", datei.read_text(encoding="utf-8")) if f not in FORMATE]
    assert not falsch, f"unbekannte --format-Werte: {falsch}"


@pytest.mark.parametrize("datei", DATEIEN, ids=lambda p: str(p.relative_to(WURZEL)))
def test_unterbefehle_gibt_es(datei):
    text = datei.read_text(encoding="utf-8")
    befehle = re.findall(r"(?:^|[\s`$])erechnung ([a-zäöü][a-zäöü-]*)", text)
    falsch = sorted({b for b in befehle if b not in BEFEHLE and b != "import"})
    assert not falsch, f"unbekannte Unterbefehle: {falsch}"


def test_skills_enden_mit_hinweisanweisung():
    for skill in WURZEL.glob("skills/*/SKILL.md"):
        assert "keine Steuer- oder Rechtsberatung" in skill.read_text(encoding="utf-8"), skill
