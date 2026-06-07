# Three-Layer Memory Architecture — Design Rationale

> Why an agent needs three memory tiers, not one, and what goes where.

## The problem with a single memory system

When users ask "should I use Obsidian or Mnemosyne?" or "is GitHub memory the same as a vault?" — the correct answer is **both, but for different things**. Each layer serves a different retrieval pattern:

| Layer | Query latency | Curation | Volatility | Access pattern |
|-------|--------------|----------|------------|----------------|
| Mnemosyne | <200ms | Automatic (agent) | Hours–days | Every turn, subconscious |
| Obsidian | ~2s (file read) | Human + agent | Months–years | On request, browse |
| GitHub | Pull + execute | Versioned (agent) | Permanent | When running tools |

Forcing everything into one layer creates:
- **Just Mnemosyne:** agent can retrieve fast but *you* can't browse or edit the knowledge
- **Just Obsidian:** agent has to search markdown files every turn, slow and fragile
- **Just GitHub:** neither fast retrieval nor human readability

## The trigger question

The hardest design problem: what earns a seat in the vault vs. stays in Mnemosyne?

**Test:** would you read this with human eyes a month from now?
- Yes → vault
- No → Mnemosyne

**Practical rule of thumb:**

Mnemosyne holds *operational context* — things that help me answer your next question correctly. Preferences, environment paths, project shorthand, what we were talking about. High churn, low permanence.

Obsidian holds *durable knowledge* — things you'd want to find and re-read. Architectural decisions, research syntheses, schemas, permanent scaffolding, any document I produce that you should *own*.

## Pointer pattern

When I write to the vault, I store a Mnemosyne fact pointing to the file path. This means next session I know the entry exists without scanning the vault. The pointer is the bridge between fast retrieval (I know where it is) and human readability (you open the file).

## Vault structure convention

```
vault/
├── MOC.md               # Master index — the entry point
├── 01-Projects/         # Active work — one note per project
├── 02-Decisions/        # Architectural and design records
├── 03-Research/         # Syntheses, compilations, deep dives
└── 04-Reference/        # Permanent scaffolding, profiles, source material
```

Numbered prefixes keep folder ordering stable across clients. MOC at root links to everything via `[[wikilinks]]`.

## Common questions

**Q: Does Obsidian require an account/signup?**
A: No. The desktop app is free, works fully offline, no registration needed. Obsidian Sync (cloud) is a paid add-on but entirely optional. The vault is just a folder of markdown files.

**Q: Should the vault be git-backed?**
A: Usually not for the vault itself. Wikilinks don't survive git's file-based versioning well, and markdown files benefit more from filesystem sync (Syncthing, rclone, iCloud) than from git history. Keep GitHub for *executable* artifacts (scripts, tools). The vault is a knowledge commons, not a codebase.

**Q: What about Honcho / Mem0 / MemGPT?**
A: These compete with Mnemosyne's tier, not Obsidian's. If you already have Mnemosyne, adding Honcho is redundant — Mnemosyne does the same job locally without a network hop. The vault layer is complementary to all of them.
