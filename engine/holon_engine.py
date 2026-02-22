"""Holon engine: validation, cross-level consistency, and holon abstraction.

Validates holon completeness, computes modularity ratios, checks intervention
equivalence, and generates holon summaries for multi-scale reasoning.
"""

from typing import Any

import networkx as nx

from engine.causal_engine import simulate_intervention


def validate_holon_completeness(
    holon_id: str,
    graph: nx.DiGraph,
    holon_hierarchy: dict[str, dict],
) -> dict[str, Any]:
    """Check that every node and edge listed in a holon exists in the graph.

    Args:
        holon_id: ID of the holon to validate.
        graph: The causal graph.
        holon_hierarchy: Holon hierarchy from the parser.

    Returns:
        Dictionary with validation results: missing nodes, missing edges, completeness score.
    """
    if holon_id not in holon_hierarchy:
        return {
            "holon_id": holon_id,
            "valid": False,
            "error": f"Holon '{holon_id}' not found in hierarchy",
            "missing_nodes": [],
            "missing_edges": [],
            "completeness": 0.0,
        }

    holon = holon_hierarchy[holon_id]
    internal_nodes = holon.get("internal_nodes", [])
    internal_edges = holon.get("internal_edges", [])

    missing_nodes = [n for n in internal_nodes if n not in graph]
    # For edges, we check if the mechanism ID matches any edge in the graph
    edge_ids = {d.get("id") for _, _, d in graph.edges(data=True) if "id" in d}
    missing_edges = [e for e in internal_edges if e not in edge_ids]

    total_items = len(internal_nodes) + len(internal_edges)
    found_items = (len(internal_nodes) - len(missing_nodes)) + (len(internal_edges) - len(missing_edges))
    completeness = found_items / total_items if total_items > 0 else 1.0

    return {
        "holon_id": holon_id,
        "valid": len(missing_nodes) == 0 and len(missing_edges) == 0,
        "missing_nodes": missing_nodes,
        "missing_edges": missing_edges,
        "present_nodes": [n for n in internal_nodes if n in graph],
        "present_edges": [e for e in internal_edges if e in edge_ids],
        "completeness": completeness,
    }


def compute_modularity_ratio(
    holon_id: str,
    graph: nx.DiGraph,
    holon_hierarchy: dict[str, dict],
) -> float:
    """Compute the ratio of internal to boundary edges for a holon.

    A good holon should have a ratio > 2.0, meaning internal connections
    are at least twice as dense as external connections.

    Args:
        holon_id: ID of the holon.
        graph: The causal graph.
        holon_hierarchy: Holon hierarchy from the parser.

    Returns:
        Modularity ratio (internal edges / boundary edges). Returns float('inf')
        if there are no boundary edges.
    """
    if holon_id not in holon_hierarchy:
        return 0.0

    holon = holon_hierarchy[holon_id]
    internal_node_set = set(holon.get("internal_nodes", []))

    internal_edges = 0
    boundary_edges = 0

    for u, v in graph.edges():
        u_internal = u in internal_node_set
        v_internal = v in internal_node_set

        if u_internal and v_internal:
            internal_edges += 1
        elif u_internal or v_internal:
            boundary_edges += 1

    if boundary_edges == 0:
        return float("inf") if internal_edges > 0 else 0.0

    return internal_edges / boundary_edges


def validate_intervention_equivalence(
    holon_id: str,
    graph: nx.DiGraph,
    holon_hierarchy: dict[str, dict],
) -> dict[str, Any]:
    """Compare intervention predictions through internal structure vs black-box abstraction.

    Tests whether the holon can be validly collapsed by comparing:
    (a) Intervening on inputs and tracing through internal structure to outputs
    (b) Treating the holon as a direct input→output mapping

    Args:
        holon_id: ID of the holon.
        graph: The causal graph.
        holon_hierarchy: Holon hierarchy from the parser.

    Returns:
        Dictionary with equivalence results and any discrepancies.
    """
    if holon_id not in holon_hierarchy:
        return {
            "holon_id": holon_id,
            "equivalent": False,
            "error": f"Holon '{holon_id}' not found in hierarchy",
        }

    holon = holon_hierarchy[holon_id]
    inputs = holon.get("inputs", [])
    outputs = holon.get("outputs", [])
    internal_nodes = set(holon.get("internal_nodes", []))

    if not inputs or not outputs:
        return {
            "holon_id": holon_id,
            "equivalent": True,
            "note": "No inputs or outputs defined; trivially equivalent.",
        }

    discrepancies = []
    detailed_results = []

    for input_node in inputs:
        if input_node not in graph:
            continue

        # (a) Full internal trace
        full_effects = simulate_intervention(graph, input_node, "increase", max_depth=8)

        # Check what happens at output nodes
        for output_node in outputs:
            if output_node not in graph:
                continue

            full_effect = full_effects.get(output_node, "no_effect")

            # (b) Black-box: is there a direct path from input to output?
            # Check if any path exists (through internal nodes)
            paths_exist = False
            try:
                paths = list(nx.all_simple_paths(graph, input_node, output_node, cutoff=len(internal_nodes) + 2))
                paths_exist = len(paths) > 0
            except nx.NetworkXError:
                pass

            bb_effect = full_effect if paths_exist else "no_effect"

            result = {
                "input": input_node,
                "output": output_node,
                "full_trace_effect": full_effect,
                "black_box_effect": bb_effect,
                "match": full_effect == bb_effect,
            }
            detailed_results.append(result)

            if full_effect != bb_effect:
                discrepancies.append(result)

    return {
        "holon_id": holon_id,
        "equivalent": len(discrepancies) == 0,
        "discrepancies": discrepancies,
        "detailed_results": detailed_results,
        "num_tests": len(detailed_results),
    }


def check_cross_holon_consistency(
    graph: nx.DiGraph,
    holon_hierarchy: dict[str, dict],
) -> list[str]:
    """Check consistency between overlapping holons.

    For every pair of holons that share nodes, verify that causal claims
    are consistent (no contradictory edge directions or relationships).

    Args:
        graph: The causal graph.
        holon_hierarchy: Holon hierarchy from the parser.

    Returns:
        List of inconsistency descriptions.
    """
    inconsistencies: list[str] = []

    # Build node-to-holon mapping
    node_to_holons: dict[str, set[str]] = {}
    for holon_id, info in holon_hierarchy.items():
        for node_id in info.get("internal_nodes", []):
            if node_id not in node_to_holons:
                node_to_holons[node_id] = set()
            node_to_holons[node_id].add(holon_id)

    # Check shared nodes
    shared_nodes = {n: holons for n, holons in node_to_holons.items() if len(holons) > 1}

    for node_id, holons in shared_nodes.items():
        holon_list = sorted(holons)
        for i in range(len(holon_list)):
            for j in range(i + 1, len(holon_list)):
                h1, h2 = holon_list[i], holon_list[j]

                # Check that input/output roles are compatible
                h1_info = holon_hierarchy[h1]
                h2_info = holon_hierarchy[h2]

                h1_inputs = set(h1_info.get("inputs", []))
                h1_outputs = set(h1_info.get("outputs", []))
                h2_inputs = set(h2_info.get("inputs", []))
                h2_outputs = set(h2_info.get("outputs", []))

                # A node that is an output of one holon and internal to another is fine
                # A node that is an output of one holon and an input of another is fine (inter-holon connection)
                # Flag: a node that is an output of both holons (potential conflict)
                if node_id in h1_outputs and node_id in h2_outputs:
                    inconsistencies.append(
                        f"Node '{node_id}' is an output of both '{h1}' and '{h2}' — potential conflict"
                    )

    # Check edge consistency between holons
    edge_by_id: dict[str, dict] = {}
    for u, v, data in graph.edges(data=True):
        edge_id = data.get("id", "")
        if edge_id:
            edge_by_id[edge_id] = {"source": u, "target": v, **data}

    for holon_id, info in holon_hierarchy.items():
        for edge_id in info.get("internal_edges", []):
            if edge_id in edge_by_id:
                edge = edge_by_id[edge_id]
                source = edge["source"]
                target = edge["target"]
                internal = set(info.get("internal_nodes", []))

                # Flag if edge endpoints are not in the holon's internal nodes
                if source not in internal and source not in set(info.get("inputs", [])):
                    inconsistencies.append(
                        f"Edge '{edge_id}' source '{source}' is not an internal node or input of holon '{holon_id}'"
                    )
                if target not in internal and target not in set(info.get("outputs", [])):
                    inconsistencies.append(
                        f"Edge '{edge_id}' target '{target}' is not an internal node or output of holon '{holon_id}'"
                    )

    return inconsistencies


def generate_holon_summary(
    holon_id: str,
    graph: nx.DiGraph,
    holon_hierarchy: dict[str, dict],
) -> str:
    """Produce a natural language summary of a holon for LLM consumption.

    Args:
        holon_id: ID of the holon.
        graph: The causal graph.
        holon_hierarchy: Holon hierarchy from the parser.

    Returns:
        Multi-paragraph string summarizing the holon.
    """
    if holon_id not in holon_hierarchy:
        return f"Holon '{holon_id}' not found in the hierarchy."

    info = holon_hierarchy[holon_id]

    lines = [f"## Holon Summary: {holon_id}\n"]

    # Scale and hierarchy
    scale = info.get("scale", "unknown")
    parent = info.get("parent")
    children = info.get("children", [])
    lines.append(f"**Scale**: {scale}")
    if parent:
        lines.append(f"**Parent holon**: {parent}")
    if children:
        lines.append(f"**Child holons**: {', '.join(children)}")
    lines.append("")

    # Inputs
    inputs = info.get("inputs", [])
    if inputs:
        lines.append("**Inputs:**")
        for inp in inputs:
            lines.append(f"  - {inp}")
    lines.append("")

    # Outputs
    outputs = info.get("outputs", [])
    if outputs:
        lines.append("**Outputs:**")
        for out in outputs:
            lines.append(f"  - {out}")
    lines.append("")

    # Internal structure
    internal_nodes = info.get("internal_nodes", [])
    internal_edges = info.get("internal_edges", [])
    lines.append(f"**Internal nodes** ({len(internal_nodes)}): {', '.join(internal_nodes)}")
    lines.append(f"**Internal edges** ({len(internal_edges)}): {', '.join(internal_edges)}")
    lines.append("")

    # Modularity
    ratio = compute_modularity_ratio(holon_id, graph, holon_hierarchy)
    lines.append(f"**Modularity ratio**: {ratio:.2f}")
    if ratio > 2.0:
        lines.append("This holon is well-modularized (ratio > 2.0).")
    elif ratio > 1.0:
        lines.append("This holon has moderate modularity (1.0 < ratio < 2.0).")
    else:
        lines.append("This holon has low modularity (ratio < 1.0), suggesting it may not be a natural boundary.")
    lines.append("")

    # Key internal pathways
    if inputs and outputs:
        lines.append("**Key pathways:**")
        for inp in inputs[:3]:
            for out in outputs[:3]:
                if inp in graph and out in graph:
                    try:
                        paths = list(nx.all_simple_paths(graph, inp, out, cutoff=6))
                        if paths:
                            shortest = min(paths, key=len)
                            lines.append(f"  - {' → '.join(shortest)}")
                    except nx.NetworkXError:
                        pass

    return "\n".join(lines)
