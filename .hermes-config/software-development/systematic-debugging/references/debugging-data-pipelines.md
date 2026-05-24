# Debugging Multi-Layer Data Pipelines

This reference documents the systematic approach for debugging data corruption
in multi-layer pipelines where each layer transforms or extracts data.
Learned from the BAMBAM feature export pipeline (May 2026).

## The Pipeline Pattern

Pine Script (TV) → CSV Export → Python Parser → Feature Validation → Analysis

Each layer is a potential corruption site. The bug is rarely where you think it is.

## Typical Surface Pattern

The symptom looks like:
- Analysis results are noisy/unexpected
- Feature values don't add up (vb+vs≠vol)
- Known-good signals don't match
- Feature importance contradicts intuition

## Layer-by-Layer Investigation

### Layer 1: Pine Script Generation
**Check:** Does the Pine script compute the values it thinks it does?

Symptoms:
- Compilation errors (str.tostring format strings, undefined identifiers)
- Series offsets producing NaN (especially in UDFs called from strategy.entry())
- Wrong variable names or misplaced offsets

**Verification:**
- Run the script on TV with plot() calls for each major variable
- Compare computed values against known reference points
- Test WITHOUT the function wrapper — inline the string building

**Common failure (observed):** `str.tostring(vb1[1])` inside a function called from
`strategy.entry(comment=fn())` produces NaN. This is NOT a general Pine v6 UDF bug.
It's specific to the deferred evaluation context of strategy.entry(). Pre-compute
at top level.

### Layer 2: CSV Export
**Check:** Does the exported CSV contain the right data?

Symptoms:
- BOM character corrupts first column name
- Feature string has wrong pipe-delimited count
- Signal column has comment text instead of feature vector
- Duplicate entries from overlapping signals
- Exit rows mixed with entry rows

**Verification:**
- Read the raw Signal column for the first 5 entries — does it match what the
  Pine script's `strategy.entry(comment=...)` should produce?
- Count pipe-delimited parts: v1 7-feat = 7, v2 delta = 25
- Check for KEY=VALUE strings (indicates format mismatch)
- Deduplicate on (Date and time, Price USDT, direction-prefix)

**Common failure (observed):** Pine script saved in project uses KEY=VALUE format
but the actual analysis expects raw pipe-delimited floats. The saved script ≠ the
exported CSV format.

### Layer 3: Python Parser
**Check:** Does the feature-to-variable mapping match the Pine export order?

Symptoms:
- Features appear to be from wrong categories (e.g., vb where vdRatio expected)
- NaN values after float() conversion
- All signals skipped (wrong parts count)
- Feature math is self-consistent but doesn't match known-good reference data

**Verification:**
- Print the first entry's raw parts alongside their assigned feature names
- Verify: parts[i] should correspond to the i-th value in the Pine comment string
- Check that len(parts) matches the hardcoded expected count
- For 24-feat exports: the order is vol, vd, avgVol, volRatio, vdRatio, vb, vs,
  rsi14, rsi7, dist_ema21, dist_ema50, dist_ema200, macd_hist, atr14,
  rsi14_delta, rsi7_delta, macd_hist_delta, price_mom5, volRatio_delta,
  vdRatio_delta, ema21_bear, ema21_bull, ema50_bear, ema50_bull
  (FEAT_NAMES list in analysis scripts and data_loader.py)

### Layer 4: Feature Validation
**Check:** Do the numbers internally check out?

Six checks that catch most pipeline bugs:
1. vb + vs ≈ vol (within 1%)
2. vdRatio ≈ |vd| / vol (within 0.001)
3. volRatio ≈ vol / avgVol (within 1%)
4. All cross flags are 0 or 1
5. No NaN in any feature column
6. Signal timestamps match perp data ±5min

**If check 1 fails:** The Pine export script has a series offset issue (see Layer 1).
**If check 2 fails while check 1 passes:** The vdRatio field is from a different source
than vd and vol.
**If check 5 fails:** The Pine computation produced NaN on some bars.

## When Data Looks Clean But Analysis is Wrong

If all 6 checks pass but analysis results still seem wrong:

1. Check the DATA SOURCE — is this futures perp data or spot data?
   - BTCUSDT Futures: 500+ BTC/candle typical, has taker_buy_base_vol
   - BTCUSDT Spot: 0-3.7 BTC/candle typical, limited taker data
   - Conflating them produces wrong results

2. Check the FEATURE TIER — what export was actually used?
   - 7-feat: body volume only
   - 14-feat: body + indicator levels
   - 24-feat: body + levels + deltas + cross flags
   - Different tiers produce different feature importance rankings

3. Check for BUGGY EXPORT versions
   - v1 (May 22): volRatio_delta has shifted averaging window (systematic bias)
   - v2 (May 23): make_comment() UDF corrupts vb/vs values
   - v2.2 (May 23): CLEAN — use this version

## Root Cause Documentation

When a pipeline bug is found, document:
1. Which layer the bug lives in (Pine, CSV, Python, validation)
2. The failure mechanism (not the symptom — the mechanism)
3. Which checks catch it (prevention)
4. Whether the analysis results that used the buggy data need re-running

For example:
- Bug: Pine UDF + strategy.entry() deferred eval
- Layer: 1 (Pine)
- Mechanism: str.tostring(series[n]) in UDF called from strategy.entry(comment=fn())
  sees stale series cache
- Check: vb+vs≈vol during import
- Impact: All v2 export analysis invalidated; v2.2 re-export needed
