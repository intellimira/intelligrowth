# main.py  —  Contract Clause Interrogator
# Cluster: LOCAL_SENTRY

import sys
import os
import glob

# Add root to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.core_sentry import LocalSentry

class LegalInterrogator(LocalSentry):
    def __init__(self):
        super().__init__("Contract_Interrogator", "legal_audit.db")
        self.drop_zone = os.path.abspath(os.path.join(os.path.dirname(__file__), "../drop_zone"))
        os.makedirs(self.drop_zone, exist_ok=True)
        # Risk keywords
        self.RED_FLAGS = ["unlimited liability", "automatic renewal", "non-compete", "indemnity"]

    def interrogate_contracts(self):
        """Scan dropped text files for risky legal clauses."""
        print(f" [LEGAL] Interrogating {self.drop_zone} for new contracts...")
        txt_files = glob.glob(os.path.join(self.drop_zone, "*.txt"))
        
        for file_path in txt_files:
            print(f" [LEGAL] Scanning {os.path.basename(file_path)}...")
            try:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    content = f.read().lower()
                    found_flags = [flag for flag in self.RED_FLAGS if flag in content]
                    
                    if found_flags:
                        self.log_event("RISK_DETECTED", {"file": os.path.basename(file_path), "flags": found_flags}, status="WARNING")
                    else:
                        self.log_event("LEGAL_SCAN_CLEAN", {"file": os.path.basename(file_path)})
                
                # Move to archive
                archive_dir = os.path.join(self.drop_zone, "archive")
                os.makedirs(archive_dir, exist_ok=True)
                os.rename(file_path, os.path.join(archive_dir, os.path.basename(file_path)))
                
            except Exception as e:
                self.log_event("SCAN_FAILED", {"file": file_path, "error": str(e)}, status="FAILED")

if __name__ == "__main__":
    interrogator = LegalInterrogator()
    interrogator.run_check(interrogator.interrogate_contracts, interval=60)
