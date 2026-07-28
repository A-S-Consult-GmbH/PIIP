# CrossProfile

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/CrossProfile.yaml`](../../spec/CrossProfile.yaml)

Domain-agnostic cross-profile definitions along alignments.

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/CrossProfile/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |
| [Positioning](_Positioning.md) | `https://w3id.org/piip/Positioning/1` | `pos` |
| [Alignment](_Alignment.md) | `https://w3id.org/piip/Alignment/1` | `align` |
| [Geometry](_Geometry.md) | `https://w3id.org/piip/Geometry/1` | `geo` |

## Enums

<a id="crossprofileinterpolation"></a>**`CrossProfileInterpolation`**
: Interpolation mode between corresponding points in adjacent CrossProfileSections.
  Values: `Linear`, `ConstantFromSource`, `ConstantToTarget`

## ValueTypes

<a id="crossprofilepoint"></a>**`CrossProfilePoint`**
: Single point in a cross-profile with offset, height, and interpolation to the next section.
  Members: [`LengthValue`](_Core.md#lengthvalue) `offset`, [`LengthValue`](_Core.md#lengthvalue) `height`, [`CrossProfileInterpolation`](#crossprofileinterpolation) `interpolation`

<a id="crossprofileline"></a>**`CrossProfileLine`**
: Typed sequence of CrossProfilePoints within a CrossProfileSection.
  Members: [`Link<CrossProfileTypeDefinitionArchetype>`](#crossprofiletypedefinitionarchetype) `type`, [`List<CrossProfilePoint>`](#crossprofilepoint) `points`

<a id="crossprofilesection"></a>**`CrossProfileSection`**
: Complete cross-profile at a single station, composed of typed lines.
  Members: [`align:StationValue`](_Alignment.md#stationvalue) `station`, [`List<CrossProfileLine>`](#crossprofileline) `lines`

## Components

| Component | Purpose |
|-----------|---------|
| <a id="crossprofiletypedefinitioncomponent"></a>`CrossProfileTypeDefinitionComponent` | Marker identifying an Entity as a named cross-profile line type. |
| <a id="crossprofiledefinitioncomponent"></a>`CrossProfileDefinitionComponent` | Ordered cross-profile sections along an alignment with per-point interpolation. The alignment reference is provided structurally via AlignmentConsumerArchetype. |
| <a id="crossprofiletypevolumecomponent"></a>`CrossProfileTypeVolumeComponent` | Binds a volume entity to a cross-profile line type, a discretization, and a cross-profile definition. The Sweep-System generates the MeshGeometry3DComponent from these references. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="crossprofiletypedefinitionarchetype"></a>`CrossProfileTypeDefinitionArchetype` | [`NamedArchetype`](_Core.md#namedarchetype) | [`CrossProfileTypeDefinitionComponent`](#crossprofiletypedefinitioncomponent) |
| <a id="crossprofiledefinitionarchetype"></a>`CrossProfileDefinitionArchetype` | [`NamedArchetype`](_Core.md#namedarchetype), [`pos:AlignmentConsumerArchetype`](_Positioning.md#alignmentconsumerarchetype) | [`CrossProfileDefinitionComponent`](#crossprofiledefinitioncomponent) |
| <a id="crossprofiletypevolumearchetype"></a>`CrossProfileTypeVolumeArchetype` | [`NamedArchetype`](_Core.md#namedarchetype), [`geo:MeshGeometry3DArchetype`](_Geometry.md#meshgeometry3darchetype) | [`CrossProfileTypeVolumeComponent`](#crossprofiletypevolumecomponent) |
