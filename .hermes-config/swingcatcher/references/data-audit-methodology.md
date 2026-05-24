# TV Export Data Audit — 7-Point Methodology

Every time a new BAMBAM feature export CSV arrives from TradingView, run these 7 checks before doing any analysis.

## The Checks

### 1. Feature Count = 25
The Signal column must split into exactly 25 parts: direction + 24 features.

```python
parts = row['Signal'].split('|')
assert len(parts) == 25, f"Signal has {len(parts)} parts"
```

### 2. No NaN Values
Check all 24 numeric positions for nan/NaN/empty.

```python
has_nan = any(p == 'nan' or p == 'NaN' or p == '' for p in parts[1:])
```

### 3. vb + vs ≈ vol
The split of volume into buy (vb=parts[6]) and sell (vs=parts[7]) must equal vol_body (parts[1]). Tolerance: 1%.

If this fails across many signals, the Pine export has the `strategy.entry()` deferred evaluation bug — the fix is to pre-compute all `str.tostring()` at top scope and concatenate inline.

```python
vol = float(parts[1])
vb  = float(parts[6])
vs  = float(parts[7])
assert abs(vb + vs - vol) < 0.01 * vol
```

### 4. Date Range Check
Confirm the date range matches what was expected.

```python
dt = datetime.strptime(row['Date and time'], '%Y-%m-%d %H:%M')
min_dt = min(min_dt, dt); max_dt = max(max_dt, dt)
```

### 5. Direction Counts
Count "BULL" vs "BEAR" — should be roughly balanced for raw BAMBAM.

```python
if dir.startswith('BEAR'): shorts += 1
else: longs += 1
```

### 6. Signal Column Readable
The Signal column should start with "BULL"/"BEAR", not bare "B"/"S" or empty. This affects strategy name vs capture name.

### 7. Timestamps Match Perp Data
Every signal timestamp should have a corresponding perp 5m candle within ±5 minutes.

```python
perp_times = set(dt_to_idx.keys())
sig_times = set(s['dt'] for s in signals)
overlap = len(sig_times & perp_times) / len(sig_times)
```

## Full Audit Script

```python
import csv
from datetime import datetime

path = 'export.csv'
with open(path) as f:
    c = f.read()
if c.startswith('\ufeff'): c = c[1:]

signals = []
nan_count = 0
vb_vs_mismatch = 0
total = 0
min_dt, max_dt = None, None
longs = shorts = 0

for row in csv.DictReader(c.splitlines()):
    if 'Entry' not in row.get('Type',''): continue
    total += 1
    parts = row['Signal'].split('|')
    if len(parts) != 25:
        print(f'FEATURE COUNT: signal {total} has {len(parts)} parts')
        continue
    dir = parts[0]
    if dir.startswith('BEAR'): shorts += 1 else: longs += 1
    
    dt = datetime.strptime(row['Date and time'], '%Y-%m-%d %H:%M')
    if min_dt is None or dt < min_dt: min_dt = dt
    if max_dt is None or dt > max_dt: max_dt = dt
    
    vol = float(parts[1]); vb = float(parts[6]); vs = float(parts[7])
    
    if any(p == 'nan' or p == 'NaN' or p == '' for p in parts[1:]):
        nan_count += 1
    if abs(vb + vs - vol) > 0.01 * vol:
        vb_vs_mismatch += 1
    
print(f'Signals: {total}')
print(f'Direction: {longs}L / {shorts}S')
print(f'Range: {min_dt} → {max_dt}')
print(f'NaN: {nan_count} ({nan_count/total*100:.1f}%)')
print(f'vb+vs≠vol: {vb_vs_mismatch} ({vb_vs_mismatch/total*100:.1f}%)')
```

## Tolerances

| Check | Pass | Warning | Fail |
|---|---|---|---|
| vb+vs≈vol | <1% | 1-5% | >5% → export bug |
| NaN | 0% | 1-3 signals | >3 → export bug |
| Feature count | All 25 | 1-3 off | Multiple off → export format wrong |
| Date range | Expected window | Minor shift at edges | Wrong period → reschedule |
| Balance | 40-60% per dir | 30-40% or 60-70% | <30% or >70% |

## Historical Records

- **v2 (bambam_delta_24feat_v22.csv):** 431 signals, 7/7 clean, May 23 export
- **v2.2 1-year (bambam_delta_24feat_v22_1year.csv):** 1,850 signals (957L/893S), May 2025–May 2026, 7/7 clean
- **v2 (buggy, doc_b86b):** vb+vs failed for 432/434 signals due to UDF deferred eval — confirmed that pre-compute fix resolves it
- **v1 (90-day, doc_3affc):** Feature 19 (volRatio_delta) systematically biased — used separate window instead of avgVol[5]
