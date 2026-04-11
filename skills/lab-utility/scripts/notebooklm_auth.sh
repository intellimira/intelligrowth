#!/bin/bash
# One-time NotebookLM auth - run this once, tokens last for weeks
echo "
╔═══════════════════════════════════════════════════════════╗
║  📓 NOTEBOOKLM AUTH (ONE-TIME SETUP)                    ║
╠═══════════════════════════════════════════════════════════╣
║  1. Browser will open to Google login                   ║
║  2. Sign in: intellimira@gmail.com                      ║
║  3. Click 'Allow' if prompted                          ║
║  4. Browser will auto-close when done                   ║
║  5. Done! Future runs are fully automated.              ║
╚═══════════════════════════════════════════════════════════╝
"

python3 << 'PYEOF'
import asyncio
import json
from playwright.async_api import async_playwright

async def quick_auth():
    token_path = "/home/sir-v/.notebooklm/tokens.json"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("https://accounts.google.com/")
        print("[*] Browser open - complete Google login...")
        
        # Simple wait - check every 3 seconds for success
        for i in range(120):  # 6 min max
            url = page.url
            if "notebooklm.google.com" in url and "notebook/" in url:
                cookies = await context.cookies()
                with open(token_path, 'w') as f:
                    json.dump(cookies, f)
                print(f"[✓] Auth complete! {len(cookies)} cookies saved.")
                await browser.close()
                return True
            await asyncio.sleep(3)
        
        print("[!] Timeout")
        await browser.close()
        return False

asyncio.run(quick_auth())
PYEOF
