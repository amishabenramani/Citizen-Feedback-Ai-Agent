# 🧪 Testing Guide - Advanced Analytics

## Quick Test Checklist

Use this guide to verify that all advanced analytics features are working correctly.

## ✅ Pre-Testing Setup

### 1. Install Dependencies
```bash
python setup_analytics.py
# or manually:
pip install -e .
```

### 2. Start Application
```bash
python admin_portal.py
```

### 3. Login
```
Username: admin
Password: admin123
```

### 4. Ensure Sample Data Exists
You need at least 10-20 feedback entries with varied data:
- Different areas/locations
- Different categories
- Different timestamps (spread over days/weeks)
- Different sentiments
- Different urgency levels
- Different statuses

## 🧪 Test Suite

### TEST 1: Navigation & UI
**Objective:** Verify basic navigation works

**Steps:**
1. ✓ Login to Admin Portal
2. ✓ Click "Analytics" in sidebar
3. ✓ See three radio options: Advanced, Standard, Data Tables
4. ✓ Select "🚀 Advanced Analytics"
5. ✓ Verify 5 tabs appear: Trend Analysis, SLA Monitoring, Geospatial Heatmap, Department Performance, Time Patterns

**Expected Result:** All UI elements load without errors

**Status:** ☐ Pass ☐ Fail

---

### TEST 2: Trend Analysis Tab
**Objective:** Test trend visualization and forecasting

**Steps:**
1. ✓ Click "📊 Trend Analysis" tab
2. ✓ Change period selector: daily → weekly → monthly
3. ✓ Verify trend chart updates
4. ✓ Check forecast section shows 4 periods
5. ✓ Verify sentiment trends chart appears
6. ✓ Check category trends chart appears
7. ✓ Read trend summary text

**Expected Results:**
- Charts render without errors
- Different periods show different aggregations
- Forecast values are reasonable
- Summary text is informative

**Status:** ☐ Pass ☐ Fail

**Notes:**
```
Chart displayed: Yes / No
Forecast shown: Yes / No
Summary accurate: Yes / No
```

---

### TEST 3: SLA Monitoring Tab
**Objective:** Test SLA prediction and monitoring

**Steps:**
1. ✓ Click "⚠️ SLA Monitoring" tab
2. ✓ Check three metric cards:
   - Breached SLAs
   - At Risk
   - SLA Compliance %
3. ✓ Verify recommendations appear
4. ✓ Check breached tickets section
5. ✓ Check at-risk tickets section
6. ✓ Verify probability percentages are shown
7. ✓ Verify recommended actions are displayed

**Expected Results:**
- Metrics calculate correctly
- Tickets are categorized properly
- Probability scores are between 0-100%
- Recommendations are actionable

**Status:** ☐ Pass ☐ Fail

**Notes:**
```
Breached count: ___
At-risk count: ___
Compliance %: ___
Probabilities reasonable: Yes / No
```

---

### TEST 4: Geospatial Heatmap Tab
**Objective:** Test map visualizations

**Steps:**
1. ✓ Click "🗺️ Geospatial Heatmap" tab
2. ✓ Select "Heatmap" map type
3. ✓ Verify map loads with markers/density
4. ✓ Select "Hotspots" map type
5. ✓ Verify top hotspots appear
6. ✓ Check hotspot cards below map
7. ✓ Select "Category Distribution" map type
8. ✓ Choose a category from dropdown
9. ✓ Verify map updates
10. ✓ Check recommendations section

**Expected Results:**
- All three map types render
- Maps are interactive (pan/zoom)
- Hotspot cards show scores
- Category filtering works
- Tooltips appear on hover

**Status:** ☐ Pass ☐ Fail

**Notes:**
```
Heatmap loaded: Yes / No
Hotspots visible: Yes / No
Category filter works: Yes / No
Map interactive: Yes / No
```

---

### TEST 5: Department Performance Tab
**Objective:** Test department analytics

**Steps:**
1. ✓ Click "🏢 Department Performance" tab
2. ✓ Check overall performance score card
3. ✓ Verify top performer card
4. ✓ Verify bottom performer card (if >1 dept)
5. ✓ Check horizontal bar chart comparison
6. ✓ Expand each department details
7. ✓ Verify 4 metrics shown per department:
   - Total Tickets
   - Resolution Rate
   - Satisfaction
   - SLA Compliance
8. ✓ Check recommendations section

**Expected Results:**
- Overall score calculated correctly (0-100)
- Top/bottom performers identified
- Comparison chart shows all departments
- Individual metrics are accurate
- Expandable sections work

**Status:** ☐ Pass ☐ Fail

**Notes:**
```
Overall score: ___/100
Top performer: ___________
Department count: ___
All metrics visible: Yes / No
```

---

### TEST 6: Time Patterns Tab
**Objective:** Test temporal analysis

**Steps:**
1. ✓ Click "⏰ Time Patterns" tab
2. ✓ Verify day/hour heatmap appears
3. ✓ Check heatmap has 7 rows (days)
4. ✓ Check heatmap has 24 columns (hours)
5. ✓ Verify color intensity varies
6. ✓ Check hourly distribution bar chart
7. ✓ Hover over cells to see tooltips

**Expected Results:**
- Heatmap renders correctly
- Days ordered Monday-Sunday
- Hours ordered 0-23
- Color scale represents complaint count
- Bar chart shows hourly totals
- Tooltips show day, hour, and count

**Status:** ☐ Pass ☐ Fail

**Notes:**
```
Heatmap displayed: Yes / No
Days visible: ___
Hours visible: ___
Bar chart shown: Yes / No
```

---

### TEST 7: Standard Analytics View
**Objective:** Test backward compatibility

**Steps:**
1. ✓ Return to Analytics page
2. ✓ Select "📊 Standard Analytics" radio button
3. ✓ Verify standard charts appear:
   - Sentiment donut chart
   - Category bar chart
   - Urgency bar chart
   - Status pie chart
   - Timeline chart
   - Category vs Sentiment heatmap
4. ✓ Check response metrics at bottom

**Expected Results:**
- All standard charts still work
- No errors or broken visualizations
- Metrics calculate correctly

**Status:** ☐ Pass ☐ Fail

---

### TEST 8: Data Tables View
**Objective:** Test tabular data display

**Steps:**
1. ✓ Select "📋 Data Tables" radio button
2. ✓ Check three statistics tables:
   - By Category
   - By Urgency
   - By Status
3. ✓ Verify location statistics table (if area data exists)

**Expected Results:**
- All tables display data
- Counts are accurate
- Tables are sortable/readable

**Status:** ☐ Pass ☐ Fail

---

### TEST 9: Performance Test
**Objective:** Test with larger datasets

**Steps:**
1. ✓ Use dataset with 50+ entries
2. ✓ Navigate through all tabs
3. ✓ Measure page load times
4. ✓ Check for any lag or freezing
5. ✓ Verify charts render smoothly

**Expected Results:**
- All tabs load in < 5 seconds
- No UI freezing
- Charts render without delay
- Interactions remain smooth

**Status:** ☐ Pass ☐ Fail

**Performance Notes:**
```
Tab load time: ___ seconds
Chart render time: ___ seconds
Smooth interactions: Yes / No
```

---

### TEST 10: Error Handling
**Objective:** Test with edge cases

**Steps:**
1. ✓ Test with empty dataset (no feedback)
2. ✓ Test with minimal data (1-2 entries)
3. ✓ Test with missing fields (no area, no category)
4. ✓ Test with all tickets resolved (no open SLA)
5. ✓ Verify appropriate messages appear

**Expected Results:**
- Empty data shows "No data available" message
- Missing fields show "Insufficient data" message
- App doesn't crash
- Helpful error messages displayed

**Status:** ☐ Pass ☐ Fail

**Error Messages:**
```
Empty data handled: Yes / No
Missing fields handled: Yes / No
Appropriate messages: Yes / No
```

---

## 📊 Test Results Summary

Fill in after completing all tests:

| Test # | Feature | Status | Notes |
|--------|---------|--------|-------|
| 1 | Navigation & UI | ☐ Pass ☐ Fail | |
| 2 | Trend Analysis | ☐ Pass ☐ Fail | |
| 3 | SLA Monitoring | ☐ Pass ☐ Fail | |
| 4 | Geospatial Heatmap | ☐ Pass ☐ Fail | |
| 5 | Department Performance | ☐ Pass ☐ Fail | |
| 6 | Time Patterns | ☐ Pass ☐ Fail | |
| 7 | Standard Analytics | ☐ Pass ☐ Fail | |
| 8 | Data Tables | ☐ Pass ☐ Fail | |
| 9 | Performance | ☐ Pass ☐ Fail | |
| 10 | Error Handling | ☐ Pass ☐ Fail | |

**Overall Pass Rate:** ___/10 (___%)

---

## 🐛 Common Issues & Solutions

### Issue: Map not loading
**Solution:** 
- Check internet connection (maps need external resources)
- Verify Plotly is installed: `pip install plotly`
- Clear browser cache

### Issue: No data in charts
**Solution:**
- Ensure feedback data exists
- Check required fields are populated (timestamp, category, status)
- Verify database connection

### Issue: SLA predictions showing 0%
**Solution:**
- Ensure tickets have status = 'New', 'In Review', or 'In Progress'
- Check urgency field is populated
- Verify timestamp field exists

### Issue: Department performance not showing
**Solution:**
- Ensure category field is populated
- Check department mapping in `src/advanced_analytics.py`
- Add your categories to mapping

### Issue: Heatmap shows no locations
**Solution:**
- Ensure area field is populated in feedback
- Add area coordinates in `src/geospatial_viz.py`
- Or add latitude/longitude to feedback entries

### Issue: Charts render slowly
**Solution:**
- Reduce dataset size (filter by date range)
- Close other browser tabs
- Check system resources

---

## 🔧 Manual Testing Commands

### Test Advanced Analytics Module
```python
from src.advanced_analytics import AdvancedAnalytics
from src.data_manager import DataManager

# Initialize
dm = DataManager()
analytics = AdvancedAnalytics()

# Get data
df = dm.get_feedback_dataframe()

# Test each function
trends = analytics.calculate_trends(df, period='weekly')
print("Trends:", trends['summary'])

sla = analytics.predict_sla_breaches(df)
print("SLA Breaches:", sla['breach_count'])

geo = analytics.analyze_geospatial_distribution(df)
print("Hotspots:", len(geo['location_hotspots']))

dept = analytics.analyze_department_performance(df)
print("Departments:", len(dept['department_metrics']))
```

### Test Geospatial Module
```python
from src.geospatial_viz import GeospatialVisualizer
from src.data_manager import DataManager

# Initialize
dm = DataManager()
geo_viz = GeospatialVisualizer()

# Get data
df = dm.get_feedback_dataframe()

# Test maps
heatmap = geo_viz.create_complaint_heatmap(df)
hotspot_map = geo_viz.create_hotspot_map(df)
temporal = geo_viz.create_temporal_heatmap(df)

print("Maps created successfully!")
```

---

## 📝 Test Report Template

```
ADVANCED ANALYTICS TEST REPORT
==============================

Date: _______________
Tester: _______________
Version: 2.0

ENVIRONMENT:
- Python Version: _______________
- OS: _______________
- Browser: _______________
- Database: PostgreSQL

DATASET:
- Total Feedback Entries: ___
- Date Range: ___ to ___
- Categories: ___
- Areas: ___

TEST RESULTS:
[Paste summary table here]

ISSUES FOUND:
1. _______________
2. _______________
3. _______________

RECOMMENDATIONS:
1. _______________
2. _______________
3. _______________

OVERALL STATUS: ☐ PASS ☐ FAIL ☐ PARTIAL

SIGN-OFF:
Tested by: _______________
Date: _______________
```

---

## 🎯 Acceptance Criteria

The advanced analytics implementation passes if:

- ✅ All 5 analytics tabs load without errors
- ✅ At least 8/10 tests pass
- ✅ No critical bugs or crashes
- ✅ Charts render within 5 seconds
- ✅ Data accuracy verified
- ✅ Error handling works properly
- ✅ Documentation is complete

---

## 📞 Support

If tests fail:
1. Check ADVANCED_ANALYTICS.md for troubleshooting
2. Review QUICK_START_ANALYTICS.md for setup
3. Inspect browser console for errors
4. Check Streamlit terminal output for errors
5. Verify database connection and data

---

**Good luck testing! 🚀**
