import asyncio
from playwright.async_api import async_playwright

async def agent_actuate():
    state_path = "/home/sir-v/.whop_storage_state.json"
    biz_id = "biz_wJSN9AZSnng2vT"
    products = [
        {"name": "Shadow Revenue Audit", "price": "29"},
        {"name": "Priority Launch Slot", "price": "49"},
        {"name": "White-Glove Vault Setup", "price": "199"}
    ]

    print(f"\n--- ACCT: AGENTIC ACTUATOR START (BIZ: {biz_id}) ---")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        for prod in products:
            try:
                print(f"[*] AGENT: Physically Building {prod['name']}...")
                # Whop's direct creation URL
                await page.goto(f"https://whop.com/sell/{biz_id}/products/new")
                await page.wait_for_timeout(5000)
                
                # We use generic input filling to avoid UI change blocks
                await page.keyboard.type(prod['name'])
                await page.keyboard.press("Tab")
                await page.keyboard.type(prod['price'])
                
                # Physically trigger the 'Create' sequence
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(5000)
                
                print(f"    [+] AGENT: {prod['name']} successfully actuated.")
            except Exception as e:
                print(f"    [!] Error building {prod['name']}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(agent_actuate())
