#!/usr/bin/env python3
"""
run_benchmark.py - Execute 10-run evaluation for Auto Research

Performs binary assessment (Yes/No) across 4 criteria:
1. YAML Validity - Does frontmatter parse correctly?
2. Trigger Relevance - Are triggers specific to skill purpose?
3. Tool Completeness - Are required tools included?
4. Persona Alignment - Does persona match skill type?

Output: 10x4 results matrix in TSV format
Max score: 40 (10 runs × 4 criteria)

Based on instruct_opencode.md methodology:
- 10 runs to account for AI "noise"
- Binary (Yes/No) to prevent compounding probabilities
- Median/Mode calculation for baseline
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


class BenchmarkRunner:
    """Runs 10-run evaluation benchmarks on SKILL.md files"""

    # Binary evaluation criteria
    CRITERIA = [
        "yaml_validity",  # Does the frontmatter parse correctly?
        "trigger_relevance",  # Are triggers specific to skill purpose?
        "tool_completeness",  # Are required tools included?
        "persona_alignment",  # Does persona match skill type?
    ]

    def __init__(self, skill_path: str, output_dir: Optional[str] = None):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.stem.replace("DRAFT_", "")

        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = self.skill_path.parent / "research"

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.results = []
        self.run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def load_skill(self) -> dict:
        """Load and parse SKILL.md"""
        content = self.skill_path.read_text()

        # Extract YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                return yaml.safe_load(frontmatter)

        return {}

    def generate_output(self, run_num: int) -> str:
        """
        Generate a single skill output using LLM.

        In a real implementation, this would call the LLM to generate
        a variant of the skill. For now, we'll use the current skill
        as the baseline and simulate mutations.
        """
        # For baseline runs, return current skill
        # In full implementation, this would:
        # 1. Take current SKILL.md instructions
        # 2. Use LLM to generate an output variant
        # 3. Return the generated content

        # Placeholder: read current skill
        return self.skill_path.read_text()

    def evaluate_binary(self, output: str, criteria: str) -> tuple[bool, str]:
        """
        Evaluate a single criteria with binary Yes/No.
        Returns (passed: bool, reason: str)
        """
        skill = self.load_skill()

        if criteria == "yaml_validity":
            try:
                if output.startswith("---"):
                    parts = output.split("---", 2)
                    if len(parts) >= 3:
                        yaml.safe_load(parts[1])
                        return True, "YAML parses correctly"
                return False, "YAML frontmatter missing or invalid"
            except:
                return False, "YAML parse error"

        elif criteria == "trigger_relevance":
            triggers = skill.get("triggers", [])
            description = skill.get("description", "")

            if not triggers or triggers == [[]] or triggers == []:
                return False, "No triggers defined"

            # Check if triggers are specific (not generic)
            generic = ["test", "run", "execute", "start", "stop"]
            flat_triggers = []
            for t in triggers:
                if isinstance(t, list):
                    flat_triggers.extend(t)
                else:
                    flat_triggers.append(t)

            specific = [t for t in flat_triggers if t and t.lower() not in generic]

            if len(specific) >= 2:
                return True, f"{len(specific)} specific triggers found"
            return False, "Triggers too generic or missing"

        elif criteria == "tool_completeness":
            tools = skill.get("tools", [])

            if not tools or tools == [[]] or tools == []:
                return False, "No tools defined"

            flat_tools = []
            for t in tools:
                if isinstance(t, list):
                    flat_tools.extend(t)
                else:
                    flat_tools.append(t)

            valid_tools = [t for t in flat_tools if t]

            if len(valid_tools) >= 3:
                return True, f"{len(valid_tools)} tools included"
            return False, "Too few tools defined"

        elif criteria == "persona_alignment":
            persona = skill.get("persona", "")
            name = skill.get("name", "")

            if not persona:
                return False, "No persona defined"

            # Check for valid persona format
            valid_emoji = ["⚛️", "🔬", "🤔", "✨", "⚙️", "🌑"]
            has_emoji = any(e in persona for e in valid_emoji)
            has_description = "—" in persona

            if has_emoji and has_description:
                return True, "Persona properly formatted"
            return False, "Persona missing emoji or description"

        return False, "Unknown criteria"

    def run_benchmark(self, num_runs: int = 10) -> dict:
        """
        Execute benchmark with specified number of runs.

        Returns:
            dict with: runs, scores, median, mode, total_score
        """
        print(f"Running benchmark on: {self.skill_name}")
        print(f"Criteria: {', '.join(self.CRITERIA)}")
        print(f"Runs: {num_runs}")
        print("-" * 50)

        all_results = []

        for run in range(num_runs):
            print(f"\nRun {run + 1}/{num_runs}...", end=" ")

            # Generate output (placeholder for LLM generation)
            output = self.generate_output(run)

            # Evaluate each criteria
            run_results = []
            for criteria in self.CRITERIA:
                passed, reason = self.evaluate_binary(output, criteria)
                run_results.append(
                    {"criteria": criteria, "passed": passed, "reason": reason}
                )

            # Calculate run score
            passed_count = sum(1 for r in run_results if r["passed"])
            run_score = passed_count * 10  # 10 points per criteria

            all_results.append(
                {
                    "run": run + 1,
                    "score": run_score,
                    "max_score": 40,
                    "results": run_results,
                }
            )

            print(f"Score: {run_score}/40")

        # Calculate statistics
        scores = [r["score"] for r in all_results]
        total_score = sum(scores)
        median = sorted(scores)[len(scores) // 2]

        # Calculate mode
        from collections import Counter

        mode_count = Counter(scores)
        mode = mode_count.most_common(1)[0][0] if mode_count else 0

        print("\n" + "=" * 50)
        print(f"BENCHMARK RESULTS: {self.skill_name}")
        print("=" * 50)
        print(f"Total Runs: {num_runs}")
        print(f"Total Score: {total_score}/{num_runs * 40}")
        print(f"Average: {total_score / num_runs:.1f}")
        print(f"Median: {median}")
        print(f"Mode: {mode}")
        print("-" * 50)

        # Generate results matrix
        print("\nResults Matrix (10x4):")
        print(
            f"{'Run':>4} {'YAML':>6} {'Trig':>6} {'Tool':>6} {'Pers':>6} {'Score':>6}"
        )
        print("-" * 40)

        for r in all_results:
            yaml_p = "✓" if r["results"][0]["passed"] else "✗"
            trig_p = "✓" if r["results"][1]["passed"] else "✗"
            tool_p = "✓" if r["results"][2]["passed"] else "✗"
            pers_p = "✓" if r["results"][3]["passed"] else "✗"
            print(
                f"{r['run']:>4} {yaml_p:>6} {trig_p:>6} {tool_p:>6} {pers_p:>6} {r['score']:>6}"
            )

        # Save to file
        output_file = self.output_dir / f"{self.skill_name}_{self.run_timestamp}.tsv"
        self._save_results(all_results, output_file)

        return {
            "skill_name": self.skill_name,
            "num_runs": num_runs,
            "total_score": total_score,
            "max_score": num_runs * 40,
            "average": total_score / num_runs,
            "median": median,
            "mode": mode,
            "runs": all_results,
            "output_file": str(output_file),
        }

    def _save_results(self, results: list, output_file: Path):
        """Save results to TSV file"""
        with open(output_file, "w") as f:
            # Header
            f.write("iteration\t")
            f.write("\t".join(self.CRITERIA))
            f.write("\tscore\tmax_score\n")

            # Data rows
            for r in results:
                f.write(f"{r['run']}\t")
                for cr in self.CRITERIA:
                    result = next(
                        (x for x in r["results"] if x["criteria"] == cr), None
                    )
                    f.write("yes\t" if result and result["passed"] else "no\t")
                f.write(f"{r['score']}\t{r['max_score']}\n")

        print(f"\nResults saved to: {output_file}")


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Run 10-run benchmark on SKILL.md")
    parser.add_argument("skill", help="Path to SKILL.md or draft file")
    parser.add_argument(
        "-n", "--runs", type=int, default=10, help="Number of runs (default: 10)"
    )
    parser.add_argument("-o", "--output", help="Output directory for results")

    args = parser.parse_args()

    runner = BenchmarkRunner(args.skill, args.output)
    result = runner.run_benchmark(args.runs)

    # Exit code based on score
    if result["average"] >= 34:  # 85% of 40
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
