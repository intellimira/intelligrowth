#!/usr/bin/env python3
"""
Awesome OpenCode Curator - Core Search Script

Usage:
    python3 core.py <keyword> [category]
    python3 core.py list [category]
    python3 core.py update
"""

import os
import sys
import subprocess
import json
import yaml
from pathlib import Path

DATA_PATH = Path("/home/sir-v/MiRA/projects/awesome-opencode")
CATEGORIES = ["official", "plugins", "themes", "agents", "projects", "resources"]


def search(keyword: str, category: str | None = None):
    """Search for keyword in awesome-opencode data."""
    results = []

    search_dirs = [DATA_PATH / "data" / category] if category else [DATA_PATH / "data"]

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        for yaml_file in search_dir.rglob("*.yaml"):
            try:
                with open(yaml_file) as f:
                    content = yaml.safe_load(f)
                    content_str = json.dumps(content).lower()
                    if keyword.lower() in content_str:
                        rel_path = yaml_file.relative_to(DATA_PATH)
                        results.append(
                            {
                                "file": str(rel_path),
                                "id": yaml_file.stem,
                                "data": content,
                            }
                        )
            except Exception:
                continue

    return results


def list_category(category: str | None = None):
    """List available items in category."""
    if category:
        cat_path = DATA_PATH / "data" / category
        if not cat_path.exists():
            return {"error": f"Category '{category}' not found"}

        items = []
        for item in cat_path.iterdir():
            if item.is_file() and item.suffix == ".yaml":
                items.append(item.stem)
            elif item.is_dir():
                items.append(item.name)
        return {"category": category, "items": items}
    else:
        return {"categories": CATEGORIES}


def update():
    """Pull latest from git."""
    try:
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            cwd=DATA_PATH,
            capture_output=True,
            text=True,
        )
        return {"success": result.returncode == 0, "output": result.stdout}
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        result = list_category(category)
    elif command == "update":
        result = update()
    else:
        keyword = command
        category = sys.argv[2] if len(sys.argv) > 2 else None
        result = search(keyword, category)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
