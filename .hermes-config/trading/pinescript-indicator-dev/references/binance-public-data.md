# Binance Public Data on AWS S3

Base URL: `https://data.binance.vision/`

## Available Data
- **Spot** and **Futures (UM)** daily klines
- All major trading pairs (BTCUSDT, ETHUSDT, etc.)
- All timeframes: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1mo
- Data format: zipped CSV, one file per day
- Goes back years (check monthly archives for older data)

## Key Field: `taker_buy_base`
Column index 9 in the CSV (0-indexed) — the actual volume of market-buy orders in base asset units. Critical for signal detection because:

- BAMBAM's estimate `vb = vol × (close-low)/(high-low)` consistently overestimates buying pressure at swing lows (~2% average bias, but heavily skewed at extremes)
- Real `taker_buy_base` shows actual order flow — much lower at 200-bar lows, which naturally filters false signals
- Using taker_buy with vm=1.0 (volume > average) produces ~60% fewer signals than the estimate at vm=1.5

## CSV Column Layout (Spot)
| Index | Field | Type | Notes |
|---|---|---|---|
| 0 | open_time | int | Unix ms (`÷1000` to convert micro→ms if using data.binance.vision) |
| 1 | open | float | |
| 2 | high | float | |
| 3 | low | float | |
| 4 | close | float | |
| 5 | volume | float | Base asset volume |
| 6 | close_time | int | Unix ms |
| 7 | quote_vol | float | Quote asset volume |
| 8 | trades | int | Number of trades |
| 9 | **taker_buy_base** | float | Market-buy base volume — KEY FIELD |
| 10 | taker_buy_quote | float | Market-buy quote volume |
| 11 | ignore | str | Unused |

## Timestamp Issue
The CSV timestamps from `data.binance.vision` are in **MICROSECONDS** (not milliseconds). To convert:
```python
pd.to_datetime(open_time // 1000, unit='ms')
```

## Python Fetch Pattern
```python
import requests, zipfile, io, pandas as pd
from datetime import datetime, timedelta

base = "https://data.binance.vision/data/spot/daily/klines/BTCUSDT/15m"
all_data = []
current = datetime(2026, 2, 23)
end = datetime(2026, 5, 19)

while current <= end:
    ds = current.strftime('%Y-%m-%d')
    r = requests.get(f"{base}/BTCUSDT-15m-{ds}.zip", timeout=30)
    if r.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        with z.open(z.namelist()[0]) as f:
            for line in f.read().decode('utf-8').strip().split('\n'):
                p = line.split(',')
                all_data.append({
                    't': int(p[0]) // 1000,     # micro → ms
                    'o': float(p[1]),
                    'h': float(p[2]),
                    'l': float(p[3]),
                    'c': float(p[4]),
                    'v': float(p[5]),
                    'tb': float(p[9]),          # taker_buy_base
                })
    current += timedelta(days=1)

df = pd.DataFrame(all_data)
df["dt"] = pd.to_datetime(df["t"], unit="ms")
```

## Futures vs Spot
- Futures URL prefix: `data.binance.vision/data/futures/um/daily/klines/`
- Spot URL prefix: `data.binance.vision/data/spot/daily/klines/`
- Futures data includes additional fields (like `taker_buy_base_vol` at different index)
- Both work from the same server with no API key required

## Rate Limits
No documented rate limits for the S3 bucket. Tested with sequential requests at 10-20/day with no throttling. The files are small (5-10KB per day for 15m BTCUSDT).

## Regional Blocking
If `fapi.binance.com` or `api.binance.com` returns HTTP 451, the S3 bucket at `data.binance.vision` typically still works — it's hosted on AWS CloudFront, not Binance's infrastructure.
