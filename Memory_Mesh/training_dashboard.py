#!/usr/bin/env python3
"""
MIRA Training Dashboard
Real-time visualization of model training and metrics

Features:
- Training progress bars
- Loss curves
- Model comparison
- System stats
"""

import os
import sys
import json
import time
import torch
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class TrainingDashboard:
    """
    Real-time dashboard for MIRA training system.

    Displays:
    - Model status
    - Training history
    - System metrics
    - Progress indicators
    """

    def __init__(self):
        self.models_path = Path("/home/sir-v/.mira")
        self.weave_models = self.models_path / "weave_models"
        self.miraoj_models = self.models_path / "miraoj_models"
        self.evaluation_dir = self.models_path / "evaluation"
        self.training_state = self.models_path / "training_state.json"

        self.colors = {
            "header": "\033[1;36m",  # Cyan
            "success": "\033[0;32m",  # Green
            "warning": "\033[1;33m",  # Yellow
            "error": "\033[0;31m",  # Red
            "info": "\033[0;34m",  # Blue
            "reset": "\033[0m",
        }

    def clear(self):
        """Clear screen."""
        print("\033[2J\033[H", end="")

    def progress_bar(self, value: float, max_value: float, width: int = 40) -> str:
        """Create ASCII progress bar."""
        filled = int((value / max_value) * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {value:.1f}/{max_value}"

    def color(self, text: str, color: str) -> str:
        """Apply color to text."""
        return f"{self.colors.get(color, '')}{text}{self.colors['reset']}"

    def get_model_info(self) -> Dict:
        """Get information about trained models."""
        info = {
            "weave": {},
            "miraoj": {},
            "last_trained": None,
        }

        # Weave models
        if self.weave_models.exists():
            for model_file in self.weave_models.glob("*.pt"):
                stat = model_file.stat()
                info["weave"][model_file.stem] = {
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }

            # Find latest modification
            mod_times = [
                datetime.fromtimestamp(f.stat().st_mtime)
                for f in self.weave_models.glob("*.pt")
            ]
            if mod_times:
                info["last_trained"] = max(mod_times).isoformat()

        # MIRA-OJ models
        if self.miraoj_models.exists():
            for model_file in self.miraoj_models.glob("*.pt"):
                stat = model_file.stat()
                info["miraoj"][model_file.stem] = {
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }

        # Training state
        if self.training_state.exists():
            with open(self.training_state) as f:
                info["training_state"] = json.load(f)

        return info

    def get_training_history(self) -> List[Dict]:
        """Get training history from evaluation results."""
        history = []

        if self.evaluation_dir.exists():
            for eval_file in sorted(self.evaluation_dir.glob("eval_*.json")):
                with open(eval_file) as f:
                    history.append(json.load(f))

        return history[-10:]  # Last 10 evaluations

    def get_system_stats(self) -> Dict:
        """Get system resource statistics."""
        stats = {}

        # GPU
        if torch.cuda.is_available():
            stats["gpu"] = {
                "name": torch.cuda.get_device_name(0),
                "memory_allocated": torch.cuda.memory_allocated() / 1e9,
                "memory_reserved": torch.cuda.memory_reserved() / 1e9,
            }

        # Disk
        import shutil

        total, used, free = shutil.disk_usage("/")
        stats["disk"] = {
            "total_gb": total // (2**30),
            "used_gb": used // (2**30),
            "free_gb": free // (2**30),
        }

        # Models size
        weave_size = (
            sum(f.stat().st_size for f in self.weave_models.glob("*.pt"))
            if self.weave_models.exists()
            else 0
        )
        miraoj_size = (
            sum(f.stat().st_size for f in self.miraoj_models.glob("*.pt"))
            if self.miraoj_models.exists()
            else 0
        )
        stats["models"] = {
            "weave_mb": weave_size / 1e6,
            "miraoj_mb": miraoj_size / 1e6,
            "total_mb": (weave_size + miraoj_size) / 1e6,
        }

        return stats

    def format_size(self, bytes: int) -> str:
        """Format bytes to human readable."""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes < 1024:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024
        return f"{bytes:.1f} TB"

    def render(self):
        """Render the dashboard."""
        self.clear()

        model_info = self.get_model_info()
        history = self.get_training_history()
        stats = self.get_system_stats()

        # Header
        print(self.color("╔" + "═" * 78 + "╗", "header"))
        print(self.color("║" + " MIRA TRAINING DASHBOARD ".center(78) + "║", "header"))
        print(self.color("╠" + "═" * 78 + "╣", "header"))

        # System Stats
        print(self.color("║ SYSTEM", "info"))
        if "gpu" in stats:
            gpu = stats["gpu"]
            print(f"║   GPU: {gpu['name']}")
            print(
                f"║   VRAM: {gpu['memory_allocated']:.2f}GB / {gpu['memory_reserved']:.2f}GB reserved"
            )
        if "disk" in stats:
            disk = stats["disk"]
            print(f"║   Disk: {disk['free_gb']}GB free / {disk['total_gb']}GB total")
        print(self.color("╠" + "═" * 78 + "╣", "header"))

        # Weave Models
        print(self.color("║ WEAVE MODELS", "success"))
        if model_info.get("weave"):
            for name, info in model_info["weave"].items():
                size_str = self.format_size(info["size"])
                print(f"║   {name}: {size_str}")
        else:
            print(self.color("║   No models trained yet", "warning"))
        print(self.color("╠" + "═" * 78 + "╣", "header"))

        # MIRA-OJ Models
        print(self.color("║ MIRA-OJ MODELS", "success"))
        if model_info.get("miraoj"):
            count = len(model_info["miraoj"])
            total_size = sum(m["size"] for m in model_info["miraoj"].values())
            print(f"║   {count} persona models, {self.format_size(total_size)}")
        else:
            print(self.color("║   No models trained yet", "warning"))
        print(self.color("╠" + "═" * 78 + "╣", "header"))

        # Training History
        print(self.color("║ TRAINING HISTORY", "info"))
        if history:
            latest = history[-1]
            timestamp = latest.get("timestamp", "Unknown")
            print(f"║   Last evaluation: {timestamp[:19]}")

            if "link_predictor" in latest:
                lp = latest["link_predictor"]
                f1 = lp.get("f1", 0)
                print(f"║   Link F1: {f1:.4f}")

            if "summarizer" in latest:
                sm = latest["summarizer"]
                sim = sm.get("mean_cosine_similarity", "0")
                try:
                    sim_val = float(sim)
                    print(f"║   Summarizer Cosine: {sim_val:.4f}")
                except (ValueError, TypeError):
                    print(f"║   Summarizer Cosine: {sim}")
        else:
            print(self.color("║   No training history", "warning"))
        print(self.color("╠" + "═" * 78 + "╣", "header"))

        # Commands
        print(self.color("║ COMMANDS", "warning"))
        print("║   python weaver.py --train        Train models")
        print("║   python weaver.py --continuous   Check training need")
        print("║   python model_evaluator.py       Evaluate models")
        print("║   python persona_switcher.py       Switch personas")
        print(self.color("╚" + "═" * 78 + "╝", "header"))

        # Last trained
        if model_info.get("last_trained"):
            print(f"\nLast trained: {model_info['last_trained'][:19]}")

    def run(self, interval: int = 5):
        """Run dashboard with periodic updates."""
        try:
            while True:
                self.render()
                print(f"\nRefreshing in {interval}s... (Ctrl+C to exit)")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\nDashboard closed.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Training Dashboard")
    parser.add_argument("--once", action="store_true", help="Show once and exit")
    parser.add_argument(
        "-i", "--interval", type=int, default=5, help="Refresh interval"
    )

    args = parser.parse_args()

    dashboard = TrainingDashboard()

    if args.once:
        dashboard.render()
    else:
        dashboard.run(interval=args.interval)


if __name__ == "__main__":
    main()
