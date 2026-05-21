# Quant Trading Agent — Architecture Reference

## Core Principle

Hermes is the **intelligence layer**, not the **execution layer**. Execution is already handled by the user's existing infrastructure (TradingView → WunderTrading → Hyperliquid). Hermes adds analysis, monitoring, and dynamic decision-making on top.

## Data Flow

```
                    ENTRY PIPELINE
───────────────────────────────────────────────────────────
TradingView (Pine Script indicator)
    │  When volume sweep signal fires...
    │  (every N bars, volume 40%+ above avg)
    ▼
TradingView Alert (webhook)
    ▼
WunderTrading Signal Bot
    ▼
Hyperliquid (perp exchange)
    ▼
Position opens (zero leverage, small size)
    ▼
TP set to default (e.g. 10%)


                    MONITORING PIPELINE  (Hermes)
───────────────────────────────────────────────────────────
Position opens
    │
    ▼
Hermes polls market context (every N hours/bars):
    │
    ├── Coinalyze API
    │   ├── GET /open-interest-history  — is OI recovering?
    │   ├── GET /funding-rate-history   — funding flipping positive?
    │   └── GET /liquidation-history    — flush still active?
    │
    ├── CoinGecko MCP
    │   ├── BTC dominance (%)
    │   ├── Fear & Greed Index
    │   └── Global market metrics
    │
    ├── TradingView MCP
    │   ├── get_technical_analysis — TA state of BTC
    │   ├── yahoo_price — current price context
    │   └── market_sentiment — Reddit/RSS sentiment
    │
    └── WunderTrading MCP
        ├── Check current position details
        └── Check trade history for meta-analysis
    │
    ▼
Decision engine:
    ├── Context is bullish     → HOLD, raise TP, remove hard ceiling
    ├── Context is neutral     → let default TP ride as-is
    ├── Context is bearish     → early exit or tight trailing stop
    └── Mixed signals          → scale out (50% at TP, 50% trailing)
    │
    ▼
WunderTrading MCP → modify TP/SL on position


                    META-ANALYSIS PIPELINE (Hermes, cron)
───────────────────────────────────────────────────────────
Weekly/Daily (scheduled via Hermes cron):
    ├── Pull all closed trades from WunderTrading
    ├── Tag each entry with market context at time of entry
    ├── Compute: win rate, expectancy, Sharpe, max drawdown
    ├── Pattern detection: "sweeps during extreme fear recover faster"
    └── Deliver summary to user

## MCP Server Details

### TradingView MCP
- Repo: github.com/atilaahmettaner/tradingview-mcp
- Install: `pip install tradingview-mcp-server` or `uvx tradingview-mcp-server`
- Config: stdio command via `uvx`
- Version: v0.7.0 (MIT)
- Key tools: backtest_strategy, compare_strategies, get_technical_analysis, yahoo_price, market_sentiment, financial_news, combined_analysis
- No API keys required

### CoinGecko MCP
- Docs: docs.coingecko.com/docs/ai-agent-hub/mcp-server
- Config: HTTP SSE endpoint
- First 25 API calls/min free (Demo tier), Pro for higher limits
- Key data: prices, market cap, volume, categories, trending, global metrics

### WunderTrading MCP
- Site: wundertrading.com/en/hyperliquid-trading-bot
- Purpose: connect AI agents to Hyperliquid via MCP
- Free premium tier for Hyperliquid traders
- Also supports: TradingView signal execution, Grid/DCA/Market Neutral bots
- Use cases: check open positions, modify TP/SL, close positions, get trade history

### Coinalyze API
- Docs: api.coinalyze.net/v1/doc
- Free, rate limit 40 calls/min per key
- No MCP server exists yet — needs a lightweight wrapper
- Key endpoints:
  - /future-markets, /spot-markets
  - /open-interest, /open-interest-history
  - /funding-rate, /funding-rate-history
  - /predicted-funding-rate, /predicted-funding-rate-history
  - /liquidation-history
  - /ohlcv-history
  - /exchanges

### Hyperliquid Python SDK (fallback for raw chain data)
- Repo: github.com/hyperliquid-dex/hyperliquid-python-sdk
- Use when you need data that WunderTrading doesn't surface
- Order book, positions, account info, direct order placement
- Testnet available at api.hyperliquid-testnet.xyz

## Cron Job Patterns

For ongoing monitoring:

```yaml
# ~/.hermes/config.yaml cron jobs
# Position check every 4 hours on BTC
schedule: "0 */4 * * *"
skills: ["quant-trading-agent"]
prompt: "Check my open positions on Hyperliquid via WunderTrading. For each position, get BTC's current OI trend, funding rate, and technical state. Recommend: HOLD (trending), ADJUST TP (neutral), or EXIT (bearish context)."

# Weekly performance report
schedule: "0 9 * * 1"
skills: ["quant-trading-agent"]
prompt: "Pull my trade history from WunderTrading this week. Calculate: total trades, win rate, expectancy, max drawdown, net P&L. Compare to the prior week. Note any pattern changes."
```

## See Also

- SKILL.md — core workflows and user approach
