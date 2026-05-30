# G-Brain DABT Usage

## Why G-Brain First

The DABT reference library (106 pages, 6,597 chunks) is imported into G-Brain. Vector search finds relevant passages across ALL sources simultaneously — something file search on individual source directories cannot do. `gbrain think` synthesizes across multiple sources and flags gaps/contradictions.

## In-Session Commands (MCP Tools)

These are always available — no terminal needed:

```
# Semantic search across all DABT reference material
mcp_gbrain_query(query="Ames test bacterial strains S9 activation", limit=5)

# Cross-source synthesis with gap analysis
mcp_gbrain_think(question="compare mechanisms of acetaminophen hepatotoxicity and carbon tetrachloride hepatotoxicity")

# Quick topic to chapter mapping
mcp_gbrain_query(query="dose-response assessment risk assessment paradigm", limit=3)
```

## Terminal Commands (when MCP returns insufficient depth)

```
# Direct CLI search (falls through to the same vector DB)
gbrain search "mechanism of hepatotoxicity paracetamol NAPQI"

# Cross-source synthesis with auto-gap analysis
gbrain think "explain the difference between Ames test and mouse lymphoma assay in terms of endpoint, cell type, and genetic basis"

# Keyword search when vector search is too broad
gbrain search "OECD TG 425 acute toxicity" --detail low
```

## Topic → G-Brain Query Patterns

| Topic | Example query | What to expect |
|-------|---------------|----------------|
| Genotoxicity testing | `gbrain think "Ames test vs mouse lymphoma vs micronucleus: which detects what"` | Synthesis across C&D Ch.9 + ICH S2(R1) |
| Dose-response | `gbrain think "compare NOAEL, LOAEL, BMD approaches for risk assessment"` | C&D Ch.4 + Hayes Ch.3 |
| ADME/Toxicokinetics | `gbrain query "enterohepatic circulation toxicokinetics"` | C&D Ch.5-7 |
| Regulatory guidelines | `gbrain search "ICH S5 reproductive toxicity testing"` | ICH S5(R3) full text |
| Metals toxicity | `gbrain think "arsenic vs mercury: mechanisms, targets, treatment"` | C&D Ch.23 |
| Carcinogenesis | `gbrain think "initiation promotion progression genotoxic non-genotoxic"` | C&D Ch.8 |

## Pitfalls

- **G-Brain chunks are text, not page-accurate.** The chunks preserve the content but strip extraction headers (`# Pages: X-Y`). For exact page citations, always verify against the source extraction file using file search.
- **Large files (>500KB) are soft-blocked from embedding.** C&D Ch.6 (biotransformation, 1.27MB), FDA Silverbook (1.4MB), and similar oversized files land as metadata-only — they're FTS5 searchable but invisible to vector search. If G-Brain returns nothing for a biotransformation query, fall back to file search against `extracted/casarett-doull-9e/6-biotransformation-of-xenobiotics.txt`.
- **`gbrain think` requires a configured chat model.** The brain uses the `models.think` config key. If `gbrain think` fails with "no LLM available", use `mcp_gbrain_query` instead (search only, no synthesis). Check `gbrain models` to verify.
- **G-Brain has no knowledge graph structure.** Zero links between chapters, zero tags, zero timeline entries. Do not expect `gbrain traverse` or `gbrain get_links` to return useful DABT connections. The brain is a flat vector + FTS5 index.
- **G-Brain does not track session data.** Drill results, deep dive notes, flashcards — none of this lands in G-Brain. It's a reference library, not a session state tracker.

## Verification Before a DABT Session

```bash
# Quick health check
gbrain doctor --json | grep -E 'embedding_coverage|chunk_count|page_count'

# Should show: page_count >= 106, chunk_count >= 6000

# Smoke test a core topic
gbrain search "Ames test" | head -5
# Should return hits from C&D Ch.9 + ICH S2(R1)
```

If the DABT library isn't imported:
```bash
# Import all reference pages from ~/brain/
gbrain import ~/brain/ --timeout 300000
```
