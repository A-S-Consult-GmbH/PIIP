# Positioning

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/Positioning.yaml`](../../spec/Positioning.yaml)

Abstract Provider/Consumer pattern for geometric reference systems. Defines markers and references for entities that provide or consume geometric reference systems of three dimensions: point-based (0D), alignment-based (1D with stationing), and surface-based (2D). Positioning strategies that describe HOW a consumer derives its position from a provider are defined in separate ontologies (SpotPlacement for dP=0, future LinearPlacement for dP=1). LinearPlacement builds on SpotPlacement: bounding points of a station range are themselves SpotPlacements. The separation of Provider/Consumer binding from positioning strategy enables independent evolution: new strategies can be added without modifying the structural binding pattern.

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/Positioning/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |

## Components

| Component | Purpose |
|-----------|---------|
| <a id="pointprovidercomponent"></a>`PointProviderComponent` | Marks an Entity as providing a point-shaped reference frame (position and orientation) that other entities can reference for positioning. |
| <a id="pointconsumercomponent"></a>`PointConsumerComponent` | Binds an Entity to a point provider as positional anchor for point-based positioning. The referenced provider supplies a position and an orientation frame. |
| <a id="alignmentprovidercomponent"></a>`AlignmentProviderComponent` | Marks an Entity as providing a parametric curve with stationing system (alignment) that other entities can reference for positioning. The concrete geometric definition (segments, design stages) is provided by Components in the Alignment ontology. |
| <a id="alignmentconsumercomponent"></a>`AlignmentConsumerComponent` | Binds an Entity to an alignment provider. The referenced provider supplies a parametric curve evaluable along a stationing axis. Domain-agnostic — used by Rail, Road and future domains. |
| <a id="surfaceprovidercomponent"></a>`SurfaceProviderComponent` | Marks an Entity as providing a queryable surface for height evaluation at arbitrary horizontal positions. Used for terrain models (DGM), platform surfaces, and similar 2D reference geometries. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="pointproviderarchetype"></a>`PointProviderArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`PointProviderComponent`](#pointprovidercomponent) |
| <a id="pointconsumerarchetype"></a>`PointConsumerArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`PointConsumerComponent`](#pointconsumercomponent) |
| <a id="alignmentproviderarchetype"></a>`AlignmentProviderArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`AlignmentProviderComponent`](#alignmentprovidercomponent) |
| <a id="alignmentconsumerarchetype"></a>`AlignmentConsumerArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`AlignmentConsumerComponent`](#alignmentconsumercomponent) |
| <a id="surfaceproviderarchetype"></a>`SurfaceProviderArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`SurfaceProviderComponent`](#surfaceprovidercomponent) |
