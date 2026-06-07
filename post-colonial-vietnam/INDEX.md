# Post-Colonial Vietnam Project — Working Index

**Last updated:** 2026-06-07 (post-cleanup: 17 source files, 8 writing files)
**Project root:** `/root/work/post-colonial-vietnam/`

---

## THE THESIS

> *Mục đích của một dân tộc là sản xuất ra những bậc anh hùng.*
> The purpose of a people is to produce the great man.

The project asks: what kind of civilization produces extraordinary individuals?
Six analytical lenses examine this question across seven periods of Vietnamese history (1802–1965+).

---

## FILE MAP

### I. Project Foundation

| File | Size | Purpose |
|------|------|---------|
| `writing/charter.md` | 12KB | Project charter: thesis, scope, periodization, rules of engagement |
| `writing/strategies.md` | 26KB | Operational methodology: research pipeline, synthesis, verification protocols |
| `writing/phases.md` | 11KB | Project phases and milestones |
| `writing/dna-archaeology.md` | 4.4KB | DNA/Archaeology lens background |
| `INDEX.md` | — | This file |

### II. The Four Lenses (analytical frameworks, grounded in primary sources)

| File | Size | Historian | Key Method |
|------|------|-----------|------------|
| `writing/lens-1-burckhardt.md` | 5.6KB | Jacob Burckhardt | Three Potencies (State/Religion/Culture), Querschnitt cross-section, crises as revelation |
| `writing/lens-2-nietzschean-vitalism.md` | 6.1KB | Friedrich Nietzsche | Three levels: biological substrate → individual life → vital force. No moral judgment. |
| `writing/lens-3-class-analysis.md` | 6.0KB | Chris Wickham | Materialist method: how is surplus extracted? Tax policy, bureaucracy, ownership patterns |
| `writing/lens-4-covert-luttwak.md` | 7.1KB | Edward Luttwak | Strategic logic: paradoxical reasoning, gap between doctrine and reality, covert infrastructure |

### III. Primary Source Extracts (in the historian's own words)

| File | Size | Source Text | Status |
|------|------|------------|--------|
| `method-sourcing-board/nietzsche-history-essay-extracts.md` | 6.2KB | *Uses & Disadvantages of History for Life* (Cambridge UP) | **Verified** — direct quotes, page refs |
| `method-sourcing-board/burckhardt-reflection-extracts.md` | 8.5KB | *Weltgeschichtliche Betrachtungen* (Archive.org, German) | **Verified** — German originals + English translations |
| `method-sourcing-board/luttwak-primary-extracts.md` | 7.1KB | *Grand Strategy of the Byzantine Empire* Ch.10 (Harvard UP) | **Verified** — Operational Code (7 principles) |
| `method-sourcing-board/kantorowicz-method-extracts.md` | 3.4KB | *The King's Two Bodies* (Princeton, 1957) + secondary literature | **Partial** — preface missing from scan |
| `method-sourcing-board/wickham-primary-extracts.md` | 8.2KB | British Academy interview (2014), *Framing the Early Middle Ages* intro, Magistra et Mater blog | **Verified** — extended case method, history from below |

### IV. Verified Skills (methodological personas, ready to load)

| Skill Name | Historian | Status | Key Insight |
|------------|-----------|--------|-------------|
| `burckhardt-reflection-method` | Jacob Burckhardt | **Verified** | Three Potencies, Querschnitt, crises as revelation. 39 years of Basel lecturing. |
| `nietzsche-vitalist-method` | Friedrich Nietzsche | **Verified** | No moral judgment. Three species of history. Will to power as analytical tool, not ideology. |
| `luttwak-strategic-analysis` | Edward Luttwak | **Partial-verified** | Strategy is always cultural expression. Paradoxical logic. Operational Code (7 principles). |
| `george-circle-register` | Stefan George / Kantorowicz / Norwich | **Draft** | Prose register: elevated but not academic, narrative beauty, Anglo-Saxon preference. Not yet verified against primary text. |

### V. Vietnam Primary Sources

| Source | Files | Status |
|--------|-------|--------|
| **Phạm Văn Sơn — Việt Sử Tân Biên** (7 volumes) | `sources/vstb/viet-su-tan-bien-quyen-1.txt` through `quyen-7.txt` | OCR'd from scans |
| **VSTB Translations** (chapters 2–9) | `sources/vstb/translations/ch{2,3,4,5,6,9}-translated.txt` | Translated + glossarized |
| **VSTB Glossaries** | `sources/vstb/translations/glossary-ch{2,3,4,5,6,9}.md` | Per-chapter vocabulary |
| **VSTB Synthesis** | `sources/vstb/synthesis-report.md` (37KB) | Cross-chapter synthesis |
| **Chack — Hoang Tham / Pirate Paul** (1933) | `sources/chack/hoang-tham-cleaned.txt` + translations/ | Full text + 5-part translation |
| **Chack Voice Reference** | `sources/chack/translations/voice-reference.txt` | Prose style reference |
| **Source Tracking** | `sources/source-tracking.md` | What we have, what we need |
| **Family Materials** | `sources/family-source-request.md` | Personal/oral history request |

### VI. Source PDFs (on disk)

| PDF | Size | Notes |
|-----|------|-------|
| `method-sourcing-board/burckhardt_weltgeschichtliche.pdf` | 20MB | German text, OCR'd to .txt |
| `method-sourcing-board/luttwak-byzantine-empire.pdf` | 2.5MB | Harvard UP, Conclusion extracted |
| `method-sourcing-board/luttwak-coup-detat.pdf` | 1.5MB | — |
| `method-sourcing-board/luttwak-roman-empire.pdf` | 4.5MB | — |
| `method-sourcing-board/wickham-framing-middle-ages.pdf` | 8.7MB | Introduction OCR'd |
| `method-sourcing-board/wickham-power-of-property.pdf` | 647KB | — |
| `method-sourcing-board/wickham-concluding-thoughts.pdf` | 5.7KB | — |
| `method-sourcing-board/kantorowicz-kings-two-bodies.pdf` | 8.2MB | Body text extractable, preface missing |
| `sources/chack/Hoang-Tham_pirate_Paul_Chack_1933.pdf` | 47MB | French original |

---

## HOW TO USE THIS INDEX

### Starting a new period analysis
1. Read `writing/charter.md` for periodization and scope
2. Read `writing/strategies.md` §7 for the per-period template
3. Load the four lens skills via `skill_view()`
4. Gather primary sources per `sources/source-tracking.md`
5. Apply each lens using the framework in `writing/lens-{1,2,3,4}-*.md`
6. Synthesize per `writing/strategies.md` §4 (convergence / divergence / genealogical thread)

### Loading a historian's method
Use `skill_view(name='burckhardt-reflection-method')` (or any verified skill).
For the raw primary extracts, read the corresponding file in `method-sourcing-board/`.

### Writing voice
Reference `sources/chack/translations/voice-reference.txt` for Norwich-style prose register.
The `george-circle-register` skill has the mechanical rules (capitalization, register modulation).

### Current period status
- **Period 1 (Nguyen Dynasty 1802–1862):** Not yet started
- **Period 2 (French Conquest 1858–1887):** Not yet started
- **Period 3 (Colonial Rule 1887–1945):** Not yet started
- **Period 4 (First Indochina War 1946–1954):** Not yet started
- **Period 5 (Diem Era 1955–1963):** Not yet started
- **Period 6 (Buddhist Crisis 1963–1965):** Not yet started
- **Period 7 (Covert Build-Up 1960–1965):** Not yet started

---

## WHAT'S NEXT

The foundation is built. Four lenses grounded in primary sources. Operational methodology documented. Vietnam primary sources acquired and partially translated.

**Next step: Period 1 (Nguyen Dynasty 1802–1862) — applying the four lenses.**
