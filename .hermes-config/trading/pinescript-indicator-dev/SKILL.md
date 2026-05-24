---
title: Pine Script Indicator Development
name: pinescript-indicator-dev
description: Write, debug, and reverse-engineer Pine Script indicators for TradingView. Covers v6 local-scope rules, signal timing, pivot semantics, and visual validation workflows.
trigger: When asked to write, debug, or reverse-engineer Pine Script indicators for TradingView.
category: trading
---

# Pine Script Indicator Development

## v6 Local Scope (CE10144)
Pine Script v6 rejects bare `if`/`for` without explicit local code blocks at the top level.
**Fix:** Use ternary operators, chained `and`/`or`, or built-in functions. Never use unrolled `if` chains.
- ❌ `if condA { x := ... } if condB { x := ... }` — CE10144
- ✅ `x = condA ? ... : condB ? ... : ...`  
- ✅ `for i = 2 to N` with a body (this IS valid, but risky)
- ✅ `swingHigh = not na(ta.pivothigh(left, right))` — use built-ins

## v6 Dynamic Messages: alertcondition() vs alert() (CE10123 root cause)

The `alertcondition().message` parameter requires a **`const string`** — a compile-time constant. It CANNOT accept dynamic values from `str.tostring()`, variables, or function calls. Passing a dynamic string produces **CE10123** (`Cannot call "operator +"`) which is misleading — the string concat syntax is fine, but `alertcondition()` rejects the result.

**`alert().message` accepts a `series string`** — dynamic values, `str.tostring()`, concatenation, everything works. Use `alert()` for any webhook payload that includes real data.

### CE10080: Side effects + timeframe conflict
`alert()` creates side effects. Scripts with side effects **cannot** have a `timeframe=""` argument on `indicator()`. Remove it entirely:
```pinescript
indicator("Signal Capture", overlay=true)           // ✅
indicator("Signal Capture", overlay=true, timeframe="")  // ❌ CE10080
```

### Alert UX difference
- `alertcondition()`: each call = separate condition in dropdown → user creates one alert per condition
- `alert()`: ALL calls = ONE condition: "Any alert() function call" → user creates ONE alert, one webhook URL

### TV webhook port restriction
**TradingView only allows port 80 for HTTP webhooks.** Port 8080 and other custom ports are rejected. Always bind the MCP/webhook receiver to port 80, not 8080. No HTTPS required — plain HTTP on port 80 works.

### String concat in v6
Pine Script v6 supports `+` for strings, but multi-line "line wrapping" (splitting across code lines) is deprecated. Use a **single physical line**:
```pinescript
// ✅ Single-line arrow expression
makePayload(dir) => '{"key":"' + dir + '","val":' + str.tostring(v) + '}'

// ❌ Multi-line + is deprecated
makePayload(dir) =>
    '{"key":"' + dir + '",'
    + '"val":' + str.tostring(v) + '}'
```

### Bool → string
`str.tostring(bool)` is unreliable in v6. Use ternary:
```pinescript
(b ? "true" : "false")   // ✅
str.tostring(b)           // ⚠️ unreliable
```

### v6 top-level if with `:=`
Prefer ternary over `if`/`:=` reassignment at the indicator top level. Pre-compute both branches:
```pinescript
bear_OR  = ph >= top and highVol and (isLessRatio or vd < 0)
bear_AND = ph >= top and highVol and isLessRatio and vd < 0
bearRaw  = deltaMode == "AND" ? bear_AND : bear_OR
```

The working webhook-capture Pine Script is at `templates/bambam-signal-capture.pine` — copy it, don't rewrite it.

Full v6 alert message type reference: `references/pine-v6-alerts.md` (const string vs series string, CE10080, UE differences).

## ⚠️ Pitfall: Spot Data Cannot Reproduce Perp Indicator Signals

When reverse-engineering volume-dependent indicators that run on TradingView perpetual futures (BTCUSDT.P), **Binance.US spot 5-minute data produces fundamentally different volume patterns**. In the BAMBAM/FATCAT analysis:

- Binance.US spot produced 245 BAMBAM signals vs TradingView's 434 (44% fewer)
- Only 37/72 FATCAT matches with ±15min window using spot data
- Mean price diff was only $47 (0.07%) — it's the volume, not the price
- The taker buy volume, volume delta, and volume ratio features are uncorrelated between spot and perp

**Do not waste time sweeping parameters against spot data when the target indicator runs on perps.** Use Binance S3 public bucket data (data.binance.vision, has `taker_buy_base_asset_volume` for futures), or export features from TradingView directly via a feature-export strategy.

## ⚠️ Pitfall: Rectangle Verification — Always Use Raw Signals, Not Strategy Output

When verifying that indicator A is a subset of indicator B, always use **raw indicator signals** (arrows on chart, or strategy with `pyramiding=9999`), NOT a strategy with position management. POCKETBAMBAM (the strategy version) appeared to miss 33 FATCAT entries, leading to the false conclusion that FATCAT was NOT a subset. In reality, raw BAMBAM fires on all those dates — the strategy just couldn't enter because it was still recovering from a prior drawdown. The 33 "missing" entries were a strategy artifact, not a signal logic difference.

**Protocol:** Before declaring "rectangle is broken," run a raw signal strategy (no cooldown, no capital constraints) and verify against that output.

## ⚠️ Pitfall: Timestamp-Only Filters Rarely Reproduce Volume-Based Selectivity

When a selective fork removes 80%+ of base signals and the filter is volume/delta-based, timestamp-only filters (cooldown, time-of-day, signal density) will max out around F1=0.35-0.40. This was confirmed with the BAMBAM→FATCAT analysis:

- Best cooldown-only F1: 0.356 (4h same-direction)
- Best asymmetric cooldown F1: 0.393 (40h short, 2h long)
- Best cluster+cooldown F1: 0.367
- FATCAT takes 50% position-1-in-burst, but the other 50% are scattered across positions 2-8

After exhausting timestamp filters, the next step is to export perp-specific volume features from TV and sweep volume parameters. See `references/reverse-engineering-filter-methodology.md` in the `quant-trading-agent` skill for the full methodology.

## Reverse-Engineering Workflow
1. **Start from a known-working base** that matches the target as closely as possible.
2. **THINK before coding.** When diagnosing signal mismatches, analyze the symptom first: are you seeing too many signals, too few, lone extras, or lone misses? Each symptom points to a different class of fix. Never dump code as a reflex.
3. **Add ONE filter at a time.** Validate visually (screenshots) after each addition.
4. **Never add structural filters** (pivots, cooldown, ATR gates) unless the original description or behavior confirms they exist. Guessing creates symmetric differences — you'll get both extra AND missing signals.
5. **Parameter-tune before filter-invent.** If the target has fewer signals, tighten `lessRatio`, raise `volMultiplier`, or switch `OR` → `AND` on the delta condition. If the target has more signals, loosen those same parameters. Most "advanced" invite-only indicators are the same core logic with tighter knobs, not more gates.
6. **Validate by behavior, not by assumption.** If the original has fewer signals, raise thresholds on the existing logic (e.g., `volMultiplier`, `lessRatio`) rather than inventing new filter categories.

## Backtesting Comparison Architecture
To compare your replica against the original systematically:
1. **Pine Script strategy version**: Convert `indicator()` to `strategy()` and add `log.info()` CSV output on every signal. Tune parameters via inputs and compare signal counts live. Template: `templates/pinescript_strategy.pine`
2. **Python backtest engine**: Fetch Binance OHLCV via `fapi.binance.com/fapi/v1/klines`, replicate the exact signal logic in pandas, and sweep parameters (`lessRatio` × `volMultiplier` × `deltaMode`) against the same date range. Full guide: `references/backtest-engine.md` — script: `scripts/backtest_engine.py`
3. **Binance S3 public data** (when fapi.binance.com is blocked): `references/binance-public-data.md`
4. **Selectivity analyzer Pine Script** (compare post-filters live): `templates/fatcat_selectivity_analyzer_v2.pine`
5. **Python selectivity analyzer** (sweep parameters + volume sources): `scripts/selectivity_analyzer.py`

## Signal Timing & Offset
- `offset=-1` draws the marker on the **extreme bar** (historical/repainting feel).
- `offset=0` draws on the **confirmation bar** (realistic entry timing).
- When reverse-engineering, check whether the target plots on the extreme or confirmation bar first. This single parameter changes visual alignment dramatically.

## Built-in Pivot Semantics
- `ta.pivothigh(left, right)` uses **strict `>`**: equal highs do NOT count.
- If the original seems to catch bars that are "close enough" to pivots, it may not be using `ta.pivothigh` at all.

## Cooldown Without `var` + `if`
To enforce a minimum bar gap between signals without local `if` blocks:
```pinescript
bsb = ta.barssince(rawBear[1])
bearReady = na(bsb) or bsb >= cooldownBars
bearSignal = rawBear and bearReady
```
Avoid `var int lastBearBar = na` + `if bearSignal { lastBearBar := bar_index }` — this hits CE10144 in v6.

## Common Parameter Direction
| Symptom | Likely Fix |
|---|---|
| Too many signals | Raise `volMultiplier`, lower `lessRatio`, switch delta `OR`→`AND`, tighten `lookback`, or use `use_offset=true` (signal on extreme bar, fewer candidates) |
| Too few signals | Lower `volMultiplier`, raise `lessRatio`, switch delta `AND`→`OR`, widen `lookback`, or use `use_offset=false` (signal on confirmation bar, picks up one-bar-later extremes) |
| Lone extras (we have, target doesn't) | Some filter is too permissive; remove invented filters |
| Lone misses (target has, we don't) | Some filter is too restrictive; remove or loosen |

**Delta mode** determines whether a signal requires pure exhaustion (AND) or accepts directional confirmation (OR):
- `OR` (original BAMBAM): `isLessRatio OR vd<0` for bear, `isLessRatio OR vd>0` for bull — fires on both climax bars and strong directional thrusts
- `AND` (more selective): `isLessRatio AND vd<0` for bear, `isLessRatio AND vd>0` for bull — only pure exhaustion (delta clearly on one side AND nearly balanced). This is the "exhaustion-only" pattern and typically cuts 60–70% of signals symmetrically.

## User Preference
- **Think first, don't code** when diagnosing signal mismatches. User explicitly values analysis before implementation.
- **Minimal prose** during debugging. Deliver raw code blocks; explanation belongs in the "think" phase.
- **Visual validation** via TradingView screenshots is the primary truth source.
- **Push through blockers.** If an API is blocked (HTTP 451), find an alternative — the Binance public S3 bucket (`data.binance.vision`) works when the REST API doesn't. Don't accept "can't get the data" as a stopping point; the user expects you to find a way.
- **Test every hypothesis.** When comparing two indicators, run sweeps of all parameter combinations, not incremental testing. Show the full grid, then explain the result.
- **Confirm with actual data.** Don't conclude with "probably" or "likely" when the data exists to settle the question. If it means fetching 85 days of 15m data from an S3 bucket, do it.

## Strategy Template

Full Pine Script strategy with BAMBAM signals, cooldown gate, DCA add-ons, and TP-only exits at `templates/bambam_strategy_with_gate.pine`. Drop on chart, open Strategy Tester. Green arrows = entries fired; grey arrows = signals rejected by the gate. To match FATCAT density: set `lessRatio=0.03`, `deltaMode=AND`, `gateBars=140`, then tune.

### Raw Signal Capture Strategy

`templates/bambam-raw-signals.pine` — BAMBAM indicator as a strategy with `pyramiding=9999`, no cooldown, no DCA. Every arrow = one entry. Use this to export the complete set of raw BAMBAM signals from Strategy Tester CSV. Essential first step for reverse-engineering: confirms the "rectangle" (subset relationship) between a base and a selective fork.

### Feature Export Strategy

`templates/bambam-feature-export.pine` — Exports all computed BAMBAM features at each signal bar: `vol_body`, `vd_body`, `vol_taker`, `vd_taker`, `avgVol` (both methods), `vdRatio` (both methods), `volRatio` (both methods). Use this when timestamp-only filter sweeps fail (F1 < 0.4) and you need perp-specific volume data to brute-force volume/delta parameters. The taker-buy-volume path (`request.security` + `ta.takers_buy`) captures data that spot exchanges cannot provide.

## Opaque/Invite-Only Indicator Signal Logger

When you need to capture entries from an indicator whose source code you don't have (invite-only, closed-source).

### ⚠️ Major Pitfall: `request.indicator()` DOES NOT EXIST

I hallucinated this API in a prior session. **Pine Script v5/v6 has NO `request.indicator()` function.** There is NO way to programmatically read another indicator's plot values from a separate Pine script without having the target's source code.

What `request.indicator()` was supposed to do — reading a named `plot()` from another indicator — is not possible in Pine. If you see suggestions referencing it, they are from hallucinated knowledge, not real API docs.

**What works instead:** The only reliable method for capturing entries from a closed-source indicator is the **Strategy Tester CSV export** (see below).

### Strategy Tester CSV Export (the working method)

Instead of trying to read the other indicator programmatically:

1. **Save the wrapper as a Strategy** — the `templates/fatcat-signal-logger.pine` is already a strategy, not an indicator
2. **Load the target indicator + wrapper on the same chart** — the wrapper reads nothing from the target; it just shares the same chart context
3. **Run Strategy Tester backtest** over the desired date range — this processes every bar
4. **If using manual override mode:** run bar replay, flip the manual input toggle when you see a target signal, then run the backtest with those inputs committed
5. **Export to CSV** — the Strategy Tester's "Export" button gives a clean list of every entry with timestamp, price, and direction

**Delivery:** When sharing Pine Script code with this user, paste the complete code directly in chat as a single code block. The user prefers receiving code as paste-ready text rather than file path references. Do NOT write the file and say "it's in the project" — paste it.

### Manual Mode (alternative, less reliable)

If the target only draws `plotshape()` (visual arrows with no numeric output), the logger's manual override switches let you log entries during bar replay by flipping an input toggle. Each flip creates a strategy entry + fires (suppressed) alert.

**How it works:** The wrapper IS a strategy, so during bar replay the `strategy.entry()` calls DO execute even though `alert()` is suppressed. At the end of replay, export strategy results to CSV. The webhook fires on live bars only.

**⚠️ Reality: manual override is impractical for more than 1-2 signals.** Each bar requires manually flipping the dropdown, and you must flip back to "None" between signals to avoid the debounce lock. For any multi-signal replay session, skip manual mode and use the Strategy Tester CSV export directly.

## ⚠️ Pitfall: Strategy Script Compile Errors (CE10271, Scope Issues)

**Every strategy script I sent in the May 2026 session had a compile error that the user had to catch.** Fix protocol before posting any Pine Script strategy:

1. **`type` vs `Type` in strategy() declaration:** `Type` is NOT a valid strategy parameter. Use `type=strategy.long` or omit entirely. Using `Type` crashes the compiler silently.
2. **Undefined variable references in exit logic:** A variable declared inside a local `if` block is NOT accessible outside it. `bearSignal` computed in the signal section IS available globally (top-level `=`), but if you compute it inside a local function or conditional, it can't be referenced by the exit block. Always compute signals at the top level, not inside `if strategy.position_size > 0` blocks.
3. **`var int` inside conditional reassignment without guard:** If you use `var int since = gateBars + 1` then update with `since := since + 1` inside a conditional block, ensure the update runs EVERY bar (outside the conditional) or it stalls on bars where the condition is false.
4. **Missing input declaration:** `useTp` can't be referenced in an `if` block if it was never declared as an `input.bool()`. Every variable referenced in strategy logic must be declared first.
5. **`plotshape` in strategy scope:** `plotshape` works in `indicator()` but can fail in `strategy()` if the series expression is too complex. When adding visual markers in a strategy, use simple `series=bullSignal` (a single boolean), not multi-value expressions like `series=useGate ? (...) : na`.
6. **Default gate must be OFF when comparing strategy output against another indicator:** If you're comparing your strategy's entry count against FATCAT, the cooldown gate must default to `false` (off). If the user reports *fewer* entries despite all BAMBAM arrows being visible on the chart, the gate is blocking entries. The first debugging step: check if `useGate` defaults to `false` and `gateBars` is set appropriately.
7. **Always test compile first:** Before posting a Pine Script strategy to chat, mentally trace every variable reference, every function call, every scope boundary. The user should not be your Pine compiler. Common issues: `if` inside `if` where inner block shadows outer variables, forgetting to wrap `strategy.close()` condition in `strategy.position_size > 0` guard, missing `process_orders_on_close=true` in strategy declaration.

## CSV Ground-Truth Comparison

When you have a **CSV export of the target indicator's actual entries**, you can compare your replica against real data instead of relying solely on screenshots:

### Workflow

0. **EXTRACT AND SAVE CSV entries to local cache immediately.** When the user shares a CSV file via Telegram, it arrives as a cached document at `/root/.hermes/cache/documents/doc_<hash>_<name>.csv`. These cached files DO NOT persist indefinitely — they may be cleaned up between sessions. If you rely on them for analysis and they're gone later, you lose the ground truth. On receipt: copy the CSV to a permanent location (e.g. `/root/work/trading/csv/`). Take a reading of the entry timestamps, price levels, signal names, and entry mode (long/short/both) right away. Log this in the session notes so you can reconstruct the data from session search even if the file is cleaned.

1. **Test against provided entries FIRST.** When the user has already shared CSV exports of the target indicator's entries, **do not** run off to download independent data and perform a fresh analysis. The user's CSV entries are the ground truth — match your replica against them directly. Only pivot to independent analysis if the CSV entries can't be found or are clearly insufficient. This was a hard-learned lesson: I spent multiple sessions running signal-count comparisons and density sweeps against independent data when the user had already given me the exact entries to match against.

2. **Determine what the CSV represents.** First question before any analysis: is this raw indicator signals (reversal triangles) or strategy-level position entries (grid levels)? These produce completely different signal patterns and you will waste hours trying to fit reversal logic to a position-builder sequence. Quick checks:
   - **Sequential numbering** (L1, L2, L3...) → position-builder grid, NOT independent detections. Each level is a fixed-dollar allocation deployed as price moves against the first entry. These entries do NOT correspond to 200-bar extremes — they fire on continuation.
   - **Reversal names** ("Buy"/"Sell", "Bull"/"Bear", "Long"/"Short") → raw indicator signals. These can be directly compared against your replica.
   - **All entries same direction** (longs only, no shorts) → likely a single-direction mode or a bias filter, not the full reversal logic. The CSV may omit the other direction entirely.
   - **Price matches bar close exactly** → entry executes at bar completion (not on intra-bar trigger). This is consistent with both signal types.
   - **At least one price on a bar that is NOT a new 200-bar low/high** → the entry logic is NOT the BAMBAM `pl <= btm` / `ph >= top` condition. You need a different model entirely (likely DCA grid, percentage-based, or a separate position-sizing module).

2. **Fetch OHLCV data** for the same timeframe and date range. If Binance is blocked (HTTP 451), use Bitstamp — paginate backward via the `end` parameter:
   ```
   https://www.bitstamp.net/api/v2/ohlc/btcusd/?step=300&limit=1000&end=<unix_ts>
   ```
   `step=300` = 5min candles. Bitstamp returns freely without API key for historical 5m data (~3 months depth).

3. **Align timestamps.** The CSV entry timestamps should match a candle open_time on the exchange data (within seconds). Small price differences between exchanges (<1%) are normal.

4. **Run your replica across a parameter sweep** (`lessRatio` × `volMultiplier` × `deltaMode`) and compute exact bar matches. Use the same timeframe and lookback that the target is on — different timeframes produce radically different match rates (e.g., 5m gave 0/21 match, 15m gave 6/6 match on the same indicator with tuned POCKETBAMBAM).

5. **If you get zero exact matches across all parameters, STOP.** The CSV entries use **fundamentally different signal logic** — don't force-fit parameters to match a count that was never meant to. This is a class-of-signal problem, not a tuning problem.

   *Counterexample that misled me:* I spent a full session trying to tune BAMBAM to match FATCAT "Single Direction" CSV entries, getting 0/21 exact matches across 18 param combos. The cause: the CSV was a position-building grid (sequentially numbered L-signals with ~$500 fixed allocation per level), not reversal signals at 200-bar extremes. Only 3/21 entries happened to be at 200-bar lows.

*Second trap — density ≠ timestamp match:* Signal count alignment (e.g., 19 signals from my replica vs 18 from FATCAT) is NOT evidence of correct replication. I fell into this: total counts matched, but 0/6 timestamps aligned when checked against the actual FATCAT CSV entries. Always validate at the exact timestamp (same 5m/15m bar) level before claiming a confirmed formula. Use the CSV Ground-Truth Comparison workflow above.

### Selectivity Filter Analysis
When BAMBAM catches 100% of the target entries but fires 3–4× too many total signals (precision gap, not recall gap — target entries are all valid, replica just adds noise), the differentiating filter is likely one of:

| Symptom | Likely filter |
|---|---|
| Extras cluster within hours of real entries | **Cooldown**: min bars between signals |
| Extras at same price level as last entry (<0.5% move) | **Price gate**: require min % move from last signal |
| Extras during quiet ranging | **Volume gate**: raise volMultiplier |
| Entries but with offset timing | **Lookback length**: mismatch in rolling window size between timeframes |
| Sequential multi-fire in same bar cluster | **Pivot requirement**: require swing structure + left/right confirmation |

Test these via `templates/fatcat_selectivity_analyzer.pine` — a configurable Pine Script that layers each post-filter onto the base BAMBAM signal and counts remaining signals.

### Zero-Match Diagnosis

When BAMBAM catches **none** of the target CSV entries across all tested parameter combinations (0/21 match, 0/6 match in the FATCAT analysis), the CSV entries are from a **fundamentally different signal class** — not reversal signals at all. Likely a position-builder grid: sequential L1→L2→L3 with fixed ~$500/level allocation. These entries fire on drawdown from first entry, not on 200-bar extremes. Do not waste time tuning reversal parameters — the signal logic is different.

**Quick check:** if the entry price on any bar is NOT at a new 200-bar low (for longs) or high (for shorts), the logic is NOT the BAMBAM `pl <= btm` / `ph >= top` condition. Move to position-building or DCA models instead.
Different timeframes produce radically different signal densities from the same lookback:
- 5m, 200 bars: ~16h window → high density (~450 bull signals over 8 months on BTC)
- 15m, 200 bars: ~50h window → medium density (~150 signals)
- 1h, 200 bars: ~8 day window → low density (~55 signals, close to FATCAT's 58)

When comparing, always match the timeframe the target is displayed on in TradingView, not the timeframe your data happens to have.

## ⚠️ Pitfall: Strategy Tester CSV Does NOT Include plot() Values

TradingView's Strategy Tester CSV export (the "Export" button) only exports the standard trade columns: Trade #, Type, Date and time, Signal, Price, Size, P&L, Excursion. It does **NOT** include `plot()` values even when `display=display.data_window` is set. The Data Window shows plots on screen but the CSV export strips them. The "Export chart data" right-click option may not be available on all accounts.

**Workaround: embed feature values in `strategy.entry(comment=...)`.** The `comment` field IS exported in the CSV's Signal column. Use pipe-delimited numeric values:

```pinescript
if bearRaw
    strategy.entry("S", strategy.short, comment=str.tostring(vol) + "|" + str.tostring(vd) + "|" + str.tostring(avgVol) + "|" + str.tostring(vol/avgVol) + "|" + str.tostring(vdRatio) + "|" + str.tostring(vb) + "|" + str.tostring(vs))
```

Each entry row's Signal column becomes: `421.043|130.264|346.152|1.216|0.309|275.653|145.389` (vol|vd|avgVol|volRatio|vdRatio|vb|vs). Parse with Python: `row['Signal'].split('|')`.

**⚠️ Do NOT use format strings in `str.tostring()`.** Pine v6 rejects `str.tostring(val, "#.##")` with null translation error. Use plain `str.tostring(val)` — it outputs full float precision which is fine for post-processing.

## ⚠️ Pitfall: `str.tostring()` Format Strings Fail in Pine v6

`str.tostring(val, "#.##")` produces `Script could not be translated from: null`. The format specifier syntax is not universally supported in all Pine v6 contexts. Use plain `str.tostring(val)` and truncate in post-processing:

```pinescript
// ❌ CE null translation error
comment="BEAR|v=" + str.tostring(vol, "#.##")

// ✅ Plain conversion — full float, truncate in Python
comment=str.tostring(vol) + "|" + str.tostring(vd) + "|" + str.tostring(avgVol)
```

## ⚠️ Diagnostic: `takerbuyvol` Compile Error (CE10272)

If `useTakerBuy and na(takerbuyvol)` produces `Undeclared identifier "takerbuyvol"` at compile time: **the broker does not provide real taker-buy volume data.** This definitively rules out the taker_buy_base theory — FATCAT cannot use a data field that doesn't exist on the user's broker. The volume source is NOT the differentiator. This is stronger evidence than any timestamp mismatch.

## ⚠️ Strategy Template: BAMBAM + Cooldown Gate

Full Pine Script strategy with BAMBAM signals, cooldown gate, DCA add-ons, and TP-only exits at `templates/bambam_strategy_with_gate.pine`. To match FATCAT density: set `lessRatio=0.03`, `deltaMode=AND`, `gateBars=140`, then tune from there.

## ⚠️ OG vs POCKETBAMBAM Offset Confirmation

User chart testing confirmed: OG BAMBAM fires signals **one candle before** POCKETBAMBAM entries. This means POCKETBAMBAM = BAMBAM signals + 1-bar delay (standard strategy execution at next bar open). No structural difference — pure timing. When comparing replicas, always account for this ±1 bar.

## ⚠️ Pine Script v6: alertcondition() vs alert() for Dynamic Messages

**`alertcondition().message` requires a `const string`** — a compile-time constant. It CANNOT contain dynamic values from `str.tostring()`, variables, or function calls. This produces CE10123 (`Cannot call "operator +"` — a misleading error). The `alertcondition().message` only accepts static text + `{{placeholders}}`.

**`alert().message` accepts a `series string`** — dynamic values, concatenation, `str.tostring()`, everything works. Use `alert()` for webhook payloads with real data.

**CE10080:** `alert()` is a side effect — remove `timeframe=""` from `indicator()` declaration when using `alert()`. Scripts with side effects cannot have a timeframe argument.

**String concat in v6:** `+` IS supported for strings, but multi-line "line wrapping" (splitting a single-line string across code lines with `+`) is deprecated. Use a single physical line for the entire expression, or `str.format()`.

**v6 top-level `if` with `:=`:** Prefer ternary (`cond ? a : b`) over `if`/`:=` reassignment at the indicator top level. Pre-compute both branches and select.

**Alert UX difference:** With `alert()`, all calls appear as ONE condition: "Any alert() function call." User creates one alert, one webhook URL. With `alertcondition()`, each call creates a separate condition needing its own alert.

## ⚠️ Bar Replay Does NOT Trigger Alert Webhooks

TradingView's Bar Replay mode recalculates indicators and renders visual markers (`plotshape`, `bgcolor`, labels) on replayed bars, but it does NOT fire `alert()` or `alertcondition()` webhooks. **No HTTP POST is sent during bar replay** regardless of signal conditions. This is a platform restriction — alerts only execute on live real-time data.

**Critical distinction:** Visual signals (arrows, background colors, labels drawn by `plotshape()` / `label.new()`) are NOT the same as webhook alerts. `plotshape()` draws pixels on the chart; `alert()` sends HTTP requests. During replay you WILL see the signals flash on the chart, but the `alert()` call is suppressed — they are two completely separate execution paths in the Pine runtime.

**Impact:** You cannot use bar replay to test the webhook → MCP server → SQLite pipeline. Visual signals confirm the indicator logic fired correctly, but the alert() call itself is suppressed. To test the pipeline:
1. Wait for a live real-time bar to trigger the alert, OR
2. Manually POST a test payload to the webhook server

**Strategy Tester workaround (the practical method):** While `alert()` doesn't fire during replay, the Strategy Tester DOES execute `strategy.entry()`/`strategy.exit()` calls from a strategy script during replay. This is the most practical way to get signal entry logs from a closed-source indicator:

1. Load the target indicator + a strategy wrapper on the same chart
2. Run bar replay through the desired date range — `strategy.entry()` fires on every bar where conditions are met, even though `alert()` is frozen
3. After replay, open the Strategy Tester panel and click **Export to CSV**
4. The CSV contains every entry with timestamp, price, direction, and signal name

This is more practical than manual override toggles — you don't need to flip switches during replay. The strategy evaluates automatically on every bar.

**Alternative: Manual override during replay** — For indicators that don't expose signal values, use `input.string()` toggles that the user flips when they see a visual arrow. Debounce logic (tracking `lastSignal`) prevents double-fires. However this is impractical for more than 1-2 signals; use the CSV export method for serious analysis.

**Note:** Strategy backtesting (click "Run" in the Strategy Tester) processes ALL bars instantly. Bar replay processes bars one at a time. Both execute `strategy.entry()` calls — the difference is timing, not capability.

**Timeframe field format in alert payloads:** When creating an alert with dynamic JSON, the `{{interval}}` placeholder or `timeframe.period` variable returns just the number (e.g., `"5"` for 5 minutes, `"15"` for 15 minutes), NOT `"5m"` or `"15m"`. Seconds-based timeframes include the suffix (e.g., `"15S"`). DB queries filtering by timeframe must account for this: `WHERE timeframe='5'` not `WHERE timeframe='5m'`.

## ⚠️ v6 alertcondition() vs alert() — Dynamic Message Strings (CE10123)

**`alertcondition().message` requires a `const string`** — a compile-time constant. It CANNOT contain dynamic values from variables, `str.tostring()`, or concatenation. Passing a series string produces CE10123 even if the string concatenation itself is valid.

**`alert().message` accepts a `series string`** — dynamic, can include calculated values. This is the v6 way to send dynamic webhook payloads.

```pinescript
// ❌ CE10123 — message is not const
alertcondition(bullRaw, title="Bull", message=makePayload("bull"))

// ✅ Works — alert() accepts series strings
if bullRaw
    alert(makePayload("bull"), alert.freq_once_per_bar_close)
```

**Tradeoffs:**
- `alertcondition()`: creates a named condition in the dropdown, user can customize message. But message is static.
- `alert()`: all calls share one "Any alert() function call" condition. One alert covers all. Message is dynamic.
- `alert()` counts as a side effect — remove `timeframe=""` from `indicator()` or get CE10080.

## ⚠️ v6 String Concatenation (CE10123)

String `+` concatenation IS supported in v6, but **line wrapping strings across multiple physical lines is deprecated**. Future versions will reject it.

```pinescript
// ❌ Deprecated — string literal split across lines
msg = '{"key":"' + value + '",' +
      '"key2":"' + value2 + '"}'

// ✅ Single-line — all on one physical line
msg = '{"key":"' + value + '","key2":"' + value2 + '"}'

// ✅ str.format() — still supported, but beware apostrophe quoting in template
msg = str.format('{"key":"{0}","key2":"{1}"}', value, value2)
```

**Bool to string:** use ternary `b ? "true" : "false"` instead of `str.tostring(bool)` — v6 bool handling in `str.tostring()` is unreliable.

## ⚠️ v6 `if`/`:=` at Top Level (CE10144)

Prefer ternary expressions over `if` blocks with `:=` reassignment at the indicator's top level:

```pinescript
// ❌ May cause CE10144 in v6
if deltaMode == "AND"
    bearRaw := ph >= top and highVol and isLessRatio and vd < 0

// ✅ Ternary — safe in all v6 contexts
bearRaw_OR = ph >= top and highVol and (isLessRatio or vd < 0)
bearRaw_AND = ph >= top and highVol and isLessRatio and vd < 0
bearRaw = deltaMode == "AND" ? bearRaw_AND : bearRaw_OR
```

## ⚠️ alert() and indicator() timeframe (CE10080)

`alert()` is a side effect. `indicator()` with `timeframe=""` rejects side-effect scripts. Fix: remove `timeframe` parameter entirely.

```pinescript
// ❌ CE10080
indicator("My Script", overlay=true, timeframe="")

// ✅
indicator("My Script", overlay=true)
```

## ⚠️ Pitfall: Testing Against Wrong Data When CSV Entries Exist

**When the user has already shared CSV export files** of the target indicator's entries, test your replica against those FIRST — do not run off to download independent data and perform fresh signal-count comparisons. This cost multiple sessions: I ran density sweeps against Bitstamp and Binance S3 data when the user's actual FATCAT CSV entries were sitting in `/root/.hermes/cache/documents/`. The CSV is ground truth; external data feeds have timestamp misalignment.

## ⚠️ Pitfall: strategy.entry() Comment Evaluation Timing

When building feature export scripts using `strategy.entry(comment=...)`, there's a **subtle timing issue** where `str.tostring(series_var[n])` inside a user-defined function can produce NaN or stale values.

### What DOES NOT work

```pine
make_comment(dir) =>
    c = dir + "|" + str.tostring(vb1[1])  // ← May produce NaN
    c

strategy.entry("BEAR", strategy.short, comment=make_comment("BEAR"))
```

### What DOES work

```pine
// Pre-compute ALL str.tostring() at top-level scope
s_vb  = str.tostring(vb1[1])
s_vs  = str.tostring(vs1[1])

// Concatenate strings inline — no function scope
bear_comment = "BEAR|" + s_vb + "|" + s_vs + "|" + ...
strategy.entry("BEAR", strategy.short, comment=bear_comment)
```

**The actual cause:** This is NOT a general Pine v6 UDF bug (UDFs handle history references correctly in standard usage). The issue is specific to `strategy.entry()`'s **deferred comment evaluation**. When a UDF is called from inside `strategy.entry(comment=fn())`, the function's evaluation frame sees a different series cache state than the main body did during the standard bar-by-bar pass. This is an interaction between UDF evaluation semantics, strategy.entry's deferred comment evaluation, and how series history caching works across scopes.

**The fix:** Pre-compute `str.tostring()` calls at the top level so series accesses happen during the standard evaluation pass with consistent state. String concatenation has no series-cache dependency, so it works fine in the deferred context.

**Verification:** After any export, always run the 7-point data audit:
1. Feature count = 25 (dir + 24 values)
2. No NaN values
3. vb + vs ≈ vol (critical — catches deferred eval bug)
4. Date range matches expected window
5. Direction counts roughly balanced
6. Signal column readable ("BULL"/"BEAR")
7. Timestamps match perp data within ±5min

Full audit script and tolerances: See `swingcatcher` skill's `references/data-audit-methodology.md`.

## TradingView MCP Limitations

When evaluating the TradingView MCP for data extraction, note that it CANNOT run custom Pine Scripts, read indicator plot values, or extract strategy trade logs. It only runs 6 hardcoded strategies (RSI, Bollinger, MACD, EMA cross, Supertrend, Donchian). Full breakdown: `references/tradingview-mcp-limitations.md`.

Use case: quick technical scans and running generic strategies — NOT for programmatic entry extraction from custom scripts.

## ⚠️ Pitfall: Circling Back to Disproven Theories

When a theory is disproven by hard evidence (compile error, confirmed chart test), do NOT reintroduce it in a later turn. The `taker_buy_base` theory was killed definitively by the `takerbuyvol` CE10272 compile error — FATCAT cannot use a data field that doesn't compile on the user's broker. Yet I proposed it again multiple times. Once disproven, the theory should be struck from the working hypothesis set and referenced only as a historical dead end.

## Project Directory Snapshot Pattern

When the user plans to move work to a new machine or wants a clean handoff, create a **project directory** with:
- `README.md` — current state, confirmed facts, unresolved questions
- `prompts/resume.md` — prompt the new agent reads to pick up where we left off
- `data/` — all CSVs, exports, reference data
- `pinescript/` — all .pine files (indicator, strategy, variants)
- `docs/` — setup guide, backtester scripts
- No internet dependencies — bundle everything needed locally

The `resume.md` prompt should be directive: tell the agent exactly what to do, what data to use, what filter space to sweep, and what format to output. Avoid context-dependent references — the new agent won't have the chat history.

See `references/project-directory-pattern.md` for the full template used in the BAMBAM-FATCAT handoff.

## ⚠️ Hypothesis Tested: Volume Source — DISPROVEN

The taker_buy_base theory (FATCAT uses real Binance order-flow volume) showed signal DENSITY alignment (~19 vs ~18) but FAILED timestamp-level validation: 0/6 exact bar matches against FATCAT CSV entries, and definitively killed by `takerbuyvol` CE10272 compile error on the user's broker. **Density match ≠ correct replication.** POCKETBAMBAM uses estimated volume and matches FATCAT timestamps 6/6, directly disproving the volume-source theory. See `quant-trading-agent` skill, `references/fatcat-disverified-theories.md` for the full audit.

## ⚠️ Pitfall: Binance 451 Blocks Backtest Data

When running from a restricted-region VPS, `fapi.binance.com` (and `api.binance.com`) returns HTTP 451 — geo-blocked. The `backtest_engine.py` script auto-falls back to Bitstamp, but with these caveats:

1. **Bitstamp has NO `taker_buy_base`.** The script can only compute estimated volume decomposition (`vb = volume×(close-low)/(high-low)`), not real order-flow volume. This means the volume-source sensitivity analysis (estimate vs. taker_buy) is unavailable from Bitstamp data.
2. **Bitstamp doesn't have BTCUSDT perpetual futures.** It's spot BTC/USD, which has slightly different price action from futures perps. For 5m+ timeframe signal analysis this is negligible, but sub-5m signals may not align perfectly.
3. **Binance S3 public bucket (`data.binance.vision`) is on AWS CloudFront, not Binance's own infra.** It's typically NOT geo-blocked even when the REST API is. If you need `taker_buy_base`, use the S3 bucket directly — it's the only way to get real order-flow volume when the live API is blocked.
4. **Auto-fallback is invisible.** The script will silently switch to Bitstamp and continue; the user sees `Fetched N bars from bitstamp` and may not realize the data lacks `taker_buy_base`. Always log which source was used.

## ⚠️ Critical Pitfall: Different Modes = Different Signal Logic

Indicators with multiple modes (e.g., "Single Direction" vs. standard reversal mode) produce signals that look similar (both print long entries) but use completely different logic:

- **Reversal signals** (what BAMBAM replicates): 200-bar extreme + high volume + exhaustion delta. Entries cluster at structural pivots.
- **Position-building entries** (FATCAT "Single Direction"): sequential grid levels with fixed $ allocation per level, ~30% drawdown ceiling from initial entry. Entries fire on continuation AND bounces — not just extremes.

**When you receive entry data from the user:**
1. Ask or determine whether it's raw indicator signals or strategy-level position entries
2. Check if the signal sequence is sequential (L1, L2, L3...) — this likely indicates a position-building grid, not independent signal detections
3. Verify: do entries correspond to 200-bar lows/highs? If not, the logic is different
4. If both bull and bear signals appear in the CSV, it's likely the core indicator; if only one direction, suspect a filtered mode
