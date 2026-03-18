import asyncio
from playwright.async_api import async_playwright

async def ui_force_inject():
    state_path = "/home/sir-v/.whop_storage_state.json"
    products = [
        {"name": "Shadow Revenue Audit", "price": "29"},
        {"name": "Priority Launch Slot", "price": "49"},
        {"name": "White-Glove Vault Setup", "price": "199"}
    ]

    print("\n--- ACCT: UI BRUTE-FORCE INJECTION ---")
    
    async with async_playwright() as p:
        # Launch headful so the Commander can see the physical birth of the products
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        try:
            for prod in products:
                print(f"[*] Physically Building: {prod['name']} (£{prod['price']})...")
                # Navigate directly to the new experience creation
                await page.goto("https://whop.com/sell/products/new")
                await page.wait_for_timeout(5000)
                
                # Fill Name
                name_input = await page.query_selector('input[placeholder*="Name"]')
                if name_input: await name_input.fill(prod["name"])
                
                # We stop here to let the Commander click the final 'Create'
                print(f"\n[ACTION] Please click 'CREATE' for {prod['name']} in the browser.")
                # Wait 60 seconds for each click
                await page.wait_for_timeout(60000)
                
            print("\n[SUCCESS] Brute-Force Injection Complete.")
            await context.storage_state(path=state_path)
            
        except Exception as e:
            print(f"[!] UI Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(ui_force_inject())
