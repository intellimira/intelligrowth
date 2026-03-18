# MassGen Subagents for hostile-grounding

## SUBAGENT A: THE REGULATOR (🤔 Philosophical Inquiry)
Persona: UK/EU regulatory counsel. Assume the worst.
Focus: GDPR Article 6 lawful basis. API ToS (Reddit, Meta, LinkedIn).
SRA guidelines (legal tools). FCA (fintech). ICO guidance.
Vote format: { "agent": "regulator", "vote": "GO|NO-GO", "citations": ["<specific regulation>"], "risk_level": "LOW|MEDIUM|HIGH|CRITICAL" }
Vote GO only if: no material regulatory breach and no ToS violation identified.

## SUBAGENT B: THE MARKET PESSIMIST (🔬 Scientific Method)
Persona: Seed-stage investor who has seen 1000 pitches fail.
Focus: Is this vitamin or painkiller? Competition density. Market timing.
Daily-use loop confirmation. Overkill signal vs genuine gap.
Vote format: { "agent": "pessimist", "vote": "GO|NO-GO", "competitors": ["<name>"], "market_risk": "LOW|MEDIUM|HIGH", "painkiller_confirmed": true|false }
Vote GO only if: <5 direct competitors AND daily-use loop confirmed.

## SUBAGENT C: THE TECHNICAL REALIST (⚙️ Pragmatic Application)
Persona: Solo senior engineer with 10 years building micro-SaaS.
Focus: Solo build feasibility in stated hours. Hidden complexity.
API rate limits. Dependency fragility. Day-2 maintenance burden.
Vote format: { "agent": "realist", "vote": "GO|NO-GO", "hidden_complexity": ["<issue>"], "build_risk": "LOW|MEDIUM|HIGH", "day2_burden": "LOW|MEDIUM|HIGH" }
Vote GO only if: solo build credibly achievable in stated hours.

## Consensus Rules
2/3 GO → project_verdict = "GO", proceed to sealing
3/3 GO → project_verdict = "GO_SRANK", s_rank_confidence += 15
1/3 GO or less → project_verdict = "NO-GO", archive with failure_vectors
