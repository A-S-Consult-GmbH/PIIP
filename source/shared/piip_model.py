"""
Shared runtime representation of piip ECS ontologies.

Provides dataclasses for every ontology element (Meta, Enum, Member,
ValueType, Component, Archetype, Ontology) and an OntologySet container
that loads, parses, and topologically sorts all ontology YAML files.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Path constants (relative to *this* file: source/shared/piip_model.py)
# ---------------------------------------------------------------------------

_SHARED_DIR = Path(__file__).resolve().parent
_SOURCE_DIR = _SHARED_DIR.parent
ROOT_DIR = _SOURCE_DIR.parent
SPEC_DIR = ROOT_DIR / "spec"

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_SHORTHAND_RE = re.compile(r"^(?P<type>\S+)\s+(?P<name>\S+)$")


def _extract_item(raw: Any) -> tuple[str, dict]:
    """Extract (name, body_dict) from a YAML list entry."""
    if isinstance(raw, str):
        return raw, {}
    if isinstance(raw, dict):
        for key, val in raw.items():
            return str(key), (val if isinstance(val, dict) else {})
    return str(raw), {}


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Meta:
    uri: str
    organization: str
    organization_uri: str
    version: str
    creators: list[str] = field(default_factory=list)

    @classmethod
    def from_raw(cls, raw: dict) -> Meta:
        return cls(
            uri=raw.get("Uri", ""),
            organization=raw.get("Organization", ""),
            organization_uri=raw.get("OrganizationUri", ""),
            version=raw.get("Version", ""),
            creators=raw.get("Creators") or [],
        )


@dataclass
class LinkedOntology:
    name: str
    uri: str
    prefix: str = ""

    @classmethod
    def list_from_raw(cls, items: list | None) -> list[LinkedOntology]:
        result: list[LinkedOntology] = []
        for item in items or []:
            if not isinstance(item, dict):
                continue
            for name, body in item.items():
                body = body if isinstance(body, dict) else {}
                result.append(cls(
                    name=str(name),
                    uri=body.get("Uri", ""),
                    prefix=body.get("Prefix", ""),
                ))
        return result


@dataclass
class BaseType:
    name: str
    mapped_type: str = ""

    @classmethod
    def from_raw(cls, item: Any) -> BaseType:
        name, body = _extract_item(item)
        return cls(name=name, mapped_type=body.get("Type", "") if body else "")


@dataclass
class Enum:
    name: str
    doc: str = ""
    values: list[str] = field(default_factory=list)

    @classmethod
    def from_raw(cls, item: Any) -> Enum:
        name, body = _extract_item(item)
        return cls(name=name, doc=body.get("Doc", ""), values=body.get("Values", []))


@dataclass
class Member:
    name: str
    type_ref: str
    doc: str = ""

    @classmethod
    def from_raw(cls, raw: Any) -> Member:
        if isinstance(raw, str):
            m = _SHORTHAND_RE.match(raw.strip())
            if m:
                return cls(name=m.group("name"), type_ref=m.group("type"))
            return cls(name="", type_ref=raw.strip())
        if isinstance(raw, dict):
            if "Member" in raw:
                mem = raw["Member"]
                return cls(
                    name=mem.get("Name", ""),
                    type_ref=mem.get("Type", ""),
                    doc=mem.get("Doc", ""),
                )
            for key, val in raw.items():
                m = _SHORTHAND_RE.match(key.strip())
                if m:
                    return cls(name=m.group("name"), type_ref=m.group("type"))
                return cls(name=str(val) if val else "", type_ref=str(key))
        return cls(name="", type_ref=str(raw))

    @classmethod
    def list_from_raw(cls, items: list | None) -> list[Member]:
        return [cls.from_raw(m) for m in items] if items else []


@dataclass
class ValueType:
    name: str
    doc: str = ""
    extends: str = ""
    members: list[Member] = field(default_factory=list)

    @classmethod
    def from_raw(cls, item: Any) -> ValueType:
        name, body = _extract_item(item)
        return cls(
            name=name,
            doc=body.get("Doc", ""),
            extends=body.get("Extends", ""),
            members=Member.list_from_raw(body.get("Members")),
        )


@dataclass
class Component:
    name: str
    doc: str = ""
    members: list[Member] = field(default_factory=list)

    @classmethod
    def from_raw(cls, item: Any) -> Component:
        name, body = _extract_item(item)
        return cls(
            name=name,
            doc=body.get("Doc", ""),
            members=Member.list_from_raw(body.get("Members")),
        )


@dataclass
class Archetype:
    name: str
    doc: str = ""
    includes: list[str] = field(default_factory=list)
    components: list[str] = field(default_factory=list)

    @classmethod
    def from_raw(cls, item: Any) -> Archetype:
        name, body = _extract_item(item)
        return cls(
            name=name,
            doc=body.get("Doc", ""),
            includes=body.get("Includes") or [],
            components=body.get("Components") or [],
        )


@dataclass
class InformationNeedEntry:
    """One entry in the InformationNeed map (archetype → requirement)."""
    archetype_ref: str
    doc: str = ""
    one_of: list[str] = field(default_factory=list)
    any_of: list[str] = field(default_factory=list)
    must_have: list[str] = field(default_factory=list)

    @classmethod
    def from_raw(cls, ref: str, body: Any) -> InformationNeedEntry:
        body = body if isinstance(body, dict) else {}
        return cls(
            archetype_ref=ref,
            doc=body.get("Doc", ""),
            one_of=body.get("OneOf") or [],
            any_of=body.get("AnyOf") or [],
            must_have=body.get("MustHave") or [],
        )


@dataclass
class Operation:
    """One operation inside a System."""
    name: str
    doc: str = ""
    inputs: list[Member] = field(default_factory=list)
    outputs: list[Member] = field(default_factory=list)

    @classmethod
    def from_raw(cls, item: Any) -> Operation:
        name, body = _extract_item(item)
        return cls(
            name=name,
            doc=body.get("Doc", ""),
            inputs=Member.list_from_raw(body.get("Input")),
            outputs=Member.list_from_raw(body.get("Output")),
        )


@dataclass
class System:
    """A System definition with Operations."""
    name: str
    doc: str = ""
    operations: list[Operation] = field(default_factory=list)

    @classmethod
    def from_raw(cls, item: Any) -> System:
        name, body = _extract_item(item)
        return cls(
            name=name,
            doc=body.get("Doc", ""),
            operations=[Operation.from_raw(o) for o in (body.get("Operations") or [])],
        )


@dataclass
class Ontology:
    name: str
    filename: str
    subfolder: str = ""
    meta: Meta = field(default_factory=lambda: Meta("", "", "", ""))
    doc: str = ""
    linked_ontologies: list[LinkedOntology] = field(default_factory=list)
    base_types: list[BaseType] = field(default_factory=list)
    enums: list[Enum] = field(default_factory=list)
    value_types: list[ValueType] = field(default_factory=list)
    components: list[Component] = field(default_factory=list)
    archetypes: list[Archetype] = field(default_factory=list)
    information_needs: list[InformationNeedEntry] = field(default_factory=list)
    systems: list[System] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: Path, spec_dir: Path | None = None) -> Ontology:
        """Load one ontology YAML file into the runtime model."""
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        raw: dict | None = None
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "Ontology" in item:
                    raw = item["Ontology"]
                    break
        if raw is None:
            raise ValueError(f"No Ontology root found in {path}")
        subfolder = ""
        if spec_dir:
            try:
                rel = path.relative_to(spec_dir)
                subfolder = rel.parent.as_posix()
                if subfolder == ".":
                    subfolder = ""
            except ValueError:
                pass
        return cls(
            name=raw["Name"],
            filename=path.name,
            subfolder=subfolder,
            meta=Meta.from_raw(raw.get("Meta", {})),
            doc=raw.get("Doc", ""),
            linked_ontologies=LinkedOntology.list_from_raw(raw.get("LinkedOntologies")),
            base_types=[BaseType.from_raw(bt) for bt in (raw.get("BaseTypes") or [])],
            enums=[Enum.from_raw(e) for e in (raw.get("Enums") or [])],
            value_types=[ValueType.from_raw(vt) for vt in (raw.get("ValueTypes") or [])],
            components=[Component.from_raw(c) for c in (raw.get("Components") or [])],
            archetypes=[Archetype.from_raw(a) for a in (raw.get("Archetypes") or [])],
            information_needs=[
                InformationNeedEntry.from_raw(ref, body)
                for ref, body in (raw.get("InformationNeed") or {}).items()
            ],
            systems=[System.from_raw(s) for s in (raw.get("Systems") or [])],
        )

    # Convenience properties

    @property
    def linked_names(self) -> list[str]:
        """All linked ontology names (including Core)."""
        return [lo.name for lo in self.linked_ontologies]

    @property
    def linked_prefixes(self) -> dict[str, str]:
        """Mapping {ontology_name: prefix} for links that define a Prefix."""
        return {lo.name: lo.prefix for lo in self.linked_ontologies if lo.prefix}

    def type_names(self) -> set[str]:
        """All type names defined in this ontology."""
        names: set[str] = set()
        for bt in self.base_types:
            names.add(bt.name)
        for e in self.enums:
            names.add(e.name)
        for vt in self.value_types:
            names.add(vt.name)
        for c in self.components:
            names.add(c.name)
        for a in self.archetypes:
            names.add(a.name)
        for s in self.systems:
            names.add(s.name)
        return names


@dataclass
class OntologySet:
    """Collection of ontologies, topologically sorted by dependencies."""
    ontologies: list[Ontology]
    _by_name: dict[str, Ontology] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        self._by_name = {o.name: o for o in self.ontologies}

    @classmethod
    def load(cls, spec_dir: Path | None = None) -> OntologySet:
        """Load all ontology YAML files and return them in dependency order."""
        spec_dir = spec_dir or SPEC_DIR
        raw: list[Ontology] = []
        for path in sorted(spec_dir.glob("**/*.yaml")):
            # Skip glossary / translation companion files
            if ".glossary." in path.name or ".translation." in path.name:
                continue
            try:
                raw.append(Ontology.from_yaml(path, spec_dir))
            except Exception as e:
                print(f"Warning: skipping {path.name}: {e}", file=sys.stderr)

        # Topological sort by LinkedOntologies dependencies
        by_name: dict[str, Ontology] = {o.name: o for o in raw}
        visited: set[str] = set()
        order: list[str] = []

        def visit(name: str) -> None:
            if name in visited or name not in by_name:
                return
            visited.add(name)
            for dep in by_name[name].linked_names:
                visit(dep)
            order.append(name)

        for name in by_name:
            visit(name)

        return cls(ontologies=[by_name[n] for n in order])

    def by_name(self, name: str) -> Ontology | None:
        """Lookup an ontology by its Name (O(1) dict lookup)."""
        return self._by_name.get(name)
