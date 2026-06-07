# Rapid-Fire DABT Review — Session Notes

## Speech-to-Text (STT) Garble Pattern

The user uses voice-to-text for answering flashcards. STT routinely mangles technical terms, especially:

| STT output | Actual term | How to recognize |
|-----------|------------|-----------------|
| "certainty" | "uncertainty" | Context: UF discussion |
| "CBPK" / "CBPK" | "PBPK" | Context: modeling, ADME |
| "NOAL" | "NOAEL" | Context: dose-response, RfD |
| "NOADL" | "NOAEL" | Context: same |
| "NOAA LOAL" | "NOAEL" or "LOAEL" | Context: dose-response |
| "CIP four five fifty" | "CYP450" | Context: enzymes, biotransformation |
| "Cynogen" | "Carcinogen" | Context: cancer classification |
| "Cynogen" / "Cynogenic" | "Carcinogenic" | Context: same |

### Recovery rules

1. **Never assume the user's answer is wrong based on STT output alone.** Read the surrounding context to reconstruct what they likely said.
2. **If the answer is conceptually correct but the term is garbled** → accept the answer, note the correct term in the BACK, rate based on the underlying knowledge (not the garble).
3. **If the user says "the STT screwed up" or "I did say X"** → immediately correct the rating and acknowledge. Do not defend the initial assessment.
4. **When presenting the BACK** → use the correct term clearly so the user sees the right spelling/wording, even if STT garbled it.

### Example interaction

```
STT: "Certainty factor is a factor applied to account for potential uncertainty..."
Agent: [rates hard based on "certainty" vs "uncertainty"]
User: "No, the STT screwed up. I did say uncertainty factor."
Agent: "Fair — STT garbled you. Updated rating: good ✓"
```

## Duplicate Card Detection

During review, if two cards in the same session ask essentially the same question (e.g., "What is the difference between systemic and local toxicant?" vs "What is the difference between local effect and systemic effect?"), flag it immediately:

1. Note the duplicate to the user
2. Ask which to keep (or suggest removing the less precisely worded one)
3. Delete the duplicate with `$MEMENTO delete --id CARD_ID`

This prevents wasted review time and keeps deck quality high.

## Rapid-Fire Mode Calibration

When user answers in rapid-fire mode (short, fast answers), adapt:

| Signal | Meaning | Action |
|--------|---------|--------|
| Single-word or short-phrase answer | Knows it, wants speed | Rate easy/good quickly, minimal BACK |
| Self-correcting mid-answer (e.g., "wait, no, actually...") | Thinking aloud, not confused | Wait for final answer before rating |
| "I don't know" / "we never covered this" | Genuine gap | Give clean BACK, rate hard, move on |
| Garbled but conceptually right | STT issue | Accept, correct term in BACK, rate on content |
