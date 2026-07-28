# Process Information Infrastructure Protocol (PIIP)

YAML-based information model specification following an **Entity-Component-System (ECS)** architecture for infrastructure.

## Specification

| Document | Content |
|----------|---------|
| [Syntax](doc/syntax.md) | YAML syntax reference — all elements, member forms, naming conventions, versioning rules |
| [Architecture](doc/architecture.md) | ECS architecture, three-layer concern model (Domain / System / Process), Linked Data, generation targets |
| [Validation](doc/validation.md) | Validation pipeline (L1 yamllint, L2 JSON Schema, L3 semantic cross-file checks) |
| [Ontologies](doc/_generated_ontologies.md) | Auto-generated documentation for all ontology YAML files (files prefixed with `_` are generated) |

## Quick Start

Validate all ontology YAML files:

```
cd source
pip install -r requirements.txt
python validate.py
```

Generate Markdown documentation:

```
cd source
python generate_docs.py
```

Each YAML file is named after its ontology (`spec/Core.yaml`, …) and follows this structure:

```yaml
- Ontology:
    Name: <Name>
    Meta:
        Uri: https://w3id.org/piip/<Name>/1
        Organization: A+S Consult GmbH FuE
        OrganizationUri: https://apluss.de/a+s_consult
        Version: 1.0.0
    LinkedOntologies:           # dependencies to other ontologies
        - Core:
            Uri: https://w3id.org/piip/Core/1
    Enums:                      # optional — fixed value sets
    ValueTypes:                 # optional — composite value objects (no identity)
    Components:                 # atomic, disjoint data packets (*Component)
    Archetypes:                 # descriptive Component compositions (*Archetype)
```

See [doc/syntax.md](doc/syntax.md) for the full syntax reference.

# License
Copyright &copy; 2026 A+S Consult GmbH FuE

This project uses two licenses:

| Scope | License | File |
|-------|---------|------|
| Specification (`spec/`) | [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/legalcode) | [LICENSE](LICENSE) |
| Tooling (`source/`) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [source/LICENSE](source/LICENSE) |

The ECS architecture and ontology design are based on the doctoral thesis *"Ein komponentenbasiertes Rahmenwerk für Gleisnetze: Trassierung, Topologie und Fachobjekte in einer Entity-Component-System-Architektur"* by Jens Bartnitzek (BTU Cottbus–Senftenberg).

## Specification — CC BY-ND 4.0

The specification (ontology YAML files and documentation) is licensed under the Creative Commons Attribution-NoDerivatives 4.0 International Public License.
You can implement the specification in services, clients or processing tools without restrictions.

You may also extend or modify the standard using the built-in extension and profiling mechanisms, however modified or extended versions of the standard may not be redistributed. The standard may only be redistributed in its unmodified version, under the same license.

You are free to:

- Share — copy and redistribute the material in any medium or format for any purpose, even commercially.
- The licensor cannot revoke these freedoms as long as you follow the license terms.

Under the following terms:

- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- No derivatives — If you remix, transform, or build upon the material, you may not distribute (see note below) the modified material.
- No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

## Tooling — Apache 2.0

The Python source code (`source/`) for validation and documentation generation is licensed under the Apache License, Version 2.0. This provides an explicit patent grant, protecting users from patent claims by contributors. See [source/LICENSE](source/LICENSE) for details.