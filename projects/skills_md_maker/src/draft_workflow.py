#!/usr/bin/env python3
"""
Draft Workflow Automation Script

Handles the skill draft lifecycle:
- approve: Move draft to approved, update registry, optionally move to /skills/
- reject: Move draft to rejected
- edit: Open draft for editing
- status: Show all draft statuses
- list: List all drafts

Usage:
    python draft_workflow.py approve <skill-name>
    python draft_workflow.py reject <skill-name>
    python draft_workflow.py edit <skill-name>
    python draft_workflow.py status
    python draft_workflow.py list
"""

import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DRAFT_DIR = OUTPUTS_DIR / "draft"
PENDING_DIR = OUTPUTS_DIR / "pending"
APPROVED_DIR = OUTPUTS_DIR / "approved"
REJECTED_DIR = OUTPUTS_DIR / "rejected"
SKILLS_DIR = PROJECT_ROOT.parent.parent / "skills"
REGISTRY_PATH = Path("/home/sir-v/MiRA/docs/skills_registry.md")
VECTORDB_DIR = PROJECT_ROOT / "vectordb"


def find_draft(name: str) -> Optional[Path]:
    """Find a draft by name (with or without DRAFT_ prefix)."""
    # Try with prefix
    draft_path = DRAFT_DIR / f"DRAFT_{name}.md"
    if draft_path.exists():
        return draft_path

    # Try without prefix (legacy)
    draft_path = DRAFT_DIR / f"{name}.md"
    if draft_path.exists():
        return draft_path

    # Try case-insensitive
    for f in DRAFT_DIR.glob("*.md"):
        if name.lower() in f.stem.lower():
            return f

    return None


def extract_frontmatter(content: str) -> dict:
    """Extract frontmatter from markdown file."""
    lines = content.split("\n")
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}

    fm = {}
    in_fm = False
    for line in lines[1:]:
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                break
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip().strip('"')

    return fm


def update_registry_status(name: str, status: str, approved_date: Optional[str] = None):
    """Update the skills registry with new status."""
    if not REGISTRY_PATH.exists():
        print(f"Warning: Registry not found at {REGISTRY_PATH}")
        return

    content = REGISTRY_PATH.read_text()

    # Find and update the skill section
    skill_marker = f"### {name}"
    if skill_marker in content:
        # Find the section
        lines = content.split("\n")
        new_lines = []
        in_skill_section = False
        found_status = False

        for i, line in enumerate(lines):
            if skill_marker in line:
                in_skill_section = True

            if in_skill_section:
                if "**Status**:" in line:
                    new_lines.append(f"**Status**: {status}")
                    if approved_date:
                        new_lines.append(f"**Approved Date**: {approved_date}")
                    found_status = True
                elif found_status and "---" in line:
                    new_lines.append(line)
                    in_skill_section = False
                elif not found_status:
                    new_lines.append(line)
                    if "---" in line:
                        # Add status before the --- if not found
                        new_lines.insert(-1, f"**Status**: {status}")
                        if approved_date:
                            new_lines.insert(-1, f"**Approved Date**: {approved_date}")
                        found_status = True
                        in_skill_section = False
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        REGISTRY_PATH.write_text("\n".join(new_lines))
        print(f"  → Updated registry status: {status}")
    else:
        print(f"  → Skill not found in registry: {name}")


def cmd_approve(name: str, move_to_skills: bool = False):
    """Approve a draft skill."""
    print(f"\n[APPROVE] {name}")

    draft_path = find_draft(name)
    if not draft_path:
        print(f"Error: Draft not found: {name}")
        return False

    # Read draft content
    content = draft_path.read_text()
    fm = extract_frontmatter(content)

    # Get skill name from frontmatter or filename
    skill_name = fm.get("name", name)

    # Move to approved folder
    approved_path = APPROVED_DIR / draft_path.name
    shutil.move(str(draft_path), str(approved_path))
    print(f"  → Moved to: {approved_path}")

    # Optionally move to /skills/
    if move_to_skills:
        skills_path = SKILLS_DIR / skill_name
        if skills_path.exists():
            # Backup existing
            backup_path = (
                SKILLS_DIR
                / f"{skill_name}.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
            )
            shutil.move(str(skills_path), str(backup_path))
            print(f"  → Backed up existing: {backup_path}")

        skills_path.mkdir(exist_ok=True)
        skill_md = skills_path / "SKILL.md"
        skill_md.write_text(content)
        print(f"  → Moved to: {skill_md}")

    # Update registry
    approved_date = datetime.now().strftime("%Y-%m-%d")
    update_registry_status(skill_name, "APPROVED", approved_date)

    # Note: Re-indexing would be done here if needed
    print(f"  → Approved: {skill_name}")

    return True


def cmd_reject(name: str):
    """Reject a draft skill."""
    print(f"\n[REJECT] {name}")

    draft_path = find_draft(name)
    if not draft_path:
        print(f"Error: Draft not found: {name}")
        return False

    # Move to rejected folder
    rejected_path = REJECTED_DIR / draft_path.name
    shutil.move(str(draft_path), str(rejected_path))
    print(f"  → Moved to: {rejected_path}")

    # Update registry
    fm = extract_frontmatter(draft_path.read_text())
    skill_name = fm.get("name", name)
    update_registry_status(skill_name, "REJECTED")

    print(f"  → Rejected: {name}")
    return True


def cmd_edit(name: str):
    """Open draft for editing."""
    print(f"\n[EDIT] {name}")

    draft_path = find_draft(name)
    if not draft_path:
        print(f"Error: Draft not found: {name}")
        return False

    print(f"  → Draft: {draft_path}")
    print(f"  → Edit manually, then run approve or reject")
    return True


def cmd_status():
    """Show status of all drafts."""
    print("\n[DRAFT STATUS]")

    drafts = list(DRAFT_DIR.glob("DRAFT_*.md"))
    pending = list(PENDING_DIR.glob("DRAFT_*.md"))
    approved = list(APPROVED_DIR.glob("DRAFT_*.md"))
    rejected = list(REJECTED_DIR.glob("DRAFT_*.md"))

    print(f"\n  Drafts (pending review): {len(drafts)}")
    for d in sorted(drafts):
        name = d.stem.replace("DRAFT_", "")
        print(f"    - {name}")

    if pending:
        print(f"\n  In Review: {len(pending)}")
        for p in sorted(pending):
            name = p.stem.replace("DRAFT_", "")
            print(f"    - {name}")

    if approved:
        print(f"\n  Approved: {len(approved)}")
        for a in sorted(approved):
            name = a.stem.replace("DRAFT_", "")
            print(f"    - {name}")

    if rejected:
        print(f"\n  Rejected: {len(rejected)}")
        for r in sorted(rejected):
            name = r.stem.replace("DRAFT_", "")
            print(f"    - {name}")

    print(f"\n  Total: {len(drafts) + len(pending) + len(approved) + len(rejected)}")


def cmd_regenerate():
    """Regenerate the skills registry."""
    print("\n[REGENERATE REGISTRY]")

    import json

    # Load indexed skills
    vectordb_path = PROJECT_ROOT / "vectordb" / "skills_meta.json"
    with open(vectordb_path) as f:
        data = json.load(f)

    # Get approved skills
    approved_skills = {
        p.name
        for p in SKILLS_DIR.glob("*/")
        if p.is_dir() and not p.name.startswith(".")
    }

    # Get drafts
    drafts = list(DRAFT_DIR.glob("DRAFT_*.md"))
    draft_names = {p.stem.replace("DRAFT_", "") for p in drafts}

    registry = f"""# MIRA Skills Registry

> Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
> Total Skills: {data["skills_count"]} approved, {len(drafts)} pending review

---

## Approved Skills (Council & Cabal Grounded)

"""

    for skill in data["skills"]:
        name = skill.get("name", "unknown")
        desc = skill.get("description", "No description")
        triggers = skill.get("triggers", [])
        tools = skill.get("tools", [])
        persona = skill.get("persona", "")

        status = "APPROVED"
        if name in draft_names:
            status = "APPROVED (DRAFT UPDATE PENDING)"

        registry += f"### {name}\n\n"
        registry += f"**Status**: {status}\n\n"
        registry += f"**Description**: {desc}\n\n"
        if triggers:
            registry += f"**Triggers**: {', '.join(triggers[:5])}\n\n"
        if tools:
            registry += f"**Tools**: {', '.join(tools[:5])}\n\n"
        if persona:
            registry += f"**Persona**: {persona}\n\n"
        registry += "---\n\n"

    registry += """
---

## Pending Review (Drafts - Not Yet Approved)

"""

    for draft in sorted(drafts):
        name = draft.stem.replace("DRAFT_", "")
        content = draft.read_text()

        in_frontmatter = False
        description = ""
        triggers = []
        tools = []
        persona = ""

        for line in content.split("\n"):
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    in_frontmatter = False
                continue
            if in_frontmatter:
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()
                elif line.startswith("triggers:"):
                    triggers_str = line.split(":", 1)[1].strip().strip("[]")
                    triggers = [
                        t.strip().strip('"')
                        for t in triggers_str.split(",")
                        if t.strip()
                    ]
                elif line.startswith("tools:"):
                    tools_str = line.split(":", 1)[1].strip().strip("[]")
                    tools = [
                        t.strip().strip('"') for t in tools_str.split(",") if t.strip()
                    ]
                elif line.startswith("persona:"):
                    persona = line.split(":", 1)[1].strip().strip('"')

        registry += f"### {name}\n\n"
        registry += f"**Status**: DRAFT - PENDING REVIEW\n\n"
        if description:
            registry += f"**Description**: {description}\n\n"
        if triggers:
            registry += f"**Triggers**: {', '.join(triggers[:5])}\n\n"
        if tools:
            registry += f"**Tools**: {', '.join(tools[:5])}\n\n"
        if persona:
            registry += f"**Persona**: {persona}\n\n"
        registry += "---\n\n"

    REGISTRY_PATH.write_text(registry)
    print(f"  → Registry updated: {REGISTRY_PATH}")
    print(f"  → Approved: {data['skills_count']}")
    print(f"  → Drafts: {len(drafts)}")


def cmd_list():
    """List all drafts."""
    print("\n[DRAFTS]")

    drafts = sorted(DRAFT_DIR.glob("DRAFT_*.md"))
    if not drafts:
        print("  No drafts found")
        return

    for d in drafts:
        name = d.stem.replace("DRAFT_", "")
        content = d.read_text()
        fm = extract_frontmatter(content)

        desc = fm.get("description", "No description")
        if len(desc) > 50:
            desc = desc[:50] + "..."

        persona = fm.get("persona", "")

        print(f"\n  {name}")
        print(f"    {desc}")
        if persona:
            print(f"    Persona: {persona}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "approve":
        if len(sys.argv) < 3:
            print(
                "Usage: python draft_workflow.py approve <skill-name> [--move-to-skills]"
            )
            sys.exit(1)

        name = sys.argv[2]
        move_to_skills = "--move-to-skills" in sys.argv
        cmd_approve(name, move_to_skills)

    elif command == "reject":
        if len(sys.argv) < 3:
            print("Usage: python draft_workflow.py reject <skill-name>")
            sys.exit(1)

        name = sys.argv[2]
        cmd_reject(name)

    elif command == "edit":
        if len(sys.argv) < 3:
            print("Usage: python draft_workflow.py edit <skill-name>")
            sys.exit(1)

        name = sys.argv[2]
        cmd_edit(name)

    elif command == "status":
        cmd_status()

    elif command == "regenerate":
        cmd_regenerate()

    elif command == "list":
        cmd_list()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
