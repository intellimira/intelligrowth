#!/usr/bin/env python3
"""
MIRA Autonomous Weave - Main Orchestrator
Coordinates all Weave components for self-sustaining knowledge management

Trigger: On session end + periodic maintenance
"""

import os
import sys
import json
import torch
import torch.nn as nn
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

MEMORY_MESH = Path("/home/sir-v/MiRA/Memory_Mesh")
SESSIONS_PATH = Path("/home/sir-v/MiRA/sessions")
MODELS_PATH = Path("/home/sir-v/.mira/weave_models")
MIRAOJ_MODELS_PATH = Path("/home/sir-v/.mira/miraoj_models")


# ============================================================================
# TRAINED MODEL CLASSES (same as weave_trainer.py)
# ============================================================================


class LinkPredictor(nn.Module):
    """Predicts links between zettels."""

    def __init__(self, embedding_dim: int = 384, hidden_dim: int = 256):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(embedding_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid(),
        )

    def forward(self, z1: torch.Tensor, z2: torch.Tensor) -> torch.Tensor:
        combined = torch.cat([z1, z2], dim=-1)
        return self.encoder(combined)


class ZettelSummarizer(nn.Module):
    """Generates summaries for zettels."""

    def __init__(self, embedding_dim: int = 384, hidden_dim: int = 256):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, embedding_dim),
        )

    def forward(self, embedding: torch.Tensor) -> torch.Tensor:
        return self.encoder(embedding)


class QualityScorer(nn.Module):
    """Predicts zettel quality score."""

    def __init__(self, embedding_dim: int = 384):
        super().__init__()
        self.scorer = nn.Sequential(
            nn.Linear(embedding_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def forward(self, embedding: torch.Tensor) -> torch.Tensor:
        return self.scorer(embedding)


# ============================================================================
# TRAINED MODELS MANAGER
# ============================================================================


class TrainedWeaveModels:
    """
    Loads and manages trained Weave models.

    Models are trained on MIRA_ARCH data (26.6K docs, 39.6M tokens).
    Used for inference during Weave operations.
    """

    def __init__(self):
        self.models_path = MODELS_PATH
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._models = {}
        self._loaded = False
        self._training_stats = self._load_training_stats()

    def _load_training_stats(self) -> Dict:
        """Load training statistics."""
        stats_file = self.models_path / "training_stats.json"
        if stats_file.exists():
            with open(stats_file) as f:
                return json.load(f)
        return {
            "last_trained": None,
            "link_loss": None,
            "summ_loss": None,
            "quality_loss": None,
            "num_docs": 0,
        }

    def load_models(self) -> bool:
        """Load trained models from disk."""
        if self._loaded:
            return True

        try:
            # Link Predictor
            self._models["link_predictor"] = LinkPredictor(384, 256).to(self.device)
            lp_path = self.models_path / "link_predictor.pt"
            if lp_path.exists():
                self._models["link_predictor"].load_state_dict(
                    torch.load(lp_path, map_location=self.device)
                )
                self._models["link_predictor"].eval()
                print(f"   ✅ Loaded: link_predictor.pt")

            # Summarizer
            self._models["summarizer"] = ZettelSummarizer(384, 256).to(self.device)
            sum_path = self.models_path / "summarizer.pt"
            if sum_path.exists():
                self._models["summarizer"].load_state_dict(
                    torch.load(sum_path, map_location=self.device)
                )
                self._models["summarizer"].eval()
                print(f"   ✅ Loaded: summarizer.pt")

            # Quality Scorer
            self._models["quality_scorer"] = QualityScorer(384).to(self.device)
            qs_path = self.models_path / "quality_scorer.pt"
            if qs_path.exists():
                self._models["quality_scorer"].load_state_dict(
                    torch.load(qs_path, map_location=self.device)
                )
                self._models["quality_scorer"].eval()
                print(f"   ✅ Loaded: quality_scorer.pt")

            self._loaded = True
            return True

        except Exception as e:
            print(f"   ❌ Failed to load models: {e}")
            return False

    def predict_link(self, emb1: torch.Tensor, emb2: torch.Tensor) -> float:
        """Predict probability of link between two zettels."""
        if not self._loaded:
            return 0.5

        with torch.no_grad():
            emb1 = emb1.to(self.device)
            emb2 = emb2.to(self.device)
            score = self._models["link_predictor"](emb1, emb2)
            return score.item()

    def score_quality(self, embedding: torch.Tensor) -> float:
        """Score zettel quality 0-1."""
        if not self._loaded:
            return 0.5

        with torch.no_grad():
            embedding = embedding.to(self.device)
            score = self._models["quality_scorer"](embedding)
            return score.item()

    def summarize(self, embedding: torch.Tensor) -> torch.Tensor:
        """Generate summary embedding."""
        if not self._loaded:
            return embedding

        with torch.no_grad():
            embedding = embedding.to(self.device)
            return self._models["summarizer"](embedding)

    def status(self) -> Dict:
        """Get model status."""
        return {
            "loaded": self._loaded,
            "device": str(self.device),
            "models_path": str(self.models_path),
            "training_stats": self._training_stats,
        }


# ============================================================================
# PERSONA MODELS MANAGER
# ============================================================================


class PersonaModels:
    """
    Manages trained persona models for MIRA-OJ.

    Each persona was trained on council decisions and session data.
    """

    PERSONAS = {
        "⚛️": "first_principles",
        "🔬": "scientific",
        "🤔": "philosophical",
        "✨": "creative",
        "⚙️": "pragmatic",
        "🌑": "dark_passenger",
    }

    def __init__(self):
        self.models_path = MIRAOJ_MODELS_PATH
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._models = {}
        self._loaded = False
        self._current_persona = None

    def load_all(self) -> bool:
        """Load all persona models."""
        if self._loaded:
            return True

        try:
            for emoji, name in self.PERSONAS.items():
                model_path = self.models_path / f"persona_{name}.pt"
                if model_path.exists():
                    # Load model weights
                    weights = torch.load(model_path, map_location=self.device)
                    self._models[emoji] = {"weights": weights, "name": name}
                    print(f"   ✅ Loaded: persona_{name}.pt")

            # Load response generator
            resp_path = self.models_path / "response_generator.pt"
            if resp_path.exists():
                self._models["response"] = torch.load(
                    resp_path, map_location=self.device
                )
                print(f"   ✅ Loaded: response_generator.pt")

            self._loaded = True
            return True

        except Exception as e:
            print(f"   ❌ Failed to load persona models: {e}")
            return False

    def set_persona(self, emoji: str) -> bool:
        """Set active persona."""
        if emoji in self.PERSONAS:
            self._current_persona = emoji
            return True
        return False

    def get_current_persona(self) -> Optional[str]:
        """Get current persona emoji."""
        return self._current_persona

    def list_personas(self) -> List[str]:
        """List available personas."""
        return list(self.PERSONAS.keys())

    def status(self) -> Dict:
        """Get persona model status."""
        return {
            "loaded": self._loaded,
            "current": self._current_persona,
            "available": list(self.PERSONAS.keys()),
        }


class WeaveOrchestrator:
    def __init__(self):
        self.memory_mesh = MEMORY_MESH
        self.sessions_path = SESSIONS_PATH
        self.auto_ingest_path = self.memory_mesh / "auto_ingest"
        self.smart_linker_path = self.memory_mesh / "smart_linker"
        self.usage_tracker_path = self.memory_mesh / "usage_tracker"
        self.self_improver_path = self.memory_mesh / "self_improver"
        self.vector_mesh_path = self.memory_mesh / "Vector_Mesh"

        # Trained models
        self.trained_models = TrainedWeaveModels()
        self.persona_models = PersonaModels()
        self._models_loaded = False

    def run_session_sealer(self) -> dict:
        """Run session sealing pipeline."""
        print("\n" + "=" * 60)
        print("🔍 PHASE 1: Session Sealing")
        print("=" * 60)

        try:
            sys.path.insert(0, str(self.auto_ingest_path))
            from session_sealer import SessionSealer

            sealer = SessionSealer()
            result = sealer.seal_all()

            return result
        except Exception as e:
            print(f"❌ Session Sealer error: {e}")
            return {"sealed": 0, "skipped": 0}

    def run_vector_index(self) -> dict:
        """Run Vector_Mesh indexing."""
        print("\n" + "=" * 60)
        print("🔍 PHASE 2: Vector Indexing")
        print("=" * 60)

        try:
            sys.path.insert(0, str(self.vector_mesh_path))
            import index

            result = index.index_all()

            return result if result else {"indexed": 0, "skipped": 0}
        except Exception as e:
            print(f"❌ Vector Index error: {e}")
            return {"indexed": 0, "skipped": 0}

    def run_smart_linker(self) -> dict:
        """Run smart linking pipeline."""
        print("\n" + "=" * 60)
        print("🔍 PHASE 3: Smart Linking")
        print("=" * 60)

        try:
            sys.path.insert(0, str(self.smart_linker_path))
            from relationship_finder import SmartLinker

            linker = SmartLinker()
            result = linker.link_all()

            return result
        except Exception as e:
            print(f"❌ Smart Linker error: {e}")
            return {"zettels": 0, "relationships": 0}

    def load_models(self) -> dict:
        """Load trained models."""
        print("\n" + "=" * 60)
        print("📦 Loading Trained Models")
        print("=" * 60)

        results = {"weave": False, "persona": False}

        # Load Weave models
        print("\n[Weave Models]")
        results["weave"] = self.trained_models.load_models()

        # Load Persona models
        print("\n[Persona Models]")
        results["persona"] = self.persona_models.load_all()

        self._models_loaded = results["weave"] and results["persona"]

        return results

    def run_training(self, epochs: int = 10) -> dict:
        """Run Weave training on new data."""
        print("\n" + "=" * 60)
        print("🎓 Weave Training Phase")
        print("=" * 60)

        try:
            # Import trainer
            sys.path.insert(0, str(self.memory_mesh))
            from weave_trainer import WeaveTrainer, TrainingConfig

            config = TrainingConfig(epochs=epochs)
            trainer = WeaveTrainer(config)

            # Run training
            result = trainer.train()

            print("\n✅ Training complete!")
            link_loss = (
                result.get("link_prediction", [0])[-1]
                if result.get("link_prediction")
                else 0
            )
            summ_loss = (
                result.get("summarization", [0])[-1]
                if result.get("summarization")
                else 0
            )
            quality_loss = (
                result.get("quality_scoring", [0])[-1]
                if result.get("quality_scoring")
                else 0
            )
            print(f"   Link Loss: {link_loss:.4f}")
            print(f"   Summ Loss: {summ_loss:.4f}")
            print(f"   Quality Loss: {quality_loss:.4f}")

            # Reload models
            self.trained_models._loaded = False
            self.load_models()

            return result

        except Exception as e:
            print(f"❌ Training failed: {e}")
            return {"error": str(e)}

    def run_miraoj_training(self) -> dict:
        """Run MIRA-OJ persona training."""
        print("\n" + "=" * 60)
        print("🎓 MIRA-OJ Persona Training")
        print("=" * 60)

        try:
            sys.path.insert(0, str(self.memory_mesh))
            from miraoj_trainer import MIRAOJTrainer

            trainer = MIRAOJTrainer()

            result = trainer.train()

            print("\n✅ MIRA-OJ Training complete!")
            response_loss = (
                result.get("response_generation", [0])[-1]
                if result.get("response_generation")
                else 0
            )
            print(f"   Response Loss: {response_loss:.4f}")

            # Reload models
            self.persona_models._loaded = False
            self.load_models()

            return result

        except Exception as e:
            print(f"❌ MIRA-OJ Training failed: {e}")
            return {"error": str(e)}

    def continuous_learning_check(self) -> dict:
        """
        Check if new data requires retraining.

        Continuous Learning Pipeline:
        1. Check for new sessions since last training
        2. If threshold reached, trigger training
        3. Update training stats
        """
        print("\n" + "=" * 60)
        print("🔄 Continuous Learning Check")
        print("=" * 60)

        threshold = 10  # Retrain after 10 new sessions

        # Check for new sessions
        new_sessions = list(self.sessions_path.glob("ses_*.md"))
        last_trained = self.trained_models._training_stats.get("last_trained")

        new_count = len(new_sessions)

        print(f"   Total sessions: {new_count}")
        print(f"   Last trained: {last_trained or 'Never'}")
        print(f"   Threshold: {threshold}")

        if new_count >= threshold:
            print(f"\n   📈 New sessions >= {threshold}!")
            print("   Run 'python weaver.py --train' to retrain")
            return {"needs_training": True, "new_sessions": new_count}

        return {"needs_training": False, "new_sessions": new_count}

    def run_self_improver(self) -> dict:
        """Run self-improvement analysis."""
        print("\n" + "=" * 60)
        print("🔍 PHASE 4: Self-Improvement Analysis")
        print("=" * 60)

        try:
            sys.path.insert(0, str(self.self_improver_path))
            from suggestions import SelfImprover

            improver = SelfImprover()
            suggestions = improver.run(display=True)

            return suggestions
        except Exception as e:
            print(f"❌ Self-Improver error: {e}")
            return {}

    def run_full_cycle(self) -> dict:
        """Run complete Weave cycle."""
        print("\n" + "=" * 60)
        print("🧠 MIRA AUTONOMOUS WEAVE - FULL CYCLE")
        print(f"⏰ Started: {datetime.now().isoformat()}")
        print("=" * 60)

        results = {
            "session_sealer": self.run_session_sealer(),
            "vector_index": self.run_vector_index(),
            "smart_linker": self.run_smart_linker(),
            "timestamp": datetime.now().isoformat(),
        }

        print("\n" + "=" * 60)
        print("📊 CYCLE SUMMARY")
        print("=" * 60)
        sealed = results["session_sealer"].get("sealed", 0)
        vector_result = results["vector_index"]
        indexed = (
            vector_result[0]
            if isinstance(vector_result, tuple)
            else vector_result.get("indexed", 0)
        )
        relationships = results["smart_linker"].get("relationships", 0)
        print(f"   Sessions sealed: {sealed}")
        print(f"   Zettels indexed: {indexed}")
        print(f"   Relationships: {relationships}")

        print("\n💡 Run self-improve for suggestions:")
        print("   python weaver.py --suggest")

        return results

    def run_suggestions_only(self):
        """Run only self-improvement analysis."""
        self.run_self_improver()

    def status(self) -> dict:
        """Get current Weave status."""
        status = {"timestamp": datetime.now().isoformat(), "components": {}}

        vector_db = self.vector_mesh_path / "vectors.db"
        if vector_db.exists():
            import sqlite3

            conn = sqlite3.connect(str(vector_db))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM zettels")
            zettel_count = cursor.fetchone()[0]
            conn.close()
            status["components"]["Vector_Mesh"] = f"{zettel_count} zettels indexed"
        else:
            status["components"]["Vector_Mesh"] = "Not initialized"

        graph_db = self.smart_linker_path / "graph.db"
        if graph_db.exists():
            import sqlite3

            conn = sqlite3.connect(str(graph_db))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links")
            link_count = cursor.fetchone()[0]
            conn.close()
            status["components"]["Smart_Linker"] = f"{link_count} relationships"
        else:
            status["components"]["Smart_Linker"] = "Not initialized"

        tracker_db = self.usage_tracker_path / "tracker.db"
        if tracker_db.exists():
            import sqlite3

            conn = sqlite3.connect(str(tracker_db))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM queries")
            query_count = cursor.fetchone()[0]
            conn.close()
            status["components"]["Usage_Tracker"] = f"{query_count} queries logged"
        else:
            status["components"]["Usage_Tracker"] = "Not initialized"

        sessions = list(self.sessions_path.glob("ses_*.md"))
        status["pending_sessions"] = len(sessions)

        # Add trained models status
        models_path = Path("/home/sir-v/.mira/weave_models")
        if models_path.exists():
            models = list(models_path.glob("*.pt"))
            status["components"]["Trained_Models"] = f"{len(models)} models loaded"
            status["trained_models"] = True
        else:
            status["components"]["Trained_Models"] = "Not trained"
            status["trained_models"] = False

        return status


def main():
    orchestrator = WeaveOrchestrator()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--full" or command == "-f":
            orchestrator.run_full_cycle()

        elif command == "--suggest" or command == "-s":
            orchestrator.run_suggestions_only()

        elif command == "--status":
            status = orchestrator.status()
            print("\n🧠 MIRA Autonomous Weave Status")
            print("=" * 50)
            for component, info in status["components"].items():
                print(f"   {component}: {info}")
            print(
                f"\n   Trained Models: {'✅ Loaded' if status.get('trained_models') else '❌ Not trained'}"
            )
            print(f"   Pending sessions: {status['pending_sessions']}")
            print(f"   Last checked: {status['timestamp']}")

        elif command == "--sealer":
            orchestrator.run_session_sealer()

        elif command == "--index":
            orchestrator.run_vector_index()

        elif command == "--link":
            orchestrator.run_smart_linker()

        elif command == "--load":
            orchestrator.load_models()

        elif command == "--train" or command == "-t":
            epochs = 10
            if len(sys.argv) > 2:
                try:
                    epochs = int(sys.argv[2])
                except:
                    pass
            orchestrator.run_training(epochs=epochs)

        elif command == "--train-miraoj":
            orchestrator.run_miraoj_training()

        elif command == "--train-all":
            orchestrator.run_training(epochs=10)
            orchestrator.run_miraoj_training()

        elif command == "--continuous":
            orchestrator.continuous_learning_check()

        elif command == "--help":
            print("""
🧠 MIRA Autonomous Weave Orchestrator

Usage: python weaver.py [command]

Weave Cycle Commands:
  --full, -f       Run complete Weave cycle (seal, index, link)
  --sealer         Run session sealing only
  --index          Run Vector_Mesh indexing only
  --link           Run smart linking only

Training Commands:
  --load           Load trained models
  --train, -t      Train Weave models (default 10 epochs)
  --train [n]      Train with n epochs
  --train-miraoj   Train MIRA-OJ persona models
  --train-all      Train both Weave and MIRA-OJ
  --continuous     Check if retraining needed

Other:
  --suggest, -s    Run self-improvement analysis
  --status         Show Weave status
  --help           Show this help

Examples:
  python weaver.py --full           # Full cycle
  python weaver.py --status         # Check status
  python weaver.py --train 20       # Train 20 epochs
  python weaver.py --train-all      # Full training
  python weaver.py --continuous     # Check if retraining needed
            """)
        else:
            print(f"Unknown command: {command}")
            print("Run --help for usage")

    else:
        print("🧠 MIRA Autonomous Weave")
        print("=" * 50)
        print("Run with --help for usage")
        print("Run with --status for current status")


if __name__ == "__main__":
    main()
