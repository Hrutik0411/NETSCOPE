"""
Generate a professional PowerPoint presentation for the SNA Mini-Project.
Slides: 15 total with dark blue theme, charts embedded, bullet points.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu
import os

# ── Paths ────────────────────────────────────────────────────────────────────
BASE   = r"C:\Users\prajwal yadav\.gemini\antigravity\scratch\social_network_analysis"
GRAPHS = os.path.join(BASE, "output", "graphs")
OUT    = os.path.join(BASE, "output", "SNA_Presentation.pptx")

# ── Colour Palette ────────────────────────────────────────────────────────────
DARK_BG    = RGBColor(0x0D, 0x1B, 0x2A)   # Deep navy
ACCENT     = RGBColor(0x00, 0xB4, 0xD8)   # Cyan accent
ACCENT2    = RGBColor(0x90, 0xE0, 0xEF)   # Light cyan
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
YELLOW     = RGBColor(0xFF, 0xD1, 0x66)
GREEN      = RGBColor(0x06, 0xD6, 0xA0)
LIGHT_GRAY = RGBColor(0xCC, 0xD5, 0xE0)
ORANGE     = RGBColor(0xFF, 0x8C, 0x42)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]   # completely blank layout

# ─────────────────────────────────────────────────────────────────────────────
# Helper utilities
# ─────────────────────────────────────────────────────────────────────────────

def add_slide():
    return prs.slides.add_slide(BLANK)

def bg(slide, color=DARK_BG):
    """Fill slide background."""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def box(slide, left, top, width, height,
        fill=None, line_color=None, line_width=Pt(0)):
    """Add a plain rectangle shape."""
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape

def txt(slide, text, left, top, width, height,
        size=20, bold=False, italic=False, color=WHITE,
        align=PP_ALIGN.LEFT, wrap=True, font="Calibri"):
    """Add a text box."""
    txb = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p  = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name  = font
    return txb

def txt_multi(slide, lines, left, top, width, height,
              default_size=18, default_color=WHITE, font="Calibri"):
    """
    lines: list of dicts  { text, size, bold, italic, color, align, space_before }
    """
    txb = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    first = True
    for item in lines:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = item.get("align", PP_ALIGN.LEFT)
        if "space_before" in item:
            p.space_before = Pt(item["space_before"])
        run = p.add_run()
        run.text = item.get("text", "")
        run.font.size  = Pt(item.get("size", default_size))
        run.font.bold  = item.get("bold", False)
        run.font.italic = item.get("italic", False)
        run.font.color.rgb = item.get("color", default_color)
        run.font.name  = font
    return txb

def bullet_box(slide, items, left, top, width, height,
               size=17, color=LIGHT_GRAY, bullet="▸  ", bold_first=False):
    """Add a bullet-point text box."""
    txb = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        if isinstance(item, dict):
            label  = item.get("label", "")
            detail = item.get("detail", "")
            c      = item.get("color", color)
            b      = item.get("bold", False)
            s      = item.get("size", size)
            bul    = item.get("bullet", bullet)
        else:
            label  = item
            detail = ""
            c      = color
            b      = bold_first
            s      = size
            bul    = bullet

        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = bul + label
        run.font.size  = Pt(s)
        run.font.bold  = b
        run.font.color.rgb = c
        run.font.name = "Calibri"

        if detail:
            p2 = tf.add_paragraph()
            p2.space_before = Pt(1)
            r2 = p2.add_run()
            r2.text = "      " + detail
            r2.font.size  = Pt(s - 2)
            r2.font.italic = True
            r2.font.color.rgb = ACCENT2
            r2.font.name = "Calibri"
    return txb

def header_bar(slide, title, subtitle=None):
    """Dark cyan header bar at top of slide."""
    box(slide, 0, 0, 13.33, 1.15, fill=RGBColor(0x02, 0x3E, 0x8A))
    # accent line
    box(slide, 0, 1.15, 13.33, 0.06, fill=ACCENT)
    txt(slide, title, 0.3, 0.1, 10, 0.65,
        size=28, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        txt(slide, subtitle, 0.3, 0.72, 10, 0.38,
            size=15, italic=True, color=ACCENT2, align=PP_ALIGN.LEFT)

def footer(slide, text="Social Network Analysis  |  College Mini Project"):
    box(slide, 0, 7.15, 13.33, 0.35, fill=RGBColor(0x02, 0x3E, 0x8A))
    txt(slide, text, 0.2, 7.17, 12.9, 0.3,
        size=11, color=ACCENT2, align=PP_ALIGN.CENTER)

def pic(slide, path, left, top, width, height=None):
    if os.path.exists(path):
        if height:
            slide.shapes.add_picture(path,
                Inches(left), Inches(top), Inches(width), Inches(height))
        else:
            slide.shapes.add_picture(path,
                Inches(left), Inches(top), width=Inches(width))

def card(slide, left, top, width, height, fill=RGBColor(0x02, 0x3E, 0x8A),
         border=ACCENT, bw=Pt(1.5)):
    s = box(slide, left, top, width, height, fill=fill,
            line_color=border, line_width=bw)
    return s

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
# gradient-like top bar
box(sl, 0, 0, 13.33, 3.2, fill=RGBColor(0x02, 0x3E, 0x8A))
box(sl, 0, 3.2,  13.33, 0.08, fill=ACCENT)

txt(sl, "MINI PROJECT PRESENTATION", 0.5, 0.25, 12.3, 0.55,
    size=16, color=ACCENT2, bold=False, align=PP_ALIGN.CENTER)

txt(sl,
    "Social Network Analysis for\nCommunity Detection &\nInfluential User Identification",
    0.5, 0.7, 12.3, 2.2,
    size=34, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

txt(sl, "Using NetworkX and Gephi", 0.5, 2.85, 12.3, 0.45,
    size=20, italic=True, color=YELLOW, align=PP_ALIGN.CENTER)

# Info cards
for i, (label, val) in enumerate([
    ("Subject",  "Data Mining / Social Network Analysis"),
    ("Tools",    "Python  •  NetworkX  •  Gephi  •  Matplotlib"),
    ("Year",     "Academic Year 2024–25"),
]):
    cx = 0.6 + i * 4.25
    card(sl, cx, 3.55, 3.9, 0.85)
    txt(sl, label, cx+0.15, 3.6, 3.6, 0.28, size=11, color=ACCENT2, bold=True)
    txt(sl, val,   cx+0.15, 3.88, 3.6, 0.42, size=13, color=WHITE)

footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — TABLE OF CONTENTS
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Table of Contents", "What we'll cover today")

topics = [
    ("01", "Introduction & Problem Statement"),
    ("02", "Objectives"),
    ("03", "Tools & Technologies"),
    ("04", "Dataset Description"),
    ("05", "Methodology — Centrality Analysis"),
    ("06", "Methodology — Community Detection"),
    ("07", "Network Statistics"),
    ("08", "Results — Influential Users"),
    ("09", "Results — Community Detection"),
    ("10", "Visualizations"),
    ("11", "Conclusion & Future Scope"),
]
cols = [topics[:6], topics[6:]]
for ci, col in enumerate(cols):
    for ri, (num, topic) in enumerate(col):
        lx = 0.4 + ci * 6.5
        ty = 1.45 + ri * 0.88
        card(sl, lx, ty, 6.1, 0.76, fill=RGBColor(0x02, 0x3E, 0x8A))
        txt(sl, num,   lx+0.15, ty+0.12, 0.55, 0.5, size=18, bold=True, color=ACCENT)
        txt(sl, topic, lx+0.78, ty+0.15, 5.2,  0.5, size=14, color=WHITE)

footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — INTRODUCTION
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Introduction", "What is Social Network Analysis?")

txt(sl, "A Social Network = Graph of People & Relationships",
    0.4, 1.35, 8, 0.5, size=20, bold=True, color=YELLOW)

bullet_box(sl, [
    {"label": "Node (Vertex)", "detail": "Each student = one node in the graph", "color": WHITE},
    {"label": "Edge",          "detail": "Friendship/interaction = connection between nodes", "color": WHITE},
    {"label": "Edge Weight",   "detail": "Strength of friendship (1=weak, 2=moderate, 3=strong)", "color": WHITE},
    {"label": "Social Network","detail": "The complete graph of all students & friendships", "color": WHITE},
], 0.4, 1.95, 7.5, 2.8, size=17)

# Right panel — visual concept
card(sl, 8.8, 1.3, 4.1, 5.6)
txt(sl, "SNA Answers:", 9.0, 1.45, 3.7, 0.4, size=14, bold=True, color=ACCENT)
for i, q in enumerate([
    "Who knows the most people?",
    "Who bridges groups?",
    "Who can spread info fastest?",
    "Which groups exist?",
    "How is the network structured?",
]):
    txt(sl, f"❓  {q}", 9.0, 1.95 + i*0.88, 3.7, 0.7, size=12, color=LIGHT_GRAY)

footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — PROBLEM STATEMENT & OBJECTIVES
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Problem Statement & Objectives")

# Left — Problem
card(sl, 0.3, 1.35, 5.9, 5.6)
txt(sl, "🔴  Problem Statement", 0.5, 1.5, 5.5, 0.45, size=17, bold=True, color=ORANGE)
bullet_box(sl, [
    "Hard to identify influential students",
    "Natural groups are not visible",
    "Bridge students are unknown",
    "Network structure is unclear",
], 0.5, 2.05, 5.5, 3.0, size=15, color=LIGHT_GRAY)

# Right — Objectives
card(sl, 6.8, 1.35, 6.1, 5.6)
txt(sl, "✅  Objectives", 7.0, 1.5, 5.7, 0.45, size=17, bold=True, color=GREEN)
bullet_box(sl, [
    "Build student friendship graph from CSV",
    "Compute 5 centrality measures",
    "Apply 3 community detection algorithms",
    "Calculate network statistics",
    "Generate Matplotlib visualizations",
    "Export to Gephi (GEXF format)",
], 7.0, 2.05, 5.7, 4.5, size=15, color=LIGHT_GRAY)

footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — TOOLS & TECHNOLOGIES
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Tools & Technologies Used")

tools = [
    ("🐍", "Python 3.13",      "Core programming language for entire project"),
    ("🕸️", "NetworkX 3.3",     "Graph creation, analysis, centrality & community detection"),
    ("🎨", "Gephi 0.10+",      "Interactive network visualization tool"),
    ("🐼", "Pandas 2.3",       "CSV data loading and processing"),
    ("📊", "Matplotlib 3.10",  "Static chart generation (4 PNG outputs)"),
    ("🔵", "python-louvain",   "Louvain community detection algorithm"),
]
for i, (icon, name, desc) in enumerate(tools):
    row = i // 2
    col = i % 2
    lx = 0.4  + col * 6.4
    ty = 1.42 + row * 1.75
    card(sl, lx, ty, 6.0, 1.55)
    txt(sl, icon, lx+0.18, ty+0.28, 0.6,  1.0, size=26)
    txt(sl, name, lx+0.85, ty+0.15, 4.9,  0.45, size=17, bold=True, color=ACCENT)
    txt(sl, desc, lx+0.85, ty+0.62, 4.9,  0.78, size=13, color=LIGHT_GRAY)

footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — DATASET
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Dataset Description", "30 Students  •  77 Friendship Connections")

# Stats row
for i, (val, label, color) in enumerate([
    ("30",  "Students\n(Nodes)", ACCENT),
    ("77",  "Friendships\n(Edges)", YELLOW),
    ("4",   "Departments", GREEN),
    ("3",   "Edge Weight\nLevels", ORANGE),
]):
    lx = 0.4 + i * 3.15
    card(sl, lx, 1.35, 2.9, 1.4)
    txt(sl, val,   lx+0.2, 1.42, 2.5, 0.72, size=38, bold=True, color=color, align=PP_ALIGN.CENTER)
    txt(sl, label, lx+0.2, 2.08, 2.5, 0.58, size=13, color=WHITE, align=PP_ALIGN.CENTER)

# Dept table
card(sl, 0.4, 3.0, 5.6, 3.85)
txt(sl, "Department Breakdown", 0.6, 3.1, 5.2, 0.4, size=15, bold=True, color=ACCENT)
depts = [
    ("CSE",   "S1–S8",   "8 students", "🔴"),
    ("ECE",   "S9–S15",  "7 students", "🔵"),
    ("ME",    "S16–S22", "7 students", "🟡"),
    ("CIVIL", "S23–S30", "8 students", "🟢"),
]
for i, (dept, ids, count, dot) in enumerate(depts):
    ty = 3.6 + i * 0.77
    txt(sl, dot,   0.6,  ty, 0.4, 0.55, size=16)
    txt(sl, dept,  1.05, ty, 1.2, 0.55, size=15, bold=True, color=YELLOW)
    txt(sl, ids,   2.35, ty, 1.5, 0.55, size=13, color=LIGHT_GRAY)
    txt(sl, count, 4.0,  ty, 1.6, 0.55, size=13, color=GREEN)

# Sample nodes
card(sl, 6.3, 3.0, 6.6, 3.85)
txt(sl, "Sample Student Records", 6.5, 3.1, 6.2, 0.4, size=15, bold=True, color=ACCENT)
samples = [
    ("S1",  "Arjun Sharma",   "CSE",   "3", "3.8"),
    ("S9",  "Rahul Verma",    "ECE",   "3", "3.7"),
    ("S17", "Harsh Malhotra", "ME",    "3", "3.7"),
    ("S23", "Ishaan Agarwal", "CIVIL", "3", "3.6"),
]
hdrs = ["ID", "Name", "Dept", "Yr", "GPA"]
hx   = [6.5, 7.1, 8.7, 10.1, 10.8]
for j, h in enumerate(hdrs):
    txt(sl, h, hx[j], 3.55, 0.9, 0.38, size=12, bold=True, color=ACCENT2)
for i, (sid, name, dept, yr, gpa) in enumerate(samples):
    ty = 4.0 + i * 0.72
    bg_c = RGBColor(0x04, 0x4F, 0x7C) if i%2==0 else RGBColor(0x02, 0x3E, 0x8A)
    box(sl, 6.35, ty-0.05, 6.5, 0.65, fill=bg_c)
    for j, val in enumerate([sid, name, dept, yr, gpa]):
        txt(sl, val, hx[j], ty, 0.9 if j>0 else 0.55, 0.55, size=12, color=WHITE)

footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — CENTRALITY MEASURES
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Methodology — Centrality Analysis", "5 measures to find the most influential students")

measures = [
    ("Degree Centrality",      "deg(v) / (n-1)",          "Who knows the MOST people directly?",          ACCENT),
    ("Betweenness Centrality", "Σ σ_st(v) / σ_st",        "Who BRIDGES / connects different groups?",      ORANGE),
    ("Closeness Centrality",   "(n-1) / Σ d(v,u)",        "Who can reach EVERYONE fastest?",               GREEN),
    ("Eigenvector Centrality", "(1/λ) Σ C_E(u)",          "Who is connected to OTHER influential people?", YELLOW),
    ("PageRank",               "PR(v) = (1-d)/n + d×Σ…",  "Google's algo — important nodes boost score",  RGBColor(0xFF,0x6B,0x9D)),
]
for i, (name, formula, meaning, color) in enumerate(measures):
    ty = 1.42 + i * 1.1
    card(sl, 0.35, ty, 12.65, 0.98, fill=RGBColor(0x02, 0x3E, 0x8A))
    box(sl, 0.35, ty, 0.18, 0.98, fill=color)
    txt(sl, name,    0.65, ty+0.05, 3.4, 0.42, size=15, bold=True, color=color)
    txt(sl, formula, 0.65, ty+0.52, 3.4, 0.4,  size=12, italic=True, color=ACCENT2)
    txt(sl, "→  " + meaning, 4.25, ty+0.22, 8.5, 0.55, size=14, color=LIGHT_GRAY)

footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — COMMUNITY DETECTION
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Methodology — Community Detection", "3 algorithms to find natural groups")

algos = [
    ("01", "Greedy Modularity\n(Newman-Girvan)",
     ["Starts: each node = its own community",
      "Merges: greedily maximizes Modularity Q",
      "Result: 4 communities  |  Q = 0.6278 ★"],
     ACCENT, GREEN),
    ("02", "Label Propagation",
     ["Starts: each node gets unique label",
      "Iterates: adopt most common neighbor label",
      "Result: 3 communities  |  Q = 0.5457"],
     ORANGE, ORANGE),
    ("03", "Louvain Method",
     ["Phase 1: local moves to maximize modularity",
      "Phase 2: aggregate into super-nodes, repeat",
      "Result: 4 communities  |  Q = 0.6278 ★"],
     GREEN, GREEN),
]
for i, (num, name, bullets, accent, res_color) in enumerate(algos):
    lx = 0.35 + i * 4.35
    card(sl, lx, 1.38, 4.1, 5.7)
    box(sl, lx, 1.38, 4.1, 0.08, fill=accent)
    txt(sl, num,  lx+0.18, 1.52, 0.55, 0.5, size=22, bold=True, color=accent)
    txt(sl, name, lx+0.18, 1.52, 3.75, 0.85, size=15, bold=True, color=WHITE)
    for j, b in enumerate(bullets):
        c = res_color if j == 2 else LIGHT_GRAY
        bold = j == 2
        txt(sl, ("✅  " if j==2 else "▸  ") + b,
            lx+0.2, 2.55+j*1.35, 3.7, 1.1,
            size=13, color=c, bold=bold)

txt(sl, "★  Greedy Modularity & Louvain both achieved the BEST score: 0.6278  (>0.3 = Good)",
    0.35, 7.0, 12.65, 0.4, size=13, bold=True, color=YELLOW, align=PP_ALIGN.CENTER)
footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — NETWORK STATISTICS
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Network Statistics", "Key metrics of the student social network")

stats = [
    ("30",      "Nodes",                    "Students in network",          ACCENT),
    ("77",      "Edges",                    "Friendship connections",        YELLOW),
    ("0.177",   "Density",                  "Sparse — not everyone connected",GREEN),
    ("5.13",    "Avg Degree",               "Friends per student (average)", ORANGE),
    ("Yes",     "Connected",                "Every student reachable",       GREEN),
    ("5",       "Diameter",                 "Max hops between any 2 students",ACCENT),
    ("0.4046",  "Clustering Coeff.",        "Friends tend to know each other",YELLOW),
    ("0.6278",  "Modularity Score",         "Excellent community structure!",  RGBColor(0xFF,0x6B,0x9D)),
]
for i, (val, label, desc, color) in enumerate(stats):
    row = i // 4
    col = i % 4
    lx = 0.3  + col * 3.2
    ty = 1.42 + row * 2.6
    card(sl, lx, ty, 3.0, 2.35)
    box(sl, lx, ty, 3.0, 0.07, fill=color)
    txt(sl, val,   lx+0.15, ty+0.18, 2.7, 0.85, size=30, bold=True, color=color, align=PP_ALIGN.CENTER)
    txt(sl, label, lx+0.15, ty+1.05, 2.7, 0.45, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(sl, desc,  lx+0.15, ty+1.55, 2.7, 0.65, size=11, italic=True, color=ACCENT2, align=PP_ALIGN.CENTER)

footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — TOP 5 INFLUENTIAL USERS
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Results — Top 5 Influential Students", "Ranked by combined centrality score")

medals = ["🥇", "🥈", "🥉", "④", "⑤"]
students = [
    ("S17", "Harsh Malhotra",  "ME",  "0.2414","0.1727","0.5088","0.2046","0.0396", YELLOW),
    ("S9",  "Rahul Verma",    "ECE", "0.2414","0.0982","0.4754","0.2948","0.0413", ACCENT),
    ("S1",  "Arjun Sharma",   "CSE", "0.2414","0.1166","0.4677","0.2805","0.0413", GREEN),
    ("S13", "Siddharth Rao",  "ECE", "0.2414","0.0316","0.4915","0.3157","0.0472", ORANGE),
    ("S5",  "Vikram Nair",    "CSE", "0.2414","0.0371","0.4833","0.3008","0.0470", LIGHT_GRAY),
]
# Header
hdrs  = ["", "ID", "Name", "Dept", "Degree", "Betweenness", "Closeness", "Eigenvec.", "PageRank"]
hx    = [0.3, 0.82, 1.45, 3.55, 4.3, 5.3, 6.55, 7.75, 9.05]
hwidths=[0.5, 0.6,  2.0,  0.7,  0.9, 1.1,  1.1,   1.2,  1.2]
box(sl, 0.3, 1.42, 12.7, 0.5, fill=RGBColor(0x02, 0x3E, 0x8A))
for j, (h, hx_, hw) in enumerate(zip(hdrs, hx, hwidths)):
    txt(sl, h, hx_, 1.47, hw, 0.38, size=12, bold=True, color=ACCENT2, align=PP_ALIGN.CENTER)

for i, (sid, name, dept, deg, bet, clo, eig, pgr, color) in enumerate(students):
    ty = 2.0 + i * 0.98
    bg_c = RGBColor(0x04, 0x4F, 0x7C) if i%2==0 else RGBColor(0x03, 0x3A, 0x68)
    box(sl, 0.3, ty, 12.7, 0.88, fill=bg_c)
    box(sl, 0.3, ty, 0.05, 0.88, fill=color)
    vals = [medals[i], sid, name, dept, deg, bet, clo, eig, pgr]
    for j, (v, hx_, hw) in enumerate(zip(vals, hx, hwidths)):
        c = color if j < 2 else (WHITE if j<4 else LIGHT_GRAY)
        b = j < 2
        txt(sl, v, hx_, ty+0.18, hw, 0.5, size=13 if j>1 else 16,
            bold=b, color=c, align=PP_ALIGN.CENTER)

txt(sl, "★  Harsh Malhotra (ME) is #1 — highest Betweenness (0.1727) — key bridge between departments!",
    0.3, 6.95, 12.7, 0.4, size=13, bold=True, color=YELLOW, align=PP_ALIGN.CENTER)
footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — COMMUNITY DETECTION RESULTS
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Results — Community Detection", "4 natural groups perfectly matching departments")

# Algorithm comparison
algos_res = [
    ("Greedy Modularity", "4 Communities", "0.6278", GREEN, "★ BEST"),
    ("Label Propagation", "3 Communities", "0.5457", YELLOW, "Good"),
    ("Louvain Method",    "4 Communities", "0.6278", GREEN, "★ BEST"),
]
for i, (alg, comm, mod, color, badge) in enumerate(algos_res):
    lx = 0.35 + i * 4.3
    card(sl, lx, 1.38, 4.05, 1.3)
    txt(sl, alg,   lx+0.2, 1.45, 3.6, 0.42, size=14, bold=True, color=WHITE)
    txt(sl, comm,  lx+0.2, 1.85, 2.0, 0.38, size=14, color=color, bold=True)
    txt(sl, f"Q = {mod}  {badge}", lx+0.2, 2.22, 3.6, 0.35, size=13, color=color)

# Communities
comms = [
    ("Community 1", "🔴", "CSE Cluster", "8 members",
     "Arjun Sharma, Priya Patel, Rohan Mehta, Sneha Iyer,\nVikram Nair, Ananya Krishnan, Karan Joshi, Divya Singh",
     RGBColor(0xE7, 0x4C, 0x3C)),
    ("Community 2", "🟢", "CIVIL Cluster", "8 members",
     "Ishaan Agarwal, Nisha Kapoor, Varun Chandra, Shreya Mishra,\nAkash Dubey, Ritika Sinha, Gaurav Yadav, Pallavi Jain",
     RGBColor(0x2E, 0xCC, 0x71)),
    ("Community 3", "🔵", "ECE Cluster", "7 members",
     "Rahul Verma, Pooja Desai, Aditya Kumar, Meera Reddy,\nSiddharth Rao, Kavya Menon, Nikhil Gupta",
     RGBColor(0x34, 0x98, 0xDB)),
    ("Community 4", "🟡", "ME Cluster", "7 members",
     "Tanvi Bose, Harsh Malhotra, Sonal Chauhan, Deepak Tiwari,\nRavi Pandey, Ankita Bhatt, Mohit Saxena",
     RGBColor(0xF3, 0x9C, 0x12)),
]
for i, (cname, dot, label, count, members, color) in enumerate(comms):
    col = i % 2
    row = i // 2
    lx = 0.35 + col * 6.35
    ty = 2.9  + row * 2.05
    card(sl, lx, ty, 6.1, 1.88, fill=RGBColor(0x02, 0x3E, 0x8A))
    box(sl, lx, ty, 6.1, 0.07, fill=color)
    txt(sl, dot + "  " + cname, lx+0.2, ty+0.15, 3.0, 0.42, size=15, bold=True, color=color)
    txt(sl, label + "  •  " + count, lx+0.2, ty+0.55, 5.6, 0.35, size=13, color=YELLOW)
    txt(sl, members, lx+0.2, ty+0.95, 5.7, 0.82, size=11, color=LIGHT_GRAY)

footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — NETWORK GRAPH VISUALIZATION
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Visualization — Student Social Network", "Spring layout, colored by community")

pic(sl, os.path.join(GRAPHS, "network_graph.png"), 0.35, 1.35, 8.5, 5.7)

card(sl, 9.2, 1.35, 3.8, 5.7)
txt(sl, "Legend", 9.4, 1.5, 3.4, 0.4, size=16, bold=True, color=ACCENT)

for dot, dept, count in [("🔴","CSE","8 members"),("🟢","CIVIL","8 members"),
                          ("🔵","ECE","7 members"),("🟡","ME","7 members")]:
    pass

legend = [
    ("🔴", "Community 1", "CSE — 8 students"),
    ("🟢", "Community 2", "CIVIL — 8 students"),
    ("🔵", "Community 3", "ECE — 7 students"),
    ("🟡", "Community 4", "ME — 7 students"),
]
for i, (dot, comm, detail) in enumerate(legend):
    ty = 2.1 + i * 1.1
    txt(sl, dot,    9.4,  ty, 0.4, 0.5, size=22)
    txt(sl, comm,   9.85, ty, 2.9, 0.38, size=14, bold=True, color=WHITE)
    txt(sl, detail, 9.85, ty+0.42, 2.9, 0.38, size=12, color=ACCENT2)

txt(sl, "Node SIZE = Degree Centrality\n(bigger = more connected)",
    9.4, 6.05, 3.4, 0.75, size=12, italic=True, color=YELLOW)
footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — CENTRALITY & DISTRIBUTION CHARTS
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Visualization — Centrality & Degree Distribution")

pic(sl, os.path.join(GRAPHS, "centrality_comparison.png"), 0.3, 1.35, 6.8, 4.8)
pic(sl, os.path.join(GRAPHS, "degree_distribution.png"),   7.25, 1.35, 5.75, 4.8)

txt(sl, "Fig 2: Top-10 students per centrality measure (4 charts)",
    0.3, 6.2, 6.8, 0.35, size=11, italic=True, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
txt(sl, "Fig 3: Most students have exactly 5 connections (mean=5.13)",
    7.25, 6.2, 5.75, 0.35, size=11, italic=True, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — COMMUNITY SIZE CHART
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Visualization — Community Size Distribution", "Balanced communities across departments")

pic(sl, os.path.join(GRAPHS, "community_sizes.png"), 1.5, 1.35, 7.5, 5.3)

card(sl, 9.4, 1.35, 3.55, 5.3)
txt(sl, "Key Insight", 9.6, 1.5, 3.1, 0.4, size=15, bold=True, color=ACCENT)
bullet_box(sl, [
    {"label": "4 Communities Found",          "color": GREEN,  "bold": True},
    {"label": "CSE:   8 members",             "color": WHITE},
    {"label": "CIVIL: 8 members",             "color": WHITE},
    {"label": "ECE:   7 members",             "color": WHITE},
    {"label": "ME:    7 members",             "color": WHITE},
    {"label": "All nearly equal size!",       "color": YELLOW, "bold": True},
    {"label": "Modularity = 0.6278",          "color": GREEN,  "bold": True},
    {"label": "(Excellent — >0.3 is good)",   "color": ACCENT2},
], 9.55, 2.1, 3.2, 4.3, size=13, bullet="  ")
footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — CONCLUSION & FUTURE SCOPE
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
header_bar(sl, "Conclusion & Future Scope")

# Conclusion
card(sl, 0.3, 1.38, 6.15, 5.65)
txt(sl, "✅  Conclusion", 0.5, 1.52, 5.7, 0.42, size=17, bold=True, color=GREEN)
conclusions = [
    "30 students, 77 edges — fully connected network",
    "Diameter = 5 hops (anyone reachable in 5 steps)",
    "#1 Influential: Harsh Malhotra (ME)\n      → Highest betweenness centrality",
    "4 communities detected (Q = 0.6278)\n      → Perfectly matches departments!",
    "NetworkX + Gephi = powerful SNA toolkit",
]
bullet_box(sl, conclusions, 0.5, 2.05, 5.7, 4.8, size=14, color=LIGHT_GRAY)

# Future Scope
card(sl, 6.75, 1.38, 6.2, 5.65)
txt(sl, "🚀  Future Scope", 6.95, 1.52, 5.8, 0.42, size=17, bold=True, color=ORANGE)
future = [
    "Scale to 500+ students with real data",
    "Use directed graph (who initiates friendship)",
    "Temporal analysis — track network over time",
    "Influence Maximization for info spreading",
    "Build Flask web app for interactive SNA",
    "Apply to real Twitter/LinkedIn data",
]
bullet_box(sl, future, 6.95, 2.05, 5.8, 4.8, size=14, color=LIGHT_GRAY)
footer(sl)

# ═════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — THANK YOU
# ═════════════════════════════════════════════════════════════════════════════
sl = add_slide(); bg(sl)
box(sl, 0, 0, 13.33, 7.5, fill=RGBColor(0x02, 0x3E, 0x8A))
box(sl, 0, 0,    13.33, 0.08, fill=ACCENT)
box(sl, 0, 7.42, 13.33, 0.08, fill=ACCENT)

txt(sl, "Thank You!", 0.5, 1.5, 12.33, 1.5,
    size=60, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(sl, "Questions & Discussion", 0.5, 3.1, 12.33, 0.7,
    size=24, color=ACCENT2, align=PP_ALIGN.CENTER)

box(sl, 2.5, 4.1, 8.33, 0.04, fill=ACCENT)

for i, (label, val) in enumerate([
    ("Project",  "Social Network Analysis — Community Detection & Influential User ID"),
    ("Tools",    "Python  •  NetworkX  •  Gephi  •  Pandas  •  Matplotlib"),
    ("Output",   "4 Charts  •  Word Report  •  GEXF file for Gephi"),
]):
    txt(sl, f"{label}:  {val}", 0.5, 4.4 + i*0.72, 12.33, 0.55,
        size=14, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

txt(sl, "Department of Computer Science & Engineering  |  Academic Year 2024–25",
    0.5, 6.7, 12.33, 0.45,
    size=13, italic=True, color=ACCENT2, align=PP_ALIGN.CENTER)

# ── Save ─────────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT), exist_ok=True)
prs.save(OUT)
print(f"\nPresentation saved to:\n    {OUT}")
print(f"    Slides: {len(prs.slides)}")
