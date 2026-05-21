# Mantle of Caesar (Friedrich Gundolf) — OCR Compilation Session

**Source**: University of Michigan scan ZIP (39015030536711), 328 raw `.txt` pages extracted to `/home/vthen/work/gundolf-caesar/`.

**Outcome**: Clean 185-page PDF (`The_Mantle_of_Caesar_by_Friedrich_Gundolf.pdf`, ~713 KB).

**Transfer**: `rsync -avz root@178.156.199.37:/home/vthen/work/gundolf-caesar/The_Mantle_of_Caesar_by_Friedrich_Gundolf.pdf ~/Downloads/` (VPS 178.156.199.37; user on WSL).

**Key workflow refinements applied**:
- Frequency analysis identified running headers: "The Mantle of Caesar", "The Historical Personality", "The Mythical Figure", "The Magic Name" and OCR-fused variants (e.g. "The Magic NameT").
- EXACT_REMOVE blacklist + `startswith(header)` with ≤3 char trailing tolerance for merge artifacts.
- Removed library stamps ("UNIVERSITY OF MICHIGAN", "648992"), page numbers, TOC dotted leaders, index lines, lone digits, boilerplate.
- Hard-break fix: single newlines → spaces; hyphenated words rejoined. Preserved paragraph separation.
- Used `pdf.write(6.2, text)` for continuous body (avoided multi_cell drift/corruption on long text).
- 25 mm margins, Liberation Serif, justified where possible; title page + section structure preserved.
- Multiple regeneration passes (background processes) after each cleaning iteration. Final inspection with PyMuPDF on sample pages before delivery.

**Reproduction notes**:
- Always run 2–3 cleaning iterations; new artifacts appear only after previous noise is gone.
- Delete TOC/index pages entirely rather than cleaning.
- Inspect first 5–8 pages of every generated PDF before reporting success.
- Script evolved via write_file + patch; final version handles both section-based reconstruction and monolithic fallback.

This session validated the section-based reconstruction path in the parent skill for HathiTrust-style OCR collections.