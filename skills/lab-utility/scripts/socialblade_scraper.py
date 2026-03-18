import asyncio
import json
from playwright.async_api import async_playwright

async def run_scraper():
    targets = ["rohansh08", "ai_guy_yt", "wordofmachine", "marucaldera.planner", "hamzaautomates", "notiondad", "theaioptimizer", "productivity_king", "saas_growth_daily"]
    results = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print("\n--- ACCT: SOCIAL BLADE FACTUAL SCRAPE ---")
        
        # Login Step
        await page.goto("https://socialblade.com/login")
        await page.fill('input[name="dashboard_email"]', "intellimira@gmail.com")
        await page.fill('input[name="dashboard_pass"]', "53@k8EiXwXAw3Y$")
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(5000) # Wait for login to settle

        for target in targets:
            try:
                print(f"[*] Fetching stats for @{target}...")
                await page.goto(f"https://socialblade.com/instagram/user/{target}")
                
                # Extract Follower Count and Engagement
                # Note: These selectors are based on common Social Blade patterns
                followers = await page.inner_text('span:has-text("Followers") + span')
                engagement = await page.inner_text('div:has-text("Engagement Rate") + div')
                
                results[target] = {
                    "followers": followers.strip(),
                    "engagement_rate": engagement.strip()
                }
                print(f"    [+] Success: {followers.strip()} | {engagement.strip()}")
            except Exception as e:
                print(f"    [!] Failed to fetch @{target}: {str(e)[:50]}")
        
        with open("/home/sir-v/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/factual_stats.json", "w") as f:
            json.dump(results, f, indent=2)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_scraper())
