import json
import shutil
from importlib import resources

import pytest

from erechnung.eingabe import aus_dict


def beispiel_namen() -> list[str]:
    return sorted(p.name[:-5] for p in resources.files("erechnung").joinpath("beispiele").iterdir() if p.name.endswith(".json"))


def beispiel(name: str):
    text = resources.files("erechnung").joinpath("beispiele", f"{name}.json").read_text(encoding="utf-8")
    return aus_dict(json.loads(text))


@pytest.fixture
def standard():
    return beispiel("01_standard")


def saxon_da() -> bool:
    try:
        import saxonche  # noqa: F401
    except ImportError:
        return False
    return True


braucht_saxon = pytest.mark.skipif(not saxon_da(), reason="saxonche nicht installiert")
braucht_gs = pytest.mark.skipif(shutil.which("gs") is None, reason="Ghostscript nicht installiert")
