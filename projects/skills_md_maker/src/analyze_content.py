import json
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class SkillAnalysis:
    name: str
    description: str
    triggers: List[str]
    tools: List[str]
    quality_gates: List[str]
    persona: str
    mira_tier: int
    hard_rules: List[str]
    patterns: List[str]
    conventions: List[str]


ANALYSIS_PROMPT_TEMPLATE = """You are analyzing content to extract skill metadata for an AI agent skill system.

## Source Content
{content}

## Your Task
Extract the following metadata from the content above. Return ONLY valid JSON.

## Required Fields

1. **name**: kebab-case skill name (e.g., "github-repo-analyzer")
2. **description**: 1-2 sentence description of what this skill does
3. **triggers**: List of keywords that should activate this skill (e.g., ["analyze", "github", "repo"])
4. **tools**: List of tools this skill uses (e.g., ["webfetch", "grep", "read"])
5. **quality_gates**: List of success criteria (e.g., ["analysis_complete", "json_valid"])
6. **persona**: Persona Council role (⚛️ First Principles, 🔬 Scientific Method, 🤔 Philosophical Inquiry, ✨ Creative Synthesis, ⚙️ Pragmatic Application, 🌑 The Dark Passenger)
7. **mira_tier**: Integer 1-3 (1=basic, 2=moderate complexity, 3=advanced)
8. **hard_rules**: List of hard constraints this skill must follow
9. **patterns**: Key patterns this skill implements
10. **conventions**: Code/file conventions this skill follows

## Output Format
Return ONLY a JSON object with these fields. Nothing else.

## Example Output
```json
{{
  "name": "youtube-transcriber",
  "description": "Transcribes YouTube videos and extracts key insights",
  "triggers": ["transcribe", "youtube", "video"],
  "tools": ["webfetch", "codesearch"],
  "quality_gates": ["transcript_obtained", "summary_generated"],
  "persona": "🔬 Scientific Method",
  "mira_tier": 1,
  "hard_rules": ["Never store personal data", "Use only public APIs"],
  "patterns": ["extract-then-summarize"],
  "conventions": ["output to markdown", "json metadata header"]
}}
```

Now analyze the content and return JSON:"""


def generate_analysis_prompt(content: str, url_type: str) -> str:
    """Generate the analysis prompt for the LLM"""
    return ANALYSIS_PROMPT_TEMPLATE.format(content=content[:8000])


def parse_analysis_response(response: str) -> Optional[SkillAnalysis]:
    """Parse the LLM response into a SkillAnalysis object"""
    try:
        data = json.loads(response)

        return SkillAnalysis(
            name=data.get("name", "unnamed-skill"),
            description=data.get("description", ""),
            triggers=data.get("triggers", []),
            tools=data.get("tools", []),
            quality_gates=data.get("quality_gates", []),
            persona=data.get("persona", "⚙️ Pragmatic Application"),
            mira_tier=data.get("mira_tier", 1),
            hard_rules=data.get("hard_rules", []),
            patterns=data.get("patterns", []),
            conventions=data.get("conventions", []),
        )
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")

        import re

        json_match = re.search(r"\{[\s\S]*\}", response)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return SkillAnalysis(
                    name=data.get("name", "unnamed-skill"),
                    description=data.get("description", ""),
                    triggers=data.get("triggers", []),
                    tools=data.get("tools", []),
                    quality_gates=data.get("quality_gates", []),
                    persona=data.get("persona", "⚙️ Pragmatic Application"),
                    mira_tier=data.get("mira_tier", 1),
                    hard_rules=data.get("hard_rules", []),
                    patterns=data.get("patterns", []),
                    conventions=data.get("conventions", []),
                )
            except:
                pass

        return None


def generate_skill_name(url: str, url_type: str) -> str:
    """Generate a default skill name from URL if LLM fails"""
    import re
    from pathlib import Path

    if url_type == "github":
        match = re.search(r"github\.com/([\w-]+)/([\w-]+)", url)
        if match:
            return f"{match.group(1)}-{match.group(2)}".lower()

    if url_type == "youtube":
        match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
        if match:
            return f"youtube-{match.group(1)}"

    if url_type == "reddit":
        match = re.search(r"reddit\.com/r/([\w-]+)", url)
        if match:
            return f"reddit-{match.group(1)}"

    parsed = Path(url)
    return f"skill-{parsed.stem[:30]}".lower().replace(" ", "-")


if __name__ == "__main__":
    test_content = """
    # MASFactory
    
    A graph-centric framework for orchestrating Multi-Agent Systems with Vibe Graphing.
    
    ## Features
    - Natural language intent compilation
    - Editable workflow specification
    - Executable graph generation
    - Human-in-the-loop interaction
    """

    prompt = generate_analysis_prompt(test_content, "github")
    print(prompt[:500])
    print("...")
