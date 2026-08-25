# PIIP Validation Pipeline

Three-level validation pipeline for piip ontology YAML files (`spec/**/*.yaml`).

## Usage

```bash
cd source
python validate.py              # run all levels
python validate.py --level 1    # only L1 (YAML syntax)
python validate.py --level 2    # only L2 (JSON Schema)
python validate.py --level 3    # only L3 (semantic checks)
python validate.py path/to/file.yaml   # specific file(s)
```

## Validation Levels

### L1 — YAML Syntax (yamllint)

Catches malformed YAML before any structural or semantic analysis.

| Check | Example Error |
|-------|---------------|
| Valid YAML syntax | Tabs instead of spaces, unclosed brackets |
| Duplicate mapping keys | Two `Members:` keys in same block |
| Line length | Lines exceeding 400 characters |

**Config**: [`source/validator/.yamllint.yml`](../source/validator/.yamllint.yml)

### L2 — JSON Schema (structural grammar)

Validates that the YAML structure matches the piip ontology grammar defined in [syntax.md](syntax.md).

| Check | Example Error |
|-------|---------------|
| `Ontology` has required keys: `Name`, `Meta`, `Components`, `Archetypes` | Missing `Archetypes` key |
| `Meta` has `Uri` (w3id.org pattern), `Version` (semver) | `Version: "1.0"` (not semver) |
| `LinkedOntologies` entries have `Uri`, optional `Prefix` | Missing `Uri` in linked ontology |
| Components have only `Doc` and/or `Members` | Component with `Extends` key |
| Components must **not** have `Extends` or `Includes` | `Extends: SomeComponent` in a Component |
| Members match short form (`Type name`) or explicit `Member:` with `Name`+`Type` | `Member:` missing `Type` |
| Enums require `Values` array with unique items | Duplicate enum value |
| ValueTypes allow `Extends`, `Members`, `Doc` | Unknown key in ValueType |
| Archetypes allow `Doc`, `Includes`, `Components` | Unknown key in Archetype |
| No unknown keys anywhere (`additionalProperties: false`) | Typo like `Compoents:` |

**Schema**: [`source/validator/piip_schema.json`](../source/validator/piip_schema.json)

### L3 — Semantic Checks (cross-file analysis)

Loads all ontologies into a shared runtime model and validates cross-file references, naming conventions, and prefix consistency.

| Check | Category | Example Error |
|-------|----------|---------------|
| Components end in `*Component` | Naming | `EpsgCode` instead of `EpsgCodeComponent` |
| Archetypes end in `*Archetype` | Naming | `Datum` instead of `DatumArchetype` |
| No duplicate names across ontologies | Uniqueness | `AlignmentArchetype` in both `alignment.yaml` and `generic_objects.yaml` |
| `LinkedOntologies` reference existing ontologies | References | `LinkedOntology 'Foo' not found` |
| `LinkedOntologies` URI matches actual ontology URI | Versioning | URI `…/Core/1` but actual is `…/Core/2` |
| Non-Core linked ontologies must declare `Prefix` | Prefixes | `LinkedOntology 'Geometry' must declare a Prefix` |
| Prefixes unique within each file | Prefixes | `Prefix 'geo' used by both 'Geometry' and 'Geodesy'` |
| Same ontology uses same prefix across all files | Prefixes | `Geometry` mapped to `geo` in one file, `geom` in another |
| Types from prefixed ontologies must use prefix | Prefixes | `'Point2D' must be qualified as 'geo:Point2D'` |
| Archetype `Includes` resolve to existing Archetypes | References | `Includes 'FooArchetype' which is not a known Archetype` |
| Archetype `Components` resolve to existing Components | References | `Component 'FooComponent' which is not defined` |
| ValueType `Extends` resolves to existing ValueType | References | `extends 'Foo' which is not a known ValueType` |
| Member type refs resolve (incl. `Optional<>`, `Set<>`, `List<>`, `Link<>`, `Data<>`) | References | `type 'Foo' not found in any visible ontology` |
| Prefixed type refs resolve in target ontology | References | `'Bar' not found in 'Geometry' (prefix 'geo')` |
| `Data<T>` / `Link<T>` wrap an Archetype | References | `Link<Foo>: 'Foo' is not an Archetype` |
| Archetype member types wrapped in `Link<>` or `Data<>` | References | `Archetype 'VersionedArchetype' must be wrapped in Link<> or Data<> (got 'Optional<VersionedArchetype>')` |

**Implementation**: [`source/validator/l3_semantic.py`](../source/validator/l3_semantic.py)

## Architecture

```
source/
    validate.py                 # entry point
    shared/
        piip_model.py            # dataclass model: Ontology, Component, Archetype, ...
    validator/
        l1_yamllint.py          # L1 runner
        l2_schema.py            # L2 in-process JSON Schema validation
        l3_semantic.py          # L3 cross-file semantic checks
        .yamllint.yml           # yamllint config
        piip_schema.json         # JSON Schema for piip ontology grammar
```

All three levels share the same runtime model from `shared/piip_model.py`.
