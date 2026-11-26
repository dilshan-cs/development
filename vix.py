# pip install yfinance pandas numpy
import numpy as np
import pandas as pd
import yfinance as yf

raw = yf.download("^VIX", start="2019-12-15", end="2025-01-01",
                  auto_adjust=False, progress=False)

if isinstance(raw.columns, pd.MultiIndex):
    raw.columns = raw.columns.get_level_values(0)

raw.index = pd.to_datetime(raw.index).tz_localize(None)
raw.to_csv("vix_raw_trading_days.csv")           # keep the original

vx = raw[["Close"]].rename(columns={"Close": "vix_close"})
vx["vix_change"] = vx["vix_close"].diff()                  # first difference of level
vx["vix_logchg"] = np.log(vx["vix_close"]).diff()          # log change (alternative)

full_idx = pd.date_range("2020-01-01", "2024-12-31", freq="D")
daily = vx.reindex(vx.index.union(full_idx)).sort_index()

daily["vix_is_trading_day"] = daily["vix_close"].notna().astype(int)
daily["vix_close"] = daily["vix_close"].ffill()
daily["vix_change"] = daily["vix_change"].fillna(0)      # 0 on non-trading days
daily["vix_logchg"] = daily["vix_logchg"].fillna(0)

daily = daily.loc["2020-01-01":"2024-12-31"]
daily.index.name = "date"
daily.to_csv("vix_daily.csv")

print(daily.shape, daily.isna().sum().to_dict())
print(daily["vix_is_trading_day"].mean())