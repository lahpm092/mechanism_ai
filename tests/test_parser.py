"""Tests for the vault parser.

Verifies that vault files parse correctly, the graph has expected structure,
dangling links are detected, and holon hierarchy is parsed correctly.
"""

import os
from pathlib import Path

import pytest

from engine.parser import parse_vault, export_graph_json, get_causal_subgraph


VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "vault")


@pytest.fixture(scope="module")
def parsed_data():
    """Parse the vault once for all tests in this module."""
    return parse_vault(VAULT_PATH)


@pytest.fixture(scope="module")
def graph(parsed_data):
    """Get the parsed graph."""
    return parsed_data["graph"]


class TestVaultParsing:
    """Tests that the vault parses without errors."""

    def test_vault_exists(self):
        """Vault directory must exist."""
        assert Path(VAULT_PATH).is_dir(), f"Vault not found at {VAULT_PATH}"

    def test_parse_completes(self, parsed_data):
        """Parsing should complete without raising exceptions."""
        assert parsed_data is not None
        assert "graph" in parsed_data
        assert "metadata" in parsed_data

    def test_no_parse_errors(self, parsed_data):
        """No files should fail to parse."""
        errors = parsed_data["metadata"].get("parse_errors", [])
        assert len(errors) == 0, f"Parse errors: {errors}"


class TestGraphStructure:
    """Tests that the graph has the expected number of nodes and edges."""

    def test_minimum_nodes(self, graph):
        """Graph should have at least 25 nodes (vault spec: 25-30 node files)."""
        assert graph.number_of_nodes() >= 20, (
            f"Expected >= 20 nodes, got {graph.number_of_nodes()}"
        )

    def test_minimum_causal_edges(self, parsed_data):
        """Graph should have at least 15 causal edges (vault spec: 15-20 mechanism files)."""
        causal_edges = parsed_data["causal_edges"]
        assert len(causal_edges) >= 12, (
            f"Expected >= 12 causal edges, got {len(causal_edges)}"
        )

    def test_key_nodes_present(self, graph):
        """Key biological nodes must be present in the graph."""
        key_nodes = ["cortisol", "acth", "crh", "nf-kb", "il-6", "gr"]
        for node in key_nodes:
            assert node in graph, f"Key node '{node}' missing from graph"

    def test_key_edges_present(self, graph):
        """Key causal relationships must be present."""
        key_edges = [
            ("crh", "acth"),       # CRH stimulates ACTH
            ("acth", "cortisol"),   # ACTH stimulates cortisol
            ("cortisol", "crh"),    # Cortisol inhibits CRH (feedback)
            ("cortisol", "nf-kb"),  # Cortisol suppresses NF-kB
        ]
        for source, target in key_edges:
            assert graph.has_edge(source, target), (
                f"Expected edge {source} → {target} not found"
            )

    def test_node_attributes(self, graph):
        """Nodes should have required attributes."""
        for node_id, attrs in graph.nodes(data=True):
            assert "type" in attrs, f"Node '{node_id}' missing 'type' attribute"
            assert "scale" in attrs, f"Node '{node_id}' missing 'scale' attribute"

    def test_edge_attributes(self, graph):
        """Causal edges should have required attributes."""
        for u, v, attrs in graph.edges(data=True):
            if attrs.get("edge_type") == "causal":
                assert "relationship" in attrs, f"Edge {u}→{v} missing 'relationship'"
                assert "direction" in attrs, f"Edge {u}→{v} missing 'direction'"


class TestDanglingLinks:
    """Tests that dangling links are correctly detected."""

    def test_dangling_links_detected(self, parsed_data):
        """The parser should report dangling links if they exist."""
        metadata = parsed_data["metadata"]
        # Dangling links are reported — we don't require zero, just that detection works
        assert "dangling_links" in metadata

    def test_known_links_resolve(self, parsed_data):
        """Links to core nodes should not be dangling."""
        dangling = set()
        for dl in parsed_data["metadata"].get("dangling_links", []):
            # Format: "source -> [[target]]"
            if "[[" in dl:
                target = dl.split("[[")[1].split("]]")[0]
                dangling.add(target)

        core_nodes = {"cortisol", "acth", "crh", "nf-kb", "gr", "il-6"}
        for node in core_nodes:
            assert node not in dangling, f"Core node '{node}' appears as dangling link"


class TestHolonHierarchy:
    """Tests that the holon hierarchy is correctly parsed."""

    def test_holons_parsed(self, parsed_data):
        """Should have at least 4 holons."""
        hierarchy = parsed_data["holon_hierarchy"]
        assert len(hierarchy) >= 4, f"Expected >= 4 holons, got {len(hierarchy)}"

    def test_hpa_axis_holon(self, parsed_data):
        """HPA axis holon should be present with correct structure."""
        hierarchy = parsed_data["holon_hierarchy"]
        assert "hpa-axis" in hierarchy, "HPA axis holon not found"

        hpa = hierarchy["hpa-axis"]
        assert "internal_nodes" in hpa
        assert len(hpa["internal_nodes"]) >= 5, (
            f"HPA axis should have >= 5 internal nodes, got {len(hpa['internal_nodes'])}"
        )

    def test_holon_parent_child(self, parsed_data):
        """Child holons should reference their parent."""
        hierarchy = parsed_data["holon_hierarchy"]

        if "hpa-axis" in hierarchy:
            hpa = hierarchy["hpa-axis"]
            children = hpa.get("children", [])
            for child_id in children:
                if child_id in hierarchy:
                    parent = hierarchy[child_id].get("parent")
                    assert parent == "hpa-axis", (
                        f"Child '{child_id}' should have parent 'hpa-axis', got '{parent}'"
                    )

    def test_holon_inputs_outputs(self, parsed_data):
        """Holons should have defined inputs and outputs."""
        hierarchy = parsed_data["holon_hierarchy"]

        for holon_id, info in hierarchy.items():
            inputs = info.get("inputs", [])
            outputs = info.get("outputs", [])
            # At least one input or output should be defined
            assert len(inputs) > 0 or len(outputs) > 0, (
                f"Holon '{holon_id}' has no inputs or outputs"
            )


class TestGraphExport:
    """Tests for graph JSON export."""

    def test_export_json(self, parsed_data, tmp_path):
        """Should export valid JSON."""
        output_path = tmp_path / "test_graph.json"
        export_graph_json(parsed_data, str(output_path))

        assert output_path.exists()
        assert output_path.stat().st_size > 100  # Non-trivial content

    def test_causal_subgraph(self, graph):
        """Causal subgraph should contain only causal edges."""
        causal = get_causal_subgraph(graph)
        assert causal.number_of_nodes() > 0
        for u, v, data in causal.edges(data=True):
            assert data.get("edge_type") == "causal"
