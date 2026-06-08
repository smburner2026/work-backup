---
name: hermes-output-integrity
description: Diagnose and prevent output truncation in Hermes agent responses across Telegram, Discord, and CLI.
---

# Hermes Output Integrity

Prevent fragmented, empty, or cut-off assistant outputs across messaging platforms.

## Symptoms

- User sees "(empty)" assistant messages in session history
- Responses end abruptly or are split across multiple empty turns
- session_search returns bookends with empty assistant content
- Cron-delivered reports missing body text

## Detection

```bash
# Count empty assistant turns in recent cron sessions
grep -c '"role": "assistant", "content": ""' /root/.hermes/cron/output/*/*.jsonl

# Find truncated recent sessions
find /root/.hermes/sessions -name '*.jsonl' -mtime -1 -size +100k
```

## Root Causes

1. **Platform message caps** — Telegram/Discord have per-message length limits.
2. **Compression-induced context shrink** — aggressive LCM/session compression reduces effective output window.
3. **Approval gate failures** — tool calls requiring approval with no fallback produce empty outputs.
4. **Cron mode restrictions** — cron jobs in restricted toolset mode may have narrower output paths.
5. **Multi-model switching** — context loss during grok/xai/stepfun model swaps.

## Fixes

### Immediate

- Break long outputs into chunks with explicit "PART 1 / PART 2" markers.
- For cron jobs: ensure final response is in the assistant message body, not just in tool call args.
- For session restoration: after recovery, validate with `session_search` that content is retrievable.

### Config

- Review `config.yaml` compression settings if truncation correlates with compaction events.
- Check for output caps in `config.yaml` under gateway/channel sections.

### Monitoring

- Add sanity check in nightly infrastructure report: scan recent cron outputs for empty assistant turns.
- Flag any assistant message with `content == ""` and `tool_calls == []`.

## User Preference

- "No incomplete/cut-off responses" — prefer chunked delivery over truncated single messages.
- "Direct, non-repetitive output" — avoid filler sign-offs that consume output budget.
