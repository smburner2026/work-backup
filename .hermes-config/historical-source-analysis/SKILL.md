---
name: historical-source-analysis
description: "Workflow for 4-lens (or multi-lens) analysis of historical books and primary sources. Emphasizes direct engagement with the text, concise responses, and avoidance of repetition or verbosity when the user signals frustration."
version: 1.0.0
author: Agent (from session)
license: MIT
category: research
tags: [history, analysis, 4-lens, book-analysis, primary-sources]
---

# Historical Source Analysis Workflow

## Purpose
Provides a structured approach for conducting multi-lens historical analysis (e.g., Burckhardt, Nietzschean Vitalism, Class, Covert+Luttwak) on books and primary sources. Designed to produce substantive, source-grounded output while respecting user preferences for conciseness and directness.

## Core Principles
- **Direct source engagement first**: Always prioritize specific passages, arguments, and quotes from the text over abstract or meta-commentary. If the user asks for analysis of a book, the output must reference what the book actually says.
- **Conciseness on signal**: When the user expresses frustration with repetition, verbosity, or cut-off responses ("stop repeating yourself", "why do you keep cutting out", "this is too verbose"), immediately shorten responses, remove repetitive sign-offs or closing phrases, and deliver only the requested content.
- **Clean text prerequisite**: Before beginning analysis, verify that the source text is cleanly extractable. If a previous download returned HTML or wrapped content, re-extract using the `/download/` endpoint or equivalent before proceeding.
- **Style adaptation**: Match the requested tone (e.g., 19th-century historian voice) while maintaining clarity and directness. Do not let stylistic requirements override the need for concrete source material.

## Workflow Steps
1. Confirm the source text is cleanly available in the vault (check file type and sample content).
2. **Kanban integration (mandatory for 4-lens work)**: Break all multi-lens historical analysis tasks into cards on the `historian-vietnam` board. Assign to the correct profile (jacob for 4-lens Vietnam/historical work). Never perform the analysis directly in chat without first creating and dispatching cards unless the user explicitly says otherwise.
3. If the user requests analysis, begin with direct engagement: identify key arguments or passages from the book.
4. Structure output by lens or section, grounding each claim in specific content from the source.
5. If the user signals dissatisfaction with repetition or length, switch to minimal, direct responses for the remainder of the session.
6. After difficult or iterative tasks, offer to save the approach as a skill or patch.

## Profile Isolation Rules (Strict)
- `jacob` profile = all 4-lens historical / Vietnam work (including *Background to Betrayal*, Hoang Tham, VSTB).
- `default` profile = infrastructure, Kanban dispatch, general orchestration only.
- Never mix content or memory across profiles. If a card was created under the wrong profile, immediately reclaim and reassign.

## Pitfalls to Avoid
- Producing abstract or meta-commentary when the user has explicitly asked for what the book "has written" or "what is in the book".
- Repeating sign-off phrases, summaries of previous actions, or boilerplate language after the user has complained about repetition.
- Assuming a downloaded text file is clean without verification (many archive.org stream links return HTML wrappers).
- Continuing long or repetitive responses after the user has signaled frustration with verbosity or incomplete output.

## References
- `references/extraction-pitfalls.md` — Common issues when downloading plain text from Internet Archive and how to resolve them.
- `references/user-style-preferences.md` — Captured corrections on repetition, verbosity, and direct source engagement from this and related sessions.