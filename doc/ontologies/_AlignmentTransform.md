# AlignmentTransform

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/AlignmentTransform.yaml`](../../spec/AlignmentTransform.yaml)

System contract for transforming a georeferenced track alignment from a source to a target coordinate context under a tolerance. Depends on PointTransformSystem.TransformPoint without binding a concrete runtime. The handle is injected at Start (constructor/factory binding) and held for the lifetime of the instance of the AlignmentTransformSystem. Pointwise adaptive densification and parametric element reconstruction are admissible runtime variants of the same outer contract. Slim provenance is a system-concern ValueType. Data inputs use deep Link resolution; representation completeness is declared in InformationNeed (Archetype → OneOf), not in the Domain model.

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/AlignmentTransform/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |
| [Alignment](_Alignment.md) | `https://w3id.org/piip/Alignment/1` | `align` |
| [Rail](_Rail.md) | `https://w3id.org/piip/Rail/1` | `rail` |
| [SpatialReference](_SpatialReference.md) | `https://w3id.org/piip/SpatialReference/1` | `sref` |
| [PointTransform](_PointTransform.md) | `https://w3id.org/piip/PointTransform/1` | `pt` |

## ValueTypes

<a id="alignmenttransformsystemhandle"></a>**`AlignmentTransformSystemHandle`**
: Typed handle of a started AlignmentTransformSystem runtime instance. Part of the public AlignmentTransform contract. Field semantics match pt:PointTransformSystemHandle; the ValueType is bound to this system so callers cannot mix handles from different systems.
  Members: [`Uri`](_Core.md#uri) `endpoint`, [`UUID`](_Core.md#uuid) `systemId`, [`Uri`](_Core.md#uri) `contractUri`

<a id="alignmenttransformprovenance"></a>**`AlignmentTransformProvenance`**
: Black-box-visible derivation metadata for an alignment produced by TransformAlignment. Identity references use Link (GUID); no full Data copies of geometries. No internal geodetic parameter sets.
  Members: [`Optional<Link<rail:TrackAlignmentArchetype>>`](_Rail.md#trackalignmentarchetype) `sourceAlignment`, [`Optional<Link<sref:CoordinateContextArchetype>>`](_SpatialReference.md#coordinatecontextarchetype) `sourceContext`, [`Optional<Link<sref:CoordinateContextArchetype>>`](_SpatialReference.md#coordinatecontextarchetype) `targetContext`, [`String`](_Core.md#string) `methodId`, [`Optional<UUID>`](_Core.md#uuid) `pointTransformSystemId`, [`Real`](_Core.md#real) `requestedTolerance`, [`Optional<Real>`](_Core.md#real) `achievedAccuracy`

<a id="alignmenttransformresult"></a>**`AlignmentTransformResult`**
: Result of TransformAlignment (PlacementResult pattern): on success alignment Data and provenance are set; on failure errorMessage is set and alignment is absent. No redundant success flag.
  Members: [`Optional<Data<rail:TrackAlignmentArchetype>>`](_Rail.md#trackalignmentarchetype) `alignment`, [`Optional<AlignmentTransformProvenance>`](#alignmenttransformprovenance) `provenance`, [`Optional<String>`](_Core.md#string) `errorMessage`

## InformationNeed

| Archetype | Rule | Components |
|-----------|------|------------|
| [`align:HorizontalDesignStageArchetype`](_Alignment.md#horizontaldesignstagearchetype) | OneOf | [`align:SegmentedHorizontalDesignStageComponent`](_Alignment.md#segmentedhorizontaldesignstagecomponent), [`align:Nurb2DHorizontalDesignStageComponent`](_Alignment.md#nurb2dhorizontaldesignstagecomponent) |
| [`align:VerticalDesignStageArchetype`](_Alignment.md#verticaldesignstagearchetype) | OneOf | [`align:SegmentedVerticalDesignStageComponent`](_Alignment.md#segmentedverticaldesignstagecomponent) |
| [`align:CantDesignStageArchetype`](_Alignment.md#cantdesignstagearchetype) | OneOf | [`align:SegmentedCantDesignStageComponent`](_Alignment.md#segmentedcantdesignstagecomponent) |

## Systems

### <a id="alignmenttransformsystem"></a>`AlignmentTransformSystem`

Track alignment transformation under tolerance. Start binds a live PointTransformSystemHandle (factory/constructor injection). TransformAlignment uses that binding; it does not accept a new handle per call. Own instance identity is AlignmentTransformSystemHandle. Payload InformationNeed is ontology-level (not per-operation paths).

#### `Start`

Start the AlignmentTransformSystem and bind the given PointTransformSystemHandle for the instance lifetime (constructor/factory pattern). Returns AlignmentTransformSystemHandle for subsequent operations. Dependency on the PointTransformSystem is expressed by the typed handle input and LinkedOntologies.

**Input:**

| Type | Name | Description |
|------|------|-------------|
| [`pt:PointTransformSystemHandle`](_PointTransform.md#pointtransformsystemhandle) | `pointTransform` | Started S1 instance used for all TransformPoint calls of this S2 instance. |

**Output:**

| Type | Name |
|------|------|
| [`AlignmentTransformSystemHandle`](#alignmenttransformsystemhandle) | `handle` |

#### `TransformAlignment`

Transform a track alignment into the target coordinate context on the AlignmentTransformSystem instance identified by handle. Uses the PointTransformSystem bound at Start. Alignment and contexts are Data (by-value, deep Link resolve), not Link (GUID-only). Representation completeness: ontology InformationNeed on design-stage Archetypes encountered in the payload closure. Does not prescribe pointwise versus parametric strategy.

**Input:**

| Type | Name | Description |
|------|------|-------------|
| [`AlignmentTransformSystemHandle`](#alignmenttransformsystemhandle) | `handle` | Started AlignmentTransformSystem instance to invoke. |
| [`Data<rail:TrackAlignmentArchetype>`](_Rail.md#trackalignmentarchetype) | `sourceAlignment` | By-value track alignment. Serialise Archetype Components; deep-resolve Link members. Nested design stages validated via InformationNeed. |
| [`Data<sref:CoordinateContextArchetype>`](_SpatialReference.md#coordinatecontextarchetype) | `sourceContext` |  |
| [`Data<sref:CoordinateContextArchetype>`](_SpatialReference.md#coordinatecontextarchetype) | `targetContext` |  |
| [`Real`](_Core.md#real) | `tolerance` | Maximum admissible linearisation / reconstruction error. |

**Output:**

| Type | Name |
|------|------|
| [`AlignmentTransformResult`](#alignmenttransformresult) | `result` |

#### `Shutdown`

Stop the AlignmentTransformSystem instance identified by the handle. Releases the bound AlignmentTransformSystemHandle association.

**Input:**

| Type | Name | Description |
|------|------|-------------|
| [`AlignmentTransformSystemHandle`](#alignmenttransformsystemhandle) | `handle` |  |

**Output:**

| Type | Name |
|------|------|
| [`Boolean`](_Core.md#boolean) | `success` |
