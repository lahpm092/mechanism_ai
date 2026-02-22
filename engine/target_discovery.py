"""Target discovery: intervention analysis and druggable target identification.

Given a disease phenotype (set of nodes in abnormal states), identifies
intervention targets that could restore normal function. Ranks targets
by predicted efficacy, evidence strength, and off-target effects.
"""

from typing import Any

import networkx as nx

from engine.causal_engine import (
    find_all_causal_paths,
    find_backdoor_adjustment_set,
    find_confounders,
    is_identifiable,
    simulate_intervention,
)
from engine.graph_core import find_ancestors, find_descendants


# Maps abnormal states to required intervention directions
STATE_TO_INTERVENTION: dict[str, str] = {
    "elevated": "decrease",
    "reduced": "increase",
    "desensitized": "restore_sensitivity",
    "overactive": "inhibit",
    "underactive": "activate",
    "absent": "restore",
    "constitutive": "inhibit",
}

# Inverse: what we want the node state to become
STATE_TO_DESIRED: dict[str, str] = {
    "elevated": "decrease",
    "reduced": "increase",
    "desensitized": "increase",
    "overactive": "decrease",
    "underactive": "increase",
    "absent": "increase",
    "constitutive": "decrease",
}


def discover_targets(
    graph: nx.DiGraph,
    disease_phenotype: dict[str, str],
    holon_hierarchy: dict[str, dict] | None = None,
    max_depth: int = 4,
) -> list[dict[str, Any]]:
    """Discover intervention targets for a disease phenotype.

    Args:
        graph: The causal graph.
        disease_phenotype: Dict mapping node IDs to their abnormal states
            (e.g., {"nf-kb": "elevated", "gr": "desensitized"}).
        holon_hierarchy: Optional holon hierarchy for holon impact analysis.
        max_depth: Maximum depth for upstream tracing.

    Returns:
        Ranked list of intervention target dictionaries.
    """
    disease_nodes = set(disease_phenotype.keys())

    # Step 1: Find root causes by tracing upstream from disease nodes
    candidate_targets = _find_candidate_targets(graph, disease_phenotype, max_depth)

    # Step 2: For each candidate, simulate the intervention
    scored_targets: list[dict[str, Any]] = []

    for target_id, target_info in candidate_targets.items():
        intervention_dir = target_info["intervention_direction"]

        # Map restore_sensitivity/activate/inhibit to increase/decrease for simulation
        sim_direction = _normalize_direction(intervention_dir)

        # Simulate intervention
        cascade = simulate_intervention(graph, target_id, sim_direction, max_depth=6)

        # Score: how many disease nodes would normalize?
        normalization_score = _score_normalization(
            cascade, disease_phenotype
        )

        # Evidence strength along causal paths
        evidence_score = _score_evidence(graph, target_id, disease_nodes)

        # Identifiability
        identifiable = all(
            is_identifiable(graph, target_id, dn)
            for dn in disease_nodes
            if dn in graph and dn != target_id
        )

        # Off-target effects
        off_target = {
            node: effect for node, effect in cascade.items()
            if node not in disease_nodes
        }

        # Causal paths to disease nodes
        causal_paths = {}
        for dn in disease_nodes:
            if dn != target_id:
                paths = find_all_causal_paths(graph, target_id, dn, max_length=max_depth + 2)
                if paths:
                    causal_paths[dn] = paths

        # Adjustment sets
        adjustment_sets = {}
        for dn in disease_nodes:
            if dn != target_id and dn in graph:
                adj = find_backdoor_adjustment_set(graph, target_id, dn)
                if adj is not None:
                    adjustment_sets[dn] = [list(s) for s in adj[:3]]  # Top 3 sets

        # Affected holons
        affected_holons = set()
        if holon_hierarchy:
            for holon_id, info in holon_hierarchy.items():
                internal = set(info.get("internal_nodes", []))
                affected = set(cascade.keys()) | {target_id}
                if internal & affected:
                    affected_holons.add(holon_id)

        # Compute composite score
        composite_score = (
            normalization_score * 3.0 +
            evidence_score * 2.0 +
            (1.0 if identifiable else 0.0) * 1.5 +
            max(0, 1.0 - len(off_target) * 0.1) * 1.0
        )

        # Build rationale
        rationale = _build_rationale(
            target_id, intervention_dir, cascade, disease_phenotype, target_info
        )

        scored_targets.append({
            "target": target_id,
            "intervention": intervention_dir,
            "rationale": rationale,
            "predicted_cascade": cascade,
            "affected_holons": sorted(affected_holons),
            "evidence_strength": _categorize_score(evidence_score),
            "causal_paths": {k: [list(p) for p in v[:3]] for k, v in causal_paths.items()},
            "identifiable": identifiable,
            "adjustment_sets": adjustment_sets,
            "normalization_score": normalization_score,
            "off_target_effects": len(off_target),
            "composite_score": composite_score,
            "is_root_cause": target_info.get("is_root_cause", False),
        })

    # Sort by composite score (descending)
    scored_targets.sort(key=lambda t: t["composite_score"], reverse=True)

    return scored_targets


def _find_candidate_targets(
    graph: nx.DiGraph,
    disease_phenotype: dict[str, str],
    max_depth: int,
) -> dict[str, dict]:
    """Find candidate intervention targets by tracing upstream from disease nodes.

    Args:
        graph: The causal graph.
        disease_phenotype: Disease phenotype description.
        max_depth: Maximum upstream trace depth.

    Returns:
        Dictionary mapping candidate target IDs to their info.
    """
    candidates: dict[str, dict] = {}

    # All disease nodes are potential targets
    for node_id, state in disease_phenotype.items():
        if node_id in graph:
            desired = STATE_TO_DESIRED.get(state, "modulate")
            intervention = STATE_TO_INTERVENTION.get(state, "modulate")
            candidates[node_id] = {
                "intervention_direction": intervention,
                "desired_effect": desired,
                "is_root_cause": False,
                "upstream_of": [node_id],
                "disease_state": state,
            }

    # Trace upstream from each disease node to find root causes
    for node_id, state in disease_phenotype.items():
        if node_id not in graph:
            continue

        ancestors = find_ancestors(graph, node_id)
        for ancestor in ancestors:
            # Check if this ancestor is already a disease node
            is_disease_node = ancestor in disease_phenotype

            # Check path length
            try:
                paths = list(nx.all_simple_paths(graph, ancestor, node_id, cutoff=max_depth))
                if not paths:
                    continue
            except nx.NetworkXError:
                continue

            if ancestor not in candidates:
                # Determine intervention direction based on what we want at the disease node
                desired = STATE_TO_DESIRED.get(state, "modulate")
                # Trace direction through path to determine what intervention on ancestor achieves desired effect
                intervention_dir = _infer_intervention_direction(
                    graph, ancestor, node_id, desired
                )
                candidates[ancestor] = {
                    "intervention_direction": intervention_dir,
                    "desired_effect": desired,
                    "is_root_cause": not is_disease_node,
                    "upstream_of": [node_id],
                    "disease_state": disease_phenotype.get(ancestor, "normal"),
                }
            else:
                if node_id not in candidates[ancestor]["upstream_of"]:
                    candidates[ancestor]["upstream_of"].append(node_id)

    # Mark nodes that are upstream of many disease nodes as higher priority root causes
    for cid, cinfo in candidates.items():
        if len(cinfo["upstream_of"]) > 1 and cid not in disease_phenotype:
            cinfo["is_root_cause"] = True

    return candidates


def _infer_intervention_direction(
    graph: nx.DiGraph,
    source: str,
    target: str,
    desired_target_effect: str,
) -> str:
    """Infer what intervention direction on source achieves desired effect on target.

    Args:
        graph: The causal graph.
        source: Source node.
        target: Target node.
        desired_target_effect: Desired effect direction at target.

    Returns:
        Required intervention direction at source.
    """
    # Simple heuristic: simulate increase and see if target moves in desired direction
    effects = simulate_intervention(graph, source, "increase", max_depth=6)
    target_effect = effects.get(target, "no_effect")

    if target_effect == desired_target_effect:
        return "increase"
    elif target_effect in ("increase", "decrease") and desired_target_effect in ("increase", "decrease"):
        return "decrease" if target_effect != desired_target_effect else "increase"
    else:
        return "modulate"


def _score_normalization(
    cascade: dict[str, str],
    disease_phenotype: dict[str, str],
) -> float:
    """Score how many disease nodes would normalize under the intervention cascade.

    Args:
        cascade: Predicted effects from the intervention.
        disease_phenotype: Disease phenotype.

    Returns:
        Score from 0.0 to 1.0.
    """
    if not disease_phenotype:
        return 0.0

    normalized = 0
    for node_id, state in disease_phenotype.items():
        desired = STATE_TO_DESIRED.get(state, "modulate")
        predicted = cascade.get(node_id, "no_effect")

        if predicted == desired:
            normalized += 1
        elif predicted == "modulate" and desired != "no_effect":
            normalized += 0.3  # Partial credit

    return normalized / len(disease_phenotype)


def _score_evidence(
    graph: nx.DiGraph,
    target: str,
    disease_nodes: set[str],
) -> float:
    """Score the evidence strength along paths from target to disease nodes.

    Args:
        graph: The causal graph.
        target: Target node.
        disease_nodes: Set of disease node IDs.

    Returns:
        Average evidence score (0.0 to 1.0).
    """
    strength_scores = {"strong": 1.0, "moderate": 0.6, "weak": 0.3, "contested": 0.1}
    scores: list[float] = []

    for dn in disease_nodes:
        if dn == target or dn not in graph:
            continue

        try:
            paths = list(nx.all_simple_paths(graph, target, dn, cutoff=6))
        except nx.NetworkXError:
            continue

        for path in paths[:5]:  # Limit to first 5 paths
            path_score = 1.0
            for i in range(len(path) - 1):
                edge_data = graph.edges.get((path[i], path[i + 1]), {})
                strength = edge_data.get("evidence_strength", "unknown")
                path_score *= strength_scores.get(strength, 0.5)
            scores.append(path_score)

    return sum(scores) / len(scores) if scores else 0.0


def _categorize_score(score: float) -> str:
    """Categorize a numeric evidence score."""
    if score >= 0.7:
        return "strong"
    elif score >= 0.4:
        return "moderate"
    elif score >= 0.1:
        return "weak"
    else:
        return "insufficient"


def _normalize_direction(direction: str) -> str:
    """Normalize an intervention direction to increase/decrease for simulation."""
    increase_terms = {"increase", "activate", "restore_sensitivity", "restore"}
    decrease_terms = {"decrease", "inhibit"}

    if direction in increase_terms:
        return "increase"
    elif direction in decrease_terms:
        return "decrease"
    else:
        return "increase"  # Default


def _build_rationale(
    target_id: str,
    intervention: str,
    cascade: dict[str, str],
    disease_phenotype: dict[str, str],
    target_info: dict,
) -> str:
    """Build a natural language rationale for the intervention target.

    Args:
        target_id: Target node ID.
        intervention: Intervention type.
        cascade: Predicted cascade effects.
        disease_phenotype: Disease phenotype.
        target_info: Additional target information.

    Returns:
        Rationale string.
    """
    parts = []

    if target_info.get("is_root_cause"):
        parts.append(f"{target_id} is identified as a root cause upstream of multiple disease nodes.")
    else:
        parts.append(f"{target_id} is a direct disease node.")

    disease_state = target_info.get("disease_state", "")
    if disease_state and disease_state != "normal":
        parts.append(f"Current state: {disease_state}.")

    parts.append(f"Proposed intervention: {intervention}.")

    # Summarize cascade effects on disease nodes
    effects_on_disease = []
    for dn, state in disease_phenotype.items():
        if dn in cascade:
            effects_on_disease.append(f"{dn} → {cascade[dn]}")

    if effects_on_disease:
        parts.append(f"Predicted effects on disease nodes: {'; '.join(effects_on_disease)}.")

    upstream_of = target_info.get("upstream_of", [])
    if len(upstream_of) > 1:
        parts.append(
            f"This target is upstream of {len(upstream_of)} disease nodes "
            f"({', '.join(upstream_of)}), making it a high-leverage intervention point."
        )

    return " ".join(parts)


def generate_target_report(
    targets: list[dict[str, Any]],
    disease_phenotype: dict[str, str],
) -> str:
    """Generate a markdown report of target discovery results.

    Args:
        targets: Ranked list of targets from discover_targets().
        disease_phenotype: The disease phenotype that was analyzed.

    Returns:
        Markdown-formatted report string.
    """
    lines = [
        "# Target Discovery Report\n",
        "## Disease Phenotype\n",
    ]

    for node, state in disease_phenotype.items():
        lines.append(f"- **{node}**: {state}")
    lines.append("")

    lines.append(f"## Candidate Targets ({len(targets)} found)\n")

    for i, target in enumerate(targets, 1):
        lines.append(f"### {i}. {target['target']}")
        lines.append(f"- **Intervention**: {target['intervention']}")
        lines.append(f"- **Composite Score**: {target['composite_score']:.2f}")
        lines.append(f"- **Normalization Score**: {target['normalization_score']:.2f}")
        lines.append(f"- **Evidence Strength**: {target['evidence_strength']}")
        lines.append(f"- **Identifiable**: {'Yes' if target['identifiable'] else 'No'}")
        lines.append(f"- **Root Cause**: {'Yes' if target['is_root_cause'] else 'No'}")
        lines.append(f"- **Off-target Effects**: {target['off_target_effects']}")

        if target.get("affected_holons"):
            lines.append(f"- **Affected Holons**: {', '.join(target['affected_holons'])}")

        lines.append(f"\n**Rationale**: {target['rationale']}\n")

        cascade = target.get("predicted_cascade", {})
        if cascade:
            lines.append("**Predicted Cascade**:")
            for node, effect in sorted(cascade.items()):
                lines.append(f"  - {node}: {effect}")
            lines.append("")

        lines.append("---\n")

    return "\n".join(lines)
