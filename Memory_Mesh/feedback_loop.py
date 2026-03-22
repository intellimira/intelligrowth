#!/usr/bin/env python3
"""
MIRA Feedback Loop
Collects and processes user feedback for continuous model improvement

Pipeline:
1. Collect feedback (explicit + implicit)
2. Analyze patterns
3. Adjust training priorities
4. Re-train on weak areas
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


class FeedbackCollector:
    """
    Collects user feedback on MIRA responses.

    Feedback Types:
    - Explicit: User ratings, corrections
    - Implicit: Response time, follow-up questions, edits
    """

    def __init__(self):
        self.db_path = Path("/home/sir-v/.mira/feedback.db")
        self.feedback_dir = Path("/home/sir-v/.mira/feedback")
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize feedback database."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                query TEXT,
                response TEXT,
                feedback_type TEXT,
                rating INTEGER,
                persona TEXT,
                tags TEXT,
                metadata TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pattern_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                pattern_type TEXT,
                pattern_text TEXT,
                frequency INTEGER,
                severity INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_priority (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                skill_area TEXT,
                priority_score REAL,
                feedback_count INTEGER,
                trend TEXT
            )
        """)

        conn.commit()
        conn.close()

    def add_feedback(
        self,
        query: str,
        response: str,
        feedback_type: str,
        rating: int = 0,
        persona: str = None,
        tags: List[str] = None,
        metadata: Dict = None,
    ) -> int:
        """
        Add feedback to the database.

        Args:
            query: User's query
            response: MIRA's response
            feedback_type: "explicit", "implicit", "correction"
            rating: 1-5 scale (for explicit feedback)
            persona: Active persona
            tags: Topic tags
            metadata: Additional metadata

        Returns:
            Feedback ID
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO feedback 
            (timestamp, query, response, feedback_type, rating, persona, tags, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                datetime.now().isoformat(),
                query,
                response,
                feedback_type,
                rating,
                persona,
                json.dumps(tags or []),
                json.dumps(metadata or {}),
            ),
        )

        feedback_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Analyze pattern
        self._analyze_pattern(query, response, feedback_type, rating)

        return feedback_id

    def _analyze_pattern(
        self, query: str, response: str, feedback_type: str, rating: int
    ):
        """Analyze feedback for patterns."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # Extract common patterns
        patterns = []

        # Check for low ratings
        if rating > 0 and rating <= 2:
            patterns.append(("low_rating", 1))

        # Check for correction keywords
        correction_keywords = ["wrong", "incorrect", "better", "should be", "try again"]
        for kw in correction_keywords:
            if kw in query.lower() or kw in response.lower():
                patterns.append((f"correction_{kw}", 2))

        # Check for follow-up (implicit positive)
        if "?" in query and len(response) > 500:
            patterns.append(("thorough_response", -1))  # Negative = good

        # Update pattern counts
        for pattern_type, severity in patterns:
            cursor.execute(
                """
                INSERT INTO pattern_analysis 
                (timestamp, pattern_type, pattern_text, frequency, severity)
                VALUES (?, ?, ?, 1, ?)
                ON CONFLICT(pattern_type, pattern_text) 
                DO UPDATE SET frequency = frequency + 1
            """,
                (datetime.now().isoformat(), pattern_type, "", severity),
            )

        conn.commit()
        conn.close()

    def get_patterns(self, min_frequency: int = 3) -> List[Dict]:
        """Get frequent feedback patterns."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT pattern_type, pattern_text, frequency, severity
            FROM pattern_analysis
            WHERE frequency >= ?
            ORDER BY severity DESC, frequency DESC
        """,
            (min_frequency,),
        )

        patterns = [
            {"type": r[0], "text": r[1], "frequency": r[2], "severity": r[3]}
            for r in cursor.fetchall()
        ]

        conn.close()
        return patterns

    def calculate_training_priorities(self) -> List[Dict]:
        """
        Calculate training priorities based on feedback.

        Returns:
            List of skill areas ranked by improvement priority
        """
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # Analyze feedback by type
        cursor.execute("""
            SELECT 
                feedback_type,
                COUNT(*) as count,
                AVG(rating) as avg_rating
            FROM feedback
            WHERE rating > 0
            GROUP BY feedback_type
        """)

        type_analysis = {
            r[0]: {"count": r[1], "avg_rating": r[2]} for r in cursor.fetchall()
        }

        # Calculate priorities
        priorities = []

        for ftype, data in type_analysis.items():
            # Lower rating = higher priority
            priority = (5 - (data["avg_rating"] or 3)) * data["count"]
            priorities.append(
                {
                    "skill_area": ftype,
                    "priority_score": priority,
                    "feedback_count": data["count"],
                    "avg_rating": data["avg_rating"],
                    "trend": "increasing" if priority > 10 else "stable",
                }
            )

        # Sort by priority
        priorities.sort(key=lambda x: x["priority_score"], reverse=True)

        # Store priorities
        for p in priorities:
            cursor.execute(
                """
                INSERT INTO training_priority
                (timestamp, skill_area, priority_score, feedback_count, trend)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    datetime.now().isoformat(),
                    p["skill_area"],
                    p["priority_score"],
                    p["feedback_count"],
                    p["trend"],
                ),
            )

        conn.commit()
        conn.close()

        return priorities

    def get_summary(self) -> Dict:
        """Get feedback summary."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # Total feedback
        cursor.execute("SELECT COUNT(*) FROM feedback")
        total = cursor.fetchone()[0]

        # By type
        cursor.execute("""
            SELECT feedback_type, COUNT(*) 
            FROM feedback 
            GROUP BY feedback_type
        """)
        by_type = dict(cursor.fetchall())

        # Average rating
        cursor.execute("SELECT AVG(rating) FROM feedback WHERE rating > 0")
        avg_rating = cursor.fetchone()[0] or 0

        # By persona
        cursor.execute("""
            SELECT persona, AVG(rating) 
            FROM feedback 
            WHERE rating > 0 AND persona IS NOT NULL
            GROUP BY persona
        """)
        by_persona = {r[0]: r[1] for r in cursor.fetchall()}

        conn.close()

        return {
            "total_feedback": total,
            "by_type": by_type,
            "avg_rating": round(avg_rating, 2),
            "by_persona": by_persona,
            "patterns": self.get_patterns(),
            "priorities": self.calculate_training_priorities(),
        }


class FeedbackLoop:
    """
    Main feedback loop for continuous improvement.

    Integrates feedback collection with training pipeline.
    """

    def __init__(self):
        self.collector = FeedbackCollector()
        self.training_state_path = Path("/home/sir-v/.mira/training_state.json")

    def record_interaction(
        self,
        query: str,
        response: str,
        persona: str = None,
        quality_score: float = None,
        response_time_ms: int = None,
    ):
        """
        Record an interaction for the feedback loop.

        Args:
            query: User query
            response: MIRA response
            persona: Active persona
            quality_score: Optional quality rating
            response_time_ms: Response generation time
        """
        metadata = {
            "quality_score": quality_score,
            "response_time_ms": response_time_ms,
            "response_length": len(response),
        }

        # Determine feedback type
        if quality_score is not None:
            if quality_score >= 4:
                feedback_type = "implicit_positive"
                rating = 5
            elif quality_score >= 3:
                feedback_type = "implicit_neutral"
                rating = 3
            else:
                feedback_type = "implicit_negative"
                rating = 1
        else:
            feedback_type = "implicit_neutral"
            rating = 0

        self.collector.add_feedback(
            query=query,
            response=response,
            feedback_type=feedback_type,
            rating=rating,
            persona=persona,
            metadata=metadata,
        )

    def record_correction(
        self,
        query: str,
        original_response: str,
        corrected_response: str,
        persona: str = None,
    ):
        """Record a user correction."""
        self.collector.add_feedback(
            query=query,
            response=original_response,
            feedback_type="correction",
            rating=1,
            persona=persona,
            tags=["correction"],
            metadata={"corrected": corrected_response},
        )

    def get_improvement_suggestions(self) -> List[str]:
        """Get suggestions for model improvement."""
        summary = self.collector.get_summary()
        suggestions = []

        # Based on low-rated areas
        for priority in summary.get("priorities", []):
            if priority["priority_score"] > 5:
                suggestions.append(
                    f"Focus training on {priority['skill_area']} "
                    f"(priority: {priority['priority_score']:.1f})"
                )

        # Based on patterns
        for pattern in summary.get("patterns", []):
            if pattern["severity"] > 0:
                suggestions.append(
                    f"Address {pattern['type']} pattern "
                    f"(seen {pattern['frequency']} times)"
                )

        # Based on persona performance
        for persona, rating in summary.get("by_persona", {}).items():
            if rating < 3.5:
                suggestions.append(
                    f"Improve {persona} persona training (rating: {rating:.1f})"
                )

        return suggestions

    def should_retrain(self) -> tuple[bool, str]:
        """
        Determine if models should be retrained.

        Returns:
            (should_retrain, reason)
        """
        summary = self.collector.get_summary()

        # Check feedback count
        if summary["total_feedback"] < 20:
            return False, "Insufficient feedback (< 20)"

        # Check average rating
        if summary["avg_rating"] < 3.0:
            return True, f"Low avg rating ({summary['avg_rating']:.1f})"

        # Check for high-priority issues
        for priority in summary.get("priorities", []):
            if priority["priority_score"] > 20:
                return True, f"High priority issue: {priority['skill_area']}"

        return False, "Performance acceptable"

    def print_status(self):
        """Print feedback loop status."""
        summary = self.collector.get_summary()

        print("\n" + "=" * 60)
        print("🔄 MIRA FEEDBACK LOOP STATUS")
        print("=" * 60)

        print(f"\n📊 Feedback Summary:")
        print(f"   Total interactions: {summary['total_feedback']}")
        print(f"   Average rating: {summary['avg_rating']:.2f}")

        print(f"\n📈 By Type:")
        for ftype, count in summary.get("by_type", {}).items():
            print(f"   {ftype}: {count}")

        print(f"\n🎭 By Persona:")
        for persona, rating in summary.get("by_persona", {}).items():
            emoji = persona if persona else "?"
            print(f"   {emoji}: {rating:.2f}")

        print(f"\n🎯 Improvement Suggestions:")
        suggestions = self.get_improvement_suggestions()
        if suggestions:
            for s in suggestions[:5]:
                print(f"   • {s}")
        else:
            print("   No major issues detected")

        should_retrain, reason = self.should_retrain()
        print(f"\n🔄 Should Retrain: {'YES' if should_retrain else 'NO'}")
        print(f"   Reason: {reason}")

        print()


def main():
    """CLI for feedback loop."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Feedback Loop")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument(
        "--record",
        nargs=4,
        metavar=("QUERY", "RESPONSE", "TYPE", "RATING"),
        help="Record feedback",
    )
    parser.add_argument("--patterns", action="store_true", help="Show patterns")
    parser.add_argument("--suggest", action="store_true", help="Get suggestions")

    args = parser.parse_args()

    loop = FeedbackLoop()

    if args.status:
        loop.print_status()
    elif args.patterns:
        patterns = loop.collector.get_patterns()
        print("\n📋 Feedback Patterns:")
        for p in patterns:
            print(f"   {p['type']}: {p['frequency']}x (severity: {p['severity']})")
    elif args.suggest:
        suggestions = loop.get_improvement_suggestions()
        print("\n💡 Improvement Suggestions:")
        for s in suggestions:
            print(f"   • {s}")
    elif args.record:
        query, response, ftype, rating = args.record
        loop.record_interaction(
            query, response, feedback_type=ftype, rating=int(rating)
        )
        print("✅ Feedback recorded")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
