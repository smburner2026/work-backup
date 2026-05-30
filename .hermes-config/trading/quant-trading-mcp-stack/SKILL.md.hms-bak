---
name: quant-trading-mcp-stack
description: "MCP server stack for the quant trading project — TradingView MCP (research/backtesting) + Wundertrading TP-only proxy (execution constrained to take-profit modifications only)."
version: 1.0.0
author: Hermes Agent
tags: [trading, mcp, wundertrading, tradingview, proxy, take-profit]
---

# Quant Trading MCP Stack

## Servers

### 1. TradingView MCP (research & backtesting)
- **Package:** `tradingview-mcp-server` (PyPI, MIT, free, no API key required)
- **Executable:** `tradingview-mcp`
- **Config:**
  ```yaml
  mcp_servers:
    tradingview:
      command: uvx
      args: ["--from", "tradingview-mcp-server", "tradingview-mcp"]
      timeout: 120
  ```
- **27 tools** including:
  - `backtest_strategy` / `compare_strategies` / `walk_forward_backtest_strategy`
  - `yahoo_price` / `market_snapshot`
  - `get_technical_analysis` / `multi_timeframe_analysis`
  - `market_sentiment` / `financial_news` / `combined_analysis`
  - `volume_breakout_scanner` / `smart_volume_scanner` / `coin_analysis`
  - `top_gainers` / `top_losers` / `bollinger_scan`
  - `consecutive_candles_scan` / `advanced_candle_pattern`

### 2. Wundertrading TP-Only Proxy
- **Path:** `/root/work/trading/wundertrading_proxy_server.py`
- **Config:**
  ```yaml
  mcp_servers:
    wundertrading:
      command: python3
      args: ["/root/work/trading/wundertrading_proxy_server.py"]
      env:
        WUNDER_API_KEY: ""
        WUNDER_SECRET_KEY: ""
      timeout: 30
  ```
- **Exposed tools (4):**
  - `get_live_strategies` — list open positions (read-only)
  - `get_strategy` — get position details, entry price, current status (read-only)
  - `edit_take_profit` — update take profit levels ONLY (constitutional constraint)
  - `proxy_health` — check config status

## Constitutional Constraints

The Wundertrading proxy PHYSICALLY CANNOT:
- Close positions (`close_strategy_market` does not exist in the proxy)
- Set stop losses (`stopLossPrice` param is filtered out)
- Cancel strategies
- Place new trades
- Use trailing stops

The `edit_take_profit` tool only accepts: `strategy_id`, `take_profits` (array of {price, portfolio}), `base_on`.
Portfolio sum must equal 1.0 (validated in the proxy before forwarding).

## Credential Setup

When API keys are ready:
```bash
export WUNDER_API_KEY="your_hmac_api_key"
export WUNDER_SECRET_KEY="your_hmac_secret_key"
```
Then restart Hermes session, or update config.yaml with the actual keys and run `/reload-mcp`.

## Testing

```bash
# Test connection and list tools
hermes mcp test tradingview
hermes mcp test wundertrading

# Note: hermes mcp does NOT have a "call" subcommand.
# Use mcporter for ad-hoc tool calls from terminal:
# mcporter call tradingview market_snapshot

# Check proxy health (via MCP inspector or your code)
```

## Architecture Note

The Wundertrading proxy is a **separate process** that sits between Hermes and the Wundertrading MCP API:
```
Hermes Agent → (stdio) → Proxy MCP → (HTTP) → Wundertrading API (wundertrading.com:2083/mcp)
```

The proxy binary does not contain sell/close/stop code paths. This is architectural, not config-level — the constraint cannot be overridden by changing config.yaml or prompt instructions.

## Three-Layer Architecture (Quant Project)

The full stack has three layers, with Obsidian as source of truth:

```
┌──────────────────────────────────────────────┐
│  OBSIDIAN VAULT (strategy-vault/)            │ ← Source of truth
│  Strategy cards, trader profiles, rules      │
│  User curates. Hermes reads/writes.          │
├──────────────────────────────────────────────┤
│  PYTHON SCRIPTS (/root/work/trading/scripts/)│ ← Execution layer
│  - backtest_bambam_fatcat.py                 │
│  - wundertrading_proxy_server.py             │
│  - Coinalyze data fetcher (planned)          │
├──────────────────────────────────────────────┤
│  HERMES BOARD (control surface)             │ ← Orchestration
│  Reads cards → extracts params → runs        │
│  Python → interprets results → updates cards │
│  Tracks: rules, confluence, results, status  │
└──────────────────────────────────────────────┘
```

### Key files

| Path | Purpose |
|------|---------|
| `/root/work/trading/scripts/backtest_bambam_fatcat.py` | BAMBAM signal generator + backtest engine |
| `/root/work/trading/wundertrading_proxy_server.py` | TP-only MCP proxy |
| `/root/work/trading/bambam-fatcat-project/` | BAMBAM/FATCAT research data |

### Workflow sequence

1. User writes/updates a strategy card in Obsidian vault
2. Hermes reads the card, extracts parameters (timeframe, volume multiplier, TP targets)
3. Hermes calls the Python backtester with those parameters
4. Python returns structured JSON results
5. Hermes writes results back to the strategy card (## Backtest Results section)
6. When confluence conditions are met and backtest validates, card is marked webhook-ready

### Risk assessment (from session analysis)

- **Entry edge is structural** (BTC martingale, small size, no stops, 20% YOY proven) — not a fragile technical pattern
- **Simulation risk:** backtest encodes deterministic proxy rules for AI decisions — the real AI may diverge from the proxy. Mitigation: run rules proxy and AI in parallel during paper phase, track divergence.
- **Data gaps:** CVD data from Binance API (30-day limit), OI from Coinalyze (not yet built). Mitigation: validate with available data first, add sources incrementally.
- **Constitutional constraints:** never sell BTC at loss, never set stop losses, Hermes only calls `edit_take_profit`.


See `references/constrained-proxy-pattern.md` for the reusable pattern documentation and implementation template.
