"""
Citizen Feedback AI Agent - Main Launcher
Choose between Citizen Portal (Public) or Admin Portal (Government)
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Citizen Feedback AI Agent",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        padding-top: 3rem;
        max-width: 1200px;
    }
    
    .hero-section {
        background: linear-gradient(-45deg, #667eea, #764ba2, #6B8DD6, #8E37D7);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        border-radius: 24px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 50%, #e0e0e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: rgba(255,255,255,0.85);
        text-align: center;
        margin-bottom: 0;
        font-weight: 400;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
    }
    
    .portal-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .portal-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    .citizen-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(99, 102, 241, 0.15) 100%);
        border-color: rgba(59, 130, 246, 0.4);
    }
    
    .admin-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(168, 85, 247, 0.15) 100%);
        border-color: rgba(139, 92, 246, 0.4);
    }
    
    .portal-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .portal-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        color: #ffffff !important;
    }
    
    .portal-desc {
        font-family: 'Inter', sans-serif;
        color: rgba(255,255,255,0.8);
        margin-bottom: 1.5rem;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <p class="main-title">🏛️ Citizen Feedback AI Agent</p>
        <p class="subtitle">AI-Powered Platform for Citizen Engagement & Government Services</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Portal selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="portal-card citizen-card">
            <div class="portal-icon">👥</div>
            <div class="portal-title">Citizen Portal</div>
            <div class="portal-desc">Submit feedback, track your submissions, and stay updated with community improvements</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Citizen Portal", key="citizen", use_container_width=True, type="primary"):
            st.info("Run in terminal: `streamlit run citizen_portal.py`")
    
    with col2:
        st.markdown("""
        <div class="portal-card admin-card">
            <div class="portal-icon">⚙️</div>
            <div class="portal-title">Admin Portal</div>
            <div class="portal-desc">Powerful dashboard for government officials to manage and analyze citizen feedback</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔐 Launch Admin Portal", key="admin", use_container_width=True):
            st.info("Run in terminal: `streamlit run admin_portal.py`")


if __name__ == "__main__":
    main()
