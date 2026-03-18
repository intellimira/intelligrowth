import asyncio
from playwright.async_api import async_playwright

async def exhaustive_scan():
    state_path = "/home/sir-v/.whop_storage_state.json"
    biz_id = "biz_wJSN9AZSnng2vT"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT: EXHAUSTIVE UI SCAN ---")
        await page.goto(f"https://whop.com/sell/{biz_id}/products")
        await page.wait_for_timeout(10000)
        
        # Capture all text on the page
        text_content = await page.evaluate("() => document.body.innerText")
        print("[*] Dashboard Text Pulse (First 500 chars):")
        print(text_content[:500])
        
        # Specifically look for products in the 'grid' or 'list'
        if "Shadow Revenue Audit" in text_content:
            print("[+] Verified: Shadow Revenue Audit is present.")
        if "Priority Launch Slot" in text_content:
            print("[+] Verified: Priority Launch Slot is present.")
        if "White-Glove Vault Setup" in text_content:
            print("[+] Verified: White-Glove Vault Setup is present.")
            
        # Check for non-standard terms usually found in Whop's AI-generated starter templates
        rogue_indicators = ["Monthly retainer", "Sample", "Example", "Standard", "Pro Plan"]
        for ri in rogue_indicators:
            if ri in text_content:
                print(f"[!] POTENTIAL ROGUE DETECTED: Found string '{ri}' in dashboard.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(exhaustive_scan())
