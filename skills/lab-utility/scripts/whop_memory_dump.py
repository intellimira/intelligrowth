import asyncio
from playwright.async_api import async_playwright

async def dump_memory():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n[*] Navigating to IntelliGrow Dashboard...")
        await page.goto("https://whop.com/sell/settings/general")
        await page.wait_for_timeout(10000)
        
        # We physically extract the 'whop_biz_id' from the page's localStorage or global state
        biz_id = await page.evaluate("() => localStorage.getItem('active_biz_id') || window.__WHOP_DATA__?.biz_id")
        print(f"[!] DUMPED BIZ ID: {biz_id}")
        
        # If null, we try to find it in the URL via forced navigation to 'Settings'
        if not biz_id:
            print("[*] LocalStorage empty. Checking URL structure...")
            await page.goto("https://whop.com/sell/settings/developer")
            await page.wait_for_timeout(5000)
            url = page.url
            print(f"[+] Final Settings URL: {url}")
            # Whop often hides the ID in the URL path now
            import re
            match = re.search(r'biz_[a-zA-Z0-9]+', url)
            if match:
                biz_id = match.group(0)
                print(f"[SUCCESS] FOUND ID VIA URL MEMORY: {biz_id}")

        await browser.close()
        return biz_id

if __name__ == "__main__":
    asyncio.run(dump_memory())
