import asyncio
from playwright.async_api import async_playwright
import re

async def optic_capture():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        # Launch Headful for visual selection
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT WHOP AGENT: OPTIC CAPTURE ---")
        await page.goto("https://whop.com/sell")
        
        print("[ACTION] Please click on the 'IntelliGrow' business box in the browser.")
        print("[*] I am waiting for the URL to change to a 'biz_' path...")
        
        # We wait for the URL to update with the business ID
        try:
            # Polling URL for 2 minutes
            for _ in range(120):
                url = page.url
                match = re.search(r'biz_[a-zA-Z0-9]+', url)
                if match:
                    biz_id = match.group(0)
                    print(f"\n[SUCCESS] OPTIC CAPTURED ID: {biz_id}")
                    # Update local knowledge
                    with open("/home/sir-v/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/ACTIVE_BIZ_ID.txt", "w") as f:
                        f.write(biz_id)
                    break
                await asyncio.sleep(1)
            else:
                print("[!] Timeout: No selection detected.")
        except Exception as e:
            print(f"[!] Optic Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(optic_capture())
