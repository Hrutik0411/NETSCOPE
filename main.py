#!/usr/bin/env python3
"""
Social Network Analysis System
Community Detection & Influential User Identification
College Mini Project

Run:  python main.py
"""

import os
import sys
import time

# Force UTF-8 output on Windows so box-drawing characters render correctly
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Path setup – allow running from any working directory
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

EDGES_PATH  = os.path.join(BASE_DIR, "data", "student_edges.csv")
NODES_PATH  = os.path.join(BASE_DIR, "data", "student_nodes.csv")
GRAPHS_DIR  = os.path.join(BASE_DIR, "output", "graphs")
GEPHI_DIR   = os.path.join(BASE_DIR, "output", "gephi")

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from src.graph_builder       import load_graph, get_basic_stats, print_stats
from src.centrality          import compute_all_centrality, identify_influential_users
from src.community_detection import (
    detect_communities_louvain,
    detect_communities_greedy,
    detect_communities_label_propagation,
    print_communities,
    get_community_stats,
)
from src.visualizer import (
    plot_network,
    plot_centrality_comparison,
    plot_degree_distribution,
    plot_community_sizes,
    export_to_gephi,
)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def banner(text: str) -> None:
    width = 64
    print("\n" + "╔" + "═" * width + "╗")
    for line in text.strip().split("\n"):
        print("║  " + line.ljust(width - 2) + "  ║")
    print("╚" + "═" * width + "╝\n")


def step_header(n: int, title: str) -> None:
    print(f"\n{'─' * 66}")
    print(f"  [STEP {n}] {title}")
    print(f"{'─' * 66}")


def tick(msg: str) -> None:
    print(f"  ✓ {msg}")


def info(msg: str) -> None:
    print(f"  → {msg}")


def computing(msg: str) -> None:
    print(f"  ⟳ {msg}", end="", flush=True)


def done() -> None:
    print("  ✓")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    # ── Splash ───────────────────────────────────────────────────────────
    banner(
        "SOCIAL NETWORK ANALYSIS SYSTEM\n"
        "Community Detection & Influential User Identification\n"
        "              College Mini Project"
    )

    start_time = time.time()

    # ════════════════════════════════════════════════════════════════════
    # STEP 1 – Load Data & Build Graph
    # ════════════════════════════════════════════════════════════════════
    step_header(1, "Loading Data & Building Graph")

    print(f"  → Edge data : {EDGES_PATH}")
    print(f"  → Node data : {NODES_PATH}")

    G = load_graph(EDGES_PATH, NODES_PATH)
    tick(f"Loaded {G.number_of_nodes()} nodes (students) and {G.number_of_edges()} edges (friendships)")

    # ════════════════════════════════════════════════════════════════════
    # STEP 2 – Basic Network Statistics
    # ════════════════════════════════════════════════════════════════════
    step_header(2, "Basic Network Statistics")
    stats = get_basic_stats(G)
    print_stats(stats)

    # ════════════════════════════════════════════════════════════════════
    # STEP 3 – Centrality Analysis
    # ════════════════════════════════════════════════════════════════════
    step_header(3, "Centrality Analysis")

    measures = [
        ("Degree Centrality",      "degree"),
        ("Betweenness Centrality", "betweenness"),
        ("Closeness Centrality",   "closeness"),
        ("Eigenvector Centrality", "eigenvector"),
        ("PageRank",               "pagerank"),
    ]

    for label, _ in measures:
        print(f"  ⟳ Computing {label}...", end="\r")

    centrality_data = compute_all_centrality(G)

    for label, _ in measures:
        print(f"  ✓ {label:<32} computed")

    # ════════════════════════════════════════════════════════════════════
    # STEP 4 – Top Influential Users
    # ════════════════════════════════════════════════════════════════════
    step_header(4, "Top 5 Influential Users (by Combined Centrality)")
    identify_influential_users(G, top_n=5)

    # ════════════════════════════════════════════════════════════════════
    # STEP 5 – Community Detection
    # ════════════════════════════════════════════════════════════════════
    step_header(5, "Community Detection")

    node_attrs = dict(G.nodes(data=True))

    # --- Algorithm 1: Greedy Modularity ---
    print("\n  [Algorithm 1] Greedy Modularity Communities (NetworkX built-in)")
    communities_greedy = detect_communities_greedy(G)
    greedy_stats = get_community_stats(G, communities_greedy)
    info(f"Found {greedy_stats['num_communities']} communities  "
         f"│  Modularity: {greedy_stats['modularity']:.4f}  "
         f"│  Sizes: {greedy_stats['sizes']}")
    print_communities(communities_greedy, node_attrs)

    # --- Algorithm 2: Label Propagation ---
    print("\n\n  [Algorithm 2] Label Propagation Communities (NetworkX built-in)")
    communities_lp = detect_communities_label_propagation(G)
    lp_stats = get_community_stats(G, communities_lp)
    info(f"Found {lp_stats['num_communities']} communities  "
         f"│  Modularity: {lp_stats['modularity']:.4f}  "
         f"│  Sizes: {lp_stats['sizes']}")
    print_communities(communities_lp, node_attrs)

    # --- Algorithm 3: Louvain (optional) ---
    print("\n\n  [Algorithm 3] Louvain Method (python-louvain, optional)")
    communities_louvain = detect_communities_louvain(G)
    louvain_stats = get_community_stats(G, communities_louvain)
    info(f"Found {louvain_stats['num_communities']} communities  "
         f"│  Modularity: {louvain_stats['modularity']:.4f}  "
         f"│  Sizes: {louvain_stats['sizes']}")
    print_communities(communities_louvain, node_attrs)

    # Use greedy communities as the "canonical" result for visualisations
    communities = communities_greedy
    comm_stats  = greedy_stats

    # ════════════════════════════════════════════════════════════════════
    # STEP 6 – Visualisations
    # ════════════════════════════════════════════════════════════════════
    step_header(6, "Generating Visualizations")

    os.makedirs(GRAPHS_DIR, exist_ok=True)

    # 6a Network graph
    net_path = os.path.join(GRAPHS_DIR, "network_graph.png")
    plot_network(G, communities=communities, centrality=centrality_data,
                 title="Student Social Network – Community Clusters", save_path=net_path)
    tick(f"Network graph saved      → {os.path.relpath(net_path, BASE_DIR)}")

    # 6b Centrality comparison
    cent_path = os.path.join(GRAPHS_DIR, "centrality_comparison.png")
    plot_centrality_comparison(centrality_data, save_path=cent_path)
    tick(f"Centrality comparison    → {os.path.relpath(cent_path, BASE_DIR)}")

    # 6c Degree distribution
    deg_path = os.path.join(GRAPHS_DIR, "degree_distribution.png")
    plot_degree_distribution(G, save_path=deg_path)
    tick(f"Degree distribution      → {os.path.relpath(deg_path, BASE_DIR)}")

    # 6d Community sizes
    com_path = os.path.join(GRAPHS_DIR, "community_sizes.png")
    plot_community_sizes(communities, save_path=com_path)
    tick(f"Community sizes chart    → {os.path.relpath(com_path, BASE_DIR)}")

    # ════════════════════════════════════════════════════════════════════
    # STEP 7 – Export to Gephi
    # ════════════════════════════════════════════════════════════════════
    step_header(7, "Exporting to Gephi (GEXF format)")

    os.makedirs(GEPHI_DIR, exist_ok=True)
    gexf_path = os.path.join(GEPHI_DIR, "social_network.gexf")
    export_to_gephi(G, communities, centrality_data, save_path=gexf_path)
    tick(f"GEXF file saved          → {os.path.relpath(gexf_path, BASE_DIR)}")
    info("Open Gephi → File → Open → select social_network.gexf")
    info("Then: Run Layout (ForceAtlas2) and apply Partition (community) colouring")

    # ════════════════════════════════════════════════════════════════════
    # STEP 8 – Summary Report
    # ════════════════════════════════════════════════════════════════════
    step_header(8, "Summary Report")

    elapsed = time.time() - start_time

    # Top 3 influential students by degree
    top3_deg = centrality_data["degree"][:3]
    top3_str = ", ".join(
        f"{node}({G.nodes[node].get('name', node).split()[0]})"
        for node, _ in top3_deg
    )

    summary_rows = [
        ("Network Size",             f"{stats['nodes']} students,  {stats['edges']} connections"),
        ("Network Density",          f"{stats['density']} (sparse)"),
        ("Average Connections",      f"{stats['avg_degree']} per student"),
        ("Clustering Coefficient",   str(stats["avg_clustering"])),
        ("Communities Detected",     f"{comm_stats['num_communities']} (Greedy Modularity)"),
        ("Modularity Score",         f"{comm_stats['modularity']:.4f}"),
        ("Top Influential Students", top3_str),
        ("Visualizations Created",   "4 PNG files in output/graphs/"),
        ("Gephi Export",             "output/gephi/social_network.gexf"),
        ("Total Runtime",            f"{elapsed:.2f} seconds"),
    ]

    col1_w = max(len(r[0]) for r in summary_rows) + 2
    col2_w = max(len(r[1]) for r in summary_rows) + 2

    print("  ╔" + "═" * col1_w + "╦" + "═" * col2_w + "╗")
    for i, (label, value) in enumerate(summary_rows):
        lc = f" {label} ".ljust(col1_w)
        vc = f" {value} ".ljust(col2_w)
        print(f"  ║{lc}║{vc}║")
        if i < len(summary_rows) - 1:
            print("  ╠" + "═" * col1_w + "╬" + "═" * col2_w + "╣")
    print("  ╚" + "═" * col1_w + "╩" + "═" * col2_w + "╝")

    print("\n  Analysis complete!  All outputs saved to the output/ directory.\n")
    print("═" * 66 + "\n")


if __name__ == "__main__":
    main()
