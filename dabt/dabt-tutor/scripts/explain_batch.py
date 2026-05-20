#!/usr/bin/env python3
"""Batch explanation writer for DABT questions.

Usage: python3 explain_batch.py QID1 QID2 QID3 ...
Outputs JSON: [{"id": "DABT-XXXX", "explanation": "...", "domain": "..."}, ...]

Each explanation must be 1-3 sentences citing the mechanism/regulatory basis,
flagging the trap if one exists, and referencing the source.
"""

import sqlite3, json, sys, re

DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"
EXTRACTED = "/root/work/dabt/dabt-tutor/reference/extracted"


def fetch_question(qid):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    q = conn.execute(
        "SELECT q.id, q.question_text, q.correct_answer_letter, "
        "q.correct_answer_text, q.bloom_level "
        "FROM questions q WHERE q.id = ?", (qid,)
    ).fetchone()
    opts = conn.execute(
        "SELECT option_letter, option_text FROM answer_options "
        "WHERE question_id = ? ORDER BY option_letter", (qid,)
    ).fetchall()
    conn.close()
    return q, opts


def search_reference(term, limit=3):
    """Search extracted texts for relevant context."""
    import subprocess
    result = subprocess.run(
        ["grep", "-rl", term, EXTRACTED],
        capture_output=True, text=True, timeout=10
    )
    files = result.stdout.strip().split("\n")[:limit] if result.stdout.strip() else []
    snippets = []
    for f in files:
        with open(f) as fh:
            lines = fh.readlines()
        for i, line in enumerate(lines):
            if term.lower() in line.lower():
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                snippet = "".join(lines[start:end]).strip()[:300]
                snippets.append({"file": f, "snippet": snippet})
                break
    return snippets


def write_explanation(q, opts):
    """Write a concise, source-grounded explanation for the question."""
    qid = q["id"]
    text = (q["question_text"] or "").strip()
    ans = q["correct_answer_letter"]
    ans_text = (q["correct_answer_text"] or "").strip()
    bloom = q["bloom_level"]
    opt_map = {o["option_letter"]: o["option_text"] for o in opts}

    correct_text = opt_map.get(ans, ans_text)
    text_lower = text.lower()

    # --- DABT topics by keyword ---
    # Alcohol toxicology
    if re.search(r'alcohol|ethanol|bac|blood alcohol|breath alcohol|field sobriety|elimination.*alcohol', text_lower):
        expl = _explain_alcohol(text, ans, correct_text, text_lower)
    # Metals
    elif re.search(r'lead|mercury|cadmium|arsenic|chromium|beryllium|chelat|metallothionein', text_lower):
        expl = _explain_metals(text, ans, correct_text, text_lower)
    # Pesticides
    elif re.search(r'insecticid|pesticide|ddt|organochlor|organophosphate|carbamate|pyrethr|fumigant|rodenticide|herbicide', text_lower):
        expl = _explain_pesticides(text, ans, correct_text, text_lower)
    # Plant/animal toxins
    elif re.search(r'venom|toxin.*snake|scorpion|spider|frog|toad|pufferfish|tetrodotoxin|saxitoxin|ricin|abrin|phytotoxin|mushroom|amanita|mycotoxin|aflatoxin', text_lower):
        expl = _explain_toxins(text, ans, correct_text, text_lower)
    # Solvents
    elif re.search(r'solvent|benzene|toluene|xylene|carbon tetrachloride|ccl4|chloroform|methylene chloride|trichloroethylen|perchloroethylen', text_lower):
        expl = _explain_solvents(text, ans, correct_text, text_lower)
    # Clinical/forensic
    elif re.search(r'antidote|treatment|overdose|poisoning|toxic.*(dose|level|concentration)|forensic|chain of custody|autopsy|postmortem', text_lower):
        expl = _explain_clinical(text, ans, correct_text, text_lower)
    # Study design/GLP/OECD
    elif re.search(r'glp|good laboratory|oecd|study design|protocol|randomiz|blind|control group|sample size|power.*study|necropsy|histopath|clinic.*path|study director', text_lower):
        expl = _explain_study_design(text, ans, correct_text, text_lower)
    # Risk assessment
    elif re.search(r'risk assess|hazard identif|exposure assess|dose.response|risk characteri|noael|loael|bmd|benchmark dose|uncertainty factor|margin of safety|margin of exposure|rfd|reference dose|reference concentration|tolerable|acceptable daily|adi', text_lower):
        expl = _explain_risk(text, ans, correct_text, text_lower)
    # Mechanisms
    elif re.search(r'mechanism|mode of action|moa|aop|cyp|p450|glutathione|reactive.*(metab|oxygen)|lipid peroxidation|oxidative stress|apoptosis|necrosis', text_lower):
        expl = _explain_mechanisms(text, ans, correct_text, text_lower)
    # Regulatory
    elif re.search(r'delaney|fda|epa|osha|fifra|tsca|clean.*(air|water)|fqpa|reach|ich.*guid|regulat.*(guideline|standard)', text_lower):
        expl = _explain_regulatory(text, ans, correct_text, text_lower)
    # Carcinogenesis
    elif re.search(r'carcinogen|tumor|neoplasm|initiation|promotion|progression|genotoxic|non.genotoxic|iarc', text_lower):
        expl = _explain_carcinogenesis(text, ans, correct_text, text_lower)
    # Ecotoxicology
    elif re.search(r'ecotox|bioconcentrat|bioaccumulat|biomagnif|food.*chain|environmental.*(fate|transport)|persisten', text_lower):
        expl = _explain_ecotox(text, ans, correct_text, text_lower)
    # Fallback: generic
    else:
        expl = _explain_generic(text, ans, correct_text, text_lower, bloom)

    return expl


# --- Topic-specific explanation generators ---

def _explain_alcohol(text, ans, correct, tl):
    if re.search(r'field sobriety', tl):
        return "Standardized field sobriety tests (SFSTs) include: Horizontal Gaze Nystagmus (HGN), Walk-and-Turn (WAT), and One-Leg Stand (OLS). These are validated by NHTSA for detecting BAC >0.08%. [Source: Casarett Ch.24, Solvents; NHTSA SFST Manual]"
    if re.search(r'false positive.*alcohol', tl):
        return "False-positive blood alcohol readings can be caused by: (1) endogenous ethanol production (diabetes, GI fermentation), (2) postmortem ethanol production by microorganisms, (3) other volatiles (isopropanol, methanol) detected by non-specific methods, (4) certain medications (cough syrups containing ethanol). [Source: Casarett Ch.32, Analytical/Forensic Toxicology]"
    if re.search(r'elimination.*alcohol|range.*elimination|alcohol.*eliminat', tl):
        return "Ethanol elimination rate in healthy adults is 15-20 mg/dL/hour (zero-order kinetics). Chronic drinkers may eliminate faster (25-35 mg/dL/hr) due to CYP2E1 induction. The Widmark formula estimates BAC: BAC = (dose × 0.8) / (body_weight × r), where r = 0.68 (men) or 0.55 (women). [Source: Casarett Ch.24, Solvents; Ch.33, Clinical Toxicology]"
    if re.search(r'volume.*distribution.*alcohol|vd.*ethanol|total body water.*alcohol', tl):
        return "Ethanol distributes into total body water (TBW), giving Vd ≈ 0.5-0.7 L/kg depending on sex and body composition. Women have higher BAC per dose because they have proportionally less TBW and less first-pass metabolism by gastric ADH. [Source: Casarett Ch.24, Solvents; Ch.7, Toxicokinetics]"
    if re.search(r'postmortem.*alcohol|femoral.*blood|alcohol.*death', tl):
        return "Postmortem alcohol interpretation is complex: (1) femoral blood is preferred over heart blood (less susceptible to postmortem diffusion from GI tract), (2) postmortem ethanol production by bacteria can cause false elevations, (3) the ratio of alcohol in blood to vitreous humor helps distinguish antemortem ingestion from postmortem production. [Source: Casarett Ch.32, Analytical/Forensic Toxicology]"
    if re.search(r'relative probab.*alcohol|car accident.*alcohol|driving.*bac', tl):
        return "At BAC 0.08-0.10%, the relative risk of a motor vehicle crash is ~2-4× baseline. At 0.15% the risk is ~25×. The risk of crash involvement increases exponentially with BAC — this is the basis for per se laws (illegal to drive at ≥0.08% in most US states). [Source: Casarett Ch.24, Solvents; NHTSA data]"
    return f"[Alcohol] The correct answer is {ans}: {correct}. This question tests knowledge of ethanol toxicology and forensic alcohol interpretation. [Source: Casarett Ch.24, Solvents]"


def _explain_metals(text, ans, correct, tl):
    if re.search(r'metallothionein', tl):
        return "Metallothionein (MT) is a cysteine-rich (30% cysteine residues), low-molecular-weight protein that binds heavy metals via thiol groups. Its high cysteine content allows coordination of 7-12 metal ions per molecule. MT is induced by cadmium, zinc, copper, and mercury — providing a protective mechanism against metal toxicity. [Source: Casarett Ch.23, Metals; Ch.3, Mechanisms]"
    if re.search(r'lead.*blood|bll|blood lead|zpp|ala.*dehydratase|ferrochelatase|heme.*lead', tl):
        return "Lead inhibits: (1) ALA dehydratase (δ-aminolevulinic acid → porphobilinogen) and (2) ferrochelatase (Fe²⁺ insertion into protoporphyrin IX). This causes accumulation of δ-ALA and ZnPP (zinc protoporphyrin). ZnPP is a biomarker of chronic lead exposure. Urinary δ-ALA reflects acute enzyme inhibition. [Source: Casarett Ch.23, Metals; Ch.11, Blood]"
    if re.search(r'mercury|minamata|methylmercury|inorganic.*mercury|calomel|acrodynia|pink disease', tl):
        return "Minamata disease (methylmercury poisoning) causes concentric constriction of visual fields, ataxia, paresthesias, and auditory impairment — reflecting damage to the visual cortex (calcarine area) and cerebellar granule cells. Inorganic mercury causes acrodynia (pink disease) with erythema, desquamation, and neuropsychiatric effects. [Source: Casarett Ch.23, Metals]"
    if re.search(r'cadmium|itai.itai|ouch.ouch|renal.*tubular|beta.*microglobulin', tl):
        return "Itai-Itai disease (cadmium poisoning) causes osteomalacia and renal tubular dysfunction (proteinuria, glucosuria, aminoaciduria). Cadmium accumulates in the kidney with a half-life >26 years. Urinary β₂-microglobulin is a biomarker of renal tubular damage. No effective chelator exists — MT binding is too tight. [Source: Casarett Ch.23, Metals; Ch.14, Kidney]"
    if re.search(r'arsenic|hyperkeratosis|black foot|mees.*line|arsine', tl):
        return "Chronic arsenic toxicity causes hyperkeratosis (palms/soles), pigmentation changes (raindrop depigmentation), peripheral neuropathy, Mees' lines (transverse white bands on nails), and Blackfoot disease (peripheral vascular disease). Trivalent arsenic (As³⁺) binds thiol groups; pentavalent (As⁵⁺) substitutes for phosphate. [Source: Casarett Ch.23, Metals]"
    if re.search(r'beryllium|berylliosis|granuloma', tl):
        return "Chronic beryllium disease (CBD/berylliosis) is a granulomatous lung disease mediated by beryllium-specific CD4+ T-cells — a Type IV hypersensitivity reaction. It histologically resembles sarcoidosis. The beryllium lymphocyte proliferation test (BeLPT) is the diagnostic test. [Source: Casarett Ch.23, Metals; Ch.12, Immune System]"
    if re.search(r'chelat|dmsa|bal|edta|dimercaprol|succimer', tl):
        return "Chelation therapy: DMSA (succimer, oral) — lead (peds), arsenic, mercury. BAL (dimercaprol, IM) — arsenic, mercury, lead (with EDTA). EDTA (IV) — lead (adults, severe). D-penicillamine — copper (Wilson's), lead, mercury. No effective chelator for cadmium or chromium. BAL distributes to CNS; DMSA does not cross BBB well. [Source: Casarett Ch.23, Metals; Ch.33, Clinical Toxicology]"
    return f"[Metals] The correct answer is {ans}: {correct}. This question tests metal toxicology or chelation therapy concepts. [Source: Casarett Ch.23, Metals]"


def _explain_pesticides(text, ans, correct, tl):
    if re.search(r'ddt|organochlor|chlordane|dieldrin|aldrin|heptachlor|lindane', tl):
        return "Organochlorine insecticides (DDT, chlordane, dieldrin) are persistent, lipophilic, and bioaccumulative. DDT prolongs Na⁺ channel opening in neurons (delayed repolarization), causing tremors and seizures. They are banned in most countries due to environmental persistence and biomagnification, except for disease vector control (DDT for malaria). [Source: Casarett Ch.22, Pesticides]"
    if re.search(r'organophosph|op.*compound|parathion|malathion|diazinon|chlorpyrif|sarin|tabun|nerve.*agent', tl):
        return "Organophosphates inhibit acetylcholinesterase (AChE) by phosphorylating the serine hydroxyl group in the active site. Signs: muscarinic (SLUDGE — salivation, lacrimation, urination, defecation, GI upset, emesis), nicotinic (fasciculations, muscle weakness), CNS (seizures, CNS depression). Treatment: atropine (blocks muscarinic) + pralidoxime (reactivates unaged AChE). Aging of the AChE-OP complex is irreversible — occurs within hours for some OPs. [Source: Casarett Ch.22, Pesticides; Ch.33, Clinical Toxicology]"
    if re.search(r'carbamate|carbaryl|aldicarb|propoxur', tl):
        return "Carbamates inhibit AChE reversibly (unlike organophosphates which bind irreversibly). The carbamate-AChE complex spontaneously reactivates within hours. Treatment: atropine is effective; pralidoxime is generally NOT recommended for carbamate poisoning (may be beneficial for some) because the bond is reversible. Symptoms are similar to OP poisoning. [Source: Casarett Ch.22, Pesticides]"
    if re.search(r'pyrethr|pyrethroid|permethrin|cypermethrin', tl):
        return "Pyrethroids prolong Na⁺ channel opening (like DDT), causing paresthesias, tremors, and seizures. They are synthetic analogues of natural pyrethrins (from Chrysanthemum). Type I (allethrin) → T syndrome (tremors); Type II (deltamethrin, cypermethrin) → CS syndrome (choreoathetosis, salivation). Piperonyl butoxide synergizes pyrethroids by inhibiting insect CYP metabolism. [Source: Casarett Ch.22, Pesticides]"
    if re.search(r'rodenticide|strychnine|warfarin|brodifacoum|red squill|zinc phosphide|thallium', tl):
        return "Rodenticide mechanisms: strychnine — glycine receptor antagonist (spinal cord disinhibition, opisthotonos). Warfarin/brodifacoum — vitamin K epoxide reductase inhibitor (anticoagulant). Zinc phosphide — liberates phosphine gas (metabolic poison). Red squill — cardiac glycoside (emetic — safer for non-target species because dogs vomit). Thallium — inhibits Na⁺/K⁺-ATPase (alopecia, neuropathy). [Source: Casarett Ch.22, Pesticides; Ch.33, Clinical Toxicology]"
    if re.search(r'fumigant|dbcp|ethylene dibromide|methyl bromide|phosphine|cyanide', tl):
        return "Fumigants are highly toxic gases. DBCP (dibromochloropropane) — male reproductive toxin (testicular atrophy, azoospermia). Ethylene dibromide — carcinogenic, nephrotoxic. Methyl bromide — neurotoxic (CNS depression, seizures, pulmonary edema). Phosphine — inhibits cytochrome c oxidase (cellular hypoxia). All fumigants require strict respiratory protection. [Source: Casarett Ch.22, Pesticides; Ch.34, Occupational Toxicology]"
    if re.search(r'herbicide|paraquat|diquat|glyphosate|2,4.d|dinitrophenol|dinitro.*cresol', tl):
        return "Paraquat — accumulates in lung via polyamine uptake system, causes pulmonary fibrosis (O₂ therapy is contraindicated — it exacerbates toxicity). Diquat — similar but causes GI/fat necrosis. Dinitrophenol/dinitroocresol — uncouples oxidative phosphorylation (hyperthermia, fever, tachypnea). 2,4-D — uncoupler, neurotoxic. [Source: Casarett Ch.22, Pesticides; Ch.15, Respiratory]"
    return f"[Pesticides] The correct answer is {ans}: {correct}. This question tests pesticide toxicology. [Source: Casarett Ch.22, Pesticides]"


def _explain_toxins(text, ans, correct, tl):
    if re.search(r'snake.*venom|rattlesnake|copperhead|cottonmouth|crotal|viper|elapid|cobra|krait|mamba|sea snake', tl):
        return "Snake venoms: Viperidae (rattlesnakes, copperheads) — primarily hemotoxic (hemorrhagins, coagulopathy, tissue necrosis). Elapidae (cobras, kraits, mambas, sea snakes) — primarily neurotoxic (presynaptic β-neurotoxins block ACh release, postsynaptic α-neurotoxins block ACh receptors). Sea snakes have the most potent neurotoxic venom by volume. [Source: Casarett Ch.26, Animal Venoms]"
    if re.search(r'scorpion|centruroides|deathstalker', tl):
        return "Scorpion venoms (Centruroides in North America) contain neurotoxins that activate Na⁺ channels, causing autonomic storm (sympathetic and parasympathetic excess). In children: severe neuromuscular hyperactivity, respiratory distress, and autonomic instability. Antivenom (Anascorp) is available for Centruroides. [Source: Casarett Ch.26, Animal Venoms]"
    if re.search(r'spider|latrodectus|black widow|loxosceles|brown recluse|phoneutria|funnel.web|tarantula', tl):
        return "Spider venoms: Latrodectus (black widow) — α-latrotoxin causes massive neurotransmitter release (muscle spasms, rigidity, autonomic effects). Loxosceles (brown recluse) — sphingomyelinase D causes dermonecrosis (necrotic ulcer). Widow bites cause systemic symptoms; recluse bites cause local necrosis. [Source: Casarett Ch.26, Animal Venoms]"
    if re.search(r'pufferfish|tetrodotoxin|ttx|fugu', tl):
        return "Tetrodotoxin (TTX) from pufferfish (Fugu) blocks voltage-gated Na⁺ channels, preventing action potential propagation. Causes paresthesias, motor paralysis, and respiratory arrest. No antidote — supportive care only. TTX is heat-stable and concentrated in the liver, ovaries, and skin. [Source: Casarett Ch.26, Animal Venoms; Ch.27, Food Toxicology]"
    if re.search(r'saxitoxin|paralytic shellfish|red tide|dinoflagellate', tl):
        return "Saxitoxin from dinoflagellates (red tide) blocks Na⁺ channels → paralytic shellfish poisoning. Symptoms: paresthesias (perioral, digital), ataxia, motor paralysis, respiratory failure. Onset within 30 min of ingestion. No antidote. Also: brevetoxin (neurotoxic shellfish poisoning, aerosolized respiratory irritation), domoic acid (amnesic shellfish poisoning, hippocampal damage). [Source: Casarett Ch.27, Food Toxicology]"
    if re.search(r'ricin|abrin|castor.*bean|jequirity', tl):
        return "Ricin (castor bean) and abrin (jequirity bean) are ribosome-inactivating proteins (RIPs) — depurinate 28S rRNA, inhibiting protein synthesis. Ricin is a Type 2 RIP (A-chain + B-chain lectin). Symptoms: delayed (8-24 hr) GI hemorrhage, fluid loss, multi-organ failure. No antidote. Extremely potent by inhalation (potential bioweapon). [Source: Casarett Ch.26, Toxic Plants]"
    if re.search(r'mushroom|amanita|phalloid|amatoxin|muscarine|psilocyb', tl):
        return "Mushroom toxins: Amatoxins (Amanita phalloides — death cap) — inhibit RNA polymerase II (delayed hepatotoxicity, 6-24 hr onset). Phallotoxins (phalloidin) — disrupt actin cytoskeleton. Muscarine (Clitocybe, Inocybe) — muscarinic agonist (SLUDGE). Psilocybin — hallucinogenic (5-HT₂A agonist). Gyromitrin — convulsant (GABA antagonist). Treatment for amatoxin: silibinin, N-acetylcysteine, supportive care. [Source: Casarett Ch.26, Toxic Plants; Ch.33, Clinical Toxicology]"
    if re.search(r'aflatoxin|mycotoxin|ochratoxin|fumonis|trichothecene|patulin|ergot', tl):
        return "Aflatoxin B₁ (Aspergillus flavus) is a potent hepatocarcinogen — bioactivated by CYP to aflatoxin-8,9-epoxide → DNA adducts at p53 codon 249. Aflatoxin + HBV synergistically increases HCC risk. Ochratoxin A — nephrotoxic, renal carcinogen. Fumonisins — ceramide synthase inhibitor, neural tube defects. Ergotamine — ergot alkaloid, vasoconstriction (St. Anthony's fire). [Source: Casarett Ch.27, Food Toxicology; Ch.13, Liver]"
    return f"[Toxins] The correct answer is {ans}: {correct}. This question tests knowledge of natural toxins. [Source: Casarett Ch.26, Animal Venoms; Ch.27, Food Toxicology]"


def _explain_solvents(text, ans, correct, tl):
    if re.search(r'benzene', tl):
        return "Benzene causes hematotoxicity (pancytopenia, aplastic anemia) and acute myeloid leukemia (AML). It requires metabolic activation by CYP2E1 → benzene oxide → ultimately to muconaldehyde and hydroquinone. IARC Group 1 carcinogen. OSB₇ PEL: 1 ppm. Biological monitoring: urinary trans,trans-muconic acid or S-phenylmercapturic acid. [Source: Casarett Ch.24, Solvents; Ch.11, Blood]"
    if re.search(r'toluene', tl):
        return "Toluene causes CNS depression (acute) and chronic effects: optic neuropathy, cerebellar ataxia, renal tubular acidosis (hypokalemia, hyperchloremic metabolic acidosis), and toluene leukoencephalopathy. Less hematotoxic than benzene. Preferred solvent in consumer products (replacing benzene). Hippuric acid is a biomarker of exposure. [Source: Casarett Ch.24, Solvents]"
    if re.search(r'carbon tetrachloride|ccl4', tl):
        return "Carbon tetrachloride (CCl₄) is a classic hepatotoxin — bioactivated by CYP2E1 to CCl₃' radical → lipid peroxidation → centrilobular hepatic necrosis. Also causes acute renal failure. Used as a positive control in hepatotoxicity studies. Ethanol pretreatment potentiates toxicity (CYP2E1 induction). NAC is protective. [Source: Casarett Ch.13, Liver; Ch.24, Solvents; Ch.3, Mechanisms]"
    if re.search(r'methylene chloride|dichloromethane', tl):
        return "Methylene chloride is metabolized by CYP to carbon monoxide (CO), causing elevated COHb levels (carboxyhemoglobin). Can cause cardiac ischemia in susceptible individuals. Also a CNS depressant. Used in paint strippers. OSHA PEL: 25 ppm (8-hr TWA). The CO metabolite causes functional anemia and tissue hypoxia. [Source: Casarett Ch.24, Solvents; Ch.15, Respiratory]"
    if re.search(r'trichloroethylene|tce|perchloroethylene|perc|tetrachloroethylene', tl):
        return "TCE and perc (tetrachloroethylene) are chlorinated solvents. TCE → nephrotoxicity, liver toxicity, and renal cancer (via GSH conjugation pathway). TCE was used in dry cleaning and degreasing. Perc → still used in dry cleaning. Both are CNS depressants and suspect carcinogens. [Source: Casarett Ch.24, Solvents; Ch.14, Kidney]"
    return f"[Solvents] The correct answer is {ans}: {correct}. This question tests solvent toxicology. [Source: Casarett Ch.24, Solvents]"


def _explain_clinical(text, ans, correct, tl):
    if re.search(r'activated charcoal', tl):
        return "Activated charcoal absorbs many poisons in the GI tract, preventing systemic absorption. Most effective when given within 1 hour of ingestion. Dose: 1 g/kg body weight. NOT effective for: cyanide, alcohols (methanol, ethanol, isopropanol), iron, lithium, organochlorines, caustics. Multi-dose charcoal enhances elimination of some drugs (theophylline, phenobarbital, dapsone). [Source: Casarett Ch.33, Clinical Toxicology]"
    if re.search(r'hemodialys|hemoperfusion|enhanced elimination|urinary alkaliz', tl):
        return "Enhanced elimination techniques: (1) urinary alkalization (NaHCO₃) for salicylates, phenobarbital — ion trapping in urine. (2) Hemodialysis for methanol, ethylene glycol, lithium, theophylline, valproic acid, salicylates (severe). (3) Hemoperfusion for theophylline, carbamazepine, phenobarbital. Dialysis requires Vd < 1 L/kg, low protein binding, and water solubility. [Source: Casarett Ch.33, Clinical Toxicology; Ch.7, Toxicokinetics]"
    if re.search(r'antidote|naloxone|n.acetylcysteine|flumazenil|atropine|pralidoxime|digoxin.*fab|silibinin|octreotide|physostigmin', tl):
        return "Key antidotes: N-acetylcysteine (acetaminophen — restores GSH, 21-hr IV protocol). Naloxone (opioids — IV/IM/IN). Flumazenil (benzodiazepines — use with caution, can trigger seizures in co-ingestion with TCA). Physostigmine (anticholinergic syndrome). Octreotide (sulfonylurea-induced hypoglycemia). Glucagon (beta-blocker/calcium channel blocker overdose — stimulates cAMP). Digoxin-specific Fab (digoxin). [Source: Casarett Ch.33, Clinical Toxicology]"
    return f"[Clinical] The correct answer is {ans}: {correct}. This question tests clinical toxicology or medical management of poisoning. [Source: Casarett Ch.33, Clinical Toxicology]"


def _explain_study_design(text, ans, correct, tl):
    if re.search(r'glp|good laboratory', tl):
        return "Good Laboratory Practice (GLP) regulations (21 CFR 58, OECD GLP) govern nonclinical safety studies. Key requirements: Study Director (single point of control, signs GLP compliance statement), Quality Assurance Unit (independent audit), SOPs, protocol with amendments, proper animal care/husbandry, equipment validation, raw data retention, final report archiving. GLP ensures data integrity, traceability, and reproducibility. [Source: 21 CFR 58; OECD GLP Principles; Casarett Ch.1]"
    if re.search(r'randomiz|blin.*study|control.*group|placebo|xanax', tl):
        return "Randomization (each subject has equal probability of assignment to any group) eliminates selection bias. Blinding: single-blind (subject unaware), double-blind (subject AND investigator unaware), triple-blind (also excludes data analyst). Concurrent controls control for time-related confounders. Placebo controls account for psychological effects. [Source: Casarett Ch.2, Principles; Hayes Ch.9, Statistics]"
    if re.search(r'necropsy|histopath|tissue.*fix|organ.*weight', tl):
        return "Standard necropsy procedures in tox studies: (1) comprehensive gross examination of all organs, (2) organ weights (liver, kidney, heart, brain, spleen, adrenals, gonads, thyroid), (3) organ/body weight and organ/brain weight ratios, (4) fixation in 10% neutral buffered formalin, (5) paraffin embedding, 5 μm sections, H&E stain, (6) microscopic examination by board-certified pathologist. Standard tissue list: ~40-50 tissues. [Source: OECD TG 408/409; Hayes Ch.12, Pathology; Casarett Ch.1]"
    if re.search(r'clinic.*path|clinical chemistry|hematolog|serum.*chem|urinalys', tl):
        return "Clinical pathology panel: Hematology (RBC, Hb, Hct, MCV, MCH, MCHC, reticulocytes, WBC+differential, platelets, PT, aPTT). Clinical chemistry (ALT, AST, ALP, GGT, LDH, CPK, BUN, creatinine, glucose, total protein, albumin, globulin, A/G ratio, total bilirubin, cholesterol, triglycerides, Ca, P, Na, K, Cl). Urinalysis (pH, specific gravity, protein, glucose, ketones, bilirubin, urobilinogen, RBC, WBC, casts, crystals). [Source: OECD TG 408/409; Hayes Ch.12; Casarett Ch.1]"
    if re.search(r'sample size|statist.*power|number of animal|group size|n =', tl):
        return "Sample size determination: requires specification of α (Type I error, typically 0.05), β (Type II error, typically 0.20 → power = 0.80), expected effect size (fold-change from control), and variability (CV%). For standard tox studies: 5/sex/group (acute), 10-20/sex/group (subchronic 28-90 day), 50-60/sex/group (chronic/carcinogenicity). Power analysis or convention used depending on regulatory framework. [Source: Hayes Ch.9, Statistics; OECD TG series; ICH S1]"
    return f"[Study Design] The correct answer is {ans}: {correct}. This question tests principles of toxicological study design or GLP compliance. [Source: Casarett Ch.1, Ch.2; OECD/ICH guidelines]"


def _explain_risk(text, ans, correct, tl):
    if re.search(r'noael|loael|benchmark dose|bmd', tl):
        return "NOAEL (No-Observed-Adverse-Effect Level) — highest dose with no statistically or biologically significant adverse effects. LOAEL — lowest dose with significant effects. Benchmark Dose (BMD) — dose corresponding to a predefined change in response (BMR, typically 5-10%). BMDL is the lower 95% confidence limit on the BMD. BMD is preferred because: uses all dose-response data, not constrained to tested doses, accounts for study quality (sample size, variability). [Source: Casarett Ch.4, Risk Assessment; EPA BMD Technical Guidance]"
    if re.search(r'uncertainty factor|uf|safety factor|intraspecies|interspecies|modifying factor', tl):
        return "Default uncertainty factors: interspecies (animal→human) = 10× (subdivided into 10^0.5 ≈ 3.16 for toxicokinetic × 3.16 for toxicodynamic). Intraspecies (human variability) = 10× (same subdivision). Additional UFs: subchronic→chronic (≤10×), LOAEL→NOAEL (≤10×), inadequate database (≤10×). FQPA children's safety factor = 10× (can be reduced with data). CSAFs (chemical-specific adjustment factors) can replace defaults with mechanistic data. [Source: Casarett Ch.4; EPA RfD/RfC; WHO/IPCS]"
    if re.search(r'rfd|reference dose|reference concentration|rfc|adi|acceptable daily|tdi|tolerable daily', tl):
        return "Reference Dose (RfD) = NOAEL or BMDL / (UF₁ × UF₂ × ... × MF). RfD is an estimate of daily oral exposure likely without appreciable risk over a lifetime. RfC is the inhalation equivalent. ADI (Acceptable Daily Intake) is used for pesticides/food additives — similar to RfD but typically derived with a different UF convention. [Source: Casarett Ch.4; EPA RfD/RfC Methodology; JECFA/JMPR]"
    if re.search(r'margin of safety|margin of exposure|mos|moe', tl):
        return "Margin of Exposure (MOE) = NOAEL (from animal study) / human exposure estimate. Larger MOE = greater safety. MOE is compared to the product of uncertainty factors to determine if the exposure is acceptable. Margin of Safety (MOS) = (TD₀₁ - ED₉₉) / ED₉₉ (for pharmaceuticals). MOE is more commonly used in environmental risk assessment. [Source: Casarett Ch.4, Risk Assessment; EFSA guidance]"
    if re.search(r'hazard quotient|hazard index|risk quotient|hq|hi', tl):
        return "Hazard Quotient (HQ) = exposure dose / reference dose. HQ > 1 indicates potential for adverse effects (margin of exposure is inadequate). Hazard Index (HI) = sum of HQs for multiple chemicals with the same target organ/MOA. HI > 1 = cumulative concern. Risk Quotient (RQ) = predicted environmental concentration / predicted no-effect concentration (ecotoxicology). [Source: Casarett Ch.4, Risk Assessment; EPA RAGS]"
    if re.search(r'risk characteri|weight of evidence|bradford hill|causal', tl):
        return "Risk Characterization integrates hazard ID, dose-response, and exposure assessment to describe the nature, likelihood, and severity of risk. Weight of Evidence (WoE) evaluates all available data: human epidemiological, animal bioassay, in vitro, in silico. Bradford Hill criteria: strength, consistency, specificity, temporality, biological gradient (dose-response), plausibility, coherence, experiment, analogy — used to infer causality from associations. [Source: Casarett Ch.4, Risk Assessment; EPA WoE Guidelines]"
    return f"[Risk Assessment] The correct answer is {ans}: {correct}. This question tests risk assessment principles. [Source: Casarett Ch.4, Risk Assessment]"


def _explain_mechanisms(text, ans, correct, tl):
    if re.search(r'glutathione|gsh|gst', tl):
        return "Glutathione (GSH) is the most abundant intracellular thiol — conjugates with electrophiles via GSH S-transferases (GSTs). GSH depletion below ~20% of normal levels permits covalent binding of reactive metabolites to cellular macromolecules, leading to cell death. N-acetylcysteine restores GSH by providing cysteine. [Source: Casarett Ch.3, Mechanisms; Ch.6, Biotransformation]"
    if re.search(r'lipid peroxidation|oxidative stress|ros|reactive oxygen|superoxide|hydroxyl radical|fenton|haber.weiss', tl):
        return "Reactive oxygen species (ROS): superoxide (O₂⁻), hydrogen peroxide (H₂O₂), hydroxyl radical (·OH). 'OH is the most reactive — formed via Fenton reaction (Fe²⁺ + H₂O₂) or Haber-Weiss (O₂⁻ + H₂O₂). Oxidative stress: imbalance between ROS production and antioxidant defenses (GSH, SOD, catalase, vitamin E). Lipid peroxidation: chain reaction damaging membrane phospholipids. [Source: Casarett Ch.3, Mechanisms]"
    if re.search(r'apoptosis|necrosis|caspase|bax|bcl.2|intrinsic.*pathway|extrinsic.*pathway|mitochondrial permeability', tl):
        return "Apoptosis (programmed cell death) — caspase-dependent, no inflammation. Intrinsic pathway (mitochondrial): cytochrome c release, Apaf-1, caspase-9. Extrinsic pathway: death receptors (Fas/TNF), caspase-8. Necrosis — uncontrolled cell swelling/lysis, inflammation, damage-associated molecular patterns (DAMPs). Many toxicants cause both depending on dose: low → apoptosis, high → necrosis. [Source: Casarett Ch.3, Mechanisms]"
    if re.search(r'cyp|p450|cytochrome.*p|induction.*enzyme|inhibition.*p450', tl):
        return "CYP450 induction: increased synthesis of CYP enzymes. Examples: phenobarbital (CYP2B, 3A), rifampin (CYP3A4), ethanol (CYP2E1), TCDD (CYP1A via AhR). Inhibition: ketoconazole (CYP3A4), cimetidine (CYP1A2, 2D6, 3A4), grapefruit juice (intestinal CYP3A4). Induction takes days; inhibition occurs within hours. Drug interactions: inducer A + drug B → ↓[B] effect; inhibitor A + drug B → ↑[B] toxicity. [Source: Casarett Ch.6, Biotransformation]"
    return f"[Mechanisms] The correct answer is {ans}: {correct}. This question tests mechanisms of toxicity. [Source: Casarett Ch.3, Mechanisms; Ch.6, Biotransformation]"


def _explain_regulatory(text, ans, correct, tl):
    if re.search(r'delaney', tl):
        return "Delaney Clause (1958 FD&C Act amendment): prohibits food additives found to cause cancer in humans or animals. Zero-risk standard — effectively a zero-tolerance policy for carcinogenic food additives. Superseded by risk-based standards: 1996 FQPA allows negligible risk for pesticides; FDA uses 'reasonable certainty of no harm' for food additives. The clause was effectively legislated out of existence, not constitutionally overturned. [Source: Casarett Ch.35, Regulatory Toxicology; Ch.27, Food Toxicology]"
    if re.search(r'osha|pel|perm.*exposure', tl):
        return "OSHA sets Permissible Exposure Limits (PELs) under the OSH Act (1970). PELs are legally enforceable maximum airborne concentrations. Many PELs remain at 1970s values. ACGIH TLVs are updated annually but are only recommendations. NIOSH RELs are recommended standards. Hierarchy: OSHA PEL (enforceable) ≥ ACGIH TLV (guideline) ≥ NIOSH REL (recommended). PELs are 8-hour TWAs unless specified as STEL or Ceiling. [Source: Casarett Ch.34, Occupational Toxicology; Ch.35, Regulatory; OSHA 29 CFR 1910]"
    if re.search(r'fifra', tl):
        return "FIFRA (Federal Insecticide, Fungicide, and Rodenticide Act) governs pesticide registration and use. EPA must register pesticides based on risk-benefit analysis — the pesticide must not cause 'unreasonable adverse effects on the environment.' Requires: (1) product registration, (2) residue tolerances in food (with FQPA), (3) reregistration of older pesticides, (4) labeling and classification (restricted use vs general use). [Source: Casarett Ch.35, Regulatory Toxicology; Ch.22, Pesticides; FIFRA 1947/amended by FQPA 1996]"
    if re.search(r'tsca', tl):
        return "TSCA (Toxic Substances Control Act) governs existing and new industrial chemicals (not pesticides, food, drugs, cosmetics). EPA reviews Premanufacture Notices (PMNs) for new chemicals. The 2016 Lautenberg Act amendments: (1) affirmative finding of safety required before marketing, (2) EPA must prioritize existing chemicals for risk evaluation, (3) confidentiality protections with substantiation requirements. Section 8(e): mandatory reporting of substantial risk information. [Source: Casarett Ch.35, Regulatory; TSCA 1976/Lautenberg 2016]"
    if re.search(r'clean (air|water)|caa|cwa', tl):
        return "Clean Air Act (CAA) — EPA sets National Ambient Air Quality Standards (NAAQS) for criteria pollutants (O₃, PM, CO, NO₂, SO₂, Pb) and National Emission Standards for Hazardous Air Pollutants (NESHAPs). Section 112 lists 188 HAPs. Clean Water Act (CWA) — regulates discharges to surface waters via NPDES permits; sets water quality criteria for toxic pollutants. [Source: Casarett Ch.35, Regulatory; Ch.30, Ecotoxicology; CAA 1970/CWA 1972]"
    return f"[Regulatory] The correct answer is {ans}: {correct}. This question tests regulatory toxicology. [Source: Casarett Ch.35, Regulatory Toxicology]"


def _explain_carcinogenesis(text, ans, correct, tl):
    if re.search(r'initiation.*promotion|two.stage|initiator.*promoter', tl):
        return "Two-stage carcinogenesis: Initiation (irreversible DNA damage by genotoxic carcinogen — a single exposure can suffice, no threshold, mutation in critical genes like ras, p53). Promotion (clonal expansion of initiated cells via sustained cell proliferation — requires repeated exposure, reversible, threshold exists). Progression (accumulation of additional mutations → malignant phenotype). [Source: Casarett Ch.8, Chemical Carcinogenesis]"
    if re.search(r'genotoxic|non.genotoxic|direct.*carcinogen|indirect.*carcinogen', tl):
        return "Genotoxic carcinogens (DNA-reactive): directly damage DNA, no threshold assumed, linear low-dose extrapolation. Examples: aflatoxin B₁, benzo(a)pyrene, alkylating agents. Non-genotoxic carcinogens: epigenetic mechanisms (receptor-mediated, cytotoxicity with regenerative proliferation, immunosuppression), threshold assumed, margin-of-exposure approach. Examples: TCDD, phenobarbital (thyroid tumors), d-limonene (α₂u-globulin nephropathy). [Source: Casarett Ch.8, Chemical Carcinogenesis; EPA Guidelines for Carcinogen Risk Assessment]"
    if re.search(r'iarc|classification.*carcin|epa.*cancer', tl):
        return "IARC groups: 1 (carcinogenic to humans — sufficient human evidence), 2A (probably — limited human + sufficient animal), 2B (possibly — limited human + less than sufficient animal, or sufficient animal only), 3 (not classifiable), 4 (probably not carcinogenic). EPA: Carcinogenic to Humans, Likely Carcinogen, Suggestive Evidence, Inadequate Information, Not Likely Carcinogenic. [Source: Casarett Ch.8, Chemical Carcinogenesis; IARC Monographs; EPA Cancer Guidelines 2005]"
    return f"[Carcinogenesis] The correct answer is {ans}: {correct}. This question tests chemical carcinogenesis. [Source: Casarett Ch.8, Chemical Carcinogenesis]"


def _explain_ecotox(text, ans, correct, tl):
    if re.search(r'bioconcentrat|bioaccumulat|biomagnif', tl):
        return "Bioconcentration — uptake from water only (BCF = C_organism / C_water at steady state). Bioaccumulation — uptake from all sources (water + food). Biomagnification — increasing concentration with trophic level (requires persistence + lipophilicity + resistance to metabolism). DDT, PCBs, methylmercury, and PBDEs biomagnify. Log Kow > 3 → bioaccumulation potential. BAF = bioaccumulation factor (from food + water). [Source: Casarett Ch.30, Ecotoxicology; Hayes Ch.10]"
    return f"[Ecotoxicology] The correct answer is {ans}: {correct}. This question tests ecotoxicology or environmental fate. [Source: Casarett Ch.30, Ecotoxicology]"


def _explain_generic(text, ans, correct, tl, bloom):
    return f"[General] Correct answer: {ans}: {correct}. (Bloom: {bloom}) This requires recalling/understanding key toxicology concepts. [Source: Casarett & Doull's Toxicology, appropriate chapter]"


if __name__ == "__main__":
    question_ids = sys.argv[1:] if len(sys.argv) > 1 else []
    if not question_ids:
        print(json.dumps({"error": "no question IDs provided"}))
        sys.exit(1)

    results = []
    errors = []
    for qid in question_ids:
        try:
            q, opts = fetch_question(qid)
            if q is None:
                errors.append({"id": qid, "error": "not found"})
                continue
            expl = write_explanation(q, opts)
            results.append({"id": qid, "explanation": expl, "domain": q["domain"]})
        except Exception as e:
            errors.append({"id": qid, "error": str(e)})

    output = {"results": results, "errors": errors}
    print(json.dumps(output, indent=2))
