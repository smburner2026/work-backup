# Pipeline Audit Findings — 2026-06-02

Full audit of `extract.py` + `hermes_skill_gen.py`. 32 findings total (5 critical, 15 medium, 12 low).

## Critical Fixes Applied

### extract.py
- **C1: sys.exit() in helper functions** → Replaced with `ExtractionError` exceptions in `extract_docx()`, `extract_epub()`, `extract_rtf()`. Caller (`main()`) catches and exits cleanly. Script is now reusable as a library.
- **C2: OUTPUT_DIR race condition** → Default path now includes PID: `book_skill_work_<pid>`. Concurrent runs no longer clobber each other. Override via `BOOK_SKILL_WORKDIR` env var.
- **C3: metadata.json encoding** → Write now uses explicit `encoding="utf-8"`.

### hermes_skill_gen.py
- **C4: Form-feed detection** → Now scans backwards up to 5 lines for `\f` (handles blank lines between form feed and heading). Was only checking `lines[i-1]`.
- **C5: Hardcoded skip list** → Replaced Aion-specific terms (`'AION'`, `'PRINCETON UNIVERSITY PRESS'`) with generic publisher boilerplate (`'FOREWORD'`, `'PREFACE'`, `'CONTENTS'`, `'INDEX'`, etc.).

## Medium Fixes Applied

- **M9: Token estimate** → Standardized to `words * 1.33` (~1.33 tokens/word). Was `words // 3` (~0.33 tokens/word) — 4x undercount.
- **M12: metadata.json error handling** → `load_metadata()` now catches `json.JSONDecodeError` and `OSError`.
- **M13: Empty slug edge case** → `slugify()` returns `"untitled"` instead of empty string.
- **Dead code cleanup** → Removed unused `textwrap` import, dead `skip_words` set.

## Remaining Known Issues (not yet fixed)

### extract.py
- **M4: latin-1 fallback** → `read_text_file()` falls back to `latin-1` which silently garbles binary data. Low priority — only affects misidentified files.
- **M6: No input file size guard** → Multi-GB files could exhaust memory in Python-based extractors.
- **L2: has_toc scans first 30K chars** → Books with lengthy forewords may have ToC beyond this.
- **L3: No atexit cleanup** → Crashed runs leave stale OUTPUT_DIR. PID isolation mitigates this.

### hermes_skill_gen.py
- **M10: Strict heading equality** → `stripped.upper() == title_upper` requires exact match between body text and ToC. Variations (dashes, subtitles, encoding) cause silent chapter skips.
- **M14: Strategy 3 false positives** → Centered uppercase headings can match running headers/footers, not just chapter titles.
- **L7: book_type parameter unused** → `generate_chapter_summary()` accepts it but ignores it.
- **L8: chapters parameter unused** → `generate_glossary()` accepts it but ignores it.
- **L9: extract_chapter_text splits twice** → `text.split("\n")` called twice per chapter extraction.

## Testing Notes

Tested on:
- **Aion (Jung)** — 374 pages, 132K words, Roman numeral chapters (I–XV). 15/15 chapters detected + 1 false positive from appendix.
- **Man and His Symbols (Jung)** — 301 pages, 138K words, multi-author essay format. 3 chapters detected via `N. Title` pattern.

Both produced clean output after fixes.
