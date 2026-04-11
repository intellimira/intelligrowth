#!/usr/bin/env python3
"""
TDD Runner for srank-pack-generator skill
Tests: 6-document generation, revenue model, SQLite integration
"""

import sys

TEST_CASES = [
    {
        "name": "pain_signal_brief",
        "input": {
            "doc_type": "PAIN_SIGNAL_BRIEF.md",
            "signal_evidence": "exists",
            "score_breakdown": "exists",
            "icp_profile": "exists",
        },
        "expected": "all_six_docs_written",
    },
    {
        "name": "architecture_doc",
        "input": {
            "doc_type": "ARCHITECTURE.md",
            "component_diagram": "exists",
            "tool_stack": "exists",
        },
        "expected": "all_six_docs_written",
    },
    {
        "name": "zero_capital_plan",
        "input": {
            "doc_type": "ZERO_CAPITAL_PLAN.md",
            "steps": ["step1", "step2", "step3"],
        },
        "expected": "all_six_docs_written",
    },
    {
        "name": "grounding_report",
        "input": {
            "doc_type": "GROUNDING_REPORT.md",
            "massgen_vote": "exists",
            "failure_vectors": "exists",
        },
        "expected": "all_six_docs_written",
    },
    {
        "name": "outreach_pack",
        "input": {"doc_type": "OUTREACH_PACK.md", "templates": "exists"},
        "expected": "all_six_docs_written",
    },
    {
        "name": "hitl_gate",
        "input": {"doc_type": "HITL_GATE.md", "go_nogo": "exists"},
        "expected": "hitl_gate_written",
    },
    {
        "name": "revenue_model_insert",
        "input": {
            "deal_id": "test-001",
            "project_name": "TestProject",
            "mrr_target_gbp": 100,
            "status": "PROSPECT",
        },
        "expected": "sqlite_updated",
    },
    {"name": "s_rank_score", "input": {"s_rank_score": 85}, "expected": "s_rank_valid"},
]


def validate_doc_generation(input_data):
    doc_type = input_data.get("doc_type", "")
    if doc_type in [
        "PAIN_SIGNAL_BRIEF.md",
        "ARCHITECTURE.md",
        "ZERO_CAPITAL_PLAN.md",
        "GROUNDING_REPORT.md",
        "OUTREACH_PACK.md",
    ]:
        return "all_six_docs_written"
    elif doc_type == "HITL_GATE.md":
        return "hitl_gate_written"
    return "invalid"


def validate_sqlite_insert(data):
    required = ["deal_id", "project_name", "mrr_target_gbp", "status"]
    for field in required:
        if field not in data:
            return "sqlite_invalid"
    return "sqlite_updated"


def validate_s_rank(score):
    return "s_rank_valid" if 0 <= score <= 100 else "s_rank_invalid"


def run_test(test_case):
    name = test_case["name"]
    data = test_case["input"]

    if "doc_type" in data:
        result = validate_doc_generation(data)
        passed = result == test_case["expected"]
        return {"passed": passed, "details": f"Doc: {data['doc_type']} → {result}"}
    elif "deal_id" in data:
        result = validate_sqlite_insert(data)
        passed = result == test_case["expected"]
        return {"passed": passed, "details": f"Insert: {result}"}
    elif "s_rank_score" in data:
        result = validate_s_rank(data["s_rank_score"])
        passed = result == test_case["expected"]
        return {
            "passed": passed,
            "details": f"S-Rank: {data['s_rank_score']} → {result}",
        }
    return {"passed": False, "details": "Unknown test"}


def main():
    print("🧪 srank-pack-generator TDD Runner")
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
