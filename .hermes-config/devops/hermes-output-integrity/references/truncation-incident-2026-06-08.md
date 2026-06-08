# Output Truncation Incident — 2026-06-08

## Symptoms observed

- Long skill_manage outputs caused by two sequential `create` calls were not delivered as a single final chunk.
- User asked "Why are getting cut off" — indicating truncation, not just multi-tool delay.

## Likely causes

1. Telegram message length constraint
2. Compression/session threshold reducing effective output window mid-response
3. Multi-step tool result formatting

## Immediate mitigations applied

- Split long operations across multiple turns with explicit deliverables.
- Keep core instruction blocks concise.
- Break agent memory and skill lists into compact entries.

## Monitoring

- Re-run after creating umbrella skills: check whether tool result delivery completes.
- If truncation persists, inspect `config.yaml` for per-channel message caps.
