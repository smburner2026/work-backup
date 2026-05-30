# Worked Example: Deep Learning Session

**Video:** Andrej Karpathy — From Vibe Coding to Agentic Engineering
**URL:** https://www.youtube.com/watch?v=96jN2OCOfLs
**Channel:** Sequoia Capital (AI Ascent 2026)
**Duration:** 29:49

## Extraction Methods Used

| Method | Outcome |
|--------|---------|
| youtube-transcript-api | ❌ IP blocked (cloud VPS) |
| oEmbed API | ✅ Title, channel, thumbnail |
| web_search (title + channel) | ✅ Karpathy's own bearblog summary, 2 detailed articles |
| Browser subagent | ✅ Enriched metadata, chapters |
| Synthesis across 3 sources | ✅ Domain-tuned analysis |

**Lesson:** When transcript is blocked, oEmbed + web_search is the fastest path. Only escalate to browser subagent when the user needs data that search can't surface.

## Full Analysis (what was delivered to user)

### Core Thesis — 3 Frameworks

#### 1. The Agentic Inflection (Dec 2025)
Agents crossed a threshold. The unit of programming shifted from typing lines to delegating macro-actions. The programmer becomes an orchestrator.

→ **Relevance to quant trading:** This is already the user's workflow (Hermes orchestrates, Pi codes). Karpathy validates the pattern as the new normal.

#### 2. Software 3.0
| Era | Mechanism | Human Role |
|-----|-----------|------------|
| 1.0 | Explicit code | Write rules |
| 2.0 | Neural weights | Build datasets |
| **3.0** | **Context window** | **Program via prompts + tools** |

Key example: MenuGen — the entire app stack collapses into a single prompt. "Some apps should stop existing as apps."

→ **Relevance to quant trading:** How much of the pipeline (data fetch → signal calc → order gen → P&L track) is temporary scaffolding that could collapse into an agent context?

#### 3. Verifiability Explains Everything
"Old software automates what you can specify. AI automates what you can verify."
Coding advanced fastest because tests pass/fail. Capability is jagged — spikes where labs have trained, blind spots elsewhere.

→ **Relevance to quant trading:** Trading has clear verification (P&L, Sharpe, drawdown). This is an ideal domain for agent self-improvement via RL.

### Actionable Takeaways for Quant Work
1. Build a verification loop around swingcatcher signals (P&L feedback as RL signal)
2. Ask which scripts could collapse into agent context instead of multi-script pipelines
3. Test agents on YOUR specific patterns — don't assume generalization from general coding benchmarks
4. Invest in taste/judgment (regime detection, signal quality) — that's the non-outsourceable human edge

### Open Questions
- How to build reliable verification infrastructure for agent-generated trading logic?
- Where does the user's domain sit on the "model's rails" spectrum?
