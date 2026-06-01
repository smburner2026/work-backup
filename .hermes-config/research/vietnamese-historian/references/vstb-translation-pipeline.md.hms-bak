# VSTB Translation Pipeline — Việt Sử Tân Biên

## Overview

Translate OCR'd Vietnamese text from VSTB into English with a scholarly Burckhardtian voice. Each chapter is cleaned → glossarized → translated as a self-contained unit.

## Pipeline Steps

```
STEP 1: CLEAN           STEP 2: GLOSSARY        STEP 3: TRANSLATE       STEP 4: REVIEW
══════════════          ════════════════         ════════════════        ════════════════
Fix OCR errors          Extract proper nouns     delegate_task           User reviews
- diacritics            - people (Bảy Viễn...)   with cleaned text       - voice check
- spacing artifacts     - places (Gia Định...)   + glossary              - name preservation
- broken characters     - ranks (Thiếu Tướng..)  + voice guidelines      - idiom accuracy
- strip page markers    - orgs (Việt Minh...)     Burckhardtian voice     - register consistency
- segment by chapter    - period terms            Preserve Vietnamese     → feedback loop
                        - untranslatable terms    No footnotes
```

## Voice Guidelines (User-Confirmed)

**Target**: Burckhardtian scholarly prose — cultured, precise, measured. Not stiff academic, but the voice of a cultivated historian writing for intelligent readers. The Vietnamese narrative voice should carry through — Phạm Văn Sơn writes with partisan energy and vivid detail; preserve that.

**Rules**:
1. ALL proper names stay in Vietnamese — never translate "Nguyễn Văn Tường" or "Kiến Phúc"
2. Titles and terms: translate on first occurrence with Vietnamese in parentheses, then English. E.g. "Khâm sứ (French Resident)" first, then "Resident"
3. Dates: preserve both lunar and Western as given in the text
4. Dialogue: render in natural spoken register — raw, colloquial. The emperor's outburst "Tao lành, tao sẽ chặt đầu cả ba họ chúng mày!" should feel raw and colloquial, not sanitized
5. Footnotes: integrate the author's footnotes into the text as parenthetical notes or weave them into the narrative. NO translator footnotes
6. Chapter headings: translate them
7. Page markers: remove from output
8. OCR failures: note briefly as "[Page N — original text could not be recovered from OCR]" and continue
9. DO NOT add commentary, interpretation, or analysis. This is a translation, not a summary
10. Output as plain text, not markdown

**What NOT to do**:
- No anglicized names ("Seven Vien" for "Bảy Viễn")
- No translator footnotes or bracketed explanations
- No moral judgment on historical figures
- No stiff academic register — it should read like a cultivated historian, not a dissertation

## Glossary Template

Build a glossary per chapter (or per volume section) before translating. Categories:

```markdown
## Proper Names (NEVER translate)
- Kiến Phúc (vua) — emperor, reigned 1883-1884
- Nguyễn Văn Tường — regent, power broker at Huế court
...

## Titles & Terms (translate with explanation on first use, then English)
- vua — king/emperor (use "emperor" in scholarly context)
- triều đình — court (the imperial court at Huế)
- Nam Triều — the Southern Court
- Phụ chính — Regent
- tòa Khâm — French Residency
- Khâm sứ — French Resident
...

## Treaties & Events
- Hòa ước Quý Mùi (1883) = Treaty of Huế / Harmand Treaty
- Hiệp ước 1884 = Treaty of 1884 (Patenôtre Treaty)
- thất thủ kinh thành — the fall of the Capital (Huế, 1885)
- Cần Vương — "Aid the King" resistance movement
...

## Period Terms
- Bắc Kỳ — Tonkin (northern Vietnam)
- Trung Kỳ — Annam (central Vietnam)
- thực dân — colonialist / colonizer
- bảo hộ — protectorate
...
```

Save glossary alongside the cleaned source and translation:
```
sources/vstb/translations/
├── ch1-raw.txt           # raw OCR extract (with page markers)
├── ch1-clean.txt         # cleaned Vietnamese source
├── glossary-ch1.md       # glossary for this chapter
└── ch1-translated.txt    # English translation
```

## Delegation Pattern

```python
delegate_task(
    goal="Translate the attached cleaned Vietnamese OCR text of Chapter X...",
    context="""
    Source file: /tmp/vstb-translate/chN-clean.txt
    Glossary file: /tmp/vstb-translate/glossary-chN.md
    
    Read both files, translate the chapter, write to: /tmp/vstb-translate/chN-translated.txt
    """,
    toolsets=["file", "terminal"]
)
```

The delegate reads source + glossary, translates following voice guidelines, writes output. Parent reviews.

## Pipeline Strategy: Test → Validate → Parallel Workers

Confirmed with user: the sample translation is a **test phase**. Once the pipeline is validated (voice, quality, mechanics), bulk work goes to **parallel cheaper model workers**, not the primary reasoning model.

### Flow

1. **Test phase** (current) — run sample through full pipeline on primary model (deepseek-v4-flash via OpenCode Go). Catch edge cases, establish voice, fix process bugs.
2. **Validate** — user reviews the sample, signs off on voice/format/approach.
3. **Scale** — dispatch chapters to cheaper parallel workers (e.g., openrouter:cheaper-model or a different provider tier). The tested pipeline becomes the worker instruction.
4. **Review** — spot-check parallel output against established voice.

### Sample Status

Sample complete: **Chapters I-III, Volume 6** (Phần Thứ Nhất).
- **Chapter I** — "Tình Hình Việt Pháp Trước Vụ Thất Thủ Kinh Thành Năm Ất Dậu 1885" — palace murders, French treaty enforcement, Hàm Nghi's enthronement
- **Chapter II** — "Vua Hàm Nghi và Tôn Thất Thuyết" — French ultimatum, Gia Hưng Quận Vương assassination, currency crisis, five-point memorandum
- **Chapter III** — "De Courcy Khiêu Khích Kháng Chiến Nam Triều" — de Courcy's arrival, Hong Men feast trap, three-day ultimatum, preparations for battle

Combined output file: `vstb-vol6-sample-translation.txt` (28 KB, ~140 lines). Sent to Telegram.

Files on WSL at `/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/`:
- `ch1-clean.txt`, `ch1-translated.txt`, `glossary-ch1.md`
- `ch2-clean.txt`, `ch2-translated.txt`
- `ch3-clean.txt`
- `vstb-vol6-sample-translation.txt` (combined Chapters I-III)

Also synced to VPS at `/tmp/vstb-translate/` and `/root/work/post-colonial-vietnam/sources/vstb/translations/`.

### Lessons Learned from Sample

1. **Stale excerpt trap** — When fixing page 13's OCR failure in the full volume text (`viet-su-tan-bien-quyen-6.txt`), the chapter excerpt file (`ch1-clean.txt`) was NOT automatically updated. It still had `[OCR FAILED — page could not be recovered]`. Always re-verify chapter excerpts against the latest full volume text before translating.

2. **OCR garbles that need manual correction during translation:**
   - Broken diacritics: `đẩä` → `đã`, `nghiềm'` → `nghiêm`
   - Hyphenated word splits from line breaks: `dai-diên` → `đại diện`, `Hiệp-ưởc` → `Hiệp ước`
   - Number OCR errors: `1781884` → `17-8-1884`
   - French text garbled: `Bắcdầu bôitinh` → `Bắc Đẩu Bội Tinh`
   - Footnote French source text heavily corrupted (OCR fails on mixed Vietnamese/French)

3. **Glossary building scope** — For Chapter I, ~40 terms were extracted. This is typical for a first chapter of ~3 pages. The glossary grows with each chapter but most terms stabilize after 2-3 chapters.

4. **CRITICAL: Subagent file corruption** — When a delegate_task subagent fixes OCR failures in the full volume text, it may truncate the file instead of surgically replacing lines. This destroyed Volume 6 (502→67 pages). Always verify page count before AND after any file modification. If corruption detected, re-run full OCR.

5. **CRITICAL: File sync propagates corruption** — After the Volume 6 corruption, `scp` propagated the bad file to VPS. Always verify file integrity before syncing.

6. **delegate_task timeouts on slower models** — With mimo-v2.5-pro, sub-agents consistently timed out (600s) on cleaning + translation tasks. Workaround: do cleaning manually, translate directly. This may improve with faster models.

7. **Combined output file** — After translating multiple chapters, combine into a single file with chapter separators (`========`) and a header/title block. Send to user via Telegram as a file attachment with a summary message.

8. **File path delivery** — Always state the output file path prominently at the top of the response. User reads in terminal and needs to find files quickly. Do not bury paths in narrative.

## Batch Strategy

| Size | Strategy | Worker Tier |
|------|----------|-------------|
| Single chapter | One delegate_task | Test phase: primary model |
| 2-3 chapters | Parallel delegate_task(tasks=[...]) — include glossary + voice note in EACH context | Scale phase: cheaper model |
| Full volume | Kanban cards per chapter, each dispatched to parallel worker | Scale phase: cheaper model pool |

For parallel batches, include BOTH the glossary AND the voice guidelines in every delegate context to maintain consistency.

## Quality Checklist

After translation, spot-check:
- [ ] Proper names preserved (not translated)
- [ ] Titles translated on first use, then English
- [ ] Dialogue in natural spoken register
- [ ] Dates preserved (lunar + Western)
- [ ] No translator footnotes or commentary added
- [ ] Voice consistent — scholarly but not stiff, Vietnamese energy carries through
- [ ] OCR failures noted (not silently skipped)

## Output Location

All translation artifacts live at:
- **WSL (primary)**: `/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/`
- **VPS (synced)**: `/root/work/post-colonial-vietnam/sources/vstb/translations/`

Sync after each chapter completion: `scp local-machine:/home/vthen/.../translations/* /root/work/.../translations/`
