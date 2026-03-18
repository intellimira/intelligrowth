# 📋 SHADOW OPS v4.0 DEVELOPMENT TODO

## 🏗 PHASE 1: FOUNDATION & GOVERNANCE
- [x] Initialize `/skills/` directory structure.
- [x] Create `.mira/policies/` and `.mira/scores/` directories.
- [x] Deploy global `AGENT_TOOL_POLICY.json` to `.mira/policies/`.
- [x] Verify `SHADOW_OPS_MANIFEST.md` accuracy in root.

## 🤖 PHASE 2: AGENT DEPLOYMENT
- [x] Hydrate `pain-sentry` (SKILL.md, policy.json).
- [x] Hydrate `pain-scorer` (SKILL.md, policy.json).
- [x] Hydrate `arch-synthesiser` (SKILL.md, policy.json).
- [x] Hydrate `hostile-grounding` (SKILL.md, policy.json, SUBAGENT.md).
- [x] Hydrate `srank-pack-generator` (SKILL.md, policy.json).
- [x] Hydrate `opencode-builder` (SKILL.md, policy.json).
- [x] Hydrate `revenue-tracker` (SKILL.md, policy.json).
- [x] Hydrate `self-anneal-watchdog` (SKILL.md, policy.json).

## ⚔️ PHASE 3: THE HARDENED WEAVE
- [x] Manifest `graph_design.json` MASTER BLUEPRINT.
- [x] Update `mas_run.py` with v4.0 RootGraph and VibeGraph logic.
- [x] Implement MIRA Lineage recording hook.
- [x] Implement Threshold-Based Switch node (Score 72).
- [x] Activate MassGen Consensus logic for Grounding node.

## 🎮 PHASE 4: COMMAND CENTRE
- [x] Initialize `shadow_ops.db` SQLite database.
- [x] Create `deals` table schema.
- [x] Create `lineage` table schema (project and deal tables manifested).
- [x] Deploy `shadow_ops_command_centre.html` to dashboard skill.
- [x] Connect dashboard to live SQLite data feeds.

## 🔄 PHASE 5: BACKTESTING & VALIDATION
- [x] Test Signal: Simulate a "Pain Signal" (Zapier Pricing rant).
- [/] Verification:
    - [ ] Did the Sentry tag it?
    - [ ] Did the Scorer route it correctly?
    - [ ] Did the Grounding node trigger adversarial votes?
    - [ ] Is the result committed to the Lineage Record?
- [ ] Verify the Command Centre visually reflects this test signal in the UI.
