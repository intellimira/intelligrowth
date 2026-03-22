#!/usr/bin/env python3
"""
MIRA Weave Watchdog - Monitors for new sessions and triggers Weave
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

MEMORY_MESH = Path("/home/sir-v/MiRA/Memory_Mesh")
SESSIONS_PATH = Path("/home/sir-v/MiRA/sessions")
LOG_FILE = MEMORY_MESH / "watchdog.log"


class SessionHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run = 0
        self.debounce_seconds = 60

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".md") and "ses_" in event.src_path:
            now = time.time()
            if now - self.last_run < self.debounce_seconds:
                return

            self.last_run = now
            self.process_new_session(event.src_path)

    def process_new_session(self, filepath):
        print(f"\n{'=' * 60}")
        print(f"🆕 New session detected: {Path(filepath).name}")
        print(f"⏰ {datetime.now().isoformat()}")
        print(f"{'=' * 60}")

        log(f"New session: {filepath}")

        self.run_weave_cycle()

    def run_weave_cycle(self):
        try:
            print("\n🔄 Running Weave cycle...\n")
            log("Starting Weave cycle")

            result = subprocess.run(
                [sys.executable, str(MEMORY_MESH / "weaver.py"), "--full"],
                capture_output=True,
                text=True,
                cwd=str(MEMORY_MESH.parent),
                timeout=300,
            )

            if result.returncode == 0:
                print("✅ Weave cycle completed")
                log("Weave cycle completed successfully")
            else:
                print(f"❌ Weave cycle failed: {result.stderr[:200]}")
                log(f"Weave cycle failed: {result.stderr[:200]}")

        except subprocess.TimeoutExpired:
            print("❌ Weave cycle timed out")
            log("Weave cycle timed out")
        except Exception as e:
            print(f"❌ Error: {e}")
            log(f"Error: {e}")


def log(message: str):
    """Log to file."""
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def run_watchdog(interval: int = 60):
    """Run watchdog in watch mode."""
    print("👁️  MIRA Weave Watchdog")
    print("=" * 60)
    print(f"📁 Watching: {SESSIONS_PATH}")
    print(f"⏱️  Debounce: {interval} seconds")
    print(f"📝 Log: {LOG_FILE}")
    print("\nPress Ctrl+C to stop\n")

    log(f"Watchdog started - watching {SESSIONS_PATH}")

    event_handler = SessionHandler()
    observer = Observer()
    observer.schedule(event_handler, str(SESSIONS_PATH), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Watchdog stopped")
        log("Watchdog stopped")
        observer.stop()

    observer.join()


def run_once():
    """Run Weave cycle once (for cron/scheduled runs)."""
    print("🔄 Running Weave cycle (scheduled)...")
    log("Scheduled Weave cycle started")

    try:
        result = subprocess.run(
            [sys.executable, str(MEMORY_MESH / "weaver.py"), "--full"],
            capture_output=True,
            text=True,
            cwd=str(MEMORY_MESH.parent),
            timeout=300,
        )

        if result.returncode == 0:
            print("✅ Weave cycle completed")
            log("Scheduled Weave cycle completed")
        else:
            print(f"❌ Failed: {result.stderr[:200]}")
            log(f"Scheduled Weave cycle failed")

    except Exception as e:
        print(f"❌ Error: {e}")
        log(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--once":
            run_once()
        elif sys.argv[1] == "--help":
            print("""
👁️  MIRA Weave Watchdog

Usage:
  python watchdog.py            # Start watching (Ctrl+C to stop)
  python watchdog.py --once    # Run Weave cycle once (for cron)
  python watchdog.py --help     # Show this help

The watchdog monitors the sessions folder and automatically
triggers the Weave cycle when new sessions are created.
            """)
        else:
            print(f"Unknown option: {sys.argv[1]}")
    else:
        run_watchdog()
