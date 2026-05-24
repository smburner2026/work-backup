# Webhook-Based Signal Capture (Alternative to CSV Exports)

When TradingView CSV exports produce inconsistent results (missing rows,
different date ranges per export, PBB showing fewer entries than FATCAT
despite the chart showing the opposite), use **TV alert webhooks** as the
capture mechanism instead.

## Architecture

```
TradingView (your browser)
  ├── BAMBAM indicator (alertcondition → JSON webhook payload)
  ├── FATCAT indicator (chart condition alert → JSON webhook)
  └── ⚠️ Bar Replay mode → visual signals ONLY (alerts do NOT fire)
         ↓ HTTP POST
Local MCP server (mcp_server.py)
  └── SQLite database: signals.db
         ↓ query
  sweep.py reads clean time-aligned data
```

## Setup

1. Start the MCP server: `python3 mcp_server.py http`
   - Listens on port 8080, writes every POST to `signals.db`
   - `GET /stats` — check count
   - `GET /signals?source=fatcat&start=2025-01-01` — query

2. **BAMBAM** uses `bambam-signal-capture.pine` which has structured
   JSON built into `alertcondition()`. Create alert pointing at
   `http://localhost:8080`.

   ⚠️ **Pine Script v6:** The `makePayload` function MUST be a single-line
   `=>` arrow expression — multi-line `+` concatenation and `str.format()`
   both fail with CE10123. Use the known-working template from
   `templates/bambam-signal-capture.pine`; do not rewrite from scratch.

3. **FATCAT** is invite-only, can't modify source. Use TV's chart
   condition alert: "When Ferocious FATCAT plots a Buy shape → webhook".
   Message template:
   ```json
   {"source":"fatcat","direction":"bull","symbol":"{{ticker}}",
    "timeframe":"15m","timestamp":"{{timenow}}","price":{{close}}}
   ```

4. **⚠️ Bar Replay limitation:** Right-click → Bar Replay → set start
   date → speed: max. Visual plotshape markers render correctly, but
   **alerts (and thus webhook HTTP POSTs) do NOT fire.** This is a
   TradingView platform restriction — alerts only trigger on live
   real-time bars. Use bar replay for visual validation only; test
   the actual pipeline via live signals or manual POST.

## ⚠️ Bar Replay Does NOT Fire Webhooks

TradingView's Bar Replay mode replays historical candles and re-calculates indicators — visual markers (plotshape, bgcolor, labels) render correctly. However, **`alert()` and `alertcondition()` calls do NOT execute during bar replay.** No HTTP POST is sent, regardless of signal conditions. This is a platform restriction: alerts only fire on live real-time bars.

**Impact:** You cannot use bar replay to populate the signal database or test the webhook pipeline end-to-end. Visual confirmation of signal timing works, but no data reaches the MCP server.

**Alternatives for testing:**
1. Wait for a live bar to trigger the alert naturally
2. Manually POST a test payload to verify the server: `curl -X POST http://<host>:<port>/ -H "Content-Type: application/json" -d '{"source":"bambam","direction":"bear","symbol":"BTCUSDT","timeframe":"5","price":75000,"timestamp":"1773619200000"}'`
3. Use bar replay to identify signal timestamps, then batch-POST those timestamps manually

**Timeframe field format:** Pine Script alert messages send the interval as a number string — `"5"` for 5 minutes, `"15"` for 15 minutes, `"15S"` for 15 seconds. Do NOT query for `"5m"` or `"15m"` in the database; match `"5"` and `"15"` instead.

## Why This Fixes the CSV Problem

| Problem | CSV Exports | Webhook Capture |
|---|---|---|
| Row drops | Random truncation | Every signal captured |
| Date range mismatch | Manual export each time | One replay pass, both indicators |
| Different runs | Separate sessions | Same chart, same Bar Replay |
| Manual overhead | Export → download | Batch via manual POST |

## MCP Server (mcp_server.py)

Two modes:
- `python3 mcp_server.py http` — HTTP server for TV webhooks
- `python3 mcp_server.py mcp` — stdio MCP protocol for Hermes

Four MCP tools:
- `capture_signal` — store a signal (for Hermes-native integration)
- `query_signals` — get signals by source/date range
- `get_stats` — DB statistics
- `export_json` — dump to JSON file for sweep.py

## CrITICAL: The TV MCP (atilaahmettaner) Cannot Do This

The existing `tradingview-mcp-server` package has 30+ tools but NONE of
them can:
- Load a custom Pine Script (BAMBAM, FATCAT, or any custom script)
- Read indicator plot values or plotshape events
- Extract strategy trade logs programmatically

It only runs 6 hardcoded strategies (RSI, Bollinger, MACD, EMA cross,
Supertrend, Donchian). Do NOT propose using the TV MCP for signal
extraction from custom indicators — use the webhook + local server
pattern instead.

## Bar Replay Constraints

- Requires premium TradingView account (the user has one)
- Ties up a browser tab during replay (90 days at max speed ≤ 1 hour)
- Can run in a second tab while the live trading tab stays active
- TV allows multiple alerts on the same indicator — create a second
  alert pointed at localhost, leave the WunderTrading alert intact
