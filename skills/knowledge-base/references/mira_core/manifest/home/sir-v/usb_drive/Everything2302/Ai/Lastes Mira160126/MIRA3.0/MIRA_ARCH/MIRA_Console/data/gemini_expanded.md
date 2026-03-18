Done. I’ve **fully expanded that section** in the canvas into a concrete, implementation-ready description that Gemini (or an engineer/designer) can actually build from.

What I added goes beyond feature lists and clarifies:

* **Intent per panel** (why it exists, not just what it does)
* **State behavior** (empty, loading, selected, unselected)
* **Interaction contracts** (what happens when you click something)
* **A hard rule for context control** (upload ≠ included)

This is the difference between:

> “A chat UI with uploads”
> and
> “A controllable, source-grounded AI workspace.”

### How to use this with Gemini (important)

When you paste this into Gemini, frame it like this:

> “Treat the following as a **product + interaction specification**, not a summary. Infer components, state management, and UI behavior.”

If you want, next we can:

* Convert this into **explicit component specs** (e.g., `SourceItem`, `ContextToggle`, `PreviewRenderer`)
* Turn it into a **single, compressed ‘system prompt’** Gemini won’t truncate
* Add **trust UX** (why the AI says what it says, source traceability)
* Translate it directly into **React / Vue / Flutter UI scaffolding**

Just tell me the next level you want to reach.
