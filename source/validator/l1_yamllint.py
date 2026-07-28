"""L1 — YAML syntax validation via yamllint + file-level byte checks."""
from __future__ import annotations

import subprocess
from pathlib import Path

_VALIDATOR_DIR = Path(__file__).resolve().parent
YAMLLINT_CFG = _VALIDATOR_DIR / ".yamllint.yml"

# UTF-8 BOM (EF BB BF)
_BOM = b"\xef\xbb\xbf"


def check_bom(files: list[Path]) -> int:
    """Check that every file starts with a UTF-8 BOM. Returns number of files missing BOM."""
    errors = 0
    for f in files:
        with open(f, "rb") as fh:
            head = fh.read(3)
        if head != _BOM:
            print(f"  {f.name}: missing UTF-8 BOM")
            errors += 1
    return errors


def run_yamllint(files: list[Path]) -> int:
    """Run yamllint on given files. Returns number of files with errors."""
    errors = 0
    for f in files:
        cmd = ["yamllint", "-c", str(YAMLLINT_CFG), str(f)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stdout, end="")
            print(result.stderr, end="")
            errors += 1
    return errors
