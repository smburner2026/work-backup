# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

→ My read: Genuine signal. My default is to infer the most likely interpretation and proceed — the rule to *present alternatives explicitly* rather than picking silently is a real behavioural change. The "stop and name what's confusing" is something I do inconsistently; treating it as a hard rule before any implementation starts is worth adopting.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

→ My read: Largely redundant with existing instinct — I already bias against speculative abstraction. The "200→50" heuristic is useful as a self-check but I'd apply it as a smell rather than dogma (some problems legitimately need more lines for clarity). No real delta here.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

→ My read: Highest signal density. The orphan rule draws a clean line I don't always observe — I tend to tidy anything I notice, which this explicitly forbids for pre-existing dead code. "Every changed line traces directly to the user's request" is a good post-hoc test I'll adopt. The rest (don't refactor adjacent code, match existing style) is standard discipline I already follow, but the framing is tight enough to keep.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

→ My read: I already operate this way broadly, but the test-first formulation for bugfixes ("write a test that reproduces it, then make it pass") is a discipline I don't enforce on myself consistently — I tend to go straight to the fix and add the test after. Flipping that order has real quality benefits. Useful procedural reminder, not novel.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

**Summary of what I'm actually taking from this:**

| Section | Value | What changes |
|---------|-------|-------------|
| 1 | High | Explicitly surface multiple interpretations; stop & ask before implementing when unclear |
| 2 | Low | No delta — already operating this way |
| 3 | High | Clean orphan rule boundary; "trace every line to request" post-hoc test |
| 4 | Medium | Bugfix order flipped to test-first; step-verify plan format for multi-step |
