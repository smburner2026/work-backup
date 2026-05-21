# agent-data Evaluation

**Date:** 2026-05-21
**URL:** agent-data.dev
**Package:** agent-data@0.8.0 (npm, proprietary)
**Verdict:** NO-GO

## What it is
Proprietary CLI tool (Aiptiq Labs) that acts as a marketplace/API gateway for structured real-time data. Single CLI interface (`agent-data search → call → structured JSON`). Pay-per-call ($0.008/call).

Current endpoints: flights (status/fares), restaurant reservations (Resy/OpenTable), AI blog aggregation (OpenAI/Anthropic/etc.), social media (HN/Lobsters), events (coming soon).

## Evaluation for Quant Trading Agent

**Target use case:** Real-time market data for the BTC vol sweep / quant trading agent.

**Existing stack vs agent-data:**

| Trading Need | Current Solution (free) | agent-data |
|---|---|---|
| OHLCV / technical analysis | TradingView MCP | ❌ Doesn't exist |
| Crypto spot/futures prices | CoinGecko MCP | ❌ Doesn't exist |
| OI / funding / liquidations | Coinalyze REST API | ❌ Doesn't exist |
| Trade execution | WunderTrading + Hyperliquid API | ❌ Doesn't exist |
| Market sentiment (X/Reddit) | None currently | ❌ Only HN/Lobsters |

**Assessment:** Zero overlap with any trading/crypto/market data category. Even if crypto endpoints were added, it would be a paid wrapper around the same free APIs already used via MCP — but at $0.008/call.

**Verdict:** Not useful for the trading use case. The architecture (self-discovering CLI) is well-designed but the data categories (travel/food/media) are entirely orthogonal to trading needs. No action taken.

**Where it WOULD be useful:** Consumer-facing agent tasks — flights + dinner + blog monitoring. Not relevant to current project priorities.
