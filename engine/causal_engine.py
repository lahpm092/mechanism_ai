"""Causal inference engine: d-separation, backdoor criterion, identifiability.

Implements formal causal reasoning operations on the parsed causal graph,
including d-separation testing, backdoor adjustment set finding,
identifiability checking, and intervention simulation.
"""

from collections import deque
from typing import Any

import networkx as nx

from engine.graph_core import find_all_directed_paths


# --- Direction composition for intervention simulation ---

DIRECTION_COMPOSE: dict[tuple[str, str], str] = {
    ("increase", "excitatory"): "increase",
    ("increase", "inhibitory"): "decrease",
    ("increase", "modulatory"): "modulate",
    ("decrease", "excitatory"): "decrease",
    ("decrease", "inhibitory"): "increase",
    ("decrease", "modulatory"): "modulate",
    ("modulate", "excitatory"): "modulate",
    ("modulate", "inhibitory"): "modulate",
    ("modulate", "modulatory"): "modulate",
}

# Map relationship types to direction categories
RELATIONSHIP_TO_DIRECTION: dict[str, str] = {
    "stimulates": "excitatory",
    "activates": "excitatory",
    "upregulates": "excitatory",
    "converts_to": "excitatory",
    "inhibits": "inhibitory",
    "degrades": "inhibitory",
    "downregulates": "inhibitory",
    "modulates": "modulatory",
}


def d_separated(
    graph: nx.DiGraph,
    x: str | set[str],
    y: str | set[str],
    z: set[str] | None = None,
) -> bool:
    """Test if X and Y are d-separated given conditioning set Z.

    Uses the Bayes-Ball algorithm to determine d-separation in the causal DAG.

    Args:
        graph: The causal DAG.
        x: Node or set of nodes X.
        y: Node or set of nodes Y.
        z: Conditioning set Z (may be empty).

    Returns:
        True if X and Y are d-separated given Z.
    """
    if isinstance(x, str):
        x = {x}
    if isinstance(y, str):
        y = {y}
    if z is None:
        z = set()

    # Validate nodes exist
    for node in x | y | z:
        if node not in graph:
            raise ValueError(f"Node '{node}' not found in graph")

    # Use the Bayes-Ball algorithm
    # A node is "reachable" from X given Z if there exists an active path
    reachable = _bayes_ball_reachable(graph, x, z)

    # X and Y are d-separated if no node in Y is reachable from X
    return len(reachable & y) == 0


def _bayes_ball_reachable(
    graph: nx.DiGraph,
    sources: set[str],
    conditioned: set[str],
) -> set[str]:
    """Find all nodes reachable via active paths from source nodes given conditioning.

    Implements the Bayes-Ball algorithm for d-separation testing.

    Args:
        graph: The causal DAG.
        sources: Set of source nodes.
        conditioned: Set of conditioned (observed) nodes.

    Returns:
        Set of all nodes reachable via active paths.
    """
    # First, find all ancestors of conditioned nodes
    ancestors_of_z = set()
    for z_node in conditioned:
        if z_node in graph:
            ancestors_of_z |= nx.ancestors(graph, z_node)
    ancestors_of_z |= conditioned

    # BFS with state tracking: (node, direction)
    # direction: "up" means we arrived from a child, "down" means from a parent
    visited: set[tuple[str, str]] = set()
    reachable: set[str] = set()

    queue: deque[tuple[str, str]] = deque()

    # Initialize: start from source nodes going both up and down
    for s in sources:
        queue.append((s, "up"))
        queue.append((s, "down"))

    while queue:
        current, direction = queue.popleft()

        if (current, direction) in visited:
            continue
        visited.add((current, direction))

        if current not in sources:
            reachable.add(current)

        # If we arrived going "up" (from a child)
        if direction == "up" and current not in conditioned:
            # Can pass through to parents (chain/fork going up)
            for parent in graph.predecessors(current):
                if (parent, "up") not in visited:
                    queue.append((parent, "up"))
            # Can pass through to other children (fork)
            for child in graph.successors(current):
                if (child, "down") not in visited:
                    queue.append((child, "down"))

        # If we arrived going "down" (from a parent)
        elif direction == "down":
            # If not conditioned, can continue down (chain)
            if current not in conditioned:
                for child in graph.successors(current):
                    if (child, "down") not in visited:
                        queue.append((child, "down"))
            # If conditioned or ancestor of conditioned, can go up (collider activation)
            if current in ancestors_of_z:
                for parent in graph.predecessors(current):
                    if (parent, "up") not in visited:
                        queue.append((parent, "up"))

    return reachable


def _break_feedback_cycles(graph: nx.DiGraph) -> nx.DiGraph:
    """Create a DAG by removing feedback (inhibitory back-) edges from cycles.

    In biological graphs, feedback loops are expected. For causal inference
    algorithms that require a DAG, we break cycles by removing edges that
    are marked as inhibitory feedback (i.e., edges going "backward" in the
    dominant causal direction).

    Args:
        graph: Possibly cyclic directed graph.

    Returns:
        A DAG copy of the graph with feedback edges removed.
    """
    if nx.is_directed_acyclic_graph(graph):
        return graph.copy()

    dag = graph.copy()

    # Iteratively remove feedback edges until acyclic
    max_iterations = 50
    for _ in range(max_iterations):
        if nx.is_directed_acyclic_graph(dag):
            break

        try:
            cycles = list(nx.simple_cycles(dag))
        except Exception:
            break

        if not cycles:
            break

        # For each cycle, find the best edge to remove (prefer inhibitory/feedback)
        removed = False
        for cycle in cycles:
            best_edge = None
            best_score = -1

            for i in range(len(cycle)):
                u = cycle[i]
                v = cycle[(i + 1) % len(cycle)]
                if dag.has_edge(u, v):
                    edge_data = dag.edges[u, v]
                    score = 0
                    if edge_data.get("direction") == "inhibitory":
                        score += 2
                    edge_id = edge_data.get("id", "")
                    if "inhibit" in edge_id or "feedback" in edge_id or "suppress" in edge_id:
                        score += 2
                    if score > best_score:
                        best_score = score
                        best_edge = (u, v)

            if best_edge and dag.has_edge(*best_edge):
                dag.remove_edge(*best_edge)
                removed = True
                break  # Re-check cycles after removal

        if not removed:
            # Remove any edge from first cycle as fallback
            if cycles:
                cycle = cycles[0]
                u, v = cycle[0], cycle[1 % len(cycle)]
                if dag.has_edge(u, v):
                    dag.remove_edge(u, v)

    return dag


def find_backdoor_adjustment_set(
    graph: nx.DiGraph,
    treatment: str,
    outcome: str,
) -> list[set[str]] | None:
    """Find valid adjustment sets satisfying Pearl's backdoor criterion.

    The backdoor criterion requires finding a set Z such that:
    1. No node in Z is a descendant of the treatment.
    2. Z blocks every backdoor path from treatment to outcome.

    For graphs with feedback cycles, cycles are broken before applying
    the criterion (standard approach for biological causal graphs).

    Args:
        graph: The causal graph (may contain feedback cycles).
        treatment: Treatment node ID.
        outcome: Outcome node ID.

    Returns:
        List of valid adjustment sets, or None if the effect is not identifiable
        via backdoor adjustment. Returns empty list inside the list if no
        adjustment is needed (no backdoor paths).
    """
    if treatment not in graph or outcome not in graph:
        raise ValueError(f"Treatment or outcome node not found in graph")

    # If there's a direct edge, the effect is trivially identifiable
    if graph.has_edge(treatment, outcome):
        # Check if there are any backdoor paths that need adjustment
        dag = _break_feedback_cycles(graph)
        descendants_of_treatment = nx.descendants(dag, treatment) if treatment in dag else set()
        parents_of_treatment = set(dag.predecessors(treatment)) if treatment in dag else set()

        if not parents_of_treatment:
            return [set()]

        # Build manipulated graph (remove edges out of treatment)
        manipulated = dag.copy()
        out_edges = list(manipulated.out_edges(treatment))
        manipulated.remove_edges_from(out_edges)

        if d_separated(manipulated, treatment, outcome, set()):
            return [set()]

        # Try parent set
        candidate_nodes = set(dag.nodes()) - descendants_of_treatment - {treatment, outcome}
        parent_set = parents_of_treatment & candidate_nodes
        if parent_set:
            try:
                if d_separated(manipulated, treatment, outcome, parent_set):
                    return [parent_set]
            except ValueError:
                pass

        # Try individual candidates
        for node in candidate_nodes:
            try:
                if d_separated(manipulated, treatment, outcome, {node}):
                    return [{node}]
            except ValueError:
                pass

        # Direct edge exists, so the effect is identifiable even without
        # a formal adjustment set (we can use the front-door or direct method)
        return [set()]

    # No direct edge — use standard backdoor on DAG
    dag = _break_feedback_cycles(graph)
    descendants_of_treatment = nx.descendants(dag, treatment) if treatment in dag else set()
    candidate_nodes = set(dag.nodes()) - descendants_of_treatment - {treatment, outcome}
    parents_of_treatment = set(dag.predecessors(treatment)) if treatment in dag else set()

    if not parents_of_treatment:
        return [set()]

    manipulated = dag.copy()
    out_edges = list(manipulated.out_edges(treatment))
    manipulated.remove_edges_from(out_edges)

    if d_separated(manipulated, treatment, outcome, set()):
        return [set()]

    valid_sets: list[set[str]] = []

    parent_set = parents_of_treatment & candidate_nodes
    if parent_set:
        try:
            if d_separated(manipulated, treatment, outcome, parent_set):
                valid_sets.append(parent_set)
        except ValueError:
            pass

    for node in candidate_nodes:
        try:
            if d_separated(manipulated, treatment, outcome, {node}):
                valid_sets.append({node})
        except ValueError:
            pass

    if not valid_sets:
        candidate_list = list(candidate_nodes)
        for i in range(min(len(candidate_list), 20)):
            for j in range(i + 1, min(len(candidate_list), 20)):
                pair = {candidate_list[i], candidate_list[j]}
                try:
                    if d_separated(manipulated, treatment, outcome, pair):
                        valid_sets.append(pair)
                except ValueError:
                    pass
                if valid_sets:
                    break
            if valid_sets:
                break

    if valid_sets:
        valid_sets.sort(key=len)
        return valid_sets

    return None


def is_identifiable(
    graph: nx.DiGraph,
    treatment: str,
    outcome: str,
) -> bool:
    """Check if the causal effect P(outcome | do(treatment)) is identifiable.

    Uses a simplified check: the effect is identifiable if:
    1. There's a direct edge from treatment to outcome, OR
    2. There exists a valid backdoor adjustment set, OR
    3. There's an identifiable front-door path through mediators.

    Args:
        graph: The causal graph (may contain cycles).
        treatment: Treatment node ID.
        outcome: Outcome node ID.

    Returns:
        True if the causal effect is identifiable.
    """
    if treatment not in graph or outcome not in graph:
        return False

    # Direct edge implies identifiability (we can measure it)
    if graph.has_edge(treatment, outcome):
        return True

    # Check if there's any directed path (the effect exists to identify)
    try:
        paths = list(nx.all_simple_paths(graph, treatment, outcome, cutoff=6))
        if not paths:
            return False
    except nx.NetworkXError:
        return False

    # Check backdoor criterion
    adjustment = find_backdoor_adjustment_set(graph, treatment, outcome)
    if adjustment is not None:
        return True

    # Check front-door criterion
    mediators = find_mediators(graph, treatment, outcome)
    if mediators:
        for m in mediators:
            m_adjustment = find_backdoor_adjustment_set(graph, m, outcome)
            if m_adjustment is not None:
                return True

    return False


def find_all_causal_paths(
    graph: nx.DiGraph,
    source: str,
    target: str,
    max_length: int = 5,
) -> list[list[str]]:
    """Find all directed causal paths from source to target.

    Args:
        graph: The causal graph.
        source: Source node ID.
        target: Target node ID.
        max_length: Maximum path length (number of edges).

    Returns:
        List of paths, where each path is a list of node IDs.
    """
    return find_all_directed_paths(graph, source, target, max_length)


def find_mediators(
    graph: nx.DiGraph,
    treatment: str,
    outcome: str,
) -> list[str]:
    """Find all nodes that mediate the effect of treatment on outcome.

    A mediator lies on at least one directed path from treatment to outcome
    and is neither the treatment nor the outcome.

    Args:
        graph: The causal graph.
        treatment: Treatment node ID.
        outcome: Outcome node ID.

    Returns:
        List of mediator node IDs.
    """
    if treatment not in graph or outcome not in graph:
        return []

    paths = find_all_causal_paths(graph, treatment, outcome, max_length=10)
    mediator_set: set[str] = set()
    for path in paths:
        # Exclude first (treatment) and last (outcome) nodes
        for node in path[1:-1]:
            mediator_set.add(node)

    return sorted(mediator_set)


def simulate_intervention(
    graph: nx.DiGraph,
    intervention_node: str,
    direction: str = "increase",
    max_depth: int = 6,
) -> dict[str, str]:
    """Simulate the downstream effects of intervening on a node.

    Traces downstream effects through the causal graph, composing edge
    directions to predict the effect on each reachable node.

    Args:
        graph: The causal graph.
        intervention_node: Node to intervene on.
        direction: Direction of intervention ("increase" or "decrease").
        max_depth: Maximum depth to trace effects.

    Returns:
        Dictionary mapping downstream node IDs to predicted effect direction.
    """
    if intervention_node not in graph:
        return {}

    effects: dict[str, str] = {}
    # BFS through the graph
    queue: deque[tuple[str, str, int]] = deque()

    # Start from the intervention node's children
    for successor in graph.successors(intervention_node):
        edge_data = graph.edges[intervention_node, successor]
        edge_direction = _get_edge_direction(edge_data)
        effect = DIRECTION_COMPOSE.get((direction, edge_direction), "modulate")
        queue.append((successor, effect, 1))

    visited: set[str] = {intervention_node}

    while queue:
        node, current_effect, depth = queue.popleft()

        if depth > max_depth:
            continue

        if node in visited:
            # If already visited with same effect, skip
            if node in effects and effects[node] == current_effect:
                continue
            # If conflicting effects, mark as modulate
            if node in effects and effects[node] != current_effect:
                effects[node] = "modulate"
                continue

        visited.add(node)
        effects[node] = current_effect

        # Propagate to successors
        for successor in graph.successors(node):
            if successor not in visited or successor not in effects:
                edge_data = graph.edges[node, successor]
                edge_direction = _get_edge_direction(edge_data)
                next_effect = DIRECTION_COMPOSE.get(
                    (current_effect, edge_direction), "modulate"
                )
                queue.append((successor, next_effect, depth + 1))

    return effects


def _get_edge_direction(edge_data: dict) -> str:
    """Extract the functional direction category from edge data.

    Args:
        edge_data: Edge attribute dictionary.

    Returns:
        Direction category: "excitatory", "inhibitory", or "modulatory".
    """
    # First check the explicit direction field
    direction = edge_data.get("direction", "")
    if direction in ("excitatory", "inhibitory", "modulatory"):
        return direction

    # Fall back to relationship type
    relationship = edge_data.get("relationship", "")
    return RELATIONSHIP_TO_DIRECTION.get(relationship, "modulatory")


def find_confounders(
    graph: nx.DiGraph,
    x: str,
    y: str,
) -> list[str]:
    """Find common causes of X and Y that would confound observational estimates.

    A confounder is a node that is an ancestor of both X and Y (common cause).

    Args:
        graph: The causal graph.
        x: First node ID.
        y: Second node ID.

    Returns:
        List of confounder node IDs.
    """
    if x not in graph or y not in graph:
        return []

    ancestors_x = nx.ancestors(graph, x)
    ancestors_y = nx.ancestors(graph, y)

    # Common ancestors are potential confounders
    common_ancestors = ancestors_x & ancestors_y

    # Filter: a true confounder must have a directed path to both X and Y
    confounders = []
    for ancestor in common_ancestors:
        has_path_to_x = nx.has_path(graph, ancestor, x)
        has_path_to_y = nx.has_path(graph, ancestor, y)
        if has_path_to_x and has_path_to_y:
            confounders.append(ancestor)

    return sorted(confounders)


def get_markov_blanket(graph: nx.DiGraph, node: str) -> set[str]:
    """Get the Markov blanket of a node (parents, children, co-parents).

    Args:
        graph: The causal graph.
        node: Node ID.

    Returns:
        Set of node IDs in the Markov blanket.
    """
    if node not in graph:
        return set()

    blanket: set[str] = set()

    # Parents
    blanket |= set(graph.predecessors(node))

    # Children
    children = set(graph.successors(node))
    blanket |= children

    # Co-parents (other parents of children)
    for child in children:
        blanket |= set(graph.predecessors(child))

    # Remove the node itself
    blanket.discard(node)

    return blanket
