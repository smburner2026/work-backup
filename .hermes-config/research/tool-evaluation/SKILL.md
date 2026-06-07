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
5. **Dead-fork detection** — If the repo is a fork (`.fork == true`), compare against the parent IMMEDIATELY:
   ```bash
   gh api repos/<owner>/<name>/compare/<parent>:main...main \
     --jq '{ahead_by, behind_by, total_commits: (.commits | length), files_changed: (.files | length)}'
   ```
   **`ahead_by == 0 && behind_by > 1000` is an instant NO-GO.** The "fork" is a frozen snapshot of upstream with no original work, drifting further every day. Security patches and bug fixes from the parent will never land here. Installing it = running a stale snapshot. Check: any releases? Any open issues? Any security policy? If all three are missing, confirm NO-GO. The number of stars is irrelevant — a 24-star dead fork is still dead.
6. **Generic-tool-mislabeled-as-targeted** — When a tool's README claims "built for X platform" but the "verified hosts" / "supported clients" / "tested with" list in the actual docs does NOT include X, the targeting is marketing, not real. Cross-check the README's first-paragraph claim against the supported-hosts list before recommending.

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
| 3 | **Env vars** | Any API key name collision? Check for shared env var names (e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY) between the new tool and Hermes's NOUS_API_KEY/OPENCODE_GO_API_KEY. | `env \| grep -iE "ANTHROPIC\|OPENAI\|NOUS\|OPENROUTER\|OPENCODE" \| sort` |
| 4 | **Config files** | Does the new tool use a config dir that overlaps with Hermes? | Check `~/.hermes/`, `~/.<toolname>/`, `/usr/local/lib/hermes-agent/` |
| 5 | **Databases** | Shared SQLite files? Different engines? Check what DB engine the new tool uses vs Hermes's SQLite + Mnemosyne. | `ls ~/.hermes/*.db`, `sqlite3 <db> .tables` |
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
6. **The use-case question:** "Does the tool's value proposition target a use case I actually have?" — this is a sharper filter than the threshold question. Many well-engineered tools solve problems specific to other workflows (multi-agent orchestration, IDE integration, cross-tool memory) that don't apply to a single-Hermes stack. A tool can pass every technical check and still be NO-GO because the user only has one of the legs the tool stands on. See "Engineering GO ≠ User GO" gate in Phase 5.
7. **Self-hosted/open-source alternative check.** Before vetoing a tool category entirely (e.g., "Firecrawl — rejected because paid SaaS"), check whether a self-hosted open-source alternative exists. The cost/benefit calculus for a self-hosted MIT-licensed tool is fundamentally different from a paid API. Search for: `<category> self-hosted github`, `<toolname> alternative open source`, or equivalent. The method-sourcing blind spot (GroktoCrawl — a self-hosted MIT-licensed Firecrawl-compatible stack — existed at v0.6.0 but was never surfaced in the T0-T3 evaluation) is the canonical failure this step prevents. A category veto should say "Firecrawl SaaS is vetoed, but the category has a self-hosted option at groktopus/groktocrawl" rather than "Firecrawl vetoed."

### Phase 4b — Listicle / Multi-Tool Review Pattern

When the user shares a roundup post (X thread, blog "top 5" list, "awesome-X" curated list, Reddit roundup) and asks "are these useful?", do NOT evaluate the list as a unit. Evaluate each item against the full framework, then synthesize. Specifics:

1. **Strip the framing** — X listicles use hyperbolic claim + FOMO hook ("you haven't caught up yet?"). The framing is marketing. The list contents are the actual signal. Read the list, ignore the prose.
2. **Don't trust the listicle's own numbers** — Hit the GitHub API for star count, last push, contributors, releases. Listicles systematically inflate ("3,400+ stars" → check) AND occasionally undercount; treat every number in the post as suspect and verify before quoting. Use `gh api repos/<owner>/<name> --jq` once per repo — it's a 5-second call.
3. **Quick triage each item** — Phases 1-3 for each repo. Mark each as REAL+USEFUL / REAL+REDUNDANT / SUSPICIOUS / FAKE.
4. **Flag the use-case problem** — Many roundups aggregate tools targeting use cases the user doesn't have (e.g., a listicle targeting multi-tool agent users when the user runs only Hermes; or targeting team workflows when the user is solo). A list of 5 "useful tools" can be 5 NO-GOs for one user.
5. **Honor prior rejections** — If the user has previously said "I tried X and wasn't happy with it" (in this session OR a prior one — check `session_search` / `memory` for that exact name), drop it from the recommendation set. Don't relitigate, don't ask "what was wrong," don't try to talk them into it. A negative prior verdict is a hard veto unless the user explicitly reopens it.
6. **Deep-dive the credible ones** — For items that pass Phases 1-4, run the full Phase 5 synthesis on each. A viral roundup is a *lead* — not a recommendation.
7. **Cite the curated list, not the viral post** — Real discovery sources: `awesome-X` GitHub lists, vendor docs, independent technical blog posts, Reddit threads with reproducible benchmarks. Viral posts are starting points; curated lists are maps.
8. **The listicle-collapse verdict is real** — When triage yields 0/5 GO for the user's stack, the honest answer is "skip the listicle entirely," not "pick the best of bad options." A 0/5 result is data: the roundup is targeting an audience that doesn't include this user. Say so plainly and stop. Trying to install something to validate the listicle is a sunk-cost trap.

**Pattern from real evaluation (2026-06-05 listicle):** A roundup of "5 不可不装的 Hermes 插件" was triaged per-item. The "must install" framing hid: (a) a 27-star hobby project, (b) a paid-skill marketplace with a 402 crypto-payment path, (c) a community workspace the user had already tried and rejected, (d) a frozen fork 8,403 commits behind upstream with zero releases, and (e) a memory tool whose README explicitly did NOT list Hermes as a supported host. Net: 0/5 GO once prior-rejection + preconditions + dead-fork detection were applied. Full transcript in `references/listicle-hermes-ecosystem-2026-06.md`. Earlier example (RTK/Plur) in `references/rtk-plur-evaluation.md`.

### Phase 5 — Synthesis & Recommendation

**Final pre-recommendation gate — "Engineering GO ≠ User GO":**

A tool can pass every technical check (real code, real benchmark, no security issues, compatible stack) and still be NO-GO. The user-specific gate is: "Does the value proposition of this tool solve a problem the user actually has, in the architecture the user actually runs?"

Concrete failure mode: a well-engineered cross-tool memory layer (e.g. Plur) targeting Claude Code + Cursor + Windsurf + OpenClaw + Hermes — passes every technical check, but the user runs only Hermes and already has a memory stack. The tool is correct engineering and wrong fit. Don't install.

This is the inverse of the "Ignore the existing stack" pitfall. That pitfall is "you already have this, skip it." This gate is "you don't have the preconditions for this to add value, skip it."

Run both: stack overlap (do I already have something that does this?) AND preconditions check (does my setup have the legs this tool stands on?). A tool can fail either check and be NO-GO.

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
- **Trusting listicle numbers** — Star counts, "must install" counts, "X users love this" counts in roundup posts are systematically wrong (inflated, deflated, or fabricated). Hit the GitHub API for every claim before quoting. A listicle that says "3,400+ stars" might mean 5407 (listicles under-count) or 24 (listicles conflate forks with the parent). Verify, don't parrot.
- **Ignoring the existing stack** — "New shiny" bias. Always check first whether your current stack already solves this problem with comparable quality.
- **Missing the preconditions check** — A tool targeting multi-tool/multi-machine/multi-agent workflows is NO-GO for a single-instance user. The "engineering GO ≠ user GO" gate (Phase 5) catches this.
- **Forcing a recommendation from a 0/5 listicle** — When triage yields zero actionable picks for the user's stack, the right answer is "skip the listicle," not "pick the least-bad option and install it." Installing something to validate the roundup is a sunk-cost trap. A listicle's 0/5 result is data: it's targeting an audience that doesn't include this user. The user probably already has the working stack the listicle is selling.
- **Assuming compatibility** — Hermes v0.13 vs v0.14 API differences matter. Always search the local Hermes codebase for the APIs the plugin expects.
- **Overlooking maintenance burden** — A plugin that works today but has no tests, no CI, and one maintainer is a liability you'll pay for later.
- **Cost creep** — $0.008/call sounds cheap until you're making 500 calls/day for a trading bot.
- **Token efficiency claims** — Every CLI tool claims to save tokens. Verify by examining the actual output sizes.
- **Vendor benchmark with thin N** — A tool claiming "X% improvement" or "X wins / 0 losses" with N=10-50 trials is marketing until proven otherwise. Real benchmark standards want N in the hundreds at minimum for headline claims. A "12-0 in house rules" with N=12 is the kind of stat that gets printed in slides, not papers. **Check the methodology page**: how many decisive trials, how many models tested, what was the baseline. If the numbers come from a vendor-built benchmark on vendor-defined scenarios, treat as marketing.
- **No independent validation** — When the only sources confirming a benchmark are the vendor's own blog and README, the benchmark is the vendor's claim. Search for: independent blog posts, Medium articles, Reddit threads, GitHub issues with reproducible numbers, counter-articles that actually test the tool under adversarial conditions (e.g. "I uninstalled this and here's why"). A tool with one real third-party review is more credible than a tool with zero. RTK (89% reduction, 2,900 commands, multiple independent blog confirmations) vs. Plur (vendor benchmark, 19 decisive contests, no third-party reviews) is a textbook contrast.
- **"AI-native" marketing** — 90% of "built for agents" tools are just standard APIs with a CLI wrapper. Evaluate the DATA, not the packaging.
- **Generic tool re-labeled for SEO** — "Built specifically for X" in the headline but the README's supported-hosts list does not include X. The targeting is keyword-stuffing for the listicle search index. Cross-check the actual support list before taking the headline at face value.
- **Overclaim confidence from a single source** — "Found in one issue mention, sounds real" is not "verified real." A repo cited in an upstream issue may not exist, may be a private internal project, or may be a vaporware placeholder. **Before labeling a pick as REAL+USEFUL, verify the repo exists, is public, has a README, and ships a working install path.** If you only have one source, downgrade to "INVESTIGATE, don't install." The forum-debate pattern below catches this.
- **Relitigating a prior rejection** — If the user has said "I tried X and wasn't happy with it" (this session or any prior), drop it from the recommendation set immediately and don't push back. A negative prior verdict is a hard veto. The user reopens the topic when they want to, not when the agent decides the verdict was wrong.
- **Recommending based on benchmark, not on the user's actual usage profile** — A tool can have a great benchmark for a use case the user doesn't have. RTK claims 89% reduction on `cargo test` output — if the user never runs `cargo test`, the benchmark is irrelevant. Always check what the user *actually* runs. See "Empirical verification via session analysis" below.

## Phase 5b — Forum-Debate Stress Test (model disagreement before recommending)

When uncertain about the strength of a recommendation, model a forum debate BEFORE delivering the verdict. This is not "let me hedge" — it's a structured adversarial pass that surfaces evidence weaknesses the original analysis missed.

**When to use it:**
- Two or more picks in a list, and the user asks "which are actually worth it"
- You've labeled something "real" or "useful" but only have one source
- The recommendation depends on assumptions you haven't verified
- The user explicitly asks "model a debate on this"

**How to run it:**

1. **One thread per pick.** For each item you're about to recommend, open a thread.

2. **Three voices per thread:**
   - **@op (the install advocate)** — restate the case for installing, citing the evidence you have.
   - **@neon_audit (the steelman)** — strengthen the case. What's the strongest argument FOR?
   - **@kernel_therapist (the critical)** — attack the recommendation. What evidence is missing? What assumptions are unverified? What is the user actually doing?
   - **@op (honest update)** — after hearing the critic, restate what you actually know vs what you assumed. This is the most useful post.

3. **@moderator_verdict** — summarize: evidence quality (STRONG / WEAK), fit to user (HIGH / MEDIUM / LOW), and final action (install / investigate / defer / skip).

4. **At the end, deliver a revised recommendation** that may differ from the original.

**What it catches that a straight recommendation misses:**

- Single-source evidence masquerading as "verified" — the critic forces you to admit you only read one issue
- Assumptions about user behavior you haven't checked — the critic asks "does the user actually do this?"
- Overclaim on confidence — a list of 3 picks that all read as "GO" almost always has 1-2 that should be "INVESTIGATE"

**Pattern from real evaluation:** A tool-evaluation session recommended 3 picks (RTK, Nightwire, entroly-context-optimizer) framed as a "signal-rich pick." Forum-debate stress test exposed that 2 of 3 had only N=1 evidence (one issue mention each, never directly verified), and the third (RTK) was the only one with real benchmark data and independent validation. Final ranking: 1 GO with caveats, 1 investigate, 1 defer. Confidence recalibrated honestly.

**Pitfall — don't skip because "I already analyzed it":** The debate costs ~3 minutes and routinely surfaces one assumption that, if wrong, would make the recommendation actively harmful. It's the cheapest insurance against confident-wrong answers.

## Phase 5c — Empirical Verification via Session Analysis (the user's actual usage profile)

A tool's benchmark tells you its capability. The user's session DB tells you whether the capability is *applicable*. When recommending a tool that targets a specific use case (shell output compression, large file reads, broad web extracts, multi-tool memory), **verify the use case actually exists in the user's history before recommending.**

**How to query the session DB:**

Sessions are stored as JSONL at `~/.hermes/sessions/*.jsonl`. Each line is a message in a session. The relevant fields:

```python
import json, glob
from collections import Counter

files = sorted(glob.glob('/root/.hermes/sessions/*.jsonl'))

# Tool calls live in assistant messages
for line in open(file, 'r', errors='ignore'):
    obj = json.loads(line)
    for tc in obj.get('tool_calls', []):
        name = tc.get('function', {}).get('name', '')
        # count: tool_call_count[name] += 1

# Tool results live in role=tool messages
if obj.get('role') == 'tool':
    name = obj.get('tool_name') or obj.get('name') or ''
    content = obj.get('content') or ''
    size = len(content) if isinstance(content, str) else 0
    # count: tool_result_total_bytes[name] += size
```

**What to look for:**

- **Tool call frequency by name** — which tools does the user actually call?
- **Tool result size distribution by tool** — which tools return large outputs?
- **For shell commands specifically:** the first word of each command (cargo, git, find, grep, kubectl, docker, etc.) — does the user run the high-output commands the tool is designed for?
- **Top result-size outliers** — find the 1-2 calls that dominate context cost (often a single repeated skill load, or a single repeated search)

**What it kills:**

- Tools with great benchmarks for a use case the user doesn't have (RTK for a user who runs no `cargo test`/`git log` on long histories)
- Tools that solve a problem the user's other tools already solve (a memory layer for a user with Mnemosyne + USER.md + curator)
- Tools that would overlap with high-frequency, low-cost existing tools (a search tool when the user already uses `search_files` heavily)

**Pattern from real evaluation:** A tool-evaluation session recommended RTK (rtk-hermes) as a clear install based on the 89% noise-reduction benchmark. Empirical session analysis found the user's shell commands average 1.7 KB per call, with 0 calls over 100 KB and zero `cargo`/`npm`/`kubectl`/`docker` commands in 82 sessions. The benchmark use case (compressing huge `cargo test` output) didn't exist in the user's workflow. **The recommendation flipped from GO to NO-GO based on actual usage data, not benchmark claims.** The larger context-eaters in the user's sessions turned out to be `skill_view` (25.5% of tool result bytes), `session_search` (14.9%), and `read_file` (14.0%) — none of which RTK addresses.

**When to skip this analysis:** if the tool targets a generic capability (file sync, password manager, note-taking) rather than a use case, session analysis is less informative. The pattern is most useful for tools with benchmark-driven marketing ("saves 80% on X" where X is a specific workload).

**Save the analysis under `references/session-analysis-<toolname>.md`** when it changes a recommendation, so future sessions can re-validate without re-querying.

## Phase 5d — Solve With Existing Capabilities Before Proposing New Tools

The user has a strong preference: **edit or use existing capabilities before adding new tools/skills/plugins.** This is a default, not a one-time preference. When the user asks for an optimization, audit what they already have first.

**The hierarchy (use the highest that's sufficient):**

1. **Behavior change** — same tools, different parameters, tighter queries, smaller windows. E.g., `session_search` with `limit=2` instead of broad discovery; `read_file` with `offset`/`limit` to truncate.
2. **Configuration change** — adjust defaults in `~/.hermes/config.yaml`, add `AGENTS.md` rules, set `MEMORY.md` conventions. No new artifacts, just a new line.
3. **Edit existing skill/tool** — trim a bloated SKILL.md, split into core + `references/`, tighten frontmatter `description` to reduce load frequency. The artifact already exists, you're modifying it.
4. **New skill/tool** — only when the above three are insufficient. **Always pair with an explicit cost: "this adds N skills/plugins/dependencies to the stack."**

**Pitfall — "New shiny" bias:** When you have a fluent `skill_manage` or `terminal` tool, the path of least resistance is to install something new. The user has explicitly flagged this as spaghetti-code risk: "I really don't like to be collecting a medley of things and then end up having spaghetti code later on down the line." A recommendation that requires 3+ new skills/plugins to implement is almost always wrong — refactor the question.

**Pitfall — Counting "already have" as a free win:** If the existing solution requires behavior change the user has to remember (e.g., "always pass `limit=2` to session_search"), that friction is real. Configuration changes (set the default once) are cheaper than behavior changes.

## References

See `references/` for session-specific evaluation transcripts:
- `hermes-lcm-audit.md` — Full audit of Lossless Context Management plugin (DAG-based context engine), installed and verified
- `agent-data-evaluation.md` — Evaluation of agent-data CLI for quant trading use case (NO-GO: wrong data categories)
- `browse-sh-evaluation.md` — Evaluation of browse.sh browser automation CLI (conditional: needs Browserbase key for protected sites)
- `doga-evaluation.md` — Full audit of DOGA (probabilistic thinking layer plugin for Hermes): Monte Carlo engine, De Bono hats, recursive reasoning, security review, installation. GO verdict — installed and enabled.
- *(removed — evaluation deleted)*
- `autoned-vibe-trading-evaluation.md` — Evaluation of AutoHedge (thinnish swarms-library wrapper, hype) and Vibe-Trading (substantial HKU research project with DAG orchestration, grounding pre-fetch, ReAct worker, Shadow Account). Demonstrates the claims-vs-source gap inspection methodology.
- `skillopt-evaluation.md` — Evaluation of hermes-SkillOpt community repo. NO-GO as tool (built-in SkillOpt covers it), but the underlying Microsoft Research methodology (SkillOpt + SkillLens papers) generalizes to any LLM instruction optimization — extraction pipelines, backtesting, prompt engineering. Key insight: LLM judges are 46.4% worse than chance at evaluating skills by reading them.
- `rtk-plur-evaluation.md` — Hermes ecosystem X-listicle review (5 tools). Demonstrates the listicle review pattern (Phase 4b): per-item triage against the framework, ignore the viral framing, deep-dive the credible items. rtk-hermes: initial GO based on benchmark, **revised to NO-GO after empirical session analysis** (user's shell commands average 1.7 KB, no high-volume commands the benchmark targets). plur: NO-GO via preconditions check. Key lessons: vendor benchmarks with N=12-19 are marketing; engineering GO ≠ user GO when the user lacks the preconditions; benchmark GO ≠ user GO when the user doesn't have the use case the benchmark targets.
- `listicle-hermes-ecosystem-2026-06.md` — "5 不可不装的 Hermes 插件" Chinese-language listicle review. 0/5 GO result once dead-fork detection (compare API), prior-rejection (hermes-workspace already tried), preconditions check, and "generic tool re-labeled for SEO" (mnemo-cortex README does not list Hermes as a supported host) were applied. The listicle's "must install" framing hid a 27-star hobby project, a paid-skill marketplace, a frozen 8,403-commits-behind fork, and a mis-targeted memory tool. Lesson: a 0/5 triage result is a real outcome, not a failure to find a recommendation.
- `session-analysis-technique.md` — How to query `~/.hermes/sessions/*.jsonl` to find what the user actually uses (tool call frequency, result size distribution, shell command first-words). The empirical-verification step that complements the framework.
