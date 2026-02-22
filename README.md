# CausalGraph: Dual-Layer Holonic Causal Metagraph

A prototype of a **dual-layer holonic causal metagraph** for biological knowledge. The system uses **markdown files with wikilinks as the authoring/reasoning layer** and a **parsed formal graph as the computation/validation layer**.

**Domain:** HPA (Hypothalamic-Pituitary-Adrenal) Axis and its connections to the immune system (~30 nodes, ~18 causal edges, 6 holons).

## Architecture

```
Markdown Vault (Knowledge Layer)     →    Formal Graph (Computation Layer)
├── nodes/*.md       (entities)            NetworkX DiGraph
├── mechanisms/*.md  (causal edges)        d-separation, backdoor criterion
├── holons/*.md      (abstractions)        holon validation, modularity
└── [[wikilinks]]    (navigation)          target discovery, intervention sim
```

## Quick Start

```bash
pip install -r requirements.txt

# Build the graph from markdown vault
python scripts/build_graph.py --vault ./vault --output ./outputs

# Run causal queries
python scripts/query_graph.py --intervention cortisol increase
python scripts/query_graph.py --d-sep cortisol il-6 --given stress-signal
python scripts/query_graph.py --paths stress-signal il-6 --max-length 5
python scripts/query_graph.py --backdoor cortisol nf-kb

# Validate vault structural integrity
python scripts/validate_vault.py --vault ./vault --output ./outputs/validation_report.md

# Discover drug targets for a disease phenotype
python scripts/discover_targets.py \
  --phenotype '{"nf-kb": "elevated", "il-6": "elevated", "gr": "desensitized"}' \
  --output ./outputs/target_report.md

# Run tests
pytest tests/ -v
```

## Project Structure

```
vault/                  # Markdown knowledge graph
├── nodes/              # 30 entity files (molecules, receptors, cell types)
├── mechanisms/         # 18 causal edge files (directed relationships)
├── holons/             # 6 holon files (multi-scale abstractions)
├── _schema/            # Frontmatter schema templates
├── _moc-*.md           # Maps of Contents
└── _index.md           # Entry point

engine/                 # Computation layer
├── parser.py           # Vault → NetworkX graph
├── graph_core.py       # Path finding, subgraph extraction
├── causal_engine.py    # d-separation, backdoor criterion, intervention simulation
├── holon_engine.py     # Holon validation, modularity, abstraction checking
├── target_discovery.py # Drug target identification from disease phenotypes
├── visualizer.py       # Interactive HTML graph visualizations (pyvis)
└── validator.py        # Structural integrity checks

tests/                  # 71 tests
├── test_parser.py
├── test_causal_engine.py
├── test_holon_consistency.py
├── test_target_discovery.py
└── test_llm_reasoning.py

scripts/                # CLI tools
├── build_graph.py
├── query_graph.py
├── validate_vault.py
└── discover_targets.py
```

## What This Proves

1. **Markdown as knowledge graph**: The vault is human-readable, git-versionable, and parseable into a formal graph
2. **Wikilinks encode graph structure**: The parsed graph matches expected biological network topology
3. **LLMs can navigate it**: Navigation tests prove wikilink-following gathers sufficient context for causal reasoning
4. **Formal causal inference works**: d-separation, backdoor criterion, and identifiability on the parsed graph
5. **Holonic abstraction is valid**: Multi-scale reasoning through validated holon boundaries
6. **Target discovery is actionable**: Biologically plausible drug targets from disease phenotypes
7. **Dual-layer architecture is sound**: Markdown for authoring + formal graph for computation

## Tech Stack

- Python 3.11+, NetworkX, pyvis, python-frontmatter, pytest, click
