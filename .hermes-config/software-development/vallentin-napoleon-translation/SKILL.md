---
name: valledin-translation
description: "Translate Berthold Vallentin's 'Napoleon' (1923, George Circle) from German to English. Loads george-circle-register foundation skill for prose rules — CFR mechanics, register modulation, and German compound handling."
---

# Vallentin Napoleon Translation

## Register

**Foundation skill:** `george-circle-register` — all CFR rules, active verbs, calque avoidance, capitalization conventions, Fraktur OCR pitfalls, and register modulation are defined there. This skill carries only project-specific details: source paths, glossary, and known pitfalls.

## Source
- Original German PDF: `/root/work/vallentin-napoleon.pdf` (553 pages, Google Books)
- UCAL OCR: `/root/work/translation-project/Translation - Bethold Vallentin's Napoleon/b4569992/`
- Cleaned German: `/root/work/vallentin-clean4/` (35 .de.txt, ~1.5M chars)
- English: `NAPOLEON_COMPLETE.txt` in same dir (182K words) + 36 chapter .en.txt
- Project zip (glossary, style, Lorimer notes): `/root/.hermes/cache/documents/`

## Style: Lorimer + Kaufmann
- **No calques** — unpack German compounds
- **Active verbs** over nominalizations
- **Anglo-Saxon** over Latinate
- **Capitalize**: Pope, Emperor, Caesar, Empire, Revolution, Spirit of the Age, the Apparition
- **Lowercase**: man, hero, deed, form, myth, figure, being
- **American spelling** (labor, color, judgment, practiced)
- **Foreign quotes** stay in original, italicized
- **Em-dashes with spaces** — like this

## Core Glossary
| German | English |
|--------|---------|
| Wesen | being |
| Tat | deed |
| Erleben | experience |
| Unmittelbarkeit | immediacy |
| Erscheinung | apparition |
| Gestalt | figure/form |
| Volk | folk |
| bürgerlich | bourgeois |
| Geist | spirit/mind/intellect |
| geschichtlich | historical |
| Bedingtheit | conditioning |
| Schicksal | destiny |

## Pitfalls
- Subagent voice drift: always editorial pass
- Fraktur OCR: missing spaces "dieGeschichte" → fix lowercase→uppercase
- Book One Ch.III uses "ACTION" not "ACTING" for heading in existing translation
- Book Four files may have English names from subagents — rename to match
- Zeittafel appended to Schlusswort in source — extract separately
