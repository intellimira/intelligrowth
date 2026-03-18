import asyncio
from playwright.async_api import async_playwright

async def run_whop_auth():
    print("\n--- ACCT: WHOP.COM AUTHENTICATION BRIDGE ---")
    print("[*] Launching Whop.com...")
    print("[*] INSTRUCTIONS:")
    print("    1. Sign in to your Whop account in the browser window.")
    print("    2. Once you are on your dashboard, ACCT will vault the session.")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("https://whop.com/login")
        
        print("\n[*] Waiting for you to complete the sign-in...")
        try:
            # Increased timeout to 10 mins for manual entry
            await page.wait_for_selector('a[href*="/dashboard"]', timeout=600000)
            
            state_path = "/home/sir-v/.whop_storage_state.json"
            await context.storage_state(path=state_path)
            print(f"\n[+] SUCCESS: Whop Session Vaulted at {state_path}")
        except Exception as e:
            print(f"\n[!] Auth Timeout or Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_whop_auth())
