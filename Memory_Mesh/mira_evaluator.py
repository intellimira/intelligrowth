#!/usr/bin/env python3
"""
MIRA Evaluation Framework
Test datasets with ground truth for proper evaluation

Test Sets:
1. Link Prediction: Known correct zettel links
2. Summarization: Expert-written summaries
3. Response Quality: Scored query-response pairs

Features:
- Automated evaluation pipeline
- Precision/recall/F1 metrics
- Weekly improvement reports
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score


class TestDataset:
    """Base class for test datasets."""

    def __init__(self, name: str, tests: List[Dict]):
        self.name = name
        self.tests = tests

    def __len__(self):
        return len(self.tests)

    def __getitem__(self, idx):
        return self.tests[idx]


class LinkPredictionTestSet(TestDataset):
    """
    Test set for link prediction.

    Format:
    {
        "zettel1": "content...",
        "zettel2": "content...",
        "should_link": true/false,
        "reason": "explanation"
    }
    """

    def __init__(self):
        # Create test cases from MIRA patterns
        tests = self._create_tests()
        super().__init__("link_prediction", tests)

    def _create_tests(self) -> List[Dict]:
        """Create test cases based on MIRA patterns."""
        return [
            # Related topics (should link)
            {
                "zettel1": "MIRA uses Ollama for local inference. This provides privacy-first AI.",
                "zettel2": "OpenJarvis is Stanford's local-first AI agent framework.",
                "should_link": True,
                "reason": "Both discuss local-first AI frameworks",
            },
            {
                "zettel1": "Vector embeddings capture semantic meaning in high-dimensional space.",
                "zettel2": "Ollama provides nomic-embed-text for generating embeddings.",
                "should_link": True,
                "reason": "Embeddings are related to vector representations",
            },
            {
                "zettel1": "PyTorch provides CUDA support for GPU acceleration.",
                "zettel2": "RTX 2060 has 6GB VRAM for neural network training.",
                "should_link": True,
                "reason": "Both relate to GPU-based deep learning",
            },
            {
                "zettel1": "Session logs record conversational patterns.",
                "zettel2": "Zettels are interconnected knowledge notes.",
                "should_link": True,
                "reason": "Both are MIRA knowledge management concepts",
            },
            # Unrelated topics (should not link)
            {
                "zettel1": "Python programming language syntax and features.",
                "zettel2": "Quantum computing uses qubits and superposition.",
                "should_link": False,
                "reason": "Completely different domains",
            },
            {
                "zettel1": "MIRA training uses PyTorch for neural networks.",
                "zettel2": "Breakfast recipes with eggs and toast.",
                "should_link": False,
                "reason": "Cooking unrelated to AI",
            },
            {
                "zettel1": "AutoResearch optimizes model hyperparameters.",
                "zettel2": "Stock market prediction algorithms.",
                "should_link": False,
                "reason": "Different optimization domains",
            },
            {
                "zettel1": "Persona Council convenes for multi-perspective decisions.",
                "zettel2": "Weather forecasting models.",
                "should_link": False,
                "reason": "MIRA internals vs external science",
            },
        ]


class SummarizationTestSet(TestDataset):
    """
    Test set for summarization quality.

    Format:
    {
        "content": "long content...",
        "expected_summary_theme": "main topic",
        "quality_score": 1-5
    }
    """

    def __init__(self):
        tests = self._create_tests()
        super().__init__("summarization", tests)

    def _create_tests(self) -> List[Dict]:
        """Create summarization test cases."""
        return [
            {
                "content": """
MIRA is a sovereign AI agent framework that learns from its own history. 
It uses The Weave system for knowledge management and zettel linking. 
The framework includes Persona Council for multi-perspective decision making.
AutoResearch enables self-optimization through experimentation.
Memory Mesh stores all knowledge in interconnected zettels.
Training uses PyTorch with CUDA acceleration on RTX 2060 GPU.
""",
                "expected_theme": "MIRA AI framework architecture",
                "quality_score": 4,
            },
            {
                "content": """
Ollama provides local AI inference without cloud dependencies.
It supports various models including nomic-embed-text for embeddings.
Qwen2.5-coder is optimized for code generation tasks.
Local inference ensures privacy and data sovereignty.
Models can be downloaded and run offline.
""",
                "expected_theme": "Ollama local AI capabilities",
                "quality_score": 5,
            },
            {
                "content": """
Python is a programming language.
It has many features.
People use Python for various tasks.
""",
                "expected_theme": "Python basics",
                "quality_score": 2,  # Too generic
            },
            {
                "content": """
PyTorch neural networks use tensors for data representation.
Gradient descent optimizes weights through backpropagation.
Batch normalization stabilizes training.
Dropout prevents overfitting.
AdamW optimizer provides adaptive learning rates.
""",
                "expected_theme": "Deep learning fundamentals",
                "quality_score": 5,
            },
            {
                "content": """
stuff things items
random words here
more random content
not meaningful at all
but still text
""",
                "expected_theme": "Incoherent content",
                "quality_score": 1,
            },
        ]


class ResponseQualityTestSet(TestDataset):
    """
    Test set for response quality.

    Format:
    {
        "query": "user query",
        "response": "MIRA response",
        "expected_score": 1-5,
        "criteria": ["accuracy", "helpfulness", "relevance"]
    }
    """

    def __init__(self):
        tests = self._create_tests()
        super().__init__("response_quality", tests)

    def _create_tests(self) -> List[Dict]:
        """Create response quality test cases."""
        return [
            {
                "query": "What is MIRA's Weave system?",
                "response": """MIRA's Weave system is the knowledge management layer that:

1. **Session Sealing** - Processes session logs into zettels
2. **Vector Indexing** - Embeds content for semantic search
3. **Smart Linking** - Discovers relationships between zettels
4. **Quality Scoring** - Evaluates content quality

The Weave continuously improves through self-training on accumulated knowledge.""",
                "expected_score": 5,
                "criteria": ["accurate", "comprehensive", "well-structured"],
            },
            {
                "query": "How do I train a neural network?",
                "response": """Training neural networks involves:

1. Prepare data (features + labels)
2. Initialize weights randomly
3. Forward pass to get predictions
4. Calculate loss vs ground truth
5. Backpropagate to compute gradients
6. Update weights with optimizer

Repeat until convergence.""",
                "expected_score": 4,
                "criteria": ["accurate", "helpful", "concise"],
            },
            {
                "query": "What is 2+2?",
                "response": "Yes, I can help with that. Neural networks are complex systems that process information through layers of interconnected nodes using mathematical transformations to learn patterns from data.",
                "expected_score": 2,
                "criteria": ["relevant", "concise", "accurate"],
            },
            {
                "query": "Tell me about quantum computing",
                "response": "Quantum computing uses quantum mechanical phenomena like superposition and entanglement to perform computation. Qubits can exist in multiple states simultaneously, enabling parallel processing of many possibilities. Quantum computers can solve certain problems exponentially faster than classical computers.",
                "expected_score": 5,
                "criteria": ["accurate", "educational", "clear"],
            },
            {
                "query": "How do I make coffee?",
                "response": "I don't have information about that in my training data.",
                "expected_score": 1,
                "criteria": ["honest", "helpful"],
            },
            {
                "query": "What is the meaning of life?",
                "response": "The meaning of life is a philosophical question that different cultures and individuals answer differently. Some find meaning through relationships, others through achievement or spirituality. There's no single universal answer.",
                "expected_score": 4,
                "criteria": ["thoughtful", "balanced", "reflective"],
            },
        ]


class MiraEvaluator:
    """
    Comprehensive MIRA evaluation system.

    Uses ground truth test sets for proper metrics.
    """

    def __init__(self, test_data_dir: Path = Path("~/.mira/test_data")):
        self.test_data_dir = Path(os.path.expanduser(test_data_dir))
        self.test_data_dir.mkdir(parents=True, exist_ok=True)

        # Load test sets
        self.link_tests = LinkPredictionTestSet()
        self.summary_tests = SummarizationTestSet()
        self.response_tests = ResponseQualityTestSet()

        # Results storage
        self.results_db = self.test_data_dir / "evaluation_results.db"
        self._init_results_db()

    def _init_results_db(self):
        """Initialize results database."""
        conn = sqlite3.connect(str(self.results_db))
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                test_type TEXT,
                metric_name TEXT,
                value REAL,
                metadata TEXT
            )
        """)

        conn.commit()
        conn.close()

    def evaluate_link_prediction(
        self, predictions: List[float], threshold: float = 0.5
    ) -> Dict:
        """
        Evaluate link prediction predictions.

        Args:
            predictions: List of predicted probabilities (0-1)
            threshold: Decision threshold

        Returns metrics dictionary.
        """
        y_true = [t["should_link"] for t in self.link_tests.tests]
        y_pred = [p > threshold for p in predictions]

        metrics = {
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
            "accuracy": accuracy_score(y_true, y_pred),
            "test_size": len(self.link_tests),
        }

        self._save_metrics("link_prediction", metrics)
        return metrics

    def evaluate_summarization(self, quality_scores: List[float]) -> Dict:
        """
        Evaluate summarization quality scores.

        Args:
            quality_scores: List of predicted quality scores

        Returns metrics dictionary.
        """
        y_true = [t["quality_score"] for t in self.summary_tests.tests]
        y_pred = quality_scores

        # Correlation
        import numpy as np

        correlation = np.corrcoef(y_true, y_pred)[0, 1] if len(y_true) > 1 else 0

        # Mean absolute error
        mae = np.mean(np.abs(np.array(y_true) - np.array(y_pred)))

        # Within tolerance (score within 1)
        within_tolerance = sum(
            1 for t, p in zip(y_true, y_pred) if abs(t - p) <= 1
        ) / len(y_true)

        metrics = {
            "correlation": correlation if not np.isnan(correlation) else 0,
            "mae": mae,
            "within_tolerance": within_tolerance,
            "test_size": len(self.summary_tests),
        }

        self._save_metrics("summarization", metrics)
        return metrics

    def evaluate_response_quality(self, quality_scores: List[float]) -> Dict:
        """
        Evaluate response quality predictions.

        Args:
            quality_scores: List of predicted quality scores

        Returns metrics dictionary.
        """
        y_true = [t["expected_score"] for t in self.response_tests.tests]
        y_pred = quality_scores

        import numpy as np

        correlation = np.corrcoef(y_true, y_pred)[0, 1] if len(y_true) > 1 else 0
        mae = np.mean(np.abs(np.array(y_true) - np.array(y_pred)))

        # Accuracy at different tolerances
        acc_1 = sum(1 for t, p in zip(y_true, y_pred) if abs(t - p) <= 1) / len(y_true)
        acc_2 = sum(1 for t, p in zip(y_true, y_pred) if abs(t - p) <= 2) / len(y_true)

        metrics = {
            "correlation": correlation if not np.isnan(correlation) else 0,
            "mae": mae,
            "accuracy_1": acc_1,
            "accuracy_2": acc_2,
            "test_size": len(self.response_tests),
        }

        self._save_metrics("response_quality", metrics)
        return metrics

    def _save_metrics(self, test_type: str, metrics: Dict):
        """Save metrics to database."""
        conn = sqlite3.connect(str(self.results_db))
        cursor = conn.cursor()

        for metric_name, value in metrics.items():
            cursor.execute(
                """
                INSERT INTO evaluation_results (timestamp, test_type, metric_name, value)
                VALUES (?, ?, ?, ?)
            """,
                (datetime.now().isoformat(), test_type, metric_name, value),
            )

        conn.commit()
        conn.close()

    def run_full_evaluation(
        self,
        link_predictions: List[float] = None,
        summary_scores: List[float] = None,
        response_scores: List[float] = None,
    ) -> Dict:
        """
        Run complete evaluation suite.

        Args:
            link_predictions: Predicted link probabilities
            summary_scores: Predicted summary quality scores
            response_scores: Predicted response quality scores

        Returns comprehensive results.
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "test_sets": {
                "link_prediction": len(self.link_tests),
                "summarization": len(self.summary_tests),
                "response_quality": len(self.response_tests),
            },
        }

        # Evaluate each
        if link_predictions:
            results["link_prediction"] = self.evaluate_link_prediction(link_predictions)

        if summary_scores:
            results["summarization"] = self.evaluate_summarization(summary_scores)

        if response_scores:
            results["response_quality"] = self.evaluate_response_quality(
                response_scores
            )

        # Overall score
        all_scores = []
        if "link_prediction" in results:
            all_scores.append(results["link_prediction"].get("f1", 0))
        if "summarization" in results:
            all_scores.append(results["summarization"].get("correlation", 0))
        if "response_quality" in results:
            all_scores.append(results["response_quality"].get("correlation", 0))

        results["overall_score"] = (
            sum(all_scores) / len(all_scores) if all_scores else 0
        )

        return results

    def get_historical_metrics(self, test_type: str = None) -> List[Dict]:
        """Get historical evaluation metrics."""
        conn = sqlite3.connect(str(self.results_db))
        cursor = conn.cursor()

        if test_type:
            cursor.execute(
                """
                SELECT timestamp, test_type, metric_name, value
                FROM evaluation_results
                WHERE test_type = ?
                ORDER BY timestamp DESC
                LIMIT 100
            """,
                (test_type,),
            )
        else:
            cursor.execute("""
                SELECT timestamp, test_type, metric_name, value
                FROM evaluation_results
                ORDER BY timestamp DESC
                LIMIT 100
            """)

        results = [
            {"timestamp": r[0], "test_type": r[1], "metric": r[2], "value": r[3]}
            for r in cursor.fetchall()
        ]

        conn.close()
        return results

    def generate_report(self, results: Dict) -> str:
        """Generate formatted evaluation report."""
        report = f"""
╔═══════════════════════════════════════════════════════════════════╗
║             MIRA EVALUATION REPORT                             ║
╠═══════════════════════════════════════════════════════════════════╣
║ Date: {results["timestamp"][:19]:<51} ║
╠═══════════════════════════════════════════════════════════════════╣
"""

        if "link_prediction" in results:
            lp = results["link_prediction"]
            report += f"""║ LINK PREDICTION ({lp["test_size"]} tests)                           ║
║─────────────────────────────────────────────────────────────║
║ F1 Score:        {lp["f1"]:.3f}                                   ║
║ Precision:       {lp["precision"]:.3f}                                   ║
║ Recall:          {lp["recall"]:.3f}                                   ║
║ Accuracy:        {lp["accuracy"]:.3f}                                   ║
"""

        if "summarization" in results:
            sm = results["summarization"]
            report += f"""║ SUMMARIZATION ({sm["test_size"]} tests)                            ║
║─────────────────────────────────────────────────────────────║
║ Correlation:     {sm["correlation"]:.3f}                                   ║
║ MAE:             {sm["mae"]:.3f}                                   ║
║ Within ±1:      {sm["within_tolerance"]:.1%}                                  ║
"""

        if "response_quality" in results:
            rq = results["response_quality"]
            report += f"""║ RESPONSE QUALITY ({rq["test_size"]} tests)                           ║
║─────────────────────────────────────────────────────────────║
║ Correlation:     {rq["correlation"]:.3f}                                   ║
║ MAE:             {rq["mae"]:.3f}                                   ║
║ Accuracy ±1:     {rq["accuracy_1"]:.1%}                                  ║
║ Accuracy ±2:     {rq["accuracy_2"]:.1%}                                  ║
"""

        report += f"""╠═══════════════════════════════════════════════════════════════════╣
║ OVERALL SCORE:   {results.get("overall_score", 0):.3f}                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""

        return report


def main():
    """CLI for MIRA evaluation."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Evaluation Framework")
    parser.add_argument("--eval", action="store_true", help="Run full evaluation")
    parser.add_argument("--link-tests", action="store_true", help="Show link tests")
    parser.add_argument(
        "--summary-tests", action="store_true", help="Show summary tests"
    )
    parser.add_argument(
        "--response-tests", action="store_true", help="Show response tests"
    )
    parser.add_argument(
        "--history", action="store_true", help="Show historical metrics"
    )

    args = parser.parse_args()

    evaluator = MiraEvaluator()

    if args.link_tests:
        print(f"\n📋 Link Prediction Tests ({len(evaluator.link_tests)}):")
        for i, test in enumerate(evaluator.link_tests.tests):
            print(f"  {i + 1}. Should link: {test['should_link']} - {test['reason']}")

    elif args.summary_tests:
        print(f"\n📋 Summarization Tests ({len(evaluator.summary_tests)}):")
        for i, test in enumerate(evaluator.summary_tests.tests):
            print(
                f"  {i + 1}. Score: {test['quality_score']} - {test['expected_theme']}"
            )

    elif args.response_tests:
        print(f"\n📋 Response Quality Tests ({len(evaluator.response_tests)}):")
        for i, test in enumerate(evaluator.response_tests.tests):
            print(
                f"  {i + 1}. Score: {test['expected_score']} - Q: {test['query'][:40]}..."
            )

    elif args.history:
        history = evaluator.get_historical_metrics()
        print(f"\n📊 Historical Metrics ({len(history)} entries):")
        for h in history[:10]:
            print(
                f"  {h['timestamp'][:19]} - {h['test_type']}: {h['metric']}={h['value']:.3f}"
            )

    elif args.eval:
        # Run with simulated predictions
        import numpy as np

        # Simulated predictions (should be replaced with actual model outputs)
        link_preds = [0.8, 0.7, 0.9, 0.6, 0.2, 0.1, 0.15, 0.1]
        summary_scores = [4.0, 4.5, 2.5, 4.8, 1.2]
        response_scores = [4.8, 4.0, 2.5, 4.5, 1.5, 4.0]

        results = evaluator.run_full_evaluation(
            link_predictions=link_preds,
            summary_scores=summary_scores,
            response_scores=response_scores,
        )

        print(evaluator.generate_report(results))

    else:
        parser.print_help()
        print("\n📊 Test Datasets:")
        print(f"   Link Prediction: {len(evaluator.link_tests)} tests")
        print(f"   Summarization: {len(evaluator.summary_tests)} tests")
        print(f"   Response Quality: {len(evaluator.response_tests)} tests")
        print("\nUse --eval to run evaluation with simulated predictions.")


if __name__ == "__main__":
    main()
