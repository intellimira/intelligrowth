#!/usr/bin/env python3
"""
MIRA Shadow Ops Orchestrator
Coordinates all Lines of Business through infrastructure layer.
"""

import os
import sys
import json
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# Configuration
MIRA_ROOT = Path("/home/sir-v/MiRA")
MEMORY_MESH = MIRA_ROOT / "Memory_Mesh"
SKILLS_DIR = MIRA_ROOT / "skills"
WEAVE_LOG = MEMORY_MESH / "weave_orchestration_log.jsonl"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(MEMORY_MESH / "orchestrator.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("mira_orchestrator")

# LOB Definitions
SHADOW_OPS_LOBS = {
    "enquiry_pipeline": {
        "skill": "email-automation",
        "script": "poll_enquiries.py",
        "path": MEMORY_MESH,
        "description": "Gmail → Score → Alert",
        "run_method": "script",
        "hitl_trigger": "new_high_priority_leads",
    },
    "social_hunter": {
        "skill": "social-hunter",
        "script": None,  # Will run skill directly
        "path": SKILLS_DIR / "social-hunter",
        "description": "Reddit/HN/Indie lead extraction",
        "run_method": "skill",
        "hitl_trigger": "significant_lead_signal",
    },
    "revenue_tracker": {
        "skill": "revenue-tracker",
        "script": None,
        "path": SKILLS_DIR / "revenue-tracker",
        "description": "Deals P&L tracking",
        "run_method": "skill",
        "hitl_trigger": "significant_revenue_change",
    },
    "shadow_ops_prover": {
        "skill": "shadow-ops-prover",
        "script": "scripts/scout_node.py",
        "path": SKILLS_DIR / "shadow-ops-prover",
        "description": "7-stage monetization pipeline",
        "run_method": "script",
        "hitl_trigger": "new_proven_lead",
    },
    "srank_generator": {
        "skill": "srank-pack-generator",
        "script": None,
        "path": SKILLS_DIR / "srank-pack-generator",
        "description": "Business document generation",
        "run_method": "skill",
        "hitl_trigger": "approved_deal_ready",
    },
    "pain_scorer": {
        "skill": "pain-scorer",
        "script": None,
        "path": SKILLS_DIR / "pain-scorer",
        "description": "Signal evaluation - on demand",
        "run_method": "skill",
        "hitl_trigger": None,  # On-demand only
    },
}


class ShadowOpsOrchestrator:
    def __init__(self, mode: str = "select"):
        self.mode = mode
        self.results = []
        self.hitl_alerts = []

    def log_to_weave(self, event: Dict[str, Any]):
        """Log orchestration events to The Weave"""
        event["timestamp"] = datetime.now().isoformat()
        event["orchestrator"] = "mira_shadow_ops"

        with open(WEAVE_LOG, "a") as f:
            f.write(json.dumps(event) + "\n")

        logger.info(f"📝 Weave logged: {event.get('event_type', 'unknown')}")

    def run_lob(self, lob_name: str, lob_config: Dict) -> Dict[str, Any]:
        """Execute a single Line of Business"""
        logger.info(f"▶ Running LOB: {lob_name}")

        result = {
            "lob": lob_name,
            "skill": lob_config["skill"],
            "status": "pending",
            "output": None,
            "error": None,
            "timestamp": datetime.now().isoformat(),
        }

        try:
            if lob_config["run_method"] == "script":
                script_path = lob_config["path"] / lob_config["script"]
                if script_path.exists():
                    # Run the script
                    output = subprocess.run(
                        ["python3", str(script_path)],
                        capture_output=True,
                        text=True,
                        timeout=300,  # 5 min timeout
                    )
                    result["status"] = "success" if output.returncode == 0 else "failed"
                    result["output"] = output.stdout[:500] if output.stdout else None
                    result["error"] = output.stderr[:500] if output.stderr else None
                else:
                    result["status"] = "skipped"
                    result["error"] = f"Script not found: {script_path}"

            elif lob_config["run_method"] == "skill":
                result["status"] = "ready"
                result["output"] = f"Skill {lob_config['skill']} ready for execution"

            # Check HITL triggers
            if lob_config.get("hitl_trigger") and result["status"] == "success":
                self.hitl_alerts.append(
                    {
                        "lob": lob_name,
                        "trigger": lob_config["hitl_trigger"],
                        "timestamp": result["timestamp"],
                    }
                )

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)[:500]
            logger.error(f"❌ LOB {lob_name} failed: {e}")

        self.log_to_weave(
            {"event_type": "lob_execution", "lob": lob_name, "status": result["status"]}
        )

        return result

    def run_all(self, selected_lobs: Optional[List[str]] = None) -> List[Dict]:
        """Execute all LOBs or selected ones"""
        lobs_to_run = selected_lobs if selected_lobs else list(SHADOW_OPS_LOBS.keys())

        logger.info(f"🚀 Starting orchestrator in '{self.mode}' mode")
        logger.info(f"📋 LOBs to run: {lobs_to_run}")

        for lob_name in lobs_to_run:
            if lob_name in SHADOW_OPS_LOBS:
                result = self.run_lob(lob_name, SHADOW_OPS_LOBS[lob_name])
                self.results.append(result)
            else:
                logger.warning(f"⚠️ Unknown LOB: {lob_name}")

        return self.results

    def summary(self) -> Dict[str, Any]:
        """Generate execution summary"""
        total = len(self.results)
        success = sum(1 for r in self.results if r["status"] == "success")
        failed = sum(1 for r in self.results if r["status"] in ["failed", "error"])
        skipped = sum(1 for r in self.results if r["status"] == "skipped")
        ready = sum(1 for r in self.results if r["status"] == "ready")

        return {
            "total_lobs": total,
            "success": success,
            "failed": failed,
            "skipped": skipped,
            "ready": ready,
            "hitl_alerts": len(self.hitl_alerts),
            "alerts": self.hitl_alerts,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Shadow Ops Orchestrator")
    parser.add_argument(
        "--mode",
        choices=["auto", "select", "watch", "test"],
        default="select",
        help="Run mode",
    )
    parser.add_argument("--lobs", nargs="+", help="Specific LOBs to run (default: all)")
    parser.add_argument("--test", action="store_true", help="Dry-run validation")

    args = parser.parse_args()

    # Initialize orchestrator
    orchestrator = ShadowOpsOrchestrator(mode=args.mode)

    if args.test:
        logger.info("🧪 Test mode - validating configuration only")
        for lob_name, config in SHADOW_OPS_LOBS.items():
            logger.info(f"  ✓ {lob_name}: {config['skill']}")
        logger.info(f"  ✓ Total LOBs: {len(SHADOW_OPS_LOBS)}")
        print("\n✅ Configuration valid - Ready for execution")
        return

    # Run LOBs
    results = orchestrator.run_all(args.lobs)

    # Print summary
    summary = orchestrator.summary()
    print("\n" + "=" * 50)
    print("📊 SHADOW OPS ORCHESTRATION SUMMARY")
    print("=" * 50)
    print(f"  Total LOBs:  {summary['total_lobs']}")
    print(f"  ✅ Success:   {summary['success']}")
    print(f"  ❌ Failed:    {summary['failed']}")
    print(f"  ⏭️  Skipped:   {summary['skipped']}")
    print(f"  📋 Ready:     {summary['ready']}")
    print(f"  🚨 HITL Alerts: {summary['hitl_alerts']}")
    print("=" * 50)

    if summary["hitl_alerts"]:
        print("\n🚨 HITL TRIGGERS REQUIRING ATTENTION:")
        for alert in summary["alerts"]:
            print(f"  - {alert['lob']}: {alert['trigger']}")

    # Log final status
    orchestrator.log_to_weave(
        {"event_type": "orchestration_complete", "summary": summary}
    )


if __name__ == "__main__":
    main()
