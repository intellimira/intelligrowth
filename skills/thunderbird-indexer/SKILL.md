# Thunderbird Email Indexer Skill

> **Version:** 1.0.0  
> **Author:** MIRA Sentinel  
> **Purpose:** Index, search, and analyze Thunderbird local email cache

---

## Overview

This skill provides CLI tools to index and query emails from Thunderbird's local IMAP cache. It parses Mbox files, extracts metadata and body content, and stores them in a searchable SQLite database with FTS5 full-text search.

## Thunderbird Profile Location

```
/home/sir-v/snap/thunderbird/common/.thunderbird/s72xlcuu.default/
```

### Accounts

| Account | Email | Path |
|---------|-------|------|
| Primary | `intellimira@gmail.com` | `ImapMail/imap.gmail.com/` |
| Secondary | `randolphdube@gmail.com` | `ImapMail/imap.gmail-1.com/` |

---

## Usage

```bash
# Index all emails (run once to build cache)
thunderbird-indexer index

# Search emails by keyword
thunderbird-indexer search "shadow ops"

# Search by sender
thunderbird-indexer from "client@example.com"

# Search by subject
thunderbird-indexer subject "invoice"

# Get folder statistics
thunderbird-indexer stats

# List all folders
thunderbird-indexer folders

# Extract attachments from specific sender
thunderbird-indexer attachments --sender "vendor@company.com"

# Get email count per folder
thunderbird-indexer folder-stats

# Search within date range
thunderbird-indexer date-range 2025-01-01 2025-03-15

# Show recent emails
thunderbird-indexer recent --limit 20

# Full-text search with highlighting
thunderbird-indexer fts "urgent deadline"

# Thread analysis
thunderbird-indexer threads --subject "project update"
```

---

## Database Schema

```sql
-- Main emails table
CREATE TABLE emails (
    id INTEGER PRIMARY KEY,
    message_id TEXT UNIQUE,
    account TEXT,
    folder TEXT,
    subject TEXT,
    sender TEXT,
    sender_email TEXT,
    recipients TEXT,
    date TEXT,
    timestamp INTEGER,
    has_attachments INTEGER,
    snippet TEXT,
    body_text TEXT
);

-- FTS5 virtual table for full-text search
CREATE VIRTUAL TABLE emails_fts USING fts5(
    subject, sender_email, body_text,
    content='emails',
    content_rowid='id'
);

-- Attachments table
CREATE TABLE attachments (
    id INTEGER PRIMARY KEY,
    email_id INTEGER,
    filename TEXT,
    content_type TEXT,
    size INTEGER,
    FOREIGN KEY(email_id) REFERENCES emails(id)
);

-- Indexes
CREATE INDEX idx_sender ON emails(sender_email);
CREATE INDEX idx_date ON emails(date);
CREATE INDEX idx_folder ON emails(folder);
CREATE INDEX idx_account ON emails(account);
```

---

## Implementation

- **Script:** `thunderbird-indexer.py` in skill directory
- **Database:** `~/.local/share/thunderbird-indexer/emails.db`
- **Dependencies:** Python 3, standard library (`mailbox`, `sqlite3`, `email`)

---

## Integration Points

| MIRA Component | Integration |
|----------------|-------------|
| `active_recall` | Can query this skill for email context |
| `revenue-tracker` | Extract invoices/attachments for deal tracking |
| `shadow-ops-prover` | Track SHADOW-OPS pipeline emails |
| `knowledge-base` | Index important email threads as Zettels |

---

## Workflow

1. **Initial Index:** Run `thunderbird-indexer index` to build full cache
2. **Incremental Update:** Re-run to pick up new emails (idempotent)
3. **Query:** Use search commands to find specific emails
4. **Extract:** Pull attachments or export specific threads

---

## Example Queries

```bash
# Find all invoices from specific sender
thunderbird-indexer search "invoice" --sender "billing@company.com"

# Get all SHADOW-OPS emails from past month
thunderbird-indexer folder "SHADOW-OPS" --limit 100

# Extract all PDFs from primary account
thunderbird-indexer attachments --account "intellimira@gmail.com" --type pdf

# Search both accounts for keyword
thunderbird-indexer search "contract" --account "all"
```

---

## Notes

- Thunderbird must NOT be running during indexing (lock file check)
- First index takes 5-10 minutes for ~1000 emails
- Incremental updates are fast (< 1 minute)
- Attachments are NOT downloaded, only metadata extracted from cache
