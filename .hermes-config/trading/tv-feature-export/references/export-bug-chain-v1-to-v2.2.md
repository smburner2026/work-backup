# Export Bug Chain: v1 → v2 → v2.1 → v2.2

**Discovered May 23, 2026** during cross-validation audit of BAMBAM 24-feature delta export.

## Bug 1: volRatio_delta (v1)

**Symptom:** Feature 18 (volRatio_delta) had systematic bias — mean=1.61, 70% positive values. Should be symmetric around zero.

**Root cause:** The v1 delta export computed the 5-bar-ago volRatio denominator from a SHIFTED averaging window:

```pine
// v1 WRONG:
volRatio_5 = vol_body_5 / some_avgVol_that_was_recomputed_from_bars_6_to_205
```

While the current volRatio uses bars 1-200 for the denominator. These are two different 200-bar windows with only 195 bars overlapping. The 5-bar shift systematically inflated the delta.

**Fix:** Use `avgVol[5]` — the same rolling average formula, just sampled 5 bars earlier:

```pine
// v2.1 CORRECT:
volRatio_5 = vol_body_5 / avgVol[5]
```

Now both denominators share the same window definition.

## Bug 2: Make_comment UDF (v2)

**Symptom:** 399/431 signals failed vb+vs≈vol sanity check. First signal in CSV had literal `NaN` at features 5-6. For non-NaN rows, vb+vs summed to less than vol.

**Root cause:** A `make_comment()` UDF was introduced to build the pipe-delimited feature string. Inside the UDF, `str.tostring(vb1[1])` was called. When this UDF is passed to `strategy.entry(comment=make_comment("BEAR"))`, Pine v6 defers the function call. In the deferred context, `vb1[1]` can resolve to stale or NaN values because the evaluation frame sees a different series cache state than the main body did during the standard bar-by-bar pass.

**Important:** This is NOT a general Pine v6 UDF bug. UDFs handle history references correctly in standard usage (e.g., inside `if` blocks, assignment, plot statements). The issue is specific to functions called from inside `strategy.entry(comment=fn())` — a deferred evaluation context.

**Fix:** Pre-compute ALL `str.tostring()` calls at top-level scope. String concatenation has no series-cache dependency, so it works fine in the deferred context:

```pine
// CORRECT:
s_vb = str.tostring(vb1[1])
s_vs = str.tostring(vs1[1])
bear_comment = "BEAR|" + s_vb + "|" + s_vs + "|" + ...
strategy.entry("BEAR", strategy.short, comment=bear_comment)
```

## Bug 3 (#.## Format Strings)

**Symptom:** Pine v6 compile error: `Script could not be translated from: null`.

**Root cause:** `str.tostring(val, "#.##")` with format specifier fails in some Pine v6 contexts.

**Fix:** Use bare `str.tostring(val)` with no format argument.

## Detection: The vb+vs≈vol Sanity Check

**ALL THREE bugs are caught by a single check:** For every entry row, verify that the float at position 6 (vb) + position 7 (vs) = position 1 (vol) within 1%.

This check detects:
- Bug 1: volRatio_delta wrong (indirect — vol and vd must match, which constrains vb and vs)
- Bug 2: vb/vs are NaN or wrong values
- Bug 3: Export failed entirely (no rows to check)

**Automated:** `scripts/audit-export-pipeline.py` runs this and 6 other checks.

## Timeline

| Version | Status | Bug | Files |
|---|---|---|---|
| v1 (May 22) | Buggy | volRatio_delta shifted window | Cache CSV, lost after cleanup |
| v2 (May 23) | Buggy | make_comment UDF breaks vb/vs | `doc_b86b15...v2.csv` (do not use) |
| v2.1 (May 23) | Misdiagnosed | Code correct, explanation wrong | `04_...v2.1.txt` (claude audit pending) |
| v2.2 (May 23) | Correct | Fixed, diagnosed properly | `data/exports/bambam_delta_24feat_v22.csv` |

## Lesson

When building Pine export scripts with `strategy.entry(comment=...)`:
1. NEVER put `str.tostring(series[n])` inside a UDF called from strategy.entry.
2. ALWAYS run the vb+vs≈vol sanity check on EVERY new export.
3. ALWAYS check for NaN values in ALL feature columns.
4. Document the format clearly so the Python parser and Pine script stay in sync.

These four rules would have caught all three bugs before any analysis was run on bad data.
