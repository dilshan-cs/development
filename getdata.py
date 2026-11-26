import pandas as pd
import requests

url = "https://api.binance.com/api/v3/klines"

start = pd.Timestamp("2025-01-01", tz="UTC")
end = pd.Timestamp("2026-10-26", tz="UTC") 

params = {  
    "symbol": "BTCUSDT",
    "interval": "1d",
    "startTime": int(start.timestamp() * 1000),
    "endTime": int(end.timestamp() * 1000),
    "limit": 1000
} 

response = requests.get(url, params=params,timeout=30)
response.raise_for_status()

print("Status code:", response.status_code)
print("Response:", response.text[:1000])


data = response.json()


columns = [
    "open_time", "open", "high", "low", "close",
    "volume", "close_time", "quote_volume",
    "number_of_trades", "taker_buy_base_volume",
    "taker_buy_quote_volume", "ignore"
]
    
df = pd.DataFrame(data, columns=columns)
df["date"] = pd.to_datetime(
    df["open_time"], unit="ms", utc=True
)
for col in ["open", "high", "low", "close", "volume"]:
    df[col] = pd.to_numeric(df[col])


df = df[["date", "open", "high", "low", "close", "volume"]]

df.to_csv("btc_daily_2025.csv", index=False)

print(df.head())
print("Total rows:", len(df))



















