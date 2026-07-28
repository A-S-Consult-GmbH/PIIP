# SpotPlacement

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/SpotPlacement.yaml`](../../spec/SpotPlacement.yaml)

Horizontal and vertical positioning strategies for spot-based positioning. Defines HOW a discrete position is derived relative to point providers (Positioning ontology) or along alignment providers (Positioning + Alignment ontologies). The Provider/Consumer binding pattern is defined in the Positioning ontology; this ontology defines only the concrete strategies and the SpotPlacementComponent that combines them. Named 'Spot' to distinguish parametric access from geometric result: Point describes the geometric primitive, Spot describes discrete evaluation at a single location.

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/SpotPlacement/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |
| [Geometry](_Geometry.md) | `https://w3id.org/piip/Geometry/1` | `geo` |
| [Positioning](_Positioning.md) | `https://w3id.org/piip/Positioning/1` | `pos` |
| [Alignment](_Alignment.md) | `https://w3id.org/piip/Alignment/1` | `align` |
| [CrossProfile](_CrossProfile.md) | `https://w3id.org/piip/CrossProfile/1` | `cp` |

## Enums

<a id="verticalalignmentreference"></a>**`VerticalAlignmentReference`**
: Selects the vertical reference height from an alignment provider. ReferenceAxis uses the height at the reference axis (e.g. top of rail without superelevation, reference edge for roads). Gradient uses the height from the vertical design stage (gradient height, typically at the centreline).
  Values: `ReferenceAxis`, `Gradient`

<a id="projectiondirection"></a>**`ProjectionDirection`**
  Values: `TopToBottom`, `BottomToTop`

## ValueTypes

<a id="horizontalplacement"></a>**`HorizontalPlacement`**
: additionalToX, additionalToY are applied after the main positioning
  Members: [`Optional<LengthValue>`](_Core.md#lengthvalue) `additionalToX`, [`Optional<LengthValue>`](_Core.md#lengthvalue) `additionalToY`

<a id="verticalplacement"></a>**`VerticalPlacement`**
: additionalToHeight is applied after the main positioning
  Members: [`Optional<LengthValue>`](_Core.md#lengthvalue) `additionalToHeight`

## Components

| Component | Purpose |
|-----------|---------|
| <a id="spotplacementcomponent"></a>`SpotPlacementComponent` | Positions an Entity at a discrete location by combining a horizontal and vertical placement strategy with an optional local transformation. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="spotplacedarchetype"></a>`SpotPlacedArchetype` | [`pos:PointProviderArchetype`](_Positioning.md#pointproviderarchetype) | [`SpotPlacementComponent`](#spotplacementcomponent) |
