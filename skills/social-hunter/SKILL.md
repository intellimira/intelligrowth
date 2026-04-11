---
name: social-hunter
description: Autonomous lead signal extraction from Reddit, Hacker News, and Indie Hackers. Self-improving scout with sentiment analysis and pain-point detection. Use when identifying high-friction user aches for MicroSaaS opportunity validation.
---

# Social-Hunter: Intent-Based Warm Lead Scout

**ACCT v1.6.3 Sovereign Implementation**  
**Integration:** MIRA Ecosystem

## Core Mandate

Autonomous discovery and validation of high-friction pain points across community platforms. The "Canabalise" protocol finds the "ache"—specific, recurring, and economically impactful problems that users are desperate to solve.

## Architecture

```
Scout Config (JSON) → Cron Job → Sentiment Analysis → Lead Signals → Memory Mesh
                                    ↓
                          Self-Improvement Loop
```

## Components

### 1. Scout Configuration (`scout_config.json`)
Defines target platforms, queries, and thresholds:
- **Reddit:** r/SaaS, r/Trading, r/Entrepreneur
- **Hacker News:** hn.algolia.com
- **Indie Hackers:** indiehackers.com

### 2. Cron Job (`social_hunter_cron.py`)
- Hourly execution for high-priority scouts
- Self-improving query mutation
- Telemetry to Memory Mesh

### 3. Sentiment Analysis
Uses `analyze_sentiment.py` to score:
- Urgency (time/money loss)
- Complexity (manual workarounds)
- Frustration (emotional language)

## Commands

### Run Social-Hunter Manually
```bash
cd /home/sir-v/MiRA/docs/MiRA_Search_Canabalise
python3 social_hunter_cron.py
```

### Install Cron Job
```bash
# Add to crontab
crontab -e

# Add line for hourly execution:
0 * * * * cd /home/sir-v/MiRA/docs/MiRA_Search_Canabalise && python3 social_hunter_cron.py >> /home/sir-v/MiRA/docs/MiRA_Search_Canabalise/social_hunter.log 2>&1
```

### Check Lead Signals
```bash
cat /home/sir-v/MiRA/Memory_Mesh/lead_signals.json
```

### View Web Voyage Log
```bash
cat /home/sir-v/MiRA/Memory_Mesh/web_voyage_log.json
```

## Self-Improvement Logic

If yield < 10%:
1. Expand queries with emotional keywords
2. Add new keyword categories (frustration, loss, wish, desperation)
3. Re-run scout with mutated queries

## Integration Points

| Target | MIRA Component |
|--------|---------------|
| Lead Signals | `Memory_Mesh/lead_signals.json` |
| Telemetry | `Memory_Mesh/web_voyage_log.json` |
| Scoring | `pain_scorer` skill |
| Outreach | `shadow-ops-prover` skill |

## Scout Status

| Scout | Target | Frequency | Status |
|-------|--------|-----------|--------|
| SaaS_Struggles | reddit.com/r/SaaS | hourly | ✅ Active |
| Dev_Pain | news.ycombinator.com | daily | ✅ Active |
| Solopreneur_Friction | indiehackers.com | daily | ✅ Active |
| Trader_Tilt | reddit.com/r/Trading | hourly | ✅ Active |
| Home_Care_Turnover | reddit.com/r/homehealthcare | daily | ✅ Active |
| Lead_Gen_Pain | reddit.com/r/Entrepreneur | hourly | ✅ Active |

---

*Powered by ACCT Sovereign v1.6.3*
