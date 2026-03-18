# main.py  —  SME Payroll Compliance Fix
# Cluster: LOCAL_SENTRY

import sys
import os
import csv
import glob

# Add root to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.core_sentry import LocalSentry

class PayrollSentry(LocalSentry):
    def __init__(self):
        super().__init__("SME_Payroll", "payroll_compliance.db")
        self.drop_zone = os.path.abspath(os.path.join(os.path.dirname(__file__), "../drop_zone"))
        os.makedirs(self.drop_zone, exist_ok=True)
        # Thresholds: Simple compliance rules
        self.MIN_WAGE = 10.0 # Example
        self.MAX_HOURS = 40.0 # Standard week before OT

    def audit_payroll_csv(self):
        """Monitor for new payroll reports and flag anomalies."""
        print(f" [PAYROLL] Monitoring {self.drop_zone} for new reports...")
        csv_files = glob.glob(os.path.join(self.drop_zone, "*.csv"))
        
        for file_path in csv_files:
            print(f" [PAYROLL] Auditing {os.path.basename(file_path)}...")
            try:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Rule 1: Hourly rate check
                        try:
                            rate = float(row.get('Hourly_Rate', 0))
                            hours = float(row.get('Hours_Worked', 0))
                            
                            if rate < self.MIN_WAGE:
                                self.log_event("COMPLIANCE_ALERT", f"Sub-minimum wage: {row['Employee_ID']} at {rate}", status="ALERT")
                            
                            if hours > self.MAX_HOURS and row.get('Overtime_Flag', 'N') == 'N':
                                self.log_event("COMPLIANCE_ALERT", f"Unflagged Overtime: {row['Employee_ID']} - {hours} hrs", status="ALERT")
                            
                            # Log valid entries as PROCESSED
                            self.log_event("PAYROLL_AUDIT", {"id": row['Employee_ID'], "status": "OK"})
                        except (ValueError, KeyError):
                            self.log_event("PARSE_ERROR", f"Invalid data in row: {row}", status="ERROR")
                
                # Move to archive
                archive_dir = os.path.join(self.drop_zone, "archive")
                os.makedirs(archive_dir, exist_ok=True)
                os.rename(file_path, os.path.join(archive_dir, os.path.basename(file_path)))
                
            except Exception as e:
                self.log_event("AUDIT_FAILED", {"file": file_path, "error": str(e)}, status="FAILED")

if __name__ == "__main__":
    sentry = PayrollSentry()
    sentry.run_check(sentry.audit_payroll_csv, interval=300)
