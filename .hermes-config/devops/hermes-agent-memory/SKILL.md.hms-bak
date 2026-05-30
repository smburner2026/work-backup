---
name: hermes-agent-memory
description: "Durable operational memory — procedural knowledge, environment facts, and operating principles that would otherwise clutter the always-hot MEMORY injection. Load this when you need the full operating context: anchoring protocol, cron job references, environment facts, tool-specific workflows, and project conventions."
version: 1.0
author: Hermes Agent
tags: [memory, operating-principles, reference, environment, workflows]
related_skills: [profile-compression, hermes-agent, gbrain]
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
- **Memory system**: Mnemosyne (vector + FTS5), ~2,200/2,200 chars always-hot, ~1,375/1,375 chars USER profile
- **GBrain**: v0.41.20.0 at ~/gbrain, PGLite engine, OpenRouter NVIDIA Nemotron embeddings (1024d). MCP server via config.yaml wrapper script. Dream cycle cron at 02:00 UTC daily.
- **DABT**: Exam Oct 15 2026. G-Brain is PRIMARY reference (mcp_gbrain_query/mcp_gbrain_think). Source tags: casarett-doull, hayes, regulation, abt-handbook, dabt.

## Cron Jobs Reference

| Job | Schedule UTC | Local (UTC+7) | Type | Purpose |
|-----|-------------|---------------|------|---------|
| **Euphy Nightly Journal Prompt** | 0 1 * * * | 08:00 | agent | Morning journal invitation in Discord. |
| **gbrain-dream-cycle** | 0 2 * * * | 09:00 | no_agent script | Nightly G-Brain sync+embed+extract+dream. ⚠️ 120s timeout — mechanical phases complete, LLM phases may be cut off. Marker file tracks freshness. |
| **DABT Weekly Truth Audit** | 0 5 * * 0 | Sun 12:00 | agent | DB coverage check + random sample truth audit. |
| **gbrain-dabt-maintenance** | 0 5 * * 0 | Sun 12:00 | agent | G-Brain DABT health check + stale embed. |
| **nightly-self-improvement** | 0 6 * * * | 13:00 | agent | Session review → profile compression → system audit. Uses profile-compression skill. |
| **nightly-self-audit** | 0 8 * * * | 15:00 | no_agent script | Checks Hermes/lcm/mnemosyne/doga updates, gbrain embed API health, dream cycle marker freshness, cron job errors. Silent if OK. |
| **work-backup** | 0 6 * * 0 | Sun 13:00 | no_agent script | Weekly work directory backup. |
| **Euphy Daily Bullet Journal** | 0 12 * * * | 19:00 | agent | Daily bullet journal generation in Discord. |
| **Euphy Weekly Bullet Journal** | 0 12 * * 0 | Sun 19:00 | agent | Weekly overview with upcoming tasks. |
| **Euphy Monthly Bullet Journal** | 0 13 28 * * | 20:00 on 28th | agent | Monthly update with deadlines. Schedule fixed May 27 (was 03:00 UTC+7). |
| **DABT Miss Journal Weekly Synthesis** | 0 12 * * 0 | Sun 19:00 | agent | Cross-session miss analysis via G-Brain. |

## Communication Constraints

- English only. Proper nouns in VN (Vietnamese).
- No footnotes. Token-conscious.
- Standard markdown → Telegram auto-format. Supported: **bold**, *italic*, ~~strikethrough~~, ||spoiler||, `inline code`, ```blocks```, [links](url), ## headers. No tables.
- File delivery: include `MEDIA:/absolute/path/to/file` in response for native platform delivery.

## Token Efficiency Practices

These rules reduce per-turn token waste on high-frequency operations:

- **web_search**: Default to `limit=3` (not 5). Only request more when the first batch is insufficient. Prefer specific queries over broad ones.
- **web_extract**: Only extract pages you actually need content from. For short pages, prefer curl+sed or a targeted read over full web_extract.
- **GBrain queries**: Use `limit` parameter (`mcp_gbrain_query(query, limit=3-5)`). Don't default to 20. When you only need a citation, not full context, use search rather than think.
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
