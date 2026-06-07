# DABT Vault — Kanban Board

> Task list for the ongoing DABT vault work. Use as a kanban import or just check off as you go. Last updated 2026-06-05.

## Status legend

- [ ] = pending
- [~] = in progress
- [x] = complete
- [!] = blocked

## Backlog (in priority order)

### Tier 1 — Active study focus (Domain I + III, 74% of exam)

- [x] **MOC for all 4 exam domains + organ systems** — 5 MOC notes written
- [x] **Stub concept notes for all 81 indexed topics** — 81/81 done
- [x] **Substantive notes for highest-weight concepts** — Adversity Determination (16%), MOA (25%) done
- [~] **Substantive notes for Domain I-C Interpret** — Adversity done; need: NOAEL/LOAEL, Data Interpretation, Statistical Analysis, Pathology Interpretation, Histopathology
- [~] **Substantive notes for Domain III-C Dose-Response** — need: BMD, POD Selection, NOAEL/UF/MF, Dose-Response Modeling
- [~] **Substantive notes for Domain III-A Hazard ID** — need: Cancer Classification, Weight of Evidence, Hazard ID
- [ ] **Link drill questions to concept notes** — 7,567 questions in dabt.db; tag high-weight questions with `[[concept-name]]` for backlink surfacing
- [ ] **Write first deep-dive on a Domain I-C topic** — Adversity Determination is the natural first
- [ ] **Drill session 1 → first miss journal entry through the new workflow** — proves the loop end-to-end

### Tier 2 — Domain II (Mechanistic, 13%)

- [ ] **Substantive notes for: Mechanisms of Toxicity, Biotransformation/Metabolism, Genotoxicity/DNA Damage, Carcinogenesis & Mutagenesis** — these are the high-leverage Mechanism concepts that show up in every domain
- [ ] **Cross-link Mechanism concepts into Domain I-C and III-C notes** — they're upstream of adversity determination and dose-response

### Tier 3 — Domain IV + Organ Systems (Applied, 13% + cross-cutting)

- [ ] **Substantive notes for the 4 deep-dive targets already done** — metals, lead, arsenic-cadmium-chromium, mercury
- [ ] **Substantive notes for: Liver, Kidney, Lung, Nervous System toxicities** — highest-frequency organ systems on the exam
- [ ] **Bind applied tox stubs to mechanism concepts** — e.g., metals-chelation links to [[biotransformation-metabolism]] and [[adversity-determination]]

### Tier 4 — Quality + maintenance

- [ ] **Tag every concept note with priority** — based on which questions miss in the next 30 days
- [ ] **Obsidian Bases for "all questions testing this concept"** — requires Bases skill + dabt.db joins
- [ ] **JSON Canvas of concept graph for Domain III** — visual map of how the 16 Domain III concepts relate
- [ ] **Voice-mode touchups** — STT garbles terms; have a glossary of "heard → intended" mappings surfaced in a concept note

## Recurring maintenance (automated)

- [x] **Weekly orphan audit** (cron: `4ef68bad336d`, Sundays 04:00 UTC) — reports concept notes with no backlinks
- [x] **3-day weak areas summary** (cron: `ac7c330dcb88`, every 3 days at 09:00 UTC) — surfaces recurring miss journal concepts

## Source pipeline (not yet wired)

- [ ] **One-shot PDF → markdown conversion for any non-extracted reference** — e.g., ABT 2026 handbook full text
- [ ] **Auto-tag new concept notes with the kepano OFM syntax** — pick up `obsidian-markdown` skill before any new write
- [ ] **Backup vault to git on a daily cron** — `git add . && git commit -m "vault snapshot $(date)"`

## Acceptance bar (how we know this is working)

A concept note earns its keep when:
1. The backlink panel shows ≥ 1 incoming link from a miss journal entry, drill question, or another concept
2. The related concepts section actually reflects the right neighbours
3. Open it in Obsidian and the navigation graph makes sense (you can reach related concepts in 1-2 clicks)

A stub is *not* complete — it's a *pull target*. You open the stub, expand it with what you learned in the deep-dive / drill, and the backlink graph gets richer.

## Stop conditions

Stop the expansion when:
- The orphan audit reports < 5 orphans
- Every concept has at least 1 drill question linked
- You can answer a question on any concept by opening 1 note (not searching 5)

That state is "exam-ready" — the vault is a working second memory, not a reference library.
