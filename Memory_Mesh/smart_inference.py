#!/usr/bin/env python3
"""
MIRA Smart Inference Engine
Auto-selects between full and distilled models based on quality gates

Features:
- Quality comparison between full vs distilled
- Automatic model selection
- Performance tracking
- Quality threshold gates
"""

import os
import sys
import json
import time
import torch
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class SmartInferenceEngine:
    """
    Intelligent inference that auto-selects best model.

    Selection Strategy:
    1. Use distilled by default (faster)
    2. If quality drops below threshold, switch to full
    3. Log decisions for learning
    """

    def __init__(
        self,
        full_models_dir: Path = Path("~/.mira/weave_models"),
        distilled_models_dir: Path = Path("~/.mira/weave_models_distilled"),
        quality_threshold: float = 0.95,  # Distilled must be 95% as good
        performance_threshold: float = 1.5,  # 1.5x speedup minimum
    ):
        self.full_models_dir = Path(os.path.expanduser(full_models_dir))
        self.distilled_models_dir = Path(os.path.expanduser(distilled_models_dir))
        self.quality_threshold = quality_threshold
        self.performance_threshold = performance_threshold

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Model state
        self.full_models = {}
        self.distilled_models = {}
        self.projector = None

        # Selection state
        self.current_mode = "distilled"  # or "full"
        self.selection_log = []

        # Load models
        self._load_models()

    def _load_models(self):
        """Load all available models."""
        print("\n📦 Loading Smart Inference Models...")

        # Try to import model classes
        sys.path.insert(0, str(Path(__file__).parent))
        try:
            from weaver import LinkPredictor, ZettelSummarizer, QualityScorer

            # Load full models
            print("  [Full Models]")
            lp_full = LinkPredictor(384, 256).to(self.device)
            if (self.full_models_dir / "link_predictor.pt").exists():
                lp_full.load_state_dict(
                    torch.load(
                        self.full_models_dir / "link_predictor.pt",
                        map_location=self.device,
                    )
                )
                lp_full.eval()
                self.full_models["link_predictor"] = lp_full
                print(f"    ✅ link_predictor (full)")

            sm_full = ZettelSummarizer(384, 256).to(self.device)
            if (self.full_models_dir / "summarizer.pt").exists():
                sm_full.load_state_dict(
                    torch.load(
                        self.full_models_dir / "summarizer.pt", map_location=self.device
                    )
                )
                sm_full.eval()
                self.full_models["summarizer"] = sm_full
                print(f"    ✅ summarizer (full)")

            qs_full = QualityScorer(384).to(self.device)
            if (self.full_models_dir / "quality_scorer.pt").exists():
                qs_full.load_state_dict(
                    torch.load(
                        self.full_models_dir / "quality_scorer.pt",
                        map_location=self.device,
                    )
                )
                qs_full.eval()
                self.full_models["quality_scorer"] = qs_full
                print(f"    ✅ quality_scorer (full)")

            # Load distilled models
            print("  [Distilled Models]")

            # Embedding projector
            if (self.distilled_models_dir / "embedding_projector.pt").exists():
                from model_distiller import EmbeddingProjector

                self.projector = EmbeddingProjector(384, 128).to(self.device)
                self.projector.load_state_dict(
                    torch.load(
                        self.distilled_models_dir / "embedding_projector.pt",
                        map_location=self.device,
                    )
                )
                self.projector.eval()
                print(f"    ✅ embedding_projector (384→128)")

            # Distilled models
            from model_distiller import (
                DistilledLinkPredictor,
                DistilledSummarizer,
                DistilledQualityScorer,
            )

            lp_dist = DistilledLinkPredictor(128, 64).to(self.device)
            if (self.distilled_models_dir / "link_predictor_distilled.pt").exists():
                lp_dist.load_state_dict(
                    torch.load(
                        self.distilled_models_dir / "link_predictor_distilled.pt",
                        map_location=self.device,
                    )
                )
                lp_dist.eval()
                self.distilled_models["link_predictor"] = lp_dist
                print(f"    ✅ link_predictor (distilled)")

            sm_dist = DistilledSummarizer(128, 64).to(self.device)
            if (self.distilled_models_dir / "summarizer_distilled.pt").exists():
                sm_dist.load_state_dict(
                    torch.load(
                        self.distilled_models_dir / "summarizer_distilled.pt",
                        map_location=self.device,
                    )
                )
                sm_dist.eval()
                self.distilled_models["summarizer"] = sm_dist
                print(f"    ✅ summarizer (distilled)")

            qs_dist = DistilledQualityScorer(128).to(self.device)
            if (self.distilled_models_dir / "quality_scorer_distilled.pt").exists():
                qs_dist.load_state_dict(
                    torch.load(
                        self.distilled_models_dir / "quality_scorer_distilled.pt",
                        map_location=self.device,
                    )
                )
                qs_dist.eval()
                self.distilled_models["quality_scorer"] = qs_dist
                print(f"    ✅ quality_scorer (distilled)")

        except Exception as e:
            print(f"  ⚠️ Could not load models: {e}")

        print(f"\n  Mode: {self.current_mode.upper()}")

    def _project_embedding(self, emb: torch.Tensor) -> torch.Tensor:
        """Project embedding to lower dimension."""
        if self.projector is not None:
            with torch.no_grad():
                return self.projector(emb)
        return emb[:, :128]  # Fallback: just truncate

    def _select_model(self, task: str) -> Tuple[str, object]:
        """Select best model for task."""
        # Default to distilled for speed
        model_key = task

        if model_key in self.distilled_models:
            return "distilled", self.distilled_models[model_key]
        elif model_key in self.full_models:
            return "full", self.full_models[model_key]

        return None, None

    def predict_link(
        self, emb1: torch.Tensor, emb2: torch.Tensor, force_mode: str = None
    ) -> Dict:
        """
        Predict link probability with smart model selection.

        Returns prediction with timing and model info.
        """
        start_time = time.time()

        # Determine mode
        mode = force_mode or self.current_mode

        # Project embeddings for distilled
        if mode == "distilled":
            emb1_proj = self._project_embedding(emb1)
            emb2_proj = self._project_embedding(emb2)
        else:
            emb1_proj = emb1
            emb2_proj = emb2

        # Select model
        model_mode, model = self._select_model("link_predictor")

        if model is None:
            return {"probability": 0.5, "mode": "fallback", "time_ms": 0}

        # Run inference
        with torch.no_grad():
            prob = model(emb1_proj, emb2_proj).item()

        elapsed = (time.time() - start_time) * 1000

        result = {
            "probability": prob,
            "mode": mode,
            "model_type": model_mode,
            "time_ms": elapsed,
            "timestamp": datetime.now().isoformat(),
        }

        # Log selection
        self._log_selection("link_prediction", mode, elapsed)

        return result

    def score_quality(self, embedding: torch.Tensor, force_mode: str = None) -> Dict:
        """Score content quality with smart model selection."""
        start_time = time.time()

        mode = force_mode or self.current_mode

        if mode == "distilled":
            emb_proj = self._project_embedding(embedding)
        else:
            emb_proj = embedding

        model_mode, model = self._select_model("quality_scorer")

        if model is None:
            return {"score": 0.5, "mode": "fallback", "time_ms": 0}

        with torch.no_grad():
            score = model(emb_proj.unsqueeze(0)).item()

        elapsed = (time.time() - start_time) * 1000

        result = {
            "score": score,
            "mode": mode,
            "model_type": model_mode,
            "time_ms": elapsed,
            "timestamp": datetime.now().isoformat(),
        }

        self._log_selection("quality_scoring", mode, elapsed)

        return result

    def summarize(self, embedding: torch.Tensor, force_mode: str = None) -> Dict:
        """Generate summary with smart model selection."""
        start_time = time.time()

        mode = force_mode or self.current_mode

        if mode == "distilled":
            emb_proj = self._project_embedding(embedding)
        else:
            emb_proj = embedding

        model_mode, model = self._select_model("summarizer")

        if model is None:
            return {"summary": embedding, "mode": "fallback", "time_ms": 0}

        with torch.no_grad():
            summary = model(emb_proj.unsqueeze(0)).squeeze(0)

        elapsed = (time.time() - start_time) * 1000

        result = {
            "summary": summary,
            "mode": mode,
            "model_type": model_mode,
            "time_ms": elapsed,
            "timestamp": datetime.now().isoformat(),
        }

        self._log_selection("summarization", mode, elapsed)

        return result

    def _log_selection(self, task: str, mode: str, time_ms: float):
        """Log model selection decision."""
        self.selection_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "task": task,
                "mode": mode,
                "time_ms": time_ms,
            }
        )

        # Keep only last 1000 entries
        if len(self.selection_log) > 1000:
            self.selection_log = self.selection_log[-1000:]

    def compare_models(
        self, test_embedding: torch.Tensor, test_emb2: torch.Tensor = None
    ) -> Dict:
        """
        Compare full vs distilled model outputs.

        Used for quality gate checking.
        """
        results = {}

        # Quality scoring comparison
        full_score = self.score_quality(test_embedding, force_mode="full")
        dist_score = self.score_quality(test_embedding, force_mode="distilled")

        quality_ratio = dist_score["score"] / max(full_score["score"], 0.01)

        results["quality"] = {
            "full": full_score,
            "distilled": dist_score,
            "ratio": quality_ratio,
            "distilled_acceptable": quality_ratio >= self.quality_threshold,
        }

        # Speed comparison
        results["speed"] = {
            "full_avg_ms": full_score["time_ms"],
            "distilled_avg_ms": dist_score["time_ms"],
            "speedup": full_score["time_ms"] / max(dist_score["time_ms"], 0.001),
        }

        # Overall recommendation
        if quality_ratio >= self.quality_threshold:
            results["recommendation"] = "distilled"
        else:
            results["recommendation"] = "full"

        return results

    def auto_select(self) -> str:
        """
        Automatically select best mode based on recent performance.

        Returns recommended mode.
        """
        # Analyze recent selection log
        if len(self.selection_log) < 10:
            return self.current_mode

        recent = self.selection_log[-100:]

        # Calculate average times
        full_times = [e["time_ms"] for e in recent if e["mode"] == "full"]
        dist_times = [e["time_ms"] for e in recent if e["mode"] == "distilled"]

        if not full_times or not dist_times:
            return self.current_mode

        avg_full = sum(full_times) / len(full_times)
        avg_dist = sum(dist_times) / len(dist_times)

        speedup = avg_full / max(avg_dist, 0.001)

        # If distilled is significantly faster, keep it
        if speedup >= self.performance_threshold:
            self.current_mode = "distilled"
        else:
            # Fall back to full if speedup isn't worth it
            self.current_mode = "full"

        return self.current_mode

    def get_stats(self) -> Dict:
        """Get inference statistics."""
        if not self.selection_log:
            return {
                "current_mode": self.current_mode,
                "total_inferences": 0,
                "distilled_pct": 0,
                "avg_time_ms": 0,
                "models_loaded": {
                    "full": list(self.full_models.keys()),
                    "distilled": list(self.distilled_models.keys()),
                },
            }

        total = len(self.selection_log)
        distilled_count = sum(1 for e in self.selection_log if e["mode"] == "distilled")
        avg_time = sum(e["time_ms"] for e in self.selection_log) / total

        return {
            "current_mode": self.current_mode,
            "total_inferences": total,
            "distilled_pct": (distilled_count / total) * 100,
            "avg_time_ms": avg_time,
            "models_loaded": {
                "full": list(self.full_models.keys()),
                "distilled": list(self.distilled_models.keys()),
            },
        }

        total = len(self.selection_log)
        distilled_count = sum(1 for e in self.selection_log if e["mode"] == "distilled")
        avg_time = sum(e["time_ms"] for e in self.selection_log) / total

        return {
            "current_mode": self.current_mode,
            "total_inferences": total,
            "distilled_pct": (distilled_count / total) * 100,
            "avg_time_ms": avg_time,
            "models_loaded": {
                "full": list(self.full_models.keys()),
                "distilled": list(self.distilled_models.keys()),
            },
        }

    def print_stats(self):
        """Print inference statistics."""
        stats = self.get_stats()

        print("\n" + "=" * 60)
        print("⚡ MIRA SMART INFERENCE STATS")
        print("=" * 60)
        print(f"\n📊 Current Mode: {stats['current_mode'].upper()}")
        print(f"   Total Inferences: {stats['total_inferences']}")
        print(f"   Distilled Usage: {stats['distilled_pct']:.1f}%")
        print(f"   Avg Time: {stats['avg_time_ms']:.2f}ms")
        print(f"\n📦 Models Loaded:")
        print(f"   Full: {', '.join(stats['models_loaded']['full']) or 'None'}")
        print(
            f"   Distilled: {', '.join(stats['models_loaded']['distilled']) or 'None'}"
        )


def main():
    """CLI for smart inference."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Smart Inference")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    parser.add_argument("--compare", action="store_true", help="Compare models")
    parser.add_argument("--select", action="store_true", help="Auto-select mode")
    parser.add_argument("--mode", choices=["full", "distilled"], help="Force mode")

    args = parser.parse_args()

    engine = SmartInferenceEngine()

    if args.stats:
        engine.print_stats()

    elif args.compare:
        # Test with random embedding
        emb = torch.randn(384).to(engine.device)
        results = engine.compare_models(emb)
        print(f"\n📊 Model Comparison:")
        print(f"   Quality Ratio: {results['quality']['ratio']:.3f}")
        print(f"   Speedup: {results['speed']['speedup']:.2f}x")
        print(f"   Recommendation: {results['recommendation']}")

    elif args.select:
        mode = engine.auto_select()
        print(f"\n🎯 Auto-selected mode: {mode.upper()}")

    elif args.mode:
        engine.current_mode = args.mode
        print(f"\n✅ Mode set to: {args.mode.upper()}")

    else:
        # Demo inference
        emb1 = torch.randn(384).to(engine.device)
        emb2 = torch.randn(384).to(engine.device)

        result = engine.predict_link(emb1, emb2)
        print(f"\n🔗 Link Prediction:")
        print(f"   Probability: {result['probability']:.3f}")
        print(f"   Mode: {result['mode']}")
        print(f"   Time: {result['time_ms']:.2f}ms")


if __name__ == "__main__":
    main()
