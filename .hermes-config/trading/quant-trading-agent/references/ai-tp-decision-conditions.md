# AI TP Decision Conditions (May 2026)

The user specified three conditions that govern when the AI should override the fixed 10% TP:

## Condition 1: Above MA

**Check:** Is BTC price above a key moving average?

| Parameter | Value |
|---|---|
| **Data source** | TradingView MCP — `get_technical_analysis(symbol=BTCUSDT)` or `multi_timeframe_analysis` |
| **Typical MA** | 50-day or 200-day SMA/EMA |
| **"Healthy"** | Price > MA = bullish regime context |
| **"Unhealthy"** | Price < MA = bearish, don't stretch TP |

## Condition 2: OI Healthy

**Check:** Is Open Interest recovering or still collapsing?

| Parameter | Value |
|---|---|
| **Data source** | Coinalyze REST API (not yet built — planned as custom MCP wrapper) |
| **Endpoint** | Coinalyze open interest history endpoint |
| **"Healthy"** | OI trending upward over lookback, or OI > rolling average |
| **"Unhealthy"** | OI still declining = the move lacks institutional backing |

## Condition 3: CVD Healthy

**Check:** Is Cumulative Volume Delta positive/rising?

| Parameter | Value |
|---|---|
| **Data source** | Binance free API — taker buy/sell volume |
| **Endpoint** | `GET https://fapi.binance.com/futures/data/takerbuySellVol?symbol=BTCUSDT&period=15m` |
| **Auth** | None required. Rate limit: 1000 req/5min |
| **Calculation** | For each period: CVD_delta = buyVol - sellVol. Cumulative: sum of deltas over lookback |
| **"Healthy"** | CVD rising or positive = aggressive buying supports the move |
| **"Unhealthy"** | CVD flat or falling = move lacks taker support |

## Decision Table

```
if above_MA AND OI_healthy AND CVD_healthy →
    STRETCH TP (remove fixed 10%, set wider target up to 20% max)
else →
    LEAVE FIXED TP (10% — the proven 20% YOY baseline)
```

All three must align. One out of three is not enough — the fixed 10% TP is the default, proven baseline. The AI only overrides it when confluence confirms a genuine washout recovery.

## Safety Bounds

- Max stretched TP: 20% (2× baseline)
- Never remove TP entirely
- No trailing stop (constitutional for BTC)
- No stop loss (constitutional for BTC)
- Re-check conditions every monitoring interval
- If conditions deteriorate after stretching, reset to fixed 10% TP
- Verify-read after every TP change: call `get_strategy` to confirm update
