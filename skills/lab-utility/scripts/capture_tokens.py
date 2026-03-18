import asyncio
import os
import json
from playwright.async_api import async_playwright

async def capture_google_tokens():
    """
    Opens an interactive browser for the user to sign in to Google/NotebookLM.
    Captures cookies once the dashboard is reached.
    """
    token_path = "/home/sir-v/ACCT_SYSTEM/Skill_Vault/notebook_bridge/tokens.json"
    os.makedirs(os.path.dirname(token_path), exist_ok=True)

    print("\n--- ACCT: INTERACTIVE SIGN-IN INITIATED ---")
    print("[*] Launching Chromium (Non-Headless)...")
    print("[*] Please sign in to your Google account in the browser window.")
    print("[*] Once you are at https://notebooklm.google.com/, come back here.")

    async with async_playwright() as p:
        # Launch browser in non-headless mode for user interaction
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("https://notebooklm.google.com/")

        # Wait for the user to navigate to the dashboard (sign-in completion)
        # We wait for a specific element that exists on the dashboard or URL change
        print("[*] Waiting for user to reach NotebookLM dashboard...")
        
        # Poll every 5 seconds to check if we are on the dashboard
        while True:
            current_url = page.url
            if "notebooklm.google.com" in current_url and "/notebook/" in current_url:
                # Some versions might just be at the root after login
                break
            if "notebooklm.google.com" in current_url and "login" not in current_url and "signin" not in current_url:
                # Likely dashboard
                break
            await asyncio.sleep(5)

        print("[+] Dashboard detected. Capturing session cookies...")
        cookies = await context.cookies()
        
        with open(token_path, 'w') as f:
            json.dump(cookies, f)
        
        print(f"[+] Tokens successfully vaulted at: {token_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_google_tokens())
