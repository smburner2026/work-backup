# Swing Research Pipeline

Proper backtesting research architecture for trading strategy development — built after hitting F1 caps with manual threshold sweeps on FATCAT.

## Architecture (from Claude audit, May 2026)

```
swing_research/
├── configs/tf_{timeframe}.yaml     # Per-timeframe params (pivot %, horizon, ATR-mult)
├── lib/
│   ├── data_loader.py              # Load perp OHLC + BAMBAM signals, align by timestamp
│   ├── labeling.py                 # ATR-based ZigZag pivot labeling + triple-barrier
│   ├── features.py                 # Feature engineering, normalization (TODO)
│   ├── models.py                   # LightGBM wrappers, baselines (TODO)
│   └── eval.py                     # Holdout metrics, calibration, permutation tests (TODO)
├── scripts/
│   ├── 01_visualize_labels.py      # Plot labeled signals on price chart
│   └── 02_audit_pivots.py          # Diagnose why pivots were missed (proximity? excursion? hold?)
├── outputs/
│   ├── label_viz_{tf}_{ver}.html   # Interactive plotly label visualization
│   ├── pivot_audit_{tf}_{ver}.csv  # Audit table: every pivot, why it passed/failed
│   └── labeled_signals_{tf}.csv    # Signals with labels → LightGBM input
└── data/
    ├── perp_5m.csv                 # Symlink to merged Binance perp data
    └── signals_5m.csv              # Symlink to BAMBAM signal export
```

## Three Decisions Before Any Code

Claude identified these as the critical pre-architecture questions:

### 1. Reversal Definition
What counts as a swing high/low:
- **Mean-reversion swing**: Price moved direction A in last K bars, signal fires, want direction B for X% within N bars
- **Trend exhaustion**: Price made new local extreme (BAMBAM's `ph >= top`), want meaningful retrace from that extreme
- **Volatility expansion in opposing direction**: Signal fires, price moves >X ATR against recent trend within N bars

### 2. Metric to Optimize
- **Hit rate** (what v1 SwingCatcher used) — easy to game with tiny samples
- **Expectancy** = hit_rate × avg_win − miss_rate × avg_loss — much more useful
- **Sharpe** — accounts for variance
- **Best fit at specific stop/target combo** — realistic for actual trading

### 3. Trading Horizon
Label must match the actual trade plan. If holding 4h, label for 4h. If exiting on first 1% move or 30min (whichever first), label for that. Optimizing for a fiction wastes time.

## Labeling Methodology

### ATR-Based ZigZag Pivots (lib/labeling.py)

Instead of fixed % thresholds, use ATR-multiplier to auto-adjust to volatility:

```yaml
# configs/tf_5m_v3.yaml (current active config)
zigzag_atr_mult: 8.0      # Swing = 8× ATR reversal
pivot_proximity_bars: 24   # Signal must be within 24 bars of pivot
min_reversal_atr_mult: 7.0 # Counter-move must be ≥7× ATR
min_holding_bars: 24       # Counter-move must sustain ≥24 bars
```

### Triple-Barrier Labels (from Advances in Financial ML, López de Prado)

Instead of single `close[N]` snapshot, use path-dependent labeling:

```python
def triple_barrier_label(prices, idx, direction, tp_pct, sl_pct, horizon):
    """
    +1 if take-profit hit first
    -1 if stop-loss hit first
     0 if neither within horizon (timeout)
    """
```

This catches reversals where price spikes to target then reverses before end-of-window.

### Per-Timeframe YAML Configs

Each timeframe gets its own config because parameters scale differently:

| Parameter | 5m | 15m | 1h | 1d |
|---|---|---|---|---|
| Reversal magnitude | 1-3% | 2-5% | 3-8% | 5-15% |
| Holding period (bars) | 24-96 | 12-48 | 6-24 | 5-20 |
| Lookback for pivot confirmation | 12-48 bars | 10-30 bars | 5-15 bars | 3-10 bars |
| Signal frequency | hundreds/month | hundreds/month | 50-200/month | few/month |
| Sample size for ML training | thousands | thousands | hundreds | ~100 — NOT feasible |

The 5m timeframe is the proof of concept. Higher timeframes (4h+, daily) need 1-3 years of data before ML is viable.

## Data Split Methodology (Chronological)

Critical for time series — random splits leak future info into training:

```python
n = len(signals)
train_end = int(n * 0.60)
val_end   = int(n * 0.80)
# train: [0, train_end) — fit model
# val:   [train_end, val_end) — tune hyperparams
# test:  [val_end, n) — honest evaluation (ONCE)
```

If test results disappoint, do NOT go back and tune. That's the rule.

## Model Selection

For 24 features with nonlinear interactions on ~400-2000 training samples:

**Gradient boosted trees (LightGBM, XGBoost)** — correct tool:
- Handle feature interactions natively
- Robust to feature scale
- Feature importances tell you which indicators matter
- Probability outputs → set threshold post-hoc
- Built-in early stopping → prevent overfit
- 30-line script outperforms 200-line manual threshold grid

**Separate models per direction** — not a single model with `direction` feature. Long/short dynamics are asymmetric in crypto (downside differs from upside), and you have enough signals to train separate models.

## Sanity Checks (Built-In Requirements)

After any model training, run:

1. **Permutation test**: Shuffle labels and retrain. Real AUC must be >2σ above shuffled AUC. If not, model finds noise.
2. **Time-decay check**: Score on test data split into halves. If early-test AUC=0.65 and late-test AUC=0.51, edge is decaying (common in crypto).
3. **Calibration**: When model says "70% chance," is it right 70% of the time? Use `sklearn.calibration.calibration_curve`.

## Current State (May 23, 2026)

- **v3 labels active**: exc≥7ATR, hold≥24bar, prox≤24bar
- **90-day 431-signal test**: 127 True labels (29.5%)
- **1-year 1,850-signal export**: Ready for labeling + training
- **Next**: Claude visual review of v3 HTML, then LightGBM per direction

## Key Lessons from Previous Iterations

1. **Hit rate alone misleads** — 72.7% Precision mode produced only 11 signals in 90 days; 3 losers at 3:1 could flip expectancy negative.
2. **Close+48 label misses path** — If price spikes 2% at bar 30 then reverses by bar 48, close+48 says "miss" but TP would have printed 2%.
3. **Manual threshold grid doesn't scale** — Adding OI, funding rate, and taker ratio (the plan) makes pair/triple sweeps explode combinatorially. LightGBM scales trivially — just add columns.
4. **Separate long/short models** — Avoids fragile SHORT_HIGHER/SHORT_LOWER list errors (v1 SwingCatcher had 5 versions of this list across 3 scripts, not always consistent).
5. **Train/val/test chronological** — Without it, the "best" config is determined on data the model has already seen.
6. **Labeling must be visually validated** — 7,994 pivots at v1 (too many) vs 599 at v2 (correct range). Only the HTML plot catches tuning errors — numbers alone hide the problem.

## See Also

- `configs/tf_5m_v3.yaml` — Current active labeling config
- `scripts/01_visualize_labels.py` — Generate interactive label visualization
- `scripts/02_audit_pivots.py` — Diagnose why specific pivots were missed
- `lib/labeling.py` — ATR ZigZag implementation
- `lib/data_loader.py` — Perp + signal CSV loader (handles both `time_str` and `open_time_str`)
