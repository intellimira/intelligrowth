---
name:          revenue-tracker
description:   Tracks revenue, costs, and profit per deal. Reads/writes the
               deals SQLite table. Called by dashboard and Gemini CLI queries.
               Also calculates portfolio-level P&L.
triggers:      [track revenue, update deal, profit, MRR, P&L, financial summary]
tools:         [sqlite_read, sqlite_write, read_file, write_file]
quality_gates: [profit_calculated, deal_status_valid, mrr_updated, p_and_l_accurate]
persona:       "⚙️ Pragmatic Application — accurate numbers, zero drama"
mira_tier:     1
---

## Status Progression
PROSPECT → ARCH_COMPLETE → GROUNDED → HITL_PENDING → GO → BUILD_COMPLETE → LAUNCHED → MRR_ACTIVE → CHURNED

## P&L Calculation
profit_gbp = total_revenue_gbp - dev_cost_gbp - gemini_cost_gbp - infra_cost_gbp
roi_pct = (profit_gbp / total_cost_gbp) * 100
