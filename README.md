# 🏛️ Citizen Feedback AI Agent

An AI-powered dual-portal web application for citizen engagement and government feedback management. Built with Streamlit, Python, and PostgreSQL.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
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
- PostgreSQL 13 or higher
- uv (recommended) or pip

### Installation

#### 1. Clone and Install Dependencies

```bash
cd citizen-feedback-ai-agent
uv sync
```

#### 2. Set Up PostgreSQL Database

**Option A: Using Docker (Recommended)**
```bash
docker run --name citizen-feedback-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=citizen_feedback \
  -p 5432:5432 \
  -d postgres:15
```

**Option B: Install PostgreSQL Locally**
- Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
- Create a new database named `citizen_feedback`

```sql
CREATE DATABASE citizen_feedback;
```

#### 3. Configure Database Connection

**Option A: Using Environment Variable (Recommended)**
```bash
# Windows (PowerShell)
$env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/citizen_feedback"

# Windows (CMD)
set DATABASE_URL=postgresql://postgres:postgres@localhost:5432/citizen_feedback

# Linux/Mac
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/citizen_feedback
```

**Option B: Using Configuration File**
Update `data/db_config.json` with your database credentials:
```json
{
  "database_url": "postgresql://username:password@host:port/database_name"
}
```

#### 4. Initialize Database and Migrate Data

```bash
python migrate_to_postgres.py
```

This will:
- ✅ Create all necessary database tables
- ✅ Migrate existing JSON data (if any) to PostgreSQL
- ✅ Verify database connection
- ✅ Create a backup of your data

#### 5. Run the Application

```bash
# Launch the main portal selector
streamlit run main.py

# Or run portals separately:
streamlit run citizen_portal.py --server.port 8501
streamlit run admin_portal.py --server.port 8502
```

### Admin Login Credentials
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Full Access |
| manager | manager123 | Manager |
| staff | staff123 | Staff |

## 💾 Database Information

### PostgreSQL Schema

The application uses a single `feedback` table with the following structure:

```sql
CREATE TABLE feedback (
    id VARCHAR(50) PRIMARY KEY,
    feedback_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP,
    name VARCHAR(200),
    citizen_name VARCHAR(200),
    email VARCHAR(200),
    citizen_email VARCHAR(200),
    phone VARCHAR(50),
    citizen_phone VARCHAR(50),
    feedback_type VARCHAR(100),
    category VARCHAR(100),
    urgency VARCHAR(50),
    area VARCHAR(200),
    address TEXT,
    location TEXT,
    title VARCHAR(500),
    feedback TEXT,
    sentiment VARCHAR(50),
    sentiment_score FLOAT,
    keywords JSON,
    summary TEXT,
    status VARCHAR(50) DEFAULT 'New',
    admin_notes TEXT,
    assigned_to VARCHAR(200),
    priority VARCHAR(50) DEFAULT 'Normal'
);
```

### Fallback Mode

The application includes automatic fallback to JSON file storage if PostgreSQL is unavailable:
- ✅ Seamless switching between PostgreSQL and JSON
- ✅ No data loss during connection failures
- ✅ Automatic retry on next application start

### Database Management Commands

```bash
# Initialize database
python migrate_to_postgres.py

# Export PostgreSQL data to JSON backup
python -c "from migrate_to_postgres import export_postgres_to_json; export_postgres_to_json('backup.json')"

# View database statistics
python -c "from migrate_to_postgres import show_database_stats; show_database_stats()"
```

## 📁 Project Structure

```
citizen-feedback-ai-agent/
├── main.py                      # Launcher / Portal selector
├── citizen_portal.py            # 👥 Public citizen website
├── admin_portal.py              # ⚙️ Government admin website
├── migrate_to_postgres.py       # 🔄 Database migration script
├── pyproject.toml               # Dependencies
├── README.md                    # Documentation
├── .env.example                 # Environment variables template
├── data/                        # Data storage
│   ├── feedback.json            # JSON fallback storage
│   ├── db_config.json           # Database configuration
│   └── n8n_config.json          # n8n webhook configuration
└── src/                         # Core modules
    ├── __init__.py
    ├── feedback_analyzer.py     # 🤖 AI analysis engine
    ├── data_manager.py          # 💾 Data storage layer (PostgreSQL + JSON)
    ├── database.py              # 🔌 Database connection manager
    ├── db_models.py             # 📊 SQLAlchemy models
    ├── n8n_client.py            # 🔗 n8n integration
    └── dashboard.py             # 📈 Visualization components
```

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                   CITIZEN FEEDBACK AI AGENT                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────┐      ┌──────────────────────┐            │
│  │   👥 CITIZEN PORTAL   │      │   ⚙️ ADMIN PORTAL     │            │
│  │   (Port 8501)         │      │   (Port 8502)        │            │
│  │                       │      │                       │            │
│  │  • Submit Feedback    │      │  • Dashboard          │            │
│  │  • Track Status       │      │  • Manage Feedback    │            │
│  │  • View Updates       │      │  • Priority Queue     │            │
│  │  • Help & FAQs        │      │  • Staff Assignments  │            │
│  └───────────┬───────────┘      └───────────┬───────────┘            │
│              │                              │                        │
│              └──────────────┬───────────────┘                        │
│                             │                                        │
│              ┌──────────────▼───────────────┐                        │
│              │    🤖 AI ANALYSIS ENGINE      │                        │
│              │   (Sentiment, Keywords, etc.) │                        │
│              └──────────────┬───────────────┘                        │
│                             │                                        │
│              ┌──────────────▼───────────────┐                        │
│              │    💾 DATA MANAGER            │                        │
│              │   (PostgreSQL + JSON Fallback)│                        │
│              └──────────────┬───────────────┘                        │
│                             │                                        │
│              ┌──────────────▼───────────────┐                        │
│              │    🗄️  POSTGRESQL DATABASE    │                        │
│              │   (Primary Storage)           │                        │
│              │                               │                        │
│              │   🔗 n8n Webhook Integration  │                        │
│              │   (Optional Automation)       │                        │
│              └──────────────────────────────┘                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔗 n8n Integration

The application includes built-in n8n webhook integration for automation workflows:

### Setup n8n Integration

1. Configure webhook URL in `data/n8n_config.json`:
```json
{
  "webhook_base_url": "https://your-n8n-instance.com/webhook"
}
```

2. The system automatically sends events to n8n:
   - `feedback-submitted`: When new feedback is received
   - `feedback-resolved`: When feedback status changes to "Resolved"

3. n8n continues to work with PostgreSQL data seamlessly

### Example n8n Workflows
- Send email notifications when feedback is submitted
- Create tickets in project management tools
- Send SMS alerts for urgent issues
- Post updates to Slack/Discord channels

## 📖 Usage Guide

### For Citizens

1. **Submit Feedback**
   - Go to Citizen Portal → Submit Feedback
   - Fill in your details and describe the issue
   - Get a tracking ID upon submission
   - Data is automatically stored in PostgreSQL

2. **Track Your Submission**
   - Go to Track My Feedback
   - Enter your tracking ID or email
   - View current status and admin responses

### For Administrators

1. **Login** with admin credentials
2. **Dashboard** - View real-time metrics and charts from PostgreSQL
3. **All Feedback** - Filter, search, and manage submissions
4. **Priority Queue** - Handle urgent issues first
5. **Assignments** - Assign feedback to staff members
6. **Export** - Download reports in CSV/JSON

## 🔧 Configuration

### Database Configuration

**Priority Order:**
1. `DATABASE_URL` environment variable (highest priority)
2. `data/db_config.json` configuration file
3. Default: `postgresql://postgres:postgres@localhost:5432/citizen_feedback`

**Connection String Format:**
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

**Example Configurations:**

Local PostgreSQL:
```
postgresql://postgres:postgres@localhost:5432/citizen_feedback
```

Remote PostgreSQL:
```
postgresql://user:password@db.example.com:5432/citizen_feedback
```

Cloud PostgreSQL (Heroku):
```
postgres://username:password@hostname:5432/database
```

Cloud PostgreSQL (Railway, Render):
```
postgresql://username:password@hostname:5432/database
```

### Environment Variables

Create a `.env` file (use `.env.example` as template):
```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/citizen_feedback

# n8n Integration (Optional)
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook
```



## 📊 API Reference

### DataManager (PostgreSQL + JSON Fallback)

```python
from src.data_manager import DataManager

# Initialize with PostgreSQL (default)
dm = DataManager(use_postgres=True)

# Initialize with JSON only (fallback)
dm = DataManager(use_postgres=False)

# Add feedback (automatically uses PostgreSQL or JSON)
feedback_id = dm.add_feedback({
    "name": "John Doe",
    "email": "john@example.com",
    "title": "Street light issue",
    "feedback": "The street light on Main St is broken",
    "category": "Infrastructure"
})

# Get all feedback
all_feedback = dm.get_all_feedback()

# Get specific feedback
feedback = dm.get_feedback_by_id(feedback_id)

# Update feedback
dm.update_feedback(feedback_id, {"status": "In Progress"})

# Get as DataFrame
df = dm.get_feedback_dataframe()

# Get statistics
stats = dm.get_statistics()

# Export to JSON backup
dm.export_to_json("backup.json")
```

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

### Database Connection

```python
from src.database import Database

# Initialize database
Database.initialize()

# Test connection
if Database.test_connection():
    print("Connected!")

# Get connection info
info = Database.get_connection_info()

# Use session scope (recommended)
with Database.session_scope() as session:
    # Your database operations here
    session.add(feedback)
    # Auto-commits on success, rolls back on error

# Direct session access
session = Database.get_session()
try:
    # Your operations
    session.commit()
finally:
    session.close()
```

## 🔄 Migration & Backup

### Migrate from JSON to PostgreSQL

```bash
python migrate_to_postgres.py
```

This comprehensive script will:
1. ✅ Initialize PostgreSQL database
2. ✅ Create all tables
3. ✅ Migrate existing JSON data
4. ✅ Verify migration
5. ✅ Create backup

### Manual Migration

```python
from src.data_manager import DataManager
import json

# Load from JSON
with open('data/feedback.json', 'r') as f:
    data = json.load(f)

# Initialize DataManager with PostgreSQL
dm = DataManager(use_postgres=True)

# Import each entry
for entry in data:
    dm.add_feedback(entry)
```

### Backup PostgreSQL to JSON

```python
from migrate_to_postgres import export_postgres_to_json

export_postgres_to_json("backup/feedback_backup.json")
```

## 🚨 Troubleshooting

### PostgreSQL Connection Issues

**Problem:** "Could not connect to PostgreSQL"

**Solutions:**
1. Verify PostgreSQL is running:
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql  # Linux
   brew services list                # Mac
   # Check Docker container
   docker ps | grep postgres
   ```

2. Check connection string format
3. Verify firewall settings
4. Check PostgreSQL logs

**Fallback:** Application automatically switches to JSON file storage

### Database Not Updating

**Problem:** Changes not persisted to database

**Solutions:**
1. Check database permissions
2. Verify connection in logs
3. Try manual migration: `python migrate_to_postgres.py`
4. Check `data/db_config.json` configuration

### n8n Integration Not Working

**Problem:** Webhooks not receiving data

**Solutions:**
1. Verify `data/n8n_config.json` webhook URL
2. Check n8n workflow is activated
3. Review console logs for HTTP errors
4. Test webhook with curl:
   ```bash
   curl -X POST https://your-n8n-url/webhook/feedback-submitted \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
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
