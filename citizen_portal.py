"""
Citizen Portal - Public Website
For citizens to submit feedback, track their submissions, and view public updates.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from src.feedback_analyzer import FeedbackAnalyzer
from src.data_manager import DataManager

# Page configuration
st.set_page_config(
    page_title="Citizen Feedback Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Citizen Portal (Blue Theme)
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E40AF;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .citizen-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .status-new { background: #DBEAFE; color: #1E40AF; }
    .status-review { background: #E9D5FF; color: #6B21A8; }
    .status-progress { background: #FEF3C7; color: #92400E; }
    .status-resolved { background: #D1FAE5; color: #065F46; }
    .info-box {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-radius: 8px;
        padding: 1rem;
    }
    .stButton>button {
        background-color: #3B82F6;
        color: white;
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


def render_sidebar():
    """Render citizen sidebar."""
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/city-hall.png", width=80)
        st.title("🏛️ Citizen Portal")
        st.caption("Your Voice Matters!")
        
        st.divider()
        
        page = st.radio(
            "Navigate",
            [
                "🏠 Home",
                "📝 Submit Feedback",
                "🔍 Track My Feedback",
                "📢 Public Announcements",
                "❓ Help & FAQs"
            ],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Citizen identification (optional)
        st.subheader("🆔 Your Tracker ID")
        citizen_email = st.text_input(
            "Enter your email to track submissions",
            placeholder="your@email.com",
            label_visibility="collapsed"
        )
        if citizen_email:
            st.session_state.citizen_id = citizen_email
            st.success(f"Tracking: {citizen_email[:20]}...")
        
        st.divider()
        st.caption("© 2024 City Government")
        st.caption("Need help? Call: 311")
        
        return page


def render_home_page():
    """Render home page."""
    st.markdown('<p class="main-header">🏛️ Welcome to Citizen Feedback Portal</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your voice shapes our community. Share feedback, report issues, or suggest improvements.</p>', unsafe_allow_html=True)
    
    # Quick action cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="citizen-card">
            <h3>📝 Submit Feedback</h3>
            <p>Report issues, share concerns, or suggest improvements for your community.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Submit Now →", key="home_submit"):
            st.session_state.nav_to = "submit"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="citizen-card">
            <h3>🔍 Track Status</h3>
            <p>Check the status of your previously submitted feedback and get updates.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Track Now →", key="home_track"):
            st.session_state.nav_to = "track"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="citizen-card">
            <h3>📢 Announcements</h3>
            <p>View public updates, resolved issues, and community improvements.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Updates →", key="home_announce"):
            st.session_state.nav_to = "announce"
            st.rerun()
    
    st.divider()
    
    # Statistics
    st.subheader("📊 Community Impact")
    df = st.session_state.data_manager.get_feedback_dataframe()
    
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(df) if not df.empty else 0
    resolved = len(df[df['status'] == 'Resolved']) if not df.empty and 'status' in df else 0
    in_progress = len(df[df['status'] == 'In Progress']) if not df.empty and 'status' in df else 0
    
    with col1:
        st.metric("📬 Total Submissions", total)
    with col2:
        st.metric("✅ Issues Resolved", resolved)
    with col3:
        st.metric("🔄 In Progress", in_progress)
    with col4:
        resolution_rate = (resolved / total * 100) if total > 0 else 0
        st.metric("📈 Resolution Rate", f"{resolution_rate:.0f}%")
    
    # Recent resolved issues (public)
    st.divider()
    st.subheader("✅ Recently Resolved Issues")
    
    if not df.empty and 'status' in df.columns:
        resolved_df = df[df['status'] == 'Resolved'].head(5)
        if not resolved_df.empty:
            for _, row in resolved_df.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="info-box">
                        <strong>✅ {row.get('title', 'Untitled')}</strong><br>
                        <small>Category: {row.get('category', 'N/A')} | Resolved on: {row.get('updated_at', row.get('timestamp', 'N/A'))[:10] if row.get('updated_at') or row.get('timestamp') else 'N/A'}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No resolved issues to display yet.")
    else:
        st.info("No feedback data available yet. Be the first to submit!")


def render_submit_page():
    """Render feedback submission page for citizens."""
    st.markdown('<p class="main-header">📝 Submit Your Feedback</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Help us improve by sharing your concerns, suggestions, or compliments.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("citizen_feedback_form", clear_on_submit=True):
            st.subheader("📋 Feedback Details")
            
            # Contact Information
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Your Name *", placeholder="John Doe")
            with col_b:
                email = st.text_input("Email *", placeholder="john@example.com", 
                                     help="Required for tracking your submission")
            
            phone = st.text_input("Phone (Optional)", placeholder="+1 234 567 8900")
            
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
                area = st.text_input("Neighborhood/Area *", placeholder="Downtown")
            with col_loc2:
                address = st.text_input("Street Address (Optional)", placeholder="123 Main St")
            
            # Feedback Content
            st.subheader("📝 Your Feedback")
            title = st.text_input("Brief Title *", placeholder="Pothole on Main Street")
            
            feedback_text = st.text_area(
                "Detailed Description *",
                placeholder="Please describe the issue in detail. Include what you observed, when it happened, and any other relevant information...",
                height=150
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
                # Validation
                if not name or not email or not title or not feedback_text or not area:
                    st.error("⚠️ Please fill in all required fields (marked with *)")
                elif not consent:
                    st.error("⚠️ Please agree to the terms to submit your feedback")
                else:
                    # AI Analysis
                    analysis = st.session_state.analyzer.analyze(feedback_text)
                    
                    # Generate tracking ID
                    tracking_id = st.session_state.data_manager.generate_id()
                    
                    # Create feedback entry
                    feedback_entry = {
                        "id": tracking_id,
                        "timestamp": datetime.now().isoformat(),
                        "name": name,
                        "email": email,
                        "phone": phone if phone else "N/A",
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
                        "priority": "Normal"
                    }
                    
                    # Save
                    st.session_state.data_manager.add_feedback(feedback_entry)
                    st.session_state.submitted_ids.append(tracking_id)
                    
                    # Success message
                    st.balloons()
                    st.success(f"""
                    ✅ **Feedback Submitted Successfully!**
                    
                    📋 **Your Tracking ID:** `{tracking_id}`
                    
                    Save this ID to track your submission status. 
                    We'll also send updates to: {email}
                    """)
    
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
                # Status styling
                status_colors = {
                    "New": ("🆕", "#DBEAFE", "#1E40AF"),
                    "In Review": ("👀", "#E9D5FF", "#6B21A8"),
                    "In Progress": ("🔄", "#FEF3C7", "#92400E"),
                    "Resolved": ("✅", "#D1FAE5", "#065F46"),
                    "Closed": ("📁", "#F3F4F6", "#374151")
                }
                
                status = row.get('status', 'New')
                emoji, bg_color, text_color = status_colors.get(status, ("📋", "#F3F4F6", "#374151"))
                
                st.markdown(f"""
                <div style="background: {bg_color}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                    <h3 style="color: {text_color}; margin: 0;">
                        {emoji} {row.get('title', 'Untitled')}
                    </h3>
                    <p style="color: {text_color}; opacity: 0.8;">
                        Tracking ID: <strong>{row.get('id', 'N/A')}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📋 Submission Details**")
                    st.write(f"**Category:** {row.get('category', 'N/A')}")
                    st.write(f"**Location:** {row.get('location', 'N/A')}")
                    st.write(f"**Submitted:** {row.get('timestamp', 'N/A')[:10]}")
                    st.write(f"**Urgency:** {row.get('urgency', 'N/A')}")
                
                with col2:
                    st.markdown("**📊 Current Status**")
                    st.write(f"**Status:** {emoji} {status}")
                    if row.get('assigned_to'):
                        st.write(f"**Assigned To:** {row.get('assigned_to')}")
                    if row.get('admin_notes'):
                        st.info(f"**Admin Response:** {row.get('admin_notes')}")
                
                with st.expander("View Full Feedback"):
                    st.write(row.get('feedback', 'No description'))
                
                st.divider()
    
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
