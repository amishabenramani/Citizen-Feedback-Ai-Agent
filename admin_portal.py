"""
Admin Portal - Government Officials Website
For administrators to manage, analyze, and respond to citizen feedback.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
from streamlit_option_menu import option_menu

from src.feedback_analyzer import FeedbackAnalyzer
from src.data_manager import DataManager
from src.dashboard import Dashboard
from src.n8n_client import send_feedback_resolved

# Page configuration
st.set_page_config(
    page_title="Admin Portal - Citizen Feedback",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS for Admin Portal (Light theme aligned with Citizen Portal)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');

    :root {
        --surface: #ffffff;
        --surface-muted: #f8fafc;
        --border: #e5e7eb;
        --text-strong: #1f2937;
        --text: #374151;
        --muted: #9ca3af;
        --purple: #7c3aed;
        --purple-strong: #6d28d9;
        --purple-soft: #ede9fe;
    }

    #MainMenu, footer, header,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
    }

    .stApp {
        background: var(--surface-muted);
        min-height: 100vh;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
    }

    .main .block-container {
        padding: 1.5rem 2rem !important;
        max-width: 1200px;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-strong) !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* Header Section */
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--purple-strong);
        margin-bottom: 0.35rem;
        letter-spacing: -0.4px;
    }

    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 1.1rem;
    }

    /* Metrics/KPI Cards - Enhanced UI */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #7c3aed, #a855f7);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .metric-card:hover {
        border-color: #ddd6fe;
        box-shadow: 0 8px 20px rgba(124, 58, 237, 0.12);
        transform: translateY(-2px);
    }

    .metric-card:hover::before {
        opacity: 1;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #9ca3af;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.75rem;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1f2937;
        font-family: 'Poppins', sans-serif;
        line-height: 1;
        margin-bottom: 0.75rem;
    }

    .metric-change {
        font-size: 0.85rem;
        font-weight: 600;
        color: #10b981;
    }

    /* Chart Cards */
    .chart-container {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .chart-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1.25rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #f3f4f6;
        font-family: 'Poppins', sans-serif;
    }

    /* Alert Box */
    .alert-box {
        background: linear-gradient(135deg, #fef2f2 0%, #ffe5e5 100%);
        border: 1.5px solid #fecdd3;
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
    }

    .alert-box h4 {
        margin: 0;
        color: #991b1b;
        font-family: 'Poppins', sans-serif;
    }

    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Data Table Enhancement */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #e5e7eb !important;
    }

    .stDataFrame tbody tr:hover {
        background-color: #f8fafc !important;
    }

    /* Sidebar shell */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid var(--border);
        padding: 0 !important;
        width: 260px !important;
        display: block !important;
        visibility: visible !important;
        transform: none !important;
        margin-left: 0 !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 0 !important;
        display: block !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 0 !important;
    }

    /* Force sidebar to always be visible */
    [data-testid="stSidebar"][aria-expanded="false"] {
        display: block !important;
        visibility: visible !important;
    }

    /* Hide collapse button if needed */
    button[kind="header"] {
        display: none !important;
    }

    /* Sidebar header */
    .admin-sidebar-header {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        padding: 22px 20px 18px;
        border-radius: 0 0 18px 18px;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.18);
        color: #ffffff;
    }

    .admin-sidebar-header h2 {
        margin: 4px 0 0 0;
        font-size: 20px;
        font-weight: 700;
    }

    .admin-sidebar-header .subtitle {
        margin: 2px 0 0 0;
        color: rgba(255,255,255,0.85);
        font-size: 13px;
    }

    /* Option menu tweaks */
    .nav-link {
        background: #ffffff !important;
        border-radius: 12px !important;
        margin: 4px 12px !important;
        padding: 12px 14px !important;
        border: 1px solid #f1f1f6 !important;
        color: #4b5563 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
        transition: all 0.18s ease !important;
    }

    .nav-link:hover {
        background: #f5f3ff !important;
        border-color: #ddd6fe !important;
        transform: translateX(4px);
        color: var(--purple) !important;
        box-shadow: 0 3px 10px rgba(124, 58, 237, 0.12) !important;
    }

    .nav-link-selected {
        background: linear-gradient(135deg, #ede9fe 0%, #f6f4ff 100%) !important;
        border-color: #c4b5fd !important;
        color: var(--purple-strong) !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.16) !important;
    }

    .sidebar-divider {
        height: 1px;
        background: var(--border);
        margin: 10px 14px;
    }

    /* Ensure option-menu container is visible */
    [data-testid="stSidebar"] nav,
    [data-testid="stSidebar"] .nav-link,
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] .st-emotion-cache-16txtl3,
    [data-testid="stSidebar"] .st-emotion-cache-1gulkj5,
    [data-testid="stSidebar"] > div > div {
        display: block !important;
        visibility: visible !important;
    }

    /* Make all sidebar content visible */
    [data-testid="stSidebar"] * {
        visibility: visible !important;
    }

    /* Cards */
    .admin-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    }

    .priority-critical { background: #fef2f2; border: 1px solid #fecdd3; }
    .priority-high { background: #fffbeb; border: 1px solid #fde68a; }
    .priority-normal { background: #eef2ff; border: 1px solid #c7d2fe; }
    .priority-low { background: #ecfdf3; border: 1px solid #bbf7d0; }

    /* Buttons */
    .stButton > button[kind="primary"], .stDownloadButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.24) !important;
        font-weight: 600 !important;
    }

    .stButton > button[kind="secondary"] {
        background: #f3f4f6 !important;
        color: #4b5563 !important;
        border-radius: 10px !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        background: #ffffff !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-strong) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--purple) !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.12) !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: #ffffff !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-strong) !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderContent {
        background: #ffffff !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #f3f4f6;
        border-radius: 14px;
        padding: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #6b7280;
    }

    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: var(--purple) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }

    /* Alerts */
    .stSuccess { background: #ecfdf5 !important; color: #047857 !important; }
    .stInfo { background: #eff6ff !important; color: #1d4ed8 !important; }
    .stWarning { background: #fffbeb !important; color: #92400e !important; }
    .stError { background: #fef2f2 !important; color: #991b1b !important; }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(124,58,237,0.35), transparent);
        margin: 1.75rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Admin credentials (In production, use proper authentication)
ADMIN_USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "manager": hashlib.sha256("manager123".encode()).hexdigest(),
    "staff": hashlib.sha256("staff123".encode()).hexdigest()
}


def init_session_state():
    """Initialize session state."""
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = FeedbackAnalyzer()
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = Dashboard()
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if 'admin_username' not in st.session_state:
        st.session_state.admin_username = None


def render_login():
    """Render clean centered admin login page."""
    
    # Full page centered CSS (light, aligned to citizen theme)
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&display=swap');

    .stApp { background: #f8fafc !important; }

    .main .block-container { 
        padding: 0 !important; 
        max-width: 100% !important;
        margin: 0 !important;
    }
    header, #MainMenu, footer, [data-testid="stHeader"], [data-testid="stToolbar"], section[data-testid="stSidebar"] { display: none !important; }
    .stDeployButton { display: none !important; }

    .main > div { 
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }

    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 1.5px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
        color: #1f2937 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.12) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
    }

    [data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 26px;
        max-width: 420px;
        margin: 0 auto;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Centered login container
    col_spacer1, col_center, col_spacer2 = st.columns([1, 2, 1])
    
    with col_center:
        # Brand Logo - using stronger color enforcement
        st.markdown("""
        <div style="text-align: center; margin-bottom: 24px;">
            <div style="width: 56px; height: 56px; background: linear-gradient(135deg, #7c3aed, #8b5cf6); 
                        border-radius: 14px; display: inline-flex; align-items: center; justify-content: center;
                        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35); margin-bottom: 16px;">
                <span style="font-size: 28px;">🏛️</span>
            </div>
            <h1 style="font-family: Poppins, sans-serif; font-size: 24px; font-weight: 700; 
                       color: #7c3aed;">Admin Login</h1>
            <p style="font-size: 14px; color: #6b21a8; font-weight: 500;">
                Sign in to access the dashboard</p>
        </div>
        <style>
            .stMarkdown h1 { color: #7c3aed !important; }
            .stMarkdown p { color: #6b21a8 !important; }
        </style>
        """, unsafe_allow_html=True)
        
        # Login Form
        with st.form("login_form", clear_on_submit=False):
            st.markdown('<p style="font-size: 13px; font-weight: 600; color: #7c3aed; margin-bottom: 6px;">Username</p>', unsafe_allow_html=True)
            username = st.text_input("username", placeholder="Enter username", label_visibility="collapsed")
            
            st.markdown('<p style="font-size: 13px; font-weight: 600; color: #7c3aed; margin: 12px 0 6px 0;">Password</p>', unsafe_allow_html=True)
            password = st.text_input("password", type="password", placeholder="Enter password", label_visibility="collapsed")
            
            st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
            login_btn = st.form_submit_button("Sign in", use_container_width=True)
            
            if login_btn:
                if username in ADMIN_USERS:
                    hashed = hashlib.sha256(password.encode()).hexdigest()
                    if ADMIN_USERS[username] == hashed:
                        st.session_state.admin_logged_in = True
                        st.session_state.admin_username = username
                        st.rerun()
                    else:
                        st.error("❌ Invalid password")
                else:
                    st.error("❌ User not found")
        
        # Demo credentials
        st.markdown("""
        <div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 10px; padding: 14px 16px; margin-top: 16px;">
            <p style="font-size: 11px; font-weight: 700; color: #7c3aed; margin: 0 0 8px 0; text-transform: uppercase;">
                🔑 Demo Credentials</p>
            <p style="font-family: monospace; font-size: 13px; color: #4b5563; margin: 0;">
                <code style="background: #fff; padding: 2px 6px; border-radius: 4px;">admin</code> / 
                <code style="background: #fff; padding: 2px 6px; border-radius: 4px;">admin123</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Right column intentionally left empty for clean design


def render_sidebar():
    """Render premium admin sidebar."""
    if 'admin_page' not in st.session_state:
        st.session_state.admin_page = "Dashboard"

    with st.sidebar:
        username = st.session_state.admin_username or "Admin"

        st.markdown(f"""
        <div class="admin-sidebar-header">
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="width:46px; height:46px; border-radius:12px; background: rgba(255,255,255,0.18);
                            display:flex; align-items:center; justify-content:center; font-size:24px;">
                    ⚙️
                </div>
                <div>
                    <h2>Admin Portal</h2>
                    <div class="subtitle">Signed in as {username}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        menu_options = [
            "Dashboard",
            "All Feedback",
            "Priority Queue",
            "Assignments",
            "Staff Management",
            "Analytics",
            "Export Data",
            "Settings",
        ]

        icons = [
            "speedometer2",
            "card-checklist",
            "exclamation-triangle-fill",
            "people",
            "person-badge",
            "bar-chart-line",
            "box-arrow-down",
            "gear",
        ]

        default_index = menu_options.index(st.session_state.admin_page) if st.session_state.admin_page in menu_options else 0
        
        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=icons,
            default_index=default_index,
            key="admin_nav_menu",
            styles={
                "container": {"padding": "12px 0 8px 0", "background-color": "transparent"},
                "icon": {"color": "#2563eb", "font-size": "18px"},
                "nav-link": {
                    "text-align": "left", 
                    "font-weight": "600", 
                    "font-size": "14px",
                    "background-color": "#ffffff",
                    "color": "#4b5563",
                    "border-radius": "12px",
                    "margin": "4px 12px",
                    "padding": "12px 14px",
                },
                "nav-link-selected": {
                    "font-weight": "700", 
                    "color": "#2563eb",
                    "background-color": "#ede9fe",
                },
            },
        )
        st.session_state.admin_page = selected

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        if st.button("🚪 Sign Out", type="secondary", key="signout", disabled=False, help="Sign out", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.session_state.admin_username = None
            st.rerun()

        st.markdown("""
        <div style="text-align:center; padding: 12px 0 16px 0;">
            <p style="color:#9ca3af; font-size:12px; margin:0;">Admin Portal v2.0</p>
        </div>
        """, unsafe_allow_html=True)

        return selected


def render_dashboard():
    """Render premium admin dashboard."""
    # Hero Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(124, 58, 237, 0.1) 100%);
                border-radius: 20px; padding: 2.5rem; margin-bottom: 2rem; 
                border: 1.5px solid rgba(139, 92, 246, 0.2);">
        <h1 style="font-family: 'Poppins', sans-serif; font-size: 2.5rem; font-weight: 800;
                   background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 50%, #7c3aed 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin: 0 0 0.5rem 0; letter-spacing: -0.5px;">📊 Admin Dashboard</h1>
        <p style="color: rgba(107, 114, 128, 0.9); margin: 0; font-size: 1.05rem; font-weight: 500;">
            Real-time overview of citizen feedback and system performance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.data_manager.get_feedback_dataframe()
    
    if df.empty:
        st.markdown("""
        <div style="background: rgba(59, 130, 246, 0.08); border-radius: 16px; padding: 3rem;
                    text-align: center; border: 1px solid rgba(59, 130, 246, 0.2);">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📭</div>
            <h3 style="color: #60a5fa;">No feedback data available yet</h3>
            <p style="color: rgba(148, 163, 184, 0.8);">
                Waiting for citizens to submit their first feedback.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Premium Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total = len(df)
    new = len(df[df['status'] == 'New']) if 'status' in df else 0
    in_review = len(df[df['status'] == 'In Review']) if 'status' in df else 0
    in_progress = len(df[df['status'] == 'In Progress']) if 'status' in df else 0
    resolved = len(df[df['status'] == 'Resolved']) if 'status' in df else 0
    
    metrics_data = [
        ("📬", "Total", total, "#a78bfa", "rgba(139, 92, 246, 0.1)"),
        ("🆕", "New", new, "#60a5fa", "rgba(59, 130, 246, 0.1)"),
        ("👀", "In Review", in_review, "#f472b6", "rgba(244, 114, 182, 0.1)"),
        ("🔄", "In Progress", in_progress, "#fbbf24", "rgba(251, 191, 36, 0.1)"),
        ("✅", "Resolved", resolved, "#34d399", "rgba(52, 211, 153, 0.1)")
    ]
    
    for col, (icon, label, value, color, bg) in zip([col1, col2, col3, col4, col5], metrics_data):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="background: {bg}; border: 1px solid {color}30;">
                <div style="font-size: 1.75rem; margin-bottom: 0.75rem;">{icon}</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: {color}; font-family: 'Poppins', sans-serif; margin-bottom: 0.5rem;">
                    {value}
                </div>
                <div style="font-size: 0.9rem; color: #6b7280; font-weight: 600;">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Urgent items alert with premium styling
    if 'urgency' in df.columns:
        urgent = df[df['urgency'].isin(['High', 'Emergency'])]
        urgent_new = urgent[urgent['status'] == 'New'] if 'status' in urgent else urgent
        
        if not urgent_new.empty:
            st.markdown("""
            <div class="alert-box">
                <h4>🚨 Urgent Items Requiring Immediate Attention</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for _, row in urgent_new.head(5).iterrows():
                urgency = row.get('urgency', 'High')
                if urgency == 'Emergency':
                    border_color = "#dc2626"
                    bg_color = "rgba(220, 38, 38, 0.1)"
                    badge_color = "#f87171"
                else:
                    border_color = "#f59e0b"
                    bg_color = "rgba(245, 158, 11, 0.1)"
                    badge_color = "#fbbf24"
                    
                st.markdown(f"""
                <div style="background: {bg_color}; padding: 1rem 1.25rem; border-radius: 12px; 
                            margin-bottom: 0.75rem; border-left: 4px solid {border_color};
                            border: 1px solid {border_color}30;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #e2e8f0; font-size: 1rem;">{row.get('title', 'Untitled')}</strong>
                            <div style="color: rgba(148, 163, 184, 0.8); font-size: 0.85rem; margin-top: 0.25rem;">
                                {row.get('category', 'N/A')} • {row.get('area', row.get('location', 'N/A'))}
                            </div>
                        </div>
                        <span style="background: {border_color}25; color: {badge_color}; padding: 0.3rem 0.75rem;
                                     border-radius: 20px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">
                            {urgency}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Status Distribution</div>', unsafe_allow_html=True)
        if 'status' in df.columns:
            status_counts = df['status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                hole=0.4,
                color_discrete_sequence=['#3B82F6', '#8B5CF6', '#F59E0B', '#10B981', '#6B7280']
            )
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">😊 Sentiment Analysis</div>', unsafe_allow_html=True)
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()
            colors = {'Positive': '#10B981', 'Neutral': '#F59E0B', 'Negative': '#EF4444'}
            fig = px.bar(
                x=sentiment_counts.index,
                y=sentiment_counts.values,
                color=sentiment_counts.index,
                color_discrete_map=colors
            )
            fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=300)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Category and urgency charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📁 By Category</div>', unsafe_allow_html=True)
        if 'category' in df.columns:
            cat_counts = df['category'].value_counts().head(8)
            fig = px.bar(
                y=cat_counts.index,
                x=cat_counts.values,
                orientation='h',
                color_discrete_sequence=['#3B82F6']
            )
            fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=300)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">⚡ By Urgency</div>', unsafe_allow_html=True)
        if 'urgency' in df.columns:
            urgency_order = ['Low', 'Medium', 'High', 'Emergency']
            urgency_counts = df['urgency'].value_counts().reindex(urgency_order, fill_value=0)
            colors = ['#10B981', '#F59E0B', '#F97316', '#DC2626']
            fig = go.Figure(data=[go.Bar(
                x=urgency_counts.index,
                y=urgency_counts.values,
                marker_color=colors
            )])
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional charts row - Timeline and Location
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Submissions Over Time</div>', unsafe_allow_html=True)
        if 'timestamp' in df.columns:
            # Convert timestamp to date and count by date
            df['date'] = pd.to_datetime(df['timestamp']).dt.date if df['timestamp'].notna().any() else pd.to_datetime('today').date()
            daily_counts = df.groupby('date').size().reset_index(name='count')
            daily_counts = daily_counts.sort_values('date')
            
            fig = px.line(
                daily_counts,
                x='date',
                y='count',
                markers=True,
                color_discrete_sequence=['#3B82F6']
            )
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20), 
                height=300,
                xaxis_title="Date",
                yaxis_title="Submissions"
            )
            fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📍 By Location</div>', unsafe_allow_html=True)
        if 'location' in df.columns:
            location_counts = df['location'].value_counts().head(10)
            if not location_counts.empty:
                fig = px.bar(
                    x=location_counts.values,
                    y=location_counts.index,
                    orientation='h',
                    color_discrete_sequence=['#8B5CF6']
                )
                fig.update_layout(
                    showlegend=False, 
                    margin=dict(l=20, r=20, t=20, b=20), 
                    height=300,
                    xaxis_title="Count",
                    yaxis_title="Location"
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No location data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # # AI Insights charts
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    #     st.markdown('<div class="chart-title">🤖 AI Priority Distribution</div>', unsafe_allow_html=True)
    #     if 'ai_priority' in df.columns:
    #         ai_priority_counts = df['ai_priority'].value_counts()
    #         if not ai_priority_counts.empty:
    #             priority_order = ['Low', 'Medium', 'High']
    #             ai_priority_counts = ai_priority_counts.reindex(priority_order, fill_value=0)
    #             colors = ['#10B981', '#F59E0B', '#EF4444']
                
    #             fig = go.Figure(data=[go.Bar(
    #                 x=ai_priority_counts.index,
    #                 y=ai_priority_counts.values,
    #                 marker_color=colors
    #             )])
    #             fig.update_layout(
    #                 margin=dict(l=20, r=20, t=20, b=20), 
    #                 height=300, 
    #                 showlegend=False,
    #                 xaxis_title="AI Priority",
    #                 yaxis_title="Count"
    #             )
    #             st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    #         else:
    #             st.info("No AI priority data available")
    #     st.markdown('</div>', unsafe_allow_html=True)
    
    # with col2:
    #     st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    #     st.markdown('<div class="chart-title">🎯 AI Confidence Levels</div>', unsafe_allow_html=True)
    #     if 'ai_confidence' in df.columns:
    #         confidence_data = df['ai_confidence'].dropna()
    #         if not confidence_data.empty:
    #             # Create histogram of confidence levels
    #             fig = px.histogram(
    #                 confidence_data,
    #                 nbins=10,
    #                 color_discrete_sequence=['#6366F1']
    #             )
    #             fig.update_layout(
    #                 margin=dict(l=20, r=20, t=20, b=20), 
    #                 height=300,
    #                 xaxis_title="Confidence Level",
    #                 yaxis_title="Count",
    #                 showlegend=False 
    #             )
    #             st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    #         else:
    #             st.info("No AI confidence data available")
    #     st.markdown('</div>', unsafe_allow_html=True)
    # """Render all feedback management page."""
    # st.markdown('<p class="main-header">📋 All Feedback</p>', unsafe_allow_html=True)
    
    # df = st.session_state.data_manager.get_feedback_dataframe()
    
    # if df.empty:
    #     st.info("No feedback available.")
    #     return
    
    # # Filters
    # st.subheader("🔍 Filters")
    # col1, col2, col3, col4, col5 = st.columns(5)
    
    # with col1:
    #     status_filter = st.multiselect("Status", df['status'].unique().tolist() if 'status' in df else [])
    # with col2:
    #     category_filter = st.multiselect("Category", df['category'].unique().tolist() if 'category' in df else [])
    # with col3:
    #     urgency_filter = st.multiselect("Urgency", df['urgency'].unique().tolist() if 'urgency' in df else [])
    # with col4:
    #     sentiment_filter = st.multiselect("Sentiment", df['sentiment'].unique().tolist() if 'sentiment' in df else [])
    # with col5:
    #     search = st.text_input("🔍 Search", placeholder="Search by title or ID...")
    
    # # Apply filters
    # filtered_df = df.copy()
    # if status_filter:
    #     filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    # if category_filter:
    #     filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
    # if urgency_filter:
    #     filtered_df = filtered_df[filtered_df['urgency'].isin(urgency_filter)]
    # if sentiment_filter:
    #     filtered_df = filtered_df[filtered_df['sentiment'].isin(sentiment_filter)]
    # if search:
    #     mask = (
    #         filtered_df['title'].str.contains(search, case=False, na=False) |
    #         filtered_df['id'].str.contains(search, case=False, na=False)
    #     )
    #     filtered_df = filtered_df[mask]
    
    # st.caption(f"Showing {len(filtered_df)} of {len(df)} items")
    
    # st.divider()
    
    # # Feedback list with improved UI
    # for counter, (idx, row) in enumerate(filtered_df.iterrows()):
    #     # Determine priority class and colors
    #     urgency = row.get('urgency', 'Medium')
    #     status = row.get('status', 'New')

    #     if urgency == 'Emergency':
    #         border_color = "#dc2626"
    #         bg_color = "rgba(220, 38, 38, 0.08)"
    #         priority_badge = "🚨 EMERGENCY"
    #     elif urgency == 'High':
    #         border_color = "#f59e0b"
    #         bg_color = "rgba(245, 158, 11, 0.08)"
    #         priority_badge = "⚠️ HIGH"
    #     elif urgency == 'Low':
    #         border_color = "#10b981"
    #         bg_color = "rgba(16, 185, 129, 0.08)"
    #         priority_badge = "✅ LOW"
    #     else:
    #         border_color = "#6b7280"
    #         bg_color = "rgba(107, 114, 128, 0.08)"
    #         priority_badge = "📋 MEDIUM"

    #     # Status colors
    #     status_colors = {
    #         "New": ("🆕", "#dbeafe", "#1e40af"),
    #         "In Review": ("👀", "#e9d5ff", "#6b21a8"),
    #         "In Progress": ("🔄", "#fef3c7", "#92400e"),
    #         "Resolved": ("✅", "#d1fae5", "#065f46"),
    #         "Closed": ("📁", "#f3f4f6", "#374151")
    #     }
    #     status_emoji, status_bg, status_text = status_colors.get(status, ("📋", "#f3f4f6", "#374151"))

    #     # Create expandable card with better layout
    #     with st.container():
    #         # Header row with status and priority
    #         col_header1, col_header2, col_header3 = st.columns([3, 1, 1])

    #         with col_header1:
    #             st.markdown(f"""
    #             <div style="font-size: 1.1rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">
    #                 {row.get('title', 'Untitled')}
    #             </div>
    #             <div style="color: #6b7280; font-size: 0.9rem;">
    #                 ID: <code style="background: #f3f4f6; padding: 2px 6px; border-radius: 4px;">{row.get('id', 'N/A')}</code>
    #                 • Submitted: {row.get('timestamp', 'N/A')[:10] if row.get('timestamp') else 'N/A'}
    #             </div>
    #             """, unsafe_allow_html=True)

    #         with col_header2:
    #             st.markdown(f"""
    #             <div style="text-align: center;">
    #                 <div style="background: {status_bg}; color: {status_text}; padding: 0.5rem 1rem;
    #                            border-radius: 20px; font-weight: 600; font-size: 0.9rem; display: inline-block;">
    #                     {status_emoji} {status}
    #                 </div>
    #             </div>
    #             """, unsafe_allow_html=True)

    #         with col_header3:
    #             st.markdown(f"""
    #             <div style="text-align: center;">
    #                 <div style="background: {bg_color}; color: {border_color}; padding: 0.5rem 1rem;
    #                            border-radius: 20px; font-weight: 600; font-size: 0.9rem; border: 1px solid {border_color}30;
    #                            display: inline-block;">
    #                     {priority_badge}
    #                 </div>
    #             </div>
    #             """, unsafe_allow_html=True)

    #         # Main content in a styled container
    #         st.markdown(f"""
    #         <div style="background: {bg_color}; border: 1px solid {border_color}30; border-radius: 12px;
    #                     padding: 1.5rem; margin: 1rem 0; border-left: 4px solid {border_color};">
    #         """, unsafe_allow_html=True)

    #         # Content grid
    #         col1, col2, col3 = st.columns([2, 1, 1])

    #         with col1:
    #             st.markdown("**👤 Citizen Information**")
    #             st.write(f"**Name:** {row.get('name', 'Anonymous')}")
    #             st.write(f"**Email:** {row.get('email', 'N/A')}")
    #             st.write(f"**Phone:** {row.get('phone', 'N/A')}")

    #             st.markdown("**📍 Location & Category**")
    #             st.write(f"**Category:** {row.get('category', 'N/A')}")
    #             st.write(f"**Location:** {row.get('location', 'N/A')}")

    #         with col2:
    #             st.markdown("**🤖 AI Analysis**")

    #             # Sentiment with emoji
    #             sentiment = row.get('sentiment', 'N/A')
    #             sentiment_emojis = {'Positive': '😊', 'Neutral': '😐', 'Negative': '😟'}
    #             sentiment_emoji = sentiment_emojis.get(sentiment, '📝')
    #             st.write(f"**Sentiment:** {sentiment_emoji} {sentiment}")

    #             # AI Priority
    #             ai_priority = row.get('ai_priority', 'N/A')
    #             priority_emojis = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
    #             priority_emoji = priority_emojis.get(ai_priority, '⚪')
    #             st.write(f"**AI Priority:** {priority_emoji} {ai_priority}")

    #             # Confidence score
    #             confidence = row.get('ai_confidence')
    #             if confidence is not None:
    #                 conf_pct = int(confidence * 100)
    #                 st.progress(conf_pct / 100, text=f"Confidence: {conf_pct}%")

    #         with col3:
    #             st.markdown("**📊 Quick Stats**")

    #             # Keywords count
    #             keywords = row.get('keywords', [])
    #             if isinstance(keywords, list):
    #                 st.write(f"**Keywords:** {len(keywords)} detected")
    #             else:
    #                 st.write("**Keywords:** N/A")

    #             # AI Category
    #             ai_category = row.get('ai_category', 'N/A')
    #             st.write(f"**AI Category:** {ai_category}")

    #             # Assignment status
    #             assigned = row.get('assigned_to', 'Unassigned')
    #             if assigned != 'Unassigned':
    #                 st.write(f"**Assigned:** ✅ {assigned}")
    #             else:
    #                 st.write("**Assigned:** ❌ Unassigned")

    #         # Feedback content in expandable section
    #         with st.expander("📝 View Full Feedback Content"):
    #             st.write("**Description:**")
    #             st.write(row.get('feedback', 'No content provided'))

    #             if row.get('ai_summary'):
    #                 st.write("**AI Summary:**")
    #                 st.info(row['ai_summary'])

    #             if row.get('ai_keywords') and isinstance(row['ai_keywords'], list) and row['ai_keywords']:
    #                 st.write("**AI-Detected Topics:**")
    #                 topics_html = " ".join([f'<span style="background: #e0e7ff; color: #3730a3; padding: 2px 8px; border-radius: 12px; margin: 2px; display: inline-block; font-size: 0.85rem;">{topic}</span>' for topic in row['ai_keywords'][:10]])
    #                 st.markdown(f'<div style="margin-top: 0.5rem;">{topics_html}</div>', unsafe_allow_html=True)

    #         # Admin notes section
    #         if row.get('admin_notes'):
    #             st.markdown("**📋 Admin Response:**")
    #             st.success(row['admin_notes'])

    #         st.markdown("</div>", unsafe_allow_html=True)
            
    #         # Action buttons
    #         col_actions1, col_actions2, col_actions3, col_actions4 = st.columns(4)
            
    #         with col_actions1:
    #             if st.button("👀 View Details", key=f"view_{row.get('id', 'unknown')}_{counter}", use_container_width=True):
    #                 st.session_state.selected_feedback = row.get('id')
    #                 st.rerun()
            
    #         with col_actions2:
    #             if st.button("✏️ Update Status", key=f"update_{row.get('id', 'unknown')}_{counter}", use_container_width=True):
    #                 st.session_state.editing_feedback = row.get('id')
    #                 st.rerun()
            
    #         with col_actions3:
    #             if st.button("👤 Assign", key=f"assign_{row.get('id', 'unknown')}_{counter}", use_container_width=True):
    #                 st.session_state.assigning_feedback = row.get('id')
    #                 st.rerun()
            
    #         with col_actions4:
    #             if st.button("📧 Respond", key=f"respond_{row.get('id', 'unknown')}_{counter}", use_container_width=True):
    #                 st.session_state.responding_feedback = row.get('id')
    #                 st.rerun()
            
    #         st.divider()

def render_all_feedback():
    """Render all feedback management page."""
    st.markdown('<p class="main-header">📋 All Feedback</p>', unsafe_allow_html=True)

    df = st.session_state.data_manager.get_feedback_dataframe()

    if df.empty:
        st.info("No feedback available.")
        return

    # Add filters
    st.markdown("### 🔍 Filters")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        status_filter = st.multiselect(
            "Status",
            options=["New", "In Review", "In Progress", "Resolved", "Closed"],
            default=[],
            key="status_filter"
        )

    with col2:
        urgency_filter = st.multiselect(
            "Priority",
            options=["Low", "Medium", "High", "Emergency"],
            default=[],
            key="urgency_filter"
        )

    with col3:
        category_filter = st.multiselect(
            "Category",
            options=df['category'].dropna().unique().tolist() if 'category' in df.columns else [],
            default=[],
            key="category_filter"
        )

    with col4:
        assigned_filter = st.multiselect(
            "Assigned To",
            options=df['assigned_to'].dropna().unique().tolist() if 'assigned_to' in df.columns else [],
            default=[],
            key="assigned_filter"
        )

    # Apply filters
    filtered_df = df.copy()

    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]

    if urgency_filter:
        filtered_df = filtered_df[filtered_df['urgency'].isin(urgency_filter)]

    if category_filter:
        filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]

    if assigned_filter:
        filtered_df = filtered_df[filtered_df['assigned_to'].isin(assigned_filter)]

    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} feedback items**")

    # Simple feedback list
    for idx, row in filtered_df.iterrows():
        # Determine priority class
        urgency = row.get('urgency', 'Medium')
        if urgency == 'Emergency':
            priority_class = 'priority-critical'
        elif urgency == 'High':
            priority_class = 'priority-high'
        elif urgency == 'Low':
            priority_class = 'priority-low'
        else:
            priority_class = 'priority-normal'

        with st.expander(f"**{row.get('id', 'N/A')}** - {row.get('title', 'Untitled')} [{row.get('status', 'New')}]"):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("**📋 Feedback Details**")
                st.write(f"**ID:** `{row.get('id', 'N/A')}`")
                st.write(f"**From:** {row.get('name', 'Anonymous')} ({row.get('email', 'N/A')})")
                st.write(f"**Phone:** {row.get('phone', 'N/A')}")
                st.write(f"**Category:** {row.get('category', 'N/A')}")
                st.write(f"**Location:** {row.get('location', 'N/A')}")
                st.write(f"**Submitted:** {row.get('timestamp', 'N/A')[:16] if row.get('timestamp') else 'N/A'}")

                st.divider()

                st.markdown("**📝 Feedback Content**")
                st.write(row.get('feedback', 'No content'))

                st.divider()

                st.markdown("**🤖 AI Analysis**")

                # Basic Analysis
                sentiment_emoji = {'Positive': '😊', 'Neutral': '😐', 'Negative': '😟'}
                st.write(f"**Basic Sentiment:** {sentiment_emoji.get(row.get('sentiment', ''), '📝')} {row.get('sentiment', 'N/A')} (Score: {row.get('sentiment_score', 0):.2f})")
                st.write(f"**Keywords:** {', '.join(row.get('keywords', [])) if isinstance(row.get('keywords'), list) else row.get('keywords', 'N/A')}")
                st.write(f"**Summary:** {row.get('summary', 'N/A')}")

                st.divider()

                # Advanced AI Analysis
                if row.get('ai_sentiment') or row.get('ai_confidence'):
                    st.markdown("**🚀 Advanced AI Analysis**")

                    col_ai1, col_ai2 = st.columns(2)

                    with col_ai1:
                        ai_sentiment = row.get('ai_sentiment', 'N/A')
                        ai_sentiment_emoji = {'Positive': '🟢', 'Neutral': '🟡', 'Negative': '🔴'}
                        st.write(f"**AI Sentiment:** {ai_sentiment_emoji.get(ai_sentiment, '⚪')} {ai_sentiment}")

                        ai_priority = row.get('ai_priority', 'N/A')
                        ai_priority_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                        st.write(f"**AI Priority:** {ai_priority_emoji.get(ai_priority, '⚪')} {ai_priority}")

                    with col_ai2:
                        ai_confidence = row.get('ai_confidence')
                        if ai_confidence is not None:
                            confidence_pct = int(ai_confidence * 100)
                            st.progress(confidence_pct / 100, text=f"Confidence: {confidence_pct}%")
                        else:
                            st.write("**Confidence:** N/A")

                        ai_category = row.get('ai_category', 'N/A')
                        st.write(f"**AI Category:** 📁 {ai_category}")

                    # AI Summary and Keywords
                    if row.get('ai_summary'):
                        with st.expander("📝 AI Summary"):
                            st.write(row['ai_summary'])

                    if row.get('ai_keywords') and isinstance(row['ai_keywords'], list) and row['ai_keywords']:
                        with st.expander("🏷️ AI-Detected Topics"):
                            st.write(", ".join(row['ai_keywords'][:15]))  # Show top 15

            with col2:
                st.markdown("**📊 Current Status**")
                st.write(f"**Status:** {row.get('status', 'New')}")
                st.write(f"**Urgency:** {row.get('urgency', 'Medium')}")
                if row.get('assigned_to'):
                    st.write(f"**Assigned To:** {row.get('assigned_to')}")
                if row.get('admin_notes'):
                    st.info(f"**Admin Response:** {row.get('admin_notes')}")

                st.divider()

                # Quick Actions
                st.markdown("**⚡ Quick Actions**")

                # Status update
                current_status = row.get('status', 'New')
                new_status = st.selectbox(
                    "Update Status",
                    ["New", "In Review", "In Progress", "Resolved", "Closed"],
                    index=["New", "In Review", "In Progress", "Resolved", "Closed"].index(current_status),
                    key=f"status_{row.get('id', idx)}"
                )

                # Priority
                current_priority = row.get('priority', 'Normal')
                priority_options = ["Low", "Normal", "High", "Critical"]
                new_priority = st.selectbox(
                    "Priority",
                    priority_options,
                    index=priority_options.index(current_priority) if current_priority in priority_options else 1,
                    key=f"priority_{row.get('id', idx)}"
                )

                # Assignment - Get staff from database
                staff_names = st.session_state.data_manager.get_staff_names(active_only=True)
                current_assigned = row.get('assigned_to', '')

                if staff_names:
                    # Use selectbox with staff from database
                    staff_options = ["None"] + staff_names
                    if current_assigned and current_assigned not in staff_options:
                        staff_options.insert(1, current_assigned)

                    default_index = staff_options.index(current_assigned) if current_assigned in staff_options else 0
                    assigned = st.selectbox(
                        "Assign To",
                        staff_options,
                        index=default_index,
                        key=f"assign_{row.get('id', idx)}"
                    )
                    if assigned == "None":
                        assigned = ""
                else:
                    # No staff in database, use text input
                    assigned = st.text_input(
                        "Assign To",
                        value=current_assigned,
                        placeholder="Add staff in Staff Management first",
                        key=f"assign_{row.get('id', idx)}"
                    )

                # Admin Notes
                admin_notes = st.text_area(
                    "Admin Notes/Response",
                    value=row.get('admin_notes', ''),
                    placeholder="Add notes or response for citizen...",
                    key=f"notes_{row.get('id', idx)}"
                )

                # Save button with workflow validation
                if st.button("💾 Save Changes", key=f"save_{row.get('id', idx)}", use_container_width=True):
                    # Workflow validation: Only allow In Progress/Resolved/Closed if assigned
                    if new_status in ["In Progress", "Resolved", "Closed"] and (not assigned or assigned == "None"):
                        st.error(f"❌ Cannot mark as '{new_status}' without assigning to staff. Please select a staff member first.")
                    else:
                        # Update the feedback
                        updates = {
                            'status': new_status,
                            'priority': new_priority,
                            'assigned_to': assigned,
                            'admin_notes': admin_notes,
                            'updated_at': datetime.now().isoformat()
                        }

                        success = st.session_state.data_manager.update_feedback(row.get('id'), updates)
                        if success:
                            # Send notification if resolved
                            if new_status == "Resolved":
                                # Get updated feedback data for n8n notification
                                updated_feedback = st.session_state.data_manager.get_feedback_by_id(row.get('id'))
                                if updated_feedback:
                                    send_feedback_resolved(updated_feedback)

                            st.success("✅ Feedback updated successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to update feedback.")

                # Delete button
                if st.button("�️ Delete", key=f"delete_{row.get('id', idx)}", type="secondary", use_container_width=True):
                    st.session_state.data_manager.delete_feedback(row.get('id'))
                    st.warning("Feedback deleted")
                    st.rerun()
def render_priority_queue():
    """Render priority queue for urgent items."""
    st.markdown('<p class="main-header">🚨 Priority Queue</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Urgent and high-priority items requiring immediate attention</p>', unsafe_allow_html=True)
    
    df = st.session_state.data_manager.get_feedback_dataframe()
    
    if df.empty:
        st.info("No feedback available.")
        return
    
    # Filter urgent items
    urgent_df = df[
        (df['urgency'].isin(['High', 'Emergency'])) | 
        (df.get('priority', pd.Series(['Normal'] * len(df))).isin(['High', 'Critical']))
    ]
    
    # Further filter to only non-resolved
    if 'status' in urgent_df.columns:
        urgent_df = urgent_df[~urgent_df['status'].isin(['Resolved', 'Closed'])]
    
    if urgent_df.empty:
        st.success("✅ No urgent items pending! All caught up.")
        return
    
    st.warning(f"⚠️ {len(urgent_df)} urgent items require attention")
    
    # Sort by urgency (Emergency first) then by date
    urgency_order = {'Emergency': 0, 'High': 1, 'Medium': 2, 'Low': 3}
    urgent_df['urgency_rank'] = urgent_df['urgency'].map(urgency_order)
    urgent_df = urgent_df.sort_values(['urgency_rank', 'timestamp'])
    
    for _, row in urgent_df.iterrows():
        urgency = row.get('urgency', 'Medium')
        bg_color = '#FEE2E2' if urgency == 'Emergency' else '#FEF3C7'
        border_color = '#DC2626' if urgency == 'Emergency' else '#F59E0B'
        
        st.markdown(f"""
        <div style="background: {bg_color}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 5px solid {border_color};">
            <h4 style="margin: 0;">{'🚨' if urgency == 'Emergency' else '⚠️'} {row.get('title', 'Untitled')}</h4>
            <p><strong>ID:</strong> {row.get('id', 'N/A')} | 
               <strong>Category:</strong> {row.get('category', 'N/A')} | 
               <strong>Status:</strong> {row.get('status', 'New')} |
               <strong>Location:</strong> {row.get('location', 'N/A')}</p>
            <p><strong>From:</strong> {row.get('name', 'Anonymous')} | 
               <strong>Submitted:</strong> {row.get('timestamp', 'N/A')[:16] if row.get('timestamp') else 'N/A'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👀 Mark In Review", key=f"review_{row.get('id')}"):
                st.session_state.data_manager.update_status(row.get('id'), 'In Review')
                st.rerun()
        with col2:
            if st.button("🔄 Mark In Progress", key=f"progress_{row.get('id')}"):
                st.session_state.data_manager.update_status(row.get('id'), 'In Progress')
                st.rerun()
        with col3:
            if st.button("✅ Mark Resolved", key=f"resolve_{row.get('id')}"):
                # Update status and add timestamp
                feedback_id = row.get('id')
                st.session_state.data_manager.update_status(feedback_id, 'Resolved')
                
                # Get updated entry and ensure all required fields are set
                updated = st.session_state.data_manager.get_feedback_by_id(feedback_id)
                if updated:
                    # Ensure required fields for n8n
                    if 'updated_at' not in updated or not updated.get('updated_at'):
                        from datetime import datetime
                        updated['updated_at'] = datetime.now().isoformat()
                    if 'admin_notes' not in updated or not updated.get('admin_notes'):
                        updated['admin_notes'] = 'Resolved by admin'
                    if 'assigned_to' not in updated or not updated.get('assigned_to'):
                        updated['assigned_to'] = 'City Admin'
                    
                    # CRITICAL: Ensure citizen email and name are present
                    if not updated.get('citizen_email'):
                        updated['citizen_email'] = updated.get('email', '')
                    if not updated.get('citizen_name'):
                        updated['citizen_name'] = updated.get('name', 'Anonymous')
                    
                    # Validate email exists before sending to n8n
                    if not updated.get('citizen_email'):
                        st.error("❌ Cannot send email: Citizen email address is missing in feedback data!")
                        print(f"[ERROR] Missing citizen_email for feedback {feedback_id}")
                    else:
                        try:
                            print(f"[DEBUG] Sending resolution for {feedback_id}")
                            print(f"[DEBUG] citizen_email: '{updated.get('citizen_email')}'")
                            print(f"[DEBUG] citizen_name: '{updated.get('citizen_name')}'")
                            result = send_feedback_resolved(updated)
                            print(f"[DEBUG] Resolution result: {result}")
                            if result:
                                st.success("✅ Resolved and email sent to citizen!")
                            else:
                                st.warning("✅ Resolved but email notification had an issue. Check logs.")
                        except Exception as e:
                            print(f"[ERROR] Resolution email error: {e}")
                            st.error(f"❌ Error sending resolution email: {e}")
                st.rerun()
        
        st.divider()


def render_assignments():
    """Render staff assignments page."""
    st.markdown('<p class="main-header">👥 Staff Assignments</p>', unsafe_allow_html=True)
    
    df = st.session_state.data_manager.get_feedback_dataframe()
    
    if df.empty:
        st.info("No feedback to assign.")
        return
    
    # Get assignment stats
    if 'assigned_to' in df.columns:
        assigned = df[df['assigned_to'].notna() & (df['assigned_to'] != '')]
        unassigned = df[df['assigned_to'].isna() | (df['assigned_to'] == '')]
    else:
        assigned = pd.DataFrame()
        unassigned = df
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📋 Unassigned", len(unassigned))
    with col2:
        st.metric("👤 Assigned", len(assigned))
    
    st.divider()
    
    # Assignments by staff
    if not assigned.empty and 'assigned_to' in assigned.columns:
        st.subheader("📊 Workload by Staff")
        staff_counts = assigned['assigned_to'].value_counts()
        fig = px.bar(
            x=staff_counts.index,
            y=staff_counts.values,
            color_discrete_sequence=['#3B82F6']
        )
        fig.update_layout(xaxis_title="Staff Member", yaxis_title="Assigned Items")
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Get staff from database
    staff_names = st.session_state.data_manager.get_staff_names(active_only=True)
    
    # Unassigned items
    st.subheader("📋 Unassigned Items")
    
    if unassigned.empty:
        st.success("✅ All items have been assigned!")
    else:
        for _, row in unassigned.head(20).iterrows():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.write(f"**{row.get('id')}** - {row.get('title', 'Untitled')} | {row.get('category', 'N/A')} | {row.get('urgency', 'Medium')}")
            
            with col2:
                if staff_names:
                    # Show selectbox with staff from database
                    staff_options = ["Select staff..."] + staff_names
                    selected = st.selectbox(
                        "Staff",
                        options=staff_options,
                        key=f"staff_select_{row.get('id')}",
                        label_visibility="collapsed"
                    )
                else:
                    # No staff in database
                    selected = st.selectbox(
                        "Staff",
                        options=["No staff available - Add in Staff Management"],
                        key=f"staff_select_{row.get('id')}",
                        label_visibility="collapsed"
                    )
            
            with col3:
                # Assign button
                if st.button("Assign", key=f"assign_btn_{row.get('id')}", type="primary"):
                    if selected and selected != "Select staff..." and "No staff available" not in selected:
                        st.session_state.data_manager.update_feedback(row.get('id'), {'assigned_to': selected})
                        st.success(f"✅ Assigned to {selected}")
                        st.rerun()
                    else:
                        st.error("⚠️ Please select a staff member")
            
            st.divider()


def render_advanced_analytics():
    """Render the Advanced Analytics dashboard as a dedicated page."""
    st.markdown('<p class="main-header">� Analytics & Insights</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Comprehensive trends, performance metrics, and detailed feedback analysis</p>', unsafe_allow_html=True)

    df = st.session_state.data_manager.get_feedback_dataframe()

    if df.empty:
        st.info("No data for analytics.")
        return

    st.session_state.dashboard.render_advanced_analytics_dashboard(df)



def render_export():
    """Render data export page."""
    st.markdown('<p class="main-header">📤 Export Data</p>', unsafe_allow_html=True)
    
    df = st.session_state.data_manager.get_feedback_dataframe()
    
    if df.empty:
        st.info("No data to export.")
        return
    
    st.subheader("📊 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV Export
        st.markdown("### 📄 CSV Export")
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            "citizen_feedback_export.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col2:
        # JSON Export
        st.markdown("### 📋 JSON Export")
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            "📥 Download JSON",
            json_data,
            "citizen_feedback_export.json",
            "application/json",
            use_container_width=True
        )
    
    st.divider()
    
    # Preview
    st.subheader("👁️ Data Preview")
    st.dataframe(df, use_container_width=True)
    
    # Statistics
    st.divider()
    st.subheader("📊 Export Statistics")
    st.write(f"**Total Records:** {len(df)}")
    st.write(f"**Columns:** {', '.join(df.columns.tolist())}")


def render_settings():
    """Render admin settings page."""
    st.markdown('<p class="main-header">⚙️ Settings</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗄️ Data Management")
        
        df = st.session_state.data_manager.get_feedback_dataframe()
        st.info(f"Total records in database: {len(df)}")
        
        st.divider()
        
        st.warning("⚠️ Danger Zone")
        
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.session_state.get('confirm_clear', False):
                st.session_state.data_manager.clear_all_data()
                st.session_state.confirm_clear = False
                st.success("All data cleared!")
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.error("⚠️ Click again to confirm deletion of ALL data!")
    
    with col2:
        st.subheader("👤 Account Info")
        st.write(f"**Username:** {st.session_state.admin_username}")
        st.write(f"**Role:** Administrator")
        st.write(f"**Last Login:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        st.divider()
        
        st.subheader("ℹ️ System Info")
        st.write("**Version:** 1.0.0")
        st.write("**Environment:** Production")


def render_staff_management():
    """Render staff management page with CRUD operations."""
    st.markdown('<p class="main-header">👥 Staff Management</p>', unsafe_allow_html=True)
    
    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["📋 All Staff", "➕ Add Staff", "📊 Staff Stats"])
    
    with tab1:
        st.subheader("All Staff Members")
        
        # Get all staff (including inactive)
        all_staff = st.session_state.data_manager.get_all_staff(active_only=False)
        
        if not all_staff:
            st.info("No staff members found. Add staff members using the 'Add Staff' tab.")
        else:
            # Display as cards with edit/delete options
            for staff in all_staff:
                status_color = "#10B981" if staff['active'] == 'Active' else "#9CA3AF"
                status_bg = "rgba(16, 185, 129, 0.1)" if staff['active'] == 'Active' else "rgba(156, 163, 175, 0.1)"
                
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="background: {status_bg}; padding: 1rem; border-radius: 12px; 
                                    border-left: 4px solid {status_color}; margin-bottom: 1rem;">
                            <h4 style="margin: 0; color: #1f2937;">{staff['name']}</h4>
                            <p style="margin: 0.5rem 0 0 0; color: #6b7280; font-size: 0.9rem;">
                                📧 {staff.get('email', 'N/A')} | 📱 {staff.get('phone', 'N/A')}<br>
                                🏢 {staff.get('department', 'N/A')} | 💼 {staff.get('role', 'N/A')}<br>
                                <span style="background: {status_color}30; color: {status_color}; padding: 0.2rem 0.5rem; 
                                      border-radius: 12px; font-size: 0.75rem; font-weight: 600;">
                                    {staff['active']}
                                </span>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_staff_{staff['id']}", use_container_width=True):
                            st.session_state[f"editing_staff_{staff['id']}"] = True
                            st.rerun()
                    
                    with col3:
                        if staff['active'] == 'Active':
                            if st.button("🗑️ Deactivate", key=f"del_staff_{staff['id']}", type="secondary", use_container_width=True):
                                st.session_state.data_manager.delete_staff(staff['id'])
                                st.success(f"Deactivated {staff['name']}")
                                st.rerun()
                        else:
                            if st.button("✅ Activate", key=f"act_staff_{staff['id']}", type="primary", use_container_width=True):
                                st.session_state.data_manager.update_staff(staff['id'], {'active': 'Active'})
                                st.success(f"Activated {staff['name']}")
                                st.rerun()
                    
                    # Edit form (appears when edit button is clicked)
                    if st.session_state.get(f"editing_staff_{staff['id']}", False):
                        with st.expander("Edit Staff Details", expanded=True):
                            with st.form(key=f"edit_form_{staff['id']}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    edit_name = st.text_input("Name", value=staff['name'], key=f"edit_name_{staff['id']}")
                                    edit_email = st.text_input("Email", value=staff.get('email', ''), key=f"edit_email_{staff['id']}")
                                    edit_dept = st.text_input("Department", value=staff.get('department', ''), key=f"edit_dept_{staff['id']}")
                                with col2:
                                    edit_phone = st.text_input("Phone", value=staff.get('phone', ''), key=f"edit_phone_{staff['id']}")
                                    edit_role = st.text_input("Role", value=staff.get('role', ''), key=f"edit_role_{staff['id']}")
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True):
                                        updates = {
                                            'name': edit_name,
                                            'email': edit_email,
                                            'phone': edit_phone,
                                            'department': edit_dept,
                                            'role': edit_role
                                        }
                                        if st.session_state.data_manager.update_staff(staff['id'], updates):
                                            st.success("✅ Staff updated successfully!")
                                            st.session_state[f"editing_staff_{staff['id']}"] = False
                                            st.rerun()
                                        else:
                                            st.error("❌ Failed to update staff")
                                with col2:
                                    if st.form_submit_button("Cancel", use_container_width=True):
                                        st.session_state[f"editing_staff_{staff['id']}"] = False
                                        st.rerun()
    
    with tab2:
        st.subheader("Add New Staff Member")
        
        with st.form(key="add_staff_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name *", placeholder="Enter full name")
                email = st.text_input("Email", placeholder="staff@example.com")
                department = st.text_input("Department", placeholder="e.g., Public Works")
            
            with col2:
                phone = st.text_input("Phone", placeholder="+1234567890")
                role = st.text_input("Role", placeholder="e.g., Field Inspector")
            
            if st.form_submit_button("➕ Add Staff", type="primary", use_container_width=True):
                if not name:
                    st.error("❌ Name is required!")
                else:
                    staff_data = {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'department': department,
                        'role': role,
                        'active': 'Active'
                    }
                    staff_id = st.session_state.data_manager.add_staff(staff_data)
                    if staff_id:
                        st.success(f"✅ Staff member '{name}' added successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to add staff. Name or email might already exist.")
    
    with tab3:
        st.subheader("Staff Statistics")
        
        all_staff = st.session_state.data_manager.get_all_staff(active_only=False)
        active_staff = [s for s in all_staff if s['active'] == 'Active']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Staff", len(all_staff))
        with col2:
            st.metric("Active Staff", len(active_staff))
        with col3:
            st.metric("Inactive Staff", len(all_staff) - len(active_staff))
        
        st.divider()
        
        # Staff by department
        if active_staff:
            departments = [s.get('department', 'Unassigned') for s in active_staff]
            dept_counts = pd.Series(departments).value_counts()
            
            st.subheader("📊 Staff by Department")
            fig = px.bar(
                x=dept_counts.values,
                y=dept_counts.index,
                orientation='h',
                color_discrete_sequence=['#3B82F6']
            )
            fig.update_layout(xaxis_title="Number of Staff", yaxis_title="Department", height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Workload distribution - only show staff from database
        df = st.session_state.data_manager.get_feedback_dataframe()
        if not df.empty and 'assigned_to' in df.columns:
            st.subheader("📈 Current Workload Distribution")
            
            # Get staff names from database
            staff_names = st.session_state.data_manager.get_staff_names(active_only=False)
            
            assigned = df[df['assigned_to'].notna() & (df['assigned_to'] != '')]
            if not assigned.empty:
                # Filter to only show staff from database
                workload_all = assigned['assigned_to'].value_counts()
                workload = workload_all[workload_all.index.isin(staff_names)]
                
                if not workload.empty:
                    fig = px.bar(
                        x=workload.index,
                        y=workload.values,
                        color_discrete_sequence=['#8B5CF6']
                    )
                    fig.update_layout(xaxis_title="Staff Member", yaxis_title="Assigned Feedbacks", height=300)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No assignments to registered staff members yet")
            else:
                st.info("No assignments yet")


def main():
    """Main entry point for Admin Portal."""
    init_session_state()
    
    # Check login
    if not st.session_state.admin_logged_in:
        # Hide sidebar for login page
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none !important;}
        .stApp {background: #ffffff !important;}
        </style>
        """, unsafe_allow_html=True)
        render_login()
        return

    page = render_sidebar()
    
    if page == "Dashboard":
        render_dashboard()
    elif page == "All Feedback":
        render_all_feedback()
    elif page == "Priority Queue":
        render_priority_queue()
    elif page == "Assignments":
        render_assignments()
    elif page == "Staff Management":
        render_staff_management()
    elif page == "Analytics":
        render_advanced_analytics()
    elif page == "Export Data":
        render_export()
    elif page == "Settings":
        render_settings()


if __name__ == "__main__":
    main()
