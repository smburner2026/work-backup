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

### 6. Handling Reference Documents

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

## Verification

This skill is working if:
- Fewer unnecessary changes in diffs
- Fewer rewrites due to overcomplication
- Clarifying questions come before implementation rather than after mistakes
- Orphan cleanup is scoped to what your changes made unused
