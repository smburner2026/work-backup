---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault — Long-Term Memory Layer

The vault is the *durable* layer in a three-tier memory architecture:
| Layer | Engine | Content | Trigger |
|-------|--------|---------|---------|
| Reflex | Mnemosyne | Facts, preferences, project context, session shorthand | Automatic every turn |
| Durable | Obsidian vault | Syntheses, decisions, research, permanent scaffolding | Anything worth reading with human eyes |
| Executable | GitHub | Scripts, tools, automation | Push on completion |

## Write-trigger discipline

**Mnemosyne keeps:** user facts, environment details, project shorthand, session pointers, anything stale in 7 days. Fast, automatic, no curation.

**Vault gets:** syntheses, architecture decisions, research compilations, reference material, anything the user would read later with human eyes. Structured, durable, curated.

**Write to the vault when you produce something the user should own as a document.** Then store a Mnemosyne pointer to the file path so you know it exists.

## Vault path

Resolved from `OBSIDIAN_VAULT_PATH` in `~/.hermes/.env`. Currently: `/root/obsidian-vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Vault structure

```
obsidian-vault/
├── MOC.md                     # Master index — links to everything
├── 01-Projects/               # Active work — book, Vallentin, DABT, trading
│   └── strategy-vault/        # Trading strategy cards (see below)
├── 02-Decisions/              # Architectural and design records
├── 03-Research/               # Syntheses, compilations, deep dives
└── 04-Reference/              # Permanent scaffolding
```

### Strategy Vault (01-Projects/strategy-vault)

A structured archive of trading setups, rules, and reference material. Each strategy gets a subdirectory with a strategy card, backtest results, and referenced examples.

```
strategy-vault/
├── traders/                   # Profile notes from trader extraction
│   └── {trader-name}/
│       └── profile.md         # Their system, rules, risk, examples
├── strategies/                # One subdirectory per strategy setup
│   └── {strategy-name}/
│       ├── card.md            # Confluence, entries, invalidation, risk, trims
│       ├── backtest/          # Simulation outputs, CSV, charts
│       └── examples/          # Screenshots with annotations
└── references/                # Raw notes, tagged sources, extracted rules
```

### Strategy Card Template (`card.md`)

Each card follows a structured format Hermes can parse for backtesting and execution:

```markdown
# Strategy: [name]
Source: [trader profile / original]
Timeframe: [H4 / 15m / etc.]
Market: [BTCUSDT]

## Confluence
- Condition 1: [e.g. above 200 MA]
- Condition 2: [e.g. OI healthy — recovering, above 30d avg]
- Condition 3: [e.g. CVD healthy — trend positive]

## Entry
- Signal: [e.g. BAMBAM bull sweep]
- Confirmation: [e.g. volume > 1.5× rolling avg]

## Invalidation
- [what breaks the setup]

## Risk
- Size: [small / martingale plan]
- No stops: [yes — asset always recovers]

## Trims / TP
- Base TP: [e.g. 10%]
- Stretch TP: [when confluence conditions are met]
- Trail: [if applicable]

## Examples
- ![chart](path/to/screenshot)
- Notes on why this setup worked/failed
```

### Hermes Board Workflow (Obsidian → Python → Hermes)

The three-layer execution pattern established for the quant trading project:

1. **User maintains** strategy notes in Obsidian vault as the source of truth.
2. **Python scripts** (backtester, data fetcher, signal generator) run the analysis — these live in `/root/work/trading/` and accept structured inputs.
3. **Hermes** acts as the control surface: reads strategy cards from Obsidian, extracts parameters, calls Python scripts with those parameters, interprets results, and writes updated strategy cards back.

Integration pattern:
- `read_file` vault note → extract parameters → `terminal("python3 script.py --param X")` → parse JSON output → `patch` or `write_file` vault note with results.
- The Hermes Board concept tracks: rules (from Obsidian), confluence (data from MCP/Coinalyze), results (from Python backtest), and webhook readiness (execution status).

Scripts directory: `/root/work/trading/scripts/` — backtesting, data collection, signal processing.
MCP stack skill: `quant-trading-mcp-stack` for the server infrastructure.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

### The agent is the linker

**Default assumption (recurring user preference): when a user asks for an Obsidian vault, they want the *agent* to do the linking, not learn the syntax.** They will explicitly say "I want you to do the linking for me" or "I don't want to do the manual links." Do not propose wikilink tutorials or hand the user the keyboard.

What this means in practice:
- When creating a concept note, *you* write the outgoing `[[wikilinks]]` to related concepts, source chapters, miss-journal entries, and MOCs.
- When writing a miss journal entry, *you* add the inbound wikilink from the entry to the concept note — the backlink panel then surfaces the connection.
- When bootstrapping a new project area, *you* run a one-shot linking pass on the existing extracted material before handing the vault to the user.
- The user reviews your links for quality, but does not write them.

If the user *does* want to learn the syntax (rare; only when they're going to maintain the vault themselves long-term), then walk them through OFM callouts, properties, and embed syntax. Otherwise: do the work.

### Kepano skills (kepano/obsidian-skills) for OpenCode / Claude Code / Codex

For LLM agents that need to write *correct* Obsidian Flavored Markdown (wikilinks, callouts, properties, Bases, Canvas, CLI), install Steph Ango's curated set at the OpenCode skills path. The skills are format references, not semantic engines — they do not auto-link — but they make the agent's output match what Obsidian expects.

Install (OpenCode — full repo, not just the `skills/` subdir):
```bash
mkdir -p ~/.opencode/skills/
git clone https://github.com/kepano/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```
Restart OpenCode after cloning — auto-discovery reads SKILL.md files on startup. The 5 skills shipped: `obsidian-markdown`, `obsidian-bases`, `json-canvas`, `obsidian-cli`, `defuddle`. See `references/kepano-skills-install.md` for the full install matrix per agent platform.

## Pointer pattern

After writing to the vault, store a Mnemosyne fact so you know the entry exists:

```
mnemosyne_remember(content="Vault entry: /root/obsidian-vault/02-Decisions/Some-Note.md — architectural decision, 2026-05-19", importance=0.6)
```

This lets you fetch the file on request without rescanning the vault every turn.

## Vaulting reference works (books, translations, databases)

When the user says "move X into the vault" for an external reference work (book translation, question bank, research corpus):

1. **Locate** the source files — find them on disk, note their paths and sizes
2. **Identify what the work IS** — not just "a book" but *its intellectual context* (author, period, genre, relation to active projects)
3. **Map the structure** — chapter breakdown, topic index, key sections. The vault note is a *map* of the work, not a copy of its raw text
4. **Write a structured vault note** with:
   - Metadata (author, title, status, date)
   - Structural outline (books/chapters/topics)
   - Source file paths (where the actual text lives)
   - Cross-references to related vault entries via [[wikilinks]]
   - Any translation or register notes
5. **Update the MOC** — add a line to the relevant section
6. **Store a Mnemosyne pointer** so the vault entry is discoverable on next turn

**Key principle:** The vault holds maps, not territory. The actual text stays in `/root/work/` (and GitHub for executables). The vault note is the index card — metadata, structure, location, significance.

**When NOT to vault a work:** If it's transient reading material, a single-use reference, or something that would be stale within a month, leave it in the working directory. The vault is for *durable reference* — material you'd want to find again a year from now.

## Pitfalls

- **Vault path is configured but doesn't exist.** `OBSIDIAN_VAULT_PATH` may point at a directory that was never created or was deleted. Always `ls -la "$path"` before doing any vault work. If the user says "I don't get the value prop" — they likely have an env-var-only setup with no actual vault. Bootstrap a minimal one or surface the gap.
- **Don't impose heavy structure on a user with a minimal README.** If the existing `wiki/README.md` says "no schema, no index, no log, no obligations," respect it. Add only what earns its keep: a concepts/ subdir and tag conventions are usually enough. Heavy structure (numbered folders, mandatory frontmatter, daily templates) is a tax the user didn't ask for.
- **Don't pitch Obsidian as a "second brain" / 100% tool.** It's a 30% tool with one genuinely unique feature (backlinks). The honest framing: "plain-text editor with backlink discovery." Anything more is hype the user will see through.
- **G-Brain-style automation without the G-Brain stack.** When the user mentions a previous AI-over-their-notes tool that "kept crashing," the migration target is plain markdown + the agent doing on-demand synthesis, not a more sophisticated engine. See `references/gbrain-to-plain-markdown-migration.md`.
- **Install ≠ integrate.** Cloning the kepano skills (or any skill) is necessary but not sufficient. The agent must actually use the new patterns — write proper OFM, use wikilinks on inbound edges, surface backlinks. Files on disk alone are dead weight.
- **Verify the right file before flagging absence.** When the project has a config (AGENTS.md, `dabt-config.json`, `package.json`, etc.) that explicitly names a path, follow *that* path — do not check sibling or parent files. Concrete failure: the DABT project has a stub `dabt.db` at the project root (0 bytes, never populated) AND a real `reference/data/dabt.db` (9.3 MB, 7,567 questions). AGENTS.md says the real one is at `reference/data/dabt.db`. Checking the wrong file and flagging "the DB is empty!" is a hard-fail — read the config, follow it, and only then claim absence.
- **Stop deliberating when the user gives an explicit go.** Signals: "proceed", "set it up now", "I have N months", "just do it", "start populating." After 1–2 clarifying turns, default to executing with safe defaults. The user has heard the menu; they want motion, not more options. Spending 12 turns on framing and value props when the user said "proceed" 3 turns ago is a hard-fail.
- **Stub quality must be functional, not empty.** A "stub" concept note is a *pull target* — definition + exam weight + source pointers + 1–2 related links. An empty stub (just a header) is dead weight and erodes the user's trust in the system. See `references/vault-bootstrap-for-study-projects.md` Phase 2 for the regenerable-stub pattern.

## Related references

- `references/three-layer-architecture.md` — design rationale for Mnemosyne + Obsidian + GitHub, common questions about vault setup, why not git-backed, third-party memory tool comparison.
- `references/vault-bootstrap.md` — step-by-step for creating a new Obsidian vault from scratch, including directory structure, MOC template, and journal entry setup.
- `references/kepano-skills-install.md` — install matrix for kepano/obsidian-skills across Claude Code, Codex, OpenCode; what each of the 5 skills covers; restart behavior.
- `references/vault-bootstrap-for-study-projects.md` — class-level recipe for "user has extracted reference material + drill DB + miss journal + an empty wiki/ folder" → vault + concept note + re-platformed miss journal. Includes Phase 2 (full population) for the "user has 80+ indexed topics and 4 months until the exam" case.
- `references/vault-maintenance-cron.md` — class-level cron patterns for keeping a study vault healthy (orphan audit, weak-area summary). No-LLM, no_agent scripts that deliver summaries to the user. Applies to DABT, USMLE, CFA, bar prep — any structured-vault study workflow.
- `references/gbrain-to-plain-markdown-migration.md` — pattern for moving a G-Brain-coupled skill (miss journal, recall, takes) to filesystem when G-Brain is decommissioned. What survives, what doesn't, how to backfill.
