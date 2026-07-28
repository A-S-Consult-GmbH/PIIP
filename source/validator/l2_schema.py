"""L2 — JSON Schema structural validation via jsonschema (in-process)."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml

_VALIDATOR_DIR = Path(__file__).resolve().parent
ONTOLOGY_SCHEMA_PATH = _VALIDATOR_DIR / "piip_schema.json"

_ontology_schema: dict | None = None

def get_ontology_schema() -> dict:
    global _ontology_schema
    if _ontology_schema is None:
        with open(ONTOLOGY_SCHEMA_PATH, encoding="utf-8") as f:
            _ontology_schema = json.load(f)
    return _ontology_schema # type: ignore

def run_json_schema(files: list[Path], schema: dict) -> int:
    """Validate each file against a JSON Schema. Returns number of files with errors."""
    validator = jsonschema.Draft202012Validator(schema)
    errors = 0
    for f in files:
        with open(f, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        file_errors = list(validator.iter_errors(data))
        if file_errors:
            for err in file_errors:
                path = ".".join(str(p) for p in err.absolute_path) or "(root)"
                print(f"  {f.name}::{path}: {err.message}")
            errors += 1
        else:
            print(f"  ok: {f.name}")
    return errors
