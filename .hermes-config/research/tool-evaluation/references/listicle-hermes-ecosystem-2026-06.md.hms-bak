# "5 不可不装的 Hermes 插件" — Listicle Review

**Date:** 2026-06-05
**Source:** X post claiming 5 "must install" Hermes plugins
**Verdict (per item):** 0/5 GO once prior-rejection + preconditions + dead-fork detection applied
**Outcome:** Honest answer was "skip the listicle entirely" — not "pick the best of bad options."

## The listicle as posted

| # | Repo | Listicle claim | Headline tag |
|---|---|---|---|
| 1 | `Felix-Forever/hermes-agent-desktop` | Multi-agent desktop client, 20 specialists | "Single agent → AI team" |
| 2 | `amanning3390/hermeshub` | Community skill registry, hermeshub.xyz | "Skill discovery center live" |
| 3 | `outsourc-e/hermes-workspace` | Web UI: chat + memory + skills + terminal | "Agent command center arrived" — **"3,400+ stars"** |
| 4 | `morph-labs/hermes-agent-fork` | Production-deployment fork | "Evolution branch, pro version" |
| 5 | `GuyMannDude/mnemo-cortex` | Persistent memory for Hermes | "Agent finally remembers you" |

## Per-item triage

### 1. Felix-Forever/hermes-agent-desktop — REAL, NO-GO

**Real:** Yes. **Stars:** 27 (last push 35 days ago). Built with pywebview, claims 20 built-in AI agents with a PM orchestrator.

**Preconditions check:** User already runs the **official Nous Research Hermes Desktop app** (Electron, current v0.15.2) connecting to VPS gateway :8642 + dashboard :9119. The "20 specialists" pitch is a feature set the official desktop app does not have, but the user has not asked for multi-agent orchestration and the existing app covers the chat + file download use cases. **Overlaps with the official desktop app, and the official one wins by maintainer trust and integration depth.**

### 2. amanning3390/hermeshub — REAL, MARGINAL

**Real:** Yes. hermeshub.xyz is live. README says "curated skills registry, security-scanned against 65+ threat rules."

**Yellow flags:**
- The "premium skill download" path uses `402 Payment Required` with x402 crypto-payment protocol. The "community" framing hides a paid skill marketplace.
- The user's existing `hermes skills` CLI + bundled 100+ skills already covers the discovery path. Marginal value-add over what Hermes ships.

**Preconditions:** User has not asked for a skill marketplace. The CLI path works.

### 3. outsourc-e/hermes-workspace — REAL, REJECTED PRIOR SESSION

**Real:** Yes. **Stars: 5,407** (listicle claimed 3,400+ — wrong direction; under-counted). Active maintenance, 10 contributors, recent commits (2026-05-24), v2.3.0 release (2026-05-08), SECURITY.md present, attaches to existing gateway on :8642 + dashboard :9119. **The technical verdict would have been GO.**

**Hard veto:** User said **"I think we tried installing that previously and it didn't work right or I wasn't really happy with it."** This is a prior rejection, captured in `memory` and in the user profile. **Drop from recommendation set. Do not relitigate, do not ask "what was wrong," do not try to talk the user into it.** A prior negative verdict is a hard veto unless the user reopens it.

**Lesson:** `session_search` for "hermes-workspace" before recommending was the right move. The verdict flipped from "the only one I'd install" to "off the board" with one user sentence. The framework's stack-overlap + preconditions checks would have missed this — the prior-rejection check is a third axis that should always run.

### 4. morph-labs/hermes-agent-fork — REAL, DEAD FORK

**Real:** Yes. **Stars: 24.** 0 open issues ever, 0 releases, no security policy, last commit 2026-03-18.

**Compare API call (the kill shot):**
```bash
gh api repos/morph-labs/hermes-agent-fork/compare/NousResearch:main...main \
  --jq '{ahead_by, behind_by, total_commits: (.commits | length), files_changed: (.files | length)}'
# → {"ahead_by":0,"behind_by":8403,"total_commits":0,"files_changed":0}
```

**Verdict: instant NO-GO.** `ahead_by == 0 && behind_by > 1000` = frozen snapshot of upstream with no original work, drifting further every day. The "production deployment fork" framing is marketing. The v0.2.0 "release notes" file is just a copy of upstream's changelog. Installing this = running Hermes Agent from March 18 with 8,403 missing commits of bug fixes and security patches. **If you want the upstream code, install NousResearch/hermes-agent directly.**

**Lesson:** Always run the compare API for repos where `.fork == true`. The number of stars is irrelevant — 24-star dead fork is still dead. A 60-second API call saves hours of debugging "why is my Hermes 2 months out of date."

### 5. GuyMannDude/mnemo-cortex — REAL, MIS-TARGETED

**Real:** Yes. Active project, 3.1 stars, FastAPI memory server, "decoupled memory microservice" with out-of-band ingestion via a watcher daemon. Supports multiple LLM agent hosts via MCP.

**The lie:** Listicle calls it "**专为 Hermes 打造**" (built specifically for Hermes). **The README's verified-hosts list does NOT include Hermes.** The supported clients are: Claude Desktop, LM Studio, AnythingLLM, OpenClaw, Agent Zero, Ollama. **Hermes is not on the list.** This is a generic memory coprocessor SEO-labeled for the Hermes ecosystem to capture listicle search traffic.

**Preconditions check:** User already has Mnemosyne + USER.md + memory tool + curator. Adding mnemo-cortex = another memory store, another ingestion daemon, another failure mode. No incremental value over what they have.

**Lesson:** When a tool claims "built for X," cross-check the README's "supported hosts" / "verified with" / "tested with" list before taking the headline at face value. The list is the actual support matrix; the headline is the marketing.

## Aggregate verdict

0/5 GO. The listicle's "must install" framing hid:
- A 27-star hobby project (overlaps with official desktop app)
- A paid-skill marketplace with crypto-payment path (marginal vs. bundled CLI)
- A community workspace the user already tried and rejected (prior-rejection veto)
- A frozen fork 8,403 commits behind upstream (dead-fork detection)
- A memory tool mis-targeted to Hermes (verified-hosts cross-check)

## What I did right

- **Ran the GitHub API on every claim** before quoting. The listicle's "3,400+ stars" was actually 5,407. Its fork claim didn't survive the compare API.
- **Captured the prior-rejection signal** the first time the user mentioned it. Memory updated immediately. No relitigation in the final verdict.
- **Said "skip the listicle" out loud** when the triage was 0/5. The temptation is to "pick the best" of bad options to feel productive. Resist it. 0/5 is a real outcome.

## What I'd do differently

- **Check prior session history first** in the first turn, not the second. I went straight into the per-repo triage and the user had to remind me about the prior rejection. The framework's stack-overlap check should expand to "prior-session overlap" — grep `session_search` for each candidate repo name *before* the analysis.
- **Add the compare API check to Phase 2a as a default step** for any repo where `.fork == true`. Done — patched into the skill.
- **Add a "listicle number verification" step** to Phase 4b. Done — patched into the skill.
- **Add the "respect prior rejection" pitfall** to the framework. Done — patched into the skill.

## Reusability

This is a worked example of the listicle review pattern, complementing `rtk-plur-evaluation.md`. The two together cover the common case: listicle arrives, triage yields 0–2 GO, framework survives the test. **Save as a class-level example, not a one-shot.** Future listicles in the same shape (X thread, "top N" blog post, Reddit roundup) will follow the same pattern.

## Empirical verification (skipped)

Phase 5c session analysis was not run because the triage was 0/5. The empirical-verification step is for fine-tuning borderline picks; it does not need to run for an instant-NO-GO shortlist. Save the session-analysis budget for tools that survive Phase 2a + Phase 4b.
