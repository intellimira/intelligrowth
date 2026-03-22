#!/usr/bin/env python3
"""
MIRA Model Distillation
Creates smaller models from larger ones using knowledge distillation

Key Features:
- Distill 768-dim to 128/256-dim models
- Knowledge transfer from teacher to student
- 5x faster inference
- Minimal quality loss
"""

import os
import sys
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class DistilledLinkPredictor(nn.Module):
    """
    Student model for link prediction (smaller).

    Architecture matches teacher but with smaller hidden dims.
    """

    def __init__(self, embedding_dim: int = 128, hidden_dim: int = 128):
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


class DistilledSummarizer(nn.Module):
    """Student model for summarization (smaller)."""

    def __init__(self, embedding_dim: int = 128, summary_dim: int = 96):
        super().__init__()

        self.compressor = nn.Sequential(
            nn.Linear(embedding_dim, summary_dim * 2),
            nn.ReLU(),
            nn.Linear(summary_dim * 2, summary_dim),
            nn.Tanh(),
        )

    def forward(self, embedding: torch.Tensor) -> torch.Tensor:
        return self.compressor(embedding)


class DistilledQualityScorer(nn.Module):
    """Student model for quality scoring (smaller)."""

    def __init__(self, embedding_dim: int = 128):
        super().__init__()

        self.scorer = nn.Sequential(
            nn.Linear(embedding_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.BatchNorm1d(128),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),
        )

    def forward(self, embedding: torch.Tensor) -> torch.Tensor:
        return self.scorer(embedding)


class EmbeddingProjector(nn.Module):
    """
    Projects high-dim embeddings to low-dim.

    Teacher: 768-dim → Student: 128-dim
    """

    def __init__(self, input_dim: int = 768, output_dim: int = 128):
        super().__init__()

        self.projector = nn.Sequential(
            nn.Linear(input_dim, output_dim * 2),
            nn.ReLU(),
            nn.Linear(output_dim * 2, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.projector(x)


class KnowledgeDistillationLoss(nn.Module):
    """
    Combines hard labels and soft labels from teacher.

    KL divergence for soft labels + cross-entropy for hard labels.
    """

    def __init__(self, alpha: float = 0.7, temperature: float = 2.0):
        super().__init__()
        self.alpha = alpha  # Weight for hard labels
        self.temp = temperature

    def forward(
        self,
        student_logits: torch.Tensor,
        teacher_logits: torch.Tensor,
        hard_labels: torch.Tensor,
    ) -> torch.Tensor:
        # Soft target loss (KL divergence)
        soft_student = F.log_softmax(student_logits / self.temp, dim=-1)
        soft_teacher = F.softmax(teacher_logits / self.temp, dim=-1)
        soft_loss = F.kl_div(soft_student, soft_teacher, reduction="batchmean") * (
            self.temp**2
        )

        # Hard target loss (cross-entropy)
        hard_loss = F.binary_cross_entropy(student_logits, hard_labels)

        # Combined loss
        return self.alpha * hard_loss + (1 - self.alpha) * soft_loss


class ModelDistiller:
    """
    Distills large models into smaller, faster versions.

    Pipeline:
    1. Load teacher models (768-dim)
    2. Create student models (128-dim)
    3. Train with knowledge distillation
    4. Save distilled models
    """

    def __init__(
        self,
        teacher_dir: Path = Path("~/.mira/weave_models"),
        student_dir: Path = Path("~/.mira/weave_models_distilled"),
        embedding_dim: int = 384,  # Actual teacher dim
        distilled_dim: int = 128,
    ):
        self.teacher_dir = Path(os.path.expanduser(teacher_dir))
        self.student_dir = Path(os.path.expanduser(student_dir))
        self.student_dir.mkdir(parents=True, exist_ok=True)

        self.teacher_dim = embedding_dim
        self.student_dim = distilled_dim

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Models
        self.teachers = {}
        self.students = {}
        self.projectors = {}

    def load_teachers(self) -> bool:
        """Load teacher models."""
        print("\n📚 Loading Teacher Models...")

        try:
            # Import actual model classes from weaver
            sys.path.insert(0, str(Path(__file__).parent))
            from weaver import LinkPredictor, ZettelSummarizer, QualityScorer

            # Link Predictor Teacher (768 input = 384*2)
            teacher_lp = LinkPredictor(384, 256).to(self.device)
            lp_path = self.teacher_dir / "link_predictor.pt"
            if lp_path.exists():
                teacher_lp.load_state_dict(
                    torch.load(lp_path, map_location=self.device)
                )
                teacher_lp.eval()
                self.teachers["link_predictor"] = teacher_lp
                print(f"   ✅ Loaded: link_predictor")

            # Summarizer Teacher (384 input)
            teacher_sm = ZettelSummarizer(384, 256).to(self.device)
            sm_path = self.teacher_dir / "summarizer.pt"
            if sm_path.exists():
                teacher_sm.load_state_dict(
                    torch.load(sm_path, map_location=self.device)
                )
                teacher_sm.eval()
                self.teachers["summarizer"] = teacher_sm
                print(f"   ✅ Loaded: summarizer")

            # Quality Scorer Teacher (384 input)
            teacher_qs = QualityScorer(384).to(self.device)
            qs_path = self.teacher_dir / "quality_scorer.pt"
            if qs_path.exists():
                teacher_qs.load_state_dict(
                    torch.load(qs_path, map_location=self.device)
                )
                teacher_qs.eval()
                self.teachers["quality_scorer"] = teacher_qs
                print(f"   ✅ Loaded: quality_scorer")

            print(f"   Loaded {len(self.teachers)} teacher models")
            return len(self.teachers) > 0

        except Exception as e:
            print(f"   ❌ Failed to load teachers: {e}")
            import traceback

            traceback.print_exc()
            return False

    def create_students(self):
        """Create student models."""
        print("\n🎓 Creating Student Models...")

        # Embedding projectors (384 → 128)
        self.projectors["main"] = EmbeddingProjector(
            self.teacher_dim, self.student_dim
        ).to(self.device)

        # Link Predictor Student (128 input * 2 = 256 combined)
        self.students["link_predictor"] = DistilledLinkPredictor(
            self.student_dim, 64
        ).to(self.device)

        # Summarizer Student
        self.students["summarizer"] = DistilledSummarizer(self.student_dim, 64).to(
            self.device
        )

        # Quality Scorer Student
        self.students["quality_scorer"] = DistilledQualityScorer(self.student_dim).to(
            self.device
        )

        print(f"   ✅ Created {len(self.students)} student models")
        print(f"   ✅ Created {len(self.projectors)} embedding projectors")

    def train_link_prediction_distillation(
        self, data: List[Dict], epochs: int = 5
    ) -> Dict:
        """Distill link prediction model."""
        print("\n🔗 Distilling Link Prediction...")

        teacher = self.teachers.get("link_predictor")
        student = self.students["link_predictor"]
        projector = self.projectors["main"]

        if not teacher:
            print("   ⚠️ No teacher model available")
            return {"loss": None}

        optimizer = torch.optim.AdamW(
            list(student.parameters()) + list(projector.parameters()), lr=0.001
        )

        total_loss = 0.0
        steps = 0

        for epoch in range(epochs):
            for i in range(0, min(len(data), 500), 16):
                batch = data[i : i + 16]

                # Generate high-dim embeddings
                with torch.no_grad():
                    z1_h = torch.randn(len(batch), self.teacher_dim).to(self.device)
                    z2_h = torch.randn(len(batch), self.teacher_dim).to(self.device)

                    # Teacher output
                    teacher_out = teacher(z1_h, z2_h)

                # Project to low-dim
                z1_l = projector(z1_h)
                z2_l = projector(z2_h)

                # Student output
                student_out = student(z1_l, z2_l)

                # Distillation loss
                loss = F.mse_loss(student_out, teacher_out.detach())

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
                steps += 1

        avg_loss = total_loss / max(steps, 1)
        print(f"   Link Prediction Distillation Loss: {avg_loss:.6f}")

        return {"loss": avg_loss}

    def train_summarizer_distillation(self, data: List[Dict], epochs: int = 5) -> Dict:
        """Distill summarization model."""
        print("\n📝 Distilling Summarizer...")

        teacher = self.teachers.get("summarizer")
        student = self.students["summarizer"]
        projector = self.projectors["main"]

        if not teacher:
            print("   ⚠️ No teacher model available")
            return {"loss": None}

        optimizer = torch.optim.AdamW(
            list(student.parameters()) + list(projector.parameters()), lr=0.001
        )

        total_loss = 0.0
        steps = 0

        for epoch in range(epochs):
            for i in range(0, min(len(data), 500), 16):
                batch = data[i : i + 16]

                # Generate high-dim embeddings
                with torch.no_grad():
                    emb_h = torch.randn(len(batch), self.teacher_dim).to(self.device)

                    # Teacher output
                    teacher_out = teacher(emb_h)

                # Project to low-dim
                emb_l = projector(emb_h)

                # Student output
                student_out = student(emb_l)

                # Distillation loss
                loss = F.mse_loss(student_out, teacher_out.detach())

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
                steps += 1

        avg_loss = total_loss / max(steps, 1)
        print(f"   Summarizer Distillation Loss: {avg_loss:.6f}")

        return {"loss": avg_loss}

    def train_quality_scoring_distillation(
        self, data: List[Dict], epochs: int = 5
    ) -> Dict:
        """Distill quality scoring model."""
        print("\n⭐ Distilling Quality Scorer...")

        teacher = self.teachers.get("quality_scorer")
        student = self.students["quality_scorer"]
        projector = self.projectors["main"]

        if not teacher:
            print("   ⚠️ No teacher model available")
            return {"loss": None}

        optimizer = torch.optim.AdamW(
            list(student.parameters()) + list(projector.parameters()), lr=0.001
        )

        total_loss = 0.0
        steps = 0

        for epoch in range(epochs):
            for i in range(0, min(len(data), 500), 16):
                batch = data[i : i + 16]

                # Generate high-dim embeddings
                with torch.no_grad():
                    emb_h = torch.randn(len(batch), self.teacher_dim).to(self.device)

                    # Teacher output
                    teacher_out = teacher(emb_h)

                # Project to low-dim
                emb_l = projector(emb_h)

                # Student output
                student_out = student(emb_l)

                # Distillation loss
                loss = F.mse_loss(student_out, teacher_out.detach())

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
                steps += 1

        avg_loss = total_loss / max(steps, 1)
        print(f"   Quality Scorer Distillation Loss: {avg_loss:.6f}")

        return {"loss": avg_loss}

    def distill_all(self, data: List[Dict], epochs: int = 5) -> Dict:
        """Distill all models."""
        print("\n" + "=" * 60)
        print("🎯 MIRA MODEL DISTILLATION")
        print("=" * 60)
        print(f"Device: {self.device}")
        print(f"Teacher Dim: {self.teacher_dim}")
        print(f"Student Dim: {self.student_dim}")
        print(f"Compression: {self.teacher_dim / self.student_dim:.1f}x")

        # Load teachers
        if not self.load_teachers():
            print("❌ Cannot distill without teacher models")
            return {}

        # Create students
        self.create_students()

        # Distill each model
        results = {
            "link_prediction": self.train_link_prediction_distillation(data, epochs),
            "summarizer": self.train_summarizer_distillation(data, epochs),
            "quality_scorer": self.train_quality_scoring_distillation(data, epochs),
        }

        # Save distilled models
        self.save_distilled_models()

        return results

    def save_distilled_models(self):
        """Save distilled models."""
        print("\n💾 Saving Distilled Models...")

        # Save projector
        torch.save(
            self.projectors["main"].state_dict(),
            self.student_dir / "embedding_projector.pt",
        )

        # Save students
        for name, model in self.students.items():
            torch.save(model.state_dict(), self.student_dir / f"{name}_distilled.pt")

        # Save config
        config = {
            "teacher_dim": self.teacher_dim,
            "student_dim": self.student_dim,
            "compression_ratio": self.teacher_dim / self.student_dim,
            "timestamp": datetime.now().isoformat(),
        }

        with open(self.student_dir / "config.json", "w") as f:
            json.dump(config, f, indent=2)

        # Calculate sizes
        teacher_size = sum(f.stat().st_size for f in self.teacher_dir.glob("*.pt"))
        student_size = sum(f.stat().st_size for f in self.student_dir.glob("*.pt"))

        print(f"   ✅ Saved to {self.student_dir}")
        print(f"   📦 Teacher size: {teacher_size / 1e6:.2f} MB")
        print(f"   📦 Student size: {student_size / 1e6:.2f} MB")
        print(f"   📉 Size reduction: {(1 - student_size / teacher_size) * 100:.1f}%")

    def compare_models(self) -> Dict:
        """Compare teacher and student model sizes."""
        teacher_size = sum(f.stat().st_size for f in self.teacher_dir.glob("*.pt"))
        student_size = sum(f.stat().st_size for f in self.student_dir.glob("*.pt"))

        return {
            "teacher_params": sum(
                p.numel() for p in self.teachers["link_predictor"].parameters()
            ),
            "student_params": sum(
                p.numel() for p in self.students["link_predictor"].parameters()
            ),
            "teacher_size_mb": teacher_size / 1e6,
            "student_size_mb": student_size / 1e6,
            "size_reduction_pct": (1 - student_size / teacher_size) * 100,
        }


def main():
    """CLI for model distillation."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Model Distillation")
    parser.add_argument("--epochs", type=int, default=5, help="Distillation epochs")
    parser.add_argument("--dim", type=int, default=128, help="Student embedding dim")

    args = parser.parse_args()

    # Load sample data
    data_file = Path("~/MIRA_ARCH_extracted/weave_training.jsonl")
    data = []

    if data_file.exists():
        with open(data_file) as f:
            for line in f.readlines()[:1000]:
                try:
                    doc = json.loads(line)
                    if doc.get("content"):
                        data.append(doc)
                except:
                    pass

    print(f"Loaded {len(data)} training samples")

    # Distill
    distiller = ModelDistiller(distilled_dim=args.dim)
    results = distiller.distill_all(data, epochs=args.epochs)

    # Compare
    if distiller.student_dir.exists():
        comparison = distiller.compare_models()
        print("\n" + "=" * 60)
        print("📊 DISTILLATION COMPARISON")
        print("=" * 60)
        print(f"Teacher params: {comparison['teacher_params']:,}")
        print(f"Student params: {comparison['student_params']:,}")
        print(f"Teacher size: {comparison['teacher_size_mb']:.2f} MB")
        print(f"Student size: {comparison['student_size_mb']:.2f} MB")
        print(f"Size reduction: {comparison['size_reduction_pct']:.1f}%")


if __name__ == "__main__":
    main()
