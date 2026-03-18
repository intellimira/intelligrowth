#!/usr/bin/env python3
"""
Website Generator - Creates HTML/CSS from SPEC.md

Reads website specifications from materials/ and outputs:
- index.html
- styles.css
- assets/

Usage:
    python src/website_generator.py
    python src/website_generator.py --spec outputs/draft/SPEC.md
    python src/website_generator.py --output outputs/approved/
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class WebsiteGenerator:
    """Generates HTML/CSS from website specifications"""

    DEFAULT_CSS = """
/* Base Styles */
:root {
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --secondary: #64748b;
  --accent: #f59e0b;
  --background: #ffffff;
  --surface: #f8fafc;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border: #e2e8f0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: var(--text-primary);
  background: var(--background);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header */
header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 1rem 0;
}

header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary);
}

nav ul {
  display: flex;
  list-style: none;
  gap: 2rem;
}

nav a {
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.2s;
}

nav a:hover {
  color: var(--primary);
}

/* Hero */
.hero {
  padding: 4rem 0;
  text-align: center;
  background: var(--surface);
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.hero p {
  font-size: 1.25rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto 2rem;
}

.cta-button {
  display: inline-block;
  background: var(--primary);
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s;
}

.cta-button:hover {
  background: var(--primary-dark);
}

/* Sections */
section {
  padding: 4rem 0;
}

section h2 {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 2rem;
}

/* Services */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.service-card {
  padding: 2rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--surface);
}

.service-card h3 {
  margin-bottom: 1rem;
}

/* Testimonials */
.testimonials {
  background: var(--surface);
}

.testimonial {
  max-width: 600px;
  margin: 0 auto 2rem;
  text-align: center;
}

.testimonial blockquote {
  font-size: 1.25rem;
  font-style: italic;
  margin-bottom: 1rem;
}

.testimonial cite {
  color: var(--text-secondary);
}

/* CTA */
.cta-section {
  background: var(--primary);
  color: white;
  text-align: center;
}

.cta-section h2 {
  color: white;
}

.cta-section .cta-button {
  background: white;
  color: var(--primary);
}

/* Footer */
footer {
  background: var(--text-primary);
  color: white;
  padding: 3rem 0;
  text-align: center;
}

footer a {
  color: white;
  margin: 0 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }
  
  nav ul {
    gap: 1rem;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
}
"""

    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.materials_dir = self.project_dir / "materials"
        self.output_dir = self.project_dir / "outputs" / "draft"

    def load_brief(self) -> dict:
        """Load brief.md and extract key information"""
        brief_path = self.materials_dir / "brief.md"
        if not brief_path.exists():
            return {}

        content = brief_path.read_text()

        # Try simple key: value format first
        result = {}
        for line in content.split("\n"):
            line = line.strip()
            if ":" in line and not line.startswith("#") and not line.startswith("|"):
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()

        return {
            "project_name": result.get("project_name")
            or result.get("Business Name")
            or result.get("Project Name"),
            "business_name": result.get("business_name") or result.get("business name"),
            "tagline": result.get("tagline") or result.get("Tagline/Slogan"),
            "headline": result.get("headline") or result.get("Headline"),
            "subheadline": result.get("subheadline") or result.get("Subheadline"),
            "cta_text": result.get("cta_text")
            or result.get("CTA Button")
            or result.get("button text"),
            "primary_color": result.get("primary_color") or result.get("primary color"),
        }

    def _extract_field(self, content: str, field: str) -> Optional[str]:
        """Extract field value from markdown"""
        pattern = rf"{re.escape(field)}\s*(.+?)(?:\n|$)"
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def load_colors(self) -> dict:
        """Load brand colors from brief.md or brand/colors.md"""
        # First try simple format from brief.md
        brief_path = self.materials_dir / "brief.md"
        if brief_path.exists():
            content = brief_path.read_text()
            colors = {}
            for line in content.split("\n"):
                line = line.strip()
                if (
                    ":" in line
                    and not line.startswith("#")
                    and not line.startswith("|")
                ):
                    key, value = line.split(":", 1)
                    if "color" in key.lower():
                        hex_val = value.strip().replace("#", "")
                        if len(hex_val) == 6:
                            colors[key.lower().replace("_", "").replace(" ", "")] = (
                                "#" + hex_val
                            )

            if colors:
                return {
                    "primary": colors.get("primarycolor") or colors.get("primary"),
                    "secondary": colors.get("secondarycolor")
                    or colors.get("secondary"),
                    "accent": colors.get("accentcolor") or colors.get("accent"),
                }

        # Fall back to brand/colors.md
        colors_path = self.materials_dir / "brand" / "colors.md"
        if not colors_path.exists():
            return {}

        content = colors_path.read_text()
        return {
            "primary": self._extract_hex(content, "Primary | #"),
            "secondary": self._extract_hex(content, "Secondary | #"),
            "accent": self._extract_hex(content, "Accent | #"),
        }

    def _extract_hex(self, content: str, field: str) -> Optional[str]:
        """Extract hex color from markdown"""
        pattern = rf"{re.escape(field)}\s*([0-9a-fA-F]{{6}})"
        match = re.search(pattern, content)
        return f"#{match.group(1)}" if match else None

    def load_content(self) -> dict:
        """Load page content from content/pages/"""
        pages = {}
        pages_dir = self.materials_dir / "content" / "pages"

        if pages_dir.exists():
            for md_file in pages_dir.glob("*.md"):
                if "_example" not in md_file.name:
                    pages[md_file.stem] = md_file.read_text()

        return pages

    def generate_html(self, brief: dict, content: dict) -> str:
        """Generate HTML from brief and content"""
        project_name = brief.get("project_name") or "My Website"
        business_name = brief.get("business_name") or project_name
        headline = brief.get("headline") or f"Welcome to {business_name}"
        subheadline = brief.get("subheadline") or "Professional websites that convert"
        cta_text = brief.get("cta_text") or "Get Started"
        tagline = brief.get("tagline") or ""

        # Extract services from content if available
        services_html = ""
        if "home" in content:
            home_content = content["home"]
            services_html = self._extract_services(home_content)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - {tagline}</title>
    <meta name="description" content="{subheadline}">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">{business_name}</div>
            <nav>
                <ul>
                    <li><a href="#services">Services</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>{headline}</h1>
            <p>{subheadline}</p>
            <a href="#contact" class="cta-button">{cta_text}</a>
        </div>
    </section>

    <section id="services">
        <div class="container">
            <h2>Our Services</h2>
            <div class="services-grid">
                {services_html or self._default_services()}
            </div>
        </div>
    </section>

    <section id="about" class="testimonials">
        <div class="container">
            <h2>About Us</h2>
            <div class="testimonial">
                <blockquote>Helping businesses grow with professional web solutions.</blockquote>
            </div>
        </div>
    </section>

    <section id="contact" class="cta-section">
        <div class="container">
            <h2>Ready to Get Started?</h2>
            <p>Let's build something amazing together.</p>
            <br>
            <a href="#" class="cta-button">Contact Us</a>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; {datetime.now().year} {business_name}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

    def _extract_services(self, content: str) -> str:
        """Extract services section from markdown"""
        # Simple extraction - could be enhanced
        return self._default_services()

    def _default_services(self) -> str:
        """Default services if none provided"""
        return """
            <div class="service-card">
                <h3>Web Design</h3>
                <p>Beautiful, modern website designs tailored to your brand.</p>
            </div>
            <div class="service-card">
                <h3>Development</h3>
                <p>Clean, efficient code that performs beautifully.</p>
            </div>
            <div class="service-card">
                <h3>SEO</h3>
                <p>Get found on Google with our SEO optimization services.</p>
            </div>
        """

    def generate_css(self, colors: dict) -> str:
        """Generate CSS with custom colors"""
        css = self.DEFAULT_CSS

        if colors.get("primary"):
            css = css.replace("#2563eb", colors["primary"])
        if colors.get("accent"):
            css = css.replace("#f59e0b", colors["accent"])

        return css

    def generate(self) -> dict:
        """Generate website files"""
        print(f"Generating website from: {self.project_dir}")

        # Load inputs
        brief = self.load_brief()
        colors = self.load_colors()
        content = self.load_content()

        print(f"  Project: {brief.get('project_name', 'Unknown')}")
        print(f"  Primary color: {colors.get('primary', 'default')}")

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate files
        html = self.generate_html(brief, content)
        css = self.generate_css(colors)

        # Write files
        html_path = self.output_dir / "index.html"
        css_path = self.output_dir / "styles.css"

        html_path.write_text(html)
        css_path.write_text(css)

        print(f"\n✓ Website generated!")
        print(f"  HTML: {html_path}")
        print(f"  CSS: {css_path}")

        return {
            "html": str(html_path),
            "css": str(css_path),
            "project": brief.get("project_name", "website"),
        }


def main():
    parser = argparse.ArgumentParser(description="Generate website from materials")
    parser.add_argument("--project", "-p", default=".", help="Project directory")
    parser.add_argument("--spec", "-s", help="Specific SPEC.md file to use")
    parser.add_argument("--output", "-o", help="Output directory")

    args = parser.parse_args()

    generator = WebsiteGenerator(args.project)

    if args.spec:
        generator.output_dir = Path(args.spec).parent

    if args.output:
        generator.output_dir = Path(args.output)

    result = generator.generate()

    print(f"\nNext steps:")
    print(f"  1. Review output in {generator.output_dir}")
    print(f"  2. If approved, copy to outputs/approved/")
    print(f"  3. Deploy to hosting")


if __name__ == "__main__":
    main()
