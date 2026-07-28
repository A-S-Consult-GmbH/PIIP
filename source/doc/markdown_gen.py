"""
Markdown generation for PIIP ontology documentation.

Produces:
- Per-ontology markdown files under doc/ontologies/_{Name}.md
- doc/_generated_ontologies.md  — lookup table
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from shared.piip_model import (
    Member,
    Ontology,
    OntologySet,
)

AUTO_GEN_NOTE = (
    "> **Note**: This file is auto-generated. Do not edit manually."
)

ONTOLOGIES_DOC_DIR = "ontologies"

_CONTAINER_RE = re.compile(r"^(Optional|Set|List|Link|Data)<(.+)>$")
_PREFIX_RE = re.compile(r"^(\w+):(.+)$")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ont_md_filename(ont: Ontology) -> str:
    """Relative path from doc/ to the ontology's markdown file."""
    return f"{ONTOLOGIES_DOC_DIR}/_{Path(ont.filename).stem}.md"


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _anchor_id(name: str) -> str:
    """Lowercase anchor id for a type name."""
    return name.lower()


# ---------------------------------------------------------------------------
# Type linking
# ---------------------------------------------------------------------------

def _strip_container(type_ref: str) -> str:
    """Strip Optional/Set/List/Link/Data wrappers to get the bare type."""
    cm = _CONTAINER_RE.match(type_ref)
    if cm:
        return _strip_container(cm.group(2))
    return type_ref


def _build_type_index(ont_set: OntologySet | None) -> dict[str, str]:
    """Build {type_name: ontology_name} for all types across all ontologies."""
    if not ont_set:
        return {}
    idx: dict[str, str] = {}
    for o in ont_set.ontologies:
        for name in o.type_names():
            idx[name] = o.name
    return idx


def _build_ont_lookup(
    ont: Ontology,
    ont_set: OntologySet | None,
) -> dict[str, str]:
    """Build {ontology_name: relative_md_path from ont's location} for cross-linking."""
    if not ont_set:
        return {}
    src_dir = Path("doc") / ONTOLOGIES_DOC_DIR
    result: dict[str, str] = {}
    for o in ont_set.ontologies:
        target = Path("doc") / ONTOLOGIES_DOC_DIR / f"_{Path(o.filename).stem}.md"
        result[o.name] = os.path.relpath(target, src_dir).replace("\\", "/")
    return result


def _link_ref(
    type_ref: str,
    ont: Ontology,
    ont_lookup: dict[str, str],
    type_index: dict[str, str],
) -> str:
    """Link a type reference to its definition. Returns markdown or plain code."""
    bare = _strip_container(type_ref)

    # Prefixed type (e.g. geo:Point3D)
    pm = _PREFIX_RE.match(bare)
    if pm:
        prefix, name = pm.group(1), pm.group(2)
        # Find target ontology by prefix
        target_ont_name = None
        for lo in ont.linked_ontologies:
            if lo.prefix == prefix:
                target_ont_name = lo.name
                break
        if target_ont_name and name in type_index:
            md_path = ont_lookup.get(target_ont_name, "")
            anchor = _anchor_id(name)
            link = f"{md_path}#{anchor}" if md_path else f"#{anchor}"
            return f"[`{type_ref}`]({link})"
        return f"`{type_ref}`"

    # Unqualified type
    if bare in type_index:
        target_ont_name = type_index[bare]
        md_path = ont_lookup.get(target_ont_name, "")
        if target_ont_name == ont.name:
            md_path = ""
        anchor = _anchor_id(bare)
        link = f"{md_path}#{anchor}" if md_path else f"#{anchor}"
        return f"[`{type_ref}`]({link})"

    return f"`{type_ref}`"


def _link_members_inline(
    members: list[Member],
    ont: Ontology,
    ont_lookup: dict[str, str],
    type_index: dict[str, str],
) -> str:
    """Render members with linked type refs."""
    parts = []
    for m in members:
        linked = _link_ref(m.type_ref, ont, ont_lookup, type_index)
        if m.name:
            parts.append(f"{linked} `{m.name}`")
        else:
            parts.append(linked)
    return ", ".join(parts)


def _link_ref_str(
    ref: str,
    ont: Ontology,
    ont_lookup: dict[str, str],
    type_index: dict[str, str],
    visible_bare: set[str],
) -> str:
    """Link a plain string reference (Includes, Components, InformationNeed)."""
    pm = _PREFIX_RE.match(ref)
    if pm:
        prefix, name = pm.group(1), pm.group(2)
        target_ont_name = None
        for lo in ont.linked_ontologies:
            if lo.prefix == prefix:
                target_ont_name = lo.name
                break
        if target_ont_name and name in type_index:
            md_path = ont_lookup.get(target_ont_name, "")
            anchor = _anchor_id(name)
            link = f"{md_path}#{anchor}" if md_path else f"#{anchor}"
            return f"[`{ref}`]({link})"
        return f"`{ref}`"
    if ref in type_index:
        target_ont_name = type_index[ref]
        md_path = ont_lookup.get(target_ont_name, "")
        if target_ont_name == ont.name:
            md_path = ""
        anchor = _anchor_id(ref)
        link = f"{md_path}#{anchor}" if md_path else f"#{anchor}"
        return f"[`{ref}`]({link})"
    return f"`{ref}`"


# ---------------------------------------------------------------------------
# Per-ontology markdown
# ---------------------------------------------------------------------------

def generate_ontology_markdown(
    ont: Ontology,
    ont_set: OntologySet | None = None,
) -> str:
    """Generate a full standalone markdown file for one ontology."""
    parts: list[str] = []
    ont_lookup = _build_ont_lookup(ont, ont_set)
    type_index = _build_type_index(ont_set)

    # Collect all visible bare type names for same-file refs
    visible_bare: set[str] = set()
    for src in [ont] + [o for o in (ont_set.ontologies if ont_set else []) if o.name in {lo.name for lo in ont.linked_ontologies}]:
        visible_bare.update(src.type_names())

    # --- Title ---
    parts.append(f"# {ont.name}")
    parts.append("")
    parts.append(AUTO_GEN_NOTE)
    parts.append("")

    # --- Source file reference (docs live in doc/ontologies/) ---
    src_rel = f"{ont.subfolder}/{ont.filename}" if ont.subfolder else ont.filename
    parts.append(f"**Source**: [`spec/{src_rel}`](../../spec/{src_rel})")
    parts.append("")

    # --- Doc ---
    if ont.doc:
        parts.append(md_escape(ont.doc))
        parts.append("")

    # --- Meta table ---
    parts.append("## Meta")
    parts.append("")
    parts.append("| Key | Value |")
    parts.append("|-----|-------|")
    parts.append(f"| URI | `{ont.meta.uri}` |")
    parts.append(f"| Organization | {md_escape(ont.meta.organization)} |")
    parts.append(f"| OrganizationUri | `{ont.meta.organization_uri}` |")
    parts.append(f"| Version | `{ont.meta.version}` |")
    if ont.meta.creators:
        parts.append(f"| Creators | {', '.join(ont.meta.creators)} |")
    parts.append("")

    # --- Linked Ontologies table ---
    if ont.linked_ontologies:
        parts.append("## Linked Ontologies")
        parts.append("")
        parts.append("| Ontology | URI | Prefix |")
        parts.append("|----------|-----|--------|")
        for lo in ont.linked_ontologies:
            target_md = ont_lookup.get(lo.name, "")
            if target_md:
                name_cell = f"[{lo.name}]({target_md})"
            else:
                name_cell = f"`{lo.name}`"
            parts.append(f"| {name_cell} | `{lo.uri}` | `{lo.prefix or '—'}` |")
        parts.append("")

    # --- BaseTypes ---
    if ont.base_types:
        parts.append("## BaseTypes")
        parts.append("")
        bt_names = [
            f"<a id=\"{_anchor_id(bt.name)}\"></a>`{bt.name}`"
            for bt in ont.base_types
        ]
        parts.append(", ".join(bt_names))
        parts.append("")

    # --- Enums ---
    if ont.enums:
        parts.append("## Enums")
        parts.append("")
        for enum in ont.enums:
            val_strs = [f"`{v}`" for v in enum.values]
            parts.append(f"<a id=\"{_anchor_id(enum.name)}\"></a>**`{enum.name}`**")
            if enum.doc:
                parts.append(f": {md_escape(enum.doc)}")
            parts.append(f"  Values: {', '.join(val_strs)}")
            parts.append("")

    # --- ValueTypes ---
    if ont.value_types:
        parts.append("## ValueTypes")
        parts.append("")
        for vt in ont.value_types:
            header = f"<a id=\"{_anchor_id(vt.name)}\"></a>**`{vt.name}`**"
            if vt.extends:
                header += f" extends {_link_ref(vt.extends, ont, ont_lookup, type_index)}"
            parts.append(header)
            if vt.doc:
                parts.append(f": {md_escape(vt.doc)}")
            if vt.members:
                parts.append(f"  Members: {_link_members_inline(vt.members, ont, ont_lookup, type_index)}")
            parts.append("")

    # --- Components ---
    if ont.components:
        parts.append("## Components")
        parts.append("")
        parts.append("| Component | Purpose |")
        parts.append("|-----------|---------|")
        for comp in ont.components:
            doc = md_escape(comp.doc)
            anchor = f"<a id=\"{_anchor_id(comp.name)}\"></a>"
            parts.append(f"| {anchor}`{comp.name}` | {doc} |")
        parts.append("")

    # --- Archetypes ---
    if ont.archetypes:
        parts.append("## Archetypes")
        parts.append("")
        parts.append("| Archetype | Includes | Own Components |")
        parts.append("|-----------|----------|----------------|")
        for arch in ont.archetypes:
            inc_parts = [_link_ref_str(i, ont, ont_lookup, type_index, visible_bare) for i in arch.includes]
            inc_str = ", ".join(inc_parts) or "—"
            comp_parts = [_link_ref_str(c, ont, ont_lookup, type_index, visible_bare) for c in arch.components]
            comp_str = ", ".join(comp_parts) or "_(none)_"
            anchor = f"<a id=\"{_anchor_id(arch.name)}\"></a>"
            parts.append(f"| {anchor}`{arch.name}` | {inc_str} | {comp_str} |")
        parts.append("")

    # --- InformationNeed ---
    if ont.information_needs:
        parts.append("## InformationNeed")
        parts.append("")
        parts.append("| Archetype | Rule | Components |")
        parts.append("|-----------|------|------------|")
        for need in ont.information_needs:
            arch_ref = _link_ref_str(need.archetype_ref, ont, ont_lookup, type_index, visible_bare)
            for rule_name, ref_list in [("OneOf", need.one_of), ("AnyOf", need.any_of), ("MustHave", need.must_have)]:
                if ref_list:
                    refs = ", ".join(
                        _link_ref_str(r, ont, ont_lookup, type_index, visible_bare)
                        for r in ref_list
                    )
                    parts.append(f"| {arch_ref} | {rule_name} | {refs} |")
        parts.append("")

    # --- Systems ---
    if ont.systems:
        parts.append("## Systems")
        parts.append("")
        for sys in ont.systems:
            parts.append(f"### <a id=\"{_anchor_id(sys.name)}\"></a>`{sys.name}`")
            parts.append("")
            if sys.doc:
                parts.append(md_escape(sys.doc))
                parts.append("")
            for op in sys.operations:
                parts.append(f"#### `{op.name}`")
                parts.append("")
                if op.doc:
                    parts.append(md_escape(op.doc))
                    parts.append("")
                if op.inputs:
                    parts.append("**Input:**")
                    parts.append("")
                    parts.append("| Type | Name | Description |")
                    parts.append("|------|------|-------------|")
                    for m in op.inputs:
                        linked = _link_ref(m.type_ref, ont, ont_lookup, type_index)
                        parts.append(f"| {linked} | `{m.name}` | {md_escape(m.doc)} |")
                    parts.append("")
                else:
                    parts.append("**Input:** _(none)_")
                    parts.append("")
                if op.outputs:
                    parts.append("**Output:**")
                    parts.append("")
                    parts.append("| Type | Name |")
                    parts.append("|------|------|")
                    for m in op.outputs:
                        linked = _link_ref(m.type_ref, ont, ont_lookup, type_index)
                        parts.append(f"| {linked} | `{m.name}` |")
                    parts.append("")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Ontologies lookup table
# ---------------------------------------------------------------------------

def generate_ontologies_lookup(ont_set: OntologySet) -> str:
    """Generate generated_ontologies.md with a table linking to all ontology docs."""
    parts: list[str] = []

    parts.append("# Generated Ontology Documentation")
    parts.append("")
    parts.append(AUTO_GEN_NOTE)
    parts.append("")

    parts.append("| Ontology | Description |")
    parts.append("|----------|-------------|")
    for ont in ont_set.ontologies:
        md_file = _ont_md_filename(ont)
        doc = md_escape(ont.doc) if ont.doc else "—"
        parts.append(f"| [{ont.name}]({md_file}) | {doc} |")
    parts.append("")

    return "\n".join(parts)
