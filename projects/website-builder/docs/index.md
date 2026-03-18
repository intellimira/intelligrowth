# website-builder Project

> AI-powered website generation from project materials

---

## Overview

This project provides a standardized workflow for generating stunning websites from your materials. Part of the MiRA skill ecosystem.

---

## Project Structure

```
website-builder/
├── docs/                   # Documentation
├── materials/              # User dumps materials here
│   ├── brief.md           # Project brief template
│   ├── brand/             # Brand assets
│   ├── content/           # Page content
│   ├── templates/          # Design templates
│   └── inspiration/       # Reference sites
├── outputs/
│   ├── draft/            # Generated before approval
│   └── approved/         # Final approved outputs
├── src/
│   └── website_generator.py
├── references/            # Cached sources
├── SKILL.md              # Skill definition
└── TODO.md              # Project tasks
```

---

## Quick Start

### 1. Fill Out Brief
Edit `materials/brief.md` with your project details

### 2. Add Brand Assets
- Colors: `materials/brand/colors.md`
- Logo: `materials/brand/logo.png`
- Fonts: `materials/brand/fonts/`

### 3. Add Content
- Pages: `materials/content/pages/`

### 4. Generate
```bash
python src/website_generator.py
```

### 5. Review & Approve
- Check `outputs/draft/`
- Copy to `outputs/approved/`

---

## Sessions

| Date | Session | Summary |
|------|---------|---------|
| Mar 15 | session_log_20260315_website-builder | Initial project setup |

---

## Standards

This project follows the MiRA session log & project standards:
- Session logs in `docs/`
- Drafts in `outputs/draft/`
- Approved in `outputs/approved/`
- HITL approval before final

---

*Last updated: 2026-03-15*
