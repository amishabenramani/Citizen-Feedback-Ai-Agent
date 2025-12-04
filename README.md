# 🏛️ Citizen Feedback AI Agent

An AI-powered dual-portal web application for citizen engagement and government feedback management. Built with Streamlit and Python.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Two Separate Portals

### 👥 Citizen Portal (Public)
For citizens to interact with government services:
- 📝 Submit feedback, complaints, or suggestions
- 🔍 Track submission status with tracking ID
- 📢 View public announcements & resolved issues
- ❓ Access help center and FAQs

### ⚙️ Admin Portal (Government Officials)
For administrators to manage citizen feedback:
- 📊 Real-time analytics dashboard
- 📋 Complete feedback management
- 🚨 Priority queue for urgent issues
- 👥 Staff assignment system
- 📤 Data export (CSV/JSON)
- 🔐 Secure login authentication

## 🤖 AI-Powered Features

- **Sentiment Analysis**: Automatically detect positive, negative, or neutral feedback
- **Keyword Extraction**: Identify key topics and themes
- **Smart Summarization**: Generate concise summaries
- **Urgency Detection**: Flag time-sensitive issues
- **Category Detection**: Auto-categorize feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- uv (recommended) or pip

### Installation

```bash
cd citizen-feedback-ai-agent
uv sync
```

### Running the Portals

**Option 1: Run Both Portals (Recommended)**

Open two separate terminals:

```bash
# Terminal 1 - Citizen Portal (Port 8501)
uv run streamlit run citizen_portal.py --server.port 8501

# Terminal 2 - Admin Portal (Port 8502)
uv run streamlit run admin_portal.py --server.port 8502
```

**Option 2: Run Single Portal**

```bash
# Citizen Portal only
uv run streamlit run citizen_portal.py

# Admin Portal only
uv run streamlit run admin_portal.py
```

### Access URLs
- 👥 **Citizen Portal:** http://localhost:8501
- ⚙️ **Admin Portal:** http://localhost:8502

### Admin Login Credentials
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Full Access |
| manager | manager123 | Manager |
| staff | staff123 | Staff |

## 📁 Project Structure

```
citizen-feedback-ai-agent/
├── main.py                 # Launcher / Portal selector
├── citizen_portal.py       # 👥 Public citizen website
├── admin_portal.py         # ⚙️ Government admin website
├── pyproject.toml          # Dependencies
├── README.md               # Documentation
├── data/                   # Shared data storage
│   └── feedback.json       # Feedback database
└── src/                    # Shared modules
    ├── __init__.py
    ├── feedback_analyzer.py    # 🤖 AI analysis engine
    ├── data_manager.py         # 💾 Data storage layer
    └── dashboard.py            # 📊 Visualization components
```

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CITIZEN FEEDBACK AI AGENT                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │   👥 CITIZEN PORTAL   │      │   ⚙️ ADMIN PORTAL     │        │
│  │   (Port 8501)         │      │   (Port 8502)        │        │
│  │                       │      │                       │        │
│  │  • Submit Feedback    │      │  • Dashboard          │        │
│  │  • Track Status       │      │  • Manage Feedback    │        │
│  │  • View Updates       │      │  • Priority Queue     │        │
│  │  • Help & FAQs        │      │  • Staff Assignments  │        │
│  └───────────┬───────────┘      └───────────┬───────────┘        │
│              │                              │                    │
│              └──────────────┬───────────────┘                    │
│                             │                                    │
│              ┌──────────────▼───────────────┐                    │
│              │    🤖 AI ANALYSIS ENGINE      │                    │
│              │   (Sentiment, Keywords, etc.) │                    │
│              └──────────────┬───────────────┘                    │
│                             │                                    │
│              ┌──────────────▼───────────────┐                    │
│              │    💾 SHARED DATA STORAGE     │                    │
│              │      (data/feedback.json)     │                    │
│              └──────────────────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 📖 Usage Guide

### For Citizens

1. **Submit Feedback**
   - Go to Citizen Portal → Submit Feedback
   - Fill in your details and describe the issue
   - Get a tracking ID upon submission

2. **Track Your Submission**
   - Go to Track My Feedback
   - Enter your tracking ID or email
   - View current status and admin responses

### For Administrators

1. **Login** with admin credentials
2. **Dashboard** - View real-time metrics and charts
3. **All Feedback** - Filter, search, and manage submissions
4. **Priority Queue** - Handle urgent issues first
5. **Assignments** - Assign feedback to staff members
6. **Export** - Download reports in CSV/JSON

## 🔧 Configuration

### Data Storage

By default, feedback data is stored in `data/feedback.json`. You can modify the storage location in `src/data_manager.py`:

```python
data_manager = DataManager(data_dir="custom/path")
```

### Customizing Categories

Edit the category list in `main.py`:

```python
category = st.selectbox(
    "Category",
    [
        "🏗️ Infrastructure",
        "🚌 Transportation",
        # Add your custom categories here
    ]
)
```

## 📊 API Reference

### FeedbackAnalyzer

```python
from src.feedback_analyzer import FeedbackAnalyzer

analyzer = FeedbackAnalyzer()
result = analyzer.analyze("Your feedback text here")

# Returns:
# {
#     "sentiment": "Positive|Neutral|Negative",
#     "sentiment_score": 0.0-1.0,
#     "keywords": ["keyword1", "keyword2", ...],
#     "summary": "Brief summary of the feedback"
# }
```

### DataManager

```python
from src.data_manager import DataManager

dm = DataManager()

# Add feedback
dm.add_feedback({"title": "...", "feedback": "..."})

# Get all feedback
all_feedback = dm.get_all_feedback()

# Get as DataFrame
df = dm.get_feedback_dataframe()

# Get statistics
stats = dm.get_statistics()
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Plotly](https://plotly.com/) for interactive visualizations
- All contributors and users of this project

---

Made with ❤️ for better citizen engagement
"# citizen-feedback-ai-agent" 
