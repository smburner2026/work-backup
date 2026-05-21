# Three-Layer Memory System

> Decision record: 2026-05-19

## The Architecture

| Layer | Engine | Purpose | Retrieval |
|-------|--------|---------|-----------|
| Reflex | **Mnemosyne** | Facts, preferences, project context, session recall | Automatic, every turn — subconscious |
| Durable | **Obsidian vault** | Syntheses, decisions, research, permanent scaffolding | On request / human browse |
| Executable | **GitHub** | Scripts, tools, automation, artifacts | Git pull / execution |

## Write Triggers (What Goes Where)

**Mnemosyne keeps:**
- User facts and preferences
- Environment details (paths, keys, tool quirks)
- Session recall pointers
- Project shorthand (what's active, rough state)
- Things that would be stale in 7 days

**Obsidian gets:**
- Anything worth reading with human eyes later
- Architecture and design decisions (like this one)
- Research syntheses and compilations
- Permanent intellectual scaffolding
- Reference material that doesn't change week-to-week

**GitHub gets:**
- Scripts that execute
- Artifacts worth versioning
- Automation and tooling
- Never conversation logs, config, or .env

## The Pointer Pattern

When I write something to the Obsidian vault, I store a Mnemosyne fact pointing to the file path. This way I know the entry exists and can fetch it on request without rescanning the vault every turn.

---

*Vault path:* `/root/obsidian-vault`
*Obsidian app:* Free, no account required — available at obsidian.md
