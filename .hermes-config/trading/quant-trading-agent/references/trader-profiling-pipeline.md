# Trader Profiling Pipeline

Extract trading systems from YouTube/tweet content of successful traders, structure them by market regime, backtest, and convert to deployable indicators.

## Source Material

The Model Trader repo (github.com/tonbistudio/model-trader, MIT) provides the ingestion template. Their approach: yt-dlp → transcript → Claude extraction → gates. This pipeline extends it for multi-trader, multi-regime extraction.

## Traders Being Profiled

1. Trader XO
2. Husky XBT
3. doc XBT
4. Trader Magus
5. Crypto Chase
6. Trader Mercury
7. Pierre

Sources per trader: YouTube videos (yt-dlp), X/Twitter tweets, any available trading material.

## Extraction Prompt Structure

Modified from Model Trader's `pipeline/extract_strategy.py` two-pass approach:

**Pass 1 → Strategy profile (structured):**
Regime-tagged extraction prompt — for each setup the trader describes, tag it with:
- Timeframe: low (<1H) | medium (1H-4H) | high (daily+)
- Regime: trending | ranging | transitioning | reversal
- Entry trigger: exact conditions
- Invalidation: when it fails
- TP logic: default target + when to hold/exit early
- Risk: sizing, stop placement

**Pass 2 → Philosophy document:**
2-4k word first-person document in the trader's voice. Used as the discretion gate LLM prompt. Covers: identity, core principles, setup descriptions, entry mechanics, anti-patterns, psychological approach.

## Output Structure per Trader

```
traders/<name>/
├── profile.json            # Structured: all setups tagged by regime × timeframe
├── setups/                 # One file per regime pair
│   ├── trending_htf.md
│   ├── trending_ltf.md
│   ├── range_htf.md
│   ├── range_ltf.md
│   └── reversal.md
├── philosophy.md           # First-person voice doc for discretion gate
├── risk.md                 # Sizing, stops, max loss rules
├── anti_patterns.md        # Explicit avoidance rules
└── raw_transcripts/        # Source .txt files
```

## Backtest → Indicator Pipeline

1. Per-trader regime-tagged setups extracted
2. Convert each setup to Pine Script indicator
3. Backtest against 1-2 years BTC data via TradingView MCP
4. Keep strongest, discard weak
5. Deploy surviving indicators as TradingView alerts

## Two-Phase Execution Plan

**Phase 1 (longest, do first):** Analyze & Digest
- Build profiles for all 7 traders
- Feed sandbox with TradingView + Coinalyze + CoinGecko + order flow data
- Backtest each trader's regime-tagged setups
- Build Pine Script indicators from validated setups
- ONLY proceed to Phase 2 when strategies are backtest-proven

**Phase 2 (after Phase 1):** Execution
- Hyperliquid account setup
- WunderTrading MCP (whitelisted to TP-only)
- Discretion gate (LLM with trader philosophy, reviews TP decisions)
- Bounded Martingale sizing layer (small base, add on BTC dip, never sell at loss, dynamic TP by blended cost basis)
- Run alongside existing volume sweep strategy

## Key Difference from Model Trader

| | Model Trader | This Pipeline |
|---|---|---|
| Scope | Single trader → single scanner | 7 traders × regime splits |
| Extraction output | Flat strategy.md | Regime-tagged taxonomy per trader |
| Execution | Monolithic Python scanner | Pine Script indicators → WunderTrading |
| Discretion gate | Reviews entries | Reviews TP adjustments only |
| Sizing | Fixed per-trade % | Bounded Martingale (conviction adds) |

## References

- Model Trader repo: github.com/tonbistudio/model-trader
- The video that inspired the approach: "I Built an AI Trading System From a Trader's YouTube Videos" by Tonbi's AI Garage
- yt-dlp for YouTube transcripts: github.com/yt-dlp/yt-dlp
- Hyperliquid API: hyperliquid.xyz
