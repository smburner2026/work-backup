#!/usr/bin/env python3
"""
BAMBAM Strategy Backtester
Produces entry/exit CSV and P&L metrics.
Usage: python3 backtester.py [--less-ratio 0.03] [--vol-mult 1.0] [--gate-bars 140] [--tp-pct 5.0]
"""
import os, sys, glob, argparse
import pandas as pd
import numpy as np
from datetime import datetime

def load_data(data_dir='/root/work/trading'):
    """Load all Binance 15m futures CSVs."""
    csvs = sorted(glob.glob(os.path.join(data_dir, 'BTCUSDT-15m-*.csv')))
    if not csvs:
        print("No CSV files found. Run download first.")
        sys.exit(1)
    
    dfs = []
    for cf in csvs:
        df = pd.read_csv(cf)
        dfs.append(df)
    
    df = pd.concat(dfs).drop_duplicates(subset=['open_time']).sort_values('open_time').reset_index(drop=True)
    df['open_time_dt'] = pd.to_datetime(df['open_time'], unit='ms')
    return df

def compute_signals(df, lookback=200, less_ratio=0.05, vol_mult=1.0, delta_mode='OR'):
    """Compute BAMBAM bull/bear signals."""
    d = df.copy()
    
    # Volume decomposition (candle-body estimate)
    rng = d['high'] - d['low']
    rng = rng.replace(0, np.nan)
    d['vb'] = d['volume'] * (d['close'] - d['low']) / rng
    d['vs'] = d['volume'] * (d['high'] - d['close']) / rng
    d['vb'] = d['vb'].fillna(0)
    d['vs'] = d['vs'].fillna(0)
    
    # Pine-equivalent: check prior bar values on current bar
    d['ph'] = d['high'].shift(1)
    d['pl'] = d['low'].shift(1)
    d['vd'] = (d['vb'] - d['vs']).shift(1)
    d['vol'] = (d['vb'] + d['vs']).shift(1)
    
    d['top'] = d['ph'].rolling(window=lookback, min_periods=1).max()
    d['btm'] = d['pl'].rolling(window=lookback, min_periods=1).min()
    d['avg_vol'] = d['vol'].rolling(window=lookback, min_periods=1).mean()
    d['vd_ratio'] = np.abs(d['vd'] / d['vol'].replace(0, np.nan))
    d['is_less'] = d['vd_ratio'] < less_ratio
    d['high_vol'] = d['vol'] > (d['avg_vol'] * vol_mult)
    
    if delta_mode == 'OR':
        d['bull_signal'] = (d['pl'] <= d['btm']) & d['high_vol'] & (d['is_less'] | (d['vd'] > 0))
        d['bear_signal'] = (d['ph'] >= d['top']) & d['high_vol'] & (d['is_less'] | (d['vd'] < 0))
    else:  # AND
        d['bull_signal'] = (d['pl'] <= d['btm']) & d['high_vol'] & d['is_less'] & (d['vd'] > 0)
        d['bear_signal'] = (d['ph'] >= d['top']) & d['high_vol'] & d['is_less'] & (d['vd'] < 0)
    
    return d

def apply_gate(df, gate_bars):
    """Apply cooldown gate to bull signals."""
    d = df.copy()
    bars_since = gate_bars + 1
    gated = []
    
    for i in range(len(d)):
        bars_since += 1
        if d['bull_signal'].iloc[i]:
            if bars_since >= gate_bars:
                gated.append(True)
                bars_since = 0
            else:
                gated.append(False)
        else:
            gated.append(False)
    
    d['gated_signal'] = gated
    return d

def simulate_trades(df, tp_pct=5.0, max_adds=3):
    """Simulate TP-only exits. No stop loss."""
    trades = []
    open_trades = []  # list of (entry_idx, entry_price)
    
    for i in range(len(df)):
        # Check TP for existing trades
        if open_trades:
            current_close = df['close'].iloc[i]
            avg_price = sum(t[1] for t in open_trades) / len(open_trades)
            tp_level = avg_price * (1 + tp_pct / 100)
            
            if current_close >= tp_level:
                exit_time = df['open_time_dt'].iloc[i]
                exit_price = current_close
                entry_time = df['open_time_dt'].iloc[open_trades[0][0]]
                entry_price = avg_price
                
                # Calculate P&L for each lot
                for idx, ep in open_trades:
                    pnl_pct = (exit_price / ep - 1) * 100
                    trades.append({
                        'entry_time': df['open_time_dt'].iloc[idx],
                        'entry_price': ep,
                        'exit_time': exit_time,
                        'exit_price': exit_price,
                        'pnl_pct': pnl_pct,
                        'position_qty': len(open_trades),
                    })
                
                open_trades = []
        
        # Enter on gated bull signal
        if df['gated_signal'].iloc[i] and len(open_trades) < max_adds:
            open_trades.append((i, df['close'].iloc[i]))
    
    return trades

def main():
    parser = argparse.ArgumentParser(description='BAMBAM Strategy Backtester')
    parser.add_argument('--less-ratio', type=float, default=0.05)
    parser.add_argument('--vol-mult', type=float, default=1.0)
    parser.add_argument('--delta-mode', default='OR', choices=['OR', 'AND'])
    parser.add_argument('--lookback', type=int, default=200)
    parser.add_argument('--gate-bars', type=int, default=140, help='Cooldown (140 ≈ 35h @ 15m)')
    parser.add_argument('--tp-pct', type=float, default=5.0)
    parser.add_argument('--max-adds', type=int, default=3)
    parser.add_argument('--output', default=None)
    args = parser.parse_args()
    
    print(f"BAMBAM Backtest: lr={args.less_ratio}, vm={args.vol_mult}, mode={args.delta_mode}, gate={args.gate_bars}b, tp={args.tp_pct}%")
    
    df = load_data()
    print(f"Data: {len(df):,} bars, {df['open_time_dt'].iloc[0]} → {df['open_time_dt'].iloc[-1]}")
    
    df = compute_signals(df, args.lookback, args.less_ratio, args.vol_mult, args.delta_mode)
    
    # Raw signal stats
    raw_bull = df[df['bull_signal']]
    raw_bear = df[df['bear_signal']]
    print(f"Raw BAMBAM: {len(raw_bull)} bull, {len(raw_bear)} bear in {len(df)} bars ({len(raw_bull)/len(df)*100:.2f}%)")
    
    df = apply_gate(df, args.gate_bars)
    gated = df[df['gated_signal']]
    print(f"Gated (cooldown {args.gate_bars}b): {len(gated)} entries")
    
    trades = simulate_trades(df, args.tp_pct, args.max_adds)
    print(f"Trades: {len(trades)} exits")
    
    if trades:
        pnls = [t['pnl_pct'] for t in trades]
        wins = sum(1 for p in pnls if p > 0)
        print(f"Win rate: {wins}/{len(trades)} ({wins/len(trades)*100:.1f}%)")
        print(f"Mean P&L: {np.mean(pnls):.2f}%")
        print(f"Total P&L: {sum(pnls):.2f}%")
        print(f"Max win: {max(pnls):.2f}%")
        print(f"Max loss: {min(pnls):.2f}%")
        
        td = pd.DataFrame(trades)
        td = td.sort_values('entry_time')
        
        output = args.output or f'bambam_backtest_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
        td.to_csv(output, index=False)
        print(f"\nTrade log → {output}")
        print(f"\nFirst 10 trades:")
        for _, t in td.head(10).iterrows():
            print(f"  {t['entry_time']} @ ${t['entry_price']:.0f} → {t['exit_time']} @ ${t['exit_price']:.0f} = {t['pnl_pct']:+.2f}%")
    else:
        print("No trades generated.")

if __name__ == '__main__':
    main()
