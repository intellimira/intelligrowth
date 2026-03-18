import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
import requests


OPEN_NOTEBOOK_API = os.environ.get("OPEN_NOTEBOOK_API", "http://localhost:5055")
CACHE_DIR = Path(__file__).parent.parent.parent / "references" / "open_notebook"


@dataclass
class OpenNotebookSource:
    id: str
    name: str
    type: str
    content: str


@dataclass
class OpenNotebookChatMessage:
    role: str
    content: str
    timestamp: str


@dataclass
class OpenNotebookContent:
    notebook_id: str
    notebook_name: str
    sources: list
    chat_history: list
    fetched_at: str
    content_hash: str


class OpenNotebookIngestor:
    def __init__(self, api_url: str = OPEN_NOTEBOOK_API):
        self.api_url = api_url
        self.cache_dir = CACHE_DIR

    def _api_get(self, endpoint: str) -> dict:
        resp = requests.get(f"{self.api_url}{endpoint}", timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _get_notebooks(self) -> list:
        result = self._api_get("/api/notebooks")
        return result if isinstance(result, list) else []

    def _get_notebook(self, notebook_id: str) -> dict:
        return self._api_get(f"/api/notebooks/{notebook_id}")

    def _get_sources(self, notebook_id: str) -> list:
        try:
            result = self._api_get(f"/api/notebooks/{notebook_id}/sources")
            return result if isinstance(result, list) else []
        except Exception:
            return []

    def _get_source_content(self, source_id: str) -> str:
        try:
            resp = requests.get(f"{self.api_url}/api/sources/{source_id}", timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("content", "") or data.get("text", "")
        except:
            pass
        return ""

    def _get_chat_sessions(self, notebook_id: str) -> list:
        try:
            result = self._api_get(f"/api/notebooks/{notebook_id}/context")
            return result if isinstance(result, list) else []
        except:
            return []

    def find_notebook_by_name(self, name: str) -> Optional[dict]:
        notebooks = self._get_notebooks()
        name_lower = name.lower().strip()

        # First, try exact match
        for nb in notebooks:
            nb_name = (nb.get("name") or "").lower().strip()
            if nb_name == name_lower:
                return nb

        # Then, try partial match (search term in notebook name)
        for nb in notebooks:
            nb_name = (nb.get("name") or "").lower().strip()
            if name_lower in nb_name:
                return nb

        # Finally, try reverse partial (notebook name in search term)
        for nb in notebooks:
            nb_name = (nb.get("name") or "").lower().strip()
            if nb_name in name_lower:
                return nb

        return None

    def find_notebooks_by_names(self, names: list) -> list:
        results = []
        for name in names:
            nb = self.find_notebook_by_name(name.strip())
            if nb:
                results.append(nb)
        return results

    def fetch_notebook(
        self, notebook_id: str, force_refresh: bool = False
    ) -> OpenNotebookContent:
        nb = self._get_notebook(notebook_id)
        notebook_name = nb.get("name", "unnamed")

        cache_path = self.cache_dir / notebook_id
        last_accessed_path = cache_path / "last_accessed.json"

        if not force_refresh and last_accessed_path.exists():
            with open(last_accessed_path) as f:
                last_meta = json.load(f)
                last_hash = last_meta.get("content_hash", "")

                current_data = self._get_notebook(notebook_id)
                current_hash = hashlib.md5(
                    json.dumps(current_data, sort_keys=True).encode()
                ).hexdigest()

                if current_hash == last_hash:
                    cached_content_path = cache_path / "content.md"
                    if cached_content_path.exists():
                        cached = cached_content_path.read_text()
                        return OpenNotebookContent(
                            notebook_id=notebook_id,
                            notebook_name=notebook_name,
                            sources=last_meta.get("sources", []),
                            chat_history=last_meta.get("chat_history", []),
                            fetched_at=last_meta.get("fetched_at", ""),
                            content_hash=last_hash,
                        )

        sources = self._get_sources(notebook_id)
        source_data = []
        source_contents = []

        for src in sources:
            src_id = src.get("id")
            src_name = src.get("name", "unknown")
            src_type = src.get("type", "unknown")

            content = self._get_source_content(src_id)

            source_data.append(
                {
                    "id": src_id,
                    "name": src_name,
                    "type": src_type,
                }
            )

            source_contents.append(
                f"## Source: {src_name} ({src_type})\n\n{content[:5000]}"
            )

        chat_sessions = self._get_chat_sessions(notebook_id)
        chat_history = []
        for session in chat_sessions:
            messages = session.get("messages", [])
            for msg in messages:
                chat_history.append(
                    {
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", ""),
                    }
                )

        content_hash = hashlib.md5(json.dumps(nb, sort_keys=True).encode()).hexdigest()
        fetched_at = datetime.now().isoformat()

        cache_path.mkdir(parents=True, exist_ok=True)

        full_content = f"# {notebook_name}\n\n"
        full_content += f"**Notebook ID:** {notebook_id}\n"
        full_content += f"**Sources:** {len(sources)}\n"
        full_content += f"**Chat Sessions:** {len(chat_sessions)}\n"
        full_content += f"**Fetched:** {fetched_at}\n\n"
        full_content += "---\n\n"
        full_content += "\n\n".join(source_contents)

        if chat_history:
            full_content += "\n\n---\n\n## Chat History\n\n"
            for msg in chat_history[:50]:
                role = msg.get("role", "user")
                text = msg.get("content", "")
                full_content += f"**{role.upper()}:** {text[:1000]}\n\n"

        (cache_path / "content.md").write_text(full_content)
        (cache_path / "metadata.json").write_text(
            json.dumps(
                {
                    "notebook_id": notebook_id,
                    "notebook_name": notebook_name,
                    "sources": source_data,
                    "chat_history": chat_history,
                    "fetched_at": fetched_at,
                },
                indent=2,
            )
        )
        (cache_path / "last_accessed.json").write_text(
            json.dumps(
                {
                    "notebook_id": notebook_id,
                    "content_hash": content_hash,
                    "sources": source_data,
                    "chat_history": chat_history,
                    "fetched_at": fetched_at,
                },
                indent=2,
            )
        )

        return OpenNotebookContent(
            notebook_id=notebook_id,
            notebook_name=notebook_name,
            sources=source_data,
            chat_history=chat_history,
            fetched_at=fetched_at,
            content_hash=content_hash,
        )

    def fetch_multiple_notebooks(
        self, names: list, force_refresh: bool = False
    ) -> OpenNotebookContent:
        notebooks = self.find_notebooks_by_names(names)

        if not notebooks:
            raise ValueError(f"No notebooks found matching: {names}")

        combined_sources = []
        combined_chat = []
        all_content = []

        for nb in notebooks:
            content = self.fetch_notebook(nb["id"], force_refresh)
            combined_sources.extend(content.sources)
            combined_chat.extend(content.chat_history)

            source_md = f"## Notebook: {content.notebook_name}\n\n"
            for src in content.sources:
                source_md += f"- {src['name']} ({src['type']})\n"
            all_content.append(source_md)

        combined_content = f"# Combined Notebooks\n\n"
        combined_content += f"**Notebooks:** {len(notebooks)}\n"
        combined_content += f"**Total Sources:** {len(combined_sources)}\n"
        combined_content += f"**Total Chat Messages:** {len(combined_chat)}\n\n"
        combined_content += "---\n\n"
        combined_content += "\n\n".join(all_content)

        combined_id = "+".join([nb["id"][:8] for nb in notebooks])

        return OpenNotebookContent(
            notebook_id=combined_id,
            notebook_name=" + ".join([nb.get("name", "unnamed") for nb in notebooks]),
            sources=combined_sources,
            chat_history=combined_chat,
            fetched_at=datetime.now().isoformat(),
            content_hash=hashlib.md5(combined_content.encode()).hexdigest(),
        )

    def list_cached(self) -> list:
        if not self.cache_dir.exists():
            return []

        cached = []
        for nb_dir in self.cache_dir.iterdir():
            if nb_dir.is_dir():
                meta_path = nb_dir / "metadata.json"
                if meta_path.exists():
                    with open(meta_path) as f:
                        cached.append(json.load(f))
        return cached


def parse_skillon_command(command: str) -> tuple[list, bool]:
    command = command.strip()

    if command.startswith("/skillOn:"):
        command = command[9:].strip()
    elif command.startswith("/skillop:"):
        command = command[9:].strip()
    elif command.startswith("skillOn:"):
        command = command[8:].strip()
    elif command.startswith("skillop:"):
        command = command[8:].strip()

    force_refresh = "--force" in command or "--refresh" in command
    command = command.replace("--force", "").replace("--refresh", "").strip()

    if "+" in command:
        names = [n.strip() for n in command.split("+")]
    else:
        names = [command]

    return names, force_refresh


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print(
            "  python ingest_open_notebook.py list                    - List notebooks"
        )
        print(
            "  python ingest_open_notebook.py find <name>              - Find notebook by name"
        )
        print(
            "  python ingest_open_notebook.py fetch <name>             - Fetch notebook content"
        )
        print(
            "  python ingest_open_notebook.py fetch nb1 + nb2          - Fetch multiple notebooks"
        )
        print(
            "  python ingest_open_notebook.py cached                   - List cached notebooks"
        )
        sys.exit(1)

    command = sys.argv[1]
    ingestor = OpenNotebookIngestor()

    if command == "list":
        notebooks = ingestor._get_notebooks()
        print(f"Notebooks ({len(notebooks)}):")
        for nb in notebooks:
            print(f"  - {nb.get('name', 'unnamed')} ({nb.get('id', 'no-id')})")

    elif command == "find":
        name = " ".join(sys.argv[2:])
        nb = ingestor.find_notebook_by_name(name)
        if nb:
            print(f"Found: {nb.get('name')} ({nb.get('id')})")
        else:
            print(f"Not found: {name}")

    elif command == "fetch":
        names = " ".join(sys.argv[2:])
        names_list, force_refresh = parse_skillon_command(names)
        if len(names_list) == 1:
            nb = ingestor.find_notebook_by_name(names_list[0])
            if not nb:
                print(f"Not found: {names_list[0]}")
                sys.exit(1)
            content = ingestor.fetch_notebook(nb["id"], force_refresh)
            print(f"Fetched: {content.notebook_name}")
            print(f"Sources: {len(content.sources)}")
            print(f"Chat messages: {len(content.chat_history)}")
        else:
            content = ingestor.fetch_multiple_notebooks(names_list, force_refresh)
            print(f"Fetched {len(names_list)} notebooks")
            print(f"Total sources: {len(content.sources)}")
            print(f"Total chat messages: {len(content.chat_history)}")

    elif command == "cached":
        cached = ingestor.list_cached()
        print(f"Cached notebooks ({len(cached)}):")
        for c in cached:
            print(
                f"  - {c.get('notebook_name', 'unnamed')} ({c.get('notebook_id', 'no-id')})"
            )
