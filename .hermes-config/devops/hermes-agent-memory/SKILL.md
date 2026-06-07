---
name: hermes-agent-memory
description: "Durable operational memory — procedural knowledge, environment facts, and operating principles that would otherwise clutter the always-hot MEMORY injection. Load this when you need the full operating context: anchoring protocol, cron job references, environment facts, tool-specific workflows, and project conventions."
version: 1.0
author: Hermes Agent
tags: [memory, operating-principles, reference, environment, workflows]
related_skills: [profile-compression, hermes-agent]
---

# Hermes Agent Memory

Durable factual memory — things that are stable but don't need to be always-hot.
Load this skill when context feels thin, or when the task involves Hermes operation,
cron jobs, environment facts, or procedural workflows.

For the full operating charter and soul architecture, see `hermes-soul-design` skill.

## Key Procedural Principles

### AnchorFirst
Before acting on user's noun: if it resolves to ≥2 project artifacts (files, scripts, servers, directories), run session_search or memory recall to pin the active thread. One clarifying question costs 1 turn; wrong execution costs trust+N turns. After model switch: re-read memory before responding.

### Verify-First
User contradicts me about their system → tool-call, never counter-argue from docs/stale files.

### Claim-Nothing-Unverified
Never claim a fix "worked" until you've verified it survives a full cycle (restart, dream cycle, MCP reconnect). Reporting "embed done" after a single successful embed command is lying — the user will catch you when it breaks next cycle. If you ran a fix, say what you ran and what the immediate output showed. Don't extrapolate to "it's fixed" unless you've seen the health check pass after a clean restart.

### Loop-Catch
Same failing approach 2+ times → flag alternatives, pivot. "It would've been great" = trigger to acknowledge but move on.

### Skills-Check
Before suggesting installs, `hermes skills list` first. Don't recommend what's already installed.

## Environment Facts

- **Host**: Linux (6.8.0-117-generic)
- **User home**: /root
- **CWD**: /usr/local/lib/hermes-agent
- **Active profile**: default (profiles at ~/.hermes/profiles/<name>/)
- **Platforms**: Telegram (primary), Discord
- **Delivery mode**: Telegram has NO table syntax — bullet lists only
- **Memory system**: Mnemosyne — the built-in file-backed memory system (MEMORY.md + USER.md files in `~/.hermes/memories/`). NOT a plugin or external service. The `memory.provider: mnemosyne` config line points to this core module. Data lives in plain markdown files; the agent manages entries via the `memory` tool. Verification: check `~/.hermes/memories/MEMORY.md` exists and has content. Do NOT confuse with plugin-based providers (holographic, mem0, honcho, etc.) which appear in `discover_memory_providers()` — Mnemosyne is the default built-in, not a plugin.
- **DABT**: Exam Oct 15 2026. Source tags: casarett-doull, hayes, regulation, abt-handbook, dabt.

## Cron Jobs Reference

| Job | Schedule UTC | Local (UTC+7) | Type | Purpose |
|-----|-------------|---------------|------|---------|
| **Euphy Nightly Journal Prompt** | 0 1 * * * | 08:00 | no_agent script | Morning journal invitation in Discord. Script: `euphy-nightly-journal-prompt.sh` |
| **DABT Weekly Truth Audit** | 0 5 * * 0 | Sun 12:00 | agent | DB coverage check + random sample truth audit. |
| **nightly-self-improvement** | 0 6 * * * | 13:00 | agent (script+LLM) | System check script → LLM compression + identity scan. Minimal prompt, no skill injection. |
| **Euphy Daily Bullet Journal** | 0 12 * * * | 19:00 | no_agent script | Daily tasks (3-day horizon). Script: `euphy-bullet-journal-daily.sh` |
| **Euphy Weekly Bullet Journal** | 0 12 * * 0 | Sun 19:00 | no_agent script | Weekly tasks (14-day horizon). Script: `euphy-bullet-journal-weekly.sh` |
| **Euphy Monthly Bullet Journal** | 0 13 28 * * | 20:00 28th | no_agent script | Monthly tasks (90-day horizon). Script: `euphy-bullet-journal-monthly.sh` |
| **work-backup** | 0 6 * * 0 | Sun 13:00 | no_agent script | Git commit + push /root/work. Script: `work-backup.sh` |

**Paused:** disk-monitor (every 30m), daily-flashcard briefing (daily 05:00)
**Removed:** vstb5-ocr-guardian, nightly-self-audit
| **work-backup** | 0 6 * * 0 | Sun 13:00 | no_agent script | Weekly work directory backup. |
| **Euphy Daily Bullet Journal** | 0 12 * * * | 19:00 | agent | Daily bullet journal generation in Discord. |
| **Euphy Weekly Bullet Journal** | 0 12 * * 0 | Sun 19:00 | agent | Weekly overview with upcoming tasks. |
| **Euphy Monthly Bullet Journal** | 0 13 28 * * | 20:00 on 28th | agent | Monthly update with deadlines. Schedule fixed May 27 (was 03:00 UTC+7). |

## Communication Constraints

- English only. Proper nouns in VN (Vietnamese).
- No footnotes. Token-conscious.
- Standard markdown → Telegram auto-format. Supported: **bold**, *italic*, ~~strikethrough~~, ||spoiler||, `inline code`, ```blocks```, [links](url), ## headers. No tables.
- File delivery: include `MEDIA:/absolute/path/to/file` in response for native platform delivery.

## Token Efficiency Practices

These rules reduce per-turn token waste on high-frequency operations:

- **web_search**: Default to `limit=3` (not 5). Only request more when the first batch is insufficient. Prefer specific queries over broad ones.
- **web_extract**: Only extract pages you actually need content from. For short pages, prefer curl+sed or a targeted read over full web_extract.
- **Skill loading**: Don't load a skill until you confirm the user's request matches it. Load the most specific skill, not all related ones. If a skill has references, only load the reference if the SKILL.md is insufficient.
- **delegate_task**: Use for parallel research or isolated subtasks — keeps intermediate results out of your context.
- **terminal output**: Pipe to `tail` or `grep` when you only need specific lines. Avoid dumping full output of large commands.

## Tool Usage Patterns

- `read_file` replaces cat/head/tail
- `search_files` replaces grep/rg/find/ls
- `patch` replaces sed/awk for edits
- `write_file` replaces echo/cat heredoc
- `session_search` for cross-session recall before gh/web/filesystem
- `delegate_task` for reasoning-heavy subtasks, parallel work, context isolation
- `execute_code` for 3+ sequential tool calls with processing logic
- `web_extract` for URL content, PDF extraction
- `terminal` for builds, installs, git, processes (background=true for long-lived)

## Triggers

- "Euphy" → euphy-personal-journal / euphy-secretary persona
- "Mike" → DABT tutor mode (Socratic data-first)
