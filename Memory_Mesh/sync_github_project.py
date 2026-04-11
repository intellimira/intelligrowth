#!/usr/bin/env python3
"""
MIRA GitHub Project Sync Script v2
Tracks commits and PRs + manages status progression

Methods supported:
1. Tell me verbally - "Move X to In Progress"
2. Commit keywords - "[WIP]" in commit, "[DONE]" on merge
3. Labels - Add labels to issues/PRs
4. Manual - I update based on your commands

Usage:
  python3 sync_github_project.py           # Auto-sync commits/PRs
  python3 sync_github_project.py --status   # Update statuses based on keywords
  python3 sync_github_project.py --dry-run   # Test without making changes
"""

import subprocess
import json
import os
import sys
import re
from datetime import datetime

# Configuration
REPO_OWNER = "intellimira"
REPO_NAME = "MiRA"
PROJECT_NUMBER = 1
MY_USERNAME = "intellimira"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Project IDs
PROJECT_ID = "PVT_kwHODz-jIc4BTEtU"
STATUS_FIELD_ID = "PVTSSF_lAHODz-jIc4BTEtUzhAa_ro"

# Status option IDs
STATUS_OPTIONS = {"Todo": "f75ad846", "In Progress": "47fc9ee4", "Done": "98236657"}

# Keywords for auto-status
WIP_KEYWORDS = ["[WIP]", "[WIP]", "WIP", "work in progress", "in progress"]
DONE_KEYWORDS = ["[DONE]", "[DONE]", "DONE", "merged", "completed", "fixed"]

DRY_RUN = "--dry-run" in sys.argv
UPDATE_STATUS = "--status" in sys.argv


def run_gh(command):
    """Run gh CLI command and return output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode


def get_recent_commits(limit=10):
    """Get recent commits from the repo"""
    cmd = f"gh api repos/{REPO_OWNER}/{REPO_NAME}/commits?per_page={limit}"
    output, _ = run_gh(cmd)
    if not output:
        return []
    return json.loads(output)


def get_recent_prs(limit=10):
    """Get recent PRs from the repo"""
    cmd = f"gh api repos/{REPO_OWNER}/{REPO_NAME}/pulls?per_page={limit}&state=all"
    output, _ = run_gh(cmd)
    if not output:
        return []
    return json.loads(output)


def get_existing_items():
    """Get existing project items to avoid duplicates"""
    cmd = f"gh project item-list {PROJECT_NUMBER} --owner @me --format json"
    output, _ = run_gh(cmd)
    if not output:
        return {}

    try:
        items = json.loads(output)
        # Return dict with title as key
        return {item.get("title", ""): item for item in items}
    except:
        return {}


def determine_status_from_message(message):
    """Determine status based on commit/PR message keywords"""
    msg_lower = message.lower()

    # Check for WIP keywords
    for kw in WIP_KEYWORDS:
        if kw.lower() in msg_lower:
            return "In Progress"

    # Check for DONE keywords (for merged PRs)
    for kw in DONE_KEYWORDS:
        if kw.lower() in msg_lower:
            return "Done"

    # Default to Todo for new items
    return "Todo"


def create_project_item(title, body="", status="Todo"):
    """Create a new item in the project"""
    if DRY_RUN:
        print(f"  [DRY RUN] Would create: {title}")
        print(f"    Status: {status}")
        return

    # Create draft item
    cmd = f'gh project item-create {PROJECT_NUMBER} --owner @me --title "{title}"'
    output, code = run_gh(cmd)

    if code != 0 or not output:
        print(f"  Failed to create item: {title}")
        return

    try:
        # Try to parse JSON output
        item = json.loads(output)
        item_id = item.get("id")
        if item_id:
            # Update status via GraphQL
            update_item_status(item_id, status)
            print(f"  Created: {title} [{status}]")
    except:
        print(f"  Created: {title}")


def update_item_status(item_id, status):
    """Update the status field of a project item"""
    status_id = STATUS_OPTIONS.get(status)
    if not status_id:
        return

    # Use GraphQL to update the status field
    query = f'''
    mutation {{
      updateProjectV2ItemFieldValue(
        input: {{
          projectId: "{PROJECT_ID}",
          itemId: "{item_id}",
          fieldId: "{STATUS_FIELD_ID}",
          value: {{ singleSelectOptionId: "{status_id}" }}
        }}
      ) {{ projectV2Item {{ id }} }}
    }}
    '''

    # Escape the query for command line
    cmd = f'gh api graphql -f query="{query.replace(chr(10), " ").strip()}"'
    run_gh(cmd)


def move_item_to_status(title, new_status):
    """Move an existing item to a new status"""
    items = get_existing_items()

    # Find item with matching title
    item = items.get(title)
    if not item:
        # Try partial match
        for item_title, item_data in items.items():
            if title.lower() in item_title.lower():
                item = item_data
                break

    if not item:
        print(f"  Could not find item: {title}")
        return

    item_id = item.get("id")
    if not item_id:
        print(f"  Could not get ID for: {title}")
        return

    if DRY_RUN:
        print(f"  [DRY RUN] Would move '{title}' to {new_status}")
        return

    update_item_status(item_id, new_status)
    print(f"  ✅ Moved '{title}' to {new_status}")


def sync_commits():
    """Sync recent commits to project"""
    print("\n📡 Fetching commits...")
    commits = get_recent_commits(10)

    if not commits:
        print("  No commits found")
        return

    existing = get_existing_items()
    print(f"  Found {len(commits)} commits")
    created = 0

    for commit in commits:
        author = commit.get("commit", {}).get("author", {}).get("name", "unknown")
        login = commit.get("author", {}).get("login", "")
        sha = commit.get("sha", "")[:7]
        message = commit.get("commit", {}).get("message", "").split("\n")[0][:50]

        title = f"commit: {sha} - {message}"

        if title in existing:
            # Item exists - check if we should update status
            if UPDATE_STATUS:
                status = determine_status_from_message(message)
                move_item_to_status(title, status)
            continue

        # Determine status from keywords
        status = determine_status_from_message(message)

        # Determine category based on author
        if login == MY_USERNAME or login == "":
            category = "My Work"
        else:
            category = "Contributors"

        create_project_item(title, f"Author: {author}\nSHA: {sha}", status)
        created += 1

    print(f"  Created {created} new items")


def sync_prs():
    """Sync recent PRs to project"""
    print("\n📡 Fetching PRs...")
    prs = get_recent_prs(10)

    if not prs:
        print("  No PRs found")
        return

    existing = get_existing_items()
    print(f"  Found {len(prs)} PRs")
    created = 0

    for pr in prs:
        number = pr.get("number")
        title = pr.get("title", "")[:50]
        author = pr.get("user", {}).get("login", "unknown")
        state = pr.get("state", "open")
        merged = pr.get("merged", False)

        pr_title = f"PR #{number}: {title}"

        if pr_title in existing:
            # Update status based on PR state
            if UPDATE_STATUS:
                if merged:
                    status = "Done"
                elif state == "open":
                    status = "In Progress"
                else:
                    status = "Todo"
                move_item_to_status(pr_title, status)
            continue

        # Determine status
        if merged:
            status = "Done"
        elif state == "open":
            status = "In Progress"
        else:
            status = "Todo"

        if author == MY_USERNAME:
            category = "My Work"
        else:
            category = "Contributors"

        create_project_item(pr_title, f"Author: {author}\nState: {state}", status)
        created += 1

    print(f"  Created {created} new items")


def show_usage_examples():
    """Show examples of how to use this system"""
    print("\n" + "=" * 50)
    print("📋 STATUS PROGRESSION METHODS")
    print("=" * 50)
    print("""
1. VERBAL: Tell me "Move [item] to In Progress" or "Mark [item] Done"

2. COMMIT KEYWORDS:
   - Add "[WIP]" in commit → Auto-sets to "In Progress"
   - Merge PR with "DONE" keyword → Auto-sets to "Done"
   - Example: git commit -m "feat: new feature [WIP]"

3. LABELS: (coming soon)
   - Add "in-progress" label to PR → Sets status
   - Add "done" label → Sets to Done

4. MANUAL: Just ask me!
   - "Set project item X to Done"
   - "What's currently In Progress?"
""")
    print("=" * 50)


def main():
    print("🔄 MIRA GitHub Project Sync v2")
    print(f"  Project: MiRA Development Tracker")
    print(f"  Repo: {REPO_OWNER}/{REPO_NAME}")
    print(f"  Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")
    print(f"  Status Update: {'YES' if UPDATE_STATUS else 'NO'}")

    if not GITHUB_TOKEN:
        print("\n⚠️  Warning: GITHUB_TOKEN not set")

    # Show examples if --help or no args
    if len(sys.argv) == 1:
        show_usage_examples()

    sync_commits()
    sync_prs()

    print("\n✅ Sync complete!")


if __name__ == "__main__":
    main()
