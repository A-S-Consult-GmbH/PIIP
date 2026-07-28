# PIIP YAML Syntax Reference

The piip information model is specified in YAML files following an Entity-Component-System (ECS) architecture. Each `<name>.yaml` file defines one **ontology** — a self-contained domain module with typed links to other ontologies.

## File Naming

All ontology files use the ontology **`Name` as filename** (PascalCase) under `spec/`:

| Path | Example | Ontology IRI |
|------|---------|--------------|
| `spec/<Name>.yaml` | `spec/Core.yaml` | `https://w3id.org/piip/Core/1` |
| `spec/<Name>.yaml` | `spec/PointTransform.yaml` | `https://w3id.org/piip/PointTransform/1` |

There is no domain/system distinction in the IRI or filename. Optional subfolders under `spec/` are only local organisation; permanent links always use `{Name}` only.

w3id pattern: `https://w3id.org/piip/{Name}/{Major}` → `spec/{Name}.yaml` (or `{X.Y.Z}` → git tag `vX.Y.Z`).

## Top-Level Structure

Every file contains exactly one YAML document starting with:

```yaml
- Ontology:
    Name: <OntologyName>
    Meta:
        Uri: https://w3id.org/piip/<OntologyName>/<Major>
        Organization: <publisher>
        OrganizationUri: <publisher-url>
        Version: <Major>.<Minor>.<Patch>
    LinkedOntologies:    # optional
    BaseTypes:           # only in Core
    Enums:               # optional
    ValueTypes:          # optional
    Components:          # optional (required for domain ontologies)
    Archetypes:          # optional (required for domain ontologies)
    InformationNeed:     # optional (system ontologies)
    Systems:             # optional (system ontologies)
```

## Elements

### Meta

| Key               | Description                                                      |
|--------------------|------------------------------------------------------------------|
| `Uri`              | Globally unique, versionised Linked-Data URI (major in path).    |
| `Organization`     | Publishing organisation.                                         |
| `OrganizationUri`  | Organisation URI.                                                |
| `Version`          | Semantic version `Major.Minor.Patch`.                            |

### LinkedOntologies

Declares dependencies to other ontologies by name, versionised URI, and optional prefix.

```yaml
LinkedOntologies:
    - Core:
        Uri: https://w3id.org/piip/Core/1
    - Geometry:
        Uri: https://w3id.org/piip/Geometry/1
        Prefix: geo              # optional — required only on name collisions
```

Types from linked ontologies can be used unqualified when names are unique; otherwise qualify with `<Prefix>:<TypeName>` (e.g. `geo:Point3D`).

### BaseTypes (Core only)

Defines primitive types bound to standard namespaces, plus generic container types.

```yaml
BaseTypes:
    - UUID:       { Type: Core:UUID }
    - Entity:     { Type: Core:UUID }
    - String:    { Type: xsd:string }
    - Real:       { Type: xsd:double }
    - Integer:    { Type: xsd:integer }
    - Index:      { Type: xsd:integer }
    - Boolean:       { Type: xsd:boolean }
    - Optional<>
    - Set<>
    - List<>
```

| Container      | Semantics                                |
|----------------|------------------------------------------|
| `Optional<T>`  | Zero or one value of type `T`.           |
| `Set<T>`       | Unordered collection, no duplicates.     |
| `List<T>`      | Ordered collection, allows duplicates.   |

### Enums

Fixed set of allowed values.

```yaml
Enums:
    - SwitchType:
        Doc: Type of switch       # optional documentation
        Values: [ SimpleSwitch, OutsideCurvedSwitch, InsideCurvedSwitch, ... ]
```

### ValueTypes

Composite value objects **without Entity identity**. They are embedded in Components and carry no suffix.

```yaml
ValueTypes:
    - Point3D:
        Members:
            - Real x
            - Real y
            - Real z
```

**Extends** — single inheritance for ValueTypes:

```yaml
    - HorizontalLine:
        Extends: HorizontalSegment
        Members:
            - Point2D startPoint
            - Real startAngle
            - Real length
```

The resolved member set is: `Members(V) = Members(Parent) ∪ OwnMembers(V)`.

### Components

Disjoint, atomic data packets. Each Component describes exactly **one** facet. Components carry the suffix `*Component`.

```yaml
Components:
    - NameComponent:
        Doc: Human-readable name.      # optional
        Members:
            - Member:
                Name: name
                Type: String
                Doc: Human-readable name of the entity.
```

Components must **not** use `Extends` or `Includes`. They have no structural dependency on each other.

### Members

Members define the properties of a Component or ValueType.

**Short form** (type + name on one line):

```yaml
- String name
- Optional<VersionedArchetype> previousVersion
- Set<ReferencePartItem> parts
```

**Long form** (when `Doc` is needed):

```yaml
- Member:
    Name: anchor
    Type: Optional<LifecycleAnchorArchetype>
    Doc: Reference to the persistent lifecycle anchor Entity.
```

**Type** can be any of: `BaseType`, `Enum`, `ValueType`, or `Archetype`. An Archetype-typed member represents a **reference** to an Entity fulfilling that Archetype. Technically the reference is a `UUID`; the Archetype typing documents the expected contract.

### Archetypes

Named, descriptive compositions of Components. Archetypes carry the suffix `*Archetype`.

```yaml
Archetypes:
    - LifecycleArchetype:
        Doc: Versioned domain object with lifecycle reference.
        Includes: [ VersionedArchetype ]
        Components: [ LifecycleReferenceComponent ]
```

**Includes** — set-theoretic union of Component lists from referenced Archetypes:

```
Components(A) = OwnComponents(A) ∪ ⋃ Components(Bᵢ)
```

Includes is resolved at specification time; at runtime only Component queries exist. Archetypes follow the **Open World Assumption**: an Entity may have more Components than an Archetype declares.

### Marker Components

Components with `Doc` but **no `Members`** act as markers:

```yaml
- LifecycleAnchorComponent:
    Doc: Marker without data fields.
```

## Naming Convention

| ECS Role    | Suffix          | Example                            |
|-------------|-----------------|-------------------------------------|
| Component   | `*Component`    | `NameComponent`, `EdgeComponent`    |
| Archetype   | `*Archetype`    | `VersionedArchetype`, `NodeArchetype` |
| System      | `*System`       | `PlacementCalculationSystem`        |
| ValueType   | _(none)_        | `Point3D`, `HorizontalSegment`      |
| Enumeration | _(none)_        | `SwitchType`, `CantType`            |

## Versioning Rules

- **Major** (URI changes): breaking changes — removing, renaming, or re-typing existing elements.
- **Minor**: additive, backward-compatible changes — new Components, Archetypes, Enums.
- **Patch**: documentation or metadata corrections only.

**Published Components are structurally frozen.** New information goes into new Components. Extending an Archetype via `Includes` of new Components is a Minor change.
