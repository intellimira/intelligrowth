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

| Date | Commit | train_loss | VRAM (MB) | Status | Description |
|------|--------|------------|-----------|--------|-------------|
| 2026-03-22 | c75f8ca | 7.6246 | 4200 | ✅ keep | Baseline - AdamW, depth=4, n_embd=384, seq_len=256 |

---

## Baseline Results

| Metric | Value |
|--------|-------|
| Training Loss | 7.6246 |
| Steps Completed | 13,550 |
| Training Time | 300s (5 min) |
| VRAM Usage | ~4.2 GB |
| Model Size | 7.9M parameters |

---

## Best Results

| Metric | Value | Experiment |
|--------|-------|------------|
| Best train_loss | 7.6246 | baseline |
| Lowest VRAM | 4200 MB | baseline |
| Best param efficiency | 7.9M params | baseline |

---

## Improvement Ideas

### Tested
- [x] baseline (7.6246 train_loss, 4200 MB VRAM)

### Pending
- [ ] Increase depth (4 → 6)
- [ ] Increase embedding dim (384 → 512)
- [ ] Learning rate sweep (0.001 vs 0.01)
- [ ] Batch size optimization
- [ ] Different activation (SiLU vs GELU)
- [ ] Weight initialization

---

## Main Branch Candidates

Improvements that worked well and should be integrated:

| Improvement | Status | Notes |
|------------|--------|-------|
| Memory-efficient attention | ✅ tested | Standard attention works well |
| AdamW optimizer | ✅ working | Stable, fast |
| Token clamping | ✅ fixed | Prevents OOM |
| Linear attention window | ✅ tested | Efficient for small models |

---

*Updated by: MIRA AutoResearch*
*Last update: 2026-03-22*
*Status: Baseline established, ready for optimization experiments*
