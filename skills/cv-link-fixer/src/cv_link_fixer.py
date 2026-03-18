#!/usr/bin/env python3
"""
CV Link Fixer - Bulk URL Replacement Tool for CV Files

Usage:
    python cv_link_fixer.py --folder /path/to/cvs --old "old-url.com" --new "new-url.com" [--regenerate-pdf] [--dry-run]

Features:
- Scans folders for .md files
- Replaces URLs in content
- Optionally regenerates PDFs via LibreOffice
- Dry-run mode for testing
- Statistics reporting
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class CVLinkFixer:
    def __init__(self, folder: str, old_url: str, new_url: str, dry_run: bool = False):
        self.folder = Path(folder)
        self.old_url = old_url
        self.new_url = new_url
        self.dry_run = dry_run
        self.stats = {
            "files_scanned": 0,
            "files_modified": 0,
            "replacements_total": 0,
            "pdfs_regenerated": 0,
            "errors": [],
        }

    def scan_for_files(self) -> List[Path]:
        """Find all .md files in the folder."""
        if not self.folder.exists():
            raise FileNotFoundError(f"Folder not found: {self.folder}")

        md_files = list(self.folder.rglob("*.md"))
        return md_files

    def count_replacements(self, content: str) -> int:
        """Count occurrences of old URL in content."""
        return content.count(self.old_url)

    def replace_links(self, content: str) -> Tuple[str, int]:
        """Replace old URL with new URL in content."""
        count = content.count(self.old_url)
        new_content = content.replace(self.old_url, self.new_url)
        return new_content, count

    def process_file(self, file_path: Path) -> bool:
        """Process a single file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            replacements = self.count_replacements(content)
            if replacements == 0:
                return False

            self.stats["replacements_total"] += replacements

            if self.dry_run:
                print(
                    f"  [DRY-RUN] Would replace {replacements} occurrence(s) in {file_path.name}"
                )
                return True

            new_content, _ = self.replace_links(content)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"  ✓ Replaced {replacements} occurrence(s) in {file_path.name}")
            return True

        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            self.stats["errors"].append(error_msg)
            print(f"  ✗ {error_msg}")
            return False

    def regenerate_pdf(self, md_file: Path) -> bool:
        """Regenerate PDF from Markdown file using LibreOffice."""
        try:
            pdf_file = md_file.with_suffix(".pdf")

            cmd = [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(md_file.parent),
                str(md_file),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                print(f"  ✓ Generated {pdf_file.name}")
                return True
            else:
                print(f"  ✗ PDF generation failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"  ✗ PDF generation timed out for {md_file.name}")
            return False
        except FileNotFoundError:
            print(f"  ✗ LibreOffice not found. Install it or skip PDF regeneration.")
            return False
        except Exception as e:
            print(f"  ✗ Error generating PDF: {e}")
            return False

    def run(self, regenerate_pdf: bool = False) -> dict:
        """Main execution method."""
        print(f"\n{'=' * 60}")
        print(f"CV Link Fixer")
        print(f"{'=' * 60}")
        print(f"Folder: {self.folder}")
        print(f"Old URL: {self.old_url}")
        print(f"New URL: {self.new_url}")
        print(f"Mode: {'DRY-RUN' if self.dry_run else 'LIVE'}")
        print(f"{'=' * 60}\n")

        md_files = self.scan_for_files()
        self.stats["files_scanned"] = len(md_files)

        print(f"Found {len(md_files)} .md file(s)\n")

        for md_file in md_files:
            modified = self.process_file(md_file)
            if modified:
                self.stats["files_modified"] += 1

                if regenerate_pdf:
                    if self.regenerate_pdf(md_file):
                        self.stats["pdfs_regenerated"] += 1

        self.print_summary()
        return self.stats

    def print_summary(self):
        """Print execution summary."""
        print(f"\n{'=' * 60}")
        print(f"SUMMARY")
        print(f"{'=' * 60}")
        print(f"Files scanned:      {self.stats['files_scanned']}")
        print(f"Files modified:     {self.stats['files_modified']}")
        print(f"Total replacements: {self.stats['replacements_total']}")
        print(f"PDFs regenerated:  {self.stats['pdfs_regenerated']}")

        if self.stats["errors"]:
            print(f"\nErrors ({len(self.stats['errors'])}):")
            for error in self.stats["errors"]:
                print(f"  - {error}")

        print(f"{'=' * 60}\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Bulk URL replacement tool for CV Markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run to see what would be changed
  python cv_link_fixer.py --folder ./cvs --old "old.com" --new "new.com" --dry-run

  # Live run without PDF regeneration
  python cv_link_fixer.py --folder ./cvs --old "old.com" --new "new.com"

  # Live run with PDF regeneration
  python cv_link_fixer.py --folder ./cvs --old "old.com" --new "new.com" --regenerate-pdf

  # Target specific subfolder
  python cv_link_fixer.py --folder "/home/user/Documents/CV/2026" --old "foo.com" --new "bar.com"
        """,
    )

    parser.add_argument(
        "--folder", "-f", required=True, help="Folder containing CV .md files"
    )

    parser.add_argument("--old", "-o", required=True, help="URL pattern to replace")

    parser.add_argument("--new", "-n", required=True, help="New URL to replace with")

    parser.add_argument(
        "--regenerate-pdf",
        "-p",
        action="store_true",
        help="Regenerate PDFs after link replacement",
    )

    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Show what would be changed without making edits",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    fixer = CVLinkFixer(
        folder=args.folder, old_url=args.old, new_url=args.new, dry_run=args.dry_run
    )

    try:
        stats = fixer.run(regenerate_pdf=args.regenerate_pdf)

        if stats["errors"]:
            sys.exit(1)
        else:
            sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(130)


if __name__ == "__main__":
    main()
