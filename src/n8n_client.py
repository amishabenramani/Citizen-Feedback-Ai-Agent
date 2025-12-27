"""
n8n Client
Reads webhook base URL from data/n8n_config.json and sends events
to n8n workflows for feedback submission and resolution.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests


CONFIG_PATH = Path("data") / "n8n_config.json"


def _clean_text(text: Any) -> str:
    """Remove emojis and clean text for n8n compatibility."""
    if not isinstance(text, str):
        return str(text) if text is not None else ""
    
    # Remove emojis and special unicode characters
    import re
    # Remove emoji pattern
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub('', text).strip()


def _load_config() -> Optional[Dict[str, Any]]:
    """Load n8n config file if present."""
    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return None


def _get_base_url() -> Optional[str]:
    cfg = _load_config()
    if not cfg:
        return None
    base = cfg.get("webhook_base_url")
    if isinstance(base, str) and base.strip():
        return base.strip().rstrip("/")
    return None

def _build_url(endpoint: str) -> Optional[str]:
    """Build final webhook URL safely, supporting both base forms.

    Accepts either config base as ".../webhook" or full endpoint like
    ".../webhook/feedback-submitted". Avoids double-appending.
    """
    base = _get_base_url()
    print(f"[n8n] Base URL: {base}")
    if not base:
        return None

    b = base.rstrip("/")
    ep = endpoint.strip("/")

    # If base already ends with the endpoint, use as-is
    if b.endswith("/" + ep):
        return b
    # If base is exactly the webhook root, append endpoint
    if b.endswith("/webhook"):
        return f"{b}/{ep}"
    # Otherwise, append endpoint once
    return f"{b}/{ep}"


def _post(url: str, payload: Dict[str, Any]) -> bool:
    """POST JSON to URL with proper headers, return True on 2xx, False otherwise, with logging."""
    try:
        # Critical: Add proper headers for n8n webhook
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "CitizenFeedbackApp/1.0"
        }
        
        print(f"[n8n] Sending to: {url}")
        print(f"[n8n] Headers: {headers}")
        print(f"[n8n] Payload: {json.dumps(payload, indent=2)}")
        
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        
        print(f"[n8n] Status Code: {resp.status_code}")
        print(f"[n8n] Response Headers: {dict(resp.headers)}")
        
        # Limit body size to avoid noisy logs
        body = resp.text if len(resp.text) <= 500 else resp.text[:500]
        print(f"[n8n] Response Body: {body}")
        
        if 200 <= resp.status_code < 300:
            print(f"[n8n] ✅ SUCCESS: Webhook call successful")
            return True
        else:
            print(f"[n8n] ❌ FAILED: HTTP {resp.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"[n8n] ❌ ERROR: Request timeout after 15 seconds")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"[n8n] ❌ ERROR: Connection failed - {e}")
        return False
    except Exception as e:
        print(f"[n8n] ❌ ERROR: Unexpected error - {type(e).__name__}: {e}")
        return False


def send_feedback_submitted(entry: Dict[str, Any]) -> bool:
    """Send 'feedback-submitted' event to n8n.

    Expects fields similar to the guide. Falls back gracefully if config missing.
    """
    url = _build_url("feedback-submitted")
    if not url:
        print("[n8n] ❌ No webhook URL configured in data/n8n_config.json")
        return False

    print(f"\n" + "="*60)
    print(f"[n8n] 🚀 SENDING FEEDBACK TO n8n")
    print(f"="*60)
    print(f"[n8n] Entry keys received: {list(entry.keys())}")

    # Clean all text fields and use safe fallbacks for key names
    # Map from your app fields (id, name, email) to n8n expected fields
    citizen_email = _clean_text(entry.get("citizen_email") or entry.get("email") or "")
    
    payload = {
        "feedback_id": _clean_text(entry.get("feedback_id") or entry.get("id") or ""),
        "citizen_name": _clean_text(entry.get("citizen_name") or entry.get("name") or ""),
        "citizen_email": citizen_email,
        "email": citizen_email,  # Send as both field names for compatibility
        "citizen_phone": _clean_text(entry.get("citizen_phone") or entry.get("phone") or "N/A"),
        "category": _clean_text(entry.get("category") or ""),
        "title": _clean_text(entry.get("title") or ""),
        "feedback": _clean_text(entry.get("feedback") or ""),
        "location": _clean_text(entry.get("location") or entry.get("area") or ""),
        "urgency": _clean_text(entry.get("urgency") or "Normal"),
        "timestamp": _clean_text(entry.get("timestamp") or ""),
        "status": _clean_text(entry.get("status") or "New"),
        "sentiment": _clean_text(entry.get("sentiment") or "Neutral"),
    }
    
    # Validation
    required_fields = ["feedback_id", "citizen_name", "citizen_email", "feedback"]
    missing = [f for f in required_fields if not payload.get(f)]
    if missing:
        print(f"[n8n] ⚠️ WARNING: Missing required fields: {missing}")
        print(f"[n8n] Available entry data: {entry}")
    
    print(f"[n8n] Final URL: {url}")
    result = _post(url, payload)
    print(f"[n8n] Final Result: {'✅ SUCCESS' if result else '❌ FAILED'}")
    print(f"="*60 + "\n")
    return result


def send_feedback_resolved(entry: Dict[str, Any]) -> bool:
    """Send 'feedback-resolved' event to n8n using entry data.

    Maps admin notes to resolution_notes and uses updated_at as resolved_timestamp.
    """
    url = _build_url("feedback-resolved")
    if not url:
        return False

    # Clean all text fields
    payload = {
        "feedback_id": _clean_text(entry.get("feedback_id") or entry.get("id")),
        "citizen_name": _clean_text(entry.get("citizen_name") or entry.get("name")),
        "citizen_email": _clean_text(entry.get("citizen_email") or entry.get("email")),
        "category": _clean_text(entry.get("category")),
        "title": _clean_text(entry.get("title")),
        "original_feedback": _clean_text(entry.get("feedback")),
        "original_timestamp": _clean_text(entry.get("timestamp")),
        "resolved_timestamp": _clean_text(entry.get("updated_at") or entry.get("resolved_timestamp")),
        "assigned_to": _clean_text(entry.get("assigned_to")),
        "resolution_notes": _clean_text(entry.get("admin_notes")),
    }
    print(f"[n8n] Resolved payload: {payload}")
    print(f"[n8n] Sending to: {url}")
    result = _post(url, payload)
    print(f"[n8n] Result: {result}")
    return result
