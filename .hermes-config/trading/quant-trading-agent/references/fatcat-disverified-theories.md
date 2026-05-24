# FATCAT: Disproven Hypotheses Audit

Record of every theory we tested and why it failed. Prevents future agents from retreading dead ends.

## 1. Volume Source Swap (taker_buy_base → estimate)

**Claim:** FATCAT uses `vb = taker_buy_base` (real Binance order-flow volume) instead of BAMBAM's `vb = volume × (close-low)/(high-low)` (candle-body estimate).

**Why it seemed plausible:**
- Signal density matched (~19 taker_buy signals vs ~18 FATCAT entries on 30-day sample)
- 94% recall (17/18 FATCAT entries had a nearby BAMBAM signal)
- The estimate systematically overestimates buy volume at swing lows

**Why it's DISPROVEN:**
1. **`takerbuyvol` compile error (CE10272):** The built-in doesn't exist on the user's broker. FATCAT would face the same error.
2. **POCKETBAMBAM matches FATCAT 6/6 using estimated volume:** Same timestamps, same prices. If FATCAT used a different volume source, POCKETBAMBAM wouldn't match.
3. **Timestamp-level test: 0/6 exact bar match** against FATCAT CSV entries with taker_buy model.

**Verdict:** Dead. The density match was coincidental.

## 2. Parameter-Only Tuning (lessRatio + volMult)

**Claim:** FATCAT is BAMBAM with `lessRatio=0.03` and `volMult=1.5` (vs 0.05 and 1.0).

**Why it seemed plausible:** Symmetrical signal reduction, both sides equally. No structural change needed.

**Why it's DISPROVEN:**
- Tested on 10,848 bars Binance data: tightening lessRatio from 0.05→0.03 barely changed signal count with estimated volume (50→49 signals)
- Raising volMult to 1.5 on estimated volume only reduced from 50→42 signals (-16%)
- FATCAT needs >90% reduction from POCKETBAMBAM signal rate

**Verdict:** Insufficient. Parameters alone can't account for the gap.

## 3. Single Fixed Cooldown

**Claim:** FATCAT = BAMBAM + N-hour cooldown gate between entries.

**Evidence for:** FATCAT year data shows minimum 35h gap between entries. POCKETBAMBAM clusters fire every 15-30 minutes within clusters — a cooldown would naturally suppress them.

**Evidence against:** FATCAT v2 period has entries with ~22h gaps. A fixed 35h gate would miss those. A fixed 22h gate would still let through more entries than FATCAT shows (the v2 period has many BAMBAM signals within 22h windows).

**Verdict:** Likely part of the answer but not the complete filter. Cooldown + additional gating (price delta, delta quality) needed.

## 4. AND Delta Mode

**Claim:** FATCAT requires BOTH `isLessRatio AND vd > 0` instead of BAMBAM's `isLessRatio OR vd > 0`.

**Evidence for:** AND mode cuts ~96% of signals on estimate data (50→2 signals on 30-day sample). This is closer to the observed 92% reduction.

**Evidence against:** Not tested on-chart against FATCAT yet. The 2 signals in 30 days is lower than FATCAT's 6 in 22 days, so AND alone may be too aggressive.

**Verdict:** Strong candidate, likely combined with cooldown for the full filter.

## What We Actually Know (Confirmed)

1. **BAMBAM (OG) fires correct signals on chart** — user confirmed
2. **POCKETBAMBAM = BAMBAM + 1-bar delay** — user confirmed on chart
3. **FATCAT = BAMBAM subset** — 72/72 overlap at raw signal level within ±10min (rectangle is square)
4. **FATCAT uses same volume source as BAMBAM** — `takerbuyvol` error proves this
5. **FATCAT filter is NOT pure parameter tuning** — parameters alone give insufficient reduction
6. **FATCAT filter is NOT timestamp-based** — best cooldown-only F1 = 0.393
7. **FATCAT filter is NOT recoverable from candle-body volume features** — F1 wall at ~0.38-0.39 across ALL approaches (thresholds, ML, KS-validated features). The features overlap too much for any classifier to separate. taker buy volume or a stateful mechanism is the likely missing data source.
8. **Year data shows 29 entries over 11.5 months** — ~2.5/month average
9. **The filter reduces 434 raw BAMBAM signals to 72 FATCAT entries** — 83.4% rejection rate, asymmetric (90.3% short, 74.2% long)

## 5. Machine Learning Classification (Decision Tree, RF, GB)

**Claim:** A machine learning model trained on BAMBAM signal features could learn the FATCAT selection boundary.

**Tested:** Decision tree (depth 2-6), Random Forest (200 trees, 18 features including derived features like vb/vs ratio, signal density, time since last), Gradient Boosting (100-200 estimators).

**Results:**
- Decision tree depth=2: CV F1=0.36, degrades with depth
- Random Forest: CV F1=0.15, train F1=1.0 (massive overfitting)
- Gradient Boosting: CV F1=0.18, train F1=1.0 (same pattern)
- KS test: vb most significant (0.418, p<0.001) but distributions overlap massively

**Why it failed:** The candle-body volume features are the same ones BAMBAM already uses internally. FATCAT's filter operates on data NOT represented in these features — most likely actual taker buy/sell volume from perps order flow, which has fundamentally different distribution characteristics from the (close-low)/(high-low) estimate.

**Verdict:** Dead. ML cannot learn a boundary that doesn't exist in the feature space. The F1=0.38 wall is the absolute ceiling for candle-body-derived features regardless of model complexity.

## 6. Feature Threshold Sweep on Real Perp Data

**Claim:** With actual perp volume features from TradingView, parameter sweeps on volRatio and vdRatio would crack the filter.

**Tested:** BAMBAM feature export strategy on 5m BTCUSDT.P (90 days). Each signal carries vol|vd|avgVol|volRatio|vdRatio|vb|vs in the comment string. Swept:
- volRatio min: 1.0-5.0
- vdRatio max: 0.05-1.0
- delta mode: OR vs AND
- cooldown: 0-15h (same-dir)

**Results:** Best F1=0.378 (volRatio ≥ 3.5, no cooldown). No combination exceeds the timestamp-only wall of 0.393. The features are computable from the same candle-body estimates BAMBAM uses — they ARE BAMBAM's features, just evaluated at different parameter thresholds.

**Verdict:** Dead. The filter does not operate as a simple threshold on BAMBAM's existing features. A fundamentally different data source or stateful mechanism is required.
