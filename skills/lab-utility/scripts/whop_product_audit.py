import asyncio
from playwright.async_api import async_playwright

async def audit_and_purge():
    state_path = "/home/sir-v/.whop_storage_state.json"
    biz_id = "biz_wJSN9AZSnng2vT"
    approved = ["Shadow Revenue Audit", "Priority Launch Slot", "White-Glove Vault Setup"]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT: PRODUCT PURGE PROTOCOL ---")
        await page.goto(f"https://whop.com/sell/{biz_id}/products")
        await page.wait_for_timeout(8000)
        
        # Pull all links that might be product titles
        product_elements = await page.query_selector_all('a[href*="/products/"]')
        found_names = []
        for el in product_elements:
            name = await el.inner_text()
            if name and name.strip():
                found_names.append(name.strip())
        
        found_names = list(set(found_names))
        print(f"[*] Detected Product Names: {found_names}")
        
        rogue_products = [name for name in found_names if name not in approved and name != "Create product"]
        
        if rogue_products:
            print(f"[!] ROGUE PRODUCTS DETECTED: {rogue_products}")
            # We will now attempt to archive/delete the rogue ones
            for rogue in rogue_products:
                print(f"[*] AGENT: Commencing Purge of '{rogue}'...")
                # In a high-fidelity agentic move, we will navigate to the rogue product settings and archive it
                # For safety, I will stop after detection to confirm with Commander if multiple exist
        else:
            print("[SUCCESS] System Clean. Only approved IntelliGrow products are live.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(audit_and_purge())
