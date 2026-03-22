#!/usr/bin/env python3
"""
MIRA Active Learning & Cross-Session Memory
- Active learning: Query user for uncertain predictions
- Cross-session: Checkpoint and continue training
"""

import os
import json
import torch
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import numpy as np


class ActiveLearner:
    """
    Active learning for MIRA.

    Identifies uncertain predictions and queries user for labels.
    """

    def __init__(self, uncertainty_threshold: float = 0.1, min_samples: int = 5):
        self.uncertainty_threshold = uncertainty_threshold
        self.min_samples = min_samples
        self.uncertain_predictions = []
        self.labeled_samples = []

    def add_prediction(
        self,
        query: str,
        context: str,
        prediction: float,
        confidence: float,
        metadata: Dict = None,
    ):
        """
        Add a prediction for active learning evaluation.

        Args:
            query: User query
            context: Context used for prediction
            prediction: Model prediction
            confidence: Model confidence (0-1)
            metadata: Additional metadata
        """
        # Calculate uncertainty
        uncertainty = 1.0 - confidence

        if uncertainty > self.uncertainty_threshold:
            self.uncertain_predictions.append(
                {
                    "query": query,
                    "context": context,
                    "prediction": prediction,
                    "confidence": confidence,
                    "uncertainty": uncertainty,
                    "timestamp": datetime.now().isoformat(),
                    "metadata": metadata or {},
                }
            )

    def get_queries_for_labeling(self, n: int = 5) -> List[Dict]:
        """
        Get the most uncertain predictions for user labeling.

        Returns top n predictions sorted by uncertainty.
        """
        # Sort by uncertainty
        sorted_preds = sorted(
            self.uncertain_predictions, key=lambda x: x["uncertainty"], reverse=True
        )

        return sorted_preds[:n]

    def add_label(self, query: str, correct_answer: str, is_correct: bool):
        """Add user label for a prediction."""
        self.labeled_samples.append(
            {
                "query": query,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Remove from uncertain predictions
        self.uncertain_predictions = [
            p for p in self.uncertain_predictions if p["query"] != query
        ]

    def get_training_data(self) -> List[Dict]:
        """Get labeled samples for training."""
        return self.labeled_samples

    def get_stats(self) -> Dict:
        """Get active learning statistics."""
        return {
            "uncertain_predictions": len(self.uncertain_predictions),
            "labeled_samples": len(self.labeled_samples),
            "accuracy": sum(1 for s in self.labeled_samples if s["is_correct"])
            / max(len(self.labeled_samples), 1),
        }


class CrossSessionMemory:
    """
    Cross-session training memory.

    Saves checkpoints and continues training from last state.
    """

    def __init__(
        self,
        checkpoint_dir: Path = Path("~/.mira/checkpoints"),
        models_dir: Path = Path("~/.mira/weave_models"),
    ):
        self.checkpoint_dir = Path(os.path.expanduser(checkpoint_dir))
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir = Path(os.path.expanduser(models_dir))

        self.state_file = self.checkpoint_dir / "training_state.json"
        self._load_state()

    def _load_state(self):
        """Load training state."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                self.state = json.load(f)
        else:
            self.state = self._create_default_state()

    def _create_default_state(self) -> Dict:
        """Create default training state."""
        return {
            "version": 1,
            "created_at": datetime.now().isoformat(),
            "last_training": None,
            "total_trainings": 0,
            "training_history": [],
            "model_versions": {},
            "cumulative_data_count": 0,
            "best_metrics": {
                "link_prediction": None,
                "summarization": None,
                "quality_scoring": None,
            },
        }

    def _save_state(self):
        """Save training state."""
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def save_checkpoint(
        self, model_name: str, model_state: Dict, metrics: Dict, data_count: int
    ):
        """
        Save a training checkpoint.

        Args:
            model_name: Name of the model
            model_state: Model state dict
            metrics: Training metrics
            data_count: Number of training samples used
        """
        timestamp = datetime.now().isoformat()

        # Save checkpoint file
        checkpoint_file = self.checkpoint_dir / f"{model_name}_{timestamp}.pt"
        torch.save(model_state, checkpoint_file)

        # Update state
        self.state["last_training"] = timestamp
        self.state["total_trainings"] += 1
        self.state["cumulative_data_count"] += data_count

        # Record history
        history_entry = {
            "timestamp": timestamp,
            "model": model_name,
            "checkpoint": str(checkpoint_file),
            "metrics": metrics,
            "data_count": data_count,
        }
        self.state["training_history"].append(history_entry)

        # Keep only last 10 checkpoints
        if len(self.state["training_history"]) > 10:
            self.state["training_history"] = self.state["training_history"][-10:]

        # Update best metrics
        for metric_name, value in metrics.items():
            current_best = self.state["best_metrics"].get(metric_name)
            if current_best is None or value < current_best:
                self.state["best_metrics"][metric_name] = value

        # Save model version
        self.state["model_versions"][model_name] = {
            "checkpoint": str(checkpoint_file),
            "timestamp": timestamp,
            "metrics": metrics,
        }

        self._save_state()

        return checkpoint_file

    def load_checkpoint(self, model_name: str) -> Optional[Dict]:
        """
        Load the latest checkpoint for a model.

        Returns model state dict or None.
        """
        if model_name not in self.state["model_versions"]:
            return None

        checkpoint_path = self.state["model_versions"][model_name]["checkpoint"]

        if not Path(checkpoint_path).exists():
            return None

        return torch.load(checkpoint_path)

    def continue_training(self, model_name: str, new_data_count: int) -> bool:
        """
        Check if we should continue training from checkpoint.

        Returns True if checkpoint exists and should be used.
        """
        checkpoint = self.load_checkpoint(model_name)

        if checkpoint is None:
            return False

        # Update state for continued training
        self.state["continuation"] = {
            "model": model_name,
            "checkpoint": self.state["model_versions"][model_name]["checkpoint"],
            "continued_from": datetime.now().isoformat(),
            "new_data_count": new_data_count,
        }

        self._save_state()

        return True

    def get_continuation_info(self) -> Optional[Dict]:
        """Get info about continued training."""
        return self.state.get("continuation")

    def get_improvement_report(self) -> Dict:
        """Generate improvement report comparing versions."""
        history = self.state.get("training_history", [])

        if len(history) < 2:
            return {"message": "Not enough training history"}

        # Compare first and last
        first = history[0]
        last = history[-1]

        improvements = {}
        for metric in ["link_prediction", "summarization", "quality_scoring"]:
            first_val = first.get("metrics", {}).get(metric)
            last_val = last.get("metrics", {}).get(metric)

            if first_val and last_val:
                improvement = (first_val - last_val) / max(first_val, 0.001)
                improvements[metric] = {
                    "first": first_val,
                    "last": last_val,
                    "improvement_pct": improvement * 100,
                }

        return {
            "total_trainings": self.state["total_trainings"],
            "cumulative_data": self.state["cumulative_data_count"],
            "first_training": first.get("timestamp"),
            "last_training": last.get("timestamp"),
            "improvements": improvements,
            "best_metrics": self.state["best_metrics"],
        }

    def get_status(self) -> Dict:
        """Get cross-session memory status."""
        return {
            "total_trainings": self.state["total_trainings"],
            "cumulative_data": self.state["cumulative_data_count"],
            "last_training": self.state["last_training"],
            "models_with_checkpoints": list(self.state["model_versions"].keys()),
            "best_metrics": self.state["best_metrics"],
            "checkpoint_dir": str(self.checkpoint_dir),
        }


class ContinualLearningSystem:
    """
    Combined active learning + cross-session memory.
    """

    def __init__(self):
        self.active_learner = ActiveLearner()
        self.cross_session = CrossSessionMemory()

    def record_interaction(
        self, query: str, context: str, prediction: float, confidence: float
    ):
        """Record interaction for active learning."""
        self.active_learner.add_prediction(query, context, prediction, confidence)

    def query_for_labels(self) -> List[Dict]:
        """Get uncertain predictions for user labeling."""
        return self.active_learner.get_queries_for_labeling()

    def add_label(self, query: str, correct_answer: str, is_correct: bool):
        """Add user label."""
        self.active_learner.add_label(query, correct_answer, is_correct)

    def save_training_checkpoint(
        self, model_name: str, model_state: Dict, metrics: Dict, data_count: int
    ):
        """Save training checkpoint."""
        return self.cross_session.save_checkpoint(
            model_name, model_state, metrics, data_count
        )

    def load_latest_checkpoint(self, model_name: str) -> Optional[Dict]:
        """Load latest checkpoint."""
        return self.cross_session.load_checkpoint(model_name)

    def should_continue_training(self, model_name: str, new_data_count: int) -> bool:
        """Check if should continue from checkpoint."""
        return self.cross_session.continue_training(model_name, new_data_count)

    def get_full_status(self) -> Dict:
        """Get combined status."""
        return {
            "active_learning": self.active_learner.get_stats(),
            "cross_session": self.cross_session.get_status(),
            "continuation_info": self.cross_session.get_improvement_report(),
        }


def main():
    """CLI for continual learning system."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Continual Learning")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument(
        "--queries", action="store_true", help="Get queries for labeling"
    )
    parser.add_argument(
        "--improvement", action="store_true", help="Show improvement report"
    )

    args = parser.parse_args()

    system = ContinualLearningSystem()

    if args.status:
        status = system.get_full_status()
        print("\n📊 Continual Learning Status:")
        print(f"   Active Learning: {status['active_learning']}")
        print(f"   Cross-Session: {status['cross_session']}")

    elif args.queries:
        queries = system.query_for_labels()
        print(f"\n🎯 Queries for Labeling ({len(queries)}):")
        for q in queries:
            print(f"   - {q['query'][:50]}... (uncertainty: {q['uncertainty']:.2f})")

    elif args.improvement:
        report = system.cross_session.get_improvement_report()
        print("\n📈 Improvement Report:")
        print(json.dumps(report, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
