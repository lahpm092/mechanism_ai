"""Tests for target discovery pipeline.

Tests the GR desensitization disease phenotype scenario and verifies
biologically plausible target ranking and cascade predictions.
"""

import os

import pytest

from engine.parser import parse_vault
from engine.target_discovery import discover_targets, generate_target_report


VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "vault")


@pytest.fixture(scope="module")
def parsed_data():
    """Parse the vault once for all tests."""
    return parse_vault(VAULT_PATH)


@pytest.fixture(scope="module")
def graph(parsed_data):
    """Get the causal graph."""
    return parsed_data["graph"]


@pytest.fixture(scope="module")
def holon_hierarchy(parsed_data):
    """Get the holon hierarchy."""
    return parsed_data["holon_hierarchy"]


class TestGRDesensitizationScenario:
    """Tests the primary disease phenotype scenario: GR desensitization.

    In this scenario, chronic stress leads to GR desensitization, breaking
    the negative feedback loop. This causes:
    - Elevated cortisol (no feedback suppression)
    - Elevated CRH (no feedback suppression)
    - Elevated NF-kB (despite high cortisol, GR can't suppress it)
    - Elevated IL-6, TNF-alpha (NF-kB-driven)
    """

    @pytest.fixture
    def disease_phenotype(self):
        """GR desensitization disease phenotype."""
        return {
            "nf-kb": "elevated",
            "il-6": "elevated",
            "tnf-alpha": "elevated",
            "cortisol": "elevated",
            "crh": "elevated",
            "gr": "desensitized",
        }

    def test_discovers_targets(self, graph, holon_hierarchy, disease_phenotype):
        """Should discover at least one intervention target."""
        targets = discover_targets(graph, disease_phenotype, holon_hierarchy)
        assert len(targets) > 0, "Should discover at least one target"

    def test_gr_is_top_target(self, graph, holon_hierarchy, disease_phenotype):
        """GR should be ranked among top targets (it's the root cause)."""
        targets = discover_targets(graph, disease_phenotype, holon_hierarchy)

        target_ids = [t["target"] for t in targets]
        assert "gr" in target_ids, "GR should be among the discovered targets"

        # GR should be in the top 5
        gr_rank = target_ids.index("gr")
        assert gr_rank < 5, f"GR should be ranked in top 5, got rank {gr_rank + 1}"

    def test_nfkb_is_viable_target(self, graph, holon_hierarchy, disease_phenotype):
        """NF-kB should be a viable target (direct inflammatory suppression)."""
        targets = discover_targets(graph, disease_phenotype, holon_hierarchy)

        target_ids = [t["target"] for t in targets]
        assert "nf-kb" in target_ids, "NF-kB should be among the discovered targets"

    def test_cascade_predictions_plausible(self, graph, holon_hierarchy, disease_phenotype):
        """Predicted cascades should be biologically plausible."""
        targets = discover_targets(graph, disease_phenotype, holon_hierarchy)

        for target in targets[:3]:  # Check top 3
            cascade = target.get("predicted_cascade", {})
            if target["target"] == "nf-kb" and "il-6" in cascade:
                # Inhibiting NF-kB should decrease IL-6
                assert cascade["il-6"] in ("decrease", "modulate"), (
                    f"Inhibiting NF-kB should decrease IL-6, got {cascade['il-6']}"
                )

    def test_affected_holons_identified(self, graph, holon_hierarchy, disease_phenotype):
        """Should identify affected holons for each target."""
        targets = discover_targets(graph, disease_phenotype, holon_hierarchy)

        for target in targets[:3]:
            holons = target.get("affected_holons", [])
            # At least one holon should be affected
            assert len(holons) > 0, (
                f"Target '{target['target']}' should affect at least one holon"
            )

    def test_evidence_strength_reported(self, graph, holon_hierarchy, disease_phenotype):
        """Each target should have an evidence strength rating."""
        targets = discover_targets(graph, disease_phenotype, holon_hierarchy)

        for target in targets:
            assert "evidence_strength" in target
            assert target["evidence_strength"] in ("strong", "moderate", "weak", "insufficient")


class TestSimpleInflammationScenario:
    """Tests a simpler disease phenotype: acute inflammation."""

    @pytest.fixture
    def disease_phenotype(self):
        """Simple inflammation phenotype."""
        return {
            "nf-kb": "elevated",
            "il-6": "elevated",
        }

    def test_discovers_anti_inflammatory_targets(self, graph, holon_hierarchy, disease_phenotype):
        """Should find cortisol-related or NF-kB-targeting interventions."""
        targets = discover_targets(graph, disease_phenotype, holon_hierarchy)
        assert len(targets) > 0


class TestTargetReport:
    """Tests for target report generation."""

    def test_report_generation(self, graph, holon_hierarchy):
        """Should generate a non-empty markdown report."""
        phenotype = {"nf-kb": "elevated", "il-6": "elevated", "gr": "desensitized"}
        targets = discover_targets(graph, phenotype, holon_hierarchy)
        report = generate_target_report(targets, phenotype)

        assert len(report) > 200, "Report should be substantial"
        assert "# Target Discovery Report" in report
        assert "nf-kb" in report.lower()

    def test_report_has_all_sections(self, graph, holon_hierarchy):
        """Report should have disease phenotype and candidate sections."""
        phenotype = {"nf-kb": "elevated"}
        targets = discover_targets(graph, phenotype, holon_hierarchy)
        report = generate_target_report(targets, phenotype)

        assert "Disease Phenotype" in report
        assert "Candidate Targets" in report
