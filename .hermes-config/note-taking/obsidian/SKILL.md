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
├── 01-Projects/               # Active work — book, Vallentin, DABT
├── 02-Decisions/              # Architectural and design records
├── 03-Research/               # Syntheses, compilations, deep dives
└── 04-Reference/              # Permanent scaffolding
```

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

## Related references

- `references/three-layer-architecture.md` — design rationale for Mnemosyne + Obsidian + GitHub, common questions about vault setup, why not git-backed, third-party memory tool comparison.
