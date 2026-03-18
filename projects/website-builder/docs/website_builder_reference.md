# Website Builder Reference Guide

> Complete reference for the website-builder skill

---

## Overview

The website-builder skill generates stunning websites from project materials using AI-powered VibeGraphing methodology.

## Quick Start

### 1. Prepare Materials
Fill out `materials/brief.md` and add supporting materials.

### 2. Generate Website
```bash
cd projects/website-builder
python src/website_generator.py
```

### 3. Review Output
Check `outputs/draft/` for generated files:
- `index.html`
- `styles.css`

### 4. Approve
Copy to `outputs/approved/` for final delivery.

---

## Materials Reference

### Required: brief.md

The project brief is required. See template at `materials/brief.md`.

**Key fields:**
| Field | Description |
|-------|-------------|
| Project Name | Name of your project |
| Business Name | Business name |
| Tagline | Short tagline |
| Target Audience | Who you're building for |
| Services | What you offer |
| Homepage Headline | Main hero headline |
| CTA Button | Call-to-action text |

### Optional: brand/colors.md

Brand colors template at `materials/brand/colors.md`.

**Usage:**
- Define primary, secondary, accent colors
- Auto-applied to generated CSS
- Supports hex colors (#000000 format)

### Optional: content/pages/

Page content in markdown format.

**Supported pages:**
- `home.md` - Homepage content
- `about.md` - About page
- `services.md` - Services page
- `contact.md` - Contact page

**Format:** Standard Markdown with frontmatter

---

## Commands

### Basic Generation
```bash
python src/website_generator.py
```

### Custom Project Directory
```bash
python src/website_generator.py --project /path/to/project
```

### Custom Output Location
```bash
python src/website_generator.py --output outputs/my-site/
```

### Use Specific SPEC
```bash
python src/website_generator.py --spec outputs/draft/SPEC.md
```

---

## Output Files

### Generated Files
| File | Description |
|------|-------------|
| `index.html` | Main HTML file |
| `styles.css` | CSS stylesheet |
| `assets/` | Images, fonts (if included) |

### Output Locations
| Stage | Location |
|-------|----------|
| Draft | `outputs/draft/` |
| Approved | `outputs/approved/` |

---

## Quality Gates

The skill enforces these gates:

- [ ] **brief_filled** - Project brief completed
- [ ] **materials_prepared** - All materials in place
- [ ] **spec_generated** - SPEC.md created
- [ ] **html_created** - HTML/CSS generated
- [ ] **human_approved** - User approved output

---

## Integration with skills_md_maker

This skill integrates with the broader MiRA ecosystem:

1. **Create skill from source**
   ```bash
   /skillm: projects/website-builder
   ```

2. **Generate specification**
   The skill reads `materials/` and creates `SPEC.md`

3. **Generate code**
   Runs `website_generator.py` to produce HTML/CSS

---

## Templates

### brief.md Template

```markdown
# Website Project Brief

## Project Overview
| Field | Your Answer |
|-------|-------------|
| **Project Name** | |
| **Business Name** | |
| **Tagline** | |

## Business Information
### Services/Products
1. 
2. 
3. 

### Target Audience
- Demographics: 
- Pain Points: 
- Goals: 

## Website Requirements
### Pages Needed
- [ ] Homepage
- [ ] About Us
- [ ] Services

## Design Preferences
### Style Vibe
- [ ] Modern/Minimal
- [ ] Professional/Corporate
- [ ] Creative/Artistic

## Content Draft
### Homepage Hero Section
- Headline: 
- Subheadline: 
- CTA Button: 
```

### colors.md Template

```markdown
# Brand Colors

## Primary Colors
| Color | Hex |
|-------|-----|
| Primary | #______ |

## CSS Variables
```css
:root {
  --color-primary: #______;
}
```
```

---

## Examples

### Example 1: Simple Business Website

**materials/brief.md:**
```markdown
Project Name: My Business Site
Business Name: Acme Solutions
Tagline: Professional Services for Everyone
Headline: Build Your Future with Us
CTA Button: Get Started
```

**Generated:** Basic 5-page responsive website

### Example 2: Creative Agency

**materials/brief.md:**
```markdown
Project Name: Creative Agency
Business Name: Design Studio
Tagline: We Create Beautiful Things
Headline: Award-Winning Design Agency
CTA Button: View Our Work
```

**Materials added:**
- `materials/brand/colors.md` - Primary #6366f1
- `materials/content/pages/home.md` - Custom hero

### Example 3: E-commerce Store

**materials/brief.md:**
```markdown
Project Name: Online Store
Business Name: Shop Local
Tagline: Quality Products, Local Delivery
Headline: Shop the Best Products Online
CTA Button: Shop Now
```

**Features included:**
- Product grid
- Cart section
- Contact form

---

## Troubleshooting

### "No brief.md found"
Ensure `materials/brief.md` exists and is filled out.

### "Colors not applying"
Check hex format in `materials/brand/colors.md` - must be 6 digits (#000000)

### "Content not showing"
Page content must be in `materials/content/pages/` with .md extension

---

## File Structure

```
website-builder/
├── docs/
│   ├── index.md
│   ├── quickstart.md
│   └── website_builder_reference.md  ← You are here
├── materials/
│   ├── brief.md              ← REQUIRED
│   ├── brand/
│   │   └── colors.md        ← Optional
│   └── content/
│       └── pages/           ← Optional
├── outputs/
│   ├── draft/               # Generated here
│   └── approved/            # Final output
├── src/
│   └── website_generator.py
└── SKILL.md
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| skills_md_maker | Generate SKILL.md from any source |
| ai-website-builder | AI-powered website creation |

---

*Last updated: 2026-03-15*
*Part of MiRA skill ecosystem*
