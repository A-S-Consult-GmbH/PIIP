#!/usr/bin/env python3
"""
PIIP Ontology Validation Pipeline — L1 (yamllint) + L2 (JSON Schema) + L3 (semantic).

Usage:
    python validate.py                          # all levels, all files
    python validate.py path/to/geodesy.yaml     # specific file(s)
    python validate.py --level 1                # only yamllint
    python validate.py --level 2                # only JSON Schema
    python validate.py --level 3                # only semantic checks
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from shared.piip_model import OntologySet, SPEC_DIR
from validator.l1_yamllint import check_bom, run_yamllint
from validator.l2_schema import get_ontology_schema, run_json_schema
from validator.l3_semantic import run_semantic_checks


def find_ontology_files(targets: list[str] | None) -> list[Path]:
    """Return list of YAML ontology files to validate."""
    if targets:
        return [Path(t).resolve() for t in targets]
    return sorted(
        p for p in SPEC_DIR.glob("**/*.yaml")
    )

def main() -> int:
    parser = argparse.ArgumentParser(description="piip validation pipeline")
    parser.add_argument("files", nargs="*", help="Ontology YAML files (default: all)")
    parser.add_argument(
        "--level", type=int, choices=[1, 2, 3], default=0,
        help="Run only this level. Default: all.",
    )
    args = parser.parse_args()

    ontology_files = find_ontology_files(args.files or None)
    all_files = ontology_files
    
    if not all_files:
        print("No files found.")
        return 1    

    total_errors = 0
    run_l1 = args.level in (0, 1)
    run_l2 = args.level in (0, 2)
    run_l3 = args.level in (0, 3)

    # --- L1: YAML syntax + file-level checks ---
    if run_l1:
        print(f"=== L1: yamllint ({len(all_files)} files) ===")
        bom_errors = check_bom(all_files)
        l1 = run_yamllint(all_files) + bom_errors
        if l1:
            print(f"  L1 FAILED: {l1} file(s) with YAML lint / BOM errors\n")
        else:
            print(f"  L1 passed: all {len(all_files)} files OK\n")
        total_errors += l1

    # --- L2: JSON Schema ---
    if run_l2:
        print(f"=== L2: JSON Schema ({len(all_files)} files) ===")
        l2 = run_json_schema(ontology_files, get_ontology_schema())
        if l2:
            print(f"  L2 FAILED: {l2} file(s) with schema errors\n")
        else:
            print(f"  L2 passed: all {len(all_files)} files OK\n")
        total_errors += l2

    # --- L3: Semantic cross-file checks ---
    if run_l3:
        print("=== L3: Semantic checks ===")
        ont_set = OntologySet.load()
        errors = run_semantic_checks(ont_set)
        for e in errors:
            print(f"  {e}")
        if errors:
            print(f"  L3 FAILED: {len(errors)} semantic error(s)\n")
        else:
            print(f"  L3 passed: all ontologies OK\n")
        total_errors += len(errors)

    # --- Summary ---
    if total_errors:
        print(f"VALIDATION FAILED: {total_errors} error(s)")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
