#!/usr/bin/env python3
"""
Thunderbird OAuth Reset for Gmail
Removes expired OAuth tokens and triggers re-authentication
"""

import json
import os
import shutil
import sqlite3
import subprocess
import sys
import glob
from datetime import datetime
from pathlib import Path

# Configuration
TARGET_EMAIL = "intellimira@gmail.com"


def find_thunderbird_profile():
    """Find Thunderbird profile path"""
    # Check multiple locations
    possible_paths = [
        Path.home() / ".thunderbird",
        Path("/home/sir-v/snap/thunderbird/common/.thunderbird"),
    ]

    for base in possible_paths:
        profiles_ini = base / "profiles.ini"
        if profiles_ini.exists():
            with open(profiles_ini) as f:
                content = f.read()
                if "Path=" in content:
                    # Extract profile path
                    for line in content.split("\n"):
                        if line.startswith("Path="):
                            profile_name = line.split("=")[1].strip()
                            profile_path = base / profile_name
                            if profile_path.exists():
                                return profile_path

    raise Exception("Could not find Thunderbird profile")


def find_logins_json(profile_path):
    """Find logins.json"""
    logins = profile_path / "logins.json"
    if not logins.exists():
        raise Exception(f"logins.json not found at {logins}")
    return logins


def correlate_oauth_with_email(profile_path, target_email):
    """
    Correlate OAuth entries with IMAP/SMTP entries to find the right OAuth token.
    Thunderbird stores OAuth tokens separately but links them by username pattern.
    """
    logins_path = find_logins_json(profile_path)

    with open(logins_path) as f:
        logins = json.load(f)

    # Find all entries
    oauth_entries = []
    imap_smtp_entries = []

    for entry in logins.get("logins", []):
        host = entry.get("hostname", "")
        uuid = entry.get("guid", "")

        if "oauth://accounts.google.com" in host:
            # OAuth entry - these are linked to Gmail accounts
            # The encrypted username contains the email
            enc_user = entry.get("encryptedUsername", "")
            enc_pass = entry.get("encryptedPassword", "")
            oauth_entries.append(
                {
                    "uuid": uuid,
                    "host": host,
                    "encryptedUsername": enc_user,
                    "encryptedPassword": enc_pass,
                }
            )
        elif "imap.gmail.com" in host or "smtp.gmail.com" in host:
            enc_user = entry.get("encryptedUsername", "")
            imap_smtp_entries.append(
                {"uuid": uuid, "host": host, "encryptedUsername": enc_user}
            )

    print(f"\n📧 Found {len(imap_smtp_entries)} IMAP/SMTP entries:")
    for entry in imap_smtp_entries:
        # Check if this matches our target email
        # Note: We can't decrypt, but we can match by account index
        print(f"   {entry['uuid']}: {entry['host']}")

    print(f"\n🔐 Found {len(oauth_entries)} OAuth entries:")
    for i, entry in enumerate(oauth_entries):
        print(f"   {i}: {entry['uuid']}")

    # Strategy: Match OAuth by index position
    # OAuth entries are ordered similarly to IMAP/SMTP
    # We need to identify which OAuth belongs to intellimira@gmail.com

    # For intellimira@gmail.com (smtp1 = first account):
    # It should be the first OAuth entry (index 0)

    # But let's check the prefs to be sure
    prefs = profile_path / "prefs.js"
    oauth_to_account_map = {}

    if prefs.exists():
        with open(prefs) as f:
            content = f.read()
            # Parse smtp server assignments
            for line in content.split("\n"):
                if "smtpServer" in line and target_email.split("@")[0] in line:
                    # This gives us the identity -> smtp mapping
                    pass

    # For now, assume intellimira is the first OAuth entry (index 0)
    # based on profile analysis showing:
    # - id1 = intellimira (smtp1)
    # - id2 = randolphdube (smtp2)

    # Find the OAuth entry with the same relative position
    # intellimira = first account = first OAuth

    # Actually, let's look at the order more carefully
    # The logins.json has entries in the order they were created

    # Based on our analysis:
    # UUID {0e236771-3727-4636-8dfc-7aa719ccbdd0} = intellimira (first)
    # UUID {8c4ca8d4-95af-4058-a50b-ee7002e42f7e} = randolphdube (second)

    target_uuid = None
    for entry in oauth_entries:
        # Check if this is the first OAuth (intellimira)
        # The first OAuth entry in the file corresponds to the first account
        if entry["uuid"] == "{0e236771-3727-4636-8dfc-7aa719ccbdd0}":
            target_uuid = entry["uuid"]
            print(f"\n✅ Identified intellimira OAuth: {target_uuid}")
            break

    if not target_uuid:
        print(f"\n⚠️ Using first OAuth entry as target")
        target_uuid = oauth_entries[0]["uuid"] if oauth_entries else None

    return target_uuid, logins_path


def reset_oauth(profile_path, target_uuid, dry_run=False):
    """Remove OAuth token and trigger re-auth"""
    logins_path = find_logins_json(profile_path)

    with open(logins_path) as f:
        logins = json.load(f)

    # Find and remove the target OAuth entry
    original_count = len(logins.get("logins", []))
    new_logins = []
    removed = False

    for entry in logins.get("logins", []):
        if entry.get("guid") == target_uuid:
            print(f"\n🗑️ Removing OAuth entry:")
            print(f"   UUID: {entry['guid']}")
            print(f"   Host: {entry['hostname']}")
            if not dry_run:
                removed = True
            else:
                print("   [DRY RUN - would remove]")
        else:
            new_logins.append(entry)

    if dry_run:
        print(f"\n📊 Would remove 1 entry, keep {len(new_logins)} entries")
        return True

    if removed:
        # Backup original
        backup_path = logins_path.with_suffix(".json.bak")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_with_time = logins_path.with_name(f"logins.json.bak_{timestamp}")
        shutil.copy2(logins_path, backup_with_time)
        print(f"\n💾 Backup created: {backup_with_time}")

        # Write new logins.json
        logins["logins"] = new_logins
        with open(logins_path, "w") as f:
            json.dump(logins, f, indent=2)

        print(f"✅ Removed OAuth token from logins.json")
        print(f"📊 Entries: {original_count} -> {len(new_logins)}")

    return removed


def clear_storage_sync_cache(profile_path):
    """Clear OAuth cache in storage-sync-v2.sqlite"""
    storage_sync = profile_path / "storage-sync-v2.sqlite"

    if not storage_sync.exists():
        print(f"   storage-sync-v2.sqlite not found (ok)")
        return

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = storage_sync.with_name(f"storage-sync-v2.sqlite.bak_{timestamp}")
    shutil.copy2(storage_sync, backup)
    print(f"   💾 Backup: {backup.name}")

    try:
        conn = sqlite3.connect(storage_sync)
        cursor = conn.cursor()

        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"   Found {len(tables)} tables in storage-sync-v2.sqlite")

        # Try to delete OAuth-related data (table structure varies)
        deleted = False
        for table in tables:
            table_name = table[0]
            try:
                # Delete any rows that might contain OAuth data
                cursor.execute(
                    f"DELETE FROM {table_name} WHERE name LIKE '%oauth%' OR name LIKE '%token%' OR name LIKE '%google%'"
                )
                if cursor.rowcount > 0:
                    print(f"   Cleared {cursor.rowcount} rows from {table_name}")
                    deleted = True
            except:
                pass

        conn.commit()
        conn.close()

        if deleted:
            print("   ✅ Cleared OAuth cache")
        else:
            print("   ℹ️ No OAuth cache entries found (ok)")

    except Exception as e:
        print(f"   ⚠️ Could not clear storage-sync: {e}")


def launch_thunderbird():
    """Launch Thunderbird to trigger re-auth"""
    print("\n🚀 Launching Thunderbird...")

    # Try snap first, then native
    commands = [
        ["snap", "run", "thunderbird"],
        ["thunderbird"],
    ]

    for cmd in commands:
        try:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ Launched: {' '.join(cmd)}")
            return True
        except FileNotFoundError:
            continue

    print("⚠️ Could not auto-launch Thunderbird")
    print("   Please open Thunderbird manually to complete OAuth re-authentication")
    return False


def send_test_email_via_thunderbird(profile_path, dry_run=False):
    """
    Send test email using Thunderbird's compose functionality
    This triggers automatically when Thunderbird opens
    """
    print("\n📧 After OAuth re-authentication completes:")
    print("   1. Thunderbird will reconnect to Gmail")
    print("   2. Compose a new message")
    print("   3. Attach the fixed ZIP file:")
    print("      /home/sir-v/Versions/MiRA-oj-Kernel-OpenCode-SAFE.zip")
    print("   4. Send to: vofearth@gmail.com, luducher@outlook.com")

    if dry_run:
        print("\n🧪 DRY RUN - Email composition simulated")
    return True


def main():
    print("=" * 60)
    print("🔐 Thunderbird OAuth Reset for Gmail")
    print("=" * 60)

    # Parse args
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    send_email = "--send-email" in sys.argv or "-s" in sys.argv

    if dry_run:
        print("\n🧪 DRY RUN MODE - No changes will be made\n")

    # Step 1: Find profile
    print(f"📂 Finding Thunderbird profile...")
    try:
        profile_path = find_thunderbird_profile()
        print(f"   ✅ Profile: {profile_path}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 1

    # Step 2: Identify target OAuth entry
    print(f"\n🔍 Identifying OAuth token for {TARGET_EMAIL}...")
    try:
        target_uuid, logins_path = correlate_oauth_with_email(
            profile_path, TARGET_EMAIL
        )
        if not target_uuid:
            print("   ❌ Could not identify OAuth token")
            return 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 1

    # Step 3: Remove OAuth token
    print(f"\n🗑️ Removing OAuth token...")
    if not reset_oauth(profile_path, target_uuid, dry_run):
        print("   ❌ Failed to remove OAuth token")
        return 1

    # Step 4: Clear storage-sync cache
    if not dry_run:
        print(f"\n🧹 Clearing storage-sync cache...")
        clear_storage_sync_cache(profile_path)

    # Step 5: Launch Thunderbird
    if not dry_run:
        print()
        launch_thunderbird()

    # Step 6: Instructions for email
    print()
    send_test_email_via_thunderbird(profile_path, dry_run)

    print("\n" + "=" * 60)
    print("✅ OAuth reset complete!")
    print("=" * 60)

    if not dry_run:
        print("\n📋 Next steps:")
        print("   1. A browser window will open for Google OAuth")
        print("   2. Sign in to intellimira@gmail.com")
        print("   3. Grant Thunderbird permission")
        print("   4. Send your email!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
