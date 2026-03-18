import os, json, re

def seal_hardened_outreach(name, problem, solution, tech_path, icp):
    solution_name = name.replace("_", " ").upper()
    path = f".brain/outputs/outreach_packages/outreach_{name}.md"
    
    md = f"""# EXECUTIVE OUTREACH COMMAND: {solution_name}

---

## 🔵 LINKEDIN COMMAND (DM)
> *Strategy: Cognitive Reframing / High-Intent*

"Hi [Recipient], I noticed your work at {icp}. I've been interrogating the energy cost of {problem} and built a local-first 'Shadow Script' that solves this for zero cost using {tech_path}.

I'm looking for a Design Partner to vet the logic. Open to seeing the 3-field diagnostic?"

---

## 📧 BUSINESS EMAIL COMMAND
**Subject:** Eliminating {solution_name} Friction

"Dear [Recipient],

Our Sovereign Audit of the {icp} sector identified a recurring 'Ugly Glue' friction point: {problem}.

We have engineered a surgical cure: {solution}. 

**The HOW (Technical Path):**
{tech_path}

This solution runs locally on your edge—meaning zero data leakage and zero subscription fatigue. I've attached a self-service diagnostic to quantify your cost of inaction.

Would you be open to a diagnostic review?"

---

## ⚡️ TRUTH SERUM GATE
**Diagnostic Invite:** `[Self-Service Workflow Diagnostic: {solution_name}]`
**Action:** Authorized for Sovereign Interrogation.
"""
    os.makedirs(".brain/outputs/outreach_packages", exist_ok=True)
    with open(path, 'w') as f:
        f.write(md)
    print(f" [OUTREACH HARDENED] {path}")

# Load all grounded assets
import glob
packs = glob.glob(".brain/outputs/client_packages/*.md")

print("\n--- SHADOW OPERATOR: UNIVERSAL OUTREACH HARDENING ---")
for p in packs:
    name = os.path.basename(p).replace(".md", "")
    with open(p, 'r') as f:
        content = f.read()
    
    # Simple extraction for the hardening script
    problem = re.search(r"ANALYSED PROBLEM STATEMENT.*?\n(.*?)\n", content, re.DOTALL)
    solution = re.search(r"THE STRATEGIC CURE.*?\n(.*?)\n", content, re.DOTALL)
    tech_path = re.search(r"TECHNICAL ACHIEVEMENT PATH.*?\n(.*?)\n", content, re.DOTALL)
    icp = re.search(r"### 🎯 ICP.*?\n(.*?)\n", content, re.DOTALL)
    
    seal_hardened_outreach(
        name, 
        problem.group(1) if problem else "Market tension", 
        solution.group(1) if solution else "Sovereign unbundling", 
        tech_path.group(1) if tech_path else "Local-first logic", 
        icp.group(1) if icp else "Industry stakeholders"
    )
