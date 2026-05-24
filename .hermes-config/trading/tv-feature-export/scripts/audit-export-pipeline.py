#!/usr/bin/env python3
"""
EXPORT DATA INTEGRITY AUDIT — Generic version.
Point at any TV Strategy Tester CSV export + optional price data CSV.
Runs 6-layer audit and reports pass/fail/warning for each check.

Usage:
    python3 audit-export-pipeline.py <export.csv> [perp_5m.csv]

Example:
    python3 audit-export-pipeline.py data/exports/newpair_24feat.csv data/perp_5m.csv
"""
import csv, sys, os
from datetime import datetime, timezone, timedelta

PASS = 0; FAIL = 0; WARN = 0

def check(name, cond, detail=""):
    global PASS, FAIL, WARN
    if cond:
        PASS += 1; print(f"  ✓ {name}")
    else:
        FAIL += 1; print(f"  ✗ {name}  ← {detail}")

def warn(name, detail=""):
    global WARN, WARN
    WARN += 1; print(f"  ⚠ {name}  ← {detail}")

def load_csv(path):
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def parse_ts(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)

# === CONFIG ===
export_path = sys.argv[1] if len(sys.argv) > 1 else None
perp_path = sys.argv[2] if len(sys.argv) > 2 else None

if not export_path:
    print("Usage: python3 audit-export-pipeline.py <export.csv> [perp_5m.csv]")
    sys.exit(1)

print(f"\n{'='*60}")
print(f"DATA INTEGRITY AUDIT")
print(f"Export: {export_path}")
print(f"{'='*60}")

# ===== LAYER 1: Raw CSV format =====
print(f"\n{'─'*60}\nLAYER 1: RAW CSV FORMAT\n{'─'*60}")

rows = load_csv(export_path)
entries = [r for r in rows if 'Entry' in r.get('Type', '')]
check(f"Entry rows present (found {len(entries)})", len(entries) > 0)

keys = [(r['Date and time'], r['Price USDT']) for r in entries]
check("No duplicate (time,price)", len(keys) == len(entries))

# Detect format and check parsing
sample = entries[0]['Signal'] if entries else ""
parts = sample.split('|')
is_raw_float = False
is_direction_float = False
is_key_value = False

if len(parts) == 1 and parts[0] in ('BEAR', 'BULL'):
    check("Format: Raw capture (direction only)", True)
elif all(_is_float(p) for p in parts):
    feat_count = len(parts)
    check(f"Format: {feat_count} raw pipe-delimited floats", True)
    is_raw_float = True
elif parts[0] in ('BEAR', 'BULL') and len(parts) > 1 and all(_is_float(p) for p in parts[1:]):
    feat_count = len(parts) - 1
    check(f"Format: Direction prefix + {feat_count} floats", True)
    is_direction_float = True
elif '=' in parts[1]:
    warn("Format appears to be KEY=VALUE — analysis scripts expect raw floats!")
    is_key_value = True
else:
    warn(f"Unknown format. First part: {parts[0]}, count: {len(parts)}")

# Check for NaN/null floats
null_count = 0
for r in entries:
    signal_parts = r['Signal'].split('|')
    start = 1 if signal_parts[0] in ('BEAR', 'BULL') and not _is_float(signal_parts[0]) else 0
    for p in signal_parts[start:]:
        if '=' in p: continue  # skip KEY=VALUE
        try:
            float(p)
        except ValueError:
            null_count += 1
check("No NaN/null float values", null_count == 0, f"{null_count} bad values")

# Count directions
if is_direction_float:
    shorts = sum(1 for r in entries if r['Signal'].startswith('BEAR'))
    longs = len(entries) - shorts
    check("Both directions present", shorts > 0 and longs > 0, f"S={shorts} L={longs}")

# ===== LAYER 2: Timestamp alignment =====
if perp_path and os.path.exists(perp_path):
    print(f"\n{'─'*60}\nLAYER 2: TIMESTAMP ALIGNMENT\n{'─'*60}")

    perp_rows = load_csv(perp_path)
    perp_times = set()
    for r in perp_rows:
        ts = r.get('open_time_str', r.get('Date and time', ''))
        try:
            perp_times.add(parse_ts(ts))
        except:
            pass

    check(f"Perp data loaded ({len(perp_times)} timestamps)", len(perp_times) > 0)

    signal_times = set()
    for r in entries:
        try:
            signal_times.add(parse_ts(r['Date and time']))
        except:
            pass

    matched_exact = sum(1 for st in signal_times if st in perp_times)
    matched_offset = sum(1 for st in signal_times if st not in perp_times and 
                         ((st - timedelta(minutes=5)) in perp_times or 
                          (st + timedelta(minutes=5)) in perp_times))
    unmatched = len(signal_times) - matched_exact - matched_offset
    
    check("All signal times match a perp candle (±5min)", unmatched == 0, f"{unmatched} unmatched")
    check(f"Exact match rate > 50%", matched_exact > len(signal_times) * 0.5,
          f"{matched_exact}/{len(signal_times)}")

    # Time range
    perp_min = min(perp_times); perp_max = max(perp_times)
    sig_min = min(signal_times); sig_max = max(signal_times)
    check("Perp data covers signal range", perp_min <= sig_min and perp_max >= sig_max,
          f"Sig: {sig_min} to {sig_max}\n  Perp: {perp_min} to {perp_max}")
else:
    print(f"\n{'─'*60}\nLAYER 2: TIMESTAMP ALIGNMENT (skipped — no perp data)\n{'─'*60}")
    warn("No perp data provided — timestamp alignment not checked")

# ===== LAYER 3: Feature math =====
print(f"\n{'─'*60}\nLAYER 3: FEATURE MATH CONSISTENCY\n{'─'*60}")

# Only check if we have a known feature layout
if is_raw_float and len(parts) >= 7:
    # Try to recompute volRatio from vol and avgVol if 7+ features
    feats = []
    for r in entries:
        p = r['Signal'].split('|')
        if len(p) >= 7:
            feats.append((float(p[0]), float(p[1]), float(p[2]), float(p[3]), float(p[4]), float(p[5]), float(p[6])))
    
    vr_errors = sum(1 for v, vd, av, vr, vdr, vb, vs in feats if av > 0 and abs(vr - v/av) > 0.01 * v/av)
    vdr_errors = sum(1 for v, vd, av, vr, vdr, vb, vs in feats if v > 0 and abs(vdr - abs(vd)/v) > 0.001)
    vs_check = sum(1 for v, vd, av, vr, vdr, vb, vs in feats if abs(vb + vs - v) > 0.01 * abs(v))
    
    check(f"volRatio ≈ vol/avgVol ({100-vr_errors/len(feats)*100:.0f}% OK)", 
          vr_errors / len(feats) < 0.1, f"{vr_errors} errors")
    check(f"vdRatio ≈ |vd|/vol", vdr_errors == 0, f"{vdr_errors} errors")
    check(f"vb + vs ≈ vol", vs_check == 0, f"{vs_check} errors")

elif is_direction_float and len(parts) >= 8:
    # Direction prefix + 7+ body features
    feats = []
    for r in entries:
        p = r['Signal'].split('|')
        if len(p) >= 8:
            feats.append((float(p[1]), float(p[2]), float(p[3]), float(p[4]), float(p[5]), float(p[6]), float(p[7])))
    
    vr_errors = sum(1 for v, vd, av, vr, vdr, vb, vs in feats if av > 0 and abs(vr - v/av) > 0.01 * v/av)
    vdr_errors = sum(1 for v, vd, av, vr, vdr, vb, vs in feats if v > 0 and abs(vdr - abs(vd)/v) > 0.001)
    
    check(f"volRatio ≈ vol/avgVol ({100-vr_errors/len(feats)*100:.0f}% OK)", 
          vr_errors / len(feats) < 0.1, f"{vr_errors} errors")
    check("vdRatio ≈ |vd|/vol", vdr_errors == 0, f"{vdr_errors} errors")
    
    # Check cross flags (last 4 features) are binary
    if len(parts) >= 25:
        cross_flags = []
        for r in entries:
            p = r['Signal'].split('|')
            if len(p) >= 25:
                cross_flags.extend([int(float(p[i])) for i in range(21, 25)])
        non_binary = sum(1 for f in cross_flags if f not in (0, 1))
        check(f"Cross flags are binary (0 or 1): {len(cross_flags)} checks", 
              non_binary == 0, f"{non_binary} non-binary")

else:
    warn("No feature math checks — unsupported format")

# ===== LAYER 4: Price data integrity =====
if perp_path and os.path.exists(perp_path):
    print(f"\n{'─'*60}\nLAYER 4: PRICE DATA INTEGRITY\n{'─'*60}")

    parsed = []
    for r in perp_rows:
        ts = r.get('open_time_str', r.get('Date and time', ''))
        try:
            dt = parse_ts(ts)
            close = float(r['close'] if 'close' in r else r.get('Close', 0))
            vol = float(r['volume'] if 'volume' in r else r.get('Volume', 0))
            tbv = float(r.get('taker_buy_base_vol', r.get('taker_buy_volume', 0)))
            parsed.append({'dt': dt, 'close': close, 'volume': vol, 'tbv': tbv})
        except:
            pass

    check("Sorted by time", all(parsed[i]['dt'] <= parsed[i+1]['dt'] for i in range(len(parsed)-1)))
    
    dts = [p['dt'] for p in parsed]
    check("No duplicate timestamps", len(dts) == len(set(dts)))
    
    gaps = [(parsed[i-1]['dt'], parsed[i]['dt'], (parsed[i]['dt']-parsed[i-1]['dt']).total_seconds())
            for i in range(1, len(parsed)) if (parsed[i]['dt']-parsed[i-1]['dt']).total_seconds() != 300]
    
    if gaps:
        warn(f"{len(gaps)} gaps in price data")
        for g in gaps[:3]:
            warn(f"  {g[0]} → {g[1]} ({g[2]/60:.0f}min gap)")
    else:
        check("No gaps (all 5m intervals)", True)
    
    prices = [p['close'] for p in parsed]
    check("Prices in sane range (>$100, <$1M)", 
          all(100 < p < 1000000 for p in prices))
    check("Volumes non-negative", all(p['volume'] >= 0 for p in parsed))
    
    taker_ok = sum(1 for p in parsed if p['tbv'] > p['volume'] * 1.01)
    check("Taker buy ≤ volume (within 1%)", taker_ok == 0, f"{taker_ok} violations")
    
    # Detect spot vs perp
    volumes = sorted([p['volume'] for p in parsed])
    p99 = volumes[int(len(volumes)*0.99)]
    if p99 < 10:
        print(f"  ℹ Volume distribution suggests SPOT data (99th pctl={p99:.2f} BTC)")
    elif p99 > 100:
        print(f"  ℹ Volume distribution suggests PERP data (99th pctl={p99:.2f} BTC)")
    else:
        print(f"  ℹ Volume distribution: 99th pctl={p99:.2f} BTC — indeterminate")

else:
    print(f"\n{'─'*60}\nLAYER 4: PRICE DATA INTEGRITY (skipped)\n{'─'*60}")

# ===== SUMMARY =====
print(f"\n{'='*60}")
print(f"AUDIT SUMMARY")
print(f"{'='*60}")
print(f"  Passed: {PASS}")
print(f"  Failed: {FAIL}")
print(f"  Warnings: {WARN}")
print(f"  Verdict: {'✓ OK' if FAIL == 0 else '✗ HAS ISSUES — review failures above'}")
print()

def _is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    pass
