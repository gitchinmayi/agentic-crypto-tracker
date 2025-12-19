import requests
import json
import os
from datetime import datetime


class FetchAgent:
    def __init__(self):
        self.api_url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum&vs_currencies=usd"
        )

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_file = os.path.join(base_dir, "data", "crypto_prices.json")

    def fetch_prices(self):
        print("[FetchAgent] Fetching live crypto prices...")

        response = requests.get(self.api_url, timeout=10)
        response.raise_for_status()

        prices = response.json()
        data = {
            "timestamp": datetime.utcnow().isoformat(),
            "prices": prices
        }

        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

        print("[FetchAgent] Prices fetched successfully ✅")
        print(json.dumps(data, indent=2))

        return data

