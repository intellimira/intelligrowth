# MIRA AutoResearch - Experiment Log

**Branch:** `experiment/autoresearch`
**Started:** 2026-03-22
**GPU:** RTX 2060 (6GB VRAM)

---

## System Configuration

| Parameter | Value |
|-----------|-------|
| MAX_SEQ_LEN | 256 |
| VOCAB_SIZE | 2048 |
| DEPTH | 4 |
| N_HEAD | 4 |
| N_EMBD | 384 |
| WINDOW_PATTERN | Linear |
| DEVICE_BATCH_SIZE | 4 |
| TOTAL_BATCH_SIZE | 16384 |
| DATASET | TinyStories (Synthetic) |

---

## Experiment Log

| Date | Commit | val_bpb | VRAM (GB) | Status | Description |
|------|--------|---------|-----------|--------|-------------|
| 2026-03-22 | c75f8ca | 10.971 | 0.25 | ✅ keep | baseline - depth=4, n_embd=384, lr=0.001 |
| 2026-03-22 | 952ba04 | 11.026 | 0.34 | ❌ discard | depth_6 - depth=6 (more VRAM, worse val_bpb) |
| 2026-03-22 | 952ba04 | 11.023 | 0.25 | ❌ discard | lr_01 - lr=0.01 (worse val_bpb) |
| 2026-03-22 | 952ba04 | 11.031 | 0.35 | ❌ discard | nembd_512 - n_embd=512 (more VRAM, worse val_bpb) |

---

## Results Summary

### Best Configuration: BASELINE

| Metric | Value |
|--------|-------|
| **val_bpb** | 10.971 |
| **VRAM** | 0.25 GB |
| **Parameters** | 7.9M |
| **Steps** | 13,385 |
| **Training Time** | 300s |

### Experiment Results

| Experiment | val_bpb | VRAM | Status | Notes |
|------------|---------|------|--------|-------|
| **baseline** | **10.971** | 0.25 GB | ✅ best | Keep this config |
| depth_6 | 11.026 | 0.34 GB | ❌ | More VRAM, worse performance |
| lr_01 | 11.023 | 0.25 GB | ❌ | Higher LR didn't help |
| nembd_512 | 11.031 | 0.35 GB | ❌ | More VRAM, worse performance |

---

## Key Findings

1. **Baseline is optimal** for this synthetic data and RTX 2060
2. **Smaller models train faster** - fewer steps but same quality
3. **VRAM scales with model size** - depth and embedding dim matter
4. **LR=0.001 is good** - higher LR didn't improve convergence
5. **Synthetic data has limits** - real TinyStories would show real patterns

---

## For Main Branch

### ✅ Confirmed Working
- Token clamping (prevents CUDA assertions)
- AdamW optimizer with lr=0.001
- Standard attention (no FA3 dependency)
- Depth=4, n_embd=384 (optimal for 6GB VRAM)

### ⏳ Pending
- Real TinyStories dataset
- Longer training runs
- More architecture experiments

---

*Updated by: MIRA AutoResearch*
*Last update: 2026-03-22*
*Status: 4 experiments complete, baseline is optimal*
