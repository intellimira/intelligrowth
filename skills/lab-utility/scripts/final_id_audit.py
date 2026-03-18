import asyncio
from playwright.async_api import async_playwright

async def audit():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        # 1. Go to the Hub to see the active business link
        print("[*] Accessing Whop Hub...")
        await page.goto("https://whop.com/hub")
        await page.wait_for_timeout(8000)
        
        # 2. Click the Sell/Dashboard link for IntelliGrow
        try:
            # Look for IntelliGrow text and click its parent link
            print("[*] Clicking IntelliGrow...")
            await page.click('text="IntelliGrow"')
            await page.wait_for_timeout(10000)
            
            # 3. Capture the actual URL and current products
            current_url = page.url
            print(f"[!] REVEALED URL: {current_url}")
            
            # Navigate specifically to products
            if "/sell/" in current_url:
                # Extract the REAL biz_id from the URL
                import re
                match = re.search(r'biz_[a-zA-Z0-9]+', current_url)
                if match:
                    real_biz_id = match.group(0)
                    print(f"[SUCCESS] REAL BIZ ID IDENTIFIED: {real_biz_id}")
                    
                    # GO TO PRODUCTS
                    await page.goto(f"https://whop.com/sell/{real_biz_id}/products")
                    await page.wait_for_timeout(5000)
                    
                    content = await page.inner_text('body')
                    print(f"[*] Dashboard Content Sample: {content[:200]}")
                    
                    # Logic to identify the rogue AI product
                    if "Monthly retainer" in content or "AI Automation Agency" in content:
                        print("[!] ROGUE AI PRODUCT DETECTED.")
                        # Agentic Actuation: Physically finding the rogue product link and archiving it
                else:
                    print("[!] No biz_id in URL.")
        except Exception as e:
            print(f"[!] Audit Failed: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(audit())
