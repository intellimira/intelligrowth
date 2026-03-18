from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem
from textual.containers import Container, Horizontal, Vertical
from datetime import datetime
import os

class ACCTDashboard(App):
    """The high-speed ACCT Sovereign Cockpit v0.1."""
    
    CSS = """
    Screen {
        background: #0a0a0a;
    }
    #sidebar {
        width: 30;
        background: #1a1a1a;
        border-right: solid #00ff41;
        padding: 1;
    }
    #main-content {
        padding: 1;
    }
    .node-active {
        color: #00ff41;
        text-style: bold;
    }
    .section-title {
        background: #00ff41;
        color: black;
        width: 100%;
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    #sensory-feed {
        height: 1fr;
        border: double #00ff41;
        background: #001100;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("NODAL MESH STATUS", classes="section-title")
                yield Label("⚛️ Analytic: [ONLINE]", classes="node-active")
                yield Label("🔬 Empirical: [ONLINE]", classes="node-active")
                yield Label("✨ Creative: [ONLINE]", classes="node-active")
                yield Label("⚙️ Pragmatic: [ONLINE]", classes="node-active")
                yield Label("👁️ Sensory: [ACTIVE]", classes="node-active")
                yield Label("🌑 Risk: [WATCHING]", classes="node-active")
                
                yield Label("\nSYSTEM STATS", classes="section-title")
                yield Label("Intelligence: v1.5 Sovereign")
                yield Label("Memory Mesh: 346 Zettels")
                yield Label("Synapses: 40+ Detected")
                
            with Vertical(id="main-content"):
                yield Label("ACTIVE ORCHESTRATOR: QUEST LOG", classes="section-title")
                yield Static("[*] CURRENT QUEST: The Sovereign Cockpit (TUI Build-out)")
                yield Static("[*] STATUS: Phase 1 Prototype Implementation")
                
                yield Label("\n👁️ REAL-TIME SENSORY FEED", classes="section-title")
                with Vertical(id="sensory-feed"):
                    yield Static("> [18:30:27] MOTION_DETECTED at Front Door (Risk Trigger)")
                    yield Static("> [18:30:27] OCR_TEXT_RECOGNIZED: 'Project Alpha' (Analytic Trigger)")
                    yield Static("> [19:45:12] SESSION_CONSOLIDATION: v1.5 Evolution Sealed")
                    yield Static("> [20:05:00] NOTEBOOKLM_SYNC: 7 Experiments Initialized")
                    yield Static("> [20:10:00] DASHBOARD_INITIALIZATION: Textual v0.1 Online")

        yield Footer()

if __name__ == "__main__":
    app = ACCTDashboard()
    app.run()
