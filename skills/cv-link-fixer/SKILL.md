---
name: cv-link-fixer
description: Bulk URL replacement tool for CV Markdown files. Scans folders for .md files, replaces URLs, optionally regenerates PDFs. Use when updating portfolio links, company URLs, or any bulk text replacement across multiple CV files.
---

# CV Link Fixer Skill

## Overview

A reusable tool for bulk URL replacement across multiple CV files. Part of the CV Builder ecosystem but can be used independently.

## Quick Start

### Within MIRA

```bash
# Load the skill
load skill cv-link-fixer

# Fix links in a CV folder
fix-links in /home/sir-v/Documents/CV/Master from intelligrowthai.com to linkedin.com/company/intelligrowthai

# With PDF regeneration
fix-links in /Documents/CV/2026 from old.com to new.com --regenerate-pdf
```

### As Standalone CLI

```bash
# Navigate to skill folder
cd /home/sir-v/MiRA/skills/cv-link-fixer/src

# Dry run first (recommended)
python cv_link_fixer.py --folder /path/to/cvs --old "old.com" --new "new.com" --dry-run

# Live run
python cv_link_fixer.py --folder /path/to/cvs --old "old.com" --new "new.com"

# With PDF regeneration
python cv_link_fixer.py --folder /path/to/cvs --old "old.com" --new "new.com" --regenerate-pdf
```

## Commands

| Command | Description |
|---------|-------------|
| `fix-links in <folder> from <old> to <new>` | Replace URLs in all .md files |
| `fix-links scan <folder>` | Scan and report URL occurrences without changing |
| `fix-links dry-run <folder> from <old> to <new>` | Preview changes without applying |

## Options

| Flag | Description |
|------|-------------|
| `--folder, -f` | Target folder containing CV files |
| `--old, -o` | URL pattern to find |
| `--new, -n` | URL replacement |
| `--regenerate-pdf, -p` | Regenerate PDFs after changes |
| `--dry-run, -d` | Preview without making changes |

## Examples

### Example 1: Fix Portfolio Link

```bash
python cv_link_fixer.py \
  --folder /home/sir-v/Documents/CV/Master \
  --old "intelligrowthai.com" \
  --new "linkedin.com/company/intelligrowthai" \
  --regenerate-pdf
```

### Example 2: Update Company Name Across All CVs

```bash
python cv_link_fixer.py \
  --folder /home/sir-v/Documents/CV \
  --old "OldCompany Ltd" \
  --new "NewCompany Inc" \
  --regenerate-pdf
```

### Example 3: Dry Run

```bash
python cv_link_fixer.py \
  --folder /home/sir-v/Documents/CV/2026 \
  --old "example.com" \
  --new "newdomain.co.uk" \
  --dry-run
```

## Integration with CV Builder

This skill works alongside the CV Builder skill:

1. **CV Builder** - Creates CVs from multiple sources
2. **CV Link Fixer** - Updates URLs after CV creation
3. **Workflow**:
   ```
   Create CVs → Identify URL issues → Use cv-link-fixer → Done
   ```

## Requirements

- Python 3.8+
- LibreOffice (optional, for PDF regeneration)

## File Structure

```
cv-link-fixer/
├── SKILL.md                    # This file
├── src/
│   └── cv_link_fixer.py         # Core CLI tool
├── templates/
│   └── sample_config.yaml       # Example configuration
└── README.md                    # GitHub documentation
```

## Error Handling

- **Folder not found**: Returns error with path
- **No matches**: Reports "0 files modified"
- **LibreOffice missing**: Skips PDF regeneration with warning
- **Permission errors**: Reports which files failed

## Notes

- Only processes `.md` files
- Recursively scans subfolders
- Preserves all other content unchanged
- Case-sensitive matching
