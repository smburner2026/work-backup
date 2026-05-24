"""
BAMBAM vs FATCAT Signal Generator — Binance 15m with taker_buy_base
====================================================================
Purpose: Replicate the exact signal count comparison that confirmed
         FATCAT uses real taker_buy volume vs BAMBAM's estimate.

Usage:
    python scripts/selectivity_analyzer.py

Expected output:
    Signal counts for both volume sources at vm=1.0, 1.5, 2.0
"""

import requests, zipfile, io, pandas as pd, numpy as np
from datetime import datetime, timedelta

# === CONFIG ===
PAIR = "BTCUSDT"
TIMEFRAME = "15m"
START = datetime(2026, 2, 23)
END = datetime(2026, 5, 19)
LOOKBACK = 200
BASE_URL = f"https://data.binance.vision/data/spot/daily/klines/{PAIR}/{TIMEFRAME}"

# === FETCH ===
all_data = []
current = START
while current <= END:
    ds = current.strftime('%Y-%m-%d')
    try:
        r = requests.get(f"{BASE_URL}/{PAIR}-{TIMEFRAME}-{ds}.zip", timeout=30)
        if r.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            with z.open(z.namelist()[0]) as f:
                for line in f.read().decode('utf-8').strip().split('\n'):
                    p = line.split(',')
                    all_data.append({'t': int(p[0])//1000, 'o': float(p[1]),
                        'h': float(p[2]), 'l': float(p[3]), 'c': float(p[4]),
                        'v': float(p[5]), 'tb': float(p[9])})
    except Exception as e:
        pass
    current += timedelta(days=1)

df = pd.DataFrame(all_data)
df["dt"] = pd.to_datetime(df["t"], unit="ms")
df = df.sort_values("t").reset_index(drop=True)

# === FEATURES ===
rng = (df["h"] - df["l"]).replace(0, np.nan)
vb_est = (df["v"] * (df["c"] - df["l"]) / rng).fillna(0)
vs_est = (df["v"] * (df["h"] - df["c"]) / rng).fillna(0)
df["pl"] = df["l"].shift(1)
df["btm"] = df["pl"].rolling(window=LOOKBACK, min_periods=1).min()

def count_signals(vol_type, vm, lr=0.03, dm="OR"):
    """Count signals for given volume source and parameters."""
    raw = pd.Series(False, index=df.index)
    
    for i in range(LOOKBACK, len(df)):
        if vol_type == "EST":
            bvol = (vb_est + vs_est).shift(1).iloc[i]
            avg = (vb_est + vs_est).shift(1).rolling(LOOKBACK, min_periods=1).mean().iloc[i]
            vd = (vb_est - vs_est).shift(1).iloc[i]
        else:
            bvol = df["v"].shift(1).iloc[i]
            avg = df["v"].shift(1).rolling(LOOKBACK, min_periods=1).mean().iloc[i]
            vd = ((df["tb"] - (df["v"] - df["tb"])).shift(1)).iloc[i]
        
        if bvol <= 0: continue
        vdr = abs(vd / bvol)
        isl = vdr < lr
        hv = bvol > avg * vm
        dok = (isl or vd > 0) if dm == "OR" else (isl and vd > 0)
        raw.iloc[i] = (df['pl'].iloc[i] <= df['btm'].iloc[i]) and hv and dok
    
    sig = raw.shift(-1).fillna(False)
    return int(sig[df['dt'] >= str(START.date())].sum())

# === COMPARE ===
print(f"{'Volume':>10} {'vm=1.0':>8} {'vm=1.5':>8} {'vm=2.0':>8}")
print("="*40)
for vol in ["EST", "TAKER"]:
    counts = [count_signals(vol, v) for v in [1.0, 1.5, 2.0]]
    print(f"{vol:>10} {counts[0]:>8} {counts[1]:>8} {counts[2]:>8}")

print(f"\n{'FATCAT':>10} {18:>8}")
print(f"{'BAMBAM':>10} {50:>8}")
