"""
visualizer.py
=============
Creates multiple visualizations of the student social network using Matplotlib.
Also exports the graph to GEXF format for Gephi.
"""

import os
import math
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for file saving
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np


# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

COMMUNITY_COLORS = [
    "#E74C3C",  # Red
    "#2ECC71",  # Green
    "#3498DB",  # Blue
    "#F39C12",  # Orange
    "#9B59B6",  # Purple
    "#1ABC9C",  # Teal
    "#E67E22",  # Carrot
    "#34495E",  # Dark grey
]


def _get_color(idx: int) -> str:
    return COMMUNITY_COLORS[idx % len(COMMUNITY_COLORS)]


# ---------------------------------------------------------------------------
# Main plotting functions
# ---------------------------------------------------------------------------

def plot_network(
    G: nx.Graph,
    communities: dict = None,
    centrality: dict = None,
    title: str = "Student Social Network",
    save_path: str = None,
) -> None:
    """
    Draw the social network graph.

    - Nodes are coloured by community (if provided).
    - Node size is proportional to degree centrality (if provided).
    - Uses spring_layout for positioning.

    Parameters
    ----------
    G           : nx.Graph
    communities : dict, optional
        Mapping node -> community_id.
    centrality  : dict, optional
        Dictionary from compute_all_centrality(); uses 'degree' key.
    title       : str
    save_path   : str, optional
        If given, save the figure to this path.
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    pos = nx.spring_layout(G, seed=42, k=2.5 / math.sqrt(G.number_of_nodes()))

    # Node colours
    if communities:
        node_colors = [_get_color(communities.get(n, 0)) for n in G.nodes()]
    else:
        node_colors = ["#3498DB"] * G.number_of_nodes()

    # Node sizes based on degree centrality
    if centrality and "degree" in centrality:
        deg_dict = dict(centrality["degree"])
        base = 800
        node_sizes = [base + deg_dict.get(n, 0) * 3000 for n in G.nodes()]
    else:
        node_sizes = [600] * G.number_of_nodes()

    # Edge widths proportional to weight
    edge_weights = [G[u][v].get("weight", 1) for u, v in G.edges()]
    max_w = max(edge_weights) if edge_weights else 1
    edge_widths = [0.5 + 2.0 * (w / max_w) for w in edge_weights]

    nx.draw_networkx_edges(
        G, pos, ax=ax,
        width=edge_widths,
        alpha=0.4,
        edge_color="#aaaaaa",
    )
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=node_colors,
        node_size=node_sizes,
        alpha=0.92,
        linewidths=1.5,
        edgecolors="white",
    )

    # Labels: show short name
    labels = {}
    for n in G.nodes():
        name = G.nodes[n].get("name", n)
        short = name.split()[0] if name else n
        labels[n] = f"{n}\n{short}"

    nx.draw_networkx_labels(
        G, pos, labels=labels, ax=ax,
        font_size=6.5,
        font_color="white",
        font_weight="bold",
    )

    # Legend for communities
    if communities:
        unique_cids = sorted(set(communities.values()))
        patches = [
            mpatches.Patch(color=_get_color(cid), label=f"Community {cid + 1}")
            for cid in unique_cids
        ]
        legend = ax.legend(
            handles=patches,
            loc="upper left",
            fontsize=9,
            framealpha=0.8,
            facecolor="#1a1a2e",
            edgecolor="white",
            labelcolor="white",
        )

    ax.set_title(title, fontsize=16, fontweight="bold", color="white", pad=20)
    ax.axis("off")
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def plot_centrality_comparison(centrality_data: dict, save_path: str = None) -> None:
    """
    Plot horizontal bar charts (top 10 nodes) for four centrality measures
    arranged in a 2×2 subplot grid.

    Parameters
    ----------
    centrality_data : dict
        Dictionary from compute_all_centrality().
    save_path : str, optional
    """
    measures = [
        ("degree",      "Degree Centrality",      "#3498DB"),
        ("betweenness", "Betweenness Centrality",  "#E74C3C"),
        ("closeness",   "Closeness Centrality",    "#2ECC71"),
        ("pagerank",    "PageRank",                "#F39C12"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.patch.set_facecolor("#1a1a2e")
    fig.suptitle("Centrality Measures Comparison (Top 10 Nodes)",
                 fontsize=16, fontweight="bold", color="white", y=1.01)

    for ax, (key, label, color) in zip(axes.flat, measures):
        data = centrality_data.get(key, [])[:10]
        if not data:
            ax.axis("off")
            continue

        nodes  = [item[0] for item in reversed(data)]
        scores = [item[1] for item in reversed(data)]

        bars = ax.barh(nodes, scores, color=color, alpha=0.85, edgecolor="white", linewidth=0.5)
        ax.set_facecolor("#16213e")
        ax.set_title(label, fontsize=12, fontweight="bold", color="white")
        ax.tick_params(colors="white", labelsize=9)
        ax.spines[:].set_color("#444444")
        ax.set_xlabel("Score", color="#cccccc", fontsize=9)

        # Value labels on bars
        for bar, score in zip(bars, scores):
            ax.text(
                bar.get_width() + 0.002,
                bar.get_y() + bar.get_height() / 2,
                f"{score:.4f}",
                va="center",
                fontsize=7,
                color="white",
            )

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def plot_degree_distribution(G: nx.Graph, save_path: str = None) -> None:
    """
    Plot the degree distribution of the graph as a histogram.

    Parameters
    ----------
    G         : nx.Graph
    save_path : str, optional
    """
    degrees = [d for _, d in G.degree()]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    bins = range(min(degrees), max(degrees) + 2)
    n, _, patches = ax.hist(degrees, bins=bins, color="#3498DB", edgecolor="white",
                            linewidth=0.8, alpha=0.85, align="left")

    # Colour bars by frequency
    max_count = max(n)
    for patch, count in zip(patches, n):
        intensity = count / max_count if max_count > 0 else 0
        patch.set_facecolor(plt.cm.cool(0.2 + 0.8 * intensity))

    ax.set_title("Degree Distribution of Student Network",
                 fontsize=14, fontweight="bold", color="white")
    ax.set_xlabel("Degree (Number of Connections)", color="#cccccc", fontsize=11)
    ax.set_ylabel("Number of Students", color="#cccccc", fontsize=11)
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#444444")

    # Annotations
    avg_deg = sum(degrees) / len(degrees)
    ax.axvline(avg_deg, color="#E74C3C", linestyle="--", linewidth=2,
               label=f"Mean = {avg_deg:.2f}")
    ax.legend(facecolor="#1a1a2e", edgecolor="white", labelcolor="white")

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def plot_community_sizes(communities: dict, save_path: str = None) -> None:
    """
    Plot a bar chart showing the number of members in each community.

    Parameters
    ----------
    communities : dict
        Mapping node -> community_id.
    save_path   : str, optional
    """
    groups: dict = {}
    for node, cid in communities.items():
        groups.setdefault(cid, []).append(node)

    sorted_cids  = sorted(groups.keys())
    labels       = [f"Community {cid + 1}" for cid in sorted_cids]
    sizes        = [len(groups[cid]) for cid in sorted_cids]
    colors       = [_get_color(cid) for cid in sorted_cids]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    bars = ax.bar(labels, sizes, color=colors, edgecolor="white", linewidth=1.0, alpha=0.88)

    for bar, size in zip(bars, sizes):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.15,
            str(size),
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
            color="white",
        )

    ax.set_title("Community Size Distribution",
                 fontsize=14, fontweight="bold", color="white")
    ax.set_xlabel("Community", color="#cccccc", fontsize=11)
    ax.set_ylabel("Number of Members", color="#cccccc", fontsize=11)
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#444444")
    ax.set_ylim(0, max(sizes) + 3)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def export_to_gephi(
    G: nx.Graph,
    communities: dict,
    centrality_data: dict,
    save_path: str,
) -> None:
    """
    Export the graph to GEXF format, attaching community and centrality
    scores as node attributes for use in Gephi.

    Parameters
    ----------
    G               : nx.Graph
    communities     : dict
        Mapping node -> community_id.
    centrality_data : dict
        Dictionary from compute_all_centrality().
    save_path       : str
        Destination .gexf file path.
    """
    # Build lookup dicts from centrality data
    deg_d = dict(centrality_data.get("degree",      []))
    bet_d = dict(centrality_data.get("betweenness", []))
    clo_d = dict(centrality_data.get("closeness",   []))
    eig_d = dict(centrality_data.get("eigenvector", []))
    pgr_d = dict(centrality_data.get("pagerank",    []))

    # Enrich node attributes
    for node in G.nodes():
        G.nodes[node]["community"]           = int(communities.get(node, -1))
        G.nodes[node]["degree_centrality"]   = float(round(deg_d.get(node, 0), 6))
        G.nodes[node]["betweenness"]         = float(round(bet_d.get(node, 0), 6))
        G.nodes[node]["closeness"]           = float(round(clo_d.get(node, 0), 6))
        G.nodes[node]["eigenvector"]         = float(round(eig_d.get(node, 0), 6))
        G.nodes[node]["pagerank"]            = float(round(pgr_d.get(node, 0), 6))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    nx.write_gexf(G, save_path)
