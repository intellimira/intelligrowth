import asyncio
from playwright.async_api import async_playwright

async def final_strike():
    state_path = "/home/sir-v/.whop_storage_state.json"
    biz_id = "biz_wJSN9AZSnng2vT"
    products = [
        {"name": "Shadow Revenue Audit", "price": "29"},
        {"name": "Priority Launch Slot", "price": "49"},
        {"name": "White-Glove Vault Setup", "price": "199"}
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("\n--- ACCT: EXECUTING TRIPLE-STRIKE ---")
        for prod in products:
            try:
                print(f"[*] Building: {prod['name']}...")
                await page.goto(f"https://whop.com/sell/{biz_id}/products/new")
                await page.wait_for_timeout(5000)
                
                # Physical Keyboard Emulation to bypass React blocks
                await page.keyboard.type(prod['name'])
                await page.keyboard.press("Tab")
                await page.keyboard.type(prod['price'])
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(5000)
                print(f"    [+] {prod['name']} CREATED.")
            except:
                print(f"    [!] Build failed for {prod['name']}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(final_strike())
