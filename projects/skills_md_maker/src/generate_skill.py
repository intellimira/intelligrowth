import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

from analyze_content import SkillAnalysis


PROJECT_ROOT = Path(__file__).parent.parent
DRAFT_DIR = PROJECT_ROOT / "outputs" / "draft"
APPROVED_DIR = PROJECT_ROOT / "outputs" / "approved"


class SkillGenerator:
    def __init__(self):
        self.draft_dir = DRAFT_DIR
        self.approved_dir = APPROVED_DIR
        self.draft_dir.mkdir(parents=True, exist_ok=True)
        self.approved_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, analysis: SkillAnalysis, source_url: str) -> str:
        """Generate SKILL.md from analysis and save to draft"""
        skill_name = analysis.name or "unnamed-skill"

        skill_md = self._render_skill_md(analysis, source_url)

        draft_file = self.draft_dir / f"{skill_name}.md"
        with open(draft_file, "w") as f:
            f.write(skill_md)

        return str(draft_file)

    def _render_skill_md(self, analysis: SkillAnalysis, source_url: str) -> str:
        """Render SKILL.md from analysis"""

        triggers = (
            ", ".join(f"[{t}]" for t in analysis.triggers)
            if analysis.triggers
            else "[trigger]"
        )

        hard_rules = ""
        if analysis.hard_rules:
            hard_rules = "\n## Hard Rules\n"
            for rule in analysis.hard_rules:
                hard_rules += f"1. {rule}\n"

        patterns = ""
        if analysis.patterns:
            patterns = "\n## Patterns\n"
            for pattern in analysis.patterns:
                patterns += f"- {pattern}\n"

        conventions = ""
        if analysis.conventions:
            conventions = "\n## Conventions\n"
            for conv in analysis.conventions:
                conventions += f"- {conv}\n"

        quality_gates = (
            ", ".join(analysis.quality_gates) if analysis.quality_gates else "[gate]"
        )

        return f"""---
name: {analysis.name}
description: {analysis.description}
triggers: [{triggers}]
tools: [{", ".join(analysis.tools)}]
quality_gates: [{quality_gates}]
persona: "{analysis.persona}"
mira_tier: {analysis.mira_tier}
---

## Source
- URL: {source_url}
- Generated: {datetime.now().isoformat()}

{hard_rules}

## Output Contract
- Output to: `skills/{analysis.name}/SKILL.md`
- Log to: `.mira/scores/`

{patterns}
{conventions}

## Workflow
1. [Describe step 1]
2. [Describe step 2]
3. [Describe step 3]

## Quality Gates
{chr(10).join(f"- [ ] {gate}" for gate in analysis.quality_gates) if analysis.quality_gates else "- [ ] Implement quality checks"}
"""

    def approve(self, skill_name: str) -> Optional[str]:
        """Move draft to approved"""
        draft_file = self.draft_dir / f"{skill_name}.md"

        if not draft_file.exists():
            print(f"Draft not found: {draft_file}")
            return None

        approved_file = self.approved_dir / f"{skill_name}.md"

        with open(draft_file, "r") as f:
            content = f.read()

        with open(approved_file, "w") as f:
            f.write(content)

        return str(approved_file)

    def reject(self, skill_name: str) -> bool:
        """Delete draft"""
        draft_file = self.draft_dir / f"{skill_name}.md"

        if draft_file.exists():
            draft_file.unlink()
            return True

        return False

    def list_drafts(self) -> list[str]:
        """List all pending drafts"""
        return [f.stem for f in self.draft_dir.glob("*.md")]

    def list_approved(self) -> list[str]:
        """List all approved skills"""
        return [f.stem for f in self.approved_dir.glob("*.md")]


def generate_from_analysis(analysis: SkillAnalysis, source_url: str) -> str:
    """Convenience function to generate a skill"""
    generator = SkillGenerator()
    return generator.generate(analysis, source_url)


if __name__ == "__main__":
    generator = SkillGenerator()

    print("Drafts:")
    for draft in generator.list_drafts():
        print(f"  - {draft}")

    print("\nApproved:")
    for approved in generator.list_approved():
        print(f"  - {approved}")
