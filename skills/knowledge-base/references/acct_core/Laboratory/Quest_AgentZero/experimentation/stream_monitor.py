import re
import time

class ACCTStreamMonitor:
    """
    Simulates real-time stream monitoring (Intuition Layer).
    Checks tokens as they are 'generated' and triggers Nodal Interventions.
    """
    def __init__(self):
        # Define hurdles and the node that handles them
        self.hurdles = {
            r"AWS_SECRET|PASSWORD|API_KEY": "Risk Node: CREDENTIAL LEAK DETECTED",
            r"rm -rf /": "Risk Node: DESTRUCTIVE COMMAND DETECTED",
            r"hallucination": "Analytic Node: LOGIC INCOHERENCE DETECTED"
        }

    def monitor_stream(self, simulated_text):
        print("\n--- ACCT INTUITION: STREAM MONITOR ACTIVE ---")
        buffer = ""
        for token in simulated_text.split():
            buffer += token + " "
            print(f"{token}", end=" ", flush=True)
            time.sleep(0.05) # Simulate generation latency

            # Check hurdles in the current buffer
            for pattern, intervention in self.hurdles.items():
                if re.search(pattern, buffer, re.IGNORECASE):
                    print(f"\n\n[!!!] INTERVENTION: {intervention}")
                    print(f"[*] ACTION: Stream Terminated. Triggering Refactor Protocol...")
                    return False
        
        print("\n\n[+] Stream Complete: No Hurdles Detected.")
        return True

if __name__ == "__main__":
    monitor = ACCTStreamMonitor()
    
    # Test 1: Safe Stream
    monitor.monitor_stream("I will now generate a safe Python script for file management.")
    
    # Test 2: Unsafe Stream (Credential Trigger)
    monitor.monitor_stream("To access the vault, use the following: AWS_SECRET_KEY = '12345'")
