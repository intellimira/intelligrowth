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
| DATASET | TinyStories |

---

## Experiment Log

| Date | Commit | val_bpb | VRAM (MB) | Status | Description |
|------|--------|---------|-----------|--------|-------------|
| 2026-03-22 | baseline | TBD | TBD | pending | Baseline run |

---

## Best Results

| Metric | Value | Experiment |
|--------|-------|------------|
| Best val_bpb | - | - |
| Lowest VRAM | - | - |
| Best param efficiency | - | - |

---

## Improvement Ideas

### Tested
- [ ] baseline

### Pending
- [ ] Increase depth (4 → 6)
- [ ] Increase embedding dim (384 → 512)
- [ ] Learning rate sweep
- [ ] Batch size optimization
- [ ] Different activation (SiLU)
- [ ] Weight initialization

---

## Main Branch Candidates

Improvements that worked well and should be integrated:

| Improvement | Status | Notes |
|------------|--------|-------|
| Memory-efficient attention | pending | Would help 6GB cards |
| Mixed precision training | pending | Faster, less VRAM |
| Gradient checkpointing | pending | Enable larger models |
| Dynamic batch sizing | pending | Better utilization |

---

*Updated by: MIRA AutoResearch*
*Last update: 2026-03-22*
