# MIRA Interactive UI Patterns
## Solo Leveling x OpenCode `question` Tool

---

## The Core Pattern

Use the `question` tool with these field combinations:

```python
question(
    questions=[{
        "question": "HEADER TEXT - sets context",
        "header": "SECTION LABEL", 
        "options": [
            {"label": "EMOJI + SHORT LABEL", "description": "What happens"},
            ...
        ]
    }]
)
```

---

## Theme Variations

### 1. Minimal (Clean Focus)
```
question: "What do you want to do?"
options: [
  {"label": "→ Continue", "description": "Move forward"},
  {"label": "→ Cancel", "description": "Abort mission"}
]
```

### 2. MIRA Solo Leveling (Dark + Power)
```
question: "🌑 THE SHADOW AWAKENS"
options: [
  {"label": "◆ COPY ──── Direct path", "description": "Paste content now"},
  {"label": "◆ VESSEL ──── External source", "description": "Upload PDF file"},
  {"label": "◆ SEER ──── Describe vision", "description": "Tell me what you see"},
  {"label": "◆ SHADOW ──── Retreat", "description": "Handle later"}
]
```

### 3. Flow State (Action-Oriented)
```
question: "⚡ QUICK ACTION NEEDED"
options: [
  {"label": "1️⃣ PASTE ──── Add content", "description": "Copy & paste directly"},
  {"label": "2️⃣ UPLOAD ──── Attach file", "description": "Export as PDF"},
  {"label": "3️⃣ SKIP ──── Continue", "description": "Handle later"}
]
```

### 4. Card Grid (Visual Spacing)
```
question: "SELECT METHOD"
options: [
  {"label": "[ 1 ] PASTE", "description": "Copy content"},
  {"label": "[ 2 ] UPLOAD", "description": "Export PDF"},
  {"label": "[ 3 ] RESEARCH", "description": "Describe topics"},
  {"label": "[ 4 ] SKIP", "description": "Defer"}
]
```

---

## Implementation Examples

### Example 1: Taylor Content Transfer
```python
question(
    questions=[{
        "question": "🌊 TAYLOR CORPUS: Content Transfer",
        "header": "Method",
        "options": [
            {"label": "📋 Paste", "description": "Copy content → paste here"},
            {"label": "📄 Upload", "description": "Export PDF → upload"},
            {"label": "💬 Describe", "description": "Tell me topics → I research"},
            {"label": "⏭️ Skip", "description": "Handle later"}
        ]
    }]
)
```

### Example 2: Workflow Decision
```python
question(
    questions=[{
        "question": "⚙️ WORKFLOW MODE",
        "header": "Choose Path",
        "options": [
            {"label": "🚀 AUTO ──── Full automation", "description": "I handle everything"},
            {"label": "🎯 HITL ──── Human in loop", "description": "Confirm each step"},
            {"label": "👁️ WATCH ──── Observe only", "description": "Show me what you'd do"}
        ]
    }]
)
```

### Example 3: Dark Passenger (Mystical)
```python
question(
    questions=[{
        "question": "🌑 THE SHADOW SPEAKS",
        "header": "Choose",
        "options": [
            {"label": "◆ 1 ◆ ──── COPY", "description": "The direct path"},
            {"label": "◆ 2 ◆ ──── VESSEL", "description": "The external vessel"},
            {"label": "◆ 3 ◆ ──── SEER", "description": "Through the vision"},
            {"label": "◆ 4 ◆ ──── SHADOW", "description": "Retreat to darkness"}
        ]
    }]
)
```

---

## Emoji Set Reference

| Theme | Emojis |
|-------|--------|
| Minimal | →, ✓, ✗, • |
| Action | ⚡, 🚀, 🎯, ⏭️ |
| MIRA/Solo | ◆, 🌑, 🌊, 🔮 |
| Content | 📋, 📄, 💬, 🖼️ |
| Status | ✅, ❌, ⚠️, 🔄 |

---

## Status

- [x] Pattern documented
- [x] Theme variations created  
- [x] Implementation examples written
- [ ] OpenCode UI team feedback (what renders best?)

---

*Solo Leveling: E → D → C → B → A → S*
