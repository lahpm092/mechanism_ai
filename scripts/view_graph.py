#!/usr/bin/env python3
"""Terminal graph viewer for the causal metagraph.

Usage:
    python scripts/view_graph.py
    python scripts/view_graph.py --vault ./vault
    python scripts/view_graph.py --node cortisol
    python scripts/view_graph.py --edge crh-stimulates-acth
"""

import sys
from pathlib import Path

import click

project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.rule import Rule

console = Console()

SCALE_STYLES = {
    "molecular":  "bold blue",
    "cellular":   "bold green",
    "tissue":     "bold yellow",
    "organ":      "bold red",
    "system":     "bold magenta",
    "process":    "bold white",
    "signal":     "bold yellow",
    "unknown":    "dim white",
}

REL_STYLES = {
    "stimulates":   "green",
    "activates":    "green",
    "upregulates":  "bright_green",
    "converts_to":  "green",
    "inhibits":     "red",
    "degrades":     "bright_red",
    "downregulates":"red",
    "modulates":    "yellow",
    "unknown":      "dim white",
}

EVIDENCE_CHARS = {
    "strong":   "████",
    "moderate": "███░",
    "weak":     "██░░",
    "contested":"█░░░",
    "unknown":  "░░░░",
}


def _load(vault: str):
    from engine.parser import parse_vault
    with console.status("[bold cyan]Parsing vault…"):
        data = parse_vault(vault)
    return data


def _show_overview(data: dict) -> None:
    meta = data["metadata"]
    graph = data["graph"]

    import networkx as nx
    centrality = nx.degree_centrality(graph)

    # ── Stats panel ──────────────────────────────────────────────────────────
    stats = Table.grid(padding=(0, 2))
    stats.add_column(style="bold cyan")
    stats.add_column()
    stats.add_row("Nodes",          str(meta["total_nodes"]))
    stats.add_row("Causal edges",   str(meta["total_causal_edges"]))
    stats.add_row("Ref edges",      str(meta["total_reference_edges"]))
    stats.add_row("Holons",         str(meta["total_holons"]))
    stats.add_row("Orphan nodes",   str(len(meta.get("orphan_nodes", []))))
    stats.add_row("Dangling links", str(len(meta.get("dangling_links", []))))
    console.print(Panel(stats, title="[bold]Causal Metagraph Overview", border_style="cyan"))

    # ── Nodes table ──────────────────────────────────────────────────────────
    nt = Table(
        title="Nodes",
        box=box.SIMPLE_HEAVY,
        show_lines=False,
        expand=True,
    )
    nt.add_column("ID",          style="bold white", no_wrap=True)
    nt.add_column("Scale",       no_wrap=True)
    nt.add_column("Type",        no_wrap=True)
    nt.add_column("Degree",      justify="right")
    nt.add_column("Edges",       no_wrap=True)

    for node_id in sorted(graph.nodes()):
        attrs = graph.nodes[node_id]
        scale = attrs.get("scale", "unknown")
        ntype = attrs.get("type", "unknown")
        deg_in  = graph.in_degree(node_id)
        deg_out = graph.out_degree(node_id)
        total   = deg_in + deg_out
        style   = SCALE_STYLES.get(scale, "white")
        edge_txt = f"↑{deg_in} ↓{deg_out}" if total else "[dim]orphan[/dim]"
        nt.add_row(
            Text(node_id, style=style),
            Text(scale, style=style),
            ntype,
            str(total),
            edge_txt,
        )
    console.print(nt)

    # ── Edges table ──────────────────────────────────────────────────────────
    et = Table(
        title="Causal Edges",
        box=box.SIMPLE_HEAVY,
        show_lines=False,
        expand=True,
    )
    et.add_column("Source",       style="bold white", no_wrap=True)
    et.add_column("",             no_wrap=True, width=3)
    et.add_column("Target",       style="bold white", no_wrap=True)
    et.add_column("Relationship", no_wrap=True)
    et.add_column("Evidence",     no_wrap=True)
    et.add_column("Mechanism ID", style="dim", no_wrap=True)

    for u, v, attrs in sorted(graph.edges(data=True), key=lambda x: (x[0], x[1])):
        rel  = attrs.get("relationship", "unknown")
        evid = attrs.get("evidence_strength", "unknown")
        mid  = attrs.get("id", "")
        rel_style  = REL_STYLES.get(rel, "white")
        evid_bar   = EVIDENCE_CHARS.get(evid, "░░░░")
        et.add_row(
            u,
            Text("→", style=rel_style),
            v,
            Text(rel, style=rel_style),
            f"{evid_bar} {evid}",
            mid,
        )
    console.print(et)

    # ── Holons ───────────────────────────────────────────────────────────────
    ht = Table(title="Holons", box=box.SIMPLE_HEAVY, expand=True)
    ht.add_column("Holon ID",      style="bold magenta", no_wrap=True)
    ht.add_column("Scale",         no_wrap=True)
    ht.add_column("Nodes",         justify="right")
    ht.add_column("Inputs",        no_wrap=True)
    ht.add_column("Outputs",       no_wrap=True)

    for holon_id, info in sorted(data["holon_hierarchy"].items()):
        ht.add_row(
            holon_id,
            info.get("scale", ""),
            str(len(info.get("internal_nodes", []))),
            ", ".join(info.get("inputs", [])),
            ", ".join(info.get("outputs", [])),
        )
    console.print(ht)


def _show_markdown(file_id: str, parsed_files: dict, label: str = "") -> bool:
    """Print the full markdown for a file_id. Returns False if not found."""
    entry = parsed_files.get(file_id)
    if not entry:
        console.print(f"[red]No markdown file found for[/red] [bold]{file_id}[/bold]")
        return False

    title = label or file_id
    fm = entry.get("frontmatter", {})
    content = entry.get("content", "")

    # Frontmatter
    if fm:
        fm_lines = []
        for k, v in fm.items():
            fm_lines.append(f"  {k}: {v}")
        fm_text = "\n".join(fm_lines)
        console.print(Panel(
            Text(fm_text, style="dim cyan"),
            title=f"[bold yellow]Frontmatter — {title}",
            border_style="yellow",
            padding=(0, 1),
        ))

    # Body as rendered markdown
    console.print(Rule(f"[bold white]{title}"))
    console.print(Markdown(content))
    console.print()
    return True


def _interactive_loop(data: dict) -> None:
    """REPL: type a node/edge/holon ID to read its markdown."""
    graph = data["graph"]
    parsed_files = data["parsed_files"]
    all_ids = sorted(parsed_files.keys())

    console.print(Panel(
        "[bold cyan]Commands[/bold cyan]\n"
        "  [bold]<id>[/bold]        — show markdown for node, edge, or holon\n"
        "  [bold]list[/bold]        — list all available IDs\n"
        "  [bold]nodes[/bold]       — list node IDs only\n"
        "  [bold]edges[/bold]       — list edge/mechanism IDs\n"
        "  [bold]overview[/bold]    — show the full graph overview tables\n"
        "  [bold]q / quit[/bold]    — exit",
        title="Terminal Graph Viewer",
        border_style="cyan",
    ))
    _show_overview(data)

    while True:
        try:
            cmd = Prompt.ask("\n[bold green]>[/bold green]").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not cmd:
            continue
        if cmd in ("q", "quit", "exit"):
            break
        if cmd == "overview":
            _show_overview(data)
            continue
        if cmd == "list":
            for i in sorted(all_ids):
                console.print(f"  {i}")
            continue
        if cmd == "nodes":
            for n in sorted(graph.nodes()):
                attrs = graph.nodes[n]
                scale = attrs.get("scale", "unknown")
                style = SCALE_STYLES.get(scale, "white")
                console.print(f"  [{style}]{n}[/{style}]  [dim]{scale}[/dim]")
            continue
        if cmd == "edges":
            for u, v, attrs in sorted(graph.edges(data=True), key=lambda x: x[0]):
                mid = attrs.get("id", f"{u}→{v}")
                rel = attrs.get("relationship", "")
                console.print(f"  [bold]{mid}[/bold]  [dim]{u} → {v}  ({rel})[/dim]")
            continue

        # Try to show markdown
        _show_markdown(cmd, parsed_files, label=cmd)


@click.command()
@click.option("--vault",  default="./vault",  help="Path to vault directory.")
@click.option("--node",   default=None,       help="Show markdown for a specific node ID and exit.")
@click.option("--edge",   default=None,       help="Show markdown for a specific mechanism ID and exit.")
def main(vault: str, node: str | None, edge: str | None) -> None:
    """Interactive terminal viewer for the causal metagraph."""
    vault_path = str(Path(vault).resolve())
    data = _load(vault_path)

    if node:
        _show_markdown(node, data["parsed_files"], label=node)
    elif edge:
        _show_markdown(edge, data["parsed_files"], label=edge)
    else:
        _interactive_loop(data)


if __name__ == "__main__":
    main()
