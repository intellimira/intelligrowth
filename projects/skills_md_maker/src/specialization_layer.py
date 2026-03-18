"""
Specialization Layer - Pass 2 of Vibe Graphing
Specialized agents for deep extraction based on Persona Council findings
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class SpecialistResult:
    specialist_type: str
    deep_findings: Dict[str, Any]
    refined_triggers: List[str]
    refined_tools: List[str]
    quality_gates: List[str]
    hard_rules: List[str]
    persona: str
    confidence: float


SPECIALIST_PROMPTS = {
    "code_analyzer": {
        "name": "Code Analysis Specialist",
        "focus": "Programming patterns, APIs, and code structure",
        "prompt": """You are a Code Analysis Specialist. Analyze this codebase and extract:

1. **Primary Language(s)**: What language(s) are used?
2. **Key Functions/APIs**: What are the main entry points?
3. **Dependencies**: What libraries/frameworks?
4. **Code Patterns**: What patterns (MVC, functional, etc.)?
5. **File Structure**: How is code organized?

Provide JSON:
{
  "language": "primary language",
  "frameworks": ["list"],
  "apis": ["key functions"],
  "patterns": ["patterns used"],
  "structure": "directory structure summary"
}""",
    },
    "doc_analyzer": {
        "name": "Documentation Specialist",
        "focus": "README, docs, and user-facing content",
        "prompt": """You are a Documentation Specialist. Analyze these docs and extract:

1. **Purpose**: What does this project do?
2. **Usage**: How is it used?
3. **Key Features**: What are the main features?
4. **Examples**: Any usage examples?
5. **Audience**: Who is this for?

Provide JSON:
{
  "purpose": "one sentence",
  "usage": "how to use",
  "features": ["key features"],
  "examples": ["examples"],
  "audience": "target users"
}""",
    },
    "data_analyzer": {
        "name": "Data Schema Specialist",
        "focus": "Data structures, schemas, and models",
        "prompt": """You are a Data Schema Specialist. Analyze this data and extract:

1. **Data Types**: What kinds of data?
2. **Schemas**: Any structured schemas?
3. **Storage**: How is data stored?
4. **Transformations**: Any data processing?
5. **Models**: Any data models?

Provide JSON:
{
  "data_types": ["types"],
  "schemas": ["schema definitions"],
  "storage": "how stored",
  "transformations": ["processing steps"],
  "models": ["data models"]
}""",
    },
    "config_analyzer": {
        "name": "Configuration Specialist",
        "focus": "Config files, settings, and environment",
        "prompt": """You are a Configuration Specialist. Analyze this config and extract:

1. **Settings**: What configurable options?
2. **Environment**: Env vars needed?
3. **Defaults**: Default values?
4. **Secrets**: Any sensitive config?

Provide JSON:
{
  "settings": ["config options"],
  "env_vars": ["required env vars"],
  "defaults": {"key": "default value"},
  "secrets": ["sensitive items"]
}""",
    },
    "script_analyzer": {
        "name": "Script Analysis Specialist",
        "focus": "Scripts, automation, and CLI tools",
        "prompt": """You are a Script Analysis Specialist. Analyze this script/code and extract:

1. **Purpose**: What does the script do?
2. **Usage**: How is it run?
3. **Inputs**: What inputs needed?
4. **Outputs**: What does it produce?

Provide JSON:
{
  "purpose": "what it does",
  "usage": "how to run",
  "inputs": ["required inputs"],
  "outputs": ["produced outputs"]
}""",
    },
    "web_analyzer": {
        "name": "Web Content Specialist",
        "focus": "Web content, HTML, and frontend",
        "prompt": """You are a Web Content Specialist. Analyze this web content and extract:

1. **Content Type**: What kind of content?
2. **Key Information**: What are the main points?
3. **Structure**: How is it organized?
4. **Interactivity**: Any dynamic elements?

Provide JSON:
{
  "content_type": "type of content",
  "key_info": ["main points"],
  "structure": "how organized",
  "interactivity": "dynamic elements"
}""",
    },
    "general_analyzer": {
        "name": "General Analysis Specialist",
        "focus": "Generic content analysis",
        "prompt": """You are a General Analysis Specialist. Analyze this content and extract:

1. **Topic**: What is this about?
2. **Key Points**: Main takeaways?
3. **Format**: What format is this?
4. **Context**: Any context clues?

Provide JSON:
{
  "topic": "main topic",
  "key_points": ["list"],
  "format": "content format",
  "context": "any context"
}""",
    },
}


class SpecializationLayer:
    def __init__(self):
        self.specialists = SPECIALIST_PROMPTS

    def select_specialist(
        self, content_type: str, persona_council_recommendation: str
    ) -> str:
        specialist_map = {
            "code": "code_analyzer",
            "document": "doc_analyzer",
            "data": "data_analyzer",
            "config": "config_analyzer",
            "script": "script_analyzer",
            "web": "web_analyzer",
            "empty": "general_analyzer",
            "unknown": "general_analyzer",
        }

        if persona_council_recommendation in self.specialists:
            return persona_council_recommendation

        return specialist_map.get(content_type, "general_analyzer")

    def analyze(self, content: str, specialist_type: str) -> SpecialistResult:
        if specialist_type not in self.specialists:
            specialist_type = "general_analyzer"

        specialist = self.specialists[specialist_type]

        content_sample = content[:20000]

        try:
            from masfactory.utils.llm import ollama_chat

            full_prompt = f"""{specialist["prompt"]}

CONTENT TO ANALYZE:
---
{content_sample}
---

Respond ONLY with valid JSON."""

            response = ollama_chat(
                prompt=full_prompt,
                model="llama3.2",
                system="You are a JSON-only response bot.",
            )

            data = json.loads(response)

            refined_triggers = self._extract_triggers(data, specialist_type)
            refined_tools = self._extract_tools(data, specialist_type)
            quality_gates = self._generate_quality_gates(data, specialist_type)
            hard_rules = self._generate_hard_rules(data, specialist_type)
            persona = self._select_persona(data, specialist_type)

            return SpecialistResult(
                specialist_type=specialist_type,
                deep_findings=data,
                refined_triggers=refined_triggers,
                refined_tools=refined_tools,
                quality_gates=quality_gates,
                hard_rules=hard_rules,
                persona=persona,
                confidence=0.8,
            )

        except Exception as e:
            return SpecialistResult(
                specialist_type=specialist_type,
                deep_findings={"error": str(e)},
                refined_triggers=[],
                refined_tools=[],
                quality_gates=[],
                hard_rules=[],
                persona="⚙️ Pragmatic Application",
                confidence=0.0,
            )

    def _extract_triggers(self, findings: Dict, specialist: str) -> List[str]:
        triggers = []

        if specialist == "code_analyzer":
            if "apis" in findings:
                triggers.extend(findings.get("apis", [])[:3])
            if "frameworks" in findings:
                triggers.extend(
                    [f"build-{f}" for f in findings.get("frameworks", [])[:2]]
                )

        elif specialist == "doc_analyzer":
            if "features" in findings:
                triggers.extend(findings.get("features", [])[:3])

        elif specialist == "data_analyzer":
            if "data_types" in findings:
                triggers.extend(findings.get("data_types", [])[:3])

        return list(set(triggers))[:10]

    def _extract_tools(self, findings: Dict, specialist: str) -> List[str]:
        tools = []

        if specialist == "code_analyzer":
            if "frameworks" in findings:
                tools.extend(findings.get("frameworks", []))

        elif specialist == "config_analyzer":
            if "env_vars" in findings:
                tools.append("env_reader")
            tools.append("config_parser")

        return list(set(tools))[:10]

    def _generate_quality_gates(self, findings: Dict, specialist: str) -> List[str]:
        gates = ["analysis_complete"]

        if specialist == "code_analyzer":
            gates.append("code_valid")
            gates.append("dependencies_resolved")
        elif specialist == "config_analyzer":
            gates.append("config_valid")
            gates.append("secrets_secured")

        return gates

    def _generate_hard_rules(self, findings: Dict, specialist: str) -> List[str]:
        rules = []

        if specialist == "config_analyzer":
            secrets = findings.get("secrets", [])
            if secrets:
                rules.append("Never commit secrets to version control")

        return rules

    def _select_persona(self, findings: Dict, specialist: str) -> str:
        persona_map = {
            "code_analyzer": "⚙️ Pragmatic Application",
            "doc_analyzer": "✨ Creative Synthesis",
            "data_analyzer": "🔬 Scientific Method",
            "config_analyzer": "🌑 The Dark Passenger",
            "script_analyzer": "⚙️ Pragmatic Application",
            "web_analyzer": "✨ Creative Synthesis",
            "general_analyzer": "🤔 Philosophical Inquiry",
        }

        return persona_map.get(specialist, "⚙️ Pragmatic Application")

    def to_json(self, result: SpecialistResult) -> str:
        return json.dumps(asdict(result), indent=2)


def run_specialization(content: str, specialist_type: str) -> SpecialistResult:
    layer = SpecializationLayer()
    return layer.analyze(content, specialist_type)


if __name__ == "__main__":
    test_content = """
    def build_project(name):
        # Build a new project
        pass
    
    def run_tests():
        # Run tests
        pass
    """

    result = run_specialization(test_content, "code_analyzer")
    print(SpecializationLayer().to_json(result))
