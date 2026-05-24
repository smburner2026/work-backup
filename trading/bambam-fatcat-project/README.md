# BAMBAM-FATCAT Reverse Engineering Project

## Overview

**Goal:** Determine the exact filtration mechanism that makes Ferocious Fatcat (invite-only) more selective than BAMBAM/POCKETBAMBAM, so the strategy can be replicated.

**Status:** The signal chain is confirmed. The exact filter parameters are not — brute-force sweep needed.

## Confirmed Facts

1. **BAMBAM (OG)** — Pine Script indicator. Uses candle-body volume estimate. Signal: prior bar hitting a 200-bar extreme with high volume and delta exhaustion. Fires correct signals on TradingView chart.

2. **POCKETBAMBAM** — BAMBAM signals acted on as entries, with 1-bar delay (15 min on 15m chart). Same script, same parameters, same volume source. PBB entry = BAMBAM signal time + 1 bar.

3. **FATCAT** — Invite-only fork by same author (BAMBAMTHECHONKMASTER). ~92% more selective than POCKETBAMBAM. FATCAT entries are a SUBSET of POCKETBAMBAM entries (6/21 in v2 period). Does NOT use `taker_buy_base` — the `takerbuyvol` built-in produces a compile error on the user's broker, and FATCAT would face the same error. The filter is a parameter or gating mechanism, not a volume source change.

4. **Data mismatch** — External Binance data (data.binance.vision archives) does NOT produce matching BAMBAM signal timestamps vs TradingView. Exact timestamp reproduction requires a matching data feed.

## File Inventory

### Data (`data/`)
- `fatcat_year.csv` — 29 FATCAT entries over 11.5 months (Jun 2025 - May 2026)
- `pocketbambam.csv` — 21 POCKETBAMBAM entries (Apr-May 2026, "v2 period")
- `fatcat_v2.csv` — 6 FATCAT entries (Apr-May 2026, same period as PBB)
- `binance_15m_futures.zip` — 10,848 bars of 15m BTCUSDT futures OHLCV (Oct 2025 - May 2026), includes `taker_buy_volume` column

### Pine Script (`pinescript/`)
- `bambam-vwap-bands.pine` — OG BAMBAM indicator with VWAP bands
- `bambam-gate-indicator.pine` — BAMBAM with configurable cooldown gate (visual comparison tool)
- `bambam-strategy.pine` — BAMBAM strategy with entries, TP-only exits, DCA adds

### Prompts (`prompts/`)
- `resume.md` — Prompt for Hermes to resume this project

## What We Know About the Filter

The FATCAT filter is NOT:
- Volume source change (takerbuyvol doesn't compile → dead theory)
- A single-cooldown rule (gaps between FATCAT entries range from 35h to 1196h, with some gaps as tight as 22h in the v2 period)
- Simple parameter tuning alone (lessRatio 0.05→0.03 barely changes signal count with estimated volume)

Likely components:
- **Cooldown gate** — minimum bars between accepted entries (candidate: 35h ≈ 140 bars @ 15m)
- **AND mode delta** — requires BOTH isLessRatio AND vd > 0 (more selective)
- **Price delta filter** — only enter if price dropped below prior entry by a minimum threshold
- Or a combination of the above

## Brute-Force Plan

POCKETBAMBAM entries = the complete BAMBAM signal set (verified on chart). FATCAT entries = the target subset. Sweep every filter combination against the PBB signal list and find which produces the FATCAT subset.

Filter space:
| Filter | Range | Step |
|---|---|---|
| Cooldown (bars) | 1–500 | 1 |
| Min price drop (%) | 0–10% | 0.1% |
| Delta mode | OR / AND | — |
| lessRatio threshold | 0.01–0.10 | 0.005 |
| volMult | 0.5–5.0 | 0.1 |

~10M combos, runs in minutes on 32GB offline.

## Next Steps

1. Install Hermes on the 32GB offline box
2. Transfer this entire project directory
3. Load `prompts/resume.md` into Hermes
4. Run the brute-force sweep
5. Validate the winning combo against the FATCAT indicator on TradingView
