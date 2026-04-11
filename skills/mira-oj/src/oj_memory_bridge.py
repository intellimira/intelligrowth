#!/usr/bin/env python3
"""
MIRA-OJ Memory Bridge
=====================
Phase 2: Memory_Mesh Integration
Connects Vector_Mesh (zettels, sessions, corpus) to MIRA-OJ synthesis.

Usage:
    from oj_memory_bridge import OJMemoryBridge

    bridge = OJMemoryBridge()
    result = bridge.synthesize_with_context("What is Wu Wei?")
"""

import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# CONFIGURATION
# ============================================================================

VECTOR_MESH_DB = "/home/sir-v/MiRA/skills/Vector_Mesh/vectors.db"
ZETTELS_PATH = "/home/sir-v/MiRA/Memory_Mesh/zettels/"
SESSIONS_PATH = "/home/sir-v/MiRA/sessions/"
TAYLOR_CHUNKS_PATH = "/home/sir-v/MiRA/skills/Vector_Mesh/embeddings/taylor_chunks/"


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class MemoryChunk:
    """A chunk from memory storage."""

    text: str
    source: str  # zettel, session, taylor, abi
    source_path: str
    score: float
    domain: Optional[str] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class ContextBundle:
    """Bundle of contextual memories for synthesis."""

    query: str
    chunks: List[MemoryChunk]
    session_context: Optional[Dict] = None
    zettel_links: List[str] = None

    def __post_init__(self):
        if self.zettel_links is None:
            self.zettel_links = []


# ============================================================================
# MAIN BRIDGE CLASS
# ============================================================================


class OJMemoryBridge:
    """
    Bridge between MIRA-OJ and Memory_Mesh.

    Enables:
    - Vector search across all memory sources
    - Session context injection
    - Zettel cross-referencing
    - ABI0.1 business context integration
    """

    def __init__(
        self,
        vector_db_path: str = VECTOR_MESH_DB,
        zettels_path: str = ZETTELS_PATH,
        sessions_path: str = SESSIONS_PATH,
        taylor_chunks_path: str = TAYLOR_CHUNKS_PATH,
    ):
        self.vector_db_path = vector_db_path
        self.zettels_path = zettels_path
        self.sessions_path = sessions_path
        self.taylor_chunks_path = taylor_chunks_path

        # Check what's available
        self._check_sources()

    def _check_sources(self):
        """Verify which sources are available."""
        self.sources = {
            "vector_db": os.path.exists(self.vector_db_path),
            "zettels": os.path.exists(self.zettels_path),
            "sessions": os.path.exists(self.sessions_path),
            "taylor_chunks": os.path.exists(self.taylor_chunks_path),
        }

        # Count items
        if self.sources["zettels"]:
            self.zettel_count = len(list(Path(self.zettels_path).rglob("*.md")))
        else:
            self.zettel_count = 0

        if self.sources["sessions"]:
            self.session_count = len(list(Path(self.sessions_path).glob("ses_*.md")))
        else:
            self.session_count = 0

    # ⚛️ First Principles: Core search functionality
    def vector_search(
        self,
        query: str,
        use_zettels: bool = True,
        use_sessions: bool = True,
        use_taylor: bool = True,
        use_abi: bool = True,
        top_k: int = 5,
    ) -> List[MemoryChunk]:
        """
        Search across memory sources using vector similarity.

        This is the core of Phase 2 - enables OJ to reference
        actual zettels and sessions in synthesis.
        """
        results = []

        # Use Vector_Mesh search script if available
        search_script = "/home/sir-v/MiRA/skills/Vector_Mesh/src/search.py"

        if os.path.exists(search_script):
            try:
                result = subprocess.run(
                    ["python3", search_script, query],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    # Parse results from script
                    for line in result.stdout.strip().split("\n"):
                        if line and "|" in line:
                            parts = line.split("|")
                            if len(parts) >= 3:
                                chunk = MemoryChunk(
                                    text=parts[0].strip(),
                                    source="vector",
                                    source_path=parts[1].strip(),
                                    score=float(parts[2].strip())
                                    if len(parts) > 2
                                    else 0.5,
                                )
                                results.append(chunk)
            except Exception as e:
                print(f"Vector search error: {e}")

        # Fallback: Direct search if vector search fails
        if not results:
            results = self._direct_search(query, top_k)

        return results[:top_k]

    def _direct_search(self, query: str, top_k: int) -> List[MemoryChunk]:
        """Fallback direct search through zettels."""
        results = []
        query_lower = query.lower()

        # Search zettels
        if self.sources["zettels"]:
            zettel_files = list(Path(self.zettels_path).rglob("*.md"))[:100]
            for md_file in zettel_files:
                try:
                    content = md_file.read_text(encoding="utf-8", errors="ignore")
                    if query_lower in content.lower():
                        # Extract relevant snippet
                        lines = content.split("\n")
                        snippets = [l for l in lines if query_lower in l.lower()]
                        snippet = snippets[0][:200] if snippets else content[:200]

                        chunk = MemoryChunk(
                            text=snippet,
                            source="zettel",
                            source_path=str(md_file),
                            score=0.5,
                        )
                        results.append(chunk)
                except:
                    continue

        # Search sessions
        if self.sources["sessions"]:
            for session_file in Path(self.sessions_path).glob("ses_*.md"):
                try:
                    content = session_file.read_text(encoding="utf-8", errors="ignore")
                    if query_lower in content.lower():
                        lines = content.split("\n")
                        snippets = [l for l in lines if query_lower in l.lower()]
                        snippet = snippets[0][:200] if snippets else content[:200]

                        chunk = MemoryChunk(
                            text=snippet,
                            source="session",
                            source_path=str(session_file),
                            score=0.4,
                        )
                        results.append(chunk)
                except:
                    continue

        return results[:top_k]

    # 🔬 Scientific Method: Systematic context gathering
    def gather_context(
        self,
        query: str,
        include_sessions: bool = True,
        include_zettels: bool = True,
        include_taylor: bool = True,
        include_abi: bool = True,
    ) -> ContextBundle:
        """
        Systematically gather all relevant context for a query.

        This is what makes OJ synthesis "MIRA-aware" instead of generic.
        """
        chunks = []

        # Vector search across all sources
        search_results = self.vector_search(
            query,
            use_zettels=include_zettels,
            use_sessions=include_sessions,
            use_taylor=include_taylor,
            use_abi=include_abi,
            top_k=5,
        )
        chunks.extend(search_results)

        # Get session context (recent sessions, patterns)
        session_context = None
        if include_sessions:
            session_context = self._get_session_context()

        # Get related zettels for cross-referencing
        zettel_links = []
        if include_zettels:
            zettel_links = self._find_zettel_links(query)

        return ContextBundle(
            query=query,
            chunks=chunks,
            session_context=session_context,
            zettel_links=zettel_links,
        )

    def _get_session_context(self) -> Dict:
        """Extract recent session patterns."""
        sessions = []
        session_files = sorted(
            Path(self.sessions_path).glob("ses_*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )[:5]  # Last 5 sessions

        for session_file in session_files:
            try:
                content = session_file.read_text(encoding="utf-8", errors="ignore")
                # Extract key info
                first_lines = "\n".join(content.split("\n")[:20])
                sessions.append(
                    {"file": session_file.name, "preview": first_lines[:300]}
                )
            except:
                continue

        return {"recent_sessions": sessions, "count": len(sessions)}

    def _find_zettel_links(self, query: str) -> List[str]:
        """Find related zettels for cross-referencing."""
        links = []
        query_lower = query.lower()

        # Find zettels with matching tags or content
        links = []
        query_lower = query.lower()

        if self.sources["zettels"]:
            zettel_files = list(Path(self.zettels_path).rglob("*.md"))[:20]
            for md_file in zettel_files:
                try:
                    content = md_file.read_text(encoding="utf-8", errors="ignore")
                    # Simple relevance check
                    if any(word in content.lower() for word in query_lower.split()[:3]):
                        links.append(md_file.stem)
                except:
                    continue

        return links[:5]

    # ✨ Creative: Synthesis with full context
    def synthesize_with_context(
        self, query: str, use_memory: bool = True, persona: Optional[str] = None
    ) -> Tuple[str, Dict]:
        """
        Synthesize response with full MIRA context.

        Returns:
            - Enhanced response (with MIRA context if available)
            - Metadata (sources used, confidence, etc.)
        """
        metadata = {
            "sources_used": [],
            "zettel_references": [],
            "session_references": [],
            "confidence": 0.5,
            "context_length": 0,
        }

        if not use_memory:
            return query, metadata

        # Gather full context
        context = self.gather_context(
            query,
            include_sessions=True,
            include_zettels=True,
            include_taylor=True,
            include_abi=True,
        )

        if not context.chunks:
            return query, metadata

        # Build context injection
        context_parts = []

        for chunk in context.chunks:
            source_label = f"[{chunk.source.upper()}]"
            context_parts.append(f"{source_label} {chunk.text[:150]}")
            metadata["sources_used"].append(chunk.source)

        # Add session context
        if context.session_context:
            recent = context.session_context.get("recent_sessions", [])
            if recent:
                metadata["session_references"] = [s["file"] for s in recent]

        # Add zettel links
        if context.zettel_links:
            metadata["zettel_references"] = context.zettel_links[:3]

        # Build enhanced query
        context_str = "\n\n".join(context_parts)
        enhanced_query = f"""Based on MIRA's knowledge base:

{context_str}

---

User question: {query}

Provide a synthesis that draws on the above context where relevant."""

        metadata["confidence"] = min(0.9, 0.5 + (len(context.chunks) * 0.1))
        metadata["context_length"] = len(context_str)

        return enhanced_query, metadata

    # ⚙️ Pragmatic: Simple integration with existing OJ
    def inject_into_oj_prompt(
        self, base_prompt: str, query: str, use_memory: bool = True
    ) -> str:
        """
        Inject memory context into OJ's existing prompt structure.

        Use this to wrap existing OJ prompts with MIRA context.
        """
        if not use_memory:
            return base_prompt

        enhanced_query, metadata = self.synthesize_with_context(query, use_memory=True)

        # Inject as system context
        injection = f"""
<!-- MIRA CONTEXT INJECTION (Phase 2) -->
<!-- Sources: {", ".join(metadata["sources_used"])} -->
<!-- Zettels: {", ".join(metadata["zettel_references"][:3]) if metadata["zettel_references"] else "none"} -->
<!-- Session refs: {len(metadata["session_references"])} recent -->

{base_prompt}
"""
        return injection

    # 🌑 Dark Passenger: Error handling
    def health_check(self) -> Dict:
        """Check bridge health and availability."""
        return {
            "bridge_status": "active",
            "sources": self.sources,
            "zettel_count": self.zettel_count,
            "session_count": self.session_count,
            "vector_search": self.sources["vector_db"],
            "last_check": datetime.now().isoformat(),
        }


# ============================================================================
# STANDALONE FUNCTIONS
# ============================================================================


def search_memory(query: str, top_k: int = 5) -> List[MemoryChunk]:
    """Quick search function."""
    bridge = OJMemoryBridge()
    return bridge.vector_search(query, top_k=top_k)


def synthesize_with_mira_context(query: str) -> Tuple[str, Dict]:
    """Quick synthesis with full context."""
    bridge = OJMemoryBridge()
    return bridge.synthesize_with_context(query)


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("""
MIRA-OJ Memory Bridge - Phase 2
================================

Usage:
    python3 oj_memory_bridge.py search "<query>" [top_k]
    python3 oj_memory_bridge.py synthesize "<query>"
    python3 oj_memory_bridge.py health
    
Examples:
    python3 oj_memory_bridge.py search "Wu Wei Taoism" 5
    python3 oj_memory_bridge.py synthesize "What is Chi?"
    python3 oj_memory_bridge.py health
""")
        sys.exit(1)

    command = sys.argv[1]

    if command == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else "test"
        top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 5

        results = search_memory(query, top_k)
        print(f"\n{'=' * 60}")
        print(f"SEARCH RESULTS: {query}")
        print(f"{'=' * 60}\n")

        for i, chunk in enumerate(results, 1):
            print(f"[{i}] {chunk.source.upper()}")
            print(f"    Path: {chunk.source_path}")
            print(f"    Score: {chunk.score:.2f}")
            print(f"    Text: {chunk.text[:150]}...")
            print()

    elif command == "synthesize":
        query = sys.argv[2] if len(sys.argv) > 2 else "test"

        response, metadata = synthesize_with_mira_context(query)

        print(f"\n{'=' * 60}")
        print(f"SYNTHESIS RESULT")
        print(f"{'=' * 60}")
        print(f"\nConfidence: {metadata['confidence']:.1%}")
        print(f"Sources: {', '.join(metadata['sources_used'])}")
        print(
            f"Zettels: {', '.join(metadata['zettel_references'][:3]) if metadata['zettel_references'] else 'none'}"
        )
        print(f"\n{response[:500]}...")

    elif command == "health":
        bridge = OJMemoryBridge()
        health = bridge.health_check()

        print(f"\n{'=' * 60}")
        print(f"MIRA-OJ Memory Bridge Health")
        print(f"{'=' * 60}\n")

        print(f"Bridge Status: {health['bridge_status']}")
        print(f"Vector DB: {'✅' if health['sources']['vector_db'] else '❌'}")
        print(f"Zettels: {health['zettel_count']} available")
        print(f"Sessions: {health['session_count']} available")
        print(f"Last Check: {health['last_check']}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
