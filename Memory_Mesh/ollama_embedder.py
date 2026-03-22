#!/usr/bin/env python3
"""
MIRA Embedding Generator
Generates real semantic embeddings using Ollama

Uses nomic-embed-text for high-quality embeddings
Cached for performance
"""

import os
import json
import time
import hashlib
import sqlite3
import requests
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class OllamaEmbedder:
    """
    Semantic embeddings via Ollama API.

    Uses nomic-embed-text for fast, high-quality embeddings.
    Includes caching to avoid re-computation.
    """

    def __init__(
        self,
        model: str = "nomic-embed-text",
        base_url: str = "http://localhost:11434",
        cache_dir: str = "~/.mira/embeddings",
    ):
        self.model = model
        self.base_url = base_url
        self.cache_dir = Path(os.path.expanduser(cache_dir))
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize cache DB
        self.cache_db = self.cache_dir / "embeddings.db"
        self._init_cache()

        # Embedding dimension (nomic-embed-text = 768)
        self.embedding_dim = 768

    def _init_cache(self):
        """Initialize cache database."""
        conn = sqlite3.connect(str(self.cache_db))
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_hash TEXT UNIQUE,
                text_preview TEXT,
                embedding BLOB,
                model TEXT,
                created_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    def _hash_text(self, text: str) -> str:
        """Generate hash for text."""
        return hashlib.sha256(text.encode()).hexdigest()

    def _get_cached(self, text: str) -> Optional[List[float]]:
        """Get embedding from cache."""
        text_hash = self._hash_text(text)

        conn = sqlite3.connect(str(self.cache_db))
        cursor = conn.cursor()

        cursor.execute(
            "SELECT embedding FROM embeddings WHERE text_hash = ? AND model = ?",
            (text_hash, self.model),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            import numpy as np

            return np.frombuffer(result[0], dtype=np.float32).tolist()

        return None

    def _cache_embedding(self, text: str, embedding: List[float]):
        """Cache embedding."""
        text_hash = self._hash_text(text)
        text_preview = text[:100]

        import numpy as np

        emb_array = np.array(embedding, dtype=np.float32)

        conn = sqlite3.connect(str(self.cache_db))
        cursor = conn.cursor()

        cursor.execute(
            """INSERT OR REPLACE INTO embeddings 
               (text_hash, text_preview, embedding, model, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (
                text_hash,
                text_preview,
                emb_array.tobytes(),
                self.model,
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def embed(
        self, text: str, use_cache: bool = True, max_length: int = 8000
    ) -> List[float]:
        """
        Generate embedding for text.

        Args:
            text: Input text
            use_cache: Use cached embeddings if available
            max_length: Maximum text length (Ollama limit)

        Returns:
            Embedding vector (768 dimensions)
        """
        # Check cache
        if use_cache:
            cached = self._get_cached(text)
            if cached:
                return cached

        # Truncate long texts
        truncated = text[:max_length] if len(text) > max_length else text

        # Generate embedding
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": truncated},
                timeout=30,
            )

            if response.status_code == 200:
                embedding = response.json()["embedding"]

                # Cache result
                self._cache_embedding(text, embedding)

                return embedding
            else:
                print(f"⚠️ Ollama error: {response.status_code}")
                return self._fallback_embedding()

        except Exception as e:
            print(f"⚠️ Embedding failed: {e}")
            return self._fallback_embedding()

    def _fallback_embedding(self) -> List[float]:
        """Return zero vector as fallback."""
        import numpy as np

        return np.zeros(self.embedding_dim).tolist()

    def embed_batch(
        self, texts: List[str], use_cache: bool = True, show_progress: bool = True
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts
            use_cache: Use cached embeddings
            show_progress: Show progress bar

        Returns:
            List of embedding vectors
        """
        embeddings = []
        total = len(texts)

        for i, text in enumerate(texts):
            emb = self.embed(text, use_cache=use_cache)
            embeddings.append(emb)

            if show_progress and (i + 1) % 100 == 0:
                print(f"   Embedded {i + 1}/{total} texts...")

        return embeddings

    def embed_with_metadata(
        self, texts: List[str], metadata: List[Dict] = None
    ) -> List[Dict]:
        """
        Generate embeddings with metadata.

        Args:
            texts: List of texts
            metadata: Optional metadata for each text

        Returns:
            List of {text, embedding, metadata} dicts
        """
        embeddings = self.embed_batch(texts)

        results = []
        for i, emb in enumerate(embeddings):
            result = {
                "text": texts[i],
                "embedding": emb,
                "text_hash": self._hash_text(texts[i]),
            }

            if metadata and i < len(metadata):
                result["metadata"] = metadata[i]

            results.append(result)

        return results

    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        conn = sqlite3.connect(str(self.cache_db))
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM embeddings")
        count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT created_at FROM embeddings ORDER BY created_at DESC LIMIT 1"
        )
        last_used = cursor.fetchone()

        conn.close()

        cache_size = self.cache_db.stat().st_size if self.cache_db.exists() else 0

        return {
            "cached_embeddings": count,
            "cache_size_mb": cache_size / 1e6,
            "last_used": last_used[0] if last_used else None,
            "model": self.model,
            "embedding_dim": self.embedding_dim,
        }

    def clear_cache(self):
        """Clear embedding cache."""
        conn = sqlite3.connect(str(self.cache_db))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM embeddings")
        conn.commit()
        conn.close()
        print("✅ Cache cleared")


class EmbeddingDatasetBuilder:
    """
    Builds embedding datasets for training.

    Processes MIRA_ARCH data and generates embeddings.
    """

    def __init__(self, embedder: OllamaEmbedder = None):
        self.embedder = embedder or OllamaEmbedder()

    def build_from_jsonl(
        self, input_file: Path, text_field: str = "content", output_file: Path = None
    ) -> Path:
        """
        Build embedding dataset from JSONL file.

        Args:
            input_file: Input JSONL file
            text_field: Field containing text to embed
            output_file: Output file path

        Returns:
            Path to output file
        """
        if output_file is None:
            output_file = input_file.parent / f"{input_file.stem}_with_embeddings.jsonl"

        print(f"\n📝 Building embedding dataset...")
        print(f"   Input: {input_file}")
        print(f"   Output: {output_file}")

        # Read input
        with open(input_file) as f:
            lines = f.readlines()

        texts = []
        metadata = []

        for line in lines:
            doc = json.loads(line)
            text = doc.get(text_field, "")
            if text:
                texts.append(text)
                metadata.append(doc)

        print(f"   Processing {len(texts)} texts...")

        # Generate embeddings
        results = self.embedder.embed_with_metadata(texts, metadata)

        # Save
        with open(output_file, "w") as f:
            for result in results:
                f.write(json.dumps(result) + "\n")

        print(f"   ✅ Saved {len(results)} embeddings to {output_file}")

        return output_file

    def build_training_dataset(
        self, source_dir: Path = Path("~/MIRA_ARCH_extracted"), output_dir: Path = None
    ) -> Dict[str, Path]:
        """
        Build embedding datasets for all training data.

        Args:
            source_dir: MIRA_ARCH extracted data
            output_dir: Output directory

        Returns:
            Dict of dataset name -> path
        """
        source_dir = Path(os.path.expanduser(source_dir))
        output_dir = output_dir or Path("~/.mira/training_data")
        output_dir.mkdir(parents=True, exist_ok=True)

        datasets = {}

        # Process each dataset
        for jsonl_file in source_dir.glob("*.jsonl"):
            if "embeddings" not in jsonl_file.name:
                print(f"\n{'=' * 60}")

                output = self.build_from_jsonl(
                    jsonl_file,
                    text_field="content",
                    output_file=output_dir / f"{jsonl_file.stem}_embedded.jsonl",
                )

                datasets[jsonl_file.stem] = output

        return datasets


def main():
    """CLI for embedding generation."""
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Embedding Generator")
    parser.add_argument("--text", help="Single text to embed")
    parser.add_argument("--file", type=Path, help="Process JSONL file")
    parser.add_argument("--batch", type=Path, help="Batch process all MIRA_ARCH files")
    parser.add_argument("--stats", action="store_true", help="Show cache stats")
    parser.add_argument("--clear", action="store_true", help="Clear cache")

    args = parser.parse_args()

    embedder = OllamaEmbedder()

    if args.stats:
        stats = embedder.get_cache_stats()
        print("\n📊 Embedding Cache Stats:")
        print(f"   Cached: {stats['cached_embeddings']} embeddings")
        print(f"   Size: {stats['cache_size_mb']:.2f} MB")
        print(f"   Model: {stats['model']}")
        print(f"   Dim: {stats['embedding_dim']}")

    elif args.clear:
        embedder.clear_cache()

    elif args.text:
        print(f"\n📝 Embedding: {args.text[:50]}...")
        embedding = embedder.embed(args.text)
        print(f"   ✅ Generated {len(embedding)}-dim embedding")
        print(f"   Preview: {embedding[:5]}...")

    elif args.file:
        builder = EmbeddingDatasetBuilder(embedder)
        builder.build_from_jsonl(args.file)

    elif args.batch:
        builder = EmbeddingDatasetBuilder(embedder)
        datasets = builder.build_training_dataset(source_dir=args.batch)
        print("\n✅ All datasets processed:")
        for name, path in datasets.items():
            print(f"   {name}: {path}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
