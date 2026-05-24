"""
lib/labeling.py
===============

The most important file in this project. If labels are wrong,
every downstream model is garbage. Read carefully and validate
visually before trusting any output.

WHAT THIS DOES:
1. Computes ATR-based ZigZag pivots from perp OHLC data.
   A "pivot" is a local high/low where price reversed by at
   least N * ATR before continuing. The ATR threshold means the
   algorithm self-tunes to volatility regime — quiet days have
   tighter pivots, volatile days have looser ones.

2. For each BAMBAM signal, decides if it qualifies as a
   "true reversal" by checking THREE conditions:
     a. Signal fires near a confirmed pivot (within N bars)
     b. Counter-move after the pivot is significant (≥ X ATR)
     c. Counter-move is sustained (lasts ≥ M bars)

WHY ATR-BASED:
- Fixed % thresholds break across regimes. A "1.5% swing" in
  Jan 2024 chop is a real pivot; the same 1.5% during a high-vol
  Aug 2024 day is just noise. ATR normalizes to current volatility.

WHY THE THREE-CONDITION LABEL:
- (a) alone catches any pivot, even tiny ones that flip back fast.
- (b) without (c) catches wicks/fakeouts.
- (c) without (b) catches slow grinds, not true reversals.
- All three together = "this was the main pivot before an
  extended counter-trend move", which is what the user asked for.

KEY METHODOLOGY NOTE — NO LOOKAHEAD LEAKAGE:
Labels are computed from FUTURE perp data (we need to see what
happened after the signal to know if it was a reversal). This
is fine for TRAINING labels, but at INFERENCE time you obviously
can't see the future. The model learns to predict labels from
the 24 features available AT signal time. Features and labels
must come from different time windows — features from bar[1]
backward, labels from bar+1 forward. The data_loader guarantees
this by using the BAMBAM signal's own snapshot features.
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Literal


# ============================================================
# ATR
# ============================================================

def compute_atr(perp_df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Standard Wilder's ATR. Returns a Series aligned to perp_df.index.

    Wilder's smoothing (not simple MA) matches what TradingView's
    ta.atr() produces, so the ATR values here will match the
    `atr14` feature in the BAMBAM signal export.
    """
    high = perp_df['high']
    low = perp_df['low']
    close_prev = perp_df['close'].shift(1)

    tr = pd.concat([
        high - low,
        (high - close_prev).abs(),
        (low - close_prev).abs(),
    ], axis=1).max(axis=1)

    # Wilder's smoothing = EMA with alpha = 1/period
    atr = tr.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    return atr


# ============================================================
# ZIGZAG PIVOT DETECTION
# ============================================================

@dataclass
class Pivot:
    """A confirmed swing high or swing low."""
    idx: int                          # position in perp_df
    timestamp: pd.Timestamp
    price: float
    kind: Literal['high', 'low']
    atr_at_pivot: float               # for diagnostic / threshold introspection


def compute_zigzag_pivots(
    perp_df: pd.DataFrame,
    atr: pd.Series,
    atr_mult: float = 2.0,
) -> list[Pivot]:
    """
    ATR-based ZigZag.

    Algorithm:
    - Walk forward bar by bar.
    - Maintain a "tentative extreme" — the most recent unconfirmed
      candidate high or low.
    - The tentative extreme is CONFIRMED as a pivot when price
      moves at least (atr_mult * ATR_at_tentative) in the opposite
      direction.
    - When confirmed, the tentative extreme becomes a Pivot, and
      we start looking for the next opposite-direction extreme.

    Returns: list of Pivot, in chronological order, alternating
             between 'high' and 'low'.

    NOTE: The most recent pivot in the list may be unconfirmed at
    the end of the data range (we ran out of bars before seeing
    a reversal). We INCLUDE it but flag it during labeling so it
    isn't used to label signals (we can't trust an unconfirmed
    pivot to actually have been the extreme).
    """
    pivots: list[Pivot] = []
    n = len(perp_df)

    high_arr = perp_df['high'].to_numpy()
    low_arr = perp_df['low'].to_numpy()
    times = perp_df.index
    atr_arr = atr.to_numpy()

    # Seed: first valid ATR bar. Direction starts as "unknown" —
    # we'll set it once we see the first qualifying move.
    start = int(np.argmax(~np.isnan(atr_arr)))
    if start >= n - 1:
        return []

    # Trend direction we're currently tracking:
    #   'up'   = looking for higher highs, will confirm a HIGH pivot
    #            when price drops by atr_mult * ATR from peak
    #   'down' = looking for lower lows, will confirm a LOW pivot
    #            when price rises by atr_mult * ATR from trough
    # Seed by comparing first two bars.
    if high_arr[start + 1] >= high_arr[start]:
        direction = 'up'
        ext_idx = start + 1 if high_arr[start + 1] > high_arr[start] else start
        ext_price = high_arr[ext_idx]
    else:
        direction = 'down'
        ext_idx = start + 1 if low_arr[start + 1] < low_arr[start] else start
        ext_price = low_arr[ext_idx]

    for i in range(start + 1, n):
        a = atr_arr[i]
        if np.isnan(a):
            continue
        threshold = atr_mult * a

        if direction == 'up':
            # Update tentative high if we made a new one
            if high_arr[i] > ext_price:
                ext_idx = i
                ext_price = high_arr[i]
            # Check if low_arr[i] has dropped enough from ext to confirm
            elif (ext_price - low_arr[i]) >= threshold:
                pivots.append(Pivot(
                    idx=ext_idx,
                    timestamp=times[ext_idx],
                    price=ext_price,
                    kind='high',
                    atr_at_pivot=atr_arr[ext_idx],
                ))
                # Flip: now tracking down. Start tentative low at current bar.
                direction = 'down'
                ext_idx = i
                ext_price = low_arr[i]
        else:  # direction == 'down'
            if low_arr[i] < ext_price:
                ext_idx = i
                ext_price = low_arr[i]
            elif (high_arr[i] - ext_price) >= threshold:
                pivots.append(Pivot(
                    idx=ext_idx,
                    timestamp=times[ext_idx],
                    price=ext_price,
                    kind='low',
                    atr_at_pivot=atr_arr[ext_idx],
                ))
                direction = 'up'
                ext_idx = i
                ext_price = high_arr[i]

    # NOTE: we deliberately DO NOT append the final unconfirmed
    # extreme. Signals near it can't be labeled reliably — we
    # don't know yet if it'll hold as a pivot.
    return pivots


# ============================================================
# LABELING
# ============================================================

def label_signals(
    signals_df: pd.DataFrame,
    perp_df: pd.DataFrame,
    pivots: list[Pivot],
    atr: pd.Series,
    *,
    pivot_proximity_bars: int,
    min_reversal_atr_mult: float,
    min_holding_bars: int,
    lookahead_bars: int,
) -> pd.DataFrame:
    """
    Label each signal as a "true reversal" or not.

    A LONG signal qualifies as a true reversal if:
      1. It fires within `pivot_proximity_bars` of a pivot LOW
      2. The price reaches at least
         (pivot_low + min_reversal_atr_mult * ATR_at_pivot)
         within `lookahead_bars`
      3. That upper level (or close to it) is sustained for
         at least `min_holding_bars` consecutive bars

    SHORT signals: mirror condition for pivot HIGH.

    Returns signals_df with NEW columns added:
        is_true_reversal       bool — the target label
        nearest_pivot_idx      int  — perp bar of closest matching pivot
        pivot_distance_bars    int  — |signal_idx - pivot_idx|
        forward_excursion_atr  float — how far price moved in favorable
                                       direction (in ATR units), for diagnostics
        forward_hold_bars      int  — how many bars the favorable move held
        labeling_skipped       bool — True if signal is too close to end
                                       of data or no valid pivot nearby

    The diagnostic columns are critical for VALIDATION — you
    should plot histograms of forward_excursion_atr and
    forward_hold_bars and confirm they look reasonable before
    trusting `is_true_reversal`.
    """
    n_bars = len(perp_df)
    close_arr = perp_df['close'].to_numpy()
    high_arr = perp_df['high'].to_numpy()
    low_arr = perp_df['low'].to_numpy()
    atr_arr = atr.to_numpy()

    # Split pivots by kind for fast nearest-neighbor lookup
    pivot_lows = [p for p in pivots if p.kind == 'low']
    pivot_highs = [p for p in pivots if p.kind == 'high']
    pivot_low_idxs = np.array([p.idx for p in pivot_lows]) if pivot_lows else np.array([])
    pivot_high_idxs = np.array([p.idx for p in pivot_highs]) if pivot_highs else np.array([])

    out = signals_df.copy()
    out['is_true_reversal'] = False
    out['nearest_pivot_idx'] = -1
    out['pivot_distance_bars'] = -1
    out['forward_excursion_atr'] = np.nan
    out['forward_hold_bars'] = 0
    out['labeling_skipped'] = False

    for sig_idx, row in out.iterrows():
        bar_idx = int(row['perp_idx'])
        direction = row['direction']

        # Skip if not enough lookahead bars remain
        if bar_idx + lookahead_bars >= n_bars:
            out.at[sig_idx, 'labeling_skipped'] = True
            continue

        # ---- Step 1: find nearest matching pivot ----
        if direction == 'long':
            candidate_idxs = pivot_low_idxs
            candidate_pivots = pivot_lows
        else:
            candidate_idxs = pivot_high_idxs
            candidate_pivots = pivot_highs

        if len(candidate_idxs) == 0:
            out.at[sig_idx, 'labeling_skipped'] = True
            continue

        # Find closest pivot by bar distance
        dists = np.abs(candidate_idxs - bar_idx)
        nearest_pos = int(np.argmin(dists))
        nearest_pivot = candidate_pivots[nearest_pos]
        distance = int(dists[nearest_pos])

        out.at[sig_idx, 'nearest_pivot_idx'] = nearest_pivot.idx
        out.at[sig_idx, 'pivot_distance_bars'] = distance

        if distance > pivot_proximity_bars:
            # Signal didn't fire near a pivot — condition (a) fails
            continue

        # ---- Step 2: check counter-move magnitude ----
        pivot_atr = nearest_pivot.atr_at_pivot
        if np.isnan(pivot_atr) or pivot_atr <= 0:
            out.at[sig_idx, 'labeling_skipped'] = True
            continue

        required_move = min_reversal_atr_mult * pivot_atr
        pivot_price = nearest_pivot.price

        # Look forward from the pivot bar (NOT the signal bar) for
        # the counter-move. Using pivot bar makes the label about
        # the pivot's quality, independent of when the signal fired
        # within the proximity window.
        fwd_start = nearest_pivot.idx + 1
        fwd_end = min(fwd_start + lookahead_bars, n_bars)
        if fwd_end - fwd_start < min_holding_bars:
            out.at[sig_idx, 'labeling_skipped'] = True
            continue

        fwd_high = high_arr[fwd_start:fwd_end]
        fwd_low = low_arr[fwd_start:fwd_end]
        fwd_close = close_arr[fwd_start:fwd_end]

        if direction == 'long':
            # Need price to rise by required_move
            target_price = pivot_price + required_move
            max_excursion = (fwd_high.max() - pivot_price) / pivot_atr
            hit_mask = fwd_close >= target_price
        else:
            target_price = pivot_price - required_move
            max_excursion = (pivot_price - fwd_low.min()) / pivot_atr
            hit_mask = fwd_close <= target_price

        out.at[sig_idx, 'forward_excursion_atr'] = max_excursion

        if not hit_mask.any():
            continue  # magnitude condition (b) fails

        # ---- Step 3: check sustained holding ----
        # We require the favorable side to remain dominant for
        # min_holding_bars CONSECUTIVE bars after first hitting target.
        first_hit = int(np.argmax(hit_mask))  # first True index
        # From first_hit forward, count consecutive bars that stay
        # on the favorable side of the pivot price.
        if direction == 'long':
            staying = fwd_close[first_hit:] >= pivot_price
        else:
            staying = fwd_close[first_hit:] <= pivot_price

        # Longest run of True from the start of `staying`
        if len(staying) == 0:
            continue
        run_len = 0
        for v in staying:
            if v:
                run_len += 1
            else:
                break
        out.at[sig_idx, 'forward_hold_bars'] = run_len

        if run_len >= min_holding_bars:
            out.at[sig_idx, 'is_true_reversal'] = True

    return out


def labeling_summary(labeled: pd.DataFrame) -> dict:
    """
    Quick stats for sanity-checking a labeling run.

    Print this immediately after labeling. The numbers below are
    the ones to look at HARD before training any model:

    - total / valid / skipped: how many signals you have to work with
    - reversal_rate: fraction of valid signals labeled True.
        If this is >25%, your label is probably too loose
          (catching pullbacks, not true reversals).
        If it's <2%, your label is probably too tight
          (won't have enough positive examples to train on).
        For "main trend reversals" expect 5-15% baseline.
    - by direction: should be roughly balanced; large skew suggests
      either market regime imbalance in your data window or a
      bug in the directional logic.
    - excursion_atr stats: how far did winning reversals go?
      Median should be meaningfully > min_reversal_atr_mult,
      otherwise you're on the edge of the threshold and small
      data changes will flip labels.
    """
    total = len(labeled)
    skipped = labeled['labeling_skipped'].sum()
    valid = total - skipped
    reversals = labeled['is_true_reversal'].sum()

    by_dir = labeled.groupby('direction').agg(
        n_total=('is_true_reversal', 'size'),
        n_reversals=('is_true_reversal', 'sum'),
    )
    by_dir['rate'] = by_dir['n_reversals'] / by_dir['n_total']

    winners = labeled[labeled['is_true_reversal']]
    return {
        'total_signals': int(total),
        'valid_signals': int(valid),
        'skipped_signals': int(skipped),
        'true_reversals': int(reversals),
        'reversal_rate': float(reversals / valid) if valid else 0.0,
        'by_direction': by_dir.to_dict(),
        'winner_excursion_atr_median': float(winners['forward_excursion_atr'].median())
            if len(winners) else float('nan'),
        'winner_hold_bars_median': float(winners['forward_hold_bars'].median())
            if len(winners) else float('nan'),
    }
