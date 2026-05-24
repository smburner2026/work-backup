---
name: swingcatcher
description: >
  Optimized BAMBAM variant for swing high/low capture on crypto perps.
  Uses ATR-based ZigZag labeling + LightGBM models across multiple timeframes.
  Three deliverable tiers: labels (validate first), features + train/val/test,
  and evaluation with sanity checks. The old grid-search approach (build_swingcatcher.py)
  is archived below — the corrected pipeline lives in swing_research/.
category: trading
triggers:
  - swingcatcher
  - swing catcher
  - backtest bambam
  - optimize bambam params
  - pivot labeling
  - triple barrier label
  - zigzag labeling
  - true reversal label
---

# SwingCatcher — Corrected Pipeline (May 23 2026)

## ⚠️ CRITICAL WARNING

The original SwingCatcher results (72.7% Precision, 53.3% Balanced) are **overfit** and should NOT be trusted for deployment. The pipeline that produced them had:

- **No train/test split** — thresholds optimized and evaluated on the same 431 signals
- **Close+48 snapshot labels** — not path-dependent (misses spike-and-reverse scenarios)
- **Manual threshold grid** — doesn't scale to multi-feature expansions
- **Hit rate as sole metric** — ignores expectancy, Sharpe, and risk

The corrected approach is below. Do not deploy the old `.pine` scripts from the grid-search era.

---

## Corrected Pipeline (Claude Architecture, May 23 2026)

### Working Implementation

Located at `/root/work/trading/bambam-fatcat-project/swing_research/`:

```
swing_research/
├── configs/
│   └── tf_5m_v3.yaml          # Current best 5m config
├── lib/
│   ├── data_loader.py         # CSV → clean DataFrame with perp index
│   └── labeling.py            # ATR ZigZag pivots + 3-condition label
├── scripts/
│   ├── 01_visualize_labels.py # RUN FIRST — validate labels visually
│   └── 02_audit_pivots.py     # Diagnose WHY pivots missed labels
├── data/
│   ├── perp_5m.csv → symlink
│   └── signals_5m.csv → symlink
└── outputs/
    ├── label_viz_5m_v2.png
    ├── label_viz_5m_v3.png
    └── pivot_audit_5m.csv
```

### Run Sequence

```bash
# 1. Validate labels (DO NOT SKIP)
python scripts/01_visualize_labels.py configs/tf_5m.yaml

# 2. Audit why pivots were missed
python scripts/02_audit_pivots.py configs/tf_5m.yaml

# 3. Only after labels look right → chronological split + train models
```

### Labeling Methodology

**Define "true reversal" as a signal that satisfies ALL THREE conditions:**
1. **Proximity:** Signal fires within N bars of a confirmed pivot (structural high/low)
2. **Excursion:** Counter-move after the pivot is ≥ X × ATR (meaningful reversal magnitude)
3. **Sustained:** Counter-move lasts ≥ M consecutive bars (not a wick/fakeout)

**ZigZag pivot detection** (ATR-based, not %-based):
- Walks forward bar by bar
- Maintains a tentative extreme (highest high or lowest low)
- Confirms as a pivot when price reverses by ≥ N × ATR
- Returns alternating high/low pivots in chronological order
- Unconfirmed pivots at data edge are excluded

**ATR-based thresholds** (not fixed %):
- Self-tune to volatility regime. A 1.5% swing in low-vol environments is a real pivot; the same 1.5% in high-vol is noise.
- Fixed % thresholds break across regimes. Wilder's smoothing matches TV's `ta.atr()`.

### 5m Config Tuning (3 iterations)

| Parameter | v1 (initial) | v2 (retuned) | v3 (relaxed) |
|---|---|---|---|
| zigzag_atr_mult | 2.0 | **8.0** | 8.0 |
| pivot_proximity_bars | 6 | 12 | **24** |
| min_reversal_atr_mult | 3.0 | 12.0 | **7.0** |
| min_holding_bars | 24 | 48 | **24** |

- **v1:** 7,994 pivots, 60.6% reversal rate → way too loose (catching noise)
- **v2:** 599 pivots, 6.7% reversal rate → too tight (missed structural reversals like Mar 4, 17, 22)
- **v3:** 599 pivots, **29.5% reversal rate** (127/431 signals) — above the 5-15% target band, under review by user. Audit showed excursion failed (7%) and holding failed (2%) are now minor; 91% of misses are prox failures, mostly from pre-signal-window Oct-Feb pivots.

### Pivot Audit Findings (May 23 2026)

The `02_audit_pivots.py` diagnostic showed:

| Failure Mode | v2 Count | v3 Count |
|---|---|---|
| Signal too far from pivot | 471 (85%) | 430 (91%) |
| Signal exists, excursion failed | 72 (13%) | 32 (7%) |
| Signal exists, holding failed | 12 (2%) | 10 (2%) |

The apparent 85-91% "too far" figures are distorted by Oct 2025–Feb 20 pivots that predate the BAMBAM signal export (which starts Feb 21). Within the Feb 21–May 20 window, the picture is cleaner — most pivots have signals within reasonable distance, and the excursion/hold failures are the primary tuning levers.

**Key insight from audit:** The median missed-pivot excursion was 7.65 ATR (v2), meaning most near-miss pivots had real counter-moves that just fell short of the 12.0 threshold. This directly drove the v3 relaxation to 7.0 ATR (which captured 71→127 True signals).

### Planned Model Pipeline (not yet built)

```python
# Chronological split — random splits leak future info
n = len(signals)
train_end = int(n * 0.60)
val_end = int(n * 0.80)

# Separate models per direction (crypto has asymmetric up/down dynamics)
# LightGBM handles feature interactions natively — scales to OI/funding data

model = lgb.LGBMClassifier(
    n_estimators=200, learning_rate=0.05,
    max_depth=4, min_child_samples=20,
    reg_alpha=0.1, reg_lambda=0.1)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)],
          callbacks=[lgb.early_stopping(20)])

# Required sanity checks:
# 1. Permutation test (shuffle labels → real AUC > 2σ above shuffled)
# 2. Time-decay check (score halves of test — edge decay?)
# 3. Calibration (does 70% probability ≈ 70% actual?)
# 4. Test: one look at the end. If disappointing, don't retune.
```

---

## Historical Archive — Original Grid-Search Results (May 22 2026)

These results are from the `build_swingcatcher.py` / `swingcatcher_staged.py` scripts, which have the structural flaws noted above. Retained for reference only — **do NOT use for deployment decisions.**

### Original Pareto Frontier

| Tier | LB | LR | VM | Mode | vdRatio filter | rsi14_delta filter | Hit% | n/90d |
|---|---|---|---|---|---|---|---|---|
| Precision | 400 | 0.10 | 0.5 | AND | ≤0.074(S) / ≥0.074(L) | ≥26.07(S) / ≤26.07(L) | 72.7% | 11 |
| Balanced | 400 | 0.20 | 0.5 | AND | ≤0.136(S) / ≥0.136(L) | ≥24.90(S) / ≤24.90(L) | 53.3% | 30 |
| Coverage | 400 | 0.20 | 0.5 | AND | (none) | (none) | 35.3% | 156 |
| Default BAMBAM | 200 | 0.05 | 1.0 | OR | (none) | (none) | 27.0% | 434 |

### Original Optimization Steps

1. Sweep 480 BAMBAM parameter combos (8 lookbacks × 6 lessRatios × 5 volMults × 2 deltaModes)
2. Layer 14 indicator features at multiple percentile thresholds
3. Fine-tune best region with indicator pair sweeps

### Original Key Learnings

- AND mode dominates OR (2× better swing capture at equivalent signal counts)
- High lookback (LB=400) outperforms default (LB=200)
- Low volMult (VM=0.5) works well when combined with vdRatio check
- EMA cross flags are noise (KS<0.05, p>0.99)
- vdRatio is the strongest single discriminator; rsi14_delta captures momentum deceleration

### Original Pine Scripts

Location: `swingcatcher_precision.pine`, `swingcatcher_balanced.pine` in the project root.
Generated from v1 delta export data (volRatio_delta bug). Thresholds likely shift with v2.2 data.

---

### Data Sources (May 23 2026)

**Primary signal dataset:**
- `data/exports/bambam_delta_24feat_v22_1year.csv` — **1,850 signals** (957L/893S), May 2025–May 2026, v2.2 export, 7/7 audit clean. This is THE canonical signal CSV.
- `data/exports/bambam_delta_24feat_v22.csv` — 90-day subset (431 signals, Feb–May 2026), superseded.

**Binance Futures perp data (on VPS):**
- `data/binance_futures/BTCUSDT/merged_5m.csv` — **67,393 rows** (Oct 2025–May 2026), 20 columns incl. `basis_bps`. Pulled from VPS — **covers only ~7.5 months** of the 1-year signal range.
- Individual files: `klines_5m.csv`, `premium_index_5m.csv`, `funding_8h.csv` — all 67k rows.
- **Missing:** May–Sep 2025 (~5 months, ~44k rows). Also missing: OI/taker/top_trader data (5 individual files are header-only — Telegram upload truncation).
- **Full dataset (168k rows, May 2025–Jun 2026) lives on the user's local machine** — needs SCP transfer from `~/trading-scripts/BTCUSDT/`.

**Binance API limitations (discovered May 23):**
- `openInterestHist`, `takerlongshortRatio`, `topLongShortAccountRatio`, `topLongShortPositionRatio`, `globalLongShortAccountRatio` — **30-day max lookback at 5m interval**. Binance deletes older data.
- `klines`, `premiumIndexKlines`, `fundingRate` — full period, no lookback limit.
- `startTime` parameter format works for klines (ms int) but the non-klines endpoints reject dates outside their retention window. The script now falls back gracefully (`max_lookback_days=30`).
- Premium index: `basis_bps = close × 10,000` (perp vs index premium/discount).
- See `references/binance-api-patterns.md` for full endpoint reference.

**Data gap:** 1-year signals (May 2025–May 2026) vs VPS perp data (Oct 2025–May 2026). ~5 months of signals lack perp enrichment. Enrichment requires the full dataset from the user's machine.

**Pipeline scripts:**
- `binance_futures_data.py` — OHLCV + OI + taker ratio + top trader ratios + funding + premium index. Default: 12-month May 2025–May 2026 BTCUSDT. Run on LOCAL machine (VPS geo-blocked).
- `enrich_signals.py` — TV export + merged data → enriched CSV with swing labels.

### Pipeline scripts

- `binance_futures_data.py` — OHLCV + OI + taker ratio + top trader ratios + funding
- `enrich_signals.py` — TV export + merged data → enriched CSV
- `audit_pipeline.py` — 6-layer integrity check
- `build_swingcatcher.py` — Original (flawed) single-feature sweep
- `swingcatcher_staged.py` — Original (flawed) coarse→fine grid

### Delivery Preference

When sharing Pine Scripts for the user to export from TradingView:
1. Produce as `.txt` files in `scripts/` directory
2. Provide SCP download command in chat
3. Include inline comments explaining the export methodology, bug history, and data contract
4. Keep in-chat explanations concise — verbose narrations waste turns
5. The user exports scripts externally (SCP → local machine → paste into TV → export CSV → send back)

See `references/data-audit-methodology.md` for the 7-point audit procedure run on every received CSV.

---

## References

- `references/export-bug-chain-v1-to-v2.2.md` — Full bug history and data integrity findings (pending)
- `references/pivot-audit-tuning.md` — v1/v2/v3 label tuning history and diagnostic patterns
- `references/labeling-methodology.md` — ATR-based ZigZag + 3-condition triple-barrier labeling
- `references/data-audit-methodology.md` — 7-point field-level audit procedure for every received TV export CSV
- `references/binance-api-patterns.md` — Binance Futures API quirks: endpoint lookback limits, column naming, retry strategy, date defaults
- See also: `tv-feature-export` skill for the Pine export methodology and 7-point data integrity checks
