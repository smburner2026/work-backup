# AutoHedge & Vibe-Trading Evaluation (2026-05-31)

**Source:** Harman (@itsharmanjot) tweet — "10 GitHub repos so good they shouldn't be free"
**Question:** Useful or AI hype slope?
**Method:** GitHub API source code inspection (not just READMEs)

---

## AutoHedge (The-Swarm-Corporation/AutoHedge)

| Field | Value |
|-------|-------|
| Version | 0.1.5 |
| Stars | ~2,900 |
| Author | Kye Gomez (kye@apac.ai) — also creator of `swarms` library |
| Core deps | `swarms`, `swarm-models`, `solders` (Solana), `yfinance` |
| Real source | ~300 lines across core files (main.py, workers.py, prompts.py) |
| Tests | None visible |

**Verdict: Hype.** The repo is a thin wrapper around the author's own `swarms` library. The "4 agent" pipeline (Director → Quant → Risk → Execution) is just `max_loops=1` GPT-4.1 calls chained via the library's `handoffs` mechanism. No backtesting, no paper trading, no P&L tracking. The Solana trading tools exist in the repo but are never called in the main loop — the run() method returns conversation history as a string. The README says "enterprise-grade" but the code is a weekend-project shell at v0.1.5.

**Useful takeaway:** The Director → specialist agent pipeline pattern is valid. The implementation here is not. Evaluate by checking `max_loops` and whether tools are actually wired into the main loop.

---

## Vibe-Trading (HKUDS/Vibe-Trading)

| Field | Value |
|-------|-------|
| Version | Multiple (pip package `vibe-trading-ai`) |
| Stars | ~9,200 |
| Author | HKU Data Science lab |
| Core | Custom DAG engine, ReAct worker, Shadow Account, 77 skills, 29 swarm presets |
| Tests | Present under agent/tests/ |
| MCP | Has mcp_server.py — MCP server for Claude/OpenClaw/Cursor integration |

**Verdict: Legit substance.** This is a proper engineering project with genuine architectural contributions:

1. **SwarmRuntime** — DAG-based multi-agent orchestration with topological layering, ThreadPoolExecutor parallelism, file-based persistence, event callbacks, cancellation support
2. **Grounding pre-fetch** — Fetches real OHLCV data before agent reasoning and injects it as a "Ground Truth" block with explicit citation rules that prevent LLMs from quoting training-data prices
3. **ReAct worker** — Full ReAct loop with micro-compaction (keeps last 3 tool results), deliverable quality classification, heartbeat timers, token budgeting
4. **Shadow Account** — Extracts implicit trading patterns from broker CSVs → codifies as if-then rules → backtests across A/HK/US/crypto → produces comparison report
5. **77 modular skills** — Self-contained skill directories loaded on-demand
6. **29 swarm presets** — YAML configurations for different team compositions (investment committee, equity research, crypto desk, etc.)

**Key pattern worth borrowing:** The DAG orchestration + grounding pre-fetch + output contract gates form a reusable architecture for any multi-agent workflow, not just trading.

---

## Evaluation Technique Used

How the substance was separated from claims:

1. GitHub API `contents/` endpoint → directory structure overview
2. `raw.githubusercontent.com` → README, pyproject.toml, each source file
3. Cross-reference README claims against actual source code:
   - "4 agents" → actually 5 agents defined, but only director_agent.run() is called
   - "autonomous trading" → Solana tools exist but never wired into main loop
   - "enterprise-grade" → v0.1.5, no tests, single author
   - Vibe-Trading's claims held up: actual DAG engine, actual ReAct loop, actual Shadow Profile
4. Check pyproject.toml for version + dependency graph
5. Read the orchestration entry point (not just file names) to trace actual data flow
6. Check for test directories and CI config
