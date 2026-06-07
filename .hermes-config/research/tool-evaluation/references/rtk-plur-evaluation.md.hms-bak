# rtk-hermes vs plur — Hermes Ecosystem Listicle Review

**Date:** 2026-06-05
**Source:** X post by @XAMTO_AI listing "5 Hermes ecosystem tools" (`x.com/i/status/2062655324046385531`)
**Verdict (per item):**
- `fathah/hermes-desktop` — REAL, USEFUL (already in user's stack)
- `AkoliteZA/hermes-agent-idea-workflow` — REAL, REDUNDANT (overlaps with built-in `plan` and `ideation` skills)
- `plur-ai/plur` — REAL, NO-GO for this user (cross-tool memory, user only runs Hermes, has Mnemosyne/USER.md/curator stack already)
- `ogallotti/rtk-hermes` — REAL, **NO-GO after empirical session analysis** (benchmark targets `cargo test`-class output; user's actual shell calls average 1.7 KB with no high-volume commands — see Empirical Verification below)
- `mudrii/hermesd` — REAL, niche (TUI dashboard, redundant with existing audit scripts)

## Listicle review pattern (the actual lesson)

The X post itself was a viral roundup with marketing framing ("blown the ceiling off", "you haven't caught up yet?"). The list contents were the only signal. Per-item triage against the framework found 2 of 5 actionable, 1 redundant, 1 NO-GO for preconditions, 1 already-installed.

**Don't trust the list — trust the per-item analysis.**

## The two deep-dives

### rtk-hermes — GO

**What it is:** Small Hermes plugin (8 commits) wrapping the RTK CLI proxy. Uses `pre_tool_call` hook to rewrite shell commands through `rtk rewrite` for token-compressed output.

**Underlying engine (RTK):**
- Rust, MIT, 54.8k stars, 1,077 commits
- 89% avg noise reduction across 2,927 real dev commands
- Per-command: `cargo test` -91.8%, `git status` -80.8%, `find` -78.3%, `grep` -49.5%, `git diff` -94%
- Reproducible per-command: `cargo test` 4,823 → 11 tokens (-99%)

**Independent validation:**
- madplay.github.io blog post confirming the 80% reduction claim
- Medium post: "I Only Compressed CLI Output, Yet Tokens Dropped by 80%" — real third-party test
- Counter-article: "The Over-Optimization Trap: Why I Uninstalled My AI Token Optimizer" — real downside (when output is huge, even 80% can exceed CLI limits). Useful signal that RTK is a *default* optimizer, not a *guaranteed* one. Mitigated by opt-out (`rtk passthrough`).

**Compatibility check:**
- User's VPS: Rust toolchain needed but not present (`which rustc cargo` returned empty). Pre-built binary available via `install.sh`.
- Disk: ~150MB build footprint
- No env var / port / config-dir conflicts with Hermes

**Stack overlap:** None — RTK is unique in the user's stack. No competing CLI-output compression.

**Verdict:** **NO-GO after empirical verification.** Engineering GO (real code, real benchmark, no security issues, compatible stack). User GO fails on a different gate: the benchmark use case (compressing huge `cargo test` output, large `find`/`grep -r`, etc.) doesn't exist in the user's actual workflow. The user's shell commands are 1.7 KB average, mostly navigation (`cd`, `ls`) and small inspections (`grep`, `cat`, `find`). RTK's value is concentrated in the noisy high-volume commands, and the user doesn't run them. Save the 150MB Rust install and 5-min smoke test. **If the user's workload shifts to a build/test/debug heavy profile (Rust/Node projects, long shell pipelines), re-validate by re-running the session analysis.**

### plur — NO-GO (preconditions check failed)

**What it is:** Cross-tool shared memory layer. Local-first YAML storage in `~/.plur/`. Schema-aware retrieval (BM25 + local embeddings). 381 commits, mature codebase.

**Headline claim:** "Haiku with PLUR outperforms Opus without it — 2.6x better on tool routing at 10x less cost."

**Benchmark audit (the actual lesson):**
- Vendor published: 31 wins / 4 losses across 19 decisive contests. 12-0 on "house rules" specifically.
- **N=19 decisive contests is not statistically robust.** Real benchmark standards want hundreds of trials for headline claims.
- **The "12-0 house rules" stat is N=12.** That's the kind of number that gets printed in slides, not validated in papers.
- LongMemEval 86.7% is more credible (reproducible, `benchmark/run.ts` is on GitHub).
- **Independent validation: none found.** No blog posts, no Medium articles, no Reddit threads with reproducible numbers, no third-party reviews.

**Why NO-GO for this user specifically (the engineering-GO-≠-user-GO lesson):**
- Plur's value proposition is **cross-tool memory**: Claude Code ↔ Cursor ↔ Windsurf ↔ OpenClaw ↔ Hermes
- User runs **only Hermes**
- User already has a memory stack: Mnemosyne + USER.md + `hermes-agent-memory` skill + memory tool + curator
- Adding Plur = another YAML store, another engram extractor on every session, another failure mode to debug
- The headline "Haiku 2.6x better at 10x less cost" only makes sense if you're choosing between expensive Opus *and* no memory. User has memory. The comparison doesn't apply.

**Risk if installed anyway:** Low technical risk (well-built, local-first, MIT, no cloud calls in current version). High *complexity* risk.

**Verdict:** Skip. Well-engineered but solves a problem the user doesn't have. The preconditions check (Phase 4 step 6 / Phase 5 gate) catches this — the user doesn't have the multi-tool leg Plur stands on.

## What I'd do differently next time

- **Don't call a list "pure slop" until I've verified each item.** I initially overcorrected; the repos were real, only the framing was marketing. The listicle review pattern (Phase 4b in SKILL.md) prevents this.
- **Surface the N of vendor benchmarks explicitly.** "12-0 in house rules" sounds impressive until you realize N=12. The pitfall section now flags this.
- **Run the preconditions check alongside the stack-overlap check.** A tool can fail stack-overlap (you have this) OR preconditions (you can't benefit from this). Both are NO-GO signals.
- **Empirical session analysis before recommending use-case tools.** RTK flipped from GO to NO-GO once I queried the actual session DB and found the user's shell commands are 1.7 KB average, not the multi-KB noisy commands the benchmark targets. The lesson: benchmark claims describe capability; session analysis describes applicability. Both must align. See Phase 5c in SKILL.md and `session-analysis-technique.md`.

## Empirical Verification: rtk-hermes session analysis

The RTK benchmark claim ("89% noise reduction across 2,927 real dev commands, per-command: `cargo test` -91.8%, `git status` -80.8%, `find` -78.3%") is real. The use case it targets — compressing high-volume shell command output — is also real. But the user's actual workflow is *not* that use case.

**Method:** Queried `~/.hermes/sessions/*.jsonl` (82 sessions, 17.7 MB total, 2,155 tool calls).

**Findings:**

| Tool | Calls | Result bytes | Avg per call |
|---|---|---|---|
| `terminal` (shell) | 1,013 | 1,759 KB | **1.7 KB** |
| `read_file` | 181 | 996 KB | 5.4 KB |
| `web_extract` | 38 | 191 KB | 5.0 KB |
| `web_search` | 63 | 352 KB | 5.6 KB |
| `skill_view` | 127 | 1,812 KB | 14.3 KB |
| `session_search` | 104 | 1,059 KB | 10.2 KB |

**Shell size distribution:** 724 calls under 1 KB, 222 calls 1-10 KB, 34 calls 10-100 KB, **0 calls over 100 KB.**

**Top shell command first-words:** `cd` (197), `python3` (152), `ls` (68), `hermes` (46), `grep` (40), `curl` (32), `cat` (27), `find` (25), `git` (7). **Zero `cargo`, zero `npm test`, zero `kubectl`, zero `docker`, zero `pytest -v`, zero `make`.**

**The mismatch:** RTK's value is concentrated in compressing the long tail of noisy output. The user's shell commands are mostly *navigational* (cd/ls) or *small inspections* (grep/cat/find). The 89% claim is true; it just doesn't apply to the user's actual commands.

**Cost of being wrong on this:** 150MB Rust toolchain on a 2GB VPS, an escape hatch to remember, and ongoing maintenance for a benefit of near-zero. Empirical verification caught this *before* the install.

**When this would flip:** If the user starts a Rust/Node/build-heavy project, or runs `git log --all` on a long history regularly, the analysis would change. Re-run the session analysis when the workload shifts.

## Top context-eaters the user actually has (the optimization targets RTK doesn't address)

| Category | Result bytes | What dominates it | Mitigation |
|---|---|---|---|
| `skill_view` (25.5%) | 1,812 KB | `hermes-agent` skill loaded 19× at 50+ KB each | Trim/split heavy skills; tighten frontmatter `description` |
| `session_search` (14.9%) | 1,059 KB | 20 of 104 calls return 20-100 KB from broad OR queries | Pass `limit=2`; tighten queries; use `lcm_describe` for cheap metadata |
| `read_file` (14.0%) | 996 KB | 11 of 181 calls return 20-100 KB | Default to `limit=200, offset=1` for first scan reads |

Combined potential: ~50% reduction in tool-result context without installing anything. This is the "edit existing capabilities before adding new tools" path (Phase 5d in SKILL.md + Engineering Discipline section 9).

## What this evaluation cost (for budgeting future deep-dives)

- ~3 web searches + 3 page extractions + 2 `web_extract` calls
- ~1 minute wall time
- The reference transcript (~50 lines) is saved for future re-evaluation if the user asks about either tool again, or for the pattern when a similar listicle appears.
