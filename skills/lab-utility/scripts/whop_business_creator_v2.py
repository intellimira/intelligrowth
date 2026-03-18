import asyncio
from playwright.async_api import async_playwright

async def create():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        # Launch headful so you can assist if UI blocks me
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("[*] Opening Whop Creation Page...")
        await page.goto("https://whop.com/create")
        
        print("[*] Please ensure 'IntelliGrow' is typed and click 'Create' if I am blocked.")
        # Try to find any input and type IntelliGrow
        try:
            await page.wait_for_selector('input', timeout=15000)
            await page.fill('input', "IntelliGrow")
            print("[+] Typed 'IntelliGrow' into the first available field.")
        except:
            pass

        # Wait for you to finish or for the dashboard to load
        print("[*] Waiting for Dashboard confirmation...")
        try:
            await page.wait_for_url("**/dashboard**", timeout=120000)
            print("[SUCCESS] Business Dashboard Active.")
            await context.storage_state(path=state_path)
        except:
            print("[!] Still waiting... please finish the creation in the browser window.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(create())
