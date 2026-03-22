---
name: autoresearch
description: Autonomous AI research framework using Karpathy's AutoResearch methodology. Runs self-improving LLM training experiments and integrates results into Memory_Mesh. Use when optimizing MIRA capabilities, exploring LLM improvements, or running autonomous experiments.
triggers: [autoresearch, experiment, train, LLM, optimize model, autonomous research]
tools: [bash, read_file, glob, write_file]
---

# MIRA AutoResearch Skill

Autonomous LLM research framework integrated with MIRA's Memory_Mesh.

## Overview

This skill enables MIRA to:
- Run autonomous LLM training experiments
- Track results in Memory_Mesh
- Identify improvements for main branch
- Optimize MIRA's own capabilities

## System Configuration

| Component | Specification |
|-----------|---------------|
| **GPU** | NVIDIA RTX 2060 (6GB VRAM) |
| **Model** | TinyStories dataset |
| **Framework** | PyTorch + Custom training |
| **Time Budget** | 5 minutes per experiment |

## Directory Structure

```
experiments/
└── autoresearch/
    ├── prepare_rtx2060.py    # Data preparation
    ├── train_rtx2060.py      # Training script
    ├── config_rtx2060.yaml   # Configuration
    └── results.tsv           # Experiment log
```

## Commands

### Setup
```bash
cd /home/sir-v/MiRA/experiments/autoresearch
python3 prepare_rtx2060.py
```

### Run Experiment
```bash
cd /home/sir-v/MiRA/experiments/autoresearch
python3 train_rtx2060.py
```

### Check Results
```bash
cd /home/sir-v/MiRA/experiments/autoresearch
cat results.tsv
```

## Memory_Mesh Integration

### Auto-Logging

After each experiment, the skill:
1. Logs results to `experiments/autoresearch/results.tsv`
2. Creates a zettel in `Memory_Mesh/zettels/` for significant findings
3. Updates the experiment index in Memory_Mesh

### Results Format

```tsv
commit	val_bpb	memory_gb	status	description
a1b2c3d	1.234567	4.5	keep	baseline
b2c3d4e	1.220000	4.6	keep	increased depth to 6
```

## Experiment Loop

```
1. Propose hypothesis
2. Modify train_rtx2060.py
3. Run 5-minute training
4. Evaluate val_bpb (lower is better)
5. If improved → keep change
6. If worse → discard
7. Log to Memory_Mesh
8. Repeat
```

## Optimization Ideas to Explore

### High Priority (RTX 2060 Friendly)
- [ ] Learning rate tuning (0.01 → 0.02, 0.005)
- [ ] Depth adjustment (4 → 6 layers)
- [ ] Embedding dimension scaling
- [ ] Batch size optimization
- [ ] Weight initialization strategies

### Medium Priority
- [ ] Different activation functions (GELU vs SiLU)
- [ ] Learning rate scheduling (cosine, warmup)
- [ ] Gradient clipping tuning
- [ ] Weight decay optimization

### Low Priority (VRAM Heavy)
- [ ] Attention mechanism variations
- [ ] Residual connections
- [ ] Layer normalization position

## Edge Case Improvements

### For Main Branch
Improvements that can be pulled into main MIRA:

| Improvement | Benefit | Complexity |
|-------------|---------|------------|
| **Memory-efficient attention** | Reduce VRAM for all models | Medium |
| **Mixed precision training** | Faster training | Low |
| **Gradient checkpointing** | Enable larger models | Medium |
| **Dynamic batch sizing** | Better GPU utilization | Low |
| **Early stopping heuristics** | Save compute | Low |

## Monitoring

### Watchdog Integration
The watchdog monitors for new experiments and:
- Triggers Weave cycle
- Updates experiment index
- Notifies of significant findings

### Log Files
- `experiments/autoresearch/run.log` - Training output
- `Memory_Mesh/weave_watchdog.log` - Weave activity
- `Memory_Mesh/experiments/` - Zettels for each experiment

## Usage Examples

### Start New Experiment
```
Start a new experiment to try depth 6 layers.
```

### Check Progress
```
Show me the current experiment results.
```

### Pull Improvements
```
What improvements should we pull to main branch?
```

### Optimize MIRA
```
Help me optimize MIRA's vector search using insights from experiments.
```

## Status

| Component | Status |
|-----------|--------|
| Framework | ✅ Ready |
| Data Prep | ⏳ Run prepare_rtx2060.py first |
| Training | ⏳ Ready to experiment |
| Memory_Mesh | ✅ Integrated |

---
**Version:** 1.0
**Date:** 2026-03-22
**Branch:** experiment/autoresearch
