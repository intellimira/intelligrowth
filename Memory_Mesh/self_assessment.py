#!/usr/bin/env python3
"""
MIRA Self-Assessment System
Implicit feedback through MIRA's own evaluation of its performance

Key Features:
- Self-assessed confidence scores
- Improvement detection
- Topic coverage tracking
- Automated quality flags
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import numpy as np


class MiraSelfAssessment:
    """
    MIRA self-assesses its own performance without user input.

    Tracks:
    - Response confidence scores
    - Improvement flags
    - Topic coverage
    - Quality trends
    """

    def __init__(self, db_path: str = "/home/sir-v/.mira/self_assessment.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

        # Thresholds
        self.confidence_threshold = 0.7
        self.improvement_threshold = 0.1
        self.coverage_threshold = 0.8

    def _init_db(self):
        """Initialize self-assessment database."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                query TEXT,
                response_length INTEGER,
                confidence_score REAL,
                topic TEXT,
                persona TEXT,
                improvement_flag INTEGER DEFAULT 0,
                metadata TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quality_trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                metric_name TEXT,
                value REAL,
                window_size INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topic_coverage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE,
                interactions INTEGER DEFAULT 0,
                avg_confidence REAL DEFAULT 0,
                last_seen TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS improvements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                area TEXT,
                description TEXT,
                confidence_delta REAL,
                status TEXT DEFAULT 'detected'
            )
        """)

        conn.commit()
        conn.close()

    def assess_interaction(
        self,
        query: str,
        response: str,
        topic: str = "general",
        persona: str = None,
        model_confidence: float = None,
    ) -> Dict:
        """
        Assess a single interaction.

        Returns self-assessed metrics.
        """
        # Calculate confidence score
        confidence = self._calculate_confidence(query, response, model_confidence)

        # Detect topic
        detected_topic = self._detect_topic(query)

        # Check for improvement
        improvement = self._check_improvement(confidence, detected_topic)

        # Record interaction
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO interactions 
            (timestamp, query, response_length, confidence_score, topic, persona, improvement_flag, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                datetime.now().isoformat(),
                query[:500],
                len(response),
                confidence,
                detected_topic,
                persona,
                1 if improvement["flag"] else 0,
                json.dumps({"raw_topic": topic}),
            ),
        )

        interaction_id = cursor.lastrowid

        # Update topic coverage
        cursor.execute(
            """
            INSERT INTO topic_coverage (topic, interactions, avg_confidence, last_seen)
            VALUES (?, 1, ?, ?)
            ON CONFLICT(topic) DO UPDATE SET
                interactions = interactions + 1,
                avg_confidence = (avg_confidence * interactions + ?) / (interactions + 1),
                last_seen = ?
        """,
            (
                detected_topic,
                confidence,
                datetime.now().isoformat(),
                confidence,
                datetime.now().isoformat(),
            ),
        )

        # Record improvement if detected
        if improvement["flag"]:
            cursor.execute(
                """
                INSERT INTO improvements (timestamp, area, description, confidence_delta)
                VALUES (?, ?, ?, ?)
            """,
                (
                    datetime.now().isoformat(),
                    detected_topic,
                    improvement["description"],
                    improvement["delta"],
                ),
            )

        conn.commit()
        conn.close()

        return {
            "interaction_id": interaction_id,
            "confidence": confidence,
            "topic": detected_topic,
            "improvement": improvement,
            "needs_training": confidence < self.confidence_threshold,
        }

    def _calculate_confidence(
        self, query: str, response: str, model_confidence: float = None
    ) -> float:
        """
        Calculate self-assessed confidence.

        Factors:
        - Response length (optimal range)
        - Query complexity
        - Topic familiarity
        - Model confidence (if available)
        """
        confidence = 0.5

        # Response length factor (optimal: 200-2000 chars)
        resp_len = len(response)
        if 200 <= resp_len <= 2000:
            confidence += 0.15
        elif resp_len < 100:
            confidence -= 0.2
        elif resp_len > 5000:
            confidence -= 0.1

        # Query complexity (longer queries = more complex = lower confidence)
        query_len = len(query)
        if query_len < 100:
            confidence += 0.1
        elif query_len > 500:
            confidence -= 0.1

        # Topic familiarity (check history)
        topic = self._detect_topic(query)
        topic_familiarity = self._get_topic_familiarity(topic)
        confidence += topic_familiarity * 0.2

        # Model confidence if available
        if model_confidence is not None:
            confidence = confidence * 0.7 + model_confidence * 0.3

        # Add small random variation to simulate uncertainty
        confidence += np.random.normal(0, 0.05)

        return max(0.0, min(1.0, confidence))

    def _detect_topic(self, text: str) -> str:
        """Detect topic from text."""
        text_lower = text.lower()

        topics = {
            "coding": [
                "code",
                "python",
                "function",
                "api",
                "implement",
                "bug",
                "debug",
            ],
            "ai_ml": [
                "model",
                "training",
                "neural",
                "machine learning",
                "ai",
                "embedding",
            ],
            "writing": ["write", "draft", "document", "essay", "blog"],
            "research": ["research", "study", "analyze", "investigate", "findings"],
            "planning": ["plan", "strategy", "roadmap", "schedule", "timeline"],
            "creative": ["creative", "brainstorm", "idea", "design", "imagine"],
            "technical": [
                "system",
                "architecture",
                "infrastructure",
                "deployment",
                "devops",
            ],
            "business": ["revenue", "market", "customer", "sales", "business model"],
        }

        for topic, keywords in topics.items():
            if any(kw in text_lower for kw in keywords):
                return topic

        return "general"

    def _get_topic_familiarity(self, topic: str) -> float:
        """Get familiarity score for topic based on history."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute(
            "SELECT interactions, avg_confidence FROM topic_coverage WHERE topic = ?",
            (topic,),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            interactions, avg_conf = result
            # More interactions + higher confidence = more familiar
            familiarity = min(1.0, (interactions / 10) * (avg_conf / 0.7))
            return familiarity

        return 0.0  # Unknown topic

    def _check_improvement(self, confidence: float, topic: str) -> Dict:
        """Check if this represents an improvement."""
        # Get recent average for this topic
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT AVG(confidence_score) 
            FROM interactions 
            WHERE topic = ? 
            AND timestamp > datetime('now', '-7 days')
            ORDER BY timestamp DESC
            LIMIT 20
        """,
            (topic,),
        )

        result = cursor.fetchone()
        conn.close()

        if result and result[0]:
            recent_avg = result[0]
            delta = confidence - recent_avg

            if delta > self.improvement_threshold:
                return {
                    "flag": True,
                    "delta": delta,
                    "description": f"Confidence improved for {topic}: +{delta:.2f}",
                }

        return {"flag": False, "delta": 0.0, "description": None}

    def get_confidence_trend(self, window_hours: int = 24) -> Dict:
        """Get confidence trend over time window."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                AVG(confidence_score) as avg_conf,
                COUNT(*) as count,
                MIN(confidence_score) as min_conf,
                MAX(confidence_score) as max_conf
            FROM interactions
            WHERE timestamp > datetime('now', '-' || ? || ' hours')
        """,
            (window_hours,),
        )

        result = cursor.fetchone()
        conn.close()

        return {
            "window_hours": window_hours,
            "avg_confidence": result[0] or 0.5,
            "interaction_count": result[1] or 0,
            "min_confidence": result[2] or 0,
            "max_confidence": result[3] or 1.0,
            "status": self._get_status(result[0] or 0.5),
        }

    def _get_status(self, confidence: float) -> str:
        """Get status from confidence score."""
        if confidence >= 0.8:
            return "excellent"
        elif confidence >= 0.7:
            return "good"
        elif confidence >= 0.5:
            return "acceptable"
        else:
            return "needs_improvement"

    def get_topic_coverage(self) -> List[Dict]:
        """Get topic coverage report."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute("""
            SELECT topic, interactions, avg_confidence, last_seen
            FROM topic_coverage
            ORDER BY interactions DESC
        """)

        results = [
            {
                "topic": r[0],
                "interactions": r[1],
                "avg_confidence": r[2],
                "last_seen": r[3],
            }
            for r in cursor.fetchall()
        ]

        conn.close()

        total = sum(r["interactions"] for r in results) or 1

        # Add coverage percentage
        for r in results:
            r["coverage_pct"] = (r["interactions"] / total) * 100

        return results

    def get_improvements_detected(self, limit: int = 10) -> List[Dict]:
        """Get detected improvements."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp, area, description, confidence_delta, status
            FROM improvements
            ORDER BY timestamp DESC
            LIMIT ?
        """,
            (limit,),
        )

        results = [
            {
                "timestamp": r[0],
                "area": r[1],
                "description": r[2],
                "delta": r[3],
                "status": r[4],
            }
            for r in cursor.fetchall()
        ]

        conn.close()
        return results

    def should_train(self) -> Tuple[bool, str]:
        """
        Determine if training should be triggered.

        Returns (should_train, reason)
        """
        trend = self.get_confidence_trend(window_hours=24)

        # Check confidence threshold
        if trend["avg_confidence"] < self.confidence_threshold:
            return True, f"Low confidence: {trend['avg_confidence']:.2f}"

        # Check interaction count
        if trend["interaction_count"] < 10:
            return False, f"Insufficient interactions: {trend['interaction_count']}"

        # Check for improvements
        improvements = self.get_improvements_detected(limit=5)
        if not improvements:
            return False, "No recent improvements detected"

        # Check coverage
        coverage = self.get_topic_coverage()
        low_coverage = [c for c in coverage if c["coverage_pct"] < 5]
        if len(low_coverage) > 3:
            return True, f"Low topic coverage: {len(low_coverage)} topics under 5%"

        return False, "Performance acceptable"

    def get_full_report(self) -> Dict:
        """Get comprehensive self-assessment report."""
        trend_24h = self.get_confidence_trend(24)
        trend_7d = self.get_confidence_trend(168)
        coverage = self.get_topic_coverage()
        improvements = self.get_improvements_detected()
        should_train, reason = self.should_train()

        return {
            "timestamp": datetime.now().isoformat(),
            "confidence_trend_24h": trend_24h,
            "confidence_trend_7d": trend_7d,
            "topic_coverage": coverage[:10],  # Top 10
            "improvements_detected": len(improvements),
            "should_train": should_train,
            "training_reason": reason,
            "status": trend_24h["status"],
        }

    def print_report(self):
        """Print formatted self-assessment report."""
        report = self.get_full_report()

        print("\n" + "=" * 60)
        print("🔍 MIRA SELF-ASSESSMENT REPORT")
        print("=" * 60)

        print(f"\n📊 Confidence Trend (24h):")
        print(f"   Average: {report['confidence_trend_24h']['avg_confidence']:.2f}")
        print(f"   Min: {report['confidence_trend_24h']['min_confidence']:.2f}")
        print(f"   Max: {report['confidence_trend_24h']['max_confidence']:.2f}")
        print(f"   Interactions: {report['confidence_trend_24h']['interaction_count']}")
        print(f"   Status: {report['status'].upper()}")

        print(f"\n📈 Confidence Trend (7d):")
        print(f"   Average: {report['confidence_trend_7d']['avg_confidence']:.2f}")
        print(f"   Interactions: {report['confidence_trend_7d']['interaction_count']}")

        print(f"\n🎯 Topic Coverage:")
        for topic in report["topic_coverage"][:5]:
            print(
                f"   {topic['topic']}: {topic['interactions']} ({topic['avg_confidence']:.2f})"
            )

        print(f"\n✨ Improvements Detected: {report['improvements_detected']}")

        print(f"\n🔄 Training Recommendation:")
        if report["should_train"]:
            print(f"   ✅ YES - {report['training_reason']}")
        else:
            print(f"   ⏭️ NO - {report['training_reason']}")

        print()


def main():
    """CLI for self-assessment."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Self-Assessment")
    parser.add_argument(
        "--assess", nargs=2, metavar=("QUERY", "RESPONSE"), help="Assess an interaction"
    )
    parser.add_argument("--report", action="store_true", help="Full report")
    parser.add_argument("--trend", action="store_true", help="Confidence trend")
    parser.add_argument("--topics", action="store_true", help="Topic coverage")
    parser.add_argument(
        "--should-train", action="store_true", help="Check training need"
    )

    args = parser.parse_args()

    assessor = MiraSelfAssessment()

    if args.assess:
        query, response = args.assess
        result = assessor.assess_interaction(query, response)
        print(f"\n✅ Assessment Complete:")
        print(f"   Confidence: {result['confidence']:.2f}")
        print(f"   Topic: {result['topic']}")
        print(f"   Improvement: {result['improvement']['flag']}")
        print(f"   Needs Training: {result['needs_training']}")

    elif args.report:
        assessor.print_report()

    elif args.trend:
        print(f"\n📈 Confidence Trend (24h):")
        print(json.dumps(assessor.get_confidence_trend(24), indent=2))

    elif args.topics:
        print(f"\n🎯 Topic Coverage:")
        for topic in assessor.get_topic_coverage():
            print(f"   {topic['topic']}: {topic['interactions']} interactions")

    elif args.should_train:
        should, reason = assessor.should_train()
        print(f"\n🔄 Should Train: {should}")
        print(f"   Reason: {reason}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
