"""L3 — Semantic cross-file validation of piip ontologies."""
from __future__ import annotations

import re
from typing import Any

from shared.piip_model import Ontology, OntologySet

_CONTAINER_RE = re.compile(r"^(Optional|Set|List|Link|Data)<(.+)>$")
_CARDINALITY_RE = re.compile(r"^(Optional|Set|List)<(.+)>$")
_DATA_LINK_RE = re.compile(r"^(Data|Link)<(.+)>$")
_PREFIX_RE = re.compile(r"^(\w+):(.+)$")


# ---------------------------------------------------------------------------
# Visibility helpers
# ---------------------------------------------------------------------------

def _linked_sources(ont: Ontology, ont_set: OntologySet) -> list[Ontology]:
    """Return [ont] + all directly linked ontologies."""
    sources: list[Ontology] = [ont]
    for lo in ont.linked_ontologies:
        linked = ont_set.by_name(lo.name)
        if linked is not None:
            sources.append(linked)
    return sources


def _visible_member_types(ont: Ontology, ont_set: OntologySet) -> set[str]:
    """Types valid in Member.type_ref: BaseType | Enum | ValueType | Archetype | System."""
    types: set[str] = set()
    for src in _linked_sources(ont, ont_set):
        types.update(bt.name for bt in src.base_types)
        types.update(e.name for e in src.enums)
        types.update(vt.name for vt in src.value_types)
        types.update(a.name for a in src.archetypes)
        types.update(s.name for s in src.systems)
    return types


def _visible_archetypes(ont: Ontology, ont_set: OntologySet) -> set[str]:
    names: set[str] = set()
    for src in _linked_sources(ont, ont_set):
        names.update(a.name for a in src.archetypes)
    return names


def _visible_components(ont: Ontology, ont_set: OntologySet) -> set[str]:
    names: set[str] = set()
    for src in _linked_sources(ont, ont_set):
        names.update(c.name for c in src.components)
    return names


def _visible_value_types(ont: Ontology, ont_set: OntologySet) -> set[str]:
    names: set[str] = set()
    for src in _linked_sources(ont, ont_set):
        names.update(vt.name for vt in src.value_types)
    return names


def _visible_systems(ont: Ontology, ont_set: OntologySet) -> set[str]:
    """System names visible to this ontology (own + linked)."""
    names: set[str] = set()
    for src in _linked_sources(ont, ont_set):
        names.update(s.name for s in src.systems)
    return names


def _build_prefix_map(ont: Ontology, ont_set: OntologySet) -> dict[str, str]:
    """Build {bare_type_name: required_prefix} for types from prefixed ontologies.

    Types defined in the ontology itself or in Core (no prefix) are excluded.
    """
    pmap: dict[str, str] = {}
    for lo in ont.linked_ontologies:
        if not lo.prefix:
            continue
        target = ont_set.by_name(lo.name)
        if target is None:
            continue
        for name in target.type_names():
            pmap[name] = lo.prefix
    return pmap


def _strip_container(type_ref: str) -> str:
    """Strip Optional/Set/List/Link/Data wrappers to get the bare type."""
    cm = _CONTAINER_RE.match(type_ref)
    if cm:
        return _strip_container(cm.group(2))
    return type_ref


def _strip_cardinality(type_ref: str) -> str:
    """Strip Optional/Set/List wrappers only; leave Link<> and Data<> intact."""
    cm = _CARDINALITY_RE.match(type_ref)
    if cm:
        return _strip_cardinality(cm.group(2))
    return type_ref


def _resolve_prefixed_ref(
    ref: str,
    ont: Ontology,
    ont_set: OntologySet,
    visible_bare: set[str],
) -> str | None:
    """Resolve a possibly prefixed reference (Includes/Components/Extends).

    Returns error string or None.
    """
    pm = _PREFIX_RE.match(ref)
    if pm:
        prefix, bare = pm.group(1), pm.group(2)
        for lo in ont.linked_ontologies:
            if lo.prefix == prefix:
                target = ont_set.by_name(lo.name)
                if target is None:
                    return f"linked ontology '{lo.name}' not loaded"
                if bare in target.type_names():
                    return None
                return f"'{bare}' not found in '{lo.name}' (prefix '{prefix}')"
        return f"unknown prefix '{prefix}'"
    if ref in visible_bare:
        return None
    return f"'{ref}' not found in any visible ontology"


def _check_prefix_usage(
    type_ref: str,
    prefix_map: dict[str, str],
) -> str | None:
    """Check that types from prefixed ontologies use their prefix.

    Returns error string or None.
    """
    bare = _strip_container(type_ref)

    # Already prefixed — ok (correctness checked elsewhere)
    if _PREFIX_RE.match(bare):
        return None

    # Is this type from a prefixed ontology?
    required = prefix_map.get(bare)
    if required:
        return f"'{bare}' must be qualified as '{required}:{bare}'"
    return None


def _is_visible_archetype(
    type_ref: str,
    ont: Ontology,
    ont_set: OntologySet,
) -> bool:
    """True if type_ref names an Archetype visible from ont (prefixed or bare)."""
    pm = _PREFIX_RE.match(type_ref)
    if pm:
        prefix, bare = pm.group(1), pm.group(2)
        if prefix == "xsd":
            return False
        if prefix == "Core":
            core_ont = ont_set.by_name("Core")
            if core_ont is None:
                return False
            return bare in {a.name for a in core_ont.archetypes}
        for lo in ont.linked_ontologies:
            if lo.prefix == prefix:
                target = ont_set.by_name(lo.name)
                if target is None:
                    return False
                return bare in {a.name for a in target.archetypes}
        return False
    return type_ref in _visible_archetypes(ont, ont_set)


def _check_data_link_archetype(
    type_ref: str,
    ont: Ontology,
    ont_set: OntologySet,
) -> str | None:
    """Check that Data<T> and Link<T> wrap an Archetype. Returns error string or None."""
    dm = _DATA_LINK_RE.match(type_ref)
    if not dm:
        return None
    wrapper, inner = dm.group(1), dm.group(2)
    if _is_visible_archetype(inner, ont, ont_set):
        return None
    pm = _PREFIX_RE.match(inner)
    if pm:
        prefix, bare = pm.group(1), pm.group(2)
        if prefix == "xsd":
            return f"{wrapper}<{inner}>: '{inner}' is not an Archetype"
        if prefix == "Core":
            return f"{wrapper}<{inner}>: '{bare}' is not an Archetype in 'Core'"
        for lo in ont.linked_ontologies:
            if lo.prefix == prefix:
                target = ont_set.by_name(lo.name)
                if target is None:
                    return None  # already reported elsewhere
                return f"{wrapper}<{inner}>: '{bare}' is not an Archetype in '{lo.name}'"
        return None  # unknown prefix, already reported
    vis = _visible_archetypes(ont, ont_set)
    if inner not in vis:
        return f"{wrapper}<{inner}>: '{inner}' is not an Archetype"
    return None


def _check_archetype_wrapping(
    type_ref: str,
    ont: Ontology,
    ont_set: OntologySet,
) -> str | None:
    """Archetype member types must be wrapped in Link<> or Data<>.

    Cardinality wrappers (Optional/Set/List) are stripped first. Bare Archetype,
    Optional<Archetype>, Set<Archetype> are errors. Link<T> / Data<T> are checked
    by _check_data_link_archetype.
    """
    core = _strip_cardinality(type_ref)
    derr = _check_data_link_archetype(core, ont, ont_set)
    if derr:
        return derr
    if _DATA_LINK_RE.match(core):
        return None
    if _is_visible_archetype(core, ont, ont_set):
        return (
            f"Archetype '{core}' must be wrapped in Link<> or Data<> "
            f"(got '{type_ref}')"
        )
    return None


# ---------------------------------------------------------------------------
# Type resolution
# ---------------------------------------------------------------------------

def _resolve_member_type(
    type_ref: str,
    ont: Ontology,
    ont_set: OntologySet,
    visible: set[str],
) -> str | None:
    """Try to resolve a member type reference. Returns error string or None."""
    # Strip container wrapper
    cm = _CONTAINER_RE.match(type_ref)
    if cm:
        return _resolve_member_type(cm.group(2), ont, ont_set, visible)

    # Prefixed type  (e.g.  geo:AffineTransformation3D)
    pm = _PREFIX_RE.match(type_ref)
    if pm:
        prefix, bare = pm.group(1), pm.group(2)
        # Built-in namespaces
        if prefix in ("xsd", "Core"):
            return None
        for lo in ont.linked_ontologies:
            if lo.prefix == prefix:
                target = ont_set.by_name(lo.name)
                if target is None:
                    return f"linked ontology '{lo.name}' not loaded"
                target_types: set[str] = set()
                target_types.update(bt.name for bt in target.base_types)
                target_types.update(e.name for e in target.enums)
                target_types.update(vt.name for vt in target.value_types)
                target_types.update(a.name for a in target.archetypes)
                target_types.update(s.name for s in target.systems)
                if bare in target_types:
                    return None
                return f"'{bare}' not found in '{lo.name}' (prefix '{prefix}')"
        return f"unknown prefix '{prefix}'"

    # Unqualified type
    if type_ref in visible:
        return None
    return f"'{type_ref}' not found in any visible ontology"


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_semantic_checks(ont_set: OntologySet) -> list[str]:
    """Run all L3 semantic checks. Returns list of human-readable error strings."""
    errors: list[str] = []

    # --- Global duplicate name detection ---
    global_names: dict[str, list[str]] = {}
    for ont in ont_set.ontologies:
        for collection in (ont.enums, ont.value_types, ont.components, ont.archetypes, ont.systems):
            for item in collection:
                global_names.setdefault(item.name, []).append(ont.filename)

    for name, files in sorted(global_names.items()):
        if len(files) > 1:
            errors.append(f"duplicate name '{name}' defined in: {', '.join(files)}")

    # Track cross-file prefix consistency: {ontology_name: {prefix: [files...]}}
    prefix_usage: dict[str, dict[str, list[str]]] = {}

    for ont in ont_set.ontologies:
        tag = ont.filename

        # --- Naming conventions ---
        for comp in ont.components:
            if not comp.name.endswith("Component"):
                errors.append(f"{tag}: Component '{comp.name}' must end with 'Component'")
        for arch in ont.archetypes:
            if not arch.name.endswith("Archetype"):
                errors.append(f"{tag}: Archetype '{arch.name}' must end with 'Archetype'")

        # --- LinkedOntologies actually loaded + URI version match ---
        for lo in ont.linked_ontologies:
            target = ont_set.by_name(lo.name)
            if target is None:
                errors.append(f"{tag}: LinkedOntology '{lo.name}' not found")
            elif lo.uri and lo.uri != target.meta.uri:
                errors.append(
                    f"{tag}: LinkedOntology '{lo.name}' references URI "
                    f"'{lo.uri}' but actual URI is '{target.meta.uri}'"
                )

        # --- Prefix checks ---
        # Non-Core linked ontologies must declare a Prefix
        for lo in ont.linked_ontologies:
            if lo.name != "Core" and not lo.prefix:
                errors.append(
                    f"{tag}: LinkedOntology '{lo.name}' must declare a Prefix"
                )

        # Prefixes must be unique within an ontology
        seen_prefixes: dict[str, str] = {}
        for lo in ont.linked_ontologies:
            if lo.prefix:
                if lo.prefix in seen_prefixes:
                    errors.append(
                        f"{tag}: Prefix '{lo.prefix}' used by both "
                        f"'{seen_prefixes[lo.prefix]}' and '{lo.name}'"
                    )
                else:
                    seen_prefixes[lo.prefix] = lo.name

        # Same ontology should use the same prefix across all files
        _collect_prefix_consistency(ont, prefix_usage)

        # Build prefix enforcement map for this ontology
        prefix_map = _build_prefix_map(ont, ont_set)

        # Pre-compute visibility sets
        vis_archetypes = _visible_archetypes(ont, ont_set)
        vis_components = _visible_components(ont, ont_set)
        vis_value_types = _visible_value_types(ont, ont_set)
        vis_member_types = _visible_member_types(ont, ont_set)

        # --- Archetype.Includes → must be known Archetypes ---
        for arch in ont.archetypes:
            for inc in arch.includes:
                err = _resolve_prefixed_ref(inc, ont, ont_set, vis_archetypes)
                if err:
                    errors.append(
                        f"{tag}: Archetype '{arch.name}' Includes: {err}"
                    )

        # --- Archetype.Components → must be known Components ---
        for arch in ont.archetypes:
            for comp_ref in arch.components:
                err = _resolve_prefixed_ref(comp_ref, ont, ont_set, vis_components)
                if err:
                    errors.append(
                        f"{tag}: Archetype '{arch.name}' Components: {err}"
                    )

        # --- ValueType.Extends → must be known ValueType ---
        for vt in ont.value_types:
            if vt.extends:
                err = _resolve_prefixed_ref(vt.extends, ont, ont_set, vis_value_types)
                if err:
                    errors.append(
                        f"{tag}: ValueType '{vt.name}' Extends: {err}"
                    )

        # --- Member type references → must resolve ---
        all_members: list[tuple[str, Any]] = []
        for comp in ont.components:
            for m in comp.members:
                all_members.append((f"Component '{comp.name}'", m))
        for vt in ont.value_types:
            for m in vt.members:
                all_members.append((f"ValueType '{vt.name}'", m))

        for context, member in all_members:
            err = _resolve_member_type(member.type_ref, ont, ont_set, vis_member_types)
            if err:
                errors.append(
                    f"{tag}: {context}, Member '{member.name}': type {err}"
                )
            perr = _check_prefix_usage(member.type_ref, prefix_map)
            if perr:
                errors.append(
                    f"{tag}: {context}, Member '{member.name}': {perr}"
                )
            derr = _check_archetype_wrapping(member.type_ref, ont, ont_set)
            if derr:
                errors.append(
                    f"{tag}: {context}, Member '{member.name}': {derr}"
                )

        # --- System Operation I/O type references → must resolve ---
        vis_all_types = vis_member_types | vis_components | vis_archetypes
        for sys in ont.systems:
            for op in sys.operations:
                for m in op.inputs:
                    err = _resolve_member_type(m.type_ref, ont, ont_set, vis_all_types)
                    if err:
                        errors.append(
                            f"{tag}: System '{sys.name}' Operation '{op.name}' Input '{m.name}': type {err}"
                        )
                    derr = _check_archetype_wrapping(m.type_ref, ont, ont_set)
                    if derr:
                        errors.append(
                            f"{tag}: System '{sys.name}' Operation '{op.name}' Input '{m.name}': {derr}"
                        )
                for m in op.outputs:
                    err = _resolve_member_type(m.type_ref, ont, ont_set, vis_all_types)
                    if err:
                        errors.append(
                            f"{tag}: System '{sys.name}' Operation '{op.name}' Output '{m.name}': type {err}"
                        )
                    derr = _check_archetype_wrapping(m.type_ref, ont, ont_set)
                    if derr:
                        errors.append(
                            f"{tag}: System '{sys.name}' Operation '{op.name}' Output '{m.name}': {derr}"
                        )

        # --- InformationNeed references → archetype keys + component refs must resolve ---
        for need in ont.information_needs:
            err = _resolve_prefixed_ref(need.archetype_ref, ont, ont_set, vis_archetypes)
            if err:
                errors.append(f"{tag}: InformationNeed key: {err}")
            for ref_list_name, ref_list in [("OneOf", need.one_of), ("AnyOf", need.any_of), ("MustHave", need.must_have)]:
                for ref in ref_list:
                    err = _resolve_prefixed_ref(ref, ont, ont_set, vis_components)
                    if err:
                        errors.append(
                            f"{tag}: InformationNeed '{need.archetype_ref}' {ref_list_name}: {err}"
                        )

    # --- Cross-file prefix consistency ---
    for ont_name, prefixes in sorted(prefix_usage.items()):
        if len(prefixes) > 1:
            detail = "; ".join(
                f"'{p}' in {', '.join(fs)}" for p, fs in sorted(prefixes.items())
            )
            errors.append(
                f"inconsistent prefix for '{ont_name}': {detail}"
            )

    return errors


def _collect_prefix_consistency(
    ont: Ontology,
    usage: dict[str, dict[str, list[str]]],
) -> None:
    """Record which prefix each file uses for each linked ontology."""
    for lo in ont.linked_ontologies:
        if lo.prefix:
            usage.setdefault(lo.name, {}).setdefault(lo.prefix, []).append(ont.filename)
