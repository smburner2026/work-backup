---
name: source-provenance-tracker
description: "Track provenance of every extracted fact — source, page, excerpt, confidence. Cross-reference sources, flag contradictions, build a citable research knowledge base."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [history, provenance, citations, cross-reference, knowledge-base, research]
    category: research
    related_skills: [historical-source-acquisition, historical-source-extraction]
    requires_toolsets: [file, search]
---

# Source Provenance Tracker

Track where every extracted fact came from. Cross-reference multiple sources. Flag contradictions. Build a research-grade knowledge base with full citations.

## When to Use

- User has extracted data from multiple historical sources and needs to track provenance
- User wants to cross-reference facts across sources
- User wants to identify contradictions or discrepancies between sources
- User wants a citable knowledge base for a research project
- User asks "where does this fact come from?" or "do these sources agree?"

## Core Principle

**Every fact must have a provenance chain:** source → page → excerpt → confidence.

A fact without provenance is an assertion. A fact with provenance is evidence.

## The Provenance Model

### Fact Record Structure

Every extracted fact gets this metadata:

```json
{
  "fact_id": "uuid",
  "claim": "John Smith was a carpenter in 1875",
  "subject": "John Smith",
  "predicate": "occupation",
  "object": "carpenter",
  "provenance": {
    "source_slug": "chicago-directory-1875",
    "source_title": "Chicago City Directory 1875",
    "page": 42,
    "excerpt": "Smith, John — carpenter — 123 Main St",
    "extraction_date": "2026-05-29",
    "confidence": "high"
  },
  "tags": ["occupation", "chicago", "1875"]
}
```

### Local File-Based Provenance Tracking

Store all provenance data in markdown files within a `provenance/` directory:

**1. Per-source provenance files:**
```
provenance/<source-slug>/
├── facts.md          # All facts extracted from this source
├── metadata.json     # Source metadata (title, date, quality)
└── timeline.md       # Timeline entries with provenance
```

**2. Cross-source links file:**
```markdown
# provenance/cross-references.md

## Cross-Source Links

### Chicago 1875 ↔ Chicago 1880
- **Link type:** same_city_different_year
- **Context:** Same city directory series, 5 years apart
- **Sources:** chicago-1875, chicago-1880

### Chicago 1875 ↔ Census 1880
- **Link type:** corroborates
- **Context:** John Smith appears in both sources with same occupation
- **Sources:** chicago-1875, census-1880-il
```

**3. Timeline entries:**
```markdown
# provenance/timeline.md

## 1875
- **John Smith — carpenter — 123 Main St**
  - Source: Chicago Directory 1875, p.42
  - Detail: Full entry from city directory
```

## Cross-Referencing Workflow

### Step 1 — Build a Fact Index

After extracting from multiple sources, compile a fact index:

```markdown
## Fact Index: <Research Topic>

### Subject: John Smith

| Fact | Source 1 | Source 2 | Source 3 | Status |
|------|----------|----------|----------|--------|
| Occupation: carpenter | Chicago 1875, p.42 | Census 1880, p.12 | ✅ Confirmed |
| Address: 123 Main St | Chicago 1875, p.42 | Chicago 1880, p.55 | ✅ Confirmed |
| Age: 35 | — | Census 1880, p.12 | Single source |
| Born: Ireland | — | Census 1880, p.12 | Single source |
```

### Step 2 — Identify Agreement and Contradiction

For each fact found in multiple sources:

**Agreement (✅):**
- Same information in 2+ sources → high confidence
- Note: agreement doesn't guarantee truth, but strengthens the claim

**Contradiction (⚠️):**
- Different information in 2+ sources → flag for resolution
- Common causes: OCR errors, different people with same name, different time periods, transcription errors
- Resolution: check original source quality, look for additional corroborating evidence

**Single source (📝):**
- Only one source has this fact → note as unconfirmed
- Look for additional sources to corroborate

### Step 3 — Contradiction Resolution

When sources disagree:

1. **Check source quality** — which source is more authoritative? Government record > newspaper > personal account
2. **Check date proximity** — which source is closer to the event?
3. **Check OCR quality** — is the contradiction an OCR error?
4. **Check for same-name confusion** — are these the same person?
5. **Look for additional sources** — can a third source resolve the contradiction?
6. **Document the ambiguity** — if unresolvable, note both claims with their provenance

```markdown
### Contradiction Report

**Fact:** John Smith's occupation
**Source A:** "carpenter" (Chicago Directory 1875, p.42, confidence: high)
**Source B:** "builder" (Census 1880, p.12, confidence: medium)
**Analysis:** "Carpenter" and "builder" are related but distinct occupations.
Both could be accurate if Smith changed jobs between 1875-1880.
**Resolution:** Keep both facts with date context. Note the career change.
```

## Provenance Query Patterns

### "Where does this fact come from?"

```bash
# Search provenance files for the fact
grep -r "John Smith" provenance/

# Check specific source's facts
cat provenance/chicago-1875/facts.md
```

### "What do we know about X from all sources?"

```bash
# Search all provenance files
grep -r "John Smith" provenance/ --include="*.md"

# Compile facts from all sources
cat provenance/*/facts.md | grep -A2 "John Smith"
```

### "Do sources A and B agree on X?"

```bash
# Read both sources' fact files
cat provenance/chicago-1875/facts.md
cat provenance/census-1880-il/facts.md

# Compare specific facts (manual or scripted)
```

## Output: Research Knowledge Base

The end product is a structured knowledge base with full provenance:

```
research/
├── provenance/
│   ├── <source-slug>/
│   │   ├── facts.md          # All facts extracted from this source
│   │   ├── metadata.json     # Source metadata
│   │   └── timeline.md       # Timeline entries with provenance
│   ├── cross-references.md   # Cross-source links
│   ├── timeline.md           # Master timeline with provenance
│   └── provenance-index.json # Master index of all facts
├── knowledge-base/
│   ├── subjects/
│   │   ├── john-smith.md          # All facts about John Smith
│   │   └── ...
│   ├── contradictions.md           # All unresolved contradictions
│   ├── source-agreements.md        # Facts confirmed by multiple sources
│   └── single-source-claims.md     # Facts needing corroboration
└── sources/
    ├── chicago-1875/
    │   ├── original.pdf
    │   ├── extracted.txt
    │   ├── metadata.json
    │   └── extraction.json
    └── ...
```

### Subject Fact Sheet Format

```markdown
# John Smith

## Facts

### Confirmed (multiple sources)
- **Occupation:** carpenter → builder (career change between 1875-1880)
  - Source 1: Chicago Directory 1875, p.42 — "Smith, John — carpenter"
  - Source 2: Census 1880, p.12 — "Smith, John — builder"
- **Address:** 123 Main St, Chicago
  - Source 1: Chicago Directory 1875, p.42
  - Source 2: Chicago Directory 1880, p.55

### Single Source (needs corroboration)
- **Age:** 35 (in 1880)
  - Source: Census 1880, p.12 — "Smith, John — age 35"
  - Implies birth year ~1845
- **Birthplace:** Ireland
  - Source: Census 1880, p.12

### Contradictions
- None found

## Sources
1. Chicago City Directory 1875 (archive.org, downloaded 2026-05-29)
2. US Census 1880, Illinois (familysearch.org, downloaded 2026-05-29)
```

## Pitfalls

- **Don't lose provenance during extraction.** Every record must carry its source/page/excerpt. If you're extracting in batches, make sure each batch includes provenance metadata.
- **Name matching is hard.** "John Smith" in one source might be "J. Smith" or "Smith, John" or "John Smyth" in another. Normalize names for matching but preserve original spellings.
- **Dates are tricky.** Old sources may use different calendar systems, fiscal years, or dating conventions. Note the dating system used.
- **Don't over-link.** Only create cross-source links when you're confident the same entity appears in both sources. A wrong link is worse than no link.
- **Contradictions are information.** Don't suppress them. A contradiction between sources is itself a finding worth documenting.
- **Keep the original.** Never modify the extracted text or original PDF. Provenance tracking is additive, not destructive.

## Verification

After completing the workflow:
1. ✅ All extracted facts have provenance metadata
2. ✅ Cross-source facts identified and linked
3. ✅ Contradictions flagged with resolution attempts
4. ✅ Single-source facts noted for future corroboration
5. ✅ Subject fact sheets created with full citations
6. ✅ Provenance files created in `provenance/` directory
