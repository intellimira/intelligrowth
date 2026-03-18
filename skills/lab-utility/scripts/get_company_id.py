import asyncio
from playwright.async_api import async_playwright

async def get_id():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("[*] Finding Company ID...")
        await page.goto("https://whop.com/dashboards")
        await page.wait_for_timeout(5000)
        
        url = page.url
        print(f"[+] Current Dashboard URL: {url}")
        
        # The URL usually looks like whop.com/dashboard/biz_XXXXX
        if "biz_" in url:
            biz_id = url.split("biz_")[1].split("/")[0]
            print(f"[SUCCESS] FOUND COMPANY ID: biz_{biz_id}")
        else:
            # Fallback: check content for biz_ prefix
            content = await page.content()
            import re
            match = re.search(r'biz_[a-zA-Z0-9]+', content)
            if match:
                print(f"[SUCCESS] FOUND COMPANY ID VIA CRAWL: {match.group(0)}")
            else:
                print("[!] Could not find ID. Manual check required.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_id())
