---
name: website-builder
description: Generate stunning websites from project materials. Reads brief.md, brand assets, and content, then generates HTML/CSS using AI-powered VibeGraphing methodology.
triggers: [website, build-site, create-site, generate-website, web-design, ai-website]
tools: [read, write, glob, grep, webfetch, codesearch]
quality_gates: [brief_filled, materials_prepared, spec_generated, html_created, human_approved]
persona: "✨ Creative Synthesis — pattern extraction and skill synthesis"
mira_tier: 1
---

## Overview

This skill generates professional websites from your project materials. It follows a standardized workflow for collecting requirements, generating specifications, and producing production-ready HTML/CSS.

## Standard Operating Procedure

### Phase 1: Materials Collection

User provides materials in `materials/` folder:

```
materials/
├── brief.md           # Project requirements (REQUIRED)
├── brand/
│   ├── colors.md     # Brand colors
│   ├── logo.png      # Logo file
│   └── fonts/        # Font files
├── content/
│   └── pages/        # Page content (.md files)
├── templates/         # Design preferences
└── inspiration/       # Reference sites
```

### Phase 2: Specification Generation

Generate `SPEC.md` in `outputs/draft/`:

- Parse brief.md for requirements
- Analyze brand colors and assets
- Process content from pages/
- Generate website specification

### Phase 3: Code Generation

Run website generator:

```bash
python src/website_generator.py --project .
```

Outputs to `outputs/draft/`:
- index.html
- styles.css

### Phase 4: Review & Approval

- Review in `outputs/draft/`
- User approves → Copy to `outputs/approved/`
- User requests changes → Modify materials → Regenerate

## Usage

### 1. Prepare Materials

Fill out `materials/brief.md` template
Add brand assets to `materials/brand/`
Add content to `materials/content/pages/`

### 2. Generate Website

```bash
cd projects/website-builder
python src/website_generator.py
```

### 3. Review Output

Check `outputs/draft/` for:
- index.html
- styles.css

### 4. Approve

Copy to `outputs/approved/` for final delivery

## Quality Gates

- [ ] brief_filled - Project brief completed
- [ ] materials_prepared - All materials in place
- [ ] spec_generated - SPEC.md created
- [ ] html_created - HTML/CSS generated
- [ ] human_approved - User approved the output

## Output Contract

| Output | Location |
|--------|----------|
| SPEC.md | `outputs/draft/SPEC.md` |
| HTML | `outputs/draft/index.html` |
| CSS | `outputs/draft/styles.css` |
| Approved | `outputs/approved/` |

## Examples

See `materials/content/pages/home_example.md` for content template example.

---

*Part of MiRA skill ecosystem*
*Standard operating procedure for website generation*
