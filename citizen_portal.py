"""
Citizen Portal - Public Website
For citizens to submit feedback, track their submissions, and view public updates.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu

from src.feedback_analyzer import FeedbackAnalyzer
from src.data_manager import DataManager
from src.n8n_client import send_feedback_submitted

# Page configuration
st.set_page_config(
    page_title="Citizen Feedback Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS for Citizen Portal (Clean White Theme with Purple Accents)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');
    
    /* ========== REMOVE ALL STREAMLIT DEFAULT SPACING ========== */
    #MainMenu, footer, header,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        visibility: hidden !important;
    }
    
    /* Root app container - zero top spacing */
    .stApp {
        background: #f8fafc;
        min-height: 100vh;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* App view container */
    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Main content block container */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin-top: 0 !important;
        max-width: 1200px;
    }
    
    /* First element in main content - no extra spacing */
    .main .block-container > div:first-child,
    .main [data-testid="stVerticalBlock"] > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* ========== SIDEBAR - ZERO TOP SPACING ========== */
    [data-testid="stSidebar"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 0 !important;
        gap: 0 !important;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Sidebar content starts at top */
    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* ========== GLOBAL APP BACKGROUND ========== */
    
    /* Premium Header Styling */
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f2937;
        text-align: left;
        margin-bottom: 0.25rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #6b7280;
        text-align: left;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    /* Clean Cards */
    .citizen-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .citizen-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(124, 58, 237, 0.12);
        border-color: #c4b5fd;
    }
    
    .citizen-card h3 {
        color: #1f2937;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .citizen-card p {
        color: #6b7280;
        line-height: 1.5;
        font-size: 0.9rem;
    }
    
    /* Status Badges - Clean Style */
    .status-badge {
        padding: 0.35rem 0.85rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.3px;
        display: inline-block;
    }
    
    .status-new { 
        background: #eff6ff; 
        color: #2563eb;
    }
    .status-review { 
        background: #f5f3ff; 
        color: #7c3aed;
    }
    .status-progress { 
        background: #fffbeb; 
        color: #d97706;
    }
    .status-resolved { 
        background: #ecfdf5; 
        color: #059669;
    }
    
    /* Info Box */
    .info-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.25rem;
        color: #374151;
    }
    
    .info-box h4 {
        color: #7c3aed;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        margin-bottom: 0.75rem;
        font-size: 0.95rem;
    }
    
    .info-box ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    
    .info-box li {
        margin-bottom: 0.4rem;
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    /* Premium Button Styling */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.65rem 1.5rem;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        border: none;
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.4);
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 10px !important;
        color: #1f2937 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #9ca3af !important;
    }
    
    /* Radio and Checkbox */
    .stRadio > div {
        background: #ffffff;
        border-radius: 10px;
        padding: 0.5rem;
        border: 1px solid #e5e7eb;
    }
    
    .stRadio label, .stCheckbox label {
        color: #374151 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Metrics Card Styling */
    [data-testid="stMetricValue"] {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #7c3aed !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #e5e7eb !important;
        color: #1f2937 !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderContent {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f3f4f6;
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #6b7280;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 0.6rem 1.2rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #ffffff;
        color: #7c3aed;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #7c3aed !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Sidebar Premium Styling - Clean Drawer Design */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb;
        min-width: 260px !important;
        width: 260px !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: #ffffff !important;
        width: 260px !important;
        padding: 0 !important;
    }
    
    /* Remove ALL extra padding and gaps from sidebar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Force sidebar to always be visible */
    [data-testid="stSidebar"][aria-expanded="false"] {
        display: block !important;
        width: 260px !important;
        margin-left: 0 !important;
        transform: none !important;
    }
    
    /* Hide collapse button */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding: 0 !important;
    }
    
    /* Sidebar button styling - LEFT ALIGNED with tight spacing */
    [data-testid="stSidebar"] .stButton {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        background: transparent !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        margin: 0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        font-weight: 400 !important;
        color: #4b5563 !important;
        box-shadow: none !important;
        transition: all 0.15s ease !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
        min-height: unset !important;
        height: auto !important;
        line-height: 1.4 !important;
    }
    
    [data-testid="stSidebar"] .stButton > button p {
        text-align: left !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #f3f4f6 !important;
        color: #1f2937 !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:active,
    [data-testid="stSidebar"] .stButton > button:focus {
        background: #ede9fe !important;
        color: #7c3aed !important;
        box-shadow: none !important;
    }
    
    /* Active nav button */
    [data-testid="stSidebar"] .nav-active > button {
        background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%) !important;
        color: #7c3aed !important;
        font-weight: 500 !important;
    }
    
    /* Section Labels */
    .section-label {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.65rem !important;
        font-weight: 700 !important;
        color: #6b7280 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 0.5rem 1rem 0.25rem !important;
        margin: 0 !important;
        display: block !important;
    }
    
    /* Divider Line */
    .sidebar-divider {
        height: 1px;
        background: #e5e7eb;
        margin: 0.35rem 0.75rem;
    }
    
    /* Sidebar text input styling */
    [data-testid="stSidebar"] .stTextInput {
        padding: 0 0.75rem !important;
        margin: 0 !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        color: #1f2937 !important;
        font-size: 0.8rem !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.1) !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
    }
    
    /* Sidebar Success message */
    [data-testid="stSidebar"] .stSuccess {
        background: #ecfdf5 !important;
        border-left-color: #10b981 !important;
        color: #065f46 !important;
        font-size: 0.75rem !important;
        padding: 0.35rem 0.5rem !important;
        margin: 0.25rem 0.75rem !important;
    }
    
    /* FAB Button */
    .fab-button {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .fab-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
    }
    
    /* Divider styling */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent);
        margin: 2rem 0;
    }
    
    /* Success/Warning/Error alerts - Light theme */
    .stSuccess {
        background: #ecfdf5 !important;
        border-radius: 10px !important;
        border-left: 4px solid #10b981 !important;
        color: #065f46 !important;
    }
    
    .stInfo {
        background: #eff6ff !important;
        border-radius: 10px !important;
        border-left: 4px solid #3b82f6 !important;
        color: #1e40af !important;
    }
    
    .stWarning {
        background: #fffbeb !important;
        border-radius: 10px !important;
        border-left: 4px solid #f59e0b !important;
        color: #92400e !important;
    }
    
    .stError {
        background: #fef2f2 !important;
        border-radius: 10px !important;
        border-left: 4px solid #ef4444 !important;
        color: #991b1b !important;
    }
    
    /* Text color fixes - Dark text for light theme */
    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #374151 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* File uploader styling - Light theme */
    [data-testid="stFileUploader"] {
        background: #ffffff;
        border-radius: 12px;
        border: 2px dashed #d1d5db;
        padding: 1rem;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #7c3aed;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #60a5fa) !important;
    }
    
    /* Caption styling */
    .stCaption {
        color: rgba(148, 163, 184, 0.7) !important;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state."""
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = FeedbackAnalyzer()
    if 'citizen_id' not in st.session_state:
        st.session_state.citizen_id = None
    if 'submitted_ids' not in st.session_state:
        st.session_state.submitted_ids = []
    if 'menu_selection' not in st.session_state:
        st.session_state.menu_selection = "Home"
    if 'menu_index' not in st.session_state:
        st.session_state.menu_index = 0
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    if 'stay_on_page' not in st.session_state:
        st.session_state.stay_on_page = False
    if 'success_shown' not in st.session_state:
        st.session_state.success_shown = False
    if 'n8n_success' not in st.session_state:
        st.session_state.n8n_success = False
    if 'submission_in_progress' not in st.session_state:
        st.session_state.submission_in_progress = False


def render_sidebar():
    """Render citizen sidebar with clean, modern option_menu navigation."""
    
    # Reset menu_changed flag at the start of each render
    # This prevents false positives from previous renders
    if 'menu_changed' not in st.session_state:
        st.session_state.menu_changed = False
    
    # Custom CSS for modern sidebar styling
    st.markdown("""
    <style>
    /* ========== SIDEBAR CONTAINER ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fefefe 0%, #f8f9fc 100%);
        padding: 0;
        border-right: 1px solid #e8e8ef;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 0;
    }
    
    /* ========== SIDEBAR HEADER ========== */
    .sidebar-header {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        padding: 24px 20px;
        margin: 0;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.2);
    }
    
    .sidebar-header-content {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .sidebar-icon {
        width: 45px;
        height: 45px;
        background: rgba(255,255,255,0.2);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        backdrop-filter: blur(10px);
    }
    
    .sidebar-title {
        font-family: 'Poppins', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        line-height: 1.2;
    }
    
    .sidebar-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: rgba(255,255,255,0.85);
        margin: 0;
        font-weight: 400;
    }
    
    /* ========== SECTION TITLES ========== */
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 700;
        color: #8b8b9e;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        padding: 20px 20px 10px 20px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .section-title::before {
        content: '';
        width: 4px;
        height: 4px;
        background: #7c3aed;
        border-radius: 50%;
    }
    
    /* ========== MENU CONTAINER ========== */
    .menu-container {
        padding: 10px 15px;
    }
    
    /* ========== OPTION MENU OVERRIDES ========== */
    .nav-link {
        background: #ffffff !important;
        border-radius: 12px !important;
        margin: 4px 0 !important;
        padding: 12px 16px !important;
        border: 1px solid #f0f0f5 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }
    
    .nav-link:hover {
        background: #f5f3ff !important;
        border-color: #ddd6fe !important;
        transform: translateX(3px);
        box-shadow: 0 3px 10px rgba(124, 58, 237, 0.1) !important;
    }
    
    .nav-link-selected {
        background: linear-gradient(135deg, #ede9fe 0%, #f3e8ff 100%) !important;
        border-color: #c4b5fd !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15) !important;
    }
    
    /* ========== QUICK TRACK SECTION ========== */
    .quick-track-container {
        padding: 0 20px;
        margin-top: 10px;
    }
    
    .quick-track-input {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 14px;
        width: 100%;
        transition: all 0.2s ease;
    }
    
    .quick-track-input:focus {
        border-color: #7c3aed;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
        outline: none;
    }
    
    /* ========== FOOTER ========== */
    .sidebar-footer {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 15px 20px;
        text-align: center;
        border-top: 1px solid #f0f0f5;
        background: #fafafa;
    }
    
    .sidebar-footer p {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: #9ca3af;
        margin: 0;
    }
    
    .sidebar-footer span {
        color: #7c3aed;
        font-weight: 600;
    }
    
    /* ========== STREAMLIT INPUT OVERRIDE ========== */
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 1.5px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
        color: #374151 !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
    }
    
    /* Success message styling */
    [data-testid="stSidebar"] .stSuccess {
        background: #ecfdf5 !important;
        border: 1px solid #a7f3d0 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
    }
    
    /* Hide default sidebar padding */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    
    /* Ensure sidebar header starts at very top */
    [data-testid="stSidebar"] > div > div > div {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    [data-testid="stSidebar"] .element-container:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        # Header with gradient background - starts at top
        st.markdown("""
        <div class="sidebar-header" style="margin-top: -1rem;">
            <div class="sidebar-header-content">
                <div class="sidebar-icon">🏛️</div>
                <div>
                    <p class="sidebar-title">Citizen Portal</p>
                    <p class="sidebar-subtitle">Your Voice Matters</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add spacing
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)

        # Determine default selection
        # CRITICAL: Use stored menu_selection when on submit page to prevent unwanted navigation
        is_on_submit_page = st.session_state.get('current_page') == 'submit'
        is_in_submission = st.session_state.get('submission_in_progress', False)

        # Hard lock the sidebar ONLY during actual submission (not after success)
        if is_on_submit_page and is_in_submission:
            st.session_state.menu_selection = "Submit Feedback"
            st.session_state.menu_index = 1
            st.session_state.menu_changed = False
            st.session_state.current_page = "submit"
            st.markdown("<div style='padding:8px 12px; border-radius:8px; background:#f5f3ff; border:1px solid #e4e0ff; color:#4b5563; font-size:13px;'>Navigation is locked while your submission is processing.</div>", unsafe_allow_html=True)
            return "📝 Submit Feedback"

        if st.session_state.get('stay_on_page'):
            default_idx = 1
        else:
            default_idx = st.session_state.get('menu_index', 0)

        # Main Navigation Menu
        selected = option_menu(
            menu_title=None,
            options=["Home", "Submit Feedback", "Track Status", "Announcements", "Help & FAQs"],
            icons=["house-door", "pencil-square", "search", "bell", "question-circle"],
            default_index=default_idx,
            key="navbar_menu",
            styles={
                "container": {
                    "padding": "10px 15px",
                    "background-color": "transparent",
                },
                "icon": {
                    "color": "#7c3aed",
                    "font-size": "18px",
                },
                "nav-link": {
                    "font-family": "'Inter', sans-serif",
                    "font-size": "15px",
                    "font-weight": "500",
                    "color": "#4b5563",
                    "padding": "12px 16px",
                    "margin": "4px 0",
                    "border-radius": "12px",
                    "background": "#ffffff",
                    "border": "1px solid #f0f0f5",
                    "box-shadow": "0 1px 3px rgba(0,0,0,0.04)",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #ede9fe 0%, #f3e8ff 100%)",
                    "color": "#7c3aed",
                    "font-weight": "600",
                    "border": "1px solid #c4b5fd",
                    "box-shadow": "0 4px 12px rgba(124, 58, 237, 0.15)",
                },
            },
        )
        
    # Check if menu selection actually changed by comparing with stored selection
        current_selection = selected
        stored_selection = st.session_state.get('menu_selection', "Home")
        
        # CRITICAL: When on submit page during submission, IGNORE menu selection change
        # This prevents the option_menu from triggering unwanted navigation
        is_on_submit_page = st.session_state.get('current_page') == 'submit'
        # Only treat as submission while the form is actively processing
        is_in_submission = st.session_state.get('submission_in_progress', False)
        
        if is_on_submit_page and is_in_submission and current_selection != "Submit Feedback":
            # We're on submit page, but option_menu is showing a different selection
            # This is the menu widget's internal state bug - IGNORE it
            # Keep the stored selection and don't update anything
            st.session_state.menu_changed = False
        elif current_selection != stored_selection and not st.session_state.get('nav_to'):
            # Normal menu change detection
            st.session_state.menu_changed = True
        else:
            st.session_state.menu_changed = False
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <p style="font-family: 'Inter', sans-serif; font-size: 12px; color: #9ca3af; margin: 0;">
                © 2024 City Gov · <span style="color: #7c3aed; font-weight: 600;">311</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Map selection to page names
    page_mapping = {
        "Home": "🏠 Home",
        "Submit Feedback": "📝 Submit Feedback",
        "Track Status": "🔍 Track My Feedback",
        "Announcements": "📢 Public Announcements",
        "Help & FAQs": "❓ Help & FAQs"
    }
    
    # Check if navigation was triggered from home page buttons FIRST
    # Process nav_to BEFORE menu_changed to avoid interference
    # BUT: Don't process navigation if we just submitted a form successfully
    if 'nav_to' in st.session_state and st.session_state.nav_to and not st.session_state.get('stay_on_page', False):
        nav_target = st.session_state.nav_to
        st.session_state.nav_to = None  # Clear the navigation trigger
        st.session_state.menu_changed = False  # Clear any pending menu_changed flag
        
        # Clear any stale submit state so we don't re-show old success messages
        st.session_state.stay_on_page = False
        st.session_state.success_shown = False
        st.session_state.submission_in_progress = False
        st.session_state.last_tracking_id = None
        st.session_state.last_email = None
        st.session_state.n8n_success = False

        # Align menu selection/index with target so next rerun keeps the correct page
        if nav_target == "home":
            st.session_state.menu_selection = "Home"
            st.session_state.menu_index = 0
        elif nav_target == "submit":
            st.session_state.menu_selection = "Submit Feedback"
            st.session_state.menu_index = 1
        elif nav_target == "track":
            st.session_state.menu_selection = "Track Status"
            st.session_state.menu_index = 2
        elif nav_target == "announce":
            st.session_state.menu_selection = "Announcements"
            st.session_state.menu_index = 3
        
        # Map nav_to values to page names
        nav_mapping = {
            "home": "🏠 Home",
            "submit": "📝 Submit Feedback",
            "track": "🔍 Track My Feedback",
            "announce": "📢 Public Announcements"
        }
        
        if nav_target in nav_mapping:
            return nav_mapping[nav_target]
    
    # Check if menu selection changed - reset stay_on_page flag ONLY when user manually navigates to a different page
    # Don't clear it if they're still on the Submit Feedback page viewing the success message
    # Also skip this check if nav_to was just processed (which returned above)
    if st.session_state.get('menu_changed'):
        st.session_state.menu_changed = False
        
        # Allow manual navigation after success; only lock during active submission
        stored_selection = st.session_state.get('menu_selection', "Home")
        if not st.session_state.get('submission_in_progress', False):
            st.session_state.stay_on_page = False
            st.session_state.last_tracking_id = None
            st.session_state.last_email = None
            st.session_state.n8n_success = False
            st.session_state.success_shown = False
    
    # Update session state - save the selection and index
    # CRITICAL: Don't update if we're ignoring the menu change during submission
    is_on_submit_page = st.session_state.get('current_page') == 'submit'
    # Consider only actual submission activity as locked state
    is_in_submission = st.session_state.get('submission_in_progress', False)
    
    if not (is_on_submit_page and is_in_submission and selected != "Submit Feedback"):
        # Only update if not in the ignored state
        st.session_state.menu_selection = selected
    
    options_list = ["Home", "Submit Feedback", "Track Status", "Announcements", "Help & FAQs"]
    try:
        st.session_state.menu_index = options_list.index(st.session_state.menu_selection)
    except ValueError:
        st.session_state.menu_index = 0
    
    key_mapping = {
        "Home": "home",
        "Submit Feedback": "submit",
        "Track Status": "track",
        "Announcements": "announcements",
        "Help & FAQs": "favorites"
    }
    # CRITICAL: Use stored menu_selection for page rendering, not option_menu's selected value
    # This prevents option_menu's widget state from causing unwanted navigation
    st.session_state.current_page = key_mapping.get(st.session_state.menu_selection, "home")
    
    # Return page based on stored menu_selection, not option_menu's selected value
    return page_mapping.get(st.session_state.menu_selection, "🏠 Home")


def render_home_page():
    """Render home page with premium design."""
    # Hero Section - No top margin
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(99, 102, 241, 0.1) 100%);
                border-radius: 24px; padding: 2.5rem; margin-top: 0; margin-bottom: 2rem; text-align: center;
                border: 1px solid rgba(59, 130, 246, 0.2); position: relative; overflow: hidden;">
        <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
                    background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
                    animation: pulse 4s ease-in-out infinite;"></div>
        <h1 style="font-family: 'Poppins', sans-serif; font-size: 2.8rem; font-weight: 800;
                   background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 50%, #818cf8 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   margin: 0 0 1rem 0; position: relative; z-index: 1;">
            🏛️ Welcome to Citizen Feedback Portal
        </h1>
        <p style="font-family: 'Inter', sans-serif; font-size: 1.2rem; color: rgba(148, 163, 184, 0.95);
                  margin: 0; max-width: 600px; margin: 0 auto; position: relative; z-index: 1;">
            Your voice shapes our community. Share feedback, report issues, or suggest improvements.
        </p>
    </div>
    <style>
        @keyframes pulse {
            0%, 100% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.05); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Quick action cards with premium glassmorphism
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="citizen-card" style="text-align: center; min-height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
            <h3 style="margin-bottom: 0.75rem;">Submit Feedback</h3>
            <p style="font-size: 0.95rem; line-height: 1.5;">
                Report issues, share concerns, or suggest improvements for your community.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Submit Now →", key="home_submit", use_container_width=True):
            st.session_state.nav_to = "submit"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="citizen-card" style="text-align: center; min-height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="margin-bottom: 0.75rem;">Track Status</h3>
            <p style="font-size: 0.95rem; line-height: 1.5;">
                Check the status of your previously submitted feedback and get updates.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Track Now →", key="home_track", use_container_width=True):
            st.session_state.nav_to = "track"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="citizen-card" style="text-align: center; min-height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📢</div>
            <h3 style="margin-bottom: 0.75rem;">Announcements</h3>
            <p style="font-size: 0.95rem; line-height: 1.5;">
                View public updates, resolved issues, and community improvements.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Updates →", key="home_announce", use_container_width=True):
            st.session_state.nav_to = "announce"
            st.rerun()
    
    st.divider()
    
    # Premium Statistics Section with enhanced cards
    st.markdown("""
    <h2 style="font-family: 'Poppins', sans-serif; font-weight: 700; color: #1f2937;
               text-align: center; margin-bottom: 2rem;">
        📊 Community Impact Dashboard
    </h2>
    """, unsafe_allow_html=True)

    df = st.session_state.data_manager.get_feedback_dataframe()

    if df.empty:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(99, 102, 241, 0.05) 100%);
                    border-radius: 20px; padding: 3rem; text-align: center; margin: 2rem 0;
                    border: 2px solid rgba(59, 130, 246, 0.2);">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">📭</div>
            <h3 style="color: #3b82f6; margin-bottom: 1rem;">Welcome to the Citizen Feedback Portal!</h3>
            <p style="color: rgba(107, 114, 128, 0.9); font-size: 1.1rem; max-width: 500px; margin: 0 auto;">
                Be the first to share your feedback and help improve our community.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        total = len(df)
        resolved = len(df[df['status'] == 'Resolved']) if 'status' in df else 0
        in_progress = len(df[df['status'] == 'In Progress']) if 'status' in df else 0
        new_feedback = len(df[df['status'] == 'New']) if 'status' in df else 0

        # Calculate additional metrics
        resolution_rate = (resolved / total * 100) if total > 0 else 0
        avg_response_time = "2.3 days"  # This could be calculated from actual data
        citizen_satisfaction = "87%"  # This could be calculated from sentiment data

        # Enhanced metrics grid
        col1, col2, col3, col4 = st.columns(4)

        metrics_data = [
            {
                "icon": "📬",
                "title": "Total Submissions",
                "value": total,
                "subtitle": "Community voices heard",
                "color": "#3b82f6",
                "bg": "rgba(59, 130, 246, 0.1)",
                "trend": "+12% this month"
            },
            {
                "icon": "✅",
                "title": "Issues Resolved",
                "value": resolved,
                "subtitle": f"{resolution_rate:.0f}% resolution rate",
                "color": "#10b981",
                "bg": "rgba(16, 185, 129, 0.1)",
                "trend": "+8% this month"
            },
            {
                "icon": "🔄",
                "title": "In Progress",
                "value": in_progress,
                "subtitle": "Being addressed",
                "color": "#f59e0b",
                "bg": "rgba(245, 158, 11, 0.1)",
                "trend": f"{new_feedback} new today"
            },
            {
                "icon": "🎯",
                "title": "Avg Response Time",
                "value": avg_response_time,
                "subtitle": "Quick resolution",
                "color": "#8b5cf6",
                "bg": "rgba(139, 92, 246, 0.1)",
                "trend": "Target: < 3 days"
            }
        ]

        for col, metric in zip([col1, col2, col3, col4], metrics_data):
            with col:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {metric['bg']} 0%, rgba(255,255,255,0.9) 100%);
                            border: 1px solid {metric['color']}30; border-radius: 16px; padding: 1.5rem;
                            text-align: center; margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                            transition: transform 0.2s ease; cursor: pointer;"
                            onmouseover="this.style.transform='translateY(-2px)'"
                            onmouseout="this.style.transform='translateY(0)'">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">{metric['icon']}</div>
                    <div style="font-size: 2rem; font-weight: 800; color: {metric['color']};
                               font-family: 'Poppins', sans-serif; margin-bottom: 0.5rem;">
                        {metric['value']}
                    </div>
                    <div style="font-size: 0.9rem; color: #374151; font-weight: 600; margin-bottom: 0.5rem;">
                        {metric['title']}
                    </div>
                    <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 0.5rem;">
                        {metric['subtitle']}
                    </div>
                    <div style="font-size: 0.75rem; color: {metric['color']}; font-weight: 600;">
                        {metric['trend']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Recent activity section
        st.markdown("""
        <h3 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #1f2937;
                   margin: 2rem 0 1rem 0; text-align: center;">
            🔥 Recent Activity
        </h3>
        """, unsafe_allow_html=True)

        # Recent submissions and resolutions
        col_recent1, col_recent2 = st.columns(2)

        with col_recent1:
            st.markdown("**🆕 Latest Submissions**")
            recent_subs = df.sort_values('timestamp', ascending=False).head(3) if 'timestamp' in df else pd.DataFrame()

            if not recent_subs.empty:
                for _, row in recent_subs.iterrows():
                    status_emoji = {"New": "🆕", "In Review": "👀", "In Progress": "🔄", "Resolved": "✅"}.get(row.get('status', 'New'), "📋")
                    st.markdown(f"""
                    <div style="background: #f8fafc; border-radius: 8px; padding: 0.75rem; margin: 0.5rem 0;
                               border-left: 3px solid #3b82f6;">
                        <div style="font-weight: 600; color: #1f2937; font-size: 0.9rem;">{row.get('title', 'Untitled')}</div>
                        <div style="color: #6b7280; font-size: 0.8rem;">
                            {status_emoji} {row.get('category', 'N/A')} • {row.get('timestamp', 'N/A')[:10] if row.get('timestamp') else 'N/A'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recent submissions")

        with col_recent2:
            st.markdown("**✅ Recently Resolved**")
            resolved_recent = df[df['status'] == 'Resolved'].sort_values('updated_at', ascending=False).head(3) if 'status' in df and 'updated_at' in df else pd.DataFrame()

            if not resolved_recent.empty:
                for _, row in resolved_recent.iterrows():
                    st.markdown(f"""
                    <div style="background: #f0fdf4; border-radius: 8px; padding: 0.75rem; margin: 0.5rem 0;
                               border-left: 3px solid #10b981;">
                        <div style="font-weight: 600; color: #065f46; font-size: 0.9rem;">✅ {row.get('title', 'Untitled')}</div>
                        <div style="color: #6b7280; font-size: 0.8rem;">
                            {row.get('category', 'N/A')} • Resolved {row.get('updated_at', 'N/A')[:10] if row.get('updated_at') else 'N/A'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recently resolved issues")
    
    # # Quick Actions Section
    # st.markdown("""
    # <h3 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #1f2937;
    #            text-align: center; margin: 2rem 0 1rem 0;">
    #     ⚡ Quick Actions
    # </h3>
    # """, unsafe_allow_html=True)
    
    # # Quick action buttons in a grid
    # col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    
    # with col_q1:
    #     st.markdown("""
    #     <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    #                 border-radius: 12px; padding: 1.5rem; text-align: center; margin-bottom: 1rem;
    #                 border: 1px solid #93c5fd; cursor: pointer; transition: all 0.2s ease;"
    #                 onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(59, 130, 246, 0.3)'"
    #                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(59, 130, 246, 0.2)'">
    #         <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
    #         <div style="font-weight: 600; color: #1e40af;">Submit Feedback</div>
    #         <div style="font-size: 0.8rem; color: #3730a3; margin-top: 0.25rem;">Share your concerns</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    #     if st.button("Submit Now", key="quick_submit", use_container_width=True):
    #         st.session_state.nav_to = "submit"
    #         st.rerun()
    
    # with col_q2:
    #     st.markdown("""
    #     <div style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
    #                 border-radius: 12px; padding: 1.5rem; text-align: center; margin-bottom: 1rem;
    #                 border: 1px solid #86efac; cursor: pointer; transition: all 0.2s ease;"
    #                 onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(34, 197, 94, 0.3)'"
    #                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(34, 197, 94, 0.2)'">
    #         <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
    #         <div style="font-weight: 600; color: #166534;">Track Status</div>
    #         <div style="font-size: 0.8rem; color: #14532d; margin-top: 0.25rem;">Check your submissions</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    #     if st.button("Track Now", key="quick_track", use_container_width=True):
    #         st.session_state.nav_to = "track"
    #         st.rerun()
    
    # with col_q3:
    #     st.markdown("""
    #     <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    #                 border-radius: 12px; padding: 1.5rem; text-align: center; margin-bottom: 1rem;
    #                 border: 1px solid #fcd34d; cursor: pointer; transition: all 0.2s ease;"
    #                 onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(245, 158, 11, 0.3)'"
    #                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(245, 158, 11, 0.2)'">
    #         <div style="font-size: 2rem; margin-bottom: 0.5rem;">📢</div>
    #         <div style="font-weight: 600; color: #92400e;">Announcements</div>
    #         <div style="font-size: 0.8rem; color: #78350f; margin-top: 0.25rem;">View updates</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    #     if st.button("View Updates", key="quick_announce", use_container_width=True):
    #         st.session_state.nav_to = "announce"
    #         st.rerun()
    
    # with col_q4:
    #     st.markdown("""
    #     <div style="background: linear-gradient(135deg, #e9d5ff 0%, #d8b4fe 100%);
    #                 border-radius: 12px; padding: 1.5rem; text-align: center; margin-bottom: 1rem;
    #                 border: 1px solid #c4b5fd; cursor: pointer; transition: all 0.2s ease;"
    #                 onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(139, 92, 246, 0.3)'"
    #                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(139, 92, 246, 0.2)'">
    #         <div style="font-size: 2rem; margin-bottom: 0.5rem;">❓</div>
    #         <div style="font-weight: 600; color: #6b21a8;">Help & FAQ</div>
    #         <div style="font-size: 0.8rem; color: #581c87; margin-top: 0.25rem;">Get assistance</div>
    #     </div>
    #     """, unsafe_allow_html=True)
    #     if st.button("Get Help", key="quick_help", use_container_width=True):
    #         st.session_state.nav_to = "help"
    #         st.rerun()
    
    # Recent resolved issues (public)
    st.divider()
    st.markdown("""
    <h3 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #34d399; 
               margin-bottom: 1rem;">
        ✅ Recently Resolved Issues
    </h3>
    """, unsafe_allow_html=True)
    
    if not df.empty and 'status' in df.columns:
        resolved_df = df[df['status'] == 'Resolved'].head(5)
        if not resolved_df.empty:
            for _, row in resolved_df.iterrows():
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.08); border-radius: 12px; padding: 1rem;
                            border-left: 4px solid #10b981; margin-bottom: 0.75rem;
                            border: 1px solid rgba(16, 185, 129, 0.2);">
                    <strong style="color: #34d399;">✅ {row.get('title', 'Untitled')}</strong><br>
                    <small style="color: rgba(148, 163, 184, 0.8);">
                        Category: {row.get('category', 'N/A')} |
                        Location: {row.get('location', 'N/A')} |
                        Resolved: {row.get('updated_at', row.get('timestamp', 'N/A'))[:10] if row.get('updated_at') or row.get('timestamp') else 'N/A'}
                    </small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🎉 No resolved issues to display yet. Be the first to submit feedback!")
    else:
        st.info("📭 No feedback data available yet. Be the first to submit!")


def render_submit_page():
    """Render feedback submission page for citizens."""
    # IMPORTANT: Reset submission_in_progress flag when arriving at this page
    # This ensures the form is never stuck in a "submission in progress" state
    # after navigating away and coming back
    if st.session_state.get('submission_in_progress', False):
        print("[feedback] RESET: submission_in_progress flag was True, resetting to False")
        st.session_state.submission_in_progress = False
    
    st.markdown('<p class="main-header">📝 Submit Your Feedback</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Help us improve by sharing your concerns, suggestions, or compliments.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("citizen_feedback_form", clear_on_submit=True):
            st.subheader("📋 Feedback Details")
            
            # Contact Information
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input(
                    "Your Name *",
                    placeholder="John Doe",
                    key="citizen_name",
                    autocomplete="name"
                )
            with col_b:
                email = st.text_input(
                    "Email *",
                    placeholder="john@example.com",
                    help="Required for tracking your submission",
                    key="citizen_email",
                    autocomplete="email"
                )
            
            phone = st.text_input(
                "Phone (Optional)",
                placeholder="+1 234 567 8900",
                key="citizen_phone",
                autocomplete="tel"
            )
            
            st.divider()
            
            # Feedback Type
            feedback_type = st.radio(
                "Type of Feedback",
                ["🚨 Report an Issue", "💡 Suggestion", "👍 Compliment", "❓ Question"],
                horizontal=True
            )
            
            # Category Selection
            category = st.selectbox(
                "Category *",
                [
                    "🏗️ Roads & Infrastructure",
                    "🚌 Public Transportation",
                    "💡 Street Lighting",
                    "🗑️ Waste Management",
                    "🌳 Parks & Recreation",
                    "💧 Water & Sewage",
                    "🏥 Healthcare Services",
                    "📚 Education & Schools",
                    "🛡️ Public Safety",
                    "🏢 Government Services",
                    "🔊 Noise Complaints",
                    "🏠 Housing",
                    "📱 Other"
                ]
            )
            
            # Urgency
            urgency = st.select_slider(
                "How urgent is this?",
                options=["Low", "Medium", "High", "Emergency"],
                value="Medium"
            )
            
            # Location
            st.subheader("📍 Location Details")
            col_loc1, col_loc2 = st.columns(2)
            with col_loc1:
                area = st.text_input(
                    "Neighborhood/Area *",
                    placeholder="Downtown",
                    key="citizen_area",
                    autocomplete="address-level2"
                )
            with col_loc2:
                address = st.text_input(
                    "Street Address (Optional)",
                    placeholder="123 Main St",
                    key="citizen_address",
                    autocomplete="address-line1"
                )
            
            # Feedback Content
            st.subheader("📝 Your Feedback")
            title = st.text_input(
                "Brief Title *",
                placeholder="Pothole on Main Street",
                key="feedback_title",
                autocomplete="on"
            )
            
            feedback_text = st.text_area(
                "Detailed Description *",
                placeholder="Please describe the issue in detail. Include what you observed, when it happened, and any other relevant information...",
                height=150,
                key="feedback_text"
            )
            
            # Optional photo upload placeholder
            st.file_uploader("Attach Photos (Optional)", type=['jpg', 'jpeg', 'png'], 
                           accept_multiple_files=True,
                           help="Upload photos to help us understand the issue better")
            
            # Consent
            consent = st.checkbox("I agree to the terms and allow the city to contact me regarding this feedback")
            
            # Submit
            submitted = st.form_submit_button("🚀 Submit Feedback", type="primary", use_container_width=True)
            
            if submitted:
                # Set flag to prevent menu navigation from interfering with submission
                st.session_state.submission_in_progress = True
                
                # Clear any pending navigation to prevent interference with form submission
                st.session_state.nav_to = None
                
                # Immediate user feedback and debug logging
                st.toast("Submitting your feedback...", icon="✅")
                
                # Validation
                if not name or not email or not title or not feedback_text or not area:
                    st.session_state.submission_in_progress = False
                    st.error("⚠️ Please fill in all required fields (marked with *)")
                elif not consent:
                    st.session_state.submission_in_progress = False
                    st.error("⚠️ Please agree to the terms to submit your feedback")
                else:
                    try:
                        # AI Analysis
                        analysis = st.session_state.analyzer.analyze(feedback_text)
                        
                        # AI-powered comprehensive analysis
                        feedback_dict = {
                            'feedback': feedback_text,
                            'id': None,  # Will be set after ID generation
                            'urgency': urgency,
                            'category': category,
                            'area': area
                        }
                        ai_analysis = st.session_state.data_manager.analyze_feedback_with_ai(feedback_dict)
                        
                        # Generate tracking ID
                        tracking_id = st.session_state.data_manager.generate_id()
                        
                        # Create feedback entry (using both formats for compatibility)
                        feedback_entry = {
                            # Primary fields (for internal use)
                            "id": tracking_id,
                            "timestamp": datetime.now().isoformat(),
                            "name": name,
                            "email": email,
                            "phone": phone if phone else "N/A",
                            
                            # n8n-compatible field names
                            "feedback_id": tracking_id,
                            "citizen_name": name,
                            "citizen_email": email,
                            "citizen_phone": phone if phone else "N/A",
                            
                            # Common fields
                            "feedback_type": feedback_type,
                            "category": category,
                            "urgency": urgency,
                            "area": area,
                            "address": address if address else "Not specified",
                            "location": f"{area}, {address}" if address else area,
                            "title": title,
                            "feedback": feedback_text,
                            "sentiment": analysis["sentiment"],
                            "sentiment_score": analysis["sentiment_score"],
                            "keywords": analysis["keywords"],
                            "summary": analysis["summary"],
                            "status": "New",
                            "admin_notes": "",
                            "assigned_to": "",
                            "priority": "Normal",
                            
                            # AI Analysis Results
                            "ai_sentiment": ai_analysis.get('analyses', {}).get('nlp', {}).get('sentiment', 'Neutral') if isinstance(ai_analysis.get('analyses', {}).get('nlp', {}).get('sentiment'), str) else ai_analysis.get('analyses', {}).get('nlp', {}).get('sentiment', {}).get('sentiment', 'Neutral'),
                            "ai_sentiment_score": ai_analysis.get('analyses', {}).get('nlp', {}).get('sentiment_score'),
                            "ai_confidence": ai_analysis.get('analyses', {}).get('nlp', {}).get('confidence'),
                            "ai_priority": ai_analysis.get('recommendations', {}).get('priority_level'),
                            "ai_category": ai_analysis.get('analyses', {}).get('nlp', {}).get('category'),
                            "ai_summary": ai_analysis.get('analyses', {}).get('nlp', {}).get('summary'),
                            "ai_keywords": ai_analysis.get('analyses', {}).get('nlp', {}).get('keywords', [])
                        }
                        
                        # Store analysis for display
                        st.session_state.last_analysis = {
                            'sentiment': ai_analysis.get('analyses', {}).get('nlp', {}).get('sentiment', 'Neutral') if isinstance(ai_analysis.get('analyses', {}).get('nlp', {}).get('sentiment'), str) else ai_analysis.get('analyses', {}).get('nlp', {}).get('sentiment', {}).get('sentiment', 'Neutral'),
                            'priority': ai_analysis.get('recommendations', {}).get('priority_level'),
                            'category': ai_analysis.get('analyses', {}).get('nlp', {}).get('category'),
                            'confidence': ai_analysis.get('analyses', {}).get('nlp', {}).get('confidence'),
                            'summary': ai_analysis.get('analyses', {}).get('nlp', {}).get('summary'),
                            'keywords': ai_analysis.get('analyses', {}).get('nlp', {}).get('keywords', [])
                        }
                        
                        # Save
                        st.session_state.data_manager.add_feedback(feedback_entry)
                        st.session_state.submitted_ids.append(tracking_id)
                        
                        # Set flag to stay on this page and preserve menu selection
                        st.session_state.stay_on_page = True
                        st.session_state.success_shown = False  # Reset success_shown flag for proper display
                        st.session_state.menu_selection = "Submit Feedback"
                        st.session_state.menu_index = 1
                        st.session_state.last_tracking_id = tracking_id
                        st.session_state.last_email = email
                        
                        # Send to n8n (if configured) - with better error handling
                        try:
                            n8n_success = send_feedback_submitted(feedback_entry)
                            st.session_state.n8n_success = n8n_success
                        except Exception as e:
                            st.session_state.n8n_success = False
                        finally:
                            # Always mark submission as complete
                            st.session_state.submission_in_progress = False
                        
                        # Force rerun to display success message
                        st.rerun()
                    except Exception as e:
                        st.session_state.stay_on_page = False
                        st.session_state.submission_in_progress = False
                        st.error("❌ Submission failed. Please try again.")
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>ℹ️ Submission Tips</h4>
            <ul>
                <li>Be specific about the location</li>
                <li>Describe the issue clearly</li>
                <li>Include photos if possible</li>
                <li>Provide accurate contact info</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="margin-top: 1rem;">
            <h4>⏱️ Response Times</h4>
            <ul>
                <li><strong>Emergency:</strong> 24 hours</li>
                <li><strong>High:</strong> 3-5 days</li>
                <li><strong>Medium:</strong> 1-2 weeks</li>
                <li><strong>Low:</strong> 2-4 weeks</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box" style="margin-top: 1rem;">
            <h4>📞 Emergency?</h4>
            <p>For life-threatening emergencies, please call <strong>911</strong> immediately.</p>
            <p>For urgent city services, call <strong>311</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show success message below the form if just submitted
    if st.session_state.get('stay_on_page', False):
        st.divider()
        # Show celebration only once per successful submission
        if not st.session_state.get('success_shown', False):
            st.balloons()
            st.session_state.success_shown = True
        st.success(f"""
        ✅ **Feedback Submitted Successfully!**
        
        📋 **Your Tracking ID:** `{st.session_state.get('last_tracking_id', 'N/A')}`
        
        Save this ID to track your submission status. 
        We'll also send updates to: {st.session_state.get('last_email', 'your email')}
        
        **Note:** Please check your spam/junk folder for the confirmation email. 
        It may take a few minutes to arrive.
        """)
        
        # Show n8n webhook status
        if st.session_state.get('n8n_success', False):
            st.success("✅ Webhook notification sent to n8n workflow!")
        else:
            st.info("ℹ️ Note: Webhook notification could not be sent. Your feedback has been saved locally. Check terminal logs for details.")
        
        # Display AI Analysis Results
        if st.session_state.get('last_analysis'):
            st.markdown("### 🤖 AI Analysis Results")
            
            analysis = st.session_state.last_analysis
            col_ai1, col_ai2, col_ai3 = st.columns(3)
            
            with col_ai1:
                sentiment = analysis.get('sentiment', 'N/A')
                sentiment_color = {'Positive': '🟢', 'Negative': '🔴', 'Neutral': '🟡'}.get(sentiment, '⚪')
                st.metric("Sentiment", f"{sentiment_color} {sentiment}")
            
            with col_ai2:
                priority = analysis.get('priority', 'Medium')
                priority_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}.get(priority, '⚪')
                st.metric("Priority", f"{priority_color} {priority}")
            
            with col_ai3:
                category = analysis.get('category', 'General')
                st.metric("Category", f"📁 {category}")
            
            # Show confidence if available
            if 'confidence' in analysis and analysis['confidence'] is not None:
                confidence_pct = int(analysis['confidence'] * 100)
                st.progress(confidence_pct / 100, text=f"AI Confidence: {confidence_pct}%")
            
            # Show summary if available
            if analysis.get('summary'):
                with st.expander("📝 AI Summary"):
                    st.write(analysis['summary'])
            
            # Show keywords if available
            if analysis.get('keywords') and analysis['keywords']:
                with st.expander("🏷️ Key Topics Detected"):
                    keywords_str = ", ".join(analysis['keywords'][:10])  # Show top 10
                    st.write(keywords_str)
        
        # Add buttons to navigate or submit another
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("📝 Submit Another Feedback", use_container_width=True, key="submit_another"):
                # Reset submission state for next form submission
                st.session_state.stay_on_page = False
                st.session_state.success_shown = False
                st.session_state.last_tracking_id = None
                st.session_state.last_email = None
                st.session_state.n8n_success = False
                st.rerun()
        
        with col_btn2:
            if st.button("🔍 Track Status", use_container_width=True, key="track_from_success"):
                # Clear success state before navigating
                st.session_state.stay_on_page = False
                st.session_state.success_shown = False
                st.session_state.last_tracking_id = None
                st.session_state.last_email = None
                st.session_state.n8n_success = False
                st.session_state.nav_to = "track"
                st.rerun()
        
        with col_btn3:
            if st.button("🏠 Back Home", use_container_width=True, key="home_from_success"):
                # Clear success state before navigating
                st.session_state.stay_on_page = False
                st.session_state.success_shown = False
                st.session_state.last_tracking_id = None
                st.session_state.last_email = None
                st.session_state.n8n_success = False
                st.session_state.nav_to = "home"
                st.rerun()


def render_track_page():
    """Render feedback tracking page."""
    st.markdown('<p class="main-header">🔍 Track Your Feedback</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Enter your tracking ID or email to check the status of your submissions.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        tracking_id = st.text_input("🔢 Tracking ID", placeholder="Enter your tracking ID (e.g., A1B2C3D4)")
    
    with col2:
        email = st.text_input("📧 Or Email Address", placeholder="Enter email used during submission")
    
    search_btn = st.button("🔍 Search", type="primary", use_container_width=True)
    
    st.divider()
    
    if search_btn or tracking_id or email:
        df = st.session_state.data_manager.get_feedback_dataframe()
        
        if df.empty:
            st.warning("No feedback records found.")
            return
        
        # Filter by tracking ID or email
        results = pd.DataFrame()
        
        if tracking_id:
            results = df[df['id'].str.upper() == tracking_id.upper()]
        elif email:
            results = df[df['email'].str.lower() == email.lower()]
        
        if results.empty:
            st.warning("❌ No matching submissions found. Please check your tracking ID or email.")
            st.info("💡 Tip: The tracking ID was provided when you submitted your feedback.")
        else:
            st.success(f"✅ Found {len(results)} submission(s)")

            for _, row in results.iterrows():
                # Enhanced status styling with better colors and icons
                status_colors = {
                    "New": ("🆕", "#dbeafe", "#1e40af", "#3b82f6"),
                    "In Review": ("👀", "#e9d5ff", "#6b21a8", "#8b5cf6"),
                    "In Progress": ("🔄", "#fef3c7", "#92400e", "#f59e0b"),
                    "Resolved": ("✅", "#d1fae5", "#065f46", "#10b981"),
                    "Closed": ("📁", "#f3f4f6", "#374151", "#6b7280")
                }

                status = row.get('status', 'New')
                emoji, bg_color, text_color, accent_color = status_colors.get(status, ("📋", "#f3f4f6", "#374151", "#6b7280"))

                # Priority indicator
                urgency = row.get('urgency', 'Medium')
                priority_colors = {
                    "Emergency": ("🚨", "#dc2626", "EMERGENCY"),
                    "High": ("⚠️", "#f59e0b", "HIGH PRIORITY"),
                    "Medium": ("📋", "#6b7280", "MEDIUM"),
                    "Low": ("✅", "#10b981", "LOW")
                }
                pri_emoji, pri_color, pri_text = priority_colors.get(urgency, ("📋", "#6b7280", "MEDIUM"))

                # Main feedback card with improved design
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {bg_color} 0%, rgba(255,255,255,0.9) 100%);
                            border: 2px solid {accent_color}30; border-radius: 16px; padding: 2rem; margin: 1.5rem 0;
                            box-shadow: 0 4px 20px rgba(0,0,0,0.08); position: relative; overflow: hidden;">
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: {accent_color};"></div>

                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">
                        <div>
                            <h3 style="color: {text_color}; margin: 0 0 0.5rem 0; font-size: 1.4rem; font-weight: 700;">
                                {emoji} {row.get('title', 'Untitled')}
                            </h3>
                            <div style="display: flex; gap: 1rem; align-items: center;">
                                <span style="background: {accent_color}20; color: {accent_color}; padding: 0.3rem 0.8rem;
                                           border-radius: 20px; font-weight: 600; font-size: 0.85rem;">
                                    Tracking ID: {row.get('id', 'N/A')}
                                </span>
                                <span style="background: {pri_color}20; color: {pri_color}; padding: 0.3rem 0.8rem;
                                           border-radius: 20px; font-weight: 600; font-size: 0.85rem;">
                                    {pri_emoji} {pri_text}
                                </span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji}</div>
                            <div style="background: {bg_color}; color: {text_color}; padding: 0.5rem 1rem;
                                       border-radius: 25px; font-weight: 700; border: 2px solid {accent_color}40;">
                                {status.upper()}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Information grid with better layout
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**📋 Submission Details**")
                    with st.container():
                        st.markdown(f"""
                        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 3px solid {accent_color};">
                            <div style="margin-bottom: 0.5rem;"><strong>Category:</strong> {row.get('category', 'N/A')}</div>
                            <div style="margin-bottom: 0.5rem;"><strong>Location:</strong> {row.get('location', 'N/A')}</div>
                            <div><strong>Submitted:</strong> {row.get('timestamp', 'N/A')[:10] if row.get('timestamp') else 'N/A'}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with col2:
                    st.markdown("**📊 Current Status**")
                    with st.container():
                        status_info = []
                        status_info.append(f"**Status:** {emoji} {status}")

                        if row.get('assigned_to'):
                            status_info.append(f"**Assigned To:** 👤 {row.get('assigned_to')}")

                        if row.get('updated_at'):
                            status_info.append(f"**Last Updated:** 📅 {row.get('updated_at')[:10]}")

                        # Progress indicator based on status
                        progress_map = {"New": 10, "In Review": 30, "In Progress": 70, "Resolved": 100, "Closed": 100}
                        progress = progress_map.get(status, 10)

                        st.markdown(f"""
                        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 3px solid {accent_color};">
                            {"<br>".join(status_info)}
                            <div style="margin-top: 1rem;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                    <span style="font-size: 0.9rem; color: #6b7280;">Progress</span>
                                    <span style="font-size: 0.9rem; color: {accent_color}; font-weight: 600;">{progress}%</span>
                                </div>
                                <div style="width: 100%; height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden;">
                                    <div style="width: {progress}%; height: 100%; background: {accent_color}; border-radius: 4px;"></div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                with col3:
                    st.markdown("**🤖 AI Analysis**")
                    with st.container():
                        sentiment = row.get('sentiment', 'N/A')
                        sentiment_emojis = {'Positive': '😊', 'Neutral': '😐', 'Negative': '😟'}
                        sentiment_emoji = sentiment_emojis.get(sentiment, '📝')

                        ai_info = []
                        ai_info.append(f"**Sentiment:** {sentiment_emoji} {sentiment}")

                        if row.get('ai_priority'):
                            priority_emojis = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                            pri_emoji = priority_emojis.get(row.get('ai_priority'), '⚪')
                            ai_info.append(f"**AI Priority:** {pri_emoji} {row.get('ai_priority')}")

                        if row.get('ai_confidence'):
                            conf_pct = int(float(row.get('ai_confidence', 0)) * 100)
                            ai_info.append(f"**Confidence:** {conf_pct}%")

                        st.markdown(f"""
                        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 3px solid {accent_color};">
                            {"<br>".join(ai_info)}
                        </div>
                        """, unsafe_allow_html=True)

                # Expandable sections for detailed content
                col_exp1, col_exp2 = st.columns(2)

                with col_exp1:
                    with st.expander("📝 View Full Feedback"):
                        st.write(row.get('feedback', 'No description provided'))

                with col_exp2:
                    if row.get('admin_notes'):
                        with st.expander("📋 Official Response"):
                            st.success(row['admin_notes'])
                    else:
                        with st.expander("📋 Official Response"):
                            st.info("No official response yet. We'll update you when there's news!")

                # AI Insights section if available
                if row.get('ai_summary') or (row.get('ai_keywords') and isinstance(row.get('ai_keywords'), list)):
                    with st.expander("🤖 AI Insights"):
                        if row.get('ai_summary'):
                            st.markdown("**AI Summary:**")
                            st.info(row['ai_summary'])

                        if row.get('ai_keywords') and isinstance(row['ai_keywords'], list) and row['ai_keywords']:
                            st.markdown("**Detected Topics:**")
                            topics_html = " ".join([f'<span style="background: #e0e7ff; color: #3730a3; padding: 3px 8px; border-radius: 12px; margin: 2px; display: inline-block; font-size: 0.8rem;">#{topic}</span>' for topic in row['ai_keywords'][:12]])
                            st.markdown(f'<div style="margin-top: 0.5rem;">{topics_html}</div>', unsafe_allow_html=True)

                st.markdown("---")
    
    # Show recent submissions if user has session history
    if st.session_state.submitted_ids:
        st.subheader("📋 Your Recent Submissions (This Session)")
        for tid in st.session_state.submitted_ids[-5:]:
            st.code(tid)


def render_announcements_page():
    """Render public announcements page."""
    st.markdown('<p class="main-header">📢 Public Announcements</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Stay updated with community improvements and resolved issues.</p>', unsafe_allow_html=True)
    
    df = st.session_state.data_manager.get_feedback_dataframe()
    
    # Filter tabs
    tab1, tab2, tab3 = st.tabs(["✅ Resolved Issues", "🔄 In Progress", "📊 Statistics"])
    
    with tab1:
        if not df.empty and 'status' in df.columns:
            resolved = df[df['status'] == 'Resolved'].sort_values('timestamp', ascending=False)
            
            if not resolved.empty:
                for _, row in resolved.head(10).iterrows():
                    st.markdown(f"""
                    <div class="citizen-card">
                        <h4>✅ {row.get('title', 'Untitled')}</h4>
                        <p><strong>Category:</strong> {row.get('category', 'N/A')} | 
                           <strong>Area:</strong> {row.get('location', 'N/A')}</p>
                        <p><em>{row.get('summary', 'Issue has been resolved.')}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No resolved issues to display yet.")
        else:
            st.info("No announcements available.")
    
    with tab2:
        if not df.empty and 'status' in df.columns:
            in_progress = df[df['status'] == 'In Progress'].sort_values('timestamp', ascending=False)
            
            if not in_progress.empty:
                for _, row in in_progress.head(10).iterrows():
                    st.markdown(f"""
                    <div style="background: #FEF3C7; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #F59E0B;">
                        <h4 style="margin: 0;">🔄 {row.get('title', 'Untitled')}</h4>
                        <p><strong>Category:</strong> {row.get('category', 'N/A')} | 
                           <strong>Area:</strong> {row.get('location', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No issues currently in progress.")
        else:
            st.info("No data available.")
    
    with tab3:
        if not df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📁 By Category")
                if 'category' in df.columns:
                    category_counts = df['category'].value_counts()
                    st.bar_chart(category_counts)
            
            with col2:
                st.subheader("📍 By Area")
                if 'area' in df.columns:
                    area_counts = df['area'].value_counts().head(10)
                    st.bar_chart(area_counts)
        else:
            st.info("No statistics available yet.")


def render_help_page():
    """Render help and FAQs page."""
    st.markdown('<p class="main-header">❓ Help & FAQs</p>', unsafe_allow_html=True)
    
    st.subheader("📖 Frequently Asked Questions")
    
    with st.expander("How do I submit feedback?"):
        st.write("""
        1. Click on "📝 Submit Feedback" in the sidebar
        2. Fill in your contact information
        3. Select the category that best matches your feedback
        4. Provide a clear title and detailed description
        5. Click "Submit Feedback"
        6. Save your tracking ID to check status later
        """)
    
    with st.expander("How can I track my submission?"):
        st.write("""
        1. Go to "🔍 Track My Feedback"
        2. Enter either your Tracking ID or email address
        3. Click "Search" to view your submission status
        """)
    
    with st.expander("What do the status labels mean?"):
        st.write("""
        - **🆕 New**: Your feedback has been received and is awaiting review
        - **👀 In Review**: An administrator is reviewing your feedback
        - **🔄 In Progress**: Work is being done to address your feedback
        - **✅ Resolved**: The issue has been addressed
        - **📁 Closed**: The feedback case has been closed
        """)
    
    with st.expander("How long does it take to get a response?"):
        st.write("""
        Response times depend on urgency:
        - **Emergency**: Within 24 hours
        - **High Priority**: 3-5 business days
        - **Medium Priority**: 1-2 weeks
        - **Low Priority**: 2-4 weeks
        """)
    
    with st.expander("What if I have an emergency?"):
        st.write("""
        **For life-threatening emergencies, call 911 immediately.**
        
        For urgent city services (water main breaks, dangerous road conditions, etc.), 
        please call 311 for immediate assistance.
        """)
    
    st.divider()
    
    st.subheader("📞 Contact Us")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📱 Phone**
        - Emergency: 911
        - City Services: 311
        - Office: (555) 123-4567
        """)
    
    with col2:
        st.markdown("""
        **📧 Email**
        - feedback@city.gov
        - support@city.gov
        """)
    
    with col3:
        st.markdown("""
        **🏢 Office Hours**
        - Mon-Fri: 8AM - 5PM
        - Sat: 9AM - 1PM
        - Sun: Closed
        """)


def main():
    """Main entry point for Citizen Portal."""
    init_session_state()
    page = render_sidebar()
    
    if page == "🏠 Home":
        render_home_page()
    elif page == "📝 Submit Feedback":
        render_submit_page()
    elif page == "🔍 Track My Feedback":
        render_track_page()
    elif page == "📢 Public Announcements":
        render_announcements_page()
    elif page == "❓ Help & FAQs":
        render_help_page()


if __name__ == "__main__":
    main()
