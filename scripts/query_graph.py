#!/usr/bin/env python3
"""CLI: Run causal queries on the parsed graph.

Usage:
    python scripts/query_graph.py --d-sep cortisol il-6 --given stress-signal
    python scripts/query_graph.py --intervention cortisol increase
    python scripts/query_graph.py --paths stress-signal il-6 --max-length 5
    python scripts/query_graph.py --backdoor cortisol nf-kb
    python scripts/query_graph.py --confounders cortisol il-6
"""

import json
import sys
from pathlib import Path

import click


@click.command()
@click.option("--vault", default="./vault", help="Path to the vault directory.")
@click.option("--d-sep", nargs=2, type=str, default=None, help="Test d-separation between two nodes.")
@click.option("--given", multiple=True, help="Conditioning set for d-separation (can repeat).")
@click.option("--intervention", nargs=2, type=str, default=None, help="Simulate intervention: NODE DIRECTION.")
@click.option("--paths", nargs=2, type=str, default=None, help="Find all causal paths between two nodes.")
@click.option("--max-length", default=5, type=int, help="Maximum path length for path queries.")
@click.option("--backdoor", nargs=2, type=str, default=None, help="Find backdoor adjustment set.")
@click.option("--confounders", nargs=2, type=str, default=None, help="Find confounders between two nodes.")
@click.option("--mediators", nargs=2, type=str, default=None, help="Find mediators between two nodes.")
def main(vault, d_sep, given, intervention, paths, max_length, backdoor, confounders, mediators):
    """Run causal queries on the parsed vault graph."""
    project_root = str(Path(__file__).parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from engine.parser import parse_vault
    from engine.causal_engine import (
        d_separated,
        find_all_causal_paths,
        find_backdoor_adjustment_set,
        find_confounders as find_confounders_fn,
        find_mediators as find_mediators_fn,
        simulate_intervention,
    )

    click.echo("Parsing vault...")
    parsed_data = parse_vault(vault)
    graph = parsed_data["graph"]
    click.echo(f"Graph loaded: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges\n")

    if d_sep:
        x, y = d_sep
        z = set(given) if given else set()
        click.echo(f"D-Separation Test: {x} ⊥ {y} | {z if z else '∅'}")
        try:
            result = d_separated(graph, x, y, z)
            status = "d-separated (independent)" if result else "d-connected (dependent)"
            click.echo(f"Result: {status}")
        except ValueError as e:
            click.echo(f"Error: {e}")

    elif intervention:
        node, direction = intervention
        click.echo(f"Intervention Simulation: do({node} = {direction})")
        effects = simulate_intervention(graph, node, direction)
        if effects:
            click.echo(f"\nPredicted downstream effects:")
            for target_node, effect in sorted(effects.items()):
                click.echo(f"  {target_node}: {effect}")
        else:
            click.echo("No downstream effects predicted (node may not exist).")

    elif paths:
        source, target = paths
        click.echo(f"Causal Paths: {source} → {target} (max length: {max_length})")
        found_paths = find_all_causal_paths(graph, source, target, max_length)
        if found_paths:
            click.echo(f"\n{len(found_paths)} path(s) found:")
            for i, path in enumerate(found_paths, 1):
                click.echo(f"  {i}. {' → '.join(path)}")
        else:
            click.echo("No paths found.")

    elif backdoor:
        treatment, outcome = backdoor
        click.echo(f"Backdoor Criterion: {treatment} → {outcome}")
        try:
            adj_sets = find_backdoor_adjustment_set(graph, treatment, outcome)
            if adj_sets is not None:
                click.echo(f"\n{len(adj_sets)} valid adjustment set(s):")
                for i, adj_set in enumerate(adj_sets, 1):
                    if adj_set:
                        click.echo(f"  {i}. {{{', '.join(adj_set)}}}")
                    else:
                        click.echo(f"  {i}. ∅ (no adjustment needed)")
            else:
                click.echo("Effect is NOT identifiable via backdoor adjustment.")
        except ValueError as e:
            click.echo(f"Error: {e}")

    elif confounders:
        x, y = confounders
        click.echo(f"Confounders: {x} ← ? → {y}")
        found = find_confounders_fn(graph, x, y)
        if found:
            click.echo(f"\n{len(found)} confounder(s):")
            for c in found:
                click.echo(f"  - {c}")
        else:
            click.echo("No confounders found.")

    elif mediators:
        treatment, outcome = mediators
        click.echo(f"Mediators: {treatment} → ? → {outcome}")
        found = find_mediators_fn(graph, treatment, outcome)
        if found:
            click.echo(f"\n{len(found)} mediator(s):")
            for m in found:
                click.echo(f"  - {m}")
        else:
            click.echo("No mediators found.")

    else:
        click.echo("No query specified. Use --help for options.")


if __name__ == "__main__":
    main()
