---
name: post-removal-verification
description: "Post-removal verification protocol for Hermes component deletion — 10-point sweep, stale log noise vs live failures, skill/script smoke tests, structured PASS/FAIL report."
---

# Post-Removal Verification

The `Component Removal Checklist` in `SKILL.md` covers the **cleanup pass** — what to grep for and patch. This file covers the **verification pass** — how to prove nothing broke.

User has a stated preference for "comprehensive diagnostics, not piecemeal." One pass, structured report, every claim backed by a real command output. "Looks clean" is not verification.

## When to run

- After any Component Removal Checklist completion
- When the user says "make sure that didn't break anything," "diagnostic sweep," "verify clean," or "did the nuke work"
- Before declaring a tool/service deletion complete in a status report

## Structured PASS/FAIL report

Output a table with one row per check and a real command backing each claim. A line that says "PASS" without showing what was run is not verification. Format:

```
| Check | Status | Notes |
|---|---|---|
| Active code references | ✅ PASS | `grep -rl gbrain ~/.hermes/skills/ ...` → 0 matches |
| Running processes | ✅ PASS | `ps aux | grep gbrain` → empty |
```

Use ✅/⚠️/✗. Distinguish **active references** (must be 0) from **historical artifacts** (informational — `.hms-bak` files, old session JSON, `.usage.json` telemetry).

## The 10-point verification sweep

Run these in this order. Each is a single shell command:

| # | Check | Command |
|---|---|---|
| 1 | Active code references | `grep -rl --include='*.md' --include='*.py' --include='*.sh' --include='*.yaml' --include='*.yml' --include='*.json' -iE '<component>\|<mcp_name>' ~/.hermes/skills/ ~/.hermes/scripts/ ~/.hermes/config.yaml ~/.hermes/.env 2>/dev/null \| grep -v '\.hms-bak' \| grep -v '/.archive/' \| grep -v '/.hub/'` |
| 2 | Config deep scan (every section) | `python3 -c "import yaml; ..."` walking the parsed YAML tree for the component string (catches nested references grep misses) |
| 3 | Profiles | `find ~/.hermes/profiles -type f \| xargs grep -l '<component>' 2>/dev/null` |
| 4 | MCP server list | `python3 -c "import yaml; c=yaml.safe_load(open('~/.hermes/config.yaml')); print(c.get('mcp', 'NO MCP SECTION'))"` |
| 5 | Running processes | `ps aux \| grep -iE '<component>' \| grep -v grep` |
| 6 | Crontab | `crontab -l 2>/dev/null \| grep -i <component>` |
| 7 | Systemd user services | `systemctl --user list-units --type=service \| grep -i <component>` |
| 8 | Disk artifacts | `ls -d /root/<component> /root/.<component> /var/log/<component> 2>/dev/null` then `du -sh` for any found |
| 9 | Recent log errors (live, not historical) | `find ~/.hermes/logs -type f -mtime -1 \| xargs grep -i '<component>'` |
| 10 | Skill manifest | `hermes skills list 2>&1 \| grep -i <component>` |

**Exclude from active check** (informational, not errors):
- `~/.hermes/skills/.hms-bak` (auto-snapshots, overwritten on next edit)
- `~/.hermes/skills/.archive/` (dormant, not loaded)
- `~/.hermes/skills/.hub/index-cache/` (remote hub cache, refreshed by curator)
- `~/.hermes/skills/.usage.json` (telemetry from old installs, auto-pruned)
- `~/.hermes/sessions/*.json` (historical transcripts, never loaded)

## Stale log noise vs live failures — the critical distinction

Log files can have `mtime` that's hours or days old. A `grep '<component>' ~/.hermes/logs/mcp-stderr.log` showing 30 matches might look like "the component is still loading" — when in fact the file last wrote 9 hours ago and the matches are from before deletion. This pattern is the #1 false positive in post-removal verification.

**Always check file mtime before interpreting log contents:**

```bash
stat -c '%y  %n' ~/.hermes/logs/<file>.log
# Compare to current time:
date
```

**Rule of thumb:**
- Log file `mtime` < most recent pre-deletion activity timestamp → matches are **historical**, not live
- Log file `mtime` within last few minutes of deletion → matches are **live**, investigate
- Gateway log has fresh `inbound message` entries from the user after deletion → loader has definitely re-read config without the component

**Example interpretation:** `mcp-stderr.log` last write `2026-06-05 02:28:19`, current time `11:32:00`, user has been chatting since 11:04. The gbrain entries in the log are 9 hours stale. The loader has re-read config and is silently dropping gbrain. **No live failure.**

## Functional smoke test of patched skills

After a large skill patch (10+ files), verify the rewrites actually parse and don't have broken tool calls:

```bash
# Verify YAML frontmatter parses
for s in skill1 skill2 skill3; do
  path=$(find ~/.hermes/skills -path "*$s/SKILL.md" 2>/dev/null | head -1)
  [ -n "$path" ] && python3 -c "import yaml; d=yaml.safe_load(open('$path').read().split('---',2)[1] if '---' in open('$path').read() else ''); print('  ✓ $s:', d.get('name','?'))"
done
```

For skills that load external libraries (e.g. dabt-reference loading reference library paths), also smoke-test the actual workflow:

```bash
# Test file_search path actually works
DABT_DIR=$(python3 -c "import json; d=json.load(open('~/.hermes/skills/education/dabt-project-workflow/dabt-config.json')); print(d.get('reference_library',{}).get('extracted_dir',''))")
ls -d "$DABT_DIR" 2>/dev/null && find "$DABT_DIR" -name '*.md' | head -3
```

## Operational script smoke test

Scripts you patched (e.g. `nightly-infrastructure-audit.py`, `dabt-weekly-audit.py`, `self-audit.sh`) should be run end-to-end. A 5-second run is cheaper than discovering 3 days later that a removed function is still called from `main()`.

```bash
python3 ~/.hermes/scripts/<patched-script>.py 2>&1 | head -40
bash ~/.hermes/skills/devops/hermes-maintenance/scripts/self-audit.sh 2>&1 | head -20
```

If the script imports a module you removed a function from, it will fail at import or first call. Catch this in the verification pass, not at the next cron tick.

## `hermes doctor` final check

The aggregated health check. Pre-existing issues (e.g. `DEEPSEEK_API_KEY` not set, browser npm audit, mnemosyne plugin not found) are **noise** — flag them as pre-existing, not as a result of the removal. Only new failures or warnings related to the removed component count against the verification.

```bash
hermes doctor 2>&1 | tail -50
```

## Subagent model availability — pitfall for parallel sweeps

When you delegate the verification sweep to parallel subagents (`delegate_task` with `tasks=[...]`), the subagent inherits the **parent's model**. If the parent model was just switched to a model the provider catalog hasn't indexed yet (e.g. brand-new model release, recent provider switch), the subagent's first call returns `HTTP 404` and the subagent fails immediately. The parent gets a clean error and zero data — the sweep "passes" vacuously because nothing ran.

**Detection:** all subagent tasks return in <30s with identical `HTTP 404` exit_reason and zero tool traces.

**Fix:** if subagent 404s, run the diagnostic **directly in the parent** with `terminal` calls. Loses parallelism but gets the data. Or wait until the provider indexes the new model.

**This is not a "tool doesn't work" problem** — it's a transient catalog state. Don't write it into the skill as a permanent constraint. Capture as a "this specific model wasn't in the catalog on day 1" note, not a durable rule.

## Verification report template

```
# 🩺 <Component> Removal Verification Report

**Status: ✅ Clean / ⚠️ X issues / ✗ N issues**

## Sweep results

| Check | Status | Notes |
|---|---|---|
| Active code references | ✅ PASS | 0 matches in active files |
| Config deep scan | ✅ PASS | 0 matches across every section |
| Profiles | ✅ PASS | 0 matches |
| Running processes | ✅ PASS | None |
| Crontab | ✅ PASS | No entries |
| Systemd user services | ✅ PASS | None |
| Disk artifacts | ⚠️ INFO | /root/<path> (86M) still exists, not referenced |
| Recent log errors (live) | ✅ PASS | All <component> errors predate deletion |
| 12 patched skills parse | ✅ PASS | All frontmatter YAML parses |
| hermes doctor | ✅ PASS | 3 pre-existing issues (unrelated) |
| operational scripts | ✅ PASS | Run clean |

## Notes
- <stale log noise interpretation>
- <historical artifacts that are NOT errors>

## Optional cleanup (user decision)
- `rm -rf /root/<orphan>` — reclaim disk
- `hermes skills check --auto-archive` — prune telemetry
```

## Worked example — gbrain removal (June 2026)

A 3-step deletion that the user wanted verified.

**Step 1 — cleanup pass:** 25+ skill files patched (SKILL.md + references/), 3 operational scripts patched (`nightly-infrastructure-audit.py`, `dabt-weekly-audit.py`, `self-audit.sh`), memory updated, config-guard cron already gone. 12+ skill files got full content rewrites (G-Brain → file search / Obsidian / local files) — not just sed replacements.

**Step 2 — verification pass:** ran the 10-point sweep. All 10 checks PASS or INFO. Three notable findings, all benign:
- `/root/brain` (86M) still on disk — git-tracked orphan, no active code reads it. Flagged as **optional cleanup** (`rm -rf /root/brain`).
- `.hub/index-cache/hermes-index.json` has 8 remote hub entries mentioning gbrain (e.g. `garrytan/gstack/setup-gbrain`) — refreshed by curator on next run. Not load-bearing.
- `.usage.json` has telemetry for `gbrain`, `dabt-gbrain-miss-journal`, etc. — auto-pruned. Not load-bearing.

**Step 3 — false positive caught:** `mcp-stderr.log` showed 30+ gbrain startup attempts. Looked alarming. Checked mtime: last write `02:28:19`, current time `11:32:00`, user has been chatting since 11:04. All matches are 9 hours stale — pre-deletion. **No live failure.** The MCP loader was already not loading gbrain when the user said "I deleted gbrain."

**Step 4 — operational smoke tests:** `nightly-infrastructure-audit.py` ran clean, `dabt-weekly-audit.py` produced full audit data, `hermes-maintenance/scripts/self-audit.sh` ran clean, 14 patched skills all parsed their YAML frontmatter.

**Step 5 — `hermes doctor`:** 3 pre-existing issues (DeepSeek key, browser npm audit, mnemosyne plugin) — flagged as pre-existing, not as a result of the removal. All unrelated to gbrain.

**Subagent 404 lesson learned:** Initially tried parallel `delegate_task` sweep. All 3 subagent tasks returned in ~10s with `HTTP 404` from opencode-go — the new model (`minimax-m3`) wasn't indexed yet. Switched to direct `terminal` calls in the parent. Lesson captured in "Subagent model availability" pitfall above.

**Final result:** PASS. No active references, no live failures, no broken pipelines. User's report flagged `/root/brain` and `.usage.json` cleanup as optional follow-up.

## Pitfalls

- **"Log mtime < activity timestamp = historical"** is a heuristic, not a guarantee. If the gateway was restarted after deletion, the new gateway process started fresh and has its own mcp-stderr.log — that file's mtime is the real indicator.
- **`hermes doctor` noise is pre-existing** — never blame a removal for an issue that was there before. Diff against a doctor run from before the deletion if in doubt.
- **`.usage.json` entries are not "active" — they are records of past skill usage.** A skill that was loaded 30 times will leave telemetry forever. The curator prunes idle entries; don't manually delete.
- **One stale log line ≠ live failure.** A single 02:28 gbrain attempt 9 hours after deletion is noise. A cluster of attempts at 11:32 (matching current time) is live — investigate.
- **The "skill still parses" check is necessary but not sufficient.** It catches YAML errors and missing files. It does NOT catch a skill whose `mcp_gbrain_query` call would fail at runtime. To catch runtime breakage, you'd need a full integration test — usually overkill for a one-off deletion. Document the gap and move on.
