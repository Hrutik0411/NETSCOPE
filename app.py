
import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Social Network Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent

# ---------------- THEME ----------------
# ---------------- THEME ----------------
st.markdown("""
<style>

/* MAIN APPLICATION */
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #14234b 0%, transparent 35%),
        radial-gradient(ellipse at 90% 10%, #21134b 0%, transparent 30%),
        #070d1c;
    color: #edf2ff;
}

/* MAIN CONTENT SPACING */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* HEADINGS */
h1, h2, h3 {
    color: #f8faff !important;
    letter-spacing: -0.5px;
}

h1 {
    font-weight: 800 !important;
}

/* SIDEBAR BACKGROUND */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0c1530 0%,
        #080f23 55%,
        #0b1024 100%
    );
    border-right: 1px solid rgba(67, 130, 255, 0.35);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* SIDEBAR BRANDING */
[data-testid="stSidebar"] h2 {
    font-size: 27px !important;
    font-weight: 850 !important;
    background: linear-gradient(90deg, #22d3ee, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #9aafd4;
}

/* SIDEBAR DIVIDERS */
[data-testid="stSidebar"] hr {
    border-color: rgba(129, 140, 248, 0.22);
}

/* SIDEBAR NAVIGATION CARDS */
[data-testid="stSidebar"] div[data-testid="stRadio"] > label {
    display: none;
}

[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
    gap: 9px;
}

[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    background: rgba(19, 35, 66, 0.78);
    border: 1px solid rgba(100, 145, 220, 0.16);
    border-radius: 13px;
    padding: 11px 13px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
    background: rgba(35, 65, 112, 0.8);
    border-color: #38bdf8;
    transform: translateX(3px);
}

[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(100deg, #075985, #4338ca, #7e22ce);
    border: 1px solid #67e8f9;
    box-shadow: 0 0 16px rgba(56, 189, 248, 0.22);
}

[data-testid="stSidebar"] div[data-testid="stRadio"] label p {
    color: #edf4ff !important;
    font-weight: 600;
}

/* DEPARTMENT FILTER */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #101d36;
    border: 1px solid #334b79;
    border-radius: 12px;
}

[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: linear-gradient(100deg, #075985, #5b21b6);
    border: 1px solid #38bdf8;
    border-radius: 7px;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(20, 39, 75, 0.96),
        rgba(15, 23, 48, 0.96)
    );
    border: 1px solid rgba(91, 145, 255, 0.28);
    border-radius: 17px;
    padding: 19px;
    box-shadow: 0 7px 24px rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #38bdf8;
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.13);
    transform: translateY(-2px);
}

[data-testid="stMetricLabel"] {
    color: #a9bbdc !important;
}

[data-testid="stMetricValue"] {
    color: #93c5fd !important;
    font-weight: 750;
}

/* BUTTONS */
div.stButton > button,
div.stDownloadButton > button {
    background: linear-gradient(100deg, #075985, #4338ca, #6d28d9);
    color: white;
    border: 1px solid rgba(103, 232, 249, 0.5);
    border-radius: 11px;
    font-weight: 650;
    transition: all 0.2s ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    border-color: #67e8f9;
    box-shadow: 0 0 17px rgba(56, 189, 248, 0.3);
    color: white;
}

/* INPUTS */
[data-baseweb="input"] > div,
[data-baseweb="select"] > div,
[data-baseweb="textarea"] {
    background: #111d35;
    border-color: #334b79;
    border-radius: 10px;
}

/* DATA TABLES */
[data-testid="stDataFrame"] {
    border: 1px solid #293d62;
    border-radius: 12px;
    overflow: hidden;
}

/* ALERTS AND INFORMATION BOXES */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* SECTION DIVIDERS */
hr {
    border-color: rgba(129, 140, 248, 0.2);
}

/* PLOTLY CONTAINERS */
[data-testid="stPlotlyChart"] {
    border-radius: 15px;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #080f20;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(#0891b2, #7c3aed);
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
# ---------------- DATA LOADING ----------------
@st.cache_data
def load_data():
    nodes = pd.read_csv(
        BASE_DIR / "data" / "student_nodes.csv"
    )
    edges = pd.read_csv(
        BASE_DIR / "data" / "student_edges.csv"
    )

    required_nodes = {
        "StudentID", "Name", "Department", "Year", "GPA"
    }
    required_edges = {"Source", "Target", "Weight"}

    if not required_nodes.issubset(nodes.columns):
        raise ValueError("Student node columns are missing.")

    if not required_edges.issubset(edges.columns):
        raise ValueError("Student edge columns are missing.")

    if nodes["StudentID"].duplicated().any():
        raise ValueError("Duplicate student IDs found.")

    known_ids = set(nodes["StudentID"])
    referenced_ids = set(edges["Source"]) | set(edges["Target"])

    if not referenced_ids.issubset(known_ids):
        raise ValueError("Edges reference unknown students.")

    return nodes, edges


def create_graph(nodes, edges):
    graph = nx.Graph()

    for _, student in nodes.iterrows():
        graph.add_node(
            student["StudentID"],
            name=student["Name"],
            department=student["Department"],
            year=int(student["Year"]),
            gpa=float(student["GPA"])
        )

    for _, edge in edges.iterrows():
        graph.add_edge(
            edge["Source"],
            edge["Target"],
            weight=float(edge["Weight"])
        )

    return graph
    
def network_figure(graph):
    fig = go.Figure()

    if graph.number_of_nodes() == 0:
        return fig

    node_ids = tuple(sorted(graph.nodes()))
    edge_records = tuple(
        sorted(tuple(sorted(edge)) for edge in graph.edges())
    )

    positions = graph_positions(node_ids, edge_records)

    edge_x, edge_y = [], []

    for source, target in graph.edges():
        x0, y0 = positions[source]
        x1, y1 = positions[target]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(color="#34415f", width=1.4),
        hoverinfo="skip",
        showlegend=False
    ))

    degrees = dict(graph.degree())

    for department in sorted({
        graph.nodes[n]["department"] for n in graph.nodes()
    }):
        members = [
            n for n in graph.nodes()
            if graph.nodes[n]["department"] == department
        ]

        fig.add_trace(go.Scatter(
            x=[positions[n][0] for n in members],
            y=[positions[n][1] for n in members],
            mode="markers+text",
            text=[n for n in members],
            textposition="top center",
            textfont=dict(color="#dbe5ff", size=10),
            marker=dict(
                size=[12 + degrees[n] * 2.5 for n in members],
                color=DEPARTMENT_COLORS.get(
                    department, "#94a3b8"
                ),
                line=dict(color="#e2e8f0", width=1),
                opacity=0.92
            ),
            name=department,
            showlegend=True
        ))

    fig.update_layout(
        height=530,
        paper_bgcolor="#131d33",
        plot_bgcolor="#131d33",
        font=dict(color="#cbd5e1"),
        margin=dict(l=15, r=15, t=20, b=15),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        legend=dict(orientation="h", y=-0.05, x=0),
        hovermode="closest",
        dragmode="pan"
    )

    return fig



try:
    nodes_df, edges_df = load_data()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
    st.error(f"Unable to load project data: {error}")
    st.stop()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🌐 NETSCOPE")
    st.caption("SOCIAL NETWORK INTELLIGENCE")
    st.divider()

    st.markdown("### Navigation")
    page = st.radio(
        "Select page",
        [
            "Overview",
            "Network Explorer",
            "Centrality Analysis",
            "Community Detection",
            "Department Insights",
            "Gephi Integration"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("### Network Filters")

    departments = sorted(
        nodes_df["Department"].unique().tolist()
    )

    selected_departments = st.multiselect(
        "Departments",
        departments,
        default=departments
    )

    st.caption("Dataset: Student Friendship Network")
    st.caption("Engine: NetworkX + Plotly")
    st.caption("Gephi integration: Coming soon")

# ---------------- FILTER NETWORK ----------------
filtered_nodes = nodes_df[
    nodes_df["Department"].isin(selected_departments)
].copy()

selected_ids = set(filtered_nodes["StudentID"])

filtered_edges = edges_df[
    edges_df["Source"].isin(selected_ids)
    & edges_df["Target"].isin(selected_ids)
].copy()

G = create_graph(filtered_nodes, filtered_edges)

# ---------------- NETWORK METRICS ----------------
total_nodes = G.number_of_nodes()
total_edges = G.number_of_edges()

density = nx.density(G)
average_degree = (
    sum(dict(G.degree()).values()) / total_nodes
    if total_nodes else 0
)

components = (
    nx.number_connected_components(G)
    if total_nodes else 0
)

# ---------------- VISUALIZATION ----------------
DEPARTMENT_COLORS = {
    "CSE": "#8b5cf6",
    "ECE": "#06b6d4",
    "ME": "#f59e0b",
    "CIVIL": "#22c55e"
}


@st.cache_data
def graph_positions(node_ids, edge_records):
    graph = nx.Graph()
    graph.add_nodes_from(node_ids)

    for source, target in edge_records:
        graph.add_edge(source, target)

    return nx.spring_layout(graph, seed=42)



def explorer_figure(graph, selected_node):
    fig = go.Figure()

    if graph.number_of_nodes() == 0:
        return fig

    node_ids = tuple(sorted(graph.nodes()))
    edge_records = tuple(
        sorted(tuple(sorted(edge)) for edge in graph.edges())
    )

    positions = graph_positions(node_ids, edge_records)

    neighbors = set(graph.neighbors(selected_node))
    selected_group = {selected_node} | neighbors

    # Draw edges with thickness based on friendship strength
    for weight in sorted({
        graph[u][v].get("weight", 1)
        for u, v in graph.edges()
    }):
        edge_x, edge_y = [], []

        for u, v, data in graph.edges(data=True):
            if data.get("weight", 1) == weight:
                edge_x.extend([
                    positions[u][0], positions[v][0], None
                ])
                edge_y.extend([
                    positions[u][1], positions[v][1], None
                ])

        fig.add_trace(go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(
                color="#64748b",
                width=1.2 + float(weight) * 1.5
            ),
            opacity=0.65,
            hoverinfo="skip",
            showlegend=False
        ))

    # Node colors: selected, neighbors and remaining students
    colors = []
    sizes = []
    customdata = []

    for node in graph.nodes():
        attrs = graph.nodes[node]
        degree = graph.degree(node)

        if node == selected_node:
            colors.append("#facc15")
        elif node in neighbors:
            colors.append("#06b6d4")
        else:
            colors.append("#64748b")

        sizes.append(
            29 if node == selected_node
            else 20 if node in neighbors
            else 12 + degree * 1.2
        )

        customdata.append([
            attrs["name"],
            attrs["department"],
            attrs["year"],
            attrs["gpa"],
            degree
        ])

    fig.add_trace(go.Scatter(
        x=[positions[n][0] for n in graph.nodes()],
        y=[positions[n][1] for n in graph.nodes()],
        mode="markers+text",
        text=list(graph.nodes()),
        textposition="top center",
        textfont=dict(size=10, color="#dbeafe"),
        customdata=customdata,
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(color="#e2e8f0", width=1.2),
            opacity=0.95
        ),
        hovertemplate=(
            "<b>%{customdata[0]}</b>"
            "<br>ID: %{text}"
            "<br>Department: %{customdata[1]}"
            "<br>Year: %{customdata[2]}"
            "<br>GPA: %{customdata[3]:.2f}"
            "<br>Connections: %{customdata[4]}"
            "<extra></extra>"
        ),
        showlegend=False
    ))

    fig.update_layout(
        height=620,
        paper_bgcolor="#131d33",
        plot_bgcolor="#131d33",
        font=dict(color="#e2e8f0"),
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        hovermode="closest",
        dragmode="pan"
    )

    return fig



# ---------------- CENTRALITY ANALYSIS ----------------
def calculate_centrality(graph):

    results = {}

    if graph.number_of_nodes() == 0:
        return results

    # Friendship strength becomes inverse path distance
    weighted_graph = graph.copy()

    for u, v, data in weighted_graph.edges(data=True):
        strength = float(data.get("weight", 1))
        data["distance"] = 1.0 / max(strength, 0.001)

    # 1. Degree Centrality
    results["Degree Centrality"] = nx.degree_centrality(graph)

    # 2. Betweenness Centrality
    results["Betweenness Centrality"] = nx.betweenness_centrality(
        weighted_graph,
        normalized=True,
        weight="distance"
    )

    # 3. Closeness Centrality
    results["Closeness Centrality"] = nx.closeness_centrality(
        weighted_graph,
        distance="distance"
    )

    # 4. Eigenvector Centrality
    try:
        results["Eigenvector Centrality"] = nx.eigenvector_centrality(
            graph,
            max_iter=2000,
            weight="weight"
        )
    except nx.PowerIterationFailedConvergence:
        results["Eigenvector Centrality"] = {
            node: 0.0 for node in graph.nodes()
        }

    # 5. PageRank
    results["PageRank"] = nx.pagerank(
        graph,
        alpha=0.85,
        weight="weight"
    )

    return results

# ---------------- COMMUNITY DETECTION ----------------
def calculate_communities(graph):

    if graph.number_of_nodes() == 0:
        return {}

    algorithms = {}

    # 1. Louvain
    louvain_groups = nx.community.louvain_communities(
        graph,
        weight="weight",
        seed=42
    )

    algorithms["Louvain"] = louvain_groups

    # 2. Greedy Modularity
    greedy_groups = nx.community.greedy_modularity_communities(
        graph,
        weight="weight"
    )

    algorithms["Greedy Modularity"] = greedy_groups

    # 3. Label Propagation
    label_groups = list(
        nx.community.asyn_lpa_communities(
            graph,
            weight="weight",
            seed=42
        )
    )

    algorithms["Label Propagation"] = label_groups

    results = {}

    for algorithm, groups in algorithms.items():

        # Sort groups by size, then by smallest student ID
        groups = sorted(
            [set(group) for group in groups],
            key=lambda group: (
                -len(group),
                min(str(node) for node in group)
            )
        )

        membership = {}

        for community_id, group in enumerate(groups, start=1):
            for node in group:
                membership[node] = community_id

        # Calculate modularity
        if graph.number_of_edges() > 0 and len(groups) > 1:
            modularity = nx.community.modularity(
                graph,
                groups,
                weight="weight"
            )
        else:
            modularity = 0.0

        results[algorithm] = {
            "groups": groups,
            "membership": membership,
            "modularity": modularity,
            "count": len(groups)
        }

    return results

# ---------------- MAIN CONTENT ----------------
if page == "Overview":
    st.title("Social Network Intelligence")
    st.caption(
        "Explore relationships, network structure and student communities"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", total_nodes)

    with col2:
        st.metric("Friendship Connections", total_edges)

    with col3:
        st.metric("Network Density", f"{density:.3f}")

    with col4:
        st.metric("Average Degree", f"{average_degree:.2f}")

    st.write("")

    left, right = st.columns([2.1, 1])

    with left:
        st.subheader("Interactive Network Map")
        st.plotly_chart(
            network_figure(G),
            use_container_width=True,
            config={"displaylogo": False}
        )

    with right:
        st.subheader("Network Insights")

        st.metric("Connected Components", components)

        clustering = (
            nx.average_clustering(G)
            if total_nodes else 0
        )

        st.metric(
            "Clustering Coefficient",
            f"{clustering:.3f}"
        )

        st.metric(
            "Active Departments",
            filtered_nodes["Department"].nunique()
        )

        st.info(
            "Node size represents the number of friendships. "
            "Node color represents the department."
        )

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Department Distribution")

        department_counts = (
            filtered_nodes["Department"]
            .value_counts()
        )

        fig = go.Figure(go.Bar(
            x=department_counts.index,
            y=department_counts.values,
            marker_color=[
                DEPARTMENT_COLORS.get(d, "#94a3b8")
                for d in department_counts.index
            ]
        ))

        fig.update_layout(
            height=320,
            paper_bgcolor="#131d33",
            plot_bgcolor="#131d33",
            font=dict(color="#cbd5e1"),
            xaxis_title="Department",
            yaxis_title="Students",
            margin=dict(l=20, r=20, t=20, b=30)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Degree Distribution")

        degree_values = [
            degree for _, degree in G.degree()
        ]

        fig = go.Figure(go.Histogram(
            x=degree_values,
            xbins=dict(
                start=-0.5,
                end=max(degree_values, default=0) + 0.5,
                size=1
            ),
            marker_color="#8b5cf6"
        ))

        fig.update_layout(
            height=320,
            paper_bgcolor="#131d33",
            plot_bgcolor="#131d33",
            font=dict(color="#cbd5e1"),
            xaxis_title="Number of Connections",
            yaxis_title="Number of Students",
            margin=dict(l=20, r=20, t=20, b=30)
        )

        st.plotly_chart(fig, use_container_width=True)


elif page == "Network Explorer":

    st.title("Network Explorer")
    st.caption(
        "Explore individual students, friendships and network relationships."
    )

    st.divider()

    if total_nodes == 0:
        st.warning("No students available. Check your department filters.")
        st.stop()

    # Search students
    search_query = st.text_input(
        "🔍 Search student",
        placeholder="Enter student name or ID..."
    )

    search_results = filtered_nodes[
        filtered_nodes["Name"].str.contains(
            search_query, case=False, na=False
        )
        | filtered_nodes["StudentID"].str.contains(
            search_query, case=False, na=False
        )
    ].copy()

    if search_results.empty:
        st.warning("No matching students found.")
        st.stop()

    student_options = search_results["StudentID"].tolist()

    selected_node = st.selectbox(
        "Select a student to explore",
        student_options,
        format_func=lambda sid: (
            f"{sid} — "
            f"{nodes_df.loc[nodes_df['StudentID'] == sid, 'Name'].iloc[0]}"
        )
    )

    student = nodes_df[
        nodes_df["StudentID"] == selected_node
    ].iloc[0]

    neighbors = list(G.neighbors(selected_node))
    degree = G.degree(selected_node)

    weighted_degree = sum(
        data.get("weight", 1)
        for _, _, data in G.edges(selected_node, data=True)
    )

    clustering = nx.clustering(G, selected_node)

    # Student profile
    st.divider()
    st.subheader("Student Profile")

    p1, p2, p3, p4, p5 = st.columns(5)

    p1.metric("Student ID", selected_node)
    p2.metric("Department", student["Department"])
    p3.metric("Academic Year", int(student["Year"]))
    p4.metric("GPA", f"{student['GPA']:.2f}")
    p5.metric("Friendships", degree)

    st.divider()

    # Network visualization
    left, right = st.columns([2, 1])

    with left:
        st.subheader("Relationship Network")
        st.plotly_chart(
            explorer_figure(G, selected_node),
            use_container_width=True,
            config={"displaylogo": False}
        )

        st.caption(
            "Yellow = Selected student | Cyan = Direct friends | "
            "Grey = Other students. Thicker lines indicate stronger friendships."
        )

    with right:
        st.subheader("Relationship Insights")

        st.metric("Direct Friends", degree)
        st.metric("Total Friendship Strength", weighted_degree)
        st.metric("Local Clustering", f"{clustering:.3f}")

        st.info(
            "Local clustering measures how strongly this student's "
            "friends are connected to one another."
        )

    st.divider()

    # Friends table
    st.subheader("Direct Connections")

    if neighbors:
        friend_records = []

        for friend in neighbors:
            attrs = G.nodes[friend]

            friend_records.append({
                "Student ID": friend,
                "Name": attrs["name"],
                "Department": attrs["department"],
                "Year": attrs["year"],
                "Friendship Strength": G[selected_node][friend]["weight"]
            })

        friends_df = pd.DataFrame(friend_records)

        friends_df = friends_df.sort_values(
            "Friendship Strength",
            ascending=False
        )

        st.dataframe(
            friends_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("This student has no connections in the selected network.")

    st.divider()

    # Friendship strength chart
    st.subheader("Friendship Strength Distribution")

    if neighbors:
        strength_df = friends_df[
            "Friendship Strength"
        ].value_counts().sort_index()

        strength_fig = go.Figure(go.Bar(
            x=[
                f"Strength {int(x)}"
                for x in strength_df.index
            ],
            y=strength_df.values,
            marker_color=["#64748b", "#06b6d4", "#8b5cf6"]
        ))

        strength_fig.update_layout(
            height=300,
            paper_bgcolor="#131d33",
            plot_bgcolor="#131d33",
            font=dict(color="#cbd5e1"),
            xaxis_title="Friendship Strength",
            yaxis_title="Number of Friends",
            margin=dict(l=20, r=20, t=20, b=30)
        )

        st.plotly_chart(
            strength_fig,
            use_container_width=True
        )


elif page == "Centrality Analysis":

    st.title("Centrality & Influence Analysis")

    st.caption(
        "Identify influential students and understand their "
        "importance in the friendship network."
    )

    st.divider()

    if total_nodes == 0:
        st.warning("No students available for centrality analysis.")
        st.stop()

    with st.spinner("Calculating centrality measures..."):
        centrality_results = calculate_centrality(G)

    # Prepare centrality dataframe
    centrality_data = []

    for node in G.nodes():

        attrs = G.nodes[node]

        record = {
            "Student ID": node,
            "Name": attrs["name"],
            "Department": attrs["department"],
            "Year": attrs["year"],
            "Connections": G.degree(node)
        }

        for metric, scores in centrality_results.items():
            record[metric] = scores.get(node, 0)

        centrality_data.append(record)

    centrality_df = pd.DataFrame(centrality_data)

    # Ranking controls
    st.subheader("Influence Ranking")

    control1, control2 = st.columns([2, 1])

    with control1:
        selected_metric = st.selectbox(
            "Select Centrality Algorithm",
            [
                "Degree Centrality",
                "Betweenness Centrality",
                "Closeness Centrality",
                "Eigenvector Centrality",
                "PageRank"
            ]
        )

    with control2:
        top_n = st.slider(
            "Number of students",
            min_value=5,
            max_value=max(5, min(total_nodes, 30)),
            value=min(10, total_nodes)
        )

    ranking_df = centrality_df.sort_values(
        selected_metric,
        ascending=False
    ).head(top_n).copy()

    ranking_df.insert(
        0,
        "Rank",
        range(1, len(ranking_df) + 1)
    )

    # Top three students
    st.subheader("Top Influential Students")

    top_three = ranking_df.head(3)

    cols = st.columns(3)

    for index, (_, student) in enumerate(top_three.iterrows()):

        with cols[index]:
            st.metric(
                f"Rank #{int(student['Rank'])} · {student['Student ID']}",
                f"{student[selected_metric]:.4f}"
            )

            st.caption(
                f"{student['Name']} · {student['Department']}"
            )

    st.divider()

    # Ranking visualization
    left, right = st.columns([1.7, 1])

    with left:
        st.subheader(f"{selected_metric} Rankings")

        chart_df = ranking_df.sort_values(
            selected_metric,
            ascending=True
        )

        fig = go.Figure(go.Bar(
            x=chart_df[selected_metric],
            y=chart_df["Name"],
            orientation="h",
            marker=dict(
                color=chart_df[selected_metric],
                colorscale="Purples",
                showscale=False
            ),
            customdata=chart_df[
                ["Student ID", "Department"]
            ].values,
            hovertemplate=(
                "<b>%{y}</b>"
                "<br>Student ID: %{customdata[0]}"
                "<br>Department: %{customdata[1]}"
                "<br>Score: %{x:.5f}"
                "<extra></extra>"
            )
        ))

        fig.update_layout(
            height=470,
            paper_bgcolor="#131d33",
            plot_bgcolor="#131d33",
            font=dict(color="#cbd5e1"),
            xaxis_title="Centrality Score",
            yaxis_title="Student",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:
        st.subheader("Algorithm Explanation")

        explanations = {
            "Degree Centrality":
                "Measures the proportion of students directly connected to a student.",

            "Betweenness Centrality":
                "Measures how frequently a student lies on shortest paths between other students.",

            "Closeness Centrality":
                "Measures how close a student is to all other reachable students.",

            "Eigenvector Centrality":
                "Measures influence based on connections to other influential students.",

            "PageRank":
                "Estimates importance based on the importance of connected students."
        }

        st.info(explanations[selected_metric])

        st.metric(
            "Highest Score",
            f"{ranking_df[selected_metric].max():.5f}"
        )

        st.metric(
            "Average Score",
            f"{centrality_df[selected_metric].mean():.5f}"
        )

    st.divider()

    # Full ranking table
    st.subheader("Complete Centrality Leaderboard")

    display_columns = [
        "Rank",
        "Student ID",
        "Name",
        "Department",
        "Connections",
        selected_metric
    ]

    st.dataframe(
        ranking_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    # Compare all five metrics
    st.divider()

    st.subheader("Five-Metric Student Comparison")

    selected_students = st.multiselect(
        "Choose students to compare",
        centrality_df["Student ID"].tolist(),
        default=centrality_df.nlargest(
            min(3, total_nodes),
            selected_metric
        )["Student ID"].tolist()
    )

    if selected_students:

        comparison = centrality_df[
            centrality_df["Student ID"].isin(selected_students)
        ]

        metric_names = list(centrality_results.keys())

        fig = go.Figure()

        for _, student in comparison.iterrows():

            fig.add_trace(go.Bar(
                name=f"{student['Student ID']} - {student['Name']}",
                x=metric_names,
                y=[student[m] for m in metric_names]
            ))

        fig.update_layout(
            barmode="group",
            height=420,
            paper_bgcolor="#131d33",
            plot_bgcolor="#131d33",
            font=dict(color="#cbd5e1"),
            yaxis_title="Centrality Score",
            xaxis_title="Algorithm",
            legend_title="Students",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Select students to compare their centrality scores.")

    # Download complete report
    st.divider()

    csv_data = centrality_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Complete Centrality Report",
        data=csv_data,
        file_name="centrality_analysis.csv",
        mime="text/csv"
    )


elif page == "Community Detection":

    st.title("Community Detection & Cluster Intelligence")

    st.caption(
        "Discover student groups, identify tightly connected communities "
        "and compare community detection algorithms."
    )

    st.divider()

    if total_nodes == 0:
        st.warning("No students available for community analysis.")
        st.stop()

    with st.spinner("Detecting student communities..."):
        community_results = calculate_communities(G)

    algorithm = st.selectbox(
        "Select Community Detection Algorithm",
        [
            "Louvain",
            "Greedy Modularity",
            "Label Propagation"
        ]
    )

    result = community_results[algorithm]

    groups = result["groups"]
    membership = result["membership"]
    modularity = result["modularity"]

    # ---------------- SUMMARY METRICS ----------------
    st.subheader("Community Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Students", total_nodes)
    c2.metric("Communities Detected", result["count"])
    c3.metric("Modularity Score", f"{modularity:.4f}")
    c4.metric(
        "Largest Community",
        max((len(group) for group in groups), default=0)
    )

    st.divider()

    # ---------------- COMMUNITY GRAPH ----------------
    st.subheader(f"{algorithm} Network Visualization")

    palette = [
        "#8b5cf6",
        "#06b6d4",
        "#f59e0b",
        "#22c55e",
        "#ec4899",
        "#3b82f6",
        "#f97316",
        "#a3e635",
        "#e879f9",
        "#14b8a6"
    ]

    node_ids = tuple(sorted(G.nodes()))

    edge_records = tuple(
        sorted(tuple(sorted(edge)) for edge in G.edges())
    )

    positions = graph_positions(node_ids, edge_records)

    fig = go.Figure()

    # Draw edges
    edge_x = []
    edge_y = []

    for u, v in G.edges():
        edge_x.extend([
            positions[u][0],
            positions[v][0],
            None
        ])

        edge_y.extend([
            positions[u][1],
            positions[v][1],
            None
        ])

    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(color="#475569", width=1.3),
        opacity=0.6,
        hoverinfo="skip",
        showlegend=False
    ))

    # Draw each community separately
    for community_id in range(1, len(groups) + 1):

        members = [
            node for node in G.nodes()
            if membership[node] == community_id
        ]

        color = palette[(community_id - 1) % len(palette)]

        fig.add_trace(go.Scatter(
            x=[positions[n][0] for n in members],
            y=[positions[n][1] for n in members],
            mode="markers+text",
            text=members,
            textposition="top center",
            textfont=dict(size=10, color="#e2e8f0"),
            marker=dict(
                size=[
                    14 + G.degree(n) * 1.5
                    for n in members
                ],
                color=color,
                line=dict(color="#ffffff", width=1)
            ),
            name=f"Community {community_id}",
            customdata=[
                [
                    G.nodes[n]["name"],
                    G.nodes[n]["department"],
                    G.degree(n)
                ]
                for n in members
            ],
            hovertemplate=(
                "<b>%{customdata[0]}</b>"
                "<br>Student ID: %{text}"
                "<br>Department: %{customdata[1]}"
                "<br>Connections: %{customdata[2]}"
                f"<br>Community: {community_id}"
                "<extra></extra>"
            )
        ))

    fig.update_layout(
        height=620,
        paper_bgcolor="#131d33",
        plot_bgcolor="#131d33",
        font=dict(color="#cbd5e1"),
        margin=dict(l=10, r=10, t=20, b=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        legend=dict(orientation="h", y=-0.05),
        hovermode="closest",
        dragmode="pan"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displaylogo": False}
    )

    st.caption(
        "Each color represents a different detected community. "
        "Node size represents the number of connections."
    )

    st.divider()

    # ---------------- ALGORITHM COMPARISON ----------------
    st.subheader("Algorithm Performance Comparison")

    comparison_records = []

    for name, data in community_results.items():
        sizes = [len(group) for group in data["groups"]]

        comparison_records.append({
            "Algorithm": name,
            "Communities": data["count"],
            "Modularity": data["modularity"],
            "Largest Community": max(sizes, default=0),
            "Smallest Community": min(sizes, default=0)
        })

    comparison_df = pd.DataFrame(comparison_records)

    left, right = st.columns(2)

    with left:
        st.markdown("#### Modularity Comparison")

        modularity_fig = go.Figure(go.Bar(
            x=comparison_df["Algorithm"],
            y=comparison_df["Modularity"],
            marker_color=["#8b5cf6", "#06b6d4", "#22c55e"],
            text=comparison_df["Modularity"].round(4),
            textposition="outside"
        ))

        modularity_fig.update_layout(
            height=370,
            paper_bgcolor="#131d33",
            plot_bgcolor="#131d33",
            font=dict(color="#cbd5e1"),
            yaxis_title="Modularity Score",
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(
            modularity_fig,
            use_container_width=True
        )

    with right:
        st.markdown("#### Community Size Distribution")

        size_records = []

        for community_id, group in enumerate(groups, start=1):
            size_records.append({
                "Community": f"Community {community_id}",
                "Students": len(group)
            })

        size_df = pd.DataFrame(size_records)

        size_fig = go.Figure(go.Pie(
            labels=size_df["Community"],
            values=size_df["Students"],
            hole=0.55,
            textinfo="label+value",
            marker=dict(
                colors=[
                    palette[(i) % len(palette)]
                    for i in range(len(groups))
                ]
            )
        ))

        size_fig.update_layout(
            height=370,
            paper_bgcolor="#131d33",
            font=dict(color="#cbd5e1"),
            margin=dict(l=10, r=10, t=20, b=20)
        )

        st.plotly_chart(
            size_fig,
            use_container_width=True
        )

    st.divider()

    # ---------------- DEPARTMENT COMPOSITION ----------------
    st.subheader("Department Composition of Communities")

    composition_records = []

    for community_id, group in enumerate(groups, start=1):

        for node in group:

            composition_records.append({
                "Community": f"Community {community_id}",
                "Department": G.nodes[node]["department"],
                "Student ID": node,
                "Student Name": G.nodes[node]["name"]
            })

    composition_df = pd.DataFrame(composition_records)

    department_matrix = pd.crosstab(
        composition_df["Community"],
        composition_df["Department"]
    )

    department_fig = go.Figure()

    for department in department_matrix.columns:

        department_fig.add_trace(go.Bar(
            name=department,
            x=department_matrix.index,
            y=department_matrix[department]
        ))

    department_fig.update_layout(
        barmode="stack",
        height=380,
        paper_bgcolor="#131d33",
        plot_bgcolor="#131d33",
        font=dict(color="#cbd5e1"),
        xaxis_title="Community",
        yaxis_title="Number of Students",
        legend_title="Department",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        department_fig,
        use_container_width=True
    )

    st.divider()

    # ---------------- COMMUNITY MEMBERSHIP ----------------
    st.subheader("Explore Community Members")

    selected_community = st.selectbox(
        "Select a community",
        list(range(1, len(groups) + 1)),
        format_func=lambda x: f"Community {x}"
    )

    selected_members = [
        node for node in G.nodes()
        if membership[node] == selected_community
    ]

    member_records = []

    for node in selected_members:

        attrs = G.nodes[node]

        member_records.append({
            "Student ID": node,
            "Name": attrs["name"],
            "Department": attrs["department"],
            "Year": attrs["year"],
            "Connections": G.degree(node)
        })

    members_df = pd.DataFrame(member_records)

    st.metric("Students in Selected Community", len(members_df))

    st.dataframe(
        members_df.sort_values(
            "Connections",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

        # ---------------- DOWNLOAD REPORT ----------------
    st.divider()

    st.download_button(
        "Download Community Membership Report",
        data=composition_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{algorithm.lower().replace(' ', '_')}_communities.csv",
        mime="text/csv"
    )

    st.download_button(
        "Download Algorithm Comparison",
        data=comparison_df.to_csv(index=False).encode("utf-8"),
        file_name="community_algorithm_comparison.csv",
        mime="text/csv"
    )
    
elif page == "Department Insights":

    st.title("Department Intelligence & Relationship Analytics")

    st.caption(
        "Explore department-level friendships, student influence, "
        "academic performance and cross-department relationships."
    )

    st.divider()

    if total_nodes == 0:
        st.warning("No students available. Adjust your department filters.")
        st.stop()

    # ---------------- STUDENT-LEVEL METRICS ----------------

    pagerank_scores = nx.pagerank(
        G,
        alpha=0.85,
        weight="weight"
    )

    degree_scores = nx.degree_centrality(G)

    department_records = []

    for node in G.nodes():
        attrs = G.nodes[node]

        department_records.append({
            "Student ID": node,
            "Name": attrs["name"],
            "Department": attrs["department"],
            "GPA": attrs["gpa"],
            "Connections": G.degree(node),
            "PageRank": pagerank_scores[node],
            "Degree Centrality": degree_scores[node]
        })

    student_metrics_df = pd.DataFrame(department_records)

    # ---------------- DEPARTMENT SUMMARY ----------------

    st.subheader("Department Performance Overview")

    department_summary = (
        student_metrics_df.groupby("Department")
        .agg(
            Students=("Student ID", "count"),
            Average_GPA=("GPA", "mean"),
            Average_Connections=("Connections", "mean"),
            Total_Connections=("Connections", "sum"),
            Average_PageRank=("PageRank", "mean"),
            Average_Degree_Centrality=("Degree Centrality", "mean")
        )
        .reset_index()
    )

    department_summary["Average_GPA"] = (
        department_summary["Average_GPA"].round(2)
    )

    department_summary["Average_Connections"] = (
        department_summary["Average_Connections"].round(2)
    )

    department_summary["Average_PageRank"] = (
        department_summary["Average_PageRank"].round(5)
    )

    department_summary["Average_Degree_Centrality"] = (
        department_summary["Average_Degree_Centrality"].round(4)
    )

    # KPI cards
    best_connections = department_summary.sort_values(
        "Average_Connections",
        ascending=False
    ).iloc[0]

    best_pagerank = department_summary.sort_values(
        "Average_PageRank",
        ascending=False
    ).iloc[0]

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Departments",
        len(department_summary)
    )

    k2.metric(
        "Students",
        total_nodes
    )

    k3.metric(
        "Highest Avg. Connections",
        best_connections["Department"],
        f"{best_connections['Average_Connections']:.2f} per student"
    )

    k4.metric(
        "Highest Avg. PageRank",
        best_pagerank["Department"],
        f"{best_pagerank['Average_PageRank']:.5f}"
    )

    st.divider()

    # ---------------- DEPARTMENT COMPARISON ----------------

    st.subheader("Department Comparison")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Average GPA by Department")

        gpa_fig = go.Figure(go.Bar(
            x=department_summary["Department"],
            y=department_summary["Average_GPA"],
            marker_color="#8b5cf6",
            text=department_summary["Average_GPA"],
            textposition="outside"
        ))

        gpa_fig.update_layout(
            height=350,
            paper_bgcolor="#131d33",
            plot_bgcolor="#131d33",
            font=dict(color="#cbd5e1"),
            yaxis_title="Average GPA",
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(
            gpa_fig,
            use_container_width=True
        )

    with right:
        st.markdown("#### Average Connections by Department")

        connections_fig = go.Figure(go.Bar(
            x=department_summary["Department"],
            y=department_summary["Average_Connections"],
            marker_color="#06b6d4",
            text=department_summary["Average_Connections"],
            textposition="outside"
        ))

        connections_fig.update_layout(
            height=350,
            paper_bgcolor="#131d33",
            plot_bgcolor="#131d33",
            font=dict(color="#cbd5e1"),
            yaxis_title="Average Connections",
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(
            connections_fig,
            use_container_width=True
        )

    st.divider()

    # ---------------- CROSS DEPARTMENT ANALYSIS ----------------

    st.subheader("Cross-Department Friendship Analysis")

    cross_department_records = []

    for source, target, data in G.edges(data=True):

        source_department = G.nodes[source]["department"]
        target_department = G.nodes[target]["department"]

        cross_department_records.append({
            "Student ID 1": source,
            "Student 1": G.nodes[source]["name"],
            "Department 1": source_department,
            "Student ID 2": target,
            "Student 2": G.nodes[target]["name"],
            "Department 2": target_department,
            "Friendship Strength": data.get("weight", 1),
            "Cross Department": (
                source_department != target_department
            )
        })

    relationship_df = pd.DataFrame(
        cross_department_records
    )

    if not relationship_df.empty:

        cross_edges = relationship_df[
            relationship_df["Cross Department"]
        ].copy()

        internal_edges = relationship_df[
            ~relationship_df["Cross Department"]
        ].copy()

        cross_count = len(cross_edges)
        internal_count = len(internal_edges)

    else:
        cross_edges = pd.DataFrame()
        internal_edges = pd.DataFrame()
        cross_count = 0
        internal_count = 0

    total_relationships = cross_count + internal_count

    cross_percentage = (
        cross_count / total_relationships * 100
        if total_relationships else 0
    )

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Cross-Department Friendships",
        cross_count
    )

    r2.metric(
        "Within-Department Friendships",
        internal_count
    )

    r3.metric(
        "Cross-Department Percentage",
        f"{cross_percentage:.1f}%"
    )

    # Department connection matrix
    departments = sorted(
        student_metrics_df["Department"].unique()
    )

    connection_matrix = pd.DataFrame(
        0,
        index=departments,
        columns=departments
    )

    for source, target in G.edges():

        source_department = G.nodes[source]["department"]
        target_department = G.nodes[target]["department"]

        if source_department != target_department:
            connection_matrix.loc[
                source_department, target_department
            ] += 1

            connection_matrix.loc[
                target_department, source_department
            ] += 1

    st.markdown("#### Cross-Department Connection Matrix")

    matrix_fig = go.Figure(go.Heatmap(
        z=connection_matrix.values,
        x=connection_matrix.columns,
        y=connection_matrix.index,
        colorscale="Viridis",
        text=connection_matrix.values,
        texttemplate="%{text}",
        hovertemplate=(
            "Department 1: %{y}"
            "<br>Department 2: %{x}"
            "<br>Connections: %{z}"
            "<extra></extra>"
        )
    ))

    matrix_fig.update_layout(
        height=400,
        paper_bgcolor="#131d33",
        plot_bgcolor="#131d33",
        font=dict(color="#cbd5e1"),
        xaxis_title="Department",
        yaxis_title="Department",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        matrix_fig,
        use_container_width=True
    )

    # Cross department friendship records
    st.markdown("#### Cross-Department Friendship Details")

    if not cross_edges.empty:

        cross_edges = cross_edges.sort_values(
            "Friendship Strength",
            ascending=False
        )

        st.dataframe(
            cross_edges[
                [
                    "Student 1",
                    "Department 1",
                    "Student 2",
                    "Department 2",
                    "Friendship Strength"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "No cross-department friendships exist in the current selection."
        )

    st.divider()

    # ---------------- GPA VS NETWORK INFLUENCE ----------------

    st.subheader("Academic Performance vs Network Influence")

    st.caption(
        "Explore the relationship between student GPA and PageRank. "
        "This is an exploratory comparison, not a causal analysis."
    )

    scatter_fig = go.Figure()

    for department in departments:

        department_data = student_metrics_df[
            student_metrics_df["Department"] == department
        ]

        scatter_fig.add_trace(go.Scatter(
            x=department_data["GPA"],
            y=department_data["PageRank"],
            mode="markers",
            name=department,
            marker=dict(
                size=12,
                line=dict(color="#ffffff", width=1),
                opacity=0.85
            ),
            customdata=department_data[
                ["Name", "Student ID", "Connections"]
            ].values,
            hovertemplate=(
                "<b>%{customdata[0]}</b>"
                "<br>ID: %{customdata[1]}"
                "<br>GPA: %{x:.2f}"
                "<br>PageRank: %{y:.5f}"
                "<br>Connections: %{customdata[2]}"
                "<extra></extra>"
            )
        ))

    scatter_fig.update_layout(
        height=450,
        paper_bgcolor="#131d33",
        plot_bgcolor="#131d33",
        font=dict(color="#cbd5e1"),
        xaxis_title="Student GPA",
        yaxis_title="PageRank",
        legend_title="Department",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        scatter_fig,
        use_container_width=True
    )

    if (
        len(student_metrics_df) > 1
        and student_metrics_df["GPA"].nunique() > 1
        and student_metrics_df["PageRank"].nunique() > 1
    ):

        correlation = student_metrics_df[
            ["GPA", "PageRank"]
        ].corr().iloc[0, 1]

        st.metric(
            "GPA vs PageRank Pearson Correlation",
            f"{correlation:.3f}"
        )

    else:
        st.info(
            "Insufficient variation in GPA or PageRank "
            "to calculate correlation."
        )

    st.divider()

    # ---------------- DEPARTMENT LEADERBOARD ----------------

    st.subheader("Department Intelligence Leaderboard")

    display_summary = department_summary.rename(
        columns={
            "Average_GPA": "Average GPA",
            "Average_Connections": "Average Connections",
            "Total_Connections": "Total Connections",
            "Average_PageRank": "Average PageRank",
            "Average_Degree_Centrality": "Average Degree Centrality"
        }
    )

    st.dataframe(
        display_summary,
        use_container_width=True,
        hide_index=True
    )

    # ---------------- DOWNLOAD REPORTS ----------------

    st.divider()

    st.download_button(
        "Download Department Analysis",
        data=department_summary.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="department_analysis.csv",
        mime="text/csv"
    )

    st.download_button(
        "Download Friendship Analysis",
        data=relationship_df.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="department_friendships.csv",
        mime="text/csv"
    )

elif page == "Gephi Integration":

    st.title("Gephi Network Integration")

    st.caption(
        "Export your social network with student attributes, "
        "centrality scores and community information for Gephi analysis."
    )

    st.divider()

    if total_nodes == 0:
        st.warning("No students available. Adjust your department filters.")

    else:
        # ---------------- NETWORK ANALYSIS ----------------

        pagerank_scores = nx.pagerank(
            G,
            alpha=0.85,
            weight="weight"
        )

        degree_scores = nx.degree_centrality(G)

        if G.number_of_edges() > 0:
            communities = nx.community.louvain_communities(
                G,
                weight="weight",
                seed=42
            )
        else:
            communities = [{node} for node in G.nodes()]

        community_map = {}

        for community_id, community in enumerate(communities, start=1):
            for node in community:
                community_map[node] = community_id

        # ---------------- PREPARE GEXF FILE ----------------

        export_graph = nx.Graph(G)

        for node in export_graph.nodes():

            export_graph.nodes[node]["label"] = str(
                export_graph.nodes[node].get("name", node)
            )

            export_graph.nodes[node]["PageRank"] = float(
                pagerank_scores[node]
            )

            export_graph.nodes[node]["Degree_Centrality"] = float(
                degree_scores[node]
            )

            export_graph.nodes[node]["Community"] = int(
                community_map[node]
            )

        gexf_data = "\n".join(
            nx.generate_gexf(export_graph)
        )

        # ---------------- NETWORK SUMMARY ----------------

        st.subheader("Export Network Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Students", G.number_of_nodes())
        c2.metric("Friendships", G.number_of_edges())
        c3.metric("Communities", len(communities))
        c4.metric(
            "Departments",
            len(set(
    nx.get_node_attributes(G, "department").values()
))
        )

        st.divider()

        # ---------------- DOWNLOAD ----------------

        st.subheader("Download Gephi Network")

        st.write(
            "Download your network in GEXF format. "
            "You can import this file directly into Gephi."
        )

        st.download_button(
            label="Download Network as GEXF",
            data=gexf_data.encode("utf-8"),
            file_name="social_network_analysis.gexf",
            mime="application/gexf+xml"
        )

        st.success(
            "Your Gephi export is ready. "
            "It includes student attributes, friendship weights, "
            "PageRank, degree centrality and community labels."
        )

        st.divider()

        # ---------------- GEPHI INSTRUCTIONS ----------------

        st.subheader("How to Open Your Network in Gephi")

        st.markdown("""
        1. Download the GEXF file above.
        2. Open Gephi on your computer.
        3. Select **File → Open**.
        4. Choose `social_network_analysis.gexf`.
        5. Open the Overview workspace.
        6. Select a layout such as **ForceAtlas 2**.
        7. Click Run to visualize the network.
        """)

        st.info(
            "In Gephi, use the Community attribute to color nodes "
            "and PageRank or Degree_Centrality to size nodes. "
            "Use the Weight attribute to inspect friendship strength."
        )

else:
    st.title(page)
    st.info(
        "This module will be implemented in the next development steps."
    )

    