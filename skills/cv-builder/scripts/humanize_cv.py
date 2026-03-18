#!/usr/bin/env python3
"""
Humanize CV text using TextHumanize library.
Bypasses AI detection for resumes.
"""

import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from texthumanize import humanize
import re


def should_humanize(line):
    """Determine if a line should be humanized."""
    stripped = line.strip()

    # Skip these types of lines
    if not stripped:
        return False
    if stripped.startswith("#"):
        return False  # Headers
    if stripped.startswith("|"):
        return False  # Tables
    if stripped.startswith("- ") and len(stripped) < 50:
        return False  # Short bullets
    if re.match(r"\|[\s\-:]+\|", stripped):
        return False  # Table separators

    return True


def humanize_cv_file(input_path, output_path):
    """Humanize a CV file, preserving structure."""

    with open(input_path, "r") as f:
        content = f.read()

    lines = content.split("\n")
    processed_lines = []

    for line in lines:
        if should_humanize(line):
            try:
                result = humanize(line)
                processed_lines.append(result.text)
            except Exception as e:
                print(f"Warning: Failed to humanize line: {e}")
                processed_lines.append(line)
        else:
            processed_lines.append(line)

    output = "\n".join(processed_lines)

    with open(output_path, "w") as f:
        f.write(output)

    print(f"Humanization complete!")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python humanize_cv.py <input.md> <output.md>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    humanize_cv_file(input_file, output_file)
