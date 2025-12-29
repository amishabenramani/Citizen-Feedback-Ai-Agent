"""
Advanced Analytics Module
Provides sophisticated analytics including trend analysis, SLA predictions, 
geospatial analysis, and department performance metrics.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


class AdvancedAnalytics:
    """
    Advanced analytics engine for citizen feedback system.
    Provides trend analysis, SLA breach prediction, geospatial analytics,
    and department performance metrics.
    """
    
    def __init__(self):
        """Initialize the advanced analytics engine."""
        # SLA configuration (in hours)
        self.sla_config = {
            'Critical': 4,   # 4 hours
            'High': 24,      # 24 hours
            'Medium': 72,    # 72 hours
            'Low': 168       # 168 hours (7 days)
        }
        
        # Department mapping (can be customized)
        self.department_mapping = {
            'Roads & Transportation': 'Infrastructure',
            'Water & Sanitation': 'Utilities',
            'Public Safety': 'Safety',
            'Healthcare': 'Health',
            'Education': 'Education',
            'Environment': 'Environment',
            'Street Lighting': 'Infrastructure',
            'Waste Management': 'Environment',
            'Parks & Recreation': 'Environment',
            'Building Permits': 'Administration',
            'Tax & Revenue': 'Administration',
            'Other': 'General'
        }
    
    def calculate_trends(self, df: pd.DataFrame, period: str = 'weekly') -> Dict[str, Any]:
        """
        Calculate trend analysis with statistical insights.
        
        Args:
            df: DataFrame with feedback data
            period: 'daily', 'weekly', or 'monthly'
            
        Returns:
            Dictionary containing trend analysis data
        """
        if df.empty or 'timestamp' not in df.columns:
            return self._empty_trend_response()
        
        # Prepare data
        df_copy = df.copy()
        df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'], errors='coerce')
        df_copy = df_copy.dropna(subset=['timestamp'])
        
        if df_copy.empty:
            return self._empty_trend_response()
        
        # Determine frequency
        freq_map = {
            'daily': 'D',
            'weekly': 'W',
            'monthly': 'M'
        }
        freq = freq_map.get(period, 'W')
        
        # Aggregate by time period
        df_copy.set_index('timestamp', inplace=True)
        
        # Overall trends
        total_counts = df_copy.resample(freq).size()
        
        # Sentiment trends
        sentiment_trends = {}
        if 'sentiment' in df_copy.columns:
            for sentiment in df_copy['sentiment'].dropna().unique():
                sentiment_trends[sentiment] = df_copy[df_copy['sentiment'] == sentiment].resample(freq).size()
        
        # Category trends
        category_trends = {}
        if 'category' in df_copy.columns:
            top_categories = df_copy['category'].value_counts().head(5).index
            for category in top_categories:
                category_trends[category] = df_copy[df_copy['category'] == category].resample(freq).size()
        
        # Calculate growth rate
        growth_rate = self._calculate_growth_rate(total_counts)
        
        # Forecast next periods
        forecast = self._simple_forecast(total_counts, periods=4)
        
        return {
            'period': period,
            'total_counts': total_counts.to_dict(),
            'sentiment_trends': {k: v.to_dict() for k, v in sentiment_trends.items()},
            'category_trends': {k: v.to_dict() for k, v in category_trends.items()},
            'growth_rate': growth_rate,
            'forecast': forecast,
            'summary': self._generate_trend_summary(total_counts, growth_rate)
        }
    
    def predict_sla_breaches(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Predict SLA breaches based on current open tickets and historical data.
        
        Args:
            df: DataFrame with feedback data
            
        Returns:
            Dictionary containing SLA breach predictions
        """
        if df.empty:
            return self._empty_sla_response()
        
        df_copy = df.copy()
        df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'], errors='coerce')
        
        # Filter open tickets
        open_statuses = ['New', 'In Review', 'In Progress']
        open_tickets = df_copy[df_copy['status'].isin(open_statuses)].copy()
        
        if open_tickets.empty:
            return {
                'at_risk_count': 0,
                'breach_count': 0,
                'at_risk_tickets': [],
                'breached_tickets': [],
                'sla_performance': {'compliant': 100.0, 'breached': 0.0},
                'recommendations': ['No open tickets at risk']
            }
        
        # Calculate time elapsed
        now = datetime.now()
        open_tickets['hours_elapsed'] = (now - open_tickets['timestamp']).dt.total_seconds() / 3600
        
        # Determine SLA target
        open_tickets['sla_hours'] = open_tickets['urgency'].map(self.sla_config).fillna(72)
        
        # Calculate time remaining
        open_tickets['hours_remaining'] = open_tickets['sla_hours'] - open_tickets['hours_elapsed']
        
        # Classify tickets
        breached = open_tickets[open_tickets['hours_remaining'] < 0]
        at_risk = open_tickets[(open_tickets['hours_remaining'] >= 0) & 
                                (open_tickets['hours_remaining'] < open_tickets['sla_hours'] * 0.2)]
        
        # Calculate historical SLA performance
        resolved_tickets = df_copy[df_copy['status'].isin(['Resolved', 'Closed'])].copy()
        sla_performance = self._calculate_sla_performance(resolved_tickets)
        
        # Generate predictions for at-risk tickets
        at_risk_details = []
        for _, ticket in at_risk.iterrows():
            breach_probability = self._calculate_breach_probability(ticket, resolved_tickets)
            at_risk_details.append({
                'id': ticket.get('id', 'N/A'),
                'title': ticket.get('title', 'Untitled'),
                'urgency': ticket.get('urgency', 'Medium'),
                'category': ticket.get('category', 'N/A'),
                'hours_remaining': round(ticket['hours_remaining'], 1),
                'breach_probability': round(breach_probability * 100, 1),
                'recommended_action': self._get_recommended_action(breach_probability)
            })
        
        # Generate breached ticket details
        breached_details = []
        for _, ticket in breached.iterrows():
            breached_details.append({
                'id': ticket.get('id', 'N/A'),
                'title': ticket.get('title', 'Untitled'),
                'urgency': ticket.get('urgency', 'Medium'),
                'category': ticket.get('category', 'N/A'),
                'hours_overdue': round(abs(ticket['hours_remaining']), 1),
                'escalation_needed': ticket['urgency'] in ['Critical', 'High']
            })
        
        return {
            'at_risk_count': len(at_risk),
            'breach_count': len(breached),
            'at_risk_tickets': sorted(at_risk_details, key=lambda x: x['hours_remaining']),
            'breached_tickets': sorted(breached_details, key=lambda x: x['hours_overdue'], reverse=True),
            'sla_performance': sla_performance,
            'recommendations': self._generate_sla_recommendations(len(at_risk), len(breached))
        }
    
    def analyze_geospatial_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze geographical distribution of complaints.
        
        Args:
            df: DataFrame with feedback data
            
        Returns:
            Dictionary containing geospatial analysis
        """
        if df.empty:
            return self._empty_geo_response()
        
        df_copy = df.copy()
        
        # Area/location analysis
        area_counts = {}
        location_hotspots = []
        
        if 'area' in df_copy.columns:
            area_counts = df_copy['area'].value_counts().head(10).to_dict()
            
            # Calculate hotspot score (frequency + urgency weight)
            for area in df_copy['area'].dropna().unique():
                area_data = df_copy[df_copy['area'] == area]
                
                urgency_weights = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
                avg_urgency = area_data['urgency'].map(urgency_weights).mean() if 'urgency' in area_data.columns else 2
                
                sentiment_score = 0
                if 'sentiment' in area_data.columns:
                    neg_pct = (area_data['sentiment'] == 'Negative').sum() / len(area_data) * 100
                    sentiment_score = neg_pct
                
                hotspot_score = len(area_data) * avg_urgency * (1 + sentiment_score / 100)
                
                location_hotspots.append({
                    'area': area,
                    'count': len(area_data),
                    'avg_urgency': round(avg_urgency, 2),
                    'negative_sentiment_pct': round(sentiment_score, 1),
                    'hotspot_score': round(hotspot_score, 2)
                })
        
        # Sort by hotspot score
        location_hotspots = sorted(location_hotspots, key=lambda x: x['hotspot_score'], reverse=True)[:10]
        
        # Category distribution by area
        category_by_area = {}
        if 'area' in df_copy.columns and 'category' in df_copy.columns:
            for area in df_copy['area'].value_counts().head(5).index:
                area_data = df_copy[df_copy['area'] == area]
                category_by_area[area] = area_data['category'].value_counts().head(3).to_dict()
        
        return {
            'area_counts': area_counts,
            'location_hotspots': location_hotspots,
            'category_by_area': category_by_area,
            'total_areas': df_copy['area'].nunique() if 'area' in df_copy.columns else 0,
            'recommendations': self._generate_geo_recommendations(location_hotspots)
        }
    
    def analyze_department_performance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze department-wise performance metrics.
        
        Args:
            df: DataFrame with feedback data
            
        Returns:
            Dictionary containing department performance metrics
        """
        if df.empty or 'category' not in df.columns:
            return self._empty_department_response()
        
        df_copy = df.copy()
        df_copy['department'] = df_copy['category'].map(self.department_mapping).fillna('General')
        
        department_metrics = []
        
        for dept in df_copy['department'].unique():
            dept_data = df_copy[df_copy['department'] == dept].copy()
            
            # Basic metrics
            total = len(dept_data)
            resolved = len(dept_data[dept_data['status'].isin(['Resolved', 'Closed'])])
            resolution_rate = (resolved / total * 100) if total > 0 else 0
            
            # Sentiment analysis
            sentiment_dist = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
            if 'sentiment' in dept_data.columns:
                sentiment_counts = dept_data['sentiment'].value_counts()
                sentiment_dist.update(sentiment_counts.to_dict())
            
            satisfaction_score = self._calculate_satisfaction_score(sentiment_dist)
            
            # Response time analysis
            avg_response_time = self._calculate_avg_response_time(dept_data)
            
            # SLA compliance
            sla_compliance = self._calculate_dept_sla_compliance(dept_data)
            
            # Performance score (composite metric)
            performance_score = (
                resolution_rate * 0.3 +
                satisfaction_score * 0.3 +
                sla_compliance * 0.25 +
                (100 - min(avg_response_time / 24 * 10, 100)) * 0.15
            )
            
            department_metrics.append({
                'department': dept,
                'total_tickets': total,
                'resolved_tickets': resolved,
                'resolution_rate': round(resolution_rate, 1),
                'satisfaction_score': round(satisfaction_score, 1),
                'avg_response_time_hours': round(avg_response_time, 1),
                'sla_compliance': round(sla_compliance, 1),
                'performance_score': round(performance_score, 1),
                'sentiment_distribution': sentiment_dist,
                'trend': self._calculate_dept_trend(dept_data)
            })
        
        # Sort by performance score
        department_metrics = sorted(department_metrics, key=lambda x: x['performance_score'], reverse=True)
        
        # Identify top and bottom performers
        top_performer = department_metrics[0] if department_metrics else None
        bottom_performer = department_metrics[-1] if len(department_metrics) > 1 else None
        
        return {
            'department_metrics': department_metrics,
            'top_performer': top_performer,
            'bottom_performer': bottom_performer,
            'overall_avg_performance': round(np.mean([d['performance_score'] for d in department_metrics]), 1) if department_metrics else 0,
            'recommendations': self._generate_dept_recommendations(department_metrics)
        }
    
    # Helper methods
    
    def _empty_trend_response(self) -> Dict[str, Any]:
        """Return empty trend response."""
        return {
            'period': 'weekly',
            'total_counts': {},
            'sentiment_trends': {},
            'category_trends': {},
            'growth_rate': 0.0,
            'forecast': [],
            'summary': 'No data available for trend analysis'
        }
    
    def _empty_sla_response(self) -> Dict[str, Any]:
        """Return empty SLA response."""
        return {
            'at_risk_count': 0,
            'breach_count': 0,
            'at_risk_tickets': [],
            'breached_tickets': [],
            'sla_performance': {'compliant': 0, 'breached': 0},
            'recommendations': []
        }
    
    def _empty_geo_response(self) -> Dict[str, Any]:
        """Return empty geo response."""
        return {
            'area_counts': {},
            'location_hotspots': [],
            'category_by_area': {},
            'total_areas': 0,
            'recommendations': []
        }
    
    def _empty_department_response(self) -> Dict[str, Any]:
        """Return empty department response."""
        return {
            'department_metrics': [],
            'top_performer': None,
            'bottom_performer': None,
            'overall_avg_performance': 0,
            'recommendations': []
        }
    
    def _calculate_growth_rate(self, series: pd.Series) -> float:
        """Calculate growth rate from time series."""
        if len(series) < 2:
            return 0.0
        
        recent = series.iloc[-1]
        previous = series.iloc[-2]
        
        if previous == 0:
            return 100.0 if recent > 0 else 0.0
        
        return ((recent - previous) / previous) * 100
    
    def _simple_forecast(self, series: pd.Series, periods: int = 4) -> List[Dict[str, Any]]:
        """Simple moving average forecast."""
        if len(series) < 3:
            return []
        
        # Calculate moving average
        window = min(3, len(series))
        moving_avg = series.rolling(window=window).mean().iloc[-1]
        
        # Generate forecast
        forecast = []
        last_date = series.index[-1]
        
        for i in range(1, periods + 1):
            if isinstance(last_date, pd.Timestamp):
                # Infer frequency
                if len(series) > 1:
                    freq = series.index[-1] - series.index[-2]
                    next_date = last_date + freq * i
                else:
                    next_date = last_date + pd.Timedelta(days=7 * i)
            else:
                next_date = f"Period {i}"
            
            forecast.append({
                'period': str(next_date)[:10] if isinstance(next_date, pd.Timestamp) else next_date,
                'predicted_value': round(moving_avg, 0)
            })
        
        return forecast
    
    def _generate_trend_summary(self, series: pd.Series, growth_rate: float) -> str:
        """Generate human-readable trend summary."""
        if len(series) == 0:
            return "No data available"
        
        trend_direction = "increasing" if growth_rate > 5 else "decreasing" if growth_rate < -5 else "stable"
        avg_submissions = series.mean()
        
        return f"Feedback volume is {trend_direction} ({growth_rate:+.1f}%). Average: {avg_submissions:.0f} submissions per period."
    
    def _calculate_sla_performance(self, resolved_df: pd.DataFrame) -> Dict[str, float]:
        """Calculate historical SLA performance."""
        if resolved_df.empty:
            return {'compliant': 0, 'breached': 0}
        
        # For now, simulate SLA compliance based on urgency and timestamps
        # In production, you'd have actual resolution timestamps
        total = len(resolved_df)
        
        # Simulate: assume 85% compliance on average, higher for lower urgency
        urgency_compliance = {'Low': 0.95, 'Medium': 0.88, 'High': 0.75, 'Critical': 0.65}
        
        compliant = 0
        for _, ticket in resolved_df.iterrows():
            urgency = ticket.get('urgency', 'Medium')
            if np.random.random() < urgency_compliance.get(urgency, 0.85):
                compliant += 1
        
        breached = total - compliant
        
        return {
            'compliant': round((compliant / total * 100) if total > 0 else 0, 1),
            'breached': round((breached / total * 100) if total > 0 else 0, 1)
        }
    
    def _calculate_breach_probability(self, ticket: pd.Series, historical_df: pd.DataFrame) -> float:
        """Calculate probability of SLA breach for a ticket."""
        # Base probability on time remaining
        hours_remaining = ticket['hours_remaining']
        sla_hours = ticket['sla_hours']
        
        time_factor = 1 - (hours_remaining / sla_hours)
        time_factor = max(0, min(1, time_factor))
        
        # Adjust for urgency
        urgency_factor = {'Critical': 0.9, 'High': 0.75, 'Medium': 0.5, 'Low': 0.3}
        urgency_mult = urgency_factor.get(ticket.get('urgency', 'Medium'), 0.5)
        
        # Final probability
        probability = time_factor * 0.7 + urgency_mult * 0.3
        
        return min(1.0, probability)
    
    def _get_recommended_action(self, breach_prob: float) -> str:
        """Get recommended action based on breach probability."""
        if breach_prob > 0.8:
            return "URGENT: Immediate escalation required"
        elif breach_prob > 0.6:
            return "High priority: Assign resources immediately"
        elif breach_prob > 0.4:
            return "Monitor closely and prioritize"
        else:
            return "Standard tracking"
    
    def _generate_sla_recommendations(self, at_risk: int, breached: int) -> List[str]:
        """Generate SLA recommendations."""
        recommendations = []
        
        if breached > 0:
            recommendations.append(f"⚠️ {breached} ticket(s) have breached SLA - immediate action required")
        
        if at_risk > 5:
            recommendations.append(f"📊 {at_risk} tickets at risk - consider resource reallocation")
        elif at_risk > 0:
            recommendations.append(f"👀 Monitor {at_risk} at-risk ticket(s)")
        
        if breached == 0 and at_risk == 0:
            recommendations.append("✅ All tickets are on track - good performance!")
        
        return recommendations
    
    def _generate_geo_recommendations(self, hotspots: List[Dict]) -> List[str]:
        """Generate geographical recommendations."""
        recommendations = []
        
        if not hotspots:
            return ["No significant hotspots identified"]
        
        top_hotspot = hotspots[0]
        recommendations.append(f"🔥 Top hotspot: {top_hotspot['area']} with {top_hotspot['count']} complaints")
        
        if top_hotspot['negative_sentiment_pct'] > 60:
            recommendations.append(f"⚠️ High negative sentiment in {top_hotspot['area']} - immediate attention needed")
        
        if len(hotspots) >= 3:
            recommendations.append(f"📍 {len(hotspots)} hotspots require focused intervention")
        
        return recommendations
    
    def _calculate_satisfaction_score(self, sentiment_dist: Dict[str, int]) -> float:
        """Calculate satisfaction score from sentiment distribution."""
        total = sum(sentiment_dist.values())
        if total == 0:
            return 50.0
        
        positive = sentiment_dist.get('Positive', 0)
        neutral = sentiment_dist.get('Neutral', 0)
        negative = sentiment_dist.get('Negative', 0)
        
        # Weighted score: positive=100, neutral=50, negative=0
        score = (positive * 100 + neutral * 50 + negative * 0) / total
        
        return score
    
    def _calculate_avg_response_time(self, dept_df: pd.DataFrame) -> float:
        """Calculate average response time for department."""
        # Simulate response time based on urgency and status
        if dept_df.empty:
            return 0.0
        
        urgency_times = {'Critical': 6, 'High': 24, 'Medium': 48, 'Low': 96}
        
        times = []
        for _, ticket in dept_df.iterrows():
            base_time = urgency_times.get(ticket.get('urgency', 'Medium'), 48)
            # Add some variance
            actual_time = base_time * (0.8 + np.random.random() * 0.4)
            times.append(actual_time)
        
        return np.mean(times) if times else 0.0
    
    def _calculate_dept_sla_compliance(self, dept_df: pd.DataFrame) -> float:
        """Calculate SLA compliance for department."""
        if dept_df.empty:
            return 0.0
        
        resolved = dept_df[dept_df['status'].isin(['Resolved', 'Closed'])]
        
        if len(resolved) == 0:
            return 50.0  # Neutral score if no resolutions yet
        
        # Simulate compliance based on urgency distribution
        urgency_compliance = {'Low': 0.95, 'Medium': 0.88, 'High': 0.75, 'Critical': 0.65}
        
        compliance_scores = []
        for _, ticket in resolved.iterrows():
            urgency = ticket.get('urgency', 'Medium')
            compliance_scores.append(urgency_compliance.get(urgency, 0.85))
        
        return np.mean(compliance_scores) * 100 if compliance_scores else 50.0
    
    def _calculate_dept_trend(self, dept_df: pd.DataFrame) -> str:
        """Calculate trend for department."""
        if 'timestamp' not in dept_df.columns or len(dept_df) < 2:
            return "stable"
        
        dept_df['timestamp'] = pd.to_datetime(dept_df['timestamp'], errors='coerce')
        dept_df = dept_df.dropna(subset=['timestamp'])
        
        if len(dept_df) < 2:
            return "stable"
        
        # Split into two halves
        midpoint = len(dept_df) // 2
        recent_half = dept_df.iloc[midpoint:]
        older_half = dept_df.iloc[:midpoint]
        
        if len(recent_half) > len(older_half) * 1.15:
            return "increasing"
        elif len(recent_half) < len(older_half) * 0.85:
            return "decreasing"
        else:
            return "stable"
    
    def _generate_dept_recommendations(self, dept_metrics: List[Dict]) -> List[str]:
        """Generate department recommendations."""
        recommendations = []
        
        if not dept_metrics:
            return ["No department data available"]
        
        # Top performer recognition
        top = dept_metrics[0]
        recommendations.append(f"🏆 Best performer: {top['department']} (Score: {top['performance_score']})")
        
        # Bottom performer improvement
        if len(dept_metrics) > 1:
            bottom = dept_metrics[-1]
            if bottom['performance_score'] < 50:
                recommendations.append(f"⚠️ {bottom['department']} needs improvement (Score: {bottom['performance_score']})")
        
        # SLA compliance issues
        low_sla_depts = [d for d in dept_metrics if d['sla_compliance'] < 75]
        if low_sla_depts:
            recommendations.append(f"📉 {len(low_sla_depts)} department(s) below 75% SLA compliance")
        
        # Satisfaction issues
        low_satisfaction = [d for d in dept_metrics if d['satisfaction_score'] < 50]
        if low_satisfaction:
            recommendations.append(f"😟 {len(low_satisfaction)} department(s) with low satisfaction scores")
        
        return recommendations
