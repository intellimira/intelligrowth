# Lesson 10: AI Agents in Production

## Introduction

As AI agents move from prototypes to production, understanding behavior, monitoring performance, and evaluating outputs becomes critical.

## Observability: Traces and Spans

- **Trace**: Complete agent task from start to finish
- **Span**: Individual steps within the trace

### Key Metrics to Track

| Metric | Description |
|--------|-------------|
| Latency | How quickly does agent respond? |
| Costs | Expense per agent run |
| Request Errors | Failed requests |
| User Feedback | Explicit ratings, comments |
| Implicit Feedback | Repeated queries, retries |
| Accuracy | Correct/desirable outputs |

## Evaluation Categories

### Offline Evaluation
- Controlled setting with test datasets
- Repeatable with clear accuracy metrics
- Part of CI/CD pipelines

### Online Evaluation
- Live, real-world environment
- Monitors real user interactions
- Captures model drift over time

### Combining Both
```
evaluate offline → deploy → monitor online → collect failures → add to offline dataset → refine → repeat
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Inconsistent performance | Refine prompts, divide into subtasks |
| Continuous loops | Clear termination conditions, use reasoning models |
| Poor tool calls | Test tools outside agent, refine parameters |
| Multi-agent inconsistency | Refine prompts, build hierarchical routing |

## Cost Management

1. **Use smaller models** for simpler tasks
2. **Router models** to route by complexity
3. **Cache responses** for common requests

## MIRA Integration Notes

This lesson informs MIRA's:
- **ACCT Dashboard**: Observability and monitoring
- **Sovereign Cockpit**: Real-time system status
- **Self-Anneal Watchdog**: Performance tracking

---
*Source: [Microsoft AI Agents for Beginners - Lesson 10](https://microsoft.github.io/ai-agents-for-beginners/10-ai-agents-production/)*
