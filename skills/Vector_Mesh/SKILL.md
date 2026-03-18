---
name: Vector_Mesh
description: Local-first vector embeddings storage and search. Uses Ollama for embeddings, SQLite for vector storage. Enables semantic search across MIRA knowledge.
triggers: [vector search, semantic search, embeddings, similarity, find similar]
tools: [bash, read_file, write_file, glob]
quality_gates: [embeddings_generated, search_works, storage_valid]
persona: "⚛️ First Principles — foundational data structures"
mira_tier: 2
---

# Vector_Mesh

Local-first vector embeddings for MIRA's knowledge ecosystem.

## Status

**EARMARKED FOR IMPLEMENTATION**

## Architecture

```
Vector_Mesh/
├── embeddings/          # Ollama-generated embeddings
├── vectors.db          # SQLite vector storage
├── index.py            # Indexing script
└── search.py           # Similarity search
```

## Implementation Approach

### Local-First (Primary)
- **Embeddings:** Use Ollama's embedding models (e.g., nomic-embed-text)
- **Storage:** SQLite with custom vector columns or JSON
- **Search:** Cosine similarity via Python

### Stub Implementation (Phase 1)
- Simple file-based index
- JSON storage for embeddings metadata
- Manual re-index trigger

### Full Implementation (Phase 2)
- Ollama integration for embeddings
- Vector similarity search
- Auto-index on session completion

## Usage

```bash
# Index a folder
python index.py /path/to/knowledge

# Search
python search.py "query about shadow ops"

# Find similar
python search.py --similar-to session_20260315
```

## Integration

| Component | Integration Point |
|-----------|------------------|
| skills_md_maker | Auto-index new skills |
| active_recall | Vector search fallback |
| Memory_Mesh | Index zettels |
| sessions | Index session logs |

## Dependencies

- Ollama (for embeddings)
- Python + numpy (for similarity)
- SQLite (for storage)

## Future: Cloud Bridge

Stub for future cloud embeddings:
```python
# cloud_bridge.py (future)
def embed_cloud(text):
    # OpenAI/Anthropic API call
    pass
```
