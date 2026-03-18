# Open Notebook Cookbook

## Quick Start

### 1. Check Open Notebook Status

```bash
# Check if running
curl -s http://localhost:5055/health

# If not running, check logs
tail -f /tmp/open_notebook_api.log
```

### 2. Set Up API Key

```bash
export OPEN_NOTEBOOK_API_KEY=$(pass show open-notebook/api-key 2>/dev/null || echo "change-me")
```

### 3. Test Connection

```bash
curl -s http://localhost:5055/api/models \
  -H "Authorization: Bearer $OPEN_NOTEBOOK_API_KEY"
```

---

## Common Workflows

### Workflow 1: Research a Topic

```
1. Create notebook
2. Add sources (URLs, PDFs)
3. Wait for ingestion
4. Search and chat
5. Generate insights/podcast
```

**MIRA Commands:**
```markdown
mira: create notebook "Research: AI Agents"
mira: add these sources to my research notebook:
  - https://arxiv.org/abs/2310.12345
  - /path/to/paper.pdf
mira: search for "autonomous agents capabilities"
mira: ask my notebook what the limitations are
```

### Workflow 2: Summarize Meeting Notes

```
1. Create meeting notebook
2. Upload transcript/audio
3. Generate podcast summary
4. Share podcast
```

**MIRA Commands:**
```markdown
mira: create notebook "Team Standup $(date)"
mira: add the transcript from /path/to/meeting.txt
mira: generate a podcast summary
mira: download the podcast to ~/Downloads/
```

### Workflow 3: Knowledge Base Search

```
1. Pre-ingest documents
2. Search across all
3. Create synthesis
```

**MIRA Commands:**
```markdown
mira: search open notebook for "revenue optimization techniques"
mira: show me the top 5 results with snippets
mira: add these to my strategy notebook
```

---

## API Reference

### Notebooks

#### List Notebooks
```bash
GET /api/notebooks
```

#### Create Notebook
```bash
POST /api/notebooks
{
  "name": "string",
  "description": "string (optional)"
}
```

#### Get Notebook
```bash
GET /api/notebooks/{id}
```

#### Delete Notebook
```bash
DELETE /api/notebooks/{id}
```

---

### Sources

#### List Sources
```bash
GET /api/sources?notebook_id={id}
```

#### Add URL Source
```bash
POST /api/sources
{
  "notebook_id": "uuid",
  "type": "url",
  "url": "https://..."
}
```

#### Upload File
```bash
POST /api/sources/upload
Content-Type: multipart/form-data
- file: (binary)
- notebook_id: uuid
```

---

### Search

#### Semantic Search
```bash
POST /api/search
{
  "query": "string",
  "notebook_id": "uuid (optional)",
  "limit": 10,
  "rerank": true
}
```

Response:
```json
{
  "results": [
    {
      "source_id": "uuid",
      "content": "text chunk...",
      "score": 0.95,
      "metadata": {
        "title": "Document Title",
        "url": "..."
      }
    }
  ]
}
```

---

### Chat

#### Chat with Notebook
```bash
POST /api/chat
{
  "notebook_id": "uuid",
  "message": "What are the key findings?",
  "model": "qwen3:8b",
  "stream": false
}
```

Response:
```json
{
  "response": "The key findings are...",
  "sources": ["uuid1", "uuid2"]
}
```

---

### Podcasts

#### Generate Podcast
```bash
POST /api/podcasts
{
  "notebook_id": "uuid",
  "style": "educational|conversational",
  "language": "en",
  "duration": 300
}
```

#### Get Podcast Status
```bash
GET /api/podcasts/{episode_id}
```

#### Download Podcast
```bash
GET /api/podcasts/{episode_id}/audio
```

---

## Troubleshooting

### "Connection refused" on port 5055

Open Notebook API is not running. Start it:

```bash
cd /media/sir-v/Axion-Ext/MiRA/open_notebook_local
source .venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 5055
```

### "Authentication failed"

Check your API key:

```bash
echo $OPEN_NOTEBOOK_API_KEY
```

### "Embedding failed"

Check Ollama is running:

```bash
curl http://localhost:11434/api/tags
```

---

## Advanced Usage

### Batch Source Ingestion

```python
import requests
import os

API_KEY = os.getenv("OPEN_NOTEBOOK_API_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
NOTEBOOK_ID = "your-notebook-id"

urls = [
    "https://example.com/article1",
    "https://example.com/article2",
    "https://example.com/article3",
]

for url in urls:
    response = requests.post(
        "http://localhost:5055/api/sources",
        headers=HEADERS,
        json={"notebook_id": NOTEBOOK_ID, "type": "url", "url": url}
    )
    print(f"Added: {url} -> {response.status_code}")
```

### Search and Summarize Pipeline

```python
# Search
search_response = requests.post(
    "http://localhost:5055/api/search",
    headers=HEADERS,
    json={"query": "your query", "limit": 5}
)
results = search_response.json()["results"]

# Chat with top results
chat_response = requests.post(
    "http://localhost:5055/api/chat",
    headers=HEADERS,
    json={
        "notebook_id": NOTEBOOK_ID,
        "message": f"Summarize these findings: {[r['content'] for r in results]}"
    }
)
print(chat_response.json()["response"])
```
