#!/usr/bin/env python3
"""
MIRA Telegram Alert System
Sends Telegram notifications for qualified leads.
"""

import json
import os
import sys
from pathlib import Path

# Configuration
TELEGRAM_BOT_TOKEN = os.environ.get("MIRA_TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("MIRA_TELEGRAM_CHAT_ID", "")
ENQUIRIES_REPO = "/home/sir-v/MiRA/enquiries_local"


def send_telegram_message(message, silent=False):
    """Send message via Telegram Bot API"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(
            "⚠️ Telegram not configured. Set MIRA_TELEGRAM_BOT_TOKEN and MIRA_TELEGRAM_CHAT_ID"
        )
        print(f"Message:\n{message}")
        return False

    import urllib.request
    import urllib.parse

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_notification": silent,
    }

    try:
        req = urllib.request.Request(
            url, data=urllib.parse.urlencode(data).encode(), method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            return result.get("ok", False)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False


def format_lead_alert(lead):
    """Format a lead as Telegram alert"""
    score = lead.get("pain_score", 0)
    urgency = lead.get("urgency", "")

    message = f"""
{urgency} <b>New Lead Alert</b>

<b>Name:</b> {lead.get("name", "Unknown")}
<b>Email:</b> {lead.get("email", "N/A")}
<b>Interest:</b> {lead.get("interest", "other").upper()}
<b>Company:</b> {lead.get("company", "N/A")}

<b>Pain Score:</b> {score}/10
<b>Action:</b> {lead.get("recommended_action", "Review")}

<b>Message:</b>
{lead.get("message", "No message")[:300]}...
"""
    return message


def check_and_alert():
    """Check for new qualified leads and send alerts"""
    repo = Path(ENQUIRIES_REPO)
    if not repo.exists():
        print("Enquiries repo not found. Run poll_enquiries.py first.")
        return

    alerted_file = repo / ".alerted_leads"
    alerted_ids = set()

    if alerted_file.exists():
        with open(alerted_file) as f:
            alerted_ids = set(json.load(f))

    new_alerts = []

    for folder in ["prospects", "outreach"]:
        folder_path = repo / folder
        if not folder_path.exists():
            continue

        for json_file in folder_path.glob("*.json"):
            try:
                with open(json_file) as f:
                    lead = json.load(f)

                lead_id = lead.get("id")
                score = lead.get("pain_score", 0)

                # Alert if score >= 7 and not already alerted
                if score >= 7 and lead_id not in alerted_ids:
                    if send_telegram_message(format_lead_alert(lead)):
                        alerted_ids.add(lead_id)
                        new_alerts.append(lead_id)
                        print(f"✅ Alert sent for {lead.get('name')} (score: {score})")
                    else:
                        print(f"❌ Failed to alert {lead.get('name')}")

            except Exception as e:
                print(f"Error processing {json_file}: {e}")

    # Save alerted IDs
    with open(alerted_file, "w") as f:
        json.dump(list(alerted_ids), f)

    if new_alerts:
        print(f"\n📱 Sent {len(new_alerts)} Telegram alerts")
    else:
        print("No new qualified leads to alert.")


def send_weekly_digest():
    """Send weekly digest of all leads"""
    from score_leads import process_leads_from_repo, generate_report

    repo = Path(ENQUIRIES_REPO)
    if not repo.exists():
        return

    results = process_leads_from_repo(repo)
    report = generate_report(results)

    message = f"""
📊 <b>Weekly Lead Digest</b>

{report}

Reply with any question to get MIRA's analysis.
"""

    send_telegram_message(message, silent=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Telegram Alert System")
    parser.add_argument("--digest", action="store_true", help="Send weekly digest")
    parser.add_argument(
        "--check", action="store_true", help="Check and alert new leads"
    )

    args = parser.parse_args()

    if args.digest:
        send_weekly_digest()
    else:
        check_and_alert()
