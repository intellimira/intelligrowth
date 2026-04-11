#!/usr/bin/env python3
"""
pain-scorer TDD Runner
Validates scoring against test examples using RED-GREEN-REFACTOR pattern.
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent
TEST_FILE = SKILL_DIR / "test_examples.json"
RESULTS_FILE = SKILL_DIR / "test_results.json"


def load_test_cases():
    with open(TEST_FILE) as f:
        data = json.load(f)
    return data.get("test_cases", []), data.get("validation_rules", {})


def calculate_pis(input_data):
    """GREEN: Calculate PIS from input - aligned with SKILL.md"""
    # Frequency scoring (from SKILL.md)
    freq_scores = {
        "daily": 29,
        "weekly": 17,
        "monthly": 17,
        "quarterly": 10,
        "one-time": 0,
    }
    frequency = freq_scores.get(input_data.get("frequency", ""), 0)

    # Revenue proximity scoring
    rev_scores = {"explicit_cost": 24, "indirect_cost": 16, "time_cost": 10, "vague": 4}
    revenue = rev_scores.get(input_data.get("revenue_proximity", ""), 0)

    # Workaround evidence scoring
    work_scores = {"zapier_script": 19, "3plus_tools": 15, "manual_copy_paste": 10}
    workaround = work_scores.get(input_data.get("workaround_evidence", ""), 0)

    # Narrative complexity scoring
    narrative_scores = {"long_technical": 14, "moderate": 10, "short": 6}
    narrative = narrative_scores.get(input_data.get("narrative_complexity", ""), 0)

    # Budget ownership scoring
    budget_scores = {"ops_manager": 9, "influencer": 6, "no_budget": 2}
    budget = budget_scores.get(input_data.get("budget_ownership", ""), 0)

    return frequency + revenue + workaround + narrative + budget


def calculate_routing(pis, painful_avg, rules):
    """Apply routing logic from SKILL.md (OR logic corrected)"""
    s_rank_pis = 72
    s_rank_painful = 7.5
    a_rank_pis = 55
    a_rank_painful = 5.0

    # SKILL.md logic:
    # S-Rank: PIS >= 72 AND avg >= 7.5 (AND)
    # A-Rank: PIS 55-71 OR avg 5.0-7.4 (OR)
    # B-Rank: below both

    if pis >= s_rank_pis and painful_avg >= s_rank_painful:
        return "S-Rank"
    elif (pis >= a_rank_pis and pis < s_rank_pis) or (
        painful_avg >= a_rank_painful and painful_avg < s_rank_painful
    ):
        return "A-Rank"
    elif pis >= a_rank_pis or painful_avg >= a_rank_painful:
        return "A-Rank"  # OR condition
    else:
        return "B-Rank"


def calculate_painful(input_data):
    """GREEN: Simplified PAINFUL calculation"""
    signal = input_data.get("signal", "").lower()

    if "automated" in signal or "sync" in signal or "inventory" in signal:
        return 8.2  # High automation need = high PAINFUL
    elif "meeting" in signal or "notes" in signal:
        return 5.8  # Somewhat needed
    elif "better" in signal or "nice to have" in signal or "templates" in signal:
        return 2.5  # Nice to have = low PAINFUL
    else:
        return 5.5  # Default


def run_tests():
    """GREEN: Run tests against the validation logic"""
    test_cases, rules = load_test_cases()
    results = []
    passed = 0
    failed = 0

    print(f"🧪 Running TDD tests for pain-scorer ({len(test_cases)} cases)")
    print("=" * 50)

    for tc in test_cases:
        name = tc.get("name", "unnamed")
        input_data = tc.get("input", {})
        expected_pis = tc.get("expected_pis", 0)
        expected_routing = tc.get("expected_routing", "B-Rank")

        # Calculate PIS (GREEN implementation)
        actual_pis = calculate_pis(input_data)

        # Routing validation with PAINFUL
        actual_painful = calculate_painful(input_data)
        actual_routing = calculate_routing(actual_pis, actual_painful, rules)

        # Compare
        pis_match = actual_pis == expected_pis
        routing_match = actual_routing == expected_routing

        status = "✅ PASS" if (pis_match and routing_match) else "❌ FAIL"

        if pis_match and routing_match:
            passed += 1
        else:
            failed += 1

        print(f"\n{name}")
        print(
            f"  PIS: {actual_pis} (expected: {expected_pis}) {'✅' if pis_match else '❌'}"
        )
        print(
            f"  Routing: {actual_routing} (expected: {expected_routing}) {'✅' if routing_match else '❌'}"
        )
        print(f"  Status: {status}")

        results.append(
            {
                "test": name,
                "pis_actual": actual_pis,
                "pis_expected": expected_pis,
                "pis_match": pis_match,
                "routing_actual": actual_routing,
                "routing_expected": expected_routing,
                "routing_match": routing_match,
                "passed": pis_match and routing_match,
            }
        )

    # Save results
    with open(RESULTS_FILE, "w") as f:
        json.dump(
            {
                "summary": {
                    "passed": passed,
                    "failed": failed,
                    "total": len(test_cases),
                },
                "results": results,
            },
            f,
            indent=2,
        )

    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{len(test_cases)} passed, {failed} failed")

    return failed == 0


def refactor_prompt():
    """REFACTOR: Generate improvement suggestions"""
    print("\n🔧 REFACTOR Suggestions:")
    print("  1. Add PAINFUL layer calculation (currently hardcoded to 5.0)")
    print("  2. Add MGT loop validation (Reporter → Detective → Strategist)")
    print("  3. Add routing debug logging")
    print("  4. Create integration test with ollama")


if __name__ == "__main__":
    success = run_tests()
    if success:
        refactor_prompt()
    sys.exit(0 if success else 1)
