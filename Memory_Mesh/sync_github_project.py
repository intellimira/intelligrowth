#!/usr/bin/env python3
"""
MIRA GitHub Project Sync Script
Tracks commits and PRs to GitHub Project board

Usage: python3 sync_project.py [--dry-run]
"""

import subprocess
import json
import os
import sys
from datetime import datetime

# Configuration
REPO_OWNER = "intellimira"
REPO_NAME = "MiRA"
PROJECT_NUMBER = 1
MY_USERNAME = "intellimira"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Project IDs
PROJECT_ID = "PVT_kwHODz-jIc4BTEtU"
CATEGORY_FIELD_ID = "PVTSSF_lAHODz-jIc4BTEtUzhBf7SI"
TYPE_FIELD_ID = "PVTSSF_lAHODz-jIc4BTEtUzhBf7jE"

# Field option IDs
OPTIONS = {
    "My Work": "b9dacb9d",  # You'll need to get actual ID
    "Contributors": "6e4d9c8d",
    "Planned": "5e3d8c7d",
    "Commit": "7f5e4d3d",
    "PR": "8e6f5e4d",
    "Issue": "9f7e6f5d",
}

DRY_RUN = "--dry-run" in sys.argv


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
        return set()

    try:
        items = json.loads(output)
        # Extract titles to check for duplicates
        existing = set()
        for item in items:
            if "title" in item:
                existing.add(item["title"])
        return existing
    except:
        return set()


def create_project_item(title, body, category, item_type):
    """Create a new item in the project"""
    if DRY_RUN:
        print(f"  [DRY RUN] Would create: {title}")
        print(f"    Category: {category}, Type: {item_type}")
        return

    # Create draft item
    cmd = f'gh project item-create {PROJECT_NUMBER} --owner @me --title "{title}" --format json'
    output, code = run_gh(cmd)

    if code != 0 or not output:
        print(f"  Failed to create item: {title}")
        return

    try:
        item = json.loads(output)
        item_id = item.get("id")
        if item_id:
            # Note: gh project doesn't easily support setting custom fields via CLI
            # Would need GraphQL for that
            print(f"  Created: {title}")
    except Exception as e:
        print(f"  Error parsing response: {e}")


def sync_commits():
    """Sync recent commits to project"""
    print("\n📡 Fetching commits...")
    commits = get_recent_commits(10)

    if not commits:
        print("  No commits found")
        return

    existing = get_existing_items()

    print(f"  Found {len(commits)} commits")

    for commit in commits:
        author = commit.get("commit", {}).get("author", {}).get("name", "unknown")
        login = commit.get("author", {}).get("login", "")
        sha = commit.get("sha", "")[:7]
        message = commit.get("commit", {}).get("message", "").split("\n")[0][:50]

        title = f"commit: {sha} - {message}"

        if title in existing:
            continue

        # Determine category based on author
        if login == MY_USERNAME or login == "":
            category = "My Work"
        else:
            category = "Contributors"

        create_project_item(title, f"Author: {author}\nSHA: {sha}", category, "Commit")


def sync_prs():
    """Sync recent PRs to project"""
    print("\n📡 Fetching PRs...")
    prs = get_recent_prs(10)

    if not prs:
        print("  No PRs found")
        return

    existing = get_existing_items()
    print(f"  Found {len(prs)} PRs")

    for pr in prs:
        number = pr.get("number")
        title = pr.get("title", "")[:50]
        author = pr.get("user", {}).get("login", "unknown")
        state = pr.get("state", "open")

        pr_title = f"PR #{number}: {title}"

        if pr_title in existing:
            continue

        if author == MY_USERNAME:
            category = "My Work"
        else:
            category = "Contributors"

        create_project_item(
            pr_title, f"Author: {author}\nState: {state}", category, "PR"
        )


def main():
    print("🔄 MIRA GitHub Project Sync")
    print(f"  Project: MiRA Development Tracker")
    print(f"  Repo: {REPO_OWNER}/{REPO_NAME}")
    print(f"  Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")

    if not GITHUB_TOKEN:
        print("\n⚠️  Warning: GITHUB_TOKEN not set")

    sync_commits()
    sync_prs()

    print("\n✅ Sync complete!")


if __name__ == "__main__":
    main()
