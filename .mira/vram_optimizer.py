"""
MIRA-OJ VRAM & Performance Optimizer
AutoResearch findings integrated into MIRA-OJ

Based on experiments on RTX 2060 (6GB VRAM):
- Baseline: depth=4, n_embd=384 = optimal
- Token clamping prevents crashes
- AdamW lr=0.001 is stable
"""

import torch
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DeviceProfile:
    """Device capability profile for MIRA-OJ inference."""

    name: str
    vram_gb: float
    tier: str  # "high", "medium", "low", "minimal"
    recommended_depth: int
    recommended_n_embd: int
    recommended_batch: int
    efficiency_mode: bool = False


def detect_vram() -> float:
    """Detect available VRAM in GB."""
    if not torch.cuda.is_available():
        return 0.0

    try:
        vram_bytes = torch.cuda.get_device_properties(0).total_memory
        return vram_bytes / (1024**3)
    except Exception:
        return 0.0


def get_device_profile(vram_gb: Optional[float] = None) -> DeviceProfile:
    """
    Get optimal device profile based on available VRAM.

    Based on AutoResearch findings:
    - 6GB VRAM: depth=4, n_embd=384 works perfectly
    - VRAM scales with model size quadratically
    """
    if vram_gb is None:
        vram_gb = detect_vram()

    name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"

    # Profile mapping based on experiments
    if vram_gb >= 24:
        return DeviceProfile(
            name=name,
            vram_gb=vram_gb,
            tier="high",
            recommended_depth=12,
            recommended_n_embd=768,
            recommended_batch=16,
            efficiency_mode=False,
        )
    elif vram_gb >= 12:
        return DeviceProfile(
            name=name,
            vram_gb=vram_gb,
            tier="medium",
            recommended_depth=8,
            recommended_n_embd=512,
            recommended_batch=8,
            efficiency_mode=False,
        )
    elif vram_gb >= 6:
        return DeviceProfile(
            name=name,
            vram_gb=vram_gb,
            tier="low",
            recommended_depth=4,
            recommended_n_embd=384,
            recommended_batch=4,
            efficiency_mode=False,
        )
    elif vram_gb >= 2:
        return DeviceProfile(
            name=name,
            vram_gb=vram_gb,
            tier="minimal",
            recommended_depth=2,
            recommended_n_embd=256,
            recommended_batch=1,
            efficiency_mode=True,
        )
    else:
        return DeviceProfile(
            name=name if torch.cuda.is_available() else "CPU",
            vram_gb=0.0,
            tier="cpu",
            recommended_depth=1,
            recommended_n_embd=128,
            recommended_batch=1,
            efficiency_mode=True,
        )


def check_memory_available(required_mb: float) -> bool:
    """Check if required memory is available."""
    if not torch.cuda.is_available():
        return False

    try:
        allocated = torch.cuda.memory_allocated() / (1024**2)
        reserved = torch.cuda.memory_reserved() / (1024**2)
        available = reserved - allocated
        return available >= required_mb
    except Exception:
        return False


def optimize_for_device(profile: DeviceProfile) -> dict:
    """
    Generate optimization parameters based on device profile.

    Based on AutoResearch experiments:
    - Smaller models train faster per step
    - VRAM usage = f(depth, n_embd)
    - batch_size affects throughput
    """
    return {
        "max_depth": profile.recommended_depth,
        "max_n_embd": profile.recommended_n_embd,
        "max_batch": profile.recommended_batch,
        "use_fp16": profile.vram_gb < 12,
        "gradient_checkpointing": profile.vram_gb < 6,
        "efficiency_mode": profile.efficiency_mode,
        "attention_type": "standard" if profile.vram_gb < 24 else "flash",
    }


def format_vram_report() -> str:
    """Generate VRAM status report."""
    profile = get_device_profile()

    report = f"""
╔═══════════════════════════════════════════════════════════╗
║              MIRA-OJ DEVICE PROFILE                      ║
╠═══════════════════════════════════════════════════════════╣
║ Device:     {profile.name:<44} ║
║ VRAM:       {profile.vram_gb:.1f} GB{" " * 38}║
║ Tier:       {profile.tier:<44} ║
╠═══════════════════════════════════════════════════════════╣
║ RECOMMENDED SETTINGS                                     ║
║───────────────────────────────────────────────────────────║
║ Depth:       {profile.recommended_depth}{" " * 42}║
║ Embedding:   {profile.recommended_n_embd}{" " * 42}║
║ Batch:       {profile.recommended_batch}{" " * 42}║
║ FP16:        {"Yes" if profile.vram_gb < 12 else "No":<44} ║
║ Efficiency:  {"Yes" if profile.efficiency_mode else "No":<44} ║
╚═══════════════════════════════════════════════════════════╝
"""
    return report


if __name__ == "__main__":
    print(format_vram_report())
