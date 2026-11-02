"""
graph_builder.py
================
Builds a NetworkX graph from CSV data files.
Provides basic network statistics computation.
"""

import os
import pandas as pd
import networkx as nx


def load_graph(edges_path: str, nodes_path: str) -> nx.Graph:
    """
    Load a NetworkX graph from edge and node CSV files.

    Parameters
    ----------
    edges_path : str
        Path to the CSV file containing edge data (Source, Target, Weight).
    nodes_path : str
        Path to the CSV file containing node attributes
        (StudentID, Name, Department, Year, GPA).

    Returns
    -------
    nx.Graph
        An undirected weighted graph with node attributes attached.
    """
    if not os.path.exists(edges_path):
        raise FileNotFoundError(f"Edge file not found: {edges_path}")
    if not os.path.exists(nodes_path):
        raise FileNotFoundError(f"Node file not found: {nodes_path}")

    edges_df = pd.read_csv(edges_path)
    nodes_df = pd.read_csv(nodes_path)

    G = nx.Graph()

    # Add nodes with attributes
    for _, row in nodes_df.iterrows():
        G.add_node(
            row["StudentID"],
            name=row["Name"],
            department=row["Department"],
            year=int(row["Year"]),
            gpa=float(row["GPA"]),
        )

    # Add edges with weights
    for _, row in edges_df.iterrows():
        src = row["Source"]
        tgt = row["Target"]
        weight = float(row.get("Weight", 1.0))
        G.add_edge(src, tgt, weight=weight)

    return G


def get_basic_stats(G: nx.Graph) -> dict:
    """
    Compute basic network statistics for the given graph.

    Parameters
    ----------
    G : nx.Graph
        The NetworkX graph to analyse.

    Returns
    -------
    dict
        Dictionary containing:
        - nodes          : number of nodes
        - edges          : number of edges
        - density        : network density
        - avg_degree     : average node degree
        - is_connected   : whether the graph is fully connected
        - num_components : number of connected components
        - diameter       : diameter of the largest connected component
        - avg_clustering : average clustering coefficient
    """
    n = G.number_of_nodes()
    e = G.number_of_edges()
    density = nx.density(G)
    degrees = [d for _, d in G.degree()]
    avg_degree = sum(degrees) / n if n > 0 else 0.0
    is_connected = nx.is_connected(G)
    num_components = nx.number_connected_components(G)

    # Diameter is only defined for a connected graph; use largest component
    if is_connected:
        diameter = nx.diameter(G)
    else:
        largest_cc = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc)
        diameter = nx.diameter(subgraph)

    avg_clustering = nx.average_clustering(G)

    return {
        "nodes": n,
        "edges": e,
        "density": round(density, 4),
        "avg_degree": round(avg_degree, 4),
        "is_connected": is_connected,
        "num_components": num_components,
        "diameter": diameter,
        "avg_clustering": round(avg_clustering, 4),
    }


def print_stats(stats: dict) -> None:
    """
    Pretty-print the basic network statistics as a formatted table.

    Parameters
    ----------
    stats : dict
        Dictionary returned by :func:`get_basic_stats`.
    """
    rows = [
        ("Total Students (Nodes)", str(stats["nodes"])),
        ("Total Connections (Edges)", str(stats["edges"])),
        ("Network Density", str(stats["density"])),
        ("Average Degree", str(stats["avg_degree"])),
        ("Is Fully Connected", "Yes" if stats["is_connected"] else "No"),
        ("Connected Components", str(stats["num_components"])),
        ("Diameter (largest CC)", str(stats["diameter"])),
        ("Avg. Clustering Coeff.", str(stats["avg_clustering"])),
    ]

    col1_w = max(len(r[0]) for r in rows) + 2
    col2_w = max(len(r[1]) for r in rows) + 2
    total_w = col1_w + col2_w + 3  # borders + separator

    top    = "  ╔" + "═" * col1_w + "╦" + "═" * col2_w + "╗"
    sep    = "  ╠" + "═" * col1_w + "╬" + "═" * col2_w + "╣"
    bottom = "  ╚" + "═" * col1_w + "╩" + "═" * col2_w + "╝"

    print(top)
    for i, (label, value) in enumerate(rows):
        label_cell = f" {label} ".ljust(col1_w)
        value_cell = f" {value} ".ljust(col2_w)
        print(f"  ║{label_cell}║{value_cell}║")
        if i < len(rows) - 1:
            print(sep)
    print(bottom)
