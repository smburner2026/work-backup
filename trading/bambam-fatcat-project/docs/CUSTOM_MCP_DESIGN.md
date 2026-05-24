# BAMBAM-FATCAT Custom TradingView MCP — Design Notes

## The Problem

The existing `atilaahmettaner/tradingview-mcp` runs 6 built-in strategies. It cannot load custom Pine Scripts (BAMBAM, FATCAT, or any invite-only indicator). It has no tool to read `plotshape` events or indicator trigger timestamps.

## What We Need

A custom MCP server that:
1. Connects to TradingView's chart data API (same data as the TV web app)
2. Loads a custom Pine Script indicator onto a chart
3. Reads indicator output values at each bar (plot values, plotshape events)
4. Returns: symbol, timestamp, signal type, price for every trigger event
5. Can do this historically (not just real-time) — scan N bars of history

## Architecture Options

### Option A: Headless Browser (Puppeteer/Playwright)
- Spawn a headless Chromium that loads tradingview.com
- Inject the Pine Script via the Pine Editor API
- Read indicator values from the chart DOM
- Return structured signal data

**Pros:** Full TV capability, can load ANY Pine Script from the TV library
**Cons:** Fragile (DOM-dependent), heavy (requires Chromium), rate-limited by TV login

### Option B: Pine Script Webhook Bridge
- Add a small Pine Script snippet to BAMBAM/FATCAT that pings a webhook on each signal
- Webhook hits a local MCP server that logs the timestamp
- Structured query endpoint aggregates logs

**Pros:** Lightweight, real-time, deterministic
**Cons:** Requires modifying the Pine Script (can't do for invite-only scripts), only captures signals going forward

### Option C: Pythin REST Client (TV Chart API)
- TV has undocumented internal APIs used by the web app
- `https://charting*.tradingview.com/` endpoints
- Can fetch chart data, study templates, and indicator outputs

**Pros:** Direct data, no browser needed
**Cons:** Unofficial, may break, requires reverse-engineering auth tokens

## Recommended: Option A + B Hybrid

Phase 1 — **Webhook Bridge (immediate, for BAMBAM):**
Add `alertcondition(bullSignal, "HTTP", url)` to the BAMBAM indicator → webhook logs into a local MCP server. Gives us forward-looking signal data instantly. No invite-only issues (BAMBAM is open).

Phase 2 — **Headless Scanner (for FATCAT and others):**
A Python script using Playwright that logs into TV, loads a chart, applies the indicator, and reads plot data for a given date range. Returns a structured JSON of signal events. This handles invite-only scripts since they're available in your TV account.

Phase 3 — **Unified MCP Server:**
Wraps both Phase 1 and Phase 2 as MCP tools. Tool `read_indicator_signals(indicator_name, symbol, timeframe, date_range)` returns all trigger events as structured data. Tool `subscribe_indicator(indicator_name, webhook_url)` sets up the real-time bridge.

## Priority

The brute-force sweep (already written at `sweep.py`) needs only the CSV data we have. The MCP is for phase 2 — validating the sweep results against live TV data and scaling to more indicators.

To proceed with Phase 1: add `alertcondition()` HTTP webhooks to the BAMBAM Pine Script. That alone decouples signal capture from CSV exports.
