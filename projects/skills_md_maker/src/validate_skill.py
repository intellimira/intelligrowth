#!/usr/bin/env python3
"""
validate_skill.py - Quality scoring for SKILL.md files

Scoring formula (0-100):
- yaml_validity * 20      # YAML parses correctly (0 or 20)
- trigger_recall * 25     # Triggers match use case (0-25)
- tool_coverage * 25     # Tools match requirements (0-25)
- persona_fit * 15      # Persona matches skill type (0-15)
- workflow_clarity * 15  # Workflow is actionable (0-15)

Target: 85+ for "production ready"
"""

import re
import sys
from pathlib import Path
from typing import Optional

import yaml


class SkillValidator:
    """Validates SKILL.md files and calculates quality score"""

    PERSONAS = {
        "⚛️ First Principles": ["pain-sentry", "first-principles"],
        "🔬 Scientific Method": ["pain-scorer", "ai-agent-foundations", "scientific"],
        "🤔 Philosophical Inquiry": ["philosophical"],
        "✨ Creative Synthesis": ["arch-synthesiser", "creative", "synthesis"],
        "⚙️ Pragmatic Application": [
            "opencode-builder",
            "revenue-tracker",
            "local-ai-stack",
            "srank-pack-generator",
            "pragmatic",
        ],
        "🌑 Dark Passenger": ["hostile-grounding", "self-anneal-watchdog", "dark"],
    }

    def __init__(self):
        self.score = 0
        self.breakdown = {}

    def parse_skill_md(self, content: str) -> Optional[dict]:
        """Extract YAML frontmatter from SKILL.md"""
        try:
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    return yaml.safe_load(frontmatter)
            return None
        except yaml.YAMLError as e:
            print(f"YAML parse error: {e}")
            return None

    def score_yaml_validity(self, skill: dict) -> float:
        """Score: YAML parses correctly (0 or 20)"""
        required_fields = ["name", "description", "triggers", "tools", "persona"]
        missing = [f for f in required_fields if not skill.get(f)]

        if missing:
            self.breakdown["yaml_validity"] = 0
            return 0

        self.breakdown["yaml_validity"] = 20
        return 20

    def score_trigger_recall(self, skill: dict) -> float:
        """Score: Triggers match use case (0-25)"""
        triggers = skill.get("triggers", [])

        if not triggers or triggers == [[]] or triggers == []:
            self.breakdown["trigger_recall"] = 0
            return 0

        # Count valid triggers
        if isinstance(triggers, list):
            # Flatten if nested
            flat = []
            for t in triggers:
                if isinstance(t, list):
                    flat.extend(t)
                else:
                    flat.append(t)
            trigger_count = len([t for t in flat if t])
        else:
            trigger_count = 0

        # Score: 1-3 triggers = 10, 4-6 = 17, 7+ = 25
        if trigger_count >= 7:
            score = 25
        elif trigger_count >= 4:
            score = 17
        elif trigger_count >= 1:
            score = 10
        else:
            score = 0

        self.breakdown["trigger_recall"] = score
        return score

    def score_tool_coverage(self, skill: dict) -> float:
        """Score: Tools match requirements (0-25)"""
        tools = skill.get("tools", [])

        if not tools or tools == [[]] or tools == []:
            self.breakdown["tool_coverage"] = 0
            return 0

        # Count valid tools
        if isinstance(tools, list):
            flat = []
            for t in tools:
                if isinstance(t, list):
                    flat.extend(t)
                else:
                    flat.append(t)
            tool_count = len([t for t in flat if t])
        else:
            tool_count = 0

        # Score: 1-2 tools = 10, 3-5 = 17, 6+ = 25
        if tool_count >= 6:
            score = 25
        elif tool_count >= 3:
            score = 17
        elif tool_count >= 1:
            score = 10
        else:
            score = 0

        self.breakdown["tool_coverage"] = score
        return score

    def score_persona_fit(self, skill: dict) -> float:
        """Score: Persona matches skill type (0-15)"""
        persona = skill.get("persona", "")
        name = skill.get("name", "")

        if not persona or persona == "⚙️ Pragmatic Application":
            # Check if persona matches skill name patterns
            name_lower = name.lower()

            for persona_key, keywords in self.PERSONAS.items():
                if any(kw in name_lower for kw in keywords):
                    self.breakdown["persona_fit"] = 15
                    return 15

            # Generic "Pragmatic Application" gets partial
            self.breakdown["persona_fit"] = 5
            return 5

        # Check if persona contains valid emoji + description
        valid_personas = ["⚛️", "🔬", "🤔", "✨", "⚙️", "🌑"]
        has_emoji = any(p in persona for p in valid_personas)
        has_description = "—" in persona or len(persona) > 10

        if has_emoji and has_description:
            self.breakdown["persona_fit"] = 15
            return 10  # Partial - could be better

        self.breakdown["persona_fit"] = 5
        return 5

    def score_workflow_clarity(self, content: str, skill: dict) -> float:
        """Score: Workflow is actionable (0-15)"""
        # Check for workflow section
        workflow_pattern = r"##\s+Workflow"
        has_workflow_header = bool(re.search(workflow_pattern, content, re.IGNORECASE))

        # Check for hard rules
        hard_rules_pattern = r"##\s+Hard\s+Rules"
        has_hard_rules = bool(re.search(hard_rules_pattern, content, re.IGNORECASE))

        # Check for quality gates
        quality_gates = skill.get("quality_gates", [])
        has_quality_gates = (
            quality_gates and quality_gates != [] and quality_gates != [[]]
        )

        score = 0
        if has_workflow_header:
            score += 5
        if has_hard_rules:
            score += 5
        if has_quality_gates:
            score += 5

        self.breakdown["workflow_clarity"] = score
        return score

    def validate_file(self, filepath: str) -> dict:
        """Validate a single SKILL.md file and return score breakdown"""
        path = Path(filepath)

        if not path.exists():
            return {"error": f"File not found: {filepath}", "score": 0}

        content = path.read_text()
        skill = self.parse_skill_md(content)

        if not skill:
            return {
                "file": filepath,
                "error": "Failed to parse YAML frontmatter",
                "score": 0,
                "breakdown": {},
            }

        # Calculate scores
        yaml_score = self.score_yaml_validity(skill)
        trigger_score = self.score_trigger_recall(skill)
        tool_score = self.score_tool_coverage(skill)
        persona_score = self.score_persona_fit(skill)
        workflow_score = self.score_workflow_clarity(content, skill)

        total = yaml_score + trigger_score + tool_score + persona_score + workflow_score

        return {
            "file": filepath,
            "name": skill.get("name", "unknown"),
            "score": total,
            "breakdown": self.breakdown,
            "yaml_validity": yaml_score,
            "trigger_recall": trigger_score,
            "tool_coverage": tool_score,
            "persona_fit": persona_score,
            "workflow_clarity": workflow_score,
        }

    def validate_directory(self, dirpath: str) -> list:
        """Validate all SKILL.md files in a directory"""
        path = Path(dirpath)
        results = []

        for md_file in path.rglob("*.md"):
            # Skip non-draft files in root
            if md_file.name == "SKILL.md" and md_file.parent.name == "skills_md_maker":
                continue
            result = self.validate_file(str(md_file))
            results.append(result)

        return sorted(results, key=lambda x: x.get("score", 0), reverse=True)


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Validate SKILL.md quality")
    parser.add_argument("path", help="File or directory to validate")
    parser.add_argument(
        "--detailed", "-d", action="store_true", help="Show detailed breakdown"
    )
    parser.add_argument(
        "--format", choices=["table", "json"], default="table", help="Output format"
    )

    args = parser.parse_args()

    validator = SkillValidator()
    path = Path(args.path)

    if path.is_file():
        results = [validator.validate_file(str(path))]
    else:
        results = validator.validate_directory(str(path))

    if args.format == "json":
        import json

        print(json.dumps(results, indent=2))
        return

    # Table output
    print(
        f"{'Name':<30} {'Score':>6} {'YAML':>4} {'Trig':>4} {'Tool':>4} {'Pers':>4} {'Flow':>4}"
    )
    print("-" * 70)

    for r in results:
        if "error" in r and r.get("score") == 0:
            print(f"{'ERROR':<30} {0:>6} {r.get('error', '')}")
            continue

        b = r.get("breakdown", {})
        print(
            f"{r.get('name', 'unknown'):<30} {r.get('score', 0):>6} "
            f"{b.get('yaml_validity', 0):>4} {b.get('trigger_recall', 0):>4} "
            f"{b.get('tool_coverage', 0):>4} {b.get('persona_fit', 0):>4} "
            f"{b.get('workflow_clarity', 0):>4}"
        )

    # Summary
    scores = [r.get("score", 0) for r in results if "error" not in r]
    if scores:
        print("-" * 70)
        print(
            f"Total: {len(scores)} skills | Avg: {sum(scores) / len(scores):.1f} | "
            f"Passing (85+): {len([s for s in scores if s >= 85])}"
        )

    if args.detailed:
        print("\n=== DETAILED BREAKDOWN ===")
        for r in results:
            if "error" in r:
                continue
            print(f"\n{r.get('name')}:")
            for key, val in r.get("breakdown", {}).items():
                print(f"  {key}: {val}")


if __name__ == "__main__":
    main()
