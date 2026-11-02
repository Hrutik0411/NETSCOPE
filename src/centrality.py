"""
centrality.py
=============
Compute various centrality measures on the student social network.
Provides helpers to rank and display the most influential users.
"""

import networkx as nx


# ---------------------------------------------------------------------------
# Individual centrality helpers
# ---------------------------------------------------------------------------

def degree_centrality(G: nx.Graph) -> list:
    """
    Compute degree centrality for all nodes.

    Returns
    -------
    list of (node, score) tuples sorted descending by score.
    """
    scores = nx.degree_centrality(G)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def betweenness_centrality(G: nx.Graph) -> list:
    """
    Compute betweenness centrality for all nodes.

    Returns
    -------
    list of (node, score) tuples sorted descending by score.
    """
    scores = nx.betweenness_centrality(G, normalized=True, weight="weight")
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def closeness_centrality(G: nx.Graph) -> list:
    """
    Compute closeness centrality for all nodes.

    Returns
    -------
    list of (node, score) tuples sorted descending by score.
    """
    scores = nx.closeness_centrality(G)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def eigenvector_centrality(G: nx.Graph) -> list:
    """
    Compute eigenvector centrality for all nodes.

    Returns
    -------
    list of (node, score) tuples sorted descending by score.
    """
    try:
        scores = nx.eigenvector_centrality(G, max_iter=1000, weight="weight")
    except nx.PowerIterationFailedConvergence:
        scores = {n: 0.0 for n in G.nodes()}
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def pagerank(G: nx.Graph) -> list:
    """
    Compute PageRank for all nodes.

    Returns
    -------
    list of (node, score) tuples sorted descending by score.
    """
    scores = nx.pagerank(G, alpha=0.85, weight="weight")
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# ---------------------------------------------------------------------------
# Aggregate helper
# ---------------------------------------------------------------------------

def compute_all_centrality(G: nx.Graph) -> dict:
    """
    Compute all centrality measures and return them as a single dictionary.

    Returns
    -------
    dict with keys:
        'degree', 'betweenness', 'closeness', 'eigenvector', 'pagerank'
    Each value is a list of (node, score) tuples sorted descending.
    """
    return {
        "degree":       degree_centrality(G),
        "betweenness":  betweenness_centrality(G),
        "closeness":    closeness_centrality(G),
        "eigenvector":  eigenvector_centrality(G),
        "pagerank":     pagerank(G),
    }


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------

def identify_influential_users(G: nx.Graph, top_n: int = 5) -> None:
    """
    Identify and print the top-N most influential users across all
    centrality measures using a formatted ASCII table.

    Parameters
    ----------
    G      : nx.Graph
        The NetworkX graph (nodes should carry a 'name' attribute).
    top_n  : int
        Number of top nodes to display.
    """
    all_c = compute_all_centrality(G)

    # Build lookup dicts for easy access
    deg_d  = dict(all_c["degree"])
    bet_d  = dict(all_c["betweenness"])
    clo_d  = dict(all_c["closeness"])
    eig_d  = dict(all_c["eigenvector"])
    pgr_d  = dict(all_c["pagerank"])

    # Rank nodes by average of normalised scores
    nodes = list(G.nodes())
    avg_scores = {}
    for n in nodes:
        avg_scores[n] = (
            deg_d.get(n, 0)
            + bet_d.get(n, 0)
            + clo_d.get(n, 0)
            + eig_d.get(n, 0)
            + pgr_d.get(n, 0)
        ) / 5.0

    top_nodes = sorted(avg_scores, key=lambda x: avg_scores[x], reverse=True)[:top_n]

    # --- Header row ---
    h0  = " # "
    h1  = " Student ID "
    h2  = " Name                  "
    h3  = " Dept "
    h4  = " Degree  "
    h5  = " Betw.   "
    h6  = " Close.  "
    h7  = " EigVec  "
    h8  = " PageRank"

    def sep_row(ch="╠", v="║", h="═"):
        cols = [len(h0), len(h1), len(h2), len(h3), len(h4), len(h5), len(h6), len(h7), len(h8)]
        parts = [h * c for c in cols]
        return v + (ch + v).join(parts) + v  # inner; wrap with outer ║

    # Rebuild with proper box chars
    col_widths = [len(h0), len(h1), len(h2), len(h3), len(h4), len(h5), len(h6), len(h7), len(h8)]

    def make_top():
        parts = ["═" * w for w in col_widths]
        return "  ╔" + "╦".join(parts) + "╗"

    def make_mid():
        parts = ["═" * w for w in col_widths]
        return "  ╠" + "╬".join(parts) + "╣"

    def make_bot():
        parts = ["═" * w for w in col_widths]
        return "  ╚" + "╩".join(parts) + "╝"

    def make_row(*cells):
        padded = [str(c).ljust(col_widths[i]) for i, c in enumerate(cells)]
        return "  ║" + "║".join(padded) + "║"

    print(make_top())
    print(make_row(h0.strip(), h1.strip(), h2.strip(), h3.strip(),
                   h4.strip(), h5.strip(), h6.strip(), h7.strip(), h8.strip()))
    print(make_mid())

    for rank, node in enumerate(top_nodes, start=1):
        attrs = G.nodes[node]
        name = attrs.get("name", node)[:22]
        dept = attrs.get("department", "N/A")[:4]
        d  = f"{deg_d.get(node, 0):.4f}"
        b  = f"{bet_d.get(node, 0):.4f}"
        c  = f"{clo_d.get(node, 0):.4f}"
        e  = f"{eig_d.get(node, 0):.4f}"
        p  = f"{pgr_d.get(node, 0):.4f}"
        print(make_row(str(rank), node, name, dept, d, b, c, e, p))
        if rank < top_n:
            print(make_mid())

    print(make_bot())
