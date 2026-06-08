# Artifact Query System Evaluation (2026-06-07 session)

## Trigger
User is evaluating new artifact organization/query systems (llm-wiki, artifact-pyramids, etc.) for the long-running factual Wiki under euphy.

## Required Process
1. Always run a small empirical test on real user artifacts (e.g. vstb translations/OCR or current news dumps).
2. Report token usage and query precision metrics for both the current system and the candidate.
3. Use structured adversarial debate (dissenter voice) when presenting the results.

## User Preferences
- Strong preference for direct action after clear "Yes proceed" or "go ahead and run the tests" signals — do not surface option menus.
- Prefers structured debate when assessing new methodologies.

## Outcome from 2026-06-07 session
- artifact-pyramids shows measurable token reduction (L1 Summary ~33-68% smaller than equivalent llm-wiki page) when downstream agents start at L1.
- Value is realized only if the librarian consistently produces L1 summaries as the primary artifact.
- Hybrid approach recommended: keep llm-wiki for structured provenance; use artifact-pyramids L1 layer for progressive disclosure on factual wiki content.