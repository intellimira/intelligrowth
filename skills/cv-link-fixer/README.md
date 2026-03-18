# CV Link Fixer

Bulk URL replacement tool for CV Markdown files. Scans folders for `.md` files, replaces URLs, and optionally regenerates PDFs.

## Features

- 🔍 Scans folders recursively for `.md` files
- 🔄 Bulk URL/pattern replacement
- 📄 Optional PDF regeneration via LibreOffice
- 🧪 Dry-run mode for safe testing
- 📊 Detailed statistics reporting

## Installation

```bash
# Clone or download this repository
git clone https://github.com/yourusername/cv-link-fixer.git
cd cv-link-fixer

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

## Usage

### Basic Command

```bash
python src/cv_link_fixer.py --folder /path/to/cvs --old "old-url.com" --new "new-url.com"
```

### With PDF Regeneration

```bash
python src/cv_link_fixer.py \
  --folder /path/to/cvs \
  --old "old-url.com" \
  --new "new-url.com" \
  --regenerate-pdf
```

### Dry Run (Preview)

```bash
python src/cv_link_fixer.py \
  --folder /path/to/cvs \
  --old "old-url.com" \
  --new "new-url.com" \
  --dry-run
```

## Command-Line Options

| Flag | Short | Description | Required |
|------|-------|-------------|----------|
| `--folder` | `-f` | Folder containing CV .md files | Yes |
| `--old` | `-o` | URL/text to replace | Yes |
| `--new` | `-n` | Replacement URL/text | Yes |
| `--regenerate-pdf` | `-p` | Regenerate PDFs after changes | No |
| `--dry-run` | `-d` | Preview without making changes | No |
| `--verbose` | `-v` | Enable verbose output | No |

## Examples

### Example 1: Fix Portfolio Link

```bash
python src/cv_link_fixer.py \
  --folder ~/Documents/CV/Master \
  --old "intelligrowthai.com" \
  --new "linkedin.com/company/intelligrowthai" \
  --regenerate-pdf
```

### Example 2: Update Company Name

```bash
python src/cv_link_fixer.py \
  --folder ~/Documents/CV \
  --old "OldCompany Ltd" \
  --new "NewCompany Inc"
```

### Example 3: Scan Only (No Changes)

```bash
python src/cv_link_fixer.py \
  --folder ~/Documents/CV/2026 \
  --old "example.com" \
  --new "replacement.com" \
  --dry-run
```

## Output Example

```
============================================================
CV Link Fixer
============================================================
Folder: /home/user/Documents/CV/Master
Old URL: intelligrowthai.com
New URL: linkedin.com/company/intelligrowthai
Mode: LIVE
============================================================

Found 4 .md file(s)

  ✓ Replaced 1 occurrence(s) in Randolph_Dube_1_Pass.md
  ✓ Replaced 1 occurrence(s) in Randolph_Dube_1_Pass_Humanized.md
  ✓ Replaced 1 occurrence(s) in Randolph_Dube_6_Pass.md
  ✓ Replaced 1 occurrence(s) in Randolph_Dube_Library_of_Libraries.md
  ✓ Generated Randolph_Dube_1_Pass.pdf
  ✓ Generated Randolph_Dube_1_Pass_Humanized.pdf
  ✓ Generated Randolph_Dube_6_Pass.pdf
  ✓ Generated Randolph_Dube_Library_of_Libraries.pdf

============================================================
SUMMARY
============================================================
Files scanned:      4
Files modified:      4
Total replacements: 4
PDFs regenerated:   4
============================================================
```

## Requirements

- Python 3.8+
- LibreOffice (optional, for PDF regeneration)

No external Python packages required - uses only standard library.

## Use Cases

1. **Portfolio Link Updates** - Fix broken/old portfolio URLs
2. **Company Rebranding** - Update company names across all CVs
3. **Contact Info Changes** - Bulk update email/phone/links
4. **URL Normalization** - Add/remove https://, www, trailing slashes

## Integrating with MIRA

This tool is designed to work with the MIRA personal AI assistant. Place in:

```
/home/sir-v/MiRA/skills/cv-link-fixer/
```

Load via: `load skill cv-link-fixer`

## License

MIT License - Free to use and modify.

## Author

Created as part of the MIRA (Modular Intelligence Reinforcement Architecture) ecosystem.
