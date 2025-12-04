"""
Dashboard Module
Provides visualization and analytics components for the citizen feedback dashboard.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any


class Dashboard:
    """
    Dashboard component for visualizing citizen feedback analytics.
    """
    
    def __init__(self):
        """Initialize the dashboard with color schemes."""
        self.color_scheme = {
            'primary': '#3B82F6',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'info': '#6366F1',
            'neutral': '#6B7280'
        }
        
        self.sentiment_colors = {
            'Positive': '#10B981',
            'Neutral': '#F59E0B',
            'Negative': '#EF4444'
        }
        
        self.category_colors = px.colors.qualitative.Set3
    
    def render_metrics(self, df: pd.DataFrame):
        """
        Render key metrics cards.
        
        Args:
            df: DataFrame with feedback data
        """
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(df)
        
        # Calculate metrics
        positive = len(df[df['sentiment'] == 'Positive']) if 'sentiment' in df else 0
        negative = len(df[df['sentiment'] == 'Negative']) if 'sentiment' in df else 0
        
        # New feedback (last 7 days)
        if 'timestamp' in df.columns:
            df['timestamp_dt'] = pd.to_datetime(df['timestamp'], errors='coerce')
            week_ago = datetime.now() - timedelta(days=7)
            new_this_week = len(df[df['timestamp_dt'] >= week_ago])
        else:
            new_this_week = 0
        
        # Resolved feedback
        resolved = len(df[df['status'] == 'Resolved']) if 'status' in df else 0
        
        with col1:
            st.metric(
                label="📊 Total Feedback",
                value=total,
                delta=f"+{new_this_week} this week" if new_this_week > 0 else None
            )
        
        with col2:
            positive_pct = (positive / total * 100) if total > 0 else 0
            st.metric(
                label="😊 Positive",
                value=f"{positive_pct:.1f}%",
                delta=f"{positive} submissions"
            )
        
        with col3:
            negative_pct = (negative / total * 100) if total > 0 else 0
            st.metric(
                label="😟 Negative",
                value=f"{negative_pct:.1f}%",
                delta=f"{negative} submissions",
                delta_color="inverse"
            )
        
        with col4:
            resolution_rate = (resolved / total * 100) if total > 0 else 0
            st.metric(
                label="✅ Resolved",
                value=f"{resolution_rate:.1f}%",
                delta=f"{resolved} resolved"
            )
    
    def render_charts(self, df: pd.DataFrame):
        """
        Render main analytics charts.
        
        Args:
            df: DataFrame with feedback data
        """
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_sentiment_chart(df)
        
        with col2:
            self._render_category_chart(df)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_urgency_chart(df)
        
        with col2:
            self._render_status_chart(df)
        
        st.divider()
        
        self._render_timeline_chart(df)
        
        st.divider()
        
        self._render_heatmap(df)
    
    def _render_sentiment_chart(self, df: pd.DataFrame):
        """Render sentiment distribution pie chart."""
        st.subheader("😊 Sentiment Distribution")
        
        if 'sentiment' not in df.columns:
            st.info("No sentiment data available")
            return
        
        sentiment_counts = df['sentiment'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.4,
            marker_colors=[self.sentiment_colors.get(s, '#6B7280') for s in sentiment_counts.index]
        )])
        
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            margin=dict(l=20, r=20, t=20, b=20),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_category_chart(self, df: pd.DataFrame):
        """Render category distribution bar chart."""
        st.subheader("📁 Feedback by Category")
        
        if 'category' not in df.columns:
            st.info("No category data available")
            return
        
        category_counts = df['category'].value_counts()
        
        fig = px.bar(
            x=category_counts.values,
            y=category_counts.index,
            orientation='h',
            color=category_counts.index,
            color_discrete_sequence=self.category_colors
        )
        
        fig.update_layout(
            showlegend=False,
            xaxis_title="Count",
            yaxis_title="",
            margin=dict(l=20, r=20, t=20, b=20),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_urgency_chart(self, df: pd.DataFrame):
        """Render urgency distribution chart."""
        st.subheader("⚡ Urgency Levels")
        
        if 'urgency' not in df.columns:
            st.info("No urgency data available")
            return
        
        urgency_order = ['Low', 'Medium', 'High', 'Critical']
        urgency_colors = ['#10B981', '#F59E0B', '#F97316', '#EF4444']
        
        urgency_counts = df['urgency'].value_counts()
        # Reorder
        urgency_counts = urgency_counts.reindex(urgency_order, fill_value=0)
        
        fig = go.Figure(data=[go.Bar(
            x=urgency_counts.index,
            y=urgency_counts.values,
            marker_color=urgency_colors
        )])
        
        fig.update_layout(
            xaxis_title="Urgency Level",
            yaxis_title="Count",
            margin=dict(l=20, r=20, t=20, b=20),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_status_chart(self, df: pd.DataFrame):
        """Render status distribution chart."""
        st.subheader("📋 Status Overview")
        
        if 'status' not in df.columns:
            st.info("No status data available")
            return
        
        status_counts = df['status'].value_counts()
        status_colors = {
            'New': '#3B82F6',
            'In Review': '#8B5CF6',
            'In Progress': '#F59E0B',
            'Resolved': '#10B981',
            'Closed': '#6B7280'
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            marker_colors=[status_colors.get(s, '#6B7280') for s in status_counts.index]
        )])
        
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            margin=dict(l=20, r=20, t=20, b=20),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_timeline_chart(self, df: pd.DataFrame):
        """Render feedback submission timeline."""
        st.subheader("📈 Feedback Timeline")
        
        if 'timestamp' not in df.columns:
            st.info("No timestamp data available")
            return
        
        # Convert timestamps
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['timestamp'], errors='coerce').dt.date
        
        # Group by date
        daily_counts = df_copy.groupby('date').size().reset_index(name='count')
        daily_counts['date'] = pd.to_datetime(daily_counts['date'])
        
        fig = px.area(
            daily_counts,
            x='date',
            y='count',
            title='',
            color_discrete_sequence=[self.color_scheme['primary']]
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Submissions",
            margin=dict(l=20, r=20, t=20, b=20),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_heatmap(self, df: pd.DataFrame):
        """Render category vs sentiment heatmap."""
        st.subheader("🗺️ Category vs Sentiment Heatmap")
        
        if 'category' not in df.columns or 'sentiment' not in df.columns:
            st.info("Insufficient data for heatmap")
            return
        
        # Create cross-tabulation
        crosstab = pd.crosstab(df['category'], df['sentiment'])
        
        fig = px.imshow(
            crosstab.values,
            x=crosstab.columns.tolist(),
            y=crosstab.index.tolist(),
            color_continuous_scale='RdYlGn',
            aspect='auto'
        )
        
        fig.update_layout(
            xaxis_title="Sentiment",
            yaxis_title="Category",
            margin=dict(l=20, r=20, t=20, b=20),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_recent_feedback(self, df: pd.DataFrame, limit: int = 5):
        """
        Render recent feedback submissions.
        
        Args:
            df: DataFrame with feedback data
            limit: Number of recent items to show
        """
        st.subheader("🕐 Recent Feedback")
        
        if df.empty:
            st.info("No recent feedback")
            return
        
        # Sort by timestamp
        if 'timestamp' in df.columns:
            df_sorted = df.sort_values('timestamp', ascending=False)
        else:
            df_sorted = df
        
        recent = df_sorted.head(limit)
        
        for _, row in recent.iterrows():
            sentiment_emoji = {
                'Positive': '😊',
                'Neutral': '😐',
                'Negative': '😟'
            }
            
            emoji = sentiment_emoji.get(row.get('sentiment', ''), '📝')
            
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{emoji} {row.get('title', 'Untitled')}**")
                    st.caption(f"{row.get('category', 'N/A')} | {row.get('timestamp', 'N/A')[:10]}")
                
                with col2:
                    st.caption(f"Status: {row.get('status', 'N/A')}")
                
                with col3:
                    st.caption(f"Urgency: {row.get('urgency', 'N/A')}")
                
                st.divider()
    
    def render_word_cloud_data(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Generate word frequency data for word cloud.
        
        Args:
            df: DataFrame with feedback data
            
        Returns:
            Dictionary of word frequencies
        """
        if 'keywords' not in df.columns:
            return {}
        
        word_freq = {}
        
        for keywords in df['keywords']:
            if isinstance(keywords, list):
                for word in keywords:
                    word_freq[word] = word_freq.get(word, 0) + 1
            elif isinstance(keywords, str):
                for word in keywords.split(','):
                    word = word.strip()
                    if word:
                        word_freq[word] = word_freq.get(word, 0) + 1
        
        return word_freq
