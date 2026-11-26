# pip install requests pandas
import requests
import pandas as pd

URL = "https://api.alternative.me/fng/"
params = {"limit": 0, "format": "json"}   # limit=0 returns the full history

resp = requests.get(URL, params=params, timeout=30)
resp.raise_for_status()
data = resp.json()["data"]

df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["timestamp"].astype(int), unit="s").dt.normalize()
df["fng_value"] = df["value"].astype(int)
df = (df[["date", "fng_value", "value_classification"]]
        .sort_values("date")
        .set_index("date"))

# Save the full raw history first
df.to_csv("fear_greed_raw_full.csv")

# Restrict to your study window
df = df.loc["2020-01-01":"2024-12-31"]

# Check for missing days
full_idx = pd.date_range("2020-01-01", "2024-12-31", freq="D")
missing = full_idx.difference(df.index)
print("Rows:", len(df), "| Missing days:", len(missing))
if len(missing):
    print(missing)

df = df.reindex(full_idx)
df["fng_value"] = df["fng_value"].ffill()   # only if a few days are missing
df.index.name = "date"
df[["fng_value"]].to_csv("fear_greed_daily.csv")