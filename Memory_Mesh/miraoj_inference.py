#!/usr/bin/env python3
"""
MIRA-OJ Inference Engine
Uses trained models for enhanced response generation

Features:
- Trained Weave model inference
- Persona-aware response weighting
- Quality scoring
- Link prediction for context
"""

import os
import sys
import torch
import torch.nn as nn
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Add to path
MEMORY_MESH = Path("/home/sir-v/MiRA/Memory_Mesh")
sys.path.insert(0, str(MEMORY_MESH))


class InferenceEngine:
    """
    MIRA-OJ Inference Engine using trained models.

    Loads trained weights and provides inference capabilities.
    """

    def __init__(self):
        self.models_path = Path("/home/sir-v/.mira")
        self.weave_models_path = self.models_path / "weave_models"
        self.miraoj_models_path = self.models_path / "miraoj_models"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self._models = {}
        self._loaded = False

        # Persona mappings
        self.PERSONAS = {
            "⚛️": "first_principles",
            "🔬": "scientific",
            "🤔": "philosophical",
            "✨": "creative",
            "⚙️": "pragmatic",
            "🌑": "dark_passenger",
        }

    def load_models(self) -> bool:
        """Load all trained models."""
        if self._loaded:
            return True

        print("Loading MIRA-OJ Inference Engine...")

        try:
            # Import model classes
            from weaver import LinkPredictor, ZettelSummarizer, QualityScorer

            # Load Weave models
            print("  [Weave Models]")

            self._models["link_predictor"] = LinkPredictor(384, 256).to(self.device)
            lp_path = self.weave_models_path / "link_predictor.pt"
            if lp_path.exists():
                self._models["link_predictor"].load_state_dict(
                    torch.load(lp_path, map_location=self.device)
                )
                self._models["link_predictor"].eval()
                print(f"    ✅ link_predictor")

            self._models["summarizer"] = ZettelSummarizer(384, 256).to(self.device)
            sm_path = self.weave_models_path / "summarizer.pt"
            if sm_path.exists():
                self._models["summarizer"].load_state_dict(
                    torch.load(sm_path, map_location=self.device)
                )
                self._models["summarizer"].eval()
                print(f"    ✅ summarizer")

            self._models["quality_scorer"] = QualityScorer(384).to(self.device)
            qs_path = self.weave_models_path / "quality_scorer.pt"
            if qs_path.exists():
                self._models["quality_scorer"].load_state_dict(
                    torch.load(qs_path, map_location=self.device)
                )
                self._models["quality_scorer"].eval()
                print(f"    ✅ quality_scorer")

            # Load Persona models
            print("  [Persona Models]")
            for emoji, name in self.PERSONAS.items():
                model_path = self.miraoj_models_path / f"persona_{name}.pt"
                if model_path.exists():
                    weights = torch.load(model_path, map_location=self.device)
                    self._models[f"persona_{name}"] = weights
                    print(f"    ✅ {emoji} {name}")

            # Response generator
            resp_path = self.miraoj_models_path / "response_generator.pt"
            if resp_path.exists():
                self._models["response_generator"] = torch.load(
                    resp_path, map_location=self.device
                )
                print(f"    ✅ response_generator")

            self._loaded = True
            print("\n✅ All models loaded!")
            return True

        except Exception as e:
            print(f"\n❌ Failed to load models: {e}")
            return False

    def score_content_quality(self, content_embedding: torch.Tensor) -> float:
        """Score content quality using trained model."""
        if not self._loaded or "quality_scorer" not in self._models:
            return 0.5

        with torch.no_grad():
            emb = content_embedding.to(self.device)
            score = self._models["quality_scorer"](emb.unsqueeze(0))
            return score.item()

    def predict_link_probability(
        self, zettel1_embedding: torch.Tensor, zettel2_embedding: torch.Tensor
    ) -> float:
        """Predict link probability between two zettels."""
        if not self._loaded or "link_predictor" not in self._models:
            return 0.5

        with torch.no_grad():
            z1 = zettel1_embedding.to(self.device)
            z2 = zettel2_embedding.to(self.device)
            prob = self._models["link_predictor"](z1.unsqueeze(0), z2.unsqueeze(0))
            return prob.item()

    def get_summarized_embedding(self, content_embedding: torch.Tensor) -> torch.Tensor:
        """Get summarized embedding using trained model."""
        if not self._loaded or "summarizer" not in self._models:
            return content_embedding

        with torch.no_grad():
            emb = content_embedding.to(self.device)
            summary = self._models["summarizer"](emb.unsqueeze(0))
            return summary.squeeze(0)

    def get_persona_weights(self, emoji: str) -> Optional[Dict]:
        """Get trained persona weights."""
        name = self.PERSONAS.get(emoji)
        if not name:
            return None
        return self._models.get(f"persona_{name}")

    def suggest_links(
        self,
        current_zettel_emb: torch.Tensor,
        candidate_zettels: List[torch.Tensor],
        threshold: float = 0.7,
    ) -> List[Tuple[int, float]]:
        """
        Suggest links to other zettels based on trained model.

        Returns:
            List of (zettel_index, probability) tuples
        """
        suggestions = []

        for i, candidate_emb in enumerate(candidate_zettels):
            prob = self.predict_link_probability(current_zettel_emb, candidate_emb)
            if prob >= threshold:
                suggestions.append((i, prob))

        # Sort by probability
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions

    def rank_context_by_quality(
        self, context_embeddings: List[torch.Tensor]
    ) -> List[Tuple[int, float]]:
        """
        Rank context by quality score.

        Returns:
            List of (context_index, quality_score) tuples
        """
        rankings = []

        for i, emb in enumerate(context_embeddings):
            score = self.score_content_quality(emb)
            rankings.append((i, score))

        # Sort by quality
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings


class MiraOJInference:
    """
    High-level MIRA-OJ inference interface.

    Combines all trained models for enhanced responses.
    """

    def __init__(self):
        self.engine = InferenceEngine()
        self.engine.load_models()

        # Current persona
        self._current_persona = None
        self._load_persona_state()

    def _load_persona_state(self):
        """Load persisted persona state."""
        state_file = Path("/home/sir-v/.mira/persona_state.json")
        if state_file.exists():
            import json

            with open(state_file) as f:
                state = json.load(f)
                self._current_persona = state.get("current_persona")

    def set_persona(self, emoji: str):
        """Set active persona."""
        if emoji in self.engine.PERSONAS:
            self._current_persona = emoji
            return True
        return False

    def get_current_persona(self) -> Optional[str]:
        """Get current persona emoji."""
        return self._current_persona

    def enhance_response(
        self,
        query: str,
        base_response: str,
        context_embeddings: List[torch.Tensor] = None,
    ) -> Dict:
        """
        Enhance response using trained models.

        Args:
            query: User query
            base_response: Base response to enhance
            context_embeddings: Optional context embeddings

        Returns:
            Enhancement analysis
        """
        result = {
            "query": query,
            "base_response_length": len(base_response),
            "persona": self._current_persona,
            "quality_score": 0.5,
            "suggested_improvements": [],
            "context_ranking": [],
        }

        if not self.engine._loaded:
            return result

        # Analyze quality
        if context_embeddings:
            # Score context
            rankings = self.engine.rank_context_by_quality(context_embeddings)
            result["context_ranking"] = rankings[:5]

            # Get top quality
            if rankings:
                result["quality_score"] = rankings[0][1]

        # Persona analysis
        if self._current_persona:
            weights = self.engine.get_persona_weights(self._current_persona)
            if weights:
                result["persona_active"] = True
                result["persona_weights_loaded"] = True

        return result

    def get_inference_stats(self) -> Dict:
        """Get inference engine statistics."""
        return {
            "models_loaded": self.engine._loaded,
            "current_persona": self._current_persona,
            "available_personas": list(self.engine.PERSONAS.keys()),
            "device": str(self.engine.device),
            "models": {"weave": list(self.engine._models.keys())},
        }


def main():
    """Demo and test the inference engine."""
    print("=" * 60)
    print("🎯 MIRA-OJ Inference Engine Demo")
    print("=" * 60)

    inference = MiraOJInference()

    # Get stats
    stats = inference.get_inference_stats()
    print("\n📊 Inference Stats:")
    print(f"   Models loaded: {stats['models_loaded']}")
    print(f"   Device: {stats['device']}")
    print(f"   Current persona: {stats['current_persona'] or 'None'}")

    # Demo enhancement
    print("\n🔍 Demo Enhancement:")
    result = inference.enhance_response(
        query="What is quantum computing?",
        base_response="Quantum computing uses quantum mechanics...",
        context_embeddings=[torch.randn(384) for _ in range(3)],
    )
    print(f"   Quality Score: {result['quality_score']:.4f}")
    print(f"   Response Length: {result['base_response_length']}")


if __name__ == "__main__":
    main()
