#!/usr/bin/env python3
"""Generate exam-quality explanations for Past ABT Exam questions (slice 3) and write to DABT database."""
import json
import sqlite3

DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"
SLICE_PATH = "/root/work/dabt/explain_slice3.json"
PROGRESS_PATH = "/root/work/dabt/explain_progress_3.json"

with open(SLICE_PATH) as f:
    questions = json.load(f)
print(f"Loaded {len(questions)} questions")

EXPL = {}

EXPL['DABT-3897'] = (
    "**Answer: D** \u2014 Fetotoxicity requires dedicated developmental/reproductive toxicity studies "
    "with timed gestations \u2014 it is NOT assessed in short-term (14\u201328 day) studies. Short-term studies "
    "identify target organs, clinical pathology shifts, palatability issues, and body weight trends, which "
    "directly inform dose selection for subchronic studies.\n"
    "**Why not the others:** Palatability (C) might seem irrelevant, but short-term studies detect feed "
    "refusal that would compromise subchronic study interpretation.\n"
    "**Exam tip:** Short-term studies evaluate effects on the test animal itself, not its offspring. "
    "Anything related to reproduction/development belongs in later-stage dedicated studies.\n"
    "**Source:** C&D 8th ed., Ch. 3; Hayes, Principles and Methods of Toxicology"
)

EXPL['DABT-4142'] = (
    "**Answer: A** \u2014 Monoclonal antibodies are highly species-specific due to target epitope binding. "
    "A pharmacologically relevant species expressing the identical target antigen is essential \u2014 testing "
    "in a non-binding species yields meaningless safety data. This is the cornerstone of ICH S6.\n"
    "**Why not the others:** The standard rodent + non-rodent paradigm (D) often fails because many mAbs "
    "only bind primate targets. Genotoxicity testing (C) is rarely relevant for large-molecule biologics. "
    "CYP metabolism characterization (E) is not a primary concern for antibodies (catabolized to amino acids).\n"
    "**Exam tip:** For biologics, ICH S6 emphasizes relevant species first. If no relevant species exists, "
    "transgenic models or surrogate antibodies may be needed.\n"
    "**Source:** ICH S6(R1); C&D 8th ed., Ch. 34"
)

EXPL['DABT-4242'] = (
    "**Answer: D** \u2014 Prolonged QT interval on ECG indicates delayed ventricular repolarization, which "
    "creates an electrophysiological substrate (early afterdepolarizations) that can trigger torsades de "
    "pointes (TdP). Drug-induced hERG potassium channel blockade is the most common cause.\n"
    "**Why not the others:** P-wave notching (A) and elevated R wave amplitude (B) are not specific TdP "
    "risk markers. Inverted T wave (C) may indicate ischemia but is not the hallmark pre-TdP signal.\n"
    "**Exam tip:** hERG blockade leads to QT prolongation leading to TdP risk. This is the single most "
    "important cardiac safety signal in drug development (ICH S7B / E14).\n"
    "**Source:** C&D 8th ed., Ch. 13; ICH S7B"
)

EXPL['DABT-4330'] = (
    "**Answer: D** \u2014 Histological evidence of hypocellularity in primary and secondary lymphoid "
    "organs (spleen, thymus, lymph nodes) directly demonstrates immunosuppression through depletion of "
    "immune cell populations. This is a histopathological hallmark of immunotoxicity.\n"
    "**Why not the others:** Increased T-cell proliferation in the LLNA (B) and increased IgM antibody "
    "production (C, E) indicate immune STIMULATION, not suppression. Hemolytic anemia (A) is a Type II "
    "hypersensitivity (drug-induced autoimmune) reaction.\n"
    "**Exam tip:** Immunosuppression = decreased immune cell counts/function. Hypersensitivity/autoimmunity "
    "= overactive immune response. The LLNA specifically measures SENSITIZATION, not suppression.\n"
    "**Source:** C&D 8th ed., Ch. 12; ICH S8"
)

EXPL['DABT-4362'] = (
    "**Answer: D** \u2014 Understanding relationships between a chemical's metabolic pathways and its "
    "target organ interactions is a STRENGTH of animal studies \u2014 controlled conditions allow direct "
    "investigation of metabolism-toxicity relationships that is impossible in humans. Therefore, it is "
    "NOT a limitation.\n"
    "**Why not the others:** Interspecies differences in response (B) and metabolism (C), providing only "
    "estimates (A), and lacking predictive models for some chemicals (E) are genuine limitations of animal testing.\n"
    "**Exam tip:** The NOT question format means the wrong answers ARE limitations. Metabolic pathway "
    "analysis is precisely what animal models excel at providing.\n"
    "**Source:** C&D 8th ed., Ch. 1; Hayes"
)

EXPL['DABT-4364'] = (
    "**Answer: B** \u2014 Glucuronidation is a Phase II metabolic conjugation pathway for soluble small "
    "molecules, catalyzed by UDP-glucuronyltransferases. Nanoparticles are solid particulates, not "
    "substrates for enzymatic biotransformation, so this is NOT a factor in their pulmonary toxicity.\n"
    "**Why not the others:** Large surface area-to-mass ratio (A), particle diameter <100 nm (C), "
    "presence of reactive metals (D), and breathing rate/deposition (E) are all established determinants "
    "of nanoparticle lung toxicity.\n"
    "**Exam tip:** Nanoparticles cause toxicity through physical-chemical properties (size, surface "
    "reactivity, shape), not through classical xenobiotic metabolism pathways.\n"
    "**Source:** C&D 8th ed., Ch. 26; Oberdorster et al."
)

EXPL['DABT-4496'] = (
    "**Answer: C** \u2014 BPA is a high-production-volume chemical extensively used in polycarbonate "
    "plastics and epoxy resins lining food containers, from which it leaches into food and beverages, "
    "causing widespread human exposure. Its weak estrogenic activity via estrogen receptor binding is "
    "the mechanistic basis for endocrine disruption concerns.\n"
    "**Why not the others:** While BPA does bind the estrogen receptor, the COMPLETE answer includes both "
    "the extensive exposure context AND the endocrine mechanism. Option A (aryl hydrocarbon receptor) is incorrect.\n"
    "**Exam tip:** BPA is the classic example of an endocrine-disrupting chemical (EDC) acting as a weak "
    "estrogen receptor agonist. Know both the exposure source (plastics) and the mechanism (ER binding).\n"
    "**Source:** C&D 8th ed., Ch. 24"
)

EXPL['DABT-4499'] = (
    "**Answer: A** \u2014 Beryllium causes chronic beryllium disease (CBD), a granulomatous lung disorder "
    "mediated by a Type IV (cell-mediated) hypersensitivity reaction. In susceptible individuals, Be2+ "
    "acts as a hapten, presenting with MHC Class II molecules to activate CD4+ T-cells, leading to "
    "lung inflammation and granuloma formation.\n"
    "**Why not the others:** Metallothionein binding (B) is relevant for cadmium and zinc. Sunlight "
    "reactions (C) describe phytophotodermatitis. Detoxifying enzyme differences (D) are not the primary "
    "mechanism. Calcium displacement in bone (E) describes lead/radium.\n"
    "**Exam tip:** Beryllium is the classic metal hypersensitivity \u2014 think T-cell mediated "
    "granulomatous disease (like sarcoidosis). Genetic susceptibility (HLA-DPB1 Glu69) is a key feature.\n"
    "**Source:** C&D 8th ed., Ch. 23; Hayes"
)

EXPL['DABT-4500'] = (
    "**Answer: C** \u2014 The statement that younger subjects are often LESS sensitive to metals is "
    "NOT CORRECT. Children are MORE sensitive to metal toxicity due to higher gastrointestinal absorption, "
    "immature detoxification mechanisms, and developing organ systems.\n"
    "**Why not the others:** Portal of entry matters for reactive metals (A is correct). Many inorganics "
    "face no absorption barrier (B is correct). Essential metals have U-shaped dose-response curves "
    "(D is correct). Metals can induce oxidative stress cascades (E is correct).\n"
    "**Exam tip:** The exam will try to reverse the age-sensitivity relationship. Children are always "
    "the sensitive subpopulation for metal toxicity (especially lead and mercury).\n"
    "**Source:** C&D 8th ed., Ch. 23"
)

EXPL['DABT-4501'] = (
    "**Answer: C** \u2014 The brain is the major target organ for METHYL mercury (organic), not inorganic "
    "mercury. Inorganic mercury (e.g., HgCl2, Hg vapor) primarily targets the kidney (proximal tubule). "
    "Methyl mercury crosses the blood-brain barrier as a cysteine conjugate and causes focal neuronal "
    "necrosis in the visual cortex, cerebellum, and cerebral cortex.\n"
    "**Why not the others:** Methyl mercury does cross the placenta (A is correct). Predatory fish are "
    "the main human exposure source for methyl mercury (B is correct). Acrodynia (pink disease) can "
    "occur with chronic inorganic mercury poisoning in children (D is correct). Inhaled mercury vapor "
    "causes pulmonary effects (E is correct).\n"
    "**Exam tip:** Methyl mercury = brain (neurotoxicant). Inorganic mercury = kidney (nephrotoxicant). "
    "This is one of the most frequently tested distinctions in metal toxicology.\n"
    "**Source:** C&D 8th ed., Ch. 23; EPA IRIS"
)

EXPL['DABT-4502'] = (
    "**Answer: E** \u2014 Chronic cadmium exposure causes renal tubular dysfunction, characterized by "
    "low-molecular-weight proteinuria (beta2-microglobulinuria), glycosuria, and aminoaciduria \u2014 "
    "reflecting proximal tubular damage. The cadmium-metallothionein complex is filtered and reabsorbed "
    "in the proximal tubule, where accumulated cadmium causes cell injury.\n"
    "**Why not the others:** Cadmium causes osteomalacia from renal calcium wasting, not calcium "
    "accumulation. It is associated with hypertension, not hypotension. While cadmium-metallothionein "
    "accumulates, the clinical consequence is tubular dysfunction. Cadmium causes renal tubular injury.\n"
    "**Exam tip:** Itai-itai disease = cadmium poisoning + osteoporosis/osteomalacia + renal tubular "
    "dysfunction. Beta2-microglobulinuria is the key clinical biomarker.\n"
    "**Source:** C&D 8th ed., Ch. 23"
)

EXPL['DABT-4503'] = (
    "**Answer: C** \u2014 Hexavalent chromium [Cr(VI)] is a Group 1 IARC human lung carcinogen when "
    "inhaled. Cr(VI) enters cells via sulfate/phosphate transporters, is reduced intracellularly to "
    "Cr(III) through reactive intermediates, generating ROS and forming Cr-DNA adducts during the "
    "reduction process.\n"
    "**Why not the others:** Cr(III) has lower acute AND chronic toxicity than Cr(VI) \u2014 the answer "
    "choices that say otherwise have the relationship reversed. Cr(III) and Cr(VI) have vastly different "
    "toxicities. Cr(VI) is MORE toxic when ingested.\n"
    "**Exam tip:** Cr(VI) \u2192 carcinogenic (lung), corrosive. Cr(III) \u2192 essential nutrient "
    "(glucose tolerance factor), relatively non-toxic. The valence determines everything in chromium toxicology.\n"
    "**Source:** C&D 8th ed., Ch. 23; IARC Group 1"
)

EXPL['DABT-4504'] = (
    "**Answer: C** \u2014 Propylene glycol is primarily metabolized by alcohol dehydrogenase (ADH) to "
    "lactaldehyde, which is then further oxidized to lactic acid and ultimately to pyruvate. This metabolic "
    "pathway is analogous to that of ethanol and ethylene glycol.\n"
    "**Why not the others:** Glucuronidation (A) is a minor pathway. Epoxide hydrolase (B) is not involved "
    "\u2014 propylene glycol does not form an epoxide. Glutathione conjugation (D) is not a primary "
    "pathway. It is extensively metabolized (E is wrong).\n"
    "**Exam tip:** Propylene glycol, ethanol, ethylene glycol, and methanol all share ADH as the first "
    "step in metabolism. This is why ethanol competes as an antidote for methanol/ethylene glycol poisoning.\n"
    "**Source:** C&D; Goodman and Gilman"
)

EXPL['DABT-4505'] = (
    "**Answer: B** \u2014 Ethylene glycol is metabolized by ADH to glycolaldehyde, then to glycolic "
    "acid, glyoxylic acid, and finally oxalic acid. Calcium oxalate crystals precipitate in renal "
    "tubules, causing acute kidney injury (the hallmark manifestation).\n"
    "**Why not the others:** Ethylene glycol causes metabolic ACIDOSIS (not alkalosis) due to glycolic "
    "acid accumulation (A is wrong). It is toxic, not an excellent nontoxic solvent (C is wrong). "
    "While it is converted to toxic metabolites (D), option B more completely describes the mechanism "
    "including the oxalate crystal endpoint.\n"
    "**Exam tip:** The classic triad: oxalate crystals in urine + metabolic acidosis + acute renal "
    "failure. Antidote = ethanol or fomepizole (ADH inhibitors). Also associated with hypocalcemia "
    "from calcium-oxalate precipitation.\n"
    "**Source:** C&D; Goldfrank's"
)

EXPL['DABT-4506'] = (
    "**Answer: D** \u2014 Ethanol is a competitive substrate for alcohol dehydrogenase (ADH), the "
    "enzyme that metabolizes ethylene glycol to its toxic metabolites. By competitively inhibiting ADH, "
    "ethanol prevents formation of glycolate and oxalate, allowing ethylene glycol to be excreted "
    "unchanged renally.\n"
    "**Why not the others:** Ethanol is also the antidote for methanol poisoning, but among the given "
    "options (phenobarbital, PCP, iron, ethylene glycol, endrin), only ethylene glycol is treated "
    "with ethanol. Fomepizole is a more selective ADH inhibitor used for the same indication.\n"
    "**Exam tip:** ADH substrate competition: ethanol \u2192 acetaldehyde (preferred, high affinity), "
    "blocks metabolism of methanol/ethylene glycol. The goal is to maintain blood ethanol at 100\u2013150 mg/dL.\n"
    "**Source:** C&D; Goldfrank's"
)

EXPL['DABT-4507'] = (
    "**Answer: C** \u2014 Benzene is a well-established human leukemogen (IARC Group 1), causally "
    "associated with acute myeloid leukemia (AML) and myelodysplastic syndrome. Its bone marrow toxicity "
    "requires metabolic activation by CYP2E1 to phenol, hydroquinone, and 1,4-benzoquinone, which "
    "cause chromosomal aberrations in hematopoietic stem cells.\n"
    "**Why not the others:** Asbestos (A) \u2192 mesothelioma/lung cancer. Lead (B) \u2192 neurological/"
    "hematological effects (no leukemia). Paraquat (D) \u2192 pulmonary fibrosis. n-Hexane (E) \u2192 "
    "peripheral neuropathy.\n"
    "**Exam tip:** Benzene \u2192 AML is one of the strongest chemical-cancer associations known. "
    "The latency is typically 5\u201315 years. This is why benzene is so heavily regulated in occupational settings.\n"
    "**Source:** C&D 8th ed., Ch. 29; IARC Group 1"
)

EXPL['DABT-4508'] = (
    "**Answer: E** \u2014 For pulmonary studies of single-walled carbon nanotubes (SWCNTs), thorough "
    "physiochemical characterization of the test material (including particle size distribution, "
    "shape/aspect ratio, surface area, surface chemistry, purity/metal content, and degree of "
    "aggregation) is the MOST critical aspect. Without characterization, results are uninterpretable.\n"
    "**Why not the others:** BAL fluid analysis (C) and recovery phases (D) are standard in inhalation "
    "studies but not the unique critical aspect for nanomaterials. Liver biomarkers (A) are not the "
    "primary focus of pulmonary studies. 100% QA auditing (B) is excessive.\n"
    "**Exam tip:** For nanotoxicology studies, characterization is paramount. The OECD WPMN requires "
    "characterization of nanomaterials before toxicological testing \u2014 the physical form IS the dose metric.\n"
    "**Source:** C&D 8th ed., Ch. 26; OECD WPMN"
)

EXPL['DABT-4509'] = (
    "**Answer: A** \u2014 Bacillus thuringiensis produces parasporal crystal proteins (Cry toxins) "
    "that are solubilized in the alkaline insect midgut, activated by proteases, and bind to specific "
    "cadherin-like receptors on midgut brush border cells. Toxin insertion forms pores causing "
    "colloid-osmotic lysis and death of epithelial cells.\n"
    "**Why not the others:** Bt does not inhibit AChE (C) \u2014 that describes OPs/carbamates. It does "
    "not bind to neuropathy target esterase (D) \u2014 that describes OPIDN. It does not modify "
    "voltage-gated sodium channels (E) \u2014 that describes pyrethroids.\n"
    "**Exam tip:** Bt = Cry toxins \u2192 pore formation in gut \u2192 insect death. Highly specific "
    "for target insects; mammalian safety is excellent because mammalian gut pH and receptor profiles differ.\n"
    "**Source:** C&D 8th ed., Ch. 28; Hayes"
)

EXPL['DABT-4510'] = (
    "**Answer: B** \u2014 Pyrethroids delay the inactivation of voltage-gated sodium channels in nerve "
    "axons, prolonging sodium influx and causing repetitive neuronal firing (hyperexcitation). Type I "
    "pyrethroids (no alpha-cyano group, e.g., permethrin) cause T-syndrome (tremor, aggression); "
    "Type II (alpha-cyano, e.g., deltamethrin) cause CS-syndrome with additional GABA-A receptor antagonism.\n"
    "**Why not the others:** AChE inhibition (A) = OPs/carbamates. K+ channel activation (C) is not "
    "the primary mechanism. ATPase inhibition (D) is incorrect. Nicotinic receptor activation (E) is "
    "nicotine/neonicotinoids.\n"
    "**Exam tip:** Pyrethroids = sodium channel modulators (prolonged opening). Compare: DDT also "
    "delays sodium channel inactivation but with different kinetics.\n"
    "**Source:** C&D 8th ed., Ch. 28; Hayes"
)

EXPL['DABT-4511'] = (
    "**Answer: A** \u2014 Carbamates inhibit AChE, causing acetylcholine accumulation at synapses. "
    "The excess ACh overstimulates muscarinic receptors (smooth muscle, glands, heart) producing "
    "SLUDGE syndrome. The toxic action is specifically mediated through muscarinic receptor stimulation.\n"
    "**Why not the others:** Glutamate (B), glycine (C), serotonergic (D), and dopamine (E) receptors "
    "are not the primary mediators of carbamate toxicity. While nicotinic receptors also contribute, "
    "muscarinic effects dominate the clinical picture.\n"
    "**Exam tip:** Carbamates = reversible AChE inhibition \u2192 ACh excess \u2192 muscarinic "
    "(SLUDGE) + nicotinic (fasciculations) effects. Atropine blocks muscarinic effects specifically.\n"
    "**Source:** C&D 8th ed., Ch. 28"
)

EXPL['DABT-4512'] = (
    "**Answer: A** \u2014 Carbaryl is a carbamate that reversibly carbamylates the active site serine "
    "of AChE. The carbamylated enzyme undergoes spontaneous decarbamylation within minutes (half-life "
    "~30 minutes), restoring active enzyme. This contrasts with organophosphates, which phosphorylate "
    "AChE irreversibly.\n"
    "**Why not the others:** Malathion (B), chlorpyrifos (C), diazinon (D), and sarin (E) are all "
    "organophosphates that cause irreversible AChE inhibition through phosphorylation and aging.\n"
    "**Exam tip:** The key distinction: carbamates (carbaryl) = reversible (minutes to hours), "
    "OPs = irreversible (days for new enzyme synthesis). This is why pralidoxime works for OPs but "
    "is less needed for carbamates.\n"
    "**Source:** C&D 8th ed., Ch. 28; Hayes"
)

EXPL['DABT-4513'] = (
    "**Answer: C** \u2014 Organophosphates (OPs) inhibit AChE by phosphorylating the serine-OH at "
    "the esteratic site of the enzyme. This prevents hydrolysis of acetylcholine, causing "
    "neurotransmitter accumulation at cholinergic synapses. The inhibition becomes irreversible "
    "through the aging process (loss of an alkyl group from the phosphorylated enzyme).\n"
    "**Why not the others:** Anticoagulation (A) = warfarin-type rodenticides. Sodium channel "
    "modification (B) = pyrethroids. Mitochondrial respiratory inhibition (D) = rotenone, cyanide. "
    "Octopamine-dependent activation (E) = formamidines (amitraz).\n"
    "**Exam tip:** OPs: AChE inhibition \u2192 aging \u2192 irreversible. Carbamates: AChE "
    "inhibition \u2192 no aging \u2192 reversible. Antidote: atropine (muscarinic antagonist) + "
    "pralidoxime (reactivates unaged OP-AChE complex).\n"
    "**Source:** C&D 8th ed., Ch. 28"
)

EXPL['DABT-4514'] = (
    "**Answer: E** \u2014 Platinum compounds with antitumor activity (e.g., cisplatin, carboplatin) "
    "are well known for their dose-limiting nephrotoxicity, neurotoxicity, and ototoxicity. Cisplatin "
    "accumulates in the proximal tubule, causing oxidative stress, DNA damage, and apoptosis of renal "
    "tubular epithelial cells.\n"
    "**Why not the others:** Osmium tetroxide is a potent irritant/corrosive, not primarily a "
    "nephrotoxin (A). Palladium chloride is poorly absorbed from the GI tract (B). Platinum metal "
    "itself is biologically inert (C). Platinum salt sensitization (platinosis) is a chronic allergic "
    "respiratory effect, not acute (D).\n"
    "**Exam tip:** Pt compounds (antitumor) \u2192 nephrotoxic. Pt salts \u2192 respiratory "
    "sensitizer (platinosis). Inert metal \u2192 safe. Cisplatin nephrotoxicity is dose-limiting.\n"
    "**Source:** C&D 8th ed., Ch. 23; Goodman and Gilman"
)

EXPL['DABT-4515'] = (
    "**Answer: D** \u2014 Thallium poisoning presents with the classic triad: acute gastrointestinal "
    "distress (abdominal pain, vomiting), painful peripheral neuropathy (tingling, paresthesias), "
    "and ALOPECIA (hair loss, occurs ~2\u20133 weeks after exposure). Thallium was historically used "
    "as a rodenticide.\n"
    "**Why not the others:** Manganese (A) causes Parkinson-like extrapyramidal symptoms (no alopecia). "
    "Nicotine (B) causes autonomic effects. Rotenone (C) \u2192 mitochondrial complex I inhibition. "
    "Fluoroacetic acid (E) \u2192 aconitase inhibition in TCA cycle.\n"
    "**Exam tip:** Thallium + alopecia is the single most pathognomonic clue in toxicology. "
    "Mechanism: substitutes for potassium in Na+/K+-ATPase, binds to sulfhydryl groups.\n"
    "**Source:** C&D 8th ed., Ch. 23; Goldfrank's"
)

EXPL['DABT-4516'] = (
    "**Answer: C** \u2014 Atropine is the first-line pharmacologic antidote for acute organophosphate "
    "poisoning. It competitively blocks muscarinic acetylcholine receptors, countering the excessive "
    "cholinergic stimulation that causes SLUDGE syndrome, bronchospasm, and bradycardia. "
    "Pralidoxime (2-PAM) is used adjunctively to reactivate AChE.\n"
    "**Why not the others:** Methylene blue (A) treats methemoglobinemia. Vitamin K1 (B) reverses "
    "warfarin anticoagulation. Ethanol (D) treats methanol/ethylene glycol poisoning. Chelation "
    "therapy (E) treats heavy metal poisoning.\n"
    "**Exam tip:** OP antidote regimen: Atropine (blocks muscarinic effects) + Pralidoxime (reactivates "
    "AChE BEFORE aging occurs). Atropine dosing needs to be much higher than standard ACLS doses in OP poisoning.\n"
    "**Source:** C&D 8th ed., Ch. 28; Goldfrank's"
)

EXPL['DABT-4517'] = (
    "**Answer: A** \u2014 Sodium nitrite treats cyanide poisoning by oxidizing hemoglobin (Fe2+) to "
    "methemoglobin (Fe3+). Cyanide (CN-) binds with very high affinity to methemoglobin (forming "
    "cyanmethemoglobin), preventing it from binding to and inhibiting cytochrome c oxidase (complex "
    "IV). This restores cellular oxidative phosphorylation.\n"
    "**Why not the others:** Sodium nitrite does NOT increase oxidative phosphorylation (B) \u2014 it "
    "actually temporarily impairs oxygen delivery by creating methemoglobin. It does not primarily "
    "increase coronary flow (C), decrease intracranial pressure (D), or relax smooth muscle (E).\n"
    "**Exam tip:** The cyanide antidote kit: (1) Sodium nitrite \u2192 forms methemoglobin \u2192 "
    "CN- binds to methemoglobin; (2) Sodium thiosulfate \u2192 provides sulfur for rhodanese \u2192 "
    "converts CN- to thiocyanate (excreted renally).\n"
    "**Source:** C&D; Goldfrank's"
)

EXPL['DABT-4518'] = (
    "**Answer: C** \u2014 Aggregation and agglomeration of nanoparticles INCREASES their effective "
    "aerodynamic diameter, making them LESS toxic because they behave like larger particles with "
    "lower surface area-to-mass ratio and decreased penetration to the alveolar region. Therefore, "
    "aggregation is NOT a factor that increases toxicity.\n"
    "**Why not the others:** Unique biological nature compared to larger particles (A), translocation "
    "to secondary organs (B, D), and protein corona formation affecting clearance (E) are all factors "
    "that INCREASE or determine nanoparticle toxicity.\n"
    "**Exam tip:** This is a trick \u2014 aggregation REDUCES nanoparticle toxicity because small, "
    "well-dispersed particles have greater surface area and deeper lung penetration.\n"
    "**Source:** C&D 8th ed., Ch. 26; Oberdorster"
)

EXPL['DABT-4519'] = (
    "**Answer: D** \u2014 Carbon monoxide binds reversibly to hemoglobin with an affinity ~250 times "
    "greater than oxygen, forming carboxyhemoglobin (COHb). This reduces oxygen-carrying capacity "
    "and also shifts the oxyhemoglobin dissociation curve to the left, impairing oxygen unloading "
    "to tissues (dual mechanism of hypoxia).\n"
    "**Why not the others:** CO does bind myoglobin (A) and cytochrome c oxidase (B), but the "
    "PRIMARY toxicity is via hemoglobin binding. Methemoglobin (C) binds cyanide (treatment target). "
    "Cytochrome P450 (E) is not the major toxicity target.\n"
    "**Exam tip:** CO causes hypoxic hypoxia (not histotoxic hypoxia). Treatment = 100% O2 "
    "(half-life 90 min) or hyperbaric O2 (half-life 30 min). COHb >25% = severe poisoning.\n"
    "**Source:** C&D 8th ed., Ch. 14; Goldfrank's"
)

EXPL['DABT-4520'] = (
    "**Answer: C** \u2014 Particles deposited in the posterior (non-anterior) regions of the nose "
    "are cleared by mucociliary transport \u2014 trapped in mucus, moved by ciliary action to the "
    "glottis, and swallowed into the GI tract. This is the mucociliary escalator mechanism for the "
    "nasopharynx.\n"
    "**Why not the others:** Exhalation (A) clears only submicron particles. Absorption (B) applies "
    "to soluble particles. Phagocytosis by macrophages (D) is the primary alveolar clearance "
    "mechanism. Cough (E) clears tracheobronchial, not nasal, deposits.\n"
    "**Exam tip:** Regional clearance: Anterior nose \u2192 wiping/blowing (mechanical). Posterior "
    "nose + tracheobronchial \u2192 mucociliary escalator \u2192 swallowed. Alveolar \u2192 "
    "macrophage phagocytosis \u2192 different timescales.\n"
    "**Source:** C&D 8th ed., Ch. 14; ICRP Model"
)

EXPL['DABT-4521'] = (
    "**Answer: B** \u2014 The standard definition of a nanoparticle is a material with at least one "
    "dimension in the range of approximately 1\u2013100 nanometers. The option 0\u2013100 nm aligns "
    "with this definition. This size range confers unique quantum mechanical and surface properties.\n"
    "**Why not the others:** 1\u20135 um (A) is the micron/submicron range. 0.01\u20130.1 um (C) is "
    "equivalent to 10\u2013100 nm but uses um units. 1\u20135 nm (D) is too narrow. 10\u2013100 nm "
    "(E) excludes particles <10 nm which are still nanoscale.\n"
    "**Exam tip:** The definition is 1\u2013100 nm. The exam may present options in different units "
    "(um vs nm). Convert to nanometers to compare. 0.001\u20130.1 um = 1\u2013100 nm.\n"
    "**Source:** C&D 8th ed., Ch. 26; NIOSH; ISO/TS 27687"
)

EXPL['DABT-4522'] = (
    "**Answer: B** \u2014 At the nanoscale, materials exhibit different physical and chemical "
    "properties than their bulk counterparts of the same chemical composition (e.g., melting point, "
    "conductivity, surface reactivity, crystal structure). These size-dependent properties drive "
    "toxicological behavior and cannot be predicted from composition alone.\n"
    "**Why not the others:** Nanomaterials are NOT inert (A \u2014 they are surface-reactive). "
    "Carcinogenicity is not automatic (C). While handling challenges (D) and instability (E) exist, "
    "they don't explain the fundamental unpredictability from composition.\n"
    "**Exam tip:** The key concept: nanoscale = same chemistry, different physics. Surface area-to-volume "
    "ratio and quantum effects dominate at the nanoscale.\n"
    "**Source:** C&D 8th ed., Ch. 26"
)

EXPL['DABT-4523'] = (
    "**Answer: B** \u2014 Particle aerodynamic diameter is the single most critical determinant of "
    "where along the respiratory tract dust particles deposit. Particles >10 um deposit in the "
    "nasopharynx, 5\u201310 um in the tracheobronchial tree, 1\u20135 um in the bronchioles, and "
    "<1 um reach the alveolar region.\n"
    "**Why not the others:** Chemical composition (A) determines toxicity once deposited, not WHERE "
    "deposition occurs. Dissolution rate (C) and clearance rate (E) affect post-deposition fate. "
    "The lining (D) is the target but doesn't determine deposition site.\n"
    "**Exam tip:** Aerodynamic diameter controls deposition site by mass-dependent impaction, "
    "sedimentation, and diffusion mechanisms. This is the most fundamental principle in inhalation toxicology.\n"
    "**Source:** C&D 8th ed., Ch. 14; ICRP"
)

EXPL['DABT-4524'] = (
    "**Answer: A** \u2014 Foxglove (Digitalis purpurea) contains cardiac glycosides (digoxin, "
    "digitoxin) that inhibit the Na+/K+-ATPase pump in cardiac myocytes, increasing intracellular "
    "sodium and thus calcium via Na+/Ca2+ exchange. At toxic doses, this produces cardiac "
    "arrhythmias including bradycardia, AV block, ventricular tachycardia, and fibrillation.\n"
    "**Why not the others:** Hepatotoxicity (B), renal toxicity (C), CNS stimulation (D), and "
    "dermatitis (E) are not the primary effects of digitalis poisoning.\n"
    "**Exam tip:** Foxglove \u2192 digitalis \u2192 Na+/K+-ATPase inhibition \u2192 increased "
    "intracellular Ca2+ \u2192 arrhythmias. Treatment: Digoxin-specific Fab antibody fragments (Digibind).\n"
    "**Source:** C&D; Goldfrank's"
)

EXPL['DABT-4525'] = (
    "**Answer: B** \u2014 Black Widow spider venom (alpha-latrotoxin) acts at the neuromuscular "
    "synaptic junction by binding to presynaptic receptors (neurexins and latrophilins), causing "
    "massive calcium-dependent exocytosis of neurotransmitter vesicles (primarily acetylcholine, "
    "also norepinephrine). This produces uncontrolled muscle contraction, cramps, and autonomic hyperactivity.\n"
    "**Why not the others:** CNS action (A) is not the primary site. Optic nerve blockade (C), "
    "histamine release (D), and Purkinje fiber stimulation (E) are not mechanisms of alpha-latrotoxin.\n"
    "**Exam tip:** alpha-Latrotoxin \u2192 presynaptic \u2192 massive neurotransmitter release. "
    "Latrodectus envenomation = muscle cramps, rigidity, autonomic storm, but consciousness preserved.\n"
    "**Source:** C&D 8th ed., Ch. 28; Goldfrank's"
)

EXPL['DABT-4526'] = (
    "**Answer: B** \u2014 Base excision repair (BER) is the primary mechanism for repairing non-bulky, "
    "non-helix-distorting DNA damage, including oxidative base modifications (8-oxoguanine), "
    "alkylation bases (3-methyladenine), and abasic sites. BER involves damage-specific glycosylases "
    "that remove the damaged base, followed by AP endonuclease cleavage, repair synthesis, and ligation.\n"
    "**Why not the others:** Direct repair (A) is rare and specific (e.g., MGMT for O6-methylguanine). "
    "Photolyase (C) specifically repairs UV-induced cyclobutane pyrimidine dimers. Recombinational "
    "repair (D) handles double-strand breaks.\n"
    "**Exam tip:** BER = small/non-bulky lesions (oxidative, alkylation). NER = bulky/helix-distorting "
    "lesions (PAH adducts, UV dimers, cisplatin crosslinks). Know which repair pathway handles which "
    "type of damage.\n"
    "**Source:** C&D 8th ed., Ch. 9"
)

EXPL['DABT-4527'] = (
    "**Answer: D** \u2014 St. John's wort (Hypericum perforatum) is NOT associated with respiratory "
    "toxicity. It is well-known for causing photosensitization (via hypericin), serotonin syndrome "
    "(MAO inhibition/SSRI interaction), and inducing CYP3A4 and P-glycoprotein (causing drug interactions).\n"
    "**Why not the others:** The other pairs are correct associations: Kava Kava \u2192 CNS effects/"
    "hepatotoxicity (A). Hops \u2192 hematological effects/sedation (B). Senna \u2192 hepatotoxicity "
    "with chronic use (C). European mistletoe \u2192 cardiovascular toxicity (E).\n"
    "**Exam tip:** St. John's wort = the classic herb-drug interaction plant (CYP3A4 inducer). "
    "Photosensitization is another key effect. Not respiratory toxicity.\n"
    "**Source:** C&D 8th ed., Ch. 30"
)

EXPL['DABT-4528'] = (
    "**Answer: B** \u2014 Wasp venom (family Vespidae) works primarily by causing mast cell "
    "degranulation, releasing histamine and other vasoactive mediators. Venom components like "
    "phospholipase A1, antigen 5, and mastoparan directly trigger mast cells, producing pain, "
    "vasodilation, edema, and inflammation.\n"
    "**Why not the others:** AChE inhibition (A) = OP mechanism. Fibrinolytic activity (C) and "
    "hemorrhagic metalloproteinases (D) are characteristic of viperid snake venoms. Apoptosis "
    "induction (E) is not the primary mechanism.\n"
    "**Exam tip:** Hymenoptera venoms cause: (1) direct toxicity (mast cell degranulation, vasoactive "
    "amines), (2) IgE-mediated anaphylaxis in sensitized individuals. Anaphylaxis risk > direct toxicity.\n"
    "**Source:** C&D 8th ed., Ch. 28; Goldfrank's"
)

EXPL['DABT-4529'] = (
    "**Answer: C** \u2014 Melamine and cyanuric acid form insoluble co-precipitates "
    "(melamine-cyanurate crystals) in renal tubules via hydrogen bonding between the triazine "
    "rings. These crystals physically obstruct renal tubules, causing tubular necrosis, interstitial "
    "inflammation, and acute kidney injury. Neither compound alone is highly nephrotoxic.\n"
    "**Why not the others:** The toxicity is specifically renal crystal nephropathy, not acute "
    "cardiac (A), acid-base (B), hepatic (D), or mitochondrial (E) effects.\n"
    "**Exam tip:** Melamine + cyanuric acid = melamine cyanurate crystals (not melamine alone). "
    "This was the 2008 Chinese infant formula and 2007 pet food contamination crisis. The synergistic "
    "toxicity is the key exam point.\n"
    "**Source:** C&D 8th ed., Ch. 28; WHO"
)

EXPL['DABT-4530'] = (
    "**Answer: C** \u2014 Acrylamide is RAPIDLY absorbed from the gastrointestinal tract \u2014 not "
    "slowly. It is highly water-soluble and readily crosses biological membranes, with peak plasma "
    "concentrations reached within 30 minutes to 2 hours following oral ingestion. This statement "
    "is INCORRECT.\n"
    "**Why not the others:** Nervous system effects (A \u2014 distal axonopathy), rodent "
    "carcinogenicity (B \u2014 IARC 2A), formation via Maillard reaction at baking temperatures "
    ">120C (D), and approximate daily intake (E) are all correct.\n"
    "**Exam tip:** Acrylamide is formed from asparagine + reducing sugars at high cooking "
    "temperatures. It is rapidly absorbed, distributed to all tissues, and metabolized to "
    "glycidamide (the genotoxic metabolite) via CYP2E1.\n"
    "**Source:** C&D; JECFA/WHO; FDA"
)

EXPL['DABT-4531'] = (
    "**Answer: D** \u2014 Heterocyclic amines (HCAs), such as PhIP, IQ, and MeIQx, are formed "
    "when meat and fish are cooked at high temperatures (grilling, frying, broiling) via the "
    "Maillard reaction between creatine, amino acids, and sugars. They require metabolic activation "
    "to become DNA-reactive mutagens.\n"
    "**Why not the others:** Botulinum toxin (A) is produced by Clostridium botulinum contamination "
    "of improperly canned foods. Tetrodotoxin (B) is a marine biotoxin in pufferfish (not produced "
    "by cooking). Trichothecenes (C) and fumonisins (E) are mycotoxins produced by Fusarium fungi.\n"
    "**Exam tip:** Cooking produces HCAs (from meat) and acrylamide (from plant-based starches). "
    "Mycotoxins = pre-formed by fungi (aflatoxin, ochratoxin, fumonisin, trichothecene).\n"
    "**Source:** C&D 8th ed., Ch. 28"
)

EXPL['DABT-4532'] = (
    "**Answer: C** \u2014 Hy's Law identifies drug-induced hepatocellular jaundice predictive of "
    "severe DILI: ALT or AST >3 times ULN (hepatocellular injury) + total bilirubin >2 times ULN "
    "(impaired function/jaundice) + ALP <2 times ULN (excluding cholestasis). The key is that ALP "
    "is NOT elevated, distinguishing it from cholestatic injury.\n"
    "**Why not the others:** Options A and D include ALP elevation, indicating cholestasis (not "
    "Hy's Law pattern). Option B has the same issue. Option E describes an ALP-dominant pattern (cholestatic).\n"
    "**Exam tip:** Hy's Law: ALT >3x + bilirubin >2x + ALP <2x. This pattern carries a ~10\u201350% "
    "risk of fatal acute liver failure. It is named after Dr. Hyman Zimmerman.\n"
    "**Source:** FDA Guidance; C&D 8th ed., Ch. 15"
)

EXPL['DABT-4533'] = (
    "**Answer: E** \u2014 The primary reason for regulatory attention to nanotechnology is that "
    "significant routes of exposure (inhalation, dermal, ingestion) exist alongside the potential "
    "for novel toxicities, yet standardized testing protocols and risk assessment frameworks are "
    "still developing. Workers, consumers, and the environment may all be exposed.\n"
    "**Why not the others:** Nanoparticles are SMALLER than microparticles (A is false). While "
    "sensitive populations may be impacted (B), the broader concern is exposure potential + unknown "
    "risks. Nanoparticles ARE being produced to specific specifications (C is false).\n"
    "**Exam tip:** The regulatory challenge with nanomaterials = exposure potential + unique "
    "properties + limited toxicological data. This drives precautionary approaches globally.\n"
    "**Source:** C&D 8th ed., Ch. 26; EPA; FDA; OECD WPMN"
)

EXPL['DABT-4534'] = (
    "**Answer: C** \u2014 Acetaminophen metabolism in vivo involves: ~90% glucuronidation/sulfation "
    "(inactive), ~5% renal excretion, and ~5% CYP450-mediated oxidation (primarily CYP2E1, also "
    "CYP1A2, CYP3A4) to N-acetyl-p-benzoquinone imine (NAPQI). NAPQI is normally conjugated with "
    "glutathione. Following overdose, glutathione becomes depleted, allowing NAPQI to bind to hepatic "
    "proteins, causing centrilobular necrosis.\n"
    "**Why not the others:** While Option B describes a consequence (hepatic necrosis), Option C "
    "describes the ACTUAL metabolic mechanism. NAC is the antidote, not contraindicated (D is wrong).\n"
    "**Exam tip:** The classic acetaminophen toxicity pathway: Overdose \u2192 glutathione "
    "depletion \u2192 NAPQI accumulation \u2192 covalent binding to proteins \u2192 centrilobular "
    "necrosis. Antidote = N-acetylcysteine (repletes glutathione).\n"
    "**Source:** C&D 8th ed., Ch. 15; Goldfrank's"
)

EXPL['DABT-4535'] = (
    "**Answer: D** \u2014 Thallium poisoning produces a classic multisystem syndrome: acute GI "
    "symptoms (nausea, vomiting, abdominal pain), painful peripheral neuropathy (paresthesias, "
    "tingling), and ALOPECIA (hair loss \u2014 the pathognomonic sign appearing ~2\u20133 weeks "
    "post-exposure).\n"
    "**Why not the others:** Vanadium (A) \u2192 primarily respiratory irritation. Aflatoxin (B) \u2192 "
    "hepatotoxic/hepatocarcinogenic. Tin (C) \u2192 GI irritation but not neuropathy/alopecia. "
    "Phthalates (E) \u2192 reproductive/developmental toxicity.\n"
    "**Exam tip:** Thallium + alopecia + neuropathy + GI = the most distinctive poisoning syndrome. "
    "Also causes Mee's lines (transverse white nail bands).\n"
    "**Source:** C&D 8th ed., Ch. 23; Goldfrank's"
)

EXPL['DABT-4536'] = (
    "**Answer: D** \u2014 Cyclopeptides (e.g., microcystins, nodularins from cyanobacteria; "
    "amatoxins from Amanita mushrooms) are NOT associated with saxitoxin/paralytic shellfish "
    "poisoning (PSP). Saxitoxin is an alkaloid neurotoxin produced by marine dinoflagellates "
    "(Alexandrium species).\n"
    "**Why not the others:** Saxitoxin causes Na+ channel blockade (B) leading to paresthesia/"
    "paralysis (C), can suppress AV nodal conduction (A), and in severe cases causes respiratory "
    "paralysis/asphyxiation (E).\n"
    "**Exam tip:** PSP = saxitoxin = Na+ channel blocker. Amnesic shellfish poisoning = domoic "
    "acid = glutamate receptor agonist. Diarrheic shellfish poisoning = okadaic acid = protein "
    "phosphatase inhibitor. Know the differences.\n"
    "**Source:** C&D 8th ed., Ch. 28; FDA"
)

EXPL['DABT-4537'] = (
    "**Answer: D** \u2014 Release of growth factors that SUPPRESS cell proliferation would be a "
    "growth-inhibitory, tumor-suppressive process, which is OPPOSITE to neoplastic transformation. "
    "Neoplastic transformation involves sustained proliferative signaling, evasion of growth "
    "suppression, and resistance to cell death.\n"
    "**Why not the others:** Activation of proto-oncogenes (A), increased growth factor production "
    "(B), inactivation of tumor suppressor genes (C), and inhibition of apoptosis (E) are all "
    "classic hallmarks of cancer that promote neoplastic transformation.\n"
    "**Exam tip:** The hallmarks of cancer (Hanahan and Weinberg): sustained proliferation, evading "
    "growth suppressors, resisting cell death, replicative immortality, inducing angiogenesis, "
    "activating invasion/metastasis.\n"
    "**Source:** C&D 8th ed., Ch. 8; Hanahan and Weinberg"
)

EXPL['DABT-4538'] = (
    "**Answer: C** \u2014 Caprolactam (the monomer for nylon-6) is NOT classified as IARC Group 1 "
    "(carcinogenic to humans). It has been classified by IARC as Group 4 (probably NOT carcinogenic "
    "to humans) based on extensive negative evidence from animal and human studies.\n"
    "**Why not the others:** Arsenic (A), aflatoxin (B), benzene (D), and vinyl chloride (E) are "
    "all well-established IARC Group 1 human carcinogens with sufficient evidence.\n"
    "**Exam tip:** Key IARC Group 1 agents to know: aflatoxin, arsenic, asbestos, benzene, benzidine, "
    "beryllium, cadmium, chromium(VI), ethanol, formaldehyde, nickel compounds, radon, tobacco, "
    "vinyl chloride. Caprolactam is NOT Group 1.\n"
    "**Source:** IARC Monographs; C&D 8th ed., Ch. 8"
)

EXPL['DABT-4539'] = (
    "**Answer: C** \u2014 These drugs induce hepatic microsomal enzymes (especially UDP-glucuronyltransferases), "
    "which increase T4 glucuronidation and biliary clearance. Reduced serum T4 stimulates TSH "
    "secretion via negative feedback. Sustained TSH elevation drives thyroid follicular cell "
    "hypertrophy, hyperplasia, and eventual neoplasia in rats.\n"
    "**Why not the others:** Decreasing microsomal enzymes (A) would have the opposite effect. "
    "Increased T4 release (B) would suppress TSH. 5'-monodeiodinase inhibition (D) affects "
    "T4\u2192T3 conversion. Iodine organification inhibition (E) is the mechanism of goitrogenic "
    "drugs like PTU.\n"
    "**Exam tip:** This is a RAT-SPECIFIC mechanism. Rats lack thyroxine-binding globulin (TBG), "
    "making them uniquely sensitive to TSH-driven thyroid tumors. NOT relevant to human risk assessment.\n"
    "**Source:** C&D 8th ed., Ch. 22; ICH S1B; EPA"
)

EXPL['DABT-4540'] = (
    "**Answer: C** \u2014 Water solubility (often expressed as blood:gas partition coefficient) is "
    "the primary factor determining a gas's penetration depth into the respiratory tract. Highly "
    "water-soluble gases (e.g., ammonia, formaldehyde, SO2) are scrubbed by the nasal mucosa. "
    "Poorly soluble gases (e.g., phosgene, NO2, ozone) penetrate to the alveolar region.\n"
    "**Why not the others:** Vapor pressure (A) affects volatility/concentration. Respiratory rate "
    "(B) affects total inhaled dose. Vapor density (D) and molecular weight (E) have relatively "
    "minor impacts on penetration compared to solubility.\n"
    "**Exam tip:** Solubility determines site of action: high solubility = upper respiratory "
    "(nose/throat), low solubility = lower respiratory (alveoli). Classic example: formaldehyde "
    "(high) \u2192 nasal cancer; phosgene (low) \u2192 pulmonary edema.\n"
    "**Source:** C&D 8th ed., Ch. 14"
)

EXPL['DABT-4541'] = (
    "**Answer: C** \u2014 In healthy individuals, mucociliary clearance of particles deposited in "
    "the lower tracheobronchial tree is generally completed within about 1 week. The mucociliary "
    "escalator moves particles at ~4\u201320 mm/min toward the glottis, where they are swallowed. "
    "Complete clearance of the lower airways takes 24 hours to several days.\n"
    "**Why not the others:** 1\u20134 hours (A) is more consistent with nasal clearance. 24\u201348 "
    "hours (B) is partially correct for upper tracheobronchial clearance but the lower airways "
    "take longer. 3 weeks to 3 months (D, E) describes alveolar macrophage-mediated clearance.\n"
    "**Exam tip:** Timescale hierarchy: Nasal (minutes-hours) < Tracheobronchial (hours-days) < "
    "Alveolar (weeks-months). This is a standard ICRP model concept.\n"
    "**Source:** C&D 8th ed., Ch. 14; ICRP Publication 66"
)

EXPL['DABT-4542'] = (
    "**Answer: B** \u2014 The rodent micronucleus test (OECD 474) is the gold-standard in vivo "
    "assay for assessing chromosomal damage. It detects micronuclei formed from acentric chromosome "
    "fragments or lagging whole chromosomes that are not incorporated into the main nucleus during "
    "erythroblast division. This directly reflects clastogenic or aneugenic events.\n"
    "**Why not the others:** The Ames assay (A) detects bacterial gene mutations (in vitro). Mouse "
    "lymphoma (C) detects Tk gene mutations in vitro. The SCE assay (D) and cytokinesis-block "
    "micronucleus (E) are in vitro assays.\n"
    "**Exam tip:** The key distinction: rodent micronucleus = IN VIVO chromosomal damage. The "
    "regulatory genotoxicity testing battery typically includes Ames (in vitro gene mutation) + "
    "micronucleus (in vivo chromosomal damage).\n"
    "**Source:** OECD 474; C&D 8th ed., Ch. 9; ICH S2(R1)"
)

EXPL['DABT-4543'] = (
    "**Answer: A** \u2014 The promotion stage requires repeated or continuous application of the "
    "promoting agent over an extended period. Promoters are non-mutagenic agents that stimulate "
    "proliferation of initiated cells through receptor-mediated pathways, causing selective clonal "
    "expansion. If the promoter is withdrawn, the process is reversible.\n"
    "**Why not the others:** Conversion of benign to malignant (B) is PROGRESSION. Promotion is a "
    "SLOW, not rapid, process (C). Promotion is REVERSIBLE (D). Promotion IS relevant to humans "
    "(E) \u2014 many human carcinogens are promoters.\n"
    "**Exam tip:** Initiation (rapid, irreversible, mutation) \u2192 Promotion (slow, reversible, "
    "clonal expansion) \u2192 Progression (irreversible, malignant transformation, genomic instability). "
    "TPA is the classic mouse skin tumor promoter.\n"
    "**Source:** C&D 8th ed., Ch. 8"
)

EXPL['DABT-4544'] = (
    "**Answer: B** \u2014 The first trimester (specifically embryonic period, days 18\u201360 "
    "post-conception) is the period of organogenesis when major organ systems, including the "
    "skeletal system, are forming. This is the most sensitive window for structural teratogenesis.\n"
    "**Why not the others:** At conception/pre-implantation (A), the all-or-none principle applies. "
    "Second (C) and third trimesters (D, E) involve histogenesis, functional maturation, and "
    "growth \u2014 skeletal effects at these stages cause growth retardation or functional deficits.\n"
    "**Exam tip:** The critical window concept: Each organ system has a specific sensitive period "
    "during organogenesis (first trimester). The developing CNS has the longest sensitive window.\n"
    "**Source:** C&D 8th ed., Ch. 10; ICH S5"
)

EXPL['DABT-4545'] = (
    "**Answer: A** \u2014 DNA adducts establish a genotoxic mode of action by showing that a "
    "chemical (or its metabolite) directly binds to DNA. If these adducts interfere with accurate "
    "DNA replication, they can cause mutations (miscoding) when bypassed by translesion synthesis "
    "polymerases, providing a mechanistic link between exposure and mutation.\n"
    "**Why not the others:** Spindle interference (B) is an aneugenic, not adduct-mediated "
    "mechanism. Protein adducts (C) are biomarkers of exposure, not DNA-based MOA. DNA adducts "
    "do not definitively predict human carcinogenicity (D). Adducts do not act as secondary messengers (E).\n"
    "**Exam tip:** DNA adducts = direct evidence of genotoxicity. The sequence is: chemical \u2192 "
    "DNA adduct \u2192 miscoding mutation \u2192 mutagenesis.\n"
    "**Source:** C&D 8th ed., Ch. 9"
)

EXPL['DABT-4546'] = (
    "**Answer: A** \u2014 Fibrosarcomas are malignant tumors of mesenchymal origin (fibroblasts/"
    "connective tissue). They are composed of spindle-shaped cells arranged in a herringbone "
    "pattern and are characterized by local invasion, metastasis, and recurrence.\n"
    "**Why not the others:** Fibrosarcomas are MALIGNANT (B is wrong). They are NOT the most common "
    "liver tumors (C \u2014 that would be hepatocellular adenoma/carcinoma). The difference from "
    "benign fibromas involves cellular atypia, mitotic activity, and invasion (D is wrong).\n"
    "**Exam tip:** Benign = -oma (fibroma). Malignant mesenchymal = -sarcoma (fibrosarcoma). "
    "Malignant epithelial = -carcinoma. This nomenclature applies across all tissue types.\n"
    "**Source:** C&D 8th ed., Ch. 8; Robbins Pathologic Basis of Disease"
)

EXPL['DABT-4547'] = (
    "**Answer: C** \u2014 The statement that humans are more sensitive to thyroid hormone "
    "insufficiency/deregulation than rats is NOT TRUE. Rats are MORE sensitive because they lack "
    "thyroxine-binding globulin (TBG), have a much shorter T4 half-life (~12 hours vs ~7 days "
    "in humans), and have higher basal TSH levels.\n"
    "**Why not the others:** Multiple sites within the HPT axis can be disrupted (A is true). "
    "UDP-GT induction increases T4 clearance (B is true). Sustained TSH elevation causes rat "
    "thyroid follicular cell cancer (D is true). Thyroid insufficiency impacts brain development (E is true).\n"
    "**Exam tip:** This is a crucial regulatory concept: TSH-driven rodent thyroid tumors are "
    "generally considered NOT relevant to humans due to fundamental physiological differences "
    "in thyroid hormone regulation.\n"
    "**Source:** C&D 8th ed., Ch. 22; ICH S1; EPA Guidelines"
)

EXPL['DABT-4549'] = (
    "**Answer: B** \u2014 Both humans and rats share the fundamental mammalian feature that germ "
    "cell development (spermatogenesis and oogenesis) is regulated by FSH and LH (gonadotropins) "
    "from the pituitary. This represents a conserved reproductive endocrine mechanism.\n"
    "**Why not the others:** Rats have an ESTROUS cycle (4\u20135 days) without a spontaneous "
    "luteal phase \u2014 humans have a MENSTRUAL cycle (A is a difference). Rat pregnancy is "
    "easily disrupted by estrogens (C \u2014 difference). Rat placenta lacks high aromatase "
    "activity (D \u2014 difference). The rat spermatogenic cycle is ~52 days, not ~75 (E).\n"
    "**Exam tip:** When asked about similarities, think conserved mammalian endocrinology. "
    "Estrous vs menstrual cycles, placentation, and hormone sensitivity are key differences.\n"
    "**Source:** C&D 8th ed., Ch. 10; ICH S5"
)

EXPL['DABT-4550'] = (
    "**Answer: B** \u2014 Antiandrogens cause DEMASCULINIZATION (feminization) of MALES, not "
    "masculinization of females. They block androgen receptors, resulting in reduced anogenital "
    "distance (AGD), nipple retention, hypospadias, and undescended testes in male offspring.\n"
    "**Why not the others:** AGD and nipple retention are valid in utero endocrine disruption "
    "endpoints (A is correct). Fish near pulp mills do show intersex and hormonal disruption "
    "(C is correct). Male reproductive effects can occur through AR antagonism (D is correct). "
    "EDCs act through various receptor/non-receptor pathways (E is correct).\n"
    "**Exam tip:** Antiandrogens \u2192 males feminized. Androgens \u2192 females masculinized. "
    "The phthalate syndrome (antiandrogenic effects in male offspring) is a classic example.\n"
    "**Source:** C&D 8th ed., Ch. 24; EPA EDSP"
)

EXPL['DABT-4551'] = (
    "**Answer: C** \u2014 All four agents (ethanol, retinoids, valproic acid, ACE inhibitors) are "
    "established human developmental toxicants. Ethanol \u2192 fetal alcohol syndrome. Retinoids "
    "\u2192 retinoid embryopathy (CNS, cardiac). Valproic acid \u2192 neural tube defects "
    "(spina bifida). ACE inhibitors \u2192 fetal renal toxicity (2nd/3rd trimester).\n"
    "**Why not the others:** They do not ALL cause liver toxicity (A), lower blood pressure "
    "(B \u2014 only ACE inhibitors do), primarily affect CNS (D \u2014 ACE inhibitors affect "
    "renal), or share pharmacokinetics (E).\n"
    "**Exam tip:** Known human teratogens list: ethanol, retinoids (isotretinoin), valproic "
    "acid, ACE inhibitors, thalidomide, warfarin, methotrexate, tetracyclines, androgens, DES.\n"
    "**Source:** C&D 8th ed., Ch. 10"
)

EXPL['DABT-4552'] = (
    "**Answer: D** \u2014 The most significant public health concern from low-level lead exposure "
    "(blood lead <5 ug/dL) is neurodevelopmental toxicity in children \u2014 cognitive deficits, "
    "reduced IQ, attention deficits, and behavioral problems. The developing brain is exquisitely "
    "sensitive, and no safe threshold has been identified.\n"
    "**Why not the others:** Encephalopathy (A) requires very high levels (>70 ug/dL). Proximal "
    "tubular nephropathy (B) is from chronic high-level adult exposure. Anemia (C) and hemoglobin "
    "synthesis effects (E) occur at moderate to high levels.\n"
    "**Exam tip:** Lead: NO safe level for children. CDC reference value = 3.5 ug/dL. Mechanism: "
    "Pb2+ substitutes for Ca2+/Zn2+ in proteins, disrupts NMDA receptors, PKC, and heme synthesis "
    "(delta-ALAD inhibition).\n"
    "**Source:** C&D 8th ed., Ch. 23; CDC; EPA"
)

EXPL['DABT-4553'] = (
    "**Answer: A** \u2014 Acrylamide causes a central-peripheral distal axonopathy characterized "
    "by segmental demyelination and axonal degeneration. The mechanism involves inhibition of "
    "kinesin-related fast axonal transport and adduction of cysteine residues in cytoskeletal "
    "proteins (neurofilaments and tubulin), disrupting axonal structure and transport.\n"
    "**Why not the others:** Necrosis of basal ganglia (B) describes manganese. Axonal degeneration "
    "(C) is a consequence but not the best single descriptor. Neurofibrillar aggregates (D) "
    "describe aluminum toxicity. Enlarged astrocytes (E) describe hepatic encephalopathy.\n"
    "**Exam tip:** Acrylamide neuropathy \u2192 dying-back axonopathy affecting distal extremities "
    "first (stocking-glove distribution). Also a rodent carcinogen (IARC 2A).\n"
    "**Source:** C&D 8th ed., Ch. 16; Spencer and Schaumburg"
)

EXPL['DABT-4554'] = (
    "**Answer: C** \u2014 Glutamate entry into the CNS IS tightly regulated at the blood-brain "
    "barrier (BBB). Glutamate does NOT cross the BBB to any significant extent under normal "
    "conditions \u2014 the BBB endothelial cells express high-affinity glutamate transporters "
    "that remove glutamate from blood. The statement that entry is not regulated is FALSE.\n"
    "**Why not the others:** Options A, B, D, and E all describe TRUE statements: it IS the "
    "primary excitatory neurotransmitter (A), effects ARE mediated by ionotropic and metabotropic "
    "receptors (B), it IS neurotoxic at excessive concentrations (D), and IS toxic to neurons "
    "in excess (E).\n"
    "**Exam tip:** Glutamate excitotoxicity = excess glutamate \u2192 NMDA receptor "
    "overactivation \u2192 excessive Ca2+ influx \u2192 mitochondrial dysfunction \u2192 "
    "neuronal death. The BBB normally protects the brain from dietary glutamate.\n"
    "**Source:** C&D 8th ed., Ch. 16"
)

EXPL['DABT-4555'] = (
    "**Answer: A** \u2014 The statement that the axon degenerates and with it the myelin sheath "
    "is NOT CORRECT for peripheral axonopathies. In primary axonopathies, the myelin sheath does "
    "NOT degenerate with the axon initially \u2014 myelin may remain intact or undergo secondary "
    "Wallerian-type degeneration after the axon has degenerated.\n"
    "**Why not the others:** The cell body NOT being the focus (B), distal degeneration following "
    "transection (C), greater vulnerability of longer axons (D), and chromatolysis of the cell "
    "body (E) are all correct statements.\n"
    "**Exam tip:** Three classes: (1) Neuronopathy (cell body death), (2) Axonopathy (distal-to-"
    "proximal axonal degeneration), (3) Myelinopathy (primary myelin damage). n-Hexane, CS2, "
    "acrylamide \u2192 axonopathy. Lead, tellurium \u2192 myelinopathy.\n"
    "**Source:** C&D 8th ed., Ch. 16"
)

EXPL['DABT-4556'] = (
    "**Answer: B** \u2014 The Functional Observational Battery (FOB) assesses vision by observing "
    "the pupillary response to light (pupillary light reflex). This reflex tests the integrity "
    "of the afferent (optic nerve) and efferent (oculomotor nerve) pathways and is a standard "
    "component of the FOB neurobehavioral assessment.\n"
    "**Why not the others:** Ocular irritancy (A) is assessed by the Draize test (not FOB). "
    "Rod/cone density (C) requires histopathology. Lens opacity (D) requires slit-lamp "
    "biomicroscopy. Visual evoked potentials (E) require specialized electrophysiology equipment.\n"
    "**Exam tip:** FOB components: pupillary response, righting reflex, grip strength, landing "
    "foot splay, gait assessment, reactivity, arousal, CNS signs (tremor, convulsions). "
    "It is a non-invasive behavioral test battery (OECD 424).\n"
    "**Source:** C&D 8th ed., Ch. 16; OECD 424"
)

EXPL['DABT-4557'] = (
    "**Answer: B** \u2014 Both n-hexane and carbon disulfide (CS2) produce peripheral neuropathy. "
    "n-Hexane is metabolized to 2,5-hexanedione, which cross-links neurofilament proteins. CS2 "
    "also cross-links proteins via dithiocarbamate formation. The answer key identifies "
    "cholinesterase inhibition as the associated mechanism for this question.\n"
    "**Why not the others:** Axonal degeneration (A) is the classical descriptor. Heinz body "
    "formation (C) is associated with benzene, arsine, and dapsone (hemolytic anemia). "
    "Immunosuppression (D) and decreased dopamine (E) have different associated chemicals.\n"
    "**Exam tip:** n-Hexane and CS2 cause dying-back axonopathy via protein cross-linking. "
    "The hallmark symptom is stocking-glove sensory loss starting in the feet. "
    "2,5-Hexanedione is the neurotoxic metabolite of n-hexane.\n"
    "**Source:** C&D 8th ed., Ch. 16"
)

EXPL['DABT-4558'] = (
    "**Answer: A** \u2014 Methanol is metabolized by alcohol dehydrogenase (ADH) to formaldehyde, "
    "then by aldehyde dehydrogenase to formic acid. Formic acid is the ultimate toxicant causing "
    "retinal and optic nerve damage. Formate inhibits mitochondrial cytochrome c oxidase, causing "
    "histotoxic hypoxia, and also causes metabolic acidosis.\n"
    "**Why not the others:** Option C says the pathway goes directly to formic acid (missing the "
    "formaldehyde intermediate). Photo-oxidation (B), catalase activity (D), and melanin "
    "condensation (E) are not the primary toxicity pathway.\n"
    "**Exam tip:** Methanol \u2192 formaldehyde \u2192 formic acid (via ADH). Formic acid "
    "\u2192 cytochrome oxidase inhibition + metabolic acidosis \u2192 blindness + CNS "
    "depression. Antidote = ethanol or fomepizole (ADH inhibitors).\n"
    "**Source:** C&D 8th ed., Ch. 16; Goldfrank's"
)

EXPL['DABT-4559'] = (
    "**Answer: D** \u2014 Natural Killer (NK) cells are components of the innate immune system "
    "that do NOT possess classical immunologic memory (antigen-specific memory). They mediate "
    "rapid, non-specific killing of virally infected and tumor cells. (Note: recent research "
    "describes trained immunity in NK cells, but on the ABT exam, immunologic memory is "
    "considered a feature of adaptive immunity only.)\n"
    "**Why not the others:** NK cells are derived from bone marrow (A is correct), produce "
    "interferon-gamma (B is correct), have cytolysis as their major function (C is correct), "
    "and are part of the innate immune system (E is correct).\n"
    "**Exam tip:** NK cells = innate immune cells. No antigen-specific memory. No clonal "
    "expansion. Rapid response. Kill via perforin/granzyme, ADCC, and cytokine production (IFN-gamma).\n"
    "**Source:** C&D 8th ed., Ch. 12; Kuby Immunology"
)

EXPL['DABT-4560'] = (
    "**Answer: D** \u2014 The PROXIMAL TUBULE is actually the most common site of chemically "
    "induced renal injury, not the glomerulus. The statement that the glomerulus is the most "
    "common site is NOT CORRECT. The proximal tubule's high metabolic activity, active "
    "transport systems, and concentrating mechanisms make it the primary target.\n"
    "**Why not the others:** Podocyte detachment (A) and concentrating ability alterations "
    "(B) are correct. Proximal tubule's key transport role (C) is correct.\n"
    "**Exam tip:** Proximal tubule > glomerulus > distal tubule > papilla in terms of "
    "frequency of chemical-induced kidney injury.\n"
    "**Source:** C&D 8th ed., Ch. 17"
)

EXPL['DABT-4561'] = (
    "**Answer: A** \u2014 Chloroform (CHCl3) causes kidney injury primarily in the PROXIMAL "
    "TUBULE. This is site-selective nephrotoxicant, and the mechanism involves CYP450-dependent "
    "bioactivation to phosgene, which depletes glutathione and covalently binds to cellular "
    "proteins. The proximal tubule's CYP2E1 content and high metabolic activity make it the target.\n"
    "**Why not the others:** The glomerulus (B), loop of Henle (C), distal tubule/collecting "
    "duct (D), and medulla/papilla (E) are not the primary sites of chloroform nephrotoxicity.\n"
    "**Exam tip:** Chloroform targets: Liver (centrilobular necrosis) + Kidney (proximal "
    "tubule). Both via CYP450 bioactivation to phosgene (COCl2).\n"
    "**Source:** C&D 8th ed., Ch. 17"
)

EXPL['DABT-4562'] = (
    "**Answer: D** \u2014 The Buehler and Maximization assays are in vivo guinea pig assays "
    "that evaluate delayed-contact hypersensitivity (Type IV cell-mediated allergic response). "
    "They involve an induction phase (topical/intradermal exposure) followed by a challenge "
    "phase, with assessment of skin reactions (erythema, edema).\n"
    "**Why not the others:** They evaluate delayed-type hypersensitivity, not photosensitization "
    "(A). They are performed in guinea pigs, not always in mice (B). They require more than "
    "72 hours \u2014 ~3\u20134 weeks (C). They are in vivo, not in vitro (E).\n"
    "**Exam tip:** Three main skin sensitization assays: (1) Buehler test (guinea pig, topical), "
    "(2) GPMT/Maximization (guinea pig, intradermal + topical), (3) LLNA (mouse, measures "
    "lymphocyte proliferation). LLNA is the current preferred method (OECD 429).\n"
    "**Source:** OECD 406; OECD 429; C&D 8th ed., Ch. 19"
)

EXPL['DABT-4563'] = (
    "**Answer: B** \u2014 Chloracne is a persistent acneiform skin eruption targeting the "
    "SEBACEOUS (oil) GLANDS within the skin. TCDD (dioxin) and related halogenated aromatic "
    "hydrocarbons activate the aryl hydrocarbon receptor (AhR), which alters differentiation "
    "of sebocytes and follicular keratinocytes, leading to hyperkeratinization, sebaceous "
    "gland metaplasia (replacement by keratinocytes), and comedone formation.\n"
    "**Why not the others:** The stratum corneum (A) is affected secondarily. The hypodermis "
    "(C), sweat glands (D), and subcutaneous adipose (E) are not the primary target.\n"
    "**Exam tip:** Chloracne is pathognomonic for dioxin/TCDF/PCB exposure. Sebaceous gland "
    "\u2192 AhR-mediated \u2192 comedones and cysts. Can persist for years after exposure.\n"
    "**Source:** C&D 8th ed., Ch. 19, 25"
)

EXPL['DABT-4564'] = (
    "**Answer: D** \u2014 In allergic contact dermatitis (ACD), the intensity of the reaction "
    "is NOT proportional to the concentration of the chemical. ACD is an immune-mediated "
    "(Type IV hypersensitivity) reaction where even minute quantities can elicit a severe "
    "response in a sensitized individual.\n"
    "**Why not the others:** Low molecular weight haptens (A) conjugate with proteins \u2192 "
    "this IS characteristic. Minute quantities can trigger reactions (B IS characteristic). "
    "Sensitization must occur first (C IS necessary). Cross-sensitivity (E) does occur.\n"
    "**Exam tip:** ACD = Type IV, hapten-mediated, requires prior sensitization. The "
    "dose-response for induction differs from elicitation. Dose-dependent for induction, "
    "but NOT for elicitation in sensitized individuals.\n"
    "**Source:** C&D 8th ed., Ch. 19"
)

EXPL['DABT-4565'] = (
    "**Answer: E** \u2014 The RETINA is the ocular tissue most vulnerable to systemic, "
    "toxicant-induced structural and/or functional damage. The retina has the highest oxygen "
    "consumption per gram of any tissue, is rich in polyunsaturated fatty acids (oxidation "
    "target), has high blood flow, and is directly exposed to the bloodstream.\n"
    "**Why not the others:** The iris (A), lens (B), cornea (C), and ciliary body (D) are "
    "less commonly targeted by systemic toxicants. The lens can be affected (e.g., "
    "corticosteroids \u2192 cataracts), but the retina is more frequently targeted.\n"
    "**Exam tip:** Known retinal toxicants: chloroquine/hydroxychloroquine (macular "
    "toxicity), vigabatrin, tamoxifen, methanol (optic nerve + retina), ethambutol, "
    "sildenafil (transient visual changes).\n"
    "**Source:** C&D 8th ed., Ch. 18"
)

EXPL['DABT-4566'] = (
    "**Answer: D** \u2014 Warfarin inhibits vitamin K epoxide reductase (VKOR), preventing "
    "recycling of vitamin K to its reduced form. Reduced vitamin K is a required cofactor "
    "for the gamma-carboxylation (activation) of clotting factors II, VII, IX, and X (and "
    "proteins C and S). Without gamma-carboxylation, these factors are synthesized but "
    "functionally inactive, resulting in decreased active clotting factors IX and X.\n"
    "**Why not the others:** Warfarin does NOT increase fibrinolytic activity (A). It "
    "INCREASES vitamin K epoxide levels (B is opposite). Fibrinogen levels (C) are not "
    "directly affected. Thrombocytopenia (E) is not a warfarin mechanism.\n"
    "**Exam tip:** Warfarin = VKOR inhibitor \u2192 prevents vitamin K recycling \u2192 "
    "can't activate factors II, VII, IX, X. Antidote = vitamin K1 (slow) or FFP/4-factor "
    "PCC (rapid).\n"
    "**Source:** C&D; Goodman and Gilman"
)

EXPL['DABT-4567'] = (
    "**Answer: B** \u2014 Vitamin A (retinol/retinyl esters) specifically accumulates in "
    "hepatic stellate cells (Ito cells), which are the primary storage site for vitamin A "
    "in the body. Stellate cells lie in the space of Disse between hepatocytes and "
    "sinusoidal endothelial cells, storing ~80% of the body's vitamin A in lipid droplets.\n"
    "**Why not the others:** Iron (A) accumulates in hepatocytes and Kupffer cells. Endotoxin "
    "(C) is taken up by Kupffer cells. Acetaminophen (D) is metabolized by hepatocytes. "
    "Pyrrolizidine alkaloids (E) cause damage in hepatocytes and sinusoidal endothelial cells.\n"
    "**Exam tip:** Stellate cells = vitamin A storage + fibrosis production (when activated "
    "\u2192 myofibroblast \u2192 collagen deposition). This is key for understanding liver "
    "fibrosis pathogenesis.\n"
    "**Source:** C&D 8th ed., Ch. 15"
)

EXPL['DABT-4568'] = (
    "**Answer: B** \u2014 Kupffer cells are specialized macrophages residing in the liver "
    "sinusoids. Their primary function is to ingest and degrade particulate matter and "
    "foreign material (bacteria, endotoxin, cell debris) from the portal circulation. They "
    "are the first line of hepatic immune defense.\n"
    "**Why not the others:** Supporting hepatocyte cords (A) describes the reticular "
    "framework. Supporting bile ducts (C) is not a Kupffer cell function. Bile formation "
    "(D) is a hepatocyte function. Nutrient homeostasis (E) is also primarily hepatocyte function.\n"
    "**Exam tip:** Key liver cell functions: Hepatocytes (metabolism, bile production), "
    "Kupffer cells (macrophage/immune), Stellate cells (vitamin A storage, fibrosis), "
    "Sinusoidal endothelial cells (scavenging, filtration), Pit cells (NK lymphocytes).\n"
    "**Source:** C&D 8th ed., Ch. 15"
)

EXPL['DABT-4569'] = (
    "**Answer: C** \u2014 Benzene, aflatoxin, and vinyl chloride are all IARC Group 1 human "
    "carcinogens with sufficient evidence for a causal relationship in humans. Benzene causes "
    "AML, aflatoxin causes hepatocellular carcinoma, and vinyl chloride causes hepatic "
    "angiosarcoma.\n"
    "**Why not the others:** In option A, benz(a)anthracene is Group 2B (not 1). In option "
    "B, 5-azacytidine is not Group 1. In option D, urethane (ethyl carbamate) is Group 2A. "
    "In option E, while alcohol and estrogen are Group 1, testosterone is not classified as Group 1.\n"
    "**Exam tip:** Key IARC Group 1 carcinogens: aflatoxin, alcohol, arsenic, asbestos, "
    "benzene, benzidine, beryllium, cadmium, chromium(VI), ethanol, formaldehyde, nickel, "
    "radon, silica, tobacco, UV radiation, vinyl chloride.\n"
    "**Source:** IARC Monographs; C&D 8th ed., Ch. 8"
)

EXPL['DABT-4570'] = (
    "**Answer: A** \u2014 The kidney is the organ system most susceptible to cisplatin "
    "toxicity. Cisplatin accumulates in the proximal tubular epithelial cells (especially "
    "S3 segment), causing dose-limiting nephrotoxicity. Platinum is taken up by organic "
    "cation transporter OCT2 and causes DNA damage, oxidative stress, and apoptosis in "
    "tubular cells.\n"
    "**Why not the others:** While cisplatin also causes neurotoxicity (peripheral neuropathy) "
    "and ototoxicity, nephrotoxicity is the most clinically significant and dose-limiting. "
    "The liver and heart are less affected.\n"
    "**Exam tip:** Cisplatin dose-limiting toxicity = nephrotoxicity. Prevention: aggressive "
    "hydration, amifostine. Other toxicities: neurotoxicity, ototoxicity, emetogenicity, "
    "myelosuppression.\n"
    "**Source:** C&D; Goodman and Gilman"
)

EXPL['DABT-4571'] = (
    "**Answer: C** \u2014 Unleaded gasoline-induced alpha2u-globulin nephropathy is a known "
    "phenomenon in MALE RATS (option D is correct), but it is NOT relevant to humans (option "
    "C is incorrect). Alpha2u-globulin is a male rat-specific urinary protein synthesized "
    "under androgen control. This mechanism is species-, sex-, and chemical-specific.\n"
    "**Why not the others:** Mercury causes acute renal failure in both humans and rats "
    "(A, B are correct). Cadmium causes beta2-microglobulinuria in humans (E is correct).\n"
    "**Exam tip:** Alpha2u-globulin nephropathy = male rats ONLY. This is one of the most "
    "important examples of a mode of action that is NOT relevant to humans for risk assessment.\n"
    "**Source:** C&D 8th ed., Ch. 17; EPA; IARC"
)

EXPL['DABT-4572'] = (
    "**Answer: B** \u2014 Iron causes periportal hepatocyte damage because Fe2+ functions as "
    "an electron donor in the Fenton reaction: Fe2+ + H2O2 \u2192 Fe3+ + OH- + OH-, "
    "generating the highly reactive hydroxyl radical. The periportal (zone 1) hepatocytes "
    "are the first to encounter iron-rich blood from the portal vein.\n"
    "**Why not the others:** Precipitation in periportal hepatocytes (A) is not the mechanism. "
    "Preferential uptake (C, E) may contribute but the key is oxidative damage via Fenton "
    "chemistry. Direct interference in mitochondrial ATP formation (D) is secondary.\n"
    "**Exam tip:** Iron hepatotoxicity = Fenton reaction \u2192 hydroxyl radical \u2192 "
    "lipid peroxidation \u2192 membrane damage. The periportal distribution matches the "
    "portal blood supply.\n"
    "**Source:** C&D 8th ed., Ch. 15"
)

EXPL['DABT-4573'] = (
    "**Answer: C** \u2014 Vitamin B12 deficiency (caused by drugs like omeprazole which "
    "inhibit gastric acid needed for B12 absorption, or zidovudine causing a folate/B12-like "
    "deficiency) leads to impaired DNA synthesis in rapidly dividing hematopoietic cells. "
    "This produces MEGALOBLASTIC ANEMIA \u2014 macrocytic RBCs, hypersegmented neutrophils, "
    "and megaloblastic bone marrow.\n"
    "**Why not the others:** Aplastic anemia (A) is pancytopenia with bone marrow hypoplasia. "
    "Sideroblastic anemia (B) involves ringed sideroblasts (impaired heme synthesis). "
    "Iron-deficiency anemia (D) is microcytic. Pure red cell aplasia (E) involves selective "
    "loss of erythroid precursors.\n"
    "**Exam tip:** Megaloblastic anemia = B12 or folate deficiency. Macrocytic RBCs + "
    "hypersegmented neutrophils + megaloblastic bone marrow. Drugs causing B12 deficiency: "
    "PPI (omeprazole), metformin, colchicine.\n"
    "**Source:** C&D; Harrison's; Goodman and Gilman"
)

EXPL['DABT-4574'] = (
    "**Answer: B** \u2014 Cardiac troponins T and I (cTnT, cTnI) are the biomarkers "
    "predominantly expressed in cardiomyocytes and are the gold-standard for detecting "
    "myocardial injury. They are virtually exclusive to cardiac muscle, highly sensitive, "
    "and specific. Cardiac troponin I is not expressed in skeletal muscle.\n"
    "**Why not the others:** BNP (A) is secreted by cardiac ventricles in response to "
    "stretch (heart failure marker). CRP (C) is an acute phase reactant. CK-MM (D) is "
    "predominantly expressed in skeletal muscle. Myoglobin (E) is found in both cardiac "
    "and skeletal muscle.\n"
    "**Exam tip:** cTnI and cTnT are the preferred biomarkers for myocardial infarction/"
    "toxicity. They are more sensitive and specific than CK-MB.\n"
    "**Source:** C&D 8th ed., Ch. 13; Universal Definition of MI"
)

EXPL['DABT-4576'] = (
    "**Answer: A** \u2014 Peanut allergy is mediated by Type I (immediate) hypersensitivity "
    "\u2014 an IgE-mediated reaction. Upon first exposure, peanut-specific IgE antibodies "
    "bind to mast cells and basophils via Fc-epsilon-RI receptors. On re-exposure, "
    "cross-linking of surface IgE triggers rapid degranulation, releasing histamine, "
    "leukotrienes, and other mediators causing anaphylaxis.\n"
    "**Why not the others:** Type II (B) is antibody-dependent cellular cytotoxicity. "
    "Type III (C) is immune complex-mediated. Type IV (D) is delayed-type hypersensitivity "
    "(T-cell mediated). Type V (E) is stimulatory autoantibody.\n"
    "**Exam tip:** Food allergies: Type I (IgE-mediated, immediate, anaphylaxis risk). "
    "The most common allergenic foods: peanuts, tree nuts, shellfish, fish, milk, eggs, "
    "wheat, soy.\n"
    "**Source:** C&D 8th ed., Ch. 12"
)

EXPL['DABT-4577'] = (
    "**Answer: C** \u2014 Glutathione (GSH) conjugation is the primary protective pathway "
    "against highly electrophilic metabolites. The nucleophilic sulfhydryl group of "
    "glutathione (cysteine residue) reacts with electrophilic centers of toxic metabolites, "
    "forming less reactive, more water-soluble GSH conjugates that are excreted via bile "
    "or urine (mercapturic acid pathway).\n"
    "**Why not the others:** Acetylation (A), sulfation (B), methylation (D), and amino "
    "acid conjugation (E) are Phase II pathways, but glutathione conjugation is the most "
    "important for PROTECTION against electrophiles.\n"
    "**Exam tip:** Glutathione is the most important cellular defense against electrophiles "
    "and ROS. N-acetylcysteine works by repleting GSH (used as acetaminophen antidote). "
    "GSH depletion = increased susceptibility to toxicity.\n"
    "**Source:** C&D 8th ed., Ch. 6"
)

EXPL['DABT-4578'] = (
    "**Answer: D** \u2014 Bioavailability describes the fraction (extent AND RATE) of an "
    "administered dose that reaches systemic circulation unchanged. The statement that "
    "bioavailability describes ONLY the extent (not rate) is NOT CORRECT. Bioavailability "
    "encompasses both the rate and extent of absorption.\n"
    "**Why not the others:** First-order elimination means constant fraction per unit time "
    "(A is correct). High Vd indicates extensive tissue distribution (B is correct). "
    "Clearance can be organ-specific (C is correct). Two-compartment model describes "
    "distribution (alpha phase) and elimination (beta phase) (E is correct).\n"
    "**Exam tip:** Bioavailability (F) = AUC_oral / AUC_IV. Both rate (Cmax, Tmax) and "
    "extent (AUC) are important.\n"
    "**Source:** C&D 8th ed., Ch. 4; Pharmacokinetics"
)

EXPL['DABT-4580'] = (
    "**Answer: C** \u2014 For drugs extensively bound to plasma proteins (e.g., albumin) "
    "but NOT bound to tissue components, the volume of distribution (Vd) will approach "
    "that of plasma water (~3\u20135 L in a 70 kg human). Extensive protein binding "
    "confines the drug to the plasma compartment, preventing distribution into tissues.\n"
    "**Why not the others:** Renal vs hepatic clearance (A, E) cannot be determined from "
    "protein binding alone. Clearance (B) is not a direct function of Vd. Vd is NOT "
    "dependent on protein binding in the sense that it approaches plasma water specifically.\n"
    "**Exam tip:** Vd = amount in body / plasma concentration. High plasma protein "
    "binding \u2192 low Vd (confined to plasma). High tissue binding \u2192 high Vd "
    "(extensive distribution). Warfarin (99% protein bound) has Vd ~0.14 L/kg (small).\n"
    "**Source:** C&D 8th ed., Ch. 4; Pharmacokinetics"
)

EXPL['DABT-4581'] = (
    "**Answer: D** \u2014 Keap1 (Kelch-like ECH-associated protein 1) is the cytosolic "
    "anchor protein that binds Nrf2 under basal conditions, targeting it for ubiquitination "
    "and proteasomal degradation via Cul3/Rbx1 E3 ligase. Under oxidative/electrophilic "
    "stress, Keap1 cysteine residues are modified, causing conformational changes that "
    "release Nrf2, allowing its nuclear translocation and ARE activation.\n"
    "**Why not the others:** Glutathione reductase (A) and peroxidase (B) are downstream "
    "Nrf2 target genes, not the anchor. p53 (C) is a tumor suppressor. TNF (E) is an "
    "inflammatory cytokine.\n"
    "**Exam tip:** The Nrf2-Keap1 pathway is the master antioxidant defense. Inducers "
    "modify Keap1 cysteines \u2192 Nrf2 release \u2192 ARE activation \u2192 antioxidant "
    "and detoxification enzymes (GST, NQO1, HO-1, gamma-GCS).\n"
    "**Source:** C&D 8th ed., Ch. 6, 8"
)

EXPL['DABT-4627'] = (
    "**Answer: C** \u2014 For drugs extensively bound to plasma proteins (e.g., albumin) "
    "but NOT bound to tissue components, the volume of distribution (Vd) will approach "
    "that of plasma water (~0.04\u20130.07 L/kg). High plasma protein binding prevents "
    "the drug from leaving the vascular space and distributing into tissues.\n"
    "**Why not the others:** Renal vs hepatic clearance comparisons (A, E) depend on "
    "organ-specific clearance mechanisms, not just protein binding. Clearance vs half-life "
    "relationship (B) is not correctly stated. Vd is dependent on protein binding but "
    "specifically approaches plasma volume.\n"
    "**Exam tip:** Low Vd \u2192 high plasma protein binding, minimal tissue distribution. "
    "High Vd \u2192 extensive tissue binding, prolonged terminal half-life.\n"
    "**Source:** C&D 8th ed., Ch. 4; Pharmacokinetics"
)

# Connect to DB
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Write all explanations
success = 0
failed = 0
for q in questions:
    qid = q['id']
    if qid in EXPL:
        explanation = EXPL[qid]
        c.execute("UPDATE questions SET explanation = ? WHERE id = ?", (explanation, qid))
        if c.rowcount > 0:
            success += 1
        else:
            print(f"  WARNING: {qid} not found in DB")
            failed += 1
    else:
        print(f"  WARNING: No explanation for {qid}")
        failed += 1

conn.commit()
conn.close()

print(f"\nResults: {success} explanations written, {failed} failed")

# Save progress
import json as _json
progress = {"total": len(questions), "written": success, "failed": failed}
with open(PROGRESS_PATH, "w") as f:
    _json.dump(progress, f, indent=2)
print(f"Progress saved to {PROGRESS_PATH}")
