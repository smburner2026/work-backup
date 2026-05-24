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
    related_skills: [writing-plans, requesting-code-review, test-driven-development, systematic-debugging]
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

### 6C. Context Retention & Data Recall

> Once a theory is disproven, strike it. Before proposing anything, verify what's already been established. Never reconstruct plausible-sounding explanations from partial data when authoritative memory exists.

This is the single most impactful behavioral fix for complex, multi-session investigations:

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

## When to Load This Skill

- At the start of any non-trivial coding task (feature, refactor, bug fix)
- Before writing plans (`writing-plans` skill)
- Before delegating tasks to subagents
- Whenever user shares a specification or requirements document
- Whenever performing file mutations that will be reported to the user as completed

**Do NOT load for:** conversation-only modes, research, reading code without
modifying it, trivial one-line changes.

## Reference Files

- `references/CLAUDE.md` — the full source document these guidelines derive from
- `references/hermes-migration-pattern.md` — Hermes installation transfer to a new machine (backup, optimize, restore)

## Verification

This skill is working if:
- Fewer unnecessary changes in diffs
- Fewer rewrites due to overcomplication
- Clarifying questions come before implementation rather than after mistakes
- Orphan cleanup is scoped to what your changes made unused
