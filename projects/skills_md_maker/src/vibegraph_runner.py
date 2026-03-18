#!/usr/bin/env python3
"""
Vibe Graphing Runner - Main Orchestrator
Two-pass system: Persona Council → Specialization Layer
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from ingest_url import InputClassifier, InputInfo
from ingest_folder import FolderScanner
from aggregate_content import ContentAggregator, AggregatedContent
from persona_council import PersonaCouncil, PersonaCouncilResult
from specialization_layer import SpecializationLayer, SpecialistResult


PROJECT_ROOT = Path(__file__).parent.parent
REFERENCES_DIR = PROJECT_ROOT / "references"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


@dataclass
class VibeGraphResult:
    input_info: InputInfo
    content: AggregatedContent
    persona_council: PersonaCouncilResult
    specialist: SpecialistResult
    skill_name: str
    draft_path: str
    timestamp: str


class VibeGraphRunner:
    def __init__(self):
        self.classifier = InputClassifier()
        self.scanner = FolderScanner()
        self.aggregator = ContentAggregator()
        self.council = PersonaCouncil()
        self.specialization = SpecializationLayer()

    def run(self, user_input: str, skill_name: Optional[str] = None) -> VibeGraphResult:
        print(f"\n{'=' * 60}")
        print("VIBE GRAPHING PIPELINE")
        print(f"{'=' * 60}")

        print(f"\n[1/5] Classifying input...")
        input_info = self.classifier.classify(user_input)
        print(f"  → Type: {input_info.input_type} | Source: {input_info.source}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = REFERENCES_DIR / f"vg_{timestamp}"
        session_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[2/5] Fetching content...")
        if input_info.input_type == "url":
            content = self._fetch_url(input_info, str(session_dir))
        elif input_info.input_type == "folder":
            content = self.aggregator.aggregate(input_info.input_path, str(session_dir))
        elif input_info.input_type == "file":
            content = self.aggregator.aggregate_single_file(
                input_info.input_path, str(session_dir)
            )
        else:
            raise ValueError(f"Unknown input type: {input_info.input_type}")

        print(f"  → Files: {content.file_count} | Type: {content.dominant_type}")

        print(f"\n[3/5] Running Persona Council (Pass 1)...")
        council_result = self.council.analyze(
            content.content, content.dominant_type, content.file_count
        )
        print(f"  → Specialist recommended: {council_result.recommended_specialist}")

        print(f"\n[4/5] Running Specialization Layer (Pass 2)...")
        specialist_result = self.specialization.analyze(
            content.content, council_result.recommended_specialist
        )
        print(f"  → Persona: {specialist_result.persona}")

        final_skill_name = skill_name or self._generate_skill_name(
            input_info, council_result
        )

        print(f"\n[5/5] Generating draft skill...")
        draft_path = self._generate_draft(
            input_info, content, council_result, specialist_result, final_skill_name
        )
        print(f"  → Draft saved: {draft_path}")

        print(f"\n{'=' * 60}")
        print(f"✓ Vibe Graphing Complete!")
        print(f"  Skill: {final_skill_name}")
        print(f"  Draft: {draft_path}")
        print(f"{'=' * 60}\n")

        return VibeGraphResult(
            input_info=input_info,
            content=content,
            persona_council=council_result,
            specialist=specialist_result,
            skill_name=final_skill_name,
            draft_path=draft_path,
            timestamp=timestamp,
        )

    def _fetch_url(self, input_info: InputInfo, session_dir: str) -> AggregatedContent:
        if input_info.url_type == "notebooklm":
            return self._fetch_notebooklm(input_info, session_dir)

        if input_info.url_type == "open_notebook":
            return self._fetch_open_notebook(input_info, session_dir)

        from fetch_content import get_fetch_instructions

        instruction = get_fetch_instructions(input_info.url_type or "")

        print(f"  → Fetching {input_info.url_type} content...")

        content = f"""
Source: {input_info.input_path}
Type: {input_info.url_type}

[Note: Use webfetch/codesearch to fetch actual content]
Fetch instruction: {instruction}
"""

        content_file = Path(session_dir) / "content.md"
        with open(content_file, "w") as f:
            f.write(content)

        return AggregatedContent(
            content=content,
            file_count=1,
            total_size=len(content),
            file_index={"url": input_info.input_path},
            dominant_type=input_info.url_type or "web",
            timestamp=datetime.now().isoformat(),
        )

    def _fetch_notebooklm(self, input_info: InputInfo, session_dir: str):
        import asyncio
        from ingest_notebooklm import NotebookLMIngestor, ingest_notebooklm

        print(f"  → Fetching NotebookLM content...")

        content = asyncio.run(
            ingest_notebooklm(input_info.input_path, str(session_dir))
        )

        content_file = Path(session_dir) / "content.md"
        with open(content_file, "w") as f:
            f.write(content.content)

        return AggregatedContent(
            content=content.content,
            file_count=len(content.sources),
            total_size=len(content.content),
            file_index={
                "notebook_id": content.notebook_id,
                "sources": [s["name"] for s in content.sources],
            },
            dominant_type="notebooklm",
            timestamp=datetime.now().isoformat(),
        )

    def _fetch_open_notebook(self, input_info: InputInfo, session_dir: str):
        from ingest_open_notebook import OpenNotebookIngestor, parse_skillon_command

        print(f"  → Fetching Open Notebook content...")

        names, force_refresh = parse_skillon_command(input_info.input_path)

        ingestor = OpenNotebookIngestor()

        if len(names) == 1:
            nb = ingestor.find_notebook_by_name(names[0])
            if not nb:
                raise ValueError(f"Notebook not found: {names[0]}")
            content = ingestor.fetch_notebook(nb["id"], force_refresh)
        else:
            content = ingestor.fetch_multiple_notebooks(names, force_refresh)

        content_file = Path(session_dir) / "content.md"

        full_content = f"# Open Notebook: {content.notebook_name}\n\n"
        full_content += f"**Notebooks:** {len(names)}\n"
        full_content += f"**Sources:** {len(content.sources)}\n"
        full_content += f"**Chat Messages:** {len(content.chat_history)}\n\n"

        cached_path = ingestor.cache_dir / (
            content.notebook_id.split("+")[0]
            if "+" in content.notebook_id
            else content.notebook_id
        )
        if cached_path.exists():
            cached_content = (cached_path / "content.md").read_text()
            full_content += cached_content
        else:
            full_content += "[Content cached - see references/open_notebook/]"

        with open(content_file, "w") as f:
            f.write(full_content)

        return AggregatedContent(
            content=full_content,
            file_count=len(content.sources),
            total_size=len(full_content),
            file_index={
                "notebook_id": content.notebook_id,
                "sources": [s["name"] for s in content.sources],
            },
            dominant_type="open_notebook",
            timestamp=datetime.now().isoformat(),
        )

    def _generate_skill_name(
        self, input_info: InputInfo, council: PersonaCouncilResult
    ) -> str:
        if input_info.input_type == "folder":
            return Path(input_info.input_path).name.lower().replace(" ", "-")
        elif input_info.input_type == "file":
            return Path(input_info.input_path).stem.lower().replace(" ", "-")
        elif input_info.source:
            return input_info.source.lower().replace(" ", "-")

        return f"skill-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def _generate_draft(
        self,
        input_info: InputInfo,
        content: AggregatedContent,
        council: PersonaCouncilResult,
        specialist: SpecialistResult,
        skill_name: str,
    ) -> str:
        draft_dir = OUTPUTS_DIR / "draft"
        draft_dir.mkdir(parents=True, exist_ok=True)

        draft_file = draft_dir / f"{skill_name}.md"

        triggers = specialist.refined_triggers or council.consolidated_triggers
        tools = specialist.refined_tools or council.consolidated_tools

        draft = f"""---
name: {skill_name}
description: {council.purpose[:100]}
triggers: [{", ".join(triggers[:5]) if triggers else "[]"}]
tools: [{", ".join(tools[:5]) if tools else "[]"}]
quality_gates: [{", ".join(specialist.quality_gates)}]
persona: "{specialist.persona}"
mira_tier: 1
---

## Source
- Input: {input_info.input_path}
- Type: {input_info.input_type}
- Files: {content.file_count}
- Dominant type: {content.dominant_type}

## Persona Council Analysis
- Recommended specialist: {council.recommended_specialist}

### Consolidated Findings
- **Purpose**: {council.purpose}
- **Triggers**: {", ".join(triggers) if triggers else "None identified"}
- **Tools**: {", ".join(tools) if tools else "None identified"}

## Specialist Analysis
- **Specialist**: {specialist.specialist_type}
- **Persona**: {specialist.persona}

### Deep Findings
{json.dumps(specialist.deep_findings, indent=2)[:1000]}

## Hard Rules
{chr(10).join(f"- {rule}" for rule in specialist.hard_rules) if specialist.hard_rules else "- [Add hard rules]"}

## Quality Gates
{chr(10).join(f"- [ ] {gate}" for gate in specialist.quality_gates)}

## Workflow
1. [Define step 1 based on {specialist.specialist_type}]
2. [Define step 2]
3. [Define step 3]

---
*Generated: {datetime.now().isoformat()}*
*Vibe Graphing Pipeline - Two Pass System*
"""

        with open(draft_file, "w") as f:
            f.write(draft)

        return str(draft_file)


def run_vibegraph(user_input: str, skill_name: Optional[str] = None) -> VibeGraphResult:
    runner = VibeGraphRunner()
    return runner.run(user_input, skill_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vibegraph_runner.py <URL or folder path> [skill_name]")
        print("\nExamples:")
        print("  python vibegraph_runner.py /home/sir-v/MiRA/skills/opencode-builder")
        print("  python vibegraph_runner.py https://github.com/BUPT-GAMMA/MASFactory")
        sys.exit(1)

    user_input = sys.argv[1]
    skill_name = sys.argv[2] if len(sys.argv) > 2 else None

    result = run_vibegraph(user_input, skill_name)
