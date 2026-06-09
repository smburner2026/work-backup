---
name: artifact-pyramids
description: Progressive disclosure pyramid for organizing artifacts (L1 Summary → L2 Analysis Collection → L3 Dossiers). Designed as a general skill for DABT (mike) and vstb (historian) work under euphy librarian ownership.
version: 1.0.0
author: TempMoon
license: MIT
---

# Artifact Pyramids Workflow

**Owner**: euphy (librarian) maintains the pyramid structure.  
**Producers**: mike (DABT) and historian (vstb) produce raw artifacts.  
**Goal**: Enable progressive disclosure so downstream agents consume only the depth they need, reducing context and token usage while preserving provenance.

## When to Use
- New DABT or vstb artifact is ready (extraction, translation, analysis, flashcards, audit output).
- The artifact would benefit from structured layers for query and consumption.

## Core Rules (non-negotiable)
1. **Profile boundaries**: mike and historian never modify pyramid files. euphy owns the conversion.
2. **No agent-to-agent handoff**: euphy delivers finished L1/L2 artifacts.
3. **Provenance**: Every L1 and L2 page must link back to the original raw file with `sources:` frontmatter and `^[raw/...]` markers.
4. **Consumption default**: Downstream agents start with L1. Escalate to L2 only when needed.

## Reference

- `references/pyramid-conventions.md` — Naming rules, directory structure, frontmatter template, L2 qualification criteria, and scan history table. Read this at the start of each housekeeping run.

## Workflow Steps

### 1. Trigger
New artifacts detected in the euphy vault (`/root/obsidian-vault-euphy/01-Artifacts/`). The skill's canonical raw paths (`mike/dabt/artifacts/raw/` and `historian/vstb/artifacts/raw/`) are the *logical* convention, but the actual euphy vault scan paths are:

**DABT scan targets** (mike profile output):
- `01-Artifacts/mike-dabt/Flashcards/*.md` — spaced-repetition flashcards (numbered sequentially)
- `01-Artifacts/mike-dabt/miss-journal/*.md` — spaced-repetition miss journal entries
- `01-Artifacts/mike-dabt/Audits/` — audit output (currently empty directory)
- `01-Artifacts/mike-dabt/Weak-Areas/` — weak area flags (currently empty directory)

**VSTB scan targets** (historian profile output):
- `01-Artifacts/historian-collections/analysis/*.md` — lens analysis files (primer + deep dives) for **VSTB**
- `01-Artifacts/historian-collections/sources/vstb/` — synthesis report + translations + glossaries
- `01-Artifacts/historian-collections/sources/chack/` — Chack/Hoang Tham materials
- `01-Artifacts/historian-collections/Background_to_Betrayal*.md` — du Berrier primary source notes
- `01-Artifacts/historian-collections/writing/*.md` — project infrastructure (charter, strategies, lens drafts)
- `01-Artifacts/historian-collections/lens*-deep.md` — lens deep-dive files for **BTB** (in vault root, NOT in `analysis/`)

**IMPORTANT**: The same logical artifact type (e.g., lens deep-dives) can appear in multiple vault locations. The `historian-collections/` root contains lens files for *Background to Betrayal* while `historian-collections/analysis/` contains lens files for *VSTB*. Scan ALL locations — do not assume a single directory per artifact type.

**Change detection**: Compare file listing and modification timestamps against the last housekeeping run (recorded in `euphy/llm-wiki/index.md` scan history). A file is "new" if it was created or modified since the last recorded scan date.

### 2. euphy Intake
- Claim the raw artifact.
- Create **L1 Summary** (mandatory):
  - Research question
  - Key findings (tied to DABT domains or 4 lenses)
  - Implications for Wiki and project ideas
- Create **L2 Analysis Collection** (when clear dimensions exist):
  - One file per domain/lens/volume
  - Technical, risk, and value breakdown

### 3. File Naming & Structure
- L1: `topic-L1-summary.md`
- L2: `topic-L2-[dimension].md`
- Store under `euphy/llm-wiki/pyramids/dabt/` or `euphy/llm-wiki/pyramids/vstb/`

### 4. Post-Write Validation (MANDATORY)
After writing each pyramid file, verify all raw file paths in `sources:` frontmatter and `^[raw/...]` markers resolve to real files:
```bash
# Write the paths to check into a tmp file from the sources: frontmatter, then:
while read p; do
  if [ ! -f "/root/obsidian-vault-euphy/$p" ]; then
    echo "BROKEN PATH: $p"
  fi
done < /tmp/sources_to_check.txt
```
Fix any broken paths immediately with `patch` before proceeding to the next file. Common errors: truncated filenames at line-wrap boundaries, double-dash typos (`01--`), missing directory segments.

## Maintenance
- euphy runs this housekeeping cron on schedule (current: daily or as configured).
- mike and historian never touch pyramid files.

### Orphan Audit Procedure
Run after every pyramid build to verify vault linking integrity.

**DO NOT use `execute_code`** — it is blocked in cron context ("Cron jobs run without a user present to approve it"). Use `terminal()` with shell commands only:

```bash
# Count all non-pyramid .md files
find /root/obsidian-vault-euphy/01-Artifacts -name "*.md" -not -path "*/euphy/llm-wiki/*" | wc -l

# Find files with outbound wikilinks
grep -r "\[\[.*\]\]" /root/obsidian-vault-euphy/01-Artifacts --include="*.md" -l | grep -v "euphy/llm-wiki"

# Check which orphans are covered by pyramid sources
find 01-Artifacts -name "*.md" -not -path "*/euphy/llm-wiki/*" | while read f; do
  rel=$(echo "$f" | sed 's|^\./||');
  if ! grep -q "$rel" euphy/llm-wiki/pyramids/ -r 2>/dev/null;
  then echo "UNCOVERED: $f"; fi;
done
```

**Expected orphan categories** (not actionable — these are leaf nodes):
- Flashcards: expected orphans (leaf content, linked from L1 summary via `sources:` frontmatter)
- Miss journal entries: expected orphans (linked from L1 summary)
- Analysis deep-dive files: expected orphans (linked from L1/L2 via `sources:` frontmatter)
- Writing files: expected orphans (internal project infrastructure)
- Translation glossaries: expected orphans (vocabulary reference, linked from L1)
- Source-tracking / family-source files: expected orphans (project management infrastructure)
- Index/README/MOC hub files: expected orphans with outbound wikilinks (navigation infrastructure → link TO content, not FROM it)

**Actionable orphans**: Any file that should be reachable via wikilinks from the MOC or another hub file but isn't. Fix by adding a wikilink from the appropriate hub.

### Index Maintenance
After every pyramid build, update `euphy/llm-wiki/index.md`:
- Add new L1/L2 entries under the correct section
- Update the "Last updated" date and "Total pages" count
- Append a scan history entry with date, new files created, and orphan count

## Provenance Verification Rule (from use-error watchlist)
- New pyramid submissions should arrive as finished L1/L2 artifacts.
- Preserve verified pyramid outputs; do not overwrite with re-extractions unless corruption is proven.
- Version markers or archived backups should be retained before refreshing any pyramid layer.

## Integration with Existing Work
- Links from existing kanban cards (DABT or vstb boards).
- No existing artifacts are rewritten — pyramid is an overlay.

## Obsidian Vault Isolation Rules (User Preference)
- Each profile maintains a **completely isolated** Obsidian vault.
- **No cross-linking, no symlinks, no shared folders** between mike, euphy, and jacob vaults.
- The pyramid system (under euphy) is the only cross-profile coordination layer.
- Intravault linking (wikilinks, backlinks, graph view) is allowed and encouraged **inside** each individual vault only.
- When the user requests vault work, default to strict isolation unless explicitly told otherwise.

## Pitfalls

1. **`execute_code` is blocked in cron context.** Always use `terminal()` for shell commands during housekeeping runs. The error message is: "Cron jobs run without a user present to approve it."

2. **Raw file path typos during bulk writes.** When writing `sources:` frontmatter with many file paths, paths can get truncated at line-wrap boundaries or acquire typos (e.g., `01--dep-dabt/` instead of `01-Artifacts/`). Always run the post-write validation step (Step 4) to catch these before moving on.

3. **Same artifact type in multiple vault locations.** Lens deep-dives, analysis files, and other artifact types may appear in more than one directory (e.g., `historian-collections/lens*-deep.md` for BTB vs. `historian-collections/analysis/lens*-deep.md` for VSTB). Scan ALL locations listed in the scan targets — do not assume a single directory per artifact type.

4. **Hub files (MOC/INDEX/README) are expected orphans.** These files have outbound wikilinks to content but typically have no inbound wikilinks. They are navigation infrastructure, not leaf content. Do not flag them as actionable orphans.

5. **First run = all artifacts are new.** On the first housekeeping run, there is no prior scan history. Treat all artifacts as new and create the full pyramid structure from scratch. The scan history in `index.md` will establish the baseline for future diffs.

## Example for DABT
- Raw: DABT weekly audit output
- L1: "DABT Weekly Truth Audit — Key weak areas and remediation priorities"
- L2: Separate files for "Domain A", "Domain B", "Risk flags"

This skill is profile-agnostic in structure but respects mike as the sole owner of all DABT artifacts.
