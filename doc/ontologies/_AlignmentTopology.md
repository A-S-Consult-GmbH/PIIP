# AlignmentTopology

> **Note**: This file is auto-generated. Do not edit manually.

**Source**: [`spec/AlignmentTopology.yaml`](../../spec/AlignmentTopology.yaml)

Alignment-specific topology: links the domain-agnostic Topology ontology with the Alignment ontology by providing Components and Archetypes for alignment-referenced nodes and edges (micro-topology).

## Meta

| Key | Value |
|-----|-------|
| URI | `https://w3id.org/piip/AlignmentTopology/1` |
| Organization | A+S Consult GmbH FuE |
| OrganizationUri | `https://apluss.de/a+s_consult` |
| Version | `1.0.0` |
| Creators | Jens Bartnitzek |

## Linked Ontologies

| Ontology | URI | Prefix |
|----------|-----|--------|
| [Core](_Core.md) | `https://w3id.org/piip/Core/1` | `—` |
| [Topology](_Topology.md) | `https://w3id.org/piip/Topology/1` | `topo` |
| [Alignment](_Alignment.md) | `https://w3id.org/piip/Alignment/1` | `align` |

## Components

| Component | Purpose |
|-----------|---------|
| <a id="alignmentnodecomponent"></a>`AlignmentNodeComponent` | Extends a topological node with a reference to a specific station on an alignment. Used in micro-topologies to link the graph structure to the geometric alignment. The alignment is derivable from relatedStation.StationComponent.alignment. |
| <a id="alignmentedgecomponent"></a>`AlignmentEdgeComponent` | Extends a topological edge with a reference to an alignment section and a direction flag. Used in micro-topologies to link the graph structure to the geometric alignment. |

## Archetypes

| Archetype | Includes | Own Components |
|-----------|----------|----------------|
| <a id="alignmentnodearchetype"></a>`AlignmentNodeArchetype` | [`topo:NodeArchetype`](_Topology.md#nodearchetype) | [`AlignmentNodeComponent`](#alignmentnodecomponent) |
| <a id="alignmentedgearchetype"></a>`AlignmentEdgeArchetype` | [`topo:EdgeArchetype`](_Topology.md#edgearchetype) | [`AlignmentEdgeComponent`](#alignmentedgecomponent) |
