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

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 3rem;
    }
    .portal-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        border: 2px solid transparent;
        height: 100%;
    }
    .portal-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    }
    .citizen-card {
        border-color: #3B82F6;
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    }
    .admin-card {
        border-color: #6B7280;
        background: linear-gradient(135deg, #F9FAFB 0%, #E5E7EB 100%);
    }
    .portal-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .portal-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .portal-desc {
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .feature-list {
        text-align: left;
        padding-left: 1rem;
    }
    .command-box {
        background: #1F2937;
        color: #10B981;
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<p class="main-title">🏛️ Citizen Feedback AI Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Platform for Citizen Engagement & Government Services</p>', unsafe_allow_html=True)
    
    # Portal selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="portal-card citizen-card">
            <div class="portal-icon">👥</div>
            <div class="portal-title" style="color: #1E40AF;">Citizen Portal</div>
            <div class="portal-desc">For public citizens to submit and track feedback</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Features:**")
        st.markdown("""
        - ✅ Submit feedback & complaints
        - 🔍 Track submission status
        - 📢 View public announcements
        - ❓ Access help & FAQs
        """)
        
        st.markdown("**Run Command:**")
        st.code("streamlit run citizen_portal.py", language="bash")
        
        if st.button("🚀 Launch Citizen Portal", key="citizen", use_container_width=True, type="primary"):
            st.info("Run in terminal: `streamlit run citizen_portal.py`")
    
    with col2:
        st.markdown("""
        <div class="portal-card admin-card">
            <div class="portal-icon">⚙️</div>
            <div class="portal-title" style="color: #374151;">Admin Portal</div>
            <div class="portal-desc">For government officials to manage feedback</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Features:**")
        st.markdown("""
        - 📊 Analytics dashboard
        - 📋 Manage all feedback
        - 🚨 Priority queue
        - 👥 Staff assignments
        - 📤 Export reports
        """)
        
        st.markdown("**Run Command:**")
        st.code("streamlit run admin_portal.py", language="bash")
        
        if st.button("🔐 Launch Admin Portal", key="admin", use_container_width=True):
            st.info("Run in terminal: `streamlit run admin_portal.py`")
    
    st.divider()
    
    # Quick start guide
    st.subheader("🚀 Quick Start")
    
    st.markdown("""
    ### Option 1: Run Both Portals on Different Ports
    
    Open **two separate terminals** and run:
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Terminal 1 - Citizen Portal:**")
        st.code("streamlit run citizen_portal.py --server.port 8501", language="bash")
    with col2:
        st.markdown("**Terminal 2 - Admin Portal:**")
        st.code("streamlit run admin_portal.py --server.port 8502", language="bash")
    
    st.markdown("""
    ### Access URLs:
    - 👥 **Citizen Portal:** http://localhost:8501
    - ⚙️ **Admin Portal:** http://localhost:8502
    """)
    
    st.divider()
    
    # Architecture overview
    st.subheader("🏗️ System Architecture")
    
    st.markdown("""
    ```
    ┌─────────────────────────────────────────────────────────────────┐
    │                     CITIZEN FEEDBACK AI AGENT                    │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                  │
    │  ┌──────────────────────┐      ┌──────────────────────┐        │
    │  │   👥 CITIZEN PORTAL   │      │   ⚙️ ADMIN PORTAL     │        │
    │  │   (Public Website)    │      │   (Government Only)  │        │
    │  │                       │      │                       │        │
    │  │  • Submit Feedback    │      │  • Dashboard          │        │
    │  │  • Track Status       │      │  • Manage Feedback    │        │
    │  │  • View Updates       │      │  • Priority Queue     │        │
    │  │  • Help & FAQs        │      │  • Analytics          │        │
    │  └───────────┬───────────┘      └───────────┬───────────┘        │
    │              │                              │                    │
    │              └──────────────┬───────────────┘                    │
    │                             │                                    │
    │              ┌──────────────▼───────────────┐                    │
    │              │    🤖 AI ANALYSIS ENGINE      │                    │
    │              │   (Sentiment, Keywords, etc.) │                    │
    │              └──────────────┬───────────────┘                    │
    │                             │                                    │
    │              ┌──────────────▼───────────────┐                    │
    │              │    💾 SHARED DATA STORAGE     │                    │
    │              │      (data/feedback.json)     │                    │
    │              └──────────────────────────────┘                    │
    │                                                                  │
    └─────────────────────────────────────────────────────────────────┘
    ```
    """)
    
    st.divider()
    
    # Footer
    st.caption("© 2024 Citizen Feedback AI Agent | Built with ❤️ using Streamlit")


if __name__ == "__main__":
    main()
