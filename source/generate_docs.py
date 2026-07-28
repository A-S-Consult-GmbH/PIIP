#!/usr/bin/env python3
"""
Generate Markdown documentation from PIIP ontology YAML files.

Produces:
- doc/_generated_ontologies.md       — lookup table linking to all ontology docs
- doc/ontologies/_{Name}.md          — one file per ontology

Usage:
    python generate_docs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from shared.piip_model import OntologySet, SPEC_DIR, ROOT_DIR
from doc.markdown_gen import (
    ONTOLOGIES_DOC_DIR,
    generate_ontology_markdown,
    generate_ontologies_lookup,
)


DOC_DIR = ROOT_DIR / "doc"


def main() -> None:
    ont_set = OntologySet.load(SPEC_DIR)
    if not ont_set.ontologies:
        print(f"No ontology YAML files found in {SPEC_DIR}", file=sys.stderr)
        sys.exit(1)

    # 1. Per-ontology files (doc/ontologies/_{Name}.md)
    ont_dir = DOC_DIR / ONTOLOGIES_DOC_DIR
    ont_dir.mkdir(parents=True, exist_ok=True)
    for ont in ont_set.ontologies:
        ont_md = generate_ontology_markdown(ont, ont_set)
        ont_path = ont_dir / f"_{Path(ont.filename).stem}.md"
        ont_path.write_text(ont_md, encoding="utf-8")
        print(f"  Generated {ont_path.relative_to(ROOT_DIR)}")
    print(f"Generated {len(ont_set.ontologies)} ontology file(s)")

    # 2. Lookup table doc/_generated_ontologies.md
    lookup_md = generate_ontologies_lookup(ont_set)
    lookup_path = DOC_DIR / "_generated_ontologies.md"
    lookup_path.write_text(lookup_md, encoding="utf-8")
    print(f"Generated {lookup_path.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
