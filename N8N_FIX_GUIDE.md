# n8n Webhook Integration - Quick Fix Guide

## ✅ What I Fixed

### 1. **n8n_client.py** - Added Proper Headers
- ✅ Added `Content-Type: application/json` header
- ✅ Added `Accept: application/json` header
- ✅ Added detailed logging and error handling
- ✅ Increased timeout to 15 seconds
- ✅ Better field name mapping (id → feedback_id, name → citizen_name, email → citizen_email)

### 2. **citizen_portal.py** - Dual Field Names
- ✅ Added both internal fields (`id`, `name`, `email`) and n8n fields (`feedback_id`, `citizen_name`, `citizen_email`)
- ✅ Added user-visible feedback when n8n webhook succeeds/fails
- ✅ Better error handling with specific messages

### 3. **n8n_config.json** - Updated Configuration
- ✅ Added explicit endpoint URLs for clarity
- ✅ Properly structured configuration

### 4. **test_n8n_webhook.py** - New Test Script
- ✅ Quick way to test webhook without running full app
- ✅ Clear success/failure feedback
- ✅ Troubleshooting guide included

---

## 🚀 How to Test (RIGHT NOW)

### Step 1: Test the Webhook Connection

```powershell
python test_n8n_webhook.py
```

This will:
- Send a test message to your n8n webhook
- Show detailed logs of what's happening
- Tell you if it succeeded or failed

### Step 2: Check n8n Executions

1. Go to n8n: https://amisharamani.app.n8n.cloud
2. Click **Executions** (left sidebar)
3. Look for the **latest execution**
4. Open it and verify you see:
   ```json
   {
     "feedback_id": "TEST-20231227-123456",
     "citizen_name": "Test User from localhost",
     "citizen_email": "test@example.com",
     ...
   }
   ```

### Step 3: Run Your Streamlit App

```powershell
streamlit run citizen_portal.py
```

Then:
1. Fill out the feedback form
2. Click "Submit Feedback"
3. You should see: **"✅ n8n webhook notification sent successfully!"**
4. Check n8n Executions to confirm data arrived

---

## 🔧 n8n Configuration (MUST DO)

### In your n8n Webhook Node:

#### 1️⃣ **Webhook Settings**
- **HTTP Method**: POST
- **Path**: `feedback-submitted`
- **Response Mode**: When Last Node Finishes (or Immediately)

#### 2️⃣ **Add Response Headers** (CRITICAL for localhost)

Click **Options** → **Add option** → **Response Headers**

Add these 3 headers:

| Key | Value |
|-----|-------|
| `Access-Control-Allow-Origin` | `*` |
| `Access-Control-Allow-Methods` | `POST, OPTIONS` |
| `Access-Control-Allow-Headers` | `Content-Type` |

#### 3️⃣ **Publish the Workflow**

Click **Publish** (top-right). Production webhooks only work when published!

---

## 📋 Expected Data Format

Your n8n webhook should receive this JSON:

```json
{
  "feedback_id": "A1B2C3D4",
  "citizen_name": "John Doe",
  "citizen_email": "john@example.com",
  "citizen_phone": "+1234567890",
  "category": "🏗️ Roads & Infrastructure",
  "title": "Pothole on Main Street",
  "feedback": "There is a large pothole...",
  "location": "Downtown, 123 Main St",
  "urgency": "High",
  "timestamp": "2023-12-27T14:30:00.123456",
  "status": "New",
  "sentiment": "Negative"
}
```

---

## 🐛 Troubleshooting

### Problem: "Failed to send n8n notification"

**Check these in order:**

1. **Is workflow published?**
   - In n8n, top-right should say **"Publish ✔ Saved"**
   - If not, click Publish

2. **Check webhook URL**
   - Open `data/n8n_config.json`
   - Should be: `https://amisharamani.app.n8n.cloud/webhook`

3. **Check n8n logs**
   - Run your app from terminal (not double-click)
   - Look for `[n8n]` prefixed messages
   - Should see: `[n8n] ✅ SUCCESS: Webhook call successful`

4. **Response Headers missing**
   - Go to webhook node → Options → Response Headers
   - Add the 3 headers listed above

5. **Test with curl** (from PowerShell)
   ```powershell
   curl -X POST `
     https://amisharamani.app.n8n.cloud/webhook/feedback-submitted `
     -H "Content-Type: application/json" `
     -d '{\"citizen_name\":\"Curl Test\",\"citizen_email\":\"test@test.com\",\"feedback_id\":\"CURL-TEST\",\"feedback\":\"Test from curl\"}'
   ```

### Problem: n8n receives data but emails don't send

This means webhook works! Check your **email nodes** in n8n:
- Gmail node credentials
- Email addresses are correct
- No errors in execution logs

---

## 📊 Logs to Check

When you submit feedback, you should see in terminal:

```
============================================================
[n8n] 🚀 SENDING FEEDBACK TO n8n
============================================================
[n8n] Entry keys received: ['id', 'timestamp', 'name', ...]
[n8n] Final URL: https://amisharamani.app.n8n.cloud/webhook/feedback-submitted
[n8n] Headers: {'Content-Type': 'application/json', ...}
[n8n] Payload: {
  "feedback_id": "ABC123",
  ...
}
[n8n] Status Code: 200
[n8n] ✅ SUCCESS: Webhook call successful
[n8n] Final Result: ✅ SUCCESS
============================================================
```

---

## ✅ Success Checklist

- [ ] Workflow is **Published** in n8n
- [ ] Response Headers are added to webhook node
- [ ] Webhook URL ends with `/webhook` in config
- [ ] `test_n8n_webhook.py` runs successfully
- [ ] Test execution appears in n8n Executions
- [ ] Streamlit form submission shows "✅ n8n webhook notification sent successfully!"
- [ ] Real execution appears in n8n with correct data

---

## 🎯 Key Changes Summary

| Issue | Solution |
|-------|----------|
| Missing Content-Type header | ✅ Added `application/json` header |
| Field name mismatch | ✅ Map `name` → `citizen_name`, etc. |
| Poor error messages | ✅ Added detailed logging |
| No CORS headers in n8n | ✅ Added Response Headers guide |
| Timeout too short | ✅ Increased from 10s to 15s |
| Silent failures | ✅ Show success/error in UI |

---

## 🔗 Related Files

- [src/n8n_client.py](src/n8n_client.py) - Main webhook client
- [data/n8n_config.json](data/n8n_config.json) - Webhook URLs
- [citizen_portal.py](citizen_portal.py) - Feedback form
- [test_n8n_webhook.py](test_n8n_webhook.py) - Test script
- [N8N_VISUAL_GUIDE.md](N8N_VISUAL_GUIDE.md) - Original setup guide

---

**Need help?** Run `python test_n8n_webhook.py` and check the output!
