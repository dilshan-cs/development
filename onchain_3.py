
# import requests
# import pandas as pd

# BASE_URL = "https://mempool.space/api"

# # Choose a whale transaction threshold
# MIN_BTC = 1

# # Get the latest block height
# height = requests.get(
#     f"{BASE_URL}/blocks/tip/height", 
#     timeout=30
# )
# height.raise_for_status()
# latest_height = int(height.text)

# whale_transactions = []

# # Examine the latest 5 blocks
# for block_height in range(
#     latest_height,
#     latest_height - 5,
#     -1
# ):
#     block_response = requests.get(
#         f"{BASE_URL}/block-height/{block_height}",
#         timeout=30
#     )
#     block_response.raise_for_status()
#     block_hash = block_response.text

#     tx_response = requests.get(
#         f"{BASE_URL}/block/{block_hash}/txs",
#         timeout=30
#     )
#     tx_response.raise_for_status()

#     transactions = tx_response.json()

#     for tx in transactions:
#         # Total value of all transaction outputs, in satoshis
#         total_sats = sum(
#             output["value"]
#             for output in tx.get("vout", [])
#         )

#         total_btc = total_sats / 100_000_000

#         if total_btc >= MIN_BTC:
#             whale_transactions.append({
#                 "block_height": block_height,
#                 "txid": tx["txid"],
#                 "total_output_btc": total_btc,
#                 "confirmed": tx["status"]["confirmed"]
#             })

# df = pd.DataFrame(whale_transactions)

# if not df.empty:
#     df = df.drop_duplicates(subset=["txid"])
#     df.to_csv("btc_whale_transactions.csv", index=False)

# print(df.head(20))
# print("Transactions found:", len(df))



import requests
import pandas as pd

API_KEY = "kote_bDFGX5047P-41jVNoVmM_Eqiq9yXu3OB"

url = "https://kotecharts.com/api/v1/public/charts/whale-tx-volume"

params = {
    "from": "2020-01-01",
    "to": "2026-10-24",
    "granularity": "day"
}

response = requests.get(
    url,
    headers={"X-API-Key": API_KEY},
    params=params,
    timeout=30
)

response.raise_for_status()
result = response.json()

print(result)

series = result["data"]["series"]
df = pd.DataFrame(series)

print(df.head())
df.to_csv("btc_whale_volume.csv", index=False)