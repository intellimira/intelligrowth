# main.py  —  LOGISTICS FREIGHT Strategy Fix
# Cluster: LOCAL_SENTRY

import sys
import os
import csv
import glob

# Add root to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.core_sentry import LocalSentry

class FreightSentry(LocalSentry):
    def __init__(self):
        super().__init__("Freight_Fix", "logistics_strategy.db")
        self.drop_zone = os.path.abspath(os.path.join(os.path.dirname(__file__), "../drop_zone"))
        os.makedirs(self.drop_zone, exist_ok=True)
        # Simplified carrier rates for strategy comparison
        self.CARRIER_RATES = {
            "SEA_CARRIER": 0.05, # Per kg
            "AIR_CARRIER": 0.45,
            "ROAD_CARRIER": 0.15
        }

    def optimize_freight_strategy(self):
        """Monitor for new shipping manifests and apply cost-optimisation strategies."""
        print(f" [FREIGHT] Monitoring {self.drop_zone} for new shipping manifests...")
        csv_files = glob.glob(os.path.join(self.drop_zone, "*.csv"))
        
        for file_path in csv_files:
            print(f" [FREIGHT] Processing manifest: {os.path.basename(file_path)}...")
            try:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        weight = float(row.get('Weight_KG', 0.0))
                        current_cost = float(row.get('Current_Cost', 0.0))
                        
                        # Find cheapest carrier
                        best_rate = min(self.CARRIER_RATES.values())
                        optimized_cost = weight * best_rate
                        
                        if optimized_cost < current_cost:
                            saving = current_cost - optimized_cost
                            self.log_event("STRATEGY_FIX", {"shipment_id": row.get('Shipment_ID'), "saving": saving}, status="OPTIMISED")
                        else:
                            self.log_event("STRATEGY_OK", {"shipment_id": row.get('Shipment_ID')})
                
                # Move to archive
                archive_dir = os.path.join(self.drop_zone, "archive")
                os.makedirs(archive_dir, exist_ok=True)
                os.rename(file_path, os.path.join(archive_dir, os.path.basename(file_path)))
                
            except Exception as e:
                self.log_event("STRATEGY_FAILED", {"file": file_path, "error": str(e)}, status="FAILED")

if __name__ == "__main__":
    sentry = FreightSentry()
    sentry.run_check(sentry.optimize_freight_strategy, interval=600)
