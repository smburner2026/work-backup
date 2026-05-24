#!/usr/bin/env python3
"""
BAMBAM-FATCAT Backtest Engine
==============================
Fetches Binance historical data and replicates the BAMBAM-FATCAT signal logic
for comparison against TradingView entries.

Usage:
    python backtest_bambam_fatcat.py --symbol BTCUSDT --interval 5m --days 30 --less-ratio 0.03 --vol-mult 1.5

Output:
    - CSV of all signals with metadata
    - Comparison stats (signal count, frequency, distribution)
    - Optional: plot signals on price chart
"""

import requests
import pandas as pd
import numpy as np
import argparse
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time


def fetch_binance_klines(
    symbol: str = "BTCUSDT",
    interval: str = "5m",
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    limit: int = 1000
) -> pd.DataFrame:
    """Fetch historical klines from Binance Futures API."""
    url = "https://fapi.binance.com/fapi/v1/klines"
    
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    if start_time:
        params["startTime"] = start_time
    if end_time:
        params["endTime"] = end_time
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades", "taker_buy_base",
        "taker_buy_quote", "ignore"
    ])
    
    # Convert types
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    for col in ["open", "high", "low", "close", "volume", "taker_buy_base"]:
        df[col] = df[col].astype(float)
    
    df = df.sort_values("open_time").reset_index(drop=True)
    return df


def fetch_large_range(
    symbol: str,
    interval: str,
    days: int = 30
) -> pd.DataFrame:
    """Fetch large date range by paginating through Binance API."""
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    
    all_data = []
    current_start = start_time
    
    # Binance returns max 1000 bars per request
    # 5m interval: 1000 bars = ~3.5 days
    # For 200 days: ~60 requests
    
    interval_ms = {
        "1m": 60 * 1000,
        "5m": 5 * 60 * 1000,
        "15m": 15 * 60 * 1000,
        "1h": 60 * 60 * 1000,
        "4h": 4 * 60 * 60 * 1000,
        "1d": 24 * 60 * 60 * 1000
    }
    
    bar_ms = interval_ms.get(interval, 5 * 60 * 1000)
    max_bars = 1000
    
    print(f"Fetching {days} days of {interval} data for {symbol}...")
    
    while current_start < end_time:
        chunk_end = min(current_start + (max_bars * bar_ms), end_time)
        
        df = fetch_binance_klines(symbol, interval, current_start, chunk_end)
        if len(df) == 0:
            break
            
        all_data.append(df)
        
        # Update start time to after last bar
        last_time = int(df["open_time"].iloc[-1].timestamp() * 1000)
        current_start = last_time + bar_ms
        
        print(f"  Fetched {len(df)} bars up to {df['open_time'].iloc[-1]}")
        time.sleep(0.1)  # Rate limit courtesy
    
    if not all_data:
        return pd.DataFrame()
    
    result = pd.concat(all_data, ignore_index=True)
    result = result.drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)
    print(f"Total bars fetched: {len(result)}")
    return result


def calculate_volume_delta(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate BAMBAM-style volume split.
    vb = volume * (close - low) / (high - low)  — buying volume estimate
    vs = volume * (high - close) / (high - low)  — selling volume estimate
    """
    df = df.copy()
    
    # Avoid division by zero (doji bars)
    range_size = df["high"] - df["low"]
    range_size = range_size.replace(0, np.nan)
    
    df["vb"] = df["volume"] * (df["close"] - df["low"]) / range_size
    df["vs"] = df["volume"] * (df["high"] - df["close"]) / range_size
    
    # Fill NaN (doji) with 0
    df["vb"] = df["vb"].fillna(0)
    df["vs"] = df["vs"].fillna(0)
    
    # Also add taker buy ratio from Binance for comparison
    df["taker_buy_ratio"] = df["taker_buy_base"] / df["volume"]
    
    return df


def generate_signals(
    df: pd.DataFrame,
    lookback: int = 200,
    less_ratio: float = 0.03,
    vol_multiplier: float = 1.5,
    delta_mode: str = "OR",  # "OR" or "AND"
    use_offset: bool = False  # True = signal on extreme bar, False = on confirmation bar
) -> pd.DataFrame:
    """
    Generate BAMBAM-FATCAT signals.
    
    Core logic:
    - ph = high (offset=0) or high.shift(1) (offset=1)
    - top = rolling_max(ph, lookback)
    - btm = rolling_min(ph, lookback)  # or pl for lows
    - Signal when: ph >= top AND volume > avg * multiplier AND delta condition
    """
    df = df.copy()
    
    # Shift for offset logic
    if use_offset:
        # Signal on extreme bar (offset=-1 in TV)
        df["ph"] = df["high"]
        df["pl"] = df["low"]
        df["vd"] = df["vb"] - df["vs"]
        df["vol"] = df["vb"] + df["vs"]
    else:
        # Signal on confirmation bar (default in v8)
        df["ph"] = df["high"].shift(1)
        df["pl"] = df["low"].shift(1)
        df["vd"] = (df["vb"] - df["vs"]).shift(1)
        df["vol"] = (df["vb"] + df["vs"]).shift(1)
    
    # Rolling extremes
    df["top"] = df["ph"].rolling(window=lookback, min_periods=1).max()
    df["btm"] = df["pl"].rolling(window=lookback, min_periods=1).min()
    
    # Volume average
    df["avg_vol"] = df["vol"].rolling(window=lookback, min_periods=1).mean()
    
    # Volume delta ratio
    df["vd_ratio"] = np.abs(df["vd"] / df["vol"])
    df["is_less_ratio"] = df["vd_ratio"] < less_ratio
    
    # High volume condition
    df["high_vol"] = df["vol"] > (df["avg_vol"] * vol_multiplier)
    
    # Delta conditions
    if delta_mode == "OR":
        df["bear_delta"] = df["is_less_ratio"] | (df["vd"] < 0)
        df["bull_delta"] = df["is_less_ratio"] | (df["vd"] > 0)
    else:  # AND
        df["bear_delta"] = df["is_less_ratio"] & (df["vd"] < 0)
        df["bull_delta"] = df["is_less_ratio"] & (df["vd"] > 0)
    
    # Raw signals
    df["bear_raw"] = (df["ph"] >= df["top"]) & df["high_vol"] & df["bear_delta"]
    df["bull_raw"] = (df["pl"] <= df["btm"]) & df["high_vol"] & df["bull_delta"]
    
    # Final signals (shift for confirmation bar logic)
    if use_offset:
        df["bear_signal"] = df["bear_raw"]
        df["bull_signal"] = df["bull_raw"]
    else:
        df["bear_signal"] = df["bear_raw"].shift(-1).fillna(False)
        df["bull_signal"] = df["bull_raw"].shift(-1).fillna(False)
    
    return df


def export_signals(df: pd.DataFrame, output_path: str) -> None:
    """Export signal bars to CSV for comparison."""
    signal_cols = [
        "open_time", "open", "high", "low", "close", "volume",
        "vb", "vs", "vd", "vd_ratio", "top", "btm", "avg_vol",
        "bear_signal", "bull_signal"
    ]
    
    # Filter to signal bars only
    signals = df[df["bear_signal"] | df["bull_signal"]].copy()
    signals["side"] = np.where(signals["bull_signal"], "BUY", 
                      np.where(signals["bear_signal"], "SELL", "NONE"))
    
    signals = signals[signal_cols + ["side"]]
    signals.to_csv(output_path, index=False)
    print(f"Exported {len(signals)} signals to {output_path}")


def analyze_signals(df: pd.DataFrame) -> Dict:
    """Analyze signal characteristics."""
    bull_signals = df[df["bull_signal"]].copy()
    bear_signals = df[df["bear_signal"]].copy()
    
    stats = {
        "total_bars": len(df),
        "bull_signals": len(bull_signals),
        "bear_signals": len(bear_signals),
        "signal_rate": (len(bull_signals) + len(bear_signals)) / len(df) * 100,
        "avg_vd_ratio_bull": bull_signals["vd_ratio"].mean() if len(bull_signals) > 0 else 0,
        "avg_vd_ratio_bear": bear_signals["vd_ratio"].mean() if len(bear_signals) > 0 else 0,
        "avg_vol_mult_bull": (bull_signals["vol"] / bull_signals["avg_vol"]).mean() if len(bull_signals) > 0 else 0,
        "avg_vol_mult_bear": (bear_signals["vol"] / bear_signals["avg_vol"]).mean() if len(bear_signals) > 0 else 0,
    }
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="BAMBAM-FATCAT Backtest Engine")
    parser.add_argument("--symbol", default="BTCUSDT", help="Trading pair (default: BTCUSDT)")
    parser.add_argument("--interval", default="5m", help="Timeframe (default: 5m)")
    parser.add_argument("--days", type=int, default=30, help="Days of history (default: 30)")
    parser.add_argument("--lookback", type=int, default=200, help="Lookback period (default: 200)")
    parser.add_argument("--less-ratio", type=float, default=0.03, help="Less ratio (default: 0.03)")
    parser.add_argument("--vol-mult", type=float, default=1.5, help="Volume multiplier (default: 1.5)")
    parser.add_argument("--delta-mode", choices=["OR", "AND"], default="OR", help="Delta condition mode")
    parser.add_argument("--use-offset", action="store_true", help="Signal on extreme bar (like TV offset=-1)")
    parser.add_argument("--output", default="bambam_signals.csv", help="Output CSV path")
    parser.add_argument("--plot", action="store_true", help="Generate matplotlib plot")
    
    args = parser.parse_args()
    
    # Fetch data
    df = fetch_large_range(args.symbol, args.interval, args.days)
    if len(df) == 0:
        print("No data fetched. Exiting.")
        return
    
    # Calculate volume delta
    df = calculate_volume_delta(df)
    
    # Generate signals
    df = generate_signals(
        df,
        lookback=args.lookback,
        less_ratio=args.less_ratio,
        vol_multiplier=args.vol_mult,
        delta_mode=args.delta_mode,
        use_offset=args.use_offset
    )
    
    # Analyze
    stats = analyze_signals(df)
    
    print("\n" + "="*60)
    print("BAMBAM-FATCAT BACKTEST RESULTS")
    print("="*60)
    print(f"Symbol:        {args.symbol}")
    print(f"Interval:      {args.interval}")
    print(f"Total Bars:    {stats['total_bars']:,}")
    print(f"Bull Signals:  {stats['bull_signals']}")
    print(f"Bear Signals:  {stats['bear_signals']}")
    print(f"Signal Rate:   {stats['signal_rate']:.2f}%")
    print(f"Avg VD Ratio (Bull): {stats['avg_vd_ratio_bull']:.4f}")
    print(f"Avg VD Ratio (Bear): {stats['avg_vd_ratio_bear']:.4f}")
    print(f"Avg Vol Mult (Bull): {stats['avg_vol_mult_bull']:.2f}x")
    print(f"Avg Vol Mult (Bear): {stats['avg_vol_mult_bear']:.2f}x")
    print("="*60)
    
    # Export
    export_signals(df, args.output)
    
    # Optional plot
    if args.plot:
        try:
            import matplotlib.pyplot as plt
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), gridspec_kw={"height_ratios": [3, 1]})
            
            # Price
            ax1.plot(df["open_time"], df["close"], label="Close", alpha=0.7)
            
            # Signals
            bull_pts = df[df["bull_signal"]]
            bear_pts = df[df["bear_signal"]]
            
            ax1.scatter(bull_pts["open_time"], bull_pts["low"] * 0.995, 
                       color="green", marker="^", s=100, label=f"BUY ({len(bull_pts)})", zorder=5)
            ax1.scatter(bear_pts["open_time"], bear_pts["high"] * 1.005,
                       color="red", marker="v", s=100, label=f"SELL ({len(bear_pts)})", zorder=5)
            
            ax1.set_title(f"BAMBAM-FATCAT Signals — {args.symbol} {args.interval}")
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Volume
            ax2.bar(df["open_time"], df["volume"], alpha=0.5, color="gray")
            ax2.set_ylabel("Volume")
            
            plt.tight_layout()
            plt.savefig("bambam_signals.png", dpi=150)
            print("Plot saved to bambam_signals.png")
        except ImportError:
            print("matplotlib not installed. Install with: pip install matplotlib")


if __name__ == "__main__":
    main()
