# Swing Research Pipeline — Deliverable 1: Labels

Foundation for finding true reversal points across multiple timeframes
using ATR-based ZigZag pivot detection.

## What's in this deliverable

This is **deliverable 1 of N**. It does NOT train any models yet.
It loads data, computes labels, and lets you VALIDATE the labels
visually. Models come next, after you confirm the labels match
your intuition.

```
swing_research/
├── configs/
│   └── tf_5m.yaml             # 5-minute timeframe parameters
├── lib/
│   ├── data_loader.py         # Perp OHLC + BAMBAM signal loading
│   └── labeling.py            # ATR ZigZag + 3-condition reversal label
├── scripts/
│   └── 01_visualize_labels.py # Run this — produces interactive HTML
├── data/                      # Put your CSVs here (see below)
└── outputs/                   # Generated plots and labeled CSVs
```

## Setup

```bash
pip install pandas numpy pyyaml plotly
```

## Data you need

Place in `data/` (or update paths in `configs/tf_5m.yaml`):

1. **`perp_5m.csv`** — Binance perpetual OHLC 5m bars. Must have columns:
   `open_time_str` (YYYY-MM-DD HH:MM UTC), `open`, `high`, `low`,
   `close`, `volume`. This is what your existing pipeline already
   produces.

2. **`signals_5m.csv`** — TradingView Strategy Tester CSV export from
   the BAMBAM 24-Feature script (v2.2). Must have columns:
   `Type` ("Entry long" / "Entry short"), `Date and time`,
   `Price USDT`, `Signal` (the pipe-delimited 25-part string).

## Run it

```bash
cd swing_research/
python scripts/01_visualize_labels.py configs/tf_5m.yaml
```

Open `outputs/label_viz_5m.html` in a browser. Zoom in.

## What to look for in the visualization

The plot shows:
- **Candlesticks** = price
- **Red triangles down** = pivot highs (ZigZag-confirmed)
- **Green triangles up** = pivot lows
- **Gold circles** = LONG signals labeled as TRUE REVERSALS
- **Gold X's** = SHORT signals labeled as TRUE REVERSALS
- **Gray circles/X's** = signals NOT labeled as reversals

**Confirm these things:**
1. Pivots are at obvious swing highs/lows, not random points
2. Gold-colored signals are at points where the trend actually
   reversed for a meaningful period
3. Gray signals are at pullbacks, chop, or fakeouts (correctly
   filtered OUT)

**If labels look wrong**, the most common fixes are tuning
`configs/tf_5m.yaml`:

- Too few pivots? Lower `zigzag_atr_mult` (try 1.5 or 1.0)
- Too many tiny pivots? Raise `zigzag_atr_mult` (try 2.5 or 3.0)
- Too few "true reversals"? Lower `min_reversal_atr_mult` or
  `min_holding_bars`
- "True reversals" include obvious chop? Raise either of those

The script prints a summary including reversal rate. For "main
trend reversals" expect 5-15% of signals to qualify. Significantly
higher or lower suggests the threshold needs tuning.

## Next deliverables (after labels validated)

- **02_features.py** — Feature engineering, normalization, optional
  derived features beyond the 24 BAMBAM exports
- **03_splits.py** — Chronological train/val/test split
- **04_models.py** — LightGBM with proper CV, permutation tests
- **05_evaluate.py** — Honest test-set metrics, calibration,
  feature importance
- **06_multi_timeframe.py** — Run the whole pipeline across 5m, 15m,
  1h, 2h, 4h, daily and produce a comparison report

## Architecture note: adding OI / perp data later

When you add Open Interest, funding rate, long/short ratio, etc.,
they slot into `lib/data_loader.py` as additional loaders that
return DataFrames indexed by UTC timestamp. Features get computed
in `lib/features.py` from those frames. The labeling step doesn't
change — labels come from price action, regardless of what
features you feed the model. This separation is deliberate.
