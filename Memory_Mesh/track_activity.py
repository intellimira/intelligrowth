#!/usr/bin/env python3
"""
MIRA GitHub Activity Tracker
Tracks forks, contributors, stars, and watchers

Usage:
  python3 track_activity.py              # Track all activity
  python3 track_activity.py --forks      # Track only forks
  python3 track_activity.py --contributors # Track only contributors
  python3 track_activity.py --dry-run    # Test without changes
"""

import subprocess
import json
import os
import sys
import re
from datetime import datetime

# Configuration
REPO_OWNER = "intellimira"
REPOS = ["MiRA", "intelligrowth", "mira-portfolio"]  # Add more repos as needed
PROJECT_NUMBER = 1
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Project IDs
PROJECT_ID = "PVT_kwHODz-jIc4BTEtU"
STATUS_FIELD_ID = "PVTSSF_lAHODz-jIc4BTEtUzhAa_ro"

# Status option IDs
STATUS_OPTIONS = {"Todo": "f75ad846", "In Progress": "47fc9ee4", "Done": "98236657"}

DRY_RUN = "--dry-run" in sys.argv
TRACK_FORKS = "--forks" in sys.argv
TRACK_CONTRIBUTORS = "--contributors" in sys.argv
TRACK_STARS = "--stars" in sys.argv
TRACK_ALL = not (TRACK_FORKS or TRACK_CONTRIBUTORS or TRACK_STARS)


def run_gh(command):
    """Run gh CLI command and return output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode


def load_tracking_data():
    """Load previously tracked data"""
    data_file = "/home/sir-v/MiRA/Memory_Mesh/github_activity.json"
    if os.path.exists(data_file):
        try:
            with open(data_file) as f:
                return json.load(f)
        except:
            pass
    return {"forks": [], "contributors": [], "stars": []}


def save_tracking_data(data):
    """Save tracking data"""
    data_file = "/home/sir-v/MiRA/Memory_Mesh/github_activity.json"
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)


def get_existing_items():
    """Get existing project items to avoid duplicates"""
    cmd = f"gh project item-list {PROJECT_NUMBER} --owner @me --format json"
    output, _ = run_gh(cmd)
    if not output:
        return {}

    try:
        items = json.loads(output)
        return {item.get("title", ""): item for item in items}
    except:
        return {}


def create_project_item(title, item_type, status="Todo"):
    """Create a new item in the project"""
    if DRY_RUN:
        print(f"  [DRY RUN] Would create: {title} ({item_type})")
        return

    cmd = f'gh project item-create {PROJECT_NUMBER} --owner @me --title "{title}"'
    output, code = run_gh(cmd)

    if code != 0 or not output:
        print(f"  Failed to create item: {title}")
        return

    try:
        item = json.loads(output)
        item_id = item.get("id")
        if item_id:
            update_item_status(item_id, status)
            print(f"  ✅ Created: {title} ({item_type}) [{status}]")
    except:
        print(f"  ✅ Created: {title}")


def update_item_status(item_id, status):
    """Update the status field of a project item"""
    status_id = STATUS_OPTIONS.get(status)
    if not status_id:
        return

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

    cmd = f'gh api graphql -f query="{query.replace(chr(10), " ").strip()}"'
    run_gh(cmd)


def track_forks(repo):
    """Track forks of the repo"""
    print(f"\n🍴 Checking forks for {repo}...")

    cmd = f"gh api repos/{REPO_OWNER}/{repo}/forks"
    output, _ = run_gh(cmd)

    if not output:
        print(f"  No forks found or API error")
        return

    try:
        forks = json.loads(output)
    except:
        print(f"  Error parsing forks")
        return

    existing = get_existing_items()
    data = load_tracking_data()

    # Track the top 5 most recent forks
    for fork in forks[:5]:
        owner = fork.get("owner", {}).get("login", "unknown")
        name = fork.get("name", repo)
        created = fork.get("created_at", "")[:10]

        title = f"🍴 Fork: {owner}/{name}"

        # Check if we've already tracked this
        fork_key = f"{owner}/{name}"
        if fork_key in data.get("forks", []):
            continue

        # Add to tracking
        if "forks" not in data:
            data["forks"] = []
        data["forks"].append(fork_key)

        create_project_item(title, "Fork", "In Progress")
        print(f"  New fork: {owner}/{name}")

    save_tracking_data(data)


def track_contributors(repo):
    """Track contributors to the repo"""
    print(f"\n👥 Checking contributors for {repo}...")

    # Get all contributors
    cmd = f"gh api repos/{REPO_OWNER}/{repo}/contributors?per_page=10"
    output, _ = run_gh(cmd)

    if not output:
        print(f"  No contributors found or API error")
        return

    try:
        contributors = json.loads(output)
    except:
        print(f"  Error parsing contributors")
        return

    existing = get_existing_items()
    data = load_tracking_data()

    for contrib in contributors:
        login = contrib.get("login", "unknown")
        contributions = contrib.get("contributions", 0)

        # Skip if it's the owner
        if login == REPO_OWNER:
            continue

        title = f"👥 Contributor: {login} ({contributions} commits)"

        # Check if we've already tracked this
        if login in data.get("contributors", []):
            continue

        # Add to tracking
        if "contributors" not in data:
            data["contributors"] = []
        data["contributors"].append(login)

        create_project_item(title, "Contributor", "In Progress")
        print(f"  New contributor: {login} ({contributions} commits)")

    save_tracking_data(data)


def track_stars(repo):
    """Track stargazers"""
    print(f"\n⭐ Checking stars for {repo}...")

    cmd = f"gh api repos/{REPO_OWNER}/{repo}/stargazers?per_page=10"
    output, _ = run_gh(cmd)

    if not output:
        print(f"  No stars found or API error")
        return

    try:
        stars = json.loads(output)
    except:
        print(f"  Error parsing stars")
        return

    existing = get_existing_items()
    data = load_tracking_data()

    for star in stars:
        login = star.get("login", "unknown")

        title = f"⭐ Starred: {login}"

        # Check if we've already tracked this
        if login in data.get("stars", []):
            continue

        # Add to tracking
        if "stars" not in data:
            data["stars"] = []
        data["stars"].append(login)

        create_project_item(title, "Star", "In Progress")
        print(f"  New star: {login}")

    save_tracking_data(data)


def main():
    print("🔍 MIRA GitHub Activity Tracker")
    print(f"  Tracking repos: {', '.join(REPOS)}")
    print(f"  Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")

    if not GITHUB_TOKEN:
        print("\n⚠️  Warning: GITHUB_TOKEN not set")

    # Track each repo
    for repo in REPOS:
        print(f"\n{'=' * 40}")
        print(f"📦 Repo: {repo}")
        print(f"{'=' * 40}")

        if TRACK_ALL or TRACK_FORKS:
            track_forks(repo)

        if TRACK_ALL or TRACK_CONTRIBUTORS:
            track_contributors(repo)

        if TRACK_ALL or TRACK_STARS:
            track_stars(repo)

    print("\n✅ Activity tracking complete!")


if __name__ == "__main__":
    main()
