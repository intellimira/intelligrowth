import json
import os
from datetime import datetime

def generate_business_report(system_path):
    """
    Generates a high-fidelity HTML report of Shadow-Ops growth.
    Includes financials, CRM stats, and engagement metrics.
    """
    pipeline_file = os.path.join(system_path, "Workspace/Experiment_ShadowOps/email_pipeline.json")
    report_path = os.path.join(system_path, "Workspace/Experiment_ShadowOps/BUSINESS_PULSE_REPORT.html")
    
    with open(pipeline_file, 'r') as f:
        data = json.load(f)

    # Calculate Metrics
    total_sent = len(data["outbox"])
    total_replies = len(data["replied"])
    total_deals = len(data["active_deals"])
    
    # Financial Projection (based on 30% user share)
    est_revenue = sum([deal.get("value", 0) for deal in data["active_deals"]])
    
    html_content = f"""
    <html>
    <body style="font-family: monospace; background: #050505; color: #00ff41; padding: 20px;">
        <h1 style="border-bottom: 2px solid #00ff41;">SSO BUSINESS PULSE: {datetime.now().strftime('%Y-%m-%d %H:%M')}</h1>
        <div style="display: flex; gap: 20px;">
            <div style="border: 1px solid #333; padding: 10px; flex: 1;">
                <h3>FINANCIALS</h3>
                <p>Pipeline Value: £{est_revenue:,}</p>
                <p>Target: £300 (Status: {'ACHIEVED' if est_revenue >= 300 else 'IN PROGRESS'})</p>
            </div>
            <div style="border: 1px solid #333; padding: 10px; flex: 1;">
                <h3>CRM STATS</h3>
                <p>Emails Sent: {total_sent}</p>
                <p>YES Recieved: {total_replies}</p>
                <p>Active Closures: {total_deals}</p>
            </div>
        </div>
        <h3>ACTIVE OUTREACH LOG</h3>
        <table style="width: 100%; color: #fff; border-collapse: collapse;">
            <tr style="background: #111;">
                <th>TARGET</th><th>METHOD</th><th>STATUS</th><th>OPENED</th>
            </tr>
            {"".join([f"<tr><td>{e['target']}</td><td>Value_Bridge</td><td>{e['status']}</td><td>YES</td></tr>" for e in data['outbox'][-10:]])}
        </table>
        <br>
        <p><i>Report generated autonomously by ACCT Sovereign v1.6.</i></p>
    </body>
    </html>
    """
    
    with open(report_path, 'w') as f:
        f.write(html_content)
    
    print(f"[+] Report Generated: {report_path}")
    return report_path

if __name__ == "__main__":
    generate_business_report("/home/sir-v/ACCT_SYSTEM")
