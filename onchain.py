import requests 
import pandas as pd

url = "https://bitcoin-data.com/v1/active-addresses/csv"

response = requests.get(url, timeout=30)
response.raise_for_status()



df = pd.read_csv(pd.io.common.StringIO(response.text))

print(df.head())
print(df.columns)

df.to_csv("btc_active_addresses.csv", index=False)