import asyncio
from playwright.async_api import async_playwright
import os

async def capture():
    report_path = "file://" + os.path.abspath("/home/sir-v/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/SOVEREIGN_ULTIMA_REPORT.html")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        print(f"[*] Rendering Aetheric Terminal: {report_path}")
        await page.goto(report_path)
        # Wait for JS animation/gauges to finish
        await page.wait_for_timeout(5000)
        
        screenshot_path = "/home/sir-v/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/AETHERIC_SNAPSHOT.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"[SUCCESS] Snapshot Captured: {screenshot_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture())
