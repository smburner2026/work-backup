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

## Workflow Steps

### 1. Trigger
Raw artifact placed in `mike/dabt/artifacts/raw/` or `historian/vstb/artifacts/raw/`.

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

## Maintenance
- euphy runs quarterly audit for orphaned L1 summaries and provenance gaps.
- mike and historian never touch pyramid files.

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

## Example for DABT
- Raw: DABT weekly audit output
- L1: "DABT Weekly Truth Audit — Key weak areas and remediation priorities"
- L2: Separate files for "Domain A", "Domain B", "Risk flags"

This skill is profile-agnostic in structure but respects mike as the sole owner of all DABT artifacts.
