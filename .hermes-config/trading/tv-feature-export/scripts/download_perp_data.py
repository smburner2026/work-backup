#!/usr/bin/env python3
"""
Download BTCUSDT perpetual 5m candles from Binance Futures API.
Each candle includes taker_buy_base_asset_volume (field [9]).

If geo-blocked, try:
  1. Run on local machine (not VPS)
  2. Use VPN/proxy: HTTPS_PROXY=socks5://127.0.0.1:1080 python download_perp_data.py
  3. NordVPN on VPS: nordvpn connect && python download_perp_data.py

Output: CSV with columns:
  open_time, open_time_str, open, high, low, close, volume, close_time,
  quote_volume, trades, taker_buy_base_vol, taker_buy_quote_vol

Key field: taker_buy_base_vol (field [9]) = actual taker buy volume on perps
"""

import requests
import csv
import time
import sys
from datetime import datetime, timezone

SYMBOL = "BTCUSDT"
INTERVAL = "5m"
START_DATE = "2025-10-01"
END_DATE = "2026-05-23"
OUTPUT = "btcusdt_perp_5m.csv"

ENDPOINTS = [
    "https://fapi.binance.com/fapi/v1/klines",
]

def download_klines(base_url, symbol, interval, start_ms, end_ms, limit=1500):
    all_data = []
    current = start_ms
    while current < end_ms:
        params = {
            'symbol': symbol, 'interval': interval,
            'startTime': current, 'endTime': end_ms, 'limit': limit,
        }
        try:
            resp = requests.get(base_url, params=params, timeout=30)
            data = resp.json()
            if isinstance(data, dict) and 'code' in data:
                print(f"API error: {data.get('msg', data)}")
                return None
            if not data:
                break
            all_data.extend(data)
            current = data[-1][0] + 1
            print(f"  Downloaded {len(all_data)} candles, up to {datetime.fromtimestamp(current/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC")
            time.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
            return None
    return all_data

def main():
    start_ms = int(datetime.strptime(START_DATE, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
    end_ms = int(datetime.strptime(END_DATE, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
    for url in ENDPOINTS:
        print(f"Trying {url}...")
        data = download_klines(url, SYMBOL, INTERVAL, start_ms, end_ms)
        if data is None:
            print(f"  Failed, trying next endpoint...")
            continue
        print(f"  Total candles: {len(data)}")
        with open(OUTPUT, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['open_time', 'open_time_str', 'open', 'high', 'low', 'close',
                           'volume', 'close_time', 'quote_volume', 'trades',
                           'taker_buy_base_vol', 'taker_buy_quote_vol'])
            for candle in data:
                writer.writerow([
                    candle[0],
                    datetime.fromtimestamp(candle[0]/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M'),
                    candle[1], candle[2], candle[3], candle[4],
                    candle[5], candle[6], candle[7], candle[8],
                    candle[9], candle[10],
                ])
        print(f"  Saved to {OUTPUT}")
        zero_count = sum(1 for c in data if float(c[9]) == 0)
        print(f"  Zero taker_buy_vol candles: {zero_count}/{len(data)}")
        if zero_count > len(data) * 0.5:
            print("  WARNING: Most taker values are zero — exchange may not provide taker data")
        else:
            print("  Taker data looks good!")
        return OUTPUT
    print("\nAll endpoints failed. Options:")
    print("  1. Run this on your local machine (not VPS)")
    print("  2. Use VPN: HTTPS_PROXY=socks5://127.0.0.1:1080 python download_perp_data.py")
    print("  3. NordVPN on VPS: nordvpn connect && python download_perp_data.py")
    return None

if __name__ == "__main__":
    main()