"""ZUGFeRD-PDFs mit Mustang (Java) auf PDF/A-3 und gültiges XML prüfen.

    python scripts/mustang_check.py beispiele/*/zugferd_en16931.pdf [--java java]

Exit-Code 0, wenn Mustang alle Dateien als valid meldet.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _werkzeuge import MUSTANG_SHA256, MUSTANG_URL, datei  # noqa: E402


def main() -> int:
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("pdf", nargs="+")
    a.add_argument("--java", default="java")
    args = a.parse_args()
    jar = datei(MUSTANG_URL, MUSTANG_SHA256)
    fehler = 0
    for pdf in args.pdf:
        lauf = subprocess.run([args.java, "-jar", str(jar), "--no-notices", "--action", "validate", "--source", pdf],
                              capture_output=True, text=True)
        status = re.findall(r'<summary status="([a-z]+)"', lauf.stdout)
        ok = bool(status) and status[-1] == "valid"
        fehler += not ok
        print(f"{'valid  ' if ok else 'INVALID'} {pdf}")
        if not ok:
            print(lauf.stdout[-3000:])
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
