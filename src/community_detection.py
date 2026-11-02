"""
community_detection.py
======================
Detect communities in the student social network using multiple algorithms.

Primary algorithms (NetworkX built-in, no extra install required):
  - Greedy Modularity Communities
  - Label Propagation Communities

Optional algorithm (requires python-louvain / community package):
  - Louvain Method (falls back to greedy if not installed)
"""

import networkx as nx
from networkx.algorithms import community as nx_comm


# ---------------------------------------------------------------------------
# Algorithm implementations
# ---------------------------------------------------------------------------

def detect_communities_louvain(G: nx.Graph) -> dict:
    """
    Detect communities using the Louvain method.

    Requires the ``community`` (python-louvain) package.
    Falls back to :func:`detect_communities_greedy` if not available.

    Parameters
    ----------
    G : nx.Graph

    Returns
    -------
    dict mapping node -> community_id (int, 0-indexed)
    """
    try:
        import community as community_louvain  # python-louvain
        partition = community_louvain.best_partition(G, weight="weight")
        return partition
    except ImportError:
        print("  [INFO] python-louvain not installed. Falling back to Greedy Modularity.")
        return detect_communities_greedy(G)


def detect_communities_greedy(G: nx.Graph) -> dict:
    """
    Detect communities using the Greedy Modularity Maximisation algorithm.

    Parameters
    ----------
    G : nx.Graph

    Returns
    -------
    dict mapping node -> community_id (int, 0-indexed)
    """
    communities = nx_comm.greedy_modularity_communities(G, weight="weight")
    partition = {}
    for cid, community_set in enumerate(communities):
        for node in community_set:
            partition[node] = cid
    return partition


def detect_communities_label_propagation(G: nx.Graph) -> dict:
    """
    Detect communities using the Label Propagation algorithm.

    Parameters
    ----------
    G : nx.Graph

    Returns
    -------
    dict mapping node -> community_id (int, 0-indexed)
    """
    communities = nx_comm.label_propagation_communities(G)
    partition = {}
    for cid, community_set in enumerate(communities):
        for node in community_set:
            partition[node] = cid
    return partition


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_communities(communities: dict, node_attrs: dict = None) -> None:
    """
    Print communities in a readable grouped format.

    Parameters
    ----------
    communities : dict
        Mapping node -> community_id as returned by the detect_* functions.
    node_attrs : dict, optional
        Mapping node -> attribute dict (e.g. from G.nodes(data=True)).
        Used to show student name alongside ID.
    """
    # Group nodes by community id
    groups: dict = {}
    for node, cid in communities.items():
        groups.setdefault(cid, []).append(node)

    for cid in sorted(groups.keys()):
        members = sorted(groups[cid])
        dept_counter: dict = {}
        member_strings = []

        for node in members:
            if node_attrs and node in node_attrs:
                name = node_attrs[node].get("name", node)
                dept = node_attrs[node].get("department", "?")
                dept_counter[dept] = dept_counter.get(dept, 0) + 1
                member_strings.append(f"{node}({name})")
            else:
                member_strings.append(node)

        dominant_dept = (
            max(dept_counter, key=dept_counter.get) if dept_counter else "Mixed"
        )
        label = f"{dominant_dept} cluster" if dept_counter else "cluster"

        print(f"\n  Community {cid + 1} ({len(members)} members - {label}):")
        # Print members in rows of 4
        row_size = 4
        for i in range(0, len(member_strings), row_size):
            chunk = member_strings[i : i + row_size]
            print("    " + ",  ".join(chunk))


def get_community_stats(G: nx.Graph, communities: dict) -> dict:
    """
    Compute statistics about the detected communities.

    Parameters
    ----------
    G           : nx.Graph
    communities : dict
        Mapping node -> community_id.

    Returns
    -------
    dict with keys:
        'num_communities'  : int
        'modularity'       : float
        'sizes'            : list of ints (one per community)
        'avg_size'         : float
        'largest_community': int (community_id)
        'smallest_community': int (community_id)
    """
    groups: dict = {}
    for node, cid in communities.items():
        groups.setdefault(cid, set()).add(node)

    sizes = {cid: len(members) for cid, members in groups.items()}

    try:
        # Build list-of-sets for modularity calculation
        community_sets = [groups[cid] for cid in sorted(groups.keys())]
        modularity = nx_comm.modularity(G, community_sets, weight="weight")
    except Exception:
        modularity = float("nan")

    size_list = [sizes[cid] for cid in sorted(sizes.keys())]

    return {
        "num_communities": len(groups),
        "modularity": round(modularity, 4),
        "sizes": size_list,
        "avg_size": round(sum(size_list) / len(size_list), 2) if size_list else 0,
        "largest_community": max(sizes, key=sizes.get),
        "smallest_community": min(sizes, key=sizes.get),
    }
