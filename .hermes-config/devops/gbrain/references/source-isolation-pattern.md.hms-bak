# G-Brain Source Isolation — Multi-Project Separation

## When to Use

You have multiple independent projects in the same G-Brain instance and need to prevent cross-contamination. For example: DABT toxicology study alongside a Vietnam history project. You want searches, queries, and `gbrain think` calls scoped to one project without accidentally pulling in the other's content.

## The Pattern: Isolated Sources

G-Brain supports multiple **sources** within a single brain. Sources can be:
- **`federated: true`** (default) — pages visible in cross-source searches and `source_id='__all__'` queries
- **`federated: false`** — pages isolated to that source. Only visible when querying with that specific `source_id`

### Creating an Isolated Source

```bash
# Via CLI
gbrain sources add <source-id> --name "Project Name"

# Via MCP
mcp_gbrain_sources_add(
    id="project-name",
    name="Project Name",
    federated=false
)
```

This creates an empty source. Pages are associated with it via the `source` field in frontmatter.

### Setting Page Source

Pages belong to a source via frontmatter:

```
---
type: book
source: project-name
---

# Page Content
```

When creating a page with `mcp_gbrain_put_page` or `gbrain put`, include `source: <source-id>` in the frontmatter to associate it.

### Querying Within a Source

```python
# Search only within the isolated source (MCP)
mcp_gbrain_query(
    query="search terms",
    source_id="project-name"
)

# Cross-source search (returns from ALL sources)
mcp_gbrain_query(
    query="search terms",
    source_id="__all__"
)

# Source-scoped think (synthesis limited to source context)
mcp_gbrain_think(
    question="synthesis question",
    source_id="project-name"
)
```

## Source Lifecycle

| Action | Command |
|--------|---------|
| List sources | `mcp_gbrain_sources_list()` |
| Add source | `mcp_gbrain_sources_add(id, name, federated)` |
| Remove source | `mcp_gbrain_sources_remove(id, confirm_destructive=true)` |
| Archive (soft delete) | Use `mcp_gbrain_delete_page` on individual pages |

## Real Example

This setup was used when adding a Vietnam history project alongside existing DABT toxicology content:

```bash
# DABT content lives in default source (federated) — existing setup
# Create isolated Vietnam project source
mcp_gbrain_sources_add(
    id="vietnam-project",
    name="Post-Colonial Vietnam Project",
    federated=false
)
```

Result:

| Source | Federation | Pages | Used For |
|--------|-----------|-------|----------|
| `default` | federated | 150+ | DABT study, general notes |
| `vietnam-project` | isolated | growing | Vietnam history research |

When working on the Vietnam project, queries default to `source_id='vietnam-project'`. DABT queries default to `source_id='default'`. They never cross unless explicitly passing `source_id='__all__'`.

## Slug Prefix Convention (Belt and Suspenders)

Even within isolated sources, use distinct slug prefixes to make page organization self-documenting:

| Project | Slug Prefix | Example |
|---------|-------------|---------|
| DABT | `casarett-doull/`, `hayes/`, `abt-handbook/` | `casarett-doull/10-developmental-toxicology` |
| Vietnam | `vstb/`, `vietnam/` | `vstb/viet-su-tan-bien-quyen-1` |

This makes `gbrain list --sort slug` output visually scannable regardless of source filters.

## Limitations

- **Source is a bag, not a filesystem.** Pages within a source are not organized in a hierarchy — the slug prefix is just a naming convention.
- **`mcp_gbrain_put_page` doesn't have a `source` parameter.** The source comes from the frontmatter `source:` field in the page content. If omitted, the page lands in the caller's current source context.
- **`mcp_gbrain_search` (FTS5 keyword) doesn't filter by source.** Only `mcp_gbrain_query` (vector search) supports `source_id`. For keyword-only isolation, rely on slug prefix conventions.
- **Source counts may show 0 pages** even after creating pages with matching frontmatter. The CLI's `sources list` shows counts; these refresh on sync. The page still lives in the correct source for query-time filtering.

## See Also

- gbrain docs: `docs/architecture/brains-and-sources.md` — the two-axis mental model
- gbrain skill: `sources_add` / `sources_list` tool documentation
