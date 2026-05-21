---
name: quant-trading-agent
description: Build and operate a quant trading agent using Hermes as the intelligence layer — backtesting, multi-trader profiling (YouTube/tweet extraction → regime-tagged setups → Pine Script indicators), context-dependent exits, multi-MCP signal confirmation, and trade meta-analysis on top of existing execution infrastructure.
category: trading
tags: ["mcp", "trading", "backtesting", "pine-script", "hyperliquid", "tradingview", "coinalyze", "wundertrading"]
---

# Quant Trading Agent

## Overview

Hermes as the quant/AI layer on top of existing trading infrastructure. The foundational insight: **Hermes does not execute trades** — that's already handled by WunderTrading → Hyperliquid or similar. Hermes provides the analysis, monitoring, and intelligence that a set-and-forget bot cannot.

The value-add is:
1. **Context-dependent exits** instead of fixed TPs
2. **Multi-source signal confirmation** (OI, funding, volume, sentiment)
3. **Meta-analysis** of trade history to sharpen the edge over time
4. **Parameter backtesting at scale** to optimize the core strategy

## Architecture

```
TradingView (Pine Script signal)
    → WunderTrading (execution)
        → Hyperliquid (perps venue)
              ↑
Hermes Agent  |
    ├── monitors positions via WunderTrading MCP
    ├── checks context via Coinalyze API (OI, funding, liquidations)
    ├── checks market sentiment via CoinGecko MCP
    ├── checks technicals via TradingView MCP
    └── recommends/modifies TP/SL based on market context
```

### MCP Stack

| Server | Purpose | Setup |
|---|---|---|
| **TradingView MCP** | Backtesting, 23+ TA indicators, sentiment (Reddit/RSS), Yahoo Finance prices | `uvx tradingview-mcp-server` |
| **CoinGecko MCP** | Crypto market context: dominance, sentiment, global metrics, trending | HTTP SSE endpoint |
| **WunderTrading MCP** | Position monitoring, TP/SL modification, order management on Hyperliquid | Follow WT docs |
| **Coinalyze API** | Open interest, funding rates, liquidations, OHLCV history | REST (free, 40 calls/min). Wrap as custom MCP. |

## Key Workflows

### 1. Position Monitoring with Context-Dependent Exits

The core workflow. Instead of a fixed TP that caps trends:

```
Position opens via WunderTrading
    → Hermes polls every N hours/bars:
        ├── OI recovering?          → trend has legs → HOLD, raise TP
        ├── Funding flipping pos?   → real buying   → HOLD
        ├── BTC dominance dropping? → alt season    → HOLD (if alt)
        ├── Volume still elevated?  → continuation  → HOLD
        ├── All quiet?              → let fixed TP ride as-is
        └── OI tanking, funding neg?→ early exit or tight trailing stop
```

Execute via: WunderTrading MCP → modify TP/SL on the position.

### 2. Backtesting at Scale

Use TradingView MCP tools:
- `backtest_strategy` — test one of 6 strategies with Sharpe, Calmar, Max DD, Profit Factor
- `compare_strategies` — rank all 6 on the same symbol
- Brute-force parameter ranges (bar count, volume threshold, timeframe)

### 3. Monte Carlo Simulation (quantitative technique)

⚠️ **This user's personal strategy is NOT Monte Carlo** — it's a bounded Martingale (conviction hold, add on dip, never sell at loss). Monte Carlo simulation is a useful general quant tool for path-dependent risk estimation, not a label for their approach. See "User's Specific Approach" below.

- Simulate 10,000+ paths of the strategy on historical data
- Assess: probability of being underwater > X%, average max drawdown, 95th percentile worst case
- Validate position sizing decisions

### 4. Trade Logging & Meta-Analysis

- Pull trade history from WunderTrading
- Tag each entry with market context at time of entry (fear/greed, OI regime, funding regime)
- Discover pattern improvements: *"sweeps in extreme fear regimes recover 40% faster"*

## User's Specific Approach (for this user)

- **Asset:** BTC only (the axiom being BTC will always go up eventually)
- **Entry signal:** Volume sweep — every N bars, volume jumps 40%+ above rolling average
- **Risk management:** Zero leverage, small position size, perpetual hold
- **Sizing philosophy:** Bounded Martingale — conviction hold + double down on BTC dip at small size. Small base entry, add on drawdown, never sell at a loss. TP-only exits.
- **⚠️ Key correction:** NOT Monte Carlo. That was a Hermes memory error. The approach is a bounded Martingale where increasing position size on drawdown is intentional, but the TP must scale with the blended cost basis — fixed 10% TP after a dip-add produces asymmetric risk/reward.
- **Current execution:** TradingView Pine Script → WunderTrading → Hyperliquid
- **Pain point:** Fixed TPs cap the upside of conviction adds; needs dynamic TP that scales with blended cost basis
- **Project evolved toward:** Multi-trader profiling pipeline (Phase 1: analyze/digest → backtest → indicators; Phase 2: execution layers). See `references/trader-profiling-pipeline.md`.

## Pitfalls

- **Do NOT** propose building execution infrastructure from scratch — the user already has TradingView + WunderTrading + Hyperliquid running profitably
- **Do NOT** propose backtesting the core strategy — they've validated it in production for months
- **Do NOT** suggest Alpaca for this user — Hyperliquid is a different venue with different liquidity (perps-focused DEX vs. brokerage)
- **Do NOT** pitch fixed TPs as the solution — context-dependent exits are the actual value Hermes adds
- **WunderTrading middleman:** the user's execution path goes through WunderTrading, which may not expose all Hyperliquid features. For raw chain data (order book, on-chain positions), fall back to the Hyperliquid Python SDK directly
- **Position monitoring frequency:** match the strategy's timeframe. A 1h strategy polls every 1-2 hours; a 4h strategy polls less often. Over-monitoring is noise, under-monitoring misses context shifts

## Related Files

- `references/architecture.md` — full MCP stack data flow and detail on each server
- `references/trader-profiling-pipeline.md` — multi-trader YouTube content extraction, regime-tagged profiling, backtest-to-indicator pipeline, and two-phase build plan
