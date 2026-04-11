#!/usr/bin/env python3
"""
Shadow Ops Cron Integration
Runs Shadow Ops Orchestrator on a schedule via cron
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

MIRA_ROOT = Path("/home/sir-v/MiRA")
ORCHESTRATOR = MIRA_ROOT / "Memory_Mesh" / "shadow_ops_orchestrator.py"
LOG_DIR = MIRA_ROOT / "Memory_Mesh" / "logs"
LOG_DIR.mkdir(exist_ok=True)


def run_orchestrator():
    """Run the Shadow Ops Orchestrator"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"shadow_ops_{timestamp}.log"

    try:
        result = subprocess.run(
            ["python3", str(ORCHESTRATOR)], capture_output=True, text=True, timeout=300
        )

        with open(log_file, "w") as f:
            f.write(f"=== Shadow Ops Run: {timestamp} ===\n")
            f.write(f"Return code: {result.returncode}\n\n")
            f.write(f"--- STDOUT ---\n{result.stdout}\n\n")
            f.write(f"--- STDERR ---\n{result.stderr}\n")

        print(f"✅ Shadow Ops completed. Log: {log_file}")
        return result.returncode

    except subprocess.TimeoutExpired:
        print("❌ Shadow Ops timed out (>5 min)")
        return 1
    except Exception as e:
        print(f"❌ Shadow Ops failed: {e}")
        return 1


def setup_cron():
    """Generate crontab entry for Shadow Ops"""
    cron_entry = "0 */6 * * * cd /home/sir-v/MiRA && python3 Memory_Mesh/shadow_ops_cron.py >> Memory_Mesh/logs/cron.log 2>&1"

    print("Shadow Ops Cron Setup")
    print("=" * 50)
    print(f"To add to crontab, run:")
    print(f"  crontab -e")
    print(f"")
    print(f"Add this line:")
    print(f"  {cron_entry}")
    print("=" * 50)
    print(f"Alternatively, append to existing crontab:")
    print(f"  echo '{cron_entry}' | crontab -")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_cron()
    elif len(sys.argv) > 1 and sys.argv[1] == "--run":
        run_orchestrator()
    else:
        print("Shadow Ops Cron Integration")
        print("  --run    Run orchestrator once")
        print("  --setup  Show crontab setup instructions")


if __name__ == "__main__":
    main()
