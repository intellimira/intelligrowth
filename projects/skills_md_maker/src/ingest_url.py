import re
import os
from dataclasses import dataclass
from typing import Optional, Literal
from datetime import datetime
from pathlib import Path


@dataclass
class InputInfo:
    input_path: str
    input_type: Literal["url", "folder", "file"] = "url"
    url_type: Optional[str] = "web"
    source: str = ""
    identifier: Optional[str] = None
    timestamp: str = ""

    def __post_init__(self):
        if self.timestamp is None or self.timestamp == "":
            self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    @property
    def type(self) -> str:
        return self.input_type


class InputClassifier:
    URL_PATTERNS = {
        "youtube": [
            r"youtube\.com/watch",
            r"youtu\.be/",
            r"youtube\.com/shorts",
            r"m\.youtube\.com",
        ],
        "github": [
            r"github\.com/[\w-]+/[\w-]+",
            r"github\.com/[\w-]+/[\w-]+/blob",
            r"github\.com/[\w-]+/[\w-]+/tree",
            r"raw\.githubusercontent\.com",
        ],
        "reddit": [
            r"reddit\.com/r/",
            r"old\.reddit\.com/r/",
        ],
        "arxiv": [
            r"arxiv\.org/abs/",
            r"arxiv\.org/pdf/",
        ],
        "notebooklm": [
            r"notebooklm\.google\.com/notebook/",
            r"notebooklm\.google\.com/user/",
        ],
        "open_notebook": [
            r"^/skillOn:",
            r"^/skillop:",
            r"^skillOn:",
            r"^skillop:",
        ],
        "web": [
            r"https?://",
        ],
    }

    SUPPORTED_EXTENSIONS = {
        ".md",
        ".py",
        ".json",
        ".txt",
        ".yaml",
        ".yml",
        ".js",
        ".ts",
        ".go",
        ".rs",
        ".java",
    }

    def classify(self, user_input: str) -> InputInfo:
        user_input = user_input.strip()

        if (
            user_input.startswith("/skillOn:")
            or user_input.startswith("/skillon:")
            or user_input.startswith("/skillop:")
            or user_input.startswith("/skillon:")
            or user_input.startswith("skillOn:")
            or user_input.startswith("skillon:")
            or user_input.startswith("skillop:")
            or user_input.startswith("skillon:")
        ):
            return self._classify_open_notebook(user_input)

        if self._is_url(user_input):
            return self._classify_url(user_input)
        elif self._is_local_path(user_input):
            return self._classify_local_path(user_input)
        else:
            return InputInfo(
                input_path=user_input,
                input_type="url",
                url_type="web",
                source="unknown",
            )

    def _is_url(self, user_input: str) -> bool:
        return user_input.startswith("http://") or user_input.startswith("https://")

    def _classify_open_notebook(self, user_input: str) -> InputInfo:
        if user_input.startswith("/skillOn:"):
            notebook_name = user_input[9:].strip()
        elif user_input.startswith("/skillon:"):
            notebook_name = user_input[9:].strip()
        elif user_input.startswith("/skillop:"):
            notebook_name = user_input[9:].strip()
        elif user_input.startswith("skillOn:"):
            notebook_name = user_input[8:].strip()
        elif user_input.startswith("skillon:"):
            notebook_name = user_input[8:].strip()
        elif user_input.startswith("skillop:"):
            notebook_name = user_input[8:].strip()
        else:
            notebook_name = user_input

        return InputInfo(
            input_path=user_input,
            input_type="url",
            url_type="open_notebook",
            source=notebook_name,
            identifier=notebook_name,
        )

    def _is_local_path(self, user_input: str) -> bool:
        path = Path(user_input)
        if path.exists():
            return True
        if (
            user_input.startswith("/")
            or user_input.startswith("./")
            or user_input.startswith("../")
        ):
            expanded = Path(os.path.expanduser(user_input))
            if expanded.exists():
                return True
        return False

    def _classify_url(self, url: str) -> InputInfo:
        for url_type, patterns in self.URL_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    identifier = self._extract_identifier(url, url_type)
                    return InputInfo(
                        input_path=url,
                        input_type="url",
                        url_type=url_type,
                        source=self._get_source_name(url, url_type),
                        identifier=identifier,
                    )
        return InputInfo(input_path=url, input_type="url", url_type="web", source="web")

    def _classify_local_path(self, path_str: str) -> InputInfo:
        expanded = Path(os.path.expanduser(path_str))

        if not expanded.exists():
            return InputInfo(
                input_path=path_str, input_type="folder", source="not_found"
            )

        if expanded.is_dir():
            return InputInfo(
                input_path=str(expanded),
                input_type="folder",
                source=expanded.name,
            )
        elif expanded.is_file():
            ext = expanded.suffix.lower()
            return InputInfo(
                input_path=str(expanded),
                input_type="file",
                source=expanded.name,
            )

        return InputInfo(input_path=path_str, input_type="folder", source="unknown")

    def _extract_identifier(self, url: str, url_type: str) -> Optional[str]:
        if url_type == "youtube":
            match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
            return match.group(1) if match else None

        elif url_type == "github":
            match = re.search(r"github\.com/([\w-]+/[\w-]+)", url)
            return match.group(1) if match else None

        elif url_type == "reddit":
            match = re.search(r"reddit\.com/r/([\w-]+)", url)
            return match.group(1) if match else None

        elif url_type == "arxiv":
            match = re.search(r"arxiv\.org/(abs|pdf)/(\d+\.\d+)", url)
            return match.group(2) if match else None

        elif url_type == "notebooklm":
            match = re.search(
                r"notebooklm\.google\.com/(notebook|user)/([a-zA-Z0-9]+)", url
            )
            return match.group(2) if match else None

        return None

    def _get_source_name(self, url: str, url_type: str) -> str:
        if url_type == "youtube":
            return "youtube"
        elif url_type == "github":
            match = re.search(r"github\.com/([\w-]+)", url)
            return f"github:{match.group(1)}" if match else "github"
        elif url_type == "reddit":
            return "reddit"
        elif url_type == "arxiv":
            return "arxiv"
        elif url_type == "notebooklm":
            return "notebooklm"
        else:
            try:
                from urllib.parse import urlparse

                return urlparse(url).netloc
            except:
                return "web"


# Backward compatibility alias
URLInfo = InputInfo
URLClassifier = InputClassifier


def parse_skillm_command(command: str) -> tuple[str, Optional[str]]:
    """Parse /skillm <URL> or /skillm recommend <task>"""
    command = command.strip()

    if command.startswith("/skillm"):
        rest = command[7:].strip()
    elif command.startswith("skillm"):
        rest = command[6:].strip()
    else:
        rest = command

    if rest.startswith("recommend"):
        task = rest[9:].strip()
        return "recommend", task

    if rest.startswith("index"):
        return "index", None

    if rest.startswith("ingest"):
        return "ingest", None

    return "ingest", rest


if __name__ == "__main__":
    import sys

    test_inputs = [
        "https://github.com/BUPT-GAMMA/MASFactory",
        "https://www.youtube.com/watch?v=QFlQuX_cddk",
        "https://reddit.com/r/microsaas",
        "https://arxiv.org/abs/2603.06007",
        "https://example.com/article",
        "/home/sir-v/MiRA/skills",
        "./projects/skills_md_maker",
    ]

    classifier = InputClassifier()
    for inp in test_inputs:
        info = classifier.classify(inp)
        print(
            f"{info.input_type:10} | {info.url_type or 'N/A':10} | {info.source:30} | {info.input_path[:40]}"
        )
