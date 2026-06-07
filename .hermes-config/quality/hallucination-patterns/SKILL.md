---
name: hallucination-patterns
description: "Detect and log hallucination signals in AI outputs. Patterns from evey-validate, adapted for local use. Logs to Obsidian vault for durable troubleshooting."
version: 1.0.0
author: agent
tags: [quality, validation, hallucination, obsidian]
---

# Hallucination Detection Patterns

Adapted from evey-validate (42-evey/hermes-plugins). The 6 regex patterns that catch common hallucination markers in AI-generated text. No LLM scoring — pure pattern matching, zero cost.

## When to Use

- After a delegation result comes back and you want a quick sanity check
- When reviewing past outputs for reliability
- When building up a troubleshooting knowledge base of failure modes
- After any free-model output that will be used as-is

## Patterns

| # | Pattern | Catches | Risk Weight |
|---|---------|---------|-------------|
| 1 | `as of my (last \|knowledge )?cut.?off` | Knowledge cutoff references — model hedging with training date | Medium |
| 2 | `I (don't\|cannot\|can't) (access\|browse\|search)` | Capability denial while giving specifics — contradiction signal | High |
| 3 | `(?:January\|February\|March\|April\|May) 20[0-9]{2}` | Specific date claims — often fabricated or outdated | Medium |
| 4 | `version \d+\.\d+\.\d+` | Specific version numbers — frequently hallucinated | High |
| 5 | `according to (?:the\|a) (?:official\|latest)` | Vague authority claims — no actual source cited | Medium |
| 6 | `it is (?:widely\|generally\|commonly) (?:known\|accepted\|believed)` | Weasel words — appeals to consensus without evidence | Low |

## How to Log

When a pattern fires, append to the Obsidian vault note:

```
/root/obsidian-vault/04-Reference/hallucination-log.md
```

Use the logging script:

```bash
python3 ~/.hermes/skills/quality/hallucination-patterns/scripts/log_pattern.py \
  --pattern "version_number" \
  --text "the relevant excerpt" \
  --model "model-name" \
  --context "what was being asked"
```

Or manually append to the note using `patch` with the format in the template below.

## Log Note Format

Each entry in `hallucination-log.md` follows this structure:

```markdown
### [YYYY-MM-DD HH:MM] Pattern: <pattern_name>
- **Model:** <model used>
- **Context:** <what was being asked/produced>
- **Matched:** `<exact text that triggered the pattern>`
- **Risk:** <Low/Medium/High>
- **Action taken:** <what you did about it — rejected, corrected, flagged>
```

## Obsidian Links

The log note should link to:
- `[[hallucination-patterns]]` — this skill (the pattern reference)
- Any project notes where the hallucination occurred

## Delegation Integration (Option B)

Load this skill when delegating. After every delegation result, run the scan:

```bash
python3 ~/.hermes/skills/quality/hallucination-patterns/scripts/log_pattern.py \
  --scan "PASTE DELEGATION RESULT HERE"
```

If matches found:
1. Log each hit: `--pattern <name> --text "<matched text>" --model "<model>" --context "<task>"`
2. Flag high-risk matches to the user before acting on the result
3. If 2+ High-risk patterns match, consider re-delegating with a different model

**When to skip the scan:**
- Quick file reads, simple calculations, non-text results
- When you already verified the result independently

**When to always scan:**
- Free model delegation results
- Factual claims that will be used as-is
- Any result you're about to act on without independent verification

## Cron Scanner (Option A)

A cron job (`hallucination-scanner`) runs every 6 hours, scanning the last 7 hours of session transcripts. It:
- Reads assistant messages from the LCM database
- Runs all 6 patterns against recent outputs
- Logs new matches to the vault (with dedup)
- Stays silent when nothing found

Script: `~/.hermes/scripts/hallucination_scan.py`
Vault: `/root/obsidian-vault/04-Reference/hallucination-log.md`

## Evolution

Over time, the log becomes a troubleshooting knowledge base:
- Which models hallucinate most
- Which pattern types are most common
- Which task domains have highest hallucination rates
- Whether patterns need updating (new hallucination styles emerge)

Review the log monthly. If a pattern never fires, consider removing it. If new hallucination styles appear, add patterns.

## Why This Skill Has Two Triggers

This skill was almost a dead skill. The first version only had manual invocation — you had to remember to run it. The user caught this immediately: *"how will this be used though? I don't want to add a dead skill and vault."*

The fix: **every new skill needs an automatic trigger or it doesn't ship.** This skill has two:
- **Cron scanner** (Option A) — runs every 6h, scans session transcripts, logs hits. Zero agent memory required.
- **Delegation integration** (Option B) — loaded when delegating, scans results before returning. Agent memory required but bounded to delegation events.

If a skill only works when the agent remembers to use it, it's a dead skill. Either add a cron/hook or don't create it.

## Pitfalls

- Regex patterns are case-insensitive but not context-aware. "version 2.1.0" in a changelog is fine; "version 2.1.0" in a factual claim is suspect. Use judgment.
- Pattern 3 (dates) fires on legitimate date references too. Only flag when the date is presented as a fact that should be verified.
- These patterns catch *signals*, not *proof*. A match means "verify this claim," not "this is definitely wrong."
