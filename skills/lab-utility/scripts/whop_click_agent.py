import asyncio
from playwright.async_api import async_playwright
import re

async def click_and_reveal():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT WHOP AGENT: CLICK-AND-REVEAL ---")
        await page.goto("https://whop.com/sell")
        await page.wait_for_timeout(8000)
        
        print("[*] Looking for 'IntelliGrow' element to click...")
        # We find the element that contains the text 'IntelliGrow' and click it
        try:
            # First, list all visible text to ensure we see it
            content = await page.inner_text('body')
            if "IntelliGrow" in content:
                print("[+] 'IntelliGrow' detected on page. Clicking...")
                await page.click('text="IntelliGrow"')
                await page.wait_for_timeout(10000)
                
                final_url = page.url
                print(f"[!] REVEALED URL: {final_url}")
                
                # Check for biz_ ID
                match = re.search(r'biz_[a-zA-Z0-9]+', final_url)
                if match:
                    print(f"[SUCCESS] AGENT REVEALED BIZ ID: {match.group(0)}")
                else:
                    print("[!] Click successful but URL did not reveal biz_ ID.")
            else:
                print("[!] 'IntelliGrow' not found in visible text. Scanning for grid items...")
                # Fallback: click the first business card
                await page.click('div[role="button"]')
                await page.wait_for_timeout(5000)
                print(f"[!] Fallback URL: {page.url}")
        except Exception as e:
            print(f"[!] Click Action Failed: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(click_and_reveal())
