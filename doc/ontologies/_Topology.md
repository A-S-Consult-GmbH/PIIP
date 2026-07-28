# Topology

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/Topology.yaml`](../../spec/Topology.yaml)

Domain-agnostic topology ontology: directed graphs with nodes, edges, and recursive macro-abstraction. No alignment or geometry dependencies.

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/Topology/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |

## Enums

<a id="edgedirection"></a>**`EdgeDirection`**
: Defines the direction of an edge.
  Values: `Forward`, `Backward`, `Both`

## Components

| Component | Purpose |
|-----------|---------|
| <a id="nodecomponent"></a>`NodeComponent` | Marks an Entity as a topological node. Pure marker without data fields. |
| <a id="edgecomponent"></a>`EdgeComponent` | Topological edge connecting two nodes in a directed graph. |
| <a id="topologycomponent"></a>`TopologyComponent` | Aggregation of nodes and edges forming a topological network. |
| <a id="macronodecomponent"></a>`MacroNodeComponent` | Aggregated node grouping inner and outer topological elements of a finer topology. Enables recursive abstraction across topological levels. |
| <a id="macroedgecomponent"></a>`MacroEdgeComponent` | Aggregated edge grouping inner topological elements of a finer topology. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="nodearchetype"></a>`NodeArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`NodeComponent`](#nodecomponent) |
| <a id="edgearchetype"></a>`EdgeArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`EdgeComponent`](#edgecomponent) |
| <a id="topologyarchetype"></a>`TopologyArchetype` | [`LifecycleArchetype`](_Core.md#lifecyclearchetype) | [`TopologyComponent`](#topologycomponent) |
| <a id="macronodearchetype"></a>`MacroNodeArchetype` | [`NodeArchetype`](#nodearchetype) | [`MacroNodeComponent`](#macronodecomponent) |
| <a id="macroedgearchetype"></a>`MacroEdgeArchetype` | [`EdgeArchetype`](#edgearchetype) | [`MacroEdgeComponent`](#macroedgecomponent) |
