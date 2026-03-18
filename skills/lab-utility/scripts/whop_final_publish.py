import asyncio
from playwright.async_api import async_playwright

async def run_publish():
    state_path = "/home/sir-v/.whop_storage_state.json"
    biz_id = "biz_wJSN9AZSnng2vT"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT: FINAL PUBLISHING BRIDGE ---")
        print("[*] Navigating to IntelliGrow Products...")
        await page.goto(f"https://whop.com/sell/{biz_id}/products")
        
        print("[ACTION] Please click each product and hit 'PUBLISH' or 'SAVE'.")
        print("[*] I will keep this window open for 10 minutes for you to finish...")
        
        try:
            await page.wait_for_timeout(600000) 
            # Save the final published state
            await context.storage_state(path=state_path)
            print("[v] Session Updated with Published Products.")
        except:
            pass
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_publish())
