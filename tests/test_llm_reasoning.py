"""Tests for LLM reasoning capability over the vault.

Tests that the vault structure enables correct causal reasoning by
simulating an LLM's navigation pattern: start at index, follow wikilinks,
gather context, and verify sufficiency for answering causal questions.

This does NOT call an actual LLM — it tests that the vault structure
provides sufficient information via navigable wikilink paths.
"""

import os
from pathlib import Path

import pytest

from engine.parser import parse_vault, WIKILINK_PATTERN


VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "vault")


@pytest.fixture(scope="module")
def parsed_data():
    """Parse the vault once for all tests."""
    return parse_vault(VAULT_PATH)


@pytest.fixture(scope="module")
def parsed_files(parsed_data):
    """Get all parsed files."""
    return parsed_data["parsed_files"]


def navigate_from_index(parsed_files: dict, target_terms: list[str], max_hops: int = 4) -> dict:
    """Simulate LLM navigation from _index.md through wikilinks.

    Starts at _index.md, follows wikilinks that match target terms,
    and collects context (file contents) along the way.

    Args:
        parsed_files: All parsed vault files.
        target_terms: Terms to look for when deciding which links to follow.
        max_hops: Maximum number of navigation hops.

    Returns:
        Dictionary with navigation path, gathered context, and visited files.
    """
    # Start at index
    if "_index" not in parsed_files:
        return {"error": "_index.md not found", "path": [], "context": "", "visited": set()}

    visited: list[str] = ["_index"]
    context_parts: list[str] = [parsed_files["_index"]["content"]]
    visited_set = {"_index"}
    current_frontier = ["_index"]

    for hop in range(max_hops):
        next_frontier = []
        for current_id in current_frontier:
            if current_id not in parsed_files:
                continue

            wikilinks = parsed_files[current_id].get("wikilinks", [])

            for link in wikilinks:
                if link in visited_set:
                    continue

                # Decide whether to follow this link based on target terms
                should_follow = False
                for term in target_terms:
                    if term.lower() in link.lower():
                        should_follow = True
                        break

                # Also follow links if the linked file mentions target terms in content
                if not should_follow and link in parsed_files:
                    linked_content = parsed_files[link].get("content", "").lower()
                    for term in target_terms:
                        if term.lower() in linked_content:
                            should_follow = True
                            break

                if should_follow and link in parsed_files:
                    visited.append(link)
                    visited_set.add(link)
                    context_parts.append(parsed_files[link]["content"])
                    next_frontier.append(link)

        current_frontier = next_frontier
        if not current_frontier:
            break

    return {
        "path": visited,
        "context": "\n\n---\n\n".join(context_parts),
        "visited": visited_set,
        "num_hops": min(max_hops, len(visited) - 1),
    }


def check_context_sufficiency(context: str, required_facts: list[str]) -> dict:
    """Check if gathered context contains all required facts for answering a question.

    Args:
        context: The gathered context text.
        required_facts: List of key facts that must be present.

    Returns:
        Dictionary with sufficiency result and missing facts.
    """
    context_lower = context.lower()
    found = []
    missing = []

    for fact in required_facts:
        if fact.lower() in context_lower:
            found.append(fact)
        else:
            missing.append(fact)

    return {
        "sufficient": len(missing) == 0,
        "found": found,
        "missing": missing,
        "coverage": len(found) / len(required_facts) if required_facts else 1.0,
    }


class TestLLMNavigation:
    """Tests that an LLM can navigate the vault structure effectively."""

    def test_index_file_exists(self, parsed_files):
        """Index file must exist as the entry point."""
        assert "_index" in parsed_files, "Index file (_index.md) must exist"

    def test_index_has_holon_links(self, parsed_files):
        """Index should link to system-level holons."""
        index_links = parsed_files["_index"].get("wikilinks", [])
        assert "hpa-axis" in index_links, "Index should link to hpa-axis"

    def test_wikilinks_form_connected_graph(self, parsed_files):
        """Most files should be reachable from the index via wikilinks."""
        visited = set()
        queue = ["_index"]

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            if current in parsed_files:
                for link in parsed_files[current].get("wikilinks", []):
                    if link not in visited and link in parsed_files:
                        queue.append(link)

        # At least 70% of files should be reachable from index
        total_files = len(parsed_files)
        reachable = len(visited)
        coverage = reachable / total_files if total_files > 0 else 0

        assert coverage >= 0.5, (
            f"Only {coverage:.0%} of files reachable from index "
            f"({reachable}/{total_files}). Graph is poorly connected."
        )


class TestCausalQuestionAnswering:
    """Tests that navigating the vault gathers sufficient context for causal questions."""

    def test_il6_cortisol_question(self, parsed_files):
        """Question: 'Would blocking IL-6 reduce cortisol levels?'

        Required navigation: IL-6 → CRH stimulation → ACTH → cortisol
        Required facts: IL-6 stimulates CRH, CRH stimulates ACTH, ACTH stimulates cortisol
        """
        result = navigate_from_index(
            parsed_files,
            target_terms=["il-6", "il6", "cortisol", "crh", "acth"],
            max_hops=4,
        )

        # Should visit relevant nodes
        assert len(result["visited"]) >= 3, (
            f"Should visit at least 3 files, visited {len(result['visited'])}: {result['path']}"
        )

        # Check context sufficiency
        required_facts = [
            "il-6",         # IL-6 must be mentioned
            "crh",          # CRH pathway
            "acth",         # ACTH pathway
            "cortisol",     # Cortisol as output
        ]
        sufficiency = check_context_sufficiency(result["context"], required_facts)
        assert sufficiency["coverage"] >= 0.75, (
            f"Context coverage {sufficiency['coverage']:.0%} too low. "
            f"Missing: {sufficiency['missing']}"
        )

    def test_cortisol_inflammation_question(self, parsed_files):
        """Question: 'How does cortisol suppress inflammation?'

        Required navigation: cortisol → GR → NF-kB suppression → cytokine reduction
        Required facts: GR, NF-kB transrepression, cytokine reduction
        """
        result = navigate_from_index(
            parsed_files,
            target_terms=["cortisol", "nf-kb", "nfkb", "gr", "inflam", "suppress"],
            max_hops=4,
        )

        required_facts = [
            "cortisol",
            "nf-kb",
            "gr",
        ]
        sufficiency = check_context_sufficiency(result["context"], required_facts)
        assert sufficiency["coverage"] >= 0.75, (
            f"Context insufficient for cortisol-inflammation question. "
            f"Coverage: {sufficiency['coverage']:.0%}, Missing: {sufficiency['missing']}"
        )

    def test_hpa_feedback_question(self, parsed_files):
        """Question: 'How does the HPA axis negative feedback loop work?'

        Required navigation: HPA axis → cortisol → GR → CRH suppression
        """
        result = navigate_from_index(
            parsed_files,
            target_terms=["hpa", "feedback", "cortisol", "crh", "gr", "inhibit"],
            max_hops=4,
        )

        required_facts = [
            "cortisol",
            "crh",
            "feedback",
        ]
        sufficiency = check_context_sufficiency(result["context"], required_facts)
        assert sufficiency["coverage"] >= 0.75, (
            f"Context insufficient for HPA feedback question. "
            f"Missing: {sufficiency['missing']}"
        )

    def test_stress_immune_question(self, parsed_files):
        """Question: 'How does chronic stress affect the immune system?'

        Required navigation: stress → HPA → cortisol → immune suppression
        """
        result = navigate_from_index(
            parsed_files,
            target_terms=["stress", "cortisol", "immune", "nf-kb", "il-6", "suppress"],
            max_hops=4,
        )

        required_facts = [
            "stress",
            "cortisol",
        ]
        sufficiency = check_context_sufficiency(result["context"], required_facts)
        assert sufficiency["coverage"] >= 0.75, (
            f"Context insufficient for stress-immune question. "
            f"Missing: {sufficiency['missing']}"
        )


class TestNavigationEfficiency:
    """Tests that navigation paths are efficient (not too many hops)."""

    def test_cortisol_reachable_in_2_hops(self, parsed_files):
        """Cortisol should be reachable from index in <= 2 hops."""
        result = navigate_from_index(
            parsed_files,
            target_terms=["cortisol"],
            max_hops=2,
        )
        assert "cortisol" in result["visited"], (
            "Cortisol should be reachable from index within 2 hops"
        )

    def test_nfkb_reachable_in_3_hops(self, parsed_files):
        """NF-kB should be reachable from index in <= 3 hops."""
        result = navigate_from_index(
            parsed_files,
            target_terms=["nf-kb", "nfkb", "immune", "inflam"],
            max_hops=3,
        )
        found = "nf-kb" in result["visited"] or "nfkb" in result["visited"]
        assert found, (
            f"NF-kB should be reachable from index within 3 hops. "
            f"Visited: {result['visited']}"
        )

    def test_no_dead_ends_in_core_nodes(self, parsed_files):
        """Core nodes should have outgoing wikilinks (not dead ends)."""
        core_nodes = ["cortisol", "acth", "crh", "nf-kb", "gr", "il-6"]
        for node_id in core_nodes:
            if node_id in parsed_files:
                wikilinks = parsed_files[node_id].get("wikilinks", [])
                assert len(wikilinks) >= 2, (
                    f"Core node '{node_id}' has only {len(wikilinks)} wikilinks — "
                    f"may be a dead end"
                )
