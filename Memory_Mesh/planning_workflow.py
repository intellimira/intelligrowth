#!/usr/bin/env python3
"""
MIRA Planning Workflow (gstack-inspired)
Adopts gstack's planning methodology: office-hours → plan-* → execution.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuration
MIRA_ROOT = Path("/home/sir-v/MiRA")
PLANNING_LOG = MIRA_ROOT / "Memory_Mesh" / "planning_workflow.jsonl"

# Planning Categories (gstack-inspired)
PLANNING_CATEGORIES = {
    "office-hours": {
        "description": "Strategic planning - big picture thinking",
        "template": "office_hours_template.md",
        "frequency": "weekly",
    },
    "plan-ceo-review": {
        "description": "Executive-level strategic review",
        "template": "ceo_review_template.md",
        "frequency": "weekly",
    },
    "plan-eng-review": {
        "description": "Engineering/planning work review",
        "template": "eng_review_template.md",
        "frequency": "daily",
    },
    "plan-design-review": {
        "description": "Design/planning decision review",
        "template": "design_review_template.md",
        "frequency": "as_needed",
    },
    "plan-devex-review": {
        "description": "Developer experience planning",
        "template": "devex_template.md",
        "frequency": "weekly",
    },
}


class MIRAPlanningWorkflow:
    """
    MIRA's planning workflow based on gstack methodology.
    Uses OJ as Architect for planning, MIRA as Executioner for implementation.
    """

    def __init__(self):
        self.current_plan = None
        self.plan_history = []

    def log_planning_event(self, event: Dict[str, Any]):
        """Log planning events to The Weave"""
        event["timestamp"] = datetime.now().isoformat()

        with open(PLANNING_LOG, "a") as f:
            f.write(json.dumps(event) + "\n")

    def start_planning_session(
        self, category: str, topic: str, context: str = ""
    ) -> Dict[str, Any]:
        """Begin a new planning session"""

        if category not in PLANNING_CATEGORIES:
            return {"error": f"Unknown category: {category}"}

        session = {
            "phase": "office-hours",
            "category": category,
            "topic": topic,
            "context": context,
            "status": "active",
            "started_at": datetime.now().isoformat(),
        }

        self.current_plan = session

        self.log_planning_event(
            {
                "event_type": "planning_session_start",
                "category": category,
                "topic": topic,
            }
        )

        print(f"\n📋 Planning Session Started")
        print(f"   Category: {category}")
        print(f"   Topic: {topic}")
        print(f"   Description: {PLANNING_CATEGORIES[category]['description']}")

        return session

    def analyze_with_oj(self, prompt: str) -> Dict[str, Any]:
        """Use OJ (via Ollama) to architect the plan"""

        print(f"\n🏗️ OJ (Architect) Analysis:")
        print(f"   Prompt: {prompt[:100]}...")

        # This would call Ollama with OJ prompts
        # For now, return placeholder
        analysis = {
            "oj_analysis": "OJ would design the approach here",
            "design": "Plan structure from OJ",
            "approach": "Step-by-step from OJ",
        }

        self.log_planning_event(
            {"event_type": "oj_architect_analysis", "analysis": analysis}
        )

        return analysis

    def generate_plan(
        self,
        objective: str,
        constraints: List[str] = None,
        stakeholders: List[str] = None,
    ) -> Dict[str, Any]:
        """Generate a structured plan"""

        constraints = constraints or []
        stakeholders = stakeholders or []

        plan = {
            "objective": objective,
            "constraints": constraints,
            "stakeholders": stakeholders,
            "phases": [
                {
                    "name": "Analysis",
                    "description": "Understand the problem",
                    "duration": "estimated",
                    "output": "Problem statement",
                },
                {
                    "name": "Design",
                    "description": "Design the solution",
                    "duration": "estimated",
                    "output": "Solution architecture",
                },
                {
                    "name": "Implementation",
                    "description": "Execute the plan",
                    "duration": "estimated",
                    "output": "Working solution",
                },
                {
                    "name": "Review",
                    "description": "Validate and iterate",
                    "duration": "estimated",
                    "output": "Final delivery",
                },
            ],
            "created_at": datetime.now().isoformat(),
        }

        self.current_plan["plan"] = plan
        self.current_plan["phase"] = "plan-generated"

        self.log_planning_event(
            {
                "event_type": "plan_generated",
                "objective": objective,
                "phases": len(plan["phases"]),
            }
        )

        return plan

    def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute plan as MIRA (Executioner)"""

        print(f"\n⚙️ MIRA (Executioner) Plan Execution:")

        execution = {
            "plan": plan,
            "status": "in_progress",
            "completed_phases": [],
            "started_at": datetime.now().isoformat(),
        }

        # In real implementation, this would trigger actual execution
        for phase in plan["phases"]:
            print(f"   📦 Phase: {phase['name']} - {phase['description']}")

        self.log_planning_event(
            {"event_type": "plan_execution_started", "phases": len(plan["phases"])}
        )

        return execution

    def review_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Review plan with Persona Council (multiple perspectives)"""

        print(f"\n🔄 Plan Review (Persona Council):")

        perspectives = {
            "first_principles": "Does this align with core principles?",
            "scientific_method": "Is this verifiable and testable?",
            "philosophical": "What are the implications?",
            "creative": "Is there a more elegant solution?",
            "pragmatic": "Is this practical to implement?",
            "dark_passenger": "What could go wrong?",
        }

        review = {
            "perspectives": perspectives,
            "approved": True,  # Would be HITL decision
            "feedback": "Plan looks solid",
            "timestamp": datetime.now().isoformat(),
        }

        self.log_planning_event(
            {"event_type": "plan_review_complete", "review": review}
        )

        return review

    def complete_session(self, plan: Dict, execution: Dict = None) -> Dict:
        """Complete the planning session"""

        session = {
            "status": "completed",
            "plan": plan,
            "execution": execution,
            "completed_at": datetime.now().isoformat(),
        }

        self.plan_history.append(session)
        self.current_plan = None

        self.log_planning_event(
            {
                "event_type": "planning_session_complete",
                "plan_objective": plan.get("objective"),
            }
        )

        print(f"\n✅ Planning Session Complete!")
        print(f"   Objective: {plan.get('objective')}")

        return session


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Planning Workflow")
    parser.add_argument("--start", type=str, help="Start planning session with topic")
    parser.add_argument("--category", default="office-hours", help="Planning category")
    parser.add_argument("--plan", action="store_true", help="Generate plan")
    parser.add_argument("--execute", action="store_true", help="Execute plan")
    parser.add_argument("--review", action="store_true", help="Review plan")
    parser.add_argument(
        "--list-categories", action="store_true", help="List categories"
    )

    args = parser.parse_args()

    workflow = MIRAPlanningWorkflow()

    if args.list_categories:
        print("\n📋 Planning Categories (gstack-inspired):")
        print("=" * 50)
        for cat, config in PLANNING_CATEGORIES.items():
            print(f"  {cat:20} - {config['description']}")
        print("=" * 50)

    elif args.start:
        session = workflow.start_planning_session(
            category=args.category, topic=args.start
        )

        if args.plan:
            plan = workflow.generate_plan(
                objective=args.start,
                constraints=["time", "resources"],
                stakeholders=["user", "mira"],
            )
            print(f"\n📝 Plan generated with {len(plan['phases'])} phases")

            if args.review:
                review = workflow.review_plan(plan)
                print(f"\n✅ Review complete: {review['approved']}")

            if args.execute:
                execution = workflow.execute_plan(plan)
                workflow.complete_session(plan, execution)

    else:
        print("MIRA Planning Workflow")
        print("  --start 'topic'       Start planning session")
        print("  --category 'type'     Planning category (default: office-hours)")
        print("  --plan                Generate plan")
        print("  --execute             Execute plan")
        print("  --review               Review with Persona Council")
        print("  --list-categories      List planning categories")


if __name__ == "__main__":
    main()
