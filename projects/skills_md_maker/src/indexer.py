#!/usr/bin/env python3
"""
Auto-indexer for newly approved skills.
This can be run manually or set up as a watcher.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from index_skills import SkillIndexer


PROJECT_ROOT = Path(__file__).parent.parent
SKILLS_ROOT = Path("/home/sir-v/MiRA/skills")
APPROVED_DIR = PROJECT_ROOT / "outputs" / "approved"


def index_new_skills():
    """Index any new skills that haven't been indexed yet"""
    indexer = SkillIndexer()

    existing_names = set(indexer.list_skills())

    new_count = 0

    for skill_dir in SKILLS_ROOT.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        if skill_dir.name in existing_names:
            continue

        print(f"Indexing new skill: {skill_dir.name}")

        if indexer.index_skill(skill_file):
            new_count += 1
            print(f"  ✓ Indexed: {skill_dir.name}")

    if new_count == 0:
        print("No new skills to index.")
    else:
        print(f"\nIndexed {new_count} new skill(s).")

    return new_count


def index_from_approved():
    """Index skills from approved outputs"""
    indexer = SkillIndexer()

    if not APPROVED_DIR.exists():
        print(f"Approved directory not found: {APPROVED_DIR}")
        return 0

    count = 0

    for approved_file in APPROVED_DIR.glob("*.md"):
        skill_name = approved_file.stem

        if skill_name in indexer.list_skills():
            print(f"Already indexed: {skill_name}")
            continue

        print(f"Indexing from approved: {skill_name}")

        if indexer.index_skill(approved_file):
            count += 1
            print(f"  ✓ Indexed: {skill_name}")

    return count


def reindex_all():
    """Clear and reindex all skills"""
    import shutil

    vectordb_dir = PROJECT_ROOT / "vectordb"

    if vectordb_dir.exists():
        shutil.rmtree(vectordb_dir)

    vectordb_dir.mkdir(parents=True, exist_ok=True)

    indexer = SkillIndexer()
    count = indexer.index_all()

    print(f"Reindexed {count} skills.")
    return count


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Skill indexer")
    parser.add_argument("--new", action="store_true", help="Index new skills only")
    parser.add_argument(
        "--approved", action="store_true", help="Index from approved folder"
    )
    parser.add_argument("--reindex", action="store_true", help="Clear and reindex all")

    args = parser.parse_args()

    count = 0

    if args.reindex:
        count = reindex_all()
    elif args.approved:
        count = index_from_approved()
        print(f"\nIndexed {count} from approved.")
    elif args.new:
        count = index_new_skills()
    else:
        count = index_new_skills()

    return count


if __name__ == "__main__":
    main()
