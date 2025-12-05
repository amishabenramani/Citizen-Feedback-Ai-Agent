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
    Premium Dashboard component for visualizing citizen feedback analytics.
    Features glassmorphism design and modern chart styling.
    """
    
    def __init__(self):
        """Initialize the dashboard with premium color schemes."""
        # Premium gradient colors
        self.color_scheme = {
            'primary': '#8b5cf6',
            'primary_light': '#a78bfa',
            'success': '#10B981',
            'success_light': '#34d399',
            'warning': '#F59E0B',
            'warning_light': '#fbbf24',
            'danger': '#EF4444',
            'danger_light': '#f87171',
            'info': '#3b82f6',
            'info_light': '#60a5fa',
            'neutral': '#6B7280'
        }
        
        # Premium sentiment colors with gradients
        self.sentiment_colors = {
            'Positive': '#10B981',
            'Neutral': '#F59E0B',
            'Negative': '#EF4444'
        }
        
        # Modern category color palette
        self.category_colors = [
            '#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', 
            '#ef4444', '#ec4899', '#06b6d4', '#84cc16',
            '#f97316', '#6366f1', '#14b8a6', '#a855f7'
        ]
        
        # Chart layout template for dark theme
        self.chart_layout = {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': 'rgba(148, 163, 184, 0.9)', 'family': 'Inter, sans-serif'},
            'margin': dict(l=20, r=20, t=40, b=20),
            'height': 320
        }
    
    def render_metrics(self, df: pd.DataFrame):
        """
        Render premium key metrics cards with glassmorphism.
        
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
        
        metrics = [
            ("📊", "Total Feedback", total, f"+{new_this_week} this week" if new_this_week > 0 else None, self.color_scheme['primary']),
            ("😊", "Positive", f"{(positive / total * 100) if total > 0 else 0:.1f}%", f"{positive} submissions", self.color_scheme['success']),
            ("😟", "Negative", f"{(negative / total * 100) if total > 0 else 0:.1f}%", f"{negative} submissions", self.color_scheme['danger']),
            ("✅", "Resolved", f"{(resolved / total * 100) if total > 0 else 0:.1f}%", f"{resolved} resolved", self.color_scheme['info'])
        ]
        
        for col, (icon, label, value, delta, color) in zip([col1, col2, col3, col4], metrics):
            with col:
                st.markdown(f"""
                <div style="background: {color}15; border-radius: 16px; padding: 1.5rem; 
                            text-align: center; border: 1px solid {color}30;
                            backdrop-filter: blur(10px);">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: {color}; 
                                font-family: 'Poppins', sans-serif;">{value}</div>
                    <div style="font-size: 0.85rem; color: rgba(148, 163, 184, 0.9); margin-top: 0.25rem;">
                        {label}
                    </div>
                    {"<div style='font-size: 0.75rem; color: " + self.color_scheme['success'] + "; margin-top: 0.5rem;'>" + str(delta) + "</div>" if delta else ""}
                </div>
                """, unsafe_allow_html=True)
    
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
        """Render premium sentiment distribution donut chart."""
        st.markdown("""
        <h3 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #e2e8f0; 
                   font-size: 1.1rem; margin-bottom: 1rem;">
            😊 Sentiment Distribution
        </h3>
        """, unsafe_allow_html=True)
        
        if 'sentiment' not in df.columns:
            st.info("No sentiment data available")
            return
        
        sentiment_counts = df['sentiment'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.5,
            marker_colors=[self.sentiment_colors.get(s, '#6B7280') for s in sentiment_counts.index],
            textinfo='percent+label',
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            **self.chart_layout,
            showlegend=True,
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(color='rgba(148, 163, 184, 0.9)')
            ),
            annotations=[dict(
                text='Sentiment',
                x=0.5, y=0.5,
                font_size=14,
                font_color='rgba(148, 163, 184, 0.8)',
                showarrow=False
            )]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_category_chart(self, df: pd.DataFrame):
        """Render premium category distribution bar chart."""
        st.markdown("""
        <h3 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #e2e8f0; 
                   font-size: 1.1rem; margin-bottom: 1rem;">
            📁 Feedback by Category
        </h3>
        """, unsafe_allow_html=True)
        
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
        
        fig.update_traces(
            marker_line_width=0,
            hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
        )
        
        fig.update_layout(
            **self.chart_layout,
            showlegend=False,
            xaxis=dict(
                title="Count",
                gridcolor='rgba(139, 92, 246, 0.1)',
                tickfont=dict(color='rgba(148, 163, 184, 0.8)')
            ),
            yaxis=dict(
                title="",
                tickfont=dict(color='rgba(148, 163, 184, 0.9)')
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_urgency_chart(self, df: pd.DataFrame):
        """Render premium urgency distribution chart."""
        st.markdown("""
        <h3 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #e2e8f0; 
                   font-size: 1.1rem; margin-bottom: 1rem;">
            ⚡ Urgency Levels
        </h3>
        """, unsafe_allow_html=True)
        
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
            marker_color=urgency_colors,
            marker_line_width=0,
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            **self.chart_layout,
            xaxis=dict(
                title="Urgency Level",
                tickfont=dict(color='rgba(148, 163, 184, 0.9)'),
                gridcolor='rgba(139, 92, 246, 0.05)'
            ),
            yaxis=dict(
                title="Count",
                tickfont=dict(color='rgba(148, 163, 184, 0.8)'),
                gridcolor='rgba(139, 92, 246, 0.1)'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_status_chart(self, df: pd.DataFrame):
        """Render premium status distribution chart."""
        st.markdown("""
        <h3 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #e2e8f0; 
                   font-size: 1.1rem; margin-bottom: 1rem;">
            📋 Status Overview
        </h3>
        """, unsafe_allow_html=True)
        
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
            marker_colors=[status_colors.get(s, '#6B7280') for s in status_counts.index],
            textinfo='percent+label',
            textfont=dict(size=11, color='white'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            **self.chart_layout,
            showlegend=True,
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(color='rgba(148, 163, 184, 0.9)')
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_timeline_chart(self, df: pd.DataFrame):
        """Render premium feedback submission timeline."""
        st.markdown("""
        <h3 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #e2e8f0; 
                   font-size: 1.1rem; margin-bottom: 1rem;">
            📈 Feedback Timeline
        </h3>
        """, unsafe_allow_html=True)
        
        if 'timestamp' not in df.columns:
            st.info("No timestamp data available")
            return
        
        # Convert timestamps
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['timestamp'], errors='coerce').dt.date
        
        # Group by date
        daily_counts = df_copy.groupby('date').size().reset_index(name='count')
        daily_counts['date'] = pd.to_datetime(daily_counts['date'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_counts['date'],
            y=daily_counts['count'],
            mode='lines',
            fill='tozeroy',
            line=dict(color=self.color_scheme['primary'], width=2),
            fillcolor='rgba(139, 92, 246, 0.2)',
            hovertemplate='<b>%{x|%b %d, %Y}</b><br>Submissions: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            **self.chart_layout,
            height=280,
            xaxis=dict(
                title="Date",
                tickfont=dict(color='rgba(148, 163, 184, 0.8)'),
                gridcolor='rgba(139, 92, 246, 0.05)',
                showgrid=True
            ),
            yaxis=dict(
                title="Submissions",
                tickfont=dict(color='rgba(148, 163, 184, 0.8)'),
                gridcolor='rgba(139, 92, 246, 0.1)',
                showgrid=True
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_heatmap(self, df: pd.DataFrame):
        """Render premium category vs sentiment heatmap."""
        st.markdown("""
        <h3 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #e2e8f0; 
                   font-size: 1.1rem; margin-bottom: 1rem;">
            🗺️ Category vs Sentiment Heatmap
        </h3>
        """, unsafe_allow_html=True)
        
        if 'category' not in df.columns or 'sentiment' not in df.columns:
            st.info("Insufficient data for heatmap")
            return
        
        # Create cross-tabulation
        crosstab = pd.crosstab(df['category'], df['sentiment'])
        
        fig = px.imshow(
            crosstab.values,
            x=crosstab.columns.tolist(),
            y=crosstab.index.tolist(),
            color_continuous_scale=[
                [0, '#1e1b4b'],
                [0.25, '#4c1d95'],
                [0.5, '#7c3aed'],
                [0.75, '#a78bfa'],
                [1, '#c4b5fd']
            ],
            aspect='auto'
        )
        
        fig.update_layout(
            **self.chart_layout,
            height=400,
            xaxis=dict(
                title="Sentiment",
                tickfont=dict(color='rgba(148, 163, 184, 0.9)'),
                side='bottom'
            ),
            yaxis=dict(
                title="Category",
                tickfont=dict(color='rgba(148, 163, 184, 0.9)')
            ),
            coloraxis_colorbar=dict(
                title="Count",
                tickfont=dict(color='rgba(148, 163, 184, 0.8)')
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_recent_feedback(self, df: pd.DataFrame, limit: int = 5):
        """
        Render premium recent feedback submissions.
        
        Args:
            df: DataFrame with feedback data
            limit: Number of recent items to show
        """
        st.markdown("""
        <h3 style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #e2e8f0; 
                   font-size: 1.1rem; margin-bottom: 1rem;">
            🕐 Recent Feedback
        </h3>
        """, unsafe_allow_html=True)
        
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
            sentiment_config = {
                'Positive': ('😊', '#10B981', 'rgba(16, 185, 129, 0.1)'),
                'Neutral': ('😐', '#F59E0B', 'rgba(245, 158, 11, 0.1)'),
                'Negative': ('😟', '#EF4444', 'rgba(239, 68, 68, 0.1)')
            }
            
            sentiment = row.get('sentiment', 'Neutral')
            emoji, color, bg = sentiment_config.get(sentiment, ('📝', '#6B7280', 'rgba(107, 114, 128, 0.1)'))
            
            st.markdown(f"""
            <div style="background: {bg}; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;
                        border: 1px solid {color}25; transition: all 0.3s ease;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{emoji}</span>
                        <strong style="color: #e2e8f0;">{row.get('title', 'Untitled')}</strong>
                        <div style="color: rgba(148, 163, 184, 0.7); font-size: 0.8rem; margin-top: 0.25rem;">
                            {row.get('category', 'N/A')} • {str(row.get('timestamp', 'N/A'))[:10] if row.get('timestamp') else 'N/A'}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: {color}20; color: {color}; padding: 0.2rem 0.6rem;
                                     border-radius: 20px; font-size: 0.7rem; font-weight: 600;">
                            {row.get('status', 'New')}
                        </span>
                        <div style="color: rgba(148, 163, 184, 0.6); font-size: 0.75rem; margin-top: 0.25rem;">
                            {row.get('urgency', 'Medium')}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
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
