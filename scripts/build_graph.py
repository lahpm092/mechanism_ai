#!/usr/bin/env python3
"""CLI: Parse vault and export graph JSON + HTML visualizations.

Usage:
    python scripts/build_graph.py --vault ./vault --output ./outputs
"""

import json
import sys
from pathlib import Path

import click


@click.command()
@click.option("--vault", default="./vault", help="Path to the vault directory.")
@click.option("--output", default="./outputs", help="Path to the output directory.")
def main(vault: str, output: str) -> None:
    """Parse the markdown vault and generate graph artifacts."""
    # Add project root to path
    project_root = str(Path(__file__).parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from engine.parser import parse_vault, export_graph_json
    from engine.visualizer import (
        generate_full_graph_visualization,
        generate_holon_map,
    )

    vault_path = Path(vault).resolve()
    output_path = Path(output).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    click.echo(f"Parsing vault at: {vault_path}")
    parsed_data = parse_vault(str(vault_path))

    metadata = parsed_data["metadata"]
    click.echo(f"  Nodes: {metadata['total_nodes']}")
    click.echo(f"  Causal edges: {metadata['total_causal_edges']}")
    click.echo(f"  Reference edges: {metadata['total_reference_edges']}")
    click.echo(f"  Holons: {metadata['total_holons']}")

    if metadata["dangling_links"]:
        click.echo(f"  Dangling links: {len(metadata['dangling_links'])}")
    if metadata["orphan_nodes"]:
        click.echo(f"  Orphan nodes: {len(metadata['orphan_nodes'])}")

    # Export graph JSON
    json_path = output_path / "graph.json"
    click.echo(f"\nExporting graph JSON to: {json_path}")
    export_graph_json(parsed_data, str(json_path))

    # Generate interactive graph visualization
    graph_html = output_path / "graph_interactive.html"
    click.echo(f"Generating interactive graph: {graph_html}")
    generate_full_graph_visualization(
        parsed_data["graph"],
        str(graph_html),
        parsed_files=parsed_data["parsed_files"],
    )

    # Generate holon map
    holon_html = output_path / "holon_map.html"
    click.echo(f"Generating holon map: {holon_html}")
    generate_holon_map(
        parsed_data["graph"],
        parsed_data["holon_hierarchy"],
        str(holon_html),
    )

    click.echo("\nBuild complete.")
    click.echo(f"  Graph JSON: {json_path}")
    click.echo(f"  Interactive graph: {graph_html}")
    click.echo(f"  Holon map: {holon_html}")


if __name__ == "__main__":
    main()
