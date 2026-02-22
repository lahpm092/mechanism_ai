"""Validator: structural integrity tests for the vault and parsed graph.

Checks acyclicity, dangling links, schema compliance, orphan nodes,
holon completeness, evidence completeness, and bidirectional references.
"""

from pathlib import Path
from typing import Any

import frontmatter
import networkx as nx

from engine.holon_engine import check_cross_holon_consistency, validate_holon_completeness
from engine.parser import REQUIRED_HOLON_FIELDS, REQUIRED_MECHANISM_FIELDS, REQUIRED_NODE_FIELDS


def run_full_validation(
    graph: nx.DiGraph,
    holon_hierarchy: dict[str, dict],
    parsed_data: dict[str, Any],
    vault_path: str,
) -> dict[str, Any]:
    """Run all structural integrity tests on the vault and graph.

    Args:
        graph: The parsed causal graph.
        holon_hierarchy: Holon hierarchy from the parser.
        parsed_data: Full parsed data from parse_vault().
        vault_path: Path to the vault directory.

    Returns:
        Dictionary with all validation results.
    """
    results: dict[str, Any] = {}

    # 1. Acyclicity check
    results["acyclicity"] = check_acyclicity(graph)

    # 2. Dangling link check
    results["dangling_links"] = check_dangling_links(parsed_data)

    # 3. Schema compliance
    results["schema_compliance"] = check_schema_compliance(parsed_data)

    # 4. Orphan check
    results["orphan_nodes"] = check_orphan_nodes(graph, parsed_data)

    # 5. Holon completeness
    results["holon_completeness"] = check_holon_completeness(graph, holon_hierarchy)

    # 6. Cross-holon consistency
    results["cross_holon_consistency"] = check_cross_holon_consistency_wrapper(graph, holon_hierarchy)

    # 7. Evidence completeness
    results["evidence_completeness"] = check_evidence_completeness(parsed_data)

    # 8. Bidirectional link check
    results["bidirectional_links"] = check_bidirectional_links(parsed_data)

    # Summary
    total_checks = len(results)
    passed = sum(1 for v in results.values() if v.get("passed", False))
    results["summary"] = {
        "total_checks": total_checks,
        "passed": passed,
        "failed": total_checks - passed,
        "pass_rate": passed / total_checks if total_checks > 0 else 0.0,
    }

    return results


def check_acyclicity(graph: nx.DiGraph) -> dict[str, Any]:
    """Check if the causal edges form a DAG.

    Feedback loops that resolve across time/holon levels are flagged but
    don't cause failure.

    Args:
        graph: The causal graph.

    Returns:
        Validation result dictionary.
    """
    is_dag = nx.is_directed_acyclic_graph(graph)
    cycles = []

    if not is_dag:
        try:
            cycles = list(nx.simple_cycles(graph))
        except Exception:
            cycles = [list(scc) for scc in nx.strongly_connected_components(graph) if len(scc) > 1]

    # Flag biological feedback loops (these are expected)
    feedback_keywords = {"feedback", "inhibits", "suppress"}
    expected_cycles = []
    unexpected_cycles = []

    for cycle in cycles:
        # Check if any edge in the cycle is a known feedback mechanism
        is_feedback = False
        for i in range(len(cycle)):
            u = cycle[i]
            v = cycle[(i + 1) % len(cycle)]
            if graph.has_edge(u, v):
                edge_data = graph.edges[u, v]
                edge_id = edge_data.get("id", "")
                relationship = edge_data.get("relationship", "")
                if any(kw in edge_id.lower() for kw in feedback_keywords) or \
                   relationship in ("inhibits", "downregulates"):
                    is_feedback = True
                    break

        if is_feedback:
            expected_cycles.append(cycle)
        else:
            unexpected_cycles.append(cycle)

    return {
        "passed": is_dag or (len(unexpected_cycles) == 0),
        "is_dag": is_dag,
        "total_cycles": len(cycles),
        "expected_feedback_cycles": expected_cycles,
        "unexpected_cycles": unexpected_cycles,
        "message": "DAG" if is_dag else f"{len(cycles)} cycle(s) found ({len(expected_cycles)} expected feedback loops)",
    }


def check_dangling_links(parsed_data: dict[str, Any]) -> dict[str, Any]:
    """Check that every wikilink resolves to an existing file.

    Args:
        parsed_data: Full parsed data from parse_vault().

    Returns:
        Validation result dictionary.
    """
    dangling = parsed_data.get("metadata", {}).get("dangling_links", [])

    return {
        "passed": len(dangling) == 0,
        "count": len(dangling),
        "dangling_links": dangling[:50],  # Limit to first 50
        "message": f"{len(dangling)} dangling link(s) found" if dangling else "All links resolve",
    }


def check_schema_compliance(parsed_data: dict[str, Any]) -> dict[str, Any]:
    """Check that every file's frontmatter contains all required fields.

    Args:
        parsed_data: Full parsed data from parse_vault().

    Returns:
        Validation result dictionary.
    """
    violations: list[dict] = []

    # Check nodes
    for node_id, data in parsed_data.get("nodes_raw", {}).items():
        fm = data.get("frontmatter", {})
        missing = REQUIRED_NODE_FIELDS - set(fm.keys())
        if missing:
            violations.append({
                "file": node_id,
                "category": "node",
                "missing_fields": list(missing),
            })

    # Check mechanisms
    for mech_id, data in parsed_data.get("mechanisms_raw", {}).items():
        fm = data.get("frontmatter", {})
        missing = REQUIRED_MECHANISM_FIELDS - set(fm.keys())
        if missing:
            violations.append({
                "file": mech_id,
                "category": "mechanism",
                "missing_fields": list(missing),
            })

    # Check holons
    for holon_id, data in parsed_data.get("holons_raw", {}).items():
        fm = data.get("frontmatter", {})
        missing = REQUIRED_HOLON_FIELDS - set(fm.keys())
        if missing:
            violations.append({
                "file": holon_id,
                "category": "holon",
                "missing_fields": list(missing),
            })

    return {
        "passed": len(violations) == 0,
        "count": len(violations),
        "violations": violations,
        "message": f"{len(violations)} schema violation(s)" if violations else "All files comply with schema",
    }


def check_orphan_nodes(
    graph: nx.DiGraph,
    parsed_data: dict[str, Any],
) -> dict[str, Any]:
    """Flag nodes with no causal edges (only reference edges).

    Args:
        graph: The causal graph.
        parsed_data: Full parsed data.

    Returns:
        Validation result dictionary.
    """
    orphans = parsed_data.get("metadata", {}).get("orphan_nodes", [])

    return {
        "passed": len(orphans) == 0,
        "count": len(orphans),
        "orphan_nodes": orphans,
        "message": f"{len(orphans)} orphan node(s)" if orphans else "No orphan nodes",
    }


def check_holon_completeness(
    graph: nx.DiGraph,
    holon_hierarchy: dict[str, dict],
) -> dict[str, Any]:
    """Check that all holons have complete internal nodes and edges.

    Args:
        graph: The causal graph.
        holon_hierarchy: Holon hierarchy.

    Returns:
        Validation result dictionary.
    """
    results = []
    all_complete = True

    for holon_id in holon_hierarchy:
        result = validate_holon_completeness(holon_id, graph, holon_hierarchy)
        results.append(result)
        if not result["valid"]:
            all_complete = False

    return {
        "passed": all_complete,
        "holon_results": results,
        "message": "All holons complete" if all_complete else "Some holons have missing elements",
    }


def check_cross_holon_consistency_wrapper(
    graph: nx.DiGraph,
    holon_hierarchy: dict[str, dict],
) -> dict[str, Any]:
    """Wrapper for cross-holon consistency check.

    Args:
        graph: The causal graph.
        holon_hierarchy: Holon hierarchy.

    Returns:
        Validation result dictionary.
    """
    inconsistencies = check_cross_holon_consistency(graph, holon_hierarchy)

    return {
        "passed": len(inconsistencies) == 0,
        "count": len(inconsistencies),
        "inconsistencies": inconsistencies,
        "message": f"{len(inconsistencies)} inconsistency(ies)" if inconsistencies else "Cross-holon consistency OK",
    }


def check_evidence_completeness(parsed_data: dict[str, Any]) -> dict[str, Any]:
    """Check that every mechanism file has at least one DOI source.

    Args:
        parsed_data: Full parsed data.

    Returns:
        Validation result dictionary.
    """
    missing_evidence: list[str] = []

    for mech_id, data in parsed_data.get("mechanisms_raw", {}).items():
        fm = data.get("frontmatter", {})
        sources = fm.get("sources", [])

        has_doi = False
        for source in sources:
            if isinstance(source, dict) and source.get("doi"):
                has_doi = True
                break
            elif isinstance(source, str) and "doi:" in source.lower():
                has_doi = True
                break

        if not has_doi:
            missing_evidence.append(mech_id)

    return {
        "passed": len(missing_evidence) == 0,
        "count": len(missing_evidence),
        "missing_evidence": missing_evidence,
        "message": f"{len(missing_evidence)} mechanism(s) missing DOI sources" if missing_evidence else "All mechanisms have DOI sources",
    }


def check_bidirectional_links(parsed_data: dict[str, Any]) -> dict[str, Any]:
    """Check that mechanism edges are mentioned in their source/target node files.

    If mechanism A→B exists, check that B's node file mentions it in
    "Upstream Causes" and A's file mentions it in "Downstream Effects".

    Args:
        parsed_data: Full parsed data.

    Returns:
        Validation result dictionary.
    """
    missing_references: list[dict] = []

    mechanisms = parsed_data.get("mechanisms_raw", {})
    nodes = parsed_data.get("nodes_raw", {})

    for mech_id, mech_data in mechanisms.items():
        fm = mech_data.get("frontmatter", {})
        source = fm.get("source", "")
        target = fm.get("target", "")

        # Check if target node mentions this mechanism
        if target in nodes:
            target_wikilinks = nodes[target].get("wikilinks", [])
            if mech_id not in target_wikilinks:
                missing_references.append({
                    "mechanism": mech_id,
                    "node": target,
                    "expected_in": "Upstream Causes",
                })

        # Check if source node mentions this mechanism
        if source in nodes:
            source_wikilinks = nodes[source].get("wikilinks", [])
            if mech_id not in source_wikilinks:
                missing_references.append({
                    "mechanism": mech_id,
                    "node": source,
                    "expected_in": "Downstream Effects",
                })

    return {
        "passed": len(missing_references) == 0,
        "count": len(missing_references),
        "missing_references": missing_references[:30],  # Limit output
        "message": f"{len(missing_references)} missing bidirectional reference(s)" if missing_references else "All bidirectional references present",
    }


def generate_validation_report(results: dict[str, Any]) -> str:
    """Generate a markdown validation report.

    Args:
        results: Results from run_full_validation().

    Returns:
        Markdown-formatted report string.
    """
    lines = ["# Vault Validation Report\n"]

    summary = results.get("summary", {})
    lines.append(f"**Total checks**: {summary.get('total_checks', 0)}")
    lines.append(f"**Passed**: {summary.get('passed', 0)}")
    lines.append(f"**Failed**: {summary.get('failed', 0)}")
    lines.append(f"**Pass rate**: {summary.get('pass_rate', 0):.0%}\n")

    for check_name, check_result in results.items():
        if check_name == "summary":
            continue

        status = "PASS" if check_result.get("passed", False) else "FAIL"
        message = check_result.get("message", "")

        lines.append(f"## {check_name.replace('_', ' ').title()}")
        lines.append(f"**Status**: {status}")
        lines.append(f"**Details**: {message}\n")

        # Add specific details for failures
        if not check_result.get("passed", False):
            if "violations" in check_result:
                for v in check_result["violations"][:10]:
                    lines.append(f"  - {v['file']} ({v['category']}): missing {v['missing_fields']}")
            if "dangling_links" in check_result and check_result["dangling_links"]:
                for dl in check_result["dangling_links"][:10]:
                    lines.append(f"  - {dl}")
            if "orphan_nodes" in check_result and check_result["orphan_nodes"]:
                for on in check_result["orphan_nodes"]:
                    lines.append(f"  - {on}")
            if "inconsistencies" in check_result and check_result["inconsistencies"]:
                for ic in check_result["inconsistencies"][:10]:
                    lines.append(f"  - {ic}")
            if "missing_evidence" in check_result and check_result["missing_evidence"]:
                for me in check_result["missing_evidence"]:
                    lines.append(f"  - {me}")
            if "missing_references" in check_result and check_result["missing_references"]:
                for mr in check_result["missing_references"][:10]:
                    lines.append(f"  - {mr['mechanism']} not found in {mr['node']} ({mr['expected_in']})")
            if "expected_feedback_cycles" in check_result and check_result["expected_feedback_cycles"]:
                lines.append("\n  Expected feedback cycles:")
                for cycle in check_result["expected_feedback_cycles"]:
                    lines.append(f"  - {' → '.join(cycle)}")
            if "unexpected_cycles" in check_result and check_result["unexpected_cycles"]:
                lines.append("\n  Unexpected cycles:")
                for cycle in check_result["unexpected_cycles"]:
                    lines.append(f"  - {' → '.join(cycle)}")

        lines.append("")

    return "\n".join(lines)
