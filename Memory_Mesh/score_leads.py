#!/usr/bin/env python3
"""
MIRA Pain Score Calculator & Lead Qualifier
Calculates pain scores for enquiries and determines outreach priority.
"""

import json
import re
from pathlib import Path

# Pain keywords and weights
PAIN_KEYWORDS = {
    # Critical pain (weight: 3)
    "critical": [
        "urgent",
        "asap",
        "immediately",
        "desperate",
        "stuck",
        "broken",
        "failing",
        "losing money",
        "revenue",
        "deadline",
        "emergency",
        "crisis",
        "help",
        "can't",
        "impossible",
        "frustrated",
    ],
    # High value (weight: 2)
    "high": [
        "automation",
        "efficiency",
        "save time",
        "reduce cost",
        "scale",
        "growth",
        "improve",
        "better",
        "faster",
        "productivity",
        "integration",
        "workflow",
        "process",
        "system",
        "ai",
        "agent",
        "machine learning",
        "bot",
        "autonomous",
    ],
    # Medium value (weight: 1)
    "medium": [
        "exploring",
        "looking",
        "considering",
        "interested",
        "curious",
        "research",
        "understand",
        "learn",
        "compare",
        "options",
    ],
}

# Interest type weights
INTEREST_WEIGHTS = {
    "consulting": 2.5,  # High intent
    "collaboration": 2.0,  # Partnership interest
    "shadow-ops": 2.5,  # Business inquiry
    "newsletter": 0.5,  # Low intent
    "just-browsing": 0.3,  # Very low intent
    "other": 1.0,
}


def calculate_pain_score(enquiry):
    """Calculate pain score for an enquiry"""
    score = 5.0  # Base score
    message = enquiry.get("message", "").lower()
    interest = enquiry.get("interest", "other")

    # Interest weight
    score += INTEREST_WEIGHTS.get(interest, 1.0)

    # Pain keywords
    critical_matches = sum(1 for kw in PAIN_KEYWORDS["critical"] if kw in message)
    high_matches = sum(1 for kw in PAIN_KEYWORDS["high"] if kw in message)
    medium_matches = sum(1 for kw in PAIN_KEYWORDS["medium"] if kw in message)

    score += critical_matches * 1.5
    score += high_matches * 0.5
    score += medium_matches * 0.2

    # Message length (longer = more serious)
    if len(message) > 200:
        score += 0.5
    if len(message) > 500:
        score += 0.5

    # Has company name
    if enquiry.get("company") and enquiry["company"] != "N/A":
        score += 0.3

    # Has specific request
    if any(
        x in message
        for x in ["need", "want", "looking for", "help with", "build", "create"]
    ):
        score += 0.5

    return min(10.0, max(1.0, round(score, 1)))


def get_urgency_label(score):
    """Get urgency label for score"""
    if score >= 9:
        return "🔥 CRITICAL"
    elif score >= 7:
        return "⚠️ HIGH"
    elif score >= 5:
        return "📊 MEDIUM"
    elif score >= 3:
        return "📝 LOW"
    else:
        return "❌ MINIMAL"


def get_action(score):
    """Get recommended action based on score"""
    if score >= 9:
        return "Immediate Telegram alert + Email + Schedule call NOW"
    elif score >= 7:
        return "Telegram alert + User notification"
    elif score >= 5:
        return "Add to weekly digest + Queue for follow-up"
    elif score >= 3:
        return "Log + Newsletter nurture sequence"
    else:
        return "Log as 'not yet qualified' + Long-term nurture"


def score_lead(enquiry):
    """Score a single lead"""
    score = calculate_pain_score(enquiry)
    enquiry["pain_score"] = score
    enquiry["urgency"] = get_urgency_label(score)
    enquiry["recommended_action"] = get_action(score)
    return enquiry


def process_leads_from_repo(repo_path):
    """Process all leads in the enquiries repo"""
    repo = Path(repo_path)
    results = {"qualified": [], "not_qualified": [], "pending": []}

    for folder in ["prospects", "newsletter", "outreach"]:
        folder_path = repo / folder
        if not folder_path.exists():
            continue

        for json_file in folder_path.glob("*.json"):
            try:
                with open(json_file) as f:
                    enquiry = json.load(f)

                # Skip if already scored
                if enquiry.get("pain_score"):
                    if enquiry["pain_score"] >= 5:
                        results["qualified"].append(enquiry)
                    else:
                        results["not_qualified"].append(enquiry)
                else:
                    scored = score_lead(enquiry)

                    # Save updated enquiry
                    with open(json_file, "w") as f:
                        json.dump(scored, f, indent=2)

                    if scored["pain_score"] >= 5:
                        results["qualified"].append(scored)
                    else:
                        results["pending"].append(scored)

            except Exception as e:
                print(f"Error processing {json_file}: {e}")

    return results


def generate_report(results):
    """Generate weekly tally report"""
    total = (
        len(results["qualified"])
        + len(results["not_qualified"])
        + len(results["pending"])
    )
    qualified_count = len(results["qualified"])
    not_qualified_count = len(results["not_qualified"])
    pending_count = len(results["pending"])

    qualified_pct = (qualified_count / total * 100) if total > 0 else 0
    not_qualified_pct = (not_qualified_count / total * 100) if total > 0 else 0

    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 MIRA LEAD SCORING REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━

New Enquiries: {total}
━━━━━━━━━━━━━━━━━━━━━━━━━━
Qualified (5+):   {qualified_count} ({qualified_pct:.1f}%)
Not Qualified:    {not_qualified_count} ({not_qualified_pct:.1f}%)
Pending:          {pending_count}

TOP PAIN POINTS (from qualified leads):
"""

    # Analyze pain points
    pain_keywords = {}
    for lead in results["qualified"]:
        msg = lead.get("message", "").lower()
        for kw in PAIN_KEYWORDS["critical"] + PAIN_KEYWORDS["high"]:
            if kw in msg:
                pain_keywords[kw] = pain_keywords.get(kw, 0) + 1

    top_pains = sorted(pain_keywords.items(), key=lambda x: x[1], reverse=True)[:5]
    for i, (kw, count) in enumerate(top_pains, 1):
        report += f"  {i}. {kw.title()} ({count} leads)\n"

    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL LEADS (9+):
"""

    critical = [l for l in results["qualified"] if l.get("pain_score", 0) >= 9]
    if critical:
        for lead in critical[:3]:
            report += (
                f"  • {lead['name']} ({lead['email']}) - Score: {lead['pain_score']}\n"
            )
    else:
        report += "  None\n"

    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")}
MIRA Self-Training System
"""

    return report


if __name__ == "__main__":
    repo_path = "/home/sir-v/MiRA/enquiries_local"
    results = process_leads_from_repo(repo_path)
    report = generate_report(results)
    print(report)
