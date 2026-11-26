# pip install pytrends pandas
import time
import pandas as pd
# pyrefly: ignore[missing-import]
from pytrends.request import TrendReq

KEYWORDS = ["bitcoin", "buy bitcoin", "crypto","BTC","btc"]   # edit as you like
TIMEFRAME = "2020-01-01 2024-12-31"
GEO = ""          # "" = worldwide

def fetch_trends(keyword, retries=5):
    for attempt in range(retries):
        try:
            pt = TrendReq(hl="en-US", tz=0, timeout=(10, 30))
            pt.build_payload([keyword], timeframe=TIMEFRAME, geo=GEO)
            df = pt.interest_over_time()
            return df[keyword].rename(f"gt_{keyword.replace(' ', '_')}")
        except Exception as e:
            wait = 30 * (attempt + 1)
            print(f"{keyword}: {e} -> retry in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"Failed: {keyword}")

# One keyword per request so each series is scaled 0-100 on its own
weekly = pd.concat([fetch_trends(k) for k in KEYWORDS], axis=1)
for k in KEYWORDS:
    time.sleep(10)

weekly.index = pd.to_datetime(weekly.index)
weekly.to_csv("google_trends_weekly_raw.csv")

# --- Weekly -> daily ---
# pytrends labels each week by its START date (Sunday). The value describes
# the whole week, so it is only known at the END of that week.
weekly_avail = weekly.copy()
weekly_avail.index = weekly_avail.index + pd.Timedelta(days=6)

daily_idx = pd.date_range("2020-01-01", "2024-12-31", freq="D")
daily = weekly_avail.reindex(daily_idx.union(weekly_avail.index))

daily_ffill  = daily.ffill().reindex(daily_idx)                       # no look-ahead
daily_interp = daily.interpolate(method="time").reindex(daily_idx)    # as in proposal

daily_ffill.to_csv("google_trends_daily_ffill.csv", index_label="date")
daily_interp.to_csv("google_trends_daily_interp.csv", index_label="date")


print(weekly.shape, daily_ffill.isna().sum().to_dict())