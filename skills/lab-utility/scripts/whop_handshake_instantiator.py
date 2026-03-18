import asyncio
from playwright.async_api import async_playwright

async def instantiate_handshake():
    state_path = "/home/sir-v/.whop_storage_state.json"
    biz_id = "biz_wJSN9AZSnng2vT"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT: INSTANTIATING MASTER HANDSHAKE (70/30 MVP) ---")
        try:
            await page.goto(f"https://whop.com/sell/{biz_id}/products/new")
            await page.wait_for_timeout(5000)
            
            # Form Entry
            await page.keyboard.type("70/30 Performance Partnership Agreement")
            await page.keyboard.press("Tab")
            await page.keyboard.type("0") 
            await page.keyboard.press("Enter")
            
            await page.wait_for_timeout(5000)
            print("[SUCCESS] MASTER HANDSHAKE is live. We can now send this link to creators to finalize the deal.")
            
        except Exception as e:
            print(f"[!] UI Interaction Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(instantiate_handshake())
