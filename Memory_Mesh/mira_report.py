#!/usr/bin/env python3
"""
MIRA Consolidated Report Generator
Generates unified system reports for Telegram and Email.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.parse

# Import MIRA modules
from mira_config import (
    get_telegram_token,
    get_telegram_chat_id,
    get_gmail_password,
    get_enquiries_repo,
)

# Additional email recipients for alerts
ALERT_RECIPIENTS = [
    "intellimira@gmail.com",
    "randolphdube@gmail.com",
]


# ═══════════════════════════════════════════════════════════════
# SYSTEM HEALTH
# ═══════════════════════════════════════════════════════════════


def get_system_health():
    """Get system health metrics"""
    health = {"timestamp": datetime.now().isoformat(), "checks": []}

    # RAM
    try:
        with open("/proc/meminfo") as f:
            mem = f.read()
            lines = mem.split("\n")
            mem_info = {}
            for line in lines:
                if ":" in line:
                    key, val = line.split(":", 1)
                    mem_info[key.strip()] = val.strip()

            total = int(mem_info.get("MemTotal", 0).split()[0]) / 1024 / 1024
            available = int(mem_info.get("MemAvailable", 0).split()[0]) / 1024 / 1024
            used = total - available
            pct = (used / total) * 100

            health["ram"] = {
                "total_gb": round(total, 1),
                "used_gb": round(used, 1),
                "available_gb": round(available, 1),
                "percent": round(pct, 1),
                "status": "✅" if pct < 90 else "⚠️" if pct < 95 else "❌",
            }
            health["checks"].append(("RAM", pct < 90))
    except Exception as e:
        health["ram"] = {"error": str(e)}
        health["checks"].append(("RAM", False))

    # Disk
    try:
        import shutil

        usage = shutil.disk_usage("/")
        total = usage.total / (1024**3)
        used = usage.used / (1024**3)
        pct = (used / total) * 100

        health["disk"] = {
            "total_gb": round(total, 1),
            "used_gb": round(used, 1),
            "percent": round(pct, 1),
            "status": "✅" if pct < 80 else "⚠️" if pct < 90 else "❌",
        }
        health["checks"].append(("Disk", pct < 80))
    except Exception as e:
        health["disk"] = {"error": str(e)}
        health["checks"].append(("Disk", False))

    # Swap
    try:
        with open("/proc/meminfo") as f:
            mem = f.read()
            swap_total_kb = 0
            swap_free_kb = 0
            for line in mem.split("\n"):
                if line.startswith("SwapTotal:"):
                    swap_total_kb = int(line.split(":")[1].strip().split()[0])
                if line.startswith("SwapFree:"):
                    swap_free_kb = int(line.split(":")[1].strip().split()[0])

            # Convert kB to GB
            swap_total = swap_total_kb / 1024 / 1024
            swap_free = swap_free_kb / 1024 / 1024

            if swap_total > 0:
                swap_used = swap_total - swap_free
                swap_pct = (swap_used / swap_total) * 100
                health["swap"] = {
                    "used_gb": round(swap_used, 1),
                    "total_gb": round(swap_total, 1),
                    "percent": round(swap_pct, 1),
                    "status": "⚠️" if swap_pct > 80 else "✅",
                }
                health["checks"].append(("Swap", swap_pct < 80))
    except:
        pass

    # Ollama
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read())
            health["ollama"] = {
                "status": "✅ Running",
                "models": len(data.get("models", [])),
            }
            health["checks"].append(("Ollama", True))
    except:
        health["ollama"] = {"status": "❌ Not Running"}
        health["checks"].append(("Ollama", False))

    # Overall status
    passed = sum(1 for _, ok in health["checks"] if ok)
    total_checks = len(health["checks"])
    health["overall"] = (
        "✅ HEALTHY"
        if passed == total_checks
        else f"⚠️ {passed}/{total_checks} checks passed"
    )

    return health


# ═══════════════════════════════════════════════════════════════
# CONFIG STATUS
# ═══════════════════════════════════════════════════════════════


def get_config_status():
    """Get configuration status"""
    status = {}

    # Telegram
    token = get_telegram_token()
    chat_id = get_telegram_chat_id()
    status["telegram"] = {
        "token": "✅ Set" if token else "❌ Missing",
        "chat_id": "✅ Set" if chat_id and chat_id != "PENDING_FETCH" else "⚠️ Pending",
    }

    # Gmail
    password = get_gmail_password()
    if password:
        try:
            import imaplib

            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            mail.login("intellimira@gmail.com", password)
            mail.logout()
            status["gmail"] = {"connection": "✅ Connected"}
        except Exception as e:
            status["gmail"] = {"connection": f"⚠️ {e}"}
    else:
        status["gmail"] = {"connection": "❌ Not configured"}

    # Enquiries repo
    repo = get_enquiries_repo()
    repo_path = Path(repo)
    status["enquiries_repo"] = {
        "path": repo,
        "exists": "✅ Found" if repo_path.exists() else "❌ Missing",
    }

    return status


# ═══════════════════════════════════════════════════════════════
# LEADS SUMMARY
# ═══════════════════════════════════════════════════════════════


def get_leads_summary():
    """Get leads summary from repo"""
    repo = Path(get_enquiries_repo())
    summary = {
        "total": 0,
        "qualified": 0,
        "pending": 0,
        "critical": 0,
        "new_today": 0,
        "by_interest": {},
    }

    if not repo.exists():
        return summary

    today = datetime.now().date()

    for folder in ["prospects", "outreach", "newsletter"]:
        folder_path = repo / folder
        if not folder_path.exists():
            continue

        for json_file in folder_path.glob("*.json"):
            try:
                with open(json_file) as f:
                    lead = json.load(f)

                summary["total"] += 1

                # Interest breakdown
                interest = lead.get("interest", "other")
                summary["by_interest"][interest] = (
                    summary["by_interest"].get(interest, 0) + 1
                )

                # Score-based
                score = lead.get("pain_score")
                if score:
                    if score >= 9:
                        summary["critical"] += 1
                    elif score >= 7:
                        summary["qualified"] += 1
                    elif score >= 5:
                        summary["pending"] += 1

                # New today
                if lead.get("timestamp"):
                    try:
                        lead_date = datetime.fromisoformat(
                            lead["timestamp"].replace("Z", "+00:00")
                        ).date()
                        if lead_date == today:
                            summary["new_today"] += 1
                    except:
                        pass

            except:
                pass

    return summary


# ═══════════════════════════════════════════════════════════════
# GMAIL STATUS
# ═══════════════════════════════════════════════════════════════


def get_gmail_status():
    """Get Gmail polling status"""
    status = {"connected": False, "last_check": None, "new_enquiries": 0}

    password = get_gmail_password()
    if not password:
        return status

    repo = Path(get_enquiries_repo())
    cache_file = repo / ".last_poll"

    if cache_file.exists():
        with open(cache_file) as f:
            status["last_check"] = f.read().strip()

    # Count new files today
    if repo.exists():
        today = datetime.now().date()
        for folder in ["prospects", "outreach", "newsletter"]:
            folder_path = repo / folder
            if not folder_path.exists():
                continue
            for json_file in folder_path.glob("*.json"):
                try:
                    mtime = datetime.fromtimestamp(json_file.stat().st_mtime).date()
                    if mtime == today:
                        status["new_enquiries"] += 1
                except:
                    pass

    status["connected"] = True
    return status


# ═══════════════════════════════════════════════════════════════
# REPORT GENERATION
# ═══════════════════════════════════════════════════════════════


def generate_telegram_report():
    """Generate Telegram-formatted report"""
    health = get_system_health()
    config = get_config_status()
    leads = get_leads_summary()
    gmail = get_gmail_status()

    report = f"""
📊 <b>MIRA SYSTEM REPORT</b>
═══════════════════════════════
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

⚙️ <b>SYSTEM HEALTH</b>
├─ RAM: {health["ram"]["used_gb"]}GB/{health["ram"]["total_gb"]}GB ({health["ram"]["percent"]}%) {health["ram"]["status"]}
├─ Disk: {health["disk"]["used_gb"]}GB/{health["disk"]["total_gb"]}GB ({health["disk"]["percent"]}%) {health["disk"]["status"]}
├─ Swap: {health.get("swap", {}).get("used_gb", 0)}GB {health.get("swap", {}).get("status", "⚠️")}
└─ Ollama: {health.get("ollama", {}).get("status", "Unknown")}

📧 <b>GMAIL STATUS</b>
├─ Connection: {"✅" if gmail["connected"] else "❌"}
├─ Last Poll: {gmail.get("last_check", "Never") or "Never"}
└─ New Today: {gmail["new_enquiries"]}

📊 <b>LEADS SUMMARY</b>
├─ Total: {leads["total"]}
├─ Qualified (7+): {leads["qualified"]}
├─ Critical (9+): {leads["critical"]}
├─ Pending (5-6): {leads["pending"]}
└─ New Today: {leads["new_today"]}

🔧 <b>CONFIG STATUS</b>
├─ Telegram: {config["telegram"]["token"]} | {config["telegram"]["chat_id"]}
├─ Gmail: {config["gmail"]["connection"]}
└─ Enquiries: {config["enquiries_repo"]["exists"]}

{health["overall"]}
"""
    return report.strip()


def generate_email_report():
    """Generate Email-formatted report"""
    health = get_system_health()
    leads = get_leads_summary()
    gmail = get_gmail_status()

    report = f"""
MIRA System Report - {datetime.now().strftime("%Y-%m-%d %H:%M")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYSTEM HEALTH
───────────────────────────────────────────────
RAM:     {health["ram"]["used_gb"]}GB / {health["ram"]["total_gb"]}GB ({health["ram"]["percent"]}%) {health["ram"]["status"]}
Disk:    {health["disk"]["used_gb"]}GB / {health["disk"]["total_gb"]}GB ({health["disk"]["percent"]}%) {health["disk"]["status"]}
Swap:    {health.get("swap", {}).get("used_gb", 0)}GB {health.get("swap", {}).get("status", "⚠️")}
Ollama:  {health.get("ollama", {}).get("status", "Unknown")}

GMAIL STATUS
───────────────────────────────────────────────
Connection:  {"Connected" if gmail["connected"] else "Not Connected"}
Last Poll:   {gmail.get("last_check", "Never") or "Never"}
New Today:   {gmail["new_enquiries"]}

LEADS SUMMARY
───────────────────────────────────────────────
Total Leads:     {leads["total"]}
Qualified (7+):  {leads["qualified"]}
Critical (9+):   {leads["critical"]}
Pending (5-6):   {leads["pending"]}
New Today:       {leads["new_today"]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: {health["overall"]}
Generated by MIRA Self-Training System
"""
    return report.strip()


def send_telegram_report(report):
    """Send report to Telegram"""
    token = get_telegram_token()
    chat_id = get_telegram_chat_id()

    if not token or not chat_id or chat_id == "PENDING_FETCH":
        print("⚠️ Telegram not configured")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": report,
        "parse_mode": "HTML",
        "disable_notification": False,
    }

    try:
        req = urllib.request.Request(
            url, data=urllib.parse.urlencode(data).encode(), method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except Exception as e:
        print(f"Error sending Telegram: {e}")
        return False


def send_email_report(report, subject=None, recipients=None):
    """Send report via email using SMTP to all recipients"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        if subject is None:
            subject = f"MIRA Report - {datetime.now().strftime('%Y-%m-%d')}"

        if recipients is None:
            recipients = ALERT_RECIPIENTS

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = "intellimira@gmail.com"
        msg["To"] = ", ".join(recipients)

        # Plain text version
        msg.attach(MIMEText(report, "plain"))

        # HTML version
        html_report = report.replace("\n", "<br>\n")
        html_report = f"""
        <html>
        <body style="font-family: monospace; background: #1a1a2e; color: #eee; padding: 20px;">
            <pre style="color: #0f0;">{html_report}</pre>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_report, "html"))

        # Send via SMTP
        password = get_gmail_password()
        if not password:
            print("⚠️ No Gmail password configured")
            return False

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("intellimira@gmail.com", password)
            server.sendmail("intellimira@gmail.com", recipients, msg.as_string())

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("intellimira@gmail.com", password)
            server.sendmail(
                "intellimira@gmail.com", "intellimira@gmail.com", msg.as_string()
            )

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def get_console_report():
    """Generate console-formatted report"""
    health = get_system_health()
    config = get_config_status()
    leads = get_leads_summary()
    gmail = get_gmail_status()

    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 MIRA SYSTEM REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

⚙️ SYSTEM HEALTH
───────────────────────────────────────────────
RAM:     {health["ram"]["used_gb"]}GB / {health["ram"]["total_gb"]}GB ({health["ram"]["percent"]}%) {health["ram"]["status"]}
Disk:    {health["disk"]["used_gb"]}GB / {health["disk"]["total_gb"]}GB ({health["disk"]["percent"]}%) {health["disk"]["status"]}
Swap:    {health.get("swap", {}).get("used_gb", 0)}GB {health.get("swap", {}).get("status", "⚠️")}
Ollama:  {health.get("ollama", {}).get("status", "Unknown")}

📧 GMAIL STATUS
───────────────────────────────────────────────
Connection:  {"✅ Connected" if gmail["connected"] else "❌ Not Connected"}
Last Poll:   {gmail.get("last_check", "Never") or "Never"}
New Today:   {gmail["new_enquiries"]}

📊 LEADS SUMMARY
───────────────────────────────────────────────
Total Leads:     {leads["total"]}
Qualified (7+):  {leads["qualified"]}
Critical (9+):   {leads["critical"]}
Pending (5-6):   {leads["pending"]}
New Today:       {leads["new_today"]}

🔧 CONFIG STATUS
───────────────────────────────────────────────
Telegram:   {config["telegram"]["token"]} | {config["telegram"]["chat_id"]}
Gmail:      {config["gmail"]["connection"]}
Enquiries:  {config["enquiries_repo"]["exists"]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{health["overall"]}
"""
    return report.strip()


def check_significant_update():
    """Check if there's a significant update worth reporting"""
    health = get_system_health()
    leads = get_leads_summary()

    significant = {
        "critical_leads": leads["critical"],
        "qualified_leads": leads["qualified"],
        "system_issues": [],
        "is_significant": False,
        "reason": "",
    }

    # Check for critical leads
    if leads["critical"] > 0:
        significant["is_significant"] = True
        significant["reason"] = f"🔥 {leads['critical']} CRITICAL lead(s) detected"

    # Check for qualified leads
    elif leads["qualified"] > 0:
        significant["is_significant"] = True
        significant["reason"] = f"⚠️ {leads['qualified']} new qualified lead(s)"

    # Check for new leads today
    elif leads["new_today"] > 0:
        significant["is_significant"] = True
        significant["reason"] = f"📬 {leads['new_today']} new enquiry(ies) today"

    # Check system health
    for check_name, passed in health["checks"]:
        if not passed:
            significant["system_issues"].append(check_name)

    if significant["system_issues"]:
        significant["is_significant"] = True
        significant["reason"] = (
            f"⚙️ System issue: {', '.join(significant['system_issues'])}"
        )

    return significant


def generate_significant_report():
    """Generate a report specifically for significant updates"""
    health = get_system_health()
    leads = get_leads_summary()
    gmail = get_gmail_status()

    # Build critical section
    critical_details = ""
    if leads["critical"] > 0:
        critical_details = f"""
🚨 CRITICAL LEADS ({leads["critical"]})
───────────────────────────────────────────────
Action Required: Immediate review needed!
"""

    qualified_details = ""
    if leads["qualified"] > 0:
        qualified_details = f"""
⚠️ QUALIFIED LEADS ({leads["qualified"]})
───────────────────────────────────────────────
Review at: /home/sir-v/MiRA/enquiries_local/prospects/
"""

    system_issues = ""
    for check_name, passed in health["checks"]:
        if not passed:
            system_issues += f"❌ {check_name} - Needs attention\n"

    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 MIRA SIGNIFICANT UPDATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

{critical_details}
{qualified_details}
{system_issues}
📊 QUICK STATS
───────────────────────────────────────────────
Total Leads:     {leads["total"]}
New Today:       {leads["new_today"]}
Qualified (7+):  {leads["qualified"]}
Critical (9+):   {leads["critical"]}

📧 GMAIL
───────────────────────────────────────────────
New Enquiries: {gmail["new_enquiries"]}

⚙️ SYSTEM HEALTH
───────────────────────────────────────────────
RAM:     {health["ram"]["used_gb"]}GB / {health["ram"]["total_gb"]}GB ({health["ram"]["percent"]}%)
Disk:    {health["disk"]["used_gb"]}GB / {health["disk"]["total_gb"]}GB ({health["disk"]["percent"]}%)
Ollama:  {health.get("ollama", {}).get("status", "Unknown")}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply to this message for MIRA analysis
"""
    return report.strip()


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MIRA Report Generator")
    parser.add_argument("--console", "-c", action="store_true", help="Print to console")
    parser.add_argument(
        "--telegram", "-t", action="store_true", help="Send to Telegram"
    )
    parser.add_argument("--email", "-e", action="store_true", help="Send to email")
    parser.add_argument("--all", "-a", action="store_true", help="Send to all channels")
    parser.add_argument(
        "--significant",
        "-s",
        action="store_true",
        help="Send only on significant updates",
    )
    parser.add_argument(
        "--check", action="store_true", help="Check if significant update exists"
    )

    args = parser.parse_args()

    # Default: console output
    if not any(
        [
            args.console,
            args.telegram,
            args.email,
            args.all,
            args.significant,
            args.check,
        ]
    ):
        args.console = True

    # Check mode - just check and report
    if args.check:
        significant = check_significant_update()
        if significant["is_significant"]:
            print(f"✅ SIGNIFICANT: {significant['reason']}")
        else:
            print("ℹ️ No significant updates")
        sys.exit(0)

    # Significant update mode
    if args.significant:
        significant = check_significant_update()
        if not significant["is_significant"]:
            print("ℹ️ No significant updates to report")
            sys.exit(0)

        print(f"📊 Significant update detected: {significant['reason']}")

        # Send significant report
        sig_report = generate_significant_report()
        print("\n" + sig_report)

        print("\n📱 Sending to Telegram...")
        if send_telegram_report(sig_report):
            print("✅ Telegram alert sent!")
        else:
            print("❌ Failed to send Telegram alert")

        print("\n📧 Sending to email...")
        if send_email_report(
            sig_report, subject=f"🚨 MIRA Alert: {significant['reason']}"
        ):
            print("✅ Email alert sent!")
        else:
            print("❌ Failed to send email alert")

        sys.exit(0)

    # Normal report mode
    telegram_report = generate_telegram_report()
    email_report = generate_email_report()
    console_report = get_console_report()

    if args.console or not any([args.telegram, args.email, args.all]):
        print(console_report)

    if args.telegram or args.all:
        print("\n📱 Sending to Telegram...")
        if send_telegram_report(telegram_report):
            print("✅ Telegram report sent!")
        else:
            print("❌ Failed to send Telegram report")

    if args.email or args.all:
        print("\n📧 Sending to email...")
        if send_email_report(email_report):
            print("✅ Email report sent!")
        else:
            print("❌ Failed to send email report")
