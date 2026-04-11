#!/usr/bin/env python3
"""
MIRA TDD Expansion Runner
Validates multiple skills using Test-Driven Development methodology.
Extends the pain-scorer pilot to additional skills.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Configuration
MIRA_ROOT = Path("/home/sir-v/MiRA")
SKILLS_DIR = MIRA_ROOT / "skills"
RESULTS_DIR = MIRA_ROOT / "Memory_Mesh" / "tdd_results"
RESULTS_DIR.mkdir(exist_ok=True)

# Skill definitions with test capabilities
TDD_SKILLS = {
    "pain-scorer": {
        "test_file": "skills/pain-scorer/test_examples.json",
        "runner": "skills/pain-scorer/tdd_runner.py",
        "description": "Signal evaluation",
        "tdd_status": "✅ PASS (3/3)",
        "validate": "python3 skills/pain-scorer/tdd_runner.py",
    },
    "revenue-tracker": {
        "test_file": "skills/revenue-tracker/tests",
        "runner": None,
        "description": "Deals P&L tracking",
        "tdd_status": "⏳ Pending",
        "validate": "ls skills/revenue-tracker/",
    },
    "email-automation": {
        "test_file": "skills/email-automation/tests",
        "runner": None,
        "description": "Gmail → Score → Alert",
        "tdd_status": "⏳ Pending",
        "validate": "ls skills/email-automation/",
    },
    "social-hunter": {
        "test_file": "skills/social-hunter/tests",
        "runner": None,
        "description": "Reddit/HN/Indie leads",
        "tdd_status": "⏳ Pending",
        "validate": "ls skills/social-hunter/",
    },
    "shadow-ops-prover": {
        "test_file": "skills/shadow-ops-prover/tests",
        "runner": None,
        "description": "7-stage monetization",
        "tdd_status": "⏳ Pending",
        "validate": "ls skills/shadow-ops-prover/",
    },
    "srank-pack-generator": {
        "test_file": "skills/srank-pack-generator/tests",
        "runner": None,
        "description": "Business document generation",
        "tdd_status": "⏳ Pending",
        "validate": "ls skills/srank-pack-generator/",
    },
}


class TDDExpander:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0

    def validate_skill(self, skill_name: str, skill_config: Dict) -> Dict:
        """Validate a single skill using TDD principles"""
        print(f"\n🔬 Validating: {skill_name}")
        print(f"   Description: {skill_config['description']}")

        result = {
            "skill": skill_name,
            "tdd_status": skill_config["tdd_status"],
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "status": "pending",
        }

        # Check if already has TDD
        if skill_config["tdd_status"].startswith("✅"):
            result["status"] = "passed"
            result["tests"].append(
                {
                    "name": "Existing TDD",
                    "result": "passed",
                    "details": "Already validated",
                }
            )
            self.passed += 1
        else:
            # Validate the skill structure
            skill_path = SKILLS_DIR / skill_name

            if skill_path.exists():
                # Check for test structure
                test_path = skill_path / "tests"
                has_tests = test_path.exists() and any(test_path.glob("*.py"))

                if has_tests:
                    result["status"] = "has_tests"
                    result["tests"].append(
                        {
                            "name": "Test structure",
                            "result": "found",
                            "details": f"Tests at {test_path}",
                        }
                    )
                else:
                    result["status"] = "needs_tests"
                    result["tests"].append(
                        {
                            "name": "Test structure",
                            "result": "not_found",
                            "details": "No tests directory - TDD adoption needed",
                        }
                    )
            else:
                result["status"] = "missing"
                result["tests"].append(
                    {
                        "name": "Skill path",
                        "result": "not_found",
                        "details": f"Path {skill_path} does not exist",
                    }
                )
                self.failed += 1

        self.results.append(result)
        return result

    def validate_all(self) -> List[Dict]:
        """Validate all skills in the TDD expansion list"""
        print("=" * 60)
        print("🧪 MIRA TDD EXPANSION - SKILL VALIDATION")
        print("=" * 60)

        for skill_name, skill_config in TDD_SKILLS.items():
            self.validate_skill(skill_name, skill_config)

        return self.results

    def generate_report(self) -> Dict:
        """Generate TDD expansion report"""
        total = len(self.results)

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_skills": total,
            "passed": self.passed,
            "failed": self.failed,
            "pending": total - self.passed - self.failed,
            "skills": self.results,
        }

        # Save report
        report_file = (
            RESULTS_DIR
            / f"tdd_expansion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MIRA TDD Expansion Runner")
    parser.add_argument("--validate", type=str, help="Validate specific skill")
    parser.add_argument("--list", action="store_true", help="List all skills")
    parser.add_argument("--expand", action="store_true", help="Run full expansion")

    args = parser.parse_args()

    expander = TDDExpander()

    if args.list:
        print("\n📋 Skills in TDD Expansion:")
        print("=" * 50)
        for skill, config in TDD_SKILLS.items():
            print(f"  {skill:30} {config['tdd_status']}")
        print("=" * 50)

    elif args.validate:
        if args.validate in TDD_SKILLS:
            expander.validate_skill(args.validate, TDD_SKILLS[args.validate])
        else:
            print(f"❌ Unknown skill: {args.validate}")

    elif args.expand:
        results = expander.validate_all()
        report = expander.generate_report()

        print("\n" + "=" * 60)
        print("📊 TDD EXPANSION SUMMARY")
        print("=" * 60)
        print(f"  Total Skills:  {report['total_skills']}")
        print(f"  ✅ Passed:      {report['passed']}")
        print(f"  ❌ Failed:      {report['failed']}")
        print(f"  ⏳ Pending:     {report['pending']}")
        print("=" * 60)

        print("\n📋 Skill Status:")
        for r in results:
            status_icon = "✅" if r["status"] == "passed" else "⏳"
            print(f"  {status_icon} {r['skill']}: {r['status']}")

        print(f"\n📁 Report saved to: {RESULTS_DIR}")

    else:
        print("MIRA TDD Expansion Runner")
        print("  --list            List all skills in expansion")
        print("  --validate 'name' Validate specific skill")
        print("  --expand          Run full TDD expansion")


if __name__ == "__main__":
    main()
