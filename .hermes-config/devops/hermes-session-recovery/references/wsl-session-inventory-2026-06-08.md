# WSL Session Inventory — Recovered 2026-06-08

Source: `/root/.hermes/sessions/sessions-wsl.json` (851 lines)

## Machine

- **WSL hostname**: local-machine
- **Tailnet IP**: 100.110.237.89
- **Role**: compute muscle (OCR, heavy tasks)
- **Home**: /home/vthen/

## Recovered Sessions (by date)

| Date Range | Topics | Key Files / Actions |
|-----------|--------|---------------------|
| May 21–23 | Early Telegram/Discord setup, first threads | Discord #general thread 20260521_225954, Telegram dm with Randoooos 20260523_224742 |
| May 30 | VPS inventory, network topology | VPS: ubuntu/KVM, 100.113.2.25; Windows desktop 100.102.166.100; Pixel 7a 100.93.156.51 |
| May 30 | Yazi installed on VPS, then removed | Removed ~42MB including fzf/jq/fd-find |
| May 31 | gbrain update to WSL (v0.41.29 → v0.42.1), then removed | WSL kept: bun, hms, skills (1041 files), memories. Removed gbrain per user: "VPS is the brain" |
| May 31 | VSTB translation pipeline | Vol 6 re-OCR via SSH to WSL (PID 5413). Vol 2 and 5 also repaired. 502 pages restored. Files: /home/vthen/work/post-colonial-vietnam/sources/vstb/ |
| May 31 | Hoang Tham OCR/translation cleanup | hoang-tham-pages/ (279 JPEGs, 46 MB) removed from WSL. Final PDF + cleaned text kept on VPS |
| June 3 | Hermes Desktop → VPS Tailscale setup | Windows desktop connected to VPS at 100.113.2.25:9119 via Tailscale. Conflict with NordVPN resolved |
| June 3 | opendataloader-pdf queued for WSL | Not yet installed; blocked by WSL unavailability |

## File Paths

- WSL home: `/home/vthen/`
- Work dir: `/home/vthen/work/post-colonial-vietnam/`
- VPS sync: `scp local-machine:...→/root/work/post-colonial-vietnam/sources/vstb/`
- SSH alias: `ssh local-machine`

## Sync State

- skills, memories, hms → synced
- gbrain → removed from WSL (brain on VPS only)
- config → intentionally different per architecture

## Status

- WSL not reached on June 3 opendataloader-pdf install
- session_search currently does NOT return WSL-origin sessions from `sessions-wsl.json`
