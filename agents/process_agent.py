import json
import os

RAW_FILE = "data/crypto_prices.json"
PROCESSED_FILE = "data/processed/processed_crypto.json"

def process_data():
    if not os.path.exists(RAW_FILE):
        print("No raw data found yet.")
        return

    with open(RAW_FILE, "r") as f:
        raw_data = json.load(f)

    raw_prices = raw_data.get("prices", {})

    processed_prices = {}

    for coin, info in raw_prices.items():
        price = info.get("usd", 0)
        prev_price = info.get("prev_usd", price)  # fallback if no previous
        percent_change = ((price - prev_price) / prev_price) * 100 if prev_price else 0

        processed_prices[coin] = {
            "usd": price,
            "prev_usd": prev_price,
            "percent_change_24h": round(percent_change, 2)
        }

    # Wrap in "prices" for AlertAgent compatibility
    processed_data = {
        "timestamp": raw_data.get("timestamp"),
        "prices": processed_prices
    }

    # Ensure processed folder exists
    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)

    with open(PROCESSED_FILE, "w") as f:
        json.dump(processed_data, f, indent=4)

    print(f"Processed data saved to {PROCESSED_FILE}")

if __name__ == "__main__":
    process_data()

