import pandas as pd

base_url = "https://bitcoin-data.com/v1"

metrics = {
    "active_addresses": "active-addresses",
    "transaction_coumt": "tx-count",
    "coin_days_destroyed": "cdd"
} 

for filename, endpoint in metrics.items():
    url = f"{base_url}/{endpoint}/csv"

    try:
        df = pd.read_csv(url)
        df.to_csv(f"btc_{filename}.csv", index=False)

        print(f"{filename}: {len(df)} rows downloaded")
        print(df.head())

    except Exception as error:
        print(f"Failed to download {filename}: {error}") 

    