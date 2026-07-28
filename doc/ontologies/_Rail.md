# Rail

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/Rail.yaml`](../../spec/Rail.yaml)

Railway domain objects: track alignment composition, route stationing, speed profiles, operational switches. Links Core, Positioning, Alignment, TrackAlignmentConnection. TrackAlignmentConnection defines geometric line connections (alignment layer); Rail adds physical and operational properties (rail profile, frog movability, speed, network membership). Naming convention: TrackAlignment = spatial alignment composition (Frenet curve); TrackSpeed = operational concern; RailTrack / RailRoute / RailSwitch = comprehensive domain objects. Architecture: Each layer is a separate Entity with independent versioning. AlignmentConsumerComponent (from Positioning) links domain objects to their alignment. Additional representations (IST, survey) modelled as optional Components.

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/Rail/1` |
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
| [TrackAlignmentConnection](_TrackAlignmentConnection.md) | `https://w3id.org/piip/TrackAlignmentConnection/1` | `tc` |

## Enums

<a id="frogmovability"></a>**`FrogMovability`**
: Movability type of a frog (common crossing) in a railway switch.
  Values: `Fixed`, `SemiMovable`, `Articulated`

## ValueTypes

<a id="permissiblespeedsegment"></a>**`PermissibleSpeedSegment`**
  Members: [`align:StationValue`](_Alignment.md#stationvalue) `startStation`, [`align:StationValue`](_Alignment.md#stationvalue) `endStation`, [`SpeedValue`](_Core.md#speedvalue) `maxSpeed`, [`String`](_Core.md#string) `reason`

<a id="permissiblespeedregister"></a>**`PermissibleSpeedRegister`**
  Members: [`Set<PermissibleSpeedSegment>`](#permissiblespeedsegment) `segments`, [`Boolean`](_Core.md#boolean) `direction`, [`SpeedValue`](_Core.md#speedvalue) `maxSpeed`, [`Link<PermissibleSpeedSettingArchetype>`](#permissiblespeedsettingarchetype) `setting`

## Components

| Component | Purpose |
|-----------|---------|
| <a id="trackalignmentcomponent"></a>`TrackAlignmentComponent` | Aggregates horizontal, vertical and cant design stages into a complete spatial track alignment (Frenet curve). Optionally references a StationingAlignmentArchetype for kilometrage (Fremdstationierung). |
| <a id="trackspeedcomponent"></a>`TrackSpeedComponent` | Permissible speed profiles for a railway track, per direction and train type. |
| <a id="railroutecomponent"></a>`RailRouteComponent` | Associates a railway route with its tracks. |
| <a id="railswitchcomponent"></a>`RailSwitchComponent` | Operational railway switch or crossing (domain layer). References its geometric definition (alignment layer) via Link<T>. Physical properties (rail profile, frog movability) belong here, not on the geometric level. Serves as MacroNode carrier in meso-topology. |
| <a id="railnetworkcomponent"></a>`RailNetworkComponent` | Collection of railway tracks, routes and switches forming a network. |
| <a id="permissiblespeedsettingcomponent"></a>`PermissibleSpeedSettingComponent` | Configuration of a permissible speed setting. |
| <a id="railprofilecomponent"></a>`RailProfileComponent` | Rail profile type (e.g. "60", "49"). |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="trackalignmentarchetype"></a>`TrackAlignmentArchetype` | [`align:AlignmentArchetype`](_Alignment.md#alignmentarchetype) | [`TrackAlignmentComponent`](#trackalignmentcomponent) |
| <a id="railtrackarchetype"></a>`RailTrackArchetype` | [`pos:AlignmentConsumerArchetype`](_Positioning.md#alignmentconsumerarchetype), [`pos:AlignmentProviderArchetype`](_Positioning.md#alignmentproviderarchetype) | [`TrackSpeedComponent`](#trackspeedcomponent) |
| <a id="railroutearchetype"></a>`RailRouteArchetype` | [`pos:AlignmentConsumerArchetype`](_Positioning.md#alignmentconsumerarchetype), [`pos:AlignmentProviderArchetype`](_Positioning.md#alignmentproviderarchetype) | [`RailRouteComponent`](#railroutecomponent) |
| <a id="railnetworkarchetype"></a>`RailNetworkArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`RailNetworkComponent`](#railnetworkcomponent) |
| <a id="railswitcharchetype"></a>`RailSwitchArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`RailSwitchComponent`](#railswitchcomponent) |
| <a id="permissiblespeedsettingarchetype"></a>`PermissibleSpeedSettingArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`PermissibleSpeedSettingComponent`](#permissiblespeedsettingcomponent) |
| <a id="railprofilearchetype"></a>`RailProfileArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`RailProfileComponent`](#railprofilecomponent) |
