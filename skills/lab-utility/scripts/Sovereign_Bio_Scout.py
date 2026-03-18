import asyncio
import json
import os
import re
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

class SovereignBioScout:
    def __init__(self, target_handles):
        self.targets = target_handles
        self.results = {}
        self.output_path = "/home/sir-v/MiRA/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/active_ops/bio_scout_recon.json"

    def parse_count(self, text):
        if not text or text == "Unknown":
            return 10000
        
        # Remove commas and handle K/M/B
        text = text.replace(',', '').upper()
        match = re.search(r'([\d.]+)([KMB]?)', text)
        if not match:
            return 10000
            
        value = float(match.group(1))
        multiplier = 1
        if match.group(2) == 'K': multiplier = 1000
        elif match.group(2) == 'M': multiplier = 1000000
        elif match.group(2) == 'B': multiplier = 1000000000
        
        final_val = int(value * multiplier)
        return max(final_val, 10000) # HARD FLOOR

    async def extract_bio_data(self, page, handle):
        clean_handle = handle.strip("@")
        print(f"[*] RECON: Investigating @{clean_handle}...")
        results = {"handle": clean_handle, "email": "NOT_FOUND", "followers": 10000, "status": "RECON_REQUIRED"}
        
        # SOURCE 1: Direct Instagram (Headless Check)
        try:
            await page.goto(f"https://www.instagram.com/{clean_handle}/", timeout=30000)
            await page.wait_for_timeout(3000)
            header = await page.query_selector('header')
            if header:
                header_text = await header.inner_text()
                # Follower Extraction
                follower_match = re.search(r'([\d.kmMK]+) followers', header_text, re.IGNORECASE)
                if follower_match:
                    results["followers"] = self.parse_count(follower_match.group(1))
                
                # Email Extraction
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = re.findall(email_pattern, header_text)
                if emails: results["email"] = emails[0]
        except Exception as e:
            print(f"    [!] IG Phase Failed: {str(e)[:40]}")

        # SOURCE 2: InsTrack (Resilience Fallback)
        if results["email"] == "NOT_FOUND":
            try:
                print(f"    [>] Fallback: InsTrack Scout...")
                await page.goto(f"https://instrack.app/instagram/{clean_handle}", timeout=30000)
                await page.wait_for_timeout(3000)
                content = await page.content()
                
                # Extract followers from InsTrack
                follower_match = re.search(r'Followers\s*</div>\s*<div[^>]*>([\d,]+)</div>', content, re.IGNORECASE)
                if follower_match:
                    results["followers"] = self.parse_count(follower_match.group(1))
                
                # Extract Email from content
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = re.findall(email_pattern, content)
                if emails: results["email"] = emails[0]
            except Exception as e:
                print(f"    [!] InsTrack Phase Failed: {str(e)[:40]}")

        # SOURCE 3: Google Dorking (Snippet Rescue)
        if results["email"] == "NOT_FOUND":
            try:
                print(f"    [>] Fallback: Google Dorking Snippet...")
                query = f"site:instagram.com/{clean_handle} \"@\""
                await page.goto(f"https://www.google.com/search?q={query}", timeout=30000)
                await page.wait_for_timeout(3000)
                snippets = await page.inner_text('body')
                
                # Parse Snippet for Email
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = re.findall(email_pattern, snippets)
                if emails: results["email"] = emails[0]
                
                # Parse Snippet for Followers
                follower_match = re.search(r'([\d.kmMK]+) Followers', snippets, re.IGNORECASE)
                if follower_match:
                    results["followers"] = self.parse_count(follower_match.group(1))
            except Exception as e:
                print(f"    [!] Google Phase Failed: {str(e)[:40]}")

        if results["email"] != "NOT_FOUND":
            results["status"] = "QUALIFIED"
            print(f"    [SUCCESS] {results['followers']} followers | Email: {results['email']}")
        else:
            print(f"    [RECON] Still missing email for @{clean_handle}")
        
        self.results[clean_handle] = results

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
            page = await context.new_page()

            for handle in self.targets:
                await self.extract_bio_data(page, handle)
                await asyncio.sleep(5) # Avoid IG rate limits

            with open(self.output_path, "w") as f:
                json.dump(self.results, f, indent=2)
            
            await browser.close()

if __name__ == "__main__":
    # Pulling unique handles from the 181 items
    import sys
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["@ai_guy_yt", "@marucaldera.planner"]
    scout = SovereignBioScout(targets)
    asyncio.run(scout.run())
