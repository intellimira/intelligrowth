import asyncio
from playwright.async_api import async_playwright
import re

async def optic_purge():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT WHOP AGENT: OPTIC PURGE ---")
        await page.goto("https://whop.com/hub")
        
        print("[ACTION] Please click 'IntelliGrow' -> 'Products'.")
        print("[*] Waiting for the URL to change to a 'products' path...")
        
        try:
            for _ in range(120):
                url = page.url
                if "/products" in url:
                    match = re.search(r'biz_[a-zA-Z0-9]+', url)
                    if match:
                        biz_id = match.group(0)
                        print(f"\n[SUCCESS] PURGE AGENT CAPTURED ID: {biz_id}")
                        content = await page.inner_text('body')
                        print(f"[*] Visible Products: \n{content[:500]}")
                        break
                await asyncio.sleep(1)
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(optic_purge())
