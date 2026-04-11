#!/usr/bin/env python3
"""
TDD Runner for shadow-ops-prover skill
Tests: 7-stage pipeline, DM score validation, 1% rule validation
"""

import sys

TEST_CASES = [
    {
        "name": "stage_1_scout",
        "input": {"stage": "Find & Vet", "followers": 50000, "er": 5.0},
        "expected": "qualified",
    },
    {
        "name": "stage_2_dna",
        "input": {"stage": "Assimilation", "audience_size": 50000, "content_fit": 0.02},
        "expected": "1_percent_rule_valid",
    },
    {
        "name": "stage_3_relay",
        "input": {"stage": "Neural Relay", "hook_sent": True},
        "expected": "hook_delivered",
    },
    {
        "name": "stage_4_report",
        "input": {"stage": "Gameplan Delivery", "gameplan_sent": True},
        "expected": "asset_delivered",
    },
    {
        "name": "stage_5_dashboard",
        "input": {"stage": "CRM Tracking", "opened": True},
        "expected": "tracked",
    },
    {"name": "dm_score_min", "input": {"dm_score": 0.75}, "expected": "dm_score_valid"},
    {
        "name": "dm_score_invalid",
        "input": {"dm_score": 0.5},
        "expected": "dm_score_invalid",
    },
    {
        "name": "1_percent_rule",
        "input": {"audience_size": 100000, "content_fit": 0.015},
        "expected": "1_percent_rule_valid",
    },
]


def validate_stage(input_data):
    stage = input_data.get("stage", "")
    if stage == "Find & Vet":
        followers = input_data.get("followers", 0)
        er = input_data.get("er", 0)
        if followers >= 10000 and followers <= 100000 and er >= 3.0:
            return "qualified"
    elif stage == "Assimilation":
        audience_size = input_data.get("audience_size", 0)
        content_fit = input_data.get("content_fit", 0)
        if audience_size >= 10000 and content_fit >= 0.01:
            return "1_percent_rule_valid"
    elif stage == "Neural Relay":
        if input_data.get("hook_sent"):
            return "hook_delivered"
    elif stage == "Gameplan Delivery":
        if input_data.get("gameplan_sent"):
            return "asset_delivered"
    elif stage == "CRM Tracking":
        return "tracked"
    return "invalid"


def validate_dm_score(score):
    return "dm_score_valid" if score >= 0.7 else "dm_score_invalid"


def validate_1_percent_rule(audience_size, content_fit):
    return "1_percent_rule_valid" if content_fit >= 0.01 else "1_percent_rule_invalid"


def run_test(test_case):
    name = test_case["name"]
    data = test_case["input"]

    if "stage" in data:
        result = validate_stage(data)
        passed = result == test_case["expected"]
        return {"passed": passed, "details": f"Result: {result}"}
    elif "dm_score" in data:
        result = validate_dm_score(data["dm_score"])
        passed = result == test_case["expected"]
        return {"passed": passed, "details": f"DM Score: {data['dm_score']} → {result}"}
    elif "audience_size" in data:
        result = validate_1_percent_rule(data["audience_size"], data["content_fit"])
        passed = result == test_case["expected"]
        return {
            "passed": passed,
            "details": f"1% Rule: {data['content_fit'] * 100}% → {result}",
        }
    return {"passed": False, "details": "Unknown test"}


def main():
    print("🧪 shadow-ops-prover TDD Runner")
    print("=" * 50)
    passed = failed = 0
    for tc in TEST_CASES:
        result = run_test(tc)
        print(f"{'✅' if result['passed'] else '❌'} {tc['name']}: {result['details']}")
        passed += result["passed"]
        failed += 1 - result["passed"]
    print("=" * 50)
    print(f"Results: {passed}/{passed + failed} passed")
    return 0 if passed == len(TEST_CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
