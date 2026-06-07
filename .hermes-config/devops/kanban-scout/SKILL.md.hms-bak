---
name: kanban-scout
description: "Specialized discovery agents — find things and report structured findings, never act on them."
version: 1.0.0
author: Hermes Agent
category: devops
platforms:
  - linux
tags:
  - kanban
  - multi-agent
  - discovery
  - scouts
  - workflow
related_skills:
  - kanban-orchestrator
  - kanban-worker
---

# Kanban Scout Pattern

Scouts are pure discovery agents. They find things, report structured findings, and stop. They never mutate state, never execute tasks, never reach conclusions beyond what they observed.

## 1. Definition

| Dimension | Scout | Not a Scout |
|-----------|-------|-------------|
| **Purpose** | Discover and report | Act, modify, execute |
| **Output** | Structured report with metadata | Side effects, state changes, task completion |
| **Scope** | Single observation axis | Cross-cutting analysis, synthesis |
| **Lifecycle** | Detect → Report → Done | Detect → Analyze → Decide → Act |
| **Autonomy** | Follows deterministic checks or narrow search | Full reasoning, tool chaining, multi-step workflows |

A scout embodies the **separation of concerns** principle: observation is distinct from action. Scouts feed the kanban intake or file system with raw findings; orchestrators and workers consume those findings to make decisions and execute tasks.

### What a scout is

- A **thin, focused agent** (or cron script) with a single job: check something and report what it found
- **Discovers** — checks a source, runs a query, monitors a condition, scrapes a page
- **Reports** — writes structured findings to a file, kanban board, or memory
- **Stops** — never queues follow-up actions, never triggers workers, never self-modifies
- **Deterministic** where possible — the report format is fixed, the logic is linear

### What a scout is not

- **Not a worker** — workers execute tasks; scouts only observe
- **Not an orchestrator** — orchestrators route findings and manage workflows; scouts just drop findings
- **Not an analyst** — scouts report raw or lightly-structured observations; they don't synthesize across findings
- **Not a self-improver** — scouts don't tune their own prompts, add sources, or expand scope

## 2. Output Schema

Every scout report uses the following structured metadata. The report itself is a markdown file or kanban card body containing these fields.

```yaml
title: <short, descriptive title of the finding>
claim: <the single observation or discovery — one claim per report>
sources:
  - <URL or path or query that produced this finding>
why_it_matters: <one-sentence context: who should care and why>
confidence: <high | medium | low>
```

### Field rules

| Field | Required | Max length | Notes |
|-------|----------|------------|-------|
| `title` | Yes | 120 chars | Should stand alone in a kanban card title |
| `claim` | Yes | 500 chars | A single, falsifiable statement — not a summary |
| `sources` | Yes | 5 entries | Each source must be a specific URL, file path, or query output |
| `why_it_matters` | Yes | 300 chars | Make the relevance explicit so consumers can triage |
| `confidence` | Yes | — | `high`: definitive observation; `medium`: reasonable inference; `low`: weak signal worth flagging |

### Example

```yaml
title: GitHub Actions runner disk usage exceeds 80%
claim: The self-hosted runner `prod-runner-01` reports 83% disk usage (26.4 GB / 31.7 GB)
sources:
  - ssh://prod-runner-01 "df -h /"
  - https://github.com/org/settings/actions/runners
why_it_matters: Runner may fail builds within 48 hours at current growth rate
confidence: high
```

### Report file conventions

- File names: `<scout-name>_<YYYY-MM-DD>.md` or `<scout-name>_<datetimestamp>.md`
- Directory: `~/.hermes/kanban/scouts/<scout-name>/`
- Each report contains **exactly one observation**. If a scout finds multiple findings, it writes multiple report files (one per finding).

## 3. Deployment Modes

Scouts deploy in one of two modes depending on complexity and frequency.

### Mode A: `no_agent: true` Cron Job (cheapest, preferred)

For **deterministic checks** — commands, scripts, API calls with structured output. No LLM tokens consumed.

```python
cronjob(
    action='create',
    name='infra-disk-scout',
    schedule='0 6 * * *',       # Daily at 06:00 UTC
    no_agent=True,
    script='scout-disk-usage.sh',
    deliver='local',             # Writes to file; kanban intake reads it
)
```

**Use when:**
- The check is a shell command, curl, or simple Python script
- Output can be parsed into the scout schema with string manipulation (grep, jq, yq)
- You don't need LLM judgment to determine what a finding means
- The check runs frequently (hourly, daily)

**Script template:**

```python
#!/usr/bin/env python3
"""Scout-print script — outputs structured YAML to stdout."""
import json, yaml, subprocess

result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
finding = {
    "title": "Root disk usage report",
    "claim": f"Disk usage: {result.stdout.strip()}",
    "sources": ["df -h /"],
    "why_it_matters": "Root disk usage affects system stability and build reliability",
    "confidence": "high",
}
print("---")
print(yaml.dump(finding, default_flow_style=False))
```

The cron runner captures stdout and writes the markdown report file. The kanban intake (or a separate cron job) picks up report files from the scouts directory and creates kanban cards.

### Mode B: Thin Agent Skill (flexible, needed for LLM judgment)

For **checks that need interpretation** — natural language sources, qualitative signals, fuzzy pattern matching.

**Skill structure:**
- Minimal frontmatter (name, description, triggers, tools)
- Tools limited to `search`, `web_search`, `extract` — never write/mutate tools
- No agent identity beyond "you are a scout"

```yaml
---
name: trend-scout
triggers:
  - check for emerging patterns
tools:
  - search
  - web_search
# No put_page, no external writes, no kanban card mutation
writes_pages: false
mutating: false
---
```

**Prompt pattern:**

```markdown
You are a scout. Your only job is to discover and report.

1. Choose one source to check
2. Run exactly one search or extraction
3. Report findings using this schema:
   - title
   - claim (one single observation)
   - sources
   - why_it_matters
   - confidence (high/medium/low)
4. Stop. Do not analyze, compare, suggest actions, or write anything beyond the report.
```

**Use when:**
- The source is unstructured (web pages, conversations, documents)
- The signal requires interpretation ("does this page mention a new compliance requirement?")
- You need to filter noise from a noisy source
- The check runs infrequently (weekly, on-demand) — LLM cost is acceptable

### Decision matrix

| Factor | Mode A (no_agent script) | Mode B (thin agent) |
|--------|--------------------------|---------------------|
| Check is a shell command or API call | ✅ | ❌ Overkill |
| Check needs natural language understanding | ❌ | ✅ |
| Runs every hour | ✅ ($0) | ❌ (token cost) |
| Runs once a week | ✅ | ✅ |
| Source is structured JSON/CSV | ✅ | ❌ |
| Source is a web page or document | ❌ | ✅ |
| Needs to parse free text | ❌ | ✅ |

## 4. Reference Example: Nightly Infrastructure Audit

The `nightly-infrastructure-audit.py` script is a canonical scout implementation.

### What it does

Runs nightly, collects a fixed set of infrastructure health signals (disk, memory, process count, SSL expiry), formats each as a scout report, and writes findings to the kanban scouts directory.

### Key design decisions

1. **One observation per run** — the script exits after writing a single report. If it finds abnormal conditions for multiple services, it writes one report with the most critical finding.
2. **No state** — reads state at runtime, writes a report, exits. Never caches, never compares to previous runs.
3. **Fixed schema** — every report follows the same YAML schema from Section 2. Consumers rely on the schema being stable.
4. **`no_agent: true`** — no LLM involvement. The script parses `df`, `free`, `ps`, and `openssl` output directly.
5. **Hard timeout guard** — the cron job's `script_timeout_seconds` is set to 30 (not the default 600) because the checks are fast. If a check hangs (e.g., SSL connect timeout on a dead host), the script is killed quickly without blocking the cron runner.

### Script structure (abbreviated)

```python
#!/usr/bin/env python3
"""nightly-infrastructure-audit.py — Scout: check infra health, report findings."""

import subprocess, yaml, sys

CHECKS = {
    "disk": ["df", "-h", "/"],
    "memory": ["free", "-h"],
    "ssl_expiry": ["openssl", "s_client", "-servername", "example.com",
                   "-connect", "example.com:443", "</dev/null"],
}

def run_check(name, cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except Exception as e:
        return f"FAILED: {e}"

def main():
    # Pick the most interesting finding
    for name, cmd in CHECKS.items():
        output = run_check(name, cmd)
        if "FAILED" in output or should_flag(output):
            report = {
                "title": f"Infra alert: {name}",
                "claim": output[:500],
                "sources": [f"command: {' '.join(cmd)}"],
                "why_it_matters": f"{name} health affects infrastructure reliability",
                "confidence": "high",
            }
            print("---")
            print(yaml.dump(report, default_flow_style=False))
            sys.exit(0)

    # Nothing to report — silent exit (watchdog pattern)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Cron registration

```python
cronjob(
    action='create',
    name='nightly-infrastructure-audit',
    schedule='0 4 * * *',
    no_agent=True,
    script='nightly-infrastructure-audit.py',
    deliver='local',
)
```

> **Note:** The actual file may live at `~/.hermes/kanban/scouts/nightly-infrastructure-audit/nightly-infrastructure-audit.py` with the cron script path pointing to it.

## 5. Pitfalls

### Rate limits

Scouts hitting external APIs (GitHub, Docker Hub, cloud providers) must respect rate limits. A scout that runs every 5 minutes and triggers a 429 will eventually get its cron job killed and produce false-negative findings (silence when it should have found something).

**Mitigations:**
- Space cron runs by at least the API's window (1 hour for most free tiers)
- Implement exponential backoff in the script if the scout runs on-demand
- Use a caching layer for deterministic checks whose source doesn't change minute-to-minute
- For Mode B (thin agent) scouts, add a guard in the prompt: "If the API returns a rate-limit error, report it as `confidence: low` with the claim 'Source unavailable (rate limited)' — do not retry"

### Stale sources

A scout that checks the same static URL every day will report the same finding until the source changes. After N identical reports, the signal becomes noise.

**Mitigations:**
- Scouts should include a source timestamp in their report
- The kanban intake (or a dedup step) should suppress duplicate findings for the same source + claim within a configurable window
- Consider adding an `expires_at` field to the output schema for time-sensitive findings
- Rotate sources periodically or add the source's last-modified timestamp to the check

### Output format discipline

If a scout's report format drifts — extra fields, missing fields, renamed keys — consumers break silently. A kanban intake that expects `why_it_matters` but gets `impact` will skip the card silently.

**Mitigations:**
- Validate the output schema in the script (Mode A) or in the agent prompt's final step (Mode B)
- Include a YAML validation step: `python3 -c "import yaml, sys; doc = yaml.safe_load(sys.stdin); assert all(k in doc for k in ['title', 'claim', 'sources', 'why_it_matters', 'confidence'])"`
- Version the schema in the report header: `schema_version: 1`
- Test consumer behavior when fields are missing — don't trust, verify

### Scope creep (scout starts analyzing)

The most common scout failure: a scout discovers something and then starts analyzing it. "I found disk at 83% — let me check if that's trending up by looking at the past 7 days of reports." This turns a scout into an analyst, which burns LLM tokens, adds latency, and duplicates orchestration logic.

**Mitigations:**
- **Hard rule in the prompt:** "If you are about to analyze, compare, or contextualize — stop. Report what you found and exit."
- **Tool restriction:** Mode B scouts should only have `search` and `extract` tools — no `python`, no `read_file`, no `put_page`
- **Code review:** Before deploying a scout, audit that it never reads its own past reports
- **Name reminds:** Name the file or function `scout_*` or `discover_*` — not `analyze_*` or `investigate_*`

### False positives

A scout that reports too many false positives will be ignored (or worse, the user will stop reading kanban boards). The confidence field is the primary defense, but over-confident false positives erode trust faster than under-confident misses.

**Mitigations:**
- Default to `confidence: low` for any finding the scout isn't sure about
- Add a "bot believes this is true" circuit-breaker: if the same source has produced 3+ false positives, demote its confidence ceiling to `medium`
- For Mode A scripts, avoid heuristic thresholds that trigger on borderline values (e.g., "disk > 80%" is fine; "disk > 79.3%" invites noise)
- Include raw evidence in the report body (not just the schema) so consumers can independently verify

### Signal / noise ratio

Scouts that run too frequently or check too many sources produce a report for every minor fluctuation. A kanban board filling with "Disk at 76%, Disk at 77%, Disk at 78%" is useless — the signal is buried in noise.

**Mitigations:**
- **Silent on OK:** Scouts should produce no output when nothing is wrong (watchdog pattern). The absence of a report IS the signal.
- **Cooldown:** If a scout finds the same condition (same source, similar claim) in consecutive runs, skip the report or set `confidence` to the lowest level
- **Tiered escalation:** First finding → `confidence: low` → write report. Same finding 3 runs later → `confidence: high` → write report. Same finding 10 runs later → skip.
- **Maintain a signal budget:** If a scout reports more than 3 findings per day from the same source, auto-silence it for 7 days and notify the orchestrator

## Related Skills

- **[kanban-orchestrator](../kanban-orchestrator/SKILL.md)** — reads scout reports and routes findings to workers or triage
- **[kanban-worker](../kanban-worker/SKILL.md)** — executes tasks derived from scout findings
