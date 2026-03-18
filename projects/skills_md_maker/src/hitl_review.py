import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional


PROJECT_ROOT = Path(__file__).parent.parent
DRAFT_DIR = PROJECT_ROOT / "outputs" / "draft"
APPROVED_DIR = PROJECT_ROOT / "outputs" / "approved"
SKILLS_ROOT = Path(__file__).parent.parent.parent / "skills"


class HITLReview:
    def __init__(self):
        self.draft_dir = DRAFT_DIR
        self.approved_dir = APPROVED_DIR
        self.skills_dir = SKILLS_ROOT

    def list_pending(self) -> list[dict]:
        """List all drafts pending review"""
        drafts = []

        for draft_file in self.draft_dir.glob("*.md"):
            stat = draft_file.stat()
            drafts.append(
                {
                    "name": draft_file.stem,
                    "file": str(draft_file),
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            )

        return sorted(drafts, key=lambda x: x["modified"], reverse=True)

    def get_draft(self, skill_name: str) -> Optional[str]:
        """Get draft content"""
        draft_file = self.draft_dir / f"{skill_name}.md"

        if not draft_file.exists():
            return None

        with open(draft_file, "r") as f:
            return f.read()

    def approve(self, skill_name: str) -> tuple[bool, str]:
        """
        Approve a draft: move to approved + create in skills/
        Returns (success, message)
        """
        draft_file = self.draft_dir / f"{skill_name}.md"

        if not draft_file.exists():
            return False, f"Draft not found: {skill_name}"

        skill_dir = self.skills_dir / skill_name

        if skill_dir.exists():
            return False, f"Skill already exists: {skill_name}. Delete or rename first."

        skill_dir.mkdir(parents=True, exist_ok=True)

        approved_file = skill_dir / "SKILL.md"

        with open(draft_file, "r") as f:
            content = f.read()

        with open(approved_file, "w") as f:
            f.write(content)

        return True, f"Approved: skills/{skill_name}/SKILL.md"

    def edit(self, skill_name: str) -> Optional[str]:
        """Return path to draft for editing"""
        draft_file = self.draft_dir / f"{skill_name}.md"

        if not draft_file.exists():
            return None

        return str(draft_file)

    def reject(self, skill_name: str) -> bool:
        """Reject and delete draft"""
        draft_file = self.draft_dir / f"{skill_name}.md"

        if draft_file.exists():
            draft_file.unlink()
            return True

        return False

    def regenerate(self, skill_name: str) -> bool:
        """Flag for regeneration (delete draft, user re-runs /skillm)"""
        return self.reject(skill_name)


def print_review_status():
    """Print current review status"""
    review = HITLReview()
    pending = review.list_pending()

    print("=" * 60)
    print("SKILL REVIEW QUEUE")
    print("=" * 60)

    if not pending:
        print("\nNo pending drafts.")
        print("\nTo create a new skill:")
        print("  /skillm <URL>")
        print("\nTo recommend skills:")
        print("  /skillm recommend 'task description'")
        return

    print(f"\n{len(pending)} pending draft(s):\n")

    for draft in pending:
        print(f"  📝 {draft['name']}")
        print(f"     Created: {draft['created'][:19]}")
        print(f"     Path: {draft['file']}")
        print()

    print("Actions:")
    print("  /skillm approve <name>   - Approve and add to skills/")
    print("  /skillm reject <name>   - Delete draft")
    print("  /skillm edit <name>     - Open draft for editing")


if __name__ == "__main__":
    print_review_status()
