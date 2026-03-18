import asyncio
from playwright.async_api import async_playwright

async def create_whop_business():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("[*] Initiating Company Creation: 'IntelliGrow'...")
        await page.goto("https://whop.com/create")
        await page.wait_for_timeout(5000)
        
        try:
            # Type Business Name
            await page.fill('input[placeholder*="name"]', "IntelliGrow")
            await page.wait_for_timeout(1000)
            
            # Select 'Digital Products' or similar if prompted
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(5000)
            
            print("[+] Company 'IntelliGrow' Created.")
            
            # Save the new state (which now includes the company access)
            await context.storage_state(path=state_path)
            print("[v] Session State Updated with Business Access.")
            
        except Exception as e:
            print(f"[!] Creation Error: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(create_whop_business())
