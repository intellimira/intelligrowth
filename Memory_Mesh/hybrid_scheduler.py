#!/usr/bin/env python3
"""
MIRA Hybrid Training Scheduler
Smart training triggers based on multiple conditions

Triggers:
1. Time-based: Every 2 hours (base)
2. Data-driven: 20+ new interactions
3. Quality-triggered: Confidence drop > 10%
4. Manual override

Features:
- Caps training to max 1 per hour
- Priority-based training selection
- Training result logging
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


class HybridTrainingScheduler:
    """
    Smart training scheduler with multiple trigger types.

    Hybrid Strategy:
    - Base: Every 2 hours
    - Data: 20+ new interactions
    - Quality: Confidence drop > 10%
    - Cap: Max 1 training per hour
    """

    def __init__(
        self,
        state_file: str = "/home/sir-v/.mira/training_scheduler_state.json",
        min_interval_hours: int = 1,  # Min time between trainings
        base_interval_hours: int = 2,  # Base time interval
        data_trigger_threshold: int = 20,
        quality_trigger_threshold: float = 0.1,
    ):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        self.min_interval = timedelta(hours=min_interval_hours)
        self.base_interval = timedelta(hours=base_interval_hours)
        self.data_threshold = data_trigger_threshold
        self.quality_threshold = quality_trigger_threshold

        self._load_state()

    def _load_state(self):
        """Load scheduler state."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                self.state = json.load(f)
        else:
            self.state = self._create_default_state()

    def _create_default_state(self) -> Dict:
        """Create default state."""
        return {
            "last_training_check": None,
            "last_training_time": None,
            "total_trainings": 0,
            "trigger_reasons": [],
            "skipped_reasons": [],
            "settings": {
                "min_interval_hours": 1,
                "base_interval_hours": 2,
                "data_trigger_threshold": 20,
                "quality_trigger_threshold": 0.1,
            },
        }

    def _save_state(self):
        """Save scheduler state."""
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def _get_interaction_count(self) -> int:
        """Get count of recent interactions."""
        from self_assessment import MiraSelfAssessment

        try:
            assessor = MiraSelfAssessment()
            conn = sqlite3.connect(str(assessor.db_path))
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*) FROM interactions
                WHERE timestamp > datetime('now', '-1 hours')
            """)

            count = cursor.fetchone()[0]
            conn.close()

            return count
        except:
            return 0

    def _get_confidence_delta(self) -> float:
        """Get confidence change over recent period."""
        from self_assessment import MiraSelfAssessment

        try:
            assessor = MiraSelfAssessment()
            conn = sqlite3.connect(str(assessor.db_path))
            cursor = conn.cursor()

            # Compare last hour vs previous hour
            cursor.execute("""
                SELECT AVG(confidence_score) FROM interactions
                WHERE timestamp > datetime('now', '-1 hours')
            """)
            recent = cursor.fetchone()[0] or 0.5

            cursor.execute("""
                SELECT AVG(confidence_score) FROM interactions
                WHERE timestamp > datetime('now', '-2 hours')
                AND timestamp <= datetime('now', '-1 hours')
            """)
            previous = cursor.fetchone()[0] or 0.5

            conn.close()

            return recent - previous
        except:
            return 0.0

    def _can_train(self) -> Tuple[bool, str]:
        """
        Check if training is allowed based on time constraints.

        Returns (can_train, reason)
        """
        if not self.state.get("last_training_time"):
            return True, "No previous training"

        last_time = datetime.fromisoformat(self.state["last_training_time"])
        time_since = datetime.now() - last_time

        if time_since < self.min_interval:
            remaining = self.min_interval - time_since
            return (
                False,
                f"Too soon: {remaining.total_seconds() / 60:.0f} min remaining",
            )

        return True, "Time constraint passed"

    def check_triggers(self) -> Dict:
        """
        Check all training triggers.

        Returns comprehensive trigger analysis.
        """
        triggers = {
            "time_based": self._check_time_trigger(),
            "data_based": self._check_data_trigger(),
            "quality_based": self._check_quality_trigger(),
            "can_train": True,
            "should_train": False,
            "primary_reason": None,
        }

        # Determine if should train
        should_train = False
        reasons = []

        # Check time
        if triggers["time_based"]["triggered"]:
            should_train = True
            reasons.append(triggers["time_based"])

        # Check data
        if triggers["data_based"]["triggered"]:
            should_train = True
            reasons.append(triggers["data_based"])

        # Check quality (only if significant drop)
        if (
            triggers["quality_based"]["triggered"]
            and triggers["quality_based"]["delta"] < -self.quality_threshold
        ):
            should_train = True
            reasons.append(triggers["quality_based"])

        # Check time constraint
        can_train, time_reason = self._can_train()
        triggers["can_train"] = can_train

        if not can_train:
            should_train = False
            triggers["blocked_reason"] = time_reason

        triggers["should_train"] = should_train
        triggers["reasons"] = reasons

        if reasons:
            triggers["primary_reason"] = reasons[0]["type"]

        return triggers

    def _check_time_trigger(self) -> Dict:
        """Check if time-based trigger is met."""
        if not self.state.get("last_training_check"):
            return {"triggered": True, "type": "time", "reason": "First check"}

        last_check = datetime.fromisoformat(self.state["last_training_check"])
        time_since = datetime.now() - last_check

        triggered = time_since >= self.base_interval

        return {
            "triggered": triggered,
            "type": "time",
            "reason": f"{time_since.total_seconds() / 3600:.1f} hours since last check",
            "threshold": f"{self.base_interval.total_seconds() / 3600:.0f} hours",
        }

    def _check_data_trigger(self) -> Dict:
        """Check if data-driven trigger is met."""
        count = self._get_interaction_count()

        triggered = count >= self.data_threshold

        return {
            "triggered": triggered,
            "type": "data",
            "reason": f"{count} interactions in last hour",
            "threshold": f"{self.data_threshold}+ interactions",
        }

    def _check_quality_trigger(self) -> Dict:
        """Check if quality-triggered is met."""
        delta = self._get_confidence_delta()

        # Trigger if significant drop
        triggered = delta < -self.quality_threshold

        return {
            "triggered": triggered,
            "type": "quality",
            "delta": delta,
            "reason": f"Confidence {'dropped' if delta < 0 else 'stable'}: {delta:+.2f}",
            "threshold": f"< {-self.quality_threshold:.2f}",
        }

    def record_training(self, triggered: bool, reason: str, results: Dict = None):
        """Record training event."""
        self.state["last_training_time"] = datetime.now().isoformat()
        self.state["last_training_check"] = datetime.now().isoformat()

        if triggered:
            self.state["total_trainings"] += 1
            self.state["trigger_reasons"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "reason": reason,
                    "results": results,
                }
            )
            # Keep last 50
            if len(self.state["trigger_reasons"]) > 50:
                self.state["trigger_reasons"] = self.state["trigger_reasons"][-50:]
        else:
            self.state["skipped_reasons"].append(
                {"timestamp": datetime.now().isoformat(), "reason": reason}
            )
            if len(self.state["skipped_reasons"]) > 50:
                self.state["skipped_reasons"] = self.state["skipped_reasons"][-50:]

        self._save_state()

    def get_status(self) -> Dict:
        """Get scheduler status."""
        triggers = self.check_triggers()

        # Time since last training
        if self.state.get("last_training_time"):
            last_training = datetime.fromisoformat(self.state["last_training_time"])
            time_since = datetime.now() - last_training
        else:
            time_since = None

        return {
            "should_train": triggers["should_train"],
            "can_train": triggers["can_train"],
            "primary_reason": triggers.get("primary_reason"),
            "triggers": {
                "time": triggers["time_based"]["triggered"],
                "data": triggers["data_based"]["triggered"],
                "quality": triggers["quality_based"]["triggered"],
            },
            "last_training": self.state.get("last_training_time"),
            "time_since_last": time_since.total_seconds() / 3600
            if time_since
            else None,
            "total_trainings": self.state.get("total_trainings", 0),
            "blocked_reason": triggers.get("blocked_reason"),
            "settings": self.state.get("settings"),
        }

    def print_status(self):
        """Print formatted status."""
        status = self.get_status()

        print("\n" + "=" * 60)
        print("⏰ MIRA HYBRID TRAINING SCHEDULER")
        print("=" * 60)

        print(f"\n🎯 Should Train: {'YES ✅' if status['should_train'] else 'NO ⏭️'}")
        if status["should_train"]:
            print(f"   Primary Reason: {status['primary_reason']}")
        elif not status["can_train"]:
            print(f"   Blocked: {status['blocked_reason']}")

        print(f"\n⏱️ Triggers:")
        print(f"   Time-based: {'✅' if status['triggers']['time'] else '❌'}")
        print(f"   Data-based: {'✅' if status['triggers']['data'] else '❌'}")
        print(f"   Quality-based: {'✅' if status['triggers']['quality'] else '❌'}")

        print(f"\n📊 Statistics:")
        print(f"   Total trainings: {status['total_trainings']}")
        print(f"   Last training: {status['last_training'] or 'Never'}")
        if status["time_since_last"]:
            print(f"   Time since: {status['time_since_last']:.1f} hours")

        print(f"\n⚙️ Settings:")
        print(f"   Min interval: {status['settings']['min_interval_hours']}h")
        print(f"   Base interval: {status['settings']['base_interval_hours']}h")
        print(f"   Data threshold: {status['settings']['data_trigger_threshold']}+")
        print(
            f"   Quality threshold: {status['settings']['quality_trigger_threshold']}"
        )

    def trigger_training(self) -> Tuple[bool, str, Dict]:
        """
        Trigger training if conditions are met.

        Returns (triggered, reason, triggers)
        """
        triggers = self.check_triggers()

        if not triggers["should_train"] or not triggers["can_train"]:
            reason = triggers.get("blocked_reason", "No trigger conditions met")
            self.record_training(False, reason)
            return False, reason, triggers

        # Training should happen
        self.record_training(True, triggers["primary_reason"])
        return True, triggers["primary_reason"], triggers


def main():
    """CLI for hybrid training scheduler."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Hybrid Training Scheduler")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--check", action="store_true", help="Check triggers")
    parser.add_argument(
        "--trigger", action="store_true", help="Trigger training if ready"
    )

    args = parser.parse_args()

    scheduler = HybridTrainingScheduler()

    if args.status:
        scheduler.print_status()

    elif args.check:
        triggers = scheduler.check_triggers()
        print("\n📋 Trigger Analysis:")
        print(json.dumps(triggers, indent=2, default=str))

    elif args.trigger:
        triggered, reason, triggers = scheduler.trigger_training()
        if triggered:
            print(f"\n✅ Training triggered: {reason}")
        else:
            print(f"\n⏭️ Training skipped: {reason}")

    else:
        scheduler.print_status()


if __name__ == "__main__":
    main()
