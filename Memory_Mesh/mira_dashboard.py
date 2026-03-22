#!/usr/bin/env python3
"""
MIRA Interactive TUI Dashboard
Unified interface for system monitoring and control.
"""

import asyncio
from datetime import datetime
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header,
    Footer,
    Static,
    Button,
    Input,
    DataTable,
    Log,
    ProgressBar,
    Tabs,
    Tab,
)
from textual.binding import Binding
from textual import events
import subprocess
import json
import os

# Import MIRA modules
from mira_report import (
    get_system_health,
    get_config_status,
    get_leads_summary,
    get_gmail_status,
    generate_telegram_report,
    generate_email_report,
    send_telegram_report,
    send_email_report,
)


class MIRAWidget(Static):
    """Base widget class"""

    pass


class SystemHealthWidget(Vertical):
    """System health metrics display"""

    def compose(self) -> ComposeResult:
        yield Static("⚙️ SYSTEM HEALTH", id="health-title")
        yield ProgressBar(id="ram-bar")
        yield Static("", id="ram-text")
        yield ProgressBar(id="disk-bar")
        yield Static("", id="disk-text")
        yield Static("", id="swap-text")
        yield Static("", id="ollama-text")
        yield Button("🔄 Refresh", id="refresh-health", variant="primary")

    def on_mount(self):
        self.refresh_data()

    def refresh_data(self):
        health = get_system_health()

        # RAM
        ram_pct = health["ram"]["percent"]
        self.query_one("#ram-bar", ProgressBar).update(progress=ram_pct)
        self.query_one("#ram-text", Static).update(
            f"RAM: {health['ram']['used_gb']}GB / {health['ram']['total_gb']}GB ({ram_pct}%) {health['ram']['status']}"
        )

        # Disk
        disk_pct = health["disk"]["percent"]
        self.query_one("#disk-bar", ProgressBar).update(progress=disk_pct)
        self.query_one("#disk-text", Static).update(
            f"Disk: {health['disk']['used_gb']}GB / {health['disk']['total_gb']}GB ({disk_pct}%) {health['disk']['status']}"
        )

        # Swap
        swap_info = health.get("swap", {})
        self.query_one("#swap-text", Static).update(
            f"Swap: {swap_info.get('used_gb', 0)}GB / {swap_info.get('total_gb', 0)}GB {swap_info.get('status', '⚠️')}"
        )

        # Ollama
        ollama_info = health.get("ollama", {})
        self.query_one("#ollama-text", Static).update(
            f"Ollama: {ollama_info.get('status', 'Unknown')}"
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "refresh-health":
            self.refresh_data()


class ConfigStatusWidget(Vertical):
    """Configuration status display"""

    def compose(self) -> ComposeResult:
        yield Static("🔧 CONFIGURATION STATUS", id="config-title")
        yield Static("", id="telegram-status")
        yield Static("", id="gmail-status")
        yield Static("", id="repo-status")
        yield Button("🔄 Refresh", id="refresh-config", variant="primary")

    def on_mount(self):
        self.refresh_data()

    def refresh_data(self):
        config = get_config_status()

        self.query_one("#telegram-status", Static).update(
            f"Telegram: {config['telegram']['token']} | {config['telegram']['chat_id']}"
        )
        self.query_one("#gmail-status", Static).update(
            f"Gmail: {config['gmail']['connection']}"
        )
        self.query_one("#repo-status", Static).update(
            f"Enquiries: {config['enquiries_repo']['exists']}"
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "refresh-config":
            self.refresh_data()


class LeadsWidget(Vertical):
    """Leads summary display"""

    def compose(self) -> ComposeResult:
        yield Static("📊 LEADS SUMMARY", id="leads-title")
        yield Static("", id="total-leads")
        yield Static("", id="qualified-leads")
        yield Static("", id="critical-leads")
        yield Static("", id="pending-leads")
        yield Static("", id="new-today")
        yield Button("🔄 Refresh", id="refresh-leads", variant="primary")

    def on_mount(self):
        self.refresh_data()

    def refresh_data(self):
        leads = get_leads_summary()

        self.query_one("#total-leads", Static).update(f"Total Leads: {leads['total']}")
        self.query_one("#qualified-leads", Static).update(
            f"Qualified (7+): {leads['qualified']}"
        )
        self.query_one("#critical-leads", Static).update(
            f"Critical (9+): {leads['critical']}"
        )
        self.query_one("#pending-leads", Static).update(
            f"Pending (5-6): {leads['pending']}"
        )
        self.query_one("#new-today", Static).update(f"New Today: {leads['new_today']}")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "refresh-leads":
            self.refresh_data()


class GmailWidget(Vertical):
    """Gmail status and polling"""

    def compose(self) -> ComposeResult:
        yield Static("📧 GMAIL STATUS", id="gmail-title")
        yield Static("", id="gmail-connection")
        yield Static("", id="gmail-last-poll")
        yield Static("", id="gmail-new")
        yield Button("🔄 Check Now", id="poll-gmail", variant="primary")
        yield Button("📥 Poll & Save", id="poll-save", variant="success")

    def on_mount(self):
        self.refresh_data()

    def refresh_data(self):
        gmail = get_gmail_status()

        self.query_one("#gmail-connection", Static).update(
            f"Connection: {'✅ Connected' if gmail['connected'] else '❌ Not Connected'}"
        )
        self.query_one("#gmail-last-poll", Static).update(
            f"Last Poll: {gmail.get('last_check', 'Never') or 'Never'}"
        )
        self.query_one("#gmail-new", Static).update(
            f"New Today: {gmail['new_enquiries']}"
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id in ["poll-gmail", "poll-save"]:
            self.app.action_poll_gmail()


class ReportsWidget(Vertical):
    """Report generation and sending"""

    def compose(self) -> ComposeResult:
        yield Static("📨 REPORTS", id="reports-title")
        yield Button("📱 Send to Telegram", id="send-telegram", variant="primary")
        yield Button("📧 Send to Email", id="send-email", variant="primary")
        yield Button("🖥️ Console Only", id="send-console", variant="secondary")
        yield Button("📊 Full Report (All)", id="send-all", variant="success")
        yield Static("", id="report-status")

    def on_button_pressed(self, event: Button.Pressed):
        status = self.query_one("#report-status", Static)

        if event.button.id == "send-telegram":
            report = generate_telegram_report()
            if send_telegram_report(report):
                status.update("✅ Report sent to Telegram!")
            else:
                status.update("❌ Failed to send to Telegram")

        elif event.button.id == "send-email":
            report = generate_email_report()
            if send_email_report(report):
                status.update("✅ Report sent to Email!")
            else:
                status.update("❌ Failed to send to Email")

        elif event.button.id == "send-console":
            from mira_report import get_console_report

            print("\n" + "=" * 60)
            print(get_console_report())
            print("=" * 60)
            status.update("✅ Report printed to console")

        elif event.button.id == "send-all":
            report = generate_telegram_report()
            tg_ok = send_telegram_report(report)
            report = generate_email_report()
            em_ok = send_email_report(report)
            status.update(
                f"📱 TG: {'✅' if tg_ok else '❌'} | 📧 EM: {'✅' if em_ok else '❌'}"
            )


class PipelineWidget(Vertical):
    """Quick actions for pipeline"""

    def compose(self) -> ComposeResult:
        yield Static("⚡ QUICK ACTIONS", id="pipeline-title")
        yield Button("📥 Poll Gmail", id="action-poll")
        yield Button("📊 Score Leads", id="action-score")
        yield Button("📱 Check Alerts", id="action-alerts")
        yield Button("🔄 Update Chat ID", id="action-chatid")
        yield Static("", id="action-status")


class MIRADashboard(App):
    """MIRA TUI Dashboard Application"""

    CSS = """
    Screen {
        background: #1a1a2e;
    }
    
    #main-container {
        height: 100%;
        layout: grid;
        grid-size: 2 3;
        grid-columns: 1fr 1fr;
        grid-rows: auto 1fr auto;
        gap: 1;
        padding: 1;
    }
    
    #title-bar {
        column-span: 2;
        height: 3;
        background: #16213e;
        border: solid #0f3460;
        content-align: center middle;
    }
    
    .widget {
        background: #16213e;
        border: solid #0f3460;
        padding: 1;
        height: 100%;
    }
    
    .widget > Static {
        margin-bottom: 1;
    }
    
    #footer-bar {
        column-span: 2;
        height: 3;
        background: #16213e;
        dock: bottom;
    }
    
    Button {
        margin: 1;
    }
    
    ProgressBar {
        margin: 1 0;
    }
    
    #report-status, #action-status {
        color: #0f0;
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("r", "refresh_all", "Refresh All", show=True),
        Binding("t", "send_telegram", "Telegram Report", show=True),
        Binding("e", "send_email", "Email Report", show=True),
        Binding("p", "poll_gmail", "Poll Gmail", show=True),
        Binding("q", "quit", "Quit", show=True),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="main-container"):
            # Title
            yield Static("📊 MIRA UNIFIED DASHBOARD", id="title-bar")

            # Row 1
            yield SystemHealthWidget(classes="widget", id="system-health")
            yield ConfigStatusWidget(classes="widget", id="config-status")

            # Row 2
            yield LeadsWidget(classes="widget", id="leads-summary")
            yield GmailWidget(classes="widget", id="gmail-status")

            # Row 3
            yield ReportsWidget(classes="widget", id="reports-section")
            yield PipelineWidget(classes="widget", id="pipeline-section")

        yield Footer()

    def action_refresh_all(self):
        """Refresh all widgets"""
        self.query_one("#system-health", SystemHealthWidget).refresh_data()
        self.query_one("#config-status", ConfigStatusWidget).refresh_data()
        self.query_one("#leads-summary", LeadsWidget).refresh_data()
        self.query_one("#gmail-status", GmailWidget).refresh_data()

    def action_send_telegram(self):
        """Send report to Telegram"""
        report = generate_telegram_report()
        send_telegram_report(report)

    def action_send_email(self):
        """Send report to Email"""
        report = generate_email_report()
        send_email_report(report)

    def action_poll_gmail(self):
        """Poll Gmail"""
        try:
            from poll_enquiries import poll_for_enquiries, save_enquiries

            enquiries = poll_for_enquiries()
            save_enquiries(enquiries)
            self.query_one("#gmail-status", GmailWidget).refresh_data()
            self.query_one("#leads-summary", LeadsWidget).refresh_data()
        except Exception as e:
            print(f"Error polling Gmail: {e}")


def run_dashboard():
    """Run the MIRA Dashboard"""
    app = MIRADashboard()
    app.run()


if __name__ == "__main__":
    run_dashboard()
