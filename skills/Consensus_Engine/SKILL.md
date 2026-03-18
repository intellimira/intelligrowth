---
name: Consensus_Engine
description: Multi-persona decision-making system. Aggregates opinions from Persona Council members to reach consensus on complex decisions.
triggers: [consensus, vote, decide, multi-persona, council decision]
tools: [read_file, write_file, bash]
quality_gates: [personas_consulted, vote_recorded, consensus_reached]
persona: "🤔 Philosophical Inquiry — weighted decision making"
mira_tier: 2
---

# Consensus_Engine

Multi-persona decision-making for MIRA.

## Status

**EARMARKED FOR IMPLEMENTATION**

## Purpose

Enable structured decision-making by aggregating Persona Council opinions:
- Present decision to multiple personas
- Weight each persona's input
- Reach consensus or identify dissent

## Persona Weights (Default)

| Persona | Weight | Decision Type |
|---------|--------|---------------|
| First Principles | 1.0 | Foundational decisions |
| Scientific Method | 1.0 | Evidence-based decisions |
| Philosophical Inquiry | 0.8 | Ethical considerations |
| Creative Synthesis | 0.6 | Innovation decisions |
| Pragmatic Application | 1.0 | Implementation decisions |
| The Dark Passenger | 0.7 | Strategic intuition |

## Implementation

### Phase 1: Stub
- Define consensus algorithm
- Document API
- Create voting mechanism

### Phase 2: Basic Implementation
- Prompt each persona for input
- Aggregate responses
- Calculate weighted consensus

### Phase 3: Full Implementation
- Parallel persona queries
- Dissent detection
- Confidence scoring

## Usage

```bash
# Query consensus
python consensus.py "Should we implement Vector_Mesh now?"

# Output
# First Principles: YES (confidence: 0.9)
# Scientific Method: YES (confidence: 0.8)
# Philosophical Inquiry: YES (confidence: 0.7)
# ...
# CONSENSUS: YES (confidence: 0.82)
```

## Integration

| Component | Integration Point |
|-----------|------------------|
| UTO Workflow | Decision points in execution |
| skills_md_maker | Skill approval decisions |
| sovereign_shadow_operator | Strategic decisions |

## Consensus Types

| Type | Threshold | Use Case |
|------|-----------|----------|
| Simple Majority | >50% | Minor decisions |
| Strong Consensus | >75% | Standard decisions |
| Unanimous | 100% | Critical decisions |
