#!/usr/bin/env python3
"""
MIRA Weave Hook - Integrates with Session Guardian
Run this after session finalization to trigger Weave cycle

Usage:
  python weaver_hook.py                    # Full cycle
  python weaver_hook.py --sealer-only     # Just seal sessions
  python weaver_hook.py --status          # Check status
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

MEMORY_MESH = Path("/home/sir-v/MiRA/Memory_Mesh")
LOG_FILE = MEMORY_MESH / "weaver_hooks.log"


def log(message: str):
    """Log message with timestamp."""
    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}"
    print(log_line)

    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")


def run_weave_command(args: list) -> bool:
    """Run weaver command and return success status."""
    try:
        result = subprocess.run(
            [sys.executable, str(MEMORY_MESH / "weaver.py")] + args,
            capture_output=True,
            text=True,
            cwd=str(MEMORY_MESH.parent),
        )

        if result.returncode == 0:
            log(f"SUCCESS: weaver.py {' '.join(args)}")
            return True
        else:
            log(f"ERROR: weaver.py {' '.join(args)} failed")
            log(f"STDERR: {result.stderr[:200]}")
            return False

    except Exception as e:
        log(f"EXCEPTION: {e}")
        return False


def run_full_cycle():
    """Run complete Weave cycle."""
    log("Starting full Weave cycle...")

    success = run_weave_command(["--full"])

    if success:
        log("Full cycle completed successfully")
    else:
        log("Full cycle had errors")

    return success


def run_sealer_only():
    """Run only session sealing."""
    log("Running session sealer only...")

    sys.path.insert(0, str(MEMORY_MESH / "auto_ingest"))
    try:
        from session_sealer import SessionSealer

        sealer = SessionSealer()
        result = sealer.seal_all()

        sealed = result.get("sealed", 0)
        log(f"Session sealing complete: {sealed} sessions sealed")

        if sealed > 0:
            log("Triggering vector index...")
            run_weave_command(["--index"])

        return True

    except Exception as e:
        log(f"ERROR in session sealer: {e}")
        return False


def check_status():
    """Check Weave status."""
    run_weave_command(["--status"])


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--full":
            run_full_cycle()
        elif command == "--sealer-only":
            run_sealer_only()
        elif command == "--status":
            check_status()
        elif command == "--help":
            print("""
MIRA Weave Hook - Session Guardian Integration

Usage:
  python weaver_hook.py              # Full cycle
  python weaver_hook.py --full      # Full cycle
  python weaver_hook.py --sealer-only  # Just seal sessions
  python weaver_hook.py --status    # Check status

This hook is called by Session Guardian after session finalization.
It triggers the Autonomous Weave to:
  1. Convert new sessions to zettels
  2. Index zettels in Vector_Mesh
  3. Create relationships via Smart Linker
  4. Log to usage tracker
            """)
        else:
            print(f"Unknown command: {command}")
            print("Run --help for usage")
    else:
        run_full_cycle()


if __name__ == "__main__":
    main()
