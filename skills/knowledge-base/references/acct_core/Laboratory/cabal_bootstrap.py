import os
import subprocess
import re

def activate_cabal_context():
    """
    Proactively loads the unified protocol mesh into the active reasoning stream.
    Used by the ACCT Cabal during problem-solving.
    """
    hub_path = "/home/sir-v/ACCT_CORE/Memory_Mesh/Protocols/ACCT_PROTOCOL_HUB.md"
    active_recall_script = "/home/sir-v/ACCT_CORE/Laboratory/Active_Recall/prototypes/active_recall.py"
    
    print("\n--- ACCT CABAL: PROTOCOL SYNCHRONIZATION ---")
    
    # 1. Read the Hub to identify the core mesh
    if os.path.exists(hub_path):
        print("[*] Accessing ACCT_PROTOCOL_HUB...")
        try:
            with open(hub_path, 'r') as f:
                hub_content = f.read()
                # Extract links to other protocols
                links = re.findall(r'\[\[(.*?)\]\]', hub_content)
                print(f"[*] Core Mesh Identified: {', '.join(links)}")
        except Exception as e:
            print(f"[!] Error reading Hub: {e}")
    
    # 2. Trigger Active Recall for current operational state
    print("[*] Initializing Active Recall Pulse...")
    try:
        subprocess.run(["python3", active_recall_script, "protocol", "core", "axiom"])
    except Exception as e:
        print(f"[!] Error during Active Recall Pulse: {e}")

    print("\n--- ACCT Cabal is now grounded in Unified Protocols. ---")

if __name__ == "__main__":
    activate_cabal_context()
