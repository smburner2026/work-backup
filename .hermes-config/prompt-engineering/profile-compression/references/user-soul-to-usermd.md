# USER.md Compression Pattern — Worked Example

This reference demonstrates compressing a Type B (User Master Persona) soul from full density (~3,750 chars) to fit Hermes's USER.md memory limit (≤1,375 chars).

## Source: Full Type B Soul (abridged)

**SOUL:** TempMoon. Bioscientist, CLI-native no-CS. Discord/tg via VPS. Direct, high-intellect, zero-tolerance marketing/euphemism. Nietzschean BGAE+Zarathustra+Genealogy (Kaufmann primary, multi-translation). George Circle/Vallentin translator. Builder custom philosophical AI agents. Self-directed—tests before committing, values elegance over ornament.
**PersonalityRubric:** O:80 C:75 E:40 A:50 N:20. IntCuriosity:90 Directness:95 Scepticism:80 SyntheticAbility:85 SimplicityPref:90. PatienceNonsense:10.
**Voice:** conversational-precise, dry humour. No-padding peer register. Corrects directly, not socially.
**ExecRules:** Direct>Polite. Evidence>Assertion. Simple>Elegant. Local>Remote. FirstPrinc>Authority. NoMarketing/Syco. FeatureDesc=ConcreteHowTo.
**ReadLoop:** Read→Process→Test→Deepen→Integrate→Repeat.
**Learn:** Gap→RequestModel→Test→IfNot:Simplify→IfYes:Apply→Solidify.
**Domain:** Bioscience bench. CLI(Linux,rsync,git,venv). Philosophy primary. Reading: cross-connection genealogical. Tools by-need. Telegram/Discord.
**Guard:** Reject euphemism/syco/vague. Correct directly. Inspect output. Authority-resist. 'IDK' > confident error.
**ConvMode:** brainstorm/think/propose/discuss = conversation, no file changes.

**Full length:** ~3,750 chars (not shown in full — this is the identity-critical portion)

## Compression decisions applied

| Content | Status | Reasoning |
|---------|--------|-----------|
| SOUL identity line | **Kept** | Irreducible — who the user IS |
| PersonalityRubric | **Kept** | Required density marker |
| VOICE | **Kept** | Communication context |
| ExecRules | **Kept** | Interaction contract |
| ReadLoop | **Dropped** | Redundant with Learn |
| Learn | **Kept, compressed** | Captures learning style |
| COMPLEX_TASK | **Dropped** | Covered by ExecRules+Guard |
| KNOWLEDGE_BASE domains | **Compressed to one line** | "Domain: Bioscience bench. CLI(Linux,rsync,git,venv). Philosophy primary." |
| Platform details | **Kept, compressed** | "Telegram/Discord primary" → lines |
| ConvMode | **Kept** | Prevents file changes on discussion words |
| Tool list (rsync/git/venv) | **Kept inline** | Useful context for CLI agent |
| Section headers | **Dropped** | Labels like "Voice:" carry structure |

## Result: Compressed USER.md (~1,344 chars)

```
TempMoon. Bioscientist, CLI-native no-CS. Discord/tg via VPS. UTC+7. Direct, high-intellect, zero-tolerance marketing/euphemism. Nietzschean BGAE+Zarathustra+Genealogy (Kaufmann primary, multi-translation). George Circle/Vallentin Napoleon translator. Builder custom philosophical AI agents. Self-directed—tests before committing, values elegance over ornament.
Personality: O:80 C:75 E:40 A:50 N:20. IntCuriosity:90 Directness:95 Scepticism:80 SyntheticAbility:85 SimplicityPref:90. PatienceNonsense:10.
Voice: conversational-precise, dry humour. No-padding peer register. Corrects directly, not socially.
Rules: Direct>Polite. Evidence>Assertion. Simple>Elegant. Local>Remote. FirstPrinc>Authority. NoMarketing/Syco. Why>What. FeatureDesc=ConcreteHowTo.
ReadLoop: Read→Process{Paraphrase,Synth,Connect}→Test{Hypothesis,CheckText}→Deepen→Integrate→Repeat.
Learn: Gap→RequestModel(Analogy,FirstPrinc)→Test→IfNot:Simplify→IfYes:Apply→Solidify.
Domain: Bioscience bench. CLI(Linux,rsync,git,venv). Philosophy primary. Reading: close cross-connection genealogical>analytical. Tools by-need only. Telegram/Discord primary.
Guard: Reject euphemism/sycophancy/vagueness. Correct directly. Inspect output before presenting. Authority-resist. 'I don't know' > confident error.
ConvMode: brainstorm/think/propose/discuss = conversation, no file changes.
```

**Key lessons from this compression:**
- Dropping section headers (no `**SOUL**` labels) saves ~80 chars and the line-beginning labels still carry structure
- Platform details and UTC offset can be one-liners, not separate entries
- KNOWLEDGE_BASE shrinks from 5-6 lines of domain details to one compact line
- The ConvMode line at the end prevents operational confusion — the model knows not to create files when the user is discussing
- "I don't know > confident error" captures more trust than a longer guardrail
