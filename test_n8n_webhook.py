"""
Test n8n Webhook Connection
Run this script to verify your n8n webhook is receiving data correctly.
"""

import json
from datetime import datetime
from src.n8n_client import send_feedback_submitted


def test_n8n_connection():
    """Test sending data to n8n webhook."""
    
    print("\n" + "="*70)
    print("🧪 TESTING n8n WEBHOOK CONNECTION")
    print("="*70 + "\n")
    
    # Create test feedback entry (matching the format from citizen_portal.py)
    test_entry = {
        # n8n-compatible fields
        "feedback_id": "TEST-" + datetime.now().strftime("%Y%m%d-%H%M%S"),
        "citizen_name": "Test User from localhost",
        "citizen_email": "test@example.com",
        "citizen_phone": "+1234567890",
        "category": "🧪 Testing",
        "title": "Test Webhook Connection",
        "feedback": "This is a test message sent from localhost to verify n8n webhook integration works correctly.",
        "location": "Test Location, 123 Test Street",
        "urgency": "Normal",
        "timestamp": datetime.now().isoformat(),
        "status": "New",
        "sentiment": "Neutral",
    }
    
    print("📋 Test Data:")
    print(json.dumps(test_entry, indent=2))
    print("\n")
    
    # Send to n8n
    print("📤 Sending to n8n webhook...\n")
    success = send_feedback_submitted(test_entry)
    
    print("\n" + "="*70)
    if success:
        print("✅ SUCCESS! n8n webhook received the data.")
        print("\n📌 Next steps:")
        print("   1. Go to n8n → Executions")
        print("   2. Look for the latest execution")
        print("   3. Click on it to see the received data")
        print("   4. Verify all fields are present")
    else:
        print("❌ FAILED! n8n webhook did not receive the data.")
        print("\n🔍 Troubleshooting:")
        print("   1. Check if workflow is PUBLISHED (not just saved)")
        print("   2. Verify webhook URL in data/n8n_config.json")
        print("   3. Check n8n webhook node settings:")
        print("      - Path should be: /feedback-submitted")
        print("      - Response Headers should include:")
        print("        • Access-Control-Allow-Origin: *")
        print("        • Access-Control-Allow-Methods: POST, OPTIONS")
        print("        • Access-Control-Allow-Headers: Content-Type")
        print("   4. Check the error logs above for specific issues")
    print("="*70 + "\n")
    
    return success


if __name__ == "__main__":
    test_n8n_connection()
