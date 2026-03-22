#!/usr/bin/env python3
"""
MIRA Autonomous Weave - Main Orchestrator
Coordinates all Weave components for self-sustaining knowledge management

Trigger: On session end + periodic maintenance
"""

import os
import sys
from pathlib import Path
from datetime import datetime

MEMORY_MESH = Path("/home/sir-v/MiRA/Memory_Mesh")
SESSIONS_PATH = Path("/home/sir-v/MiRA/sessions")


class WeaveOrchestrator:
    def __init__(self):
        self.memory_mesh = MEMORY_MESH
        self.sessions_path = SESSIONS_PATH
        self.auto_ingest_path = self.memory_mesh / "auto_ingest"
        self.smart_linker_path = self.memory_mesh / "smart_linker"
        self.usage_tracker_path = self.memory_mesh / "usage_tracker"
        self.self_improver_path = self.memory_mesh / "self_improver"
        self.vector_mesh_path = self.memory_mesh / "Vector_Mesh"

    def run_session_sealer(self) -> dict:
        """Run session sealing pipeline."""
        print("\n" + "=" * 60)
        print("🔍 PHASE 1: Session Sealing")
        print("=" * 60)

        try:
            sys.path.insert(0, str(self.auto_ingest_path))
            from session_sealer import SessionSealer

            sealer = SessionSealer()
            result = sealer.seal_all()

            return result
        except Exception as e:
            print(f"❌ Session Sealer error: {e}")
            return {"sealed": 0, "skipped": 0}

    def run_vector_index(self) -> dict:
        """Run Vector_Mesh indexing."""
        print("\n" + "=" * 60)
        print("🔍 PHASE 2: Vector Indexing")
        print("=" * 60)

        try:
            sys.path.insert(0, str(self.vector_mesh_path))
            import index

            result = index.index_all()

            return result if result else {"indexed": 0, "skipped": 0}
        except Exception as e:
            print(f"❌ Vector Index error: {e}")
            return {"indexed": 0, "skipped": 0}

    def run_smart_linker(self) -> dict:
        """Run smart linking pipeline."""
        print("\n" + "=" * 60)
        print("🔍 PHASE 3: Smart Linking")
        print("=" * 60)

        try:
            sys.path.insert(0, str(self.smart_linker_path))
            from relationship_finder import SmartLinker

            linker = SmartLinker()
            result = linker.link_all()

            return result
        except Exception as e:
            print(f"❌ Smart Linker error: {e}")
            return {"zettels": 0, "relationships": 0}

    def run_self_improver(self) -> dict:
        """Run self-improvement analysis."""
        print("\n" + "=" * 60)
        print("🔍 PHASE 4: Self-Improvement Analysis")
        print("=" * 60)

        try:
            sys.path.insert(0, str(self.self_improver_path))
            from suggestions import SelfImprover

            improver = SelfImprover()
            suggestions = improver.run(display=True)

            return suggestions
        except Exception as e:
            print(f"❌ Self-Improver error: {e}")
            return {}

    def run_full_cycle(self) -> dict:
        """Run complete Weave cycle."""
        print("\n" + "=" * 60)
        print("🧠 MIRA AUTONOMOUS WEAVE - FULL CYCLE")
        print(f"⏰ Started: {datetime.now().isoformat()}")
        print("=" * 60)

        results = {
            "session_sealer": self.run_session_sealer(),
            "vector_index": self.run_vector_index(),
            "smart_linker": self.run_smart_linker(),
            "timestamp": datetime.now().isoformat(),
        }

        print("\n" + "=" * 60)
        print("📊 CYCLE SUMMARY")
        print("=" * 60)
        sealed = results["session_sealer"].get("sealed", 0)
        vector_result = results["vector_index"]
        indexed = (
            vector_result[0]
            if isinstance(vector_result, tuple)
            else vector_result.get("indexed", 0)
        )
        relationships = results["smart_linker"].get("relationships", 0)
        print(f"   Sessions sealed: {sealed}")
        print(f"   Zettels indexed: {indexed}")
        print(f"   Relationships: {relationships}")

        print("\n💡 Run self-improve for suggestions:")
        print("   python weaver.py --suggest")

        return results

    def run_suggestions_only(self):
        """Run only self-improvement analysis."""
        self.run_self_improver()

    def status(self) -> dict:
        """Get current Weave status."""
        status = {"timestamp": datetime.now().isoformat(), "components": {}}

        vector_db = self.vector_mesh_path / "vectors.db"
        if vector_db.exists():
            import sqlite3

            conn = sqlite3.connect(str(vector_db))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM zettels")
            zettel_count = cursor.fetchone()[0]
            conn.close()
            status["components"]["Vector_Mesh"] = f"{zettel_count} zettels indexed"
        else:
            status["components"]["Vector_Mesh"] = "Not initialized"

        graph_db = self.smart_linker_path / "graph.db"
        if graph_db.exists():
            import sqlite3

            conn = sqlite3.connect(str(graph_db))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links")
            link_count = cursor.fetchone()[0]
            conn.close()
            status["components"]["Smart_Linker"] = f"{link_count} relationships"
        else:
            status["components"]["Smart_Linker"] = "Not initialized"

        tracker_db = self.usage_tracker_path / "tracker.db"
        if tracker_db.exists():
            import sqlite3

            conn = sqlite3.connect(str(tracker_db))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM queries")
            query_count = cursor.fetchone()[0]
            conn.close()
            status["components"]["Usage_Tracker"] = f"{query_count} queries logged"
        else:
            status["components"]["Usage_Tracker"] = "Not initialized"

        sessions = list(self.sessions_path.glob("ses_*.md"))
        status["pending_sessions"] = len(sessions)

        return status


def main():
    orchestrator = WeaveOrchestrator()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--full" or command == "-f":
            orchestrator.run_full_cycle()

        elif command == "--suggest" or command == "-s":
            orchestrator.run_suggestions_only()

        elif command == "--status":
            status = orchestrator.status()
            print("\n🧠 MIRA Autonomous Weave Status")
            print("=" * 50)
            for component, info in status["components"].items():
                print(f"   {component}: {info}")
            print(f"\n   Pending sessions: {status['pending_sessions']}")
            print(f"   Last checked: {status['timestamp']}")

        elif command == "--sealer":
            orchestrator.run_session_sealer()

        elif command == "--index":
            orchestrator.run_vector_index()

        elif command == "--link":
            orchestrator.run_smart_linker()

        elif command == "--help":
            print("""
🧠 MIRA Autonomous Weave Orchestrator

Usage: python weaver.py [command]

Commands:
  --full, -f       Run complete Weave cycle (seal, index, link)
  --sealer         Run session sealing only
  --index          Run Vector_Mesh indexing only
  --link           Run smart linking only
  --suggest, -s    Run self-improvement analysis
  --status         Show Weave status
  --help           Show this help

Examples:
  python weaver.py --full          # Full cycle
  python weaver.py --status         # Check status
  python weaver.py --suggest        # Get improvement suggestions
            """)
        else:
            print(f"Unknown command: {command}")
            print("Run --help for usage")

    else:
        print("🧠 MIRA Autonomous Weave")
        print("=" * 50)
        print("Run with --help for usage")
        print("Run with --status for current status")


if __name__ == "__main__":
    main()
