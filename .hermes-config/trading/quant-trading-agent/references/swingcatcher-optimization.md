# SwingCatcher Optimization — BAMBAM + Indicator Layer (May 2026)

## Problem

Build a better version of FATCAT from scratch — find BAMBAM parameters + indicator filters that maximize swing high/low capture rate (price moves >0.5% in signal direction within 4 hours).

## Methodology

### Ground Truth Labeling
- **Signal:** BAMBAM fires arrow at time T, direction D, entry at open price
- **Swing hit:** If D=short and close[T+48] < entry * 0.995 (price fell ≥0.5%), or D=long and close[T+48] > entry * 1.005 (price rose ≥0.5%)
- **Target:** 4 hours forward (48 x 5m bars), 0.5% threshold
- **Data:** 434 BAMBAM signals from 90-day TV export, matched to perp OHLCV

### BAMBAM Parameter Grid
- lookback: [50, 100, 200, 400]
- lessRatio: [0.01, 0.05, 0.10, 0.20]
- volMult: [0.5, 1.0, 2.0]
- deltaMode: ['OR', 'AND']

### Indicator Filters
Tested per signal: volRatio, vdRatio, vb, vs, avgVol, dist_ema200, dist_ema50, dist_ema21, macd_hist, rsi14, atr14, rsi14_delta, macd_hist_delta, price_mom5

SHORT_HIGHER features: for shorts, pass if feature >= threshold. For longs, pass if feature <= threshold.
SHORT_LOWER features (vdRatio): for shorts, pass if feature <= threshold. For longs, pass if feature >= threshold.

Filter applied at percentiles: 70%, 75%, 80%, 85%

## Results

### Phase 1: Raw BAMBAM Parameter Rankings (by swing hit rate)

| Rank | LB | LR | VM | DM | Hit% | n | sig/week |
|------|----|----|----|----|-------|----|----------|
| 1 | 400 | 0.20 | 0.5 | AND | 35.3% | 156 | 12.0 |
| 2 | 200 | 0.05 | 2.0 | AND | 35.0% | 40 | 3.1 |
| 3 | 400 | 0.20 | 1.0 | AND | 34.6% | 153 | 11.8 |
| 4 | 400 | 0.05 | 0.5 | AND | 34.2% | 38 | 2.9 |
| 5 | 400 | 0.01 | 0.5 | OR | 31.8% | 757 | 58.2 |

**AND mode dominates** — pure exhaustion (`isLess AND vd<0` for shorts, `isLess AND vd>0` for longs) consistently outperforms OR mode.

### Phase 2: Indicator Layer on Top Configs

Best filter combos by coverage tier:

**n >= 20 (Balanced tier):**
| Config | Filters | Hit% | n | Δ vs baseline |
|---------|---------|------|----|---------------|
| LB=400, LR=0.20, VM=0.5, AND | vdRatio@70%+rsi14_delta@70% | 53.3% | 30 | +18.1pp |
| LB=400, LR=0.20, VM=0.5, AND | vdRatio@70%+rsi14_delta@75% | 53.3% | 30 | +18.1pp |
| LB=400, LR=0.20, VM=0.5, AND | vdRatio@80%+rsi14_delta@75% | 51.9% | 27 | +16.6pp |
| LB=400, LR=0.20, VM=1.0, AND | vdRatio@70%+rsi14_delta@75% | 51.9% | 27 | +17.2pp |
| LB=400, LR=0.20, VM=0.5, AND | vdRatio@75%+rsi14_delta@75% | 51.7% | 29 | +16.5pp |

**n >= 30 (Coverage tier):**
| Config | Filters | Hit% | n |
|--------|---------|------|---|
| LB=400, LR=0.20, VM=0.5, AND | dist_ema200@80%+rsi14_delta@70% | 36.2% | 58 |

**n >= 10 (Precision tier):**
| Config | Filters | Hit% | n |
|--------|---------|------|---|
| LB=400, LR=0.10, VM=0.5, AND | vdRatio@75%+rsi14_delta@70% | 72.7% | 11 |

## Key Findings

### Winning Logic
1. **AND mode** — pure exhaustion (no directional confirmation limb)
2. **High lookback (400)** — 200-bar extreme, more significant than 50-100 bar
3. **High lessRatio (0.10-0.20)** — tighter delta ratio = more balanced buy/sell = more climactic
4. **Low volMult (0.5)** — lower volume threshold = more signals, but AND mode filters to quality
5. **Filter: vdRatio** — signal only when delta ratio is TIGHT (70-80th pctl), meaning buy/sell nearly equal at the extreme
6. **Filter: rsi14_delta** — signal only when RSI has been FALLING (70th+ pctl), meaning momentum was weakening before the reversal

### What Didn't Work
- EMA cross flags: completely random (KS<0.05, p>0.99)
- Delta features alone: redundant with levels, no F1 improvement
- ML classifiers: massive overfit (train F1=1.0, CV F1=0.15-0.23)
- volRatio alone: no improvement over raw
- Combined level+delta: F1=0.393, BELOW level-only baseline 0.398

## Best Practical Configs

| Mode | BAMBAM Params | Filters | Hit% | n | /week |
|------|--------------|---------|------|---|-------|
| **Precision** | LB=400 LR=0.10 VM=0.5 AND | vdRatio@75%+rsi14_delta@70% | 72.7% | 11 | 0.8 |
| **Balanced** | LB=400 LR=0.20 VM=0.5 AND | vdRatio@70%+rsi14_delta@70% | 53.3% | 30 | 2.3 |
| **Coverage** | LB=400 LR=0.20 VM=0.5 AND | dist_ema200@80%+rsi14_delta@70% | 36.2% | 58 | 4.5 |
| **Raw** | LB=400 LR=0.20 VM=0.5 AND | none | 35.3% | 156 | 12.0 |

## Files
- `/root/work/trading/bambam-fatcat-project/swingcatcher_fast.py` — Phase 1 coarse grid (96 configs)
- `/root/work/trading/bambam-fatcat-project/swingcatcher_results.json` — Full results JSON
- `/root/work/trading/bambam-fatcat-project/build_swingcatcher.py` — KS test + single-feature optimization