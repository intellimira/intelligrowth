# MIRA Shadow Ops - Infrastructure Orchestration

## Overview

This document defines how MIRA orchestrates Shadow Ops lines of business through infrastructure automation.

## The Shadow Ops Lines of Business

| LOB | Skill | Function | Current Run Method |
|-----|-------|-----------|---------------------|
| **Enquiry Pipeline** | email-automation | Gmail → Score → Alert | cron (poll_enquiries.py) |
| **Social Hunter** | social-hunter | Reddit/HN/Indie leads | Manual |
| **Revenue Tracker** | revenue-tracker | Deals P&L tracking | Manual |
| **Shadow Ops Prover** | shadow-ops-prover | 7-stage monetization | Manual |
| **S-Rank Generator** | srank-pack-generator | Business documents | Manual |
| **Pain Scorer** | pain-scorer | Signal evaluation | On-demand |

## Infrastructure Orchestration Layer

### Level 1: Basic Cron (Current)
```
cron → individual scripts → results
```

### Level 2: Coordinated Orchestration (Paperclip-style)
```
┌─────────────────────────────────────┐
│   orchestrator.py (Central Hub)     │
│   - Runs on schedule                 │
│   - Coordinates all LOBs             │
│   - Logs to The Weave                │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│   LOB Workers (4 parallel)           │
│   - enquiry_pipeline.py              │
│   - social_hunter.py                 │
│   - revenue_tracker.py               │
│   - shadow_ops_prover.py             │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│   Results Aggregation                │
│   - Central log                      │
│   - HITL notification                │
│   - The Weave integration             │
└─────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Create Orchestrator (Python)
- Central coordinator script
- Parallel execution of LOB workers
- Results aggregation
- Logging to The Weave

### Phase 2: LOB Worker Scripts
- Standardized interface for each LOB
- Input/Output contract
- Error handling
- HITL triggers

### Phase 3: Schedule Integration
- Cron-based triggering
- Manual trigger capability
- HITL approval gates

## File Structure

```
Memory_Mesh/
├── orchestrator.py          # Central coordination
├── lob_workers/             # LOB-specific scripts
│   ├── enquiry_pipeline.py
│   ├── social_hunter.py
│   ├── revenue_tracker.py
│   └── shadow_ops_prover.py
├── weavers/                 # The Weave integration
│   └── log_integration.py
└── cron_schedule.py          # Schedule configuration
```

## Run Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **auto** | cron | Runs all LOBs, logs results |
| **select** | manual | Choose specific LOBs |
| **watch** | manual | Real-time monitoring |
| **test** | manual | Dry-run validation |

## HITL Integration

- **Major findings:** Alert user for approval
- **Errors:** Stop and notify
- **Success:** Log to Weave silently

---

*Orchestration layer serves the sovereign - MIRA decides what runs, when, and how.*