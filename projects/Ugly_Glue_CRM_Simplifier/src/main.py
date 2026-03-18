# main.py  —  Ugly Glue CRM Simplifier
# Cluster: LOCAL_SENTRY

import sys
import os
import csv
import glob

# Add root to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.core_sentry import LocalSentry

class UglyGlueSentry(LocalSentry):
    def __init__(self):
        super().__init__("UglyGlue_CRM", "crm_glue.db")
        self.drop_zone = os.path.abspath(os.path.join(os.path.dirname(__file__), "../drop_zone"))
        os.makedirs(self.drop_zone, exist_ok=True)

    def process_csv_drops(self):
        """Monitor drop_zone for new CRM CSV exports."""
        print(f" [GLUE] Monitoring {self.drop_zone} for CSV drops...")
        csv_files = glob.glob(os.path.join(self.drop_zone, "*.csv"))
        
        for file_path in csv_files:
            print(f" [GLUE] Processing {os.path.basename(file_path)}...")
            try:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Simulated glue logic: Map 'Lead Name' to 'Customer'
                        self.log_event("CRM_SYNC", row)
                
                # Move processed file to an 'archive' folder
                archive_dir = os.path.join(self.drop_zone, "archive")
                os.makedirs(archive_dir, exist_ok=True)
                os.rename(file_path, os.path.join(archive_dir, os.path.basename(file_path)))
                print(f" [GLUE] Successfully synced and archived {os.path.basename(file_path)}")
            except Exception as e:
                self.log_event("SYNC_ERROR", {"file": file_path, "error": str(e)}, status="FAILED")

if __name__ == "__main__":
    glue = UglyGlueSentry()
    glue.run_check(glue.process_csv_drops, interval=60)
