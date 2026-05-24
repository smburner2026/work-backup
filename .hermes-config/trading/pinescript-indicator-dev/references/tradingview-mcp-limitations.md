# TradingView MCP — What It Actually Does

## Source

`atilaahmettaner/tradingview-mcp` — pip package `tradingview-mcp-server`. 2.8k GitHub stars, MIT.

## Available Tools (30+)

- `backtest_strategy` — runs one of **6 built-in strategies** only: RSI, Bollinger, MACD, EMA cross, Supertrend, Donchian
- `compare_strategies` — compares all 6 built-in strategies
- `get_technical_analysis` — reads standard indicators (RSI, MACD, Bollinger) from Yahoo Finance / exchange API
- `market_snapshot` / `yahoo_price` — price quotes from Yahoo Finance
- `market_sentiment` / `financial_news` — Reddit + RSS feeds
- `scan_by_signal`, `screen_stocks` — TradingView screener results
- `get_candlestick_patterns` — 15 pattern detector from exchange data

## What it CANNOT do

| Task | Why |
|---|---|
| Run a custom Pine Script | The built-in strategies are hardcoded; no mechanism to inject user code |
| Read indicator plot values | No tool for reading `plotshape` events or indicator output values from a chart |
| Extract strategy entry timestamps | The Strategy Tester "Export CSV" button is a manual UI action; not exposed via API |
| Access invite-only indicator source | TV does not expose source code of invite-only scripts via any API |
| Trade execution | Read-only by design (no `place_order`, no real-time streaming) |

## What This Means

The TV MCP is useful for:
- Quick technical scans of any symbol (RSI, BB, MACD)
- Running one of 6 generic strategies against crypto/stocks (not your custom ones)
- Market-wide screening (top gainers/losers, bollinger scans)
- Sentiment analysis (Reddit + RSS)

It is NOT useful for:
- Recovering the FATCAT formula (needs custom Pine Script execution)
- Pulling BAMBAM indicator signal data programmatically
- Bypassing the CSV export bug (CSV export is the only way to get strategy trade logs)
