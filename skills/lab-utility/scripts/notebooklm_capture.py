#!/usr/bin/env python3
"""NotebookLM Interactive Token Capture
Run this in a terminal, complete the Google login, and tokens will be saved.
"""

import asyncio
import json
from playwright.async_api import async_playwright


async def main():
    token_path = "/home/sir-v/.notebooklm/tokens.json"

    print("""
╔══════════════════════════════════════════════════════════════════╗
║           📓 NOTEBOOKLM INTERACTIVE LOGIN                       ║
╠══════════════════════════════════════════════════════════════════╣
║  1. Browser will open to NotebookLM                            ║
║  2. Sign in with Google (use intellimira@gmail.com)            ║
║  3. Grant access if prompted                                   ║
║  4. Return here - tokens will auto-capture                     ║
║  5. Press Ctrl+C to cancel                                    ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("[*] Opening NotebookLM...")
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")

        # Wait loop
        check_count = 0
        while check_count < 120:  # 2 minute timeout
            url = page.url
            if "notebooklm.google.com/notebook/" in url:
                print("[✓] SUCCESS! Capturing session tokens...")
                cookies = await context.cookies()
                with open(token_path, "w") as f:
                    json.dump(cookies, f)
                print(f"[✓] Saved {len(cookies)} cookies to: {token_path}")
                await browser.close()
                return
            elif "accounts.google.com" in url and "signin/rejected" in url:
                print("[!] Login rejected - check your credentials")
                await browser.close()
                return
            else:
                check_count += 1
                if check_count % 10 == 0:
                    print(f"[*] Waiting for login... ({check_count}s)")
                await asyncio.sleep(1)

        print("[!] Timeout reached")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
