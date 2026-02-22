"""Visualizer: generates interactive HTML graph visualizations.

Creates interactive, color-coded network visualizations of the causal graph,
holon hierarchy, and intervention cascades. Nodes and edges are clickable
to display their full markdown content in a side panel.
"""

import html
import json
from pathlib import Path
from typing import Any

import networkx as nx


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
    parsed_files: dict[str, dict] | None = None,
) -> str:
    """Generate an interactive HTML visualization of the full causal graph.

    Nodes are colored by scale, edges by relationship type, edge thickness
    by evidence strength, and node size by degree centrality. Clicking a
    node or edge displays its full markdown content in a side panel.

    Args:
        graph: The causal graph.
        output_path: Path to write the HTML file.
        title: Title for the visualization.
        parsed_files: Optional dict of parsed vault files (id -> {content, frontmatter, ...}).

    Returns:
        Path to the generated HTML file.
    """
    parsed_files = parsed_files or {}

    centrality = nx.degree_centrality(graph) if graph.number_of_nodes() > 0 else {}

    # Build vis.js nodes array
    vis_nodes = []
    for node_id, attrs in graph.nodes(data=True):
        scale = attrs.get("scale", "unknown")
        node_type = attrs.get("type", "unknown")
        color = SCALE_COLORS.get(scale, SCALE_COLORS["unknown"])
        cent = centrality.get(node_id, 0)
        has_edges = graph.in_degree(node_id) > 0 or graph.out_degree(node_id) > 0

        if has_edges:
            size = 15 + cent * 70
            border_width = 2
            border_color = color
            dashes = False
            opacity = 1.0
        else:
            size = 12
            border_width = 2
            border_color = "#888"
            dashes = True
            opacity = 0.7

        hover_parts = [
            f"<b>{node_id}</b>",
            f"Type: {node_type}",
            f"Scale: {scale}",
        ]
        if not has_edges:
            hover_parts.append("<i>(no causal edges — click for details)</i>")
        hover_title = "<br>".join(hover_parts)

        vis_nodes.append({
            "id": node_id,
            "label": node_id,
            "title": hover_title,
            "color": {
                "background": color,
                "border": border_color,
                "highlight": {"background": color, "border": "#333"},
            },
            "size": size,
            "shape": "dot",
            "font": {"size": 12, "color": "#333"},
            "borderWidth": border_width,
            "opacity": opacity,
            "shapeProperties": {"borderDashes": [5, 5] if dashes else False},
        })

    # Build vis.js edges array
    vis_edges = []
    for idx, (u, v, attrs) in enumerate(graph.edges(data=True)):
        relationship = attrs.get("relationship", "unknown")
        evidence = attrs.get("evidence_strength", "unknown")
        color = RELATIONSHIP_COLORS.get(relationship, RELATIONSHIP_COLORS["unknown"])
        width = EVIDENCE_WIDTH.get(evidence, 1)
        edge_id = attrs.get("id", f"edge-{idx}")

        hover_parts = [
            f"<b>{u} → {v}</b>",
            f"Relationship: {relationship}",
            f"Evidence: {evidence}",
        ]
        hover_title = "<br>".join(hover_parts)

        vis_edges.append({
            "id": edge_id,
            "from": u,
            "to": v,
            "title": hover_title,
            "color": {"color": color, "highlight": "#333"},
            "width": width,
            "arrows": "to",
            "smooth": {"type": "curvedCW", "roundness": 0.15},
            "_mechanism_id": edge_id,
        })

    # Build content lookup: node_id/mechanism_id -> markdown text
    content_map: dict[str, str] = {}
    for file_id, file_data in parsed_files.items():
        raw = file_data.get("content", "")
        fm = file_data.get("frontmatter", {})
        # Reconstruct frontmatter + content for display
        if fm:
            fm_lines = ["---"]
            for k, v in fm.items():
                fm_lines.append(f"{k}: {_yaml_value(v)}")
            fm_lines.append("---")
            full_text = "\n".join(fm_lines) + "\n\n" + raw
        else:
            full_text = raw
        content_map[file_id] = full_text

    # Serialize data for embedding
    nodes_json = json.dumps(vis_nodes, indent=None)
    edges_json = json.dumps(vis_edges, indent=None)
    content_json = json.dumps(content_map, indent=None)

    html_content = _build_full_html(title, nodes_json, edges_json, content_json)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")

    return str(output_path)


def _yaml_value(v: Any) -> str:
    """Format a value for display in YAML-like frontmatter."""
    if isinstance(v, list):
        if not v:
            return "[]"
        if all(isinstance(i, str) for i in v):
            return "[" + ", ".join(v) + "]"
        return json.dumps(v)
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    return str(v)


def _build_full_html(
    title: str,
    nodes_json: str,
    edges_json: str,
    content_json: str,
) -> str:
    """Build the complete standalone HTML file."""
    escaped_title = html.escape(title)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{escaped_title}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css"/>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; overflow: hidden; height: 100vh; background: #f8f9fa; }}
#header {{ height: 48px; background: #1a1a2e; color: #fff; display: flex; align-items: center; padding: 0 20px; font-size: 16px; font-weight: 600; }}
#main {{ display: flex; height: calc(100vh - 48px); }}
#graph-container {{ flex: 1; position: relative; }}
#mynetwork {{ width: 100%; height: 100%; }}
#panel {{ width: 0; overflow: hidden; transition: width 0.25s ease; border-left: 1px solid #ddd; background: #fff; display: flex; flex-direction: column; }}
#panel.open {{ width: 520px; }}
#panel-header {{ display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid #eee; background: #fafbfc; min-height: 48px; }}
#panel-header h3 {{ font-size: 14px; color: #333; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
#panel-close {{ cursor: pointer; background: none; border: 1px solid #ccc; border-radius: 4px; padding: 2px 8px; font-size: 18px; color: #666; }}
#panel-close:hover {{ background: #eee; }}
#panel-body {{ flex: 1; overflow-y: auto; padding: 16px; }}
#panel-body pre {{ white-space: pre-wrap; word-wrap: break-word; font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; font-size: 13px; line-height: 1.6; color: #24292e; }}
#panel-body .frontmatter {{ background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px; padding: 12px; margin-bottom: 16px; font-size: 12px; color: #586069; }}
#panel-body .md-content {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; line-height: 1.7; color: #24292e; }}
#panel-body .md-content h1 {{ font-size: 22px; font-weight: 700; margin: 0 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid #e1e4e8; }}
#panel-body .md-content h2 {{ font-size: 17px; font-weight: 600; margin: 20px 0 8px 0; padding-bottom: 4px; border-bottom: 1px solid #eee; color: #333; }}
#panel-body .md-content p {{ margin: 8px 0; }}
#panel-body .md-content a {{ color: #0366d6; text-decoration: none; }}
#panel-body .md-content a:hover {{ text-decoration: underline; }}
#panel-body .md-content code {{ background: #f6f8fa; padding: 2px 6px; border-radius: 3px; font-size: 12px; }}
#legend {{ position: absolute; top: 10px; right: 10px; background: rgba(255,255,255,0.95); border: 1px solid #ddd; border-radius: 6px; padding: 12px; font-size: 11px; z-index: 10; max-width: 180px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
#legend h4 {{ margin: 0 0 6px; font-size: 12px; }}
#legend p {{ margin: 1px 0; }}
#legend hr {{ margin: 4px 0; border: none; border-top: 1px solid #eee; }}
.hint {{ position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.7); color: #fff; padding: 6px 16px; border-radius: 20px; font-size: 12px; pointer-events: none; transition: opacity 0.5s; }}
</style>
</head>
<body>
<div id="header">{escaped_title}</div>
<div id="main">
  <div id="graph-container">
    <div id="mynetwork"></div>
    <div id="legend">
      <h4>Legend</h4>
      <p><b>Node Color = Scale</b></p>
      <p><span style="color:#4A90D9">&#9679;</span> Molecular</p>
      <p><span style="color:#27AE60">&#9679;</span> Cellular</p>
      <p><span style="color:#E67E22">&#9679;</span> Tissue</p>
      <p><span style="color:#E74C3C">&#9679;</span> Organ</p>
      <p><span style="color:#8E44AD">&#9679;</span> System</p>
      <p><span style="color:#F1C40F">&#9679;</span> Signal</p>
      <p><span style="color:#BDC3C7">&#9679;</span> No edges (orphan)</p>
      <hr>
      <p><b>Edge Color = Relationship</b></p>
      <p><span style="color:#27AE60">&#8594;</span> Stimulates / Activates</p>
      <p><span style="color:#E74C3C">&#8594;</span> Inhibits</p>
      <p><span style="color:#95A5A6">&#8594;</span> Modulates</p>
      <hr>
      <p><b>Edge Width = Evidence</b></p>
      <p>Thick = Strong &middot; Thin = Weak</p>
      <hr>
      <p style="color:#888; margin-top:4px;">Click node or edge to read</p>
    </div>
    <div class="hint" id="hint">Click any node or edge to view its full markdown</div>
  </div>
  <div id="panel">
    <div id="panel-header">
      <h3 id="panel-title">Details</h3>
      <button id="panel-close" title="Close">&times;</button>
    </div>
    <div id="panel-body"></div>
  </div>
</div>

<script>
// --- Data ---
var nodesData = {nodes_json};
var edgesData = {edges_json};
var contentMap = {content_json};

// --- Build edge lookup: "source->target" -> mechanism_id ---
var edgeLookup = {{}};
edgesData.forEach(function(e) {{
  edgeLookup[e.id] = e._mechanism_id;
}});

// --- Create network ---
var container = document.getElementById('mynetwork');
var data = {{
  nodes: new vis.DataSet(nodesData),
  edges: new vis.DataSet(edgesData)
}};
var options = {{
  physics: {{
    barnesHut: {{
      gravitationalConstant: -3000,
      centralGravity: 0.3,
      springLength: 200,
      springConstant: 0.01,
      damping: 0.09,
      avoidOverlap: 0.2
    }},
    stabilization: {{ iterations: 200 }}
  }},
  interaction: {{
    hover: true,
    tooltipDelay: 200,
    navigationButtons: true,
    keyboard: true
  }},
  edges: {{
    smooth: {{ type: 'curvedCW', roundness: 0.15 }}
  }}
}};
var network = new vis.Network(container, data, options);

// --- Panel logic ---
var panel = document.getElementById('panel');
var panelTitle = document.getElementById('panel-title');
var panelBody = document.getElementById('panel-body');
var panelClose = document.getElementById('panel-close');
var hint = document.getElementById('hint');

// Hide hint after first click
var hintVisible = true;
function hideHint() {{
  if (hintVisible) {{
    hint.style.opacity = '0';
    hintVisible = false;
    setTimeout(function() {{ hint.style.display = 'none'; }}, 500);
  }}
}}

function openPanel(id, label) {{
  hideHint();
  var md = contentMap[id];
  if (!md) {{
    panelTitle.textContent = label || id;
    panelBody.innerHTML = '<p style="color:#999">No markdown file found for <b>' + (label || id) + '</b></p>';
    panel.classList.add('open');
    return;
  }}
  panelTitle.textContent = label || id;
  panelBody.innerHTML = renderMarkdown(md);
  panel.classList.add('open');
  panelBody.scrollTop = 0;
}}

function closePanel() {{
  panel.classList.remove('open');
}}

panelClose.addEventListener('click', closePanel);

// Click on node
network.on('click', function(params) {{
  if (params.nodes.length > 0) {{
    var nodeId = params.nodes[0];
    openPanel(nodeId, nodeId);
  }} else if (params.edges.length > 0) {{
    var edgeId = params.edges[0];
    var mechId = edgeLookup[edgeId] || edgeId;
    openPanel(mechId, mechId);
  }} else {{
    closePanel();
  }}
}});

// Click on canvas background closes panel
network.on('deselectNode', closePanel);
network.on('deselectEdge', closePanel);

// --- Minimal markdown renderer ---
function renderMarkdown(text) {{
  // Split frontmatter from content
  var parts = text.split(/^---$/m);
  var fmHtml = '';
  var bodyText = text;

  if (parts.length >= 3 && text.trimStart().startsWith('---')) {{
    var fm = parts[1].trim();
    bodyText = parts.slice(2).join('---').trim();
    fmHtml = '<div class="frontmatter"><pre>' + escapeHtml(fm) + '</pre></div>';
  }}

  // Convert markdown to HTML (lightweight)
  var lines = bodyText.split('\\n');
  var html = '';
  var inParagraph = false;

  for (var i = 0; i < lines.length; i++) {{
    var line = lines[i];

    // Headers
    if (/^### (.+)/.test(line)) {{
      if (inParagraph) {{ html += '</p>'; inParagraph = false; }}
      html += '<h3>' + processInline(line.replace(/^### /, '')) + '</h3>';
      continue;
    }}
    if (/^## (.+)/.test(line)) {{
      if (inParagraph) {{ html += '</p>'; inParagraph = false; }}
      html += '<h2>' + processInline(line.replace(/^## /, '')) + '</h2>';
      continue;
    }}
    if (/^# (.+)/.test(line)) {{
      if (inParagraph) {{ html += '</p>'; inParagraph = false; }}
      html += '<h1>' + processInline(line.replace(/^# /, '')) + '</h1>';
      continue;
    }}

    // Blank line
    if (line.trim() === '') {{
      if (inParagraph) {{ html += '</p>'; inParagraph = false; }}
      continue;
    }}

    // List items
    if (/^\\s*[-*]\\s+/.test(line)) {{
      if (inParagraph) {{ html += '</p>'; inParagraph = false; }}
      html += '<p style="margin:2px 0 2px 16px">' + processInline(line.replace(/^\\s*[-*]\\s+/, '&#8226; ')) + '</p>';
      continue;
    }}

    // Regular text
    if (!inParagraph) {{
      html += '<p>';
      inParagraph = true;
    }} else {{
      html += ' ';
    }}
    html += processInline(line);
  }}
  if (inParagraph) html += '</p>';

  return fmHtml + '<div class="md-content">' + html + '</div>';
}}

function processInline(text) {{
  // Escape HTML first
  text = escapeHtml(text);
  // Bold
  text = text.replace(/\\*\\*(.+?)\\*\\*/g, '<b>$1</b>');
  // Italic
  text = text.replace(/\\*(.+?)\\*/g, '<i>$1</i>');
  // Wikilinks: [[target]] or [[target|display]]
  text = text.replace(/\\[\\[([^\\]]+?)\\|([^\\]]+?)\\]\\]/g, function(_, target, display) {{
    return '<a href="#" onclick="openPanel(\\'' + target.trim().toLowerCase().replace(/ /g, '-') + '\\', \\'' + display.trim() + '\\'); return false;">' + display.trim() + '</a>';
  }});
  text = text.replace(/\\[\\[([^\\]]+?)\\]\\]/g, function(_, target) {{
    var id = target.trim().toLowerCase().replace(/ /g, '-');
    return '<a href="#" onclick="openPanel(\\'' + id + '\\', \\'' + target.trim() + '\\'); return false;">' + target.trim() + '</a>';
  }});
  // Inline code
  text = text.replace(/`(.+?)`/g, '<code>$1</code>');
  return text;
}}

function escapeHtml(text) {{
  var div = document.createElement('div');
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}}

// Fade out hint after 5 seconds
setTimeout(function() {{
  if (hintVisible) {{
    hint.style.opacity = '0';
    setTimeout(function() {{ hint.style.display = 'none'; hintVisible = false; }}, 500);
  }}
}}, 5000);
</script>
</body>
</html>"""


def generate_holon_map(
    graph: nx.DiGraph,
    holon_hierarchy: dict[str, dict],
    output_path: str,
    title: str = "Holon Hierarchy Map",
    parsed_files: dict[str, dict] | None = None,
) -> str:
    """Generate a visualization showing holon-level structure.

    Each holon is shown as a large node, with inter-holon connections
    shown as edges between them. Clicking a holon shows its markdown.

    Args:
        graph: The causal graph.
        holon_hierarchy: Holon hierarchy from the parser.
        output_path: Path to write the HTML file.
        title: Title for the visualization.
        parsed_files: Optional dict of parsed vault files.

    Returns:
        Path to the generated HTML file.
    """
    from pyvis.network import Network as PyvisNetwork

    net = PyvisNetwork(
        height="700px",
        width="100%",
        directed=True,
        notebook=False,
        bgcolor="#FFFFFF",
        font_color="#333333",
    )

    net.heading = title
    net.barnes_hut(gravity=-5000, spring_length=300)

    level_colors = {
        "system": "#8E44AD",
        "organ": "#E74C3C",
        "cellular": "#27AE60",
        "molecular": "#4A90D9",
    }

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
    from pyvis.network import Network as PyvisNetwork

    if title is None:
        title = f"Intervention Cascade: do({intervention_node} = increase)"

    net = PyvisNetwork(
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
            color = "#3498DB"
            size = 40
        elif node_id in effects:
            color = EFFECT_COLORS.get(effects[node_id], EFFECT_COLORS["no_change"])
            size = 30
        else:
            color = "#ECF0F1"
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
