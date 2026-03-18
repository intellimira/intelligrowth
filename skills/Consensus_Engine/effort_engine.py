import time
import random

class EffortEngine:
    def __init__(self, max_cpu_load=80, min_effort=25):
        self.max_cpu_load = max_cpu_load
        self.min_effort = min_effort

    def get_current_load(self):
        # Simulating CPU load
        return random.randint(10, 95)

    def check_throttle(self):
        """
        Returns True if the node should throttle down based on Effort.
        """
        current_load = self.get_current_load()
        if current_load > self.max_cpu_load:
            print(f"[EFFORT] CPU Load High ({current_load}%). Throttling...")
            return True
        return False

    def regulate_effort(self):
        """
        Adjusts sleep time to regulate effort.
        """
        if self.check_throttle():
            # Throttle: Sleep to cool down
            throttle_time = (self.min_effort / 100.0) * 1.0 
            time.sleep(throttle_time)
            return "THROTTLED"
        return "NORMAL"

if __name__ == "__main__":
    eng = EffortEngine()
    for _ in range(5):
        status = eng.regulate_effort()
        print(f"Effort Status: {status}")
