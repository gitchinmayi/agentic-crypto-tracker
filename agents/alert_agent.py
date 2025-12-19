import json
import os

class AlertAgent:
    def __init__(self, btc_threshold=50000, eth_threshold=4000):
        self.btc_threshold = btc_threshold
        self.eth_threshold = eth_threshold
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.processed_file = os.path.join(base_dir, "data", "processed", "processed_crypto.json")

    def check_alerts(self):
        if not os.path.exists(self.processed_file):
            print(f"[AlertAgent] Processed file not found: {self.processed_file}")
            return

        with open(self.processed_file, "r") as f:
            data = json.load(f)

        btc_price = data["prices"]["bitcoin"]["usd"]
        eth_price = data["prices"]["ethereum"]["usd"]

        alerts_triggered = False

        if btc_price > self.btc_threshold:
            print(f"[ALERT] Bitcoin price is above threshold: ${btc_price}")
            alerts_triggered = True

        if eth_price > self.eth_threshold:
            print(f"[ALERT] Ethereum price is above threshold: ${eth_price}")
            alerts_triggered = True

        if not alerts_triggered:
            print("[AlertAgent] No alerts triggered.")

        return alerts_triggered


# Run standalone
if __name__ == "__main__":
    agent = AlertAgent()
    agent.check_alerts()

