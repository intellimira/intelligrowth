#!/usr/bin/env python3
"""
Convert MD files to PDF and DOCX using LibreOffice.
"""

import subprocess
import sys
import os


def convert_md(input_path, output_format, output_dir=None):
    """
    Convert MD file to PDF or DOCX using LibreOffice.

    Args:
        input_path: Path to input .md file
        output_format: 'pdf' or 'docx'
        output_dir: Directory for output (default: same as input)
    """
    if output_dir is None:
        output_dir = os.path.dirname(input_path)

    filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(filename)[0]

    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to",
        output_format,
        "--outdir",
        output_dir,
        input_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        output_file = os.path.join(output_dir, f"{name_without_ext}.{output_format}")
        print(f"✓ Converted to {output_format}: {output_file}")
        return output_file
    else:
        print(f"✗ Conversion failed: {result.stderr}")
        return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python convert_formats.py <input.md> <pdf|docx> [output_dir]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_format = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    if output_format not in ["pdf", "docx"]:
        print("Format must be 'pdf' or 'docx'")
        sys.exit(1)

    convert_md(input_file, output_format, output_dir)


if __name__ == "__main__":
    main()
