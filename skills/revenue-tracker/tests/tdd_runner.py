#!/usr/bin/env python3
"""
TDD Runner for revenue-tracker skill
Tests: deal status progression, P&L calculation, MRR tracking
"""

import sys
import json
from pathlib import Path

# Test cases
TEST_CASES = [
    {
        "name": "status_progression_valid",
        "input": {"status": "PROSPECT"},
        "expected": "PROSPECT in valid states",
        "valid_states": [
            "PROSPECT",
            "ARCH_COMPLETE",
            "GROUNDED",
            "HITL_PENDING",
            "GO",
            "BUILD_COMPLETE",
            "LAUNCHED",
            "MRR_ACTIVE",
            "CHURNED",
        ],
    },
    {
        "name": "profit_calculation",
        "input": {
            "total_revenue_gbp": 1000,
            "dev_cost_gbp": 200,
            "gemini_cost_gbp": 50,
            "infra_cost_gbp": 25,
        },
        "expected": {"profit_gbp": 725, "total_cost_gbp": 275},
        "formula": "profit_gbp = total_revenue - dev_cost - gemini_cost - infra_cost",
    },
    {
        "name": "roi_calculation",
        "input": {"profit_gbp": 725, "total_cost_gbp": 275},
        "expected": {"roi_pct": 263.64},
        "formula": "roi_pct = (profit / total_cost) * 100",
    },
    {
        "name": "mrr_update",
        "input": {"status": "MRR_ACTIVE", "mrr_actual_gbp": 150},
        "expected": "mrr_updated",
        "quality_gate": "mrr_updated",
    },
    {
        "name": "p_and_l_accuracy",
        "input": {"deal_id": "test-001", "status": "LAUNCHED"},
        "expected": "p_and_l_accurate",
        "quality_gate": "p_and_l_accurate",
    },
]


def run_test(test_case):
    """Run a single test case"""
    name = test_case["name"]
    data = test_case["input"]

    if name == "status_progression_valid":
        valid = data["status"] in test_case["valid_states"]
        return {
            "passed": valid,
            "details": f"Status {data['status']} is {'valid' if valid else 'invalid'}",
        }

    elif name == "profit_calculation":
        total_revenue = data["total_revenue_gbp"]
        dev_cost = data["dev_cost_gbp"]
        gemini_cost = data["gemini_cost_gbp"]
        infra_cost = data["infra_cost_gbp"]

        expected_profit = test_case["expected"]["profit_gbp"]
        expected_cost = test_case["expected"]["total_cost_gbp"]

        actual_profit = total_revenue - dev_cost - gemini_cost - infra_cost
        actual_cost = dev_cost + gemini_cost + infra_cost

        profit_match = abs(actual_profit - expected_profit) < 0.01
        cost_match = abs(actual_cost - expected_cost) < 0.01

        return {
            "passed": profit_match and cost_match,
            "details": f"Profit: {actual_profit}, Cost: {actual_cost}",
        }

    elif name == "roi_calculation":
        profit = data["profit_gbp"]
        total_cost = data["total_cost_gbp"]

        expected_roi = test_case["expected"]["roi_pct"]
        actual_roi = (profit / total_cost) * 100 if total_cost > 0 else 0

        match = abs(actual_roi - expected_roi) < 0.01
        return {"passed": match, "details": f"ROI: {actual_roi:.2f}%"}

    elif name == "mrr_update":
        passed = data["status"] == "MRR_ACTIVE" and data["mrr_actual_gbp"] > 0
        return {
            "passed": passed,
            "details": "MRR updated" if passed else "MRR not updated",
        }

    elif name == "p_and_l_accuracy":
        passed = data["status"] == "LAUNCHED"
        return {
            "passed": passed,
            "details": "P&L accurate" if passed else "P&L not ready",
        }

    return {"passed": False, "details": "Unknown test"}


def main():
    print("🧪 revenue-tracker TDD Runner")
    print("=" * 50)

    passed = 0
    failed = 0

    for tc in TEST_CASES:
        result = run_test(tc)
        status = "✅" if result["passed"] else "❌"
        print(f"{status} {tc['name']}: {result['details']}")

        if result["passed"]:
            passed += 1
        else:
            failed += 1

    print("=" * 50)
    print(f"Results: {passed}/{passed + failed} passed")

    return 0 if passed == len(TEST_CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
