import asyncio
from playwright.async_api import async_playwright
import re

async def optic_purge():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT WHOP AGENT: OPTIC PURGE v2 ---")
        await page.goto("https://whop.com/hub")
        
        print("[ACTION] 1. Click 'IntelliGrow' | 2. Click 'Products' in sidebar.")
        
        try:
            # Polling for 5 minutes
            for i in range(300):
                url = page.url
                if "/products" in url:
                    match = re.search(r'biz_[a-zA-Z0-9]+', url)
                    if match:
                        biz_id = match.group(0)
                        print(f"\n[SUCCESS] PURGE AGENT CAPTURED ID: {biz_id}")
                        # Final State Save
                        await context.storage_state(path=state_path)
                        
                        # Extract all text to find the rogue AI product
                        content = await page.inner_text('body')
                        print(f"[*] Dashboard Content Snapshot:\n{content[:1000]}")
                        break
                if i % 10 == 0:
                    print(f"[*] Waiting... Current URL: {url}")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(optic_purge())
