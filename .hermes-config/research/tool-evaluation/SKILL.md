---
name: tool-evaluation
description: Systematic methodology for evaluating third-party tools, plugins, projects, and services for integration fit — code audit, compatibility check, stack-overlap analysis, and recommendation. Covers the full lifecycle from initial curiosity to go/no-go decision.
version: 1.2.0
---

# Tool/Project Evaluation Framework

## When to Use

The user shares a link or mentions a new tool/project/plugin and asks any of:
- "Is this useful for us?"
- "Audit this — see if it's working"
- "Look through the code and see if it's practical"
- "Can we use this for X?"
- "What do you think of this?"

## Evaluation Pipeline

### Phase 1 — Surface Scan (what is it?)

1. **Load the home page / README** — tagline, core promise, problem statement
2. **Identify the category** — CLI tool? Plugin? Library? Service? API? MCP server?
3. **Note the authors** — established org, solo dev, research group? How many contributors?
4. **Check the version** — is it v0.1.0 (pre-alpha) or v5.2.0 (mature)?
5. **License** — MIT/Apache (safe), AGPL (veto risk), Proprietary (cost/dead-end risk)

### Phase 2 — Depth Check (does it work? does it ACTUALLY do what it claims?)

Start with the README claims, then VERIFY them against source. AI agent repos in particular systematically exaggerate in READMEs.

#### 2a — Surface-level claims audit

1. **Read the README** — tagline, feature list, architecture diagram, supported modes
2. **Check `pyproject.toml` / `package.json`** — version number, actual dependencies, author identity. v0.1.x with "enterprise-grade" in README is a red flag.
3. **Check file structure** — GitHub API `contents/` endpoint for the project root:
   - How many source files vs config/tooling boilerplate?
   - Is the core logic 300 lines wrapped in 2K lines of CLI/README/docs?
   - Agent repos: separate `agent/`, `orchestration/`, `tools/` dirs? Or everything in one file?
4. **Authorship** — Solo dev vs org/research group? Cross-reference with project's real scope.

#### 2b — Deep code inspection (the gap between README and source)

For AI agent repos, READMEs describe ideal behavior. Source code reveals actual behavior.

1. **Read the orchestration entry point** — don't just scan file names, read the actual `main.py` / `run()` / `execute()` method:
   - Does it chain agents sequentially (simple LLM call → LLM call) or does it have a real orchestration loop with state management?
   - Is the "multi-agent" pipeline just prompted text generation passed between LLM calls, or does it have structured inter-agent communication (typed outputs, validation gates, retry logic)?
   - Are the "autonomous" claims backed by actual loops, or is it `max_loops=1` with pretty logging?
2. **Read the workers/agents** — not just system prompts, but how they're instantiated and wired:
   - Each agent = `Agent(system_prompt=..., max_loops=1)`? That's prompt chaining, not multi-agent orchestration.
   - Check for actual tool implementations — does the tool code do something real, or is it a stub that returns "analysis complete"?
3. **Read the tools/** — separate from agent code:
   - Are the trading/execution tools actually wired into the main loop, or do they exist as independent modules never called?
   - Do they use real APIs with real credentials (check .env.example), or are they simulation/mock?
4. **Read `pyproject.toml` deps carefully** — Agent repos often depend on the author's own library (e.g. `swarms`, `swarm-models`). This is often a distribution channel, not a technical necessity. Evaluate: does it add value, or is it dependency marketing?
5. **Trace the actual data flow** — From user input → agent reasoning → tool call → output:
   - Is there a backtesting/validation step? Or does it go straight from LLM output → "trade signal"?
   - For trading/agent repos specifically: zero backtesting = zero credibility regardless of star count.

#### 2c — Standard integrity checks

1. **CI status** — Does CI pass? Run on multiple Python/node versions? Linting?
2. **Test quality** — Actual assertions against real behavior, or just "imports fine"?
3. **Dependencies** — Heavy frameworks (PyTorch, Playwright) or lightweight (stdlib + requests)?
4. **Installation path** — `pip install`, `npm install`, `git clone`, docker?

### Phase 3 — Compatibility Check (does it work HERE?)

Run a **systematic collision matrix** before installing any foundational piece. Check these dimensions in order:

| # | Dimension | What to check | How |
|---|-----------|---------------|-----|
| 1 | **Runtime** | Python, Node, Bun versions — do they match? Any shared venv/bin paths? | `node --version`, `bun --version`, `python3 --version`, `which <binary>` |
| 2 | **Ports** | Does the new tool listen on any network port? Could it conflict? | `ss -tlnp` or `netstat -tlnp` |
| 3 | **Env vars** | Any API key name collision? gbrain needs OPENAI_API_KEY; Hermes uses NOUS_API_KEY/OPENCODE_GO_API_KEY — zero overlap. | `env \| grep -iE "ANTHROPIC\|OPENAI\|NOUS\|OPENROUTER\|OPENCODE" \| sort` |
| 4 | **Config files** | Does the new tool use a config dir that overlaps with Hermes? | Check `~/.hermes/`, `~/.<toolname>/`, `/usr/local/lib/hermes-agent/` |
| 5 | **Databases** | Shared SQLite files? Different engines? gbrain uses PGLite (WASM Postgres); Hermes uses SQLite + Mnemosyne. | `ls ~/.hermes/*.db`, `sqlite3 <db> .tables` |
| 6 | **Cron** | Does the tool have its own scheduler? Could it conflict with Hermes cron? | `hermes cron list` or `cat ~/.hermes/cron/jobs.json` |
| 7 | **Filesystem paths** | Does the git clone/share dir collide? | Check `~/<toolname>/`, `~/.<toolname>/`, `/opt/<toolname>/` |
| 8 | **Plugins** | Does it register as a Hermes plugin? Contradict existing ones? | `ls ~/.hermes/plugins/` + `hermes plugins list` |
| 9 | **MCP/API** | Does it expose an MCP server? Already in Hermes config? | `grep -r "mcp_servers" ~/.hermes/config.yaml` |
| 10 | **Disk space** | How much will it consume? Is there room? | `df -h` then estimate: repo clone + deps + DB + embeddings |

For each dimension, document whether it's **✅ Clean** (no conflict), **⚠️ Needs config** (manual integration step), or **🔴 Blocking** (can't proceed without resolution).

Then add a row for any **existing tools that overlap** — what in the current stack already covers this territory, and whether this new tool is additive, redundant, or a replacement.

### Phase 3b — Hermes Plugin-Specific Checks

When evaluating a Hermes plugin (plugin.yaml + __init__.py in a `~/.hermes/plugins/<name>/` dir):

1. **Verify plugin.yaml** — Must have `name`, `version`, `description`, and list hooks/toolsets/commands that match what the code actually registers.
2. **Check register(ctx) exists** — The `__init__.py` must expose a top-level `def register(ctx)` function. This is the Hermes plugin entry point. Without it, the plugin does nothing.
3. **Match hooks to code** — The `hooks:` list in plugin.yaml should match the `ctx.register_hook(...)` calls inside register(). Each hook name must be in the set of valid hooks. Cross-check by grepping the Hermes source for hook invocation points.
4. **Tool registration** — Tools are registered via `ctx.register_tool(name=..., toolset=..., schema=..., handler=..., ...)`. Verify the toolset name matches what plugin.yaml declares. Check that the handler function signature matches what Hermes expects (accepts `args: Any, **kwargs: Any`, returns `str`).
5. **Security audit the code** — Before enabling, inspect for:
   - `eval()` / `exec()` / `__import__()` / `compile()` with user-controlled input
   - File writes outside expected paths (check for path traversal)
   - Network calls to hardcoded endpoints (data exfiltration risk)
   - Import of unexpected packages (supply chain risk)
   - `os.system()` / `subprocess.call()` with unsanitized input
6. **Install path** — Copy entire plugin directory to `~/.hermes/plugins/<name>/` (not `plugins/model-providers/` or other subdirectories — those have separate discovery paths for provider plugins only).
7. **Enable & verify** — `hermes plugins enable <name>`, then `/reset` for a fresh session. Verify the plugin loaded with `hermes plugins list | grep <name>` (status should show "enabled"). Check logs if it doesn't appear.
8. **Toolset visibility** — Plugins may register custom toolsets (e.g., `doga` for DOGA). These toolsets must be enabled for the LLM to see the tools. Run `hermes tools list | grep <toolset>` to confirm. If absent, the plugin's register() may not have been called — check logs for import errors.

### Phase 4 — Stack Overlap Analysis (do we already have this?)

1. **Map existing tools** — What provides this data/capability today?
2. **Compare cost** — Free MCP vs paid wrapper? Token overhead difference?
3. **Compare quality** — Dedicated purpose-built vs generic marketplace?
4. **Compare maintenance** — Actively maintained repo vs abandoned?
5. **The threshold question:** "Does this add enough NEW capability to justify the integration cost?"

### Phase 5 — Synthesis & Recommendation

Deliver a clear verdict using this format:

```
## [Tool Name] — Verdict: [GO / NO-GO / CONDITIONAL]

**What it is:** One-sentence summary.
**Code quality:** [Green flags / Yellow flags] — key observations.
**Works with our setup?** Yes/No — what config changes needed.
**Useful for [target use case]?** [Yes, because... / No, because...]
**Trade-off:** What you gain vs what it costs (money, tokens, complexity, maintenance).
**Alternative in existing stack:** What already covers this territory.

**Bottom line:** One-sentence actionable recommendation.
```

## Classification Heuristics

| Signal | Interpretation |
|--------|---------------|
| v0.x, <10 stars, single contributor | Early-stage — high risk, high potential |
| 3+ contributors, regular releases, tests | Active project — worth deeper look |
| "Coming soon" endpoints for core feature | Vapourware risk — evaluate what EXISTS, not what's promised |
| Proprietary license, API-key-gated | Vendor lock-in risk — how easy to replace? |
| Free tier + paid tiers | Evaluate on free tier first; note cost trajectory |
| Wrapper around existing free APIs | Only valuable if token reduction / convenience is significant |
| No tests, empty docs/, no CI | Tread carefully — fixes will be on YOU |

## Pitfalls

- **Over-valuing star count** — Stars measure popularity, not quality. A 50-star tool with tests and docs is better than a 5K-star tool that's abandoned.
- **Ignoring the existing stack** — "New shiny" bias. Always check first whether your current stack already solves this problem with comparable quality.
- **Assuming compatibility** — Hermes v0.13 vs v0.14 API differences matter. Always search the local Hermes codebase for the APIs the plugin expects.
- **Overlooking maintenance burden** — A plugin that works today but has no tests, no CI, and one maintainer is a liability you'll pay for later.
- **Cost creep** — $0.008/call sounds cheap until you're making 500 calls/day for a trading bot.
- **Token efficiency claims** — Every CLI tool claims to save tokens. Verify by examining the actual output sizes.
- **"AI-native" marketing** — 90% of "built for agents" tools are just standard APIs with a CLI wrapper. Evaluate the DATA, not the packaging.

## References

See `references/` for session-specific evaluation transcripts:
- `hermes-lcm-audit.md` — Full audit of Lossless Context Management plugin (DAG-based context engine), installed and verified
- `agent-data-evaluation.md` — Evaluation of agent-data CLI for quant trading use case (NO-GO: wrong data categories)
- `browse-sh-evaluation.md` — Evaluation of browse.sh browser automation CLI (conditional: needs Browserbase key for protected sites)
- `doga-evaluation.md` — Full audit of DOGA (probabilistic thinking layer plugin for Hermes): Monte Carlo engine, De Bono hats, recursive reasoning, security review, installation. GO verdict — installed and enabled.
- `gbrain-evaluation.md` — Evaluation of gbrain (Garry Tan's open-source Hermes/OpenClaw fork): `gbrain think` with gap analysis, self-wiring knowledge graph, cost matrix, integration as brain layer under Hermes. CONDITIONAL GO — complementary for DABT/history research, needs OpenAI API key.
- `autoned-vibe-trading-evaluation.md` — Evaluation of AutoHedge (thinnish swarms-library wrapper, hype) and Vibe-Trading (substantial HKU research project with DAG orchestration, grounding pre-fetch, ReAct worker, Shadow Account). Demonstrates the claims-vs-source gap inspection methodology.
