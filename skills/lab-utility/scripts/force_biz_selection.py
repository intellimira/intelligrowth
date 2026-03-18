import asyncio
from playwright.async_api import async_playwright

async def force_click():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        await page.goto("https://whop.com/dashboards")
        await page.wait_for_timeout(5000)
        
        print("[*] Dashboard Content Loaded. Looking for IntelliGrow link...")
        # Click the link that contains IntelliGrow or redirects to a biz dashboard
        try:
            await page.click('a[href*="dashboard"]:has-text("IntelliGrow")')
            await page.wait_for_timeout(5000)
            print(f"[+] Final URL: {page.url}")
        except Exception as e:
            # If click fails, try to just find all links
            links = await page.eval_on_selector_all('a', 'nodes => nodes.map(n => n.href)')
            print(f"[*] Found links: {links}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(force_click())
