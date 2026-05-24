# Binance Futures API Patterns — SwingCatcher Data Pipeline

## Endpoint Lookback Limits (5m interval)

| Endpoint | Max Lookback (5m) | Notes |
|---|---|---|
| `fapi/v1/klines` | Unlimited | OHLCV + taker_buy_base_vol. Paginate 1500 at a time |
| `fapi/v1/premiumIndexKlines` | Unlimited | Same structure as klines. `close` = premium/discount decimal |
| `fapi/v1/fundingRate` | Unlimited | 8h snapshots. Paginate 500 at a time |
| `futures/data/openInterestHist` | **30 days** | For 5m period only. Longer for larger intervals |
| `futures/data/takerlongshortRatio` | **30 days** | Same period-based retention |
| `futures/data/topLongShortAccountRatio` | **30 days** | Same |
| `futures/data/topLongShortPositionRatio` | **30 days** | Same |
| `futures/data/globalLongShortAccountRatio` | **30 days** | Same |

**Rule of thumb:** If the endpoint path contains `/futures/data/`, it's a 30-day lookback at 5m. The `/fapi/v1/` endpoints have full history.

## startTime Rejection Pattern

When `startTime` is too far in the past, these endpoints return:
```json
{"code": -1104, "msg": "parameter 'startTime' is invalid."}
```

This is NOT a format issue — the timestamp is valid ms-epoch. The API simply doesn't have data that old. **The fix is to truncate the lookback window, not change the timestamp format.**

## Retry Strategy

```python
# In fetch_paginated(), after catching API error:
lookback_ms = max_lookback_days * 86400 * 1000  # 30 days in ms
now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
truncated_start = now_ms - lookback_ms

# Update both the request param AND the pagination cursor
p['startTime'] = truncated_start
current_start = truncated_start

# Retry the request
resp = requests.get(url, params=p, timeout=30)
```

The `current_start` update is critical — without it, the while-loop re-copies `params` (which still has the original startTime) and repeats the failure.

## Column Naming

The `binance_futures_data.py` script produces merged CSV with `time_str` (not `open_time_str`). The raw klines export uses `open_time_str`. The `data_loader.py` in swing_research must handle both:

```python
ts_col = 'open_time_str' if 'open_time_str' in df.columns else 'time_str'
df['dt'] = pd.to_datetime(df[ts_col], utc=True, format='%Y-%m-%d %H:%M')
```

## Merged CSV Columns (from binance_futures_data.py)

```
time_str, open, high, low, close, volume, quote_volume, trades,
taker_buy_base_vol, oi_base, oi_usd, taker_buy_vol, taker_sell_vol,
top_long_acct, top_short_acct, top_long_pos, top_short_pos,
global_long_pct, global_short_pct, basis_bps
```

`basis_bps = premium_index_close × 10,000` — positive = perp above index (bullish premium), negative = perp below index (bearish discount).

## Date Range Default

The script defaults to `START_DATE = "2025-05-01"` (12 months). Override with CLI args:
```bash
python binance_futures_data.py symbol=ETHUSDT start=2026-01-01 end=2026-05-23
```

## Known Issue: Telegram Upload Truncation

Large CSV files (>1MB) sent through Telegram as text documents get truncated to just the header row. Always use SCP or a direct file transfer for Binance data CSVs.

Format:
```bash
# From user's machine:
scp -r ./BTCUSDT/ root@178.156.199.37:/root/work/trading/bambam-fatcat-project/data/binance_futures/
```
