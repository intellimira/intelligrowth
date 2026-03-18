import asyncio
from playwright.async_api import async_playwright

async def verify():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("[*] Checking for IntelliGrow Dashboard...")
        await page.goto("https://whop.com/dashboards")
        await page.wait_for_timeout(5000)
        
        content = await page.content()
        if "IntelliGrow" in content:
            print("[SUCCESS] Business 'IntelliGrow' Detected.")
            # Update state one more time to capture the business-specific cookies
            await context.storage_state(path=state_path)
        else:
            print("[!] 'IntelliGrow' not found in page content. Current URL: " + page.url)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
