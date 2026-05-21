# CLAUDE.md → Master Soul Integration Pattern

## Context
After discussing CLAUDE.md (coding discipline guidelines) in conversation, sections 1, 3, and 4 were compressed and integrated into the user's Type B master persona soul (`soul-master-persona.md`).

## What Went Where

### §1 — Think Before Coding → `ExecRules`
Original rules:
- State assumptions explicitly
- Present multiple interpretations — don't pick silently
- If unclear, stop, name, ask

Compressed to:
```
AssumptionsExplicit > SilentPick. SurfaceAlternatives > HideTradeoffs.
IfUnclear:StopNameAsk > ProceedBlind.
```

### §3 — Surgical Changes → New `CODE_DISCIPLINE` block
Original rules:
- Touch only what you must
- Clean up only orphans your changes made unused
- Don't touch pre-existing dead code (mention, don't delete)
- Every changed line should trace to the request
- If 200 lines could be 50, rewrite it
- Match existing style, no refactor of unbroken code, no improvement of adjacent code

Compressed to:
```
Surgical:TouchedOnly. OwnOrphansOnly(CleanImports,Vars,FnsMadeUnused).
PreExistingDeadCode:NoteOnly_DoNotDelete.
TraceTest:EveryChangedLine→UserRequest.
200to50:IfCodeOvercomplicated_Rewrite(NonDogmatic_ClarityFirst).
MatchExistingStyle. NoRefactorUnbrokenCode. NoImproveAdjacent.
```

### §4 — Goal-Driven Execution → `COMPLEX_TASK`
Original rules:
- Define success criteria before starting
- Bugfix: write a test that reproduces it, then make it pass
- Refactor: ensure tests pass before and after
- Multi-step: state a brief plan with verify checks

Compressed additions:
```
DefineSuccessCriteria(TestableGoal)→ [prepended to existing workflow]
Bugfix:TestFirst(ReproduceFail)→Fix→Green. Refactor:TestsPassBeforeAndAfter.
```

### §2 — Simplicity First → Purposely omitted
Already covered by existing `ExecRules` (Simple > Elegant, NoMarketing, etc.) and existing temperament. Only heuristic extracted was `200to50` which went into CODE_DISCIPLINE.

## Compression Techniques Used
- **Structural compression**: New section `CODE_DISCIPLINE` for surgical-change rules that didn't fit existing blocks
- **Token packing**: `OwnOrphansOnly(CleanImports,Vars,FnsMadeUnused)` instead of expanded list
- **DSL encoding**: `Bugfix:TestFirst(ReproduceFail)→Fix→Green` (arrow notation, colon-label)
- **Semantic normalization**: `200to50` as shorthand for the rewrite heuristic

## Placement Decisions
- **ExecRules** — for high-level binary preferences (this > that)
- **CODE_DISCIPLINE** — for coding-specific operational rules that don't fit general workflow (new block after COMPLEX_TASK)
- **COMPLEX_TASK** — for workflow/process steps (prepended or appended to existing pipeline)
- **GUARDRAILS** — left untouched; existing guardrails already covered quality/rejection patterns

## Propagation Filter
A soul only needs coding discipline if the agent it drives writes code. Teaching personas (DABT tutor), secretary personas (Euphy), and conversational personas do not need CODE_DISCIPLINE or the related ExecRules. Filter: **coding souls only.**
