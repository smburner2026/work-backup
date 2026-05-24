# Export Data Integrity Audit — 6-Layer Methodology

When exporting TradingView features via CSV and using them in a multi-stage analysis pipeline, verify EVERY layer independently. Each transformation (Pine → CSV → Python parse → timestamp alignment → feature math → outcome labeling) can silently corrupt or misalign data.

## The 6 Layers

### Layer 1: Raw CSV Format
- **Check**: Entry rows present? Duplicate (time, price) keys? Signal column parses correctly?
- **Common pitfall**: KEY=VALUE format in the Pine comment string (e.g. `BEAR|v=123.45`) instead of raw floats (`123.45`). The analysis code expects raw floats — labelled values crash silently.
- **Check**: NaN/null floats in feature values. Pine `na` converts to string `"na"` which crashes `float("na")`.
- **Fix**: Strip BOM (`\ufeff`), only process `'Entry'` rows, deduplicate on `(Date and time, Price USDT)`.

### Layer 2: Timestamp Alignment (TV export vs Price Data)
- **Check**: Every signal time matches a perp candle within ±5 minutes.
- **Check**: The signal time range is fully covered by the price data range.
- **Common pitfall**: TV Strategy Tester exports in UTC? Local? Need to verify timezone. Signal fires on bar `close` (T+5min) or bar `open` (T)?
- **Reference offset**: For BAMBAM signals that fire on bar close, the feature values are from bar `[1]` (prior bar). When aligning to perp candles, use `signal_time - 5min` to get the prior bar.
- **Fix**: Build a set of all perp candle timestamps, check each signal time ±5min.

### Layer 3: Feature Math Consistency
- **Check**: Derived features match their definitions:
  - `volRatio = vol / avgVol` (within 1%)
  - `vdRatio = |vd| / vol` (within ±0.001)
  - `vb + vs ≈ vol` (within 1%)
  - Cross flags (`ema21_bear/bull`, `ema50_bear/bull`) are 0 or 1
- **Check**: 7-feat and 24-feat exports agree on shared fields when run on the same signal set.
- **Common pitfall**: Pine's `math.sum(vol, lookback) / lookback` gives a WEIRD SMA (sum over lookback bars, NOT the same as rolling SMA starting at bar 0). The first `lookback-1` bars have partial data — features may be computed on incomplete lookback windows.
- **Fix**: For the first `lookback` bars, avgVol is computed on fewer than `lookback` samples. This only matters for very early signals.

### Layer 4: Price Data Integrity
- **Check**: Sorted by timestamp, no duplicates, no gaps (every 5-minute interval present).
- **Check**: Prices in sane range, volumes non-negative.
- **Check**: `taker_buy_base_vol ≤ volume` (basic sanity — taker buy can't exceed total volume).
- **Common pitfall**: Multiple price data files exist (Binance Futures perp vs Binance.US spot). They have similar column names but different volume levels (500-1000 BTC/5m perp vs 0-3.7 BTC/5m spot). Conflating them produces wrong analysis.
- **Fix**: Check volume distribution — if max volume per 5m candle is <10 BTC, it's spot data. If it's >100 BTC, it's perp. Futures files also have `taker_buy_base_vol` column; spot files don't.

### Layer 5: Ground Truth Verification
- **Check**: Every "positive" label (FATCAT entry, known swing hit) matches a raw signal within a reasonable tolerance.
- **Check**: No duplicate ground truth entries (unless multiple DCA lots — deduplicate on timestamp + signal number, not timestamp + price).
- **Common pitfall**: FATCAT CSVs may show 31 short rows but 24 unique entries. The extra 7 are DCA add-lots at the same price. Count unique entry timestamps, not total rows.
- **Fix**: Deduplicate FATCAT entries on `(Date and time, direction)` not `(Date and time, Price USDT)`.

### Layer 6: Swing Label Verification (Outcome Assessment)
- **Check**: Does the labeling method (close-at-N-bars vs best-excursion vs worst-excursion) produce consistent results?
- **Check**: Do specific known events (e.g. user-verified entries) produce the expected labels?
- **Common pitfall**: The 0.5% swing threshold is arbitrary. A signal that moves 0.32% passes FATCAT's filter but fails our swing check. This is a design tradeoff, not a data error — but should be surfaced.
- **Fix**: Run the audit with multiple thresholds (0.3%, 0.5%, 0.75%, 1.0%) and compare hit rates.

## When to Run This Audit

1. **After first export for a new pair/timeframe** — catches format mismatches before any analysis
2. **After pipeline changes** — verifies modifications didn't break parsing
3. **Before user-facing claims** — ensures you're not presenting flawed data
4. **When exporting from a different TV broker** — different brokers may format data differently

## Script

See `scripts/audit-export-pipeline.py` — a comprehensive 6-layer audit script. Copy it to your project directory, update the file paths at the top, and run.

```
python3 audit-export-pipeline.py
```

It produces a pass/fail/warning for each check at each layer. Fix any failures before proceeding to analysis.
