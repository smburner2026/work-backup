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
| **Custom TV Webhook MCP** (see below) | Reliable signal capture from custom Pine Scripts, bypasses broken CSV exports | `python3 mcp_server.py http` (from `bambam-fatcat-project/`) |

### Custom Webhook Signal Capture MCP

The TradingView MCP (`atilaahmettaner`) cannot load custom Pine Scripts or read indicator plot values. For signal capture from custom scripts (BAMBAM, FATCAT, etc.), use the **webhook bridge** pattern instead:

1. **MCP server** (`mcp_server.py`) listens on port 8080, stores every POST in SQLite
2. **BAMBAM** uses `bambam-signal-capture.pine` — has `alertcondition()` with structured JSON payload
3. **FATCAT** (invite-only) uses a TV chart condition alert with template variables
4. **⚠️ Bar Replay** — visual signals only (alerts do NOT fire during replay, see pipeline verification below)
5. DB exports directly to the brute-force sweep (`sweep.py`)

Full setup: `references/webhook-signal-capture.md` under `pinescript-indicator-dev` skill.

### Pipeline Verification (Webhook Testing)

**⚠️ Known Limitation: TradingView Bar Replay does NOT trigger `alert()` or `alertcondition()` webhooks.** Visual signals (plotshape, bgcolor, labels) render correctly during replay, but the actual `alert()` call never executes — no HTTP POST is sent. This is a TradingView platform restriction: alerts only fire on live real-time bars.

To test the webhook → MCP server → SQLite pipeline, use one of these:

**Option A — Live bar (automatic):**
The first live signal from the indicator POSTs to the webhook automatically. Check arrival:
```bash
curl http://<host>:<port>/stats
curl http://<host>:<port>/signals
```

**Option B — Manual POST simulation (recommended for testing):**
Send a test payload directly to confirm the server receives and stores:
```bash
curl -X POST http://<host>:<port>/ \
  -H "Content-Type: application/json" \
  -d '{"source":"bambam","direction":"bear","symbol":"BTCUSDT","timeframe":"5","price":75000,"timestamp":"1773619200000"}'
```

**Option C — Replay for visual validation only:**
Use bar replay to confirm the indicator fires correct signals on historical bars, then manually POST those signal parameters. This separates visual validation from pipeline testing.

**Note on timeframe field:** TradingView's Pine Script sends the interval as a number string (e.g., `"5"` for 5 minutes, `"15"` for 15 minutes), NOT `"5m"` or `"15m"`. DB queries filtering by timeframe must use `WHERE timeframe='5'`, not `timeframe='5m'`.

Convert DB timestamps (Unix epoch ms) with:
```python
from datetime import datetime; print(datetime.utcfromtimestamp(1779474945000/1000))
```

### Database Status Reporting

When reporting signal DB status to the user:

- **Always clarify the time window.** "5 signals total" is misleading if one is a test entry. Say "X signals since Y time" or "X real signals, excluding test entries."
- **Test entries** (signal #1 with placeholder data like `"timestamp":"test"`, price=78000) should be explicitly excluded from operational counts unless the user asks for total.
- **Last signal timestamp** is the most useful metric — "last signal at 19:31 UTC" tells the user whether the pipeline is live vs. stale.
- **Fatcat count should be reported separately** from BAMBAM — zero fatcat entries when the alert isn't configured yet is expected, not suspicious.

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

## CSV Ground-Truth Comparison

When the user provides a CSV export from a target indicator (e.g., FATCAT strategy report), use this methodology to compare your replica against it:

### 1. Determine what the CSV represents

First question: is this the raw signal output from the indicator, or a strategy report with position-building logic applied?

**Raw signal output** = one row per signal, minimal columns (timestamp, price, direction, maybe signal name). These can be directly compared against your replica's signal timestamps.

**Strategy/position report** = trade-level data with entries, exits, P&L, size, excursion metrics. These may include multiple entries per signal (e.g., a Martingale grid building a position across levels). The entries may be generated by a DIFFERENT module than the core reversal signals.

**Signal name pattern:**
- L1, L2, L3, ... L(N) = sequential grid levels within a single position — these are NOT independent signal detections
- "Buy"/"Sell" or "Bull"/"Bear" = directional signal names — probably raw indicator output
- Arrow/triangle references = raw indicator output

**Quick diagnostic: check if entries correspond to 200-bar lows/highs.** If at least one entry fires on a bar that is NOT a new 200-bar extreme, the CSV entries are from a position-builder, not reversal signals. Do not waste time fitting reversal logic to them.

**⚠️ Critical: CSV files from Telegram DMs are cached and may be cleaned between sessions.** When the user shares a CSV file in a Telegram message, it arrives as a cached document at `/root/.hermes/cache/documents/doc_<hash>_<name>.csv`. These cached files DO NOT persist indefinitely — Hermes's session storage may clean them. To avoid losing ground truth data:

1. **On receipt: immediately copy the CSV to a permanent location** (e.g. `/root/work/trading/csv/` or the project's `data/` directory).
2. **Log entry timestamps and key values in session notes** — the data is recoverable via `session_search` even if the file is cleaned.
3. **If the file is gone next session, use the logged timestamps to reconstruct** the analysis.

Also: the BOM character (`\ufeff`) is present in TV-exported CSVs and will cause `csv.DictReader` header mismatches (KeyError on 'Trade #'). Strip it before parsing:

```python
content = open(path).read()
if content.startswith('\ufeff'):
    content = content[1:]
reader = csv.DictReader(content.splitlines())
```

### 2. Align timestamps

Load the CSV, parse entry timestamps, and align with exchange OHLCV data. Validate that the prices and timestamps are consistent between sources.

### 3. Run replica against same data

Fetch OHLCV data for the same date range from a compatible exchange. Run the replica signal engine with all parameter combinations from the selectivity patterns. Compare:

| Metric | What it tells you |
|---|---|
| Exact timestamp match (same 5m bar) | Signal fires on same bar |
| ±N bars fuzzy match | Signal fires nearby — timing offset or different exchange price |
| Total signal count | Matching density — same number of signals over same period |
| Signal distribution over time | Clusters matching — same response to market events |

### 4. Interpret zero-match results

If your replica produces zero exact matches across all parameter settings, the CSV entries are likely from a DIFFERENT signal logic than what your replica implements. Options:
- The CSV is from a different indicator mode (e.g., position-builder grid vs. reversal triangles)
- The CSV includes additional filtering (position sizing, drawdown limits) beyond signal detection
- The CSV uses a different data source or timeframe than your OHLCV data

Document the finding and report back — don't force-fit parameters to achieve a false match.

### 5. Data sourcing for historical OHLCV

When Binance is blocked (HTTP 451), use these alternatives:

| Source | Endpoint | Notes |
|---|---|---|
| **Bitstamp** (recommended) | `https://www.bitstamp.net/api/v2/ohlc/btcusd/` | 5m data back to 2022+. Param: `step=300` (5min), `limit=1000`, paginate via `end` timestamp. Free, no key. Confirmed working from restricted VPS. |
| **CoinGecko** | `https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range` | Daily data only (93 points over 93 days for 5m = daily OHLC). Not granular enough for signal comparison. |
| **OKX** | `https://www.okx.com/api/v5/market/history-candles` | Only keeps ~3 days of 5m history. Unusable for extended backtests. |
| **Kraken** | `https://api.kraken.com/0/public/OHLC` | Only keeps ~3 days of 5m data. Unusable for extended backtests. |

See `references/comparing-replica-vs-ground-truth.md` for the full session methodology and FATCAT "Single Direction" analysis.

### Three-Part Breakdown

Every TradingView overlay indicator decomposes into:

1. **Shared Calculations** — the data foundation (volume decomposition, ATR, price sources). Identify what every downstream section consumes.
2. **Signal Logic** — the trigger conditions. Walk through each variable, what it computes, and how it contributes to the final boolean. Trace the chain: raw data → intermediate → condition → signal.
3. **Visual/Alert Layer** — plotting, bands, fills, alert conditions. The rendering is separate from the logic.

### Reverse-Engineering Hidden Formulas

When a modified/paid indicator is more selective than an open-source original but the source code is hidden:

1. **Identify the constraint space** — which parameters/conditions can change without breaking symmetry? On a symmetrical indicator (bull + bear treated equally), only shared knobs can reduce both sides equally.
2. **Candidate enumeration** — list every plausible modification (< 200 combos for most indicators):
   - Parameter tightening (ratio thresholds, multiplier bumps)
   - Boolean logic changes (removing OR limbs, adding AND gates)
   - New gate conditions (band penetration, trend filter, ATR distance)
3. **Signal disagreement data** — timestamps where original fires but modified doesn't. Each pair eliminates candidate formulas.
4. **Brute-force grid search** — simulate every candidate against historical OHLCV, score by match to observed signal pattern. Winner is the recovered formula.
5. **The pipeline works** even when the only input is screenshots — timestamps anchor the simulation, OHLCV is pulled independently from exchange APIs. No need for the user to export data.
6. **⚠️ Critical: validate at timestamp level, not count level.** Signal count alignment (e.g., 19 vs 18) is NOT evidence of correct replication. I fell into this trap. Run your candidate against the user's actual CSV entries (if provided) and check exact bar-matches. If the user has already shared CSV entries, test against those FIRST — don't run off to do independent density analysis.

### Iterative Hypothesis Testing (when user has chart access)

### Iterative Hypothesis Testing (when user has chart access)

When the user can test variants directly on TradingView but cannot share the hidden source:

1. **Start with the original formula** — the baseline is known
2. **Identify the modification space** — symmetrical indicators have only shared knobs; changing only one side means a directional filter was added
3. **Create ranked hypothesis variants** — from least to most aggressive:
   - Parameter tightening (mildest, most likely)
   - Boolean logic changes (structural, moderate)
   - Confluence gates (adds new conditions, most aggressive)
4. **Ship each variant as a standalone Pine Script** — user pastes into TV, overlays against the hidden indicator
5. **Collect binary feedback** — "fires more/less/same", "still not as selective", "closer but misses the big ones"
6. **Iterate** — combine successful changes, discard failed ones, tighten further if needed

This loop typically converges in 2-3 iterations. Each iteration teaches which modification axis matters most for that specific indicator class.

### Common Pine Script Selectivity Patterns

When an indicator needs to fire less often on LTF, these are the standard modulations (in order of typical use):

| Pattern | Code Change | Effect | Use When |
|---|---|---|---|
| **Tighten ratio threshold** | `0.05` → `0.03` or `0.02` | Removes marginal signals | Exhaustion/delta-style indicators |
| **Volume multiplier** | `vol > avgVol` → `vol > avgVol * 1.5` | Only genuine climax bars | Volume-gated reversal signals |
| **Exhaustion-only** | Remove `or vd<0` / `or vd>0` limbs | Pure exhaustion, no trend confirmation | Indicator fires on both imbalance AND exhaustion; user wants only the latter |
| **Band confluence gate** | Add `close < thresholdDown2` or `close > thresholdUp2` | Signals only at statistical extremes | VWAP/Bollinger-style bands overlaid with signals |
| **ATR minimum move** | Add `move > atr(14) * N` | Ignores shallow touches | Range/trend hybrid indicators |

The "exhaustion-only" pattern is particularly powerful: changing `(isLessRatio or vd < 0)` to just `isLessRatio` removes all signals where directional volume confirms the move, keeping only the bars where buyers and sellers fought to a near-draw despite the price extreme. This is the purest climax signature.

### Specific Indicators (this user)

- **BAMBAM (original):** `/root/work/trading/pinescript/bambam-vwap-bands.pine` (103 lines, SHA256 `24c01bc...a7ea7c`). BAMBAM signal logic: 200-bar lookback, volume delta ratio < 0.05 exhaustion filter, high-vol gate (`vol > avgVol`). VWAP bands: split buy/sell-volume VWAP at 1.5σ and 2.0σ. Plots white ▲ (bull) / black ▼ (bear). Offset=-1 prevents repaint.
  - **Signal mechanics:** Uses tick-rule volume decomposition (`vb = volume * (close-low)/(high-low)`). Volume delta `vd = vb - vs`. At a 200-bar extreme, fires when volume is above average AND either (a) delta ratio < 5% (exhaustion) OR (b) delta is net negative/positive (directional confirmation). This dual-path design means signals fire on both climax bars AND strong directional thrusts.
- **POCKETBAMBAM:** Strategy version of BAMBAM. Not a separate indicator — same script, same parameters. POCKETBAMBAM = BAMBAM signals + 1-bar delay (standard strategy next-bar-open execution). User chart confirmed: OG BAMBAM fires 1 candle before POCKETBAMBAM entries. Do NOT confuse POCKETBAMBAM with BAMBAM — they share the same signal engine; POCKETBAMBAM is the strategy wrapper, not a different signal generator.
- **Ferocious Fatcat (selective fork):** TradingView invite-only script by same author (BAMBAMTHECHONKMASTER). Green ▲ / red ▼ arrows. More selective than POCKETBAMBAM on both sides symmetrically. The hierarchy on chart (most signals to least): BAMBAM OG > POCKETBAMBAM > FATCAT.\n  - **Volume source theory DISPROVEN definitively by `takerbuyvol` compile error (CE10272).** The user's broker does not provide real taker-buy volume — FATCAT cannot use a data field that doesn't compile.\n  - **FATCAT vs BAMBAM subset relationship — REVISED (May 2026).** Initial v2-period analysis (22 days) showed 6/6 timestamp overlap, suggesting FATCAT was a clean subset of POCKETBAMBAM. A subsequent 90-day 5m comparison with identical strategy parameters (single TP 1%) disproved this: **33 FATCAT entries on non-edge days had NO corresponding POCKETBAMBAM entry** — 14 shorts and 21 longs on dates with zero BAMBAM activity. The subset relationship does NOT hold at scale. Possible explanations:\n    (a) Different signal logic between the two indicators despite shared author and naming\n    (b) POCKETBAMBAM's strategy was suppressed by Feb 20-28 drawdown (massive pyramid cluster that hit margin call), leaving it unable to take new signals for extended periods while FATCAT's different entry logic kept it active\n    (c) The single-TP-at-1% strategy structure penalizes BAMBAM's entry frequency differently than FATCAT's\n    Resolution: run BAMBAM's RAW indicator logic (not the strategy) against matching OHLCV data to determine if the raw signals exist on those unmatched dates.
  - **RESOLVED (May 2026):** Raw BAMBAM strategy export confirmed the rectangle IS square — all 72 FATCAT entries match a raw BAMBAM signal within ±10 minutes (434 raw BAMBAM signals over 90 days, 248S + 186L). The 33 previously unmatched FATCAT entries existed in raw BAMBAM but POCKETBAMBAM's strategy couldn't enter them (suppressed by Feb drawdown). FATCAT filters 83.4% of raw BAMBAM signals (90.3% of shorts, 74.2% of longs).
  - **Brute-force reverse-engineering methodology:** (1) Confirm rectangle via raw strategy export, (2) Sweep timestamp-only filters — max F1=0.393 (cooldown alone can't crack it), (3) Spot OHLCV cannot reproduce perp signals (Binance.US produces 245 vs TV's 434, only 37/72 FATCAT matches), (4) Need perp-specific volume features from TV via feature-export strategy, (5) Export features embedded in strategy comment strings (vol|vd|avgVol|volRatio|vdRatio|vb|vs), (6) Sweep volume parameters — F1 capped at 0.38 even with real perp data, (7) ML classifiers (decision tree, random forest, gradient boosting) overfit to CV F1=0.15-0.18, (8) KS tests confirm vb (p<0.001), vol (p=0.008), volRatio (p=0.006) statistically significant but overlap too large for separation, (9) FATCAT's filter likely uses taker buy volume or a stateful mechanism not available in candle-body estimates — F1 wall at ~0.38-0.39 across ALL approaches.
  - **Feature export technique:** TradingView Strategy Tester CSV does NOT include `plot()` values. Embed features in `strategy.entry(comment=str.tostring(val1)+"|"+str.tostring(val2)+...)`. Parse with Python `row['Signal'].split('|')`. Do NOT use `str.tostring(val, "#.##")` format strings — they cause null translation errors in Pine v6.
  - **Statistical confirmation (KS test):** At-sample, FATCAT-selected BAMBAM signals have significantly different volRatio (p=0.006), vol (p=0.001), and vb (p<0.001) distributions compared to rejected signals. But the distributions overlap too much for classification — precision at any volRatio threshold stays below 31% for longs and 15% for shorts.
  - **⚠️ Binance.US spot ≠ TV perp for volume-dependent indicators.** 49,783 5-min candles downloaded; price diff is small ($47 mean = 0.07%) but volume patterns are fundamentally different. Spot data cannot reproduce perp indicator signals.\n  - **CSV export discrepancy:** On year-long export, PBB showed ~60 entries vs FATCAT ~200 — inverting chart hierarchy. This is an export/settings bug. v2 period (22 days) showed correct relationship (PBB=21, FC=6). Solution: use custom webhook capture server instead of manual CSVs.
- **Both saved with backups:** Primary at `/root/work/trading/pinescript/`, copies at `/root/work/`, `/root/.hermes/safekeep/`.

### Feature Export Technique — Delta/Change Features (May 2026)

The initial 7-feature export (volume body + indicator levels only) hit an F1 ceiling of ~0.40. A 24-feature export added delta/change values:
- `rsi14_delta`, `rsi7_delta` — RSI change over 5 bars
- `macd_hist_delta` — MACD histogram change over 3 bars
- `price_mom5` — 5-bar price return %
- `volRatio_delta`, `vdRatio_delta` — volume ratio change
- `ema21_cross` / `ema50_cross` — binary flags for recent EMA crosses

**Result:** Deltas showed statistically significant KS separation (p<0.001 for rsi14_delta, macd_hist_delta, price_mom5) but offered **zero practical improvement** — F1 ceiling remained at 0.40, and combined level+delta F1 dropped below baseline. The delta features capture the same information as levels (redundant), and the EMA cross flags were completely random (KS<0.05, p>0.99).

**Lesson:** For FATCAT-style reversal signals, single-bar change values at the signal bar do not add information beyond what levels already encode. The signal at bar N already implies the change — a separate delta export just confirms what the level already says. True improvement requires multi-bar conditional logic (if bar N-1 had X and bar N has Y then signal) that requires Pine Script experimentation on TV, not offline analysis.

**Pine v6 delta export code:**
```pinescript
// Global-scope delta computation (avoids barssince conditional error CW10002)
rsi14_delta = ta.rsi(close, 14) - ta.rsi(close, 14)[5]
macd_hist_delta = histLine - histLine[3]
price_mom5 = (close - close[5]) / close[5] * 100
volRatio_delta = volRatio - volRatio[3]

// Cross flags — compute at global scope, then use in conditionals
cross_above_ema21 = close[1] > ema21[1] and close[2] <= ema21[2]
cross_below_ema21 = close[1] < ema21[1] and close[2] >= ema21[2]
bars_since_ema21_bull = ta.barssince(cross_above_ema21)
bars_since_ema21_bear = ta.barssince(cross_below_ema21)
ema21_bull_recent = bars_since_ema21_bull <= 3 and not na(bars_since_ema21_bull)
ema21_bear_recent = bars_since_ema21_bear <= 3 and not na(bars_since_ema21_bear)
```

**Key Pine v6 pitfalls for feature exports:**
- `ta.barssince()` inside conditional expression → CW10002. Extract to global var before using in boolean.
- String concat with `\` at line end → CE10156. Use single continuous line with `+`.
- `if bull` without indent on body → CE10013. Body must be indented 4 spaces.

### Vision Model Configuration for Charts

DeepSeek models (v4-flash, v4-pro) do NOT support image input — `vision_analyze` fails with `unknown variant 'image_url', expected 'text'`. To analyze TradingView chart screenshots, either:

1. **Switch main model:** `/model anthropic/claude-sonnet-4` (supports vision on OpenCode Go), then switch back after analysis.
2. **Configure auxiliary vision routing** (keeps DeepSeek for chat, Claude for images only):
   ```bash
   hermes config set auxiliary.vision.provider opencode-go
   hermes config set auxiliary.vision.model anthropic/claude-sonnet-4
   ```
   Then `/reset` or start a new session.

**OpenCode Go vision-capable models (confirmed):**

| Model | Vision | Notes |
|---|---|---|
| `anthropic/claude-sonnet-4` | ✅ | Best chart analysis — reads timestamps, prices, arrow positions |
| `anthropic/claude-3.5-sonnet` | ✅ | Excellent, slightly cheaper |
| `openai/gpt-4o` | ✅ | Good, sometimes less precise on small text |
| `kimi-k2.6` | ✅ | Strong multimodal, excellent chart detail |
| `kimi-k2.5` | ✅ | "Visual Agentic Intelligence" — 1T params |
| `qwen3.6-plus` | ✅ | Native multimodal |
| `qwen3.5-plus` | ✅ | Native image understanding |
| `mimo-v2-omni` | ✅ | "Omni" = multimodal by design |
| `minimax-m2.7` | ✅ | Vision-capable |
| `glm-5.1` | ❌ | Text-only |
| `glm-5` | ❌ | Text-only, 744B active but no image input |
| `deepseek-v4-pro` | ❌ | No vision support at all |
| `deepseek-v4-flash` | ❌ | No vision support at all |

⚠️ **Known Hermes bug:** OpenCode Go vision models may fail with `No media-understanding provider registered for opencode-go` even when the model supports vision. If this happens, switch to `anthropic/claude-sonnet-4` as the main model temporarily, or use the auxiliary vision routing workaround above.

See `references/chart-vision-workflows.md` for OCR fallback patterns and color-based arrow detection when vision isn't available.

## User's Specific Approach (for this user)

- **Asset:** BTC only (the axiom being BTC will always go up eventually)
- **Entry signal:** Volume sweep — every N bars, volume jumps 40%+ above rolling average. The BAMBAM indicator (above) is the foundation of the trading system; Ferocious Fatcat is the LTF-selective variant.
- **Risk management:** Zero leverage, small position size, perpetual hold
- **Sizing philosophy:** Bounded Martingale — conviction hold + double down on BTC dip at small size. Small base entry, add on drawdown, never sell at a loss. TP-only exits.
- **⚠️ Key correction:** NOT Monte Carlo. That was a Hermes memory error. The approach is a bounded Martingale where increasing position size on drawdown is intentional, but the TP must scale with the blended cost basis — fixed 10% TP after a dip-add produces asymmetric risk/reward.
- **Current execution:** TradingView Pine Script → WunderTrading → Hyperliquid
- **Pain point:** Fixed TPs cap the upside of conviction adds; needs dynamic TP that scales with blended cost basis
- **Current direction (May 2026):** FATCAT reverse-engineering hit an F1 ceiling at ~0.38-0.40 across all offline approaches (ML, KS tests, threshold sweeps, delta features). Pivoted to building **Swing Research pipeline** from scratch — a BAMBAM fork optimized directly for swing high/low capture. Pipeline structure at `swing_research/` with ATR-based ZigZag labeling, triple-barrier labels, and chronological train/val/test splits. Best v3 labels (May 23): 127/431 True across 90 days (29.5%) using exc≥7ATR, hold≥24bar, prox≤24bar. Full methodology in `tv-feature-export` skill's `references/swing-research-pipeline.md`. Next: train LightGBM per-direction model on the 1-year 1,850-signal export.

## Pitfalls

- **Do NOT** propose building execution infrastructure from scratch — the user already has TradingView + WunderTrading + Hyperliquid running profitably
- **Do NOT** propose backtesting the core strategy — they've validated it in production for months
- **Do NOT** suggest Alpaca for this user — Hyperliquid is a different venue with different liquidity (perps-focused DEX vs. brokerage)
- **Do NOT** pitch fixed TPs as the solution — context-dependent exits are the actual value Hermes adds
- **WunderTrading middleman:** the user's execution path goes through WunderTrading, which may not expose all Hyperliquid features. For raw chain data (order book, on-chain positions), fall back to the Hyperliquid Python SDK directly
- **Position monitoring frequency:** match the strategy's timeframe. A 1h strategy polls every 1-2 hours; a 4h strategy polls less often. Over-monitoring is noise, under-monitoring misses context shifts
- **Offline analysis ceiling for hidden indicators:** When reverse-engineering a selective indicator (FATCAT), offline analysis of exported features hit a hard F1 ceiling at ~0.38-0.40 regardless of approach (ML, KS tests, threshold sweeps, delta features, EMA cross flags). The actual filter required multi-bar conditional logic that can only be tested via Pine Script on TradingView. When offline analysis plateaus at a ceiling, pivot to building from scratch with a clear optimization target rather than continuing to probe the hidden filter.
- **Swing hit rate ≠ F1 against rejection label:** FATCAT reconstruction used F1 (precision/recall against a "rejected" label), which measures how well we predict the filter's decisions. SwingCatcher instead optimizes directly for "did price move in signal direction within 4 hours." The latter is a harder, more realistic target — and a higher-quality signal. When rebuilding from scratch, use a concrete market-outcome target rather than replicating a human filter decision.

## Related Files

- `references/architecture.md` — full MCP stack data flow and detail on each server
- `references/wundertrading-webhook-format.md` — WunderTrading webhook message format reference: two modes (strategy comment-based vs JSON), full JSON field reference, compatibility guidance when swapping indicators, TradingView alert lifecycle (persistence after removal), and Pine Script construction examples.
- `references/trader-profiling-pipeline.md` — multi-trader YouTube content extraction, regime-tagged profiling, backtest-to-indicator pipeline, and two-phase build plan
- `references/chart-vision-workflows.md` — vision model routing, OCR fallbacks, color-based arrow detection
- `references/pine-script-selectivity-patterns.md` — concrete Pine Script patterns for making indicators more/less selective: tighten ratio thresholds, volume multipliers, exhaustion-only boolean changes, band confluence gates, ATR minimum moves. Includes before/after code and expected signal reduction per pattern.
- `references/comparing-replica-vs-ground-truth.md` — methodology for comparing indicator replica output against target CSV entries, including the FATCAT "Single Direction" mode analysis (May 2026 session) and Bitstamp data sourcing fallback.
- `references/reverse-engineering-filter-methodology.md` — step-by-step methodology for reverse-engineering a hidden indicator filter: rectangle verification, timestamp-only sweep, perp data sourcing, feature export strategy, and brute-force parameter sweep. Includes key findings from BAMBAM→FATCAT analysis (F1=0.393 max for timestamp-only, spot≠perp volume data, 434→72 signal reduction).
- `references/swingcatcher-optimization.md` — SwingCatcher (May 2026): BAMBAM+indicator layer optimization targeting swing high/low capture. Best configs: LB=400 LR=0.10-0.20 VM=0.5 AND + vdRatio@70-75%+rsi14_delta@70% → 53-73% hit rate. AND mode dominance confirmed. EMA cross flags and delta features ruled out. Results saved in `swingcatcher_results.json`.
