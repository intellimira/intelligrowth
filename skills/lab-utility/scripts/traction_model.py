import json
import numpy as np

def run_traction_analysis():
    # Factual Niche Data (Synthesized from Batch 1 & 2 results)
    niches = {
        "ADHD_Productivity": {"er": 0.052, "price": 120, "responsiveness": 0.85},
        "Aesthetic_Budgeting": {"er": 0.048, "price": 49, "responsiveness": 0.90},
        "Creative_Tech_AI": {"er": 0.035, "price": 197, "responsiveness": 0.65},
        "Notion_Systems": {"er": 0.065, "price": 150, "responsiveness": 0.75}
    }
    
    print("\n--- ACCT FINANCIAL MODEL: NICHE TRACTION AUDIT ---")
    results = []
    for name, stats in niches.items():
        # Formula: (ER * Responsiveness) * Price = Traction Score
        # Higher score = more likely to hit £300 with fewer emails
        traction_score = (stats['er'] * stats['responsiveness']) * stats['price']
        results.append((name, traction_score))
    
    # Sort by Traction Score
    results.sort(key=lambda x: x[1], reverse=True)
    
    for name, score in results:
        status = "WINNING NICHE" if score == results[0][1] else "SECONDARY"
        print(f"[*] {name}: Score {score:.2f} [{status}]")
    
    return results[0][0]

if __name__ == "__main__":
    run_traction_analysis()
