# pip install yfinance pandas numpy
import numpy as np
import pandas as pd
import yfinance as yf

# Start a few days early so the first return and the weekend fill have a prior value
raw = yf.download("^GSPC", start="2019-12-15", end="2025-01-01",
                  auto_adjust=False, progress=False)

# Newer yfinance versions return MultiIndex columns; flatten if needed
if isinstance(raw.columns, pd.MultiIndex):
    raw.columns = raw.columns.get_level_values(0)

raw.index = pd.to_datetime(raw.index).tz_localize(None)
raw.to_csv("sp500_raw_trading_days.csv")        # keep the original

sp = raw[["Close"]].rename(columns={"Close": "sp500_close"})
sp["sp500_logret"] = np.log(sp["sp500_close"]).diff()

# Bitcoin trades 7 days a week, the S&P 500 only on trading days.
# Expand to every calendar day and carry the last known value forward.
full_idx = pd.date_range("2020-01-01", "2024-12-31", freq="D")
daily = sp.reindex(sp.index.union(full_idx)).sort_index()

daily["is_trading_day"] = daily["sp500_close"].notna().astype(int)
daily["sp500_close"] = daily["sp500_close"].ffill()

# Returns are 0 on weekends/holidays (no new information), not forward-filled
daily["sp500_logret"] = daily["sp500_logret"].fillna(0)

daily = daily.loc["2020-01-01":"2024-12-31"]
daily.index.name = "date"
daily.to_csv("sp500_daily.csv")

print(daily.shape, daily.isna().sum().to_dict())
print(daily["is_trading_day"].mean())   # roughly 0.69 expected