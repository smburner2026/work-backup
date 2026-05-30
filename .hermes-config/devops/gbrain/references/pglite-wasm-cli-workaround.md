# PGLite WASM CLI Workaround

## Symptom

Fresh `gbrain` CLI invocations fail with:

```
PGLite failed to initialize its WASM runtime.
  Most common cause: the macOS 26.3 WASM bug
  (https://github.com/garrytan/gbrain/issues/223).
  Run `gbrain doctor` for a full diagnosis.
  Original error: Aborted(). Build with -sASSERTIONS for more info.
```

This happens even on Linux — the error message references a macOS bug but the root cause is broader: PGLite's WASM runtime can only be initialized once per process. Each fresh CLI invocation tries to init from scratch and fails.

## The Pattern

The MCP server (`gbrain serve`) keeps the WASM runtime alive for the lifetime of the server process. So **MCP tools work when the CLI doesn't**.

| Operation | CLI | MCP tool | 
|---|---|---|
| Search | `gbrain search "query"` → ❌ WASM error | `mcp_gbrain_query(query="...")` → ✅ |
| Think/synthesis | `gbrain think "question"` → ❌ WASM error | `mcp_gbrain_think(question="...")` → ✅ |
| Health check | `gbrain doctor --json` → ❌ WASM error | `mcp_gbrain_get_health` → ✅ |
| Tag a page | `gbrain tag slug tag` → ❌ WASM error | `mcp_gbrain_add_tag(slug, tag)` → ✅ |
| List pages | `gbrain list` → ❌ WASM error | `mcp_gbrain_list_pages` → ✅ |
| Get page content | `gbrain get slug` → ❌ WASM error | `mcp_gbrain_get_page(slug)` → ✅ |
| Add link | `gbrain link from to --type T` → ❌ WASM error | `mcp_gbrain_add_link(from, to, link_type)` → ✅ |
| Submit job | `gbrain jobs submit embed` → ❌ WASM error | `mcp_gbrain_submit_job(name, data)` → ✅ |
| Page stats | `gbrain stats` → ❌ WASM error | `mcp_gbrain_get_stats` → ✅ |

## Why It Happens

PGLite is a PostgreSQL-compatible database that runs as WASM inside the Bun process. The WASM module is compiled into the Bun binary. Some Bun versions/Linux configurations can't initialize a new PGLite WASM instance in a fresh process (the `Aborted()` comes from the WASM trap handler).

The MCP server initializes PGLite once on startup and keeps the instance alive. Any tools dispatched through the MCP server reuse that instance.

## Workaround Rules

1. **For any gbrain interaction, try MCP tools first.** They're always available when Hermes is configured with the gbrain MCP server.
2. **Only fall back to CLI when no MCP equivalent exists** (e.g., `gbrain config set`, `gbrain init`, `gbrain import` — these have no MCP equivalent).
3. **For batch operations** (mass tagging, bulk import), use the MCP tools one at a time, or submit a background job via `mcp_gbrain_submit_job`.
4. **CLI `gbrain doctor --json` may still work** for filesystem-only checks (it degrades gracefully). But any operation requiring DB access fails.

## Affected Commands (all fail with fresh CLI)

- `gbrain search` / `gbrain query` / `gbrain think`
- `gbrain tag` / `gbrain tags` / `gbrain untag`
- `gbrain list` / `gbrain get` / `gbrain delete`
- `gbrain link` / `gbrain unlink` / `gbrain backlinks`
- `gbrain embed`
- `gbrain extract links`
- `gbrain stats`
- `gbrain jobs`

## Unaffected (work because MCP equivalent exists)

All ~30 `mcp_gbrain_*` tools.

## Dirty Data Directory Recovery

**The "PGLite WASM" error can also mean the existing data directory is in a dirty/crashed state.** This was confirmed on v0.41.20.0 upgrade: the error was identical (`Aborted(). Build with -sASSERTIONS...`) but the root cause was a stale `postmaster.pid` from a prior failed migration, not a genuine WASM incompatibility.

### Diagnostic Flow

When PGLite CLI commands fail with the WASM error, distinguish between two causes:

```
1. Test with a FRESH tmp directory:
   $ cd ~/gbrain && $HOME/.bun/bin/bun -e "
     import { PGlite } from '@electric-sql/pglite';
     const db = await PGlite.create('/tmp/pglite-diag');
     const r = await db.query('SELECT 1 as test');
     console.log('FRESH DIR OK:', JSON.stringify(r.rows));
     await db.close();
   "
   => SUCCESS: WASM runtime fine, data dir is the problem.
   => FAILURE: genuine WASM incompatibility. Use MCP tools.

2. Test with the EXISTING data directory:
   $ cd ~/gbrain && $HOME/.bun/bin/bun -e "
     import { PGlite } from '@electric-sql/pglite';
     import { vector } from '@electric-sql/pglite/vector';
     import { pg_trgm } from '@electric-sql/pglite/contrib/pg_trgm';
     const db = await PGlite.create({
       dataDir: '/root/.gbrain/brain.pglite',
       extensions: { vector, pg_trgm },
     });
     const r = await db.query('SELECT 1');
     await db.close();
   "
   => FAILURE while fresh dir works: dirty/corrupt data directory.

3. Check for stale postmaster.pid:
   $ cat /root/.gbrain/brain.pglite/postmaster.pid
```

### Recovery

**When the data directory is dirty but the backup is clean:**

```bash
ls -la /root/.gbrain/brain.pglite.bak/
mv /root/.gbrain/brain.pglite /root/.gbrain/brain.pglite.dirty
cp -a /root/.gbrain/brain.pglite.bak /root/.gbrain/brain.pglite
gbrain apply-migrations --yes --non-interactive
set -a; source /root/.hermes/.env 2>/dev/null; set +a
gbrain import ~/brain/
gbrain search "test query"
```

**When there's no backup, try removing stale postmaster.pid first:**

```bash
rm -f /root/.gbrain/brain.pglite/postmaster.pid
# Then retry
```

### Root Cause Chain

1. `gbrain apply-migrations` starts => PGLite creates postmaster.pid
2. Migration fails => postmaster.pid left behind
3. Next invocation reads stale pid => PGLite reports "Aborted()"
4. Error wrapped as "WASM runtime" issue => misleading

### Prevention

After any failed migration, clean up:
```bash
rm -f /root/.gbrain/brain.pglite/postmaster.pid
```

## MCP Server Lock Conflict

Separate `gbrain` CLI commands (sync, embed --stale, extract) hang with "Timed out waiting for PGLite lock" when the MCP server is running. This is lock contention, not WASM.

| Operation | With MCP Server | Without MCP Server |
|-----------|----------------|-------------------|
| sync | ❌ Hangs | ✅ Works |
| embed --stale | ❌ Hangs | ✅ Works |
| extract links --source db | ❌ Hangs | ✅ Works |
| doctor --json | ⚠️ Intermittent | ✅ Full |
| dream --dir ~/brain/ | ✅ Works | ✅ Works |

Stop MCP server before CLI commands:
```bash
pkill -f "gbrain serve" 2>/dev/null || true; sleep 2
gbrain sync --repo ~/brain/
```

### Stale Cycle Lock Recovery

If `gbrain dream` is OOM-killed, it leaves a row in `gbrain_cycle_locks` with `id='gbrain-cycle'` (TTL ~30min). Subsequent dream calls fail with "cycle_already_running".

Recovery:
```bash
cd ~/gbrain && $HOME/.bun/bin/bun -e "
import { PGlite } from '@electric-sql/pglite';
import { vector } from '@electric-sql/pglite/vector';
const db = await PGlite.create({dataDir:'/root/.gbrain/brain.pglite',extensions:{vector}});
await db.query(\"DELETE FROM gbrain_cycle_locks WHERE id='gbrain-cycle'\");
await db.close();
"
```

Or wait for TTL expiry (~30 min).

## Related

- gbrain issue [#223](https://github.com/garrytan/gbrain/issues/223)
- gbrain issue [#218](https://github.com/garrytan/gbrain/issues/218)