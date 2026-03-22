# Session Log: USB 500GB Extraction
**Date:** 2026-03-22  
**Session ID:** ses_20260322_usb500-extraction  
**Goal:** Extract content from 500GB USB HDD (same process as 1TB HDD)

---

## Actions Taken

### 1. Drive Detection
- Found `/dev/sdc` (~932GB) - new USB drive
- Mounted at `/media/sir-v/usb500` via NTFS-3g

### 2. Content Discovery
- User: **Lenovoi3** (same as 1TB HDD)
- Main content in `/Users/Lenovoi3/`
  - Desktop: 5.8GB (games/software)
  - Documents: 2.7GB
  - Downloads: 65MB

### 3. PDF Extraction
- Found **191 PDFs** in `Documents/New folder/PDF/` (1.5GB)
- Topics: Spiritual/astral projection, lucid dreaming, self-help
- Currently extracting via rsync (background)

### 4. Text Files
- `HOUSING INFORMATION .txt` → extracted
- `NOTES .txt` → extracted

### 5. MIRA/AI Search
- Keywords: mira, ai, neural, llm, openai, ollama
- Result: **NONE FOUND**

---

## Output Location
```
/home/sir-v/BackUP/usb500_documents/
├── PDFs/                    # 191 PDFs (1.5GB) - extraction in progress
├── text_files/              # 2 text files
├── notes/                   # Desktop notes
└── extraction_report.md     # Full report
```

---

## Status: In Progress
- [x] Drive mounted
- [x] Content discovered
- [x] PDFs identified (191)
- [x] Extraction started (rsync background)
- [ ] Extraction complete
