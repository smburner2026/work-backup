# Low Disk Recovery — VPS Diagnosis & Cleanup

Scenario: rsync hangs mid-transfer, `hms push/pull` stalls with no error.
Likely cause: VPS disk is full (100%).

## Diagnosis

### From local machine:
```bash
hms cleanup
```
Shows `.hms-bak` count, disk usage %, top space consumers.

### From VPS directly:
```bash
df -h /                              # check root space
du -sh /root/*/ | sort -rh | head -10  # top consumers
```

### Signs of a stuck sync due to full disk:
- `hms pull/push` hangs with no output for minutes
- SSH connection shows a large send-Q buffer:
  ```bash
  ss -t | grep <local-tailscale-ip>
  # ESTAB 0 419568 ... — send-Q > 0 means data stuck
  ```
- Rsync process stuck as `--server --sender`:
  ```bash
  ps aux | grep rsync
  ```

## Safe Cleanup Targets (in priority order)

### Tier 1 — Immediate free space (always safe to delete)

| Target | Typical size | Reason |
|---|---|---|
| `.hms-bak*` files | ~1-10MB | Recovery copies from prior syncs. Safe to delete after sync succeeds. |
| `~/.hermes/state-snapshots/` | ~1.9GB | Pre-update backups created by `hermes update`. Keep latest only, delete rest. |
| `~/.hermes/cache/` | ~200MB | Temp cached data. Cleared automatically over time. |
| `~/.hermes/sessions/*.jsonl` | ~170MB | Old session transcripts. Hermes session DB (`lcm.db`) has the canonical data. |

### Tier 2 — Source files (if extraction/reference is done)

| Target | Typical size | When safe |
|---|---|---|
| Raw course materials (e.g. `dabt-curated/`, `dabt-materials/`) | 2-4.5GB | After extraction into reference library and memory. |
| Nietzsche PDF sources | ~90MB | After anthology project is complete or if PDFs are cached elsewhere. |
| Old Binance CSV exports | ~37MB | After feature extraction. Raw klines/merged CSVs can be regenerated from the exchange. |
| Large reference PDFs (e.g. `hayes-7e.pdf` 116MB, `casarett-doull-9e.pdf` 54MB) | ~170MB | If both machines have copies and PDFs don't change. Add to rsync exclusions. |

### Tier 3 — Possibly redundant

| Target | Typical size | Check first |
|---|---|---|
| `~/.hermes/hermes-agent/` | ~1.9GB | Only needed if actively developing Hermes. Delete if installed via pip/script at `/usr/local/lib/hermes-agent/`. |
| `~/.hermes/node/` | ~220MB | Node runtime for LSP. Check if LSP is needed. |
| `~/.hermes/mnemosyne/data/` | ~650MB | Compact with `VACUUM` to reclaim space: `sqlite3 mnemosyne.db "VACUUM;"` |
| `~/.hermes/lsp/` | ~55MB | Language server binaries. Remove if not using LSP features. |

## Recovery Steps

```bash
# 1. Kill the stuck rsync if needed
ssh root@vps "killall rsync"  # or pkill -f rsync

# 2. Free space — remove state-snapshots (1.9GB)
ssh root@vps "rm -rf ~/.hermes/state-snapshots/*"

# 3. Free more — remove hms-bak files
ssh root@vps "find ~/.hermes -name '*.hms-bak*' -type f -delete"

# 4. Free more — clear cache
ssh root@vps "rm -rf ~/.hermes/cache/*"

# 5. Check
ssh root@vps "df -h /"
```

## Prevention

- `hms` script has a pre-flight check that warns at <500MB free and blocks at <100MB.
- Run `hms cleanup` weekly to catch `.hms-bak` accumulation.
- Large static files (PDFs, CSVs, datasets) that don't need to sync bidirectionally can be excluded via rsync `--exclude` patterns in the HMS script config.
- Keep an eye on state-snapshot growth — `hermes update` creates these automatically.
