"""
MIRA-OJ Autonomous Optimizer
Self-tuning inference engine based on AutoResearch findings

Capabilities:
- Automatic VRAM detection and optimization
- Token bounds safety
- Adaptive batch sizing
- Performance monitoring
- Self-improvement loop
"""

import os
import time
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime

import torch


@dataclass
class OptimizationMetrics:
    """Track optimization performance."""

    timestamp: str
    vram_used_mb: float
    vram_available_mb: float
    inference_time_ms: float
    batch_size: int
    queue_length: int
    oom_count: int
    success_count: int
    efficiency_score: float


@dataclass
class OptimizationConfig:
    """Current optimization configuration."""

    batch_size: int
    max_context_length: int
    use_fp16: bool
    gradient_checkpointing: bool
    efficiency_mode: bool
    attention_type: str  # "standard" or "flash"
    max_retries: int


class AutonomousOptimizer:
    """
    MIRA-OJ's self-tuning optimizer.

    Based on AutoResearch experiments:
    - Baseline: depth=4, n_embd=384 = optimal for 6GB VRAM
    - VRAM scales ~quadratically with model size
    - Token clamping prevents crashes
    - AdamW lr=0.001 is stable
    """

    def __init__(self, config_path: str = None):
        self.config_path = config_path or "~/.mira/optimizer_config.json"
        self.metrics_path = Path(self.config_path).parent / "optimizer_metrics.jsonl"

        self.metrics: List[OptimizationMetrics] = []
        self.config = self._load_config()

        # AutoResearch findings
        self.baseline_vram_mb = 250  # baseline config
        self.baseline_params_m = 7.9  # 7.9M params

        # Thresholds
        self.oom_threshold = 0.1  # 10% OOM rate = switch mode
        self.efficiency_target = 0.8

    def _load_config(self) -> OptimizationConfig:
        """Load or create default config."""
        path = Path(self.config_path).expanduser()
        if path.exists():
            with open(path) as f:
                data = json.load(f)
                return OptimizationConfig(**data)

        # Default config for RTX 2060
        return OptimizationConfig(
            batch_size=4,
            max_context_length=256,
            use_fp16=True,
            gradient_checkpointing=False,
            efficiency_mode=True,
            attention_type="standard",
            max_retries=3,
        )

    def _save_config(self):
        """Save current config."""
        path = Path(self.config_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(asdict(self.config), f, indent=2)

    def detect_vram(self) -> Tuple[float, float]:
        """Detect VRAM usage and availability."""
        if not torch.cuda.is_available():
            return 0.0, 0.0

        allocated = torch.cuda.memory_allocated() / (1024**2)
        reserved = torch.cuda.memory_reserved() / (1024**2)
        total = torch.cuda.get_device_properties(0).total_memory / (1024**2)
        available = total - reserved

        return allocated, available

    def get_vram_tier(self) -> str:
        """Classify device by VRAM capacity."""
        if not torch.cuda.is_available():
            return "cpu"

        total = torch.cuda.get_device_properties(0).total_memory / (1024**3)

        if total >= 24:
            return "high"
        elif total >= 12:
            return "medium"
        elif total >= 6:
            return "low"
        else:
            return "minimal"

    def optimize_for_device(self) -> OptimizationConfig:
        """
        Optimize config based on current device.

        Based on AutoResearch findings:
        - 6GB VRAM: batch=4 works well
        - Larger batches = more VRAM but faster
        - FP16 saves ~50% VRAM
        """
        tier = self.get_vram_tier()
        _, available = self.detect_vram()

        if tier == "minimal":
            self.config.batch_size = 1
            self.config.use_fp16 = True
            self.config.efficiency_mode = True
            self.config.attention_type = "standard"
        elif tier == "low":
            self.config.batch_size = 4
            self.config.use_fp16 = True
            self.config.efficiency_mode = False
            self.config.attention_type = "standard"
        elif tier == "medium":
            self.config.batch_size = 8
            self.config.use_fp16 = True
            self.config.efficiency_mode = False
            self.config.attention_type = "flash"
        else:  # high
            self.config.batch_size = 16
            self.config.use_fp16 = False
            self.config.efficiency_mode = False
            self.config.attention_type = "flash"

        self._save_config()
        return self.config

    def record_metrics(
        self,
        inference_time_ms: float,
        queue_length: int = 0,
        oom_occurred: bool = False,
    ) -> OptimizationMetrics:
        """Record performance metrics."""
        allocated, available = self.detect_vram()

        # Calculate efficiency score (lower = better for time, higher = better for VRAM)
        vram_util = (
            allocated / (allocated + available) if (allocated + available) > 0 else 0
        )
        time_score = min(1.0, 1000 / max(inference_time_ms, 1))  # target < 1s
        efficiency = (vram_util + time_score) / 2

        metric = OptimizationMetrics(
            timestamp=datetime.now().isoformat(),
            vram_used_mb=allocated,
            vram_available_mb=available,
            inference_time_ms=inference_time_ms,
            batch_size=self.config.batch_size,
            queue_length=queue_length,
            oom_count=1 if oom_occurred else 0,
            success_count=0 if oom_occurred else 1,
            efficiency_score=efficiency,
        )

        self.metrics.append(metric)

        # Persist to file
        self.metrics_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.metrics_path, "a") as f:
            f.write(json.dumps(asdict(metric)) + "\n")

        return metric

    def analyze_and_adjust(self) -> OptimizationConfig:
        """
        Analyze recent metrics and adjust configuration.

        This is the "self-evolution" loop - MIRA learns from its own performance.
        """
        if len(self.metrics) < 10:
            return self.config

        recent = self.metrics[-10:]

        # Calculate OOM rate
        oom_rate = sum(m.oom_count for m in recent) / len(recent)
        avg_time = sum(m.inference_time_ms for m in recent) / len(recent)
        avg_vram = sum(m.vram_used_mb for m in recent) / len(recent)

        # Adjust based on findings
        if oom_rate > self.oom_threshold:
            # Too many OOMs - reduce batch size
            self.config.batch_size = max(1, self.config.batch_size // 2)
            self.config.efficiency_mode = True
            print(
                f"[Optimizer] OOM rate high ({oom_rate:.1%}), reducing batch to {self.config.batch_size}"
            )

        elif avg_time > 5000 and self.config.batch_size < 16:
            # Inference too slow - could increase batch
            self.config.batch_size = min(32, self.config.batch_size + 1)
            print(
                f"[Optimizer] Inference slow ({avg_time:.0f}ms), increasing batch to {self.config.batch_size}"
            )

        self._save_config()
        return self.config

    def clamp_tokens(self, tokens: torch.Tensor, vocab_size: int) -> torch.Tensor:
        """
        Token bounds safety - prevents CUDA crashes.

        This was a critical finding from AutoResearch experiments.
        """
        return tokens.clamp(0, vocab_size - 1)

    def get_report(self) -> str:
        """Generate optimization report."""
        tier = self.get_vram_tier()
        device_name = (
            torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
        )

        if self.metrics:
            recent = self.metrics[-10:]
            avg_time = sum(m.inference_time_ms for m in recent) / len(recent)
            oom_rate = sum(m.oom_count for m in recent) / len(recent)
            avg_vram = sum(m.vram_used_mb for m in recent) / len(recent)
        else:
            avg_time = 0
            oom_rate = 0
            avg_vram = 0

        return f"""
╔═══════════════════════════════════════════════════════════════╗
║              MIRA-OJ AUTONOMOUS OPTIMIZER                    ║
╠═══════════════════════════════════════════════════════════════╣
║ DEVICE                                                      ║
║─────────────────────────────────────────────────────────────║
║ Name:      {device_name:<45} ║
║ VRAM Tier: {tier:<45} ║
║─────────────────────────────────────────────────────────────║
║ CURRENT CONFIG                                              ║
║─────────────────────────────────────────────────────────────║
║ Batch Size:   {self.config.batch_size:<42} ║
║ Context Len:  {self.config.max_context_length:<42} ║
║ FP16:         {str(self.config.use_fp16):<45} ║
║ Efficiency:   {str(self.config.efficiency_mode):<45} ║
║ Attention:    {self.config.attention_type:<45} ║
║─────────────────────────────────────────────────────────────║
║ RECENT METRICS (last 10)                                    ║
║─────────────────────────────────────────────────────────────║
║ Avg Time:     {avg_time:>8.1f} ms{" " * 30}║
║ OOM Rate:     {oom_rate:>8.1%}{" " * 34}║
║ Avg VRAM:     {avg_vram:>8.1f} MB{" " * 30}║
╠═══════════════════════════════════════════════════════════════╣
║ BASED ON AUTORESEARCH                                       ║
║─────────────────────────────────────────────────────────────║
║ Baseline: depth=4, n_embd=384, 7.9M params, 0.25GB VRAM   ║
║ Optimal LR: 0.001 with AdamW                                 ║
║ Token clamping prevents CUDA crashes                          ║
╚═══════════════════════════════════════════════════════════════╝
"""

    def run_self_check(self) -> bool:
        """
        Run self-check to verify optimizer health.

        Part of the self-evolution loop.
        """
        print("\n[Optimizer] Running self-check...")

        # Check CUDA availability
        if not torch.cuda.is_available():
            print("[Optimizer] WARNING: No CUDA available")
            return False

        # Check VRAM
        allocated, available = self.detect_vram()
        if available < 100:
            print(f"[Optimizer] WARNING: Very low VRAM ({available:.0f}MB)")

        # Test token clamping
        try:
            test_tokens = torch.tensor([0, 5000, 10000])
            clamped = self.clamp_tokens(test_tokens, vocab_size=2048)
            assert clamped.max().item() < 2048
            print("[Optimizer] Token clamping: OK")
        except Exception as e:
            print(f"[Optimizer] ERROR: Token clamping failed: {e}")
            return False

        print("[Optimizer] Self-check complete")
        return True


def main():
    """CLI for optimizer."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA-OJ Autonomous Optimizer")
    parser.add_argument(
        "--report", action="store_true", help="Show optimization report"
    )
    parser.add_argument("--optimize", action="store_true", help="Run optimization")
    parser.add_argument("--check", action="store_true", help="Run self-check")
    parser.add_argument("--metrics", action="store_true", help="Show recent metrics")

    args = parser.parse_args()

    optimizer = AutonomousOptimizer()

    if args.check or (not args.report and not args.optimize):
        optimizer.run_self_check()

    if args.report:
        print(optimizer.get_report())

    if args.optimize:
        config = optimizer.optimize_for_device()
        print(
            f"\n[Optimizer] Applied optimizations for {optimizer.get_vram_tier()} tier"
        )
        print(
            f"Config: batch={config.batch_size}, fp16={config.use_fp16}, efficiency={config.efficiency_mode}"
        )

    if args.metrics:
        if optimizer.metrics:
            print("\nRecent metrics:")
            for m in optimizer.metrics[-5:]:
                print(
                    f"  {m.timestamp}: {m.inference_time_ms:.1f}ms, VRAM={m.vram_used_mb:.0f}MB, OOM={m.oom_count}"
                )


if __name__ == "__main__":
    main()
