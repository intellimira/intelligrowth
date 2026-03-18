import asyncio
from playwright.async_api import async_playwright

async def run_gmail_handshake():
    print("\n--- ACCT: GMAIL API HANDSHAKE INITIATED ---")
    print("[*] Launching Cloud Console...")
    print("[*] INSTRUCTIONS:")
    print("    1. Sign in to intellimira@gmail.com.")
    print("    2. Enable 'Gmail API' in the Marketplace.")
    print("    3. Create 'OAuth 2.0 Client ID' (Application type: Desktop App).")
    print("    4. Once you have the credentials.json, ACCT will take it from here.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to the API Library for Gmail
        await page.goto("https://console.cloud.google.com/apis/library/gmail.googleapis.com")

        print("\n[*] Waiting for you to complete the setup...")
        # Keep alive for 10 minutes to allow for manual setup
        try:
            await asyncio.sleep(600) 
        except Exception:
            pass
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_gmail_handshake())
