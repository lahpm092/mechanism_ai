---
type: index
last_updated: 2026-02-22
total_nodes: 30
total_mechanisms: 18
total_holons: 6
---

# CausalGraph: Biological Causal Metagraph

This vault contains a holonic causal graph of human biology, focused on the neuroendocrine-immune interface. Each file is a node, edge, or holon in the graph. Navigate by following [[wikilinks]].

## System-Level Holons (Entry Points)

- [[hpa-axis]] — The hypothalamic-pituitary-adrenal stress response axis
- [[innate-immune-response]] — NF-κB-driven inflammatory signaling and its regulation

## Sub-Holons

- [[hypothalamus-crh-circuit]] — CRH/AVP production and regulation
- [[pituitary-acth-release]] — ACTH synthesis and secretion
- [[adrenal-cortex-steroidogenesis]] — Cortisol synthesis from ACTH signal
- [[glucocorticoid-feedback]] — GR-mediated negative feedback loop

## Maps of Contents

- [[_moc-neuroendocrine]] — All neuroendocrine nodes and mechanisms
- [[_moc-immune]] — All immune nodes and mechanisms
- [[_moc-metabolic]] — Metabolic connections (future expansion)

## Key Bridge Mechanisms

These mechanisms connect different holons and are critical for cross-system reasoning:

- [[cortisol-suppresses-nfkb]] — HPA → Immune suppression (primary bridge)
- [[il6-stimulates-crh]] — Immune → HPA activation
- [[il1beta-stimulates-crh]] — Immune → HPA activation
- [[tnfalpha-stimulates-hpa]] — Immune → HPA activation
- [[cortisol-shifts-th1-to-th2]] — HPA → Adaptive immune modulation

## How to Navigate This Graph

**For LLM agents**: Start here. Read this index to understand the landscape. Follow the holon links to understand system-level organization. Drill into specific nodes and mechanisms only when needed for a specific query. The wikilinks in prose sections tell you WHEN and WHY to follow them.

**For the parser**: Extract all [[wikilinks]] from all files. The frontmatter contains machine-readable metadata. The `source` and `target` fields in mechanism files define directed edges.
