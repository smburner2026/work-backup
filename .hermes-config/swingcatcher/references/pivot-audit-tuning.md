# Pivot Audit and Label Tuning Reference

## Purpose

Diagnosed why BAMBAM signals at structural pivot points don't always get labeled
"true reversal." The script `scripts/02_audit_pivots.py` produces a ranked table
of pivots sorted by missed-counter-move magnitude with the specific reason each
failed. This file records the tuning history and diagnostic patterns.

## Tuning History (5m, 90-day BTCUSDT)

### v1 (initial, zigzag=2.0, rev=3.0, hold=24)
- Pivots: 7,994 (1 per 8 bars — way too many, catching noise)
- Reversal rate: 60.6% (way too high — catching pullbacks as reversals)
- Verdict: zigzag_atr_mult=2.0 means $100-200 threshold = 0.10-0.17% at $115k BTC
  which is sub-noise. Tripled to 8.0.

### v2 (retuned, zigzag=8.0, rev=12.0, hold=48)
- Pivots: 599 (~6.6/day — good)
- Reversal rate: 6.7% (in 5-15% target band)
- Audit failure modes:
  - 85% too far from pivot (mostly Oct-Feb pivots without signals)
  - 13% excursion failed (median 7.65 ATR vs 12.0 threshold)
  - 2% hold failed
- User feedback: Missing Mar 4, 17, 22 pivots. All had excursions 9-23 ATR
  but fell below the 12.0 threshold or failed the 48-bar hold.
- Diagnosis: Thresholds too tight — 70% of near-pivot failures were excursion
  failures with median 7.65 ATR, well above noise but below the 12.0 cutoff.

### v3 (relaxed, zigzag=8.0, rev=7.0, hold=24, prox=24)
- Pivots: 599 (unchanged — pivots themselves are good)
- Reversal rate: 29.5% (above 5-15% target band, under review)
- Audit failure modes:
  - 91% too far (still dominated by pre-Feb pivots)
  - 7% excursion failed (down from 13% — the 7.0 ATR threshold helped)
  - 2% hold failed (unchanged)
- Captured: Expect ~127 true labels (vs 29 in v2)

## Key Diagnostic Patterns

1. **If a pivot shows "nearest sig is N bars from pivot (max M)":**
   - N >> M = Cause B (BAMBAM structurally doesn't fire near this type of pivot)
   - N approx M = borderline; consider loosening proximity
   - Data-range filter: if the pivot is before the earliest signal date, this is
     a data-range artifact, not a BAMBAM bug

2. **If a pivot shows "excursion failed":**
   - Check the actual excursion value vs the threshold
   - Median failed-excursion across ALL missed pivots tells you if the threshold
     is systematically too high
   - This is the most common tuning lever

3. **If a pivot shows "hold failed":**
   - The counter-move was real but didn't sustain
   - Common on spike-and-consolidation reversals (moves fast then crawls)
   - Loosening hold captures more sharp reversals but risks labeling wick-fakeouts
   - Check hold_bars value — if it's close to threshold, loosening may help

4. **"no signals of matching direction"** — Rarest cause. Means the entire export
   has zero signals in the direction of this pivot type. Unusual for balanced markets.

## Running the Audit

```bash
cd /root/work/trading/bambam-fatcat-project/swing_research
python scripts/02_audit_pivots.py configs/tf_5m.yaml
```

Output: `outputs/pivot_audit_5m.csv` with full table, plus console summary
of failure mode distribution and ranked \"biggest missed pivots\" table.

The audit script points to the current `configs/tf_5m.yaml` — override with
`tf_5m_v2.yaml` or `tf_5m_v3.yaml` to run against different tunings.
