# Bootstrapping an Obsidian Vault from Scratch

When the Obsidian vault path is configured in `~/.hermes/.env` as `OBSIDIAN_VAULT_PATH` but the directory doesn't exist, this is a greenfield vault — create it from scratch.

## When to Use

- The user says "save this to Obsidian" but the vault hasn't been created yet
- `OBSIDIAN_VAULT_PATH` is set in `.env` but `ls <path>` shows "No such file or directory"
- The user wants to migrate from flat-file storage to Obsidian

## Procedure

### Step 1 — Resolve the vault path

```
grep OBSIDIAN_VAULT_PATH /root/.hermes/.env
```

### Step 2 — Create the directory structure

Standard layout:

```bash
mkdir -p /root/obsidian-vault/{01-Projects,02-Decisions,03-Research,04-Reference,05-Journal}
```

Common folder conventions:

| Folder | Contents |
|--------|----------|
| `01-Projects/` | Active work — ongoing tasks, books, certifications |
| `02-Decisions/` | Architectural and design records (ADRs) |
| `03-Research/` | Syntheses, compilations, deep dives |
| `04-Reference/` | Permanent scaffolding — reference material |
| `05-Journal/` | Personal daily journal entries (captain's log) |

### Step 3 — Create the Map of Content (MOC.md)

The MOC is the vault's entry point. It links to every top-level section and can include one-line descriptions of important entries.

Example template:

```markdown
# Map of Content

## 05-Journal
Personal daily journal entries — captain's log style.
- [[YYYY-MM-DD]] — One-line summary

## 01-Projects
Active work.

## 02-Decisions
Architectural and design records.

## 03-Research
Syntheses, compilations, deep dives.

## 04-Reference
Permanent scaffolding.
```

### Step 4 — Create a journal section index

In `05-Journal/`, create a `.meta.md` index file:

```markdown
# Personal Journal

Daily captain's log entries. Named as `YYYY-MM-DD.md`.

- [[YYYY-MM-DD]]
```

### Step 5 — Save the first entry

For each journal entry, create `05-Journal/YYYY-MM-DD.md` in the standard format:

```markdown
**YYYY-MM-DD Day**

Oh sir... [narrative text]
```

### Step 6 — Update the MOC

After creating any significant entry, add a one-line link to the MOC:
- `- [[YYYY-MM-DD]] — Brief topic`

### Step 7 — Store a Mnemosyne pointer (optional)

```python
mnemosyne_remember(
    content="Vault entry: /root/obsidian-vault/05-Journal/2026-05-27.md — journal entry",
    importance=0.3
)
```

### Step 8 — Update the skill

If the previous storage path was outside Obsidian (e.g., `/root/journal/personal/YYYY-MM-DD.md`), update the governing skill to point to the vault instead:
- Use `skill_manage(action='patch', name='<skill>', old_string='<old path>', new_string='<vault path>')`

## Pitfalls

- **Don't use shell variables in file tool paths** — `$OBSIDIAN_VAULT_PATH` doesn't expand in `read_file`/`write_file`. Resolve to an absolute path first.
- **Vault paths may contain spaces** — file tools handle this; shell commands need quoting.
- **The vault is reference, not territory** — the Obsidian skill principle: vault holds maps and metadata; actual raw data (corpora, databases, large texts) stays in `/root/work/`.
- **Mnemonic pointers are lightweight** — `importance=0.3` is fine for vault pointers. The pointer just says "this file exists," not "this is critical user data."
