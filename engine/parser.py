"""Vault parser: reads markdown vault and produces a formal NetworkX DiGraph.

Parses YAML frontmatter, extracts wikilinks, builds node/edge/holon structures,
and validates structural integrity on parse.
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import frontmatter
import networkx as nx


WIKILINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")

# Required frontmatter fields by file category
REQUIRED_NODE_FIELDS = {"id", "type", "scale"}
REQUIRED_MECHANISM_FIELDS = {"id", "source", "target", "relationship", "direction"}
REQUIRED_HOLON_FIELDS = {"id", "type", "scale", "internal_nodes", "internal_edges"}


def parse_vault(vault_path: str) -> dict[str, Any]:
    """Parse the entire vault directory into a structured graph representation.

    Args:
        vault_path: Path to the vault directory.

    Returns:
        Dictionary containing the NetworkX graph, holon hierarchy, metadata,
        and validation issues found during parsing.
    """
    vault_path = Path(vault_path)
    if not vault_path.is_dir():
        raise FileNotFoundError(f"Vault directory not found: {vault_path}")

    # Collect all markdown files
    md_files = list(vault_path.rglob("*.md"))

    # Parse all files
    parsed_files: dict[str, dict] = {}
    parse_errors: list[str] = []

    for md_file in md_files:
        try:
            parsed = _parse_md_file(md_file, vault_path)
            if parsed:
                parsed_files[parsed["id"]] = parsed
        except Exception as e:
            parse_errors.append(f"Error parsing {md_file}: {e}")

    # Categorize files
    nodes: dict[str, dict] = {}
    mechanisms: dict[str, dict] = {}
    holons: dict[str, dict] = {}
    other_files: dict[str, dict] = {}

    for file_id, data in parsed_files.items():
        rel_path = data.get("_rel_path", "")
        fm_type = data.get("frontmatter", {}).get("type", "")

        if "mechanisms/" in rel_path:
            mechanisms[file_id] = data
        elif "holons/" in rel_path:
            holons[file_id] = data
        elif "nodes/" in rel_path:
            nodes[file_id] = data
        elif fm_type == "holon":
            holons[file_id] = data
        elif fm_type in ("index", "moc"):
            other_files[file_id] = data
        elif "source" in data.get("frontmatter", {}) and "target" in data.get("frontmatter", {}):
            mechanisms[file_id] = data
        else:
            # Could be a node or other file
            if "_schema/" not in rel_path and file_id not in ("_index",):
                nodes[file_id] = data
            else:
                other_files[file_id] = data

    # Build the NetworkX graph
    graph = nx.DiGraph()
    dangling_links: list[str] = []
    all_known_ids = set(parsed_files.keys())

    # Add nodes to graph
    for node_id, data in nodes.items():
        fm = data.get("frontmatter", {})
        graph.add_node(
            node_id,
            type=fm.get("type", "unknown"),
            scale=fm.get("scale", "unknown"),
            aliases=fm.get("aliases", []),
            holon_membership=fm.get("holon_membership", []),
            confidence=fm.get("confidence", 0.5),
            sources=fm.get("sources", []),
            tags=fm.get("tags", []),
            file_path=data.get("_rel_path", ""),
            category="node",
        )

    # Add mechanism edges (causal edges)
    causal_edges: list[dict] = []
    for mech_id, data in mechanisms.items():
        fm = data.get("frontmatter", {})
        source = fm.get("source", "")
        target = fm.get("target", "")

        # Ensure source and target nodes exist in graph
        if source and source not in graph:
            graph.add_node(source, type="unknown", scale="unknown", category="node",
                           file_path="", aliases=[], holon_membership=[],
                           confidence=0.5, sources=[], tags=[])
        if target and target not in graph:
            graph.add_node(target, type="unknown", scale="unknown", category="node",
                           file_path="", aliases=[], holon_membership=[],
                           confidence=0.5, sources=[], tags=[])

        if source and target:
            edge_attrs = {
                "id": mech_id,
                "relationship": fm.get("relationship", "unknown"),
                "direction": fm.get("direction", "unknown"),
                "mechanism_type": fm.get("mechanism_type", "unknown"),
                "evidence_type": fm.get("evidence_type", "unknown"),
                "evidence_strength": fm.get("evidence_strength", "unknown"),
                "temporal_lag": fm.get("temporal_lag", "unknown"),
                "reversible": fm.get("reversible", True),
                "context": fm.get("context", ""),
                "confidence": fm.get("confidence", 0.5),
                "holon_context": fm.get("holon_context", []),
                "mechanism_file": data.get("_rel_path", ""),
                "edge_type": "causal",
            }
            graph.add_edge(source, target, **edge_attrs)
            causal_edges.append({
                "source": source,
                "target": target,
                **{k: v for k, v in edge_attrs.items() if k != "edge_type"},
            })

    # Extract wikilinks and create reference edges
    reference_edges: list[tuple[str, str]] = []
    for file_id, data in parsed_files.items():
        wikilinks = data.get("wikilinks", [])
        for link_target in wikilinks:
            if link_target not in all_known_ids:
                dangling_links.append(f"{file_id} -> [[{link_target}]]")
            elif file_id in graph and link_target in graph:
                if not graph.has_edge(file_id, link_target):
                    # Only add reference edge if no causal edge exists
                    reference_edges.append((file_id, link_target))

    # Build holon hierarchy
    holon_hierarchy = _build_holon_hierarchy(holons)

    # Find orphan nodes (nodes with no causal edges)
    orphan_nodes = []
    for node_id in nodes:
        if node_id in graph:
            in_deg = sum(1 for _, _, d in graph.in_edges(node_id, data=True)
                         if d.get("edge_type") == "causal")
            out_deg = sum(1 for _, _, d in graph.out_edges(node_id, data=True)
                         if d.get("edge_type") == "causal")
            if in_deg == 0 and out_deg == 0:
                orphan_nodes.append(node_id)

    # Build metadata
    metadata = {
        "parsed_at": datetime.now(timezone.utc).isoformat(),
        "total_nodes": graph.number_of_nodes(),
        "total_causal_edges": len(causal_edges),
        "total_reference_edges": len(reference_edges),
        "total_holons": len(holons),
        "dangling_links": dangling_links,
        "orphan_nodes": orphan_nodes,
        "parse_errors": parse_errors,
    }

    return {
        "graph": graph,
        "metadata": metadata,
        "nodes": [_node_to_dict(graph, n) for n in graph.nodes()],
        "causal_edges": causal_edges,
        "reference_edges": reference_edges,
        "holon_hierarchy": holon_hierarchy,
        "parsed_files": parsed_files,
        "holons_raw": holons,
        "mechanisms_raw": mechanisms,
        "nodes_raw": nodes,
    }


def _parse_md_file(file_path: Path, vault_root: Path) -> dict | None:
    """Parse a single markdown file, extracting frontmatter and wikilinks.

    Args:
        file_path: Absolute path to the markdown file.
        vault_root: Root path of the vault directory.

    Returns:
        Dictionary with parsed data, or None if the file should be skipped.
    """
    try:
        post = frontmatter.load(str(file_path))
    except Exception:
        # Try reading as plain text if frontmatter parsing fails
        text = file_path.read_text(encoding="utf-8")
        post = frontmatter.Post(text)

    fm = dict(post.metadata) if post.metadata else {}
    content = post.content or ""

    # Extract wikilinks from content
    wikilinks = WIKILINK_PATTERN.findall(content)
    # Normalize wikilink targets to lowercase kebab-case IDs
    wikilinks = [_normalize_id(wl) for wl in wikilinks]

    # Determine the file ID
    file_id = fm.get("id", file_path.stem)

    rel_path = str(file_path.relative_to(vault_root))

    return {
        "id": file_id,
        "frontmatter": fm,
        "content": content,
        "wikilinks": wikilinks,
        "_file_path": str(file_path),
        "_rel_path": rel_path,
    }


def _normalize_id(raw: str) -> str:
    """Normalize a wikilink target to a consistent ID format.

    Converts to lowercase and replaces spaces with hyphens.
    Handles display text after pipe characters.
    """
    # Handle pipe syntax [[id|display text]]
    if "|" in raw:
        raw = raw.split("|")[0]
    return raw.strip().lower().replace(" ", "-")


def _build_holon_hierarchy(holons: dict[str, dict]) -> dict[str, dict]:
    """Build the holon hierarchy from parsed holon files.

    Args:
        holons: Dictionary of parsed holon file data.

    Returns:
        Dictionary mapping holon IDs to their hierarchy information.
    """
    hierarchy = {}
    for holon_id, data in holons.items():
        fm = data.get("frontmatter", {})
        inputs = fm.get("inputs", [])
        outputs = fm.get("outputs", [])

        hierarchy[holon_id] = {
            "parent": fm.get("parent_holon"),
            "children": fm.get("children_holons", []),
            "inputs": [inp["node"] if isinstance(inp, dict) else inp for inp in inputs],
            "outputs": [out["node"] if isinstance(out, dict) else out for out in outputs],
            "internal_nodes": fm.get("internal_nodes", []),
            "internal_edges": fm.get("internal_edges", []),
            "scale": fm.get("scale", "unknown"),
            "confidence": fm.get("confidence", 0.5),
        }
    return hierarchy


def _node_to_dict(graph: nx.DiGraph, node_id: str) -> dict:
    """Convert a graph node to a serializable dictionary.

    Args:
        graph: The NetworkX graph.
        node_id: ID of the node.

    Returns:
        Dictionary representation of the node.
    """
    attrs = dict(graph.nodes[node_id])
    return {
        "id": node_id,
        "type": attrs.get("type", "unknown"),
        "scale": attrs.get("scale", "unknown"),
        "holon_membership": attrs.get("holon_membership", []),
        "confidence": attrs.get("confidence", 0.5),
        "file_path": attrs.get("file_path", ""),
    }


def export_graph_json(parsed_data: dict, output_path: str) -> None:
    """Export the parsed graph to a JSON file.

    Args:
        parsed_data: Output from parse_vault().
        output_path: Path to write the JSON file.
    """
    output = {
        "metadata": parsed_data["metadata"],
        "nodes": parsed_data["nodes"],
        "causal_edges": parsed_data["causal_edges"],
        "holon_hierarchy": parsed_data["holon_hierarchy"],
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)


def get_causal_subgraph(graph: nx.DiGraph) -> nx.DiGraph:
    """Extract only causal edges from the full graph.

    Args:
        graph: The full graph with both causal and reference edges.

    Returns:
        A new DiGraph containing only causal edges.
    """
    causal_graph = nx.DiGraph()

    # Copy all nodes
    for node, attrs in graph.nodes(data=True):
        causal_graph.add_node(node, **attrs)

    # Copy only causal edges
    for u, v, attrs in graph.edges(data=True):
        if attrs.get("edge_type") == "causal":
            causal_graph.add_edge(u, v, **attrs)

    # Remove isolated nodes (no causal edges at all)
    # Actually, keep all nodes - some may be referenced but not have causal edges yet
    return causal_graph
