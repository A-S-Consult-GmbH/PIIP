# Core

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/Core.yaml`](../../spec/Core.yaml)

Self-referential core ontology: base types, identity, versioning, lifecycle, revision. No external ontology dependencies. Core is explicitly linked by all other ontologies via LinkedOntologies, but its types can be used without a prefix.

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/Core/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## BaseTypes

<a id="uuid"></a>`UUID`, <a id="entity"></a>`Entity`, <a id="versionid"></a>`VersionId`, <a id="uri"></a>`Uri`, <a id="string"></a>`String`, <a id="real"></a>`Real`, <a id="integer"></a>`Integer`, <a id="index"></a>`Index`, <a id="boolean"></a>`Boolean`, <a id="json"></a>`Json`, <a id="optional<>"></a>`Optional<>`, <a id="set<>"></a>`Set<>`, <a id="list<>"></a>`List<>`, <a id="link<>"></a>`Link<>`, <a id="anglevalue"></a>`AngleValue`, <a id="lengthvalue"></a>`LengthValue`, <a id="curvaturevalue"></a>`CurvatureValue`, <a id="slopevalue"></a>`SlopeValue`, <a id="speedvalue"></a>`SpeedValue`

## Components

| Component | Purpose |
|-----------|---------|
| <a id="namecomponent"></a>`NameComponent` | Human-readable name for identification and management. Separated from the Entity itself to allow unnamed technical entities. |
| <a id="versioncomponent"></a>`VersionComponent` | Versioning information enabling reconstruction of version histories as a directed graph. Each new version is a new Entity referencing its predecessor. |
| <a id="lifecycleanchorcomponent"></a>`LifecycleAnchorComponent` | Marker component without data fields. Explicitly marks an Entity as a persistent lifecycle identity anchor. Required under OWA to distinguish anchors from arbitrary named entities. |
| <a id="lifecyclereferencecomponent"></a>`LifecycleReferenceComponent` | Links a versioned Entity to its persistent lifecycle identity anchor (LifecycleAnchorArchetype). The reference is optional to support purely technical or conceptual entities without physical counterpart. |
| <a id="revisionmilestonecomponent"></a>`RevisionMilestoneComponent` | Marker component identifying an Entity as a revision milestone. Carries no data. |
| <a id="revisioncomponent"></a>`RevisionComponent` | Links an Entity to a specific Revision (planning milestone), indicating its status at a given planning phase and establishing contractual responsibility. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="namedarchetype"></a>`NamedArchetype` | — | [`NameComponent`](#namecomponent) |
| <a id="versionedarchetype"></a>`VersionedArchetype` | [`NamedArchetype`](#namedarchetype) | [`VersionComponent`](#versioncomponent) |
| <a id="lifecycleanchorarchetype"></a>`LifecycleAnchorArchetype` | [`NamedArchetype`](#namedarchetype) | [`LifecycleAnchorComponent`](#lifecycleanchorcomponent) |
| <a id="lifecyclearchetype"></a>`LifecycleArchetype` | [`VersionedArchetype`](#versionedarchetype) | [`LifecycleReferenceComponent`](#lifecyclereferencecomponent) |
| <a id="revisionmilestonearchetype"></a>`RevisionMilestoneArchetype` | [`NamedArchetype`](#namedarchetype) | [`RevisionMilestoneComponent`](#revisionmilestonecomponent) |
| <a id="revisionarchetype"></a>`RevisionArchetype` | [`VersionedArchetype`](#versionedarchetype) | [`RevisionComponent`](#revisioncomponent) |
