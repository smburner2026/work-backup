# Pine Script Signal Selectivity Patterns

Condensed recipe book for making Pine Script indicators more or less selective. Each pattern includes the before/after code, the expected signal reduction, and when to use it.

## 1. Tighten Ratio Threshold

**Use when:** The indicator has a ratio-based exhaustion filter (delta ratio, RSI threshold, etc.).

**Before:**
```pinescript
lessRatio = input.float(0.05, 'Less Ratio', minval=0.001, maxval=0.1)
isLessRatio = vdRatio < lessRatio
```

**After:**
```pinescript
lessRatio = input.float(0.02, 'Less Ratio', minval=0.001, maxval=0.1)
isLessRatio = vdRatio < lessRatio
```

**Effect:** ~30-50% signal reduction. Every bar with ratio between old and new threshold disappears.

**Caveat:** On LTF (1m, 5m, 15m), ratio variance is higher — a 0.02 threshold may be too tight and miss valid signals. Test on target timeframe.

---

## 2. Volume Spike Multiplier

**Use when:** The indicator gates signals with "volume above average" or similar.

**Before:**
```pinescript
highVol = vol > avgVol
```

**After:**
```pinescript
highVol = vol > avgVol * 1.5   // or 2.0
```

**Effect:** ~30-60% signal reduction. On LTF where volume variance is high, this is often the single most effective filter.

**Caveat:** On daily/weekly timeframes where volume is more stable, 1.5× may be too aggressive.

---

## 3. Exhaustion-Only (Remove Directional Confirmation)

**Use when:** The indicator has dual-path signals — one for exhaustion (near-tie) and one for directional confirmation (strong imbalance). You want ONLY the exhaustion signals.

**Before:**
```pinescript
bearSignal = ph >= top and highVol and (isLessRatio or vd < 0)
bullSignal = pl <= btm and highVol and (isLessRatio or vd > 0)
```

**After:**
```pinescript
bearSignal = ph >= top and highVol and isLessRatio
bullSignal = pl <= btm and highVol and isLessRatio
```

**Effect:** ~60-70% signal reduction. Removes all trend-confirmation signals, keeping only pure climax bars.

**Caveat:** You'll miss some valid reversals that happen on strong directional volume but still reverse. Best for contrarian/Martingale-style strategies that specifically want exhaustion.

**When it fits a strategy:** The user's bounded Martingale on BTC specifically wants to add on dips AFTER the selling climax has exhausted — not while selling is still accelerating. The exhaustion-only pattern is the natural filter for this.

---

## 4. Band Confluence Gate

**Use when:** The indicator already plots VWAP, Bollinger, or other statistical bands. Require the signal to occur outside a band.

**Before:**
```pinescript
bearSignal = ph >= top and highVol and isLessRatio
```

**After:**
```pinescript
priceExtreme = close > thresholdUp2   // outside 2σ upper band
bearSignal = ph >= top and highVol and isLessRatio and priceExtreme
```

**Effect:** ~40-50% signal reduction. Only signals at statistical extremes pass.

**Caveat:** Adds a new dependency — the signal now depends on both the original logic AND the band calculation. If bands are noisy on LTF, this can be unstable.

---

## 5. ATR-Based Minimum Move

**Use when:** The indicator fires on every touch of an N-bar extreme, including shallow bounces.

**Before:**
```pinescript
bearSignal = ph >= top and highVol and isLessRatio
```

**After:**
```pinescript
minMove = ta.atr(14) * 1.0   // require 1 ATR of movement from lookback low
rangeMove = (ph - btm) / btm * 100
significantMove = rangeMove > minMove
bearSignal = ph >= top and highVol and isLessRatio and significantMove
```

**Effect:** ~20-40% signal reduction. Filters out shallow touches.

**Caveat:** Adds complexity and a new parameter. Less elegant than tightening existing knobs.

---

## Combining Patterns

The standard progression for making an LTF indicator more selective:

1. **Start with volume multiplier** (1.5× or 2.0×) — biggest single impact
2. **Tighten ratio threshold** (0.05 → 0.03 → 0.02) — fine-tune the exhaustion filter
3. **If still too noisy:** Remove directional confirmation limb → exhaustion-only
4. **If still too noisy:** Add band confluence gate or ATR minimum move

Each step preserves the original logic while adding a new filter layer. The user's Ferocious Fatcat variant required steps 1 + 2 + 3 combined.

---

## Reverse-Engineering Workflow

When the original source is known but the modified source is hidden:

1. Read the original code carefully — identify every parameter and boolean condition
2. Determine which changes are symmetrical (affect both bull and bear equally) vs directional
3. Create ranked hypotheses from the patterns above
4. Ship each as a standalone `.pine` file with clear parameter defaults
5. User tests on TradingView against the hidden indicator
6. Collect binary feedback and iterate

Typical convergence: 2-3 iterations. The key signal is "still not as selective" — tells you the current hypothesis isn't aggressive enough, so move to the next pattern in the progression above.

---

## Reference

- Original BAMBAM: `/root/work/trading/pinescript/bambam-vwap-bands.pine`
- Hypothesis v1 (tighter knobs): `/tmp/bambam_fatcat_hypothesis.pine` (0.03 + 1.5×)
- Hypothesis v2 (exhaustion-only): `/tmp/bambam_fatcat_v2.pine` (0.02 + 2.0× + no directional limb)
