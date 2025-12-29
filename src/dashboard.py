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
from .advanced_analytics import AdvancedAnalytics
from .geospatial_viz import GeospatialVisualizer


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
        
        # Initialize advanced analytics engines
        self.analytics = AdvancedAnalytics()
        self.geo_viz = GeospatialVisualizer()
    
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
    
    # Advanced Analytics Methods
    
    def render_advanced_analytics_dashboard(self, df: pd.DataFrame):
        """
        Render comprehensive advanced analytics dashboard.
        
        Args:
            df: DataFrame with feedback data
        """
        st.markdown("""
        <h2 style="font-family: 'Poppins', sans-serif; font-weight: 700; color: #e2e8f0; 
                   font-size: 1.8rem; margin-bottom: 1.5rem; text-align: center;">
            🚀 Advanced Analytics & Insights
        </h2>
        """, unsafe_allow_html=True)
        
        # Create tabs for different analytics sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Trend Analysis", 
            "⚠️ SLA Monitoring", 
            "🗺️ Geospatial Heatmap",
            "🏢 Department Performance",
            "⏰ Time Patterns"
        ])
        
        with tab1:
            self.render_trend_analysis(df)
        
        with tab2:
            self.render_sla_monitoring(df)
        
        with tab3:
            self.render_geospatial_analysis(df)
        
        with tab4:
            self.render_department_performance(df)
        
        with tab5:
            self.render_temporal_patterns(df)
    
    def render_trend_analysis(self, df: pd.DataFrame):
        """Render trend analysis with forecasting."""
        st.markdown("### 📈 Trend Analysis & Forecasting")
        
        # Period selector
        col1, col2 = st.columns([3, 1])
        with col2:
            period = st.selectbox("Time Period", ["daily", "weekly", "monthly"], index=1, key="trend_period")
        
        # Calculate trends
        trends = self.analytics.calculate_trends(df, period=period)
        
        # Display summary
        st.info(f"**📊 {trends['summary']}**")
        
        # Overall trend chart
        if trends['total_counts']:
            dates = list(trends['total_counts'].keys())
            counts = list(trends['total_counts'].values())
            
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=dates,
                y=counts,
                mode='lines+markers',
                name='Actual',
                line=dict(color=self.color_scheme['primary'], width=3),
                marker=dict(size=8, color=self.color_scheme['primary']),
                fill='tozeroy',
                fillcolor='rgba(139, 92, 246, 0.1)'
            ))
            
            # Forecast
            if trends['forecast']:
                forecast_dates = [f['period'] for f in trends['forecast']]
                forecast_values = [f['predicted_value'] for f in trends['forecast']]
                
                fig.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=forecast_values,
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color=self.color_scheme['warning'], width=2, dash='dash'),
                    marker=dict(size=6, color=self.color_scheme['warning'])
                ))
            
            fig.update_layout(
                title=f"Feedback Volume Trend ({period.capitalize()})",
                xaxis=dict(
                    title="Period",
                    gridcolor='rgba(139, 92, 246, 0.1)',
                    tickfont=dict(color='#94a3b8')
                ),
                yaxis=dict(
                    title="Count",
                    gridcolor='rgba(139, 92, 246, 0.1)',
                    tickfont=dict(color='#94a3b8')
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', family='Inter, sans-serif'),
                height=400,
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(17, 24, 39, 0.8)',
                    bordercolor='rgba(139, 92, 246, 0.3)',
                    borderwidth=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment trends
        st.markdown("#### 😊 Sentiment Trends")
        if trends['sentiment_trends']:
            fig = go.Figure()
            
            for sentiment, data in trends['sentiment_trends'].items():
                dates = list(data.keys())
                values = list(data.values())
                color = self.sentiment_colors.get(sentiment, '#6B7280')
                
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=values,
                    mode='lines+markers',
                    name=sentiment,
                    line=dict(color=color, width=2),
                    marker=dict(size=6, color=color)
                ))
            
            fig.update_layout(
                xaxis=dict(title="Period", gridcolor='rgba(139, 92, 246, 0.1)', tickfont=dict(color='#94a3b8')),
                yaxis=dict(title="Count", gridcolor='rgba(139, 92, 246, 0.1)', tickfont=dict(color='#94a3b8')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', family='Inter, sans-serif'),
                height=350,
                hovermode='x unified',
                legend=dict(bgcolor='rgba(17, 24, 39, 0.8)', bordercolor='rgba(139, 92, 246, 0.3)', borderwidth=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Category trends
        if trends['category_trends']:
            st.markdown("#### 📁 Top Category Trends")
            fig = go.Figure()
            
            for category, data in list(trends['category_trends'].items())[:5]:
                dates = list(data.keys())
                values = list(data.values())
                
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=values,
                    mode='lines',
                    name=category,
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                xaxis=dict(title="Period", gridcolor='rgba(139, 92, 246, 0.1)', tickfont=dict(color='#94a3b8')),
                yaxis=dict(title="Count", gridcolor='rgba(139, 92, 246, 0.1)', tickfont=dict(color='#94a3b8')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', family='Inter, sans-serif'),
                height=350,
                hovermode='x unified',
                legend=dict(bgcolor='rgba(17, 24, 39, 0.8)', bordercolor='rgba(139, 92, 246, 0.3)', borderwidth=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_sla_monitoring(self, df: pd.DataFrame):
        """Render SLA breach monitoring and predictions."""
        st.markdown("### ⚠️ SLA Breach Monitoring & Prediction")
        
        # Get SLA analysis
        sla_data = self.analytics.predict_sla_breaches(df)
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: rgba(239, 68, 68, 0.15); border-radius: 12px; padding: 1.5rem;
                        border: 1px solid rgba(239, 68, 68, 0.3); text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #EF4444;">
                    {sla_data['breach_count']}
                </div>
                <div style="color: rgba(148, 163, 184, 0.9); margin-top: 0.5rem;">
                    Breached SLAs
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: rgba(245, 158, 11, 0.15); border-radius: 12px; padding: 1.5rem;
                        border: 1px solid rgba(245, 158, 11, 0.3); text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #F59E0B;">
                    {sla_data['at_risk_count']}
                </div>
                <div style="color: rgba(148, 163, 184, 0.9); margin-top: 0.5rem;">
                    At Risk
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            compliant_pct = sla_data['sla_performance'].get('compliant', 0)
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.15); border-radius: 12px; padding: 1.5rem;
                        border: 1px solid rgba(16, 185, 129, 0.3); text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #10B981;">
                    {compliant_pct:.1f}%
                </div>
                <div style="color: rgba(148, 163, 184, 0.9); margin-top: 0.5rem;">
                    SLA Compliance
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recommendations
        if sla_data['recommendations']:
            st.markdown("#### 💡 Recommendations")
            for rec in sla_data['recommendations']:
                st.info(rec)
        
        # Breached tickets
        if sla_data['breached_tickets']:
            st.markdown("#### 🚨 Breached Tickets (Immediate Action Required)")
            
            for ticket in sla_data['breached_tickets'][:10]:
                urgency_colors = {'Critical': '#EF4444', 'High': '#F97316', 'Medium': '#F59E0B', 'Low': '#10B981'}
                color = urgency_colors.get(ticket['urgency'], '#6B7280')
                
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.1); border-radius: 8px; padding: 1rem; 
                            margin-bottom: 0.5rem; border-left: 4px solid {color};">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <strong style="color: #e2e8f0;">{ticket['title']}</strong>
                            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem;">
                                {ticket['category']} • {ticket['urgency']}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: #EF4444; font-weight: 600;">
                                {ticket['hours_overdue']:.1f}h overdue
                            </div>
                            {"<div style='color: #F59E0B; font-size: 0.8rem;'>⚠️ Escalate</div>" if ticket['escalation_needed'] else ""}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # At-risk tickets
        if sla_data['at_risk_tickets']:
            st.markdown("#### ⚡ At-Risk Tickets")
            
            for ticket in sla_data['at_risk_tickets'][:15]:
                breach_prob = ticket['breach_probability']
                prob_color = '#EF4444' if breach_prob > 80 else '#F97316' if breach_prob > 60 else '#F59E0B'
                
                st.markdown(f"""
                <div style="background: rgba(245, 158, 11, 0.1); border-radius: 8px; padding: 0.875rem; 
                            margin-bottom: 0.5rem; border-left: 3px solid {prob_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <strong style="color: #e2e8f0; font-size: 0.95rem;">{ticket['title'][:50]}...</strong>
                            <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 0.15rem;">
                                {ticket['category']} • {ticket['urgency']} • {ticket['hours_remaining']:.1f}h remaining
                            </div>
                        </div>
                        <div style="text-align: right; margin-left: 1rem;">
                            <div style="background: {prob_color}20; color: {prob_color}; padding: 0.25rem 0.75rem;
                                        border-radius: 20px; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.25rem;">
                                {breach_prob:.0f}% risk
                            </div>
                            <div style="color: #94a3b8; font-size: 0.75rem;">
                                {ticket['recommended_action']}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    def render_geospatial_analysis(self, df: pd.DataFrame):
        """Render geospatial analysis and heatmaps."""
        st.markdown("### 🗺️ Geospatial Analysis & Hotspots")
        
        # Get geospatial analysis
        geo_data = self.analytics.analyze_geospatial_distribution(df)
        
        # Map type selector
        col1, col2 = st.columns([3, 1])
        with col2:
            map_type = st.selectbox("Map Type", ["Heatmap", "Hotspots", "Category Distribution"], key="map_type")
        
        # Render selected map
        if map_type == "Heatmap":
            fig = self.geo_viz.create_complaint_heatmap(df)
            st.plotly_chart(fig, use_container_width=True)
        
        elif map_type == "Hotspots":
            fig = self.geo_viz.create_hotspot_map(df, top_n=10)
            st.plotly_chart(fig, use_container_width=True)
        
        else:  # Category Distribution
            if 'category' in df.columns:
                category = st.selectbox("Select Category", ["All"] + df['category'].unique().tolist(), key="geo_category")
                fig = self.geo_viz.create_category_distribution_map(df, None if category == "All" else category)
                st.plotly_chart(fig, use_container_width=True)
        
        # Hotspot details
        st.markdown("#### 🔥 Location Hotspots")
        
        if geo_data['location_hotspots']:
            cols = st.columns(3)
            for idx, hotspot in enumerate(geo_data['location_hotspots'][:6]):
                with cols[idx % 3]:
                    score_color = '#EF4444' if hotspot['hotspot_score'] > 100 else '#F97316' if hotspot['hotspot_score'] > 50 else '#F59E0B'
                    
                    st.markdown(f"""
                    <div style="background: {score_color}15; border-radius: 10px; padding: 1rem;
                                border: 1px solid {score_color}30; margin-bottom: 1rem;">
                        <div style="font-weight: 600; color: #e2e8f0; font-size: 1rem; margin-bottom: 0.5rem;">
                            📍 {hotspot['area']}
                        </div>
                        <div style="color: #94a3b8; font-size: 0.85rem;">
                            <strong style="color: {score_color};">{hotspot['count']}</strong> complaints<br>
                            Urgency: <strong>{hotspot['avg_urgency']:.1f}</strong><br>
                            Negative: <strong>{hotspot['negative_sentiment_pct']:.0f}%</strong><br>
                            <span style="color: {score_color}; font-weight: 600;">
                                Score: {hotspot['hotspot_score']:.0f}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Recommendations
        if geo_data['recommendations']:
            st.markdown("#### 💡 Geospatial Recommendations")
            for rec in geo_data['recommendations']:
                st.info(rec)
    
    def render_department_performance(self, df: pd.DataFrame):
        """Render department-wise performance metrics."""
        st.markdown("### 🏢 Department Performance Analysis")
        
        # Get department analysis
        dept_data = self.analytics.analyze_department_performance(df)
        
        if not dept_data['department_metrics']:
            st.warning("No department data available")
            return
        
        # Overall performance score
        st.markdown(f"""
        <div style="background: rgba(139, 92, 246, 0.15); border-radius: 12px; padding: 1.5rem;
                    border: 1px solid rgba(139, 92, 246, 0.3); text-align: center; margin-bottom: 1.5rem;">
            <div style="font-size: 2rem; font-weight: 700; color: #8b5cf6;">
                {dept_data['overall_avg_performance']:.1f}/100
            </div>
            <div style="color: rgba(148, 163, 184, 0.9); margin-top: 0.5rem;">
                Overall Department Performance Score
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Top and bottom performers
        col1, col2 = st.columns(2)
        
        if dept_data['top_performer']:
            top = dept_data['top_performer']
            with col1:
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.15); border-radius: 10px; padding: 1rem;
                            border: 1px solid rgba(16, 185, 129, 0.3);">
                    <div style="text-align: center; margin-bottom: 0.5rem;">🏆</div>
                    <div style="font-weight: 600; color: #10B981; text-align: center; margin-bottom: 0.5rem;">
                        Top Performer
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #e2e8f0; text-align: center;">
                        {top['department']}
                    </div>
                    <div style="text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 0.5rem;">
                        Score: {top['performance_score']:.1f} | Resolution: {top['resolution_rate']:.0f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if dept_data['bottom_performer']:
            bottom = dept_data['bottom_performer']
            with col2:
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.15); border-radius: 10px; padding: 1rem;
                            border: 1px solid rgba(239, 68, 68, 0.3);">
                    <div style="text-align: center; margin-bottom: 0.5rem;">⚠️</div>
                    <div style="font-weight: 600; color: #EF4444; text-align: center; margin-bottom: 0.5rem;">
                        Needs Improvement
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #e2e8f0; text-align: center;">
                        {bottom['department']}
                    </div>
                    <div style="text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 0.5rem;">
                        Score: {bottom['performance_score']:.1f} | Resolution: {bottom['resolution_rate']:.0f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Performance comparison chart
        st.markdown("#### 📊 Performance Comparison")
        
        dept_names = [d['department'] for d in dept_data['department_metrics']]
        perf_scores = [d['performance_score'] for d in dept_data['department_metrics']]
        
        fig = go.Figure(data=[go.Bar(
            y=dept_names,
            x=perf_scores,
            orientation='h',
            marker=dict(
                color=perf_scores,
                colorscale=[[0, '#EF4444'], [0.5, '#F59E0B'], [1, '#10B981']],
                showscale=False
            ),
            text=[f"{score:.1f}" for score in perf_scores],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>'
        )])
        
        fig.update_layout(
            xaxis=dict(
                title="Performance Score",
                range=[0, 100],
                gridcolor='rgba(139, 92, 246, 0.1)',
                tickfont=dict(color='#94a3b8')
            ),
            yaxis=dict(
                title="",
                tickfont=dict(color='#e2e8f0')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Inter, sans-serif'),
            height=max(300, len(dept_names) * 40),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed metrics table
        st.markdown("#### 📋 Detailed Metrics")
        
        for dept in dept_data['department_metrics']:
            with st.expander(f"**{dept['department']}** - Score: {dept['performance_score']:.1f}"):
                col1, col2, col3, col4 = st.columns(4)
                
                col1.metric("Total Tickets", dept['total_tickets'])
                col2.metric("Resolution Rate", f"{dept['resolution_rate']:.1f}%")
                col3.metric("Satisfaction", f"{dept['satisfaction_score']:.1f}/100")
                col4.metric("SLA Compliance", f"{dept['sla_compliance']:.1f}%")
                
                st.markdown(f"**Avg Response Time:** {dept['avg_response_time_hours']:.1f} hours")
                st.markdown(f"**Trend:** {dept['trend'].title()}")
                
                # Sentiment distribution
                sent_dist = dept['sentiment_distribution']
                if any(sent_dist.values()):
                    st.markdown("**Sentiment Distribution:**")
                    col1, col2, col3 = st.columns(3)
                    col1.markdown(f"😊 Positive: **{sent_dist.get('Positive', 0)}**")
                    col2.markdown(f"😐 Neutral: **{sent_dist.get('Neutral', 0)}**")
                    col3.markdown(f"😟 Negative: **{sent_dist.get('Negative', 0)}**")
        
        # Recommendations
        if dept_data['recommendations']:
            st.markdown("#### 💡 Department Recommendations")
            for rec in dept_data['recommendations']:
                st.info(rec)
    
    def render_temporal_patterns(self, df: pd.DataFrame):
        """Render temporal pattern analysis."""
        st.markdown("### ⏰ Temporal Patterns & Time-Based Insights")
        
        # Day/Hour heatmap
        fig = self.geo_viz.create_temporal_heatmap(df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Response time distribution
        if 'timestamp' in df.columns and 'status' in df.columns:
            st.markdown("#### ⏱️ Response Time Analysis")
            
            df_copy = df.copy()
            df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'], errors='coerce')
            df_copy['hour'] = df_copy['timestamp'].dt.hour
            
            # Hourly submission distribution
            hourly_counts = df_copy.groupby('hour').size().reset_index(name='count')
            
            fig = go.Figure(data=[go.Bar(
                x=hourly_counts['hour'],
                y=hourly_counts['count'],
                marker=dict(
                    color=hourly_counts['count'],
                    colorscale='Viridis',
                    showscale=False
                ),
                hovertemplate='Hour: %{x}:00<br>Count: %{y}<extra></extra>'
            )])
            
            fig.update_layout(
                title="Submissions by Hour of Day",
                xaxis=dict(
                    title="Hour",
                    tickmode='linear',
                    tick0=0,
                    dtick=2,
                    gridcolor='rgba(139, 92, 246, 0.1)',
                    tickfont=dict(color='#94a3b8')
                ),
                yaxis=dict(
                    title="Count",
                    gridcolor='rgba(139, 92, 246, 0.1)',
                    tickfont=dict(color='#94a3b8')
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', family='Inter, sans-serif'),
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)

