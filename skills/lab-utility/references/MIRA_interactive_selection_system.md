# MIRA Interactive Selection System
## Based on charmbracelet/huh design patterns

## Concept

A beautiful, themable interactive selection system for MIRA that adapts to the Solo Leveling framework aesthetic. Uses ASCII-rendered selectable options that feel like clicking buttons.

## Design Patterns

### 1. Card Grid Selection
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│              │ │              │ │              │
│   [ 1 ]      │ │   [ 2 ]      │ │   [ 3 ]      │
│              │ │              │ │              │
│   PASTE      │ │   UPLOAD     │ │   DESCRIBE   │
│              │ │              │ │              │
│   Copy &     │ │   Export     │ │   Tell me    │
│   paste      │ │   PDF        │ │   topics     │
│              │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
```

### 2. Vertical List (huh-style)
```
▸ Paste Content    ──── Copy directly here
▸ Upload PDF       ──── Export & upload
▸ Describe Topics   ──── Tell me more
▸ Skip             ──── Handle later
```

### 3. Dark Passenger Theme
```
╔═══════════════════════════════════════════════╗
║  🌑 THE SHADOW SPEAKS                       ║
║  "Choose wisely, initiate..."                ║
║                                               ║
║    ◆ 1 ◆   COPY    ──── Paste content       ║
║    ◆ 2 ◆   VESSEL  ──── Upload PDF          ║
║    ◆ 3 ◆   SEER    ──── Describe it          ║
║    ◆ 4 ◆   SHADOW  ──── Retreat             ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

### 4. Minimal (Clean)
```
> Paste
> Upload  
> Describe
> Skip
```

## Implementation Approach

Since OpenCode has a native `question` tool, we can style it to match these patterns using:
- Emoji as visual anchors
- ASCII box drawing characters
- Consistent spacing/alignment
- Themed headers

## Future: Custom TUI (Go + huh)

For fully custom UI, we could create a Go binary using `charmbracelet/huh` that:
1. Runs as a subprocess
2. Captures user selection via arrow keys
3. Returns result to OpenCode
4. Theme matches MIRA aesthetic (Dark Passenger)

Example Go code:
```go
package main

import (
    "charm.land/huh/v2"
)

func main() {
    var choice string
    huh.NewSelect[string]().
        Title("🌊 MIRA: Select your path").
        Options(
            huh.NewOption("Paste Content", "paste"),
            huh.NewOption("Upload PDF", "upload"),
            huh.NewOption("Describe Topics", "describe"),
            huh.NewOption("Skip", "skip"),
        ).
        Value(&choice).
        Run()
    // Return choice to stdout for OpenCode to capture
}
```

## Status

- [x] Design patterns documented
- [ ] OpenCode question tool integration
- [ ] MIRA-themed aesthetic applied
- [ ] Multi-select support added
- [ ] Theme switching (Light/Dark/Solo-Leveling)

## References

- https://github.com/charmbracelet/huh
- https://github.com/charmbracelet/bubbletea
- https://github.com/charmbracelet/lipgloss
