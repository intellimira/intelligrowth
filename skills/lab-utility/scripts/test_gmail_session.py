import asyncio
from playwright.async_api import async_playwright

async def test_session():
    state_path = "/home/sir-v/.notebooklm/storage_state.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Load the session you created during the NotebookLM login
        context = await browser.new_context(storage_state=state_path)
        page = await context.new_page()
        
        print("[*] Attempting to access Gmail via existing session...")
        await page.goto("https://mail.google.com/mail/u/0/#inbox")
        await page.wait_for_timeout(5000)
        
        title = await page.title()
        print(f"[+] Page Title: {title}")
        
        if "Inbox" in title or "Gmail" in title:
            print("[SUCCESS] Session is valid. We can send emails via Web Injection.")
        else:
            print("[FAIL] Session expired or Gmail requires re-auth.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_session())
