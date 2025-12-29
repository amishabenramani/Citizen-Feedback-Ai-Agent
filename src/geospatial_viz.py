"""
Geospatial Visualization Module
Provides interactive maps, heatmaps, and location-based analytics.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional
import numpy as np


class GeospatialVisualizer:
    """
    Geospatial visualization engine for creating interactive maps and heatmaps.
    Supports both coordinate-based and area-based visualizations.
    """
    
    def __init__(self):
        """Initialize the geospatial visualizer."""
        # Default map center (can be customized for your city)
        self.default_center = {'lat': 40.7128, 'lon': -74.0060}  # New York City default
        self.default_zoom = 10
        
        # Color schemes
        self.heatmap_colors = [
            [0, '#1e3a8a'],    # Deep blue
            [0.2, '#3b82f6'],  # Blue
            [0.4, '#06b6d4'],  # Cyan
            [0.6, '#fbbf24'],  # Amber
            [0.8, '#f97316'],  # Orange
            [1, '#dc2626']     # Red
        ]
        
        # Area to coordinates mapping (sample data - customize for your city)
        self.area_coordinates = self._initialize_area_coordinates()
    
    def _initialize_area_coordinates(self) -> Dict[str, Dict[str, float]]:
        """
        Initialize sample area coordinates.
        In production, this should be loaded from a database or geocoding service.
        """
        return {
            'Downtown': {'lat': 40.7589, 'lon': -73.9851},
            'Midtown': {'lat': 40.7549, 'lon': -73.9840},
            'Upper East Side': {'lat': 40.7736, 'lon': -73.9566},
            'Upper West Side': {'lat': 40.7870, 'lon': -73.9754},
            'Lower Manhattan': {'lat': 40.7080, 'lon': -74.0113},
            'Brooklyn': {'lat': 40.6782, 'lon': -73.9442},
            'Queens': {'lat': 40.7282, 'lon': -73.7949},
            'Bronx': {'lat': 40.8448, 'lon': -73.8648},
            'Staten Island': {'lat': 40.5795, 'lon': -74.1502},
            'East Village': {'lat': 40.7264, 'lon': -73.9818},
            'West Village': {'lat': 40.7358, 'lon': -74.0036},
            'Chelsea': {'lat': 40.7465, 'lon': -74.0014},
            'Harlem': {'lat': 40.8116, 'lon': -73.9465},
            'Financial District': {'lat': 40.7074, 'lon': -74.0113},
            'SoHo': {'lat': 40.7233, 'lon': -74.0030}
        }
    
    def create_complaint_heatmap(self, df: pd.DataFrame, map_style: str = 'open-street-map') -> go.Figure:
        """
        Create an interactive heatmap of complaint locations.
        
        Args:
            df: DataFrame with feedback data
            map_style: Map style ('open-street-map', 'carto-positron', 'carto-darkmatter')
            
        Returns:
            Plotly figure object
        """
        if df.empty:
            return self._create_empty_map("No data available for heatmap")
        
        # Prepare location data
        location_data = self._prepare_location_data(df)
        
        if not location_data:
            return self._create_empty_map("No location data available")
        
        # Create density mapbox
        fig = go.Figure()
        
        # Add density heatmap layer
        fig.add_trace(go.Densitymapbox(
            lat=location_data['lat'],
            lon=location_data['lon'],
            z=location_data['intensity'],
            radius=20,
            colorscale=self.heatmap_colors,
            showscale=True,
            colorbar=dict(
                title="Complaint<br>Density",
                thickness=15,
                len=0.7,
                bgcolor='rgba(17, 24, 39, 0.8)',
                tickfont=dict(color='#e2e8f0')
            ),
            hovertemplate='<b>Density: %{z}</b><extra></extra>'
        ))
        
        # Calculate map center
        center_lat = np.mean(location_data['lat'])
        center_lon = np.mean(location_data['lon'])
        
        # Update layout
        fig.update_layout(
            mapbox=dict(
                style=map_style,
                center=dict(lat=center_lat, lon=center_lon),
                zoom=self.default_zoom
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Inter, sans-serif'),
            title=dict(
                text="📍 Complaint Heatmap",
                font=dict(size=18, color='#e2e8f0'),
                x=0.5,
                xanchor='center'
            ),
            height=600
        )
        
        return fig
    
    def create_hotspot_map(self, df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Create a map showing complaint hotspots with markers.
        
        Args:
            df: DataFrame with feedback data
            top_n: Number of top hotspots to display
            
        Returns:
            Plotly figure object
        """
        if df.empty or 'area' not in df.columns:
            return self._create_empty_map("No area data available for hotspot map")
        
        # Aggregate by area
        area_counts = df['area'].value_counts().head(top_n)
        
        # Prepare data for markers
        marker_data = []
        for area, count in area_counts.items():
            coords = self.area_coordinates.get(area)
            if coords:
                area_data = df[df['area'] == area]
                
                # Calculate urgency distribution
                urgency_dist = area_data['urgency'].value_counts().to_dict() if 'urgency' in area_data.columns else {}
                
                # Calculate negative sentiment percentage
                neg_pct = 0
                if 'sentiment' in area_data.columns:
                    neg_pct = (area_data['sentiment'] == 'Negative').sum() / len(area_data) * 100
                
                # Determine marker size and color based on severity
                marker_size = min(count * 3, 50)
                marker_color = self._get_hotspot_color(count, neg_pct)
                
                marker_data.append({
                    'area': area,
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'count': count,
                    'negative_pct': round(neg_pct, 1),
                    'marker_size': marker_size,
                    'marker_color': marker_color,
                    'urgency_dist': urgency_dist
                })
        
        if not marker_data:
            return self._create_empty_map("No matching areas found in coordinate database")
        
        # Create figure
        fig = go.Figure()
        
        # Add markers
        for data in marker_data:
            hover_text = f"<b>{data['area']}</b><br>"
            hover_text += f"Complaints: {data['count']}<br>"
            hover_text += f"Negative Sentiment: {data['negative_pct']}%<br>"
            if data['urgency_dist']:
                hover_text += "Urgency: " + ", ".join([f"{k}: {v}" for k, v in data['urgency_dist'].items()])
            
            fig.add_trace(go.Scattermapbox(
                lat=[data['lat']],
                lon=[data['lon']],
                mode='markers',
                marker=dict(
                    size=data['marker_size'],
                    color=data['marker_color'],
                    opacity=0.7,
                    sizemode='diameter'
                ),
                text=data['area'],
                hovertemplate=hover_text + '<extra></extra>',
                name=data['area']
            ))
        
        # Calculate map center
        lats = [d['lat'] for d in marker_data]
        lons = [d['lon'] for d in marker_data]
        center_lat = np.mean(lats)
        center_lon = np.mean(lons)
        
        # Update layout
        fig.update_layout(
            mapbox=dict(
                style='open-street-map',
                center=dict(lat=center_lat, lon=center_lon),
                zoom=11
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Inter, sans-serif'),
            title=dict(
                text=f"🔥 Top {top_n} Complaint Hotspots",
                font=dict(size=18, color='#e2e8f0'),
                x=0.5,
                xanchor='center'
            ),
            showlegend=False,
            height=600
        )
        
        return fig
    
    def create_category_distribution_map(self, df: pd.DataFrame, category: Optional[str] = None) -> go.Figure:
        """
        Create a map showing distribution of specific category or all categories.
        
        Args:
            df: DataFrame with feedback data
            category: Specific category to filter (None for all)
            
        Returns:
            Plotly figure object
        """
        if df.empty or 'area' not in df.columns or 'category' not in df.columns:
            return self._create_empty_map("Insufficient data for category distribution map")
        
        # Filter by category if specified
        if category:
            df_filtered = df[df['category'] == category].copy()
            title = f"📊 {category} Distribution"
        else:
            df_filtered = df.copy()
            title = "📊 Category Distribution by Area"
        
        if df_filtered.empty:
            return self._create_empty_map(f"No data for category: {category}")
        
        # Aggregate by area
        area_data = []
        for area in df_filtered['area'].unique():
            coords = self.area_coordinates.get(area)
            if coords:
                area_complaints = df_filtered[df_filtered['area'] == area]
                count = len(area_complaints)
                
                # Get category breakdown
                cat_breakdown = area_complaints['category'].value_counts().head(3).to_dict()
                
                area_data.append({
                    'area': area,
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'count': count,
                    'categories': cat_breakdown
                })
        
        if not area_data:
            return self._create_empty_map("No matching areas found")
        
        # Create figure with bubble markers
        fig = go.Figure()
        
        for data in area_data:
            hover_text = f"<b>{data['area']}</b><br>Total: {data['count']}<br>"
            hover_text += "<br>".join([f"{k}: {v}" for k, v in data['categories'].items()])
            
            fig.add_trace(go.Scattermapbox(
                lat=[data['lat']],
                lon=[data['lon']],
                mode='markers+text',
                marker=dict(
                    size=min(data['count'] * 2, 40),
                    color='#8b5cf6',
                    opacity=0.6
                ),
                text=str(data['count']),
                textposition='middle center',
                textfont=dict(color='white', size=10, family='Inter'),
                hovertemplate=hover_text + '<extra></extra>',
                name=data['area']
            ))
        
        # Calculate center
        lats = [d['lat'] for d in area_data]
        lons = [d['lon'] for d in area_data]
        
        fig.update_layout(
            mapbox=dict(
                style='carto-darkmatter',
                center=dict(lat=np.mean(lats), lon=np.mean(lons)),
                zoom=11
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Inter, sans-serif'),
            title=dict(
                text=title,
                font=dict(size=18, color='#e2e8f0'),
                x=0.5,
                xanchor='center'
            ),
            showlegend=False,
            height=600
        )
        
        return fig
    
    def create_temporal_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """
        Create a temporal heatmap showing complaint patterns over time and location.
        
        Args:
            df: DataFrame with feedback data
            
        Returns:
            Plotly figure object
        """
        if df.empty or 'area' not in df.columns or 'timestamp' not in df.columns:
            return self._create_empty_figure("Insufficient data for temporal heatmap")
        
        # Prepare data
        df_copy = df.copy()
        df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'], errors='coerce')
        df_copy = df_copy.dropna(subset=['timestamp'])
        
        if df_copy.empty:
            return self._create_empty_figure("No valid timestamp data")
        
        # Extract hour and day of week
        df_copy['hour'] = df_copy['timestamp'].dt.hour
        df_copy['day_of_week'] = df_copy['timestamp'].dt.day_name()
        
        # Create pivot table
        pivot = df_copy.pivot_table(
            values='id', 
            index='day_of_week', 
            columns='hour', 
            aggfunc='count', 
            fill_value=0
        )
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot = pivot.reindex([d for d in day_order if d in pivot.index])
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale=self.heatmap_colors,
            hovertemplate='<b>%{y}</b><br>Hour: %{x}<br>Complaints: %{z}<extra></extra>',
            colorbar=dict(
                title="Count",
                thickness=15,
                len=0.7,
                bgcolor='rgba(17, 24, 39, 0.8)',
                tickfont=dict(color='#e2e8f0')
            )
        ))
        
        fig.update_layout(
            title=dict(
                text="⏰ Complaint Patterns by Day & Hour",
                font=dict(size=18, color='#e2e8f0'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title="Hour of Day",
                tickfont=dict(color='#e2e8f0'),
                gridcolor='rgba(139, 92, 246, 0.1)'
            ),
            yaxis=dict(
                title="Day of Week",
                tickfont=dict(color='#e2e8f0'),
                gridcolor='rgba(139, 92, 246, 0.1)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Inter, sans-serif'),
            height=400,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    # Helper methods
    
    def _prepare_location_data(self, df: pd.DataFrame) -> Dict[str, List]:
        """Prepare location data for mapping."""
        location_data = {'lat': [], 'lon': [], 'intensity': []}
        
        if 'area' in df.columns:
            # Use area-based coordinates
            area_counts = df['area'].value_counts()
            
            for area, count in area_counts.items():
                coords = self.area_coordinates.get(area)
                if coords:
                    # Add some jitter to show density
                    for _ in range(min(count, 50)):  # Limit points per area
                        lat_jitter = np.random.normal(0, 0.01)
                        lon_jitter = np.random.normal(0, 0.01)
                        location_data['lat'].append(coords['lat'] + lat_jitter)
                        location_data['lon'].append(coords['lon'] + lon_jitter)
                        location_data['intensity'].append(count / 10)
        
        elif 'latitude' in df.columns and 'longitude' in df.columns:
            # Use actual coordinates if available
            df_coords = df.dropna(subset=['latitude', 'longitude'])
            location_data['lat'] = df_coords['latitude'].tolist()
            location_data['lon'] = df_coords['longitude'].tolist()
            location_data['intensity'] = [1] * len(df_coords)
        
        return location_data
    
    def _get_hotspot_color(self, count: int, negative_pct: float) -> str:
        """Determine marker color based on severity."""
        if count > 20 or negative_pct > 70:
            return '#dc2626'  # Red
        elif count > 10 or negative_pct > 50:
            return '#f97316'  # Orange
        elif count > 5 or negative_pct > 30:
            return '#fbbf24'  # Amber
        else:
            return '#10b981'  # Green
    
    def _create_empty_map(self, message: str) -> go.Figure:
        """Create empty map with message."""
        fig = go.Figure()
        
        fig.add_trace(go.Scattermapbox(
            lat=[self.default_center['lat']],
            lon=[self.default_center['lon']],
            mode='text',
            text=[message],
            textfont=dict(size=16, color='#e2e8f0')
        ))
        
        fig.update_layout(
            mapbox=dict(
                style='open-street-map',
                center=self.default_center,
                zoom=self.default_zoom
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            height=600,
            title=dict(
                text="📍 Map View",
                font=dict(size=18, color='#e2e8f0'),
                x=0.5,
                xanchor='center'
            )
        )
        
        return fig
    
    def _create_empty_figure(self, message: str) -> go.Figure:
        """Create empty figure with message."""
        fig = go.Figure()
        
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color='#94a3b8')
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        
        return fig
    
    def update_area_coordinates(self, area_coords: Dict[str, Dict[str, float]]):
        """
        Update or add area coordinates.
        
        Args:
            area_coords: Dictionary mapping area names to {'lat': float, 'lon': float}
        """
        self.area_coordinates.update(area_coords)
    
    def set_map_center(self, lat: float, lon: float, zoom: int = 10):
        """
        Set default map center and zoom level.
        
        Args:
            lat: Latitude
            lon: Longitude
            zoom: Zoom level (1-20)
        """
        self.default_center = {'lat': lat, 'lon': lon}
        self.default_zoom = zoom
