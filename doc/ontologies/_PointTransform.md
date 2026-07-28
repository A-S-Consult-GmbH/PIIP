# PointTransform

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/PointTransform.yaml`](../../spec/PointTransform.yaml)

System contract for transforming a single point between two coordinate contexts (Raumbezug). Concrete geodetic algorithmics (PROJ, commercial engines, optional private Geodesy) are runtime detail behind the contract. Whether EPSG/WKT descriptors are required on CRS entities in Data payloads is an InformationNeed concern. Every operation on a started instance addresses that instance via PointTransformSystemHandle. Domain payloads on the wire use Data<Archetype> (full JSON structure), not Link (GUID-only).

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/PointTransform/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |
| [Geometry](_Geometry.md) | `https://w3id.org/piip/Geometry/1` | `geo` |
| [SpatialReference](_SpatialReference.md) | `https://w3id.org/piip/SpatialReference/1` | `sref` |

## ValueTypes

<a id="pointtransformsystemhandle"></a>**`PointTransformSystemHandle`**
: Typed handle of a started PointTransformSystem runtime instance. Part of the public contract: callers of TransformPoint and Shutdown must supply this handle; Start returns it. Addressing and contract identity are separate concerns (endpoint vs. contractUri). No authentication fields in the local scenario.
  Members: [`Uri`](_Core.md#uri) `endpoint`, [`UUID`](_Core.md#uuid) `systemId`, [`Uri`](_Core.md#uri) `contractUri`

<a id="pointtransformresult"></a>**`PointTransformResult`**
: Result of TransformPoint: on success point is set and errorMessage is absent; on failure errorMessage is set and point is absent. No redundant success flag. Heavy provenance is not required for single points.
  Members: [`Optional<geo:Point3D>`](_Geometry.md#point3d) `point`, [`Optional<Real>`](_Core.md#real) `achievedAccuracy`, [`Optional<String>`](_Core.md#string) `errorMessage`

## Systems

### <a id="pointtransformsystem"></a>`PointTransformSystem`

Atomic geodetic point operation between two CoordinateContext values. Lifecycle Start/Shutdown supports local orchestration; TransformPoint is the domain-facing operation. Instance identity is carried by PointTransformSystemHandle on every post-Start operation.

#### `Start`

Start the runtime process and return a PointTransformSystemHandle for subsequent TransformPoint and Shutdown calls.

**Input:** _(none)_

**Output:**

| Type | Name |
|------|------|
| [`PointTransformSystemHandle`](#pointtransformsystemhandle) | `handle` |

#### `TransformPoint`

Transform one point from source to target coordinate context on the runtime instance identified by handle. Contexts are passed as Data (by-value JSON), not as Link (GUID-only). May fail if the point is outside the validity domain or descriptors cannot be resolved.

**Input:**

| Type | Name | Description |
|------|------|-------------|
| [`PointTransformSystemHandle`](#pointtransformsystemhandle) | `handle` | Started PointTransformSystem instance to invoke. |
| [`Data<sref:CoordinateContextArchetype>`](_SpatialReference.md#coordinatecontextarchetype) | `sourceContext` | Full coordinate-context structure (and nested CRS descriptors as needed). |
| [`Data<sref:CoordinateContextArchetype>`](_SpatialReference.md#coordinatecontextarchetype) | `targetContext` |  |
| [`geo:Point3D`](_Geometry.md#point3d) | `point` |  |
| [`Optional<Real>`](_Core.md#real) | `requestedTolerance` | Optional tolerance request; interpretation is runtime-specific. |

**Output:**

| Type | Name |
|------|------|
| [`PointTransformResult`](#pointtransformresult) | `result` |

#### `Shutdown`

Stop the runtime instance identified by the handle.

**Input:**

| Type | Name | Description |
|------|------|-------------|
| [`PointTransformSystemHandle`](#pointtransformsystemhandle) | `handle` |  |

**Output:**

| Type | Name |
|------|------|
| [`Boolean`](_Core.md#boolean) | `success` |
