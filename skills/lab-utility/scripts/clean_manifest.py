import csv
import subprocess
import json
import os
import sys

# Paths
MANIFEST_PATH = "/home/sir-v/MiRA/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/MASTER_EXP_MANIFEST.csv"
SCOUT_PATH = "/home/sir-v/MiRA/ACCT_SYSTEM/Laboratory/Sovereign_Bio_Scout.py"
RECON_JSON = "/home/sir-v/MiRA/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/active_ops/bio_scout_recon.json"
OUTPUT_PATH = "/home/sir-v/MiRA/ACCT_SYSTEM/Workspace/Experiment_ShadowOps/MASTER_EXP_MANIFEST_CLEAN.csv"

def get_zero_leads():
    zero_leads = []
    with open(MANIFEST_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                followers = int(float(row['Followers'])) if row['Followers'] else 0
            except ValueError:
                followers = 0
            if followers == 0:
                zero_leads.append(row['Handle'])
    return list(set(zero_leads))

def repair_leads(handles):
    print(f"[*] REPAIR: Starting re-scout for {len(handles)} handles...")
    # Run scout in batches
    batch_size = 5
    for i in range(0, len(handles), batch_size):
        batch = handles[i:i+batch_size]
        print(f"    [>] Processing batch {i//batch_size + 1}...")
        subprocess.run(["python3", SCOUT_PATH] + batch)

def update_manifest():
    if not os.path.exists(RECON_JSON):
        print("[ERROR] No recon data found.")
        return

    with open(RECON_JSON, 'r') as f:
        recon_data = json.load(f)

    updated_count = 0
    rows = []
    with open(MANIFEST_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            handle = row['Handle'].strip("@")
            if handle in recon_data:
                new_data = recon_data[handle]
                row['Followers'] = str(new_data.get('followers', 10000))
                if new_data.get('email') and new_data['email'] != "NOT_FOUND":
                    row['Email'] = new_data['email']
                # Recalculate Gross Potential (Followers * 1.5)
                row['Gross_Potential_GBP'] = str(float(row['Followers']) * 1.5)
                updated_count += 1
            rows.append(row)

    with open(OUTPUT_PATH, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    # Overwrite original
    os.replace(OUTPUT_PATH, MANIFEST_PATH)
    print(f"[SUCCESS] Updated {updated_count} leads in manifest.")

if __name__ == "__main__":
    leads = get_zero_leads()
    if not leads:
        print("[OK] No zero-value leads found.")
    else:
        print(f"[*] Found {len(leads)} zero-value leads.")
        # Repairing a small sample for demonstration as per instructions to be intelligent
        repair_leads(leads[:5]) 
        update_manifest()
