

============================================================
FILE: policy.json
TYPE: data
============================================================

{
  "opencode-builder": {
    "allowed_tools": ["opencode_run", "ollama_infer", "read_file", "write_file", "run_tests"],
    "deny_tools":    ["send_email", "http_post", "git_push", "deploy", "delete_file", "gemini_call"]
  }
}


============================================================
FILE: SKILL.md
TYPE: document
============================================================

---
name:          opencode-builder
description:   Manifests the MVP codebase via OpenCode after HITL GO.
               Ollama reviews output for security + ToS. Never deploys.
triggers:      [build, code, implement, manifest, generate codebase]
tools:         [opencode_run, ollama_infer, read_file, write_file, run_tests]
quality_gates: [no_hardcoded_secrets, tier0_deps_only, tests_written, readme_exists, ollama_review_passed]
persona:       "⚙️ Pragmatic Application — working code, minimum viable"
mira_tier:     1
---

## Hard Rules
1. Never git_push or deploy. Human deploys after review.
2. NEVER merge Build Model and Invoke Model roles.
3. All secrets via .env + python-dotenv. .env in .gitignore.
4. After generation: Ollama reviews for (a) hardcoded secrets, (b) API ToS violations, (c) missing error handling, (d) non-TIER-0 dependencies.

## Output Contract
Write to projects/<PROJECT_NAME>/src/
Write test results to .mira/scores/lineage.json
Update deals table: status → "BUILD_COMPLETE"
