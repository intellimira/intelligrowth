import os
import json
import re

def clean_agent_output(content):
    """Deep cleaning of agent text to remove dictionary artifacts."""
    text = str(content)
    # Remove leading/trailing braces and quotes if it's a pseudo-dict string
    text = re.sub(r"^[{\s']+", "", text)
    text = re.sub(r"[}\s']+$", "", text)
    # Remove common dict keys that leak into text
    keys_to_strip = [
        "LinkedIn DM", "Business Email", "Subject", "Note", 
        "Here is the draft", "I invite you to", "Diagnostic link"
    ]
    for key in keys_to_strip:
        text = re.sub(f"['\"]?{key}['\"]?:\s*['\"]?", "", text, flags=re.IGNORECASE)
    
    # Remove escaped newlines and other artifacts
    text = text.replace("\\n", "\n").replace("\\'", "'").replace('\"', '"')
    return text.strip()

def format_as_executive_pack(name, raw_content):
    """Wraps cleaned content in a professional executive template."""
    clean_text = clean_agent_output(raw_content)
    
    solution_name = name.replace("_", " ").replace(".md", "").replace("outreach ", "")
    
    md = f"""# EXECUTIVE OUTREACH: {solution_name.upper()}

---

## 🔵 LINKEDIN COMMAND (DM)
> *Strategy: Concise, high-intent discovery.*

{clean_text.split('Business Email')[0].strip() if 'Business Email' in clean_text else clean_text}

---

## 📧 BUSINESS EMAIL COMMAND
> *Strategy: Detailed problem-solution gap analysis.*

{clean_text.split('Business Email')[-1].strip() if 'Business Email' in clean_text else "Pending generation..."}

---

## ⚡️ THE TRUTH SERUM GATE
**Diagnostic Invite:** `[Self-Service Workflow Diagnostic: {solution_name}]`
**Action:** Authorized for "Design Partner" validation.
"""
    return md

def save_outreach(name, content):
    os.makedirs(".brain/outputs/outreach_packages", exist_ok=True)
    path = f".brain/outputs/outreach_packages/outreach_{name}"
    
    final_md = format_as_executive_pack(name, content)
    
    with open(path, 'w') as f:
        f.write(final_md)
        
    print(f" [S-RANK] Executive Pack Sealed: {path}")
    return path

if __name__ == "__main__":
    # Logic to loop through existing client_packages and re-generate
    import glob
    packs = glob.glob(".brain/outputs/client_packages/*.md")
    
    print("\n--- SHADOW OPERATOR: EXECUTIVE OVERHAUL ---")
    for p in packs:
        name = os.path.basename(p)
        with open(p, 'r') as f:
            content = f.read()
        # For the overhaul, we use the existing detailed pack to ensure informative scripts
        save_outreach(name, content)
    print("\n--- OVERHAUL COMPLETE ---")
