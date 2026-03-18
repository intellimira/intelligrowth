#!/usr/bin/env python3
"""
Job Description Fetcher

Fetches job descriptions from various job boards.
Supports: Indeed, Jobsite, Adzuna, LinkedIn, Reed, CWJobs, etc.

Usage:
    python job_fetcher.py "https://jobsite.co.uk/job/12345"
    python job_fetcher.py --file jobs.txt
"""

import argparse
import re
import sys
import urllib.request
import urllib.error
from html import unescape
from typing import Optional, Dict


class JobFetcher:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch(self, url: str) -> Dict[str, str]:
        """Fetch job description from URL."""
        print(f"Fetching: {url}")

        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                html = response.read().decode("utf-8", errors="ignore")

            return self.parse(html, url)

        except urllib.error.HTTPError as e:
            return {"error": f"HTTP Error: {e.code}", "url": url}
        except urllib.error.URLError as e:
            return {"error": f"URL Error: {e.reason}", "url": url}
        except Exception as e:
            return {"error": str(e), "url": url}

    def parse(self, html: str, url: str) -> Dict[str, str]:
        """Parse job description from HTML."""
        job = {
            "url": url,
            "title": self.extract_title(html),
            "company": self.extract_company(html),
            "location": self.extract_location(html),
            "description": self.extract_description(html),
            "requirements": self.extract_requirements(html),
            "salary": self.extract_salary(html),
        }
        return job

    def extract_title(self, html: str) -> str:
        """Extract job title."""
        patterns = [
            r"<h1[^>]*>([^<]+)</h1>",
            r"<title>([^<]+)</title>",
            r'"jobTitle"\s*:\s*"([^"]+)"',
            r'class="job-title[^"]*"[^>]*>([^<]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return unescape(match.group(1).strip())
        return "Unknown Title"

    def extract_company(self, html: str) -> str:
        """Extract company name."""
        patterns = [
            r'"companyName"\s*:\s*"([^"]+)"',
            r'class="company[^"]*"[^>]*>([^<]+)',
            r"<span[^>]*>([^<]+)</span>",
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return unescape(match.group(1).strip())
        return "Unknown Company"

    def extract_location(self, html: str) -> str:
        """Extract job location."""
        patterns = [
            r'"jobLocation"\s*:\s*"([^"]+)"',
            r'class="location[^"]*"[^>]*>([^<]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return unescape(match.group(1).strip())
        return "Unknown Location"

    def extract_description(self, html: str) -> str:
        """Extract job description."""
        # Try to find job description content
        patterns = [
            r'class="description[^"]*"[^>]*>(.*?)</div>',
            r'class="job-details[^"]*"[^>]*>(.*?)</',
            r"<article[^>]*>(.*?)</article>",
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                desc = self.clean_html(match.group(1))
                if len(desc) > 100:
                    return desc[:3000]

        # Fallback: return a portion of HTML
        return "Could not extract description. Please check manually."

    def extract_requirements(self, html: str) -> str:
        """Extract job requirements."""
        patterns = [
            r"requirements?[:\s](.*?)(?:experience|benefits|about)",
            r"qualifications?[:\s](.*?)(?:experience|benefits)",
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                return self.clean_html(match.group(1))[:1000]
        return ""

    def extract_salary(self, html: str) -> str:
        """Extract salary information."""
        patterns = [
            r"£[0-9,]+(?:\s*-\s*£[0-9,]+)?(?:\s*(?:per|p)/?(?:year|day|hour|annum))?",
            r"\$\d+(?:,\d{3})*(?:\s*-\s*\$?\d+(?:,\d{3})*)?(?:\s*(?:per|p)/?(?:year|hour))?",
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return match.group(0)
        return "Not specified"

    def clean_html(self, text: str) -> str:
        """Clean HTML tags and entities."""
        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", text)
        # Decode HTML entities
        text = unescape(text)
        # Clean whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text


def main():
    parser = argparse.ArgumentParser(description="Fetch job descriptions from URLs")
    parser.add_argument("url", nargs="?", help="Job URL to fetch")
    parser.add_argument("--file", "-f", help="File containing URLs (one per line)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    fetcher = JobFetcher()
    urls = []

    if args.file:
        with open(args.file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    elif args.url:
        urls = [args.url]
    else:
        print("Error: Provide URL or --file")
        sys.exit(1)

    for url in urls:
        job = fetcher.fetch(url)

        if args.json:
            import json

            print(json.dumps(job, indent=2))
        else:
            print(f"\n{'=' * 60}")
            print(f"Title: {job.get('title', 'N/A')}")
            print(f"Company: {job.get('company', 'N/A')}")
            print(f"Location: {job.get('location', 'N/A')}")
            print(f"Salary: {job.get('salary', 'N/A')}")
            print(f"{'=' * 60}")
            print(f"Description:\n{job.get('description', 'N/A')[:1000]}")
            print()


if __name__ == "__main__":
    main()
