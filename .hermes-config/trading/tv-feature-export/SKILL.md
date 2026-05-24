---
name: tv-feature-export
description: Export computed bar-level features from TradingView Pine Script via Strategy Tester CSV comment strings
tags: [trading, tradingview, pine, csv, feature-extraction, perps]
---

# TradingView Feature Export

Export computed bar-level features from TradingView Pine Script via Strategy Tester CSV.

## Methodology

Strategy Tester CSV only includes standard trade columns — NOT `plot()` values or Data Window content. Embed custom features via the `comment` parameter of `strategy.entry()`:

```pine
comment = str.tostring(val1) + "|" + str.tostring(val2) + "|" + str.tostring(val3)
strategy.entry("S", strategy.short, comment=comment)
```

Each Entry row's **Signal** column will contain the pipe-delimited feature vector.

## Confirmed Working Formats

### Format A: Raw pipe-delimited floats (simplest, most reliable)
```
Signal column: 1520.506|-954.626|429.371|3.541|0.628|282.94|1237.57
```
Parsed as: `parts = row['Signal'].split('|')` → array of floats.

### Format B: Direction prefix + raw floats (used for 14 and 24-feature exports)
```
Signal column: BEAR|1520.506|-954.626|429.371|3.541|0.628|282.94|1237.57
```
Parsed as: `parts = row['Signal'].split('|')` → parts[0] is direction ('BEAR'/'BULL'), parts[1:] are floats.

### Format C: KEY=VALUE (used in saved Pine script template, NOT used in actual analysis)
```
Signal column: BEAR|v=1520.51|vd=-954.63|av=429.37|vr=3.54|vdr=0.63|vb=282.94|vs=1237.57
```
**CRITICAL PITFALL:** The saved Pine script `bambam-feature-export.pine` uses this KEY=VALUE format. ALL analysis code expects raw floats without KEY= prefixes. If the saved script is used as-is, the exported CSV will NOT parse — analysis code silently skips rows with wrong format. Use only raw pipe-delimited floats. No KEY=labels.

## Feature Export Tiers

| Tier | Features | Signal Format | Pine Script |
|---|---|---|---|
| **Raw** (7) | vol, vd, avgVol, volRatio, vdRatio, vb, vs | 7 raw floats | `bambam-feature-export.pine` |
| **Indicator** (14) | 7 body + rsi14, rsi7, dist_ema21/50/200, macd_hist, atr14 | BEAR/BULL + 14 floats | `*_Indicator_Export` |
| **Delta** (24) | 14 levels + 6 deltas + 4 cross flags | BEAR/BULL + 24 floats | `*_Delta_Export` |
| **Raw Capture** (0) | None — just signal existence | BEAR or BULL text | `bambam-raw-signals.pine` |

### Delta Export: 24 features in order

```python
feat_names = ['vol','vd','avgVol','volRatio','vdRatio','vb','vs',
              'rsi14','rsi7','dist_ema21','dist_ema50','dist_ema200','macd_hist','atr14',
              'rsi14_delta','rsi7_delta','macd_hist_delta','price_mom5','volRatio_delta',
              'vdRatio_delta','ema21_bear','ema21_bull','ema50_bear','ema50_bull']
```

Parsing (from `analysis_delta_pipeline.py`):
```python
parts = row['Signal'].split('|')
if len(parts) != 25: continue  # direction + 24 features
d = 'short' if parts[0].startswith('BEAR') else 'long'
s = {'direction': d}
for i, name in enumerate(feat_names):
    s[name] = float(parts[i+1])
```

**Pitfall**: The saved `bambam-feature-export.pine` in the pinescript directory uses KEY=VALUE formatting (e.g. `BEAR|v=1520.51|vd=-954.63`). This did NOT match the format actually exported for analysis, which used bare floats. If you copy the saved script and run it, the CSV will NOT parse with existing analysis code. Use float-only pipe-delimited columns in `str.tostring()` calls.

## Critical Notes

### Pine Script Pitfalls (learned the hard way)

- **DO NOT** use `str.tostring(val, "#.##")` format strings — causes `Script could not be translated from: null` compile error. Use bare `str.tostring(val)`.
- **DO NOT** use `ta.takers_buy volume` — invalid syntax, causes `Undeclared identifier` error. Correct bare call: `ta.takers_buy` (v5/v6) or `takers_buy` (v4).
- **`ta.takers_buy` broker dependency**: On some TradingView brokers/data feeds, `takers_buy` throws `Undeclared identifier` even with correct syntax. This means the broker does NOT provide taker buy volume for that symbol. **No workaround within Pine** — must obtain taker data externally (see `scripts/download_perp_data.py`).
- **CRITICAL: strategy.entry() deferred comment evaluation bug**: When you pass `comment=make_comment("BEAR")` inside `strategy.entry()`, Pine v6 defers the function call to the moment the conditional block fires. Inside that deferred context, series history accesses like `vb1[1]` can resolve to stale or NaN values. **The cause is NOT a general Pine v6 UDF bug** — UDFs handle history references correctly in normal usage. It is specific to `strategy.entry()`'s deferred comment evaluation, where the function's evaluation frame sees a different series cache than the main body did during the standard bar-by-bar pass.

  **Confirmed empirically** May 23 2026 — 399/431 signals failed vb+vs≈vol sanity check when `str.tostring()` was inside a `make_comment()` function called from `strategy.entry(comment=...)`. The first signal's raw Signal column contained literal `NaN` at feature positions 5-6.

  **CORRECT diagnosis (per Claude audit):** Pine v6 UDFs handle history references correctly in standard usage. The issue is specific to `strategy.entry()`'s deferred comment evaluation — functions called from within a `strategy.entry()` argument don't see the same series state as top-level expressions.

  **The only reliable approach**: Pre-compute ALL `str.tostring(series[n])` calls at TOP-LEVEL SCOPE (outside any function body), store results in string variables, then concatenate inline. String concatenation has no series-cache dependency, so it works fine in deferred context:
  
  ```pine
  // CORRECT — all str.tostring() at top level:
  s_vb  = str.tostring(vb1[1])
  s_vs  = str.tostring(vs1[1])
  
  bear_comment = "BEAR|" + s_vb + "|" + s_vs + "|" + ...
  strategy.entry("BEAR", strategy.short, comment=bear_comment)
  
  // WRONG — series offset inside function called from strategy.entry():
  make_comment(dir) =>
      str.tostring(vb1[1])  // ← Deferred eval breaks on strategy.entry() calls only.
  ```
  
  This bug was NOT caught by `//@version=6` compilation — the script compiles cleanly but produces corrupt data at runtime. The only reliable detection is the `vb+vs≈vol` sanity check on the exported CSV.
  
  **General rule**: Any time you need `str.tostring()` of a series value with a history offset, do it at top-level scope, not inside a function called from a conditional strategy block.

- **DO NOT export with KEY=VALUE format**: The saved `bambam-feature-export.pine` uses `BEAR|v=1520.51|vd=-954.63|...` format. ALL analysis code (parse_entries, enrich_signals) expects raw pipe-delimited floats WITHOUT KEY= prefixes. If an export has KEY=VALUE format, Python code silently skips all rows (wrong split count). Use raw `str.tostring(val)` with no KEY= prefix.

- **volRatio_delta computation bug (v1)**: The original 24-feat export (v1, May 22) computed `volRatio_5` with a shifted averaging window (bars 6..205 for denominator, vs 1..200 for current). This silently compared ratios with mismatched denominators, creating a systematic bias (mean=1.61, 70% positive values — should be symmetric around zero). Fix: use `avgVol[5]` instead of recomputing the window, so both ratios share the same rolling window, just sampled 5 bars apart.

  ```pine
  // v1 WRONG — shifted averaging window:
  // volRatio_5 = vol_body_5 / recomputed_avgVol_from_shifted_window
  
  // v2.1 CORRECT — same window, earlier sample:
  volRatio_5 = vol_body_5 / avgVol[5]
  ```

- **Pine v6 vs v5 vs v4 syntax table**:

| Feature | v6 | v5 | v4 |
|---|---|---|---|
| String conversion | `str.tostring()` | `str.tostring()` | `tostring()` |
| Math functions | `math.abs()` | `math.abs()` | `abs()` |
| Highest/Lowest | `ta.highest()` | `ta.highest()` | `highest()` |
| Sum | `math.sum()` | `math.sum()` | `sum()` |
| Input int | `input.int()` | `input.int()` | `input()` |
| Input float | `input.float()` | `input.float()` | `input()` |
| Taker buy vol | `ta.takers_buy` | `ta.takers_buy` | `takers_buy` |
| Display constant | `display.data_window` | `display.data_window` | N/A |

### Export Method

- **Strategy Tester CSV** does NOT include `plot()` values or Data Window content — only standard trade columns. Comment-string embedding is the ONLY reliable export path.
- **Chart data export** (right-click → Export) may require TV Pro tier. Comment-string method works on all tiers.
- **pyramiding=9999** required to capture every signal without capital constraints.
- For perps (BTCUSDT.P), taker buy volume requires a broker that provides it. Binance Futures connector in TV provides it; many others don't.

## Parsing (Python)

```python
import csv
from datetime import datetime, timezone

entries = []
with open('export.csv') as f:
    content = f.read()
    if content.startswith('\ufeff'): content = content[1:]
    for row in csv.DictReader(content.splitlines()):
        if 'Entry' in row['Type']:
            parts = row['Signal'].split('|')
            dt = datetime.strptime(row['Date and time'], '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
            features = [float(p) for p in parts]
            direction = 'long' if 'long' in row['Type'] else 'short'
            entries.append({'dt': dt, 'direction': direction, 'features': features})
```

## Binance Futures Perp Data Pipeline

When TV can't provide taker volume via Pine, download directly from Binance Futures API:

```python
# binance_futures_data.py — downloads ALL available perp market data
# VPS is geo-blocked from fapi.binance.com — run on local machine
# Default: BTCUSDT 2025-10-01 to 2026-05-23
# Usage: python binance_futures_data.py [symbol=BTCUSDT] [start=2025-05-01] [end=2026-06-30]
```

Output structure — `data/binance_futures/{SYMBOL}/`:

| File | Rows* | Columns |
|---|---|---|
| `klines_5m.csv` | 111,646 | OHLCV + taker_buy_base_vol + trades |
| `open_interest_5m.csv` | 111,646 | oi_base, oi_usd |
| `taker_ratio_5m.csv` | 111,646 | buy_vol, sell_vol, ratio |
| `top_trader_account_5m.csv` | 111,646 | long_acct, short_acct, ratio |
| `top_trader_position_5m.csv` | 111,646 | long_pos, short_pos, ratio |
| `global_long_short_5m.csv` | 111,646 | long_pct, short_pct, ratio |
| `funding_8h.csv` | 1,163 | rate (8h cadence) |
| `premium_index_5m.csv` | 111,646 | premium index OHLCV (basis_bps = close × 10,000) |
| `merged_5m.csv` | 111,646 | ALL 20 columns merged by timestamp |

*Rows for BTCUSDT May 2025–May 2026 (~12.5 months, exactly 111,646 5m candles)

The **merged file** is the single-input format for enrichment:

```csv
time_str,open,high,low,close,volume,quote_volume,trades,
taker_buy_base_vol,oi_base,oi_usd,taker_buy_vol,taker_sell_vol,
top_long_acct,top_short_acct,top_long_pos,top_short_pos,
global_long_pct,global_short_pct,basis_bps
```

**Merge alignment** — all 5m datasets aligned by rounding timestamps to the nearest 5m boundary (÷300s). This handles the 10-30ms timing differences between API endpoints. Coverage is >99.9% for all columns except funding (8h cadence is normal).

**basis_bps** — the premium/discount of the perpetual contract vs the underlying index, expressed in basis points (= premium_index_close × 10,000). Positive = perp above spot (bullish, crowded longs). Negative = perp below spot (bearish, crowded shorts). History available back to Feb 2025 on Binance Futures API.

**To update existing perp data** (if you already ran the old version without premium index):
```bash
scp root@178.156.199.37:/root/work/trading/bambam-fatcat-project/binance_futures_data.py ./
python3 binance_futures_data.py symbol=BTCUSDT start=2025-05-01 end=2026-06-30
```

## Feature Export + Swing Research Pipeline (Current, May 2026)

The swing_research pipeline replaced the old monolithic analysis scripts. Key components:

### lib/data_loader.py (Column Flexibility)
The data loader accepts both `open_time_str` (raw Binance export) and `time_str` (merged file from `binance_futures_data.py`). Auto-detects which column name is present:
```python
ts_col = 'open_time_str' if 'open_time_str' in df.columns else 'time_str'
df['dt'] = pd.to_datetime(df[ts_col], utc=True, format='%Y-%m-%d %H:%M')
```

### Full Pipeline Structure
See `references/swing-research-pipeline.md` for the complete methodology (triple-barrier labels, ATR ZigZag, chronological splits, LightGBM).

### Old Analysis Scripts (ARCHIVED)
The following were confirmed dead and deleted May 23, 2026:
- `analysis_delta_pipeline.py` through `analysis_taker_volume.py` — v1 analysis on buggy data
- `build_swingcatcher.py` through `swingcatcher_full_optimization.py` — v1 threshold sweeps
- `download_perp_data.py` — replaced by `binance_futures_data.py`
- `mcp_server.py` — old webhook experiment
- `sweep.py` — v1 parameter sweep

Results preserved in `references/bambam-fatcat-analysis.md` and audit pipeline outputs.

## Indicator Export (Next Frontier)

F1 ceiling of ~0.40 on all volume/price features means FATCAT almost certainly gates on **oscillator/indicator conditions** (RSI, EMA distance, MACD histogram). Export these from TV using the same comment-string method with `strategy.entry()`.

Pine Script template for indicator export: see `templates/indicator-export.pine`.

Features to export (14 per signal, within Signal column limit):
1-7. Body-method volume features (same as existing export)
8. RSI(14) — prior bar
9. RSI(7) — faster RSI
10. Distance from EMA(21) — % above/below
11. Distance from EMA(50) — % above/below
12. Distance from EMA(200) — % above/below
13. MACD histogram — prior bar
14. ATR(14) — volatility context

DEFINITIVE RESULT (8 approaches exhausted, May 2026):
- Single-bar body thresholds: F1=0.378
- Timestamp cooldown: F1=0.393
- Single-bar taker thresholds: F1=0.373
- Combined body+taker cooldown: F1=0.398
- ML classifiers (RF/GB): CV F1=0.222
- BAMBAM parameter retrodiction: F1=0.164 (176 configs swept — FATCAT is NOT a BAMBAM retuning)
- Multi-bar 10-bar sequences: F1=0.398 (KS p<0.01 but thresholds don't help)
- Directional move filter: F1=0.398 (no improvement)

Hard F1 ceiling at ~0.40. FATCAT's filter uses logic not captured by volume/price features.

Indicator export result (May 2026): RSI/EMA/MACD/ATR exported successfully from TV with exact 434/434 timestamp match and zero NaNs. Indicators show strong statistical separation (dist_ema200 KS=0.324 p=4.3e-06; RSI14 KS=0.288 p=6.5e-05; MACD hist KS=0.271 p=2.2e-04), but they still do NOT crack FATCAT. Best combined filter: CD_short=16h, CD_long=1h, volRatio_body>=3.5, ATR14>=116 → F1=0.402, only +0.004 over prior 0.398. ML CV: logistic regression all14 F1=0.359±0.041, RF=0.272, GB=0.139. Conclusion: indicator filters alone are not the missing key; FATCAT likely uses proprietary/stateful logic or a different higher-timeframe/market-regime gate.

## Known Limitations

- Exit rows also contain the Signal column from the matching Entry — filter on `'Entry' in row['Type']`
- Duplicate entries can occur — deduplicate on `(Date and time, Price USDT)`
- Signal column length is limited — keep feature count under ~14 pipe-delimited values
- Binance.US spot data produces different BAMBAM signals than TV perps (245 vs 434) — always use perp data for signal analysis
- VPS geo-blocked from Binance Futures, Bybit, OKX (for perp data) — download from local machine
- Taker buy volume (`ta.takers_buy`) is NOT available on all TV brokers — if you get `Undeclared identifier`, the broker doesn't provide it. Fall back to external data download (see `scripts/download_perp_data.py`).

## See Also

- `references/bambam-fatcat-analysis.md` — Full reverse-engineering methodology: all 8 approaches, KS testing, ML classification, parameter retrodiction, multi-bar sequences
- `references/export-audit-methodology.md` — 6-layer data integrity audit for multi-stage pipelines. Run before trusting any export's output.
- `references/swing-research-pipeline.md` — Proper backtesting architecture: ATR ZigZag labeling, triple-barrier labels, chronological train/val/test splits, LightGBM per direction, permutation tests. Replaces the old manual-threshold-sweep approach.
- `templates/indicator-export.pine` — Pine Script template for exporting RSI/EMA/MACD/ATR indicators at signal bars (next frontier for cracking FATCAT)
- `scripts/download_perp_data.py` — Download BTCUSDT perpetual 5m candles from Binance Futures API (includes taker_buy_base_asset_volume)

## Delivery to External Auditors

When the user asks for Pine scripts or analysis scripts for Claude to audit:
- **Save as .txt files** in the `scripts/` directory — Claude reads .txt directly
- **Provide the raw scp download command** in the response (e.g. `scp root@178.156.199.37:/path/to/file ./`). Do NOT describe where the file is — give the exact command.
- **Keep explanations minimal** — verbose in-chat explanations waste turns; let the script's comments speak
- **Name files with a numeric prefix** (`01_`, `02_`, etc.) for ordering clarity
- **Generate both PNG and HTML visualizations** when producing charts — the user views on mobile, Claude views interactively
- **Summarize data status as tables, not prose** — columns: Data | Rows | Range | Status
- **When asked for a breakdown, use a tree structure** (ASCII or markdown), not a narrative
- **Offer scp commands for bulk downloads** — the user prefers `scp -r` pattern over individual file transfers

## Data Integrity — Mandatory Checks (Run After Every Export)

**Every new export must pass ALL 7 sanity checks before being trusted for analysis.** The audit script at `scripts/audit-export-pipeline.py` runs these automatically, but here's what to verify manually when the script is not available:

1. **Feature consistency:** `vb + vs ≈ vol` within 1% for ALL signals. If this fails, the `str.tostring()` calls are broken (see Pine v6 function scope bug above).
2. **Ratio consistency:** `volRatio ≈ vol / avgVol` within 1% and `vdRatio ≈ |vd| / vol` within ±0.001.
3. **No NaN values:** Scan every feature column — any NaN indicates a computation failure at the Pine level.
4. **Binary flags:** `ema21_bear`, `ema21_bull`, `ema50_bear`, `ema50_bull` must be exactly 0 or 1.
5. **Timestamp alignment:** Every signal timestamp must match a perp candle within ±5 minutes.
6. **Date range coverage:** Perp data must span the entire signal date range.
7. **Duplicate detection:** No duplicate `(Date and time, Price USDT)` pairs in the export.

**Common failure modes that these checks catch:**
- Deferred comment evaluation issue → check 1 fails (vb/vs are NaN or wrong)
- KEY=VALUE format → check 1 fails (Feature vector has wrong split count, parser skips rows)
- `str.tostring(val, "#.##")` compile error → export never produced
- Timezone mismatch → check 5 fails
- Perp data missing range → check 6 fails

The canonical export script (v2.2) is at `pinescript/bambam-delta-24feat-export.pine` in the project and `scripts/04_bambam_24feat_delta_export.txt`. It has:
- Full bug history (v1 → v2 → v2.1) in header comments — read before modifying
- All `str.tostring()` calls at top-level scope (no function scope bug)
- Fixed `volRatio_delta` computation (`avgVol[5]`)
- Entry IDs "BEAR"/"BULL" matching the raw signal capture script
- Inline `bear_comment`/`bull_comment` construction — no `make_comment()` function
- A Python parser data contract section listing every feature index → name mapping
- Usage instructions and all 7 sanity checks listed in comments

**DO NOT modify the v2.1 script lightly.** Every feature index position is locked by the Python parser's FEAT_NAMES list. Changing the order breaks the analysis pipeline silently (values map to wrong feature names).