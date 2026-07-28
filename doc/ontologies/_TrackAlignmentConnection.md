# TrackAlignmentConnection

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/TrackAlignmentConnection.yaml`](../../spec/TrackAlignmentConnection.yaml)

Geometric track connections: switches and crossings as alignment-section-based line geometry (alignment layer). Defines connection patterns and geometric type parameters. Physical properties (rail profile, frog movability) belong to the domain layer (Rail). Links Core, Alignment (AlignmentSectionArchetype).

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/TrackAlignmentConnection/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |
| [Alignment](_Alignment.md) | `https://w3id.org/piip/Alignment/1` | `align` |

## Enums

<a id="switchtype"></a>**`SwitchType`**
: Type of switch - EW, IBW, ABW, EKW, DKW, etc.
  Values: `SimpleSwitch`, `OutsideCurvedSwitch`, `InsideCurvedSwitch`, `SingleSlipSwitch`, `DoubleSlipSwitch`, `Other`

## Components

| Component | Purpose |
|-----------|---------|
| <a id="switchtypespecificationcomponent"></a>`SwitchTypeSpecificationComponent` | Geometric type parameters of a railway switch. Describes the connection pattern (type, curvature, inclination) without physical properties (rail profile, frog movability). Physical properties belong to the domain layer. |
| <a id="crossingtypespecificationcomponent"></a>`CrossingTypeSpecificationComponent` | Geometric type parameters of a railway crossing (fixed frog). Describes crossing angle without physical properties. |
| <a id="trackalignmentconnectioncomponent"></a>`TrackAlignmentConnectionComponent` | Marks an Entity as a geometric track alignment connection element (switch, crossing, etc.). Marker for alignment-layer connection geometry. |
| <a id="geometricswitchcomponent"></a>`GeometricSwitchComponent` | Geometric definition of a simple switch connecting a main track to a diverging track via alignment sections. alignment layer. |
| <a id="geometricdoubleswitchcomponent"></a>`GeometricDoubleSwitchComponent` | Geometric definition of a double switch connecting a main track to two diverging tracks via alignment sections. alignment layer. |
| <a id="geometriccrossingcomponent"></a>`GeometricCrossingComponent` | Geometric definition of a railway crossing (fixed frog) connecting two tracks via alignment sections. alignment layer. |
| <a id="geometricdoubleslipswitchcomponent"></a>`GeometricDoubleSlipSwitchComponent` | Geometric definition of a double slip switch (DKW) with four alignment sections. Two direct tracks follow the existing rail alignments through the crossing; two diverging tracks define the switch connections as auxiliary alignments between the rails. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="switchtypespecificationarchetype"></a>`SwitchTypeSpecificationArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`SwitchTypeSpecificationComponent`](#switchtypespecificationcomponent) |
| <a id="crossingtypespecificationarchetype"></a>`CrossingTypeSpecificationArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`CrossingTypeSpecificationComponent`](#crossingtypespecificationcomponent) |
| <a id="trackalignmentconnectionarchetype"></a>`TrackAlignmentConnectionArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`TrackAlignmentConnectionComponent`](#trackalignmentconnectioncomponent) |
| <a id="geometricswitcharchetype"></a>`GeometricSwitchArchetype` | [`TrackAlignmentConnectionArchetype`](#trackalignmentconnectionarchetype) | [`GeometricSwitchComponent`](#geometricswitchcomponent) |
| <a id="geometricdoubleswitcharchetype"></a>`GeometricDoubleSwitchArchetype` | [`TrackAlignmentConnectionArchetype`](#trackalignmentconnectionarchetype) | [`GeometricDoubleSwitchComponent`](#geometricdoubleswitchcomponent) |
| <a id="geometriccrossingarchetype"></a>`GeometricCrossingArchetype` | [`TrackAlignmentConnectionArchetype`](#trackalignmentconnectionarchetype) | [`GeometricCrossingComponent`](#geometriccrossingcomponent) |
| <a id="geometricdoubleslipswitcharchetype"></a>`GeometricDoubleSlipSwitchArchetype` | [`TrackAlignmentConnectionArchetype`](#trackalignmentconnectionarchetype) | [`GeometricDoubleSlipSwitchComponent`](#geometricdoubleslipswitchcomponent) |
