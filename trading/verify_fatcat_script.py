#!/usr/bin/env python3
"""Verify proposed FATCAT Pine Script change against real entries."""
import csv, os, pandas as pd, numpy as np
from datetime import datetime

os.chdir('/root/work/trading')

# Load all CSVs
csvs = sorted([f for f in os.listdir('.') if f.startswith('BTCUSDT-15m-') and f.endswith('.csv')])
print(f"Found {len(csvs)} CSV files")

dfs = []
for csv_file in csvs:
    df = pd.read_csv(csv_file)
    dfs.append(df)

df = pd.concat(dfs).drop_duplicates(subset=['open_time']).sort_values('open_time').reset_index(drop=True)
print(f"Total bars: {len(df):,}")
print(f"Range: {pd.to_datetime(df['open_time'].iloc[0], unit='ms')} to {pd.to_datetime(df['open_time'].iloc[-1], unit='ms')}")

# Load FATCAT entries
def load_fatcat(path):
    entries = []
    with open(path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        seen = set()
        for row in reader:
            if row['Type'] == 'Entry long' and row['Signal'] not in seen:
                seen.add(row['Signal'])
                entries.append({
                    'signal': row['Signal'],
                    'time': datetime.strptime(row['Date and time'][:16], '%Y-%m-%d %H:%M'),
                    'price': float(row['Price USDT']),
                })
    return entries

fatcat_v1 = load_fatcat('/root/.hermes/cache/documents/doc_cc6c34df5643_FEROCIOUS_FATCAT_Single_Direction_BINANCE_BTCUSDT_P_2026_05_21.csv')
fatcat_v2 = load_fatcat('/root/.hermes/cache/documents/doc_8af71d3ac8fc_FEROCIOUS_FATCAT_Single_Direction_BINANCE_BTCUSDT_P_2026_05_21_2.csv')

fc1_times = set(f['time'].strftime('%Y-%m-%d %H:%M') for f in fatcat_v1)
fc2_times = set(f['time'].strftime('%Y-%m-%d %H:%M') for f in fatcat_v2)

print(f"\nFATCAT v1: {len(fatcat_v1)} entries")
print(f"FATCAT v2: {len(fatcat_v2)} entries")

# Pre-compute volume estimates
df['range'] = df['high'] - df['low']
df['range'] = df['range'].replace(0, np.nan)
df['vb_estimate'] = df['volume'] * (df['close'] - df['low']) / df['range']
df['vs_estimate'] = df['volume'] * (df['high'] - df['close']) / df['range']
df['vb_estimate'] = df['vb_estimate'].fillna(0)
df['vs_estimate'] = df['vs_estimate'].fillna(0)

# Real taker_buy
df['vb_real'] = df['taker_buy_volume']
df['vs_real'] = df['volume'] - df['taker_buy_volume']

# Signal engine
def bambam_signals(df, vb_col, vs_col, lookback=200, vol_mult=1.0, less_ratio=0.03, delta_mode='OR'):
    d = df.copy()
    d['open_time_dt'] = pd.to_datetime(d['open_time'], unit='ms')
    d['ph'] = d['high'].shift(1)
    d['pl'] = d['low'].shift(1)
    d['vd'] = (d[vb_col] - d[vs_col]).shift(1)
    d['bvol'] = (d[vb_col] + d[vs_col]).shift(1)
    d['top'] = d['ph'].rolling(window=lookback, min_periods=1).max()
    d['btm'] = d['pl'].rolling(window=lookback, min_periods=1).min()
    d['avg_vol'] = d['bvol'].rolling(window=lookback, min_periods=1).mean()
    d['vd_ratio'] = np.abs(d['vd'] / d['bvol'].replace(0, np.nan))
    d['is_less'] = d['vd_ratio'] < less_ratio
    d['high_vol'] = d['bvol'] > (d['avg_vol'] * vol_mult)
    if delta_mode == 'OR':
        d['bear_delta'] = d['is_less'] | (d['vd'] < 0)
        d['bull_delta'] = d['is_less'] | (d['vd'] > 0)
    else:
        d['bear_delta'] = d['is_less'] & (d['vd'] < 0)
        d['bull_delta'] = d['is_less'] & (d['vd'] > 0)
    d['bear_raw'] = (d['ph'] >= d['top']) & d['high_vol'] & d['bear_delta']
    d['bull_raw'] = (d['pl'] <= d['btm']) & d['high_vol'] & d['bull_delta']
    d['bear_signal'] = d['bear_raw'].shift(-1).fillna(False)
    d['bull_signal'] = d['bull_raw'].shift(-1).fillna(False)
    return d

# Test configurations
configs = [
    ("BAMBAM Orig (estimate, vm=1.5, lr=0.05, OR)", 'vb_estimate', 'vs_estimate', 200, 1.5, 0.05, 'OR'),
    ("FATCAT Claim (real_taker, vm=1.0, lr=0.03, OR)", 'vb_real', 'vs_real', 200, 1.0, 0.03, 'OR'),
    ("Real taker + high vol (vm=1.5)", 'vb_real', 'vs_real', 200, 1.5, 0.03, 'OR'),
    ("Estimate only (vm=1.0, lr=0.03)", 'vb_estimate', 'vs_estimate', 200, 1.0, 0.03, 'OR'),
]

print("\n\n========== VERIFICATION ==========")

for name, vb_col, vs_col, lb, vm, lr, dm in configs:
    d = bambam_signals(df, vb_col, vs_col, lb, vm, lr, dm)
    
    # v1: Oct 7 - Dec 15 2025
    v1_sigs = d[(d['bull_signal']) & (d['open_time_dt'] >= '2025-09-25') & (d['open_time_dt'] <= '2025-12-20')]
    v1_match = set(v1_sigs['open_time_dt'].dt.strftime('%Y-%m-%d %H:%M')) & fc1_times
    
    # v2: Apr 27 - May 18 2026
    v2_sigs = d[(d['bull_signal']) & (d['open_time_dt'] >= '2026-04-25') & (d['open_time_dt'] <= '2026-05-20')]
    v2_match = set(v2_sigs['open_time_dt'].dt.strftime('%Y-%m-%d %H:%M')) & fc2_times
    
    print(f"\n{name}:")
    print(f"  v1: {len(v1_sigs):>3} signals, {len(v1_match):>2}/{len(fatcat_v1)} matched")
    print(f"  v2: {len(v2_sigs):>3} signals, {len(v2_match):>2}/{len(fatcat_v2)} matched")

# DETAILED v2 MATCH
print("\n\n========== DETAILED v2 MATCH ==========")
d_claim = bambam_signals(df, 'vb_real', 'vs_real', 200, 1.0, 0.03, 'OR')
v2_sigs = d_claim[(d_claim['bull_signal']) & (d_claim['open_time_dt'] >= '2026-04-25') & (d_claim['open_time_dt'] <= '2026-05-20')]
v2_sig_times = set(v2_sigs['open_time_dt'].dt.strftime('%Y-%m-%d %H:%M'))

print("\nGenerated signals:")
for _, s in v2_sigs.iterrows():
    ts = s['open_time_dt'].strftime('%Y-%m-%d %H:%M')
    match = "← MATCH" if ts in fc2_times else ""
    print(f"  ${s['close']:.0f} @ {ts} {match}")

print("\nFATCAT v2 entries:")
for f in fatcat_v2:
    ts = f['time'].strftime('%Y-%m-%d %H:%M')
    match = "← HIT" if ts in v2_sig_times else "← MISS"
    print(f"  ${f['price']:.0f} @ {ts} {match}")

hits = v2_sig_times & fc2_times
misses = fc2_times - v2_sig_times
extras = v2_sig_times - fc2_times
print(f"\nResult: {len(hits)}/{len(fatcat_v2)} matched, {len(misses)} missed, {len(extras)} extras")

# DETAILED v1 MATCH
print("\n\n========== DETAILED v1 MATCH ==========")
v1_sigs = d_claim[(d_claim['bull_signal']) & (d_claim['open_time_dt'] >= '2025-09-25') & (d_claim['open_time_dt'] <= '2025-12-20')]
v1_sig_times = set(v1_sigs['open_time_dt'].dt.strftime('%Y-%m-%d %H:%M'))

hits_v1 = v1_sig_times & fc1_times
misses_v1 = fc1_times - v1_sig_times
extras_v1 = v1_sig_times - fc1_times
print(f"Result: {len(hits_v1)}/{len(fatcat_v1)} matched, {len(misses_v1)} missed, {len(extras_v1)} extras")

print("\nMissed entries:")
for f in fatcat_v1:
    ts = f['time'].strftime('%Y-%m-%d %H:%M')
    if ts in misses_v1:
        print(f"  ${f['price']:.0f} @ {ts} ({f['signal']})")

# Also check POCKETBAMBAM to compare
pbb_path = '/root/.hermes/cache/documents/doc_d42c7ed3df2c_POCKETBAMBAM_-_Fixed_BINANCE_BTCUSDT.P_2026-05-21.csv'
try:
    pbb = []
    with open(pbb_path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        seen = set()
        for row in reader:
            if row['Type'] == 'Entry long' and row['Signal'] not in seen:
                seen.add(row['Signal'])
                pbb.append({
                    'signal': row['Signal'],
                    'time': datetime.strptime(row['Date and time'][:16], '%Y-%m-%d %H:%M'),
                    'price': float(row['Price USDT']),
                })
    print(f"\n\nPOCKETBAMBAM entries: {len(pbb)}")
    
    # V1: How many POCKETBAMBAM match FATCAT?
    pbb_v1_times = set(p['time'].strftime('%Y-%m-%d %H:%M') for p in pbb)
    print(f"  v1 overlap: {len(pbb_v1_times & fc1_times)}/{len(fatcat_v1)}")
    print(f"  v2 overlap: {len(pbb_v1_times & fc2_times)}/{len(fatcat_v2)}")
except:
    pass
