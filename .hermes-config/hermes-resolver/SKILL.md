---
name: hermes-resolver
description: "Routing table for Hermes skills. Load when unsure which skill handles a user request, or when you need to find the right skill for an unfamiliar task. Organized by domain with trigger phrases."
version: 1.0
author: Hermes Agent
tags: [resolver, routing, skill-index, reference]
related_skills: [hermes-agent-memory, hermes-agent]
---

# Hermes Skill Resolver

Load this resolver when a user request doesn't obviously match a skill,
or when you need to confirm you're using the best skill for the job.

**How to use:** Match the user's intent to a domain below, then load the
corresponding skill via `skill_view(name='<skill-name>')` and follow its
instructions. If multiple skills could match, read the one with the most
specific trigger match.

For a complete listing of ALL available skills, call `skills_list()`.

## DABT Study (high-frequency)
- `dabt-drill-mode`: exam practice | MCQ drill | blueprint-weighted questions | timed test
- `dabt-deep-dive`: concept understanding | first-principles | Socratic tutorial | toxicology deep-dive
- `dabt-reference`: lookup | G-Brain search | Casarett | Hayes | regulation reference
- `dabt-synthesis-review`: cross-topic consolidation | comparison matrices | flashcard generation
- `dabt-gbrain-miss-journal`: miss tracking | gap analysis | weak-area persistence
- `dabt-3-month-plan`: milestone plan | study schedule | exam prep roadmap
- `dabt-database`: practice question DB query | source-bank selection
- `dabt-notebook`: concept notebook | lightweight note-taking during sessions
- `dabt-project-workflow`: session start procedure | skill coordination | DABT entry point
- `dabt-dabt-*`: any other DABT skill

## Brain & Knowledge
- `gbrain`: brain query | synthesis | gap analysis | dream cycle | health check | embed config
- `hermes-agent-memory`: operational memory | environment facts | procedural knowledge | cron reference

## Content & Media
- `youtube-content`: YouTube transcript | video summary | thread/blog from video
- `spotify`: music | playlist | currently playing | queue
- `xurl`: X/Twitter | post | search | timeline | DM
- `gif-search`: GIF | Tenor | search reaction GIFs

## DevOps & System
- `hermes-maintenance`: update checks | manifest tracking | community additions
- `background-agents`: cron jobs | long-running tasks | background processing
- `remote-agent-infrastructure`: Tailscale | VPS | mobile access | tmux
- `secrets-management`: Bitwarden | BWS | credential storage | env vars
- `hermes-web-ui`: dashboard | workspace | remote UI
- `hermes-multi-sync`: HMS | bidirectional sync | VPS↔local

## Creative & Visual
- `excalidraw`: hand-drawn diagrams | architecture flow | sequence diagrams
- `architecture-diagram`: SVG | cloud architecture | infrastructure diagrams
- `sketch`: throwaway HTML mockups | design exploration
- `ascii-art`: pyfiglet | cowsay | image-to-ascii
- `ascii-video`: video-to-ASCII | colored ASCII | GIF
- `manim-video`: 3Blue1Brown animations | math visualization
- `p5js`: generative art | interactive | shaders | 3D
- `pixel-art`: NES palette | retro | game art

## Development
- `github-code-review`: PR review | diff analysis | inline comments
- `github-pr-workflow`: PR lifecycle | branch | commit | merge
- `github-issues`: create | triage | label | assign
- `substack-paywall-export`: paywalled articles | newsletter export | podcast download
- `substack-pdf-export`: Substack articles→PDF | text extraction
- `book-pdf-compilation`: markdown→PDF | chapter compilation | volume assembly
- `document-pipelines`: source→formatted output | web→PDF | markdown→docx
- `writing-plans`: implementation plans | bite-sized tasks | code paths
- `test-driven-development`: RED-GREEN-REFACTOR | tests before code
- `systematic-debugging`: root cause analysis | bug hunting | 4-phase debug
- `pinescript-indicator-dev`: TradingView Pine Script | indicator debugging
- `tv-feature-export`: TradingView bar features | CSV export | comment strings

## Trading
- `swingcatcher`: BAMBAM variant | swing high/low | crypto perps | LightGBM
- `quant-trading-agent`: backtesting | trader profiling | regime tagging | meta-analysis
- `swingcatcher` + `tv-feature-export`: feature engineering pipeline

## MLOps
- `huggingface-hub`: model search | download | upload | HF CLI
- `llama-cpp`: GGUF inference | local LLM | model discovery
- `dspy`: declarative LM programs | prompt optimization | RAG
- `weights-and-biases`: experiment tracking | sweeps | model registry
- `evaluating-llms-harness`: lm-eval-harness | benchmarks | MMLU | GSM8K

## Smart Home & IoT
- `openhue`: Philips Hue | lights | scenes | rooms
- `spotify` (also in Content): music playback across devices

## Utility
- `memento-flashcards`: spaced repetition | flashcard creation | deck export
- `obsidian`: vault reading | note search | creation
- `notion`: Notion API | pages | databases | markdown

## Low-Frequency / Specialized
- `comfyui`: image gen | video gen | audio gen | workflow
- `godmode`: jailbreak testing | red-teaming
- `polymarket`: prediction markets | prices | orderbooks
- `arxiv`: academic paper search | keyword | author
- `llm-wiki`: Karpathy's LLM Wiki | markdown KB

## Persona Triggers
- "Euphy" → `euphy-personal-journal` | `euphy-bullet-journal` | `euphy-obsidian-notes`
- "Mike" → DABT tutor persona (Socratic first-principles)
