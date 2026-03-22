#!/usr/bin/env python3
"""
MIRA Secure Config Loader
Loads credentials from ~/.env/mira_config
"""

import os
import json
import urllib.request
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv

# Load from secure config
CONFIG_FILE = Path.home() / ".env" / "mira_config"


def load_config():
    """Load configuration from secure .env file"""
    if CONFIG_FILE.exists():
        load_dotenv(CONFIG_FILE)
        return True
    return False


def get_telegram_token():
    """Get Telegram bot token"""
    load_config()
    return os.environ.get("MIRA_TELEGRAM_BOT_TOKEN", "")


def get_telegram_chat_id():
    """Get Telegram chat ID"""
    load_config()
    return os.environ.get("MIRA_TELEGRAM_CHAT_ID", "")


def get_gmail_password():
    """Get Gmail app password"""
    load_config()
    return os.environ.get("HIMALAYA_PASSWORD", "")


def get_enquiries_repo():
    """Get enquiries repo path"""
    load_config()
    return os.environ.get("ENQUIRIES_REPO", "/home/sir-v/MiRA/enquiries_local")


def fetch_telegram_chat_id():
    """Fetch chat ID from Telegram by calling getUpdates API"""
    token = get_telegram_token()
    if not token:
        return None, "No Telegram bot token configured"

    url = f"https://api.telegram.org/bot{token}/getUpdates"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

            if data.get("ok") and data.get("result"):
                # Get the chat from the first update
                for update in data["result"]:
                    if "message" in update:
                        chat = update["message"].get("chat", {})
                        if chat.get("username") == "Sirswali":
                            return chat.get("id"), None
                        # Return first chat found if username doesn't match
                        return chat.get("id"), None
                return None, "No messages from @Sirswali found"
            return None, "No updates available (send message to @intellimirabot first)"

    except Exception as e:
        return None, str(e)


def update_telegram_chat_id():
    """Fetch and save the Telegram chat ID"""
    chat_id, error = fetch_telegram_chat_id()

    if error:
        return False, error

    # Read current config
    with open(CONFIG_FILE) as f:
        content = f.read()

    # Replace PENDING_FETCH with actual chat_id
    new_content = content.replace(
        "MIRA_TELEGRAM_CHAT_ID=PENDING_FETCH", f"MIRA_TELEGRAM_CHAT_ID={chat_id}"
    )

    # Write back
    with open(CONFIG_FILE, "w") as f:
        f.write(new_content)

    return True, chat_id


def validate_config():
    """Validate configuration and return status"""
    load_config()

    token = get_telegram_token()
    chat_id = get_telegram_chat_id()

    issues = []

    if not token:
        issues.append("Telegram bot token not set")
    if not chat_id or chat_id == "PENDING_FETCH":
        issues.append("Telegram chat_id not set (send message to @intellimirabot)")

    if issues:
        return False, issues
    return True, []


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Config Manager")
    parser.add_argument("--status", action="store_true", help="Show config status")
    parser.add_argument(
        "--update-chat-id",
        action="store_true",
        help="Fetch and update Telegram chat ID",
    )
    parser.add_argument(
        "--test-gmail", action="store_true", help="Test Gmail connection"
    )

    args = parser.parse_args()

    if args.update_chat_id:
        print("📡 Fetching Telegram chat ID...")
        success, result = update_telegram_chat_id()
        if success:
            print(f"✅ Chat ID updated: {result}")
        else:
            print(f"❌ Failed: {result}")
            print("\n   Make sure to:")
            print("   1. Open Telegram")
            print("   2. Send any message to @intellimirabot")
            print("   3. Then run this command again")

    elif args.test_gmail:
        import imaplib

        print("📧 Testing Gmail connection...")
        password = get_gmail_password()
        if not password:
            print("❌ No Gmail password set")
        else:
            try:
                mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
                mail.login("intellimira@gmail.com", password)
                print("✅ Gmail connection successful!")
                mail.logout()
            except Exception as e:
                print(f"❌ Gmail connection failed: {e}")

    else:
        # Default: show status
        load_config()
        print("📋 MIRA Config Status")
        print("=" * 40)

        token = get_telegram_token()
        chat_id = get_telegram_chat_id()
        gmail_pw = get_gmail_password()

        print(f"Telegram Token: {'✅ Set' if token else '❌ Missing'}")
        print(
            f"Telegram Chat ID: {'✅ Set' if chat_id and chat_id != 'PENDING_FETCH' else '⚠️ PENDING'}"
        )
        print(f"Gmail Password: {'✅ Set' if gmail_pw else '❌ Missing'}")
        print(f"Enquiries Repo: {get_enquiries_repo()}")

        valid, issues = validate_config()
        if not valid:
            print("\n⚠️ Configuration Issues:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("\n✅ All systems configured!")
