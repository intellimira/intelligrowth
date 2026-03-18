import json
import pickle
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional
import numpy as np
from datetime import datetime


PROJECT_ROOT = Path(__file__).parent.parent
VECTORDB_DIR = PROJECT_ROOT / "vectordb"
SKILLS_ROOT = Path("/home/sir-v/MiRA/skills")


@dataclass
class SkillIndex:
    name: str
    description: str
    triggers: List[str]
    tools: List[str]
    persona: str
    mira_tier: int
    file_path: str
    indexed_at: str


class SkillIndexer:
    def __init__(self):
        self.vectordb_dir = VECTORDB_DIR
        self.vectordb_dir.mkdir(parents=True, exist_ok=True)

        self.index_file = self.vectordb_dir / "skills_index.pkl"
        self.meta_file = self.vectordb_dir / "skills_meta.json"

        self.skills: List[SkillIndex] = []
        self.embeddings: Optional[np.ndarray] = None

        self._load_index()

    def _load_index(self):
        """Load existing index"""
        if self.index_file.exists():
            try:
                with open(self.index_file, "rb") as f:
                    data = pickle.load(f)
                    self.skills = data.get("skills", [])
                    self.embeddings = data.get("embeddings")
            except Exception as e:
                print(f"Failed to load index: {e}")

    def _save_index(self):
        """Save index to disk"""
        with open(self.index_file, "wb") as f:
            pickle.dump({"skills": self.skills, "embeddings": self.embeddings}, f)

        meta = {
            "skills_count": len(self.skills),
            "indexed_at": datetime.now().isoformat(),
            "skills": [asdict(s) for s in self.skills],
        }

        with open(self.meta_file, "w") as f:
            json.dump(meta, f, indent=2)

    def _extract_text(self, skill: SkillIndex) -> str:
        """Extract searchable text from skill"""
        parts = [
            skill.name,
            skill.description,
            " ".join(skill.triggers),
            " ".join(skill.tools),
            skill.persona,
        ]
        return " ".join(parts)

    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text using masfactory or fallback"""
        try:
            from masfactory.utils.embedding import TfidfEmbedder

            all_texts = [self._extract_text(s) for s in self.skills]
            embedder = TfidfEmbedder(documents=all_texts, max_features=512)
            func = embedder.get_embedding_function()
            return func(text)
        except Exception as e:
            print(f"Using fallback embedding: {e}")
            return self._simple_hash_embedding(text)

    def _simple_hash_embedding(self, text: str, dim: int = 128) -> np.ndarray:
        """Simple hash-based embedding as fallback"""
        vec = np.zeros(dim)
        for i, char in enumerate(text.lower()):
            vec[ord(char) % dim] += 1

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm

        return vec

    def index_skill(self, skill_path: Path) -> bool:
        """Index a single skill"""
        if not skill_path.exists() or skill_path.suffix != ".md":
            return False

        try:
            with open(skill_path, "r") as f:
                content = f.read()

            name = skill_path.stem
            description = ""
            triggers = []
            tools = []
            persona = ""
            mira_tier = 1

            for line in content.split("\n"):
                line = line.strip()

                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip()
                elif line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()
                elif line.startswith("triggers:"):
                    triggers_str = line.split(":", 1)[1].strip().strip("[]")
                    triggers = [
                        t.strip().strip('"').strip("'")
                        for t in triggers_str.split(",")
                        if t.strip()
                    ]
                elif line.startswith("tools:"):
                    tools_str = line.split(":", 1)[1].strip().strip("[]")
                    tools = [
                        t.strip().strip('"').strip("'")
                        for t in tools_str.split(",")
                        if t.strip()
                    ]
                elif line.startswith("persona:"):
                    persona = line.split(":", 1)[1].strip().strip('"')
                elif line.startswith("mira_tier:"):
                    try:
                        mira_tier = int(line.split(":", 1)[1].strip())
                    except:
                        pass

            skill_index = SkillIndex(
                name=name,
                description=description,
                triggers=triggers,
                tools=tools,
                persona=persona,
                mira_tier=mira_tier,
                file_path=str(skill_path),
                indexed_at=datetime.now().isoformat(),
            )

            text = self._extract_text(skill_index)
            embedding = self._get_embedding(text)

            self.skills.append(skill_index)

            if self.embeddings is None:
                self.embeddings = embedding.reshape(1, -1)
            else:
                self.embeddings = np.vstack([self.embeddings, embedding])

            self._save_index()

            return True

        except Exception as e:
            print(f"Failed to index {skill_path}: {e}")
            return False

    def index_all(self) -> int:
        """Index all skills from skills/ directory"""
        if not SKILLS_ROOT.exists():
            print(f"Skills directory not found: {SKILLS_ROOT}")
            return 0

        count = 0

        for skill_dir in SKILLS_ROOT.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    if self.index_skill(skill_file):
                        count += 1

        print(f"Indexed {count} skills")
        return count

    def get_skill(self, name: str) -> Optional[SkillIndex]:
        """Get skill by name"""
        for skill in self.skills:
            if skill.name == name:
                return skill
        return None

    def list_skills(self) -> List[str]:
        """List all indexed skill names"""
        return [s.name for s in self.skills]


def index_all_skills():
    """CLI: Index all skills"""
    indexer = SkillIndexer()
    count = indexer.index_all()
    print(f"\nIndexed {count} skills to {indexer.vectordb_dir}")


if __name__ == "__main__":
    index_all_skills()
