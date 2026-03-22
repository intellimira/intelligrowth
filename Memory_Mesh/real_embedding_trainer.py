#!/usr/bin/env python3
"""
MIRA Real Embedding Trainer
Trains on real semantic embeddings from Ollama

Key Difference:
- Uses nomic-embed-text for real embeddings
- Learns from actual semantic content
- Much better link prediction and summarization
"""

import os
import sys
import json
import time
import torch
import torch.nn as nn
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime

# Add Memory_Mesh to path
MEMORY_MESH = Path("/home/sir-v/MiRA/Memory_Mesh")
sys.path.insert(0, str(MEMORY_MESH))

# Import embedder
try:
    from ollama_embedder import OllamaEmbedder

    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️ Ollama not available, using fallback embeddings")


# ============================================================================
# MODEL DEFINITIONS (Updated for 768-dim embeddings)
# ============================================================================


class RealLinkPredictor(nn.Module):
    """
    Link prediction using real 768-dim embeddings.

    Input: Two 768-dim embeddings from nomic-embed-text
    Output: Probability of link
    """

    def __init__(self, embedding_dim: int = 768, hidden_dim: int = 256):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(embedding_dim * 2, hidden_dim * 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.BatchNorm1d(hidden_dim * 2),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def forward(self, z1: torch.Tensor, z2: torch.Tensor) -> torch.Tensor:
        combined = torch.cat([z1, z2], dim=-1)
        return self.encoder(combined)


class RealZettelSummarizer(nn.Module):
    """
    Summarization using real embeddings.

    Input: 768-dim embedding
    Output: Summarized embedding (compressed representation)
    """

    def __init__(self, embedding_dim: int = 768, summary_dim: int = 384):
        super().__init__()

        self.compressor = nn.Sequential(
            nn.Linear(embedding_dim, summary_dim * 2),
            nn.ReLU(),
            nn.BatchNorm1d(summary_dim * 2),
            nn.Linear(summary_dim * 2, summary_dim),
            nn.Tanh(),  # Bounded output
        )

    def forward(self, embedding: torch.Tensor) -> torch.Tensor:
        return self.compressor(embedding)


class RealQualityScorer(nn.Module):
    """
    Quality scoring using real embeddings.

    Input: 768-dim embedding
    Output: Quality score 0-1
    """

    def __init__(self, embedding_dim: int = 768):
        super().__init__()

        self.scorer = nn.Sequential(
            nn.Linear(embedding_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.BatchNorm1d(256),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def forward(self, embedding: torch.Tensor) -> torch.Tensor:
        return self.scorer(embedding)


class RealPersonaModel(nn.Module):
    """
    Persona-specific response model using real embeddings.

    Input: Query + Context embeddings
    Output: Persona-weighted response features
    """

    def __init__(self, embedding_dim: int = 768, hidden_dim: int = 256):
        super().__init__()

        self.query_encoder = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
        )

        self.context_encoder = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
        )

        self.fusion = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, embedding_dim),
        )

    def forward(
        self, query_emb: torch.Tensor, context_emb: torch.Tensor
    ) -> torch.Tensor:
        q_encoded = self.query_encoder(query_emb)
        c_encoded = self.context_encoder(context_emb)
        combined = torch.cat([q_encoded, c_encoded], dim=-1)
        return self.fusion(combined)


# ============================================================================
# REAL EMBEDDING TRAINER
# ============================================================================


class RealEmbeddingTrainer:
    """
    Trains models on real Ollama embeddings.

    Key improvements over random embedding training:
    - Real semantic understanding
    - Better link prediction
    - Quality assessment based on content
    """

    def __init__(
        self,
        data_dir: Path = Path("~/MIRA_ARCH_extracted"),
        embed_cache: Path = Path("~/.mira/embeddings"),
        embedding_dim: int = 768,
        batch_size: int = 16,
        learning_rate: float = 0.0001,  # Lower LR for larger embeddings
        epochs: int = 10,
    ):
        self.data_dir = Path(os.path.expanduser(data_dir))
        self.embed_cache = Path(os.path.expanduser(embed_cache))
        self.embedding_dim = embedding_dim
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.epochs = epochs

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Initialize embedder
        if OLLAMA_AVAILABLE:
            self.embedder = OllamaEmbedder()
        else:
            self.embedder = None

        # Models
        self.link_predictor = RealLinkPredictor(embedding_dim).to(self.device)
        self.summarizer = RealZettelSummarizer(embedding_dim).to(self.device)
        self.quality_scorer = RealQualityScorer(embedding_dim).to(self.device)

        # Optimizers
        self.link_optimizer = torch.optim.AdamW(
            self.link_predictor.parameters(), lr=learning_rate
        )
        self.summ_optimizer = torch.optim.AdamW(
            self.summarizer.parameters(), lr=learning_rate
        )
        self.quality_optimizer = torch.optim.AdamW(
            self.quality_scorer.parameters(), lr=learning_rate
        )

        # Metrics
        self.metrics = {
            "link_prediction": [],
            "summarization": [],
            "quality_scoring": [],
            "epochs": 0,
            "start_time": None,
        }

        # Data
        self.training_data = []
        self.embeddings_cache = {}

    def get_embedding(self, text: str, force_refresh: bool = False) -> np.ndarray:
        """
        Get embedding for text, using cache if available.

        Args:
            text: Input text
            force_refresh: Force re-embedding

        Returns:
            768-dim embedding vector
        """
        if self.embedder and not force_refresh:
            emb = self.embedder.embed(text, use_cache=True)
            return np.array(emb, dtype=np.float32)

        # Fallback: return cached or random
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]

        # Generate embedding
        if self.embedder:
            emb = self.embedder.embed(text, use_cache=False)
            self.embeddings_cache[text] = np.array(emb, dtype=np.float32)
            return self.embeddings_cache[text]

        # Random fallback
        return np.random.randn(self.embedding_dim).astype(np.float32)

    def load_data(self) -> Dict:
        """Load training data with embeddings."""
        print("\n" + "=" * 60)
        print("📚 Loading Training Data with Real Embeddings")
        print("=" * 60)

        # Load weave training data
        weave_file = self.data_dir / "weave_training.jsonl"
        if weave_file.exists():
            with open(weave_file) as f:
                lines = f.readlines()[:5000]  # Limit for speed

            print(f"   Loading {len(lines)} documents...")

            for line in lines:
                doc = json.loads(line)
                content = doc.get("content", "")

                if content and len(content) > 50:
                    # Get embedding
                    emb = self.get_embedding(content)

                    self.training_data.append(
                        {
                            "content": content,
                            "embedding": emb,
                            "links": doc.get("links", []),
                            "quality_score": doc.get("quality_score", 0.5),
                        }
                    )

            print(f"   ✅ Loaded {len(self.training_data)} documents with embeddings")

        return {
            "documents": len(self.training_data),
            "embedding_dim": self.embedding_dim,
        }

    def train_link_prediction(self) -> float:
        """Train link prediction with real embeddings."""
        print("\n🔗 Training Link Prediction (Real Embeddings)...")

        criterion = nn.BCELoss()
        total_loss = 0.0
        steps = 0

        for epoch in range(min(3, self.epochs)):
            for i in range(0, len(self.training_data), self.batch_size):
                batch = self.training_data[i : i + self.batch_size]

                if len(batch) < 2:
                    continue

                # Get embeddings for pairs
                embeddings = [np.array(d["embedding"]) for d in batch]

                # Create positive pairs (from links if available)
                z1_list = []
                z2_list = []
                labels = []

                for j, doc in enumerate(batch):
                    for k in range(j + 1, min(j + 3, len(batch))):
                        z1_list.append(embeddings[j])
                        z2_list.append(embeddings[k])

                        # Check if they should link
                        doc1_links = doc.get("links", [])
                        doc2_id = batch[k].get("id", "")
                        label = 1.0 if doc2_id in doc1_links else 0.5
                        labels.append(label)

                if not z1_list:
                    continue

                # Convert to tensors
                z1 = torch.tensor(np.array(z1_list), dtype=torch.float32).to(
                    self.device
                )
                z2 = torch.tensor(np.array(z2_list), dtype=torch.float32).to(
                    self.device
                )
                y = (
                    torch.tensor(labels, dtype=torch.float32)
                    .unsqueeze(1)
                    .to(self.device)
                )

                # Forward
                pred = self.link_predictor(z1, z2)
                loss = criterion(pred, y)

                # Backward
                self.link_optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.link_predictor.parameters(), 1.0)
                self.link_optimizer.step()

                total_loss += loss.item()
                steps += 1

        avg_loss = total_loss / max(steps, 1)
        print(f"   Link Prediction Loss: {avg_loss:.4f}")

        self.metrics["link_prediction"].append(avg_loss)
        return avg_loss

    def train_summarization(self) -> float:
        """Train summarization with real embeddings."""
        print("\n📝 Training Summarization (Real Embeddings)...")

        criterion = nn.MSELoss()
        total_loss = 0.0
        steps = 0

        for epoch in range(min(3, self.epochs)):
            for i in range(0, len(self.training_data), self.batch_size):
                batch = self.training_data[i : i + self.batch_size]

                # Get embeddings
                embeddings = torch.tensor(
                    np.array([d["embedding"] for d in batch]), dtype=torch.float32
                ).to(self.device)

                # Target: compressed version of original
                # (In real impl, would use actual summaries)
                with torch.no_grad():
                    targets = embeddings[:, :384]  # First 384 dims as proxy

                # Forward
                summaries = self.summarizer(embeddings)
                loss = criterion(summaries, targets)

                # Backward
                self.summ_optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.summarizer.parameters(), 1.0)
                self.summ_optimizer.step()

                total_loss += loss.item()
                steps += 1

        avg_loss = total_loss / max(steps, 1)
        print(f"   Summarization Loss: {avg_loss:.4f}")

        self.metrics["summarization"].append(avg_loss)
        return avg_loss

    def train_quality_scoring(self) -> float:
        """Train quality scoring with real embeddings."""
        print("\n⭐ Training Quality Scoring (Real Embeddings)...")

        criterion = nn.BCELoss()
        total_loss = 0.0
        steps = 0

        for epoch in range(min(3, self.epochs)):
            for i in range(0, len(self.training_data), self.batch_size):
                batch = self.training_data[i : i + self.batch_size]

                # Get embeddings and quality scores
                embeddings = torch.tensor(
                    np.array([d["embedding"] for d in batch]), dtype=torch.float32
                ).to(self.device)

                scores = (
                    torch.tensor(
                        [d["quality_score"] for d in batch], dtype=torch.float32
                    )
                    .unsqueeze(1)
                    .to(self.device)
                )

                # Forward
                pred = self.quality_scorer(embeddings)
                loss = criterion(pred, scores)

                # Backward
                self.quality_optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.quality_scorer.parameters(), 1.0)
                self.quality_optimizer.step()

                total_loss += loss.item()
                steps += 1

        avg_loss = total_loss / max(steps, 1)
        print(f"   Quality Scoring Loss: {avg_loss:.4f}")

        self.metrics["quality_scoring"].append(avg_loss)
        return avg_loss

    def train_all(self) -> Dict:
        """Run full training on real embeddings."""
        print("\n" + "=" * 60)
        print("🎯 MIRA REAL EMBEDDING TRAINER")
        print("=" * 60)
        print(f"Device: {self.device}")
        print(f"Embedding Model: nomic-embed-text")
        print(f"Embedding Dim: {self.embedding_dim}")
        print(f"Batch Size: {self.batch_size}")
        print(f"Learning Rate: {self.learning_rate}")

        self.metrics["start_time"] = datetime.now().isoformat()

        # Load data with embeddings
        stats = self.load_data()

        if len(self.training_data) == 0:
            print("❌ No training data found")
            return self.metrics

        # Train
        print("\n" + "-" * 60)
        print("Training Phase")
        print("-" * 60)

        link_loss = self.train_link_prediction()
        summ_loss = self.train_summarization()
        quality_loss = self.train_quality_scoring()

        self.metrics["epochs"] += 1

        # Save
        self.save_models()

        return self.metrics

    def save_models(self):
        """Save trained models."""
        models_dir = Path("~/.mira/weave_models_real")
        models_dir.mkdir(parents=True, exist_ok=True)

        torch.save(
            self.link_predictor.state_dict(), models_dir / "link_predictor_real.pt"
        )
        torch.save(self.summarizer.state_dict(), models_dir / "summarizer_real.pt")
        torch.save(
            self.quality_scorer.state_dict(), models_dir / "quality_scorer_real.pt"
        )

        # Save config
        config = {
            "embedding_dim": self.embedding_dim,
            "embedding_model": "nomic-embed-text",
            "training_date": datetime.now().isoformat(),
            "metrics": self.metrics,
        }

        import json

        with open(models_dir / "config.json", "w") as f:
            json.dump(config, f, indent=2)

        print(f"\n💾 Saved real embedding models to {models_dir}")

    def get_report(self) -> str:
        """Generate training report."""
        link = (
            self.metrics["link_prediction"][-1]
            if self.metrics["link_prediction"]
            else 0
        )
        summ = self.metrics["summarization"][-1] if self.metrics["summarization"] else 0
        quality = (
            self.metrics["quality_scoring"][-1]
            if self.metrics["quality_scoring"]
            else 0
        )

        return f"""
╔═══════════════════════════════════════════════════════════════════╗
║          MIRA REAL EMBEDDING TRAINER REPORT                  ║
╠═══════════════════════════════════════════════════════════════════╣
║ TRAINING                                                    ║
║─────────────────────────────────────────────────────────────║
║ Embedding Model: nomic-embed-text (768-dim)                ║
║ Documents:        {len(self.training_data):<40} ║
║ Epochs:          {self.metrics["epochs"]:<40} ║
╠═══════════════════════════════════════════════════════════════════╣
║ METRICS                                                     ║
║─────────────────────────────────────────────────────────────║
║ Link Prediction Loss:  {link:<32.4f} ║
║ Summarization Loss:    {summ:<32.4f} ║
║ Quality Scoring Loss:  {quality:<32.4f} ║
╠═══════════════════════════════════════════════════════════════════╣
║ KEY DIFFERENCE                                              ║
║─────────────────────────────────────────────────────────────║
║ • Real semantic embeddings vs random vectors               ║
║ • Learns from actual content patterns                      ║
║ • Better generalization to new content                    ║
╚═══════════════════════════════════════════════════════════════════╝
"""


def main():
    """CLI for real embedding trainer."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Real Embedding Trainer")
    parser.add_argument(
        "--data", default="~/MIRA_ARCH_extracted", help="Data directory"
    )
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--lr", type=float, default=0.0001, help="Learning rate")
    parser.add_argument("--epochs", type=int, default=10, help="Epochs")

    args = parser.parse_args()

    trainer = RealEmbeddingTrainer(
        data_dir=Path(args.data),
        batch_size=args.batch,
        learning_rate=args.lr,
        epochs=args.epochs,
    )

    trainer.train_all()
    print(trainer.get_report())


if __name__ == "__main__":
    main()
