import os
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict

from ingest_folder import FolderScanner, FileInfo


@dataclass
class AggregatedContent:
    content: str
    file_count: int
    total_size: int
    file_index: Dict[str, str | list]
    dominant_type: str
    timestamp: str


class ContentAggregator:
    MAX_FILE_SIZE = 500_000

    def __init__(self):
        self.scanner = FolderScanner()

    def aggregate(self, folder_path: str, session_dir: str) -> AggregatedContent:
        scan = self.scanner.scan(folder_path)

        content_parts = []
        file_index = {}

        for file_info in scan.files:
            file_content = self._read_file(file_info.path)
            if file_content:
                header = f"\n\n{'=' * 60}\n"
                header += f"FILE: {file_info.relative_path}\n"
                header += f"TYPE: {file_info.file_type}\n"
                header += f"{'=' * 60}\n\n"

                content_parts.append(header + file_content)
                file_index[file_info.relative_path] = (
                    f"lines: {len(file_content.splitlines())}"
                )

        full_content = "\n".join(content_parts)

        meta = {
            "root_path": folder_path,
            "session_dir": session_dir,
            "file_count": scan.file_count,
            "total_size": scan.total_size,
            "dominant_type": scan.extensions,
            "timestamp": datetime.now().isoformat(),
        }

        meta_file = Path(session_dir) / "content_meta.json"
        with open(meta_file, "w") as f:
            json.dump(meta, f, indent=2)

        content_file = Path(session_dir) / "content.md"
        with open(content_file, "w") as f:
            f.write(full_content)

        return AggregatedContent(
            content=full_content,
            file_count=scan.file_count,
            total_size=scan.total_size,
            file_index=file_index,
            dominant_type=self.scanner.detect_dominant_type(scan),
            timestamp=datetime.now().isoformat(),
        )

    def aggregate_single_file(
        self, file_path: str, session_dir: str
    ) -> AggregatedContent:
        content = self._read_file(file_path)

        if not content:
            return AggregatedContent(
                content="",
                file_count=0,
                total_size=0,
                file_index={},
                dominant_type="empty",
                timestamp=datetime.now().isoformat(),
            )

        file_info = FileInfo(
            path=file_path,
            relative_path=Path(file_path).name,
            extension=Path(file_path).suffix,
            size=len(content),
            file_type=self.scanner.EXTENSION_TYPES.get(
                Path(file_path).suffix.lower(), "other"
            ),
        )

        full_content = f"""{"=" * 60}
FILE: {file_info.relative_path}
TYPE: {file_info.file_type}
{"=" * 60}

{content}"""

        content_file = Path(session_dir) / "content.md"
        with open(content_file, "w") as f:
            f.write(full_content)

        return AggregatedContent(
            content=full_content,
            file_count=1,
            total_size=len(content),
            file_index={file_info.relative_path: f"lines: {len(content.splitlines())}"},
            dominant_type=file_info.file_type,
            timestamp=datetime.now().isoformat(),
        )

    def _read_file(self, file_path: str) -> Optional[str]:
        path = Path(file_path)

        if not path.exists():
            return None

        try:
            stat = path.stat()
            if stat.st_size > self.MAX_FILE_SIZE:
                return f"[FILE TOO LARGE - {stat.st_size:,} bytes - truncated]"
        except:
            pass

        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(path, "r", encoding="latin-1") as f:
                    return f.read()
            except:
                return "[BINARY FILE - skipped]"
        except Exception as e:
            return f"[ERROR reading file: {e}]"

    def extract_code_summary(self, content: str) -> str:
        lines = content.split("\n")

        functions = []
        classes = []
        imports = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("import ") or stripped.startswith("from "):
                imports.append(stripped)
            elif "def " in stripped and "(" in stripped:
                functions.append(stripped)
            elif "class " in stripped and ":" in stripped:
                classes.append(stripped)

        summary = []
        if imports:
            summary.append(f"Imports ({len(imports)}): {', '.join(imports[:5])}")
        if classes:
            summary.append(f"Classes ({len(classes)}): {', '.join(classes[:5])}")
        if functions:
            summary.append(f"Functions ({len(functions)}): {', '.join(functions[:5])}")

        return "\n".join(summary) if summary else "No code structures detected"


def aggregate_folder(folder_path: str, session_dir: str) -> AggregatedContent:
    aggregator = ContentAggregator()
    return aggregator.aggregate(folder_path, session_dir)


def aggregate_file(file_path: str, session_dir: str) -> AggregatedContent:
    aggregator = ContentAggregator()
    return aggregator.aggregate_single_file(file_path, session_dir)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "/home/sir-v/MiRA/skills/opencode-builder"

    from pathlib import Path

    session_dir = str(Path(path).parent / "test_session")
    Path(session_dir).mkdir(parents=True, exist_ok=True)

    result = aggregate_folder(path, session_dir)

    print(f"Files aggregated: {result.file_count}")
    print(f"Dominant type: {result.dominant_type}")
    print(f"Total size: {result.total_size:,} chars")
    print(f"\nFile index:")
    for k, v in list(result.file_index.items())[:5]:
        print(f"  {k}: {v}")
