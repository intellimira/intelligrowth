#!/usr/bin/env python3
"""
autoresearch_loop.py - Autonomous optimization loop for SKILL.md files

Based on the Auto Research methodology from instruct_opencode.md:
- Goal: Improve quality_score to target (default 85+)
- Variable: SKILL.md content (triggers, tools, persona, hard_rules, workflow)
- Measurement: validate_skill.py scoring function

The Loop:
1. REVIEW: Read current skill + research log
2. MUTATE: Apply one focused change
3. VERIFY: Run validation scoring
4. SELECT: Keep if improved, discard if worse
5. LOG: Record result to research history
6. REPEAT: Until target score or max iterations

Usage:
    python autoresearch_loop.py outputs/draft/DRAFT_opencode-builder.md
    python autoresearch_loop.py outputs/draft/DRAFT_opencode-builder.md --target 90
    python autoresearch_loop.py outputs/draft/DRAFT_opencode-builder.md --max-iterations 20
"""

import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml


class AutoResearchLoop:
    """Autonomous optimization loop for SKILL.md quality"""

    MUTATION_STRATEGIES = [
        "trigger_tune",  # Refine trigger phrases
        "tool_expand",  # Add missing tools
        "persona_align",  # Adjust persona to skill type
        "hard_rules_add",  # Add specific constraints
        "workflow_refine",  # Clarify process steps
    ]

    def __init__(
        self,
        skill_path: str,
        target_score: int = 85,
        max_iterations: int = 20,
        research_dir: Optional[str] = None,
    ):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.stem.replace("DRAFT_", "")
        self.target_score = target_score
        self.max_iterations = max_iterations

        # Research directory
        if research_dir:
            self.research_dir = Path(research_dir)
        else:
            self.research_dir = self.skill_path.parent.parent / "research"

        self.research_dir.mkdir(parents=True, exist_ok=True)

        # Initialize research log
        self.log_file = self.research_dir / f"{self.skill_name}_research.tsv"
        self._init_log()

        # State
        self.current_score = 0
        self.best_score = 0
        self.best_content = ""
        self.iteration = 0

        # Load initial skill
        self.load_skill()

    def _init_log(self):
        """Initialize research log TSV"""
        if not self.log_file.exists():
            with open(self.log_file, "w") as f:
                f.write("iteration\tcommit\tscore\tdelta\tstatus\tdescription\n")

    def load_skill(self):
        """Load current skill content and score"""
        if not self.skill_path.exists():
            print(f"Error: Skill file not found: {self.skill_path}")
            sys.exit(1)

        self.current_content = self.skill_path.read_text()
        self.current_score = self._calculate_score()
        self.best_score = self.current_score
        self.best_content = self.current_content

        print(f"Loaded: {self.skill_name}")
        print(f"Current score: {self.current_score}/{self.target_score}")
        print("-" * 50)

    def _calculate_score(self, skill_path=None) -> int:
        """Calculate quality score using validate_skill.py"""
        target_path = skill_path if skill_path else self.skill_path

        result = subprocess.run(
            [
                "python3",
                "-c",
                f'''
import sys
sys.path.insert(0, "src")
from validate_skill import SkillValidator
v = SkillValidator()
r = v.validate_file("{target_path}")
print(r.get("score", 0))
''',
            ],
            cwd=self.skill_path.parent.parent.parent,
            capture_output=True,
            text=True,
        )

        try:
            return int(result.stdout.strip())
        except:
            return 0

    def _parse_frontmatter(self, content: str) -> dict:
        """Extract and parse YAML frontmatter"""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1])
        return {}

    def _update_frontmatter(self, content: str, updates: dict) -> str:
        """Update YAML frontmatter in content"""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                data = yaml.safe_load(frontmatter) or {}
                data.update(updates)
                new_frontmatter = yaml.dump(data, default_flow_style=False)
                return f"---\n{new_frontmatter}---\n{parts[2]}"
        return content

    def _flatten_list(self, lst) -> list:
        """Flatten a nested list, removing empty items"""
        if not isinstance(lst, list):
            return []
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(self._flatten_list(item))
            elif item:
                result.append(item)
        return result

    def _mutate(self, strategy: str) -> tuple[str, str]:
        """
        Apply mutation strategy to skill.

        Returns: (mutated_content, description)
        """
        content = self.current_content
        data = self._parse_frontmatter(content)
        description = ""

        if strategy == "trigger_tune":
            current_triggers = data.get("triggers", [])
            name = data.get("name", "")

            flat = self._flatten_list(current_triggers)

            name_lower = name.lower()
            new_triggers = []

            if "opencode" in name_lower or "builder" in name_lower:
                new_triggers = [
                    "build",
                    "code",
                    "implement",
                    "manifest",
                    "generate",
                    "opencode",
                ]
            elif "pain" in name_lower or "sentry" in name_lower:
                new_triggers = ["discover", "mine", "scan", "find pain", "monitor"]
            elif "code" in name_lower:
                new_triggers = ["build", "code", "implement", "manifest", "generate"]
            elif "shadow" in name_lower or "monet" in name_lower:
                new_triggers = ["monetize", "revenue", "profit", "outreach", "creator"]
            elif "saas" in name_lower:
                new_triggers = ["saas", "software", "subscription", "pricing", "mrr"]
            elif (
                "notebook" in name_lower
                or "bridge" in name_lower
                or "notebooklm" in name_lower
            ):
                new_triggers = ["notebook", "nbla", "audio", "summarize", "ingest"]
            elif "github" in name_lower:
                new_triggers = ["github", "repo", "code", "fetch", "analyze"]

            all_triggers = list(set(flat + new_triggers))

            if not flat or all_triggers != flat:
                content = self._update_frontmatter(content, {"triggers": all_triggers})
                description = f"expand triggers: {len(flat)} → {len(all_triggers)}"

        elif strategy == "tool_expand":
            current_tools = data.get("tools", [])
            name = data.get("name", "")
            name_lower = name.lower()

            flat = self._flatten_list(current_tools)

            new_tools = []

            if "opencode" in name_lower or "builder" in name_lower:
                new_tools = ["read", "write", "edit", "glob", "grep", "bash"]
            elif (
                "notebook" in name_lower
                or "bridge" in name_lower
                or "notebooklm" in name_lower
            ):
                new_tools = ["webfetch", "codesearch", "read", "write", "glob", "grep"]
            elif "saas" in name_lower:
                new_tools = [
                    "sqlite_read",
                    "sqlite_write",
                    "gemini_call",
                    "ollama_infer",
                ]
            elif "pain" in name_lower:
                new_tools = ["run_scrapy", "praw_fetch", "imap_read", "sqlite_write"]
            elif "code" in name_lower or "github" in name_lower:
                new_tools = ["read", "write", "edit", "bash", "codesearch", "webfetch"]

            all_tools = list(set(flat + new_tools))

            if not flat or all_tools != flat:
                content = self._update_frontmatter(content, {"tools": all_tools})
                description = f"expand tools: {len(flat)} → {len(all_tools)}"

        elif strategy == "persona_align":
            name = data.get("name", "")
            current_persona = data.get("persona", "")
            name_lower = name.lower()

            target_persona = "⚙️ Pragmatic Application — working code, minimum viable"

            if "pain" in name_lower and "scorer" in name_lower:
                target_persona = (
                    "🔬 Scientific Method — pattern extraction and systematic analysis"
                )
            elif "pain" in name_lower and "sentry" in name_lower:
                target_persona = (
                    "⚛️ First Principles — strips assumptions from raw signal"
                )
            elif "arch" in name_lower or "synth" in name_lower:
                target_persona = (
                    "✨ Creative Synthesis — novel zero-capital tool combinations"
                )
            elif "hostile" in name_lower or "grounding" in name_lower:
                target_persona = (
                    "🌑 Dark Passenger — assumption challenger, chaos identifier"
                )
            elif "watchdog" in name_lower or "anneal" in name_lower:
                target_persona = "🌑 Dark Passenger — finds failure before it finds you"

            if current_persona != target_persona:
                content = self._update_frontmatter(content, {"persona": target_persona})
                description = f"align persona: {current_persona[:20]}... → {target_persona[:20]}..."

        elif strategy == "hard_rules_add":
            if "## Hard Rules" not in content or "[Add hard rules]" in content:
                lines = content.split("\n")
                new_lines = []
                added = False

                for line in lines:
                    if line == "## Hard Rules":
                        new_lines.append(line)
                        new_lines.append("")
                        new_lines.append(
                            "1. Never overwrite existing files without confirmation"
                        )
                        new_lines.append("2. Always validate input before processing")
                        new_lines.append(
                            "3. Maintain backward compatibility with existing skills"
                        )
                        added = True
                    elif "[Add hard rules]" in line:
                        continue  # Skip placeholder
                    else:
                        new_lines.append(line)

                if added:
                    content = "\n".join(new_lines)
                    description = "add hard rules section"

        elif strategy == "workflow_refine":
            if "## Workflow" not in content or "[Define step" in content:
                lines = content.split("\n")
                new_lines = []

                for line in lines:
                    if "[Define step" in line:
                        continue  # Skip placeholders
                    else:
                        new_lines.append(line)

                # Add workflow if not present
                if "## Workflow" not in content:
                    workflow = """

## Workflow

1. Analyze input source and classify type
2. Extract relevant patterns using Persona Council
3. Apply specialization layer for deep analysis
4. Generate skill output with quality gates
5. Return validated SKILL.md
"""
                    new_lines.append(workflow)

                content = "\n".join(new_lines)
                description = "refine workflow steps"

        return content, description

    def _commit(self, description: str) -> str:
        """Git commit the current state"""
        # In a full implementation, this would git commit
        # For now, just return a timestamp-based hash
        return datetime.now().strftime("%Y%m%d%H%M%S")

    def _log_result(
        self, iteration: int, score: int, delta: int, status: str, description: str
    ):
        """Log result to research TSV"""
        with open(self.log_file, "a") as f:
            commit = self._commit(description)
            f.write(
                f"{iteration}\t{commit}\t{score}\t{delta:+d}\t{status}\t{description}\n"
            )

    def run(self):
        """Execute the optimization loop"""
        print(f"\n{'=' * 60}")
        print(f"AUTO RESEARCH LOOP: {self.skill_name}")
        print(f"{'=' * 60}")
        print(f"Target: {self.target_score}+ | Max iterations: {self.max_iterations}")
        print(f"Research log: {self.log_file}")
        print(f"{'=' * 60}\n")

        iteration = 0
        keeps = 0
        discards = 0
        crashes = 0

        while iteration < self.max_iterations:
            iteration += 1
            self.iteration = iteration

            print(f"\n--- Iteration {iteration}/{self.max_iterations} ---")

            # Select mutation strategy (rotate through)
            strategy = self.MUTATION_STRATEGIES[
                iteration % len(self.MUTATION_STRATEGIES)
            ]
            print(f"Strategy: {strategy}")

            # Apply mutation
            try:
                mutated_content, mutation_desc = self._mutate(strategy)

                # Write mutated version
                temp_path = self.skill_path.with_suffix(".tmp.md")
                temp_path.write_text(mutated_content)

                # Score mutated version (pass temp path)
                new_score = self._calculate_score(temp_path)

                # Clean up temp
                temp_path.unlink()

            except Exception as e:
                print(f"Crash: {e}")
                crashes += 1
                self._log_result(iteration, 0, 0, "crash", str(e))
                continue

            # Calculate delta
            delta = new_score - self.current_score

            # Select: keep or discard
            if new_score > self.current_score:
                status = "keep"
                keeps += 1
                self.current_content = mutated_content
                self.current_score = new_score

                # Update best if improved
                if new_score > self.best_score:
                    self.best_score = new_score
                    self.best_content = mutated_content
                    status = "keep (NEW BEST)"

                print(f"Result: {status} | Score: {self.current_score} ({delta:+d})")
                self._log_result(
                    iteration, self.current_score, delta, "keep", mutation_desc
                )

            else:
                status = "discard"
                discards += 1
                print(f"Result: {status} | Score: {self.current_score} ({delta:+d})")
                self._log_result(
                    iteration, self.current_score, delta, "discard", mutation_desc
                )

            # Check if target reached
            if self.current_score >= self.target_score:
                print(f"\n✓ TARGET REACHED: {self.current_score}/{self.target_score}")
                break

        # Save best version
        if self.best_content:
            self.skill_path.write_text(self.best_content)
            print(f"\nBest version saved: {self.best_score}")

        # Final summary
        print(f"\n{'=' * 60}")
        print(f"OPTIMIZATION COMPLETE")
        print(f"{'=' * 60}")
        print(f"Iterations: {iteration}")
        print(f"Keeps: {keeps} | Discards: {discards} | Crashes: {crashes}")
        print(
            f"Baseline: {self.best_score - sum([self.current_score])} → Best: {self.best_score}"
        )
        print(f"Research log: {self.log_file}")

        return {
            "iteration": iteration,
            "keeps": keeps,
            "discards": discards,
            "crashes": crashes,
            "best_score": self.best_score,
            "target_reached": self.best_score >= self.target_score,
        }


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Auto Research optimization loop")
    parser.add_argument("skill", help="Path to SKILL.md or draft file")
    parser.add_argument(
        "--target", type=int, default=85, help="Target score (default: 85)"
    )
    parser.add_argument(
        "--max-iterations",
        "-n",
        type=int,
        default=20,
        help="Maximum iterations (default: 20)",
    )
    parser.add_argument("--research-dir", "-o", help="Research output directory")

    args = parser.parse_args()

    loop = AutoResearchLoop(
        args.skill,
        target_score=args.target,
        max_iterations=args.max_iterations,
        research_dir=args.research_dir,
    )

    result = loop.run()

    # Exit code
    sys.exit(0 if result["target_reached"] else 1)


if __name__ == "__main__":
    main()
