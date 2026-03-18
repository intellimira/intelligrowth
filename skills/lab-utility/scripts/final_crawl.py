import asyncio
from playwright.async_api import async_playwright

async def crawl():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("[*] Performing Deep Crawl for Company ID...")
        await page.goto("https://whop.com/")
        await page.wait_for_timeout(5000)
        
        content = await page.content()
        # Find all business IDs starting with biz_
        import re
        ids = re.findall(r'biz_[a-zA-Z0-9]+', content)
        print(f"[+] Found IDs: {list(set(ids))}")
        
        # Check specific dashboard link
        dash_link = await page.query_selector('a[href*="/dashboard/biz_"]')
        if dash_link:
            href = await dash_link.get_attribute("href")
            print(f"[SUCCESS] Found Dashboard Link: {href}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(crawl())
