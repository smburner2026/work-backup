# Resume: BAMBAM-FATCAT Project

You are resuming a project to reverse-engineer the filtration mechanism
of Ferocious Fatcat vs PocketBAMBAM / BAMBAM OG.

## Files available

```
bambam-fatcat-project/
├── README.md                       # Full project doc
├── sweep.py                        # Brute-force filter sweep (600K combos)
├── mcp_server.py                   # TV webhook receiver + MCP server
│   - python3 mcp_server.py http    → HTTP + SQLite (for TV alerts)
│   - python3 mcp_server.py mcp     → stdio MCP (for Hermes integration)
├── signals.db                      # SQLite DB (auto-created)
├── data/
│   ├── fatcat_v1.csv               # 21 FATCAT entries (Oct-Dec 2025)
│   ├── fatcat_v2.csv               # 6 FATCAT entries (Apr-May 2026)
│   ├── fatcat_year.csv             # 29 FATCAT entries (full year)
│   ├── pocketbambam.csv            # 21 PBB entries (Apr-May 2026)
│   └── binance_15m/                # 113 CSVs, 10,848 bars OHLCV
├── pinescript/
│   ├── bambam-vwap-bands.pine      # OG BAMBAM indicator
│   ├── bambam-gate-indicator.pine  # Configurable ind + cooldown gate
│   ├── bambam-strategy.pine        # Strategy with entries
│   └── bambam-signal-capture.pine  # BAMBAM + structured webhook payload
├── docs/
│   ├── SETUP_GUIDE.md
│   ├── CUSTOM_MCP_DESIGN.md        # 3-phase MCP plan
│   └── FATCAT_ALERT_SETUP.md       # How to configure FATCAT webhook
└── prompts/
    └── resume.md                   # This file
```

## Current status

**Sweep script tested and ready.** The v2 CSV test shows a pure cooldown
filter (24h) hits F1=0.667 max. The full 600K combo sweep needs the
32GB box to find the optimal combination.

**Confirmed facts (do not rediscover):**
- FATCAT does NOT use taker_buy_base (takerbuyvol compile error)
- Volume source is candle-body estimate, same as BAMBAM
- PBB entries contain all FATCAT v2 entries as a subset (6/6)
- External Binance data doesn't match TV timestamps from this VPS
- The MCP server is the solution for reliable signal capture

## Two paths forward

### Path A: CSV brute-force (immediate, partial)
Run sweep.py on the existing CSVs. Uses the v2 PBB+FATCAT data.
```bash
python3 sweep.py --pbb data/pocketbambam.csv --fatcat data/fatcat_v2.csv \
  --year data/fatcat_year.csv --output sweep_results.json
```
Takes ~5 minutes on the 32GB box. Results go to sweep_results.json.

### Path B: MCP webhook capture (complete, requires setup)
1. Start mcp_server.py on the 32GB box (http mode)
2. Add BAMBAM-signal-capture.pine to TV chart, enable webhooks
3. Set up FATCAT alert using chart conditions (FATCAT_ALERT_SETUP.md)
4. Run Bar Replay over 90 days
5. Both indicator signals land in signals.db
6. Export to JSON, run sweep.py against the clean data

Path B gives you the definitive answer — no CSV export bugs, both indicators
captured from the same chart, same period, same engine.

## Key rule: NEVER propose taker_buy_base as a solution
The takerbuyvol compile error proved FATCAT can't use it.
The difference is parameter tuning + cooldown gate.
