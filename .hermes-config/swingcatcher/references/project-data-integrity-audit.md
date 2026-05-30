# Project-Level Data Integrity Audit

CSV import checks (see `data-audit-methodology.md`) are step one. Once data enters the project, run a broader project-level audit to catch cross-source inconsistencies, stale symlinks, and pipeline drift.

## Scope

Audit all data sources that feed into the analysis pipeline:

| Layer | What to check |
|---|---|
| **Signal exports** | TV-exported CSVs: feature count, NaN, vb+vs≈vol, date range, direction balance, timestamp-perp alignment |
| **Exchange data** | OHLCV continuity (no gaps, no duplicates), column naming consistency, taker volume sanity, basis computation |
| **Symlinks** | `swing_research/data/` should point to current files, not stale/deleted originals |
| **Script health** | Active Python scripts should `python -m py_compile` clean; dead scripts should be documented or archived |
| **Perp ↔ signal alignment** | Every signal timestamp has a perp candle within ±5min; signal range is fully covered by perp data range |
| **Duplicate entries** | Multi-entry signals (DCA lots at same price+time) vs true duplicates; use `(time, signal_number)` key not `(time, price)` |
| **Cross-CSV consistency** | Shared features (e.g., volRatio, vdRatio) agree across 7-feat, 14-feat, and 24-feat exports |

## Run Sequence

```python
# 1. Load all data sources
signals = load_signals('path/to/canonical.csv')
perp = load_perp('path/to/merged_5m.csv')
config = yaml.safe_load(open('configs/current.yaml'))

# 2. Run all checks, aggregate results
report = {}
report['signal_count'] = len(signals)
report['feature_audit'] = run_feature_audit(signals)         # NaN, vb+vs, feature count
report['perp_audit'] = run_perp_audit(perp)                   # gaps, duplicates, date range
report['alignment_audit'] = run_alignment_audit(signals, perp) # ±5min match rate
report['symlink_check'] = check_symlinks('swing_research/data/')
report['script_syntax'] = check_python_syntax(glob('*.py'))

# 3. Flag failures
for check, result in report.items():
    if result.get('status') != 'pass':
        print(f"✗ {check}: {result.get('detail', 'failed')}")
    else:
        print(f"✓ {check}: passed")
```

## Example: BTCUSDT 90d Audit (May 23 2026)

| Check | Result | Detail |
|---|---|---|
| Signal count | 434 | 248S / 186L, Feb 20 → May 17 |
| Features (24-feat) | ✅ pass | 7/7 checks clean (NaN=0, vb+vs≈vol, feature count=25) |
| Features (7/14-feat) | ✅ pass | Shared features agree with 24-feat |
| Perp gaps | ✅ pass | 49,783 candles, no gaps, no duplicates |
| Timestamp alignment | ✅ pass | 100% within ±5min |
| Symlinks | ⚠️ fixed | `perp_5m.csv` and `signals_5m.csv` were pointing to deleted files; re-pointed |
| FATCAT duplicate entries | ⚠️ flagged | Multiple entries at same price+time, but they're DCA lots — unique entries = 72, not false positives |
| March 16 short swing | ⚠️ flag | Returned 0.32%, below 0.5% threshold — genuine data point |
| Script syntax | ✅ pass | 2 active scripts compile clean |

## When to Re-Audit

- Every new CSV export arrives from TV
- Every time perp data is refreshed or expanded
- After refactoring pipeline scripts
- Before any analysis run that depends on the full dataset

## Audit Pitfalls

- **Don't key duplicate detection on price+time alone** — DCA strategies add lots at the same bar. Use `(timestamp, signal_number)` or `(timestamp, direction, price)` with tolerance.
- **Don't expect volume parity across exchanges** — TV perp volume ≠ Binance.US spot volume ≠ Binance Futures volume. Volume-dependent indicators can't be reproduced across different data sources.
- **Check that the perp data date range fully covers the signal range** — partial coverage means some signals lack perp features, which silently skews enrichment.
- **Audit symlinks every time** — they silently break when you move source data around and the script that uses them doesn't error (just reads stale data or dies with a confusing error).
