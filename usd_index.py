# pip install yfinance pandas numpy
import numpy as np
import pandas as pd
import yfinance as yf

raw = yf.download("DX-Y.NYB", start="2019-12-15", end="2025-01-01",
                  auto_adjust=False, progress=False)

if isinstance(raw.columns, pd.MultiIndex):
    raw.columns = raw.columns.get_level_values(0)

raw.index = pd.to_datetime(raw.index).tz_localize(None)
raw.to_csv("usdx_raw_trading_days.csv")          # keep the original

dx = raw[["Close"]].rename(columns={"Close": "usdx_close"})
dx["usdx_logret"] = np.log(dx["usdx_close"]).diff()

full_idx = pd.date_range("2020-01-01", "2024-12-31", freq="D")
daily = dx.reindex(dx.index.union(full_idx)).sort_index()

daily["usdx_is_trading_day"] = daily["usdx_close"].notna().astype(int)
daily["usdx_close"] = daily["usdx_close"].ffill()
daily["usdx_logret"] = daily["usdx_logret"].fillna(0)   # 0 on non-trading days

daily = daily.loc["2020-01-01":"2024-12-31"]
daily.index.name = "date"
daily.to_csv("usdx_daily.csv")

print(daily.shape, daily.isna().sum().to_dict())
print(daily["usdx_is_trading_day"].mean())