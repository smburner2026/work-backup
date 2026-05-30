---
name: trading-architecture-strategy-vault
description: "Full architecture for the Strategy Vault → Python Engine → Hermes Board → Execution pipeline. TV = visualization only, Python = core compute, Hermes = AI gate."
version: 1.0.0
author: Hermes Agent
tags: [trading, architecture, strategy-vault, hermes-board, python-engine]
---

# Trading Architecture: Strategy Vault → Hermes Board → Execution

## Architecture Decision (May 27, 2026)

### The Stack

Three layers:

**1. Obsidian Vault (Strategy Source of Truth)**
- User curates trader profiles, setup rules, chart examples here
- Strategy cards: confluence, entries, invalidations, risk, trims, backtest results
- Tag system: `#ready-for-board` activates a strategy for Hermes evaluation
- Python reads strategy parameters from vault notes

**2. Python Engine (Core Computation — zero token cost)**
- Persistent data fetcher: Binance WS, Coinalyze, TradingView MCP
- Monitor loop: checks MA, OI, CVD conditions every bar (24/7)
- Backtest engine: historical simulation with configurable TP targets
- Strategy development: reads Obsidian → implements in Python → validates via backtest
- When signal detected: writes signal + context to status file → wakes Hermes

**3. Hermes Board (AI Gate — token cost per decision)**
- Reads signal from Python + strategy card from Obsidian + live context
- Decides: PASS ✓ | ADJUST TP | BLOCK ✕
- Writes decision back to status file
- Only fires when Python calls it — no continuous monitoring

**4. Execution Layer**
- Python receives Hermes' decision
- CCXT for direct exchange access (optional)
- Webhook to Wundertrading / TradersPost
- Per-strategy account routing for clean P&L

### Integration Pattern (Filesystem-Based)

```
Python writes signal.json → Hermes reads it → decides → writes decision.json → Python executes
```

No complex IPC. No webhook chain. Two processes passing JSON through a file.

### TradingView Role (Visualization Only)
- Charts and price display — no alerts
- No execution dependency — pipeline continues if TV is down
- User watches the same data Python sees

### Token Math
- Python loop: $0 (pure computation)
- Python backtest: $0 (historical data, no LLM)
- Hermes evaluation: ~$0.02 per decision (1 LLM call, only when signal fires)
- Total per trade: ~$0.02

### Build Order
1. Python monitor script — persistent loop that checks conditions on each new bar
2. Backtest engine — exists at /root/work/trading/scripts/backtest_bambam_fatcat.py, needs JSON output mode
3. Obsidian strategy card template — define card fields (confluence, entries, invalidation, risk, trims)
4. Hermes decision gate — reads card + context, outputs decision
5. Execution router — sends Hermes' decision to correct webhook/account

### Strategy Lifecycle
1. Create strategy → Obsidian vault (trader profile → structured card)
2. Python reads card → backtests historically
3. Results satisfactory? → mark strategy as "active" in vault
4. Python monitor detects signal → writes signal.json with context
5. Hermes reads signal + strategy card + live context → decides
6. Python receives decision → executes via webhook to designated account

### Key Files
- Backtest engine: /root/work/trading/scripts/backtest_bambam_fatcat.py
- Wundertrading proxy: /root/work/trading/wundertrading_proxy_server.py (TP-only, no sell/close/stop)
- Architecture diagram: /root/work/trading/trading-architecture.html
- Wundertrading MCP docs: https://wundertrading.com/docs/mcp
- TradingView MCP package: tradingview-mcp-server (uvx)

### Wundertrading Constitutional Constraint
The proxy at wundertrading_proxy_server.py ONLY exposes:
- get_live_strategies (read positions)
- get_strategy (read position details)
- edit_take_profit (ONLY modifies TP levels — no close, sell, stop, cancel)
- proxy_health (check config)

WUNDER_API_KEY and WUNDER_SECRET_KEY env vars needed to activate.

### Data Sources
- Binance API: OHLCV, taker buy/sell (CVD)
- Coinalyze: OI, funding, liquidations (not yet built)
- TradingView MCP: Yahoo Finance prices, technicals, sentiment
- All feed into Python engine
