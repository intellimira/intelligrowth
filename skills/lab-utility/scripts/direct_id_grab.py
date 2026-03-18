import asyncio
from playwright.async_api import async_playwright
import re

async def grab_id():
    state_path = "/home/sir-v/.whop_storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("[*] Accessing Whop Dashboard for ID Extraction...")
        # Going to the developer page where the ID is usually in the URL
        await page.goto("https://whop.com/sell/settings/developer")
        await page.wait_for_timeout(8000)
        
        current_url = page.url
        print(f"[+] Current URL: {current_url}")
        
        # Regex search for biz_ pattern in URL or Content
        id_match = re.search(r'biz_[a-zA-Z0-9]+', current_url)
        if id_match:
            print(f"[SUCCESS] FOUND COMPANY ID IN URL: {id_match.group(0)}")
        else:
            content = await page.content()
            id_match_content = re.search(r'biz_[a-zA-Z0-9]{10,25}', content)
            if id_match_content:
                print(f"[SUCCESS] FOUND COMPANY ID IN SOURCE: {id_match_content.group(0)}")
            else:
                print("[!] ID still hidden. Whop is using high-obfuscation.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(grab_id())
