# Road

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/Road.yaml`](../../spec/Road.yaml)

Road tracks, delineators, road alignment composition. Links Core, Positioning (AlignmentConsumerArchetype, AlignmentProviderArchetype, PointProviderArchetype), Alignment (AlignmentArchetype, HorizontalDesignStageArchetype, VerticalDesignStageArchetype, CrossSlopeDesignStageArchetype), SpotPlacement (SpotPlacementComponent), Reference (ReferenceArchetype).

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/Road/1` |
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
| [SpotPlacement](_SpotPlacement.md) | `https://w3id.org/piip/SpotPlacement/1` | `spot` |
| [Reference](_Reference.md) | `https://w3id.org/piip/Reference/1` | `ref` |

## ValueTypes

<a id="crosssectioncontainer"></a>**`CrossSectionContainer`**
: Container for cross section profiles along a road track.

## Components

| Component | Purpose |
|-----------|---------|
| <a id="roadalignmentcomponent"></a>`RoadAlignmentComponent` | Aggregates horizontal, vertical and cross slope design stages into a road alignment. |
| <a id="roadtrackcomponent"></a>`RoadTrackComponent` | Physical road track with alignment and cross sections. |
| <a id="delineatorcomponent"></a>`DelineatorComponent` | Road delineator referencing its parent road, placement and reference object. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="roadalignmentarchetype"></a>`RoadAlignmentArchetype` | [`align:AlignmentArchetype`](_Alignment.md#alignmentarchetype) | [`RoadAlignmentComponent`](#roadalignmentcomponent) |
| <a id="roadtrackarchetype"></a>`RoadTrackArchetype` | [`pos:AlignmentConsumerArchetype`](_Positioning.md#alignmentconsumerarchetype), [`pos:AlignmentProviderArchetype`](_Positioning.md#alignmentproviderarchetype) | [`RoadTrackComponent`](#roadtrackcomponent) |
| <a id="delineatorarchetype"></a>`DelineatorArchetype` | [`pos:PointProviderArchetype`](_Positioning.md#pointproviderarchetype) | [`DelineatorComponent`](#delineatorcomponent) |
