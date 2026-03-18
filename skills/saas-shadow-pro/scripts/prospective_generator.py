import os
import json
from datetime import datetime

class ProspectiveGenerator:
    """
    Generates professional engagement prospectives for SaaS Shadow arm.
    Includes Plans, Costs, Instructions, and Legal docs for specific proven solutions.
    """
    def __init__(self, output_dir=".brain/outputs/saas_pro_workspaces"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.solutions = {
            "HMRC SlipStream": {
                "fixed_price": None,
                "rev_share": "70/30",
                "plan": [
                    "Phase 1: Discovery & RTI API Audit (Day 1-2)",
                    "Phase 2: SlipStream Bridge Integration (Day 3-5)",
                    "Phase 3: NMW Risk Stress Testing (Day 6-7)",
                    "Phase 4: Sovereign Deployment (Day 8+)"
                ]
            },
            "NMIP (LeadCatch)": {
                "fixed_price": "$540",
                "rev_share": None,
                "plan": [
                    "M1: Twilio Setup & Number Acquisition (Day 1-2)",
                    "M2: Recovery Logic & Validation Tests (Day 3-5)",
                    "M3: Handover & Operational Admin Guide (Day 6-7)"
                ]
            },
            "SBOD (SmartBridge)": {
                "fixed_price": "Custom / Quote",
                "rev_share": "70/30 or Flat",
                "plan": [
                    "Phase 1: SmartBill Webhook Mapping (Day 1-2)",
                    "Phase 2: Headless Engine Logic Deployment (Day 3-5)",
                    "Phase 3: Odoo Schema Enforcement Validation (Day 6-7)",
                    "Phase 4: Sync Log Initialization (Day 8)"
                ]
            }
        }

    def generate_prospective(self, client_handle, pain_point, solution_name):
        safe_handle = client_handle.replace('@', '').replace('.', '_')
        client_dir = os.path.join(self.output_dir, safe_handle)
        os.makedirs(client_dir, exist_ok=True)

        solution_data = self.solutions.get(solution_name, {
            "fixed_price": "Quote",
            "rev_share": "70/30",
            "plan": ["Phase 1: Discovery", "Phase 2: Build", "Phase 3: Deliver"]
        })

        package = {
            "metadata": {
                "client": client_handle,
                "pain_point": pain_point,
                "solution": solution_name,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "DRAFT"
            },
            "strategic_plan": solution_data["plan"],
            "cost_model": self._generate_costs(solution_data),
            "instructions": self._generate_instructions(solution_name),
            "legal_framework": self._generate_legal()
        }

        with open(os.path.join(client_dir, "engagement_prospective.json"), 'w') as f:
            json.dump(package, f, indent=2)
        
        self._generate_html_report(client_dir, package)
        return client_dir

    def _generate_costs(self, solution_data):
        return {
            "setup_fee": solution_data["fixed_price"] if solution_data["fixed_price"] else "£0 (Sovereign Partner Model)",
            "revenue_share": solution_data["rev_share"] if solution_data["rev_share"] else "N/A (Fixed Price)",
            "maintenance": "Included in agreement",
            "exit_clause": "30-day notice, client keeps all data"
        }

    def _generate_instructions(self, solution):
        return [
            f"1. Connect your primary data source to the {solution} Interface.",
            "2. Authorize the 'Shadow Node' for automated task processing.",
            "3. Review the daily 'Sovereign Pulse' logs for procedural transparency."
        ]

    def _generate_legal(self):
        return "Standard Sovereign Partnership Agreement v1.2 (Confidentiality & Data Sovereignty focused)."

    def _generate_html_report(self, client_dir, package):
        html_path = os.path.join(client_dir, "prospective_report.html")
        # Simplified for demonstration
        with open(html_path, 'w') as f:
            f.write(f"<h1>Engagement Prospective: {package['metadata']['solution']}</h1>")
            f.write(f"<p>Prepared for {package['metadata']['client']}</p>")
            f.write("<h2>Strategic Plan</h2><ul>" + "".join(f"<li>{item}</li>" for item in package['strategic_plan']) + "</ul>")
            f.write(f"<h2>Cost Model</h2><p>Setup: {package['cost_model']['setup_fee']} | Share: {package['cost_model']['revenue_share']}</p>")
        print(f"[+] HTML Prospective generated: {html_path}")

if __name__ == "__main__":
    generator = ProspectiveGenerator()
    # Testing the new modules
    generator.generate_prospective("@lead_gen_corp", "Lost inbound calls", "NMIP (LeadCatch)")
    generator.generate_prospective("@retail_odoo_user", "Manual SmartBill entry", "SBOD (SmartBridge)")
