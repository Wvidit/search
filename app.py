"""
Research Finder Agent - Streamlit Frontend
Beautiful, modern UI for discovering professors, labs, and internships
in AI+Materials and Computer Vision.
"""

import streamlit as st
import json
import time
from agent import create_client, run_full_search
from config import SEARCH_CATEGORIES, AVAILABLE_MODELS, DEFAULT_MODEL

# ──────────────── Page Configuration ────────────────
st.set_page_config(
    page_title="Research Finder Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────── Custom CSS ────────────────
st.markdown(
    """
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global Styles ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 40%, #16213e 100%);
}

/* ── Hero Section ── */
.hero-container {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #667eea 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 4s ease infinite;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}

@keyframes gradient-shift {
    0% { background-position: 0% center; }
    50% { background-position: 100% center; }
    100% { background-position: 0% center; }
}

.hero-subtitle {
    font-size: 1.15rem;
    color: #a8b2d1;
    font-weight: 400;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.6;
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15));
    border: 1px solid rgba(102,126,234,0.3);
    border-radius: 50px;
    padding: 0.35rem 1rem;
    font-size: 0.8rem;
    color: #667eea;
    font-weight: 600;
    margin-top: 1rem;
    letter-spacing: 0.05em;
}

/* ── Sidebar Styles ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid rgba(102,126,234,0.2);
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e6f1ff !important;
}

section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown label {
    color: #a8b2d1 !important;
}

/* ── Card Styles ── */
.result-card {
    background: linear-gradient(135deg, rgba(26,26,46,0.95), rgba(22,33,62,0.95));
    border: 1px solid rgba(102,126,234,0.2);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    border-radius: 16px 16px 0 0;
}

.result-card:hover {
    border-color: rgba(102,126,234,0.5);
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3), 0 0 30px rgba(102,126,234,0.1);
}

.card-name {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e6f1ff;
    margin-bottom: 0.3rem;
}

.card-affiliation {
    font-size: 0.95rem;
    color: #8892b0;
    margin-bottom: 1rem;
    font-weight: 500;
}

.card-section-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: #667eea;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 1rem;
    margin-bottom: 0.4rem;
}

.card-text {
    font-size: 0.9rem;
    color: #a8b2d1;
    line-height: 1.6;
}

.card-tag {
    display: inline-block;
    background: rgba(102,126,234,0.12);
    border: 1px solid rgba(102,126,234,0.25);
    color: #667eea;
    border-radius: 8px;
    padding: 0.25rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 0.15rem 0.2rem;
}

.card-link {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white !important;
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
    font-weight: 600;
    text-decoration: none;
    margin: 0.2rem 0.3rem;
    transition: all 0.2s ease;
}

.card-link:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(102,126,234,0.4);
}

.card-link-secondary {
    display: inline-block;
    background: rgba(102,126,234,0.1);
    border: 1px solid rgba(102,126,234,0.3);
    color: #667eea !important;
    border-radius: 8px;
    padding: 0.35rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 500;
    text-decoration: none;
    margin: 0.2rem 0.3rem;
    transition: all 0.2s ease;
}

.card-link-secondary:hover {
    background: rgba(102,126,234,0.2);
}

.notable-badge {
    background: linear-gradient(135deg, rgba(240,147,251,0.12), rgba(118,75,162,0.12));
    border: 1px solid rgba(240,147,251,0.3);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin-top: 0.8rem;
    font-size: 0.85rem;
    color: #f093fb;
    line-height: 1.5;
}

/* ── Category Header ── */
.category-header {
    background: linear-gradient(135deg, rgba(102,126,234,0.08), rgba(118,75,162,0.08));
    border: 1px solid rgba(102,126,234,0.15);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin: 2rem 0 1.5rem;
    text-align: center;
}

.category-title {
    font-size: 1.8rem;
    font-weight: 800;
    color: #e6f1ff;
    margin-bottom: 0.3rem;
}

.category-desc {
    font-size: 0.95rem;
    color: #8892b0;
    font-weight: 400;
}

/* ── Stats Bar ── */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 2rem;
    padding: 1rem 0;
    margin: 1rem 0;
}

.stat-item {
    text-align: center;
    padding: 1rem 2rem;
    background: rgba(102,126,234,0.06);
    border: 1px solid rgba(102,126,234,0.15);
    border-radius: 12px;
    min-width: 130px;
}

.stat-number {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    font-size: 0.8rem;
    color: #8892b0;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Loading Animation ── */
.search-animation {
    text-align: center;
    padding: 3rem;
}

.search-animation .pulse {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #667eea;
    margin: 0 5px;
    animation: pulse 1.4s ease-in-out infinite;
}

.search-animation .pulse:nth-child(2) { animation-delay: 0.2s; }
.search-animation .pulse:nth-child(3) { animation-delay: 0.4s; }

@keyframes pulse {
    0%, 100% { transform: scale(0.8); opacity: 0.5; }
    50% { transform: scale(1.3); opacity: 1; }
}

/* ── Source Citation ── */
.source-chip {
    display: inline-block;
    background: rgba(102,126,234,0.08);
    border: 1px solid rgba(102,126,234,0.15);
    border-radius: 6px;
    padding: 0.2rem 0.5rem;
    font-size: 0.72rem;
    color: #8892b0;
    margin: 0.1rem;
    text-decoration: none;
}

.source-chip:hover {
    background: rgba(102,126,234,0.15);
    color: #667eea;
}

/* ── Error box ── */
.error-box {
    background: rgba(255,82,82,0.08);
    border: 1px solid rgba(255,82,82,0.3);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: #ff5252;
    font-size: 0.9rem;
    margin: 1rem 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: #1a1a2e;
}
::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 3px;
}

/* ── Button Override ── */
.stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em;
    transition: all 0.3s ease !important;
    width: 100%;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.35) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(102,126,234,0.08) !important;
    border: 1px solid rgba(102,126,234,0.15) !important;
    border-radius: 10px !important;
    color: #a8b2d1 !important;
    padding: 0.5rem 1.2rem !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2)) !important;
    border-color: rgba(102,126,234,0.4) !important;
    color: #e6f1ff !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(102,126,234,0.06) !important;
    border-radius: 10px !important;
    color: #e6f1ff !important;
}

/* ── Download button ── */
.stDownloadButton>button {
    background: linear-gradient(135deg, #11998e, #38ef7d) !important;
    color: #0f0c29 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# ──────────────── Helper Functions ────────────────


def render_professor_card(prof: dict, idx: int):
    """Render a professor result card."""
    name = prof.get("name", "Unknown")
    title = prof.get("title", "")
    university = prof.get("university", "")
    department = prof.get("department", "")
    email = prof.get("email", "Not listed")
    website = prof.get("website", "")
    scholar = prof.get("google_scholar", "")
    areas = prof.get("research_areas", [])
    projects = prof.get("notable_projects", [])
    publications = prof.get("recent_publications", [])
    why = prof.get("why_notable", "")
    interdisciplinary = prof.get("interdisciplinary_info", "")
    accepts = prof.get("accepts_interns", "Unknown")
    intern_link = prof.get("internship_link", "")

    # Research area tags
    area_tags = "".join([f'<span class="card-tag">{a}</span>' for a in areas[:6]])

    # Projects list
    projects_html = ""
    for p in projects[:3]:
        projects_html += f'<div class="card-text">• {p}</div>'

    # Publications list
    pubs_html = ""
    for p in publications[:3]:
        pubs_html += f'<div class="card-text" style="font-style:italic;">📄 {p}</div>'

    # Links
    links_html = ""
    if website and website != "Not publicly listed":
        links_html += f'<a href="{website}" target="_blank" class="card-link">🌐 Website</a>'
    if scholar and scholar != "Not publicly listed":
        links_html += f'<a href="{scholar}" target="_blank" class="card-link-secondary">📊 Scholar</a>'
    if intern_link and "check" not in intern_link.lower() and intern_link != "Not publicly listed":
        links_html += f'<a href="{intern_link}" target="_blank" class="card-link">📋 Apply</a>'

    # Notable badge
    notable_html = ""
    if why:
        notable_html = f'<div class="notable-badge">⭐ {why}</div>'
    if interdisciplinary:
        notable_html += f'<div class="notable-badge" style="color:#38ef7d;border-color:rgba(56,239,125,0.3);background:rgba(56,239,125,0.08);">🤝 {interdisciplinary}</div>'

    html = f"""
    <div class="result-card">
        <div class="card-name">{name}</div>
        <div class="card-affiliation">{title} · {department} · {university}</div>
        <div style="margin-bottom:0.5rem;">📧 <span class="card-text">{email}</span></div>
        <div style="margin-bottom:0.5rem;">🎯 Accepts Interns: <span class="card-text" style="color:{'#38ef7d' if 'yes' in accepts.lower() else '#f093fb'}">{accepts}</span></div>
        <div class="card-section-title">Research Areas</div>
        <div style="margin-bottom:0.5rem;">{area_tags}</div>
        <div class="card-section-title">Notable Projects</div>
        {projects_html}
        <div class="card-section-title">Recent Publications</div>
        {pubs_html}
        {notable_html}
        <div style="margin-top:1rem;">{links_html}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_student_card(student: dict):
    """Render a PhD student result card."""
    name = student.get("name", "Unknown")
    university = student.get("university", "")
    advisor = student.get("advisor", "")
    year = student.get("year", "")
    focus = student.get("research_focus", "")
    email = student.get("email", "Not listed")
    website = student.get("website", "")
    scholar = student.get("google_scholar", "")
    works = student.get("notable_work", [])
    awards = student.get("awards", [])
    why = student.get("why_exceptional", "")

    works_html = ""
    for w in works[:3]:
        works_html += f'<div class="card-text">• {w}</div>'

    awards_html = ""
    for a in awards[:4]:
        awards_html += f'<span class="card-tag" style="border-color:rgba(240,147,251,0.3);color:#f093fb;background:rgba(240,147,251,0.1);">🏆 {a}</span>'

    links_html = ""
    if website:
        links_html += f'<a href="{website}" target="_blank" class="card-link">🌐 Website</a>'
    if scholar:
        links_html += f'<a href="{scholar}" target="_blank" class="card-link-secondary">📊 Scholar</a>'

    html = f"""
    <div class="result-card">
        <div class="card-name">{name}</div>
        <div class="card-affiliation">{year} PhD Student · {university} · Advisor: {advisor}</div>
        <div style="margin-bottom:0.5rem;">📧 <span class="card-text">{email}</span></div>
        <div class="card-section-title">Research Focus</div>
        <div class="card-text">{focus}</div>
        <div class="card-section-title">Notable Work</div>
        {works_html}
        <div class="card-section-title">Awards & Honors</div>
        <div>{awards_html}</div>
        <div class="notable-badge">⭐ {why}</div>
        <div style="margin-top:1rem;">{links_html}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_lab_card(lab: dict):
    """Render a research lab result card."""
    name = lab.get("name", "Unknown")
    institution = lab.get("university", lab.get("institution", ""))
    director = lab.get("director", "")
    website = lab.get("website", "")
    focus = lab.get("research_focus", [])
    projects = lab.get("notable_projects", [])
    team = lab.get("team_size", "Unknown")
    accepts = lab.get("accepts_interns", "Unknown")
    intern_info = lab.get("internship_info", "")
    intern_link = lab.get("internship_link", "")
    why = lab.get("why_renowned", "")

    focus_tags = "".join([f'<span class="card-tag">{f}</span>' for f in focus[:6]])

    projects_html = ""
    for p in projects[:3]:
        projects_html += f'<div class="card-text">• {p}</div>'

    links_html = ""
    if website:
        links_html += f'<a href="{website}" target="_blank" class="card-link">🌐 Lab Website</a>'
    if intern_link and "check" not in intern_link.lower():
        links_html += f'<a href="{intern_link}" target="_blank" class="card-link">📋 Apply for Internship</a>'

    html = f"""
    <div class="result-card">
        <div class="card-name">{name}</div>
        <div class="card-affiliation">🏛️ {institution} · Director: {director} · Team: ~{team}</div>
        <div style="margin-bottom:0.5rem;">🎯 Accepts Interns: <span class="card-text" style="color:{'#38ef7d' if 'yes' in str(accepts).lower() else '#f093fb'}">{accepts}</span></div>
        <div class="card-section-title">Research Focus</div>
        <div style="margin-bottom:0.5rem;">{focus_tags}</div>
        <div class="card-section-title">Notable Projects</div>
        {projects_html}
        <div class="card-section-title">How to Apply</div>
        <div class="card-text">{intern_info}</div>
        <div class="notable-badge">⭐ {why}</div>
        <div style="margin-top:1rem;">{links_html}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_internship_card(intern: dict):
    """Render an internship opportunity card."""
    name = intern.get("program_name", "Unknown")
    institution = intern.get("institution", "")
    desc = intern.get("description", "")
    areas = intern.get("research_areas", [])
    eligibility = intern.get("eligibility", "")
    duration = intern.get("duration", "")
    stipend = intern.get("stipend", "")
    deadline = intern.get("application_deadline", "")
    link = intern.get("application_link", "")
    contact = intern.get("contact_email", "")
    notes = intern.get("notes", "")

    area_tags = "".join([f'<span class="card-tag">{a}</span>' for a in areas[:5]])

    links_html = ""
    if link:
        links_html += f'<a href="{link}" target="_blank" class="card-link">🚀 Apply Now</a>'

    html = f"""
    <div class="result-card">
        <div class="card-name">{name}</div>
        <div class="card-affiliation">🏛️ {institution}</div>
        <div class="card-text" style="margin-bottom:0.8rem;">{desc}</div>
        <div class="card-section-title">Research Areas</div>
        <div style="margin-bottom:0.5rem;">{area_tags}</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin:0.8rem 0;">
            <div class="card-text">📅 <strong>Deadline:</strong> {deadline}</div>
            <div class="card-text">⏱️ <strong>Duration:</strong> {duration}</div>
            <div class="card-text">💰 <strong>Stipend:</strong> {stipend}</div>
            <div class="card-text">📧 <strong>Contact:</strong> {contact}</div>
        </div>
        <div class="card-section-title">Eligibility</div>
        <div class="card-text">{eligibility}</div>
        {'<div class="card-text" style="margin-top:0.5rem;">📝 ' + notes + '</div>' if notes else ''}
        <div style="margin-top:1rem;">{links_html}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_sources(sources: list):
    """Render grounding sources."""
    if not sources:
        return
    chips = ""
    for s in sources[:10]:
        url = s.get("url", "#")
        title = s.get("title", "Source")[:50]
        chips += f'<a href="{url}" target="_blank" class="source-chip">🔗 {title}</a> '
    st.markdown(
        f'<div style="margin-top:0.5rem;margin-bottom:1rem;">📚 <span style="color:#8892b0;font-size:0.8rem;">Sources: </span>{chips}</div>',
        unsafe_allow_html=True,
    )


# ──────────────── Hero Section ────────────────
st.markdown(
    """
<div class="hero-container">
    <div class="hero-title">Research Finder Agent</div>
    <div class="hero-subtitle">
        AI-powered discovery of top professors, labs, PhD researchers, and internship opportunities 
        in AI+Materials Science and Computer Vision — surfacing only the best from QS Top 100 
        universities and Stanford's Top 2% researchers.
    </div>
    <div class="hero-badge">⚡ POWERED BY GEMINI + GOOGLE SEARCH</div>
</div>
""",
    unsafe_allow_html=True,
)

# ──────────────── Sidebar ────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    api_key = st.text_input(
        "🔑 Gemini API Key",
        type="password",
        help="Get your free API key from https://aistudio.google.com/apikey",
        placeholder="Enter your Gemini API key...",
    )

    st.markdown("### 🤖 Model Selection")
    selected_model_name = st.selectbox(
        "Choose Gemini Model",
        options=list(AVAILABLE_MODELS.keys()),
        index=list(AVAILABLE_MODELS.keys()).index(DEFAULT_MODEL),
        help="Gemini 3 Flash is fastest, Gemini 3 Pro gives more detailed results, Gemini 2.0 Flash is the stable fallback.",
    )
    selected_model_id = AVAILABLE_MODELS[selected_model_name]

    st.markdown(
        f"""
    <div style="background:rgba(102,126,234,0.08);border:1px solid rgba(102,126,234,0.2);border-radius:10px;padding:0.6rem 0.8rem;margin:0.3rem 0 0.8rem;font-size:0.78rem;color:#a8b2d1;">
        🤖 Using: <strong style="color:#f093fb;">{selected_model_name}</strong><br>
        <code style="font-size:0.72rem;color:#667eea;">{selected_model_id}</code>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="background:rgba(102,126,234,0.08);border:1px solid rgba(102,126,234,0.2);border-radius:10px;padding:0.8rem;margin:0.8rem 0;font-size:0.82rem;color:#a8b2d1;">
        💡 <strong style="color:#667eea;">Free Tier</strong>: Get your API key from 
        <a href="https://aistudio.google.com/apikey" target="_blank" style="color:#667eea;">Google AI Studio</a>. 
        No credit card required.
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎯 Search Categories")

    selected_categories = []
    for key, cat in SEARCH_CATEGORIES.items():
        if st.checkbox(cat["title"], value=True, key=f"cat_{key}"):
            selected_categories.append(key)

    st.markdown("---")
    st.markdown("### 📊 Quality Filters")
    st.markdown(
        """
    <div style="font-size:0.82rem;color:#a8b2d1;line-height:1.6;">
    ✅ Stanford Top 2% Researchers<br>
    ✅ QS World Top 100 Universities<br>
    ✅ Active publications (last 2-3 years)<br>
    ✅ Interdisciplinary-friendly
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    search_clicked = st.button("🔍 Launch Search Agent", use_container_width=True)

# ──────────────── Main Content ────────────────

if not api_key and not search_clicked:
    # Show welcome state
    st.markdown(
        """
    <div style="text-align:center;padding:3rem 1rem;">
        <div style="font-size:4rem;margin-bottom:1rem;">🔬</div>
        <div style="font-size:1.3rem;color:#e6f1ff;font-weight:600;margin-bottom:0.5rem;">Ready to Discover</div>
        <div style="font-size:0.95rem;color:#8892b0;max-width:500px;margin:0 auto;line-height:1.6;">
            Enter your Gemini API key in the sidebar and hit <strong style="color:#667eea;">Launch Search Agent</strong> 
            to find top researchers, labs, and internship opportunities powered by AI.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Feature cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
        <div class="result-card" style="text-align:center;min-height:200px;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">🔬</div>
            <div style="color:#e6f1ff;font-weight:700;font-size:1.05rem;margin-bottom:0.5rem;">AI + Materials</div>
            <div class="card-text">Find professors pioneering AI/ML integration in ceramic materials and advanced materials science</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
        <div class="result-card" style="text-align:center;min-height:200px;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">👁️</div>
            <div style="color:#e6f1ff;font-weight:700;font-size:1.05rem;margin-bottom:0.5rem;">Computer Vision</div>
            <div class="card-text">Discover CV professors who welcome interdisciplinary students from non-CS backgrounds</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
        <div class="result-card" style="text-align:center;min-height:200px;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">🚀</div>
            <div style="color:#e6f1ff;font-weight:700;font-size:1.05rem;margin-bottom:0.5rem;">Internships</div>
            <div class="card-text">Get direct links to research internship programs at top labs and universities worldwide</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

elif search_clicked and not api_key:
    st.markdown(
        '<div class="error-box">⚠️ Please enter your Gemini API key in the sidebar to start searching.</div>',
        unsafe_allow_html=True,
    )

elif search_clicked and api_key:
    if not selected_categories:
        st.markdown(
            '<div class="error-box">⚠️ Please select at least one search category from the sidebar.</div>',
            unsafe_allow_html=True,
        )
    else:
        # Initialize client
        try:
            client = create_client(api_key)
        except Exception as e:
            st.markdown(
                f'<div class="error-box">❌ Failed to initialize Gemini client: {e}</div>',
                unsafe_allow_html=True,
            )
            st.stop()

        category_labels = {k: v["title"] for k, v in SEARCH_CATEGORIES.items()}

        all_results = {}

        # Progress tracking
        total = len(selected_categories)
        progress_bar = st.progress(0, text="Initializing search agent...")

        for i, category in enumerate(selected_categories):
            label = category_labels.get(category, category)
            progress_bar.progress(
                (i) / total,
                text=f"🔍 Searching: {label}... ({i+1}/{total})",
            )

            with st.spinner(f"🌐 Agent is surfing the web for {label}..."):
                from agent import (
                    search_professors_materials,
                    search_professors_cv,
                    search_phd_students,
                    search_labs,
                    search_internships,
                )

                fn_map = {
                    "professors_materials": search_professors_materials,
                    "professors_cv": search_professors_cv,
                    "phd_students": search_phd_students,
                    "labs": search_labs,
                    "internships": search_internships,
                }

                result = fn_map[category](client, model=selected_model_id)
                all_results[category] = result

        progress_bar.progress(1.0, text="✅ Search complete!")
        time.sleep(0.5)
        progress_bar.empty()

        # Store results in session
        st.session_state["results"] = all_results

        # ── Stats Bar ──
        total_profs = 0
        total_students = 0
        total_labs = 0
        total_internships = 0

        for cat, res in all_results.items():
            if "error" not in res:
                if cat in ("professors_materials", "professors_cv"):
                    total_profs += len(res.get("professors", []))
                elif cat == "phd_students":
                    total_students += len(res.get("phd_students", []))
                elif cat == "labs":
                    total_labs += len(res.get("labs", []))
                elif cat == "internships":
                    total_internships += len(res.get("internships", []))

        st.markdown(
            f"""
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-number">{total_profs}</div>
                <div class="stat-label">Professors</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{total_students}</div>
                <div class="stat-label">PhD Students</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{total_labs}</div>
                <div class="stat-label">Labs</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{total_internships}</div>
                <div class="stat-label">Internships</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # ── Render Results by Category ──
        tab_labels = [
            category_labels[c] for c in selected_categories if c in all_results
        ]
        if tab_labels:
            tabs = st.tabs(tab_labels)

            for tab, category in zip(tabs, selected_categories):
                with tab:
                    result = all_results.get(category, {})
                    cat_info = SEARCH_CATEGORIES[category]

                    st.markdown(
                        f"""
                    <div class="category-header">
                        <div class="category-title">{cat_info['title']}</div>
                        <div class="category-desc">{cat_info['description']}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    if "error" in result:
                        st.markdown(
                            f'<div class="error-box">❌ {result["error"]}</div>',
                            unsafe_allow_html=True,
                        )
                        if "raw_text" in result:
                            with st.expander("🔍 View Raw Response"):
                                st.text(result["raw_text"])
                        continue

                    # Render sources
                    render_sources(result.get("_sources", []))

                    # Render results based on category
                    if category in ("professors_materials", "professors_cv"):
                        professors = result.get("professors", [])
                        if not professors:
                            st.info("No results found for this category.")
                            continue
                        for i, prof in enumerate(professors):
                            render_professor_card(prof, i)

                    elif category == "phd_students":
                        students = result.get("phd_students", [])
                        if not students:
                            st.info("No results found for this category.")
                            continue
                        for s in students:
                            render_student_card(s)

                    elif category == "labs":
                        labs = result.get("labs", [])
                        if not labs:
                            st.info("No results found for this category.")
                            continue
                        for l in labs:
                            render_lab_card(l)

                    elif category == "internships":
                        internships = result.get("internships", [])
                        if not internships:
                            st.info("No results found for this category.")
                            continue
                        for intern in internships:
                            render_internship_card(intern)

        # ── Download Results ──
        st.markdown("---")
        st.markdown("### 💾 Export Results")

        # Clean results for export (remove internal keys)
        export_data = {}
        for k, v in all_results.items():
            export_data[k] = {
                key: val for key, val in v.items() if not key.startswith("_")
            }

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download as JSON",
                data=json.dumps(export_data, indent=2),
                file_name="research_finder_results.json",
                mime="application/json",
                use_container_width=True,
            )
        with col2:
            # Generate a text summary
            summary_lines = ["RESEARCH FINDER AGENT - RESULTS SUMMARY", "=" * 50, ""]
            for cat, res in export_data.items():
                cat_title = SEARCH_CATEGORIES.get(cat, {}).get("title", cat)
                summary_lines.append(f"\n{'='*50}")
                summary_lines.append(f"  {cat_title}")
                summary_lines.append(f"{'='*50}\n")

                if "error" in res:
                    summary_lines.append(f"  Error: {res['error']}\n")
                    continue

                if "professors" in res:
                    for p in res["professors"]:
                        summary_lines.append(f"  👤 {p.get('name', 'N/A')}")
                        summary_lines.append(
                            f"     {p.get('title', '')} - {p.get('university', '')}"
                        )
                        summary_lines.append(f"     📧 {p.get('email', 'N/A')}")
                        summary_lines.append(f"     🌐 {p.get('website', 'N/A')}")
                        areas = ", ".join(p.get("research_areas", []))
                        summary_lines.append(f"     🔬 Areas: {areas}")
                        summary_lines.append(
                            f"     ⭐ {p.get('why_notable', 'N/A')}"
                        )
                        summary_lines.append("")

                if "phd_students" in res:
                    for s in res["phd_students"]:
                        summary_lines.append(f"  🎓 {s.get('name', 'N/A')}")
                        summary_lines.append(
                            f"     {s.get('university', '')} - Advisor: {s.get('advisor', '')}"
                        )
                        summary_lines.append(f"     📧 {s.get('email', 'N/A')}")
                        summary_lines.append(
                            f"     🔬 Focus: {s.get('research_focus', 'N/A')}"
                        )
                        summary_lines.append("")

                if "labs" in res:
                    for l in res["labs"]:
                        summary_lines.append(f"  🏛️ {l.get('name', 'N/A')}")
                        summary_lines.append(
                            f"     {l.get('university', l.get('institution', ''))}"
                        )
                        summary_lines.append(f"     Director: {l.get('director', 'N/A')}")
                        summary_lines.append(f"     🌐 {l.get('website', 'N/A')}")
                        summary_lines.append("")

                if "internships" in res:
                    for i in res["internships"]:
                        summary_lines.append(
                            f"  📋 {i.get('program_name', 'N/A')}"
                        )
                        summary_lines.append(
                            f"     {i.get('institution', '')}"
                        )
                        summary_lines.append(
                            f"     📅 Deadline: {i.get('application_deadline', 'N/A')}"
                        )
                        summary_lines.append(
                            f"     🔗 {i.get('application_link', 'N/A')}"
                        )
                        summary_lines.append("")

            st.download_button(
                label="📄 Download as Text",
                data="\n".join(summary_lines),
                file_name="research_finder_results.txt",
                mime="text/plain",
                use_container_width=True,
            )

# ── Show cached results if they exist ──
elif "results" in st.session_state and not search_clicked:
    all_results = st.session_state["results"]

    category_labels = {k: v["title"] for k, v in SEARCH_CATEGORIES.items()}

    # Stats
    total_profs = 0
    total_students = 0
    total_labs = 0
    total_internships = 0

    for cat, res in all_results.items():
        if "error" not in res:
            if cat in ("professors_materials", "professors_cv"):
                total_profs += len(res.get("professors", []))
            elif cat == "phd_students":
                total_students += len(res.get("phd_students", []))
            elif cat == "labs":
                total_labs += len(res.get("labs", []))
            elif cat == "internships":
                total_internships += len(res.get("internships", []))

    st.markdown(
        f"""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number">{total_profs}</div>
            <div class="stat-label">Professors</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_students}</div>
            <div class="stat-label">PhD Students</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_labs}</div>
            <div class="stat-label">Labs</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_internships}</div>
            <div class="stat-label">Internships</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    available = [c for c in all_results if c in SEARCH_CATEGORIES]
    tab_labels = [category_labels[c] for c in available]

    if tab_labels:
        tabs = st.tabs(tab_labels)
        for tab, category in zip(tabs, available):
            with tab:
                result = all_results.get(category, {})
                cat_info = SEARCH_CATEGORIES[category]

                st.markdown(
                    f"""
                <div class="category-header">
                    <div class="category-title">{cat_info['title']}</div>
                    <div class="category-desc">{cat_info['description']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                if "error" in result:
                    st.markdown(
                        f'<div class="error-box">❌ {result["error"]}</div>',
                        unsafe_allow_html=True,
                    )
                    continue

                render_sources(result.get("_sources", []))

                if category in ("professors_materials", "professors_cv"):
                    for i, prof in enumerate(result.get("professors", [])):
                        render_professor_card(prof, i)
                elif category == "phd_students":
                    for s in result.get("phd_students", []):
                        render_student_card(s)
                elif category == "labs":
                    for l in result.get("labs", []):
                        render_lab_card(l)
                elif category == "internships":
                    for intern in result.get("internships", []):
                        render_internship_card(intern)

# ── Footer ──
st.markdown(
    """
<div style="text-align:center;padding:3rem 1rem 2rem;border-top:1px solid rgba(102,126,234,0.1);margin-top:3rem;">
    <div style="color:#8892b0;font-size:0.82rem;">
        Built with ❤️ using <strong style="color:#667eea;">Gemini 2.0 Flash</strong> + 
        <strong style="color:#667eea;">Google Search</strong> grounding · 
        <span style="color:#f093fb;">Research Finder Agent</span>
    </div>
    <div style="color:#495670;font-size:0.72rem;margin-top:0.3rem;">
        Results are AI-generated and should be verified independently. Contact details shown are publicly available.
    </div>
</div>
""",
    unsafe_allow_html=True,
)
