# Reference

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/Reference.yaml`](../../spec/Reference.yaml)

Musterobjekte, Baugruppen and product instances.

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/Reference/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |
| [Geometry](_Geometry.md) | `https://w3id.org/piip/Geometry/1` | `geo` |

## ValueTypes

<a id="referencepartitem"></a>**`ReferencePartItem`**
: Placement and reference to a single part within an assembly.
  Members: [`Optional<geo:AffineTransformation3D>`](_Geometry.md#affinetransformation3d) `localPlacement`, [`Link<ReferenceArchetype>`](#referencearchetype) `referenceObject`

## Components

| Component | Purpose |
|-----------|---------|
| <a id="referencegeometrycomponent"></a>`ReferenceGeometryComponent` | Geometry and local placement of a reference part (prototype). Defined once (SSoT) and reused in multiple product instances. |
| <a id="referenceassemblycomponent"></a>`ReferenceAssemblyComponent` | Collection of reference parts forming a hierarchical assembly structure. Enables nested compositions of reusable prototypes. |
| <a id="referencepartcomponent"></a>`ReferencePartComponent` | Reference to a single part within an assembly, including its local placement relative to the assembly origin. |
| <a id="productinstancecomponent"></a>`ProductInstanceComponent` | Links a domain Entity to a reference object (prototype), realizing the instantiation of a standardized component in a specific planning context. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="referencearchetype"></a>`ReferenceArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`ReferenceGeometryComponent`](#referencegeometrycomponent) |
| <a id="referenceassemblyarchetype"></a>`ReferenceAssemblyArchetype` | [`ReferenceArchetype`](#referencearchetype) | [`ReferenceAssemblyComponent`](#referenceassemblycomponent) |
| <a id="productinstancearchetype"></a>`ProductInstanceArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`ProductInstanceComponent`](#productinstancecomponent) |
