"""Graph operations: path finding, subgraph extraction, and structural queries.

Provides core graph operations on the parsed NetworkX DiGraph, including
path finding, subgraph extraction, and topology analysis.
"""

from typing import Any

import networkx as nx


def find_all_directed_paths(
    graph: nx.DiGraph,
    source: str,
    target: str,
    max_length: int = 5,
) -> list[list[str]]:
    """Find all directed paths from source to target up to max_length.

    Args:
        graph: The causal graph.
        source: Source node ID.
        target: Target node ID.
        max_length: Maximum number of edges in the path.

    Returns:
        List of paths, where each path is a list of node IDs.
    """
    if source not in graph or target not in graph:
        return []

    paths = []
    try:
        for path in nx.all_simple_paths(graph, source, target, cutoff=max_length):
            paths.append(path)
    except nx.NetworkXError:
        pass
    return paths


def find_ancestors(graph: nx.DiGraph, node: str) -> set[str]:
    """Find all ancestors of a node in the directed graph.

    Args:
        graph: The causal graph.
        node: Node ID.

    Returns:
        Set of ancestor node IDs.
    """
    if node not in graph:
        return set()
    return nx.ancestors(graph, node)


def find_descendants(graph: nx.DiGraph, node: str) -> set[str]:
    """Find all descendants of a node in the directed graph.

    Args:
        graph: The causal graph.
        node: Node ID.

    Returns:
        Set of descendant node IDs.
    """
    if node not in graph:
        return set()
    return nx.descendants(graph, node)


def extract_subgraph(
    graph: nx.DiGraph,
    node_ids: list[str],
    include_connecting_edges: bool = True,
) -> nx.DiGraph:
    """Extract a subgraph containing the specified nodes.

    Args:
        graph: The full graph.
        node_ids: List of node IDs to include.
        include_connecting_edges: If True, include all edges between the specified nodes.

    Returns:
        A new DiGraph containing only the specified nodes and their connecting edges.
    """
    valid_nodes = [n for n in node_ids if n in graph]
    subgraph = graph.subgraph(valid_nodes).copy()
    return subgraph


def get_node_degree_centrality(graph: nx.DiGraph) -> dict[str, float]:
    """Calculate degree centrality for all nodes.

    Args:
        graph: The graph.

    Returns:
        Dictionary mapping node IDs to their degree centrality.
    """
    return nx.degree_centrality(graph)


def get_node_betweenness_centrality(graph: nx.DiGraph) -> dict[str, float]:
    """Calculate betweenness centrality for all nodes.

    Args:
        graph: The graph.

    Returns:
        Dictionary mapping node IDs to their betweenness centrality.
    """
    return nx.betweenness_centrality(graph)


def find_bridge_nodes(graph: nx.DiGraph, holon_hierarchy: dict) -> list[dict[str, Any]]:
    """Find nodes that bridge between different holons.

    A bridge node is a member of multiple holons or connects nodes in different holons.

    Args:
        graph: The causal graph.
        holon_hierarchy: Holon hierarchy from the parser.

    Returns:
        List of dicts with bridge node information.
    """
    # Build node -> holon membership map
    node_holons: dict[str, set[str]] = {}
    for holon_id, info in holon_hierarchy.items():
        for node_id in info.get("internal_nodes", []):
            if node_id not in node_holons:
                node_holons[node_id] = set()
            node_holons[node_id].add(holon_id)

    bridges = []
    for node_id, holons in node_holons.items():
        if len(holons) > 1:
            bridges.append({
                "node": node_id,
                "holons": list(holons),
                "in_degree": graph.in_degree(node_id) if node_id in graph else 0,
                "out_degree": graph.out_degree(node_id) if node_id in graph else 0,
            })

    return sorted(bridges, key=lambda x: len(x["holons"]), reverse=True)


def get_graph_statistics(graph: nx.DiGraph) -> dict[str, Any]:
    """Calculate various statistics about the graph.

    Args:
        graph: The graph.

    Returns:
        Dictionary of graph statistics.
    """
    stats: dict[str, Any] = {
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "density": nx.density(graph),
        "is_dag": nx.is_directed_acyclic_graph(graph),
    }

    if graph.number_of_nodes() > 0:
        stats["avg_in_degree"] = sum(d for _, d in graph.in_degree()) / graph.number_of_nodes()
        stats["avg_out_degree"] = sum(d for _, d in graph.out_degree()) / graph.number_of_nodes()

        # Find strongly connected components (cycles)
        sccs = list(nx.strongly_connected_components(graph))
        nontrivial_sccs = [scc for scc in sccs if len(scc) > 1]
        stats["num_cycles"] = len(nontrivial_sccs)
        stats["cycle_nodes"] = [list(scc) for scc in nontrivial_sccs]

        # Find weakly connected components
        wccs = list(nx.weakly_connected_components(graph))
        stats["num_connected_components"] = len(wccs)

    return stats


def topological_sort_safe(graph: nx.DiGraph) -> list[str] | None:
    """Attempt topological sort; return None if graph has cycles.

    Args:
        graph: The directed graph.

    Returns:
        List of node IDs in topological order, or None if cycles exist.
    """
    try:
        return list(nx.topological_sort(graph))
    except nx.NetworkXUnfeasible:
        return None
