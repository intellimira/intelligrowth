import os
import json
from datetime import datetime

def generate_delivery_package(client_data):
    """
    Generates a professional delivery package for a client.
    """
    package_dir = ".brain/outputs/client_packages"
    os.makedirs(package_dir, exist_ok=True)
    
    client_handle = client_data['handle'].replace('@', '').replace('.', '_')
    file_path = os.path.join(package_dir, f"delivery_package_{client_handle}.html")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sovereign Delivery: {client_data['handle']}</title>
        <style>
            body {{ background: #0a0a0a; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; line-height: 1.6; }}
            .container {{ max-width: 800px; margin: 0 auto; background: #141414; padding: 40px; border: 1px solid #333; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            .header {{ border-bottom: 2px solid #c8922a; padding-bottom: 20px; margin-bottom: 30px; text-align: center; }}
            .header h1 {{ color: #c8922a; margin: 0; letter-spacing: 2px; text-transform: uppercase; font-size: 24px; }}
            .client-info {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; background: #1a1a1a; padding: 20px; border-radius: 4px; }}
            .info-item {{ font-size: 14px; }}
            .info-label {{ color: #888; text-transform: uppercase; font-size: 10px; letter-spacing: 1px; margin-bottom: 5px; }}
            .info-val {{ font-weight: bold; color: #f0c060; }}
            .section {{ margin-bottom: 30px; }}
            .section h2 {{ color: #c8922a; font-size: 18px; border-left: 4px solid #c8922a; padding-left: 15px; margin-bottom: 15px; }}
            .link-box {{ background: #0a0a0a; border: 1px dashed #c8922a; padding: 15px; text-align: center; margin-top: 10px; border-radius: 4px; }}
            .link-box a {{ color: #f0c060; text-decoration: none; font-weight: bold; word-break: break-all; }}
            .link-box a:hover {{ text-decoration: underline; }}
            .footer {{ margin-top: 50px; text-align: center; font-size: 12px; color: #555; border-top: 1px solid #333; padding-top: 20px; }}
            .status-badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; text-transform: uppercase; }}
            .status-delivered {{ background: rgba(78, 207, 106, 0.15); color: #4ecf6a; border: 1px solid #4ecf6a; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Monetization Delivery Package</h1>
                <p style="color: #888;">Prepared by: Sovereign Operator (intellimira@gmail.com)</p>
            </div>
            
            <div class="client-info">
                <div class="info-item">
                    <div class="info-label">Client Operative</div>
                    <div class="info-val">{client_data['handle']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Sector / Niche</div>
                    <div class="info-val">{client_data['niche']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Delivery Date</div>
                    <div class="info-val">{datetime.now().strftime('%Y-%m-%d')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Fidelity Status</div>
                    <div class="status-badge status-delivered">S-Rank Delivered</div>
                </div>
            </div>

            <div class="section">
                <h2>1. Professional Engagement Portal (NotebookLM)</h2>
                <p>Access your dedicated AI-powered workbook for project deep-dives, strategic queries, and real-time coaching.</p>
                <div class="link-box">
                    <a href="{client_data['notebook_url']}">{client_data['notebook_url']}</a>
                </div>
            </div>

            <div class="section">
                <h2>2. Solution Retrieval & Assets (Google Drive)</h2>
                <p>Retrieve all produced blueprints, HTML gameplans, and high-fidelity assets from your secure client folder.</p>
                <div class="link-box">
                    <a href="{client_data['doc_link']}">{client_data['doc_link']}</a>
                </div>
            </div>

            <div class="section">
                <h2>3. Correspondence & Communication</h2>
                <p>All project-related logs and email threads are archived here for business continuity and audit transparency.</p>
                <p style="font-size: 13px; color: #888;">Note: Use your primary business email to interact with these documents.</p>
            </div>

            <div class="footer">
                <p>Sovereign Intelligence Mesh | The Weave v4.0</p>
                <p>&copy; 2026 IntelliMira Shadow Operations</p>
            </div>
        </div>
    </body>
    </html>
    """
    with open(file_path, 'w') as f:
        f.write(html)
    return file_path

if __name__ == "__main__":
    clients = [
        {
            "handle": "@ninjaaitools",
            "niche": "AI Macro",
            "notebook_url": "https://notebooklm.google.com/notebook/77e5f886-155e-42d9-86c3-805dc3edda15",
            "doc_link": "https://docs.google.com/document/d/CLIENT_NINJAAITOOLS_LINK/edit"
        },
        {
            "handle": "@officially.val",
            "niche": "Lifestyle",
            "notebook_url": "https://notebooklm.google.com/notebook/OFFICIALLY_VAL_LINK",
            "doc_link": "https://docs.google.com/document/d/CLIENT_OFFICIALLYVAL_LINK/edit"
        },
        {
            "handle": "@ai_guy_yt",
            "niche": "AI Tech",
            "notebook_url": "https://notebooklm.google.com/notebook/AI_GUY_YT_LINK",
            "doc_link": "https://docs.google.com/document/d/CLIENT_AIGUY_LINK/edit"
        },
        {
            "handle": "@marucaldera.planner",
            "niche": "Productivity",
            "notebook_url": "https://notebooklm.google.com/notebook/MARUCALDERA_LINK",
            "doc_link": "https://docs.google.com/document/d/CLIENT_MARUCALDERA_LINK/edit"
        },
        {
            "handle": "@nataliefischer.finance",
            "niche": "Finance",
            "notebook_url": "https://notebooklm.google.com/notebook/NATALIEFISCHER_LINK",
            "doc_link": "https://docs.google.com/document/d/CLIENT_NATALIEFISCHER_LINK/edit"
        },
        {
            "handle": "@thenotionbar",
            "niche": "Notion",
            "notebook_url": "https://notebooklm.google.com/notebook/THENOTIONBAR_LINK",
            "doc_link": "https://docs.google.com/document/d/CLIENT_THENOTIONBAR_LINK/edit"
        }
    ]
    
    for client in clients:
        path = generate_delivery_package(client)
        print(f"[+] Package generated for {client['handle']}: {path}")
