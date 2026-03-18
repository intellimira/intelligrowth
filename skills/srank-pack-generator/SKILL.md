---
name:          srank-pack-generator
description:   Generates the full S-Rank Business Pack for GO-verified projects.
               Outputs all 6 documents to projects/<name>/. Revenue model
               included. Feeds data to revenue tracker.
triggers:      [seal, generate business pack, srank, create project pack]
tools:         [gemini_call, ollama_infer, sqlite_write, write_file, read_file]
quality_gates: [all_six_docs_written, revenue_model_populated, hitl_gate_written, sqlite_updated]
persona:       "⚙️ Pragmatic Application — fastest path to actionable output"
mira_tier:     1
---

## Output Documents (all 6 required for GO)
1. PAIN_SIGNAL_BRIEF.md — signal evidence, score breakdown, ICP profile
2. ARCHITECTURE.md — component diagram, tool stack, tier classification
3. ZERO_CAPITAL_PLAN.md — step-by-step £0 build path
4. GROUNDING_REPORT.md — MassGen vote distribution + failure vectors addressed
5. OUTREACH_PACK.md — cold outreach templates for target ICP
6. HITL_GATE.md — human decision prompt (GO/NO-GO with data)

## Revenue Model → SQLite `deals` Table
INSERT into deals:
{
  "deal_id": "<uuid>",
  "project_id": "<fk>",
  "project_name": "<name>",
  "status": "PROSPECT",
  "entry_price_gbp": <float>,
  "mrr_target_gbp": <float>,
  "mrr_actual_gbp": 0,
  "total_revenue_gbp": 0,
  "dev_cost_gbp": 0,
  "gemini_cost_gbp": <float>,
  "profit_gbp": 0,
  "s_rank_score": <int>,
  "created_at": "<ISO8601>",
  "updated_at": "<ISO8601>"
}
