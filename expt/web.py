import streamlit as st
import os
import subprocess
import sys
import glob
import shutil
import tempfile
import base64

# 1. Set Page Configuration
st.set_page_config(
    page_title="CMP-226 Graph Theory and Combinatorics Lab",
    layout="wide",
)

# Initialize sidebar toggle state
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Asset Processing (Logo)
LOGO_PATH = os.path.join(BASE_DIR, "Goa_College_of_Engineering_logo.jpeg")
if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    logo_src = f"data:image/png;base64,{encoded_logo}"
else:
    logo_src = "https://via.placeholder.com/80"

# 3. Global Styles (Fixed Header Fixes)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght=0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght=400;500;600&family=Plus+Jakarta+Sans:wght=300;400;500;600;700&display=swap');

/* Apply font to Streamlit default text elements */
html, body, [class*="css"], .stMarkdown, p, span, label, .stTabs {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Base backgrounds & paper pattern */
[data-testid="stAppViewContainer"] {
    background-color: #f7f6f2 !important;
    background-image: radial-gradient(#e5dec9 0.9px, #f7f6f2 0.9px);
    background-size: 24px 24px;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #f1ede6 !important;
    border-right: 1px solid #e1dbcf;
    transition: transform 0.3s ease, width 0.3s ease !important;
}
[data-testid="stSidebar"] * {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #2d3748 !important; /* Force dark text in sidebar for dark mode compatibility */
}

/* Sidebar hidden state - applied via body class */
body.sidebar-hidden [data-testid="stSidebar"] {
    display: none !important;
}
body.sidebar-hidden section[data-testid="stMain"] {
    margin-left: 0 !important;
}

/* Masthead sidebar toggle button */
.masthead-toggle-btn {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: rgba(27, 42, 74, 0.06) !important;
    border: 1px solid rgba(27, 42, 74, 0.12) !important;
    border-radius: 8px !important;
    width: 40px !important;
    height: 40px !important;
    cursor: pointer !important;
    transition: background 0.2s ease, box-shadow 0.2s ease !important;
    flex-shrink: 0 !important;
    text-decoration: none !important;
    margin-left: auto !important;
    margin-right: 5.5rem !important;
}
.masthead-toggle-btn:hover {
    background: rgba(27, 42, 74, 0.12) !important;
    box-shadow: 0 2px 8px rgba(27, 42, 74, 0.1) !important;
}
.masthead-toggle-btn svg {
    width: 18px !important;
    height: 18px !important;
    stroke: #1b2a4a !important;
    stroke-width: 2 !important;
    fill: none !important;
    stroke-linecap: round !important;
    stroke-linejoin: round !important;
}

/* Sidebar title and items styling */
div[data-testid="stSidebarUserContent"] h3 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    color: #1b2a4a !important;
    border-bottom: 2px solid #b08850;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem !important;
}
/* Style the radio items inside the sidebar */
div[data-testid="stSidebarUserContent"] [data-testid="stWidgetLabel"] p {
    font-weight: 600 !important;
    color: #1b2a4a !important;
    font-size: 0.88rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
/* Style selected radio button labels */
div[data-testid="stSidebarUserContent"] label[data-baseweb="radio"] {
    background-color: transparent;
    border: 1px solid transparent;
    padding: 6px 12px;
    border-radius: 6px;
    transition: all 0.2s ease;
    margin-bottom: 4px;
}
div[data-testid="stSidebarUserContent"] label[data-baseweb="radio"]:hover {
    background-color: rgba(176, 136, 80, 0.08);
}
div[data-testid="stSidebarUserContent"] label[data-baseweb="radio"] * {
    color: #4a5568 !important; /* Dark text for unselected options */
}
div[data-testid="stSidebarUserContent"] label[data-baseweb="radio"][data-checked="true"] {
    background-color: #ffffff;
    border: 1px solid #e1dbcf;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
}
div[data-testid="stSidebarUserContent"] label[data-baseweb="radio"][data-checked="true"] * {
    color: #1b2a4a !important; /* Accent dark text for active option */
    font-weight: 600 !important;
}

/* Remove default header background and let buttons float on top */
[data-testid="stHeader"] {
    background-color: transparent !important;
    z-index: 100000000 !important; /* 100 million to float above the fixed header */
    pointer-events: none;
}
[data-testid="stHeader"] * {
    pointer-events: auto;
}
[data-testid="stHeader"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #1b2a4a 0%, #b08850 100%);
    z-index: 100000001;
}

/* Main Content Box - Pushed down to clear fixed header */
.main .block-container {
    max-width: 1080px !important;
    padding-top: 210px !important;
    padding-bottom: 5rem !important;
}

/* Push sidebar content down just enough to clear the collapse button */
[data-testid="stSidebarUserContent"] {
    padding-top: 4rem !important;
}

/* --- Academic Masthead (Fixed on Top) --- */
.academic-masthead {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 140px !important;
    background: #ffffff !important;
    border-bottom: 1px solid #e1dbcf !important;
    z-index: 999999 !important; /* Set below sidebar and header toggle buttons */
    padding: 0 5rem !important; /* Wide padding to leave room for Streamlit overlay controls */
    box-shadow: 0 8px 24px rgba(27, 42, 74, 0.04) !important;
    display: flex !important;
    align-items: center !important;
    gap: 2rem !important;
    box-sizing: border-box !important;
}
.academic-masthead::before {
    content: "" !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 5px !important;
    background: linear-gradient(90deg, #1b2a4a 0%, #b08850 100%) !important;
}
/* --- Responsive Media Queries for Mobile Screens --- */
@media (max-width: 768px) {
    .academic-masthead {
        height: auto !important;
        min-height: 100px !important;
        padding: 1rem 1.5rem !important;
        flex-direction: row !important;
        gap: 1rem !important;
        align-items: center !important;
    }
    .masthead-logo-container {
        width: 60px !important;
        height: 60px !important;
    }
    .masthead-logo-container img {
        width: 50px !important;
        height: 50px !important;
    }
    .masthead-title {
        font-size: 1.2rem !important;
    }
    .masthead-subtitle {
        font-size: 0.7rem !important;
        margin: 0.1rem 0 0.4rem 0 !important;
    }
    .masthead-badge-row {
        gap: 0.4rem !important;
    }
    .masthead-badge, .masthead-badge-secondary {
        font-size: 0.65rem !important;
        padding: 0.2rem 0.5rem !important;
    }
    .main .block-container {
        padding-top: 140px !important;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 110px !important;
    }
}
.masthead-logo-container {
    background: #ffffff !important;
    border: 1px solid #e8e4dc !important;
    padding: 6px !important;
    border-radius: 50% !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 88px !important;
    height: 88px !important;
    flex-shrink: 0 !important;
}
.masthead-logo-container img {
    height: 76px !important;
    width: 76px !important;
    object-fit: contain !important;
    border-radius: 50% !important;
}
.masthead-text-container {
    flex-grow: 1 !important;
}
.masthead-title {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: 1.85rem !important;
    font-weight: 600 !important;
    color: #1b2a4a !important;
    margin: 0 !important;
    line-height: 1.25 !important;
}
.masthead-subtitle {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #7a7368 !important;
    margin: 0.3rem 0 0.7rem 0 !important;
    letter-spacing: 0.02em !important;
    text-transform: uppercase !important;
}
.masthead-badge-row {
    display: flex !important;
    align-items: center !important;
    gap: 0.6rem !important;
    flex-wrap: wrap !important;
}
.masthead-badge {
    background: #f1ede6 !important;
    color: #1b2a4a !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    padding: 0.35rem 0.8rem !important;
    border-radius: 20px !important;
    border: 1px solid #e1dbcf !important;
    letter-spacing: 0.02em !important;
}
.masthead-badge-secondary {
    background: rgba(176, 136, 80, 0.08) !important;
    color: #8f6c38 !important;
    border: 1px solid rgba(176, 136, 80, 0.18) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    padding: 0.35rem 0.8rem !important;
    border-radius: 20px !important;
}

/* --- Streamlit Tab Styling Overrides --- */
button[data-baseweb="tab"] {
    background-color: transparent !important;
    border: none !important;
    color: #7a7368 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 0.75rem 1.5rem !important;
    margin-right: 0.5rem !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border-radius: 8px 8px 0 0 !important;
}
button[data-baseweb="tab"]:hover {
    color: #1b2a4a !important;
    background-color: rgba(27, 42, 74, 0.04) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #1b2a4a !important;
    font-weight: 600 !important;
    background-color: #ffffff !important;
    border-bottom: 2px solid #1b2a4a !important;
    box-shadow: 0 -4px 12px rgba(27, 42, 74, 0.02) !important;
}
div[data-testid="stTabContent"] {
    background-color: #ffffff !important;
    border: 1px solid #e1dbcf !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 2rem !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02) !important;
    margin-bottom: 2rem !important;
}

/* --- Experiment Title Banner --- */
.exp-card {
    border: 1px solid #e1dbcf;
    border-radius: 12px;
    margin-bottom: 2rem;
    background: #ffffff;
    box-shadow: 0 8px 24px rgba(27, 42, 74, 0.03);
    overflow: hidden;
}
.exp-titlebar {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    background: #1b2a4a;
    padding: 1.2rem 2rem;
    border-bottom: 3px solid #b08850;
}
.exp-badge {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem;
    font-weight: 600;
    background: rgba(176, 136, 80, 0.15);
    color: #f7d49e;
    padding: 4px 12px;
    border-radius: 4px;
    white-space: nowrap;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: 1px solid rgba(176, 136, 80, 0.25);
}
.exp-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.35rem;
    font-weight: 600;
    color: #ffffff;
}
.exp-date {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem;
    color: #a4b4cf;
    white-space: nowrap;
}

/* --- Section bodies --- */
.section-body {
    padding: 0.5rem 0;
}
.section-label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #b08850;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::before {
    content: "";
    display: inline-block;
    width: 6px;
    height: 12px;
    background: #1b2a4a;
    border-radius: 2px;
}
.section-text {
    font-size: 0.98rem;
    color: #2d3748;
    line-height: 1.75;
    margin: 0;
}
.section-text b {
    color: #1b2a4a;
    font-weight: 600;
}

/* --- Mock IDE styling --- */
.ide-header {
    background-color: #1e1e24;
    border-radius: 8px 8px 0 0;
    padding: 0.6rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    border: 1px solid #2d2d34;
    border-bottom: none;
    margin-top: 1.2rem;
}
.ide-dots {
    display: flex;
    gap: 0.4rem;
}
.ide-dots .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}
.ide-dots .dot.red { background-color: #ff5f56; }
.ide-dots .dot.yellow { background-color: #ffbd2e; }
.ide-dots .dot.green { background-color: #27c93f; }
.ide-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #a4b4cf;
    margin-left: 0.5rem;
    flex: 1;
}
.ide-actions {
    display: flex;
    gap: 0.4rem;
    margin-left: auto;
}
.ide-run-btn, .ide-clear-btn {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    padding: 0.25rem 0.7rem !important;
    border-radius: 5px !important;
    border: none !important;
    cursor: pointer !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    transition: all 0.15s ease !important;
}
.ide-run-btn {
    background: #27c93f !important;
    color: #0d1117 !important;
}
.ide-run-btn:hover { background: #22b836 !important; }
.ide-clear-btn {
    background: rgba(255,95,86,0.15) !important;
    color: #ff5f56 !important;
    border: 1px solid rgba(255,95,86,0.3) !important;
}
.ide-clear-btn:hover { background: rgba(255,95,86,0.25) !important; }
/* Streamlit button overrides inside .ide-btn-col */
.ide-btn-col .stButton > button {
    background: #27c93f !important;
    color: #0d1117 !important;
    border: none !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    padding: 0.22rem 0.9rem !important;
    border-radius: 5px !important;
    height: 28px !important;
    min-height: unset !important;
    line-height: 1 !important;
    transition: background 0.15s ease !important;
}
.ide-btn-col .stButton > button:hover {
    background: #1fa832 !important;
    color: #ffffff !important;
}
.ide-clr-col .stButton > button {
    background: transparent !important;
    color: #ff5f56 !important;
    border: 1px solid rgba(255,95,86,0.35) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    padding: 0.22rem 0.7rem !important;
    border-radius: 5px !important;
    height: 28px !important;
    min-height: unset !important;
    line-height: 1 !important;
    transition: background 0.15s ease !important;
}
.ide-clr-col .stButton > button:hover {
    background: rgba(255,95,86,0.15) !important;
}
/* Remove gap between header col and buttons */
.ide-header-row {
    background-color: #1e1e24;
    border-radius: 8px 8px 0 0;
    border: 1px solid #2d2d34;
    border-bottom: none;
    padding: 0.5rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-top: 1.4rem;
}
/* Output box directly below code */
.run-output-box {
    border: 1px solid #1c2024;
    border-top: 2px solid #38ef7d;
    border-radius: 0 0 8px 8px;
    background: #0c0f12;
    padding: 0;
    margin-top: 0;
}

/* Style the sibling code block right after .ide-header */
.ide-header + div[data-testid="stCodeBlock"] {
    margin-top: 0 !important;
}
.ide-header + div[data-testid="stCodeBlock"] > div {
    border-radius: 0 0 8px 8px !important;
    border: 1px solid #2d2d34 !important;
    border-top: none !important;
    background-color: #1e1e24 !important;
}

/* --- Mock Terminal styling --- */
.terminal-header {
    background-color: #0c0f12;
    border-radius: 8px 8px 0 0;
    padding: 0.6rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    border: 1px solid #1c2024;
    border-bottom: none;
    margin-top: 1.2rem;
}
.terminal-dots {
    display: flex;
    gap: 0.4rem;
}
.terminal-dots .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}
.terminal-dots .dot.red { background-color: #ff5f56; }
.terminal-dots .dot.yellow { background-color: #ffbd2e; }
.terminal-dots .dot.green { background-color: #27c93f; }
.terminal-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #7f8c9d;
    margin-left: 0.5rem;
}

/* Style the sibling code block right after .terminal-header */
.terminal-header + div[data-testid="stCodeBlock"] {
    margin-top: 0 !important;
}
.terminal-header + div[data-testid="stCodeBlock"] > div {
    border-radius: 0 0 8px 8px !important;
    border: 1px solid #1c2024 !important;
    border-top: none !important;
    background-color: #0c0f12 !important;
}
.terminal-header + div[data-testid="stCodeBlock"] code {
    color: #38ef7d !important; /* Glow green text for terminals */
    font-family: 'JetBrains Mono', monospace !important;
}

/* Center and style matplotlib plots */
[data-testid="stImage"] {
    border: 1px solid #e1dbcf;
    border-radius: 10px;
    box-shadow: 0 8px 24px rgba(27, 42, 74, 0.05);
    background-color: #ffffff;
    padding: 1.2rem;
    margin: 1.5rem auto;
}

/* --- Conclusion Section --- */
.conclusion-section {
    padding: 1.5rem 2rem;
    background: rgba(176, 136, 80, 0.05);
    border-left: 5px solid #b08850;
    border-top: 1px solid rgba(176, 136, 80, 0.15);
    border-bottom: 1px solid rgba(176, 136, 80, 0.15);
    border-right: 1px solid rgba(176, 136, 80, 0.15);
    margin-top: 2.5rem;
    border-radius: 0 8px 8px 0;
}
.conclusion-text {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1rem;
    color: #4a371c;
    line-height: 1.7;
    margin: 0;
}

/* --- Page Footer (Fixed at Bottom) --- */
.academic-footer {
    position: fixed !important;
    left: 0 !important;
    bottom: 0 !important;
    width: 100% !important;
    background-color: #ffffff !important;
    border-top: 1px solid #e1dbcf !important;
    padding: 0.8rem 1.5rem !important;
    text-align: center !important;
    color: #5c6370 !important;
    font-size: 0.82rem !important;
    z-index: 9999998 !important; /* Just below header's z-index but above content */
    box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.04) !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 1rem !important;
    flex-wrap: wrap !important;
    box-sizing: border-box !important;
}
.academic-footer strong {
    color: #1b2a4a !important;
}
.academic-footer span.bullet {
    color: #b08850 !important;
    font-weight: bold !important;
}

/* Sidebar Toggle Logic */
.sidebar-hidden [data-testid="stSidebar"] {
    display: none !important;
}
.sidebar-hidden [data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# 4. Inject sidebar-hidden class on body via JS + toggle state
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

_sidebar_js = ""
if not st.session_state.sidebar_open:
    _sidebar_js = """
    <script>
        (function() {
            function applySidebarHide() {
                document.body.classList.add('sidebar-hidden');
            }
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', applySidebarHide);
            } else {
                applySidebarHide();
            }
            const obs = new MutationObserver(applySidebarHide);
            obs.observe(document.body, { childList: true, subtree: false });
        })();
    </script>
    """

st.markdown(f"""
{_sidebar_js}
<div class="academic-masthead">
    <div class="masthead-logo-container">
        <img src="{logo_src}" alt="GEC Logo">
    </div>
    <div class="masthead-text-container">
        <h1 class="masthead-title">Goa College of Engineering</h1>
        <div class="masthead-subtitle">"Bhausaheb Bandodkar Technical Education Complex" &nbsp;&middot;&nbsp; Farmagudi &ndash; 403 401, Goa</div>
        <div class="masthead-badge-row">
            <span class="masthead-badge">CMP-226: Graph Theory &amp; Combinatorics Lab</span>
            <span class="masthead-badge-secondary">Academic Notebook</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar toggle button - floating in main area, always visible
# Must come BEFORE sidebar widget rendering so session state is set
if st.session_state.sidebar_open:
    _toggle_icon_svg = '<line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>'
    _toggle_title = "Collapse Sidebar"
else:
    _toggle_icon_svg = '<polyline points="9 18 15 12 9 6"/>'
    _toggle_title = "Expand Sidebar"

if not st.session_state.sidebar_open:
    _hide_sidebar_css = """
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    section[data-testid="stMain"] { margin-left: 0 !important; }
    .main .block-container { max-width: 1200px !important; }
    </style>
    """
    st.markdown(_hide_sidebar_css, unsafe_allow_html=True)

# Render sidebar content only when sidebar is open
if st.session_state.sidebar_open:
    st.sidebar.markdown("### 🗂️ Lab Notebook Journals")

# 5. Dataset Definition
EXPERIMENTS = [
    {
        "key": "Expt_01", "num": 1, "date": "29/01/2026",
        "name": "Basic Graphs",
        "aim": "To implement basic graphs such as Complete Graph, Cycle Graph, Path Graph and Complete Bipartite Graph.",
        "theory": "A Graph G is formally defined as an ordered pair $G=(V,E)$, consisting of a set V of vertices (or nodes) and a set E of edges, which represent the connections between pairs of vertices. This experiment explores four distinct graph topologies implemented using the NetworkX library.<br><br><b>The Complete Graph ($K_n$)</b> is a simple undirected structure where every possible pair of distinct vertices is connected by a unique edge. In the Code: The K_5 graph is initialized with nodes {1, 2, 3, 4, 5}. Structure: Its structural density is maximized, resulting in a total of {n(n-1)/2} edges. For 5 nodes, this equals 10 connections. Visual: In the output, this appears as a star-pentagon shape where every node connects to every other node.<br><br><b>The Cycle Graph ($C_n$)</b> represents a sparse and symmetric topology where vertices are linked in a closed chain. In the Code: The C_5 graph connects nodes in a continuous loop: (1->2->3->4->5->1). Structure: Every single vertex maintains a degree of exactly two.<br><br><b>Path Graph ($P_n$)</b> is similar to the cycle but lacking the closing connection. In the Code: The P_5 structure follows a linear sequence (1->2->3->4->5). Structure: Internal nodes (2, 3, 4) have a degree of two, while the two end nodes (1 and 5) have a degree of only one because they do not 'loop' back to complete a circuit.<br><br><b>Complete Bipartite Graph ($K_{m,n}$)</b>: The Bipartite Graph is characterized by the division of vertices into two disjoint and independent sets, U and V. In the Code: The $K_{2,3}$ graph partitions nodes into set U={1,2} and set V={3,4,5}. The code defines edges such that nodes 1 and 2 connect to 3, 4, and 5. Structure: The defining property is that every edge connects a vertex from U to one in V. No edges exist between vertices within the same set (e.g., 1 is not connected to 2). Manual Layout: The code uses a custom pos dictionary to strictly define the (x, y) coordinates of each node. This forces the visual representation into two distinct rows to clearly emphasize the bipartite separation, rather than letting the library position them randomly.",
        "conclusion": "Basic graphs were successfully implemented using networkx and matplotlib.",
    },
    {
        "key": "Expt_02", "num": 2, "date": "05/02/2026",
        "name": "Graph Isomorphism Verification",
        "aim": "To implement graph isomorphism verification inorder to compare structural equivalence of the 2 graphs.",
        "theory": "<b>Definition of Graph Isomorphism:</b>- The structural equivalence of two graphs is formally defined by the mathematical concept of graph isomorphism. Two graphs G and H are said to be isomorphic (written as $G \\cong H$) if they clearly have the same structure and differ only in the names or labels assigned to their vertices and edges.<br><br><b>For simple graphs:</b> Isomorphism requires presenting a bijection $f:V(G) \\rightarrow V(H)$ such that vertices u and v are adjacent in G ($uv \\in E(G)$) if and only if their mapped counterparts f(u) and f(v) are adjacent in H ($f(u)f(v) \\in E(H)$).<br><br><b>For general graphs:</b> Because general graphs can contain multiple edges or loops, the definition requires a pair of bijections: $\\theta:V(G) \\rightarrow V(H)$ mapping the vertices and $\\phi:E(G) \\rightarrow E(H)$ mapping the edges. These must operate such that an edge e joins vertices u and v in G if and only if the mapped edge \\phi(e) joins \\theta(u) and \\theta(v) in H.<br><br><b>Verifying Structural Equivalence:</b> The structural properties of a graph are determined entirely by its adjacency relation, meaning all such properties are perfectly preserved by an isomorphism. When implementing verification algorithms (where graphs are commonly stored and represented in computers using adjacency matrices), the logic relies on the following principles:<br>1. <i>Disproving Isomorphism:</i> To prove that two graphs are not structurally equivalent, one must find a specific structural property in which they differ. If two graphs have a different number of vertices, a different number of edges, or differ in other structural invariants like their subgraphs or complements, they cannot be isomorphic.<br>2. <i>Proving Isomorphism:</i> Merely checking that a few structural properties are identical does not guarantee that $G \\cong H$. To definitively verify structural equivalence, the algorithm must explicitly find and present a bijection that preserves the adjacency relation.<br><br><b>Isomorphism Classes:</b> The isomorphism relation is reflexive, symmetric, and transitive, making it an equivalence relation. This relation partitions the set of all graphs into isomorphism classes, where any two graphs in the exact same class are pairwise isomorphic. As a result, an unlabelled graph can be thought of as a representative of its corresponding equivalence class of structurally identical graphs.",
        "conclusion": "verification of graph isomorphism were successfully implemented.",
    },
    {
        "key": "Expt_03", "num": 3, "date": "05/02/2026",
        "name": "Generation of Various Subgraphs",
        "aim": "To implement generation of various subgraphs such induced subgraphs, spanning subgraphs and edge deleted subgraphs",
        "theory": "<b>Subgraph:</b> A graph H is a subgraph of G if the vertex set of H is a subset of the vertex set of G, the edge set of H is a subset of the edge set of G, and the endpoints of edges in H are the same as in G. If H is a subgraph of G but is not equal to G, it is called a proper subgraph.<br><br><b>Spanning Subgraph:</b> A spanning subgraph is a subgraph that includes every vertex of the original graph. Even if edges are removed, the total number of vertices remains identical to the original graph.<br><br><b>Induced Subgraph:</b> An induced subgraph is formed by taking a subset of vertices from the original graph and including every edge that connects those specific vertices in the original graph. This is often referred to as a vertex-induced subgraph.<br><br><b>Edge-Induced Subgraph:</b> Edge-induced subgraph is formed by taking a subset of edges from the original graph. The vertex set of this subgraph consists of only the vertices that are endpoints of the chosen edges.<br><br><b>Graph Operations:</b> Vertex deletion involves removing a vertex and all edges connected to it. Edge deletion involves removing a specific edge while keeping all original vertices in the graph, which creates a spanning subgraph.",
        "conclusion": "subgraphs such induced subgraphs, spanning subgraphs and edge deleted subgraphs were successfully plotted using original graph.",
    },
    {
        "key": "Expt_04", "num": 4, "date": "05/02/2026",
        "name": "Degree Sequence & Havel-Hakimi Algorithm",
        "aim": "To check if the given degree sequence is graphical or not graphical using Handshaking Lemma and Havel-Hakimi Theorem.",
        "theory": "<b>Degree Of A Vertex:</b> The degree of a vertex is the number of edges connected to it. According to the Handshaking Lemma, the sum of all vertex degrees in a graph is equal to twice the number of edges. This implies that the sum of degrees must always be an even number, and the number of vertices with an odd degree must also be even.<br><br><b>Degree Sequences:</b> A degree sequence is a list of the degrees of all vertices in a graph, typically written in non-increasing order. While any graph has a degree sequence, not every sequence of integers can form a simple graph (a graph without loops or multiple edges).<br><br><b>Graphical Sequences:</b> A sequence is called graphical if there exists a simple graph that corresponds to that specific degree sequence. To determine if a sequence is graphical, it must satisfy parity requirements and specific structural constraints.<br><br><b>The Havel-Hakimi Algorithm:</b> The Havel-Hakimi algorithm is a recursive method used to determine if a degree sequence is graphical. The process involves:<br>1. Removing the largest degree from the sequence.<br>2. Subtracting 1 from the next largest degrees in the remaining sequence.<br>3. Sorting the new sequence and repeating the process.<br>If the process results in a sequence of all zeros, the original sequence is graphical. If it results in negative numbers, the sequence is not graphical.",
        "conclusion": "The given sequence is not graphical and it is verified using Handshaking Lemma and Havel-Hakimi Theorem.",
    },
    {
        "key": "Expt_05", "num": 5, "date": "12/03/2026",
        "name": "Line Graph Conversion",
        "aim": "To implement conversion of a given graph into line graph where each vertex represents an edge of the original graph, and adjacency reflects shared endpoints",
        "theory": "<b>Definition of a Line Graph:</b> The computational logic executes the formal mathematical definition of a line graph L(G), which is frequently referred to as an 'edge graph,' adjoint, conjugate, or derivative graph. The transformation obeys two core principles:<br>1. <i>Vertex Correspondence:</i> The vertex set of L(G) is precisely the edge set of the original graph G, meaning every edge in G maps to exactly one distinct vertex in L(G).<br>2. <i>Adjacency Rule:</i> Two vertices in the line graph L(G) are joined by an edge if and only if their corresponding parent edges in G are adjacent (i.e., they share a common incident vertex).<br><br><b>Objective:</b> To analyze the structural properties of a line graph L(G) and perform its construction from an initial graph G, comparing manual algorithmic steps with built-in library functions.<br><br><b>Theoretical Background:</b> A line graph L(G) directly models the incidence relationships between the edges of a graph G.<br>- <i>Vertex Mapping:</i> Every individual edge within the original graph G transitions into a discrete node in the line graph L(G).<br>- <i>Adjacency Condition:</i> An edge exists between two nodes in L(G) strictly when their parent edges in G intersect at the same vertex.<br><br><b>Implementation Methods:</b> The computational approach leverages the NetworkX and NumPy libraries for matrix manipulation and the handling of complex graph data structures.<br>- <i>Method A: Manual Construction:</i> This approach follows a specific sequence of logic to mirror the mathematical definition: Edge Extraction (Iterate through the adjacency matrix to identify all existing edges), Node Mapping (Create a new graph where each identified edge is added as a node), and Connectivity Check (Compare every pair of edges. If they share a common vertex index, an edge is added between them in the new graph).<br>- <i>Method B: Library-Based Construction:</i> Using nx.line_graph(G), the software internally maps the edge-to-vertex transitions, providing a benchmark for the manual method.<br><br><b>Mathematical Observations:</b> Based on the code's output, several properties can be verified: Vertex Count (The number of vertices in L(G) is equal to the number of edges in G). Visualization: Using a spring layout, the line graph typically appears more dense than the original graph because high-degree nodes in G create cliques (complete subgraphs) in L(G).",
        "conclusion": "construction of line graph using network function and manually were successfully implemented.",
    },
    {
        "key": "Expt_06", "num": 6, "date": "09/04/2026",
        "name": "Minimum Spanning Tree — Kruskal's Algorithm",
        "aim": "To implement Kruskal's algorithm to generate MST, ensuring all vertices are connected with minimum possible total edge weight and without cycles.",
        "theory": "A Minimum Spanning Tree (MST) of a connected, undirected, weighted graph is a tree that connects all the vertices of the graph with the minimum possible total edge weight and without forming any cycles. A spanning tree of a graph with n vertices always contains $n-1$ edges.<br><br><b>Kruskal's Algorithm</b> is a greedy algorithm used to find the MST of a graph. It works by selecting edges in increasing order of their weights and adding them to the spanning tree, ensuring that no cycle is formed.<br><br><b>Algorithm:</b><br>Step 1: Choose a link $e_1$ such that $w(e_1)$ is as small as possible.<br>Step 2: If edges $e_1, e_2, ..., e_i$ have been chosen, then choose an edge $e_{i+1}$ from $E \\setminus \\{e_1, e_2, ..., e_i\\}$ in such a way that:<br>&nbsp;&nbsp;&nbsp;&nbsp;(i) $G[\\{e_1, e_2, ..., e_{i+1}\\}]$ is acyclic;<br>&nbsp;&nbsp;&nbsp;&nbsp;(ii) $w(e_{i+1})$ is as small as possible subject to (i).<br>Step 3: Stop when step 2 cannot be implemented further.<br><br>Kruskal's algorithm always picks the edge with the least weight and gradually builds the MST by connecting different components. It uses the concept of disjoint sets (Union-Find) to detect cycles efficiently. Initially, each vertex is treated as a separate set, and edges are added only if they connect two different sets.",
        "conclusion": "Implement Kruskal's algorithm to generate MST, ensuring all vertices are connected with minimum possible total edge weight and without cycles.",
    },
    {
        "key": "Expt_07", "num": 7, "date": "09/04/2026",
        "name": "Shortest Path — Dijkstra's Algorithm",
        "aim": "To implement shortest path algorithm in order to compute the shortest path from the source vertex to all the other vertices in a weighted graph",
        "theory": "<b>The Shortest Path Problem:</b> In many real-world applications, such as transportation or communication networks, graphs have a real number w(e) associated with each edge e, which is called its weight. A graph with these assigned weights is known as a weighted graph, and the weights often represent non-negative quantities like physical distance, cost, or time. The shortest path problem involves finding a route between a starting source vertex and a destination vertex such that the total sum of the weights of the edges on that path is minimized.<br><br><b>Theoretical Background: Dijkstra's Algorithm:</b> To solve the problem of finding the shortest paths from a single source node to all other vertices in a weighted graph, we can implement an algorithm discovered independently by E. W. Dijkstra in 1959 and by P. D. Whiting and J. A. Hillier in 1960. Dijkstra's algorithm is a greedy algorithm that systematically finds optimal routes to other vertices in order of their increasing distance from the source. The algorithm can be visualized as a 'tree-growing' procedure because, at each stage, the edges that form the confirmed shortest paths make up a connected, acyclic graph, which is known as a tree. The algorithm operates by maintaining a set S of vertices to which the exact shortest paths and distances from the source are already known and finalized.<br><br><b>The Steps of the Algorithm:</b> Let the source vertex be u, and let t(z) represent the tentative shortest distance from u to any other vertex z. The algorithm proceeds through the following logical sequence:<br>1. <i>Initialize:</i> Begin by setting the set of visited vertices to include only the source, S={u}. Set the exact distance for the source to zero (t(u)=0). For all other vertices z, set the initial tentative distance t(z) to the weight of the edge w(uz) if they are directly adjacent to u, or to infinity ($\\infty$) if they are not.<br>2. <i>Visit and Select:</i> From the remaining unvisited vertices (those outside of S), select the vertex v that has the smallest tentative distance t(v). Add this newly selected vertex v to the confirmed set S.<br>3. <i>Update:</i> Explore the unvisited neighbors of the current vertex v. For each neighbor z that is not yet in S, update its tentative distance by checking if routing the path through v is shorter than the previously recorded distance. Mathematically, the new distance label becomes $\\min\\{t(z), t(v) + w(vz)\\}$.<br>4. <i>Repeat/Terminate:</i> Mark v as visited and repeat the selection and update phases. The algorithm terminates when all vertices have been added to the confirmed set ($S=V(G)$), or until the tentative distance t(z) for all remaining unvisited vertices is infinity, which indicates they are unreachable from the source.<br><br><b>Requirement:</b> A strict requirement for Dijkstra's algorithm to yield correct optimal paths is that all edge weights must be non-negative. The algorithm relies on the greedy assumption that once a vertex is added to the confirmed set S, its shortest distance is permanently finalized. If negative edge weights were present, this foundational assumption could fail, as a subsequent path containing a negative weight might theoretically reduce the total distance to a finalized vertex even further.",
        "conclusion": "shortest path was successfully found using Djikstra's algorithm with networkx function and manually.",
    },
    {
        "key": "Expt_08", "num": 8, "date": "09/04/2026",
        "name": "Generation of Closed Walks, Trails and Paths",
        "aim": "To implement the generation of closed walks, trails and path in a connected graph",
        "theory": "A <b>walk</b> in G is defined as a finite alternating sequence of vertices and edges of the form $W = v_0, e_1, v_1, e_2, v_2, ..., e_k, v_k$, where each edge $e_i = (v_{i-1}, v_i) \\in E$ for $i = 1, 2, ..., k$. The integer k is called the length of the walk, which represents the number of edges in the sequence. In a walk, both vertices and edges may be repeated any number of times. Walks are the most general type of traversal in a graph. A walk is said to be closed if the initial vertex and the final vertex are the same, that is, $v_0 = v_k$. If $v_0 \\neq v_k$, then the walk is called an open walk.<br><br>A <b>trail</b> is a walk in which all edges are distinct, that is, $e_i \\neq e_j$ for all $i \\neq j$. However, vertices may still repeat in a trail. Thus, a trail restricts the repetition of edges but allows repetition of vertices. The length of a trail is also defined as the number of edges in it. A trail is said to be closed if $v_0 = v_k$, and such a closed trail is sometimes referred to as a circuit. If $v_0 \\neq v_k$ then the trail is called an open trail.<br><br>A <b>path</b> is a walk in which all vertices are distinct, that is, $v_i \\neq v_j$ for all $i \\neq j$. As a result, no edge can be repeated in a path. A path represents the simplest form of movement in a graph without revisiting any vertex. A path is said to be open if $v_0 \\neq v_k$. A closed path is one in which $v_0 = v_k$ and no other vertices are repeated. Such a closed path is called a cycle. The number of edges in a path is called its length.<br><br>Every path is a trail and every trail is a walk, but the converse is not necessarily true.",
        "conclusion": "Implemented the generation of closed walks, trails and path in a connected graph.",
    },
    {
        "key": "Expt_09", "num": 9, "date": "16/04/2026",
        "name": "Eulerian Circuit Detection",
        "aim": "To implement Algorithm that check existence on a Eulerian circuit and constructs a circuit that transverses every edge of the graph exactly once",
        "theory": "Let $G=(V,E)$ be a finite, connected, undirected graph, where V is the set of vertices and E is the set of edges. An Eulerian circuit in G is defined as a closed trail represented by the sequence: $v_0, e_1, v_1, e_2, v_2, ..., e_m, v_m$ such that the following conditions are satisfied:<br>1. $v_0=v_m$ which means the circuit starts and ends at the same vertex, forming a closed loop.<br>2. For each $i=1,2,...,m$, the edge $e_i$ connects the vertices $v_{i-1}$ and $v_i$, ensuring that consecutive vertices in the sequence are adjacent.<br>3. $e_i \\neq e_j$ for all $i \\neq j$, which ensures that no edge is repeated in the traversal.<br>4. $\\{e_1, e_2, ..., e_m\\} = E$, which means every edge of the graph is included exactly once in the circuit.<br><br>If the number of edges in the graph is m, then the Eulerian circuit contains exactly m edges and $m+1$ vertices in the sequence $v_0, v_1, v_2, ..., v_m$.<br><br><b>Euler's Theorem:</b> A connected graph G has an Eulerian circuit if and only if $deg(v) \\equiv 0 \\pmod 2$ for all $v \\in V$, that is, every vertex of the graph has an even degree. The reason for this condition is that whenever a vertex is entered during traversal, it must also be exited, so edges are used in pairs at each vertex, resulting in an even degree. If any vertex has an odd degree, then an Eulerian circuit does not exist. However, if exactly two vertices have an odd degree, then the graph contains an Eulerian path but not an Eulerian circuit.<br><br><b>Fleury's Algorithm:</b><br>Step 1: Choose an arbitrary vertex $v_0 \\in V$ and set $w_0=v_0$.<br>Step 2: Suppose that a trail $w_0, e_1, w_1, e_2, w_2, ..., e_i, w_i$ has been constructed, where $w_i$ is the current vertex.<br>Step 3: From the set of edges incident on $w_i$, select an edge $e_{i+1}$ such that: $e_{i+1}$ is not a bridge in the remaining graph, or $e_{i+1}$ is the only edge incident on $w_i$.<br>Step 4: Let $w_{i+1}$ be the vertex adjacent to $w_i$ via the edge $e_{i+1}$.<br>Step 5: Extend the trail by adding $e_{i+1}$ and $w_{i+1}$, and remove the edge $e_{i+1}$ from the graph.<br>Step 6: Repeat Steps 2 to 5 until all edges of the graph are removed.<br>Step 7: The resulting sequence forms an Eulerian circuit, where $w_0=w_m$ and every edge is traversed exactly once.",
        "conclusion": "Implement Algorithm that check existence on a Eulerian circuit and constructs a circuit that transverses every edge of the graph exactly once",
    },
    {
        "key": "Expt_10", "num": 10, "date": "23/04/2026",
        "name": "Hamiltonian Circuit Detection",
        "aim": "To implement a method that determines whether a graph contains a Hamiltonian Circuit that is a cycle that visits every vertex exactly once except the starting vertex.",
        "theory": "Let $G=(V,E)$ be a finite, connected, undirected graph, where V is the set of vertices and E is the set of edges. A Hamiltonian circuit in G is defined as a closed cycle represented by the sequence: $v_0, v_1, v_2, ..., v_{n-1}, v_n$ such that the following conditions are satisfied:<br>1. $v_0=v_n$, which means the circuit starts and ends at the same vertex, forming a closed loop.<br>2. For each $i=1,2,...,n$, the vertices $v_{i-1}$ and $v_i$ are adjacent, meaning there exists an edge joining consecutive vertices in the sequence.<br>3. $v_i \\neq v_j$ for all $0 \\le i < j < n$ which ensures that no vertex is repeated except the starting and ending vertex.<br>4. $\\{v_0, v_1, v_2, ..., v_{n-1}\\} = V$ which means every vertex of the graph is included exactly once in the circuit.<br><br>If the graph contains n vertices, then the Hamiltonian circuit contains exactly n edges and $n+1$ vertices in the sequence. A graph G is said to be Hamiltonian if it contains a Hamiltonian circuit.<br><br>The main objective of a Hamiltonian circuit is to traverse every vertex of the graph exactly once and finally return to the starting vertex. Unlike Eulerian circuits, which focus on visiting every edge exactly once, Hamiltonian circuits are concerned with visiting every vertex exactly once. In a Hamiltonian circuit, revisiting vertices is not allowed because the purpose is to complete a cycle that passes through all vertices without repetition. The only repeated vertex is the starting vertex, which appears again at the end to complete the circuit.<br><br><b>Applications:</b> Hamiltonian circuits are widely used in practical applications such as routing problems, scheduling, computer networks, DNA sequencing, and optimization problems. One of the most famous applications is the Travelling Salesman Problem (TSP), where a salesman must visit each city exactly once and return to the starting city while minimizing the total distance travelled.<br><br>A Hamiltonian path is a path that visits every vertex exactly once but does not return to the starting vertex. If such a path forms a closed loop by connecting the last vertex back to the first vertex, then it becomes a Hamiltonian circuit. The existence of a Hamiltonian circuit depends mainly on the arrangement and connectivity of vertices in the graph. Dense graphs with many connections are generally more likely to contain Hamiltonian circuits than sparse graphs.",
        "conclusion": "Implemented a method that determines whether a graph contains a Hamiltonian Circuit that is a cycle that visits every vertex exactly once except the starting vertex.",
    },
    {
        "key": "Expt_11", "num": 11, "date": "14/05/2026",
        "name": "Greedy Graph Coloring",
        "aim": "To implement graph coloring algorithm that assign colour to the vertices such that no two adjacent vertices share the same color with minimum chromatic number.",
        "theory": "<b>Graph coloring</b> is a method of assigning colors to the vertices of a graph such that no two adjacent vertices have the same color. Let a graph be represented as: $G=(V,E)$ where: $V =$ set of vertices, $E =$ set of edges. A vertex coloring of a graph is a function: $C: V \\rightarrow \\{1,2,3,...,k\\}$ such that: $C(u) \\neq C(v)$ for every edge $(u,v) \\in E$. This means that if two vertices are connected by an edge, then they must be assigned different colors.<br><br>The minimum number of colors required to color a graph is called the <b>Chromatic Number</b> of the graph and is denoted by: $\\chi(G)$. Hence, $\\chi(G) = \\min \\{ k: G \\text{ can be colored using } k \\text{ colors} \\}$.<br><br><b>Greedy Graph Coloring Algorithm:</b><br>The Greedy Coloring Algorithm assigns colors to vertices one by one following a specific order. For each vertex, the algorithm assigns the smallest available color that has not been used by its adjacent vertices. In this method:<br>1. The vertex having the highest saturation degree is selected first.<br>2. Saturation degree is the number of different colors used by adjacent vertices.<br>3. If saturation degrees are equal, the vertex with the highest ordinary degree is selected.<br><br><b>Algorithm Steps:</b><br>Step 1: Start with all vertices uncolored.<br>Step 2: Select a vertex.<br>Step 3: Assign the smallest possible color that is not used by any adjacent vertex.<br>Step 4: Update the saturation degree of neighboring vertices.<br>Step 5: Repeat Steps 2 to 4 until all vertices are colored.<br>Step 6: Count the total number of colors used.<br><br>For every edge: $(u,v) \\in E$, the coloring condition must satisfy: $C(u) \\neq C(v)$. If the graph is colored using minimum colors, then: $\\chi(G) =$ Minimum number of colors used.",
        "conclusion": "Implement graph coloring algorithm that assign colour to the vertices such that no two adjacent vertices share the same color with minimum chromatic number.",
    }
]

# 6. Navigation Sidebar
_exp_names = [f"Experiment {e['num']:02d}: {e['name']}" for e in EXPERIMENTS]
if st.session_state.sidebar_open:
    _selected_exp_name = st.sidebar.radio("Navigate Experiments:", _exp_names)
else:
    # Keep last selected or default to first when sidebar is closed
    if "current_exp" not in st.session_state:
        st.session_state.current_exp = _exp_names[0]
    _selected_exp_name = st.session_state.current_exp

# Always render the floating toggle button
st.markdown(f"""
<style>
.sidebar-fab {{
    position: fixed !important;
    top: 160px !important;
    left: {'260px' if st.session_state.sidebar_open else '12px'} !important;
    z-index: 9999990 !important;
    background: #ffffff !important;
    border: 1.5px solid #e1dbcf !important;
    border-radius: 50% !important;
    width: 38px !important;
    height: 38px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 2px 10px rgba(27,42,74,0.10) !important;
    cursor: pointer !important;
    transition: left 0.3s ease, box-shadow 0.2s ease !important;
}}
.sidebar-fab:hover {{
    box-shadow: 0 4px 18px rgba(27,42,74,0.18) !important;
    background: #f7f3ed !important;
}}
.sidebar-fab svg {{
    stroke: #1b2a4a;
    stroke-width: 2;
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
    width: 18px;
    height: 18px;
}}
</style>
""", unsafe_allow_html=True)

with st.form(key="_sidebar_fab_form", clear_on_submit=True, border=False):
    col_fab, col_rest = st.columns([0.06, 0.94])
    with col_fab:
        _fab_clicked = st.form_submit_button(
            "☰" if st.session_state.sidebar_open else "▶",
            help="Toggle Sidebar",
            use_container_width=True,
        )
    if _fab_clicked:
        if st.session_state.sidebar_open:
            st.session_state.current_exp = _selected_exp_name
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()

# Initialize runs database in session state
if "runs" not in st.session_state:
    st.session_state.runs = {}

selected_idx = _exp_names.index(_selected_exp_name)
meta = EXPERIMENTS[selected_idx]

# 7. Subprocess Engine Setup
PATCH_HEADER = """\
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as _plt_module
import os as _os_p
import builtins

_SAVE_DIR = __SAVE_DIR_PLACEHOLDER__
_fig_counter = [0]

def _patched_show(*a, **kw):
    figs = list(_plt_module.get_fignums())
    if not figs:
        return
    for fnum in figs:
        fig = _plt_module.figure(fnum)
        out = _os_p.path.join(_SAVE_DIR, f'fig_{_fig_counter[0]}.png')
        fig.savefig(out, bbox_inches='tight', dpi=130)
        _fig_counter[0] += 1
    _plt_module.close('all')

def _patched_savefig(fname, *a, **kw):
    out = _os_p.path.join(_SAVE_DIR, f'fig_{_fig_counter[0]}.png')
    kw.setdefault('bbox_inches', 'tight')
    kw.setdefault('dpi', 130)
    _plt_module.gcf().savefig(out, *a, **kw)
    _fig_counter[0] += 1
    _plt_module.close('all')

import matplotlib.pyplot as plt
plt.show = _patched_show
plt.savefig = _patched_savefig

def _patched_input(prompt=""):
    print(prompt)
    return ""

builtins.input = _patched_input
"""

def run_script(path):
    script_dir = os.path.dirname(os.path.abspath(path))
    script_name = os.path.splitext(os.path.basename(path))[0]
    tmp_dir = tempfile.mkdtemp()
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            original = f.read()

        # Use safe replacement instead of .format() to avoid KeyErrors
        # from f-string expressions like {d[node]} inside user scripts
        patched_source = PATCH_HEADER.replace(
            "__SAVE_DIR_PLACEHOLDER__", repr(tmp_dir)
        ) + original
        patched_path = os.path.join(tmp_dir, "_patched.py")
        with open(patched_path, "w", encoding="utf-8") as f:
            f.write(patched_source)

        env = os.environ.copy()
        env["MPLBACKEND"] = "Agg"
        env["PYTHONIOENCODING"] = "utf-8"   # Fix UnicodeEncodeError for → etc.
        env["PYTHONUTF8"] = "1"             # Python 3.7+ UTF-8 mode

        result = subprocess.run(
            [sys.executable, "-X", "utf8", patched_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=script_dir,
            env=env,
            timeout=60,
        )

        images = sorted(glob.glob(os.path.join(tmp_dir, "fig_*.png")))
        img_data = []
        for img_path in images:
            dest = os.path.join(script_dir, f"_cached_{script_name}_{os.path.basename(img_path)}")
            shutil.copy2(img_path, dest)
            img_data.append(dest)

        return result.stdout.strip(), result.stderr.strip(), img_data
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

exp_dir = os.path.join(BASE_DIR, meta["key"])
num = meta["num"]
cache_key = f"ran_{meta['key']}"

# 9. Main Card Title Layout
st.markdown(f"""
<div class="exp-card">
    <div class="exp-titlebar">
        <span class="exp-badge">Experiment {num:02d}</span>
        <span class="exp-title">{meta['name']}</span>
        <span class="exp-date">&#128197; {meta['date']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 10. Implementation Layout Tabs
tab_aim, tab_theory, tab_code = st.tabs([
    "🎯 Aim", 
    "📖 Theory", 
    "💻 Source Code & Sandbox"
])

with tab_aim:
    st.markdown(f"""
    <div class="section-body">
        <div class="section-label">Aim Statement</div>
        <p class="section-text">{meta['aim']}</p>
    </div>
    """, unsafe_allow_html=True)

with tab_theory:
    st.markdown(f"""
    <div class="section-body">
        <div class="section-label">Theoretical Analysis</div>
        <p class="section-text">{meta['theory']}</p>
    </div>
    """, unsafe_allow_html=True)

with tab_code:
    st.markdown("<div style='padding: 0.5rem 0;'>", unsafe_allow_html=True)
    if os.path.isdir(exp_dir):
        py_files = sorted(glob.glob(os.path.join(exp_dir, "*.py")))
        if not py_files:
            st.info("No interactive code scripts found in this project folder module.")

        for path in py_files:
            fname = os.path.basename(path)
            script_cache_key = f"{meta['key']}_{fname}"

            # ── Read source ──────────────────────────────────────────────────
            try:
                with open(path, "r", encoding="utf-8") as f:
                    code_content = f.read()
            except Exception as e:
                st.error(str(e))
                continue

            # ── IDE Header row: dots + filename | ▶ Run | 🗑 Clear ────────────
            # Use HTML for the left side (dots + filename), Streamlit buttons on the right
            st.markdown(f"""
            <div class="ide-header" style="margin-top:1.4rem; display:flex; align-items:center; gap:0.8rem;">
                <div class="ide-dots">
                    <span class="dot red"></span>
                    <span class="dot yellow"></span>
                    <span class="dot green"></span>
                </div>
                <div class="ide-title">📁 {fname}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Code block (zero-gap below header) ───────────────────────────
            st.code(code_content, language="python")

            # ── Inline Run / Clear buttons right below code ───────────────────
            btn_col_run, btn_col_clear, btn_col_space = st.columns([1.4, 1.2, 5.4])
            with btn_col_run:
                run_btn = st.button(
                    f"▶ Run {fname}",
                    key=f"run_btn_{script_cache_key}",
                    use_container_width=True,
                    type="primary",
                )
            with btn_col_clear:
                clear_btn = st.button(
                    f"✕ Clear",
                    key=f"clear_btn_{script_cache_key}",
                    use_container_width=True,
                )

            if clear_btn:
                if script_cache_key in st.session_state.runs:
                    del st.session_state.runs[script_cache_key]
                    st.rerun()

            if run_btn:
                with st.spinner(f"⚙️ Running {fname}…"):
                    try:
                        stdout, stderr, imgs = run_script(path)
                    except Exception as e:
                        stdout, stderr, imgs = "", str(e), []
                    st.session_state.runs[script_cache_key] = {
                        "stdout": stdout,
                        "stderr": stderr,
                        "imgs": imgs,
                    }

            # ── Output: terminal + plots directly below, no extra header ──────
            if script_cache_key in st.session_state.runs:
                run_data = st.session_state.runs[script_cache_key]

                # Terminal output — show stdout and stderr together
                stdout_txt = run_data.get("stdout", "").strip()
                stderr_txt = run_data.get("stderr", "").strip()
                if stdout_txt or stderr_txt:
                    st.markdown(f"""
                    <div class="terminal-header" style="margin-top:0.6rem;">
                        <div class="terminal-dots">
                            <span class="dot red"></span>
                            <span class="dot yellow"></span>
                            <span class="dot green"></span>
                        </div>
                        <div class="terminal-title">💻 output — {fname}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    combined = ""
                    if stdout_txt:
                        combined += stdout_txt
                    if stderr_txt:
                        if combined:
                            combined += "\n\n--- stderr ---\n"
                        combined += stderr_txt
                    st.code(combined, language="")

                # Matplotlib plots
                if run_data["imgs"]:
                    for img_path in run_data["imgs"]:
                        if os.path.exists(img_path):
                            col_l, col_c, col_r = st.columns([1, 6, 1])
                            with col_c:
                                st.image(img_path, use_container_width=True)
                                st.markdown(
                                    f"<div style='text-align:center;font-size:0.82rem;"
                                    f"color:#7a7368;margin-top:-0.4rem;margin-bottom:1rem;"
                                    f"font-style:italic;'>Figure: output from {fname}</div>",
                                    unsafe_allow_html=True,
                                )

            st.markdown("<hr style='border-top:1px dashed #e1dbcf;margin:2rem 0;'/>", unsafe_allow_html=True)
    else:
        st.warning(f"Target folder `{meta['key']}` not found.")
    st.markdown("</div>", unsafe_allow_html=True)

# 11. Notebook Conclusion
st.markdown(f"""
<div class="conclusion-section">
    <div class="section-label">Conclusion Summary</div>
    <p class="conclusion-text">💡 {meta['conclusion']}</p>
</div>
""", unsafe_allow_html=True)

# 12. Student Footer Placement
st.markdown("""
<div class="academic-footer">
    <span>Student: <strong>Anup Anuj Gaonkar</strong></span>
    <span class="bullet">&bull;</span>
    <span>Roll No: <strong>24B-CO-009</strong></span>
    <span class="bullet">&bull;</span>
    <span>Semester IV &middot; Computer Engineering</span>
    <span class="bullet">&bull;</span>
    <span>Course: <strong>CMP-226 (GTC Lab)</strong></span>
    <span class="bullet">&bull;</span>
    <span><strong>Goa College of Engineering</strong></span>
</div>
""", unsafe_allow_html=True)