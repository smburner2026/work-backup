# Content Sanity Audit — Inspector's Guide

GBrain runs a content-sanity audit on every import and every dream cycle. Results live in `~/.gbrain/audit/content-sanity-*.jsonl`. Each line is one event.

## Event Types

| event_type | Color | Meaning |
|-----------|-------|---------|
| `warn` | Yellow | Page >50KB — embedded but flagged as oversized. Precision may suffer on narrow queries. |
| `soft_block` | Orange | Page >500KB — file exists in brain dir but was **not embedded**. Not searchable via vector search. Text is reachable via FTS5 keyword search only. |
| `hard` | Red | Page has junk patterns, broken content, or corruption. Rare on clean imports. |

## How to Inspect

```bash
# Count by event type
python3 -c "
import json
events = {'warn': 0, 'soft_block': 0, 'hard': 0}
with open('/root/.gbrain/audit/content-sanity-*.jsonl') as f:
    for line in f:
        e = json.loads(line)
        events[e.get('event_type', 'unknown')] += 1
print(events)
"

# Show soft_block pages (not embedded)
python3 -c "
import json
with open('/root/.gbrain/audit/content-sanity-2026-W*.jsonl') as f:
    for line in f:
        e = json.loads(line)
        if e.get('event_type') == 'soft_block':
            for r in e.get('reason_messages', []):
                print(f\"{e['slug']} — {r}\")
"

# Show most common warning reasons
python3 -c "
import json
from collections import Counter
reasons = Counter()
with open('/root/.gbrain/audit/content-sanity-2026-W*.jsonl') as f:
    for line in f:
        e = json.loads(line)
        for r in e.get('reason_messages', []):
            reasons[r] += 1
for r, c in reasons.most_common(10):
    print(f'{c:4d}x  {r}')
"
```

## How to Interpret

### warn (PAGE_OVERSIZE_WARN)
- Page is embedded and searchable via vector + FTS5
- The chunker split it but each chunk may be larger than ideal
- **Action:** Usually none. Only re-split if you notice precision problems on narrow queries about that document.

### soft_block (PAGE_OVERSIZED >500KB)
- Page exists in the brain directory's markdown files
- GBrain intentionally refused to embed it because a single 500KB+ file can't be chunked intelligently
- **Not searchable via `gbrain search` (vector)** — but still reachable via FTS5 full-text search if gbrain's search mode includes keyword fallback
- **Action:** Split the markdown file by section headings (`##` or `#`) into separate files (~50-200KB each), then re-import
- Typical candidates: textbook chapters, massive regulatory documents (FDA Redbook, Silverbook), long handbook sections

### Duplicate Events
Each file may appear twice in the audit log (once per import or dream cycle). Dedupe by slug when counting.

## Common Findings on Textbook/Regulatory Imports

| Pattern | Typical files | Fix |
|---------|-------------|-----|
| warn on regulation docs | `tg4XX.md`, `s1X-guideline.md` (50-100KB) | None needed — precision is fine |
| warn on textbook chapters | `casarett-doull-9e/ch*.md` (50-400KB) | Optional split if precision matters |
| soft_block | Silverbook (1.4MB), Redbook (1.0MB), large textbook chapters (500KB+) | Must split to get vector search coverage |

## Affect on gbrain search

- `gbrain search "query"` — vector search only. Results exclude soft_blocked pages entirely.
- `gbrain think "query"` — synthesis may still reference soft_blocked pages if it finds them via other means (graph traversal, FTS5). But without ANTHROPIC_API_KEY, think doesn't work anyway (separate issue).
