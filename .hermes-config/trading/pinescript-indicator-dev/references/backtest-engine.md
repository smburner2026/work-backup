# Backtest Engine Setup for Pine Script Comparison

## 1. Data Source: Binance Futures API

Free, no API key required for public endpoints. Provides real volume and taker-buy volume.

```bash
curl "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=5m&limit=1000"
```

Response fields relevant to BAMBAM-style indicators:
- `volume` — total base asset volume
- `taker_buy_base` — market-buy volume (approximates aggressive buying)
- `taker_buy_quote` — quote-volume of market buys

Volume delta approximation:
- `vb ≈ taker_buy_base` (aggressive buyers)
- `vs ≈ volume - taker_buy_base` (aggressive sellers)

This is coarser than BAMBAM's `vb = volume * (close-low)/(high-low)` but uses actual exchange data instead of close-position heuristic.

## 2. Python Backtest Engine

A self-contained script that:
1. Paginates through Binance API for arbitrary date ranges
2. Replicates exact Pine Script signal logic in pandas
3. Exports signal CSV with full metadata (vd_ratio, vol_mult, top/btm levels)
4. Optional matplotlib overlay

See `scripts/backtest_engine.py` for the full implementation.

### Parameter Sweep Workflow
```bash
# Baseline — same as BAMBAM v1
python backtest_engine.py --less-ratio 0.03 --vol-mult 1.5 --days 60

# Tighten to approach FATCAT density
python backtest_engine.py --less-ratio 0.01 --vol-mult 2.5 --delta-mode AND --days 60

# Compare counts
wc -l bambam_signals.csv  # signal count for each run
```

## 3. Pine Script Strategy Template

Convert `indicator()` → `strategy()` to use Strategy Tester and `log.info()` for CSV export.

Key inputs to expose for live tuning:
- `lessRatio` (0.001–0.1, step 0.001)
- `volMultiplier` (1.0–5.0, step 0.1)
- `deltaMode` (OR vs AND)
- `useOffset` (extreme bar vs confirmation bar)

See `templates/pinescript_strategy.pine` for the full template.

## 4. Cross-Validation Workflow

```
Step 1: Pine Script strategy on TradingView
  → Tune parameters with `input.*` until signal count matches original
  → Export Strategy Tester CSV

Step 2: Python backtest on same date range
  → Sweep parameter grid, find matching signal count/distribution
  → Verify the parameters from Step 1 are in the matching region

Step 3: Visual confirmation
  → Apply tuned indicator to TV chart alongside original
  → Screenshot comparison for 3–5 specific signal clusters
```

## 5. Data Quality Notes

- Binance 5m data: 1000 bars = ~3.5 days. Fetching 200 days = ~60 requests (well within 1200 weight/min limit).
- **Binance blocked (HTTP 451)?** Use Bitstamp as fallback: `https://www.bitstamp.net/api/v2/ohlc/btcusd/?step=300&limit=1000`. Step=300 = 5min. Paginate backward via `end` parameter (Unix seconds). Free, no API key. Confirmed working from restricted-location VPS. Example:
  ```python
  bitstamp_url = "https://www.bitstamp.net/api/v2/ohlc/btcusd/"
  params = {"step": 300, "limit": 1000, "end": timestamp}
  ```
  Bitstamp returns `[timestamp, open, high, low, close, volume]` — same shape as Binance.
- `high == low` (doji) bars: BAMBAM sets `vb = vs = 0`. In Python, use `.replace(0, np.nan)` before division.
- Pine Script `math.sum(vol, lookback) / lookback` = pandas `.rolling(lookback).sum() / lookback` = `.rolling(lookback).mean()`. They are identical.
