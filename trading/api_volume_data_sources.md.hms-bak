# API Volume Data Sources for Backtesting

## 1. Binance API (Recommended — Free, No Key Required for Public Data)

### Endpoint
```
GET https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=5m&limit=1000
```

### Response Format
```json
[
  [
    1499040000000,      // Open time (ms)
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume (base asset)
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base volume
    "28.46694368",      // Taker buy quote volume
    "0"                 // Ignore
  ]
]
```

### Key Fields for BAMBAM-FATCAT
- `Volume` — total base asset volume (BTC)
- `Taker buy base volume` — volume of market buys (aggressive buyers)
- `Taker buy quote volume` — quote volume of market buys
- `Number of trades` — trade count (for volume quality)

### Volume Delta Approximation
Binance doesn't provide bid/ask volume breakdown per bar, but we can approximate:
- **Buying volume** ≈ `takerBuyBaseVolume` (market orders lifting asks)
- **Selling volume** ≈ `volume - takerBuyBaseVolume` (market orders hitting bids)

This is roughly equivalent to the BAMBAM `vb`/`vs` split but coarser.

### Rate Limits
- 1200 request weight per minute
- 5m data: 1 request = 1000 bars ≈ 3.5 days
- To get 200 days: ~60 requests, trivial within rate limits

### Python Example
```python
import requests
import pandas as pd

def fetch_binance_klines(symbol="BTCUSDT", interval="5m", limit=1000):
    url = f"https://fapi.binance.com/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, params=params)
    data = r.json()
    
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades", "taker_buy_base",
        "taker_buy_quote", "ignore"
    ])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df[["open","high","low","close","volume","taker_buy_base"]] = 
        df[["open","high","low","close","volume","taker_buy_base"]].astype(float)
    return df
```

---

## 2. CoinGecko API (Free Tier: 10-30 calls/min)

### OHLC Endpoint
```
GET https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd&days=30
```

**Problem**: No volume data in OHLC endpoint.

### Market Chart Endpoint (has volume)
```
GET https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30&interval=hourly
```

**Problem**: Hourly granularity max. Not suitable for 5m backtests.

**Verdict**: Skip for this use case.

---

## 3. CryptoDataDownload.com (Free CSV Downloads)

### Direct CSV URLs
- Spot: `https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_d.csv`
- Futures: Requires free registration

**Advantage**: Pre-aggregated, no API limits.
**Disadvantage**: Daily/hourly only. Minute data requires scraping.

---

## 4. TradingView Export Methods

### A) Webhook Alerts (Real-time only)
```pinescript
alertcondition(bearSignal, "Bear", '{"side":"sell","time":"{{time}}","price":{{close}}}')
```
- Sends JSON to your webhook URL on signal
- No historical backfill
- Requires 2FA on TV account

### B) Strategy Tester CSV Export
- Apply Pine Script as `strategy()` instead of `indicator()`
- Strategy Tester tab → List of Trades → Export to CSV
- Includes: entry time, exit time, PnL, price, etc.

### C) Pine Script `log.info()` Hack
```pinescript
if bearSignal
    log.info("BEAR," + str.tostring(bar_index) + "," + str.tostring(close))
```
- Logs appear in Pine Logs tab
- Can copy/paste to spreadsheet

### D) Plot as Table (Visual Export)
```pinescript
var table t = table.new(position.top_right, 3, 100)
if bearSignal
    table.cell(t, 0, row, str.tostring(time), text_color=color.white)
    table.cell(t, 1, row, "BEAR", text_color=color.red)
    table.cell(t, 2, row, str.tostring(close), text_color=color.white)
```

---

## 5. Recommended Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Binance API    │────▶│  Python Backtest │────▶│  Signal CSV     │
│  (Historical    │     │  Engine          │     │  Export         │
│   OHLCV)        │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  Compare with    │
                        │  FATCAT signals  │
                        │  (manual export) │
                        └──────────────────┘
```

---

## 6. Data Quality Notes

- **Binance futures volume** includes both taker and maker volume
- **Taker buy ratio** (`takerBuyBase / volume`) > 0.5 means more aggressive buying
- **BAMBAM's `vb`/`vs` split** is an approximation based on close position in range
  - `vb = volume * (close - low) / (high - low)` — assumes buying pressure proportional to close position
  - This is NOT the same as actual bid/ask volume
  - For backtesting, use Binance taker data as ground truth

---

## 7. Quick Start Command

```bash
# Fetch 1000 bars of 5m BTCUSDT data
curl "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=5m&limit=1000" \
  | python3 -m json.tool > btc_5m_raw.json

# Convert to CSV with pandas
python3 -c "
import pandas as pd, json, sys
with open('btc_5m_raw.json') as f: data = json.load(f)
df = pd.DataFrame(data, columns=['ot','o','h','l','c','v','ct','qv','n','tb','tq','ig'])
df.to_csv('btc_5m.csv', index=False)
print(df.head())
"
```
