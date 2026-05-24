#!/usr/bin/env python3
"""
BAMBAM-FATCAT Backtest Engine — Parameter Sweep Tool
Fetches exchange OHLCV and replicates Pine Script signal logic in pandas.
Supports Binance (primary) and Bitstamp (fallback when Binance is blocked).

Usage:
    python backtest_engine.py --symbol BTCUSDT --interval 5m --days 30 \
        --less-ratio 0.03 --vol-mult 1.5 --delta-mode OR --plot

Outputs:
    - bambam_signals.csv (signal bars with metadata for comparison)
    - Console stats (signal count, avg vd_ratio, avg vol_mult)
    - Optional bambam_signals.png overlay chart
"""

import requests, pandas as pd, numpy as np, argparse
from datetime import datetime, timedelta
import time


def fetch_data(source="binance", symbol="BTCUSDT", interval="5m", days=30):
    """Paginate through exchange API for arbitrary date range.
    Supports 'binance' and 'bitstamp' sources.
    Bitstamp is the fallback when Binance returns HTTP 451 (blocked location).
    """
    bar_ms = {"1m": 60_000, "5m": 300_000, "15m": 900_000,
              "1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000}.get(interval, 300_000)
    chunks = []
    end_ts = int(datetime.now().timestamp())
    start_ts = int((datetime.now() - timedelta(days=days)).timestamp())

    if source == "binance":
        url = "https://fapi.binance.com/fapi/v1/klines"
        cur = start_ts * 1000
        end = end_ts * 1000
        while cur < end:
            r = requests.get(url, params={"symbol": symbol.replace("-", ""), "interval": interval,
                                          "startTime": cur, "endTime": min(cur + 999 * bar_ms, end), "limit": 1000})
            if r.status_code == 451:
                print("⚠️  Binance blocked (HTTP 451). Falling back to Bitstamp...")
                print("   Bitstamp has NO taker_buy_base field — volume-source analysis unavailable.")
                print("   For taker_buy data, use data.binance.vision S3 bucket instead.")
                return fetch_data("bitstamp", symbol, interval, days)
            r.raise_for_status()
            df = pd.DataFrame(r.json(), columns=[
                "open_time", "open", "high", "low", "close", "volume",
                "close_time", "quote_volume", "trades", "taker_buy_base",
                "taker_buy_quote", "ignore"])
            df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
            for c in ["open", "high", "low", "close", "volume", "taker_buy_base"]:
                df[c] = df[c].astype(float)
            if len(df) == 0:
                break
            chunks.append(df)
            cur = int(df["open_time"].iloc[-1].timestamp() * 1000) + bar_ms
            time.sleep(0.1)

    elif source == "bitstamp":
        url = "https://www.bitstamp.net/api/v2/ohlc/btcusd/"
        step_map = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600}
        step = step_map.get(interval, 300)
        cur = end_ts
        while cur > start_ts:
            r = requests.get(url, params={"step": step, "limit": 1000, "end": cur})
            r.raise_for_status()
            data = r.json().get("data", {}).get("ohlc", [])
            if not data:
                break
            df = pd.DataFrame(data)
            df = df.rename(columns={"timestamp": "open_time"})
            df["open_time"] = pd.to_datetime(df["open_time"].astype(int), unit="s")
            for c in ["open", "high", "low", "close", "volume"]:
                df[c] = df[c].astype(float)
            chunks.append(df)
            oldest = int(df["open_time"].iloc[0].timestamp()) - 1
            if oldest < start_ts:
                break
            cur = oldest
            time.sleep(0.3)

        if not chunks:
            raise RuntimeError("No data fetched from Bitstamp")
        result = pd.concat(chunks, ignore_index=True)
        result = result.drop_duplicates("open_time").sort_values("open_time").reset_index(drop=True)
        print(f"Fetched {len(result)} bars from Bitstamp")
        return result

    result = pd.concat(chunks, ignore_index=True).drop_duplicates("open_time").sort_values("open_time")
    print(f"Fetched {len(result)} bars from {source}")
    return result


def generate_signals(df, lookback=200, less_ratio=0.03, vol_mult=1.5,
                     delta_mode="OR", use_offset=False):
    """Replicate BAMBAM-FATCAT signal logic in pandas."""
    df = df.copy()
    rng = (df["high"] - df["low"]).replace(0, np.nan)
    df["vb"] = df["volume"] * (df["close"] - df["low"]) / rng
    df["vs"] = df["volume"] * (df["high"] - df["close"]) / rng
    df["vb"] = df["vb"].fillna(0)
    df["vs"] = df["vs"].fillna(0)

    ph = df["high"] if use_offset else df["high"].shift(1)
    pl = df["low"] if use_offset else df["low"].shift(1)
    vd = (df["vb"] - df["vs"]) if use_offset else (df["vb"] - df["vs"]).shift(1)
    vol = (df["vb"] + df["vs"]) if use_offset else (df["vb"] + df["vs"]).shift(1)

    top = ph.rolling(lookback, min_periods=1).max()
    btm = pl.rolling(lookback, min_periods=1).min()
    avg_vol = vol.rolling(lookback, min_periods=1).mean()
    vd_ratio = vd.abs() / vol
    is_less = vd_ratio < less_ratio
    high_vol = vol > avg_vol * vol_mult

    if delta_mode == "OR":
        bear_delta = is_less | (vd < 0)
        bull_delta = is_less | (vd > 0)
    else:
        bear_delta = is_less & (vd < 0)
        bull_delta = is_less & (vd > 0)

    bear_raw = (ph >= top) & high_vol & bear_delta
    bull_raw = (pl <= btm) & high_vol & bull_delta

    df["bear_signal"] = bear_raw if use_offset else bear_raw.shift(-1).fillna(False)
    df["bull_signal"] = bull_raw if use_offset else bull_raw.shift(-1).fillna(False)
    df["vd_ratio"] = vd_ratio
    df["top"] = top
    df["btm"] = btm
    return df


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="binance", choices=["binance", "bitstamp"])
    p.add_argument("--symbol", default="BTCUSDT")
    p.add_argument("--interval", default="5m")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--lookback", type=int, default=200)
    p.add_argument("--less-ratio", type=float, default=0.03)
    p.add_argument("--vol-mult", type=float, default=1.5)
    p.add_argument("--delta-mode", choices=["OR", "AND"], default="OR")
    p.add_argument("--use-offset", action="store_true")
    p.add_argument("--output", default="bambam_signals.csv")
    p.add_argument("--plot", action="store_true")
    args = p.parse_args()

    df = fetch_data(args.source, args.symbol, args.interval, args.days)
    df = generate_signals(df, args.lookback, args.less_ratio, args.vol_mult,
                          args.delta_mode, args.use_offset)

    bulls = df[df["bull_signal"]]
    bears = df[df["bear_signal"]]
    print(f"\nBULL: {len(bulls)} | BEAR: {len(bears)} | Rate: {(len(bulls)+len(bears))/len(df)*100:.2f}%")
    print(f"Avg VD Ratio (bull): {bulls['vd_ratio'].mean():.4f}" if len(bulls) else "N/A")
    print(f"Avg VD Ratio (bear): {bears['vd_ratio'].mean():.4f}" if len(bears) else "N/A")

    signals = df[df["bear_signal"] | df["bull_signal"]].copy()
    signals["side"] = np.where(signals["bull_signal"], "BUY", "SELL")
    signals[["open_time", "open", "high", "low", "close", "volume",
             "vd_ratio", "top", "btm", "side"]].to_csv(args.output, index=False)
    print(f"Exported {len(signals)} signals to {args.output}")

    if args.plot:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.plot(df["open_time"], df["close"], alpha=0.7)
        ax.scatter(bulls["open_time"], bulls["low"] * 0.995, c="green", marker="^", s=80, zorder=5)
        ax.scatter(bears["open_time"], bears["high"] * 1.005, c="red", marker="v", s=80, zorder=5)
        ax.set_title(f"{args.symbol} {args.interval} — {args.less_ratio}/{args.vol_mult}/{args.delta_mode}")
        plt.tight_layout()
        plt.savefig("bambam_signals.png", dpi=150)
        print("Plot saved to bambam_signals.png")


if __name__ == "__main__":
    main()
