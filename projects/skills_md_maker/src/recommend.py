#!/usr/bin/env python3
"""
CLI tool for skill recommendations
Usage: python recommend.py "task description"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from search_skills import search_skills, print_results, SearchResult


def format_for_opencode(results: list[SearchResult]) -> str:
    """Format results for OpenCode display"""
    if not results:
        return "No skills found matching your query."

    lines = ["## Skill Recommendations\n"]

    for i, r in enumerate(results, 1):
        score_pct = int(r.score * 100)
        lines.append(f"### {i}. {r.name} ({score_pct}% match)")
        lines.append(f"**Description:** {r.description}")
        lines.append(f"**Triggers:** {', '.join(r.triggers) if r.triggers else 'none'}")
        lines.append(f"**Tools:** {', '.join(r.tools) if r.tools else 'none'}")
        lines.append(f"**Persona:** {r.persona}")
        lines.append(f"**File:** `{r.file_path}`")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print('Usage: python recommend.py "task description"')
        print("\nExamples:")
        print('  python recommend.py "validate a SaaS idea"')
        print('  python recommend.py "build a project"')
        print('  python recommend.py "analyze code"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    print(f"Searching for: {query}\n")

    results = search_skills(query, top_k=5)

    print_results(results)

    print("\n--- For OpenCode ---\n")
    print(format_for_opencode(results))


if __name__ == "__main__":
    main()
