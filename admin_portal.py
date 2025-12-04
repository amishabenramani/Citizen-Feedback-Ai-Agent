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

from src.feedback_analyzer import FeedbackAnalyzer
from src.data_manager import DataManager
from src.dashboard import Dashboard

# Page configuration
st.set_page_config(
    page_title="Admin Portal - Citizen Feedback",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Admin Portal (Dark/Professional Theme)
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1F2937;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .admin-card {
        background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #4B5563;
        margin-bottom: 1rem;
    }
    .priority-critical {
        background: #FEE2E2;
        border-left: 5px solid #DC2626;
    }
    .priority-high {
        background: #FEF3C7;
        border-left: 5px solid #F59E0B;
    }
    .priority-normal {
        background: #DBEAFE;
        border-left: 5px solid #3B82F6;
    }
    .priority-low {
        background: #D1FAE5;
        border-left: 5px solid #10B981;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .alert-box {
        background: #FEF2F2;
        border: 1px solid #FECACA;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-radius: 8px;
        padding: 1rem;
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
    """Render admin login page."""
    st.markdown('<p class="main-header">🔐 Admin Portal Login</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Authorized personnel only</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("Enter Credentials")
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            login_btn = st.form_submit_button("🔓 Login", use_container_width=True)
            
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
        
        st.divider()
        st.info("""
        **Demo Credentials:**
        - Username: `admin` / Password: `admin123`
        - Username: `manager` / Password: `manager123`
        - Username: `staff` / Password: `staff123`
        """)


def render_sidebar():
    """Render admin sidebar."""
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/administrative-tools.png", width=80)
        st.title("⚙️ Admin Portal")
        st.caption(f"Logged in as: **{st.session_state.admin_username}**")
        
        st.divider()
        
        page = st.radio(
            "Navigate",
            [
                "📊 Dashboard",
                "📋 All Feedback",
                "🚨 Priority Queue",
                "👥 Assignments",
                "📈 Analytics",
                "📤 Export Data",
                "⚙️ Settings"
            ],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Quick stats
        df = st.session_state.data_manager.get_feedback_dataframe()
        if not df.empty:
            new_count = len(df[df['status'] == 'New']) if 'status' in df else 0
            urgent_count = len(df[df['urgency'].isin(['High', 'Emergency'])]) if 'urgency' in df else 0
            
            if new_count > 0:
                st.warning(f"🆕 {new_count} new submissions")
            if urgent_count > 0:
                st.error(f"🚨 {urgent_count} urgent items")
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.session_state.admin_username = None
            st.rerun()
        
        return page


def render_dashboard():
    """Render admin dashboard."""
    st.markdown('<p class="main-header">📊 Admin Dashboard</p>', unsafe_allow_html=True)
    
    df = st.session_state.data_manager.get_feedback_dataframe()
    
    if df.empty:
        st.info("📭 No feedback data available yet.")
        return
    
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total = len(df)
    new = len(df[df['status'] == 'New']) if 'status' in df else 0
    in_review = len(df[df['status'] == 'In Review']) if 'status' in df else 0
    in_progress = len(df[df['status'] == 'In Progress']) if 'status' in df else 0
    resolved = len(df[df['status'] == 'Resolved']) if 'status' in df else 0
    
    with col1:
        st.metric("📬 Total", total)
    with col2:
        st.metric("🆕 New", new, delta=f"+{new}" if new > 0 else None)
    with col3:
        st.metric("👀 In Review", in_review)
    with col4:
        st.metric("🔄 In Progress", in_progress)
    with col5:
        st.metric("✅ Resolved", resolved)
    
    st.divider()
    
    # Urgent items alert
    if 'urgency' in df.columns:
        urgent = df[df['urgency'].isin(['High', 'Emergency'])]
        urgent_new = urgent[urgent['status'] == 'New'] if 'status' in urgent else urgent
        
        if not urgent_new.empty:
            st.markdown("""
            <div class="alert-box">
                <h4>🚨 Urgent Items Requiring Attention</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for _, row in urgent_new.head(5).iterrows():
                urgency_color = "#DC2626" if row['urgency'] == 'Emergency' else "#F59E0B"
                st.markdown(f"""
                <div style="background: white; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid {urgency_color};">
                    <strong>{row.get('title', 'Untitled')}</strong> | 
                    {row.get('category', 'N/A')} | 
                    <span style="color: {urgency_color}; font-weight: bold;">{row.get('urgency', 'N/A')}</span>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Status Distribution")
        if 'status' in df.columns:
            status_counts = df['status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                hole=0.4,
                color_discrete_sequence=['#3B82F6', '#8B5CF6', '#F59E0B', '#10B981', '#6B7280']
            )
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("😊 Sentiment Analysis")
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
            st.plotly_chart(fig, use_container_width=True)
    
    # Category and urgency charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 By Category")
        if 'category' in df.columns:
            cat_counts = df['category'].value_counts().head(8)
            fig = px.bar(
                y=cat_counts.index,
                x=cat_counts.values,
                orientation='h',
                color_discrete_sequence=['#3B82F6']
            )
            fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚡ By Urgency")
        if 'urgency' in df.columns:
            urgency_order = ['Low', 'Medium', 'High', 'Emergency']
            urgency_counts = df['urgency'].value_counts().reindex(urgency_order, fill_value=0)
            colors = ['#10B981', '#F59E0B', '#F97316', '#DC2626']
            fig = go.Figure(data=[go.Bar(
                x=urgency_counts.index,
                y=urgency_counts.values,
                marker_color=colors
            )])
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
            st.plotly_chart(fig, use_container_width=True)


def render_all_feedback():
    """Render all feedback management page."""
    st.markdown('<p class="main-header">📋 All Feedback</p>', unsafe_allow_html=True)
    
    df = st.session_state.data_manager.get_feedback_dataframe()
    
    if df.empty:
        st.info("No feedback available.")
        return
    
    # Filters
    st.subheader("🔍 Filters")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        status_filter = st.multiselect("Status", df['status'].unique().tolist() if 'status' in df else [])
    with col2:
        category_filter = st.multiselect("Category", df['category'].unique().tolist() if 'category' in df else [])
    with col3:
        urgency_filter = st.multiselect("Urgency", df['urgency'].unique().tolist() if 'urgency' in df else [])
    with col4:
        sentiment_filter = st.multiselect("Sentiment", df['sentiment'].unique().tolist() if 'sentiment' in df else [])
    with col5:
        search = st.text_input("🔍 Search", placeholder="Search by title or ID...")
    
    # Apply filters
    filtered_df = df.copy()
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    if category_filter:
        filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
    if urgency_filter:
        filtered_df = filtered_df[filtered_df['urgency'].isin(urgency_filter)]
    if sentiment_filter:
        filtered_df = filtered_df[filtered_df['sentiment'].isin(sentiment_filter)]
    if search:
        mask = (
            filtered_df['title'].str.contains(search, case=False, na=False) |
            filtered_df['id'].str.contains(search, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    st.caption(f"Showing {len(filtered_df)} of {len(df)} items")
    
    st.divider()
    
    # Feedback list
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
                sentiment_emoji = {'Positive': '😊', 'Neutral': '😐', 'Negative': '😟'}
                st.write(f"**Sentiment:** {sentiment_emoji.get(row.get('sentiment', ''), '📝')} {row.get('sentiment', 'N/A')} (Score: {row.get('sentiment_score', 0):.2f})")
                st.write(f"**Keywords:** {', '.join(row.get('keywords', [])) if isinstance(row.get('keywords'), list) else row.get('keywords', 'N/A')}")
                st.write(f"**Summary:** {row.get('summary', 'N/A')}")
            
            with col2:
                st.markdown("**⚙️ Admin Actions**")
                
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
                
                # Assignment
                assigned = st.text_input(
                    "Assign To",
                    value=row.get('assigned_to', ''),
                    placeholder="Enter staff name",
                    key=f"assign_{row.get('id', idx)}"
                )
                
                # Admin notes
                notes = st.text_area(
                    "Admin Notes/Response",
                    value=row.get('admin_notes', ''),
                    placeholder="Add notes or response for citizen...",
                    key=f"notes_{row.get('id', idx)}"
                )
                
                # Save button
                if st.button("💾 Save Changes", key=f"save_{row.get('id', idx)}", use_container_width=True):
                    updates = {
                        'status': new_status,
                        'priority': new_priority,
                        'assigned_to': assigned,
                        'admin_notes': notes
                    }
                    st.session_state.data_manager.update_feedback(row.get('id'), updates)
                    st.success("✅ Changes saved!")
                    st.rerun()
                
                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{row.get('id', idx)}", type="secondary", use_container_width=True):
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
                st.session_state.data_manager.update_status(row.get('id'), 'Resolved')
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
    
    # Unassigned items
    st.subheader("📋 Unassigned Items")
    
    if unassigned.empty:
        st.success("✅ All items have been assigned!")
    else:
        for _, row in unassigned.head(20).iterrows():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{row.get('id')}** - {row.get('title', 'Untitled')} | {row.get('category', 'N/A')} | {row.get('urgency', 'Medium')}")
            
            with col2:
                staff = st.text_input(
                    "Assign to",
                    placeholder="Staff name",
                    key=f"quick_assign_{row.get('id')}",
                    label_visibility="collapsed"
                )
                if staff:
                    st.session_state.data_manager.update_feedback(row.get('id'), {'assigned_to': staff})
                    st.rerun()


def render_analytics():
    """Render detailed analytics page."""
    st.markdown('<p class="main-header">📈 Detailed Analytics</p>', unsafe_allow_html=True)
    
    df = st.session_state.data_manager.get_feedback_dataframe()
    
    if df.empty:
        st.info("No data for analytics.")
        return
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    st.divider()
    
    # Use dashboard component
    st.session_state.dashboard.render_charts(df)
    
    st.divider()
    
    # Additional analytics
    st.subheader("📊 Detailed Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**By Category**")
        if 'category' in df.columns:
            st.dataframe(df['category'].value_counts(), use_container_width=True)
    
    with col2:
        st.markdown("**By Urgency**")
        if 'urgency' in df.columns:
            st.dataframe(df['urgency'].value_counts(), use_container_width=True)
    
    with col3:
        st.markdown("**By Status**")
        if 'status' in df.columns:
            st.dataframe(df['status'].value_counts(), use_container_width=True)
    
    # Resolution time analysis
    st.divider()
    st.subheader("⏱️ Response Metrics")
    
    total = len(df)
    resolved = len(df[df['status'] == 'Resolved']) if 'status' in df else 0
    resolution_rate = (resolved / total * 100) if total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Resolution Rate", f"{resolution_rate:.1f}%")
    with col2:
        negative = len(df[df['sentiment'] == 'Negative']) if 'sentiment' in df else 0
        st.metric("Negative Feedback", negative)
    with col3:
        if 'sentiment_score' in df.columns:
            avg_sentiment = df['sentiment_score'].mean()
            st.metric("Avg Sentiment Score", f"{avg_sentiment:.2f}")


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


def main():
    """Main entry point for Admin Portal."""
    init_session_state()
    
    # Check login
    if not st.session_state.admin_logged_in:
        render_login()
        return
    
    page = render_sidebar()
    
    if page == "📊 Dashboard":
        render_dashboard()
    elif page == "📋 All Feedback":
        render_all_feedback()
    elif page == "🚨 Priority Queue":
        render_priority_queue()
    elif page == "👥 Assignments":
        render_assignments()
    elif page == "📈 Analytics":
        render_analytics()
    elif page == "📤 Export Data":
        render_export()
    elif page == "⚙️ Settings":
        render_settings()


if __name__ == "__main__":
    main()
