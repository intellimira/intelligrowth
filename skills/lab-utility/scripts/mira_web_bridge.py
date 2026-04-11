#!/usr/bin/env python3
"""
MIRA-Web-CLi OpenCode Bridge
============================
Enables OpenCode to access authenticated/protected web content via MIRA-Web-CLi.

Usage:
    python3 mira_web_bridge.py <url> [--auth] [--interactive]
    python3 mira_web_bridge.py --status <domain>

Examples:
    # Auto-fetch (uses saved tokens)
    python3 mira_web_bridge.py "https://notebooklm.google.com/notebook/ID"

    # Force interactive auth (opens browser for login)
    python3 mira_web_bridge.py "https://notebooklm.google.com" --auth

    # Check token status
    python3 mira_web_bridge.py --status notebooklm.google.com
"""

import sys
import asyncio
import json
import os
from datetime import datetime

# Add MIRA-Web-CLi src to path
sys.path.insert(0, "/home/sir-v/Documents/MiRA-Web-CLi/src")
from engine import SovereignEngine, TokenVault


def print_json(data):
    """Print JSON output for OpenCode to parse."""
    print(json.dumps(data, indent=2))


async def main():
    if len(sys.argv) < 2:
        print("Usage: mira_web_bridge.py <url> [--auth] [--interactive]")
        print("       mira_web_bridge.py --status <domain>")
        sys.exit(1)

    # Check status command
    if sys.argv[1] == "--status":
        domain = sys.argv[2] if len(sys.argv) > 2 else None
        if not domain:
            print("Usage: mira_web_bridge.py --status <domain>")
            sys.exit(1)

        vault = TokenVault("/home/sir-v/Documents/MiRA-Web-CLi/memory/tokens/")
        tokens = vault.load(domain)

        if tokens:
            saved = datetime.fromisoformat(tokens["timestamp"])
            age = (datetime.now() - saved).days
            valid = vault.is_valid(domain)

            print_json(
                {
                    "domain": domain,
                    "status": "VALID" if valid else "EXPIRED",
                    "age_days": age,
                    "saved_at": tokens["timestamp"],
                    "cookie_count": len(tokens.get("cookies", [])),
                }
            )
        else:
            print_json(
                {
                    "domain": domain,
                    "status": "NOT_FOUND",
                    "message": "No tokens saved. Run with --auth to authenticate.",
                }
            )
        return

    url = sys.argv[1]
    force_auth = "--auth" in sys.argv
    interactive = force_auth or "--interactive" in sys.argv

    print(f"[BRIDGE] Initializing MIRA-Web-CLi Engine...", file=sys.stderr)

    engine = SovereignEngine()

    try:
        print(f"[BRIDGE] Fetching: {url}", file=sys.stderr)

        if force_auth:
            print(f"[BRIDGE] Mode: INTERACTIVE AUTH", file=sys.stderr)
            result = await engine.auth_fetch(url, interactive=True)
        else:
            print(
                f"[BRIDGE] Mode: AUTO-FETCH (will prompt auth if needed)",
                file=sys.stderr,
            )
            result = await engine.fetch_protected(url, interactive=False)

        if "error" in result:
            if result["error"] == "LOGIN_REQUIRED":
                print_json(
                    {
                        "error": "AUTH_REQUIRED",
                        "message": f"Login required for {url}",
                        "solution": f'Run: python3 mira_web_bridge.py "{url}" --auth',
                    }
                )
            else:
                print_json(result)
            sys.exit(1)

        # Return clean output for OpenCode
        print_json(
            {
                "success": True,
                "url": result.get("url", url),
                "title": result.get("title", ""),
                "text": result.get("text", ""),
                "mode": result.get("mode", "UNKNOWN"),
                "domain": engine._extract_domain(url),
            }
        )

    except Exception as e:
        import traceback

        print_json(
            {"error": str(e), "type": type(e).__name__, "trace": traceback.format_exc()}
        )
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
