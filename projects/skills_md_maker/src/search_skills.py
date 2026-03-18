import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import pickle


PROJECT_ROOT = Path(__file__).parent.parent
VECTORDB_DIR = PROJECT_ROOT / "vectordb"
SKILLS_ROOT = Path("/home/sir-v/MiRA/skills")


@dataclass
class SearchResult:
    name: str
    description: str
    triggers: List[str]
    tools: List[str]
    persona: str
    score: float
    file_path: str


class SkillSearch:
    def __init__(self):
        self.vectordb_dir = VECTORDB_DIR
        self.index_file = self.vectordb_dir / "skills_index.pkl"

        self.skills = []
        self.embeddings = None

        self._load_index()

    def _load_index(self):
        """Load index from disk"""
        if not self.index_file.exists():
            print("No index found. Run index_skills.py first.")
            return

        try:
            with open(self.index_file, "rb") as f:
                data = pickle.load(f)
                self.skills = data.get("skills", [])
                self.embeddings = data.get("embeddings")
        except Exception as e:
            print(f"Failed to load index: {e}")

    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text"""
        try:
            from masfactory.utils.embedding import TfidfEmbedder

            all_texts = [self._extract_text(s) for s in self.skills]
            if not all_texts:
                return self._simple_hash_embedding(text)

            embedder = TfidfEmbedder(documents=all_texts, max_features=512)
            func = embedder.get_embedding_function()
            return func(text)
        except Exception as e:
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

    def _extract_text(self, skill) -> str:
        """Extract searchable text from skill"""
        parts = [
            skill.name if hasattr(skill, "name") else "",
            skill.description if hasattr(skill, "description") else "",
            " ".join(skill.triggers) if hasattr(skill, "triggers") else "",
            " ".join(skill.tools) if hasattr(skill, "tools") else "",
            skill.persona if hasattr(skill, "persona") else "",
        ]
        return " ".join(parts)

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity"""
        dot = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(dot / (norm_a * norm_b))

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search skills by query"""
        if not self.skills or self.embeddings is None:
            return []

        query_embedding = self._get_embedding(query)

        scores = []
        for i, skill in enumerate(self.skills):
            score = self._cosine_similarity(query_embedding, self.embeddings[i])
            scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for i, score in scores[:top_k]:
            skill = self.skills[i]
            results.append(
                SearchResult(
                    name=skill.name,
                    description=skill.description,
                    triggers=skill.triggers,
                    tools=skill.tools,
                    persona=skill.persona,
                    score=score,
                    file_path=skill.file_path,
                )
            )

        return results


def search_skills(query: str, top_k: int = 5) -> List[SearchResult]:
    """CLI search function"""
    search = SkillSearch()
    return search.search(query, top_k)


def print_results(results: List[SearchResult]):
    """Print search results"""
    if not results:
        print("No results found.")
        return

    print("=" * 70)
    print("SKILL RECOMMENDATIONS")
    print("=" * 70)
    print()

    for i, result in enumerate(results, 1):
        print(f"{i}. {result.name}")
        print(f"   {result.description}")
        print(f"   Triggers: {', '.join(result.triggers[:5])}")
        print(f"   Tools: {', '.join(result.tools[:3])}")
        print(f"   Score: {result.score:.3f}")
        print(f"   Path: {result.file_path}")
        print()


if __name__ == "__main__":
    import sys

    query = sys.argv[1] if len(sys.argv) > 1 else "validate SaaS idea"
    results = search_skills(query)
    print_results(results)
