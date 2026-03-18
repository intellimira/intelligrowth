import asyncio
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from notebooklm import NotebookLMClient


NOTEBOOKLM_URL_PATTERN = r"notebooklm\.google\.com/(notebook|user)/[a-zA-Z0-9]+"


@dataclass
class NotebookLMContent:
    notebook_id: str
    title: str
    sources: list
    content: str
    exported_at: str


class NotebookLMIngestor:
    def __init__(self, auth_storage_path: str = "~/.notebooklm/storage_state.json"):
        self.auth_path = os.path.expanduser(auth_storage_path)
        self.auth_storage = self.auth_path

    def extract_notebook_id(self, url: str) -> Optional[str]:
        match = re.search(r"(notebook|user)/([a-zA-Z0-9]+)", url)
        return match.group(2) if match else None

    async def fetch_notebook(self, url: str) -> NotebookLMContent:
        notebook_id = self.extract_notebook_id(url)
        if not notebook_id:
            raise ValueError(f"Could not extract notebook ID from URL: {url}")

        async with await NotebookLMClient.from_storage(self.auth_storage) as client:
            notebooks = await client.notebooks.list()

            target_notebook = None
            for nb in notebooks:
                if nb.id == notebook_id:
                    target_notebook = nb
                    break

            if not target_notebook:
                raise ValueError(
                    f"Notebook {notebook_id} not found. Make sure it's shared with you or you have access."
                )

            sources = []
            source_contents = []

            for source in target_notebook.sources:
                source_info = {
                    "id": source.id,
                    "type": source.type,
                    "name": source.name,
                }
                sources.append(source_info)

                if hasattr(source, "content") and source.content:
                    source_contents.append(
                        f"## Source: {source.name}\n\n{source.content}"
                    )
                elif hasattr(source, "text"):
                    source_contents.append(f"## Source: {source.name}\n\n{source.text}")

            content = f"# {target_notebook.title}\n\n"
            content += f"**Notebook ID:** {notebook_id}\n"
            content += f"**Sources:** {len(sources)}\n\n"
            content += "---\n\n"
            content += "\n\n".join(source_contents)

            return NotebookLMContent(
                notebook_id=notebook_id,
                title=target_notebook.title,
                sources=sources,
                content=content,
                exported_at=datetime.now().isoformat(),
            )

            sources = []
            source_contents = []

            for source in target_notebook.sources:
                source_info = {
                    "id": source.id,
                    "type": source.type,
                    "name": source.name,
                }
                sources.append(source_info)

                if hasattr(source, "content") and source.content:
                    source_contents.append(
                        f"## Source: {source.name}\n\n{source.content}"
                    )
                elif hasattr(source, "text"):
                    source_contents.append(f"## Source: {source.name}\n\n{source.text}")

            content = f"# {target_notebook.title}\n\n"
            content += f"**Notebook ID:** {notebook_id}\n"
            content += f"**Sources:** {len(sources)}\n\n"
            content += "---\n\n"
            content += "\n\n".join(source_contents)

            return NotebookLMContent(
                notebook_id=notebook_id,
                title=target_notebook.title,
                sources=sources,
                content=content,
                exported_at=datetime.now().isoformat(),
            )

    def authenticate(self):
        print("Opening browser for NotebookLM authentication...")
        print("Please log in to your Google account.")
        asyncio.run(self._authenticate())

    async def _authenticate(self):
        os.makedirs(os.path.dirname(self.auth_path), exist_ok=True)
        async with await NotebookLMClient.from_browser() as client:
            await client.save_auth(self.auth_storage)
        print(f"Authentication saved to {self.auth_path}")


def classify_notebooklm_url(url: str) -> bool:
    return bool(re.search(NOTEBOOKLM_URL_PATTERN, url, re.IGNORECASE))


async def ingest_notebooklm(
    url: str, output_dir: str = "references"
) -> NotebookLMContent:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    ingestor = NotebookLMIngestor()
    content = await ingestor.fetch_notebook(url)

    safe_name = content.notebook_id[:16]
    output_path = Path(output_dir) / f"notebooklm_{safe_name}.md"
    output_path.write_text(content.content)

    print(f"Fetched notebook: {content.title}")
    print(f"Sources: {len(content.sources)}")
    print(f"Saved to: {output_path}")

    return content


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ingest_notebooklm.py auth    - Authenticate with NotebookLM")
        print("  python ingest_notebooklm.py <url>   - Fetch notebook content")
        sys.exit(1)

    command = sys.argv[1]

    if command == "auth":
        ingestor = NotebookLMIngestor()
        ingestor.authenticate()
    else:
        asyncio.run(ingest_notebooklm(command))
