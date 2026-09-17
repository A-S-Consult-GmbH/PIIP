# PIIP Validation Pipeline

Three-level validation for ontology YAML files (`spec/**/*.yaml`). The implementation lives in [PIIP_tooling](https://github.com/A-S-Consult-GmbH/PIIP_tooling). Grammar details are in [syntax.md](syntax.md).

## Usage

```bash
pip install git+https://github.com/A-S-Consult-GmbH/PIIP_tooling.git@v0.1.0
piip validate --config piip_config.yaml
piip docs --config piip_config.yaml
```

```bash
piip validate --config piip_config.yaml --level 1
piip validate --config piip_config.yaml --level 2
piip validate --config piip_config.yaml --level 3
```

This repository is a public spec root: `piip_config.yaml` sets `entry: spec/` and profile `public` follows from w3id URIs.

## Validation Levels

### L1 — YAML Syntax (yamllint)

Catches malformed YAML before structural or semantic analysis.

| Check | Example Error |
|-------|---------------|
| Valid YAML syntax | Tabs instead of spaces, unclosed brackets |
| Duplicate mapping keys | Two `Members:` keys in same block |
| Line length | Lines exceeding 400 characters |

### L2 — JSON Schema (structural grammar)

Validates that the YAML structure matches the ontology grammar. `Meta.Uri` is an http(s) URI. The w3id prefix is a **profile** check, not part of the grammar.

| Check | Example Error |
|-------|---------------|
| `Ontology` has required keys: `Name`, `Meta` | Missing `Meta` |
| `Meta` has `Uri`, `Version` (semver) | `Version: "1.0"` (not semver) |
| `LinkedOntologies` entries have `Uri`, optional `Prefix` | Missing `Uri` in linked ontology |
| Components have only `Doc` and/or `Members` | Component with `Extends` key |
| Components must **not** have `Extends` or `Includes` | `Extends: SomeComponent` in a Component |
| Members match short form (`Type name`) or explicit `Member:` with `Name`+`Type` | `Member:` missing `Type` |
| Enums require `Values` array with unique items | Duplicate enum value |
| ValueTypes allow `Extends`, `Members`, `Doc` | Unknown key in ValueType |
| Archetypes allow `Doc`, `Includes`, `Components` | Unknown key in Archetype |
| No unknown keys anywhere (`additionalProperties: false`) | Typo like `Compoents:` |

### L3 — Semantic Checks (cross-file analysis)

Loads the transitive `LinkedOntologies` graph and checks references, naming, and prefixes.

| Check | Category | Example Error |
|-------|----------|---------------|
| Components end in `*Component` | Naming | `EpsgCode` instead of `EpsgCodeComponent` |
| Archetypes end in `*Archetype` | Naming | `Datum` instead of `DatumArchetype` |
| No duplicate names across ontologies | Uniqueness | `AlignmentArchetype` in two files |
| `LinkedOntologies` resolve by URI | References | URI not in the loaded set |
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
| Archetype member types wrapped in `Link<>` or `Data<>` | References | `Archetype 'VersionedArchetype' must be wrapped in Link<> or Data<>` |

Public ontologies use `https://w3id.org/piip/` URIs. Closed consumer ontologies use other http(s) URIs and must not use that prefix.
