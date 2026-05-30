# Hermes Agent — Detailed Memory Reference

This file backs the SKILL.md with fuller context for complex operations.
Loaded via skill_view(name='hermes-agent-memory', file_path='references/memory.md').

## Soul Architecture (Layers 0-3)

### Layer 0 — Operating Charter
- **COSTIN_OP**: Autonomous operator for the user. Job: Improve workflows + Protect attention + Advance high-value work → Intent to execution. Coordinate, inspect, decide, delegate, synthesize, QC. No waiting for perfect instructions.
- **STANCE**: Opinionated, high-agency. Push back when user is vague/unrealistic/distracted/avoidant. Separate Facts/Assumptions/JudgmentCalls/OpenQuestions.
- **AUTONOMY**: Broad autonomy, narrow hardline. Never without explicit approval: public posts, publish, purchase, paid signups, messages to real people, delete important, destructive changes, expose private info, change creds/security. Everything else → confident + grounded → move.
- **PUSHBACK**: Aggressive when earned. Disagree with evidence (data/examples/reasoning/proof/tradeoffs/alternative). Disagree to prevent flop/waste/risk/focus-loss — not sport.
- **DLGT_RULES**: Accountable for delegated work. Provide context, exact task, constraints, prior findings, expected output, verification steps. Keep subtasks narrow + concrete + outcome-based.

### Layer 1 — Hermes Architecture
- AGENT loop: Assess → GatherIntel → Plan → Execute → Verify → Deliver
- LEARN loop: Persist → SkillMgmt → Reflect → [AGENT:1a]
- Complex tasks: OMNICOMP → ChainConstructor → SkillgraphMaker

### Layer 2 — Karpathy Principles
1. Think before coding
2. Simplicity first
3. Surgical changes
4. Goal-driven execution
5. Anchor first

## G-Brain Factsheet

- **Location**: ~/gbrain (git clone, not bun install -g)
- **Version**: 0.41.20.0 (updated 2026-05-27)
- **Engine**: PGLite at ~/.gbrain/brain.pglite (WASM — single process only)
- **Embedding**: openrouter:nvidia/llama-nemotron-embed-vl-1b-v2 (1024d, free via OpenRouter)
- **Chat**: deepseek:deepseek-v4-flash via OpenCode Go (custom endpoint, provider_base_urls)
- **MCP server**: gbrain serve via ~/.hermes/scripts/gbrain-mcp-wrapper.sh
- **Dream cycle**: cron at 0 2 * * * — stops MCP → sync brain → embed → extract → dream → restarts MCP
- **PGLite quirk**: Fresh CLI invocations fail — WASM can only init once per process. MCP tools (mcp_gbrain_*) reuse the server's instance and work reliably. The dream cycle script handles this by stopping/restarting the MCP server.

### Known Issues
- **Stale postmaster.pid**: After a crash/OOM, `~/.gbrain/brain.pglite/postmaster.pid` may be left behind. Remove it before next CLI use.
- **Stale gbrain_cycle_locks**: After OOM-killed dream, a `gbrain_cycle_locks` DB row may persist. Cleared via dream cycle script or manual DELETE.
- **Config split**: `gbrain config set` writes to PGLite DB; `~/.gbrain/config.json` is fallback. `config get` reads DB (authoritative), `config show` reads JSON (may be stale).

### Backup
- PGLite auto-creates ~/.gbrain/brain.pglite.bak/ during init. Recovery: swap brain.pglite.dirty → brain.pglite from .bak.

## Environment Details

### Shell & Tools
- **PATH**: `$HOME/.bun/bin:/usr/local/bin:/usr/bin:/bin`
- **Python**: `/usr/local/lib/hermes-agent/venv/bin/python3` (VENV_PYTHON)
- **Bun**: ~/.bun/bin/bun
- **gbrain CLI**: ~/.bun/bin/gbrain (bun link from ~/gbrain/)

### Project Directories
- **Work**: /root/work/
- **Trading**: /root/work/trading/
- **Brain (gbrain repo)**: ~/brain/
- **gbrain install**: ~/gbrain/

### Skills Location
- `~/.hermes/skills/<category>/<skill-name>/SKILL.md`
- Default profile: active session. Other profiles at `~/.hermes/profiles/<name>/skills/`

## Daily/Monthly Rhythm

- **02:00** — G-Brain dream cycle (sync, embed, extract, dream — all mechanical phases)
- **06:00** — Nightly self-improvement (profile compression, memory consolidation)
- **08:00** — Nightly self-audit (update checks, gbrain health, dream completion)
- **05:00 Sun** — DABT weekly truth audit
- **05:00 Sun** — gbrain-dabt-maintenance
- **06:00 Sun** — Work backup
