---
name:          hostile-grounding
description:   Adversarial 3-subagent MassGen vote on GO/NO-GO. Consensus 2/3.
               Subagents: Regulator, Market Pessimist, Technical Realist.
triggers:      [challenge, stress-test, hostile review, grounding, validate]
tools:         [gemini_call, sqlite_write, write_file, read_file]
quality_gates: [all_three_votes_cast, consensus_reached, failure_vectors_listed, regulatory_checked]
persona:       "🌑 Dark Passenger — assumption challenger, chaos identifier"
mira_tier:     1
---
