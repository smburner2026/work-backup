---
name: dabt-3-month-plan
description: "DABT exam final-push plan — milestone-based 3-month structure for Oct 15, 2026. Built from the learner profile (TempMoon/Abud, 2 years passive reading + recent active drilling). Phase-gated, not date-gated, with embedded self-evaluation checkpoints. Use this to plan sessions and track progress against the final push."
category: education
---

# DABT 3-Month Final Push Plan

**Exam:** Oct 15, 2026
**Learner:** TempMoon/Abud — bioscientist, 2 years passive C&D + regs reading, weak on precision/terminology retrieval, strong metacognition
**Start:** ~July 15, 2026 (after Domain I + Genotoxicology deep-dive phase)

## Phase 0 — Deep-Dive Prep (pre-July 15)
Domain I deep dives + Genotoxicology fundamentals. Completed in drill sessions before the 3-month window opens.

## Phase 1 — Integration Drilling (Weeks 1-4)

| Week | Focus | Output target |
|------|-------|--------------|
| 1 | Mixed Domain I + III — RA questions needing study design and dose-response knowledge. Blueprint-weighted: 4 DI + 4 DIII + 1 DII + 1 DIV per session. | 60-80 questions |
| 2 | Genotox + Carcinogenesis (Domain II bridge) — mechanisms → cancer RA → IARC/EPA classification → ICH S1/S2 | 60-80 questions |
| 3 | Domain II remainder — cell death, oxidative stress, apoptosis vs necrosis, signaling pathways, AOP framework | 60-80 questions |
| 4 | Domain IV applied tour — organ system pattern recognition (liver, kidney, neuro, immune, repro/dev, respiratory). Sample broadly from the DB. | 80-100 questions |

**Checkpoint 1:** Rate Domain I + III precision (1-5). Below 4 on either → extend mixed drilling.

## Phase 2 — Volume & Weakness Triage (Weeks 5-8)

| Week | Focus | Output target |
|------|-------|--------------|
| 5 | Blueprint-weighted mixed exams — 50 Q/session, timed (90 sec/Q), full domain rotation. Track miss journal. | 100-150 questions |
| 6 | Weak-topic remediation — drill bottom 3 topics from miss journal. Deep session per topic + re-test. | 80-100 questions |
| 7 | Terminology lockdown — full flashcard deck review. Any hesitation → rewrite from memory. | Full deck (100-200 cards) |
| 8 | Domain II + IV sweep — unconfident subtopics (pesticides, solvents, clinical tox, food safety). | 60-80 targeted questions |

**Checkpoint 2:** Full timed mock (150-200 Q, 2.5-3 hrs). Score <70% → extra week on weakest domain.

## Phase 3 — Exam Mode (Weeks 9-12)

| Week | Focus | Output target |
|------|-------|--------------|
| 9 | Mock exam 1 — full 250 Q, timed, no open-book. Score + triage. | 1 full mock + error analysis |
| 10 | Gap-closure sprint — drill 2-3 weakest sub-domains from mock. | 100+ remediation questions |
| 11 | Mock exam 2 — same conditions. Trend comparison. | 1 full mock + trend analysis |
| 12 | Taper — light review. Flashcard deck + miss journal. No new content. | Review only |

## Supporting Infrastructure

- **Flashcard deck** — built during Phases 0-1, maintained through Phase 2. 150-200 cards by Phase 3.
- **Miss journal** — persisted in the project directory. After each session, write structured session summary + weak areas. Before each session, review past entries for gap patterns. Enables data-driven Phase 2 triage across 30+ sessions.
- **DB access** — 3,796 clean questions in SQLite at `reference/data/dabt.db`. Use blueprint-weighted sampling. Domain III is scarce (170 Qs) — conserve for Phase 3 mocks.
- **Reference texts** — C&D during Phase 0 only. By Phase 1, settle disputes only. By Phase 2, textbooks collect dust.

## Volume Target Summary

| Phase | Questions | Purpose |
|-------|-----------|---------|
| Phase 0 | ~150-200 | Build precision on core topics |
| Phase 1 | ~260-340 | Cross-domain integration |
| Phase 2 | ~240-330 | Volume + weakness triage |
| Phase 3 | ~450 | 2 full mocks + gap closure |
| **Total** | **~1,100-1,200** | Sufficient for this learner profile |

## Self-Evaluation Checkpoints

Built into each phase transition. The checkpoints produce honest scaling (1-5) on:
- Domain I precision
- Domain III integration
- Terminology speed
- Cross-domain linking ability

If any checkpoint shows below-target scores, the plan pauses at that phase until remediation lifts it. No forward motion on a weak foundation.

## Execution Notes

- Consistency > intensity. 30 min most days > 6-hour weekend marathons.
- Questions > reading. Every hour spent on retrieval practice is 2-3x more valuable than passive review for this learner.
- The miss journal is not optional. It's the highest-leverage tool for Phase 2.
- Domain III (Risk Assessment) is the largest weight at 38% AND the most scarce in the DB (170 Q). Conserve for Phase 3 mocks.
