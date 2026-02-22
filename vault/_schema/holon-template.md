---
id: <unique-id>
type: holon
scale: <molecular | cellular | tissue | organ | system>
parent_holon: <parent-id or null>
children_holons: []
inputs:
  - node: <node-id>
    description: "<input description>"
outputs:
  - node: <node-id>
    description: "<output description>"
internal_nodes: []
internal_edges: []
sources: []
confidence: <0.0-1.0>
---

# <Holon Name>

Description of the holon.

## Functional Summary

How the holon operates.

## Input-Output Behavior (Black Box Abstraction)

Abstract description of inputs, outputs, and transfer function.

## Cross-Holon Interactions

Interactions with other holons.

## Intervention Equivalence

Whether the holon can be collapsed for downstream reasoning.
