# Historian Extraction Status

Track primary source verification for each foundation skill. Updated 2026-06-06.

## Verification Status

| Historian | Skill | Status | Primary Source | Key Finding |
|-----------|-------|--------|---------------|-------------|
| **Burckhardt** | `burckhardt-reflection-method` | `primary` | *Weltgeschichtliche Betrachtungen* (Archive.org, German, djvu.txt 611KB). Three Potencies, Querschnitt, crises as revelation, "terrible simplifiers" extracted with German originals + English translations. | Key: "culture is the highest potency" — State and Religion are means, Culture is the flower. Crises reveal what prosperity conceals. |
| **Nietzsche** | `nietzsche-vitalist-method` | `primary` | *On the Uses and Disadvantages of History for Life* (Cambridge UP, Hollingdale trans.) OCR'd from PDF. Three species of history: monumental/antiquarian/critical. Full method extracted with page refs. | "Each species belongs to a certain soil and climate." Monumental→great man thesis, Antiquarian→Burckhardtian immersion, Critical→class+covert analysis. Key: "We want to serve history only to the extent that history serves life." |
| **Luttwak** | `luttwak-strategic-analysis` | `partial-verified` | *Grand Strategy of the Byzantine Empire* (2009, 513pp) downloaded from libgen. Conclusion pp.424-433 extracted. | Training framed him as systems engineer. He's a *cultural* analyst: "strategy is always the expression of an entire culture" (p.437). "Second-order effects" and "systems thinking" may belong to *Strategy* (1987), not verified here. |
| **Wickham** | `wickham-material-foundation` | `primary` | British Academy interview (2014), *Framing the Early Middle Ages* Introduction pp.30-36, Magistra et Mater blog. Extended case method, history from below, Weberian ideal types, surplus extraction as core question. | "You follow the lives of a set of individuals through time to see what their lives tell you about the society." Key: not Marxist materialist — comparative methodologist using materialist tools. |
| **George Circle** | `george-circle-register` | `unverified` | No primary texts sourced. Prose mechanics built from training. | Needs verification against Kantorowicz's *King's Two Bodies* or Stefan George circle texts. |

## Training vs. Horse's Mouth — Key Corrections

### Luttwak
- Training: "Power has a mechanics... analyzed with the precision of engineering" → **Wrong framing**
- Luttwak: "Strategy is always the expression of an entire culture" (p.437) → **Cultural analyst, not engineer**
- Training: "Refusal to fight fair" as clever insight → **Luttwak: subversion is the DEFAULT, fighting is the failure case**
- Training broadened his scope to "military, diplomatic, economic, psychological instruments" → **His own definition: "knowledge and persuasion... interact with military strength"** — no economic instruments in core definition

### Wickham
- Training: Core framing = "property relations, surplus extraction, class structures" → **Wrong emphasis**
- Wickham: Core framing = "a failure to confront difference... in a comparative way" (p.34) → **Comparative methodologist, not materialist**
- Training: Unifying question = "Who produces the wealth?" → **Wickham doesn't state one — deliberately multi-thematic**
- Training missed Weber entirely → **Wickham explicitly uses "Weberian ideal types" (p.36)**

## Sourcing Method

User preference: **lectures, articles, interviews** (short-cycle), not full books. Exception: when the book IS the primary method statement (as with Luttwak's Byzantine conclusion and Wickham's Introduction).

**Successful workflow:** `book-hunting` skill → libgen.li → edition page → extract MD5 → scrape ads.php → get dynamic key → get.php download. Free models can't parse the HTML; need capable model for the intermediary pages.

## Next Actions
1. ~~Source Nietzsche *Untimely Meditations* essay on history~~ **DONE — OCR'd 2026-06-06, primary verified**
2. ~~Source Burckhardt *Reflections on World History*~~ **DONE — Archive.org German text OCR'd 2026-06-07, primary verified**
3. Verify George Circle register against Kantorowicz primary text (*King's Two Bodies* on disk)
4. ~~Verify Wickham surplus extraction claims~~ **DONE — British Academy interview + blog + Framing intro verified 2026-06-07**
5. Source Norwich introduction/method statement
6. Source Stefan George "Das Wort" poem (translations found online, original German needed)
