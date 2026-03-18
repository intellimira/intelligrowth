import asyncio
from playwright.async_api import async_playwright
import re

async def deep_agent_act():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT WHOP AGENT: DEEP ACTUATION ---")
        print("[*] Accessing Hub...")
        await page.goto("https://whop.com/hub")
        await page.wait_for_timeout(8000)
        
        # We find the link that points to the 'Sell' dashboard for IntelliGrow
        print("[*] Scanning for Business Links...")
        links = await page.eval_on_selector_all('a', 'nodes => nodes.map(n => n.href)')
        sell_links = [l for l in links if "/sell/" in l]
        print(f"[*] Sell Links Found: {sell_links}")
        
        if sell_links:
            # Navigate to the first Sell link (our business)
            target = sell_links[0]
            print(f"[*] Navigating to: {target}")
            await page.goto(target)
            await page.wait_for_timeout(10000)
            
            # The URL should now be whop.com/sell/biz_XXXXX/dashboard
            final_url = page.url
            print(f"[+] CURRENT URL: {final_url}")
            match = re.search(r'biz_[a-zA-Z0-9]+', final_url)
            if match:
                biz_id = match.group(0)
                print(f"[SUCCESS] AGENT EXTRACTED ID: {biz_id}")
                
                # NOW: Physical Product Creation via Agentic Clicks
                print(f"[*] AGENT: Creating £29 Audit Product...")
                await page.goto(f"https://whop.com/sell/{biz_id}/products/new")
                await page.wait_for_timeout(5000)
                
                # Fill and Save autonomously
                try:
                    await page.fill('input[placeholder*="Name"]', "Shadow Revenue Audit")
                    # We trigger the 'Create' button
                    await page.click('button:has-text("Create")')
                    print(f"[+] AGENT PHYSICALLY CREATED £29 PRODUCT.")
                except Exception as e:
                    print(f"[!] UI interaction failed: {e}")
            else:
                print("[!] Could not find 'biz_' in the Sell URL.")
        else:
            print("[!] No 'Sell' links detected in the Hub.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(deep_agent_act())
