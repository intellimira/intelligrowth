#!/usr/bin/env python3
"""
MIRA Continuous Learning Scheduler
Runs periodic training when new sessions accumulate

Triggered by cron or can be run manually
"""

import sys
from pathlib import Path

# Add Memory_Mesh to path
MEMORY_MESH = Path("/home/sir-v/MiRA/Memory_Mesh")
sys.path.insert(0, str(MEMORY_MESH))

from weaver import WeaveOrchestrator
from datetime import datetime


def main():
    print(f"\n🤖 MIRA Continuous Learning - {datetime.now().isoformat()}")
    print("=" * 60)

    orchestrator = WeaveOrchestrator()

    # Check if training is needed
    check = orchestrator.continuous_learning_check()

    if check.get("needs_training"):
        print("\n🚀 Starting continuous learning cycle...")

        # Train Weave models
        print("\n[1/2] Training Weave models...")
        weave_result = orchestrator.run_training(epochs=5)  # Quick training

        # Train MIRA-OJ models
        print("\n[2/2] Training MIRA-OJ persona models...")
        miraoj_result = orchestrator.run_miraoj_training()

        print("\n✅ Continuous learning complete!")
        print(f"   Timestamp: {datetime.now().isoformat()}")

        # Save training timestamp
        save_training_timestamp()

        return 0
    else:
        print(
            f"\n⏭️  No training needed. {check.get('new_sessions', 0)} sessions < 10 threshold"
        )
        return 0


def save_training_timestamp():
    """Save training timestamp to tracking file."""
    import json

    timestamp_file = Path("/home/sir-v/.mira/last_training.json")
    timestamp_file.parent.mkdir(parents=True, exist_ok=True)

    with open(timestamp_file, "w") as f:
        json.dump(
            {"timestamp": datetime.now().isoformat(), "reason": "continuous_learning"},
            f,
        )


if __name__ == "__main__":
    sys.exit(main())
