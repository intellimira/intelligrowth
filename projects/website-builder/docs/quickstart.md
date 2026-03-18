# Website Builder - Quick Start

> Generate a stunning website in 5 minutes

---

## Step 1: Prepare Your Materials

### Option A: Use Template
Open `materials/brief.md` and fill in your details.

### Option B: Use Example
Copy `materials/content/pages/home_example.md` to `materials/content/pages/home.md` and customize.

---

## Step 2: Run the Generator

```bash
cd /home/sir-v/MiRA/projects/website-builder
python src/website_generator.py
```

---

## Step 3: Review Output

Your generated website is in `outputs/draft/`:
- `index.html` - Open in browser
- `styles.css` - Your custom styles

---

## Step 4: Approve or Iterate

### If you like it:
Copy to approved:
```bash
cp outputs/draft/index.html outputs/approved/
cp outputs/draft/styles.css outputs/approved/
```

### If you want changes:
1. Update materials (brief.md, colors.md, content)
2. Run generator again
3. Review new output

---

## What's Included

### Default Features
- Responsive design (mobile-friendly)
- Hero section with headline & CTA
- Services section
- About section
- Contact/CTA section
- Footer

### Customization Options
- Brand colors
- Custom content per page
- Multiple pages

---

## Example: Quick Business Site

### 1. Fill brief.md
```markdown
| Field | Value |
|-------|-------|
| Project Name | My Business |
| Business Name | John's Plumbing |
| Tagline | Trusted Service Since 1985 |
| Headline | Professional Plumbing Services |
| CTA Button | Call Now |
```

### 2. Run
```bash
python src/website_generator.py
```

### 3. Done!
Open `outputs/draft/index.html` in your browser.

---

## Need Help?

See `docs/website_builder_reference.md` for complete documentation.

---

*5 minutes to your first website!*
