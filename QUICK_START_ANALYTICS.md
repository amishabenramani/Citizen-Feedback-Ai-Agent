# Quick Start Guide - Advanced Analytics

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -e .
```

This will install numpy and all required packages.

### 2. Run the Application
```bash
# Start Admin Portal
python admin_portal.py

# Or use Streamlit directly
streamlit run admin_portal.py
```

### 3. Access Advanced Analytics

1. Login to Admin Portal (default: admin/admin123)
2. Navigate to **Analytics** in the sidebar
3. Select **"🚀 Advanced Analytics"** at the top

## 📊 Features at a Glance

### Five Main Tabs:

#### 📈 **Trend Analysis**
- View weekly/monthly feedback trends
- See 4-period forecast
- Monitor sentiment changes
- Track category trends

**Quick Actions:**
- Change time period (daily/weekly/monthly)
- Review growth rate
- Check forecast predictions

---

#### ⚠️ **SLA Monitoring**
- See breached tickets
- View at-risk tickets with breach probability
- Check compliance percentage
- Get recommendations

**Quick Actions:**
- Address breached tickets immediately
- Prioritize high-risk tickets
- Monitor compliance trends

---

#### 🗺️ **Geospatial Heatmap**
- View complaint density heatmap
- Identify top 10 hotspots
- See category distribution by area
- Check temporal patterns

**Quick Actions:**
- Select map type (Heatmap/Hotspots/Category)
- Review hotspot scores
- Focus resources on high-priority areas

---

#### 🏢 **Department Performance**
- Compare all departments
- View top/bottom performers
- Check detailed metrics
- See performance trends

**Quick Actions:**
- Review overall performance score
- Expand departments for details
- Identify improvement areas

---

#### ⏰ **Time Patterns**
- Analyze day/hour patterns
- View hourly distribution
- Identify peak times

**Quick Actions:**
- Schedule staff based on patterns
- Optimize response times

## 💡 Common Use Cases

### Use Case 1: Daily Operations Check
```
1. Go to SLA Monitoring tab
2. Check breached tickets → Take immediate action
3. Review at-risk tickets → Prioritize
4. Note compliance percentage
```

### Use Case 2: Weekly Planning
```
1. Go to Trend Analysis tab
2. Select "weekly" period
3. Review forecast for next 4 weeks
4. Plan resources accordingly
```

### Use Case 3: Geographic Resource Allocation
```
1. Go to Geospatial Heatmap tab
2. Select "Hotspots" map type
3. Review top 10 hotspot areas
4. Deploy teams to high-score areas
```

### Use Case 4: Department Review
```
1. Go to Department Performance tab
2. Check overall performance score
3. Review bottom performers
4. Create improvement plans
```

## 🎯 Key Metrics Explained

### Performance Score (0-100)
Composite metric based on:
- **30%** Resolution Rate
- **30%** Satisfaction Score
- **25%** SLA Compliance
- **15%** Response Time

### Hotspot Score
Calculated as:
```
Count × Avg Urgency × (1 + Negative Sentiment %)
```
Higher score = Higher priority

### Breach Probability (0-100%)
Predictions based on:
- Time remaining vs. SLA target
- Ticket urgency level
- Historical patterns

### SLA Targets
- **Critical**: 4 hours
- **High**: 24 hours
- **Medium**: 72 hours
- **Low**: 168 hours

## 🔧 Quick Customization

### Change SLA Targets
Edit `src/advanced_analytics.py`:
```python
self.sla_config = {
    'Critical': 4,   # Change to your target
    'High': 24,
    'Medium': 72,
    'Low': 168
}
```

### Update Area Coordinates
Edit `src/geospatial_viz.py`:
```python
self.area_coordinates = {
    'Your Area': {'lat': 40.7589, 'lon': -73.9851},
    # Add more areas...
}
```

### Customize Department Mapping
Edit `src/advanced_analytics.py`:
```python
self.department_mapping = {
    'Your Category': 'Your Department',
    # Add more mappings...
}
```

## 📱 Tips for Best Results

1. **Keep Data Updated**: Ensure timestamps and statuses are current
2. **Add Location Data**: Include area/latitude/longitude in feedback
3. **Regular Monitoring**: Check SLA tab daily
4. **Act on Insights**: Use recommendations to guide actions
5. **Compare Periods**: Track improvements over time

## 🐛 Troubleshooting

**Issue**: No data in analytics
- **Solution**: Ensure you have submitted some feedback first

**Issue**: Empty maps
- **Solution**: Add 'area' field to feedback submissions

**Issue**: Incorrect forecasts
- **Solution**: Need at least 7 days of historical data

**Issue**: Department metrics not showing
- **Solution**: Ensure 'category' field is populated

## 📞 Need Help?

1. Check `ADVANCED_ANALYTICS.md` for detailed documentation
2. Review inline docstrings in source files
3. Look at example outputs in documentation

## 🎉 You're Ready!

Start exploring your data with advanced analytics and make data-driven decisions!

---

**Quick Reference Commands:**

```bash
# Install
pip install -e .

# Run
python admin_portal.py

# Access
http://localhost:8501
```

**Navigation:**
Analytics → 🚀 Advanced Analytics → Choose Tab

**Key Shortcut:**
Press `Ctrl+R` (or `Cmd+R` on Mac) to refresh Streamlit app
