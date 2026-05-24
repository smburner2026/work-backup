# Reverse-Engineering a Hidden Indicator Filter (Methodology)

## Problem

You have two indicators: a known "base" (BAMBAM) and a closed-source "selective fork" (FATCAT). The selective fork produces fewer signals. You need to reverse-engineer the filter parameters.

## Step 1: Confirm Subset Relationship (Rectangle Check)

Create a raw signal strategy (no cooldown, no DCA, no pyramiding limits):
- `strategy()` with `pyramiding=9999`, `default_qty_value=1`
- Every arrow the indicator draws = one strategy entry
- Export Strategy Tester CSV

Compare raw signal timestamps against target entries:
- Match within ±10 minutes (5-minute timeframe)
- Count: does every target entry have a corresponding raw signal?

**If YES:** The filter operates on raw signals. You can brute-force it.
**If NO:** The target has fundamentally different signal logic. Stop trying to tune base parameters.

## Step 2: Timestamp-Only Filter Sweep

Test these filters using only signal timestamps (no OHLCV data needed):
- Same-direction cooldown (1-48h)
- Any-direction cooldown
- Asymmetric cooldowns (different for long/short)
- "First in cluster" (only position 1 in burst)
- Time-of-day filtering
- Signal density (count of same-dir signals in last N hours)

**Expected result:** If F1 maxes around 0.35-0.40, the filter is fundamentally volume/delta-based. Timestamp filters alone cannot reproduce it.

## Step 3: Get Perp-Specific Feature Data

**⚠️ CRITICAL:** Use the SAME data source as the target indicator. If it runs on TradingView BTCUSDT.P (Binance perpetuals), you MUST use perp data:
- Binance.US spot produces DIFFERENT volume patterns (245 signals vs 434 from TV)
- Price discrepancy is small ($47 mean on $70k = 0.07%) but volume delta/volumeRatio are uncorrelated
- Only 37/72 FATCAT matches with ±15min window using spot data

### Feature Export via Pine Script Comment Strings

TradingView Strategy Tester CSV does NOT include `plot()` values (even with `display=display.data_window`). The "Export chart data" option may not be available on all accounts. **Workaround:** embed feature values in `strategy.entry(comment=...)`:

```pinescript
if bearRaw
    strategy.entry("S", strategy.short, comment=str.tostring(vol) + "|" + str.tostring(vd) + "|" + str.tostring(avgVol) + "|" + str.tostring(vol/avgVol) + "|" + str.tostring(vdRatio) + "|" + str.tostring(vb) + "|" + str.tostring(vs))
```

Each entry's Signal column becomes: `421.043|130.264|346.152|1.216|0.309|275.653|145.389` (vol|vd|avgVol|volRatio|vdRatio|vb|vs). Parse with Python: `row['Signal'].split('|')`.

**⚠️ Do NOT use `str.tostring(val, "#.##")` format strings** — they cause null translation errors in Pine v6. Use plain `str.tostring(val)`.

## Step 4: Brute-Force Parameter Sweep

With perp-specific features computed for each raw signal:
1. Label each signal as target-selected (1) or rejected (0) via timestamp matching
2. Sweep all parameter combinations: volRatio × vdRatio × deltaMode × cooldown
3. For each combo: compute which signals pass, score F1 against target labels
4. The winning parameter set produces ~72 signals with highest F1

## Step 5: Statistical Validation

If the best parameter sweep F1 is below 0.40:
1. **KS test per feature** — test whether target-selected vs rejected signals have significantly different distributions for each feature
2. **Decision tree classifier** (depth 2-6) — check if any combination of features separates the classes
3. **Random Forest / Gradient Boosting** — check for nonlinear decision boundaries
4. If all approaches overfit (train F1 >> CV F1), the features available cannot reconstruct the filter

## Step 6: Assess Whether the Filter is Recoverable

| CV F1 | Conclusion |
|-------|-----------|
| ≥ 0.8 | Filter successfully reverse-engineered |
| 0.5-0.8 | Partial — main factor found, secondary factor missing |
| 0.3-0.5 | Features insufficient — filter likely uses data not in your feature set |
| < 0.3 | Fundamentally different logic or data source |

## Definitive Results (BAMBAM → FATCAT, May 2026)

### Approach 1: Timestamp-only filters
- **Best F1: 0.393** (asymmetric cooldown: 40h short, 2h long)
- Cooldown alone cannot reproduce FATCAT — too many false positives

### Approach 2: Volume feature thresholds (candle-body estimate)
- **Best F1: 0.378** (volRatio ≥ 3.5, no cooldown)
- Statistically significant but not classifiable:
  - volRatio: KS=0.232, p=0.006 (shorts KS=0.263, p=0.042)
  - vol: KS=0.233, p=0.001 (shorts KS=0.314, p=0.008)
  - vb: KS=0.308, p<0.001 (shorts KS=0.418, p=0.0001)
  - vdRatio: KS=0.147, p=0.097 (not significant)

### Approach 3: Combined timestamp + feature sweeps
- **Best F1: ~0.38** (no improvement over either alone)

### Approach 4: Decision tree (depth 2-6)
- **Best CV F1: 0.36** (depth=2)
- Overfits beyond depth 2 (train F1 >> CV F1)

### Approach 5: Random Forest (200 trees, 18 features)
- **CV F1: 0.15** (train F1=1.0 — massive overfitting)
- Added derived features: vb/vs ratio, abs(vd), vd_per_vol, vb_pct, vs_pct, time since last signal, signal density — none helped

### Approach 6: Gradient Boosting (100-200 estimators)
- **CV F1: 0.18** (train F1=1.0 — same overfitting pattern)

### Approach 7: KS test per feature
- Shorts: vb (KS=0.418, p=0.0001), vol (KS=0.314, p=0.008), volRatio (KS=0.263, p=0.042) — statistically significant but overlap too large for classification
- Longs: vb (KS=0.292, p=0.002), vol (KS=0.235, p=0.024), volRatio (KS=0.232, p=0.026) — same pattern
- vdRatio NOT significant (p=0.286 shorts, p=0.192 longs)

### Conclusion

**F1 wall at ~0.38-0.39 across ALL approaches.** The candle-body volume features that BAMBAM computes (vol, vd, vb, vs, avgVol, volRatio, vdRatio) CANNOT reconstruct FATCAT's filter. The distributions overlap too much for any threshold or ML model to separate them.

**Most likely explanation:** FATCAT uses taker buy/sell volume from perps exchange data, which is fundamentally different from the candle-body estimate `vb = volume * (close-low)/(high-low)`. The `ta.takers_buy()` function may provide this on supported brokers, but it did not compile on the user's broker (CE10272), and TV's "Export chart data" feature was not accessible.

**Next step:** Either find a way to export actual taker volume from TradingView (may require broker-specific support), or accept that FATCAT's filter cannot be reverse-engineered from available data and focus on building the best approximation.

## Key Findings Summary

| Finding | Detail |
|---------|--------|
| FATCAT ⊂ BAMBAM | 72/72 match at raw signal level (±10min) |
| Filter reduction | 434 → 72 (83.4% rejection) |
| Asymmetry | 90.3% short rejection, 74.2% long rejection |
| Best timestamp-only F1 | 0.393 (40h short, 2h long cooldown) |
| Best feature threshold F1 | 0.378 (volRatio ≥ 3.5) |
| Best ML F1 (CV) | 0.36 (decision tree depth=2) |
| ML overfitting | Train F1=1.0, CV F1=0.15-0.18 |
| Most discriminating feature | vb (buy volume estimate) — KS=0.418, p<0.001 |
| Feature overlap | Too large for classification at any threshold |
| Spot vs perp signals | 245 vs 434 on same period |
| Spot FATCAT matches | 37/72 (vs 72/72 with perp) |