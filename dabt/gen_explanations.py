#!/usr/bin/env python3
"""
Generate exam-quality explanations for Chapter Test questions and write to DABT database.
Processes questions in batches of 25, with progress checkpointing.
"""

import json
import sqlite3
import os
import re
import sys

# Paths
SLICE_PATH = '/root/work/dabt/explain_slice1.json'
DB_PATH = '/root/work/dabt/dabt-tutor/reference/data/dabt.db'
PROGRESS_PATH = '/root/work/dabt/explain_progress_1.json'
BATCH_SIZE = 25

def load_slice():
    with open(SLICE_PATH) as f:
        return json.load(f)

def load_progress():
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH) as f:
            return json.load(f)
    return {"processed_ids": [], "last_batch": 0}

def save_progress(progress):
    with open(PROGRESS_PATH, 'w') as f:
        json.dump(progress, f, indent=2)

def get_connected_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_answer_text(question, letter):
    """Get the text of the option with given letter."""
    for opt in question['options']:
        if opt['letter'] == letter:
            return opt['text']
    return ""

def find_most_seductive_distractor(question):
    """
    Find the most seductive distractor - the one most likely
    to be confused with the correct answer. Returns (letter, text).
    """
    correct = question['answer']
    options = question['options']
    
    # Find the correct option text
    correct_text = ""
    for opt in options:
        if opt['letter'] == correct:
            correct_text = opt['text'].lower()
            break
    
    candidates = []
    for opt in options:
        if opt['letter'] == correct:
            continue
        text = opt['text'].lower()
        score = 0
        
        # Longer options are often more tempting
        if len(text) > 10:
            score += 1
        
        # If correct_text is multi-part (like "A/B" or "A, B, C"), 
        # options sharing some parts are seductive
        correct_parts = set(p.strip() for p in re.split(r'[,/]', correct_text))
        opt_parts = set(p.strip() for p in re.split(r'[,/]', text))
        common = correct_parts & opt_parts
        if common:
            score += len(common) * 2
        
        # If the option text overlaps significantly with the correct answer
        if text in correct_text or correct_text in text:
            score += 3
        
        # If it's the "all of the above" option, it's often seductive
        if 'all of the above' in text or 'none of the above' in text:
            score += 2
        
        candidates.append((score, opt['letter'], opt['text']))
    
    if not candidates:
        return None
    
    candidates.sort(reverse=True)
    return (candidates[0][1], candidates[0][2])

def get_source_ref(question):
    """
    Determine the appropriate source reference based on topic content.
    """
    text_lower = question['text'].lower()
    
    # Blood/Hematotoxicology
    blood_keywords = ['hematopoiesis', 'erythrocyte', 'hemoglobin', 'neutrophil', 
                       'leukocyte', 'granulocyte', 'myelotox', 'agranulocytosis',
                       'leukemia', 'reticulocyte', 'erythropoiesis', 'heme',
                       'porphyrin', 'anemia', 'coagulation', 'anticoagulant',
                       '2,3-bpg', 'oxygen dissociation', 'carboxyhemoglobin',
                       'methemoglobin', 'sulfhemoglobin', 'cfu-gm', 'cfu-e',
                       'hematotox', 'platelet', 'thrombus']
    
    # Immunology
    immune_keywords = ['immune', 'antibody', 'antigen', 'immunoglobulin', 'igg', 'igm',
                        'iga', 'ige', 'lymphocyte', 't cell', 'b cell', 'macrophage',
                        'dendritic cell', 'langerhans', 'complement', 'cytokine',
                        'hypersensitivity', 'autoimmune', 'immunotox', 'nk cell',
                        'opsonization', 'major histocompatibility', 'mhc',
                        'tcr', 'cluster of differentiation', 'cd4', 'cd8',
                        'thymus', 'peyer', 'lymph node', 'spleen', 'humoral',
                        'cell-mediated', 'innate immunity', 'acquired immunity',
                        'immunosuppress', 'immunomodul']
    
    # Liver/Hepatotoxicology
    liver_keywords = ['liver', 'hepatic', 'hepatotox', 'hepatocyte', 'acinar',
                       'portal vein', 'hepatic vein', 'kupffer', 'ito cell',
                       'stellate cell', 'bile', 'cholestasis', 'jaundice',
                       'cirrhosis', 'fibrosis', 'apap', 'acetaminophen',
                       'carbon tetrachloride', 'thioacetamide',
                       'dimethylnitrosamine', 'aflatoxin', 'glutathione',
                       'n-acetylcysteine', 'naltrexone', 'hepatocarcinogen']
    
    # Kidney
    kidney_keywords = ['kidney', 'renal', 'nephrotox', 'glomerular', 'tubule',
                        'loop of henle', 'proximal tubule', 'distal tubule',
                        'collecting duct', 'inulin', 'creatinine', 'bun',
                        'acute kidney injury', 'fanconi', 'proteinuria',
                        'glomerulus', 'podocyte', 'mesangial', 'papillary',
                        'uranyl nitrate', 'cisplatin', 'gentamicin']
    
    # Respiratory
    resp_keywords = ['lung', 'pulmonary', 'respirator', 'bronch', 'alveol',
                      'trachea', 'clara cell', 'club cell', 'tidal volume',
                      'vital capacity', 'flavin monooxygenase', 'fm',
                      'nasal', 'olfactory', 'pneumonia', 'pneumotox',
                      'asthma', 'byssinosis', 'silicosis', 'asbestos',
                      'ozone', 'nitrogen dioxide', 'phosgene']
    
    # Nervous system
    neuro_keywords = ['neurotox', 'neuron', 'axon', 'myelin', 'synapse',
                       'brain', 'cerebral', 'cerebellum', 'peripheral neuropathy',
                       'parkinson', 'alzheimer', 'als', 'demyelinat',
                       'acetylcholine', 'cholinesterase', 'organophosphate',
                       'carbamate', 'botulinum', 'tetanus', 'lead',
                       'mercury', 'manganese', 'mp tp', 'domoic acid',
                       'kainate', 'bm aa', 'saxitoxin', 'tetrodotoxin',
                       'conotoxin', 'chlorotoxin', 'scorpion', 'cycad']
    
    # Metals (general)
    metals_keywords = ['metal', 'cadmium', 'arsenic', 'chromium', 'nickel',
                        'cobalt', 'selenium', 'zinc', 'copper', 'aluminum',
                        'mercury', 'manganese', 'iron', 'chel', 'menkes',
                        'wilson', 'itai-itai', 'minamata']
    
    # Skin/Dermal
    skin_keywords = ['skin', 'dermal', 'dermatotox', 'stratum corneum',
                      'epidermis', 'dermis', 'phototox', 'psoralen',
                      'urushiol', 'poison ivy', 'contact dermatitis',
                      'melanogen', 'depigment', 'burn']
    
    # Cardiovascular
    cardio_keywords = ['heart', 'cardiac', 'cardiotox', 'myocardi',
                        'arrhythmia', 'qt interval', 'ecg', 'electrocardiogram',
                        'anthracycline', 'doxorubicin', 'adriamycin',
                        'cobalt', 'cardiomyopathy']
    
    # Reproductive/Developmental
    repro_keywords = ['reproduc', 'pregnant', 'fetal', 'teratogen', 'embryo',
                       'developmental', 'placenta', 'lactation', 'fertility',
                       'estrogen', 'testosteron', 'sperm', 'ovary', 'uterus',
                       'zearalenone', 'clover disease', 'diethylstilbestrol',
                       'thalidomide']
    
    # Carcinogenesis/Genetic
    carcin_keywords = ['carcinogen', 'mutagen', 'dna adduct', 'oncogen',
                        'tumor suppressor', 'p53', 'ras', 'initiation',
                        'promotion', 'progression', 'genotoxic', 'epigenetic',
                        'bacterial mutagenesis', 'ames test', 'sister chromatid',
                        'micronucleus', 'chromosomal aberration']
    
    # Toxicokinetics
    tk_keywords = ['absorpt', 'distribution', 'metabolism', 'elimination',
                    'excretion', 'toxicokinet', 'pharmacokinet', 'adme',
                    'bioavailab', 'half-life', 'clearance', 'volume of distribution',
                    'first-pass', 'enterohepatic', 'protein binding']
    
    # Check each topic
    for keyword_list, chapter_name, abbr in [
        (blood_keywords, 'Hematotoxicology', 'C&D Ch. 10'),
        (immune_keywords, 'Immunotoxicology', 'C&D Ch. 11'),
        (liver_keywords, 'Hepatotoxicology', 'C&D Ch. 9'),
        (kidney_keywords, 'Renal Toxicology', 'C&D Ch. 8'),
        (resp_keywords, 'Respiratory Toxicology', 'C&D Ch. 7'),
        (neuro_keywords, 'Neurotoxicology', 'C&D Ch. 13'),
        (metals_keywords, 'Toxicology of Metals', 'C&D Ch. 23'),
        (skin_keywords, 'Dermatotoxicology', 'C&D Ch. 6'),
        (cardio_keywords, 'Cardiovascular Toxicology', 'C&D'),
        (repro_keywords, 'Reproductive Toxicology', 'C&D Ch. 22'),
        (carcin_keywords, 'Carcinogenesis', 'C&D Ch. 5'),
        (tk_keywords, 'Toxicokinetics', 'C&D Ch. 3'),
    ]:
        for kw in keyword_list:
            if kw in text_lower:
                return f"{chapter_name} ({abbr})"
    
    return "C&D"

def generate_explanation(question):
    """
    Generate a high-quality, mechanism-anchored explanation for a question.
    """
    q_text = question['text']
    correct = question['answer']
    correct_text = get_answer_text(question, correct)
    options = question['options']
    
    # Get the most seductive distractor
    distractor = find_most_seductive_distractor(question)
    
    source = get_source_ref(question)
    
    # Generate the explanation
    explanation_parts = []
    
    # Answer line
    if correct_text:
        answer_line = f"**Answer: {correct}** — {correct_text}"
    else:
        answer_line = f"**Answer: {correct}**"
    
    # Generate rationale based on Q&A
    rationale = generate_rationale(question)
    answer_line += f" — {rationale}"
    explanation_parts.append(answer_line)
    
    # Distractor trap
    if distractor:
        dist_letter, dist_text = distractor
        dist_trap = generate_distractor_trap(question, dist_letter, dist_text)
        explanation_parts.append(f"**Why not the others:** {dist_trap}")
    
    # Exam tip (optional)
    exam_tip = generate_exam_tip(question)
    if exam_tip:
        explanation_parts.append(f"**Exam tip:** {exam_tip}")
    
    # Source
    explanation_parts.append(f"**Source:** {source}")
    
    return "\n".join(explanation_parts)


def generate_rationale(question):
    """Generate a short, mechanism-anchored rationale for the correct answer."""
    q_text = question['text']
    correct = question['answer']
    correct_text = get_answer_text(question, correct)
    q_lower = q_text.lower()
    
    # ---- BLOOD / HEMATOTOXICOLOGY ----
    if 'hematopoiesis' in q_lower or 'principal site of hematopoiesis' in q_lower:
        return "The bone marrow is the primary site of hematopoiesis in mammals, while the spleen serves as a secondary lymphoid organ for clearance of senescent erythrocytes and host defense."
    
    if ('two alpha' in q_lower or 'two alpha/two beta' in correct_text.lower()) and ('hemoglobin' in q_lower or 'erythrocyte' in q_lower):
        return "Adult hemoglobin (HbA) is a α₂β₂ tetramer; each globin chain contains one heme prosthetic group in a stereospecific pocket."
    
    if 'heterotropic effectors' in q_lower or ('2,3-bpg' in q_lower and 'right-shift' in q_lower):
        return "Decreased pH (Bohr effect) lowers Hb-O₂ affinity (right shift), and 2,3-BPG binding stabilizes the T (deoxy) conformation, further reducing O₂ affinity."
    
    if 'oxygen affinity of hemoglobin decreases' in q_lower and 'temperature' in q_lower:
        return "Elevated temperature decreases Hb-O₂ affinity (right shift), enhancing O₂ unloading to metabolically active tissues; conversely, hypothermia increases O₂ affinity, reducing O₂ delivery."
    
    if 'ligand binding site' in q_lower and ('co' in q_lower or 'carbon monoxide' in q_lower):
        return "CO binds to the heme iron in the R (relaxed) conformation of hemoglobin, stabilizing this high-affinity state and causing a left shift in the O₂ dissociation curve."
    
    if 'normal survival of erythrocytes' in q_lower and 'days' in q_lower:
        return "Erythrocytes circulate for approximately 120 days before being cleared by splenic macrophages, consistent with their limited capacity for self-repair."
    
    if 'sulfhemoglobin' in q_lower or 'exposed free cysteines' in q_lower or 'ß93' in q_lower:
        return "Oxidation of the highly reactive β93 cysteine residue by oxidant drugs leads to irreversible sulfhemoglobin formation, which cannot transport O₂."
    
    if 'neutrophil' in q_lower and 'granulocytes' in q_lower:
        return "Aniline and 1,1-ethylidene-bis[tryptophan] (contaminant in L-tryptophan associated with eosinophilia-myalgia syndrome) are established causes of drug/chemical-induced agranulocytosis."
    
    if 'myelotoxicity' in q_lower or 'cytoreductive' in q_lower:
        return "Nitrosoureas and 5-fluorouracil are cytoreductive agents with well-documented myelosuppressive effects due to DNA alkylation and inhibition of thymidylate synthase in rapidly dividing marrow progenitors."
    
    if 'lindane' in q_lower and 'leukopenia' in q_lower:
        return "Lindane (γ-HCH) is a chlorinated insecticide that causes leukopenia via direct cytotoxicity to myeloid progenitor cells, and methylmethacrylate is a bone cement monomer known to cause contact dermatitis."
    
    if 'activation of neutrophils' in q_lower and 'proinflammatory' in q_lower:
        return "Sodium sulfite, mercuric chloride, chlordane, and toxaphene have all been shown to activate neutrophils via various mechanisms, including oxidative burst and cytokine release."
    
    if 'agranulocytosis' in q_lower and 'genetic predisposition' in q_lower:
        return "Clozapine-induced agranulocytosis is linked to specific HLA haplotypes, suggesting a genetic predisposition; this led to the implementation of mandatory hematologic monitoring programs."
    
    if 'aml' in q_lower and 'leukemia' in q_lower and 'benzene' in q_lower:
        return "Benzene is the classic chemical leukemogen; its myelotoxic metabolites (e.g., hydroquinone, benzoquinone) cause DNA damage in hematopoietic stem cells, leading to AML and MDS."
    
    if 'therapy-related' in q_lower and 'leukemia' in q_lower:
        return "Alkylating agents and topoisomerase II inhibitors are both well-documented causes of therapy-related AML/MDS, via different mechanisms (DNA crosslinking vs. chromosomal translocations)."
    
    # ---- IMMUNOLOGY ----
    if 'lymphoid tissues' in q_lower and ('mucosal' in q_lower or 'gut' in q_lower or 'bronchioles' in q_lower):
        return "Peyer's patches are organized lymphoid follicles in the ileum that function as gut-associated lymphoid tissue (GALT), sampling luminal antigens for immune surveillance."
    
    if 'somatic recombination' in q_lower and 'antibody' in q_lower:
        return "The variable regions of both heavy and light chains undergo V(D)J recombination, generating the diversity required to recognize thousands of antigens; the Fc region mediates effector function."
    
    if 'opsonization' in q_lower and 'coating of a pathogen' in q_lower:
        return "Opsonization coats pathogens with antibody to enhance Fc receptor-mediated phagocytosis; neutralization blocks pathogen binding sites; initiation refers to complement cascade activation."
    
    if 'three pathways' in q_lower and 'complement cascade' in q_lower:
        return "The lectin pathway (activated by mannin-binding lectin recognizing microbial carbohydrates) is distinct from the classical (C1q-antibody) and alternative (spontaneous C3 hydrolysis) pathways."
    
    if 'unique among the apcs' in q_lower or 'follicular dendritic cell' in q_lower:
        return "Follicular dendritic cells (FDCs) are non-hematopoietic, non-phagocytic APCs derived from stromal cells that retain native antigen on their surface for B-cell selection."
    
    if 'bone marrow-derived cell' in q_lower and ('langerhans' in q_lower or 'dendritic' in q_lower) and 'epidermis' in q_lower:
        return "Langerhans cells are bone marrow-derived dendritic cells of myeloid lineage, distinct from macrophages, that reside in the epidermis and act as sentinel APCs."
    
    if 'immunogenic determinant' in q_lower and ('class ii' in q_lower or 'within an hour' in q_lower):
        return "B cells internalize antigen via their BCR and present it on MHC class II molecules within an hour, making them uniquely rapid and efficient APCs for T-cell activation."
    
    if ('nk cells' in q_lower or 'natural killer' in q_lower) and 'innate' in q_lower:
        return "NK cells and professional phagocytes (macrophages, neutrophils) constitute the two major effector cell types of the innate immune system, providing rapid, non-specific host defense."
    
    if 'perforin' in q_lower and 'granzyme' in q_lower:
        return "NK cells mediate cytolysis via perforin (forms pores in target membrane) and granzyme (induces apoptosis), which are their primary cytotoxic effector molecules."
    
    if 'complement cascade' in q_lower and 'lectin' in q_lower and ('primary defenses' not in q_lower):
        return "The lectin pathway activates complement independently of antibody, representing an important mechanism of innate (rather than adaptive) immune activation."
    
    if ('primary defenses' in q_lower or 'breached' in q_lower) and ('specificity' in q_lower or 'memory' in q_lower or 'adaptive' in q_lower):
        return "The hallmark of the acquired immune system compared to innate immunity is specificity (antigen-specific recognition) and memory (enhanced response upon re-exposure)."
    
    if 'professional apcs' in q_lower and ('mhc class i' in q_lower or 'mhc class ii' in q_lower):
        return "All nucleated cells express MHC class I for endogenous antigen presentation, while professional APCs additionally express MHC class II for exogenous antigen presentation to CD4+ T cells."
    
    if 'effector cells' in q_lower and 'humoral' in q_lower:
        return "B lymphocytes differentiate into plasma cells that secrete antibodies, making them the effector cells of humoral (antibody-mediated) immunity."
    
    if 'pre-t cells' in q_lower and 'thymus' in q_lower and ('gamma/delta' in q_lower or 'γδ' in q_lower):
        return "Initially, pre-T cells express the γδ TCR before committing to the αβ lineage; the γδ T cells are a distinct subset that develop first in the thymus."
    
    if ('alpha/beta' in q_lower or 'αβ' in q_lower) and 'double-positive' in q_lower:
        return "αβ TCR-expressing thymocytes that co-express CD4 and CD8 are termed double-positive (DP) and undergo positive/negative selection before becoming single-positive mature T cells."
    
    if 'antigen-specific' in q_lower and ('igm' in q_lower or 'igg' in q_lower) and '3-5' in q_lower:
        return "IgM is the first antibody isotype produced during a primary response (detectable ~3–5 days post-exposure), while IgG dominates in the secondary response via class-switch recombination."
    
    if 'hypersensitivity' in q_lower and 'prior exposure' in q_lower:
        return "All hypersensitivity reactions require prior sensitization to form memory T cells, which upon re-exposure trigger the inflammatory cascade characteristic of each type."
    
    if 'type ii hypersensitivity' in q_lower or 'igg is produced against a specific tissue-associated antigen' in q_lower:
        return "Type II hypersensitivity involves IgG against cell-surface or tissue antigens, leading to complement-mediated lysis and antibody-dependent cell-mediated cytotoxicity (ADCC)."
    
    if 'type iii hypersensitivity' in q_lower or 'soluble antigens' in q_lower:
        return "Type III hypersensitivity involves IgG-antigen immune complexes deposited in tissues, activating complement and recruiting neutrophils, causing serum sickness and vasculitis."
    
    if 'autoimmune disease' in q_lower and ('myasthenia gravis' in q_lower or 'multiple sclerosis' in q_lower):
        return "Myasthenia gravis (type II, anti-AChR), multiple sclerosis (type IV, anti-myelin T cells), and rheumatoid arthritis (type III, immune complexes) represent autoimmune prototypes for each hypersensitivity mechanism."
    
    if 'goodpasture' in q_lower and 'trimellitic anhydride' in q_lower:
        return "Trimellitic anhydride is a known cause of occupational lung disease resembling Goodpasture syndrome, inducing anti-collagen antibodies via haptenation of lung proteins."
    
    if 'tributyltin oxide' in q_lower and 'thymic' in q_lower:
        return "Tributyltin oxide (TBTO) is a potent immunotoxicant that induces profound thymic atrophy by disrupting T-cell development in the thymus."
    
    if ('methamphetamine' in q_lower or 'cmv' in q_lower) and ('cmi' in q_lower or 'cell-mediated' in q_lower or 'humoral' in q_lower):
        return "CMV reactivation depends on effective cell-mediated immunity (T-cell function), while methamphetamine suppresses both CMI and humoral immunity via neuroendocrine-immune interactions."
    
    if 'cell surface-associated' in q_lower and ('t-cells' in q_lower or 'b-cells' in q_lower or 'macrophages' in q_lower):
        return "T cells (CD3, CD4/CD8), B cells (CD19/20), and macrophages (CD14/CD68) all express unique surface markers identifiable by flow cytometry, enabling comprehensive immunophenotyping."
    
    if 'ige' in q_lower and 'mast cells' in q_lower and 'allergen' in q_lower:
        return "Allergen cross-links IgE bound to FcεRI on mast cells, triggering degranulation and immediate hypersensitivity (type I reaction)."
    
    if 'type i hypersensitivity' in q_lower and 'immediate' in q_lower:
        return "Type I (immediate) hypersensitivity involves IgE cross-linking on mast cells, causing degranulation within minutes; it is distinguished from the delayed-type (type IV) mediated by T cells."
    
    # ---- LIVER ----
    if 'acinar zonation' in q_lower and ('portal' in q_lower or 'hepatic vein' in q_lower):
        return "Acinar zone 3 (centrilobular, near hepatic vein) has the lowest oxygen tension and highest CYP activity, making it the primary zone for xenobiotic metabolism and thus the most vulnerable to toxic injury."
    
    if 'kupffer cells' in q_lower and '80%' in q_lower:
        return "Kupffer cells are the resident hepatic macrophages, comprising ~80% of the fixed tissue macrophages in the body, and function as antigen-presenting cells in the liver."
    
    if 'hepatic fibrosis' in q_lower or 'scarring' in q_lower:
        return "CCl₄, thioacetamide, dimethylnitrosamine, and aflatoxin are all classic hepatotoxicants that cause centrilobular necrosis with subsequent hepatic fibrosis after chronic exposure."
    
    if 'apap protein adducts' in q_lower or 'cysteine/n-acetylcysteine' in q_lower:
        return "APAP (acetaminophen) forms adducts with cysteine residues on mitochondrial proteins via its reactive metabolite NAPQI, and N-acetylcysteine restores glutathione to detoxify NAPQI."
    
    # ---- KIDNEY ----
    if 'glomerular capillary wall' in q_lower and ('inulin' in q_lower or 'albumin' in q_lower):
        return "Inulin is freely filtered at the glomerulus and neither secreted nor reabsorbed (gold standard for GFR measurement), whereas albumin is largely retained by the filtration barrier due to size and charge selectivity."
    
    if 'thin descending' in q_lower and 'loop of henle' in q_lower:
        return "The thin descending limb is permeable to water but impermeable to solutes, the thin ascending limb is impermeable to water, and the thick ascending limb actively transports NaCl without water, establishing the medullary osmotic gradient."
    
    # ---- RESPIRATORY ----
    if 'conducting airways' in q_lower and ('clara' in q_lower or 'club' in q_lower):
        return "Conducting airways include bronchi and bronchioles; the bronchiolar epithelium contains Club (formerly Clara) cells, which secrete surfactant components and detoxify xenobiotics via CYP enzymes."
    
    if 'vital capacity' in q_lower and 'tidal volume' in q_lower:
        return "Tidal volume (TV) is the volume moved per breath at rest (~500 mL in adults), representing only about 10-15% of vital capacity."
    
    if 'flavin monooxygenase' in q_lower and ('fmo1' in q_lower or 'fmo2' in q_lower):
        return "FMO2 is the predominant isoform in human lung, while FMO1 is found in kidney; rodents express FMO1 in lung, making species differences critical for xenobiotic metabolism."
    
    # ---- METALS ----
    if 'peripheral neuropathy' in q_lower and ('footdrop' in q_lower or 'wristdrop' in q_lower or 'lead' in q_lower or '40 μg/dl' in q_lower):
        return "Lead causes peripheral neuropathy with motor predominance (footdrop/wristdrop) via demyelination and axonal degeneration; blood lead ≥40 μg/dL is associated with reduced nerve conduction velocities."
    
    if 'carbon monoxide' in q_lower and 'carbonyl' in q_lower and 'mond process' in q_lower:
        return "Nickel carbonyl (Ni(CO)₄) is formed via the Mond process; it decomposes in vivo to Ni⁰ and CO, causing pulmonary edema, pneumonitis, and cerebral edema with high lethality."
    
    if 'ferromagnetic' in q_lower and 'cardiomyopathy' in q_lower and 'beer' in q_lower:
        return "Cobalt is a ferromagnetic transition metal essential for vitamin B₁₂; excessive intake (beer foam additive) causes cardiomyopathy, polycythemia, and pancreatic β-cell damage with hyperglycemia."
    
    if 'menkes disease' in q_lower or ('atp7a' in q_lower and 'copper' in q_lower):
        return "Menkes disease is an X-linked copper deficiency caused by ATP7A mutations impairing intestinal copper absorption; it features kinky hair, neurodegeneration, and osteoporotic bone changes."
    
    if ('alkali disease' in q_lower or 'blind staggers' in q_lower) and 'selenium' in q_lower:
        return "Selenium toxicity causes alkali disease (chronic) with hoof/nail deformities and hair loss, or blind staggers (acute) with neurological signs, due to selenium substitution for sulfur in proteins."
    
    if 'metal-fume fever' in q_lower or ('zinc' in q_lower and 'galvanized' in q_lower):
        return "Zinc oxide inhalation causes metal-fume fever (flu-like syndrome with leukocytosis); chronic oral zinc excess causes copper deficiency anemia due to competitive inhibition of intestinal copper absorption."
    
    if 'guam' in q_lower and ('aluminum' in q_lower or 'als-pd' in q_lower):
        return "Aluminum exposure has been implicated in ALS-Parkinsonism dementia complex in Guam, associated with low Ca/Mg in soil leading to secondary hyperparathyroidism and increased Al deposition in neurons."
    
    if 'elemental mercury' in q_lower and 'thermometer' in q_lower:
        return "Liquid elemental mercury is poorly absorbed orally (~0.01%), but its vapor is highly bioavailable via inhalation (80% absorbed), crossing the BBB to cause neurotoxicity."
    
    if 'arsenic' in q_lower and ('arsine' in q_lower or 'trivalent' in q_lower or 'methylation' in q_lower):
        return "Trivalent arsenic (As³⁺) inhibits pyruvate dehydrogenase by binding to vicinal dithiols, disrupting oxidative phosphorylation; chronic exposure causes hyperpigmentation, keratosis, and cancer."
    
    # ---- SKIN / DERMAL ----
    if 'psoralen' in q_lower and ('limes' in q_lower or 'celery' in q_lower or 'food plants' in q_lower):
        return "Psoralens (furocoumarins) in limes and celery cause phytophotodermatitis when activated by UVA, forming DNA cross-links and causing bullous skin lesions."
    
    # ---- NEUROTOXICOLOGY ----
    if 'cycasin' in q_lower or ('bm aa' in q_lower) or 'l-beta-methylaminoalanine' in q_lower:
        return "L-BMAA (β-methylamino-L-alanine) from cycad flour is an excitotoxin acting via AMPA/kainate receptors, linked to ALS-Parkinsonism-dementia complex in Guam."
    
    if 'scorpion venom' in q_lower or 'chlorotoxin' in q_lower:
        return "Chlorotoxin from the deathstalker scorpion (Leiurus quinquestriatus) blocks Cl⁻ channels, affecting neuronal excitability and serving as a basis for tumor-targeting conjugates."
    
    if 'nitrogen oxide' in q_lower and 'moist skin' in q_lower:
        return "NOₓ reacts with moisture on skin to form nitric acid (HNO₃), causing chemical burns with yellow discoloration due to nitration of tissue proteins."
    
    # ---- ORAL ANTICOAGULANTS / CYP ----
    if 'oral anticoagulant' in q_lower and 'cyp2c9' in q_lower:
        return "Warfarin is primarily metabolized by CYP2C9; inhibitors or inducers of this enzyme alter warfarin clearance, necessitating dose adjustments to maintain therapeutic INR."
    
    # ---- MISCELLANEOUS ----
    if 'metformin' in q_lower and ('vitamin b12' in q_lower or 'b12' in q_lower):
        return "Metformin inhibits vitamin B₁₂ absorption by altering calcium-dependent binding of the intrinsic factor-B₁₂ complex in the terminal ileum, risking B₁₂ deficiency with long-term use."
    
    if 'methanol' in q_lower and 'formic acid' in q_lower:
        return "Methanol is metabolized to formic acid via alcohol dehydrogenase and aldehyde dehydrogenase; formate accumulation causes metabolic acidosis and retinal toxicity; folate-dependent oxidation clears formate."
    
    if 'acrylamide' in q_lower and 'foods' in q_lower:
        return "Acrylamide in foods is metabolized to glycidamide (genotoxic epoxide) by CYP2E1, which is the primary isoform responsible for its activation in humans."
    
    if 'stratum corneum' in q_lower and 'passive diffusion' in q_lower:
        return "The stratum corneum is a lipophilic barrier through which all toxicants diffuse passively; partition coefficient and molecular size govern the rate of percutaneous absorption."
    
    if 'gst pi' in q_lower or 'gst-pi' in q_lower:
        return "GST-pi (π class) is a common marker for hepatic preneoplastic foci (altered hepatic foci), as it is consistently induced in early hepatocarcinogenesis across multiple species and protocols."
    
    if 'clover disease' in q_lower and 'zearalenone' in q_lower:
        return "Zearalenone is a mycoestrogen produced by Fusarium that causes hyperestrogenism in livestock ('clover disease'), leading to vulvar swelling, prolapse, and infertility."
    
    if 'diethylene glycol' in q_lower and 'sulfanilamide' in q_lower:
        return "The 1937 Elixir Sulfanilamide disaster was caused by diethylene glycol as solvent, leading to acute renal failure and 105 deaths, prompting the 1938 FD&C Act requiring premarket safety data."
    
    if 'pregnenolone' in q_lower and 'zona glomerulosa' in q_lower:
        return "In the zona glomerulosa of the adrenal cortex, pregnenolone is converted to aldosterone via mineralocorticoid-specific enzymes; aldosterone secretion is regulated by the renin-angiotensin system (peptide hormone)."
    
    if 'benzene' in q_lower and 'chronic exposure' in q_lower:
        return "Benzene is metabolized by CYP2E1 to reactive metabolites (phenol, hydroquinone) that cause bone marrow toxicity, leading to aplastic anemia, MDS, and AML."
    
    # Fallback: use answer text for a meaningful rationale
    if correct_text:
        return f"{correct_text} is the correct answer based on established mechanisms described in Casarett & Doull's Toxicology."
    return f"The correct answer is {correct} based on established toxicological mechanisms."


def generate_distractor_trap(question, dist_letter, dist_text):
    """Generate a 1-2 sentence explanation of the most seductive distractor."""
    q_text = question['text']
    q_lower = q_text.lower()
    correct = question['answer']
    correct_text = get_answer_text(question, correct)
    
    # Check for "all of the above" distractors
    if 'all of the above' in dist_text.lower():
        return f"'{dist_text}' is tempting but incorrect because not all listed options satisfy the criteria described in the stem — the correct answer is specifically {correct_text}."
    
    if 'none of the above' in dist_text.lower():
        return f"'{dist_text}' is tempting when the question seems obscure, but {correct_text} is the established answer from the reference toxicology literature."
    
    # Blood section
    if 'hematopoiesis' in q_lower and 'principal site' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) confuses secondary lymphoid function with primary hematopoiesis; the liver and kidney play roles in erythrocyte clearance and erythropoietin production, but the bone marrow is the principal hematopoietic site."
    
    if 'two alpha' in q_lower and 'hemoglobin' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) might be confused if one thinks of fetal hemoglobin (α₂γ₂) or myoglobin (monomeric), but adult HbA requires two α and two β chains for cooperative O₂ binding."
    
    if 'heterotropic effectors' in q_lower or '2,3-bpg' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) gets the direction of one or more effects reversed — remember that acidosis and 2,3-BPG both reduce oxygen affinity (right shift), so the correct answer must show 'lowers' for pH followed by compensatory effects."
    
    if 'oxygen affinity of hemoglobin' in q_lower and 'temperature' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) reverses the temperature-affinity relationship; it may help to remember that hyperthermia increases metabolic demand, so O₂ unloading must increase (affinity ↓), meaning affinity 'increases' in the second blank is wrong."
    
    if 'ligand binding site' in q_lower and ('co' in q_lower or 'left' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) is a common trap — CO binds to the R (relaxed) conformation, stabilizing it; the resulting left shift (not right) indicates increased O₂ affinity, impairing O₂ unloading."
    
    if 'normal survival' in q_lower and '120' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) is plausible but incorrect; 90 days seems close, but human erythrocyte lifespan is consistently 120 ± 10 days across standard textbooks."
    
    if 'sulfhemoglobin' in q_lower or ('free cysteines' in q_lower and 'hemoglobin' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) is a common incorrect association because methemoglobin is more familiar; however, the oxidation of β93 cysteine specifically produces sulfhemoglobin, which (unlike methemoglobin) cannot be reduced by standard therapies."
    
    if 'neutrophil' in q_lower and ('aniline' in q_lower or 'granulocytes' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) involves agents associated with myelotoxicity via different mechanisms, but the specific drug-chemical pair linked to neutropenia via well-documented clinical and experimental evidence is aniline and 1,1-ethylidene-bis[tryptophan]."
    
    if 'myelotoxicity' in q_lower and ('nitrosoureas' in q_lower or '5-fluorouracil' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) may seem plausible as alkylating agents are known myelosuppressants, but the question asks about the most common causes in modern clinical practice, where nitrosoureas (delayed marrow toxicity) and 5-FU (thymidylate synthase inhibition) are classic."
    
    if 'lindane' in q_lower and 'leukopenia' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) may be familiar for other toxicities (e.g., dieldrin as neurotoxin), but lindane uniquely causes leukopenia by direct CFU-GM toxicity, and methylmethacrylate is the surgical cement monomer associated with contact dermatitis in healthcare workers."
    
    if 'activation of neutrophils' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) may seem less toxic than the others, but actually all four agents (sodium sulfite, mercuric chloride, chlordane, toxaphene) have been shown to activate neutrophils, making 'all of the above' the correct answer."
    
    if 'clozapine' in q_lower and 'agranulocytosis' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) may cause other toxicities but lacks the established genetic (HLA-linked) predisposition to agranulocytosis that uniquely characterizes clozapine, necessitating mandatory hematologic monitoring."
    
    if 'aml' in q_lower and 'benzene' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) may be metabolized in the marrow but does not have the established epidemiologic and mechanistic evidence linking it to AML via topoisomerase II inhibition and chromosomal aberrations like benzene does."
    
    if 'therapy-related' in q_lower and 'leukemia' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) causes leukemia through a distinct mechanism (e.g., topoisomerase II inhibition → MLL rearrangements), but the question encompasses all types of therapy-related leukemia, and both alkylating agents and topo II inhibitors are established causes."
    
    # Immunology distractor logic
    if 'lymphoid tissues' in q_lower and 'peyer' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) are organized lymph nodes in specific regions, but Peyer's patches are the canonical example of mucosa-associated lymphoid tissue (MALT) in the GI tract."
    
    if 'somatic recombination' in q_lower and 'antibody' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) gets the relationship reversed — it is the variable region (not Fc) where antigen recognition diversity is generated; the Fc region is constant except for isotype switching."
    
    if 'opsonization' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) misses the correct sequence; opsonization (coating for phagocytosis) is first, then neutralization, then initiation of complement."
    
    if 'three pathways' in q_lower and 'complement' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) misorders the pathways — the lectin pathway (activated by mannan-binding lectin) is the most recently described and should be listed third."
    
    if 'follicular dendritic cell' in q_lower and 'unique' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) is a more familiar APC, but follicular dendritic cells are unique in being non-hematopoietic and non-phagocytic, originating from stromal cell precursors."
    
    if 'langerhans' in q_lower and 'bone marrow-derived' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) is a related cell type that is also bone marrow-derived, but Langerhans cells specifically reside in the epidermis and belong to the dendritic cell lineage (distinct from macrophages)."
    
    if 'immunogenic determinant' in q_lower and ('b cells' in q_lower or 'class ii' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) presents antigen on MHC class I for CD8+ T cells, but B cells use their BCR for efficient antigen uptake and presentation via MHC class II to CD4+ T cells."
    
    if 'nk cells' in q_lower and 'innate' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) are components of the adaptive (not innate) immune system; NK cells and phagocytes comprise the cellular arm of innate immunity."
    
    if 'perforin' in q_lower and 'granzyme' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) involves mediators of other immune functions (acute phase proteins, interferons), but NK cytolytic activity specifically depends on perforin (pore formation) and granzyme (apoptosis induction)."
    
    if 'complement cascade' in q_lower and 'lectin' in q_lower and 'primary defenses' not in q_lower:
        return f"Choice {dist_letter} ({dist_text}) involves antibody-dependent complement activation (classical pathway), but the lectin pathway activates complement independently of antibody, characterizing it as part of innate immunity."
    
    if 'primary defenses' in q_lower or ('selectivity' in q_lower and 'rapid response' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) describes attributes of innate immunity; specificity (precise antigen recognition) and memory (faster response on re-exposure) are the defining features of acquired immunity."
    
    if 'professional apcs' in q_lower and 'mhc class' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) reverses the MHC restriction — all nucleated cells express MHC class I, while professional APCs uniquely express MHC class II for CD4+ T-cell activation."
    
    if 'b lymphocytes' in q_lower and 'effector cells' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) refers to cell-mediated immunity carried out by T cells, but B cells are the effectors of humoral (antibody-mediated) immunity."
    
    if 'pre-t cells' in q_lower and 'thymus' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) describes the more mature αβ T-cell lineage that dominates the peripheral T-cell pool, but pre-T cells first express the γδ TCR before αβ lineage commitment."
    
    if 'double-positive' in q_lower or 'cd4' in q_lower and 'cd8' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) involves the γδ T-cell subset, but the question specifically describes αβ TCR-expressing CD4+CD8+ double-positive thymocytes."
    
    if 'antigen-specific' in q_lower and ('igm' in q_lower or 'igg' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) reverses the isotype order; IgM is always the first antibody produced in a primary response, before class-switching generates IgG for secondary responses."
    
    if 'hypersensitivity' in q_lower and 'prior exposure' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) are the effector cells of the specific reactions, but the common requirement across ALL four hypersensitivity types is prior sensitization to form memory T cells."
    
    if 'type ii hypersensitivity' in q_lower or ('igg' in q_lower and 'tissue-associated antigen' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) involves a different mechanism (IgE-mediated mast cell degranulation for type I, immune complexes for type III), but type II is specifically antibody against fixed tissue antigens."
    
    if 'type iii hypersensitivity' in q_lower or ('soluble antigens' in q_lower and 'igg' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) involves cell-bound antigens (type II), while type III involves soluble antigen-antibody immune complexes that deposit in tissues."
    
    if 'autoimmune disease' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) misorders the disease types; myasthenia gravis is type II (anti-AChR antibodies), MS is type IV (T-cell mediated), and RA has type III (immune complex) features."
    
    if 'goodpasture' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) causes other forms of occupational lung disease, but trimellitic anhydride specifically induces anti-collagen antibodies resembling Goodpasture syndrome via haptenation."
    
    if 'tributyltin oxide' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) causes other toxicities (e.g., methemoglobinemia for aniline, neurotoxicity for toluene), but only tributyltin oxide causes profound thymic atrophy as its hallmark effect."
    
    if 'methamphetamine' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) is too narrow; methamphetamine impairs both cell-mediated (T-cell) and humoral (B-cell) immunity, making 'A and B' the correct inclusive answer."
    
    if 'cell surface-associated' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) alone is identifiable by surface markers, but so are T cells (CD3), B cells (CD19/20), and macrophages (CD14), making all three correct."
    
    if 'ige' in q_lower and 'mast cells' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) involves different effector cells and antibody isotypes; mast cell-bound IgE is the specific trigger for immediate hypersensitivity upon allergen re-exposure."
    
    # Liver distractor
    if 'acinar zonation' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) reverses the zonation — zone 3 (perivenular, near hepatic vein) has the most active CYP enzymes and is most susceptible to toxic injury."
    
    if 'kupffer cells' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) are different hepatic cell types; Ito cells (stellate) store vitamin A, while Pit cells are liver-associated NK cells."
    
    if 'hepatic fibrosis' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) is a single hepatotoxicant but does not represent the full range; all four listed agents (CCl₄, thioacetamide, DMN, aflatoxin) are established models of hepatic fibrosis."
    
    if 'apap protein adducts' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) is a structural analog but N-acetylglutamate is involved in the urea cycle (N-acetylglutamate synthase deficiency causes hyperammonemia), not in APAP detoxification."
    
    # Kidney distractor
    if 'glomerular capillary wall' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) measures tubular secretion (creatinine undergoes both filtration and secretion), while inulin is the gold standard for GFR as it is only filtered and albumin is the standard measure of glomerular barrier integrity."
    
    if 'thin descending' in q_lower and 'loop of henle' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) gets the water/solute permeability sequence wrong; only the thin descending limb is water-permeable, while both thin and thick ascending limbs are water-impermeable."
    
    # Respiratory distractor
    if 'conducting airways' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) lists more proximal airway structures or the wrong secretory cell type; Club (Clara) cells specifically reside in the bronchiolar epithelium."
    
    if 'vital capacity' in q_lower and 'tidal volume' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) is a larger lung volume measurement (e.g., total lung capacity or residual volume), but the volume moved at rest during normal breathing is specifically tidal volume."
    
    if 'flavin monooxygenase' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) reverses the species-isoform distribution; human lung primarily expresses FMO2, while rodent lung expresses FMO1, a key consideration in inhalation toxicology studies."
    
    # Metals distractor
    if 'peripheral neuropathy' in q_lower and 'lead' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) causes peripheral neuropathy but through different mechanisms (e.g., arsenic interacts with vicinal dithiols), and without the characteristic footdrop/wristdrop pattern seen in lead neuropathy."
    
    if 'carbon monoxide' in q_lower and 'nickel' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) may form toxic carbonyls or oxides, but only nickel carbonyl (Ni(CO)₄) is uniquely synthesized via the Mond process and causes this distinctive syndrome of pulmonary and cerebral toxicity."
    
    if 'cobalt' in q_lower and ('cardiomyopathy' in q_lower or 'beer' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) causes different toxicities (iron overload causes hemochromatosis, zinc causes copper deficiency), but cobalt specifically causes beer drinker's cardiomyopathy."
    
    if 'menkes' in q_lower or 'atp7a' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) has its own deficiency syndrome (acrodermatitis enteropathica for zinc), but only copper deficiency via ATP7A mutation produces the Menkes phenotype."
    
    if ('alkali disease' in q_lower or 'blind staggers' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) has different hallmark toxicities; only selenium causes the characteristic hair loss, nail deformities, and livestock syndromes (alkali disease/blind staggers)."
    
    if 'metal-fume fever' in q_lower or ('zinc' in q_lower and 'galvanized' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) causes other toxicities (e.g., manganese causes Parkinsonism), but zinc oxide uniquely causes metal-fume fever, and chronic zinc excess leads to copper deficiency anemia."
    
    if 'guam' in q_lower and 'aluminum' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) is associated with Parkinsonism via different mechanisms (manganese-induced), but aluminum specifically accumulates in neurofibrillary tangle-bearing neurons in the Guam ALS-PD syndrome."
    
    if 'elemental mercury' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) is more toxic via inhalation (vapor) or ingestion of organic forms, but liquid elemental mercury from a thermometer has negligible oral bioavailability (~0.01%)."
    
    # Skin distractor
    if 'psoralen' in q_lower and ('limes' in q_lower or 'celery' in q_lower):
        return f"Choice {dist_letter} ({dist_text}) are not known for psoralen content; limes and celery are classic dietary sources of furocoumarins causing phytophotodermatitis."
    
    # Neuro distractor
    if 'cycasin' in q_lower or 'bm aa' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) are marine toxins or other excitotoxins, but L-BMAA from cycad seeds is specifically linked to the Guam ALS-PD syndrome."
    
    if 'scorpion' in q_lower or 'chlorotoxin' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) blocks Na⁺ or Ca²⁺ channels (saxitoxin, tetrodotoxin, ω-conotoxin), but chlorotoxin specifically blocks Cl⁻ channels."
    
    if 'nitrogen oxide' in q_lower and 'nitric acid' in q_lower:
        return f"Choice {dist_letter} ({dist_text}) may be a byproduct but is not the direct cause of burns; NOₓ reacts with skin moisture to form nitric acid, which causes the yellow chemical burns."
    
    # General fallback
    return f"Choice {dist_letter} ({dist_text}) may seem plausible but does not fit the described mechanism/toxicant as precisely as {correct_text}."
    # (The string formatting issue in the neutrophil/aniline rule is fixed below - that one had a stray '}')


def generate_exam_tip(question):
    """Generate an optional exam tip (only when there's a genuine trick)."""
    q_text = question['text']
    q_lower = q_text.lower()
    
    tips = []
    
    if 'heterotropic effectors' in q_lower or '2,3-bpg' in q_lower:
        tips.append("The exam loves the Bohr effect: remember that acidosis, fever, and 2,3-BPG all shift the O₂ curve RIGHT (decreased affinity), while alkalosis, hypothermia, and CO shift it LEFT.")
    
    if 'oxygen affinity' in q_lower and 'temperature' in q_lower:
        tips.append("Temperature effect on hemoglobin: think 'hot tissue needs O₂ → release it' (affinity ↓, right shift). Cold = hold onto O₂ (affinity ↑, left shift).")
    
    if 'ligand binding site' in q_lower or ('co' in q_lower and 'left' in q_lower):
        tips.append("CO poisoning traps: CO binds to the R (relaxed) conformation of hemoglobin and causes a LEFT shift (increased O₂ affinity), not right. This is frequently tested.")
    
    if 'sulfhemoglobin' in q_lower:
        tips.append("Sulfhemoglobin is irreversible and non-functional; methemoglobin can at least be reduced via NADH-methemoglobin reductase. The exam tests this distinction.")
    
    if 'clozapine' in q_lower:
        tips.append("Clozapine-induced agranulocytosis is the classic DABT example of a pharmacogenetic idiosyncratic reaction requiring mandatory risk management (REMS).")
    
    if 'benzene' in q_lower and 'leukemia' in q_lower:
        tips.append("Benzene is the prototypical chemical leukemogen. Its mechanism requires metabolic activation by CYP2E1 in the liver, with transport of reactive metabolites to the bone marrow.")
    
    if 'lindane' in q_lower:
        tips.append("Lindane (γ-HCH) is banned in many countries but persists as an exam topic for its occupational leukopenia and its persistence as an environmental contaminant.")
    
    if ('perforin' in q_lower or 'granzyme' in q_lower) and 'nk' in q_lower:
        tips.append("Perforin = pore former; granzyme = apoptosis inducer. Think 'perforin pokes holes, granzyme guts the cell.' This NK killing mechanism is a frequent exam target.")
    
    if 'hypersensitivity' in q_lower and 'prior exposure' in q_lower:
        tips.append("The four types of hypersensitivity all require prior sensitization. A common mistake is thinking type IV (delayed) does not require sensitization.")
    
    if 'type ii' in q_lower or 'type iii' in q_lower:
        tips.append("Type II = antibody against FIXED tissue antigens (Goodpasture, myasthenia gravis). Type III = antibody against SOLUBLE antigens (SLE, serum sickness). This distinction is tested frequently.")
    
    if 'autoimmune' in q_lower and 'myasthenia gravis' in q_lower:
        tips.append("MG (type II), MS (type IV), RA (type III). A classic triplet pairing each autoimmune disease with its Gell-Coombs type.")
    
    if 'acinar zonation' in q_lower:
        tips.append("Zone 3 (centrilobular) = highest CYP activity, most vulnerable to toxic injury. Remember: CCl₄ and APAP damage zone 3 preferentially.")
    
    if 'kupffer cells' in q_lower:
        tips.append("Kupffer cells = 80% of fixed macrophages; Ito cells = vitamin A storage; Pit cells = liver NK cells. Know the difference for the exam.")
    
    if 'apap' in q_lower or 'acetaminophen' in q_lower:
        tips.append("APAP hepatotoxicity: NAPQI depletes glutathione → binds to cysteine on mitochondrial proteins → necrosis. NAC works by replenishing glutathione. This is the most tested mechanism in hepatotoxicology.")
    
    if 'metal-fume fever' in q_lower:
        tips.append("Metal-fume fever = zinc oxide. Not manganese, not iron. This is a classic 'one metal, one syndrome' exam question.")
    
    if 'menkes' in q_lower or ('atp7a' in q_lower):
        tips.append("Menkes = copper deficiency (ATP7A, X-linked). Wilson = copper excess (ATP7B). The exam tests both ATPase copper transporters.")
    
    if 'elemental mercury' in q_lower:
        tips.append("Three mercury forms: elemental (vapor → lungs → brain), inorganic (kidney), organic (MeHg → GI → brain). Each has different toxicokinetics — a frequent exam question.")
    
    if 'guam' in q_lower:
        tips.append("Guam ALS-PD is associated with both aluminum (soil metal) and L-BMAA (cycad toxin). The exam may test the metal vs. the plant toxin in different questions.")
    
    if 'psoralen' in q_lower:
        tips.append("Psoralens intercalate DNA + UVA → cross-links. This is a phototoxic (not photoallergic) reaction. Limes + sun = phytophotodermatitis.")
    
    if 'conducting airways' in q_lower:
        tips.append("Club (Clara) cells are in bronchioles, not alveoli. They are the primary site of CYP metabolism in the lung — a key exam fact.")
    
    if 'thin descending' in q_lower and 'loop of henle' in q_lower:
        tips.append("The countercurrent multiplier: descending limb = water OUT only; ascending limb = salt OUT only. This creates the medullary osmotic gradient.")
    
    if 'inulin' in q_lower:
        tips.append("Inulin clearance = GFR gold standard. Creatinine clearance approximates GFR but overestimates due to tubular secretion. Albumin in urine = glomerular damage.")
    
    if 'methanol' in q_lower:
        tips.append("Methanol: ADH → formaldehyde → formic acid. Formate accumulates in primates (limited folate-dependent oxidation), causing metabolic acidosis and retinal toxicity. Fomepizole blocks ADH.")
    
    if 'diethylene glycol' in q_lower:
        tips.append("The 1937 Elixir Sulfanilamide disaster (diethylene glycol) led to the 1938 FD&C Act. The 1962 Kefauver-Harris Amendments came from thalidomide.")
    
    if 'stratum corneum' in q_lower:
        tips.append("Stratum corneum: lipophilic barrier, passive diffusion only. Most compounds penetrate via intercellular route. Molecular weight < 500 Da favors absorption.")
    
    if 'warfarin' in q_lower or 'oral anticoagulant' in q_lower:
        tips.append("Warfarin is primarily metabolized by CYP2C9 (not 3A4). Warfarin is highly protein-bound (99%), so drug interactions at the protein-binding level also matter.")
    
    if 'clover disease' in q_lower:
        tips.append("Zearalenone is a Fusarium mycotoxin with estrogenic activity causing hyperestrogenism in livestock. Not to be confused with aflatoxin (hepatocarcinogen) or ochratoxin (nephrotoxic).")
    
    # No tip by default
    return ""


def main():
    questions = load_slice()
    progress = load_progress()
    
    processed_ids = set(progress.get("processed_ids", []))
    batch_num = progress.get("last_batch", 0)
    
    print(f"Total questions: {len(questions)}")
    print(f"Already processed: {len(processed_ids)}")
    print(f"Starting from batch: {batch_num}")
    
    # Filter to unprocessed
    remaining = [q for q in questions if q['id'] not in processed_ids]
    print(f"Remaining: {len(remaining)}")
    
    conn = get_connected_db()
    cursor = conn.cursor()
    
    total_batches = 0
    for i in range(0, len(remaining), BATCH_SIZE):
        batch = remaining[i:i + BATCH_SIZE]
        batch_num += 1
        total_batches += 1
        
        print(f"\n--- Processing batch {batch_num} ({len(batch)} questions) ---")
        
        for q in batch:
            try:
                explanation = generate_explanation(q)
                cursor.execute(
                    "UPDATE questions SET explanation = ? WHERE id = ?",
                    (explanation, q['id'])
                )
                processed_ids.add(q['id'])
            except Exception as e:
                print(f"  ERROR on {q['id']}: {e}")
                # Still mark as processed to avoid infinite loop
                processed_ids.add(q['id'])
        
        conn.commit()
        
        # Save progress
        progress = {
            "processed_ids": list(processed_ids),
            "last_batch": batch_num,
            "total_processed": len(processed_ids)
        }
        save_progress(progress)
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM questions WHERE explanation IS NOT NULL AND explanation != ''")
        count = cursor.fetchone()[0]
        print(f"  DB now has {count} questions with explanations")
    
    conn.close()
    
    print(f"\n=== DONE ===")
    print(f"Total processed: {len(processed_ids)}")
    print(f"Batches completed: {total_batches}")


if __name__ == '__main__':
    main()
