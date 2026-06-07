---
name: engineering-discipline
description: "Behavioral guidelines for rigorous, minimal, surgical coding — think first, keep it simple, touch only what's needed, verify at every step."
version: 1.0.0
author: Derived from CLAUDE.md guidelines
license: CC0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-conduct, discipline, simplicity, goal-driven, surgical-changes]
    related_skills: [writing-plans, requesting-code-review, test-driven-development, systematic-debugging, workflow-pattern-kit]
---

# Engineering Discipline

A set of behavioral guidelines for coding work, derived from the CLAUDE.md
specification. Load this skill at the start of any non-trivial coding task to
establish the operating contract before touching files.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks
(one-line fixes, obvious config changes), use judgment and proceed.

## The Principles

### 1. Think Before Coding

> Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing anything:
- **State your assumptions explicitly.** If uncertain, ask.
- **Surface multiple interpretations** — don't pick the most likely one silently.
  Present alternatives and let the user decide.
- **If a simpler approach exists**, say so. Push back when warranted.
- **If something is unclear, stop.** Name what's confusing. Ask.

**Pitfall:** The default LLM behaviour is to infer the most likely interpretation
and run with it. This rule explicitly countermands that — present options first.

**Pitfall — "Proceed" ≠ approval of your preferred option:** When you offer
the user multiple alternatives (Option A, Option B, Option C) and they respond
with a vague affirmative ("proceed," "go ahead," "OK," "sure"), do NOT assume
they chose your recommended option. Silent assumption of unstated preferences
causes frustration when the user had a different option in mind. Instead,
confirm: "Which option? A, B, or C?" One clarifying turn saves a correction turn.

**Pitfall — Distinguish asking from executing:** When the user asks a question
that starts with "how" or requests an explanation ("How does X work?", "How do
I do Y?"), **answer the question first**. Do not jump to running commands,
installing things, or making changes unless the user explicitly asks you to
act. A question about how something works is a request for information, not a
mandate to execute. If you're unsure whether they want explanation or action,
offer the explanation and ask if they'd like you to proceed.

### 2. Simplicity First

> Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

**Self-check:** "Would a senior engineer say this is overcomplicated?" If yes,
simplify.

### 3. Surgical Changes

> Touch only what you must. Clean up only your own mess.

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, **mention it** — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Do NOT remove pre-existing dead code unless asked.

**The test:** Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

> Define success criteria. Loop until verified.

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan up front:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it
work") require constant clarification.

### 5. Side-Effect Verification

> After every mutation, read back and confirm. Never trust generated text as
> evidence of a write.

LLMs can generate text that *looks like* a file entry, log line, or config
change without ever calling a mutation tool. This is not a bug — it is a
fundamental property of generative models: they produce plausible text, not
verified state transitions. The system prompt and tool boundary create the
illusion of execution; the model does not natively experience "did the write
happen?" as a grounded fact.

**Rules:**

1. **After every file write, patch, or append** — immediately read back the file
   and grep for the intended change. Confirm the line exists at the expected
   location. Do not rely on the tool's return message alone.

2. **After every removal or deletion** — read back the file and confirm the
   item is gone. If a tool returns "success" but the content is unchanged,
   retry with the correct string match.

3. **After any stateful operation** (config change, service restart, env var
   export, permission change) — verify the new state independently before
   reporting success. `cat` the config, `curl` the endpoint, check the process
   list.

4. **Do not use print-only commands as write substitutes.** `python3 -c
   "print(new_content)"` sends text to stdout, not to the file. The terminal
   output looks like a successful write but the file is untouched. Use
   purpose-built CLI tools (`write_file`, `patch`, `sed -i`, `euphy-add`) or
   the `write_file`/`patch` Hermes tools instead.

5. **When delegating tasks to subagents**, require verification handles in the
   return summary: absolute path + line number for file writes, URL + status
   code for HTTP calls, PID + port for service starts. Verify these yourself
   — subagent self-reports are not grounded evidence.

**Pitfall:** This rule costs a read-back call per write. That is intentional.
A single undetected hallucinated write can waste more time than a hundred
read-backs. The cost is a tool call and a few hundred tokens; the failure cost
is corrupted state that propagates silently.

### 6B. Model Validation — Backtesting & ML Discipline

> Define verifiable success criteria. Use chronological splits. Evaluate on held-out data exactly once. Prefer expectancy over hit rate.

**The structural problems with the May 2026 SwingCatcher scripts (build_swingcatcher.py) that prompted this section:**

- **No train/test split**: Thresholds were tuned AND evaluated on the same 431 signals. The reported 72.7% hit rate is overfit — it will degrade on unseen data. A proper validation split is mandatory for any backtest.
- **Hit rate as sole metric**: A config that "wins" 70% of trades but loses 3× more on the 30% losers is a losing strategy. **Expectancy** (hit_rate × avg_win − miss_rate × avg_loss) captures this; hit rate alone cannot. Always compute expectancy with realistic TP/SL targets.
- **Manual threshold grid doesn't scale**: Pair/triple feature sweeps explode combinatorially. The current 24-feature grid is already unmanageable; adding OI, funding rate, and taker ratio features makes it impossible. Use LightGBM or XGBoost — gradient boosted trees handle feature interactions natively and provide feature importances without manual pair-by-pair testing.
- **Close+48 fixed-horizon labels miss path dependency**: A signal that spikes +2% at bar 22 then retraces to flat by bar 48 is labeled "miss" — but a take-profit order would have captured the full 2%. Use **triple-barrier labeling** (from López de Prado's Advances in Financial ML): scan forward bar by bar, record the FIRST of (TP hit, SL hit, or timeout). This produces path-dependent labels that reflect actual order behavior.
- **Separate models per direction**: Crypto has asymmetric up/down dynamics. A single model with a "direction" dummy variable plus fragile SHORT_HIGHER/SHORT_LOWER direction lists is the wrong architecture. Train two independent models (long model, short model) — cleaner, more accurate, and avoids feature-direction confusion.

**Required validation steps for any backtesting or classification pipeline — run each in order and report all results:**

1. **Chronological split only** — Train (60%), Val (20%), Test (20%). Random cross-validation leaks future info into training. Time series requires temporal order.
2. **Val is for tuning, Test is for reporting — one look only** — If the test result disappoints, do NOT retune. That enforces honest evaluation. The test number is your confidence for deployment. If you cannot accept a low test number, you do not have a deployable strategy.
3. **Permutation test** — Shuffle labels and retrain the same pipeline. Compare real AUC to the distribution of shuffled AUCs. If real AUC is <2 σ above the shuffled mean, the model is finding noise — disqualified.
4. **Time-decay check** — Score the model on test data split chronologically in halves. If the first half scores AUC=0.65 and the second half AUC=0.51, the edge is decaying. Document this regardless — it's a known characteristic of ML in crypto.
5. **Calibration check** — When the model predicts "70% probability", is it right ~70% of the time? Use `sklearn.calibration.calibration_curve`. If calibration is off, apply Platt scaling or isotonic regression.
6. **Expectancy > Hit Rate** — A model can show 70% hit rate and negative expectancy if the 30% losers lose 3× what the winners gain. Compute: `E = (hit_rate × TP_pct) − ((1−hit_rate) × SL_pct)`, then adjust for the zero-outcome case (timeout). A positive E after realistic TP/SL is the bar.
7. **Label with path dependency** — Use triple-barrier labeling (check each forward bar for TP hit, SL hit, or timeout), NOT a fixed-horizon snapshot like `close[48]/close[0]`.
8. **Separate Long/Short models** — Two models, two training runs, two evaluation reports. Do not use a single multiclass classifier with a "direction" feature.

**When to deploy this principle:**
- Any time you write a backtest, label signals, or train a classifier on trading data
- When evaluating whther a strategy "works" — hit rate alone is never sufficient
- When adding new features (OI, funding, taker ratio) to an existing model — re-validate from step 1

### 6C. Context Retention, Data Recall & Session Anchoring

> Once a theory is disproven, strike it. Before proposing anything, verify what's already been established. Never reconstruct plausible-sounding explanations from partial data when authoritative memory exists.

This is the single most impactful behavioral fix for complex, multi-session investigations:

- **Daily-reset anchoring — see `orchestration-workflow` (Pre-Flight: Session Anchor) for the formal step sequence.** That section covers the turn-zero procedure (session_search → cross-check memory → verify install-state → then speak). This section covers the *in-conversation* data-recall discipline.

- **Before introducing any hypothesis, theory, or explanation in a conversation**, check whether it was previously discussed and what was concluded. If you don't remember, search sessions first.

- **Data recall discipline** — Before answering ANY factual question about past analysis work (data sources, counts, pipeline stages, file locations):
  1. Run `mnemosyne_recall(query="relevant topic")` FIRST — memory contains compressed authoritative facts that session search can miss.
  2. Check ALL storage locations — do not conclude "data is gone" from a single search in the project directory. Always also check `/root/.hermes/cache/documents/` for cached file attachments.
  3. Explicitly state which data source/feature tier/pipeline stage you're referencing — if there are multiple similar datasets (e.g., 7-feat, 14-feat, 24-feat exports; spot vs perp price data), disambiguate before making claims.
  4. Do NOT reconstruct plausible narratives to fill gaps in your search results. If you can't find the data, say so and ask the user where it is — don't guess where it "probably" went.
  
  **Failure mode (observed):** Files existed in cache but a narrow search only checked the project directory. I concluded "files are gone" and stitched together a wrong story about what the pipeline contained. The data was there the whole time in `/root/.hermes/cache/documents/` — I never looked for it.

- **Before introducing any hypothesis, theory, or explanation in a conversation**, check whether it was previously discussed and what was concluded. If you don't remember, search sessions first.
- **Once a theory is conclusively disproven by hard evidence** (compile error, chart confirmation, explicit user correction), strike it from the working hypothesis set. Do NOT reintroduce it in a later turn, even as a "what if" or "maybe the test was wrong." This includes theories that showed superficial evidence (e.g., signal count match) but failed the definitive test (timestamp-level validation against user's CSV).
- **When the user corrects you — on format, on conclusions, on approach — the correction is not a single-turn fix.** It must become a durable rule. If they say "stop doing X," embed "Do not X" as an explicit check in the relevant skill. Memory capture is necessary but not sufficient — skill updates lock in the lesson.
- **Trust the user on their own system — verify before counter-arguing.** When the user states something about their own system that contradicts your assumption (e.g., "marker-pdf is already installed," "we switched to a different model," "feature X doesn't work"), your first action MUST be a verification tool call — config check, filesystem stat, test run, or memory read — NOT a counter-argument or explanation of why they might be wrong. The user lives in their system daily. You have stale docs. Three common failure modes: (a) reading a stale config file instead of the authoritative source, (b) citing aspirational docs that don't match actual runtime behavior, (c) not reading your own memory notes before speaking. The fix is the same in all cases: tool call first, then speak.
- **Maintain a running list of dead-end theories** in the session's working context. When you catch yourself reaching for a disproven explanation, the list is your brake.
- **Before proposing a new analysis, ask yourself:** "Does this require the user to test something I could test myself?" If the answer is yes, rework the approach to minimize user effort. When the user says "why can't you do it?", they are telling you that you should have done it yourself.

**Pine Script delivery:** Every Pine Script I send must compile on first paste. Before posting:
1. Verify every variable is declared before use
2. Verify every function/input name matches exactly (no `useTp` when the input is `useTpToggle`)
3. Verify every `if`/`for` at body level works in v6 (ternary preferred)
4. Verify no tuple destructuring (`[a, b] =`) at the global scope
5. Trace every plotshape call — `series=` must be a valid expression, not a scope-limited variable

The user should not be my Pine compiler. A single compile error means I skipped a verification step.

### 7. Handling Reference Documents

When the user shares a document (spec, guideline, reference) without an explicit
instruction to act on it:

- **Treat it as material for discussion**, not as a prompt to implement.
- Do NOT modify memory, write files, or take action based on it unless asked.
- If in doubt, ask: "Is this for reference, or would you like me to do something
  with it?"

### 7. Cleanup Verification (Post-Mortem Audit)

After uninstalling a service, removing a component, or cleaning up a legacy
installation, verify that no traces remain across ALL dimensions — not just
the obvious directory. A partial removal leaves stale configs, orphan processes,
port bindings, and cron artifacts that cause confusion months later.

**The audit checklist — check every dimension:**

```
[ ] Directory — rm -rf target directory
[ ] Systemd service — stop, disable, remove .service file, daemon-reload
[ ] Port binding — ss -tlnp | grep <port> → empty
[ ] Running processes — ps aux | grep <name> | grep -v grep → empty
[ ] Active configs — grep -rn <name> in config files → only expected hits
[ ] Cron jobs — check active cron definitions
[ ] Env files — grep <name> .env files → empty
[ ] Shell aliases/wrappers — check ~/.local/bin/, .bashrc, /usr/local/bin/
[ ] Binary linkage — which/type → not found
```

**For each hit found:** determine if it's an active reference (config being read)
or a passive reference (documentation, history). Eliminate active references;
leave passive ones only if the user explicitly declines cleanup.

**The cross-dimension check catches things single-dimension deletion misses:**
- A removed directory still has a stalled process holding the port
- A killed process restarts because systemd was left enabled
- A cron job references a removed URL or service endpoint
- An env file sets a binding that no longer serves anything

**Pitfall:** Docker installations often leave volumes, networks, and images
behind. `docker compose down -v` removes volumes; `docker system prune` cleans
dangling images. Verify with `docker volume ls`, `docker network ls`.

**Pitfall:** User-level systemd services (`~/.config/systemd/user/`) persist
separately from system-level services. Check both.

**Pitfall — Never rm -rf, use recycle bin:** The user requires all deletions to use the recycle bin, not permanent removal. Instead of `rm -rf <path>`, use:

```bash
mkdir -p /root/recycle-bin/$(date +%Y-%m-%d)
mv <path> /root/recycle-bin/$(date +%Y-%m-%d)/
```

This applies everywhere — work files, temp files, project directories. The recycle bin makes recovery possible if the user changes their mind. The only exception is session-specific temp files in project `temp/` dirs that the user explicitly agrees to delete.

**Pitfall — Temp dir cleanup discipline:** Some workloads legitimately need `/tmp/` (OCR pages at 300 DPI produce 25MB per page — 500 pages won't fit in a project `temp/` dir). The safety rule is:

1. Always use a **dedicated subdirectory** under `/tmp/`, not bare filenames: `TMPDIR=$(mktemp -d /tmp/<project>_XXXXXXXXX)`
2. Always add **`trap 'rm -rf "$TMPDIR"' EXIT`** immediately after creating the subdirectory. Guarantees cleanup on success AND failure (SIGTERM, crash, `set -e` abort).
3. Do NOT rely on `rm -f` at the end of a script — if `set -e` is active, any intermediate error skips the cleanup line.
- When in doubt, prefer a project `temp/` subdirectory for files under 100MB total. Use `/tmp/` with trap only when the intermediate data is too large.

Canonical pattern:
```bash
TMPDIR=$(mktemp -d /tmp/project_temp_XXXXX)
trap 'rm -rf "$TMPDIR"' EXIT
cd "$TMPDIR"
# ... work ...
mv output.txt /path/to/final/
# EXIT fires automatically, removing $TMPDIR
```

### 8. Codebase Analysis Protocol — Hype vs Substance

> READMEs market; codebases reveal. Star counts reflect virality, not quality.
> Before concluding a project is useful, verify at the code level.

When evaluating an unfamiliar OSS project (as done this session with browser-use and Vibe-Trading), use this sequence. Each step answers one question. Stop when you have enough evidence to form a judgment.

**Step 1 — README + metadata (what does it claim?)**
- Read the README critically. Count marketing claims vs technical specifics.
- Check the version number and release date. v0.1.x is a prototype.
- Note the author/org. Academic lab? Solo dev? Startup?

**Step 2 — pyproject.toml / package.json / Cargo.toml (what does it depend on?)**
- Dependencies reveal architecture: `swarms` library → thin wrapper; custom `swarm/` package → real orchestration.
- Check build system. Poetry? Hatchling? Raw setuptools? Indicates maturity.
- Look at optional dependencies. Not a quality signal but reveals priorities.

**Step 3 — Directory tree (what are the module boundaries?)**
- Run tree or list the top-level package dir. Each subdirectory is a concern.
- Count the ratio: configuration/prompts vs. actual execution code.
- A `prompts.py` with no `engine.py` means the repo is prompts-with-a-wrapper.

**Step 4 — Core source files (how does it actually execute?)**
- Read the main entry point (`__main__.py`, `cli.py`, `main.py`).
- Read the central orchestration file. Look for the actual loop: is it an LLM call in a for-loop, or is it a state machine with proper error handling?
- Count lines of core logic vs. lines of CLI/UI/README.

**Step 5 — Data models (what types reveal about design)**
- Read the Pydantic/dataclass models first. They are the ground truth of what the system considers important.
- Look for: proper error states, status enums, optionality in fields (reveals incomplete design), frozen/hashable types.

**Step 6 — Execution flow (how things actually run)**
- Trace one complete path: input → agent → tool call → result → output.
- Does it handle: rate limits, timeouts, partial failures, cancellation?
- Are there unit tests for the core loop, or just integration smoke tests?

**Step 7 — Tradeoff analysis (what's real vs presentation)**
- Separate the repo into three layers:\n    a. **Core logic** — the actual execution engine. Count LOC.\n    b. **Wrapper/UI** — CLI, rich formatting, REPL. Count LOC.\n    c. **Prompts/marketing** — system prompts, README claims, social proof.\n- If (b) + (c) >> (a), the repo is presentation-heavy.
- Star count ÷ age in months gives a rough viral coefficient. 10k stars in 1 month = hype wave. 9k stars over 2 years with incremental releases = real usage.

**Signals that separate substance from hype:**

| Hype pattern | Substance pattern |
|---|---|
| "Enterprise-grade" in README | Unit tests for error paths |
| Multiple LLM-powered agents | One critical agent with well-defined state machine |
| "Autonomous X" claim | Disambiguation of human-in-loop vs fully autonomous |
| AI-generated architecture diagrams | Actual module-level docstrings |
| "pip install and run" with no error handling | Graceful degradation on API failure |
| README demos of best-case success | Documented failure modes |
| One-person repo with 5k+ stars in 2 weeks | Academic lab or team with incremental releases |

**Pitfall — Presentation layer confusion:** A repo can have a polished CLI (Rich formatting, ASCII art welcome screen) but the actual orchestration is 50 lines of `director_agent.run(task)`. The presentation layer makes it look substantial. Always count core-logic LOC separately from UI LOC.

**Pitfall — Star count as a proxy:** Stars measure interest, not correctness. The swing-trading, autonomous-agent, and "vibe coding" categories in particular have inflated star counts because they are exciting to browse, not because the code works. A 2.9k-star repo can be 300 lines of prompts; a 200-star repo can be a well-engineered crate. Always verify before reporting.

**Pitfall — Dependency-driven substance illusion:** A repo that depends on `swarms`, `langchain`, or `llama-cpp-python` inherits that library's capability in README claims. The actual code may only call `agent.run()` — the sophistication is in the dependency, not the repo. Check what the *repo itself* implements, not what its imports can theoretically do.

**When to use this protocol:**
- The user asks "is this useful or just hype?" about a specific project
- You need to understand an unfamiliar codebase before integrating or forking it
- Evaluating whether to recommend a tool, adopt a pattern, or adapt an architecture
- Any time star count would be the first signal but shouldn't be the only one

**Related skills:** `workflow-pattern-kit` — the four patterns in that kit were extracted using this analysis protocol.

## 9. MIT Component Extraction — Clean Import from OSS Repos

> *Eval the project (section 8). If the core value is in its pure-Python modules, extract them. Don't run the whole Docker stack for 200 lines of logic.*

This is the natural follow-on to the Codebase Analysis Protocol (section 8). Once you've identified that a repo's value lives in specific pure-Python functions (barrier detection, quality gates, extraction logic), the question becomes: how do you use that value without adopting the full project's deployment model?

### The extraction flow

```
OSS project (MIT/Apache/BSD)       Your Hermes-native module
├── scraper-svc/                    ├── barrier_classifier.py
│   └── scraper/                    │   (pure functions, stdlib only)
│       ├── fetch.py  ──→  ──→  ──→│
│       │   _classify_barrier()     │   classify_barrier()
│       │   BarrierInfo             │   BarrierInfo
│       └── extract.py  ──→  ──→  ├── quality_gates.py
│           assess_quality()        │   assess_quality()
│                                   │   (stdlib + regex only)
├── Dockerfile                      │
├── docker-compose.yml              │   (not copied)
├── agent-svc/, browser-svc/, ...   │   (not copied)
└── 6 other containers              │   (not needed)
```

### Steps

**Step 1 — Identify the pure-Python core**

Look at the repo's directory tree. Services that are just Python FastAPI/Flask apps without Docker-specific dependencies are candidates. The `scraper-svc/` in a crawling framework is usually a good target — it's a plain HTTP handler with the real logic in `fetch.py`, `extract.py`, etc.

Not candidates: services that import Playwright, headless browser libraries, or GPU-specific packages. Those are Docker-wrapped for a reason.

**Step 2 — Verify the license allows extraction**

Only extract from MIT, Apache 2.0, BSD, or CC0 licensed repos. Never GPL/AGPL unless the user explicitly accepts the license implications. Check the LICENSE file or `license:` in pyproject.toml. If there's no license file, assume not safe to copy.

**Step 3 — Extract the source files**

Copy only the files that hold the intelligence. Every file you DON'T copy is a dependency you don't need to manage.

| Include if | Exclude if |
|---|---|
| Pure functions with no I/O | Requires Playwright/Browser service |
| Dataclass/Pydantic models | Talks to external Docker containers |
| Stdlib + common deps only | Requires GPU or OS-level packages |
| Regex-based analysis | Coupled to parent project's config/env |

**Step 4 — Strip dependencies**

- Remove imports that reference other services in the same repo (e.g., a scraper importing the project's own `client.py` that calls the Docker API).
- Replace the project's custom cache layer (Valkey/Redis) with simpler: `functools.lru_cache`, `cachetools.TTLCache`, or plain SQLite.
- For HTTP: replace async `httpx` with `urllib.request` from stdlib, or keep `requests` as a declared dependency.

**Step 5 — Rename and re-export**

- Give the module a clean descriptive name (`barrier_classifier.py`, not `fetch.py`).
- Write a module docstring with source attribution: `Extracted from {project} v{version} (MIT License)`.
- Export only the public API the parent project would expose.

**Step 6 — Test independently**

```python
from barrier_classifier import classify_barrier
result = classify_barrier(url='https://x.com/cf_chl', title='Just a moment...')
assert result.detected and result.barrier_type == 'cloudflare'
print('Extracted module works standalone')
```

**Step 7 — Wire into the workflow**

- Import in the relevant Hermes skill's script.
- Register with ToolRegistry if Hermes tools should discover it.
- Ensure the module is on `sys.path` from where the driver (e.g., `escalate.py`) imports it.

### When to use this vs. running the full project

| Extract (this pattern) | Run the full project |
|---|---|
| Core logic is <500 LOC | Core logic is >5000 LOC |
| Pure functions, no I/O | Needs browser, GPU, or external service |
| Can be tested standalone | Needs its own DB or message queue |
| Low-maintenance (stdlib+regex) | High-maintenance (Docker, CI, upgrades) |
| VPS has tight RAM | Plenty of RAM for Docker stack |

### Verification

Before declaring the extraction complete:
1. `python3 -c "from {module} import ...; print('OK')"` — clean import
2. Run core functions against known inputs — same output as parent project
3. Verify no Docker/cache/network calls triggered by basic operation
4. Check LOC of extracted files vs. parent repo — expect 80-90% reduction

### Pitfalls

- **License creep**: A MIT project may have AGPL dependencies. Check `requirements.txt` for dependency licenses.
- **Hidden Docker coupling**: A function that looks pure might try to connect to `http://valkey:6379`. Check every import and URL string literal.
- **Version drift**: Extracted code is a snapshot. Document the source commit hash in the module docstring for future diffing.
- **Configuration coupling**: Functions reading `os.environ` should accept params instead. Add defaults at the module top.
- **Resist extracting the full repo**: If the core logic is <500 lines but Docker setup is 5000, extract. If the core logic IS 5000 lines, run it as-is.

### Related skills

- `engineering-discipline` — this section (MIT extraction follows codebase analysis)
- `workflow-pattern-kit` — extracted modules often integrate with ToolRegistry/OutputGate/DAG
- `groktocrawl-escalation` — real-world example (barrier_classifier.py, quality_gates.py extracted from GroktoCrawl)

---

## 10. User Preference: Solve With Existing Capabilities Before Proposing New Tools

> The user has a strong, durable default: **edit or use existing capabilities before adding new tools/skills/plugins.** This is a workflow override, not a one-time preference.

**Source of the rule (user quote):** *"I really don't like to be collecting a medley of things and then end up having spaghetti code later on down the line."*

**The default hierarchy for any "how do I..." or "let's optimize X" request:**

1. **Behavior change** — same tools, tighter parameters, smaller windows, better queries. No new code, no new artifacts.
2. **Configuration change** — adjust defaults in `~/.hermes/config.yaml`, add an `AGENTS.md` rule, set a `MEMORY.md` convention. One line.
3. **Edit existing skill/tool** — trim a bloated SKILL.md, split into core + `references/`, tighten frontmatter. The artifact already exists, you're modifying it.
4. **New skill/tool** — only when 1-3 are insufficient. Always pair with explicit cost: "this adds N skills/plugins/dependencies."

**When proposing anything in tier 4, name the cost explicitly.** A recommendation that requires 3+ new skills/plugins to implement is almost always wrong — refactor the question.

**Pitfall — fluent install as default path:** When you have `skill_manage` and `terminal` available, the path of least resistance is to install something new. Resist. The user has flagged this as spaghetti-code risk. If a recommendation needs more than one new skill to implement, it's probably the wrong recommendation.

**Pitfall — mistaking friction for cost:** A behavior change the user has to remember ("always pass `limit=2` to session_search") has real friction. Configuration changes (set the default once) are cheaper than behavior changes. When recommending behavior changes, suggest a config or memory line that makes the default stick.

## 11. Skill Activation: Every New Skill Needs a Trigger

> A skill without an automatic trigger is a dead skill. Don't create it.

**Source of the rule (user quote):** *"how will this be used though? I don't want to add a dead skill and vault."*

When creating a new skill, require at least ONE of these before shipping:
- **Cron job** — scheduled scan/action that runs without agent memory
- **Hook** — pre/post trigger on existing workflows (delegation, tool calls)
- **Soul injection** — loaded as part of the agent's operating model so it's always in context
- **User-invoked command** — slash command or explicit trigger the user controls

**The test:** "If I forget this skill exists tomorrow, will it still do something?" If the answer is no, it's dead. Either add a trigger or don't create it.

**Pitfall — manual-only skills:** A skill that requires the agent to remember to load it and run it will work for one session and then be forgotten. The agent's context is finite; untriggered skills get crowded out by active tasks.

**Pitfall — "I'll add the trigger later":** Later never comes. The trigger is the skill. Ship them together or don't ship.

## When To Load This Skill

- At the start of any non-trivial coding task (feature, refactor, bug fix)
- Before writing plans (`writing-plans` skill)
- Before delegating tasks to subagents
- Whenever user shares a specification or requirements document
- Whenever performing file mutations that will be reported to the user as completed
- When proposing new skills, plugins, or tools as solutions (load with `tool-evaluation`)

## Reference Files

These patterns are baked into the operating model. The `workflow-pattern-kit` skill implements them as reusable Python modules. Load it alongside this skill for any non-trivial workflow.

**OutputGate before completing any agent deliverable.** Every result from a subagent, Kanban worker, cron job, or agent task runs through OutputGate.check_deliverable() before being accepted. If the gate returns a reason string, the output is not done — send it back for rework. This catches plan stubs, mock data, raw tool envelopes, and empty results.

**DAG for parallelism.** Any task with ≥2 independent subtasks gets a DAG. Research topic A + research topic B run in parallel; synthesis runs when both finish. Multi-page OCR uses the DAG. Any fan-in pattern (multiple sources → one summary) uses the DAG. When a task fails, downstream tasks are skipped (cascade) but parallel tasks in the same layer are unaffected.

**ToolRegistry for new agent tools.** New actions use the registry: typed Pydantic params, signature-based context injection (browser_session, file_system, etc.), domain filtering. Tool functions never import infrastructure — they receive injected context. This makes tools testable (pass mocks) and swappable (change the injector, not 15 tools).

**LoopDetector for interaction loops.** Any browser, search, or API-call loop tracks actions with LoopDetector. Before each LLM call, check get_nudge_message() and inject the nudge if present. Escalating nudges at 5/8/12 repeats. Prevents wasted token budgets on stuck loops. Only applies to long-running loops (20+ actions), not trivial single-turn tasks.

**Do NOT load for:** conversation-only modes, research, reading code without
modifying it, trivial one-line changes.

**Exception:** Load section 8 (Codebase Analysis Protocol) independently when
evaluating an unfamiliar OSS project, even if no coding work follows. That
section is standalone and does not require loading the full skill.

## Reference Files

- `references/CLAUDE.md` — the full source document these guidelines derive from
- `references/hermes-migration-pattern.md` — Hermes installation transfer to a new machine (backup, optimize, restore)

## Related Skills

- `workflow-pattern-kit` — reusable agent architecture patterns (tool registry, loop detection, output gates, DAG orchestration). The four patterns in that kit were extracted using the Codebase Analysis Protocol in section 8 above. Use together when evaluating an OSS project and then building from its patterns.

## Verification

This skill is working if:
- Fewer unnecessary changes in diffs
- Fewer rewrites due to overcomplication
- Clarifying questions come before implementation rather than after mistakes
- Orphan cleanup is scoped to what your changes made unused
- Codebase analysis uses the 7-step protocol from section 8 rather than README-first impression
- Pattern extractions are scoped to actual code paths, not star count or README claims
