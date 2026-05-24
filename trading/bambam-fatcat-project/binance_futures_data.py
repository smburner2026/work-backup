#!/usr/bin/env python3
"""
BINANCE FUTURES COMPREHENSIVE DATA PULL
Downloads ALL available market data for a given symbol.

Output structure:
  data/binance_futures/{symbol}/
    klines_5m.csv                  — OHLCV + taker buy volume
    open_interest_5m.csv           — Open Interest history
    taker_ratio_5m.csv             — Taker buy/sell volume ratio
    top_trader_account_5m.csv      — Top Trader Long/Short Account Ratio
    top_trader_position_5m.csv     — Top Trader Long/Short Position Ratio
    global_long_short_5m.csv       — All traders Long/Short Account Ratio
    funding_8h.csv                 — Funding rate history
    merged_5m.csv                  — ALL 5m data merged by timestamp (single file)

USAGE:
  python binance_futures_data.py [symbol=BTCUSDT] [start=2025-10-01] [end=2026-05-23]

NOTE: Run on your LOCAL machine (not VPS) — VPS is geo-blocked from Binance Futures.
Then: scp -r data/binance_futures/ root@<vps>:/root/work/trading/bambam-fatcat-project/data/
"""

import requests
import csv
import time
import sys
import os
from datetime import datetime, timezone

# ============================================================
# CONFIG
# ============================================================
BASE_URL = "https://fapi.binance.com"
SYMBOL = "BTCUSDT"
START_DATE = "2025-05-01"
END_DATE = "2026-05-23"
INTERVAL_5M = "5m"
REQUEST_DELAY = 0.15  # seconds between requests

def ts_ms(dt_str):
    dt = datetime.strptime(dt_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)

def fetch_paginated(url, params, limit=500, max_lookback_days=None):
    """Fetch a paginated endpoint with time-based pagination.
    Handles both klines (list-of-lists) and object-array endpoints.
    
    If max_lookback_days is set (e.g. 30 for OI/taker endpoints that Binance
    truncates), retries with only the last N days when full range fails."""
    all_data = []
    current_start = params.get('startTime', 0)
    end_time = params.get('endTime', 0)
    stall_count = 0
    
    while current_start < end_time:
        p = params.copy()
        p['startTime'] = current_start
        p['limit'] = limit
        
        try:
            resp = requests.get(url, params=p, timeout=30)
            data = resp.json()
            if isinstance(data, dict) and 'code' in data:
                if max_lookback_days and ('startTime' in str(data.get('msg', '')) or 'invalid' in str(data.get('msg', ''))):
                    lookback_ms = max_lookback_days * 86400 * 1000
                    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
                    truncated_start = now_ms - lookback_ms
                    if truncated_start > current_start:
                        print(f"    Full range rejected (lookback >{max_lookback_days}d). "
                              f"Retrying with last {max_lookback_days}d...")
                        p['startTime'] = truncated_start
                        current_start = truncated_start
                        resp = requests.get(url, params=p, timeout=30)
                        data = resp.json()
                        if isinstance(data, dict) and 'code' in data:
                            print(f"  API error (retry): {data.get('msg', data)}")
                            break
                    else:
                        print(f"  API error: {data.get('msg', data)}")
                        break
                else:
                    print(f"  API error: {data.get('msg', data)}")
                    break
            if not data:
                break
            
            all_data.extend(data)
            
            # Paginate: advance startTime past last item
            last = data[-1]
            if isinstance(last, dict):
                last_ts = last.get('timestamp') or last.get('openTime') or last.get('fundingTime')
            else:
                last_ts = last[0]  # klines format
            
            if last_ts and last_ts > current_start:
                current_start = last_ts + 1
                stall_count = 0
            elif last_ts and last_ts == current_start:
                # Same timestamp = clustering, advance 1ms and retry
                stall_count += 1
                if stall_count > 3:
                    print(f"  Stalled after {stall_count} retries, breaking")
                    break
                current_start = last_ts + 1
                time.sleep(REQUEST_DELAY)
                continue
            else:
                break
            
            pct = (current_start - params.get('startTime', 0)) / (end_time - params.get('startTime', 0)) * 100
            print(f"    {len(all_data)} records ({pct:.0f}%)", end='\r')
            time.sleep(REQUEST_DELAY)
            
        except Exception as e:
            print(f"\n  Error: {e}")
            time.sleep(2)
    
    print()
    return all_data

# ============================================================
# DATA PULLS
# ============================================================

def pull_klines():
    print("  Pulling klines (5m)...")
    url = f"{BASE_URL}/fapi/v1/klines"
    data = fetch_paginated(url, {'symbol': SYMBOL, 'interval': INTERVAL_5M,
                                  'startTime': start_ms, 'endTime': end_ms}, limit=1500)
    rows = []
    for k in data:
        rows.append({
            'open_time': int(k[0]), 'open_time_str': datetime.fromtimestamp(k[0]/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M'),
            'open': float(k[1]), 'high': float(k[2]), 'low': float(k[3]), 'close': float(k[4]),
            'volume': float(k[5]), 'close_time': int(k[6]), 'quote_volume': float(k[7]),
            'trades': int(k[8]), 'taker_buy_base_vol': float(k[9]), 'taker_buy_quote_vol': float(k[10]),
        })
    return rows

def pull_open_interest():
    print("  Pulling open interest (5m)...")
    data = fetch_paginated(f"{BASE_URL}/futures/data/openInterestHist",
                            {'symbol': SYMBOL, 'period': INTERVAL_5M,
                             'startTime': start_ms, 'endTime': end_ms}, max_lookback_days=30)
    return [{'timestamp': int(d['timestamp']),
             'time_str': datetime.fromtimestamp(d['timestamp']/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M'),
             'oi_base': float(d['sumOpenInterest']),
             'oi_usd': float(d['sumOpenInterestValue'])} for d in data]

def pull_taker_ratio():
    print("  Pulling taker long/short ratio (5m)...")
    data = fetch_paginated(f"{BASE_URL}/futures/data/takerlongshortRatio",
                            {'symbol': SYMBOL, 'period': INTERVAL_5M,
                             'startTime': start_ms, 'endTime': end_ms}, max_lookback_days=30)
    return [{'timestamp': int(d['timestamp']),
             'time_str': datetime.fromtimestamp(d['timestamp']/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M'),
             'buy_vol': float(d['buyVol']), 'sell_vol': float(d['sellVol']),
             'ratio': float(d['buySellRatio'])} for d in data]

def pull_top_account():
    print("  Pulling top trader account ratio (5m)...")
    data = fetch_paginated(f"{BASE_URL}/futures/data/topLongShortAccountRatio",
                            {'symbol': SYMBOL, 'period': INTERVAL_5M,
                             'startTime': start_ms, 'endTime': end_ms}, max_lookback_days=30)
    return [{'timestamp': int(d['timestamp']),
             'time_str': datetime.fromtimestamp(d['timestamp']/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M'),
             'long_acct': float(d['longAccount']), 'short_acct': float(d['shortAccount']),
             'ratio': float(d['longShortRatio'])} for d in data]

def pull_top_position():
    print("  Pulling top trader position ratio (5m)...")
    data = fetch_paginated(f"{BASE_URL}/futures/data/topLongShortPositionRatio",
                            {'symbol': SYMBOL, 'period': INTERVAL_5M,
                             'startTime': start_ms, 'endTime': end_ms}, max_lookback_days=30)
    if data:
        print(f"    First record keys: {list(data[0].keys())}")
    return [{'timestamp': int(d['timestamp']),
             'time_str': datetime.fromtimestamp(d['timestamp']/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M'),
             'long_pos': float(d.get('longPosition', d.get('longAccount', 0))),
             'short_pos': float(d.get('shortPosition', d.get('shortAccount', 0))),
             'ratio': float(d['longShortRatio'])} for d in data]

def pull_global_ratio():
    print("  Pulling global long/short ratio (5m)...")
    data = fetch_paginated(f"{BASE_URL}/futures/data/globalLongShortAccountRatio",
                            {'symbol': SYMBOL, 'period': INTERVAL_5M,
                             'startTime': start_ms, 'endTime': end_ms}, max_lookback_days=30)
    return [{'timestamp': int(d['timestamp']),
             'time_str': datetime.fromtimestamp(d['timestamp']/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M'),
             'long_pct': float(d['longAccount']), 'short_pct': float(d['shortAccount']),
             'ratio': float(d['longShortRatio'])} for d in data]

def pull_premium_klines():
    """Pull premium index klines (perp - index premium/discount).
    The 'close' value is the premium/discount in decimal form.
    basis_bps = close * 10000 to get basis points."""
    print("  Pulling premium index klines (5m)...")
    data = fetch_paginated(f"{BASE_URL}/fapi/v1/premiumIndexKlines",
                            {'symbol': SYMBOL, 'interval': INTERVAL_5M,
                             'startTime': start_ms, 'endTime': end_ms}, limit=1500)
    rows = []
    for k in data:
        rows.append({
            'open_time': int(k[0]), 'open_time_str': datetime.fromtimestamp(k[0]/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M'),
            'open': float(k[1]), 'high': float(k[2]), 'low': float(k[3]), 'close': float(k[4]),
            'volume': float(k[5]), 'close_time': int(k[6]), 'quote_volume': float(k[7]),
            'trades': int(k[8]), 'taker_buy_base_vol': float(k[9]), 'taker_buy_quote_vol': float(k[10]),
        })
    return rows

def pull_funding():
    print("  Pulling funding rate history...")
    data = fetch_paginated(f"{BASE_URL}/fapi/v1/fundingRate",
                            {'symbol': SYMBOL, 'startTime': start_ms, 'endTime': end_ms})
    return [{'funding_time': int(d['fundingTime']),
             'time_str': datetime.fromtimestamp(d['fundingTime']/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M'),
             'rate': float(d['fundingRate'])} for d in data]

def write_csv(path, fieldnames, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(rows)
    print(f"  → {len(rows)} rows → {os.path.relpath(path)}")

def merge_5m(klines, oi, taker, top_acct, top_pos, global_ratio, premium=None):
    """Align all 5m-indexed datasets by timestamp and merge."""
    def idx(rows):
        return {round(r['timestamp'] / 300000) * 300000: r for r in rows}
    
    oi_i, taker_i = idx(oi), idx(taker)
    ta_i, tp_i = idx(top_acct), idx(top_pos)
    gl_i = idx(global_ratio)
    prem_i = {round(r['open_time'] / 300000) * 300000: r for r in premium} if premium else {}
    
    merged = []
    for k in sorted(klines, key=lambda x: x['open_time']):
        ot = k['open_time']
        o = oi_i.get(ot, {})
        t = taker_i.get(ot, {})
        ta = ta_i.get(ot, {})
        tp = tp_i.get(ot, {})
        g = gl_i.get(ot, {})
        p = prem_i.get(ot, {})
        basis_bps = round(p.get('close', '') * 10000, 2) if p.get('close', '') != '' else ''
        
        merged.append({
            'time_str': k['open_time_str'],
            'open': k['open'], 'high': k['high'], 'low': k['low'], 'close': k['close'],
            'volume': k['volume'], 'quote_volume': k['quote_volume'], 'trades': k['trades'],
            'taker_buy_base_vol': k['taker_buy_base_vol'],
            'oi_base': o.get('oi_base', ''), 'oi_usd': o.get('oi_usd', ''),
            'taker_buy_vol': t.get('buy_vol', ''), 'taker_sell_vol': t.get('sell_vol', ''),
            'top_long_acct': ta.get('long_acct', ''), 'top_short_acct': ta.get('short_acct', ''),
            'top_long_pos': tp.get('long_pos', ''), 'top_short_pos': tp.get('short_pos', ''),
            'global_long_pct': g.get('long_pct', ''), 'global_short_pct': g.get('short_pct', ''),
            'basis_bps': basis_bps,
        })
    return merged

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        if '=' in arg:
            k, v = arg.split('=', 1)
            if k == 'symbol': SYMBOL = v
            elif k == 'start': START_DATE = v
            elif k == 'end': END_DATE = v
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(script_dir, 'data', 'binance_futures', SYMBOL)
    start_ms, end_ms = ts_ms(START_DATE), ts_ms(END_DATE)
    
    print(f"\nBinance Futures Data Pull: {SYMBOL}  {START_DATE} → {END_DATE}\n")
    
    klines = pull_klines()
    write_csv(f"{out}/klines_5m.csv",
              ['open_time','open_time_str','open','high','low','close','volume','close_time',
               'quote_volume','trades','taker_buy_base_vol','taker_buy_quote_vol'], klines)
    
    oi = pull_open_interest()
    write_csv(f"{out}/open_interest_5m.csv",
              ['timestamp','time_str','oi_base','oi_usd'], oi)
    
    taker = pull_taker_ratio()
    write_csv(f"{out}/taker_ratio_5m.csv",
              ['timestamp','time_str','buy_vol','sell_vol','ratio'], taker)
    
    top_acct = pull_top_account()
    write_csv(f"{out}/top_trader_account_5m.csv",
              ['timestamp','time_str','long_acct','short_acct','ratio'], top_acct)
    
    top_pos = pull_top_position()
    write_csv(f"{out}/top_trader_position_5m.csv",
              ['timestamp','time_str','long_pos','short_pos','ratio'], top_pos)
    
    global_ratio = pull_global_ratio()
    write_csv(f"{out}/global_long_short_5m.csv",
              ['timestamp','time_str','long_pct','short_pct','ratio'], global_ratio)
    
    premium = pull_premium_klines()
    outfile = f"{out}/premium_index_5m.csv"
    write_csv(outfile,
              ['open_time','open_time_str','open','high','low','close','volume','close_time',
               'quote_volume','trades','taker_buy_base_vol','taker_buy_quote_vol'], premium)
    print(f"  → basis_bps = premium_index_close × 10,000")
    
    funding = pull_funding()
    write_csv(f"{out}/funding_8h.csv",
              ['funding_time','time_str','rate'], funding)
    
    merged = merge_5m(klines, oi, taker, top_acct, top_pos, global_ratio, premium)
    write_csv(f"{out}/merged_5m.csv",
              ['time_str','open','high','low','close','volume','quote_volume','trades',
               'taker_buy_base_vol','oi_base','oi_usd','taker_buy_vol','taker_sell_vol',
               'top_long_acct','top_short_acct','top_long_pos','top_short_pos',
               'global_long_pct','global_short_pct','basis_bps'], merged)
    
    print(f"\nDone. Output: {out}")
    print(f"scp -r {out} root@<vps>:/root/work/trading/bambam-fatcat-project/data/binance_futures/")
