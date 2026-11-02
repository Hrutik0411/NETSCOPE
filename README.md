# Social Network Analysis – Community Detection & Influential User Identification

> **College Mini Project** | Python · NetworkX · Matplotlib · Gephi

---

## 📋 Project Description

This project implements a **Social Network Analysis (SNA)** pipeline on a synthetic student
friendship dataset. It demonstrates two core SNA tasks:

1. **Community Detection** – identifying tightly-knit groups of students using graph-theoretic
   algorithms (Louvain, Greedy Modularity, Label Propagation).
2. **Influential User Identification** – ranking students by multiple centrality measures
   (Degree, Betweenness, Closeness, Eigenvector, PageRank).

The pipeline outputs professional visualisations saved as PNG files and a GEXF file for
interactive exploration in **Gephi**.

---

## 👥 Team / Authors

| Role        | Name                  |
|-------------|-----------------------|
| Developer   | *(Your Name Here)*    |
| Guide       | *(Faculty Name Here)* |
| Department  | *(Dept. Here)*        |
| Institution | *(College Name Here)* |

---

## ✨ Features

- 📊 **Five centrality measures**: Degree, Betweenness, Closeness, Eigenvector, PageRank
- 🔍 **Three community detection algorithms**: Louvain (optional), Greedy Modularity, Label Propagation
- 🎨 **Four Matplotlib visualisations**:
  - Spring-layout network graph coloured by community
  - Side-by-side centrality comparison chart (2 × 2 grid)
  - Degree distribution histogram
  - Community size bar chart
- 🗂️ **Gephi export** via GEXF with all node attributes embedded
- 🖥️ **Professional terminal output** with box-drawing tables and step-by-step progress

---

## 📁 Project Structure

```
social_network_analysis/
├── data/
│   ├── student_edges.csv          # Friendship connections (Source, Target, Weight)
│   └── student_nodes.csv          # Student attributes (ID, Name, Dept, Year, GPA)
├── output/
│   ├── graphs/                    # Generated PNG visualisations
│   └── gephi/                     # GEXF file for Gephi
├── src/
│   ├── __init__.py
│   ├── graph_builder.py           # Graph construction & basic statistics
│   ├── centrality.py              # All centrality measures
│   ├── community_detection.py     # Community detection algorithms
│   └── visualizer.py              # Matplotlib plots & Gephi export
├── main.py                        # Main pipeline entry point
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or later
- pip

### Steps

```bash
# 1. Clone / download the project
cd social_network_analysis

# 2. (Recommended) Create a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

> **Note:** `python-louvain` is optional. If it is not installed the project falls back to
> the Greedy Modularity algorithm automatically.

---

## ▶️ How to Run

```bash
python main.py
```

The script executes all eight pipeline steps and saves outputs to the `output/` directory.

---

## 📤 Output Description

| File / Location | Description |
|---|---|
| `output/graphs/network_graph.png` | Full social network coloured by community |
| `output/graphs/centrality_comparison.png` | 2 × 2 grid comparing top-10 nodes per centrality measure |
| `output/graphs/degree_distribution.png` | Histogram of degree (connection count) distribution |
| `output/graphs/community_sizes.png` | Bar chart showing member count per community |
| `output/gephi/social_network.gexf` | GEXF graph file with all attributes for Gephi |

---

## 🔬 Algorithm Explanations

### Community Detection

#### Louvain Method
A hierarchical, greedy algorithm that iteratively assigns nodes to communities to maximise
**modularity** — a measure of how well a partition separates dense groups from sparse inter-group
edges. It runs in near-linear time and produces very high modularity scores in practice.

- Reference: Blondel et al., *Fast unfolding of communities in large networks*, 2008.

#### Greedy Modularity Maximisation (Clauset-Newman-Moore)
Starts with each node in its own community and repeatedly merges the pair of communities
whose merger produces the largest increase in modularity. Deterministic and efficient for
moderately sized graphs.

- Implemented in `networkx.algorithms.community.greedy_modularity_communities`.

#### Label Propagation
Each node is initialised with a unique label. In each iteration every node adopts the label
most common among its neighbours. The algorithm terminates when no labels change. Simple,
fast, and requires no hyper-parameters.

- Implemented in `networkx.algorithms.community.label_propagation_communities`.

### Centrality Measures

| Measure | Intuition |
|---|---|
| **Degree** | Number of direct friends – raw popularity. |
| **Betweenness** | How often a node lies on the shortest path between others – bridge/broker role. |
| **Closeness** | How quickly a node can reach all others – information spreader. |
| **Eigenvector** | Being connected to well-connected peers – prestige/influence. |
| **PageRank** | Recursive version of eigenvector centrality – similar to Google's link ranking. |

---

## 🗺️ How to Open the GEXF File in Gephi

1. Download and install **Gephi** from [https://gephi.org](https://gephi.org).
2. Open Gephi and choose **File → Open…**
3. Navigate to `output/gephi/social_network.gexf` and click **Open**.
4. In the **Appearance** panel on the left:
   - Select **Nodes → Partition → community** to colour nodes by detected community.
   - Select **Nodes → Ranking → degree_centrality** to scale node sizes.
5. In the **Layout** panel, choose **ForceAtlas 2** and click **Run** until the graph stabilises.
6. Use **Statistics → Modularity** to re-compute communities inside Gephi as a comparison.
7. Export the final image via **File → Export → SVG/PDF/PNG**.

---

## 📷 Sample Output Description

When `main.py` runs successfully you will see:

```
╔══════════════════════════════════════════════════════════════════╗
║        SOCIAL NETWORK ANALYSIS SYSTEM                           ║
╚══════════════════════════════════════════════════════════════════╝
[STEP 1] Loading Data & Building Graph
  ✓ Loaded 30 nodes and 76 edges
[STEP 2] Basic Network Statistics
  ...table of metrics...
[STEP 3] Centrality Analysis
  ✓ Degree Centrality                computed
  ...
[STEP 4] Top 5 Influential Users
  ...formatted table...
[STEP 5] Community Detection
  ...community listings...
[STEP 6] Generating Visualizations
  ✓ Network graph saved → output/graphs/network_graph.png
  ...
[STEP 7] Exporting to Gephi
  ✓ GEXF file saved  → output/gephi/social_network.gexf
[STEP 8] Summary Report
  ...summary table...
```

---

## 📚 References

1. Newman, M. E. J. (2010). *Networks: An Introduction*. Oxford University Press.
2. Barabási, A.-L. (2016). *Network Science*. Cambridge University Press.
   Available free at [http://networksciencebook.com](http://networksciencebook.com).
3. Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008).
   Fast unfolding of communities in large networks.
   *Journal of Statistical Mechanics*, P10008.
4. NetworkX documentation: [https://networkx.org/documentation/stable/](https://networkx.org/documentation/stable/)
5. Gephi: [https://gephi.org](https://gephi.org)
6. Page, L., Brin, S., Motwani, R., & Winograd, T. (1999).
   *The PageRank citation ranking: Bringing order to the Web*.
   Stanford InfoLab Technical Report.
