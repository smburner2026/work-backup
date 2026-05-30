# Local G-Brain Config (as of May 28, 2026)

## Installation
- **Version:** 0.41.20.0
- **Path:** `/root/gbrain` (git clone + bun link)
- **Brain repo:** `~/brain/`
- **Config:** `~/.gbrain/config.json`

## Engine
- **Engine type:** PGLite (WASM Postgres, zero-config)
- **Database path:** `~/.gbrain/brain.pglite`
- **Backup:** `~/.gbrain/brain.pglite.bak` (empty/pre-migration — not useful for recovery)

## Model Configuration
- **Embedding:** `openrouter:nvidia/llama-nemotron-embed-vl-1b-v2` (1024d, FREE)
- **Chat model:** `deepseek:deepseek-v4-flash` (via OpenCode Go custom endpoint)
- **Chat base URL:** `https://opencode.ai/zen/go/v1` (via `provider_base_urls.deepseek`)
- **OpenRouter key:** Exists in `.hermes/.env`, not in gbrain's environment directly

## DABT Brain State
- **Chunks imported:** ~6,597
- **Sources:** Casarett & Doull 9e, Hayes 7e, ~60 regulations, ABT handbook
- **Total pages:** ~106 (all currently inaccessible — DB corrupted, see `references/pglite-database-recovery.md` for recovery options)
- **Search mode:** Conservative (set during install)

## Known Issues/Patches Applied
- **dims.ts patch applied:** `dimsProviderOptions()` in `src/core/ai/dims.ts` patched so `openai-compatible` tier returns dimensions parameter for models like NVIDIA Nemotron on OpenRouter
- **Dimension passthrough bug:** Models routed through OpenRouter as `openai-compatible` don't receive `dimensions` parameter in stock v0.41.10.1 — returns native dims instead of configured dims
- **Dream-cycling patches:** Hardcoded Anthropic defaults in propose-takes.ts, grade-takes.ts, calibration-profile.ts patched to deepseek models

## Notes
- Dream cycles are NOT yet active (no cron job running)
- MCP server IS wired into Hermes — `~/.hermes/scripts/gbrain-mcp-wrapper.sh` wraps `gbrain serve`, configured in config.yaml as `mcp_servers.gbrain`
- Only one brain exists (DABT) — no separate history brain initialized yet
- PGLite database is currently corrupted — fresh DBs initialize fine but opening the existing `brain.pglite` triggers a WASM abort. See `references/pglite-database-recovery.md` for diagnostic flow and recovery.
