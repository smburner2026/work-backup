"""
scripts/02_audit_pivots.py
==========================

Diagnostic: for each pivot, find the nearest BAMBAM signal and
report whether it qualified as a true reversal. Especially useful
for understanding WHY a major pivot didn't get a "True" label.

Output: a ranked table of pivots sorted by "missed magnitude" —
i.e., the biggest counter-moves that didn't get a True label,
with the reason they failed.

USAGE:
    python scripts/02_audit_pivots.py configs/tf_5m.yaml

WHAT TO LOOK FOR:
    - If big-magnitude pivots show "no signal within N bars" →
      BAMBAM didn't fire near them. Fix is at the signal-generation
      level, not the labeling level.
    - If big pivots show "signal exists but proximity_bars exceeded" →
      loosen pivot_proximity_bars
    - If big pivots show "excursion ok, holding failed" →
      loosen min_holding_bars
    - If big pivots show "excursion failed" →
      the move post-pivot didn't meet the ATR threshold (this is
      unusual for a big pivot, but possible if the move took a
      long time to develop)
"""

import sys
import yaml
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.data_loader import load_all
from lib.labeling import compute_atr, compute_zigzag_pivots, label_signals


def measure_pivot_magnitude(pivot, perp_df, atr, lookahead_bars):
    """
    How big was the counter-move after this pivot?
    Returns: (counter_move_atr_mult, counter_move_pct)
    """
    n = len(perp_df)
    if pivot.idx + lookahead_bars >= n:
        return np.nan, np.nan

    fwd_start = pivot.idx + 1
    fwd_end = min(fwd_start + lookahead_bars, n)
    fwd_high = perp_df['high'].iloc[fwd_start:fwd_end].max()
    fwd_low = perp_df['low'].iloc[fwd_start:fwd_end].min()

    if pivot.kind == 'low':
        move = fwd_high - pivot.price
    else:
        move = pivot.price - fwd_low

    atr_mult = move / pivot.atr_at_pivot if pivot.atr_at_pivot > 0 else np.nan
    pct = move / pivot.price * 100
    return atr_mult, pct


def main(config_path):
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    perp, sigs = load_all(cfg)
    atr = compute_atr(perp, period=cfg['atr_period'])
    pivots = compute_zigzag_pivots(perp, atr, atr_mult=cfg['zigzag_atr_mult'])

    print(f"\n{'=' * 90}")
    print(f"PIVOT AUDIT — {cfg['timeframe']}")
    print(f"{'=' * 90}")
    print(f"Loaded {len(perp):,} bars, {len(sigs):,} signals, {len(pivots):,} pivots\n")

    # Label signals (we need this to know which signals were True/False)
    labeled = label_signals(
        sigs, perp, pivots, atr,
        pivot_proximity_bars=cfg['pivot_proximity_bars'],
        min_reversal_atr_mult=cfg['min_reversal_atr_mult'],
        min_holding_bars=cfg['min_holding_bars'],
        lookahead_bars=cfg['lookahead_bars'],
    )

    # Index signals by their perp_idx for fast lookup
    sig_idx_arr = labeled['perp_idx'].to_numpy()
    sig_dir_arr = labeled['direction'].to_numpy()
    sig_label_arr = labeled['is_true_reversal'].to_numpy()
    sig_hold_arr = labeled['forward_hold_bars'].to_numpy()
    sig_exc_arr = labeled['forward_excursion_atr'].to_numpy()
    sig_dist_arr = labeled['pivot_distance_bars'].to_numpy()

    # Build pivot audit table
    rows = []
    for p in pivots:
        atr_mult, pct = measure_pivot_magnitude(p, perp, atr, cfg['lookahead_bars'])

        # Find nearest signal of MATCHING direction
        # (long signals only match low pivots; short signals only match high pivots)
        wanted_dir = 'long' if p.kind == 'low' else 'short'
        dir_mask = sig_dir_arr == wanted_dir
        if not dir_mask.any():
            rows.append({
                'pivot_time': p.timestamp,
                'kind': p.kind,
                'price': p.price,
                'counter_move_atr': atr_mult,
                'counter_move_pct': pct,
                'nearest_sig_bars': None,
                'nearest_sig_labeled': None,
                'reason': 'no signals of matching direction',
            })
            continue

        sig_dists = np.abs(sig_idx_arr[dir_mask] - p.idx)
        nearest_pos = int(np.argmin(sig_dists))
        nearest_dist = int(sig_dists[nearest_pos])

        # Pull the original index in the labeled frame
        orig_indices = np.where(dir_mask)[0]
        sig_orig_idx = orig_indices[nearest_pos]

        labeled_true = bool(sig_label_arr[sig_orig_idx])
        exc = float(sig_exc_arr[sig_orig_idx]) if not np.isnan(sig_exc_arr[sig_orig_idx]) else None
        hold = int(sig_hold_arr[sig_orig_idx])
        sig_dist_from_its_pivot = int(sig_dist_arr[sig_orig_idx])

        # Diagnose why not labeled True (if applicable)
        if labeled_true:
            reason = '✓ labeled True'
        elif nearest_dist > cfg['pivot_proximity_bars']:
            reason = f'nearest sig is {nearest_dist} bars from pivot (max {cfg["pivot_proximity_bars"]})'
        elif exc is None:
            reason = 'signal had no excursion measurement (data edge?)'
        elif exc < cfg['min_reversal_atr_mult']:
            reason = f'excursion {exc:.1f} ATR < threshold {cfg["min_reversal_atr_mult"]}'
        elif hold < cfg['min_holding_bars']:
            reason = f'hold {hold} bars < threshold {cfg["min_holding_bars"]}'
        else:
            reason = 'unknown (check labeling code)'

        rows.append({
            'pivot_time': p.timestamp,
            'kind': p.kind,
            'price': p.price,
            'counter_move_atr': atr_mult,
            'counter_move_pct': pct,
            'nearest_sig_bars': nearest_dist,
            'nearest_sig_labeled': labeled_true,
            'reason': reason,
        })

    audit = pd.DataFrame(rows)
    # Drop pivots near end of data with no measurable counter-move
    audit = audit.dropna(subset=['counter_move_atr'])

    # ---- TOP MISSED PIVOTS: biggest counter-moves NOT labeled True ----
    missed = audit[(audit['nearest_sig_labeled'] != True)].copy()
    missed = missed.sort_values('counter_move_pct', ascending=False)

    print("─" * 90)
    print("TOP 30 MISSED PIVOTS — biggest counter-moves NOT captured by a 'True' label")
    print("─" * 90)
    print(f"{'time':<19} {'kind':<5} {'price':>10} {'cmove%':>8} {'cmoveATR':>9} "
          f"{'sigBars':>8} {'reason'}")
    for _, r in missed.head(30).iterrows():
        nearest = '—' if r['nearest_sig_bars'] is None else f"{r['nearest_sig_bars']}"
        print(f"{str(r['pivot_time']):<19} {r['kind']:<5} {r['price']:>10,.0f} "
              f"{r['counter_move_pct']:>7.2f}% {r['counter_move_atr']:>8.1f} "
              f"{nearest:>8} {r['reason']}")

    # ---- DIAGNOSTIC SUMMARY ----
    print()
    print("─" * 90)
    print("WHY PIVOTS WEREN'T LABELED — summary across all missed pivots")
    print("─" * 90)
    miss_reasons = missed['reason'].value_counts()
    # Group the parameterized reasons into buckets
    buckets = {
        'BAMBAM signal too far from pivot': 0,
        'signal exists, excursion failed': 0,
        'signal exists, holding failed': 0,
        'no matching-direction signal': 0,
        'other': 0,
    }
    for reason, count in miss_reasons.items():
        if 'no signals' in reason:
            buckets['no matching-direction signal'] += count
        elif 'bars from pivot' in reason:
            buckets['BAMBAM signal too far from pivot'] += count
        elif 'excursion' in reason:
            buckets['signal exists, excursion failed'] += count
        elif 'hold' in reason:
            buckets['signal exists, holding failed'] += count
        else:
            buckets['other'] += count

    total_missed = sum(buckets.values())
    if total_missed == 0:
        print("  No missed pivots — every pivot got a True label!")
    else:
        for k, v in buckets.items():
            if v > 0:
                pct = v / total_missed * 100
                print(f"  {k:<45} {v:>4}  ({pct:.0f}%)")

    # ---- INTERPRETATION HINTS ----
    print()
    print("─" * 90)
    print("INTERPRETATION")
    print("─" * 90)

    far_pct = buckets['BAMBAM signal too far from pivot'] / max(total_missed, 1) * 100
    nosig_pct = buckets['no matching-direction signal'] / max(total_missed, 1) * 100
    structural_pct = far_pct + nosig_pct

    if structural_pct > 60:
        print(f"  {structural_pct:.0f}% of missed pivots have NO BAMBAM signal close enough.")
        print(f"  This is a SIGNAL-GENERATION problem, not a labeling problem.")
        print(f"  Options:")
        print(f"    1. Loosen pivot_proximity_bars (accept further-away signals)")
        print(f"    2. Modify BAMBAM signal generator to fire more often")
        print(f"    3. Accept that BAMBAM misses these pivots structurally")
    elif buckets['signal exists, holding failed'] > buckets['signal exists, excursion failed']:
        print(f"  Most failures are 'holding failed' — counter-moves don't sustain.")
        print(f"  Consider lowering min_holding_bars.")
    elif buckets['signal exists, excursion failed'] > 0:
        print(f"  Most failures are 'excursion failed' — counter-moves don't reach threshold.")
        print(f"  This is odd for big pivots. Investigate: maybe the move was slow and")
        print(f"  didn't hit the ATR-mult target within lookahead_bars.")

    # ---- SAVE FULL TABLE ----
    outpath = ROOT / 'outputs' / f'pivot_audit_{cfg["timeframe"]}.csv'
    outpath.parent.mkdir(exist_ok=True)
    audit.to_csv(outpath, index=False)
    print(f"\n  Full pivot audit saved: {outpath}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scripts/02_audit_pivots.py <config.yaml>")
        sys.exit(1)
    main(sys.argv[1])
