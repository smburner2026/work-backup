#!/usr/bin/env python3
"""
SIGNAL ENRICHMENT PIPELINE
Matches TV-exported signals to enriched Binance Futures data.

Takes:
  - A signal export CSV (TV Strategy Tester format with embedded features)
  - The merged_5m.csv from binance_futures_data.py

Produces:
  - enriched_signals.csv — every signal with full Binance context
  - enriched_signals_with_labels.csv — also adds swing labels

USAGE:
  python enrich_signals.py <signal_csv> [--perp perp_csv] [--label]
"""

import csv
import sys
import os
from datetime import datetime, timezone, timedelta
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))

# Feature names from the 24-feat export
FEAT_NAMES = ['vol','vd','avgVol','volRatio','vdRatio','vb','vs',
              'rsi14','rsi7','dist_ema21','dist_ema50','dist_ema200','macd_hist','atr14',
              'rsi14_delta','rsi7_delta','macd_hist_delta','price_mom5','volRatio_delta',
              'vdRatio_delta','ema21_bear','ema21_bull','ema50_bear','ema50_bull']

def load_signals(path):
    """Load signals from TV export CSV. Detects format automatically."""
    with open(path, encoding='utf-8-sig') as f:
        content = f.read()
    if content.startswith('\ufeff'):
        content = content[1:]
    
    rows = list(csv.DictReader(content.splitlines()))
    signals = []
    
    for r in rows:
        if 'Entry' not in r.get('Type', ''):
            continue
        
        sig = r['Signal']
        dt = datetime.strptime(r['Date and time'], '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
        price = float(r['Price USDT'])
        
        parts = sig.split('|')
        
        # Detect format
        if len(parts) == 25:  # 24-feat delta export
            direction = 'short' if parts[0].startswith('BEAR') else 'long'
            feats = {}
            for i, name in enumerate(FEAT_NAMES):
                feats[name] = float(parts[i+1])
            signals.append({'dt': dt, 'price': price, 'direction': direction, **feats})
        
        elif len(parts) >= 7:  # 7-feat export (no direction prefix)
            direction = 'short' if 'short' in r['Type'] else 'long'
            signals.append({
                'dt': dt, 'price': price, 'direction': direction,
                'vol': float(parts[0]), 'vd': float(parts[1]),
                'avgVol': float(parts[2]), 'volRatio': float(parts[3]),
                'vdRatio': float(parts[4]), 'vb': float(parts[5]), 'vs': float(parts[6]),
            })
        
        else:  # Raw signal capture
            direction = 'short' if sig.startswith('BEAR') else 'long'
            signals.append({'dt': dt, 'price': price, 'direction': direction})
    
    signals.sort(key=lambda s: s['dt'])
    return signals


def load_perp_data(path):
    """Load merged_5m.csv from Binance download."""
    with open(path) as f:
        content = f.read()
    if content.startswith('\ufeff'):
        content = content[1:]
    
    rows = list(csv.DictReader(content.splitlines()))
    data = []
    for r in rows:
        dt = datetime.strptime(r['time_str'], '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
        d = {'dt': dt, 'open': float(r['open']), 'high': float(r['high']),
             'low': float(r['low']), 'close': float(r['close']),
             'volume': float(r.get('volume', 0))}
        # Optional enrichment fields
        for field in ['oi_base', 'oi_usd', 'taker_buy_vol', 'taker_sell_vol',
                       'top_long_acct', 'top_short_acct', 'top_long_pos', 'top_short_pos',
                       'global_long_pct', 'global_short_pct', 'taker_buy_base_vol']:
            v = r.get(field, '')
            d[field] = float(v) if v else None
        data.append(d)
    
    data.sort(key=lambda x: x['dt'])
    return data


def enrich(signals, perp_data, offset_minutes=5):
    """Match signals to perp data by timestamp. Returns enriched signals."""
    perp_idx = {p['dt']: p for p in perp_data}
    enriched = []
    matched = 0
    
    for s in signals:
        sig_dt = s['dt']
        
        # Try exact match, then -5min, then +5min
        cand = perp_idx.get(sig_dt)
        if cand is None:
            cand = perp_idx.get(sig_dt - timedelta(minutes=5))
        if cand is None:
            cand = perp_idx.get(sig_dt + timedelta(minutes=5))
        
        if cand is None:
            continue
        
        matched += 1
        entry = {
            'signal_time': s['dt'].strftime('%Y-%m-%d %H:%M'),
            'direction': s['direction'],
            'entry_price': s['price'],
        }
        
        # Forward features from signal
        for k in ['vol', 'vd', 'avgVol', 'volRatio', 'vdRatio', 'vb', 'vs',
                   'rsi14', 'rsi7', 'dist_ema21', 'dist_ema50', 'dist_ema200',
                   'macd_hist', 'atr14', 'rsi14_delta', 'rsi7_delta', 'macd_hist_delta',
                   'price_mom5', 'volRatio_delta', 'vdRatio_delta',
                   'ema21_bear', 'ema21_bull', 'ema50_bear', 'ema50_bull']:
            if k in s:
                entry[k] = s[k]
        
        # Enrich with perp data
        entry['perp_time'] = cand['dt'].strftime('%Y-%m-%d %H:%M')
        entry['perp_open'] = cand['open']
        entry['perp_high'] = cand['high']
        entry['perp_low'] = cand['low']
        entry['perp_close'] = cand['close']
        entry['perp_volume'] = cand['volume']
        
        for field in ['oi_base', 'oi_usd', 'taker_buy_vol', 'taker_sell_vol',
                       'top_long_acct', 'top_short_acct', 'top_long_pos', 'top_short_pos',
                       'global_long_pct', 'global_short_pct', 'taker_buy_base_vol']:
            entry[field] = cand.get(field)
        
        enriched.append(entry)
    
    return enriched


def add_swing_labels(enriched, perp_data, target_pct=0.5, bars_forward=48):
    """Label each signal: did price swing target_pct within bars_forward bars?"""
    # Build fast price lookup
    perp_idx = {p['dt']: i for i, p in enumerate(perp_data)}
    close_arr = np.array([p['close'] for p in perp_data])
    high_arr = np.array([p['high'] for p in perp_data])
    low_arr = np.array([p['low'] for p in perp_data])
    N = len(perp_data)
    
    for s in enriched:
        sig_dt = datetime.strptime(s['signal_time'], '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
        idx = perp_idx.get(sig_dt)
        if idx is None:
            idx = perp_idx.get(sig_dt - timedelta(minutes=5))
        
        if idx is None or idx + bars_forward >= N:
            s['valid_signal'] = False
            continue
        
        s['valid_signal'] = True
        entry_price = s['entry_price']
        
        # Forward window
        end_close = close_arr[min(idx + bars_forward, N - 1)]
        window_best = high_arr[min(idx + bars_forward, N - 1)]
        window_worst = low_arr[min(idx + bars_forward, N - 1)]
        
        if s['direction'] == 'short':
            ret_close = (entry_price - end_close) / entry_price * 100
            best_move = (entry_price - window_best) / entry_price * 100
            worst_move = (entry_price - window_worst) / entry_price * 100
        else:
            ret_close = (end_close - entry_price) / entry_price * 100
            best_move = (window_best - entry_price) / entry_price * 100
            worst_move = (window_worst - entry_price) / entry_price * 100
        
        s['ret_close_4h'] = round(ret_close, 2)
        s['best_move_4h'] = round(best_move, 2)
        s['worst_move_4h'] = round(worst_move, 2)
        s[f'swing_{target_pct}pct'] = ret_close > target_pct
        s[f'swing_best_{target_pct}pct'] = best_move > target_pct


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    signal_path = sys.argv[1]
    perp_path = None
    add_labels = '--label' in sys.argv
    
    for i, arg in enumerate(sys.argv):
        if arg == '--perp' and i + 1 < len(sys.argv):
            perp_path = sys.argv[i + 1]
        if arg == '--label':
            add_labels = True
    
    if perp_path is None:
        # Default search paths
        for candidate in [
            os.path.join(BASE, 'data', 'binance_futures', 'BTCUSDT', 'merged_5m.csv'),
            os.path.join(BASE, 'data', 'btcusdt_perp_5m.csv'),
        ]:
            if os.path.exists(candidate):
                perp_path = candidate
                break
    
    if perp_path and os.path.exists(perp_path):
        print(f"Loading perp data: {perp_path}")
        perp_data = load_perp_data(perp_path)
    else:
        print("NO perp data found. Enrichment skipped — supply --perp <path>")
        perp_data = None
    
    print(f"Loading signals: {signal_path}")
    signals = load_signals(signal_path)
    print(f"  {len(signals)} signals loaded")
    
    if perp_data:
        enriched = enrich(signals, perp_data)
        print(f"  {len(enriched)}/{len(signals)} matched to perp data")
        
        if add_labels:
            add_swing_labels(enriched, perp_data)
        
        base_name = os.path.splitext(os.path.basename(signal_path))[0]
        out_path = os.path.join(BASE, 'data', 'exports', f'{base_name}_enriched.csv')
        
        if enriched:
            fields = list(enriched[0].keys())
            with open(out_path, 'w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader(); w.writerows(enriched)
            print(f"\n  → {out_path}  ({len(enriched)} signals)")
            
            if add_labels:
                valid = [s for s in enriched if s.get('valid_signal')]
                if valid:
                    hit_rate = sum(1 for s in valid if s.get(f'swing_0.5pct')) / len(valid)
                    print(f"  Swing hit rate (close, 0.5%): {hit_rate:.1%} ({len(valid)} valid signals)")
    else:
        print("Signals loaded but not enriched (no perp data available).")

if __name__ == '__main__':
    main()
