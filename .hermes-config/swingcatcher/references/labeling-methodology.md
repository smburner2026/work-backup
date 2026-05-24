# Labeling Methodology — May 23 2026

## What Changed and Why

The original SwingCatcher pipeline (May 21-22) used a **Close+48 fixed-horizon label:
`ret > 0.5%` at exactly bar+48. This missed:

- **Spike-and-consolidate patterns** — price hits +2% at bar 22 then retraces to flat by bar 48
- **Gap-and-reverse** — price opens favorable, reverses within hours, then re-enters trend

Claude's audit revealed this was the wrong target. FATCAT-style reversal detection needs
**structural pivot proximity**, not a directional return at a fixed future point.

## The Corrected Methodology (ZigZag + Triple-Barrier)

### Step 1: Find Structural Pivots (Not Noise Swings)

ZigZag with **ATR-based threshold** (not fixed %):

```
Walk forward bar by bar.
Maintain a tentative extreme (highest high or lowest low).
When price reverses by ≥ N × ATR from the extreme, CONFIRM the pivot.
Discard unconfirmed pivots at data edges.
```

ATR-based = self-tuning across volatility regimes:
- Low-vol environment: a 1.5% swing is a real pivot
- High-vol environment: 3-5% may be noise
- Wilder's smoothing matches `ta.atr()` in Pine

### Step 2: Label Each Signal — 3 Conditions

A signal is a "true reversal" if ALL THREE are satisfied:

1. **Proximity** — Signal fires within P bars of a confirmed pivot
2. **Excursion** — Counter-move after pivot ≥ X × ATR
3. **Sustained (Holding)** — Counter-move lasts ≥ M consec bars

False otherwise (failed on proximity, excursion, or holding).

### Step 3: Diagnose Failures

The `02_audit_pivots.py` script reports WHY each pivot was missed:

| Failure Mode | What it means | Fix lever |
|---|---|---|
| Signal too far from pivot | No BAMBAM signal within P bars | Increase `pivot_proximity_bars` |
| Excursion failed | Counter-move existed but < X × ATR | Decrease `min_reversal_atr_mult` |
| Holding failed | Counter-move started but didn't sustain M bars | Decrease `min_holding_bars` |

### Config Tuning Sequence (What We Actually Ran)

| Iteration | zigzag | proximity | reversal | holding | Reversal Rate | Lesson |
|---|---|---|---|---|---|---|
| v1 | 2.0 ATR | 6 bars | 3.0 ATR | 24 bars | 60.6% | WAY too loose — 7,994 pivots on 67k bars |
| v2 | 8.0 ATR | 12 bars | 12.0 ATR | 48 bars | 6.7% | Too tight — missed Mar 4, 17, 22 structural pivots |
| v3 | 8.0 ATR | 24 bars | 7.0 ATR | 24 bars | 29.5% | In target zone, awaiting visual review |

### Key Insight: Median Missed Excursion

v2 audit showed median excursion of missed pivots = **7.65 ATR**. This directly drove
v3's relaxation from 12.0→7.0. Without the audit numbers, tuning would be guessing.

## Comparison: Old vs New Pipeline

| Dimension | Old (May 21-22) | New (May 23) |
|---|---|---|
| **Label** | `close[idx+48] > 0.5%` | `triple_barrier(TP, SL, horizon) OR ZigZag proximity` |
| **Validation** | None (all data) | Chronological 60/20/20 |
| **Metric** | Hit rate | Expectancy + AUC + calibration |
| **Model** | Threshold grid (200 lines) | LightGBM (30 lines) |
| **Feature selection** | Manual pair/triple sweeps | Built-in feature importance |
| **Sanity checks** | None | Permutation test + time-decay + calibration |

## Relationship to Triple-Barrier Labeling

The ZigZag approach captures **structural reversals** specifically. Triple-barrier
labeling (from López de Prado) is a superset that captures ANY path-dependent
outcome (TP hit, SL hit, or timeout). For FATCAT-style reversal detection, the
ZigZag + ATR combo is more targeted because it explicitly asks: "Was this signal
at/near a confirmed pivot?"

If we later layer in OI and funding-rate features, triple-barrier becomes more
useful because we want to capture ANY profitable outcome (including trend
continuation) rather than just pivots.

## Data Status

- v2.2 Pine export: 431 signals, 24 features, volRatio_delta fixed, provenance audited
- Binance perp 5m data: 168k candles (May 2025–Jun 2026) with OI, taker ratio, top trader ratios, funding, and premium index (basis)
- Merged CSV has 13 data columns + basis_bps
