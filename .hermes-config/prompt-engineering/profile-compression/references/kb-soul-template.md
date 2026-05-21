---
title: Knowledge-Base Soul Template (Type C)
version: 1.0
description: Reference example of a Type C (Knowledge-Base) soul using the DABT Immunotoxicology curriculum as the subject. Demonstrates how to compress domain knowledge into soul notation — no personality, no rubrics, no workflow loops. Pure content compression with DSL blocks and concept grids.
---

**KNOWLEDGE_BASE_IMMUNOTOX**

CORE_FRAMEWORK: 4 immunotoxic outcomes → immunosuppression, immunostimulation, hypersensitivity (I-IV), autoimmunity

MODULE1 — Immune System Basics
  Innate: Barriers(skin/mucosa)→Macrophages/Neutrophils(phagocytosis)→NK-cells(viral/tumor)→Complement(tag/lyse). Always-on. First target in TG407.
  Adaptive: B-cells(antibodies IgM→IgG/IgA/IgE). CD4+helper(cytokines orchestrate). CD8+killer(perforin/granzyme). Treg(prevent autoimmunity). Memory B/T = vaccine basis.
  Organs_Primary: Bonemarrow(hematopoiesis,B-maturation). Thymus(T-education,neg-selection).
  Organs_Secondary: Spleen(blood-filter,Ab-production). Lymphnodes(lymph-filter). MALT/Peyer's(gut-mucosal).
  TG407/408 mandate: thymus/spleen weights + histopathology + marrow cellularity + WBC/differentials.

MODULE2 — Hypersensitivity (Gell & Coombs Types I-IV)
  Type I: IgE/mastcell immediate. Allergen→IgE→mastcell→histamine/leukotrienes. Anaphylaxis.
  Type II: IgG/IgM cell-surface→complement/ADCC. Transfusion rxns.
  Type III: Immune-complex deposition→inflammation. Serum sickness, lupus nephritis.
  Type IV: T-cell delayed. Th1/Th2/Th17→cytokines. Contact dermatitis, TB test. TG497 screens skin.
  Hapten: Small molecule + carrier = complete antigen. Key across Types I-III.

MODULE3 — Immunosuppression (4 Mechanisms)
  M1_DirectKill: Cytotoxic→dividing lymphocytes. Cyclophosphamide→thymic atrophy, ↓spleen, ↓TDAR.
  M2_SignalBlock: Cytokine inhibitors→interrupt T-B coop. ↓TDAR without cell kill.
  M3_MaturationInterfere: Block lymphocyte development. ↓marrow cellularity.
  M4_Stress: Glucocorticoid↑→thymic apoptosis. Reversible—important for TG407/408 interpretation.
  TDAR: Gold-standard functional assay. Tests T-B teamwork. ICH S8 trigger from any STS signal + WoE.

MODULE4 — Autoimmunity + Immunostimulation
  SLE: Loss self-tolerance. Anti-nuclear antibodies. Immune complex→organ damage.
  Drug-induced: Procainamide.
  TGN1412: CD28 superagonist→cytokine storm→organ failure. London 2006 Phase I.
  Mechanisms: Molecular mimicry, bystander activation, Treg failure, negative selection escape.

REGULATORY_FRAMEWORK
  ICH_S8: WoE decision tree. STS→signals?→TDAR/NK/host-resistance/phenotyping. Factors: dose-response, reversibility, exposure margin, pharmacology, population.
  TG407: 28-day rodent. Endpoints: thymus/spleen wt+histopath, marrow, hematology.
  TG408: 90-day. Same endpoints, more established.
  TG443: Extended one-gen repro tox. DIT in F1 pups. Critical window: gestation/lactation.
  TG497: Skin sensitization DPRA/KeratinoSens/h-CLAT/AOP.
  CD_8e_Ch12: Mechanisms, examples, positive controls.
  Synthesis: TG407/408 screen → ICH S8 WoE → TDAR positive → labeling, limits, monitoring.

CONCEPT_GRID
  C_TDAR: T-dependent antibody response. SRBC/KLH→IgM/IgG ELISA. Gold standard for humoral function.
  C_Hapten: Small molecule needs carrier. Across Types I-III hypersensitivity.
  C_CytokineStorm: TNF/IL-6/IFN cascade. TGN1412 archetype.
  C_DIT: Developmental immunotox. Fetal Th2-bias, immature thymus. TG443 covers.
  C_3Rs: Replace/Reduce/Refine. ICH S8 WoE avoids unnecessary functional tests.

This template demonstrates:
1. DSL nesting under KNOWLEDGE_BASE root (no SOUL/rubric/loops)
2. Section-based organization (MODULE1-4, REGULATORY, CONCEPT_GRID)
3. Abbreviated key-value blocks (M1_DirectKill: description→consequence)
4. Concept grid for cross-cutting terms
5. Synthesis lines (key integration points)
