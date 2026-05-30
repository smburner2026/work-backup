# G-Brain Integration for DABT Reference

## Status

All 106 reference pages (Casarett 9e, Hayes 7e, 60 regulations, ABT handbook) are imported into G-Brain at `~/brain/`. Total: 6,597 embedded chunks, 51MB.

## Quick Commands

```bash
# From ~/brain/ or any directory with PATH to gbrain
gbrain search "mechanism of hepatotoxicity"
gbrain think "compare Ames test and mouse lymphoma assay protocols"
gbrain search "OECD TG 425 acute toxicity"
```

## What's in G-Brain

| Source | Files | Import path |
|--------|-------|-------------|
| Casarett & Doull 9e | 35 chapters | `extracted/casarett-doull-9e/*.txt` → `~/brain/extracted/casarett-doull-9e/*.md` |
| Hayes 7e | 39 chapters | `extracted/hayes-7e/*.txt` → `~/brain/extracted/hayes-7e/*.md` |
| Regulations | 60 docs | `extracted/regulations/*.txt` → `~/brain/extracted/regulations/*.md` |
| ABT Handbook | 5 files | `extracted/abt-handbook/*.txt` → `~/brain/extracted/abt-handbook/*.md` |

## Updating G-Brain

When new reference material is added:

```bash
# Extract text to the dabt-tutor reference/extracted directory first
# Then convert to .md (skip .hms-bak files)
for f in /root/work/dabt/dabt-tutor/reference/extracted/<source>/*.txt; do
  [[ "$f" == *.hms-bak ]] && continue
  base=$(basename "$f" .txt)
  cp "$f" "/root/brain/extracted/<source>/$base.md"
done

# Import into gbrain
gbrain import /root/brain/extracted/
```

G-Brain skips unchanged files automatically (tracks by content hash).

## Embedding Model

- **Model**: `nvidia/llama-nemotron-embed-vl-1b-v2` via OpenRouter (free)
- **Dimensions**: 1024
- **Chat model**: `inclusionai/ling-2.6-flash` ($0.01/M input)
- **Search mode**: conservative

See the `devops/gbrain` skill for full install/config details and known bugs (dims.ts patch for openai-compatible models).
