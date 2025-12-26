# 🤖 n8n Visual Setup Guide (Drag & Drop - No Coding!)

## 🎯 What You'll Create

Automated email system that sends emails when:
1. ✅ Citizen submits feedback → Email to citizen + Email to admin
2. ✅ Admin resolves issue → Email to citizen with resolution details

**100% Visual - Just drag nodes and fill in fields!**

---

## 📋 Step-by-Step Setup 

### STEP 1: Create n8n Account

1. Go to **[n8n.io](https://n8n.io)**
2. Click **"Get Started"** or **"Sign Up"**
3. Create free account
4. Login to your n8n dashboard

---

### STEP 2: Create First Workflow (New Feedback Emails)

#### 2.1 Create New Workflow
1. Click **"+ New Workflow"** button (top right)
2. Name it: **"Citizen Feedback - New Submission"**
3. Click **"Save"** (top right)

#### 2.2 Add Webhook Node (This receives data from your app)
1. Click **"Add first step"** in the center
2. In search box, type: **"webhook"**
3. Click **"Webhook"** node
4. Fill in these fields:
   - **HTTP Method**: Select **POST**
   - **Path**: Type **feedback-submitted**
   - **Response Mode**: Select **Immediately**
   - **Response Code**: Type **200**
5. Click **"Execute Node"** to activate it
6. **IMPORTANT**: Copy the **Production URL** shown (looks like: `https://xxxxx.app.n8n.cloud/webhook/feedback-submitted`)
   - **Save this URL somewhere!** You'll need it later

#### 2.3 Add Gmail Node for Citizen (Confirmation Email)
1. Click the **"+"** button on the right side of Webhook node
2. Search: **"gmail"**
3. Click **"Gmail"** node
4. Fill in these fields:
   - **Resource**: Message
   - **Operation**: Send
   - **To**: Click the field → Click **"Expressions"** tab → Type: `{{ $json.citizen_email }}`
   - **Subject**: Type: `✅ Feedback Received - ID: {{ $json.feedback_id }}`
   - **Message Type**: Select **HTML**
   - **Message (HTML)**: Copy and paste this:

```html
<h2>Thank You for Your Feedback!</h2>

<p>Dear <strong>{{ $json.citizen_name }}</strong>,</p>

<p>We have received your feedback and our team will review it shortly.</p>

<div style="background: #f3f4f6; padding: 20px; border-radius: 8px;">
  <h3>📋 Your Feedback Details</h3>
  <p><strong>🔖 Tracking ID:</strong> {{ $json.feedback_id }}</p>
  <p><strong>📁 Category:</strong> {{ $json.category }}</p>
  <p><strong>📝 Title:</strong> {{ $json.title }}</p>
  <p><strong>📍 Location:</strong> {{ $json.location }}</p>
  <p><strong>🚨 Priority:</strong> {{ $json.urgency }}</p>
  <p><strong>📅 Submitted:</strong> {{ $json.timestamp }}</p>
</div>

<div style="background: #fff; padding: 15px; border-left: 4px solid #7c3aed; margin-top: 20px;">
  <p><strong>Your Feedback:</strong></p>
  <p>{{ $json.feedback }}</p>
</div>

<p style="margin-top: 30px;">You can track your submission using the tracking ID above.</p>

<p>Best regards,<br><strong>City Government Team</strong></p>
```

5. Click **"Create New Credential"** (first time only)
6. Follow the steps to connect your Gmail account
7. Click **"Save"**

#### 2.4 Add Gmail Node for Admin (Alert Email)
1. Click the **"+"** button after the first Gmail node
2. Search: **"gmail"**
3. Click **"Gmail"** node
4. Fill in these fields:
   - **Resource**: Message
   - **Operation**: Send
   - **To**: Type your admin email (e.g., `admin@city.gov`)
   - **Subject**: Type: `🚨 New Feedback: {{ $json.category }} [{{ $json.urgency }}] - ID: {{ $json.feedback_id }}`
   - **Message Type**: Select **HTML**
   - **Message (HTML)**: Copy and paste this:

```html
<h2>🆕 New Citizen Feedback Submitted</h2>

<div style="background: #fee; padding: 20px; border-radius: 8px;">
  <h3>⚠️ Action Required</h3>
  <p>A new feedback submission needs your attention.</p>
</div>

<div style="background: #f9fafb; padding: 20px; margin: 20px 0;">
  <h3>👤 Citizen Information</h3>
  <p><strong>Name:</strong> {{ $json.citizen_name }}</p>
  <p><strong>Email:</strong> {{ $json.citizen_email }}</p>
  <p><strong>Phone:</strong> {{ $json.citizen_phone }}</p>
</div>

<div style="background: #eff6ff; padding: 20px;">
  <h3>📋 Feedback Details</h3>
  <p><strong>ID:</strong> {{ $json.feedback_id }}</p>
  <p><strong>Category:</strong> {{ $json.category }}</p>
  <p><strong>Title:</strong> {{ $json.title }}</p>
  <p><strong>Location:</strong> {{ $json.location }}</p>
  <p><strong>Urgency:</strong> {{ $json.urgency }}</p>
  <p><strong>Sentiment:</strong> {{ $json.sentiment }}</p>
</div>

<div style="background: #fff; padding: 20px; border: 2px solid #e5e7eb; margin-top: 20px;">
  <h3>💬 Citizen's Feedback</h3>
  <p>{{ $json.feedback }}</p>
</div>

<p style="margin-top: 30px;"><em>This is an automated notification from the Citizen Feedback System</em></p>
```

5. Use the same Gmail credential
6. Click **"Save"**

#### 2.5 Configure CORS (Important for Browser Security)
1. Click on the **Webhook** node
2. In the node panel, scroll down and click **"Add Option"**
3. Select **"Response Headers"**
4. Add these headers (click "+ Add Header" for each):
   - **Name**: `Access-Control-Allow-Origin` | **Value**: `*`
   - **Name**: `Access-Control-Allow-Methods` | **Value**: `POST, OPTIONS`
   - **Name**: `Access-Control-Allow-Headers` | **Value**: `Content-Type`
5. Click outside the node to save

#### 2.6 Activate Workflow (CRITICAL STEP!)
1. Click **"Publish"** button (top right) to save your workflow first
2. After publishing, look for the **toggle switch** in the top bar (near workflow name)
3. Click the toggle to turn it from **"Inactive"** ❌ to **"Active"** ✅ (will turn green)
4. **Your first workflow is now live!** 🎉

⚠️ **IMPORTANT**: The workflow MUST be active for webhooks to work! If inactive, you'll get 404 errors.

---

### STEP 3: Create Second Workflow (Resolution Emails)

#### 3.1 Create New Workflow
1. Click **"Back"** to go to workflows list
2. Click **"+ New Workflow"**
3. Name it: **"Citizen Feedback - Resolution"**
4. Click **"Save"**

#### 3.2 Add Webhook Node
1. Click **"Add first step"**
2. Search: **"webhook"**
3. Click **"Webhook"** node
4. Fill in:
   - **HTTP Method**: POST
   - **Path**: Type **feedback-resolved**
   - **Response Mode**: Immediately
   - **Response Code**: 200
5. Click **"Execute Node"**
6. **IMPORTANT**: Copy the **Production URL** (save it!)

#### 3.3 Add Gmail Node for Resolution
1. Click the **"+"** button after Webhook
2. Search: **"gmail"**
3. Click **"Gmail"** node
4. Fill in:
   - **Resource**: Message
   - **Operation**: Send
   - **To**: `{{ $json.citizen_email }}`
   - **Subject**: `✅ Your Issue Has Been Resolved - ID: {{ $json.feedback_id }}`
   - **Message Type**: HTML
   - **Message (HTML)**: Copy and paste:

```html
<div style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 30px; text-align: center;">
  <h1>✅ Issue Resolved!</h1>
</div>

<div style="padding: 30px;">
  <p style="font-size: 18px;">Dear <strong>{{ $json.citizen_name }}</strong>,</p>
  
  <p>Great news! Your feedback has been successfully addressed by our team. Thank you for helping us improve our community! 🎉</p>
  
  <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <h3>📋 Original Feedback</h3>
    <p><strong>Tracking ID:</strong> {{ $json.feedback_id }}</p>
    <p><strong>Category:</strong> {{ $json.category }}</p>
    <p><strong>Title:</strong> {{ $json.title }}</p>
    <p><strong>Submitted:</strong> {{ $json.original_timestamp }}</p>
  </div>
  
  <div style="background: #ecfdf5; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981;">
    <h3>✅ Resolution Details</h3>
    <p>{{ $json.resolution_notes }}</p>
  </div>
  
  <div style="background: #f9fafb; padding: 15px; border-radius: 8px; margin-top: 20px;">
    <p><strong>Handled by:</strong> {{ $json.assigned_to }}</p>
    <p><strong>Resolved on:</strong> {{ $json.resolved_timestamp }}</p>
  </div>
  
  <p style="text-align: center; margin-top: 30px;">
    Thank you for being an engaged citizen!<br>
    <strong>City Government Team</strong>
  </p>
</div>
```

5. Use Gmail credential
6. Click **"Save"**

#### 3.4 Configure CORS for Resolution Workflow
1. Click on the **Webhook** node
2. Scroll down → **"Add Option"** → **"Response Headers"**
3. Add headers:
   - `Access-Control-Allow-Origin`: `*`
   - `Access-Control-Allow-Methods`: `POST, OPTIONS`
   - `Access-Control-Allow-Headers`: `Content-Type`

#### 3.5 Activate Workflow (CRITICAL!)
1. Click **"Publish"** (top right)
2. Toggle the switch to **"Active"** ✅ (will turn green)
3. **Your second workflow is live!** 🎉

⚠️ **Both workflows must be active for the system to work!**

---

### STEP 4: Get Your Webhook Base URL

From the URLs you copied earlier:
```
https://your-n8n.app.n8n.cloud/webhook/feedback-submitted
https://your-n8n.app.n8n.cloud/webhook/feedback-resolved
```

**Take only the base part (remove the endpoint):**
```
https://your-n8n.app.n8n.cloud/webhook
```

This is what you'll paste in your app!

---

### STEP 5: Connect to Your Python App

#### Option 1: Manual Configuration File
1. Go to your project folder: `D:\citizen-feedback-ai-agent`
2. Create a new file: `data/n8n_config.json`
3. Paste this (replace with YOUR webhook URL):

```json
{
  "webhook_base_url": "https://your-n8n.app.n8n.cloud/webhook"
}
```

4. Save the file
5. Restart both portals

---

## 🧪 Testing Your Setup

### Test in n8n First (Before connecting to app):

1. In n8n, open your first workflow
2. Click **"Test Workflow"** (top right)
3. Click on the Webhook node
4. Click **"Listen for Test Event"**
5. Use a tool like Postman or curl to send test data:

```bash
curl -X POST https://your-webhook-url/feedback-submitted \
  -H "Content-Type: application/json" \
  -d '{
    "feedback_id": "TEST123",
    "citizen_name": "Test User",
    "citizen_email": "your-email@gmail.com",
    "category": "Test",
    "title": "Test Feedback",
    "feedback": "This is a test",
    "location": "Test Location",
    "urgency": "Medium"
  }'
```

6. Check if you received the email ✅

### Test with Real App:

1. Make sure `data/n8n_config.json` has your webhook URL
2. **IMPORTANT: Activate both workflows in n8n** (toggle to green ✅)
3. Go to Citizen Portal (http://localhost:8503)
4. Submit a test feedback
5. Check your email inbox
6. If you got emails ✅ - **It's working!**

**If no emails:**
- ✅ Check both workflows are **Active** (green toggle in n8n)
- ✅ Verify Gmail credentials are connected in both Gmail nodes
- ✅ Check n8n Executions tab for errors
- ✅ Look in spam folder

---

## 🎨 Customizing Your Emails

Want to change email design? **Just edit the HTML in Gmail nodes!**

You can use these variables anywhere in your email:
- `{{ $json.citizen_name }}` - Citizen's name
- `{{ $json.citizen_email }}` - Their email
- `{{ $json.feedback_id }}` - Tracking ID
- `{{ $json.category }}` - Category
- `{{ $json.title }}` - Feedback title
- `{{ $json.feedback }}` - Full feedback text
- `{{ $json.location }}` - Location
- `{{ $json.urgency }}` - Priority (High/Medium/Low)
- `{{ $json.timestamp }}` - When submitted
- `{{ $json.sentiment }}` - Sentiment analysis
- `{{ $json.resolution_notes }}` - Resolution details (for resolved workflow)

---

## 🛠️ Troubleshooting

### No emails received?
- ✅ Check workflow is **Active** (green toggle)
- ✅ Verify Gmail credentials are connected
- ✅ Check execution history (click on workflow → "Executions" tab)
- ✅ Make sure `data/n8n_config.json` has correct URL

### Webhook not receiving data?
- ✅ Copy the webhook URL again from n8n
- ✅ Make sure you used **Production URL** (not Test URL)
- ✅ Check the path matches: `/feedback-submitted` and `/feedback-resolved`

### Gmail authentication issues?
- ✅ In n8n, go to Credentials
- ✅ Reconnect your Gmail account
- ✅ Make sure you allow less secure apps (if needed)

---

## 📚 What Data Gets Sent

### When Feedback is Submitted:
```json
{
  "feedback_id": "ABC123",
  "citizen_name": "John Doe",
  "citizen_email": "john@example.com",
  "citizen_phone": "+1234567890",
  "category": "Infrastructure",
  "title": "Pothole on Main St",
  "feedback": "There is a large pothole...",
  "location": "Main Street",
  "urgency": "High",
  "timestamp": "2024-12-07T10:30:00",
  "status": "New",
  "sentiment": "Negative"
}
```

### When Feedback is Resolved:
```json
{
  "feedback_id": "ABC123",
  "citizen_name": "John Doe",
  "citizen_email": "john@example.com",
  "category": "Infrastructure",
  "title": "Pothole on Main St",
  "original_feedback": "There is a large pothole...",
  "original_timestamp": "2024-12-07T10:30:00",
  "resolved_timestamp": "2024-12-08T15:45:00",
  "assigned_to": "Admin User",
  "resolution_notes": "Pothole has been filled and repaired"
}
```

---

## 🎉 You're Done!

**Congratulations!** 🎊 Your automated email system is ready!

Every time:
- ✅ Citizen submits feedback → Automatic emails sent
- ✅ Admin resolves issue → Resolution email sent

**All visual - no coding! Just drag, drop, and connect!** 🚀

---

## 💡 Advanced Ideas (Optional - Still No Coding!)

### Add SMS Notifications
1. Add **"Twilio"** node after webhook
2. Configure to send SMS to `{{ $json.citizen_phone }}`
3. Done!

### Add Slack Alerts
1. Add **"Slack"** node after webhook
2. Configure channel and message
3. Get instant Slack notifications!

### Add Database Logging
1. Add **"Google Sheets"** node
2. Append row with all feedback data
3. Automatic spreadsheet logging!

### Add Priority-Based Routing
1. Add **"IF"** node after webhook
2. Check if `{{ $json.urgency }}` equals "Emergency"
3. Send different emails based on priority!

**All of these use drag & drop - no coding required!** 🎨
