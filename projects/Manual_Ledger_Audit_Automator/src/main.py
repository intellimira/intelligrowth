# main.py  —  Manual Ledger Audit Automator
# Cluster: LOCAL_SENTRY

import sys
import os
import csv
import glob

# Add root to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.core_sentry import LocalSentry

class LedgerAutomator(LocalSentry):
    def __init__(self):
        super().__init__("Ledger_Automator", "ledger_audit.db")
        self.drop_zone = os.path.abspath(os.path.join(os.path.dirname(__file__), "../drop_zone"))
        os.makedirs(self.drop_zone, exist_ok=True)

    def audit_new_transactions(self):
        """Monitor bank CSV folder for new drops and perform basic validation."""
        print(f" [LEDGER] Monitoring {self.drop_zone} for new CSV ledger drops...")
        csv_files = glob.glob(os.path.join(self.drop_zone, "*.csv"))
        
        for file_path in csv_files:
            print(f" [LEDGER] Auditing {os.path.basename(file_path)}...")
            try:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    total_balance = 0.0
                    for row in reader:
                        amount = float(row.get('Amount', 0.0))
                        total_balance += amount
                        
                        # Anomaly: Duplicate detection (simulated)
                        self.log_event("TRANSACTION_CHECK", {"id": row.get('ID'), "amount": amount})
                
                if total_balance != 0.0:
                    self.log_event("AUDIT_ALERT", f"Ledger Out of Balance: {total_balance}", status="WARNING")
                else:
                    self.log_event("AUDIT_SUCCESS", "Ledger Balanced.")
                
                # Move to archive
                archive_dir = os.path.join(self.drop_zone, "archive")
                os.makedirs(archive_dir, exist_ok=True)
                os.rename(file_path, os.path.join(archive_dir, os.path.basename(file_path)))
                
            except Exception as e:
                self.log_event("AUDIT_FAILED", {"file": file_path, "error": str(e)}, status="FAILED")

if __name__ == "__main__":
    automator = LedgerAutomator()
    automator.run_check(automator.audit_new_transactions, interval=300)
