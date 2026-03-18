import asyncio
from playwright.async_api import async_playwright

async def push_product():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        # Launch Headful so you can see and assist the final click
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n[*] Navigating to Product Creation Page...")
        await page.goto("https://whop.com/dashboard/products/new")
        
        # Wait for the UI to load
        await page.wait_for_timeout(5000)
        
        print("[*] PHYSICALLY PUSHING: Shadow Revenue Audit (£29)")
        try:
            # We try to fill the name if the field is visible
            name_input = await page.query_selector('input[placeholder*="name"]')
            if name_input:
                await name_input.fill("Shadow Revenue Audit")
                print("[+] Name filled.")
            
            # We wait here to let you click 'Create' or 'Continue'
            print("\n[HITL REQUIRED] Please complete the creation of the £29 product in the browser window.")
            print("[*] I will keep the window open for 5 minutes...")
            await page.wait_for_timeout(300000)
            
            # Save the state once you are done
            await context.storage_state(path=state_path)
            print("[v] Session Updated.")
            
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(push_product())
