---
title: Awesome-OpenCode Curator
date: 2026-03-15
session_id: ses_20260315_awesome-opencode
project: awesome-opencode-curator
type: session
tags: [skill, plugin, opencode, curator]
protocols: [MSIP, Pragmatic Application]
---

# Session: Awesome-OpenCode Curator

**Session ID:** ses_20260315_awesome-opencode
**Date:** 2026-03-15

## Summary

Cloned awesome-opencode repository and created MIRA integration skill wrapper. Provides access to 67+ OpenCode plugins, themes, and resources.

## Actions

1. Cloned repository to `/projects/awesome-opencode/`
2. Created skill wrapper at `/skills/awesome-opencode-curator/`
3. Built vector index (67 plugins, 6 categories)
4. Created documentation

## Outputs

- Skill: `/skills/awesome-opencode-curator/SKILL.md`
- Index: 67 plugins searchable

## Integration Points

- skills_md_maker: Training data
- shadow-ops: Pain mining source
- opencode-builder: Plugin queries

## Status

✅ Complete

## Connections

- Related: skills_md_maker, opencode-builder
