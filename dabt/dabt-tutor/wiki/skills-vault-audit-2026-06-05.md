# DABT Skills × Vault Integration Audit

> Audit completed 2026-06-05 after the initial vault population. All 8 DABT skills + 1 supporting skill reviewed for vault awareness.

## Summary

| Skill | Pre-audit vault awareness | Post-audit | Vault artifact it produces |
|---|---|---|---|
| `dabt-project-workflow` | partial (read paths only) | **patched** | reads vault at session start; surfaces active weak areas + orphans |
| `dabt-drill-mode` | **none** | **patched** | writes miss journal entry on every block |
| `dabt-deep-dive` | **none** | **patched** | expands / creates concept note from synthesis |
| `dabt-synthesis-review` | **none** | **patched** | creates synthesis note for cross-domain connections |
| `dabt-reference` | **none** | **patched** | suggests concept note updates after substantive lookups |
| `dabt-miss-journal` | ✅ (newly written) | no change needed | owns the miss journal schema + session-start recall |
| `dabt-notebook` | ✅ (already aligned) | minor patch | owns concept note creation conventions |
| `dabt-database` | (separate — no change needed) | n/a | doesn't write to vault (read-only question lookup) |
| `dabt-3-month-plan` | (no change needed) | n/a | schedule, not session-time tool |

## The integration loop (post-patch)

```
┌─────────────────────────────────────────────────────────────┐
│  Session start (dabt-project-workflow)                       │
│    1. Read dabt-config.json                                 │
│    2. Read learner-profile + recent miss journal entries    │
│    3. Surface top-5 weak concepts (wikilink count)          │
│    4. Surface orphan concepts (no backlinks)                │
│    5. Compute curriculum coverage                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  During session                                              │
│    Drill miss  → dabt-drill-mode  → append miss journal     │
│    Deep dive   → dabt-deep-dive   → expand concept note      │
│    Synthesis   → dabt-synthesis-review → synthesis note     │
│    Reference   → dabt-reference   → suggest concept update  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Maintenance (cron, no LLM)                                  │
│    Sun 04:00 UTC: orphan audit (4ef68bad336d)               │
│    Every 3d 09:00 UTC: weak areas summary (ac7c330dcb88)   │
└─────────────────────────────────────────────────────────────┘
```

## Files modified

1. `/root/.hermes/skills/education/dabt-project-workflow/SKILL.md` — added steps 4b (read vault context) and 4c (orphan check) to session start; added "Vault write targets" reference block
2. `/root/.hermes/skills/education/dabt-drill-mode/SKILL.md` — added step 7 (VAULT UPDATE miss journal write) to per-question feedback
3. `/root/.hermes/skills/education/dabt-deep-dive/SKILL.md` — added step 6 (VAULT UPDATE concept note expansion) to deliverables
4. `/root/.hermes/skills/education/dabt-synthesis-review/SKILL.md` — added section C (VAULT UPDATE synthesis note) to mandatory deliverables
5. `/root/.hermes/skills/education/dabt-reference/SKILL.md` — added "Vault Handoff (after every lookup)" section
6. `/root/.hermes/skills/education/dabt-notebook/SKILL.md` — strengthened integration section with concrete procedure references

## What this enables

When you start your flashcard session later today (or any DABT session):

1. **I load `dabt-project-workflow` first** — it now reads your learner-profile and the recent miss journal entries, then surfaces the active weak areas as part of the session-start message.
2. **You do flashcards** — for every hard/miss, I write a `wiki/miss-journal/YYYY-MM-DD-flashcard-review-<topic>.md` entry with `[[concept-name]]` wikilinks back to the concept notes. The May 28 review already follows this format.
3. **Concept notes accumulate backlinks** — by the time you open `wiki/concepts/adversity-determination.md` in Obsidian, the backlink panel shows every miss on that concept.
4. **Sunday 04:00 UTC** — orphan audit fires automatically, you see which concepts still have no backlinks.
5. **Every 3 days at 09:00 UTC** — weak-areas summary fires, you see your top 5 recurring miss concepts.

## What I didn't touch

- **`dabt-database`** — question lookup only, doesn't write to vault. No change needed.
- **`dabt-3-month-plan`** — schedule-level skill, doesn't run at session-time. No change needed.
- **Per-project deprecated `dabt-gbrain-miss-journal`** at `/root/work/.hermes-config/education/dabt-gbrain-miss-journal/` — left in place as a historical reference; its replacement `dabt-miss-journal` is the canonical skill.

## Verification

To confirm the audit took, in a new session load `dabt-project-workflow` and look for the new steps 4b and 4c in the Session Start Procedure. Or grep the skill files for `VAULT UPDATE` — should appear 4 times across the patched skills.
