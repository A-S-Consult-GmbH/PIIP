# SpatialReference

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/SpatialReference.yaml`](../../spec/SpatialReference.yaml)

Minimal spatial reference contract for linear infrastructure: shared coordinate contexts (Raumbezug), horizontal and vertical CRS markers with optional EPSG and/or WKT descriptors, and georeferencing attachment of domain geometry. Does not model ellipsoid, datum, projection, or transformation parameter sets; those belong to an optional extended Geodesy ontology or to runtime implementations. Descriptor components are optional (Open World). Systems may impose LOIN requiring EPSG and/or WKT; fixed register identities for coordinate contexts may omit both descriptors. Alignment and other domain ontologies must not hard-link this ontology; georeferencing is attached by runtime composition (GeoreferencedComponent on the domain entity).

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/SpatialReference/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |

## BaseTypes

<a id="epochvalue"></a>`EpochValue`

## Components

| Component | Purpose |
|-----------|---------|
| <a id="epsgcodecomponent"></a>`EpsgCodeComponent` | EPSG registry entry identifying a CRS or other geodetic object. Optional descriptor on a CRS entity. See: https://epsg.org/, https://proj.org/ |
| <a id="wktcomponent"></a>`WktComponent` | Well-Known Text CRS definition (ISO 19162). Optional descriptor for CRS without EPSG entry (e.g., local projection systems) or parallel to EPSG. |
| <a id="crscomponent"></a>`CrsComponent` | Marker: Entity acts as a horizontal or 3D coordinate reference system under the minimal spatial reference contract. No geodetic decomposition in this ontology. |
| <a id="verticalcrscomponent"></a>`VerticalCrsComponent` | Marker: Entity acts as a vertical coordinate reference system (height). No vertical datum or geoid members at contract level. |
| <a id="coordinatecontextcomponent"></a>`CoordinateContextComponent` | Shared, versionable raumbezug bundle: horizontal CRS, optional vertical CRS, optional epoch. Multiple georeferenced entities reference the same context entity to avoid redundant specification and to version the spatial reference independently of geometry. |
| <a id="georeferencedcomponent"></a>`GeoreferencedComponent` | Associates a domain entity with a coordinate context (Raumbezug) for spatial interpretation. Composition only: does not pull alignment or geodetic depth into the entity type. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="epsgcodearchetype"></a>`EpsgCodeArchetype` | [`NamedArchetype`](_Core.md#namedarchetype) | [`EpsgCodeComponent`](#epsgcodecomponent) |
| <a id="wktarchetype"></a>`WktArchetype` | [`NamedArchetype`](_Core.md#namedarchetype) | [`WktComponent`](#wktcomponent) |
| <a id="coordinatereferencesystemarchetype"></a>`CoordinateReferenceSystemArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`CrsComponent`](#crscomponent) |
| <a id="verticalcoordinatereferencesystemarchetype"></a>`VerticalCoordinateReferenceSystemArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`VerticalCrsComponent`](#verticalcrscomponent) |
| <a id="coordinatecontextarchetype"></a>`CoordinateContextArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`CoordinateContextComponent`](#coordinatecontextcomponent) |
| <a id="georeferencedarchetype"></a>`GeoreferencedArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`GeoreferencedComponent`](#georeferencedcomponent) |
