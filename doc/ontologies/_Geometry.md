# Geometry

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/Geometry.yaml`](../../spec/Geometry.yaml)

Geometric primitives, value types, base material and mesh geometry.

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/Geometry/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |

## Enums

<a id="affinetransformationorder"></a>**`AffineTransformationOrder`**
  Values: `ScaleRotateTranslate`, `ScaleTranslateRotate`, `RotateScaleTranslate`, `RotateTranslateScale`, `TranslateScaleRotate`, `TranslateRotateScale`

<a id="boundingboxstate"></a>**`BoundingBoxState`**
  Values: `Empty`, `Default`, `Infinit`

## ValueTypes

<a id="point2d"></a>**`Point2D`**
  Members: [`Real`](_Core.md#real) `x`, [`Real`](_Core.md#real) `y`

<a id="point3d"></a>**`Point3D`**
  Members: [`Real`](_Core.md#real) `x`, [`Real`](_Core.md#real) `y`, [`Real`](_Core.md#real) `z`

<a id="vector2d"></a>**`Vector2D`**
  Members: [`Real`](_Core.md#real) `x`, [`Real`](_Core.md#real) `y`

<a id="vector3d"></a>**`Vector3D`**
  Members: [`Real`](_Core.md#real) `x`, [`Real`](_Core.md#real) `y`, [`Real`](_Core.md#real) `z`

<a id="color4"></a>**`Color4`**
  Members: [`Real`](_Core.md#real) `red`, [`Real`](_Core.md#real) `green`, [`Real`](_Core.md#real) `blue`, [`Real`](_Core.md#real) `alpha`

<a id="axisalignedboundingbox2d"></a>**`AxisAlignedBoundingBox2D`**
  Members: [`Real`](_Core.md#real) `xmin`, [`Real`](_Core.md#real) `xmax`, [`Real`](_Core.md#real) `ymin`, [`Real`](_Core.md#real) `ymax`, [`BoundingBoxState`](#boundingboxstate) `state`

<a id="affinetransformation3d"></a>**`AffineTransformation3D`**
  Members: [`Optional<AffineTransformationOrder>`](#affinetransformationorder) `order`, [`Optional<Real>`](_Core.md#real) `translateX`, [`Optional<Real>`](_Core.md#real) `translateY`, [`Optional<Real>`](_Core.md#real) `translateZ`, [`Optional<Real>`](_Core.md#real) `scaleX`, [`Optional<Real>`](_Core.md#real) `scaleY`, [`Optional<Real>`](_Core.md#real) `scaleZ`, [`Optional<Real>`](_Core.md#real) `rotateX`, [`Optional<Real>`](_Core.md#real) `rotateY`, [`Optional<Real>`](_Core.md#real) `rotateZ`

## Components

| Component | Purpose |
|-----------|---------|
| <a id="geometrymaterialcomponent"></a>`GeometryMaterialComponent` | Material definition for 3D geometry rendering. Versioned as a standalone Entity to enable reuse across meshes. More complex materials including textures should be added in a material ontology. |
| <a id="meshsegmentcomponent"></a>`MeshSegmentComponent` | Segment within a mesh geometry, associating a part of the mesh with a material and triangle range. |
| <a id="meshgeometrycomponent"></a>`MeshGeometryComponent` | Full 3D mesh geometry with vertices, normals, UVs and indexed segments. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="geometrymaterialarchetype"></a>`GeometryMaterialArchetype` | [`VersionedArchetype`](_Core.md#versionedarchetype) | [`GeometryMaterialComponent`](#geometrymaterialcomponent) |
| <a id="meshgeometry3dsegmentarchetype"></a>`MeshGeometry3DSegmentArchetype` | [`VersionedArchetype`](_Core.md#versionedarchetype) | [`MeshSegmentComponent`](#meshsegmentcomponent) |
| <a id="meshgeometry3darchetype"></a>`MeshGeometry3DArchetype` | [`VersionedArchetype`](_Core.md#versionedarchetype) | [`MeshGeometryComponent`](#meshgeometrycomponent) |
