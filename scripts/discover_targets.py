#!/usr/bin/env python3
"""CLI: Run the target discovery pipeline.

Usage:
    python scripts/discover_targets.py --phenotype '{"nf-kb": "elevated", "il-6": "elevated", "gr": "desensitized"}' --output ./outputs/target_report.md
"""

import json
import sys
from pathlib import Path

import click


@click.command()
@click.option("--vault", default="./vault", help="Path to the vault directory.")
@click.option("--phenotype", required=True, help="Disease phenotype as JSON dict.")
@click.option("--output", default="./outputs/target_report.md", help="Path for the target report.")
@click.option("--max-depth", default=4, type=int, help="Maximum upstream trace depth.")
def main(vault: str, phenotype: str, output: str, max_depth: int) -> None:
    """Run the target discovery pipeline for a disease phenotype."""
    project_root = str(Path(__file__).parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from engine.parser import parse_vault
    from engine.target_discovery import discover_targets, generate_target_report

    # Parse phenotype JSON
    try:
        disease_phenotype = json.loads(phenotype)
    except json.JSONDecodeError as e:
        click.echo(f"Error parsing phenotype JSON: {e}")
        sys.exit(1)

    if not isinstance(disease_phenotype, dict):
        click.echo("Phenotype must be a JSON object (dict).")
        sys.exit(1)

    vault_path = Path(vault).resolve()
    output_path = Path(output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    click.echo(f"Parsing vault at: {vault_path}")
    parsed_data = parse_vault(str(vault_path))

    graph = parsed_data["graph"]
    holon_hierarchy = parsed_data["holon_hierarchy"]

    click.echo(f"Graph loaded: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    click.echo(f"\nDisease Phenotype:")
    for node, state in disease_phenotype.items():
        in_graph = "found" if node in graph else "NOT FOUND"
        click.echo(f"  {node}: {state} ({in_graph})")

    click.echo(f"\nRunning target discovery (max_depth={max_depth})...")
    targets = discover_targets(graph, disease_phenotype, holon_hierarchy, max_depth=max_depth)

    click.echo(f"\n{len(targets)} candidate target(s) found:")
    for i, target in enumerate(targets[:10], 1):
        click.echo(
            f"  {i}. {target['target']} "
            f"(score: {target['composite_score']:.2f}, "
            f"intervention: {target['intervention']}, "
            f"evidence: {target['evidence_strength']})"
        )

    # Generate and save report
    report = generate_target_report(targets, disease_phenotype)
    output_path.write_text(report, encoding="utf-8")
    click.echo(f"\nFull report saved to: {output_path}")


if __name__ == "__main__":
    main()
