import os
import time
import glob

PACKS_DIR = ".brain/outputs/client_packages/"
os.makedirs(PACKS_DIR, exist_ok=True)

print(f"\n--- SOVEREIGN MONITOR: ACTIVE ---")
print(f"Watching for new Business Packs in: {PACKS_DIR}")

known_files = set(glob.glob(os.path.join(PACKS_DIR, "*.md")))

try:
    while True:
        current_files = set(glob.glob(os.path.join(PACKS_DIR, "*.md")))
        new_files = current_files - known_files
        
        for file_path in new_files:
            filename = os.path.basename(file_path)
            print(f"\n[!] ALERT: NEW BUSINESS PACK IDENTIFIED")
            print(f" > Location: {file_path}")
            
            # Check for "Quick Win" markers in the content
            try:
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                    if "quick win" in content or "platform arbitrage" in content or "unbundling" in content:
                        print(f" [!!!] PRIORITY ALERT: 'QUICK WIN' DETECTED in {filename}")
                        print(f" > Recommendation: Interrogate this asset immediately.")
            except: pass
            
            known_files.add(file_path)
            
        time.sleep(5)
except KeyboardInterrupt:
    print("\nMonitor stopped.")
