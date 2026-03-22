#!/usr/bin/env python3
"""
MIRA Email Enquiry Processor
Polls Gmail for website enquiries, parses them, and saves to enquiries repo.
"""

import imaplib
import email
from email.header import decode_header
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Import secure config
from mira_config import get_gmail_password, get_enquiries_repo

# Configuration
GMAIL_USER = "intellimira@gmail.com"
ENQUIRIES_REPO = get_enquiries_repo()
INTEREST_KEYWORDS = {
    "collaboration": ["COLLABORATION", "collab"],
    "consulting": ["CONSULTING"],
    "newsletter": ["NEWSLETTER", "newsletter", "updates"],
    "shadow-ops": ["SHADOW-OPS", "shadow-ops", "inquiry"],
    "just-browsing": ["JUST-BROWSING"],
}

def decode_email_header(header):
    """Decode email header properly"""
    if header is None:
        return ""
    decoded_parts = []
    try:
        parts = decode_header(header)
        for content, charset in parts:
            if isinstance(content, bytes):
                charset = charset or 'utf-8'
                try:
                    decoded_parts.append(content.decode(charset, errors='replace'))
                except:
                    decoded_parts.append(content.decode('utf-8', errors='replace'))
            else:
                decoded_parts.append(content)
    except:
        return str(header)
    return ' '.join(decoded_parts)

def extract_enquiry_type(subject):
    """Extract enquiry type from email subject"""
    subject_upper = subject.upper()
    for interest, keywords in INTEREST_KEYWORDS.items():
        for kw in keywords:
            if kw.upper() in subject_upper:
                return interest
    return "other"

def parse_email_body(msg):
    """Extract relevant info from email body"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
        except:
            pass
    return body

def extract_fields_from_email(body):
    """Extract name, email, company, message from email body"""
    lines = body.split('\n')
    fields = {
        "name": None,
        "email": None,
        "company": None,
        "message": None
    }
    
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower.startswith("name:"):
            fields["name"] = line.split(":", 1)[1].strip()
        elif line_lower.startswith("email:"):
            fields["email"] = line.split(":", 1)[1].strip()
        elif line_lower.startswith("company:"):
            fields["company"] = line.split(":", 1)[1].strip()
        elif line_lower.startswith("message:") or line_lower.startswith("message -"):
            fields["message"] = line.split(":", 1)[1].strip() if ":" in line else ""
        elif line_lower.startswith("interest:") or line_lower.startswith("i'm interested in"):
            pass  # Interest extracted from subject
    
    return fields

def connect_gmail():
    """Connect to Gmail via IMAP"""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        
        # Get password from secure config
        password = get_gmail_password()
        if password:
            mail.login(GMAIL_USER, password)
        else:
            # Try OAuth2 token from himalaya as fallback
            token_file = os.path.expanduser("~/.config/himalaya/token")
            if os.path.exists(token_file):
                with open(token_file) as f:
                    token = f.read().strip()
                mail.authenticate('XOAUTH2', lambda x: f'user={GMAIL_USER}\1auth=Bearer {token}\1\1'.encode())
            else:
                print("⚠️ No Gmail password configured.")
                print("   Set HIMALAYA_PASSWORD in ~/.env/mira_config")
                print("   Or generate an App Password from: https://myaccount.google.com/apppasswords")
                return None
        return mail
    except Exception as e:
        print(f"Error connecting to Gmail: {e}")
        return None

def poll_for_enquiries():
    """Poll Gmail for new enquiries"""
    mail = connect_gmail()
    if mail is None:
        print("Cannot connect to Gmail. Run setup first.")
        return []
    
    try:
        mail.select('"[Gmail]/All Mail"')
        
        # Search for enquiry emails (last 7 days, from not myself)
        status, messages = mail.search(None, 
            'SINCE', datetime.now().strftime("%d-%b-%Y"),
            'FROM', '@gmail.com',  # Exclude our own emails
            'SUBJECT', '[,]'  # Emails with [CATEGORY] in subject
        )
        
        if status != 'OK':
            return []
        
        enquiry_ids = messages[0].split()
        enquiries = []
        
        for msg_id in enquiry_ids[-50:]:  # Last 50 emails
            try:
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                if status != 'OK':
                    continue
                    
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                subject = decode_email_header(msg['Subject'])
                sender = decode_email_header(msg['From'])
                date = msg['Date']
                
                # Check if it's an enquiry
                interest = extract_enquiry_type(subject)
                if interest != "other":  # Valid enquiry
                    body = parse_email_body(msg)
                    fields = extract_fields_from_email(body)
                    
                    enquiry = {
                        "id": f"enquiry_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "timestamp": date,
                        "name": fields.get("name") or sender.split('@')[0],
                        "email": fields.get("email") or sender,
                        "company": fields.get("company") or "N/A",
                        "interest": interest,
                        "message": fields.get("message") or body[:500],
                        "subject": subject,
                        "status": "new",
                        "pain_score": None
                    }
                    enquiries.append(enquiry)
                    
            except Exception as e:
                print(f"Error parsing email {msg_id}: {e}")
                continue
        
        return enquiries
        
    except Exception as e:
        print(f"Error polling Gmail: {e}")
        return []
    finally:
        try:
            mail.logout()
        except:
            pass

def save_enquiries(enquiries):
    """Save enquiries to local repo clone"""
    if not enquiries:
        print("No new enquiries found.")
        return
    
    repo_path = Path(ENQUIRIES_REPO)
    if not repo_path.exists():
        print(f"Repo not found at {repo_path}. Cloning...")
        os.system(f"git clone https://github.com/intellimira/enquiries.git {repo_path}")
    
    saved_count = 0
    for enquiry in enquiries:
        # Determine folder based on interest
        folder_map = {
            "collaboration": "prospects",
            "consulting": "prospects",
            "newsletter": "newsletter",
            "shadow-ops": "outreach",
            "just-browsing": "prospects",
            "other": "prospects"
        }
        folder = folder_map.get(enquiry["interest"], "prospects")
        
        # Save as JSON
        filename = f"{enquiry['id']}_{enquiry['email'].split('@')[0]}.json"
        filepath = repo_path / folder / filename
        
        with open(filepath, 'w') as f:
            json.dump(enquiry, f, indent=2)
        
        saved_count += 1
        print(f"Saved: {filepath}")
    
    # Update leads database
    db_file = repo_path / "leads.db.json"
    leads = []
    if db_file.exists():
        with open(db_file) as f:
            leads = json.load(f)
    
    # Add new leads
    existing_emails = {l["email"] for l in leads}
    for eq in enquiries:
        if eq["email"] not in existing_emails:
            leads.append({
                "id": eq["id"],
                "email": eq["email"],
                "name": eq["name"],
                "interest": eq["interest"],
                "status": "new",
                "added": datetime.now().isoformat()
            })
    
    with open(db_file, 'w') as f:
        json.dump(leads, f, indent=2)
    
    print(f"\n✅ Saved {saved_count} enquiries. Total leads: {len(leads)}")
    
    # Push to GitHub
    os.system(f"cd {repo_path} && git add -A && git commit -m 'Auto: New enquiries {datetime.now().strftime(\"%Y-%m-%d %H:%M\")}' && git push origin main 2>/dev/null")

if __name__ == "__main__":
    print("🔍 MIRA Email Enquiry Processor")
    print("=" * 40)
    enquiries = poll_for_enquiries()
    save_enquiries(enquiries)
