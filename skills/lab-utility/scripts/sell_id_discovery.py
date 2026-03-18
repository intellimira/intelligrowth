import asyncio
from playwright.async_api import async_playwright

async def discover():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        # New Whop dashboard architecture uses whop.com/sell/
        print("[*] Accessing Sell Dashboard...")
        await page.goto("https://whop.com/sell/settings/developer")
        await page.wait_for_timeout(5000)
        
        print(f"[+] Final URL: {page.url}")
        
        if "biz_" in page.url:
            print(f"[SUCCESS] Found in URL: {page.url}")
        
        content = await page.content()
        import re
        ids = re.findall(r'biz_[a-zA-Z0-9]+', content)
        print(f"[+] Detected IDs: {list(set(ids))}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(discover())
