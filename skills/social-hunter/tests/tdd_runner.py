#!/usr/bin/env python3
"""
TDD Runner for social-hunter skill
Tests: sentiment analysis, lead signal extraction, platform targets
"""

import sys

TEST_CASES = [
    {
        "name": "sentiment_urgent",
        "input": {
            "text": "This is killing my business. Losing $5000/month on manual invoicing.",
            "platform": "reddit",
        },
        "expected_sentiment": "urgent",
        "expected_urgency_score": 8,
    },
    {
        "name": "sentiment_frustrated",
        "input": {
            "text": "This spreadsheet workaround is so frustrating and stuck.",
            "platform": "hackernews",
        },
        "expected_sentiment": "frustrated",
        "expected_urgency_score": 4,
    },
    {
        "name": "sentiment_curious",
        "input": {
            "text": "Anyone have recommendations for automation tools?",
            "platform": "indiehackers",
        },
        "expected_sentiment": "curious",
        "expected_urgency_score": 1,
    },
    {
        "name": "platform_filter_reddit",
        "input": {"platform": "reddit"},
        "expected_target": "r/SaaS",
    },
    {
        "name": "platform_filter_hn",
        "input": {"platform": "hackernews"},
        "expected_target": "hn.algolia.com",
    },
]

URGENT_KEYWORDS = [
    "losing",
    "killing",
    "emergency",
    "asap",
    "now",
    "urgent",
    "$",
    "/month",
    "/week",
]
FRUSTRATED_KEYWORDS = ["frustrated", "waste", "spreadsheet", "workaround", "stuck"]
PAIN_KEYWORDS = [
    "time",
    "money",
    "cost",
    "expensive",
    "slow",
    "tedious",
    "repetitive",
    "save",
    "looking",
    "anyone",
]


def analyze_sentiment(text: str) -> dict:
    text_lower = text.lower()
    urgency = 0
    for kw in URGENT_KEYWORDS:
        if kw in text_lower:
            urgency += 3
    for kw in FRUSTRATED_KEYWORDS:
        if kw in text_lower:
            urgency += 2
    for kw in PAIN_KEYWORDS:
        if kw in text_lower:
            urgency += 1

    if urgency >= 9:
        sentiment = "urgent"
    elif urgency >= 6:
        sentiment = "frustrated"
    elif urgency >= 1:
        sentiment = "curious"
    else:
        sentiment = "neutral"
    return {"sentiment": sentiment, "urgency": min(urgency, 10)}


def get_platform_target(platform: str) -> str:
    return {
        "reddit": "r/SaaS",
        "hackernews": "hn.algolia.com",
        "indiehackers": "indiehackers.com",
    }.get(platform, "")


def run_test(test_case):
    name = test_case["name"]
    data = test_case["input"]
    if "sentiment" in name:
        result = analyze_sentiment(data["text"])
        passed = (
            result["sentiment"] == test_case["expected_sentiment"]
            and result["urgency"] >= test_case["expected_urgency_score"]
        )
        return {
            "passed": passed,
            "details": f"Sentiment: {result['sentiment']}, Urgency: {result['urgency']}",
        }
    elif "platform" in name:
        target = get_platform_target(data["platform"])
        passed = target == test_case["expected_target"]
        return {"passed": passed, "details": f"Target: {target}"}
    return {"passed": False, "details": "Unknown test"}


def main():
    print("🧪 social-hunter TDD Runner")
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
