import asyncio
from playwright.async_api import async_playwright
import re

async def crawl_sell():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT: SELL-PATH CRAWL ---")
        await page.goto("https://whop.com/sell")
        await page.wait_for_timeout(10000)
        
        # 1. Capture the page source to find ALL biz_ IDs
        content = await page.content()
        biz_ids = list(set(re.findall(r'biz_[a-zA-Z0-9]+', content)))
        print(f"[*] Detected Business IDs in source: {biz_ids}")
        
        # 2. Extract all visible text to find the rogue product
        text = await page.evaluate("() => document.body.innerText")
        print("[*] Visible Text Summary:")
        print(text[:1000])
        
        # 3. List all links
        links = await page.eval_on_selector_all('a', 'nodes => nodes.map(n => n.href)')
        dash_links = [l for l in links if "/dashboard" in l or "/sell/biz_" in l]
        print(f"[*] Relevant Dashboard Links: {dash_links}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(crawl_sell())
