# Post-Colonial Vietnam — Worked Example (Six-Lens Project)

This is a worked example of the `historical-research` skill applied to a specific project. It shows how the six-lens analytical framework, periodization table, multilingual source strategy, and document-processing pipeline combine in practice.

## Project Location

`/root/work/post-colonial-vietnam/`

## Methodology (Six Lenses)

1. **Burckhardtian Cultural History** — total cultural immersion. Art, religion, daily life, intellectual currents, social rituals.
2. **Biography as Aperture** — individual lives illuminate the period.
3. **Nietzschean Physiological Vitalism** — no moral judgment. Will to power, ambition, vital force.
4. **Marxist Class Analysis** — the material skeleton. Capital, power, class structure shifts.
5. **Covert Apparatus** — hidden wiring. Militias, CIA networks, secret armies, paramilitary infrastructure.
6. **Ancestral DNA & Archaeology** — material and biological evidence. Population genetics, migration, material culture.

## Scope

Pre-WWII Vietnam through pre-US direct military intervention (~1945–1964). "Nothing after 1975."

## Periodization (7 Periods, Two Parts)

### Part I — Prequel (Background)
| Period | Key Lens Focus | Source Languages |
|--------|---------------|-----------------|
| 1. Nguyen Dynasty (1802–1887) | Burckhardt (court culture), Class (mandarins) | Vietnamese, French |
| 2. French Colonial (1887–1940) | Class (plantation economy), Covert (Sûreté) | French, Vietnamese |
| 3. Resistance Leaders (1930–1945) | Biography (Ho, Giap), Covert (ICP underground) | Vietnamese, French |
| 4. Japanese Occupation (1945) | Burckhardt (famine culture), Covert (OSS) | Vietnamese, Japanese, French |
| 5. First Indochina War (1946–1954) | Biography (Giap), Covert (Viet Minh intelligence) | French, Vietnamese, English |
| 6. Rise & Fall of Diem (1954–1963) | Nietzsche (Diem's will), Covert (CIA/Can Lao) | Vietnamese, English, French |

### Part II — Core Period
| Period | Key Lens Focus | Source Languages |
|--------|---------------|-----------------|
| 7. Covert Build-Up (1963–1965) | Covert (du Berrier, Lansdale, Air America, Phoenix precursors) | English, French |

## Key Source Authorities

- **Phạm Văn Sơn** — *Việt Sử Tân Biên* (multi-volume masterwork, scanned PDF, OCR with vie+fra tesseract)
- **Hillaire du Berrier** — covert apparatus layer, militias, pre-escalation intelligence
- **Family materials** — oral histories, personal documents, photographs (first-class primary sources)

## OCR Pipeline Used

For scanned Vietnamese historical texts (like *Việt Sử Tân Biên*):
1. `pdftoppm -r 300 source.pdf /tmp/page` → convert PDF pages to images
2. `tesseract /tmp/page-NNN.ppm stdout -l vie+fra --psm 1` → OCR with Vietnamese + French
3. Batch process in scripts, store as `.txt` per page
4. Post-process for Vietnamese diacritics and French loanwords

## Key Project Files

- `writing/charter.md` — project charter with full periodization
- `writing/phases.md` — methodology and workflow
- `writing/nietzschean-lens.md` — Nietzschean physiological vitalism methodology
- `writing/dna-archaeology.md` — DNA/archaeology lens methodology
- `sources/source-tracking.md` — source tracking by type
- `sources/family-source-request.md` — family brief (superseded)
