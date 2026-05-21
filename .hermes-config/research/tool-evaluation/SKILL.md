---
name: tool-evaluation
description: Systematic methodology for evaluating third-party tools, plugins, projects, and services for integration fit — code audit, compatibility check, stack-overlap analysis, and recommendation. Covers the full lifecycle from initial curiosity to go/no-go decision.
version: 1.0.0
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

### Phase 2 — Depth Check (does it work?)

1. **Code structure** — Clone or browse the repo. Look at:
   - File count, module decomposition, architecture quality
   - Is engine.py 300 lines or 3000? (monolith vs modular)
   - Does it have tests? How many? What do they cover?
2. **CI status** — Does CI pass? Run on multiple Python/node versions? Linting?
3. **Test quality** — Actual assertions against real behavior, or just "imports fine"?
4. **Dependencies** — Heavy frameworks (PyTorch, Playwright) or lightweight (stdlib + requests)?
5. **Installation path** — `pip install`, `npm install`, `git clone`, docker?

### Phase 3 — Compatibility Check (does it work HERE?)

1. **Hermes version** — Does the required Hermes API exist in our version? Check via `search_files(pattern=..., path=/usr/local/lib/hermes-agent)`
2. **Python/Node version** — Is our runtime compatible?
3. **Existing conflicts** — Does it overlap with something already installed?
4. **Config integration** — What config changes (`config.yaml`, `.env`) are needed?
5. **Plugin path** — User plugin dir? Context engine dir? Built-in? Symlink?

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
