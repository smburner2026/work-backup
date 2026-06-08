# Multi-Vault Consolidation Playbook

Use when the user asks for an artifact sweep across multiple vaults or "find everything and put it in the second brain."

## Sources to Scan
- Sibling Obsidian vaults: `/root/obsidian-vault-mike`, `/root/obsidian-vault-historian`, `/root/obsidian-vault`
- Active project directories: `/root/work/dabt/`, `/root/work/post-colonial-vietnam/`
- Artifact directories: `/root/.hermes/cron/output/`, `/root/.hermes/lcm-large-outputs/`, `/root/.hermes/backups/`
- Staging directories: `/tmp/` (esp. `/tmp/ich-import/`, outputs from imports)
- Cache artifacts: `/root/.hermes/cache/substack/` when substantive content is cached

## Consolidation Steps
1. Build Euphy MOC cross-references to sibling vaults and discovered artifact sources.
2. Under `01-Artifacts/`, create labeled subdirectories for each source vault and copy folder structures (e.g. `mike-dabt/`, `historian-collections/`).
3. Deep scan for loose metadata assets inside `.hermes`, `/tmp`, and `~/backups`. Link them from the MOC.
4. Verify presence with a single `find` per destination folder.
5. Report counts and origins; do not claim more content than exists.

## Pitfalls
- Do not copy node_modules, caches, or plugin internals into user vaults.
- mike and historian vaults are profile-scoped; they remain the canonical homes for DABT and Vietnam work. Euphy copies are for cross-referencing, not canonical replacement.
- If source vault folders are themselves empty, do not fabricate content — report the state honestly.
- Reserved subdirs in `01-Artifacts`: `mike-dabt/`, `historian-collections/`, system exported content gets its own subdir with source prefix.
