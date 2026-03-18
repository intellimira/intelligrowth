import asyncio
from playwright.async_api import async_playwright

async def run_diagnostic():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("[*] Accessing Whop Dashboards...")
        await page.goto("https://whop.com/dashboards")
        await page.wait_for_timeout(5000)
        
        # Check for existing companies
        content = await page.content()
        if "Create your first experience" in content or "Create a company" in content:
            print("[!] STATUS: No Business/Company found. System is at Zero-State.")
        else:
            print("[+] STATUS: Business/Company detected.")
            # Try to find the name of the company
            try:
                company_name = await page.inner_text('h1')
                print(f"[+] Active Business Name: {company_name}")
            except:
                pass

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_diagnostic())
