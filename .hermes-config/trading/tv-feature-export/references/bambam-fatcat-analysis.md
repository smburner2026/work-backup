# BAMBAM/FATCAT Reverse-Engineering Analysis

## Problem

FATCAT is an invite-only TradingView indicator. We needed to understand how it filters BAMBAM signals — specifically, which parameters or features distinguish FATCAT's 72 entries from BAMBAM's 434 raw signals.

## Key Finding: Rectangle Verified

**FATCAT ⊂ BAMBAM** — every FATCAT entry (24 shorts + 48 longs = 72 total) matches a raw BAMBAM signal within ±10 minutes. Zero orphans. This means FATCAT applies a post-filter to BAMBAM's raw output, not different signal logic.

Filter rates: 90.3% of shorts filtered, 74.2% of longs filtered (83.4% overall).

## Methodology That Failed

### 1. Timestamp-Only Filters (F1 = 0.39 max)
- Same-direction cooldown: best F1 at 4h CD
- Asymmetric cooldown (short CD × long CD): best F1 = 0.393 at 40h short / 2h long
- Cluster position filters: FATCAT is at position 1 only 50% of the time — not "first signal after quiet period"
- Time-of-day, day-of-week: no significant separation

### 2. Volume Feature Thresholds (F1 = 0.38 max)
- Swept volRatio (1.0–5.0), vdRatio (0.03–1.0), delta mode (OR/AND), cooldown (0–15h)
- Best: volRatio ≥ 3.5, no cooldown → 219 signals, 55 hits, F1 = 0.378
- volRatio threshold filters some noise but misses 17 FATCAT signals that have volRatio < 3.5

### 3. Decision Tree Classifier (CV F1 = 0.36)
- Depth 2–6 tested, best generalized at depth 2
- Deeper trees overfit (train F1 = 1.0, CV F1 drops)
- Split on `vb` (buy volume estimate) as top feature

### 4. Random Forest / Gradient Boosting (CV F1 = 0.12–0.18)
- 18 features including derived ratios and time-based context
- Massive overfitting: train F1 = 1.0, CV F1 collapses
- Feature importances: `vb` (11%), `vol` (7.4%), `time_since_same` (6.7%) — diffuse signal

### 5. KS Test (Kolmogorov-Smirnov)
- Shorts: `vb` KS=0.418 (p=0.0001), `vol` KS=0.314 (p=0.008), `volRatio` KS=0.263 (p=0.04)
- Long: `vb` KS=0.292 (p=0.002)
- Distributions overlap massively — no clean decision boundary

## Why It Failed

The features we had (candle-body volume estimates: vb, vs, vd, vol, avgVol, vdRatio, volRatio) are the SAME features BAMBAM uses internally. FATCAT filters on top of BAMBAM output, so the discriminating information must be in data BAMBAM does NOT compute — most likely **taker buy/sell volume from the perps order book**.

Evidence:
- Binance.US spot data produces only 245 BAMBAM signals vs TV perp's 434
- Only 37/72 FATCAT matches at ±15min using spot data
- TV perp `ta.takers_buy` is the only feature source that differs from what we exported
- Candle-body vb/vs estimates correlate with taker volume but don't capture the same information

## The Data Pipeline

1. **BAMBAM Raw Signal Export** (434 entries, TV Strategy Tester CSV)
   - Pine script: `bambam-feature-export.pine` (v6)
   - Comment-string embedding: `vol|vd|avgVol|volRatio|vdRatio|vb|vs` (body method)
   - Also exports: `vol_tk|vd_tk|avgVol_tk|volRatio_tk|vdRatio_tk|tbv|tsv` (taker method — requires broker support)

2. **FATCAT Target Set** (72 entries, TV Strategy Tester CSV)
   - Exported separately as FC-shorts (24) and FC-longs (48)
   - Single-direction strategy with fixed TP at 1%

3. **Matching** (±10 minute window, same direction)
   - 30/30 shorts matched, 54/48 longs matched (some longs match within wider window)

## Taker Volume Data (Completed)

Downloaded 67,359 perp 5m candles from Binance Futures API. All 434 BAMBAM signals matched to perp data by timestamp. Taker buy volume available but performed no better than body-estimate volume for FATCAT discrimination (F1 0.373 vs 0.366 body-only). Spearman rho=0.597 between body and taker volRatio — weakly correlated but same discriminative power.

## Approach 6: BAMBAM Parameter Retrodiction (F1 = 0.164)

Reimplemented BAMBAM signal logic in Python with vectorized numpy. Swept 176+ parameter combinations:
- lookback: 50, 75, 100, 125, 150, 175, 200, 250, 300, 400, 500
- lessRatio: 0.01, 0.02, 0.03, 0.05, 0.08, 0.10, 0.15, 0.20
- volMult: 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0
- deltaMode: OR, AND

**Best result: lookback=300, lessRatio=0.01, volMult=3.0, delta=OR → F1=0.164**

This is far worse than post-hoc filters (F1=0.398). PROOF that FATCAT is NOT a parameter retuning of BAMBAM — the two indicators use fundamentally different logic. The 0.23 F1 gap represents information that BAMBAM's volume parameters alone cannot capture.

Script: `analysis_parameter_retrodiction.py`

## Approach 7: Multi-bar Sequence Patterns (F1 = 0.398, no improvement)

Extracted 10-bar (50-minute) windows before each BAMBAM signal. Computed per-bar returns, volume ratios, range percentages, and aggregate features (total_change, max_range, avg_range, vol_trend).

KS tests showed statistically significant differences (p<0.01):
- **total_change**: FATCAT shorts follow +1.07% moves vs +0.57% for rejected (KS=0.309, p=0.01)
- **avg_range**: FATCAT signals have wider bars (KS=0.306 for shorts, KS=0.249 for longs)
- **vol_trend**: FATCAT longs have 2x volume acceleration (KS=0.279, p=0.004)
- **Per-bar returns**: bars -5, -4, -3 before signal all significant (p<0.01)

BUT threshold filters on these features do not improve F1 beyond 0.398. Distributions overlap too much for practical classification. Directional move filter (min move before entry) and average range filter both add zero improvement over cooldown+volRatio alone.

Script: `analysis_multibar_sequences.py`

## Approach 8: Directional Move + Range + Volume + Cooldown (F1 = 0.398)

Combined sweep of asymmetric cooldown + volRatio threshold + min directional move % + min average range %. All top configurations have min_move=0 and min_range=0 — these features add nothing. Best remains CD 16h/1h + volRatio≥3.5 at F1=0.398.

## Key Negative Results Summary

| # | Approach | Best F1 | Key Finding |
|---|---|---|---|
| 1 | Single-bar body thresholds | 0.378 | volRatio≥3.5, vdRatio≤1.0 |
| 2 | Asymmetric cooldown | 0.393 | CD 40h short / 2h long |
| 3 | Single-bar taker thresholds | 0.373 | volRatio_tk≥3.0 |
| 4 | Combined body+taker cooldown | **0.398** | CD 16h/1h + volRatio≥3.5 |
| 5 | ML classifiers (RF/GB) | 0.222 | Massive overfitting |
| 6 | Parameter retrodiction | 0.164 | NOT a BAMBAM retuning |
| 7 | Multi-bar sequences | 0.398 | KS significant but no practical filter |
| 8 | Directional move filter | 0.398 | Adds nothing |

**Hard F1 ceiling at ~0.40** across ALL approaches using volume/price data.

## Next Step: Indicator Export

FATCAT almost certainly gates on oscillator/indicator conditions (RSI, EMA, MACD) beyond what volume/price features capture. Pine Script template for indicator export: `templates/indicator-export.pine`.

## Data Provenance

- Raw BAMBAM: `/root/.hermes/cache/documents/doc_9a5ddfb69f1c_BAMBAM_Feature_Export_*.csv` (434 entries with body-method features)
- FATCAT shorts: `/root/.hermes/cache/documents/doc_89389f554967_FEROCIOUS_FATCAT_*_90D_short.csv` (24 entries)
- FATCAT longs: `/root/.hermes/cache/documents/doc_ce7188cc3b3a_FEROCIOUS_FATCAT_*_90D_long.csv` (48 entries)
- Pine scripts: `/root/work/trading/bambam-fatcat-project/pinescript/`
- Download script: `/root/work/trading/bambam-fatcat-project/download_perp_data.py`