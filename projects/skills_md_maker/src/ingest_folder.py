import os
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict


PROJECT_ROOT = Path(__file__).parent.parent
REFERENCES_DIR = PROJECT_ROOT / "references"


@dataclass
class FileInfo:
    path: str
    relative_path: str
    extension: str
    size: int
    file_type: str


@dataclass
class FolderScan:
    root_path: str
    files: List[FileInfo]
    total_size: int
    file_count: int
    extensions: Dict[str, int]
    timestamp: str
    session_dir: str


class FolderScanner:
    EXTENSION_TYPES = {
        ".md": "document",
        ".py": "code",
        ".js": "code",
        ".ts": "code",
        ".jsx": "code",
        ".tsx": "code",
        ".json": "data",
        ".yaml": "config",
        ".yml": "config",
        ".txt": "document",
        ".go": "code",
        ".rs": "code",
        ".java": "code",
        ".c": "code",
        ".cpp": "code",
        ".h": "code",
        ".cs": "code",
        ".rb": "code",
        ".php": "code",
        ".sh": "script",
        ".bash": "script",
        ".sql": "code",
        ".html": "web",
        ".css": "web",
        ".scss": "web",
        ".xml": "config",
        ".toml": "config",
        ".ini": "config",
        ".env": "config",
        ".gitignore": "config",
        "README": "document",
        "LICENSE": "document",
    }

    IGNORE_DIRS = {
        "__pycache__",
        ".git",
        ".venv",
        "node_modules",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "dist",
        "build",
        ".next",
        ".nuxt",
        "coverage",
        ".tox",
        "venv",
        "env",
        ".env.local",
    }

    IGNORE_FILES = {
        ".DS_Store",
        "Thumbs.db",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "poetry.lock",
        "requirements.txt",
    }

    def __init__(self):
        self.references_dir = REFERENCES_DIR
        self.references_dir.mkdir(parents=True, exist_ok=True)

    def scan(
        self, folder_path: str, recursive: bool = True, max_depth: int = 10
    ) -> FolderScan:
        root = Path(folder_path)

        if not root.exists():
            raise FileNotFoundError(f"Path does not exist: {folder_path}")

        if not root.is_dir():
            return self._scan_file(root)

        files = []
        extensions = {}
        total_size = 0

        if recursive:
            for item in root.rglob("*"):
                if item.is_file():
                    file_info = self._process_file(item, root)
                    if file_info:
                        files.append(file_info)
                        total_size += file_info.size
                        ext = file_info.extension or "no_ext"
                        extensions[ext] = extensions.get(ext, 0) + 1
        else:
            for item in root.iterdir():
                if item.is_file():
                    file_info = self._process_file(item, root)
                    if file_info:
                        files.append(file_info)
                        total_size += file_info.size
                        ext = file_info.extension or "no_ext"
                        extensions[ext] = extensions.get(ext, 0) + 1

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = self.references_dir / f"folder_{timestamp}"
        session_dir.mkdir(parents=True, exist_ok=True)

        scan_result = FolderScan(
            root_path=str(root),
            files=files,
            total_size=total_size,
            file_count=len(files),
            extensions=extensions,
            timestamp=timestamp,
            session_dir=str(session_dir),
        )

        self._save_scan_meta(scan_result)

        return scan_result

    def _scan_file(self, file_path: Path) -> FolderScan:
        root = file_path.parent
        file_info = self._process_file(file_path, root)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = self.references_dir / f"file_{timestamp}"
        session_dir.mkdir(parents=True, exist_ok=True)

        return FolderScan(
            root_path=str(root),
            files=[file_info] if file_info else [],
            total_size=file_info.size if file_info else 0,
            file_count=1,
            extensions={file_info.extension: 1} if file_info else {},
            timestamp=timestamp,
            session_dir=str(session_dir),
        )

    def _process_file(self, file_path: Path, root: Path) -> Optional[FileInfo]:
        if file_path.name in self.IGNORE_FILES:
            return None

        for ignore_dir in self.IGNORE_DIRS:
            if ignore_dir in file_path.parts:
                return None

        try:
            stat = file_path.stat()
        except (PermissionError, OSError):
            return None

        ext = file_path.suffix.lower()
        if not ext and file_path.name.upper() in ["README", "LICENSE", "TODO"]:
            ext = file_path.name.upper()

        file_type = self.EXTENSION_TYPES.get(ext, "other")

        return FileInfo(
            path=str(file_path),
            relative_path=str(file_path.relative_to(root)),
            extension=ext,
            size=stat.st_size,
            file_type=file_type,
        )

    def _save_scan_meta(self, scan: FolderScan):
        meta = {
            "root_path": scan.root_path,
            "file_count": scan.file_count,
            "total_size": scan.total_size,
            "extensions": scan.extensions,
            "timestamp": scan.timestamp,
            "files": [asdict(f) for f in scan.files[:100]],
        }

        meta_file = Path(scan.session_dir) / "scan_meta.json"
        with open(meta_file, "w") as f:
            json.dump(meta, f, indent=2)

    def detect_dominant_type(self, scan: FolderScan) -> str:
        if not scan.files:
            return "empty"

        type_counts = {}
        for f in scan.files:
            type_counts[f.file_type] = type_counts.get(f.file_type, 0) + 1

        return max(type_counts, key=type_counts.get)

    def get_file_list(
        self, scan: FolderScan, file_type: Optional[str] = None
    ) -> List[FileInfo]:
        if file_type:
            return [f for f in scan.files if f.file_type == file_type]
        return scan.files


def scan_folder(folder_path: str, recursive: bool = True) -> FolderScan:
    scanner = FolderScanner()
    return scanner.scan(folder_path, recursive)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "/home/sir-v/MiRA/skills"

    scan = scan_folder(path)

    print(f"Scanned: {scan.root_path}")
    print(f"Files: {scan.file_count}")
    print(f"Total size: {scan.total_size:,} bytes")
    print(f"\nExtensions:")
    for ext, count in sorted(scan.extensions.items(), key=lambda x: -x[1])[:10]:
        print(f"  {ext}: {count}")

    print(f"\nDominant type: {FolderScanner().detect_dominant_type(scan)}")
