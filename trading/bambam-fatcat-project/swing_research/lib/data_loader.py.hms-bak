"""
lib/data_loader.py
==================

Load and align two data sources:
  1. Perpetual OHLC bars (Binance 5m, 15m, 1h, etc.)
  2. BAMBAM signal export (from TradingView Strategy Tester CSV)

Both end up as pandas DataFrames indexed by UTC timestamp, so
downstream code (labeling, features, training) doesn't have to
care where the data came from.

KEY DESIGN CHOICES:
- Everything is UTC. Mixing timezones is a top-3 source of
  silent bugs in trading systems.
- Signals get joined to the perp bar they fired on, so every
  signal has a known bar-index in the perp series. Without
  this index, lookahead labeling can't work.
- We return both `signals_df` AND `perp_df` rather than a
  merged frame, because the labeling step needs to walk forward
  through perp bars from each signal's index. Keeping them
  separate makes that loop cheap.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_perp_ohlc(csv_path: str) -> pd.DataFrame:
    """
    Load Binance perp OHLC CSV.

    Expects columns: open_time_str, open, high, low, close, volume
    (the format your Hermes pipeline already produces).

    Returns DataFrame indexed by UTC timestamp with columns:
        open, high, low, close, volume

    The index is sorted ascending and de-duplicated. Duplicate
    timestamps in perp data usually mean a re-download glitch
    rather than legitimate data, so we keep the LAST one (most
    recent write wins).
    """
    df = pd.read_csv(csv_path)

    # Strip BOM if present (Windows CSV exports add it)
    df.columns = [c.lstrip('\ufeff') for c in df.columns]

    # Parse timestamp. Binance exports use 'YYYY-MM-DD HH:MM' UTC.
    # Handle both naming conventions: 'open_time_str' (raw Binance export)
    # and 'time_str' (merged file from binance_futures_data.py).
    ts_col = 'open_time_str' if 'open_time_str' in df.columns else 'time_str'
    df['dt'] = pd.to_datetime(df[ts_col], utc=True, format='%Y-%m-%d %H:%M')

    # Cast price/volume columns to float. Defensive — sometimes
    # these come in as strings if the CSV has quoting weirdness.
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop any row where price parsing failed
    n_before = len(df)
    df = df.dropna(subset=['open', 'high', 'low', 'close'])
    if len(df) < n_before:
        print(f"  [load_perp_ohlc] Dropped {n_before - len(df)} rows with bad price data")

    df = df.set_index('dt').sort_index()
    df = df[~df.index.duplicated(keep='last')]

    return df[['open', 'high', 'low', 'close', 'volume']]


# Feature order MUST match the Pine script's output exactly.
# Position 0 = direction (BULL/BEAR), positions 1-24 = features.
# Source of truth: 04_bambam_24feat_delta_export_v2.2.txt
BAMBAM_FEATURES = [
    'vol', 'vd', 'avgVol', 'volRatio', 'vdRatio', 'vb', 'vs',
    'rsi14', 'rsi7', 'dist_ema21', 'dist_ema50', 'dist_ema200',
    'macd_hist', 'atr14',
    'rsi14_delta', 'rsi7_delta', 'macd_hist_delta', 'price_mom5',
    'volRatio_delta', 'vdRatio_delta',
    'ema21_bear', 'ema21_bull', 'ema50_bear', 'ema50_bull',
]


def load_bambam_signals(csv_path: str, perp_df: pd.DataFrame) -> pd.DataFrame:
    """
    Load BAMBAM signal CSV from TradingView Strategy Tester export.
    Parses the pipe-delimited 'Signal' column into 24 feature columns.

    Joins each signal to its corresponding perp bar by timestamp,
    adding a 'perp_idx' column = position in perp_df. This index
    is what the labeling code uses to walk forward in price.

    Returns DataFrame indexed by UTC timestamp with columns:
        direction       'long' or 'short'
        entry_price     float, from the CSV (matches perp close)
        perp_idx        int, position of this signal in perp_df
        <24 feature cols, see BAMBAM_FEATURES above>

    DROPS signals that:
      - Aren't 'Entry' type (closes, etc.)
      - Have malformed Signal column (not 25 pipe-parts)
      - Fall outside the perp_df date range (can't be labeled)
    """
    df = pd.read_csv(csv_path)
    df.columns = [c.lstrip('\ufeff') for c in df.columns]

    # TradingView exports include Entry AND Exit rows. We only
    # want Entry. The 'Type' column contains strings like
    # "Entry long" / "Entry short" / "Exit long".
    df = df[df['Type'].str.contains('Entry', na=False)].copy()

    # Deduplicate: same timestamp + same price = same signal
    # fired twice (TradingView quirk on certain bar boundaries).
    # Direction is part of the dedup key so we don't accidentally
    # collapse a simultaneous long + short.
    df['_dedup'] = (
        df['Date and time'].astype(str) + '|' +
        df['Price USDT'].astype(str) + '|' +
        df['Signal'].str[:4]  # 'BULL' or 'BEAR' prefix
    )
    n_before = len(df)
    df = df.drop_duplicates('_dedup', keep='first')
    if len(df) < n_before:
        print(f"  [load_bambam] Dropped {n_before - len(df)} duplicate signals")

    # Parse the pipe-delimited feature string.
    # Format: BULL|f1|f2|...|f24  →  25 parts total.
    parts_split = df['Signal'].str.split('|')
    valid_mask = parts_split.str.len() == 25

    n_bad = (~valid_mask).sum()
    if n_bad > 0:
        print(f"  [load_bambam] Dropped {n_bad} signals with malformed Signal column "
              f"(expected 25 pipe-parts, got something else)")
    df = df[valid_mask].copy()
    parts_split = parts_split[valid_mask]

    # Direction from first part
    df['direction'] = parts_split.str[0].map(
        lambda s: 'long' if s.startswith('BULL') else 'short'
    )

    # Extract 24 features. We iterate so we can validate float
    # parsing rather than silently coercing NaN.
    for i, fname in enumerate(BAMBAM_FEATURES):
        df[fname] = pd.to_numeric(parts_split.str[i + 1], errors='coerce')

    # Any signal with NaN features after parsing is corrupted
    # (the v2 bug you already hunted down). Drop them but warn.
    feat_na = df[BAMBAM_FEATURES].isna().any(axis=1)
    if feat_na.sum() > 0:
        print(f"  [load_bambam] Dropped {feat_na.sum()} signals with NaN in features "
              f"(likely v2-era Pine bug — should be 0 with v2.2 export)")
    df = df[~feat_na].copy()

    # Entry price → float
    df['entry_price'] = pd.to_numeric(df['Price USDT'], errors='coerce')

    # Parse timestamp, set as index
    df['dt'] = pd.to_datetime(df['Date and time'], utc=True, format='%Y-%m-%d %H:%M')
    df = df.set_index('dt').sort_index()

    # Join to perp bars: every signal must map to a perp_idx.
    # We use get_indexer with method='nearest' but enforce that
    # the match is within 1 bar — otherwise the signal is from
    # a perp series we don't have data for.
    perp_idx = perp_df.index.get_indexer(df.index, method='nearest')
    df['perp_idx'] = perp_idx

    # Verify the match is exact (timestamp must equal perp bar time).
    # On 5m bars, a signal at 13:50 must match perp bar 13:50, not 13:45.
    matched_times = perp_df.index[perp_idx]
    time_diff_sec = np.abs((df.index - matched_times).total_seconds())
    bad_match = time_diff_sec > 60  # >1 minute = wrong bar
    if bad_match.sum() > 0:
        print(f"  [load_bambam] Dropped {bad_match.sum()} signals that don't align "
              f"to a perp bar (likely outside perp_df date range)")
    df = df[~bad_match].copy()

    # Final column set — clean output
    out_cols = ['direction', 'entry_price', 'perp_idx'] + BAMBAM_FEATURES
    return df[out_cols]


def load_all(config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convenience: load both perp and signals from a config dict.
    Returns (perp_df, signals_df).
    """
    perp = load_perp_ohlc(config['perp_csv'])
    print(f"  Loaded {len(perp):,} perp bars: "
          f"{perp.index.min()} → {perp.index.max()}")

    sigs = load_bambam_signals(config['signals_csv'], perp)
    print(f"  Loaded {len(sigs):,} clean signals "
          f"({(sigs['direction'] == 'long').sum()} long, "
          f"{(sigs['direction'] == 'short').sum()} short)")

    return perp, sigs
