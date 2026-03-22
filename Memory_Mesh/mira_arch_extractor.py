"""
MIRA_ARCH Data Extraction Pipeline
Extracts and prepares data from MIRA_ARCH backup for training

Categories:
- sessions: Conversational logs
- council: Multi-persona decision logs
- zettels: Knowledge notes
- diagnostics: Problem-solving patterns
- implementations: Decision execution logs
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
import re


@dataclass
class ExtractedDocument:
    """A single extracted document."""

    id: str
    category: str
    source_file: str
    title: str
    content: str
    tokens_estimate: int
    created_date: Optional[str]
    quality_score: float  # 0-1 based on content quality
    metadata: Dict


class MIRAARCHExtractor:
    """
    Extract structured data from MIRA_ARCH backup.

    Filters and categorizes content for training datasets.
    """

    CATEGORIES = {
        "session": ["session", "convo", "conversation"],
        "council": ["council", "cabal", "persona", "decision"],
        "zettel": ["zettel", "note", "knowledge"],
        "diagnostic": ["diagnostic", "debug", "issue", "problem"],
        "implementation": ["plan", "implement", "execution"],
        "technical": ["code", "api", "backend", "frontend"],
    }

    def __init__(self, source_dir: str):
        self.source_dir = Path(source_dir)
        self.documents: List[ExtractedDocument] = []
        self.stats = {
            "total_files": 0,
            "total_docs": 0,
            "by_category": {},
            "total_tokens": 0,
            "filtered_out": 0,
        }

    def extract_all(self, output_dir: str) -> Dict:
        """Extract all documents from MIRA_ARCH."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        print("=" * 60)
        print("MIRA_ARCH Data Extraction")
        print("=" * 60)

        # Phase 1: Scan and extract
        print("\n[1/4] Scanning MIRA_ARCH...")
        md_files = list(self.source_dir.rglob("*.md"))
        self.stats["total_files"] = len(md_files)
        print(f"  Found {len(md_files)} markdown files")

        # Phase 2: Extract and categorize
        print("\n[2/4] Extracting documents...")
        for i, file_path in enumerate(md_files):
            if i % 100 == 0:
                print(f"  Processing {i}/{len(md_files)}...")

            try:
                doc = self._extract_document(file_path)
                if doc and doc.quality_score > 0.3:  # Filter low quality
                    self.documents.append(doc)
                    self.stats["total_docs"] += 1
                    self.stats["total_tokens"] += doc.tokens_estimate

                    cat = doc.category
                    self.stats["by_category"][cat] = (
                        self.stats["by_category"].get(cat, 0) + 1
                    )
            except Exception as e:
                self.stats["filtered_out"] += 1

        print(f"  Extracted {len(self.documents)} high-quality documents")

        # Phase 3: Create training datasets
        print("\n[3/4] Creating training datasets...")
        self._create_datasets(output_dir)

        # Phase 4: Generate reports
        print("\n[4/4] Generating reports...")
        self._generate_reports(output_dir)

        return self.stats

    def _extract_document(self, file_path: Path) -> Optional[ExtractedDocument]:
        """Extract a single document."""
        # Read content
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None

        # Skip very short or empty files
        if len(content) < 100:
            return None

        # Categorize
        category = self._categorize(file_path, content)

        # Extract title
        title = self._extract_title(content, file_path)

        # Estimate tokens (rough: 4 chars per token)
        tokens = len(content) // 4

        # Quality score based on content
        quality = self._calculate_quality(content, category)

        # Extract date if available
        date = self._extract_date(content)

        doc = ExtractedDocument(
            id=self._generate_id(file_path),
            category=category,
            source_file=str(file_path),
            title=title,
            content=content,
            tokens_estimate=tokens,
            created_date=date,
            quality_score=quality,
            metadata={
                "file_size": file_path.stat().st_size,
                "file_path": str(file_path.relative_to(self.source_dir)),
            },
        )

        return doc

    def _categorize(self, file_path: Path, content: str) -> str:
        """Categorize a document based on path and content."""
        path_str = str(file_path).lower()
        content_lower = content.lower()

        for category, keywords in self.CATEGORIES.items():
            for keyword in keywords:
                if keyword in path_str or keyword in content_lower[:500]:
                    return category

        return "general"

    def _extract_title(self, content: str, file_path: Path) -> str:
        """Extract title from content or filename."""
        # Try first line (markdown title)
        lines = content.split("\n")
        for line in lines[:5]:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()[:100]

        # Fall back to filename
        return file_path.stem[:100]

    def _calculate_quality(self, content: str, category: str) -> float:
        """Calculate content quality score."""
        score = 0.5

        # Length factor
        if len(content) > 1000:
            score += 0.1
        if len(content) > 5000:
            score += 0.1

        # Code blocks (good for training)
        if "```" in content:
            score += 0.1

        # Lists (structured content)
        if content.count("\n- ") > 3:
            score += 0.1

        # Headers (well-structured)
        if content.count("\n#") > 2:
            score += 0.1

        # Penalize for too much noise
        if content.count("```png") > 5:
            score -= 0.2

        return min(1.0, max(0.0, score))

    def _extract_date(self, content: str) -> Optional[str]:
        """Extract date from content."""
        # Common date patterns
        patterns = [
            r"\d{4}-\d{2}-\d{2}",
            r"\d{2}/\d{2}/\d{4}",
            r"\w+ \d{1,2}, \d{4}",
        ]

        for pattern in patterns:
            match = re.search(pattern, content[:500])
            if match:
                return match.group(0)

        return None

    def _generate_id(self, file_path: Path) -> str:
        """Generate unique ID for document."""
        rel_path = str(file_path.relative_to(self.source_dir))
        # Hash for uniqueness
        hash_val = hash(rel_path) % 100000
        return f"doc_{hash_val:05d}"

    def _create_datasets(self, output_dir: Path):
        """Create structured training datasets."""

        # Group by category
        by_category: Dict[str, List[ExtractedDocument]] = {}
        for doc in self.documents:
            cat = doc.category
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(doc)

        # Dataset 1: Weave Training (zettels, links, summaries)
        weave_docs = [
            d
            for d in self.documents
            if d.category in ["zettel", "council", "diagnostic"]
        ]
        self._save_jsonl(weave_docs, output_dir / "weave_training.jsonl")
        print(f"  Weave dataset: {len(weave_docs)} documents")

        # Dataset 2: MIRA-OJ Training (sessions, reasoning)
        mira_docs = [
            d
            for d in self.documents
            if d.category in ["session", "council", "implementation"]
        ]
        self._save_jsonl(mira_docs, output_dir / "miraoj_training.jsonl")
        print(f"  MIRA-OJ dataset: {len(mira_docs)} documents")

        # Dataset 3: Full combined dataset
        self._save_jsonl(self.documents, output_dir / "full_dataset.jsonl")
        print(f"  Full dataset: {len(self.documents)} documents")

        # Dataset 4: Session logs only (for conversational training)
        session_docs = [d for d in self.documents if d.category == "session"]
        self._save_jsonl(session_docs, output_dir / "session_logs.jsonl")
        print(f"  Session logs: {len(session_docs)} documents")

        # Dataset 5: Council decisions (for persona training)
        council_docs = [d for d in self.documents if d.category == "council"]
        self._save_jsonl(council_docs, output_dir / "council_decisions.jsonl")
        print(f"  Council decisions: {len(council_docs)} documents")

    def _save_jsonl(self, docs: List[ExtractedDocument], output_path: Path):
        """Save documents as JSONL."""
        with open(output_path, "w", encoding="utf-8") as f:
            for doc in docs:
                # Include full content for training
                record = {
                    "id": doc.id,
                    "category": doc.category,
                    "title": doc.title,
                    "content": doc.content,
                    "tokens_estimate": doc.tokens_estimate,
                    "quality_score": doc.quality_score,
                    "created_date": doc.created_date,
                    "metadata": doc.metadata,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _generate_reports(self, output_dir: Path):
        """Generate extraction reports."""

        report = f"""
# MIRA_ARCH Data Extraction Report

**Date:** {datetime.now().isoformat()}
**Source:** {self.source_dir}

## Statistics

| Metric | Value |
|--------|-------|
| Total Files Scanned | {self.stats["total_files"]:,} |
| High-Quality Documents | {self.stats["total_docs"]:,} |
| Estimated Tokens | {self.stats["total_tokens"]:,} |
| Filtered Out | {self.stats["filtered_out"]:,} |

## By Category

| Category | Documents |
|----------|-----------|
"""

        for cat, count in sorted(self.stats["by_category"].items()):
            report += f"| {cat.capitalize()} | {count:,} |\n"

        report += f"""
## Training Datasets Created

| Dataset | Purpose |
|---------|---------|
| weave_training.jsonl | Zettel linking & summarization |
| miraoj_training.jsonl | Response generation |
| full_dataset.jsonl | All high-quality content |
| session_logs.jsonl | Conversational patterns |
| council_decisions.jsonl | Multi-persona decisions |

## Quality Thresholds

- Minimum content length: 100 characters
- Minimum quality score: 0.3
- Categories: session, council, zettel, diagnostic, implementation, technical

---
*Generated by MIRA_ARCH Extractor*
"""

        report_path = output_dir / "extraction_report.md"
        report_path.write_text(report)
        print(f"  Report: {report_path}")


def main():
    """CLI for extraction."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA_ARCH Data Extraction")
    parser.add_argument(
        "--source",
        default="/media/sir-v/BackUP/Everything2302/Ai/Lastes Mira160126/MIRA3.0/MIRA_ARCH",
        help="Source directory",
    )
    parser.add_argument(
        "--output", default="~/MIRA_ARCH_extracted", help="Output directory"
    )

    args = parser.parse_args()

    extractor = MIRAARCHExtractor(args.source)
    stats = extractor.extract_all(os.path.expanduser(args.output))

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"Documents: {stats['total_docs']:,}")
    print(f"Tokens: {stats['total_tokens']:,}")
    print(f"Categories: {list(stats['by_category'].keys())}")


if __name__ == "__main__":
    main()
