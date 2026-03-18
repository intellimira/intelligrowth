---
name: cv-builder
description: Comprehensive CV creation workflow that merges multiple CV sources into a complete career library, creates ATS-optimized versions, humanizes content to bypass AI detection, and exports to multiple formats (MD, PDF, DOCX). Use when building professional CVs from multiple source files.
---

# CV Builder Skill

## Overview

This skill creates professional CVs by:
1. Merging multiple CV sources into a complete career library
2. Creating optimized versions (ATS-friendly, comprehensive, full library)
3. Humanizing content to bypass AI detection
4. Exporting to PDF and DOCX formats

## Quick Start

### 1. Gather CV Sources

Scan for CV files in:
- `/home/sir-v/Documents/CV/`
- Check all year folders (2007-2026)
- Include .md and .docx files

### 2. Merge Process

Create `Library_of_Libraries.md`:
- Combine ALL content from all sources
- Preserve original wording exactly
- Keep duplicate achievements (library of libraries)
- Structure: Profiles → Achievements → Skills → Experience → Education

### 3. Create Pass Versions

| Pass | Pages | Purpose |
|------|-------|---------|
| 1-pass | 2 | ATS-optimized, quick apply |
| 6-pass | ~6 | Comprehensive applications |
| Full | ~50+ | Complete archive |

### 4. Humanize (Optional)

Use TextHumanize to bypass AI detection:
```bash
cd /home/sir-v/MiRA
python3 -m venv .venv-humanize
source .venv-humanize/bin/activate
pip install texthumanize
```

Run humanization on narrative text, preserve tables/headers.

### 5. Convert Formats

Use LibreOffice CLI:
```bash
# MD to PDF
libreoffice --headless --convert-to pdf --outdir OUTPUT_DIR INPUT.md

# MD to DOCX
libreoffice --headless --convert-to docx --outdir OUTPUT_DIR INPUT.md
```

## Usage Examples

- "Build a CV from my CV files"
- "Merge all my CVs into one document"
- "Create an ATS-optimized version"
- "Humanize my resume"
- "Make a 6-page comprehensive CV"

## Key Principles

1. **Preserve all content** - Never remove achievements, even if duplicated
2. **Original wording** - Don't rewrite unless humanizing
3. **Clean output** - No footer tags or metadata
4. **Multiple formats** - Always export PDF and DOCX

## Output Location

Default: `/home/sir-v/Documents/CV/Master/`

## See Also

- [ATS Rules](references/ats_rules.md) - Optimization guidelines
- [Grading Framework](references/grading_framework.md) - Industry evaluation criteria
