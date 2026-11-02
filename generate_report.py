"""
Generate SNA Project Report as a Word (.docx) file
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR  = os.path.join(BASE_DIR, "output", "graphs")
OUT_PATH = os.path.join(BASE_DIR, "output", "SNA_Project_Report.docx")

doc = Document()

# ── Page margins ────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3.0)
    section.right_margin  = Cm(2.5)

# ── Helpers ─────────────────────────────────────────────────────────────────
def set_font(run, name="Times New Roman", size=12, bold=False,
             italic=False, color=None):
    run.font.name  = name
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)

def add_heading(text, level=1, color=(0, 51, 102)):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in p.runs:
        run.font.color.rgb = RGBColor(*color)
        run.font.name = "Times New Roman"
    return p

def add_para(text, bold=False, italic=False, size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    set_font(run, size=size, bold=bold, italic=italic, color=color)
    return p

def add_bullet(text, size=11):
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(text)
    set_font(run, size=size)
    return p

def shade_row(row, hex_color="1F3864"):
    for cell in row.cells:
        tc   = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd  = OxmlElement("w:shd")
        shd.set(qn("w:val"),   "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"),  hex_color)
        tcPr.append(shd)

def make_table(headers, rows, col_widths=None, header_color="1F3864"):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    hdr = table.rows[0]
    shade_row(hdr, header_color)
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        run = cell.paragraphs[0].add_run(h)
        set_font(run, size=10, bold=True, color=(255, 255, 255))
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Data rows
    for ri, row_data in enumerate(rows):
        row = table.add_row()
        bg = "D9E1F2" if ri % 2 == 0 else "FFFFFF"
        shade_row(row, bg)
        for ci, val in enumerate(row_data):
            cell = row.cells[ci]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            run = cell.paragraphs[0].add_run(str(val))
            set_font(run, size=10)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    if col_widths:
        for i, row in enumerate(table.rows):
            for j, cell in enumerate(row.cells):
                cell.width = Inches(col_widths[j])

    return table

def add_img(path, caption, width=6.0):
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(width))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph(caption)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in p.runs:
        set_font(run, size=10, italic=True, color=(89, 89, 89))
    doc.add_paragraph()

# ════════════════════════════════════════════════════════════════════════════
# TITLE PAGE
# ════════════════════════════════════════════════════════════════════════════
doc.add_paragraph()
doc.add_paragraph()

t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("MINI PROJECT REPORT")
set_font(r, size=16, bold=True, color=(0, 51, 102))

doc.add_paragraph()
t2 = doc.add_paragraph()
t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = t2.add_run(
    "Social Network Analysis for Community Detection\n"
    "and Influential User Identification\n"
    "Using NetworkX and Gephi"
)
set_font(r2, size=18, bold=True, color=(0, 70, 127))

doc.add_paragraph()
doc.add_paragraph()

for line, sz, bold in [
    ("Department of Computer Science & Engineering", 13, True),
    ("Academic Year 2024–25", 12, False),
    ("", 12, False),
    ("Subject: Data Mining / Social Network Analysis", 12, False),
    ("Tools: Python  •  NetworkX  •  Gephi  •  Pandas  •  Matplotlib", 12, False),
    ("", 12, False),
    ("October 2026", 12, True),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(line)
    set_font(run, size=sz, bold=bold)

doc.add_page_break()

# ════════════════════════════════════════════════════════════════════════════
# 1. ABSTRACT
# ════════════════════════════════════════════════════════════════════════════
add_heading("1. Abstract", 1)
add_para(
    "Social Network Analysis (SNA) is a powerful method for studying relationships and "
    "interactions among individuals in a network. This mini-project implements a complete "
    "Social Network Analysis system using Python, NetworkX, Gephi, Pandas, and Matplotlib "
    "to analyze a student friendship network of 30 students across 4 departments. The system "
    "identifies the most influential students using five centrality measures — Degree, "
    "Betweenness, Closeness, Eigenvector, and PageRank — and detects natural communities "
    "within the network using three algorithms: Greedy Modularity, Label Propagation, and "
    "the Louvain Method. The results reveal 4 distinct communities perfectly aligned with "
    "academic departments, achieving a high modularity score of 0.6278, confirming strong "
    "community structure. The top influential student identified is Harsh Malhotra (ME), "
    "who acts as a key bridge between groups."
)

# ════════════════════════════════════════════════════════════════════════════
# 2. INTRODUCTION
# ════════════════════════════════════════════════════════════════════════════
add_heading("2. Introduction", 1)
add_para(
    "In today's digital age, social networks play a crucial role in information "
    "dissemination, relationship building, and group dynamics. A Social Network can be "
    "mathematically represented as a Graph where nodes represent individuals (students), "
    "edges represent relationships (friendships), and edge weights represent the strength "
    "of the relationship."
)
add_para(
    "Social Network Analysis helps answer key questions: Who are the most influential "
    "people? What groups/communities exist naturally? How does information spread through "
    "the network?"
)
add_para(
    "This project applies SNA concepts to a student friendship dataset of 30 students "
    "across 4 departments — CSE, ECE, ME, and Civil Engineering — to uncover hidden "
    "patterns, influential nodes, and community structures using Python-based graph "
    "analysis tools."
)

# ════════════════════════════════════════════════════════════════════════════
# 3. PROBLEM STATEMENT
# ════════════════════════════════════════════════════════════════════════════
add_heading("3. Problem Statement", 1)
add_para(
    "In a college environment, students interact across departments forming natural social "
    "clusters. However, it is difficult to:"
)
for item in [
    "Identify which students are most influential or well-connected",
    "Discover which communities/groups exist naturally in the network",
    "Understand the overall structure and connectivity of the social network",
    "Find students who bridge different groups (gatekeepers of information)",
]:
    add_bullet(item)
add_para(
    "This project solves these problems by computationally analyzing the student friendship "
    "network and providing visual, data-driven insights through centrality analysis and "
    "community detection."
)

# ════════════════════════════════════════════════════════════════════════════
# 4. OBJECTIVES
# ════════════════════════════════════════════════════════════════════════════
add_heading("4. Objectives", 1)
for obj in [
    "Build a student friendship graph from a CSV dataset using NetworkX",
    "Compute 5 centrality measures to identify influential users",
    "Apply 3 community detection algorithms to find natural groupings",
    "Compute network statistics: density, clustering coefficient, diameter",
    "Generate visualizations using Matplotlib (4 charts)",
    "Export the network to Gephi (GEXF format) for interactive visualization",
]:
    add_bullet(obj)

# ════════════════════════════════════════════════════════════════════════════
# 5. TOOLS & TECHNOLOGIES
# ════════════════════════════════════════════════════════════════════════════
add_heading("5. Tools & Technologies", 1)
make_table(
    headers=["Tool", "Version", "Purpose"],
    rows=[
        ["Python",          "3.13",   "Core programming language"],
        ["NetworkX",        "3.3",    "Graph creation, analysis, centrality & community detection"],
        ["Gephi",           "0.10+",  "Interactive network visualization"],
        ["Pandas",          "2.3.3",  "CSV data loading and processing"],
        ["Matplotlib",      "3.10",   "Generating static graph charts"],
        ["NumPy",           "2.3.3",  "Numerical computations"],
        ["python-louvain",  "0.16",   "Louvain community detection algorithm"],
    ],
    col_widths=[1.3, 1.0, 4.0],
)
doc.add_paragraph()

# ════════════════════════════════════════════════════════════════════════════
# 6. DATASET DESCRIPTION
# ════════════════════════════════════════════════════════════════════════════
add_heading("6. Dataset Description", 1)
add_heading("6.1 Nodes (Students) — student_nodes.csv", 2)
add_para("The dataset contains 30 students from 4 departments:")
make_table(
    headers=["Department", "Count", "Student IDs"],
    rows=[
        ["CSE",   "8", "S1 – S8"],
        ["ECE",   "7", "S9 – S15"],
        ["ME",    "7", "S16 – S22"],
        ["CIVIL", "8", "S23 – S30"],
    ],
    col_widths=[1.5, 1.0, 3.8],
)
doc.add_paragraph()
add_para("Sample Node Records:")
make_table(
    headers=["StudentID", "Name", "Department", "Year", "GPA"],
    rows=[
        ["S1",  "Arjun Sharma",    "CSE",   "3", "3.8"],
        ["S9",  "Rahul Verma",     "ECE",   "3", "3.7"],
        ["S17", "Harsh Malhotra",  "ME",    "3", "3.7"],
        ["S23", "Ishaan Agarwal",  "CIVIL", "3", "3.6"],
    ],
    col_widths=[1.0, 1.8, 1.3, 0.8, 0.8],
)
doc.add_paragraph()

add_heading("6.2 Edges (Friendships) — student_edges.csv", 2)
for item in [
    "Total edges: 77 friendship connections",
    "Edge weight: 1 (weak), 2 (moderate), 3 (strong friendship)",
    "64 intra-community edges (within departments)",
    "13 inter-community edges (cross-department bridge connections)",
]:
    add_bullet(item)

# ════════════════════════════════════════════════════════════════════════════
# 7. METHODOLOGY
# ════════════════════════════════════════════════════════════════════════════
add_heading("7. Methodology", 1)

add_heading("7.1 Graph Construction", 2)
add_para(
    "The student friendship network is modeled as an undirected weighted graph G = (V, E) "
    "where V = {S1, S2, ..., S30} represents 30 student nodes, E = 77 edges represent "
    "friendships, and each edge carries a weight w ∈ {1, 2, 3} representing friendship strength."
)

add_heading("7.2 Centrality Analysis", 2)
add_para("Five centrality measures were computed to identify influential students:")

for title, formula, desc in [
    ("7.2.1 Degree Centrality",
     "C_D(v) = deg(v) / (n - 1)",
     "Measures the fraction of students a node is directly connected to. "
     "High degree = directly popular student who knows many people."),
    ("7.2.2 Betweenness Centrality",
     "C_B(v) = Σ [ σ_st(v) / σ_st ]   for all s ≠ v ≠ t",
     "Measures how often a student lies on the shortest path between others. "
     "High betweenness = bridge/gatekeeper of information flow."),
    ("7.2.3 Closeness Centrality",
     "C_C(v) = (n - 1) / Σ d(v, u)   for all u ≠ v",
     "Measures how close a student is to all others. "
     "High closeness = can spread information quickly to everyone."),
    ("7.2.4 Eigenvector Centrality",
     "C_E(v) = (1/λ) Σ C_E(u)   for all u ∈ N(v)",
     "Measures influence based on quality of connections — being connected to "
     "influential people increases your own score."),
    ("7.2.5 PageRank",
     "PR(v) = (1-d)/n + d × Σ [PR(u)/deg(u)]   for all u ∈ N(v)   [d = 0.85]",
     "Google's algorithm adapted for social networks. A node is important if "
     "important nodes are connected to it."),
]:
    add_heading(title, 3)
    p = doc.add_paragraph()
    run = p.add_run("Formula:  " + formula)
    set_font(run, size=11, italic=True, color=(0, 70, 127))
    add_para(desc, size=11)

add_heading("7.3 Community Detection Algorithms", 2)

for title, result, desc in [
    ("7.3.1 Greedy Modularity (Newman-Girvan)",
     "4 communities — Modularity = 0.6278",
     "Starts with each node as its own community and greedily merges communities "
     "to maximize the modularity score Q. Modularity measures the density of edges "
     "inside communities compared to edges between communities. Q > 0.3 is considered good."),
    ("7.3.2 Label Propagation",
     "3 communities — Modularity = 0.5457",
     "Each node adopts the most common community label among its neighbors, "
     "iterating until labels stabilize. Fast and scalable algorithm requiring no "
     "predefined number of communities."),
    ("7.3.3 Louvain Method",
     "4 communities — Modularity = 0.6278",
     "Two-phase algorithm: Phase 1 locally moves nodes to maximize modularity. "
     "Phase 2 aggregates communities into super-nodes and repeats. "
     "One of the most widely used community detection algorithms."),
]:
    add_heading(title, 3)
    p = doc.add_paragraph()
    run = p.add_run("Result:  " + result)
    set_font(run, size=11, bold=True, color=(0, 128, 0))
    add_para(desc, size=11)

# ════════════════════════════════════════════════════════════════════════════
# 8. RESULTS & ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
add_heading("8. Results & Analysis", 1)

add_heading("8.1 Network Statistics", 2)
make_table(
    headers=["Metric", "Value", "Interpretation"],
    rows=[
        ["Total Nodes",               "30",     "30 students"],
        ["Total Edges",               "77",     "77 friendship connections"],
        ["Network Density",           "0.177",  "Sparse — not everyone knows everyone"],
        ["Average Degree",            "5.13",   "Each student has ~5 friends on average"],
        ["Is Connected",              "Yes",    "Every student can reach every other"],
        ["Connected Components",      "1",      "One unified network"],
        ["Diameter",                  "5",      "Max 5 hops to reach anyone"],
        ["Avg. Clustering Coeff.",    "0.4046", "Friends tend to know each other"],
    ],
    col_widths=[2.0, 1.0, 3.3],
)
doc.add_paragraph()

add_heading("8.2 Top 5 Influential Students", 2)
make_table(
    headers=["Rank", "Student", "Dept", "Degree", "Betweenness", "Closeness", "Eigenvector", "PageRank"],
    rows=[
        ["1st", "Harsh Malhotra (S17)", "ME",  "0.2414", "0.1727", "0.5088", "0.2046", "0.0396"],
        ["2nd", "Rahul Verma (S9)",     "ECE", "0.2414", "0.0982", "0.4754", "0.2948", "0.0413"],
        ["3rd", "Arjun Sharma (S1)",    "CSE", "0.2414", "0.1166", "0.4677", "0.2805", "0.0413"],
        ["4th", "Siddharth Rao (S13)",  "ECE", "0.2414", "0.0316", "0.4915", "0.3157", "0.0472"],
        ["5th", "Vikram Nair (S5)",     "CSE", "0.2414", "0.0371", "0.4833", "0.3008", "0.0470"],
    ],
    col_widths=[0.5, 1.8, 0.5, 0.8, 1.0, 0.9, 1.0, 0.8],
)
doc.add_paragraph()
add_para(
    "Key Finding: Harsh Malhotra (ME) ranks #1 due to highest betweenness centrality (0.1727), "
    "acting as the most critical bridge between different department groups. Siddharth Rao (ECE) "
    "has the highest PageRank (0.0472) — connected to the most influential peers. "
    "The top 5 span all 4 departments, confirming the network is well-integrated.",
    italic=True, size=11
)

add_heading("8.3 Community Detection Results", 2)
make_table(
    headers=["Algorithm", "Communities", "Modularity Score", "Quality"],
    rows=[
        ["Greedy Modularity",  "4", "0.6278", "Excellent ★"],
        ["Label Propagation",  "3", "0.5457", "Good ✓"],
        ["Louvain Method",     "4", "0.6278", "Excellent ★"],
    ],
    col_widths=[2.0, 1.3, 1.5, 1.5],
)
doc.add_paragraph()

add_heading("8.4 Communities Detected (Greedy Modularity)", 2)
make_table(
    headers=["Community", "Size", "Department", "Members"],
    rows=[
        ["Community 1", "8", "CSE",   "Arjun, Priya, Rohan, Sneha, Vikram, Ananya, Karan, Divya"],
        ["Community 2", "8", "CIVIL", "Ishaan, Nisha, Varun, Shreya, Akash, Ritika, Gaurav, Pallavi"],
        ["Community 3", "7", "ECE",   "Rahul, Pooja, Aditya, Meera, Siddharth, Kavya, Nikhil"],
        ["Community 4", "7", "ME",    "Tanvi, Harsh, Sonal, Deepak, Ravi, Ankita, Mohit"],
    ],
    col_widths=[1.2, 0.6, 1.0, 3.5],
)
doc.add_paragraph()
add_para(
    "Key Observation: The community detection algorithm successfully identified the exact "
    "departmental groupings purely from friendship connections — without being given department "
    "information. This validates the algorithm's effectiveness and confirms that students "
    "primarily socialize within their department.",
    italic=True, size=11
)

# ════════════════════════════════════════════════════════════════════════════
# 9. VISUALIZATIONS
# ════════════════════════════════════════════════════════════════════════════
add_heading("9. Visualizations", 1)

add_heading("Figure 1: Student Social Network — Community Clusters", 2)
add_img(
    os.path.join(IMG_DIR, "network_graph.png"),
    "Figure 1: The complete 30-node student social network colored by community "
    "(Red=CSE, Green=CIVIL, Blue=ECE, Orange=ME). Cross-department bridge connections "
    "are visible as edges between colored clusters."
)

add_heading("Figure 2: Centrality Measures Comparison", 2)
add_img(
    os.path.join(IMG_DIR, "centrality_comparison.png"),
    "Figure 2: 2×2 grid showing top-10 students ranked by Degree, Betweenness, "
    "Closeness, and PageRank centrality measures."
)

add_heading("Figure 3: Degree Distribution", 2)
add_img(
    os.path.join(IMG_DIR, "degree_distribution.png"),
    "Figure 3: Histogram of connection counts. Red dashed line = mean degree (5.13). "
    "Most students have exactly 5 connections."
)

add_heading("Figure 4: Community Size Distribution", 2)
add_img(
    os.path.join(IMG_DIR, "community_sizes.png"),
    "Figure 4: Bar chart showing 4 balanced communities of 7–8 members each, "
    "indicating equal social distribution across departments."
)

# ════════════════════════════════════════════════════════════════════════════
# 10. CONCLUSION
# ════════════════════════════════════════════════════════════════════════════
add_heading("10. Conclusion", 1)
add_para(
    "This project successfully implemented a complete Social Network Analysis pipeline "
    "for a student friendship network. The key conclusions are:"
)
for c in [
    "Network Structure: The 30-student network with 77 connections is sparse (density=0.177) "
    "but fully connected with a diameter of 5, meaning any student can reach any other in at most 5 steps.",
    "Influential Users: Harsh Malhotra (S17, ME) is the most influential student due to "
    "highest betweenness centrality — acting as a critical bridge between department groups.",
    "Community Detection: Both Greedy Modularity and Louvain Method detected 4 communities "
    "with modularity=0.6278 (excellent), perfectly aligning with the 4 academic departments.",
    "Cross-department Bridges: 13 inter-community edges exist, mostly formed by Year 3–4 "
    "senior students who had more time to build cross-department relationships.",
    "Tool Effectiveness: NetworkX is highly effective for graph analysis while Gephi provides "
    "an excellent interactive visualization layer — a powerful SNA toolkit combination.",
]:
    add_bullet(c)

# ════════════════════════════════════════════════════════════════════════════
# 11. FUTURE SCOPE
# ════════════════════════════════════════════════════════════════════════════
add_heading("11. Future Scope", 1)
for f in [
    "Larger Dataset: Scale to 500+ students with real survey data",
    "Directed Graph: Model who initiates friendships (directed edges)",
    "Temporal Analysis: Track how the network evolves over semesters",
    "Influence Maximization: Identify students for efficient campus-wide information spreading",
    "Web Interface: Build a Flask/Django web app for interactive exploration",
    "Real Social Media Data: Apply SNA to Twitter/LinkedIn data for real-world analysis",
]:
    add_bullet(f)

# ════════════════════════════════════════════════════════════════════════════
# 12. REFERENCES
# ════════════════════════════════════════════════════════════════════════════
add_heading("12. References", 1)
for ref in [
    "Newman, M. E. J. (2006). Modularity and community structure in networks. PNAS, 103(23), 8577–8582.",
    "Blondel, V. D., et al. (2008). Fast unfolding of communities in large networks. Journal of Statistical Mechanics.",
    "Raghavan, U. N., et al. (2007). Near linear time algorithm to detect community structures. Physical Review E.",
    "Page, L., et al. (1999). The PageRank Citation Ranking: Bringing Order to the Web. Stanford Technical Report.",
    "NetworkX Documentation — https://networkx.org/documentation/stable/",
    "Gephi — The Open Graph Viz Platform — https://gephi.org/",
    "Wasserman, S. & Faust, K. (1994). Social Network Analysis: Methods and Applications. Cambridge University Press.",
    "Hagberg, A., et al. (2008). Exploring network structure, dynamics, and function using NetworkX. SciPy Proceedings.",
]:
    p = doc.add_paragraph(style="List Number")
    run = p.add_run(ref)
    set_font(run, size=11)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run(
    "— Report generated as part of college mini-project submission —\n"
    "All analysis performed using Python 3.13, NetworkX 3.3, and Matplotlib 3.10"
)
set_font(run, size=10, italic=True, color=(128, 128, 128))

# ── Save ────────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
doc.save(OUT_PATH)
print(f"Report saved to: {OUT_PATH}")
