"""
scripts/01_visualize_labels.py
==============================

THE MOST IMPORTANT STEP. Run this before doing anything else.

Loads perp data + signals, runs ZigZag pivot detection, labels
signals as true-reversal-or-not, then produces:

  1. Console summary of label counts and quality stats
  2. A plot of price with pivots marked + signals colored by label,
     so you can EYEBALL whether the labels match your intuition

This script's job is to make you trust (or distrust) the labels.
If the chart looks wrong — pivots in stupid places, "true
reversal" labels on obvious chop, "false" labels on the actual
trend-turning bottoms — DO NOT proceed to training. Tune the
config (atr_mult, min_reversal_atr_mult, etc.) until the visual
matches your intuition. Then proceed.

USAGE:
    cd swing_research/
    python scripts/01_visualize_labels.py configs/tf_5m.yaml

OUTPUTS:
    A PNG saved to outputs/label_viz_<timeframe>.png and a
    plotly HTML file at outputs/label_viz_<timeframe>.html
    (the HTML is zoomable/interactive, much better for inspection).
"""

import sys
import yaml
import pandas as pd
from pathlib import Path

# Add project root to path so `from lib.x import y` works
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.data_loader import load_all
from lib.labeling import (
    compute_atr, compute_zigzag_pivots, label_signals, labeling_summary,
)


def main(config_path: str):
    print(f"\n{'=' * 70}")
    print(f"LABEL VALIDATION: {config_path}")
    print(f"{'=' * 70}\n")

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    print(f"Timeframe: {cfg['timeframe']}")
    print(f"ATR period: {cfg['atr_period']}")
    print(f"ZigZag threshold: {cfg['zigzag_atr_mult']} × ATR")
    print(f"Pivot proximity: ±{cfg['pivot_proximity_bars']} bars")
    print(f"Min reversal: {cfg['min_reversal_atr_mult']} × ATR")
    print(f"Min holding: {cfg['min_holding_bars']} bars")
    print(f"Lookahead: {cfg['lookahead_bars']} bars\n")

    # ---- LOAD ----
    print("Loading data...")
    perp, sigs = load_all(cfg)

    # ---- ATR + PIVOTS ----
    print("\nComputing ATR + ZigZag pivots...")
    atr = compute_atr(perp, period=cfg['atr_period'])
    pivots = compute_zigzag_pivots(perp, atr, atr_mult=cfg['zigzag_atr_mult'])
    print(f"  Found {len(pivots):,} confirmed pivots "
          f"({sum(1 for p in pivots if p.kind == 'high')} highs, "
          f"{sum(1 for p in pivots if p.kind == 'low')} lows)")

    if len(pivots) < 10:
        print("\n  WARNING: very few pivots. zigzag_atr_mult may be too high.")
    elif len(pivots) > len(perp) / 10:
        print("\n  WARNING: many pivots. zigzag_atr_mult may be too low.")

    # ---- LABEL ----
    print("\nLabeling signals...")
    labeled = label_signals(
        sigs, perp, pivots, atr,
        pivot_proximity_bars=cfg['pivot_proximity_bars'],
        min_reversal_atr_mult=cfg['min_reversal_atr_mult'],
        min_holding_bars=cfg['min_holding_bars'],
        lookahead_bars=cfg['lookahead_bars'],
    )

    summary = labeling_summary(labeled)
    print("\n" + "─" * 50)
    print("LABEL SUMMARY")
    print("─" * 50)
    for k, v in summary.items():
        if isinstance(v, dict):
            print(f"  {k}:")
            for kk, vv in v.items():
                print(f"      {kk}: {vv}")
        elif isinstance(v, float):
            print(f"  {k}: {v:.3f}")
        else:
            print(f"  {k}: {v}")

    rate = summary['reversal_rate']
    print()
    if rate < 0.02:
        print(f"  ⚠ Reversal rate {rate:.1%} is LOW. Label may be too tight.")
        print(f"    Consider: lower min_reversal_atr_mult or min_holding_bars.")
    elif rate > 0.25:
        print(f"  ⚠ Reversal rate {rate:.1%} is HIGH. Label may be too loose.")
        print(f"    Consider: raise min_reversal_atr_mult or min_holding_bars.")
    else:
        print(f"  ✓ Reversal rate {rate:.1%} is in the expected 2-25% range.")

    # ---- SAVE LABELED OUTPUT ----
    outdir = ROOT / 'outputs'
    outdir.mkdir(exist_ok=True)
    label_csv = outdir / f"labeled_signals_{cfg['timeframe']}.csv"
    labeled.to_csv(label_csv)
    print(f"\n  Saved labels: {label_csv}")

    # ---- VISUALIZE ----
    print("\nBuilding visualization...")
    try:
        import plotly.graph_objects as go
    except ImportError:
        print("  plotly not installed — skipping interactive HTML.")
        print("  Install with: pip install plotly")
    else:
        # Subsample perp if it's huge — plotly hates >100k candles
        plot_perp = perp
        if len(perp) > 20_000:
            print(f"  Subsampling perp from {len(perp):,} to 20,000 bars for plot")
            stride = len(perp) // 20_000
            plot_perp = perp.iloc[::stride]

        fig = go.Figure()

        # Candles
        fig.add_trace(go.Candlestick(
            x=plot_perp.index,
            open=plot_perp['open'], high=plot_perp['high'],
            low=plot_perp['low'], close=plot_perp['close'],
            name='Price', showlegend=False,
            increasing_line_color='#26a69a', decreasing_line_color='#ef5350',
        ))

        # Pivots
        pivot_high_x = [p.timestamp for p in pivots if p.kind == 'high']
        pivot_high_y = [p.price for p in pivots if p.kind == 'high']
        pivot_low_x = [p.timestamp for p in pivots if p.kind == 'low']
        pivot_low_y = [p.price for p in pivots if p.kind == 'low']

        fig.add_trace(go.Scatter(
            x=pivot_high_x, y=pivot_high_y,
            mode='markers', name='Pivot High',
            marker=dict(color='red', size=10, symbol='triangle-down',
                        line=dict(width=1, color='darkred')),
        ))
        fig.add_trace(go.Scatter(
            x=pivot_low_x, y=pivot_low_y,
            mode='markers', name='Pivot Low',
            marker=dict(color='lime', size=10, symbol='triangle-up',
                        line=dict(width=1, color='darkgreen')),
        ))

        # Signals — colored by label
        valid = labeled[~labeled['labeling_skipped']]
        for direction in ['long', 'short']:
            for label, color, suffix in [(True, 'gold', '✓ True Reversal'),
                                          (False, 'gray', '✗ Not Reversal')]:
                subset = valid[(valid['direction'] == direction) &
                               (valid['is_true_reversal'] == label)]
                if len(subset) == 0:
                    continue
                symbol = 'circle' if direction == 'long' else 'x'
                fig.add_trace(go.Scatter(
                    x=subset.index, y=subset['entry_price'],
                    mode='markers',
                    name=f"{direction.upper()} {suffix} (n={len(subset)})",
                    marker=dict(
                        color=color, size=8 if label else 5,
                        symbol=symbol,
                        line=dict(width=1, color='black' if label else 'gray'),
                        opacity=0.9 if label else 0.4,
                    ),
                    hovertemplate=(
                        f"<b>{direction.upper()}</b><br>"
                        "%{x}<br>$%{y:.2f}<br>"
                        "excursion=%{customdata[0]:.2f} ATR<br>"
                        "hold=%{customdata[1]} bars"
                    ),
                    customdata=subset[['forward_excursion_atr',
                                       'forward_hold_bars']].values,
                ))

        fig.update_layout(
            title=(f"Label Validation — {cfg['timeframe']}<br>"
                   f"<sub>ZigZag={cfg['zigzag_atr_mult']}×ATR, "
                   f"MinReversal={cfg['min_reversal_atr_mult']}×ATR, "
                   f"MinHold={cfg['min_holding_bars']} bars</sub>"),
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            height=800,
        )

        html_path = outdir / f"label_viz_{cfg['timeframe']}.html"
        fig.write_html(html_path)
        print(f"  Saved interactive plot: {html_path}")

    print(f"\n{'=' * 70}")
    print("NEXT STEP:")
    print("  Open the HTML file. Zoom in on a few areas.")
    print("  Confirm:")
    print("    - Pivots are placed at obvious tops/bottoms")
    print("    - Gold-colored signals are at REAL reversal points")
    print("    - Gray signals are at chop / pullbacks / fakeouts")
    print("  If labels look wrong, tune the config and re-run.")
    print("  Only proceed to model training once labels look right.")
    print(f"{'=' * 70}\n")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scripts/01_visualize_labels.py <config.yaml>")
        sys.exit(1)
    main(sys.argv[1])
