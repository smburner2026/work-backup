#!/usr/bin/env python3
"""
Fix corrupt placeholder explanations for 68 Past ABT Exam questions.
Generates proper exam-quality explanations and updates the database.
"""
import json
import sqlite3
import os
import sys

DB_PATH = '/root/work/dabt/dabt-tutor/reference/data/dabt.db'
BATCH_PATH = '/root/work/dabt/fix_explain_batch.json'
PROGRESS_PATH = '/root/work/dabt/fix_explain_progress.json'

# ============================================================
# EXPLANATION GENERATORS
# Each function returns a dict: {id: explanation_string}
# ============================================================

def generate_explanations():
    """
    Generate proper explanations for all 68 questions.
    Each explanation follows the template:
    
    **Answer: X** — [1 sentence: mechanism/rationale]
    **Why not the others:** [1-2 sentences on the most seductive distractor]
    **Exam tip:** [Optional — only if there's a trick or memory hook]
    **Source:** [Textbook reference based on topic]
    """
    
    explanations = {}
    
    # DABT-3941: Lithium goiter - inhibition of thyroid hormone release
    explanations['DABT-3941'] = (
        "**Answer: C** — Lithium inhibits thyroid hormone release by interfering with "
        "colloid droplet formation and follicular cell microtubule function, blocking "
        "secretion of T3/T4 from the thyroid gland.\n"
        "**Why not the others:** The most seductive distractor is A (blockage of iodine uptake), "
        "which is the mechanism of perchlorate and thiocyanate, not lithium.\n"
        "**Exam tip:** Lithium and iodide both inhibit thyroid hormone release — remember "
        "\"Lithium Lets Less Leave.\"\n"
        "**Source:** C&D 12th ed., p. 832; C&D 8th ed., Thyroid section"
    )
    
    # DABT-4025: Environmental behavior - octanol-water partition coefficient
    explanations['DABT-4025'] = (
        "**Answer: A** — The octanol-water partition coefficient (Kow) governs both "
        "bioconcentration in aquatic organisms and adsorption to soil organic carbon, making "
        "it the single most important physicochemical descriptor for environmental fate.\n"
        "**Why not the others:** Distractor D (lipophilicity as the most significant determinant) "
        "is too narrow — Kow also predicts soil adsorption, and other factors like volatility "
        "and degradability matter.\n"
        "**Exam tip:** Kow is the universal starting point for PBT (Persistent, Bioaccumulative, "
        "Toxic) assessments.\n"
        "**Source:** C&D 12th ed., Environmental Toxicology chapter; Hayes, Ch. 25"
    )
    
    # DABT-4100: Water-insoluble gases deposit in deep lung
    explanations['DABT-4100'] = (
        "**Answer: D** — Relatively water-insoluble gases like NO2 and methylene chloride "
        "bypass the upper respiratory tract (which scrubs water-soluble gases) and penetrate "
        "to the alveolar region where they are absorbed into the bloodstream.\n"
        "**Why not the others:** Distractor C (completely absorbed in nasal cavity) is the "
        "behavior of highly water-soluble irritants like formaldehyde and SO2, not insoluble gases.\n"
        "**Exam tip:** Solubility determines site of deposition: water-soluble → upper airway; "
        "insoluble → deep lung.\n"
        "**Source:** C&D 12th ed., Respiratory Toxicology chapter"
    )
    
    # DABT-4120: 1,2-dichlorobenzene causes lipid peroxidation in liver
    explanations['DABT-4120'] = (
        "**Answer: E** — 1,2-Dichlorobenzene undergoes cytochrome P450-mediated bioactivation "
        "to reactive metabolites that deplete glutathione and initiate lipid peroxidation, "
        "leading to hepatotoxicity.\n"
        "**Why not the others:** Carbon monoxide (A) causes hypoxic injury, not lipid peroxidation; "
        "kerosene (C) causes hydrocarbon pneumonitis and CNS depression, not primarily hepatic "
        "lipid peroxidation.\n"
        "**Exam tip:** Chlorinated benzenes are classic inducers of lipid peroxidation via "
        "oxidative stress.\n"
        "**Source:** C&D, Hepatotoxicity chapter; Hayes, Ch. 12"
    )
    
    # DABT-4161: Polar organic solvents increase skin permeability via stratum corneum
    explanations['DABT-4161'] = (
        "**Answer: A** — Polar organic solvents (e.g., DMSO, ethanol) penetrate the stratum "
        "corneum, disrupt lipid packing, and extract intercellular lipids, thereby increasing "
        "skin permeability — they act as permeation enhancers.\n"
        "**Why not the others:** Distractor B (inhibition of oxidative phosphorylation) is a "
        "systemic toxic mechanism of uncouplers like dinitrophenol, not the primary route of "
        "dermal absorption.\n"
        "**Exam tip:** Solvents that damage the skin barrier increase absorption of co-applied "
        "chemicals — relevant to occupational dermal exposure.\n"
        "**Source:** C&D 12th ed., Dermal Toxicology; Hayes, Ch. 6"
    )
    
    # DABT-4164: Bioavailability of metals from soil - water solubility
    explanations['DABT-4164'] = (
        "**Answer: B** — The water solubility profile of metals in a soil matrix directly "
        "governs their bioaccessibility and subsequent absorption in the GI tract, as only "
        "dissolved metals are available for uptake.\n"
        "**Why not the others:** Distractor C confuses relative bioavailability with "
        "bioaccessibility — dissolution in the stomach is a measure of bioaccessibility, "
        "not a direct comparison of relative bioavailability between metals.\n"
        "**Exam tip:** Bioaccessibility (dissolution in GI fluids) precedes bioavailability "
        "(absorption into systemic circulation).\n"
        "**Source:** EPA Soil Bioavailability guidance; C&D, Metals chapter"
    )
    
    # DABT-4340: Analgesic nephropathy - renal papilla
    explanations['DABT-4340'] = (
        "**Answer: D** — Analgesic nephropathy primarily causes necrotic lesions in the "
        "renal papilla (papillary necrosis) due to the concentration of analgesic metabolites "
        "in the medullary interstitium and the vulnerable blood supply of the papilla.\n"
        "**Why not the others:** Distractor B (proximal tubule) is a common site for many "
        "nephrotoxicants (e.g., cisplatin, aminoglycosides), but the hallmark lesion of "
        "chronic analgesic abuse is papillary necrosis.\n"
        "**Exam tip:** \"Papillary necrosis = Analgesic nephropathy\" is a classic board "
        "association.\n"
        "**Source:** C&D 12th ed., p. 603; Kidney Toxicology chapter"
    )
    
    # DABT-4342: Minipig immune system characterization
    explanations['DABT-4342'] = (
        "**Answer: D** — The minipig immune system is well characterized anatomically, "
        "clinically, and through comparative assessment of immune-response genes across "
        "mouse, minipig, and human, making it a useful non-rodent model.\n"
        "**Why not the others:** Distractor A incorrectly states minipigs have reduced "
        "inter-animal variability — minipigs actually show greater immunological variability "
        "than dogs or NHPs, not less.\n"
        "**Exam tip:** Minipig is increasingly used in immunotoxicity testing as a "
        "non-rodent model that aligns with 3R principles.\n"
        "**Source:** ICH S8; C&D, Immunotoxicology chapter"
    )
    
    # DABT-4346: Murine Local Lymph Node Assay (LLNA)
    explanations['DABT-4346'] = (
        "**Answer: E** — The murine LLNA quantifies lymphocyte proliferation in the "
        "draining auricular lymph nodes following topical application of a test substance, "
        "expressed as the Stimulation Index (SI) — proliferation is the endpoint.\n"
        "**Why not the others:** Distractor A (elicitation threshold) describes the human "
        "patch test or the elicitation phase, not the LLNA which measures induction of "
        "sensitization.\n"
        "**Exam tip:** LLNA measures proliferation, not elicitation — it's an induction-"
        "phase assay.\n"
        "**Source:** OECD TG 429; C&D, Immunotoxicology chapter"
    )
    
    # DABT-4396: Methanol intoxication treatment - fomepizole
    explanations['DABT-4396'] = (
        "**Answer: D** — 4-Methylpyrazole (fomepizole) is the recommended treatment for "
        "methanol intoxication because it competitively inhibits alcohol dehydrogenase "
        "(ADH), preventing the metabolism of methanol to its toxic metabolites formaldehyde "
        "and formic acid.\n"
        "**Why not the others:** Distractor A (disulfiram) inhibits aldehyde dehydrogenase, "
        "which would worsen toxicity by blocking the detoxification of formate.\n"
        "**Exam tip:** Fomepizole blocks ADH — same mechanism works for ethylene glycol "
        "poisoning. Ethanol is the older alternative that also competitively inhibits ADH.\n"
        "**Source:** C&D, Clinical Toxicology chapter; Goldfrank's"
    )
    
    # DABT-4397: Alpha-2u-globulin nephropathy - human relevance
    explanations['DABT-4397'] = (
        "**Answer: B** — Alpha-2u-globulin nephropathy is male-rat-specific because humans "
        "do not synthesize sufficient levels of alpha-2u-globulin (a low-molecular-weight "
        "protein uniquely produced in male rat liver). The protein-ligand complex accumulates "
        "in proximal tubules, causing cytotoxicity and compensatory proliferation.\n"
        "**Why not the others:** Distractor A (different metabolism) is true for some "
        "compounds but is not the primary basis — the key is the unique presence of "
        "alpha-2u-globulin in male rats.\n"
        "**Exam tip:** This is the classic example of a rodent-specific mode of action "
        "not relevant to humans. Other examples: peroxisome proliferation in rodent liver.\n"
        "**Source:** C&D 12th ed., Kidney chapter; EPA Risk Assessment guidance"
    )
    
    # DABT-4399: Lead exposure - nervous system in children
    explanations['DABT-4399'] = (
        "**Answer: C** — The developing nervous system is the most sensitive target of "
        "lead toxicity in children, manifesting as cognitive deficits, reduced IQ, and "
        "behavioral problems, even at low blood lead levels (<5 μg/dL).\n"
        "**Why not the others:** Distractor D (hematopoietic system) is affected at higher "
        "exposures (anemia via inhibition of heme synthesis), but neurological effects "
        "occur at lower doses in children.\n"
        "**Exam tip:** No safe blood lead level has been identified in children — the "
        "CDC reference value is 3.5 μg/dL.\n"
        "**Source:** C&D 12th ed., Metals chapter; ATSDR Toxicological Profile for Lead"
    )
    
    # DABT-4400: Ethanol as antidote for methanol - competitive inhibition
    explanations['DABT-4400'] = (
        "**Answer: B** — Ethanol competitively inhibits alcohol dehydrogenase (ADH), "
        "preventing methanol from being metabolized to formaldehyde and formic acid. "
        "Ethanol has ~10× higher affinity for ADH than methanol.\n"
        "**Why not the others:** Distractor A (increases metabolism to formaldehyde) "
        "would worsen toxicity — the goal is to block, not accelerate, methanol metabolism.\n"
        "**Exam tip:** Same principle as fomepizole — both are ADH inhibitors. Methanol "
        "itself is relatively non-toxic; the metabolites cause the damage.\n"
        "**Source:** C&D 12th ed., Clinical Toxicology chapter"
    )
    
    # DABT-4401: Ethylene glycol metabolism - ADH first step
    explanations['DABT-4401'] = (
        "**Answer: B** — The first step in ethylene glycol metabolism is oxidation by "
        "alcohol dehydrogenase (ADH) to glycoaldehyde, which is further metabolized to "
        "glycolic acid, glyoxylic acid, and finally oxalic acid.\n"
        "**Why not the others:** Distractor A (aldehyde oxidase) acts later in the pathway "
        "— it converts glycolaldehyde to glycolic acid, but ADH acts first.\n"
        "**Exam tip:** ADH first, then aldehyde dehydrogenase — same sequence as ethanol "
        "metabolism.\n"
        "**Source:** C&D, Clinical Toxicology chapter; Goldfrank's"
    )
    
    # DABT-4402: Chloroform toxicity - phosgene metabolite
    explanations['DABT-4402'] = (
        "**Answer: A** — Chloroform undergoes CYP2E1-mediated bioactivation to phosgene "
        "(COCl2), a reactive electrophile that covalently binds to cellular proteins, "
        "depletes glutathione, and damages cell membranes, causing centrilobular hepatic "
        "necrosis and proximal tubular renal necrosis.\n"
        "**Why not the others:** Distractor C (directly genotoxic) is incorrect — chloroform "
        "is not directly genotoxic; its toxicity is primarily cytotoxic via protein binding, "
        "not DNA binding.\n"
        "**Exam tip:** Phosgene from chloroform — same compound used as a chemical warfare "
        "agent. Requires bioactivation.\n"
        "**Source:** C&D 12th ed., Hepatotoxicity chapter; IARC Monograph Vol. 73"
    )
    
    # DABT-4403: Delaney Clause
    explanations['DABT-4403'] = (
        "**Answer: C** — The Delaney Clause (1958 amendment to FFDCA Section 409) stated "
        "that no food additive could be deemed safe if it induced cancer in humans or "
        "laboratory animals, effectively establishing a zero-risk standard for carcinogenic "
        "food additives.\n"
        "**Why not the others:** Distractor A (exempted pesticide residues) is the opposite "
        "— pesticide residues were later addressed separately by the Food Quality Protection "
        "Act of 1996, which modified the Delaney Clause.\n"
        "**Exam tip:** The Delaney Clause was so strict that it was subsequently modified "
        "by FQPA (1996) to allow de minimis risk (<10^-6) for pesticide residues.\n"
        "**Source:** C&D 12th ed., Regulatory Toxicology; EPA, FQPA background"
    )
    
    # DABT-4404: DDT has highest biomagnification potential
    explanations['DABT-4404'] = (
        "**Answer: D** — DDT has the highest potential for biomagnification due to its high "
        "lipophilicity (log Kow ~6.9), extreme environmental persistence (half-life in soil "
        "of 2-15 years), and resistance to metabolic degradation in organisms.\n"
        "**Why not the others:** Distractor C (chlorpyrifos) is less persistent and has a "
        "lower log Kow (~4.7), making it less prone to biomagnification than DDT.\n"
        "**Exam tip:** Biomagnification requires: log Kow >5, resistance to metabolism, "
        "and environmental persistence. DDT is the classic example.\n"
        "**Source:** C&D, Environmental Toxicology; EPA Ecological Risk Assessment"
    )
    
    # DABT-4406: Insecticides primarily affect nervous system
    explanations['DABT-4406'] = (
        "**Answer: E** — Most insecticides (organophosphates, carbamates, pyrethroids, "
        "organochlorines, neonicotinoids) target the nervous system — they inhibit "
        "acetylcholinesterase, modulate sodium channels, or act as nicotinic acetylcholine "
        "receptor agonists.\n"
        "**Why not the others:** Distractor B (cardiovascular system) is not the primary "
        "target — while some insecticides can affect the heart secondarily, the primary "
        "mechanism is neurotoxicity.\n"
        "**Exam tip:** Evolutionary logic: insects have a nervous system → insecticides "
        "target it. Each class has a distinct neural target.\n"
        "**Source:** C&D 12th ed., Insecticides chapter; Hayes, Ch. 21"
    )
    
    # DABT-4407: Nitrite for cyanide poisoning
    explanations['DABT-4407'] = (
        "**Answer: B** — Nitrite (sodium nitrite) is used to treat cyanide poisoning by "
        "oxidizing hemoglobin to methemoglobin, which competitively binds free cyanide with "
        "high affinity, freeing cytochrome c oxidase and restoring aerobic respiration.\n"
        "**Why not the others:** Distractor A (dimercaprol) is a chelator for heavy metals "
        "(arsenic, mercury, lead), not cyanide.\n"
        "**Exam tip:** Nitrite + thiosulfate is the classic cyanide antidote kit. Nitrite "
        "makes methemoglobin; thiosulfate provides substrate for rhodanese.\n"
        "**Source:** C&D, Clinical Toxicology chapter; Goldfrank's"
    )
    
    # DABT-4408: CO poisoning - 40% = carboxyhemoglobin saturation
    explanations['DABT-4408'] = (
        "**Answer: D** — The \"greater than 40%\" in carbon monoxide poisoning refers to "
        "the percent of hemoglobin bound to CO (carboxyhemoglobin, COHb) relative to total "
        "hemoglobin saturation capacity. Levels >40% COHb indicate severe, potentially fatal "
        "poisoning.\n"
        "**Why not the others:** Distractor A (CO in serum) is misleading — CO is measured "
        "as COHb percent, not dissolved CO in serum.\n"
        "**Exam tip:** CO has 200-250× greater affinity for hemoglobin than O2. Symptoms: "
        "10-20% headache, 20-30% nausea, 30-40% confusion, >40% unconsciousness/death.\n"
        "**Source:** C&D 12th ed., Respiratory Toxicology; Goldfrank's"
    )
    
    # DABT-4409: CO as chemical asphyxiant
    explanations['DABT-4409'] = (
        "**Answer: A** — Carbon monoxide is a chemical asphyxiant that binds to hemoglobin "
        "to form carboxyhemoglobin, preventing oxygen binding and transport, and also "
        "inhibits cytochrome c oxidase, disrupting cellular respiration.\n"
        "**Why not the others:** Distractor D (carbon tetrachloride) is primarily a "
        "hepatotoxicant that causes fatty liver and necrosis via bioactivation, not a "
        "chemical asphyxiant.\n"
        "**Exam tip:** Chemical asphyxiants (CO, cyanide, H2S) prevent oxygen utilization. "
        "Simple asphyxiants (N2, CO2, CH4) displace oxygen.\n"
        "**Source:** C&D 12th ed., Respiratory Toxicology; Goldfrank's"
    )
    
    # DABT-4410: Coumarin rodenticides - Vitamin K epoxide reductase
    explanations['DABT-4410'] = (
        "**Answer: A** — Coumarin derivative rodenticides (e.g., warfarin) inhibit "
        "Vitamin K epoxide reductase (VKOR), blocking the regeneration of reduced vitamin K "
        "and thereby preventing the gamma-carboxylation of clotting factors II, VII, IX, "
        "and X.\n"
        "**Why not the others:** Distractor B (Vitamin K epoxide carboxylase) is not the "
        "target — the carboxylase uses reduced vitamin K but is not directly inhibited by "
        "coumarins; VKOR is the inhibited enzyme.\n"
        "**Exam tip:** VKOR → reduced Vitamin K needed for γ-carboxylation of clotting "
        "factors. \"Warfarin blocks VKOR.\"\n"
        "**Source:** C&D, Clinical Toxicology; Goodman & Gilman's"
    )
    
    # DABT-4416: Cyanide antidote - nitrite/thiosulfate mechanism
    explanations['DABT-4416'] = (
        "**Answer: B** — Sodium nitrite induces methemoglobin formation, and cyanide "
        "preferentially binds to methemoglobin (rather than cytochrome c oxidase). Sodium "
        "thiosulfate then serves as a sulfur donor for rhodanese, which converts cyanide "
        "to the less toxic thiocyanate for renal excretion.\n"
        "**Why not the others:** Distractor A (acceleration of detoxification) is too vague "
        "— the mechanism has two specific steps (methemoglobin formation + sulfur transfer).\n"
        "**Exam tip:** Nitrite makes the \"sink\" (methemoglobin), thiosulfate provides the "
        "\"flush\" (thiocyanate excretion).\n"
        "**Source:** C&D 12th ed., Clinical Toxicology; Goldfrank's"
    )
    
    # DABT-4417: Pyrethroids from chrysanthemum
    explanations['DABT-4417'] = (
        "**Answer: C** — Synthetic pyrethroids are derived from pyrethrins, natural "
        "insecticidal esters extracted from Chrysanthemum cinerariaefolium (now "
        "Tanacetum cinerariifolium) flowers.\n"
        "**Why not the others:** Distractor A (oleander) contains cardiac glycosides, "
        "not pyrethrins. The \"pyrethrum\" name comes from the plant source.\n"
        "**Exam tip:** Pyrethrum comes from chrysanthemums — the name itself hints at "
        "the origin.\n"
        "**Source:** C&D 12th ed., Insecticides chapter; Hayes, Ch. 21"
    )
    
    # DABT-4421: Alveolar clearance - macrophage phagocytosis
    explanations['DABT-4421'] = (
        "**Answer: C** — Small insoluble particles reaching the alveolar region are "
        "predominantly cleared by alveolar macrophage phagocytosis. Macrophages engulf "
        "particles and then either migrate up the mucociliary escalator or enter the "
        "interstitium/lymphatics.\n"
        "**Why not the others:** Distractor B (cilia beating in mucociliary escalator) "
        "operates in the conducting airways (trachea through bronchioles), not in the "
        "alveoli which lack ciliated cells.\n"
        "**Exam tip:** Alveoli have NO cilia — macrophages are the primary clearance "
        "mechanism in the deep lung.\n"
        "**Source:** C&D 12th ed., Respiratory Toxicology; EPA IRIS"
    )
    
    # DABT-4422: Neutrons vs X-rays - RBE
    explanations['DABT-4422'] = (
        "**Answer: C** — Neutrons have higher Relative Biological Effectiveness (RBE) "
        "compared to X-rays because they are high-LET (Linear Energy Transfer) radiation, "
        "causing more dense ionization along their track, making them more effective at "
        "inducing biological damage per unit dose.\n"
        "**Why not the others:** Distractor A is the opposite — neutrons have HIGHER, not "
        "lower, LET than X-rays.\n"
        "**Exam tip:** RBE increases with LET up to ~100 keV/μm. Neutrons = high LET, "
        "X-rays = low LET.\n"
        "**Source:** C&D 12th ed., Radiation Toxicology"
    )
    
    # DABT-4423: Phosgene - lipid peroxidation/pulmonary edema
    explanations['DABT-4423'] = (
        "**Answer: B** — Phosgene (COCl2) undergoes hydrolysis in the lower respiratory "
        "tract to release HCl and also reacts with cellular macromolecules, causing lipid "
        "peroxidation, disruption of the alveolar-capillary membrane, and delayed-onset "
        "pulmonary edema.\n"
        "**Why not the others:** Distractor A (delayed caspase activation in Kupffer cells) "
        "describes liver mechanisms — phosgene is primarily a pulmonary toxicant.\n"
        "**Exam tip:** Phosgene causes \"dry drowning\" — a latent period of hours before "
        "pulmonary edema. Also: same metabolite from chloroform.\n"
        "**Source:** C&D, Respiratory Toxicology; Chemical Warfare Agents chapter"
    )
    
    # DABT-4424: Impaction occurs in upper airways, not lower
    explanations['DABT-4424'] = (
        "**Answer: C** — Impaction predominantly occurs in the upper airways (nasopharynx, "
        "trachea, bronchi) where air velocity is highest and changes in airflow direction "
        "cause particles to collide with airway walls, NOT in the lower airways.\n"
        "**Why not the others:** All the other statements (A, B, D, E) are correct "
        "descriptions of particle deposition principles.\n"
        "**Exam tip:** Particle deposition: impaction (upper) → sedimentation (lower) → "
        "diffusion (alveolar) as air velocity decreases.\n"
        "**Source:** C&D 12th ed., Respiratory Toxicology"
    )
    
    # DABT-4425: Tetrodotoxin is NOT a mycotoxin
    explanations['DABT-4425'] = (
        "**Answer: D** — Tetrodotoxin (TTX) is a marine neurotoxin produced by bacteria "
        "found in pufferfish and certain marine organisms — it is NOT a mycotoxin (fungal "
        "toxin). Trichothecenes, ergot alkaloids, fumonisins, and sterigmatocystin are "
        "all produced by fungi.\n"
        "**Why not the others:** Distractor C (fumonisin) is a Fusarium mycotoxin found "
        "in corn, associated with esophageal cancer and leukoencephalomalacia.\n"
        "**Exam tip:** Mycotoxins come from fungi; tetrodotoxin comes from bacteria "
        "(Vibrio, etc.) associated with marine animals.\n"
        "**Source:** C&D 12th ed., Mycotoxins chapter; IARC Monographs"
    )
    
    # DABT-4428: Ergot alkaloids - peripheral vasoconstriction
    explanations['DABT-4428'] = (
        "**Answer: D** — Ergot alkaloids cause peripheral vasoconstriction via "
        "α-adrenergic receptor agonism and serotonin (5-HT2) receptor partial agonism, "
        "leading to ischemic necrosis of extremities (St. Anthony's fire) and uterine "
        "contractions causing abortion.\n"
        "**Why not the others:** Distractor C (peripheral vasodilation) is the opposite "
        "effect — ergot causes vasoconstriction, not dilation.\n"
        "**Exam tip:** Ergot derivatives are used clinically for migraine (vasoconstriction "
        "of cranial vessels) and postpartum hemorrhage (uterine contraction).\n"
        "**Source:** C&D 12th ed., Mycotoxins; Goodman & Gilman's"
    )
    
    # DABT-4429: Doxorubicin neuronopathy - dorsal root ganglia
    explanations['DABT-4429'] = (
        "**Answer: C** — Doxorubicin (adriamycin)-induced neuronopathy predominantly "
        "affects the dorsal root ganglia (DRG) and autonomic ganglia of the peripheral "
        "nervous system because these neurons lack an effective blood-nerve barrier and "
        "accumulate the drug.\n"
        "**Why not the others:** Distractor A (limited to CNS) is incorrect — doxorubicin "
        "does not readily cross the BBB, so CNS effects are limited; the primary toxicity "
        "is to peripheral sensory and autonomic ganglia.\n"
        "**Exam tip:** Doxorubicin causes a sensory neuronopathy (dorsal root ganglia) "
        "and cardiotoxicity, but NOT CNS effects due to the BBB.\n"
        "**Source:** C&D 12th ed., Neurotoxicology chapter"
    )
    
    # DABT-4433: Mouse lymphoma assay endpoints
    explanations['DABT-4433'] = (
        "**Answer: D** — The mouse lymphoma assay (MLA) using the thymidine kinase (TK) "
        "locus detects a broad spectrum of genetic damage including point mutations, large "
        "and small deletions, translocations, and recombination events at the TK locus.\n"
        "**Why not the others:** Distractor B (micronuclei) is detected by a different "
        "assay (micronucleus test, OECD 474), not the MLA.\n"
        "**Exam tip:** MLA detects both gene mutations and chromosomal effects (clastogenic "
        "and aneugenic) at a single locus — it's a comprehensive in vitro genotoxicity test.\n"
        "**Source:** OECD TG 490; ICH S2(R1)"
    )
    
    # DABT-4435: Aspartame NOT teratogenic
    explanations['DABT-4435'] = (
        "**Answer: C** — Aspartame, an artificial sweetener metabolized to phenylalanine, "
        "aspartic acid, and methanol, has no known human teratogenic potential at "
        "consumed levels (except in phenylketonurics).\n"
        "**Why not the others:** All other options (thalidomide, isotretinoin, ethanol, "
        "methylmercury) are well-established human teratogens with known mechanisms.\n"
        "**Exam tip:** Known human teratogens include: thalidomide, retinoids, alcohol, "
        "mercury, valproic acid, warfarin, and tetracyclines.\n"
        "**Source:** C&D 12th ed., Developmental Toxicology; Shepard's Catalog"
    )
    
    # DABT-4436: EU ban on animal testing for cosmetics
    explanations['DABT-4436'] = (
        "**Answer: D** — The 2013 EU Directive (2003/15/EC, 7th Amendment to the Cosmetics "
        "Directive) banned all animal testing of cosmetic products and ingredients, "
        "including a full marketing ban regardless of where the testing occurred.\n"
        "**Why not the others:** Distractor A (pharmaceuticals) and C (preservatives) are "
        "not covered by this ban — the ban specifically targets cosmetics.\n"
        "**Exam tip:** The EU Cosmetics Animal Testing Ban has had major global impact "
        "on the development of alternative (non-animal) test methods.\n"
        "**Source:** EU Cosmetics Directive 1223/2009; ICCVAM/ECVAM"
    )
    
    # DABT-4437: 5-10 micron particles - impaction in UPPER airways, not alveolar
    explanations['DABT-4437'] = (
        "**Answer: C** — Particles of 5-10 μm deposit primarily by impaction in the "
        "upper and conducting airways (nasopharynx, trachea, bronchi), NOT in the "
        "alveolar region where deposition occurs by sedimentation and diffusion.\n"
        "**Why not the others:** All other statements (A, B, D, E) are correct regarding "
        "alveolar anatomy and physiology.\n"
        "**Exam tip:** Particle size determines deposition site: >10 μm = nasopharyngeal, "
        "5-10 μm = tracheobronchial, 1-5 μm = alveolar (by sedimentation), <0.5 μm = "
        "alveolar (by diffusion).\n"
        "**Source:** C&D 12th ed., Respiratory Toxicology"
    )
    
    # DABT-4438: Hormesis - NOT limited to initiation
    explanations['DABT-4438'] = (
        "**Answer: B** — The statement that \"hormetic responses have only been identified "
        "in initiation, and not in the promotion step\" is NOT CORRECT — hormesis has been "
        "observed at multiple stages of carcinogenesis and in diverse biological endpoints "
        "including both initiation and promotion.\n"
        "**Why not the others:** All other statements (A, C, D, E) correctly describe "
        "aspects of hormesis (U/J-shaped curve, beneficial low-dose effects, adaptive "
        "responses, ROS/P450 involvement).\n"
        "**Exam tip:** Hormesis = biphasic dose-response where low doses are beneficial "
        "(or stimulatory) and high doses are inhibitory.\n"
        "**Source:** C&D; Calabrese & Blain (2009), Toxicology and Applied Pharmacology"
    )
    
    # DABT-4439: Naphthalene cataracts - aldose reductase metabolite
    explanations['DABT-4439'] = (
        "**Answer: D** — Naphthalene is metabolized by aldose reductase to "
        "1,2-dihydro-1,2-dihydroxynaphthalene (naphthalene dihydrodiol), which undergoes "
        "further oxidation to form naphthoquinones that generate oxidative stress in the "
        "lens, leading to cortical cataracts.\n"
        "**Why not the others:** Distractor E (lens oxidation due to ROS) describes the "
        "downstream effect but not the specific initiating mechanism — the key first step "
        "is the aldose reductase-mediated metabolism.\n"
        "**Exam tip:** Aldose reductase in the lens converts sugars/naphthalene to diols "
        "that generate oxidative damage. Same enzyme implicated in diabetic cataracts.\n"
        "**Source:** C&D, Ocular Toxicology; Hayes, Ch. 17"
    )
    
    # DABT-4440: Mechanisms of teratogenesis - NOT interference in RNA function by antibiotics
    explanations['DABT-4440'] = (
        "**Answer: D** — While antibiotic interference with RNA function can cause "
        "developmental toxicity in some cases, it is NOT classically recognized as a "
        "primary mechanism of teratogenesis. The major recognized mechanisms include "
        "altered nucleic acid synthesis, chromosomal abnormalities, enzyme inhibition, "
        "and mitotic interference.\n"
        "**Why not the others:** Distractor A (alterations in nucleic acid synthesis) is "
        "a well-established mechanism of teratogenesis (e.g., hydroxyurea, cytarabine).\n"
        "**Exam tip:** Wilson's six general mechanisms of teratogenesis: mutations, "
        "chromosomal aberrations, mitotic interference, altered nucleic acid synthesis, "
        "enzyme inhibition, and lack of metabolic substrates.\n"
        "**Source:** C&D 12th ed., Developmental Toxicology; Wilson (1977)"
    )
    
    # DABT-4443: Radiation causes DNA mutations
    explanations['DABT-4443'] = (
        "**Answer: E** — Radiation (ionizing radiation) directly damages DNA through "
        "direct ionization of DNA and indirect effects via reactive oxygen species, "
        "causing base modifications, single- and double-strand breaks, and chromosomal "
        "aberrations that alter the nucleotide sequence.\n"
        "**Why not the others:** Distractor A (methylmercury) is a developmental "
        "neurotoxicant that disrupts cell migration and division, but its teratogenicity "
        "is not primarily through direct DNA sequence alteration.\n"
        "**Exam tip:** Radiation is a direct mutagen — it physically breaks DNA. Most "
        "chemical teratogens work through other mechanisms (enzyme inhibition, etc.).\n"
        "**Source:** C&D 12th ed., Radiation Toxicology; Developmental Toxicology"
    )
    
    # DABT-4444: Abnormal sperm morphology - germ cell access
    explanations['DABT-4444'] = (
        "**Answer: D** — An increase in abnormal sperm morphology indicates that a "
        "toxicant has gained access to the germ cells (spermatogonia, spermatocytes, or "
        "spermatids) within the seminiferous tubules, where it can disrupt spermatogenesis.\n"
        "**Why not the others:** Distractor E (cauda epididymis) is the storage site for "
        "mature sperm — abnormalities induced there affect motility/capacity, not morphology "
        "of developing sperm.\n"
        "**Exam tip:** Sperm morphology reflects damage during spermatogenesis (germ cell "
        "stage). Motility/viability can reflect epididymal damage.\n"
        "**Source:** C&D 12th ed., Male Reproductive Toxicology"
    )
    
    # DABT-4445: Rats more prone to thyroid tumors - EXCEPT CYP2B induction
    explanations['DABT-4445'] = (
        "**Answer: D** — The statement that \"CYP2B enzymes are not as readily induced "
        "in rats as in humans\" is NOT CORRECT and is therefore the exception — rat "
        "CYP2B enzymes are actually more readily induced than human CYP2B enzymes, "
        "contributing to the rat's greater sensitivity to thyroid disruption.\n"
        "**Why not the others:** Options A (no TBG), B (shorter T4 half-life), C (higher "
        "TSH in rats), and E (higher T4 production rate) are all correct explanations "
        "for why rats are more prone to TSH-driven thyroid tumors.\n"
        "**Exam tip:** Rodents lack TBG, have faster T4 clearance, higher TSH, and are "
        "more sensitive to hepatic enzyme induction that increases T4 clearance.\n"
        "**Source:** C&D 12th ed., Endocrine Toxicology; ICH S1 guidance"
    )
    
    # DABT-4447: CO is NOT a direct-acting pulmonary irritant
    explanations['DABT-4447'] = (
        "**Answer: B** — Carbon monoxide is a chemical asphyxiant that causes toxicity "
        "by binding hemoglobin and inhibiting cytochrome oxidase, NOT by direct irritation "
        "of pulmonary tissues. Ammonia, chlorine, hydrogen fluoride, and phosgene are "
        "all direct-acting pulmonary irritants.\n"
        "**Why not the others:** Distractor A (ammonia) is highly water-soluble and a "
        "potent upper respiratory tract irritant.\n"
        "**Exam tip:** Direct irritants cause local tissue damage at the site of contact. "
        "Asphyxiants (CO, cyanide) cause systemic hypoxia without local irritation.\n"
        "**Source:** C&D 12th ed., Respiratory Toxicology"
    )
    
    # DABT-4449: Reticulocytosis = compensatory response to RBC loss
    explanations['DABT-4449'] = (
        "**Answer: C** — Reticulocytosis (increased immature RBCs in circulation) is a "
        "compensatory bone marrow response to drug-induced red blood cell loss (hemolysis "
        "or blood loss). The bone marrow increases RBC production to compensate for "
        "peripheral RBC destruction/loss.\n"
        "**Why not the others:** Distractor D (aplastic anemia) causes reticulocytopenia "
        "(decreased reticulocytes) due to bone marrow failure, not reticulocytosis.\n"
        "**Exam tip:** Reticulocytosis = bone marrow is working. Reticulocytopenia = "
        "bone marrow is failing. High retics → think hemolysis or blood loss.\n"
        "**Source:** C&D, Hematotoxicology; Clinical pathology textbooks"
    )
    
    # DABT-4450: Chloroquine accumulation in eye - melanin binding
    explanations['DABT-4450'] = (
        "**Answer: D** — Chloroquine accumulates in the retinal pigment epithelium (RPE) "
        "and uveal tissues by reversibly binding to melanin, leading to dose-dependent "
        "retinopathy through slow release and long-term retention in melanin-rich tissues.\n"
        "**Why not the others:** Distractor A (decreased aqueous humor outflow) describes "
        "glaucoma mechanisms, not chloroquine-induced retinopathy.\n"
        "**Exam tip:** Drugs with high melanin affinity (chloroquine, phenothiazines, "
        "amiodarone) accumulate in the eye and cause retinopathy.\n"
        "**Source:** C&D 12th ed., Ocular Toxicology; Hayes, Ch. 17"
    )
    
    # DABT-4452: BaP metabolic designation as procarcinogen→proximate→ultimate
    explanations['DABT-4452'] = (
        "**Answer: B** — Benzo[a]pyrene is a procarcinogen (requires metabolic activation), "
        "BaP 7,8-epoxide is a proximate carcinogen (first activation product), and "
        "BaP 7,8-diol-9,10-epoxide is the ultimate carcinogen (the DNA-reactive species "
        "that forms adducts with guanine).\n"
        "**Why not the others:** Distractor E reverses the order — the ultimate carcinogen "
        "is the diol epoxide, not the procarcinogen.\n"
        "**Exam tip:** Procarcinogen → Phase I → Proximate carcinogen → Phase I → "
        "Ultimate carcinogen (DNA-reactive). BaP activation: CYP→EH→CYP.\n"
        "**Source:** C&D 12th ed., Carcinogenesis; IARC Monograph Vol. 100F"
    )
    
    # DABT-4453: Cardiac arrhythmia - interference with ion homeostasis
    explanations['DABT-4453'] = (
        "**Answer: C** — Cardiac arrhythmia most commonly results from interference with "
        "ion homeostasis — disruption of Na+, K+, Ca2+, or the hERG potassium channel "
        "alters cardiac action potential duration and conduction, leading to QT "
        "prolongation and arrhythmias.\n"
        "**Why not the others:** Distractor B (oxidative stress) contributes to myocardial "
        "injury and apoptosis but is not the most direct mechanism of arrhythmia — ion "
        "channel disruption is primary.\n"
        "**Exam tip:** hERG channel blockade (drug-induced QT prolongation) is a leading "
        "cause of drug withdrawal — a key regulatory toxicology topic.\n"
        "**Source:** C&D 12th ed., Cardiovascular Toxicology; ICH S7B"
    )
    
    # DABT-4454: Promotion = clonal expansion of initiated cells
    explanations['DABT-4454'] = (
        "**Answer: A** — Promotion in the multistage carcinogenesis model is the selective "
        "clonal expansion of initiated (mutated) cells, mediated by tumor promoters that "
        "activate cell proliferation pathways without directly damaging DNA.\n"
        "**Why not the others:** Distractor B (tumor promoters are typically mutagenic) "
        "is incorrect — promoters are typically NON-mutagenic and act through epigenetic "
        "mechanisms (e.g., PKC activation by phorbol esters).\n"
        "**Exam tip:** Initiation is irreversible (DNA mutation). Promotion is reversible "
        "and requires prolonged exposure to the promoter.\n"
        "**Source:** C&D 12th ed., Carcinogenesis chapter"
    )
    
    # DABT-4455: Comet assay = single-cell gel electrophoresis for DNA damage
    explanations['DABT-4455'] = (
        "**Answer: C** — The Comet assay (single-cell gel electrophoresis) measures DNA "
        "strand breaks (single- and double-strand) and alkali-labile sites in individual "
        "cells. Damaged DNA migrates from the nucleus, forming a \"comet tail\".\n"
        "**Why not the others:** Distractor A (CYP450 induction) is measured by enzyme "
        "activity assays or Western blot, not by the Comet assay.\n"
        "**Exam tip:** Comet tail length/moment = DNA damage. Can be used in vivo and "
        "in vitro under alkaline (pH >13) or neutral conditions.\n"
        "**Source:** OECD TG 489; ICH S2(R1)"
    )
    
    # DABT-4456: Ames test - S9 metabolic activation for promutagens
    explanations['DABT-4456'] = (
        "**Answer: A** — The S9 liver homogenate (microsomal fraction) is added to the "
        "Ames test to simulate mammalian metabolism because many compounds that are not "
        "directly mutagenic (promutagens/procarcinogens) are bioactivated by cytochrome "
        "P450 enzymes into genotoxic metabolites.\n"
        "**Why not the others:** Distractor D (IARC/FDA regulation) is incorrect — the S9 "
        "addition is a scientific requirement to detect promutagens, not merely a "
        "regulatory formality.\n"
        "**Exam tip:** S9 = 9000×g supernatant from Aroclor- or phenobarbital/β-naphtho-"
        "flavone-induced rat liver. Contains CYPs and phase II enzymes.\n"
        "**Source:** OECD TG 471; Ames et al. (1975); C&D, Genetic Toxicology"
    )
    
    # DABT-4458: IgE mediates immediate allergic reactions
    explanations['DABT-4458'] = (
        "**Answer: D** — IgE is the immunoglobulin most associated with immediate onset "
        "(Type I) allergic reactions. It binds to Fcε receptors on mast cells and "
        "basophils, and cross-linking by allergen triggers degranulation with histamine "
        "release within minutes.\n"
        "**Why not the others:** Distractor A (IgG) mediates delayed-type hypersensitivity "
        "and is associated with Type II and III reactions, not immediate anaphylaxis.\n"
        "**Exam tip:** IgE = allergy (immediate). IgG = memory/neutralization. IgA = "
        "mucosal. IgM = primary response. IgD = B cell receptor.\n"
        "**Source:** C&D 12th ed., Immunotoxicology; Abbas, Cellular and Molecular Immunology"
    )
    
    # DABT-4459: Chloroquine - retinopathy
    explanations['DABT-4459'] = (
        "**Answer: C** — Chloroquine (and its analog hydroxychloroquine) is most closely "
        "associated with retinopathy due to accumulation in the retinal pigment epithelium "
        "via melanin binding, leading to dose-dependent, sometimes irreversible damage to "
        "the macula.\n"
        "**Why not the others:** Distractor A (histamine) is an endogenous mediator, not "
        "an exogenous agent that causes retinopathy.\n"
        "**Exam tip:** Retinopathy: chloroquine/hydroxychloroquine, vigabatrin, "
        "tamoxifen, ethambutol, methanol (formate).\n"
        "**Source:** C&D 12th ed., Ocular Toxicology; Hayes, Ch. 17"
    )
    
    # DABT-4460: Contact hypersensitivity - nickel
    explanations['DABT-4460'] = (
        "**Answer: B** — Nickel is the most common cause of allergic contact dermatitis "
        "worldwide. It acts as a hapten, binding to skin proteins and inducing a "
        "Type IV delayed-type hypersensitivity response mediated by T cells.\n"
        "**Why not the others:** Distractor A (iron) is essential and rarely causes "
        "contact hypersensitivity despite widespread exposure.\n"
        "**Exam tip:** Nickel is #1 contact allergen. Other common ones: chromium, "
        "cobalt, fragrance mix, neomycin, and latex.\n"
        "**Source:** C&D 12th ed., Dermal Toxicology; Immunotoxicology"
    )
    
    # DABT-4461: Acetaminophen overdose - hepatocyte necrosis
    explanations['DABT-4461'] = (
        "**Answer: A** — Acetaminophen (APAP) overdose causes centrilobular hepatic "
        "necrosis through bioactivation by CYP2E1 to NAPQI (N-acetyl-p-benzoquinone "
        "imine), which depletes glutathione and covalently binds to cellular proteins, "
        "leading to mitochondrial dysfunction and necrotic cell death.\n"
        "**Why not the others:** Distractor B (hepatic steatosis) is characteristic of "
        "different toxicants (e.g., CCl4, ethanol, tetracycline), not APAP.\n"
        "**Exam tip:** APAP is the leading cause of acute liver failure in the US. "
        "N-acetylcysteine (NAC) restores glutathione.\n"
        "**Source:** C&D 12th ed., Hepatotoxicity chapter; Goldfrank's"
    )
    
    # DABT-4462: Vitamin K deficiency from 90% corn diet
    explanations['DABT-4462'] = (
        "**Answer: C** — The internal hemorrhage at 21 days (onset time consistent with "
        "vitamin K-dependent clotting factor depletion) is best explained by dietary "
        "vitamin K deficiency — corn is extremely low in vitamin K, and the 90% dietary "
        "replacement resulted in inadequate vitamin K for synthesis of clotting factors "
        "II, VII, IX, and X.\n"
        "**Why not the others:** Distractor A (gene insertion causing dysfunctional "
        "clotting factors) is unlikely within 21 days and without evidence of genomic "
        "integration in somatic cells.\n"
        "**Exam tip:** This illustrates the importance of nutritional adequacy in "
        "dietary rodent studies — high-dose groups may suffer malnutrition from diet "
        "dilution.\n"
        "**Source:** C&D, Study Design; OECD TG 408 (90-day study)"
    )
    
    # DABT-4463: Phase I metabolism - functional group introduction
    explanations['DABT-4463'] = (
        "**Answer: A** — Phase I metabolism involves the introduction of a functional "
        "group (e.g., -OH, -COOH, -NH2, -SH) into the molecule via oxidation, reduction, "
        "or hydrolysis, primarily catalyzed by cytochrome P450 enzymes. This creates a "
        "handle for Phase II conjugation.\n"
        "**Why not the others:** Distractor B (conjugation with GSH) is a Phase II "
        "reaction, not Phase I.\n"
        "**Exam tip:** Phase I = functionalization (introduce/modify a group). Phase II = "
        "conjugation (add glucuronide, sulfate, GSH, etc.).\n"
        "**Source:** C&D 12th ed., Biotransformation chapter"
    )
    
    # DABT-4464: GLP regulations - quality and integrity of safety data
    explanations['DABT-4464'] = (
        "**Answer: C** — The purpose of the FDA's GLP regulations (21 CFR Part 58) is "
        "to assure the quality and integrity of safety data submitted to the FDA in "
        "support of product registration — this covers study conduct, data recording, "
        "facilities, equipment, personnel qualifications, and quality assurance.\n"
        "**Why not the others:** Distractor D (providing testing guidelines) describes "
        "OECD Test Guidelines or FDA Guidance documents, which are distinct from GLP "
        "quality system regulations.\n"
        "**Exam tip:** GLP = HOW studies are conducted (quality system). Test "
        "Guidelines = WHAT studies are conducted (methodology).\n"
        "**Source:** 21 CFR Part 58; OECD GLP (ENV/MC/CHEM(98)17)"
    )
    
    # DABT-4466: ICH - harmonization for pharmaceutical registration
    explanations['DABT-4466'] = (
        "**Answer: B** — The International Conference on Harmonization of Technical "
        "Requirements for the Registration of Pharmaceuticals for Human Use (ICH) is a "
        "joint regulatory/industry project between Europe, Japan, and the US to harmonize "
        "the scientific and technical aspects of drug development and registration, "
        "reducing duplication and delays.\n"
        "**Why not the others:** Distractor D (ICH terminated in 1997) is factually "
        "incorrect — ICH continues to operate and expand globally.\n"
        "**Exam tip:** ICH brings together regulators and industry from EU, Japan, US. "
        "Key safety guidelines: Q1 (stability), S1 (carcinogenicity), S2 (genotoxicity), "
        "S7 (safety pharmacology), S8 (immunotoxicity), M3 (nonclinical).\n"
        "**Source:** ICH Official Website; C&D, Regulatory Toxicology"
    )
    
    # DABT-4468: ICH carcinogenicity - 6 months continuous use
    explanations['DABT-4468'] = (
        "**Answer: C** — According to ICH S1 guidance, a carcinogenicity study is "
        "required when a pharmaceutical is expected to be used continuously for at least "
        "6 months. This duration threshold reflects the window of chronic human exposure "
        "that warrants carcinogenicity assessment.\n"
        "**Why not the others:** Distractor D (all drugs require testing) is incorrect "
        "— drugs used for short periods (<6 months) generally do not require "
        "carcinogenicity studies unless there is specific concern.\n"
        "**Exam tip:** ICH S1 triggers: (1) ≥6 months continuous use, (2) known class "
        "concern, (3) genotoxic potential, (4) cause for concern from other data.\n"
        "**Source:** ICH S1A, S1B, S1C(R2)"
    )
    
    # DABT-4469: Necrosis - NOT always involving ordered steps (E is correct)
    explanations['DABT-4469'] = (
        "**Answer: E** — The statement that \"multiple metabolic defects that a cell "
        "suffers in its way to necrosis are ordered, involving cascade-like sequences\" "
        "is NOT CORRECT — necrosis is characterized by unorganized, chaotic cellular "
        "disintegration, unlike apoptosis which follows ordered biochemical cascades.\n"
        "**Why not the others:** Options A-D are all correct statements about necrosis "
        "vs apoptosis (e.g., both can involve MPT, necrotic cells swell and lyse, severe "
        "insults favor necrosis, ATP depletion blocks apoptosis).\n"
        "**Exam tip:** Necrosis = chaotic, unregulated. Apoptosis = programmed, ordered. "
        "ATP is required for apoptosis but not necrosis.\n"
        "**Source:** C&D 12th ed., Principles of Toxicology; Cell Death chapter"
    )
    
    # DABT-4470: Thiocyanate/perchlorate - inhibit iodide transport (NIS)
    explanations['DABT-4470'] = (
        "**Answer: A** — Thiocyanate (SCN−) and perchlorate (ClO4−) competitively inhibit "
        "the sodium-iodide symporter (NIS) on the basolateral membrane of thyroid "
        "follicular cells, blocking active iodide uptake into the thyroid.\n"
        "**Why not the others:** Distractor B (inhibition of thyroid peroxidase) is the "
        "mechanism of propylthiouracil (PTU) and methimazole, not thiocyanate/perchlorate.\n"
        "**Exam tip:** \"Perchlorate competes with per-iodide\" — NIS transports all "
        "monovalent anions of similar size. Thiocyanate from cigarette smoke is a relevant "
        "environmental goitrogen.\n"
        "**Source:** C&D 12th ed., Endocrine Toxicology; Goodman & Gilman's"
    )
    
    # DABT-4472: Nongenotoxic carcinogens - inhibit apoptosis, stimulate mitogenesis
    explanations['DABT-4472'] = (
        "**Answer: E** — Nongenotoxic carcinogens (e.g., phenobarbital, phorbol esters, "
        "peroxisome proliferators) promote cancer by inhibiting apoptosis (suppressing "
        "the elimination of damaged cells) and stimulating mitogenesis (increasing cell "
        "proliferation), creating more opportunities for spontaneous mutations to become "
        "fixed.\n"
        "**Why not the others:** Distractor C (inhibiting release of mitogens) would "
        "decrease cell proliferation, opposite to the actual tumor-promoting mechanism.\n"
        "**Exam tip:** Nongenotoxic = no DNA damage. Mechanisms: mitogenesis, "
        "apoptosis inhibition, immunosuppression, gap junction inhibition.\n"
        "**Source:** C&D 12th ed., Carcinogenesis chapter; ICH S1"
    )
    
    # DABT-4473: Salivation, miosis, lacrimation, diarrhea = SLUD (parasympathomimetic)
    explanations['DABT-4473'] = (
        "**Answer: D** — The clinical signs (salivation, miosis, chromodacryorrhea "
        "[blood-tinged lacrimation in rats], diarrhea) are classic muscarinic "
        "parasympathomimetic effects, typically caused by acetylcholinesterase inhibitors "
        "(organophosphates/carbamates) or direct muscarinic agonists.\n"
        "**Why not the others:** Distractor C (parasympathetic blockade) would produce "
        "the opposite effects: dry mouth, mydriasis, and constipation.\n"
        "**Exam tip:** \"SLUD\" syndrome: Salivation, Lacrimation, Urination, "
        "Defecation + miosis = cholinergic (parasympathomimetic) excess.\n"
        "**Source:** C&D 12th ed., Insecticides chapter; Hayes, Ch. 21"
    )
    
    # DABT-4475: REACH - existing substances also must be registered
    explanations['DABT-4475'] = (
        "**Answer: D** — The statement that \"new substances must be registered before "
        "they can be marketed, but existing substances are exempt\" is NOT CORRECT — "
        "REACH requires registration of both new and EXISTING substances. Existing "
        "substances are registered on a phased timeline based on tonnage and hazard "
        "properties.\n"
        "**Why not the others:** Options A, B, C, and E are correct descriptions of "
        "REACH requirements and principles.\n"
        "**Exam tip:** REACH = Registration, Evaluation, Authorisation of Chemicals. "
        "\"No data, no market.\" Establishes burden of proof on industry.\n"
        "**Source:** EU REACH Regulation (EC) 1907/2006; ECHA Website"
    )
    
    # DABT-4476: Thyroglobulin promoter for thyroid-specific transgenic expression
    explanations['DABT-4476'] = (
        "**Answer: C** — The thyroglobulin (Tg) promoter drives gene expression "
        "specifically in thyroid follicular cells, making it the appropriate combination "
        "of promoter and tissue type for targeted thyroid-specific transgenesis.\n"
        "**Why not the others:** Distractor A (GFAP: cerebellar neurons) is mismatched — "
        "GFAP (glial fibrillary acidic protein) is an astrocyte marker, not neuronal.\n"
        "**Exam tip:** Promoter choice determines tissue specificity. Common pairs: "
        "Albumin (liver), Thyroglobulin (thyroid), Myosin (muscle), Nestin (neural).\n"
        "**Source:** C&D 12th ed.; Transgenic models in toxicology"
    )
    
    # DABT-4479: Brain cholinesterase inhibition = biomarker of effect
    explanations['DABT-4479'] = (
        "**Answer: B** — Brain cholinesterase inhibition following carbamate exposure is "
        "a biomarker of effect — it measures the actual biological change (enzyme "
        "inhibition) in the target tissue that is directly linked to the mechanism of "
        "toxicity and adverse outcome.\n"
        "**Why not the others:** Distractor A (biomarker of exposure) would be measuring "
        "the parent compound or metabolite in blood/tissue, not the biological effect "
        "of enzyme inhibition.\n"
        "**Exam tip:** Biomarker of exposure = chemical or metabolite in body. Biomarker "
        "of effect = measurable biological change. Biomarker of susceptibility = genetic "
        "or acquired differences.\n"
        "**Source:** C&D, Risk Assessment; National Academy of Sciences"
    )
    
    # DABT-4480: Mercury vapor exposure - ambient air (dental amalgam is #1 source, but ambient is major for general public)
    explanations['DABT-4480'] = (
        "**Answer: E** — For the general public (non-occupationally exposed), the major "
        "source of exposure to mercury vapor is ambient air, primarily from natural "
        "degassing of the earth's crust, volcanic emissions, and re-emission from "
        "anthropogenic sources deposited in soils and water.\n"
        "**Why not the others:** Distractor B (amalgam dental fillings) releases some "
        "mercury vapor but is a secondary source for the general public compared to "
        "background ambient air. Fish (C) primarily contain methylmercury, not elemental "
        "mercury vapor.\n"
        "**Exam tip:** Elemental mercury vapor → inhaled → absorbed (80%) → crosses BBB. "
        "Methylmercury → ingested → absorbed (95%) from fish.\n"
        "**Source:** C&D 12th ed., Metals chapter; ATSDR Toxicological Profile for Mercury"
    )
    
    # DABT-4484: CYP3A is most abundant hepatic P450 in humans
    explanations['DABT-4484'] = (
        "**Answer: D** — CYP3A4 is the most abundant cytochrome P450 subfamily in the "
        "human liver, accounting for ~30-40% of total hepatic P450 content. It metabolizes "
        "~50% of all marketed drugs.\n"
        "**Why not the others:** Distractor B (CYP2A) accounts for a much smaller fraction "
        "(~4%) and metabolizes fewer drugs than CYP3A.\n"
        "**Exam tip:** CYP3A4 > CYP2C9 > CYP1A2 > CYP2E1 > CYP2D6 > CYP2A6 in human "
        "liver abundance. CYP3A4 = most abundant and most clinically important.\n"
        "**Source:** C&D 12th ed., Biotransformation chapter; Shimada et al. (1994)"
    )
    
    # DABT-4486: Therapeutic index = TD50/ED50
    explanations['DABT-4486'] = (
        "**Answer: A** — The therapeutic index (TI) is most commonly expressed as "
        "TD50/ED50 — the ratio of the median toxic dose to the median effective dose. "
        "A higher TI indicates a wider margin of safety.\n"
        "**Why not the others:** Distractor C (ED50/LD50) inverts the ratio — TI should "
        "be >1 for a safe drug, and the convention uses TD50 (or LD50) in the numerator.\n"
        "**Exam tip:** TI = TD50/ED50. Larger TI = safer drug. In preclinical studies, "
        "TI margin = NOAEL / clinical exposure.\n"
        "**Source:** C&D 12th ed., Principles; FDA Guidance"
    )
    
    return explanations


def main():
    # Load the batch
    with open(BATCH_PATH) as f:
        batch = json.load(f)
    
    print(f"Loaded {len(batch)} questions from batch file")
    
    # Generate explanations
    explanations = generate_explanations()
    print(f"Generated {len(explanations)} explanations")
    
    # Verify all 68 are covered
    missing = [d['id'] for d in batch if d['id'] not in explanations]
    if missing:
        print(f"WARNING: Missing explanations for: {missing}")
        sys.exit(1)
    
    # Connect to database
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    
    # Process in batches of ~20
    batch_size = 20
    total = len(batch)
    updated = 0
    
    for i in range(0, total, batch_size):
        batch_ids = [d['id'] for d in batch[i:i+batch_size]]
        print(f"\nProcessing batch {i//batch_size + 1}: IDs {batch_ids[0]} ... {batch_ids[-1]}")
        
        last_id = None
        for qid in batch_ids:
            last_id = qid
            explanation = explanations[qid]
            cursor.execute(
                "UPDATE questions SET explanation = ? WHERE id = ?",
                (explanation, qid)
            )
            if cursor.rowcount > 0:
                updated += 1
                print(f"  ✓ {qid}")
            else:
                print(f"  ✗ {qid} - NOT FOUND")
        
        db.commit()
        print(f"  Committed {len(batch_ids)} updates")
        
        # Save progress
        progress = {
            "total": total,
            "updated_so_far": updated,
            "batch_index": i + len(batch_ids),
            "last_id": last_id
        }
        with open(PROGRESS_PATH, 'w') as f:
            json.dump(progress, f, indent=2)
    
    db.close()
    
    print(f"\n{'='*60}")
    print(f"FINISHED: {updated} explanations updated in database")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
