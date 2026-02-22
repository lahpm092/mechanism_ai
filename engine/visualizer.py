"""Visualizer: generates interactive HTML graph visualizations using pyvis.

Creates interactive, color-coded network visualizations of the causal graph,
holon hierarchy, and intervention cascades.
"""

from pathlib import Path
from typing import Any

import networkx as nx
from pyvis.network import Network


# Color schemes
SCALE_COLORS: dict[str, str] = {
    "molecular": "#4A90D9",      # blue
    "cellular": "#27AE60",       # green
    "tissue": "#E67E22",         # orange
    "organ": "#E74C3C",          # red
    "system": "#8E44AD",         # purple
    "process": "#95A5A6",        # gray
    "signal": "#F1C40F",         # yellow
    "unknown": "#BDC3C7",        # light gray
}

RELATIONSHIP_COLORS: dict[str, str] = {
    "stimulates": "#27AE60",
    "activates": "#27AE60",
    "upregulates": "#2ECC71",
    "converts_to": "#27AE60",
    "inhibits": "#E74C3C",
    "degrades": "#C0392B",
    "downregulates": "#E74C3C",
    "modulates": "#95A5A6",
    "unknown": "#BDC3C7",
}

EVIDENCE_WIDTH: dict[str, int] = {
    "strong": 4,
    "moderate": 2,
    "weak": 1,
    "contested": 1,
    "unknown": 1,
}

EFFECT_COLORS: dict[str, str] = {
    "increase": "#27AE60",
    "decrease": "#E74C3C",
    "modulate": "#95A5A6",
    "no_change": "#BDC3C7",
}


def generate_full_graph_visualization(
    graph: nx.DiGraph,
    output_path: str,
    title: str = "Causal Metagraph: HPA Axis & Immune System",
) -> str:
    """Generate an interactive HTML visualization of the full causal graph.

    Nodes are colored by scale, edges by relationship type, edge thickness
    by evidence strength, and node size by degree centrality.

    Args:
        graph: The causal graph.
        output_path: Path to write the HTML file.
        title: Title for the visualization.

    Returns:
        Path to the generated HTML file.
    """
    net = Network(
        height="900px",
        width="100%",
        directed=True,
        notebook=False,
        bgcolor="#FFFFFF",
        font_color="#333333",
    )

    net.heading = title
    net.barnes_hut(
        gravity=-3000,
        central_gravity=0.3,
        spring_length=200,
        spring_strength=0.01,
        damping=0.09,
    )

    # Calculate degree centrality for node sizing
    centrality = nx.degree_centrality(graph) if graph.number_of_nodes() > 0 else {}

    # Add nodes
    for node_id, attrs in graph.nodes(data=True):
        scale = attrs.get("scale", "unknown")
        node_type = attrs.get("type", "unknown")
        color = SCALE_COLORS.get(scale, SCALE_COLORS["unknown"])

        # Size based on degree centrality (min 15, max 50)
        cent = centrality.get(node_id, 0)
        size = 15 + cent * 70

        # Build hover title
        hover_parts = [
            f"<b>{node_id}</b>",
            f"Type: {node_type}",
            f"Scale: {scale}",
        ]
        aliases = attrs.get("aliases", [])
        if aliases:
            hover_parts.append(f"Aliases: {', '.join(aliases)}")
        holon_membership = attrs.get("holon_membership", [])
        if holon_membership:
            hover_parts.append(f"Holons: {', '.join(holon_membership)}")
        confidence = attrs.get("confidence", 0)
        hover_parts.append(f"Confidence: {confidence}")
        hover_title = "<br>".join(hover_parts)

        net.add_node(
            node_id,
            label=node_id,
            title=hover_title,
            color=color,
            size=size,
            shape="dot",
            font={"size": 12},
        )

    # Add edges
    for u, v, attrs in graph.edges(data=True):
        relationship = attrs.get("relationship", "unknown")
        evidence = attrs.get("evidence_strength", "unknown")
        color = RELATIONSHIP_COLORS.get(relationship, RELATIONSHIP_COLORS["unknown"])
        width = EVIDENCE_WIDTH.get(evidence, 1)

        # Build hover title
        edge_parts = [
            f"<b>{u} → {v}</b>",
            f"Relationship: {relationship}",
            f"Evidence: {evidence}",
        ]
        mech_type = attrs.get("mechanism_type", "")
        if mech_type:
            edge_parts.append(f"Mechanism: {mech_type}")
        context = attrs.get("context", "")
        if context:
            edge_parts.append(f"Context: {context}")
        edge_id = attrs.get("id", "")
        if edge_id:
            edge_parts.append(f"ID: {edge_id}")

        net.add_edge(
            u, v,
            title="<br>".join(edge_parts),
            color=color,
            width=width,
            arrows="to",
        )

    # Add legend as HTML
    legend_html = _build_legend_html()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    net.save_graph(str(output_path))

    # Inject legend into the HTML
    _inject_legend(str(output_path), legend_html)

    return str(output_path)


def generate_holon_map(
    graph: nx.DiGraph,
    holon_hierarchy: dict[str, dict],
    output_path: str,
    title: str = "Holon Hierarchy Map",
) -> str:
    """Generate a visualization showing holon-level structure.

    Each holon is shown as a large node, with inter-holon connections
    shown as edges between them.

    Args:
        graph: The causal graph.
        holon_hierarchy: Holon hierarchy from the parser.
        output_path: Path to write the HTML file.
        title: Title for the visualization.

    Returns:
        Path to the generated HTML file.
    """
    net = Network(
        height="700px",
        width="100%",
        directed=True,
        notebook=False,
        bgcolor="#FFFFFF",
        font_color="#333333",
    )

    net.heading = title
    net.barnes_hut(gravity=-5000, spring_length=300)

    # Hierarchy level colors
    level_colors = {
        "system": "#8E44AD",
        "organ": "#E74C3C",
        "cellular": "#27AE60",
        "molecular": "#4A90D9",
    }

    # Add holon nodes
    for holon_id, info in holon_hierarchy.items():
        scale = info.get("scale", "unknown")
        color = level_colors.get(scale, "#95A5A6")
        n_internal = len(info.get("internal_nodes", []))
        n_edges = len(info.get("internal_edges", []))

        hover = "<br>".join([
            f"<b>{holon_id}</b>",
            f"Scale: {scale}",
            f"Internal nodes: {n_internal}",
            f"Internal edges: {n_edges}",
            f"Inputs: {', '.join(info.get('inputs', []))}",
            f"Outputs: {', '.join(info.get('outputs', []))}",
        ])

        net.add_node(
            holon_id,
            label=holon_id,
            title=hover,
            color=color,
            size=30 + n_internal * 3,
            shape="box",
            font={"size": 14, "face": "arial"},
        )

    # Add hierarchy edges (parent-child)
    for holon_id, info in holon_hierarchy.items():
        parent = info.get("parent")
        if parent and parent in holon_hierarchy:
            net.add_edge(
                parent, holon_id,
                color="#BDC3C7",
                width=2,
                dashes=True,
                title="contains",
            )

    # Add inter-holon causal connections
    # Find edges that cross holon boundaries
    node_to_holon: dict[str, set[str]] = {}
    for holon_id, info in holon_hierarchy.items():
        for node_id in info.get("internal_nodes", []):
            if node_id not in node_to_holon:
                node_to_holon[node_id] = set()
            node_to_holon[node_id].add(holon_id)

    inter_holon_edges: set[tuple[str, str]] = set()
    for u, v, data in graph.edges(data=True):
        u_holons = node_to_holon.get(u, set())
        v_holons = node_to_holon.get(v, set())

        for uh in u_holons:
            for vh in v_holons:
                if uh != vh:
                    inter_holon_edges.add((uh, vh))

    for source_holon, target_holon in inter_holon_edges:
        if source_holon in holon_hierarchy and target_holon in holon_hierarchy:
            net.add_edge(
                source_holon, target_holon,
                color="#E67E22",
                width=3,
                arrows="to",
                title=f"Cross-holon causal connection: {source_holon} → {target_holon}",
            )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    net.save_graph(str(output_path))

    return str(output_path)


def generate_intervention_visualization(
    graph: nx.DiGraph,
    intervention_node: str,
    effects: dict[str, str],
    output_path: str,
    title: str | None = None,
) -> str:
    """Generate a visualization highlighting an intervention cascade.

    Colors nodes by predicted effect direction and highlights causal paths.

    Args:
        graph: The causal graph.
        intervention_node: The node being intervened on.
        effects: Dictionary mapping node IDs to predicted effects.
        output_path: Path to write the HTML file.
        title: Optional title for the visualization.

    Returns:
        Path to the generated HTML file.
    """
    if title is None:
        title = f"Intervention Cascade: do({intervention_node} = increase)"

    net = Network(
        height="800px",
        width="100%",
        directed=True,
        notebook=False,
        bgcolor="#FFFFFF",
        font_color="#333333",
    )

    net.heading = title
    net.barnes_hut(gravity=-3000, spring_length=200)

    affected_nodes = set(effects.keys()) | {intervention_node}

    for node_id, attrs in graph.nodes(data=True):
        if node_id == intervention_node:
            color = "#3498DB"  # Bright blue for intervention target
            size = 40
        elif node_id in effects:
            color = EFFECT_COLORS.get(effects[node_id], EFFECT_COLORS["no_change"])
            size = 30
        else:
            color = "#ECF0F1"  # Very light for unaffected
            size = 15

        hover = f"<b>{node_id}</b><br>"
        if node_id == intervention_node:
            hover += "INTERVENTION TARGET"
        elif node_id in effects:
            hover += f"Predicted effect: {effects[node_id]}"
        else:
            hover += "Not affected"

        net.add_node(
            node_id,
            label=node_id,
            title=hover,
            color=color,
            size=size,
            shape="dot",
        )

    for u, v, attrs in graph.edges(data=True):
        if u in affected_nodes and v in affected_nodes:
            relationship = attrs.get("relationship", "unknown")
            color = RELATIONSHIP_COLORS.get(relationship, "#95A5A6")
            width = 3
        else:
            color = "#ECF0F1"
            width = 1

        net.add_edge(u, v, color=color, width=width, arrows="to")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    net.save_graph(str(output_path))

    return str(output_path)


def _build_legend_html() -> str:
    """Build HTML for the graph legend."""
    legend = """
    <div id="graph-legend" style="position: absolute; top: 10px; right: 10px;
         background: white; border: 1px solid #ccc; border-radius: 5px;
         padding: 10px; font-family: Arial; font-size: 12px; z-index: 1000;
         max-width: 200px;">
      <h4 style="margin: 0 0 8px 0;">Legend</h4>
      <p style="margin: 2px 0;"><b>Node Colors (Scale):</b></p>
      <p style="margin: 1px 0;"><span style="color: #4A90D9;">●</span> Molecular</p>
      <p style="margin: 1px 0;"><span style="color: #27AE60;">●</span> Cellular</p>
      <p style="margin: 1px 0;"><span style="color: #E67E22;">●</span> Tissue</p>
      <p style="margin: 1px 0;"><span style="color: #E74C3C;">●</span> Organ</p>
      <p style="margin: 1px 0;"><span style="color: #8E44AD;">●</span> System</p>
      <p style="margin: 1px 0;"><span style="color: #F1C40F;">●</span> Signal</p>
      <hr style="margin: 5px 0;">
      <p style="margin: 2px 0;"><b>Edge Colors (Relationship):</b></p>
      <p style="margin: 1px 0;"><span style="color: #27AE60;">→</span> Stimulates/Activates</p>
      <p style="margin: 1px 0;"><span style="color: #E74C3C;">→</span> Inhibits</p>
      <p style="margin: 1px 0;"><span style="color: #95A5A6;">→</span> Modulates</p>
      <hr style="margin: 5px 0;">
      <p style="margin: 2px 0;"><b>Edge Width (Evidence):</b></p>
      <p style="margin: 1px 0;">Thick = Strong</p>
      <p style="margin: 1px 0;">Medium = Moderate</p>
      <p style="margin: 1px 0;">Thin = Weak</p>
    </div>
    """
    return legend


def _inject_legend(html_path: str, legend_html: str) -> None:
    """Inject legend HTML into a pyvis-generated HTML file."""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Insert legend before closing body tag
        content = content.replace("</body>", f"{legend_html}\n</body>")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception:
        pass  # Non-critical: visualization still works without legend
