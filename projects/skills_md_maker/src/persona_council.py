"""
Persona Council - Pass 1 of Vibe Graphing
Multi-perspective analysis using the Persona Council framework
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class PersonaAnalysis:
    persona: str
    perspective: str
    findings: List[str]
    recommendations: List[str]
    confidence: float


@dataclass
class PersonaCouncilResult:
    input_type: str
    dominant_type: str
    file_count: int
    analyses: List[PersonaAnalysis]
    consolidated_triggers: List[str]
    consolidated_tools: List[str]
    purpose: str
    recommended_specialist: str
    timestamp: str


PERSONA_PROMPTS = {
    "first_principles": {
        "name": "⚛️ First Principles",
        "perspective": "Ground truth - What exactly exists in this content?",
        "prompt": """You are the First Principles analyst. Your job is to establish ground truth.

Analyze the following content and identify:
1. What files/components exist?
2. What is the core functionality?
3. What are the absolute fundamentals?

Respond in JSON:
{
  "findings": ["list of fundamental findings"],
  "recommendations": ["what must be preserved"],
  "confidence": 0.0-1.0
}""",
    },
    "scientific_method": {
        "name": "🔬 Scientific Method",
        "perspective": "Pattern detection - What recurring patterns exist?",
        "prompt": """You are the Scientific Method analyst. Your job is to find patterns.

Analyze the following content and identify:
1. What patterns recur across files?
2. What tools/dependencies are used?
3. What conventions are followed?

Respond in JSON:
{
  "findings": ["list of patterns found"],
  "recommendations": ["tools and patterns to capture"],
  "confidence": 0.0-1.0
}""",
    },
    "philosophical_inquiry": {
        "name": "🤔 Philosophical Inquiry",
        "perspective": "Purpose - What should this skill accomplish?",
        "prompt": """You are the Philosophical Inquiry analyst. Your job is to understand purpose.

Analyze the following content and identify:
1. What problem does this solve?
2. What is the intended outcome?
3. What value does it provide?

Respond in JSON:
{
  "findings": ["list of purposes identified"],
  "recommendations": ["how to frame the skill description"],
  "confidence": 0.0-1.0
}""",
    },
    "creative_synthesis": {
        "name": "✨ Creative Synthesis",
        "perspective": "Integration - How do we combine findings into skill?",
        "prompt": """You are the Creative Synthesis analyst. Your job is to create a coherent skill.

Analyze the following content and identify:
1. What triggers should activate this skill?
2. What is the best description?
3. What persona fits best?

Respond in JSON:
{
  "findings": ["synthesis elements"],
  "recommendations": ["triggers, description, persona"],
  "confidence": 0.0-1.0
}""",
    },
    "pragmatic_application": {
        "name": "⚙️ Pragmatic Application",
        "perspective": "Validation - Will this skill actually work?",
        "prompt": """You are the Pragmatic Application analyst. Your job is to validate feasibility.

Analyze the following content and identify:
1. What quality gates are needed?
2. What tools are available?
3. What could fail?

Respond in JSON:
{
  "findings": ["potential issues"],
  "recommendations": ["quality gates, validations"],
  "confidence": 0.0-1.0
}""",
    },
    "dark_passenger": {
        "name": "🌑 The Dark Passenger",
        "perspective": "Edge cases - What could go wrong?",
        "prompt": """You are the Dark Passenger analyst. Your job is to find failure modes.

Analyze the following content and identify:
1. What are the security concerns?
2. What edge cases exist?
3. What should be hard-coded as rules?

Respond in JSON:
{
  "findings": ["risks and edge cases"],
  "recommendations": ["hard rules to add"],
  "confidence": 0.0-1.0
}""",
    },
}


SPECIALIST_MAPPING = {
    "code": "code_analyzer",
    "document": "doc_analyzer",
    "data": "data_analyzer",
    "config": "config_analyzer",
    "script": "script_analyzer",
    "web": "web_analyzer",
    "empty": "general_analyzer",
}


class PersonaCouncil:
    def __init__(self, personas: Optional[List[str]] = None):
        if personas is None:
            personas = [
                "first_principles",
                "scientific_method",
                "philosophical_inquiry",
                "creative_synthesis",
                "pragmatic_application",
            ]

        self.personas = personas
        self.prompts = PERSONA_PROMPTS

    def analyze(
        self, content: str, content_type: str, file_count: int
    ) -> PersonaCouncilResult:
        analyses = []

        content_sample = content[:15000]

        for persona_key in self.personas:
            if persona_key in self.prompts:
                prompt_data = self.prompts[persona_key]
                analysis = self._run_persona(
                    persona_key,
                    prompt_data["name"],
                    prompt_data["perspective"],
                    prompt_data["prompt"],
                    content_sample,
                )
                analyses.append(analysis)

        consolidated = self._consolidate(analyses)
        recommended_specialist = self._get_specialist(content_type)

        return PersonaCouncilResult(
            input_type=content_type,
            dominant_type=content_type,
            file_count=file_count,
            analyses=analyses,
            consolidated_triggers=consolidated["triggers"],
            consolidated_tools=consolidated["tools"],
            purpose=consolidated["purpose"],
            recommended_specialist=recommended_specialist,
            timestamp=datetime.now().isoformat(),
        )

    def _run_persona(
        self, key: str, name: str, perspective: str, prompt: str, content: str
    ) -> PersonaAnalysis:
        full_prompt = f"""{prompt}

CONTENT TO ANALYZE:
---
{content}
---

Respond ONLY with valid JSON. No other text."""

        try:
            from masfactory.utils.llm import ollama_chat

            response = ollama_chat(
                prompt=full_prompt,
                model="llama3.2",
                system="You are a JSON-only response bot. Always respond with valid JSON.",
            )

            data = json.loads(response)

            return PersonaAnalysis(
                persona=name,
                perspective=perspective,
                findings=data.get("findings", []),
                recommendations=data.get("recommendations", []),
                confidence=data.get("confidence", 0.5),
            )
        except Exception as e:
            return PersonaAnalysis(
                persona=name,
                perspective=perspective,
                findings=[f"Analysis failed: {str(e)}"],
                recommendations=[],
                confidence=0.0,
            )

    def _consolidate(self, analyses: List[PersonaAnalysis]) -> Dict[str, Any]:
        triggers = []
        tools = []
        purposes = []

        for analysis in analyses:
            for rec in analysis.recommendations:
                if any(kw in rec.lower() for kw in ["trigger", "activate", "keyword"]):
                    triggers.append(rec)
                if any(kw in rec.lower() for kw in ["tool", "use", "require"]):
                    tools.append(rec)
                if any(kw in rec.lower() for kw in ["purpose", "description", "value"]):
                    purposes.append(rec)

        return {
            "triggers": list(set(triggers))[:10],
            "tools": list(set(tools))[:10],
            "purpose": purposes[0] if purposes else "Skill extracted from content",
        }

    def _get_specialist(self, content_type: str) -> str:
        return SPECIALIST_MAPPING.get(content_type, "general_analyzer")

    def to_json(self, result: PersonaCouncilResult) -> str:
        return json.dumps(asdict(result), indent=2)


def run_persona_council(
    content: str, content_type: str, file_count: int
) -> PersonaCouncilResult:
    council = PersonaCouncil()
    return council.analyze(content, content_type, file_count)


if __name__ == "__main__":
    test_content = """
    # OpenCode Builder Skill
    
    This skill builds code using OpenCode.
    
    ## Tools
    - opencode_run
    - ollama_infer
    - read_file
    - write_file
    
    ## Triggers
    - build, code, implement, manifest
    """

    result = run_persona_council(test_content, "code", 5)
    print(PersonaCouncil().to_json(result)[:1000])
