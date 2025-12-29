# Advanced Analytics & Decision Support

## 🚀 Overview

The Citizen Feedback AI Agent now includes comprehensive **Advanced Analytics & Decision Support** capabilities that go beyond simple charts to provide actionable insights, predictions, and intelligent recommendations.

## ✨ Key Features

### 1️⃣ **Smart Dashboards**

Access advanced analytics through the Admin Portal under the **Analytics** section with three view modes:
- 🚀 **Advanced Analytics** - Comprehensive insights dashboard
- 📊 **Standard Analytics** - Traditional charts and metrics
- 📋 **Data Tables** - Detailed statistical breakdowns

### 2️⃣ **Heatmap of Complaint Locations**

#### Interactive Geospatial Visualization
- **Density Heatmap**: Visualize complaint concentration across different areas
- **Hotspot Map**: Identify top complaint areas with severity indicators
- **Category Distribution Map**: View specific category distribution geographically
- **Temporal Heatmap**: Analyze complaint patterns by day and hour

#### Features:
- Color-coded intensity showing complaint density
- Multiple map styles (OpenStreetMap, Carto Positron, Carto Dark)
- Interactive tooltips with detailed information
- Customizable area coordinates for your city

**Usage:**
```python
from src.geospatial_viz import GeospatialVisualizer

geo_viz = GeospatialVisualizer()

# Create complaint heatmap
fig = geo_viz.create_complaint_heatmap(df, map_style='open-street-map')

# Create hotspot map
fig = geo_viz.create_hotspot_map(df, top_n=10)

# Category-specific distribution
fig = geo_viz.create_category_distribution_map(df, category='Roads & Transportation')
```

### 3️⃣ **Trend Analysis (Weekly/Monthly)**

#### Intelligent Time-Series Analytics
- **Multiple time periods**: Daily, Weekly, Monthly views
- **Historical trends**: Track feedback volume over time
- **Sentiment trends**: Monitor sentiment changes
- **Category trends**: Analyze top category patterns
- **Growth rate calculation**: Understand momentum
- **4-period forecast**: Predict future volumes using moving averages

#### Key Metrics:
- Total feedback trend with growth rate percentage
- Sentiment distribution over time
- Category-specific trend lines
- Automated trend summaries

**Usage:**
```python
from src.advanced_analytics import AdvancedAnalytics

analytics = AdvancedAnalytics()

# Get trend analysis
trends = analytics.calculate_trends(df, period='weekly')

print(trends['summary'])
# Output: "Feedback volume is increasing (+15.2%). Average: 45 submissions per period."

# Access forecast data
for forecast in trends['forecast']:
    print(f"{forecast['period']}: {forecast['predicted_value']} submissions")
```

### 4️⃣ **SLA Breach Prediction**

#### Proactive Service Level Management
- **Real-time monitoring**: Track all open tickets against SLA targets
- **Breach prediction**: ML-based probability scoring for at-risk tickets
- **Automatic classification**: Identify breached vs. at-risk tickets
- **Historical performance**: SLA compliance tracking
- **Smart recommendations**: Actionable insights for prevention

#### SLA Targets:
- **Critical**: 4 hours
- **High**: 24 hours
- **Medium**: 72 hours
- **Low**: 168 hours (7 days)

#### Prediction Features:
- Hours remaining until SLA breach
- Breach probability percentage (0-100%)
- Recommended actions based on risk level
- Escalation flags for urgent cases

**Usage:**
```python
# Get SLA breach predictions
sla_data = analytics.predict_sla_breaches(df)

print(f"Breached: {sla_data['breach_count']}")
print(f"At Risk: {sla_data['at_risk_count']}")
print(f"Compliance: {sla_data['sla_performance']['compliant']}%")

# Review at-risk tickets
for ticket in sla_data['at_risk_tickets']:
    print(f"{ticket['title']}: {ticket['breach_probability']}% risk")
    print(f"Action: {ticket['recommended_action']}")
```

### 5️⃣ **Department-wise Performance**

#### Comprehensive Performance Metrics
- **Performance scoring**: Composite metric (0-100) based on:
  - Resolution rate (30%)
  - Satisfaction score (30%)
  - SLA compliance (25%)
  - Response time (15%)
- **Department comparison**: Visual rankings and benchmarks
- **Detailed breakdowns**: Individual department metrics
- **Trend indicators**: Increasing, stable, or decreasing
- **Top/bottom performers**: Identify best practices and improvement areas

#### Metrics Tracked:
- Total tickets handled
- Resolution rate percentage
- Customer satisfaction score (0-100)
- Average response time (hours)
- SLA compliance percentage
- Sentiment distribution
- Performance trend

**Department Mapping:**
```python
{
    'Roads & Transportation': 'Infrastructure',
    'Water & Sanitation': 'Utilities',
    'Public Safety': 'Safety',
    'Healthcare': 'Health',
    'Education': 'Education',
    'Environment': 'Environment',
    'Street Lighting': 'Infrastructure',
    'Waste Management': 'Environment',
    # ... customizable
}
```

**Usage:**
```python
# Get department performance
dept_data = analytics.analyze_department_performance(df)

print(f"Overall Performance: {dept_data['overall_avg_performance']}/100")

# Top performer
top = dept_data['top_performer']
print(f"Best: {top['department']} - Score: {top['performance_score']}")

# Review all departments
for dept in dept_data['department_metrics']:
    print(f"{dept['department']}: {dept['performance_score']}/100")
    print(f"  Resolution: {dept['resolution_rate']}%")
    print(f"  Satisfaction: {dept['satisfaction_score']}/100")
    print(f"  SLA Compliance: {dept['sla_compliance']}%")
```

## 📊 Analytics Dashboard Components

### Trend Analysis Tab
- Overall volume trend chart with forecast
- Sentiment trends over time
- Top category trends
- Growth rate indicators
- Automated insights

### SLA Monitoring Tab
- Key metrics cards (Breached, At Risk, Compliance)
- Breached tickets list with overdue hours
- At-risk tickets with breach probability
- Recommendations and action items

### Geospatial Heatmap Tab
- Interactive map selector
- Location hotspot analysis
- Severity scoring
- Category distribution by area
- Geospatial recommendations

### Department Performance Tab
- Overall performance gauge
- Top/bottom performer cards
- Comparative performance chart
- Detailed department metrics
- Expandable department details

### Time Patterns Tab
- Day/hour heatmap
- Hourly submission distribution
- Peak time identification
- Pattern insights

## 🛠️ Technical Implementation

### Core Modules

#### `src/advanced_analytics.py`
The main analytics engine providing:
- `calculate_trends()` - Time series analysis and forecasting
- `predict_sla_breaches()` - SLA monitoring and predictions
- `analyze_geospatial_distribution()` - Location-based analytics
- `analyze_department_performance()` - Department metrics

#### `src/geospatial_viz.py`
Geospatial visualization engine:
- `create_complaint_heatmap()` - Density heatmaps
- `create_hotspot_map()` - Hotspot visualization
- `create_category_distribution_map()` - Category mapping
- `create_temporal_heatmap()` - Time-based patterns

#### `src/dashboard.py`
Enhanced dashboard with:
- `render_advanced_analytics_dashboard()` - Main analytics UI
- `render_trend_analysis()` - Trend visualizations
- `render_sla_monitoring()` - SLA dashboard
- `render_geospatial_analysis()` - Map visualizations
- `render_department_performance()` - Department metrics
- `render_temporal_patterns()` - Time pattern analysis

### Database Schema Updates

The `Feedback` model now includes:
```python
latitude = Column(Float, index=True)   # Geographic latitude
longitude = Column(Float, index=True)  # Geographic longitude
```

This enables precise location tracking and mapping.

## 📦 Dependencies

Updated `pyproject.toml` includes:
- `numpy>=1.24.0` - Numerical computations
- `plotly>=5.18.0` - Interactive visualizations
- `pandas>=2.0.0` - Data analysis
- `streamlit>=1.28.0` - Web interface

Install with:
```bash
pip install -e .
```

## 🎨 Visualization Tools

### Plotly Charts
- Interactive line charts for trends
- Bar charts for comparisons
- Donut/pie charts for distributions
- Heatmaps for patterns
- Geographic maps for spatial data

### Color Schemes
- **Success**: `#10B981` (Green)
- **Warning**: `#F59E0B` (Amber)
- **Danger**: `#EF4444` (Red)
- **Primary**: `#8b5cf6` (Purple)
- **Info**: `#3b82f6` (Blue)

## 🗺️ Geospatial Configuration

### Setting Up Area Coordinates

Update area coordinates for your city:

```python
from src.geospatial_viz import GeospatialVisualizer

geo_viz = GeospatialVisualizer()

# Add your city's areas
area_coords = {
    'Downtown': {'lat': 40.7589, 'lon': -73.9851},
    'Suburbs': {'lat': 40.8589, 'lon': -73.8851},
    'Industrial Zone': {'lat': 40.6589, 'lon': -74.0851},
}

geo_viz.update_area_coordinates(area_coords)

# Set map center
geo_viz.set_map_center(lat=40.7589, lon=-73.9851, zoom=11)
```

### Adding Coordinates to Feedback

When collecting feedback, optionally include coordinates:

```python
feedback = {
    'area': 'Downtown',
    'latitude': 40.7589,
    'longitude': -73.9851,
    # ... other fields
}
```

## 🚀 Getting Started

### 1. Access Advanced Analytics

```python
# In admin_portal.py
python admin_portal.py
```

Navigate to **Analytics** → Select **"🚀 Advanced Analytics"**

### 2. Use in Custom Scripts

```python
from src.data_manager import DataManager
from src.advanced_analytics import AdvancedAnalytics
from src.geospatial_viz import GeospatialVisualizer

# Initialize
data_manager = DataManager()
analytics = AdvancedAnalytics()
geo_viz = GeospatialVisualizer()

# Get data
df = data_manager.get_feedback_dataframe()

# Run analytics
trends = analytics.calculate_trends(df, period='weekly')
sla = analytics.predict_sla_breaches(df)
geo = analytics.analyze_geospatial_distribution(df)
dept = analytics.analyze_department_performance(df)

# Create visualizations
heatmap = geo_viz.create_complaint_heatmap(df)
hotspots = geo_viz.create_hotspot_map(df)
```

## 📈 Performance Insights

### Trend Analysis Insights
- Identify growth or decline in feedback volume
- Predict future volumes for resource planning
- Monitor sentiment shifts over time
- Track category-specific trends

### SLA Management Benefits
- **Proactive**: Prevent breaches before they happen
- **Prioritization**: Focus on high-risk tickets
- **Accountability**: Track compliance metrics
- **Optimization**: Improve response workflows

### Geospatial Benefits
- **Resource Allocation**: Deploy teams to hotspots
- **Pattern Recognition**: Identify problem areas
- **Trend Mapping**: Visualize geographic trends
- **Planning**: Data-driven infrastructure decisions

### Department Insights
- **Benchmarking**: Compare department performance
- **Best Practices**: Learn from top performers
- **Improvement Areas**: Target low-performing departments
- **Holistic View**: Understand organizational performance

## 🎯 Use Cases

### 1. City Operations Manager
- Monitor SLA compliance across departments
- Identify geographic hotspots requiring attention
- Allocate resources based on trend predictions
- Track department performance metrics

### 2. Department Head
- Review your department's performance score
- Identify improvement opportunities
- Benchmark against other departments
- Track resolution rates and satisfaction

### 3. Data Analyst
- Extract trends and patterns
- Generate reports and insights
- Forecast future volumes
- Analyze geospatial distributions

### 4. Executive Leadership
- High-level performance overview
- Strategic decision support
- Resource allocation guidance
- Long-term trend analysis

## 🔧 Customization

### Adjust SLA Targets

```python
analytics = AdvancedAnalytics()
analytics.sla_config = {
    'Critical': 2,   # 2 hours
    'High': 12,      # 12 hours
    'Medium': 48,    # 48 hours
    'Low': 120       # 120 hours
}
```

### Customize Department Mapping

```python
analytics.department_mapping = {
    'Your Category': 'Your Department',
    'Roads': 'Public Works',
    # ... etc
}
```

### Modify Color Schemes

```python
dashboard = Dashboard()
dashboard.sentiment_colors = {
    'Positive': '#00ff00',
    'Neutral': '#ffff00',
    'Negative': '#ff0000'
}
```

## 📊 Sample Outputs

### Trend Analysis
```
Feedback volume is increasing (+15.2%). Average: 45 submissions per period.
Forecast: Period 1: 52 | Period 2: 54 | Period 3: 53 | Period 4: 55
```

### SLA Monitoring
```
Breached: 3 tickets
At Risk: 7 tickets
Compliance: 87.5%

Recommendations:
⚠️ 3 ticket(s) have breached SLA - immediate action required
👀 Monitor 7 at-risk ticket(s)
```

### Geospatial Analysis
```
Top Hotspots:
1. Downtown - 45 complaints (Score: 156.3)
2. Industrial Area - 32 complaints (Score: 98.5)
3. Suburb A - 28 complaints (Score: 75.2)

🔥 Top hotspot: Downtown with 45 complaints
⚠️ High negative sentiment in Downtown - immediate attention needed
```

### Department Performance
```
Overall Performance: 72.5/100

Top Performer: Infrastructure (Score: 88.2)
- Resolution: 92%
- Satisfaction: 85/100
- SLA Compliance: 91%

Needs Improvement: Administration (Score: 58.4)
- Resolution: 68%
- Satisfaction: 52/100
- SLA Compliance: 72%
```

## 🎓 Best Practices

1. **Regular Monitoring**: Check analytics daily/weekly
2. **Act on Predictions**: Address at-risk SLA tickets proactively
3. **Resource Planning**: Use forecasts for staffing decisions
4. **Geographic Focus**: Prioritize hotspot areas
5. **Department Support**: Help low-performing departments improve
6. **Data Quality**: Ensure accurate location and timestamp data
7. **Customization**: Adjust thresholds and mappings for your context

## 🆘 Support

For issues or questions:
- Check the main README.md
- Review module docstrings
- Inspect example outputs
- Test with sample data

## 🔄 Future Enhancements

Potential additions:
- Machine learning for better predictions
- Real-time geocoding integration
- Automated report generation
- Email/SMS alerts for SLA breaches
- Advanced forecasting models (ARIMA, Prophet)
- Multi-city support
- API endpoints for analytics
- Custom dashboard builder

---

**Version**: 2.0
**Last Updated**: December 2025
**Modules**: `advanced_analytics.py`, `geospatial_viz.py`, `dashboard.py`
