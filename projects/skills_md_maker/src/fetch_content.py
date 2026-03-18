import os
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional


PROJECT_ROOT = Path(__file__).parent.parent
REFERENCES_DIR = PROJECT_ROOT / "references"


@dataclass
class FetchedContent:
    url: str
    url_type: str
    content: str
    timestamp: str
    file_path: str


class ContentFetcher:
    def __init__(self):
        self.references_dir = REFERENCES_DIR
        self.references_dir.mkdir(parents=True, exist_ok=True)

    def prepare(self, url: str, url_type: str) -> str:
        """Create timestamp folder for this fetch session"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = self.references_dir / timestamp
        session_dir.mkdir(parents=True, exist_ok=True)

        meta = {
            "url": url,
            "url_type": url_type,
            "timestamp": timestamp,
            "status": "pending_fetch",
        }

        meta_file = session_dir / "meta.json"
        with open(meta_file, "w") as f:
            json.dump(meta, f, indent=2)

        return timestamp

    def save_content(
        self, timestamp: str, content: str, url: str, url_type: str
    ) -> FetchedContent:
        """Save fetched content to references/<timestamp>/content.md"""
        session_dir = self.references_dir / timestamp
        content_file = session_dir / "content.md"

        header = f"""---
url: {url}
type: {url_type}
fetched: {datetime.now().isoformat()}
---

"""

        with open(content_file, "w") as f:
            f.write(header + content)

        meta_file = session_dir / "meta.json"
        with open(meta_file, "r") as f:
            meta = json.load(f)

        meta["status"] = "fetched"
        meta["content_length"] = len(content)

        with open(meta_file, "w") as f:
            json.dump(meta, f, indent=2)

        return FetchedContent(
            url=url,
            url_type=url_type,
            content=content,
            timestamp=timestamp,
            file_path=str(content_file),
        )

    def get_latest_session(self) -> Optional[str]:
        """Get most recent fetch session timestamp"""
        if not self.references_dir.exists():
            return None

        sessions = sorted(
            [d.name for d in self.references_dir.iterdir() if d.is_dir()], reverse=True
        )
        return sessions[0] if sessions else None

    def load_content(self, timestamp: str) -> Optional[FetchedContent]:
        """Load content from a specific session"""
        session_dir = self.references_dir / timestamp
        content_file = session_dir / "content.md"
        meta_file = session_dir / "meta.json"

        if not content_file.exists():
            return None

        with open(meta_file, "r") as f:
            meta = json.load(f)

        with open(content_file, "r") as f:
            content = f.read()

        return FetchedContent(
            url=meta.get("url", ""),
            url_type=meta.get("url_type", "web"),
            content=content,
            timestamp=timestamp,
            file_path=str(content_file),
        )


def get_fetch_instructions(url_type: str) -> str:
    """Get instructions for which tool to use based on URL type"""
    instructions = {
        "youtube": """Use webfetch to fetch the YouTube page content. Also search for transcripts or related documentation.
Extract: video title, description, key concepts, tools mentioned, patterns demonstrated.""",
        "github": """Use codesearch to find relevant documentation. Search for README, API docs, or examples.
Extract: project name, description, main features, tools/frameworks used, patterns, conventions.""",
        "reddit": """Use webfetch to fetch the Reddit post and top comments.
Extract: problem discussed, solutions proposed, tools mentioned, pain points, recommendations.""",
        "arxiv": """Use codesearch to fetch the paper abstract and key sections.
Extract: paper title, abstract, key concepts, methodology, tools, potential applications.""",
        "web": """Use webfetch to fetch the webpage content.
Extract: title, main content, key concepts, tools mentioned, patterns, conventions.""",
    }

    return instructions.get(url_type, instructions["web"])


if __name__ == "__main__":
    fetcher = ContentFetcher()

    print("ContentFetcher initialized")
    print(f"References directory: {fetcher.references_dir}")

    latest = fetcher.get_latest_session()
    if latest:
        print(f"Latest session: {latest}")
    else:
        print("No sessions found")
