import os
import json
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static, Label
from textual.containers import Container, Vertical, Horizontal

class SSOCRMDashboard(App):
    """A detailed CRM TUI for monitoring Sovereign Shadow Operations."""
    
    CSS = """
    Screen { background: #050505; }
    #header-info {
        height: 3;
        background: #111;
        color: #00ff41;
        content-align: center middle;
        text-style: bold;
        border-bottom: solid #00ff41;
    }
    DataTable {
        height: 1fr;
        border: solid #333;
        margin: 1;
    }
    .metric-panel {
        width: 30;
        background: #111;
        padding: 1;
        border-left: solid #00ff41;
    }
    .status-active { color: #00ff41; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("SOVEREIGN SHADOW OPERATOR: CRM & COMMAND CONTROL", id="header-info")
        with Horizontal():
            yield DataTable()
            with Vertical(classes="metric-panel"):
                yield Label("GLOBAL EFFECTIVENESS", classes="status-active")
                yield Static("\n[*] Total Ops: 5")
                yield Static("[*] Avg Engagement: 24.5%")
                yield Static("[*] Conversion Pipeline: $12,400")
                yield Static("\n[*] Nodal Status: ACTIVE")
                yield Static("[*] Sensory Sync: ONLINE")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("TARGET", "STATUS", "OUTREACH", "ENGAGEMENT", "PROBABILITY")
        
        # Load active ops from file system
        ops_dir = "/home/sir-v/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/active_ops"
        if os.path.exists(ops_dir):
            for filename in os.listdir(ops_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(ops_dir, filename), 'r') as f:
                        data = json.load(f)
                        table.add_row(
                            data.get("target", "N/A"),
                            data.get("status", "N/A"),
                            data.get("outreach_method", "N/A"),
                            f"{data.get('engagement_rate', 0)*100:.1f}%",
                            f"{data.get('conversion_probability', 0)*100:.0f}%"
                        )

if __name__ == "__main__":
    app = SSOCRMDashboard()
    app.run()
