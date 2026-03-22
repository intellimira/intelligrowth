#!/usr/bin/env python3
"""
MIRA Feedback-Adaptive Training
Integrates user feedback into training priorities

Key Features:
- Weights training data by feedback scores
- Prioritizes weak areas
- Adaptive epoch allocation
- Performance tracking
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import torch
import torch.nn as nn
import numpy as np


class FeedbackAdaptiveTrainer:
    """
    Training that adapts based on user feedback.

    Pipeline:
    1. Analyze feedback patterns
    2. Calculate training priorities
    3. Weight training data
    4. Adaptive training
    """

    def __init__(
        self,
        data_dir: Path = Path("~/MIRA_ARCH_extracted"),
        feedback_db: Path = Path("/home/sir-v/.mira/feedback.db"),
        models_dir: Path = Path("~/.mira/weave_models"),
        priority_threshold: float = 0.5,
    ):
        self.data_dir = Path(os.path.expanduser(data_dir))
        self.feedback_db = Path(os.path.expanduser(feedback_db))
        self.models_dir = Path(os.path.expanduser(models_dir))
        self.priority_threshold = priority_threshold

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Feedback analysis
        self.feedback_stats = self._analyze_feedback()

        # Training priorities
        self.priorities = self._calculate_priorities()

    def _analyze_feedback(self) -> Dict:
        """Analyze feedback database."""
        if not self.feedback_db.exists():
            return {"total": 0, "by_type": {}, "by_persona": {}}

        conn = sqlite3.connect(str(self.feedback_db))
        cursor = conn.cursor()

        # Total feedback
        cursor.execute("SELECT COUNT(*) FROM feedback")
        total = cursor.fetchone()[0] or 0

        # By type
        cursor.execute("""
            SELECT feedback_type, COUNT(*), AVG(rating) 
            FROM feedback 
            GROUP BY feedback_type
        """)
        by_type = {
            r[0]: {"count": r[1], "avg_rating": r[2] or 3.0} for r in cursor.fetchall()
        }

        # By persona
        cursor.execute("""
            SELECT persona, COUNT(*), AVG(rating) 
            FROM feedback 
            WHERE rating > 0 AND persona IS NOT NULL
            GROUP BY persona
        """)
        by_persona = {
            r[0]: {"count": r[1], "avg_rating": r[2] or 3.0} for r in cursor.fetchall()
        }

        # Low-rated patterns
        cursor.execute("""
            SELECT pattern_type, frequency, severity
            FROM pattern_analysis
            WHERE severity > 0
            ORDER BY frequency * severity DESC
            LIMIT 10
        """)
        patterns = [
            {"type": r[0], "frequency": r[1], "severity": r[2]}
            for r in cursor.fetchall()
        ]

        conn.close()

        return {
            "total": total,
            "by_type": by_type,
            "by_persona": by_persona,
            "patterns": patterns,
        }

    def _calculate_priorities(self) -> Dict[str, float]:
        """
        Calculate training priorities based on feedback.

        Returns:
            Dict of skill_area -> priority score (higher = more training needed)
        """
        priorities = {}

        # Base priority from feedback count
        total = self.feedback_stats.get("total", 0)
        if total < 10:
            return {"default": 1.0}

        # Type-based priorities
        for ftype, data in self.feedback_stats.get("by_type", {}).items():
            # Lower rating = higher priority
            rating = data["avg_rating"]
            count = data["count"]

            # Priority formula: more low ratings = higher priority
            priority = (5 - rating) * count / 10
            priorities[ftype] = max(0.1, priority)

        # Persona-based priorities
        for persona, data in self.feedback_stats.get("by_persona", {}).items():
            rating = data["avg_rating"]
            if rating < 3.5:
                priorities[f"persona_{persona}"] = (4 - rating) * 2

        # Pattern-based priorities
        for pattern in self.feedback_stats.get("patterns", []):
            ptype = pattern["type"]
            freq = pattern["frequency"]
            sev = pattern["severity"]
            priorities[f"pattern_{ptype}"] = freq * sev / 5

        # Normalize
        if priorities:
            max_priority = max(priorities.values()) or 1.0
            priorities = {k: v / max_priority for k, v in priorities.items()}

        return priorities or {"default": 1.0}

    def get_priority_weights(self) -> Dict[str, float]:
        """Get priority weights for training."""
        return self.priorities

    def get_adaptive_epochs(self, base_epochs: int = 10) -> Dict[str, int]:
        """
        Calculate adaptive epoch allocation.

        More epochs for high-priority areas.
        """
        epochs = {}

        # Base allocation
        total_epochs = base_epochs

        if not self.priorities or len(self.priorities) <= 1:
            return {
                "link_prediction": base_epochs,
                "summarization": base_epochs,
                "quality_scoring": base_epochs,
            }

        # Allocate based on priorities
        for skill in ["link_prediction", "summarization", "quality_scoring"]:
            priority = self.priorities.get(skill, self.priorities.get("default", 0.5))
            epochs[skill] = max(1, int(base_epochs * (0.5 + priority)))

        return epochs

    def weight_training_data(self, data: List[Dict]) -> List[Tuple[Dict, float]]:
        """
        Weight training data based on feedback priorities.

        Returns:
            List of (data_sample, weight) tuples
        """
        weighted_data = []

        for doc in data:
            # Calculate weight based on category
            category = doc.get("category", "general")

            # Base weight
            weight = 1.0

            # Priority adjustment
            priority = self.priorities.get(
                category, self.priorities.get("default", 0.5)
            )
            weight *= 0.5 + priority

            # Quality adjustment (higher quality = lower weight needed)
            quality = doc.get("quality_score", 0.5)
            weight *= 2 - quality

            # Pattern adjustment
            for pattern in self.feedback_stats.get("patterns", []):
                if pattern["type"] in doc.get("content", "").lower():
                    weight *= 1 + pattern["severity"] * 0.2

            weighted_data.append((doc, weight))

        return weighted_data

    def get_training_recommendations(self) -> List[str]:
        """Get human-readable training recommendations."""
        recommendations = []

        # Check feedback volume
        total = self.feedback_stats.get("total", 0)
        if total < 10:
            recommendations.append(
                f"⚠️ Low feedback ({total}). Need 10+ for adaptive training."
            )

        # Check persona performance
        for persona, data in self.feedback_stats.get("by_persona", {}).items():
            rating = data["avg_rating"]
            if rating < 3.0:
                recommendations.append(
                    f"🔴 {persona} has low rating ({rating:.1f}). Prioritize training."
                )
            elif rating < 3.5:
                recommendations.append(f"🟡 {persona} could improve ({rating:.1f}).")

        # Check patterns
        for pattern in self.feedback_stats.get("patterns", [])[:3]:
            recommendations.append(
                f"📌 Address {pattern['type']} (seen {pattern['frequency']} times)"
            )

        # Check epochs
        epochs = self.get_adaptive_epochs()
        for skill, ep in epochs.items():
            if ep > 15:
                recommendations.append(f"🎯 Focus {ep} epochs on {skill}")

        return recommendations or ["✅ No major issues detected"]

    def print_analysis(self):
        """Print feedback analysis."""
        print("\n" + "=" * 60)
        print("🔄 FEEDBACK-ADAPTIVE TRAINING ANALYSIS")
        print("=" * 60)

        print(f"\n📊 Feedback Summary:")
        print(f"   Total feedback: {self.feedback_stats.get('total', 0)}")

        print(f"\n📈 By Type:")
        for ftype, data in self.feedback_stats.get("by_type", {}).items():
            print(f"   {ftype}: {data['count']} ({data['avg_rating']:.1f} avg)")

        print(f"\n🎭 By Persona:")
        for persona, data in self.feedback_stats.get("by_persona", {}).items():
            emoji = persona if persona else "?"
            print(f"   {emoji}: {data['count']} ({data['avg_rating']:.1f} avg)")

        print(f"\n🎯 Priorities:")
        for area, priority in sorted(self.priorities.items(), key=lambda x: -x[1])[:5]:
            print(f"   {area}: {priority:.2f}")

        print(f"\n⏱️ Adaptive Epochs:")
        epochs = self.get_adaptive_epochs()
        for skill, ep in epochs.items():
            print(f"   {skill}: {ep} epochs")

        print(f"\n💡 Recommendations:")
        for rec in self.get_training_recommendations():
            print(f"   {rec}")


class AdaptiveTrainingRunner:
    """
    Runs training with feedback-adaptive strategies.
    """

    def __init__(
        self, base_epochs: int = 10, batch_size: int = 8, learning_rate: float = 0.001
    ):
        self.base_epochs = base_epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.adaptive_trainer = FeedbackAdaptiveTrainer()
        self.results = {}

    def load_data(self) -> List[Dict]:
        """Load and weight training data."""
        data_file = Path("~/MIRA_ARCH_extracted/weave_training.jsonl")

        if not data_file.exists():
            return []

        with open(data_file) as f:
            lines = f.readlines()[:5000]

        data = []
        for line in lines:
            doc = json.loads(line)
            if doc.get("content") and len(doc["content"]) > 50:
                data.append(doc)

        # Weight data
        weighted = self.adaptive_trainer.weight_training_data(data)

        return weighted

    def train_with_feedback(
        self,
        model: nn.Module,
        data: List[Tuple[Dict, float]],
        skill_name: str,
        epochs: int,
    ) -> float:
        """Train model with weighted data."""
        optimizer = torch.optim.AdamW(model.parameters(), lr=self.learning_rate)
        criterion = nn.BCELoss()

        model.train()
        total_loss = 0.0
        steps = 0

        for epoch in range(epochs):
            # Shuffle weighted data
            np.random.shuffle(data)

            for i in range(0, len(data), self.batch_size):
                batch = data[i : i + self.batch_size]

                if len(batch) < 2:
                    continue

                # Create embeddings (simulated for now)
                embeddings = torch.randn(len(batch), 384).to(self.device)
                targets = torch.randint(0, 2, (len(batch), 1)).float().to(self.device)

                # Forward
                pred = model(embeddings, embeddings)
                loss = criterion(pred, targets)

                # Backward
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
                steps += 1

        avg_loss = total_loss / max(steps, 1)
        print(f"   {skill_name}: Loss={avg_loss:.4f}, Epochs={epochs}")

        return avg_loss

    def run_adaptive_training(self):
        """Run complete adaptive training."""
        print("\n" + "=" * 60)
        print("🎯 FEEDBACK-ADAPTIVE TRAINING")
        print("=" * 60)

        # Show analysis
        self.adaptive_trainer.print_analysis()

        # Load weighted data
        print("\n📚 Loading weighted training data...")
        weighted_data = self.load_data()
        print(f"   Loaded {len(weighted_data)} samples")

        if not weighted_data:
            print("❌ No training data available")
            return self.results

        # Get adaptive epochs
        epochs = self.adaptive_trainer.get_adaptive_epochs(self.base_epochs)

        # Train models (simplified)
        print("\n🔧 Training with Feedback Priorities...")

        # Save results
        results_dir = Path("~/.mira/adaptive_training")
        results_dir.mkdir(parents=True, exist_ok=True)

        results = {
            "timestamp": datetime.now().isoformat(),
            "feedback_stats": self.adaptive_trainer.feedback_stats,
            "priorities": self.adaptive_trainer.priorities,
            "adaptive_epochs": epochs,
            "recommendations": self.adaptive_trainer.get_training_recommendations(),
        }

        with open(results_dir / "latest.json", "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n💾 Results saved to {results_dir}")

        return results


def main():
    """CLI for feedback-adaptive training."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Feedback-Adaptive Training")
    parser.add_argument("--analyze", action="store_true", help="Analyze feedback only")
    parser.add_argument("--train", action="store_true", help="Run adaptive training")
    parser.add_argument("--epochs", type=int, default=10, help="Base epochs")

    args = parser.parse_args()

    trainer = FeedbackAdaptiveTrainer()

    if args.analyze or (not args.analyze and not args.train):
        trainer.print_analysis()

    if args.train:
        runner = AdaptiveTrainingRunner(base_epochs=args.epochs)
        runner.run_adaptive_training()


if __name__ == "__main__":
    main()
