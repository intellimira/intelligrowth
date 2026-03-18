---
name: ACCT_Dashboard
description: MIRA ecosystem health dashboard. Displays skills status, protocol health, session metrics, and Memory Mesh stats. Integrates with Weave 4.0 dashboard as "MIRA Status" tab.
triggers: [mira status, ecosystem health, skills status, protocol status, dashboard, weave status]
tools: [read_file, glob, bash]
quality_gates: [metrics_displayed, data_fresh, links_valid]
persona: "🔬 Scientific Method — data-driven insights"
mira_tier: 2
---

# ACCT_Dashboard

MIRA's internal dashboard for monitoring ecosystem health.

## Status

**EARMARKED FOR IMPLEMENTATION**

## Integration Points

| Source | Data |
|--------|------|
| `.MIRA/ecosystem_status.md` | Skills, protocols, health scores |
| `revenue-tracker` SQLite | Deals, MRR, P&L |
| `/sessions/` | Session count, recent activity |
| `/skills/` | Skill count by tier/status |
| `/Memory_Mesh/` | Zettel count, storage stats |

## Implementation Roadmap

1. **Phase 1:** Read .MIRA/ecosystem_status.md → render metrics
2. **Phase 2:** Query revenue-tracker SQLite for deal summary
3. **Phase 3:** Count sessions → display activity
4. **Phase 4:** Weave 4.0 tab integration

## Weave 4.0 Dashboard Integration

Add as Tab 9: "MIRA Status"

```html
<!-- Sidebar -->
<div class="nitem" onclick="goTab(this,'mira')"><div class="ni-dot d-ok">M</div><div class="ni-name">MIRA Status</div><div class="ni-badge">ecosystem</div></div>

<!-- Tab -->
<div class="tab" id="ttab-mira" onclick="setTab('mira',this)">MIRA Status</div>

<!-- Panel -->
<div class="panel" id="panel-mira">
  <!-- MIRA Status content -->
</div>
```

## Display Metrics

| Metric | Source | Format |
|--------|--------|--------|
| Core Protocols | ecosystem_status.md | Health % |
| Production Skills | ecosystem_status.md | Count |
| Stub Skills | ecosystem_status.md | Count |
| Active Sessions | /sessions/ | Count |
| Memory Mesh Zettels | Memory_Mesh/zettels/ | Count |
| Total Deals | revenue-tracker | Count + £ |
| MRR | revenue-tracker | £ |

## Output

Generates markdown report or HTML panel for Weave 4.0 dashboard.
