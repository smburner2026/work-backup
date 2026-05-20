# DABT Weekly Truth Audit — Cron Job Definition

**Created:** 2026-05-20
**Job ID:** `2a16ef8310c5`
**Name:** DABT Weekly Truth Audit

## Schedule
- **Cron:** `0 5 * * 0` (Sunday at 5:00 AM UTC)
- **Repeat:** forever

## Delivery
- **Target:** origin (this Telegram chat)
- **Delivery format:** compact, one-line-per-metric, deltas-only

## Skills Loaded (in order)
1. `dabt-database` — question DB querying and blueprint-weighted sampling
2. `dabt-reference` — multi-pass reference text search (Casarett, Hayes, regs)
3. `batch-data-enrichment` — self-review and verification methodology

## Toolsets Enabled
- `terminal` — shell access for DB queries
- `file` — read/write access to workdir files
- `search` — filesystem grep for content matching

## Work Directory
`/root/work/dabt/dabt-tutor` — project workdir with dabt-config.json

## Prompt (self-contained)
> You are the DABT system truth audit. This is a scheduled weekly health check — be concise, surface only deltas and new problems. Do 3 things:
> 
> 1. COVERAGE AUDIT: Compare DB quality metrics against dabt-config.json baseline. Report only decreases.
> 
> 2. RANDOM SAMPLE: Select 5 questions, verify explanations against Casarett/Hayes. Report confirmations or flag issues.
> 
> 3. NEW CONTENT CHECK: If new questions/explanations appeared since last run, spot-check them.
> 
> Keep output one-line-per-metric, deltas-only.

## Context & Rationale
Created as part of the 2026-05-20 truth audit work that:
- Discovered the ABT Candidate Handbook was in the reference directory but unused by skills
- Identified structural bias in DB distribution vs exam blueprint weights
- Patched all DABT skills to use dabt-config.json for domain-driven prioritization
- Extracted the handbook to structured text files in reference/extracted/abt-handbook/
- Wrote root-cause analysis at reference/root-cause-handbook-unused.md

## Config Reference
All authoritative values (domain weights, DB paths, threshold targets) come from:
`dabt-config.json` — the unified project config materialized 2026-05-20

See also: `dabt-database` skill reference `references/truth-audit-2026-05-19.md` for the inaugural audit report.
