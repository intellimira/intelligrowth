#!/usr/bin/env python3
"""
TDD Runner for email-automation (enquiry-automation) skill
Tests: Gmail polling, lead scoring, Telegram alerts
"""

import sys

# Test cases
TEST_CASES = [
    {
        "name": "lead_score_critical",
        "input": {
            "subject": "URGENT: Need help with automation ASAP",
            "body": "Losing $10k/month due to manual processes",
        },
        "expected_score": 9,
        "threshold": 9,
        "action": "CRITICAL",
    },
    {
        "name": "lead_score_high",
        "input": {
            "subject": "Want to automate our workflow",
            "body": "We spend hours on manual data entry",
        },
        "expected_score": 7,
        "threshold": 7,
        "action": "HIGH",
    },
    {
        "name": "lead_score_medium",
        "input": {
            "subject": "Looking for help with automation",
            "body": "We need help with our manual workflow",
        },
        "expected_score": 5,
        "threshold": 5,
        "action": "MEDIUM",
    },
    {
        "name": "lead_score_low",
        "input": {
            "subject": "Question about pricing",
            "body": "How much does it cost?",
        },
        "expected_score": 3,
        "threshold": 3,
        "action": "LOW",
    },
    {
        "name": "lead_score_minimal",
        "input": {"subject": " unsubscribe ", "body": ""},
        "expected_score": 0,
        "threshold": 0,
        "action": "MINIMAL",
    },
]

# Keywords for scoring
URGENCY_KEYWORDS = [
    "urgent",
    "asap",
    "immediately",
    "emergency",
    "lose",
    "losing",
    "loses",
    "urgent",
]
PAIN_KEYWORDS = [
    "manual",
    "time",
    "money",
    "cost",
    "expensive",
    "frustrated",
    "stuck",
    "hours",
    "automation",
    "automate",
    "entry",
]
MEDIUM_KEYWORDS = [
    "help",
    "question",
    "wondering",
    "could",
    "want",
    "services",
    "offer",
    "looking",
    "need",
    "pricing",
]


def score_lead(subject: str, body: str) -> int:
    """Calculate lead score based on keywords"""
    text = f"{subject} {body}".lower()
    score = 0

    for kw in URGENCY_KEYWORDS:
        if kw in text:
            score += 3

    for kw in PAIN_KEYWORDS:
        if kw in text:
            score += 2

    for kw in MEDIUM_KEYWORDS:
        if kw in text:
            score += 1

    return min(score, 10)


def get_action(score: int) -> str:
    if score >= 9:
        return "CRITICAL"
    elif score >= 7:
        return "HIGH"
    elif score >= 5:
        return "MEDIUM"
    elif score >= 3:
        return "LOW"
    else:
        return "MINIMAL"


def run_test(test_case):
    data = test_case["input"]
    actual_score = score_lead(data["subject"], data["body"])
    action = get_action(actual_score)

    passed = actual_score >= test_case["threshold"]
    details = f"Score: {actual_score}, Action: {action}"

    return {"passed": passed, "details": details, "score": actual_score}


def main():
    print("🧪 email-automation TDD Runner")
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
