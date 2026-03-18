import json
import os
from datetime import datetime

class SlipStreamAudit:
    """
    SaaS Shadow Logic: HMRC Payroll & NMW Compliance Auditor.
    Detects potential breaches in hours reporting and pay compression.
    """
    def __init__(self, output_dir=".brain/outputs/saas_pro_workspaces/audits"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.nmw_rate_2026 = 12.71 # National Living Wage (21+)

    def run_audit(self, payroll_data):
        """
        Analyzes payroll records for compliance risks.
        """
        results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "risk_score": 0,
            "findings": []
        }

        total_employees = len(payroll_data)
        breaches = 0

        for emp in payroll_data:
            # Check for NMW breach
            effective_rate = emp['gross_pay'] / emp['hours_worked']
            if effective_rate < self.nmw_rate_2026:
                findings = {
                    "employee_id": emp['id'],
                    "issue": "NMW_BREACH",
                    "effective_rate": round(effective_rate, 2),
                    "required_rate": self.nmw_rate_2026,
                    "delta": round(self.nmw_rate_2026 - effective_rate, 2)
                }
                results['findings'].append(findings)
                breaches += 1

            # Check for "Exact Hours" reporting anomaly
            if emp['hours_worked'] % 1 == 0: # Suspiciously round numbers
                results['findings'].append({
                    "employee_id": emp['id'],
                    "issue": "ROUNDED_HOURS_RISK",
                    "details": "Hours appear estimated (rounded). HMRC 2026 requires exact time-tracking."
                })

        # Calculate Risk Score (0-100)
        results['risk_score'] = int((breaches / total_employees) * 100) if total_employees > 0 else 0
        
        # Save audit report
        audit_id = f"AUDIT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(os.path.join(self.output_dir, audit_id), 'w') as f:
            json.dump(results, f, indent=2)
        
        return results

if __name__ == "__main__":
    # Sample data for testing the SaaS arm logic
    test_data = [
        {"id": "EMP001", "gross_pay": 500, "hours_worked": 40},  # Rate: 12.50 (BREACH)
        {"id": "EMP002", "gross_pay": 600, "hours_worked": 42.5},# Rate: 14.11 (OK)
        {"id": "EMP003", "gross_pay": 450, "hours_worked": 37},  # Rate: 12.16 (BREACH)
        {"id": "EMP004", "gross_pay": 550, "hours_worked": 40},  # Rate: 13.75 (OK, but rounded hours)
    ]
    auditor = SlipStreamAudit()
    report = auditor.run_audit(test_data)
    print(f"[+] SlipStream Audit Complete. Risk Score: {report['risk_score']}")
    print(f"[+] Total Findings: {len(report['findings'])}")
