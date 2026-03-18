#!/usr/bin/env python3
"""
Awesome OpenCode VectorDB Index Builder

Builds a semantic index of awesome-opencode plugins for MIRA's knowledge mesh.
"""

import json
import yaml
from pathlib import Path

DATA_PATH = Path("/home/sir-v/MiRA/projects/awesome-opencode")
OUTPUT_PATH = Path("/home/sir-v/MiRA/skills/awesome-opencode-curator/vectordb")


def load_yaml_file(path: Path) -> dict | None:
    """Load a YAML file."""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def extract_all_plugins():
    """Extract plugin metadata from YAML files."""
    plugins = []
    plugins_dir = DATA_PATH / "data" / "plugins"

    if not plugins_dir.exists():
        return []

    for yaml_file in plugins_dir.glob("*.yaml"):
        plugin = load_yaml_file(yaml_file)
        if plugin:
            plugin["id"] = yaml_file.stem
            plugins.append(plugin)

    return plugins


def extract_by_category():
    """Extract all categories."""
    categories = {}
    data_dir = DATA_PATH / "data"

    for cat_dir in data_dir.iterdir():
        if cat_dir.is_dir():
            items = []
            for item in cat_dir.glob("*.yaml"):
                data = load_yaml_file(item)
                if data:
                    data["id"] = item.stem
                    items.append(data)
            categories[cat_dir.name] = items

    return categories


def build_index():
    """Build the metadata index."""
    plugins = extract_all_plugins()
    categories = extract_by_category()

    index = {
        "version": "1.0.0",
        "source": "awesome-opencode",
        "source_path": str(DATA_PATH),
        "plugin_count": len(plugins),
        "categories": {cat: len(items) for cat, items in categories.items()},
        "plugins": plugins,
        "category_data": categories,
    }

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH / "index.json", "w") as f:
        json.dump(index, f, indent=2)

    print(
        f"Index built: {len(plugins)} plugins indexed across {len(categories)} categories"
    )
    return index


if __name__ == "__main__":
    build_index()
