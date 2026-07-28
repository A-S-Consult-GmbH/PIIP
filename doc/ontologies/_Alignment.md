# Alignment

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/Alignment.yaml`](../../spec/Alignment.yaml)

Geometric alignment: horizontal, vertical, cant, cross slope, stationing, discretisation. Domain-agnostic — concrete alignment compositions (TrackAlignmentComponent, RoadAlignmentComponent) are defined in their respective domain ontologies (Rail, Road). Design stages (layer 1) are individual coordinate functions (horizontal, vertical, cant); an alignment (layer 2) is the composed Frenet curve evaluable in 3D along a stationing axis. Links Core for base types and Geometry for Point2D.

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/Alignment/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |
| [Positioning](_Positioning.md) | `https://w3id.org/piip/Positioning/1` | `pos` |
| [Geometry](_Geometry.md) | `https://w3id.org/piip/Geometry/1` | `geo` |

## Enums

<a id="horizontaltransitiontype"></a>**`HorizontalTransitionType`**
  Values: `Clothoid`, `HelmertCurve`, `HelmertHalfCurve`, `BlossCurve`, `BlossHalfCurve`, `SineCurve`, `CosineCurve`

<a id="canttype"></a>**`CantType`**
  Values: `Linear`, `HelmertCurve`, `HelmertHalfCurve`, `BlossCurve`, `BlossHalfCurve`, `SineCurve`, `CosineCurve`, `VienneseBend`

<a id="designstage"></a>**`DesignStage`**
: Defines the specific design layer of the alignment, such as horizontal alignment, vertical alignment, spatial layout, or cant.
  Values: `Horizontal`, `Vertical`, `Spatial`, `Cant`

<a id="slopesegmenttype"></a>**`SlopeSegmentType`**
  Values: `Linear`, `Parabolic`

<a id="stationreference"></a>**`StationReference`**
: Classifies the parametrisation of a station value. InternalStation is the arc length along the referenced alignment; ExternalStation is the reparametrised kilometrage station including jumps and scaling. Foreign stationing (Fremdstationierung) is expressed structurally by referencing a different alignment in the StationComponent, not by an enum value.
  Values: `InternalStation`, `ExternalStation`

## ValueTypes

<a id="horizontalsegment"></a>**`HorizontalSegment`**

<a id="horizontalline"></a>**`HorizontalLine`** extends [`HorizontalSegment`](#horizontalsegment)
  Members: [`geo:Point2D`](_Geometry.md#point2d) `startPoint`, [`AngleValue`](_Core.md#anglevalue) `startAngle`, [`LengthValue`](_Core.md#lengthvalue) `length`

<a id="horizontalcirculararc"></a>**`HorizontalCircularArc`** extends [`HorizontalSegment`](#horizontalsegment)
  Members: [`geo:Point2D`](_Geometry.md#point2d) `startPoint`, [`AngleValue`](_Core.md#anglevalue) `startAngle`, [`LengthValue`](_Core.md#lengthvalue) `length`, [`LengthValue`](_Core.md#lengthvalue) `radius`

<a id="horizontaltransition"></a>**`HorizontalTransition`** extends [`HorizontalSegment`](#horizontalsegment)
  Members: [`geo:Point2D`](_Geometry.md#point2d) `startPoint`, [`AngleValue`](_Core.md#anglevalue) `startAngle`, [`LengthValue`](_Core.md#lengthvalue) `length`, [`CurvatureValue`](_Core.md#curvaturevalue) `startCurvature`, [`CurvatureValue`](_Core.md#curvaturevalue) `endCurvature`, [`HorizontalTransitionType`](#horizontaltransitiontype) `transitionType`

<a id="horizontaltransitionviennesebend"></a>**`HorizontalTransitionVienneseBend`** extends [`HorizontalSegment`](#horizontalsegment)
  Members: [`geo:Point2D`](_Geometry.md#point2d) `startPoint`, [`AngleValue`](_Core.md#anglevalue) `startAngle`, [`LengthValue`](_Core.md#lengthvalue) `length`, [`CurvatureValue`](_Core.md#curvaturevalue) `startCurvature`, [`CurvatureValue`](_Core.md#curvaturevalue) `endCurvature`, [`LengthValue`](_Core.md#lengthvalue) `centroidalHeight`, [`AngleValue`](_Core.md#anglevalue) `deltaPsi`

<a id="verticalsegment"></a>**`VerticalSegment`**

<a id="verticalline"></a>**`VerticalLine`** extends [`VerticalSegment`](#verticalsegment)
  Members: [`LengthValue`](_Core.md#lengthvalue) `startHeight`, [`LengthValue`](_Core.md#lengthvalue) `endHeight`, [`LengthValue`](_Core.md#lengthvalue) `length`

<a id="verticalparabolicarc"></a>**`VerticalParabolicArc`** extends [`VerticalSegment`](#verticalsegment)
  Members: [`LengthValue`](_Core.md#lengthvalue) `startHeight`, [`LengthValue`](_Core.md#lengthvalue) `endHeight`, [`LengthValue`](_Core.md#lengthvalue) `length`, [`LengthValue`](_Core.md#lengthvalue) `radius`

<a id="verticalcirculararc"></a>**`VerticalCircularArc`** extends [`VerticalSegment`](#verticalsegment)
  Members: [`LengthValue`](_Core.md#lengthvalue) `startHeight`, [`LengthValue`](_Core.md#lengthvalue) `endHeight`, [`LengthValue`](_Core.md#lengthvalue) `length`, [`LengthValue`](_Core.md#lengthvalue) `radius`

<a id="cantsegment"></a>**`CantSegment`**
  Members: [`LengthValue`](_Core.md#lengthvalue) `length`, [`LengthValue`](_Core.md#lengthvalue) `cantStartLeft`, [`LengthValue`](_Core.md#lengthvalue) `cantStartRight`, [`LengthValue`](_Core.md#lengthvalue) `cantEndLeft`, [`LengthValue`](_Core.md#lengthvalue) `cantEndRight`, [`CantType`](#canttype) `cantType`

<a id="crossslopesegment"></a>**`CrossSlopeSegment`**
  Members: [`LengthValue`](_Core.md#lengthvalue) `length`, [`SlopeValue`](_Core.md#slopevalue) `slopeStart`, [`SlopeValue`](_Core.md#slopevalue) `slopeEnd`, [`SlopeSegmentType`](#slopesegmenttype) `slopeType`

<a id="stationingtriple"></a>**`StationingTriple`**
  Members: [`LengthValue`](_Core.md#lengthvalue) `internalStation`, [`LengthValue`](_Core.md#lengthvalue) `incomingStation`, [`LengthValue`](_Core.md#lengthvalue) `outgoingStation`

<a id="stationvalue"></a>**`StationValue`**
: Primitive station coordinate without identity. Used as lightweight value in lists and positioning parameters.
  Members: [`LengthValue`](_Core.md#lengthvalue) `value`, [`StationReference`](#stationreference) `reference`

<a id="nurb2dcontrolpoint"></a>**`Nurb2DControlPoint`**
  Members: [`geo:Point2D`](_Geometry.md#point2d) `position`, [`Real`](_Core.md#real) `weight`

<a id="discretizationrequirement"></a>**`DiscretizationRequirement`**
: Tolerance specification for a particular design stage during discretization. Identity-less value embedded in DiscretizationComponent.
  Members: [`DesignStage`](#designstage) `stage`, [`LengthValue`](_Core.md#lengthvalue) `tolerance`

## Components

| Component | Purpose |
|-----------|---------|
| <a id="alignmentcomponent"></a>`AlignmentComponent` | Marker identifying an Entity as a geometric alignment evaluable along a stationing axis. Carries no data; Systems derive evaluable design stages from the concrete Components present. |
| <a id="stationingcomponent"></a>`StationingComponent` | Enriches a horizontal design stage with an external stationing system for real-world kilometrage, allowing station jumps, overlaps, or gaps. |
| <a id="segmentedhorizontaldesignstagecomponent"></a>`SegmentedHorizontalDesignStageComponent` | Horizontal design stage as ordered sequence of geometric segments. |
| <a id="nurb2dhorizontaldesignstagecomponent"></a>`Nurb2DHorizontalDesignStageComponent` | Horizontal design stage as a NURBS curve in 2D. |
| <a id="segmentedverticaldesignstagecomponent"></a>`SegmentedVerticalDesignStageComponent` | Vertical profile as ordered sequence of vertical segments. |
| <a id="segmentedcantdesignstagecomponent"></a>`SegmentedCantDesignStageComponent` | Cant profile as ordered sequence of cant segments. |
| <a id="crossslopedesignstagecomponent"></a>`CrossSlopeDesignStageComponent` | Cross slope profile as ordered sequence of slope segments. |
| <a id="horizontaldesignstagecomponent"></a>`HorizontalDesignStageComponent` | Marker identifying an Entity as a horizontal design stage. Carries no data; the concrete representation is defined by SegmentedHorizontalDesignStageComponent or Nurb2DHorizontalDesignStageComponent. |
| <a id="verticaldesignstagecomponent"></a>`VerticalDesignStageComponent` | Marker identifying an Entity as a vertical design stage. |
| <a id="cantdesignstagecomponent"></a>`CantDesignStageComponent` | Marker identifying an Entity as a cant (superelevation) design stage. |
| <a id="alignmentsectioncomponent"></a>`AlignmentSectionComponent` | Defines a section from start to end on an alignment provider. The provider can be a pure alignment (layer 2) or a domain object such as a track or route (layer 3) that fulfils AlignmentProviderArchetype. |
| <a id="discretizationcomponent"></a>`DiscretizationComponent` | Parameters and results of discretizing an alignment into a qualified polyline. |
| <a id="stationcomponent"></a>`StationComponent` | Wraps a StationValue with alignment reference for entities that need identity and referenceability. Foreign stationing is expressed by referencing an alignment different from the entity's own. |
| <a id="discontinuitystationcomponent"></a>`DiscontinuityStationComponent` | Additional information for stations at discontinuities (geometry transitions, slope breaks, superelevation shifts). |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="alignmentarchetype"></a>`AlignmentArchetype` | [`pos:AlignmentProviderArchetype`](_Positioning.md#alignmentproviderarchetype) | [`AlignmentComponent`](#alignmentcomponent) |
| <a id="stationingalignmentarchetype"></a>`StationingAlignmentArchetype` | [`AlignmentArchetype`](#alignmentarchetype) | [`StationingComponent`](#stationingcomponent) |
| <a id="horizontaldesignstagearchetype"></a>`HorizontalDesignStageArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`HorizontalDesignStageComponent`](#horizontaldesignstagecomponent) |
| <a id="verticaldesignstagearchetype"></a>`VerticalDesignStageArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`VerticalDesignStageComponent`](#verticaldesignstagecomponent) |
| <a id="cantdesignstagearchetype"></a>`CantDesignStageArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`CantDesignStageComponent`](#cantdesignstagecomponent) |
| <a id="crossslopedesignstagearchetype"></a>`CrossSlopeDesignStageArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`CrossSlopeDesignStageComponent`](#crossslopedesignstagecomponent) |
| <a id="alignmentsectionarchetype"></a>`AlignmentSectionArchetype` | [`NamedArchetype`](_Core.md#namedarchetype) | [`AlignmentSectionComponent`](#alignmentsectioncomponent) |
| <a id="stationarchetype"></a>`StationArchetype` | [`NamedArchetype`](_Core.md#namedarchetype) | [`StationComponent`](#stationcomponent) |
| <a id="discontinuitystationarchetype"></a>`DiscontinuityStationArchetype` | [`StationArchetype`](#stationarchetype) | [`DiscontinuityStationComponent`](#discontinuitystationcomponent) |
| <a id="discretizationarchetype"></a>`DiscretizationArchetype` | [`NamedArchetype`](_Core.md#namedarchetype) | [`DiscretizationComponent`](#discretizationcomponent) |
