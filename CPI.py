# pip install fredapi pandas numpy
# Free API key: https://fred.stlouisfed.org/docs/api/api_key.html
import numpy as np
import pandas as pd
from fredapi import Fred

fred = Fred(api_key="d04481c302e46f1dd7534e1e2305b884")
SERIES = "CPIAUCNS"    # CPI, all urban consumers, NOT seasonally adjusted

# 1) Final values (NSA CPI is not revised, so these equal the first releases)
cpi = fred.get_series(SERIES, observation_start="2018-12-01",
                      observation_end="2024-12-31").rename("cpi_index")
cpi.index.name = "ref_month"
cpi.to_csv("cpi_raw_monthly.csv")

# 2) Release dates: first date each month's value appeared publicly
rel = fred.get_series_all_releases(SERIES)       # columns: realtime_start, date, value
rel["date"] = pd.to_datetime(rel["date"])
rel["realtime_start"] = pd.to_datetime(rel["realtime_start"])
release_date = (rel.groupby("date")["realtime_start"].min()
                   .rename("release_date"))

m = pd.concat([cpi, release_date], axis=1).dropna()
m["cpi_yoy"] = m["cpi_index"].pct_change(12) * 100      # year-on-year inflation, %
m["cpi_mom"] = m["cpi_index"].pct_change(1) * 100       # month-on-month, % (NSA, seasonal)
m["cpi_yoy_chg"] = m["cpi_yoy"].diff()                  # change in YoY inflation
m = m.dropna()
m.to_csv("cpi_monthly_with_release_dates.csv")

# 3) Monthly -> daily, indexed by RELEASE date, then forward-filled
by_release = m.set_index("release_date")[["cpi_yoy", "cpi_mom", "cpi_yoy_chg"]]
by_release = by_release[~by_release.index.duplicated(keep="last")]

full_idx = pd.date_range("2020-01-01", "2024-12-31", freq="D")
daily = by_release.reindex(by_release.index.union(full_idx)).sort_index().ffill()
daily = daily.reindex(full_idx)
daily.index.name = "date"
daily.to_csv("inflation_daily.csv")

print(daily.shape, daily.isna().sum().to_dict())
print(m[["release_date", "cpi_yoy"]].tail())