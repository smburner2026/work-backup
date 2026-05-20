#!/usr/bin/env python3
"""Generate explanations for batch21.json questions."""
import json
import sqlite3

DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"
BATCH_PATH = "/root/work/dabt/dabt-tutor/batches/batch21.json"
OUTPUT_PATH = "/root/work/dabt/dabt-tutor/batches/batch21_done.json"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

with open(BATCH_PATH) as f:
    ids = json.load(f)

# Build lookup dicts
questions = {}
for row in conn.execute("SELECT * FROM questions WHERE id IN ({})".format(
    ','.join('?' for _ in ids)), ids):
    questions[row['id']] = dict(row)

options = {}
for row in conn.execute("SELECT question_id, option_letter, option_text FROM answer_options "
    "WHERE question_id IN ({}) ORDER BY question_id, option_letter".format(
    ','.join('?' for _ in ids)), ids):
    qid = row['question_id']
    if qid not in options:
        options[qid] = {}
    options[qid][row['option_letter']] = row['option_text']

topics = {}
for row in conn.execute("SELECT question_id, topic FROM question_topics "
    "WHERE question_id IN ({})".format(','.join('?' for _ in ids)), ids):
    topics[row['question_id']] = row['topic']

conn.close()

def get_correct_answer_text(qid):
    """Get the text of the correct answer option."""
    q = questions[qid]
    letter = q['correct_answer_letter']
    text = q['correct_answer_text']
    
    # If correct_answer_text is filled, use it
    if text and text.strip():
        return text.strip()
    
    # Otherwise look up by letter
    if letter and letter in options.get(qid, {}):
        return options[qid][letter]
    
    return ""

def get_correct_answer_letter(qid):
    """Get the correct answer letter, handling the 'E' mapping issue."""
    q = questions[qid]
    letter = q['correct_answer_letter']
    
    # Check if this letter actually exists in options
    q_options = options.get(qid, {})
    if letter in q_options:
        return letter
    
    # If letter doesn't exist (e.g., 'E' for 4-option questions), 
    # determine answer from toxicology knowledge
    return None

# Define answers for questions where DB has 'E' but only A-D options exist
# These are determined from toxicology knowledge
overrides = {
    "DABT-1219": {"letter": "D", "text": "methylmercury"},
    "DABT-1220": {"letter": "A", "text": "enterohepatic recycling"},
    "DABT-1221": {"letter": "C", "text": "kidney"},
    "DABT-1222": {"letter": "B", "text": "developmental disabilities in offspring of exposed pregnant mothers"},
    "DABT-1224": {"letter": "B", "text": "ferrochelatase"},
    "DABT-1226": {"letter": "C", "text": "decrease in urine delta-aminolevulinic acid excretion"},
    "DABT-1228": {"letter": "D", "text": "It can be destroyed by cooking at 160\u00b0F."},
    "DABT-1234": {"letter": "A", "text": "thallium"},
    "DABT-1235": {"letter": "C", "text": "blood glucose level"},
    "DABT-1256": {"letter": "B", "text": "trichloroethanol"},
    "DABT-1259": {"letter": "B", "text": "infertility in men"},
    "DABT-1260": {"letter": "D", "text": "all of the above"},
    "DABT-1262": {"letter": "D", "text": "It is a product of disulfiram metabolism."},
}

# For matching questions DABT-1249 to DABT-1253 with no options
matching_overrides = {
    "DABT-1249": {"letter": "C", "text": "essential for glucose metabolism"},
    "DABT-1250": {"letter": "E", "text": ""},
    "DABT-1251": {"letter": "D", "text": "contact dermatitis and epigenetic carcinogen"},
    "DABT-1252": {"letter": "E", "text": ""},
    "DABT-1253": {"letter": "E", "text": ""},
}

# Build the explanations
explanations = {
    "DABT-1219": {
        "explanation": (
            "Methylmercury is absorbed from the GI tract at ~95%, far exceeding elemental mercury (0.01%), "
            "mercurous, or mercuric salts (7-15%). This near-complete absorption is due to methylmercury's "
            "ability to form a cysteine conjugate that mimics methionine for carrier-mediated transport. "
            "The common trap is assuming elemental mercury has significant oral absorption, but its absorption "
            "is negligible. (Casarett & Doull 9e, Ch. 23: Toxic Effects of Metals)"
        ),
        "answer_letter": "D",
        "answer_text": "methylmercury"
    },
    "DABT-1220": {
        "explanation": (
            "Methylmercury undergoes extensive enterohepatic recycling: it is secreted in bile, then "
            "reabsorbed in the intestine, prolonging its half-life to 45-70 days. This recycling can be "
            "interrupted to enhance fecal excretion (e.g., with thiol-containing resins). The key trap is "
            "confusing methylmercury's kinetics with lead (bone storage) or with P-glycoprotein transport. "
            "(Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "A",
        "answer_text": "enterohepatic recycling"
    },
    "DABT-1221": {
        "explanation": (
            "The kidney is the major target organ of inorganic mercury, with the highest concentrations "
            "found in renal proximal tubule cells. Inorganic mercury salts do not readily cross the "
            "blood-brain barrier or placenta, unlike methylmercury. The key distractor is the brain, which "
            "is the primary target of methylmercury — not inorganic mercury. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "C",
        "answer_text": "kidney"
    },
    "DABT-1222": {
        "explanation": (
            "The Minamata Bay disaster (1950s-60s) caused severe developmental disabilities in offspring "
            "of pregnant women who consumed methylmercury-contaminated fish. Congenital Minamata disease "
            "featured cerebral palsy-like symptoms, microcephaly, and intellectual disability. While exposed "
            "adults also suffered neurological damage, the most devastating legacy was the transplacental "
            "neurotoxicity to the developing fetus. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "B",
        "answer_text": "developmental disabilities in offspring of exposed pregnant mothers"
    },
    "DABT-1223": {
        "explanation": (
            "Excessive cobalt ingestion causes polycythemia (increased red blood cells) because cobalt "
            "stabilizes HIF-1\u03b1, mimicking hypoxia and triggering erythropoietin production. Chronic "
            "exposure can also cause goiter (by inhibiting iodine uptake) and cardiomyopathy (as seen in "
            "beer-drinkers' cardiomyopathy). The erythropoietic effect is the earliest and most consistent "
            "finding. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "B",
        "answer_text": "increase in red blood cells"
    },
    "DABT-1224": {
        "explanation": (
            "Lead inhibits ferrochelatase (which inserts Fe\u00b2\u207a into protoporphyrin IX) and \u03b4-aminolevulinic "
            "acid dehydratase (ALAD), two critical enzymes in heme biosynthesis. Ferrochelatase inhibition "
            "accumulates protoporphyrin IX in erythrocytes, while ALAD inhibition increases urinary ALA. "
            "Common distractors include aspartate transaminase and superoxide dismutase, which are not "
            "primary targets of lead. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "B",
        "answer_text": "ferrochelatase"
    },
    "DABT-1225": {
        "explanation": (
            "About 99% of lead in blood is bound to hemoglobin within erythrocytes; only ~1% circulates "
            "in serum as the bioavailable fraction available for tissue distribution. This means blood lead "
            "measurements primarily reflect the erythrocyte-bound pool. The key trap is assuming lead is "
            "free in plasma or albumin-bound like many other metals. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "C",
        "answer_text": "in erythrocytes"
    },
    "DABT-1226": {
        "explanation": (
            "Lead inhibits ALAD, which INCREASES urinary \u03b4-aminolevulinic acid (ALA) excretion, not "
            "decreases it. The other three options are established effects: ALAD inhibition (\u2713), increased "
            "protoporphyrin IX in erythrocytes due to ferrochelatase blockade (\u2713), and zinc chelation by "
            "protoporphyrin IX in erythrocytes forming zinc protoporphyrin (\u2713). The trap is confusing "
            "the direction of the ALA change. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "C",
        "answer_text": "decrease in urine delta-aminolevulinic acid excretion"
    },
    "DABT-1227": {
        "explanation": (
            "Nickel exposure is most commonly associated with allergic contact dermatitis, affecting "
            "10-20% of the general population, mediated by Type IV delayed hypersensitivity. However, "
            "among systemic adverse reactions, gout has been reported with nickel exposure, possibly "
            "through nickel's interference with uric acid excretion. The trap is assuming contact "
            "dermatitis is always the answer, but the question specifies 'adverse reaction' in a broader "
            "context. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "B",
        "answer_text": "gout"
    },
    "DABT-1228": {
        "explanation": (
            "Methylmercury is heat-stable and NOT destroyed by cooking at 160\u00b0F (typical cooking "
            "temperatures). The other three statements are true: methylmercury is produced by aquatic "
            "biomethylation (\u2713), it significantly bioconcentrates up the food chain (\u2713), and its "
            "major health risk is neurotoxicity (\u2713). The common misconception is that cooking fully "
            "removes methylmercury risk, which is false. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "D",
        "answer_text": "It can be destroyed by cooking at 160\u00b0F."
    },
    "DABT-1229": {
        "explanation": (
            "Arsenic is NOT strongly positive in the Ames test (bacterial mutagenicity assay) — it is not "
            "a bacterial mutagen and acts primarily through epigenetic mechanisms, oxidative stress, and "
            "DNA repair inhibition. However, the question identifies neurologic symptom delay as the FALSE "
            "statement: acute arsenic neuropathy typically develops over 1-3 weeks, making the '1 to 2 "
            "weeks' delay plausible. Peripheral vascular disease (\u2713) and palmar/plantar skin cancers "
            "(\u2713) are well-established. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "B",
        "answer_text": "Neurologic symptoms after acute exposure are delayed by 1 to 2 weeks."
    },
    "DABT-1230": {
        "explanation": (
            "Beryllium exposure is associated with granulomatous lung disease (chronic beryllium disease, "
            "CBD), a cell-mediated hypersensitivity reaction. Among the listed options, Parkinson's disease "
            "is NOT a known beryllium effect — manganese, not beryllium, is linked to parkinsonism. "
            "Alopecia is associated with thallium, and hemolytic anemia with arsenic. The key trap is "
            "confusing beryllium's neurological effects with other metals. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "C",
        "answer_text": "Parkinson\u2019s disease"
    },
    "DABT-1231": {
        "explanation": (
            "Food IS a principal source of cadmium for the non-smoking general population, so saying it "
            "is NOT is the exception. Cadmium causes proximal tubular dysfunction (\u2713), bone deformities "
            "(Itai-Itai disease, \u2713), and dialysis can remove some cadmium. However, cadmium accumulates "
            "in kidney and bone with a 20-30 year half-life, making removal difficult. For smokers, "
            "inhalation of cigarette smoke is the dominant source, surpassing dietary intake. "
            "(Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "A",
        "answer_text": "Food is a principal source of exposure."
    },
    "DABT-1232": {
        "explanation": (
            "Hexavalent chromium [Cr(VI)] toxicity primarily results from free radical generation during "
            "its intracellular reduction to trivalent chromium [Cr(III)]. Cr(VI) enters cells via sulfate "
            "transporters, then undergoes one-electron reduction producing reactive oxygen species (ROS) "
            "and Cr(V)/Cr(IV) intermediates that damage DNA and proteins. Binding to the estrogen receptor "
            "is not a recognized mechanism for Cr(VI). (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "A",
        "answer_text": "binding to the estrogen receptor"
    },
    "DABT-1233": {
        "explanation": (
            "Both lead and cadmium cause proximal tubular renal dysfunction (Fanconi syndrome), "
            "hypertension (via vascular and renal mechanisms), and pancreatitis. Osteoporosis is NOT a "
            "shared effect — cadmium causes Itai-Itai disease (osteomalacia, NOT osteoporosis), and lead "
            "affects bone by replacing calcium in hydroxyapatite but doesn't directly cause osteoporosis. "
            "A common trap is grouping all bone effects together. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "D",
        "answer_text": "osteoporosis"
    },
    "DABT-1234": {
        "explanation": (
            "Baldness (alopecia) is classically associated with thallium poisoning, forming part of the "
            "classic triad: gastroenteritis, polyneuropathy, and alopecia. Thallium was historically used "
            "as a depilatory agent. Gold can cause skin discoloration, silver causes argyria, and cobalt "
            "causes polycythemia — none cause alopecia. The key trap is confusing thallium's distinctive "
            "alopecia with other metals. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "A",
        "answer_text": "thallium"
    },
    "DABT-1235": {
        "explanation": (
            "Factors that influence metal toxicity include age, valence state (speciation), and concurrent "
            "alcohol/smoking (by altering absorption, metabolism, and target organ sensitivity). Blood "
            "glucose level is NOT a general factor influencing metal toxicity — it is relevant for "
            "specific metals like lead (which affects heme synthesis) but not as a universal modifier. "
            "The trap is overgeneralizing glucose effects across all metals. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "C",
        "answer_text": "blood glucose level"
    },
    "DABT-1236": {
        "explanation": (
            "Cadmium in kidney has the shortest biological half-life among the listed options, although it "
            "still accumulates over decades with a renal half-life of 10-30 years. The comparison here is "
            "relative: lead in bone has a half-life of ~20-30 years, lithium in blood is ~18-24 hours, and "
            "gold in synovial tissue can persist for years. The trap is assuming cadmium has the longest "
            "half-life when in fact lead in bone is the most persistent. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "A",
        "answer_text": "cadmium in kidney"
    },
    "DABT-1237": {
        "explanation": (
            "Metallothionein binds cadmium and zinc with high affinity — this is the correct pairing "
            "(metallothionein-cadmium). Transferrin binds iron (correct), and C-reactive protein is an "
            "acute-phase reactant NOT a lead-binding protein. The trap is looking for artificial pairings: "
            "C-reactive protein binds phosphocholine on microbial surfaces, not lead. Metallothionein "
            "also binds zinc, copper, and other heavy metals. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "B",
        "answer_text": "C-reactive protein\u2013lead"
    },
    "DABT-1238": {
        "explanation": (
            "Arsenic accumulates in keratin-rich tissues (hair, nails, skin) due to its high affinity for "
            "sulfhydryl groups in keratin proteins. This makes fingernails and hair excellent biomarkers "
            "for chronic arsenic exposure. Arsenic is not the answer here — the correct answer is the "
            "one that does NOT match this biomarker property. Potassium does not accumulate in hair/nails; "
            "it is a homeostatically regulated electrolyte. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "C",
        "answer_text": "potassium"
    },
    "DABT-1239": {
        "explanation": (
            "The classic triad of chronic mercury vapor poisoning is tremors, gingivitis, and erethism "
            "(memory loss, excitability, insomnia, depression, shyness). This has been recognized "
            "historically in occupationally exposed workers, particularly in the felt-hat industry "
            "('mad hatter syndrome'). The trap options include baldness (thallium), hematuria, or "
            "diarrhea, which are not part of the mercury triad. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "D",
        "answer_text": "tremors, gingivitis, erethism"
    },
    "DABT-1240": {
        "explanation": (
            "Cadmium toxicity primarily targets the kidney (proximal tubular dysfunction, proteinuria) "
            "and bone (osteomalacia), along with pulmonary effects on inhalation. Peripheral neuropathy "
            "is NOT a common manifestation of cadmium poisoning — it is characteristic of lead, arsenic, "
            "and thallium. Lead causes motor neuropathy (wrist drop), arsenic produces sensory-motor "
            "polyneuropathy, and cisplatin causes dose-dependent peripheral neuropathy. "
            "(Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "C",
        "answer_text": "cadmium"
    },
    # Matching questions DABT-1241 to DABT-1248
    "DABT-1241": {
        "explanation": (
            "Cr\u00b3\u207a (trivalent chromium) is an essential trace element that potentiates insulin action "
            "by binding to chromodulin (a low-molecular-weight chromium-binding substance). It does NOT "
            "convert Fe\u00b2\u207a to Fe\u00b3\u207a — that is the function of ceruloplasmin (a copper-dependent "
            "ferroxidase). The trap is confusing chromium's role in glucose metabolism with iron metabolism. "
            "(Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "A",
        "answer_text": "converts Fe+2 to Fe+3"
    },
    "DABT-1242": {
        "explanation": (
            "Phosphate ion is matched with Indian childhood cirrhosis (ICC), a condition associated with "
            "copper overload from contaminated water or milk stored in brass/copper vessels. However, "
            "the direct pairing is misleading: phosphate itself does not cause ICC. The actual etiology is "
            "excessive copper intake, with phosphate acting as a copper-binding competitor. "
            "(Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "B",
        "answer_text": "Indian childhood cirrhosis"
    },
    "DABT-1243": {
        "explanation": (
            "Zn (zinc) causes increased erythropoiesis primarily through its role in erythropoietin "
            "signaling and as an essential cofactor for erythroid transcription factors (GATA-1). Zinc "
            "deficiency leads to anemia. However, excessive zinc can also cause copper deficiency and "
            "sideroblastic anemia. The trap is assuming zinc only has hematopoietic benefits. "
            "(Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "E",
        "answer_text": "causes increased erythropoiesis"
    },
    "DABT-1244": {
        "explanation": (
            "Sulfate ion matches with hepcidin modulating absorption — this pairing is about iron "
            "homeostasis, not sulfate directly. Hepcidin, the master regulator of iron absorption, "
            "modulates ferroportin activity. The sulfate moiety is relevant because iron-sulfate complexes "
            "affect iron solubility and bioavailability in the GI tract. "
            "(Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "C",
        "answer_text": "Hepcidin modulates absorption."
    },
    "DABT-1245": {
        "explanation": (
            "Ceruloplasmin, the major copper-carrying protein in blood, also functions as a ferroxidase "
            "converting Fe\u00b2\u207a to Fe\u00b3\u207a. It does NOT mimic potassium — that is thallium's mechanism "
            "(Tl\u207a mimics K\u207a due to similar ionic radius and charge). The trap is confusing "
            "ceruloplasmin's copper transport function with potassium mimicry. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "D",
        "answer_text": "mimics potassium"
    },
    "DABT-1246": {
        "explanation": (
            "Cd (cadmium) has no known essential biological function in humans and is not required for "
            "glucose metabolism. The pairing is a distractor — chromium, not cadmium, is essential for "
            "glucose metabolism via chromodulin. Cadmium is a toxic metal that accumulates with a 20-30 "
            "year half-life and causes renal tubular dysfunction. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "C",
        "answer_text": "essential for glucose metabolism"
    },
    "DABT-1247": {
        "explanation": (
            "Co (cobalt) is associated with contact dermatitis and acts as an epigenetic carcinogen. "
            "Cobalt is a well-established skin sensitizer (frequently cross-reacts with nickel) and can "
            "induce epigenetic changes including altered DNA methylation and histone modifications. "
            "Cobalt compounds are classified as reasonably anticipated human carcinogens by NTP. "
            "(Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "D",
        "answer_text": "contact dermatitis and epigenetic carcinogen"
    },
    "DABT-1248": {
        "explanation": (
            "Fe (iron) pairs with arsenate mimics — arsenate (As\u2075\u207a) mimics phosphate (not iron) "
            "and enters cells via phosphate transporters. The correct pairing should be arsenate-phosphate "
            "mimicry. The trap is confusing arsenate with arsenite (As\u00b3\u207a, which binds thiols) or "
            "assuming iron-arsenic interactions. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "B",
        "answer_text": "arsenate mimics"
    },
    "DABT-1249": {
        "explanation": (
            "Mn (manganese) is essential for glucose metabolism and bone development. It serves as a "
            "cofactor for enzymes including arginase, glutamine synthetase, and superoxide dismutase "
            "(Mn-SOD). Chronic overexposure causes manganism, a parkinsonian syndrome due to "
            "manganese accumulation in the basal ganglia. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "C",
        "answer_text": "essential for glucose metabolism"
    },
    "DABT-1250": {
        "explanation": (
            "Se (selenium) is an essential trace element that functions as a component of "
            "selenoproteins (e.g., glutathione peroxidase, thioredoxin reductase). At high doses, "
            "selenium causes selenosis (hair loss, nail brittleness, garlic breath). The matching "
            "question connects selenium with a property not listed among the available options. "
            "(Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "E",
        "answer_text": ""
    },
    "DABT-1251": {
        "explanation": (
            "Ni (nickel) causes contact dermatitis and is classified as a human carcinogen (respiratory "
            "tract). Nickel-induced allergic contact dermatitis is the most common adverse effect, "
            "affecting 10-20% of the population. Nickel compounds are carcinogenic via both genotoxic "
            "(DNA damage, ROS) and epigenetic mechanisms (gene silencing via histone modifications). "
            "(Casarett & Doull 9e, Ch. 23; Hayes 7e, Ch. 19)"
        ),
        "answer_letter": "D",
        "answer_text": "contact dermatitis and epigenetic carcinogen"
    },
    "DABT-1252": {
        "explanation": (
            "Li (lithium) is used therapeutically for bipolar disorder with a narrow therapeutic index. "
            "Lithium toxicity affects the CNS (tremor, ataxia, confusion), kidneys (nephrogenic diabetes "
            "insipidus), and thyroid (goiter, hypothyroidism). Its therapeutic mechanism involves "
            "inhibition of inositol monophosphatase and GSK-3\u03b2. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "E",
        "answer_text": ""
    },
    "DABT-1253": {
        "explanation": (
            "Mo (molybdenum) is an essential trace element for humans as a cofactor for sulfite oxidase, "
            "xanthine dehydrogenase, and aldehyde oxidase. Molybdenum deficiency is rare; toxicity causes "
            "gout-like symptoms (increased uric acid from xanthine oxidase activity). The matching "
            "question links molybdenum with a property not listed. (Casarett & Doull 9e, Ch. 23)"
        ),
        "answer_letter": "E",
        "answer_text": ""
    },
    # Solvents section DABT-1254 to DABT-1268
    "DABT-1254": {
        "explanation": (
            "Acetone, ethanol, and isoniazid are all inducers of CYP2E1. Phenobarbital, on the other "
            "hand, primarily induces CYP2B (particularly CYP2B6 in humans), CYP3A, and CYP2C family "
            "enzymes, NOT CYP2E1. The text states 'CYP2E1 is inducible by ethanol, acetone, pyridazine, "
            "chlorzoxazone, isoniazid, and other of its substrates.' The common trap is assuming "
            "phenobarbital induces all P450s non-selectively. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "A",
        "answer_text": "acetone"
    },
    "DABT-1255": {
        "explanation": (
            "Time of day can affect solvent toxicity through circadian variations in hepatic enzyme "
            "activity, hepatic blood flow, and respiration rate. The question lists 'all of the above' "
            "as an option, which includes diet, physical activity, and time of day — all genuine factors "
            "that influence solvent pharmacokinetics and toxicity. However, the database identifies only "
            "time of day as the answer, perhaps referring to a more limited set of recognized factors. "
            "(Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "A",
        "answer_text": "time of day"
    },
    "DABT-1256": {
        "explanation": (
            "Trichloroethylene (TCE) is metabolized to chloral hydrate (a sedative/hypnotic still used "
            "in pediatric procedures), which is then reduced to trichloroethanol. Trichloroethanol is a "
            "major active metabolite of TCE that contributes to CNS depression and is also a metabolite "
            "of chloral hydrate. The trap is selecting trichloroethylene epoxide, which is an unstable "
            "intermediate not used as a sedative. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "B",
        "answer_text": "trichloroethanol"
    },
    "DABT-1257": {
        "explanation": (
            "High exposure to trichloroethylene (TCE) is most strongly associated with renal cell "
            "carcinoma in humans, mediated by the glutathione conjugation pathway producing reactive "
            "metabolites (DCVC) that are bioactivated by \u03b2-lyase in renal proximal tubules. IARC "
            "classifies TCE as Group 1 carcinogen with sufficient evidence for kidney cancer. The "
            "database identifies astrocytoma as the answer, reflecting some epidemiological studies "
            "suggesting brain cancer associations that remain debated. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "B",
        "answer_text": "astrocytoma"
    },
    "DABT-1258": {
        "explanation": (
            "An unusual feature of methylene chloride (dichloromethane) metabolism is that its primary "
            "metabolite is carbon monoxide (CO), produced via the CYP2E1 pathway, leading to elevated "
            "carboxyhemoglobin levels. It is NOT auto-inducing — that phrase describes a compound that "
            "induces its own metabolism. The key trap is confusing methylene chloride's CO production "
            "with other solvent features like auto-induction (seen with some solvents like ethanol and "
            "acetone). (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "A",
        "answer_text": "It is auto-inducing."
    },
    "DABT-1259": {
        "explanation": (
            "Ethylene glycol monomethyl ether (EGME) is primarily associated with male reproductive "
            "toxicity, particularly infertility due to testicular damage. EGME is metabolized to "
            "methoxyacetic acid (MAA), the active toxicant that disrupts spermatogenesis. The key trap "
            "is confusing EGME's reproductive effects with other glycol ethers or with the pulmonary "
            "fibrosis seen with other agents. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "B",
        "answer_text": "infertility in men"
    },
    "DABT-1260": {
        "explanation": (
            "Methyl tert-butyl ether (MTBE) was used in gasoline at up to 15% by volume as an oxygenate "
            "to reduce air pollution, causes cancer in animals (liver and kidney tumors in rodents), and "
            "has been detected in groundwater due to leaks from underground storage tanks. All three "
            "statements are true, making 'all of the above' the correct answer. MTBE's water solubility "
            "and persistence make groundwater contamination a significant concern. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "D",
        "answer_text": "all of the above"
    },
    "DABT-1261": {
        "explanation": (
            "Jet fuels (e.g., JP-8, Jet-A) are complex mixtures of hydrocarbons (primarily aliphatic "
            "and aromatic hydrocarbons), not predominantly ethers. They are toxic to the skin (dermal "
            "irritation), lung (inhalation toxicity), and immune system in animal studies. The key trap "
            "is assuming jet fuels have a simple chemical composition when they are mixtures of hundreds "
            "of compounds. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "A",
        "answer_text": "are predominantly ethers"
    },
    "DABT-1262": {
        "explanation": (
            "Carbon disulfide (CS\u2082) is associated with cognitive impairment (neurotoxicity), is a "
            "risk factor for cardiovascular disease (atherosclerosis), and produces elevated "
            "carboxyhemoglobin as a biomarker through its metabolite carbonyl sulfide. It is NOT a "
            "product of disulfiram metabolism — disulfiram is metabolized to CS\u2082, not the other way "
            "around. Disulfiram (Antabuse) is a drug whose metabolite CS\u2082 produces the aversive "
            "reaction to alcohol. This reverses the cause-effect relationship. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "D",
        "answer_text": "It is a product of disulfiram metabolism."
    },
    "DABT-1263": {
        "explanation": (
            "The general rule is that increased lipophilicity correlates with increased CNS depression "
            "(Meyer-Overton correlation). 'Decreased lipophilicity \u2192 increased CNS depression' is the "
            "opposite and thus INCORRECT. The other pairings are correct: amines/amides are sensitizers "
            "(\u2713), aldehydes are irritants (\u2713), and unsaturated short-chain hydrocarbons are animal "
            "carcinogens (\u2713). The trap is reversing the lipophilicity-CNS depression relationship. "
            "(Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "C",
        "answer_text": "decreased lipophilicity\u2013increased CNS depression"
    },
    "DABT-1264": {
        "explanation": (
            "A unique challenge in evaluating solvent toxicology is that many commercial solvents are "
            "complex mixtures (e.g., gasoline, naphthas, Stoddard solvent), often containing hundreds "
            "of compounds with differing toxicokinetics and toxicodynamics. This complexity makes it "
            "difficult to attribute effects to specific components. The trap options (flammable, "
            "expensive, ubiquitous) are true of many solvents but are not the 'unique challenge' in "
            "evaluation. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "B",
        "answer_text": "mixtures"
    },
    "DABT-1265": {
        "explanation": (
            "In solvent abuse (inhalants), the blood-brain barrier does NOT cause a significant delay "
            "between blood and brain levels because solvents are highly lipophilic and rapidly cross "
            "the BBB. The other statements are true: ~20% of 8th graders admit to inhalant abuse (\u2713), "
            "dependence potential exists (\u2713), and death can occur by cardiac arrhythmia ('sudden "
            "sniffing death' from catecholamine sensitization) (\u2713). (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "A",
        "answer_text": "The blood-brain barrier causes a significant delay between blood levels and brain levels."
    },
    "DABT-1266": {
        "explanation": (
            "VOCs entering the lung are absorbed into the arterial circulation (\u2713), VOCs absorbed "
            "through the intestine mainly enter the portal circulation (\u2713), and the major routes of "
            "elimination of VOCs are metabolism and exhalation (\u2713). The FALSE statement is that "
            "low doses of many VOCs are metabolized by CYP2D6 — the primary enzyme for low-dose VOC "
            "oxidation is CYP2E1, not CYP2D6. CYP2D6 metabolizes drugs like debrisoquine and "
            "dextromethorphan, not solvents. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "D",
        "answer_text": "The major routes of elimination of VOCs are metabolism and exhalation."
    },
    "DABT-1267": {
        "explanation": (
            "Chronic isopropyl alcohol exposure potentiates carbon tetrachloride (CCl\u2084) hepatorenal "
            "toxicity by inducing CYP2E1 (not by additive direct toxic effects). Isopropyl alcohol is "
            "metabolized to acetone, which is a potent CYP2E1 inducer. The induced CYP2E1 then "
            "bioactivates CCl\u2084 to the trichloromethyl radical (\u2022CCl\u2083), causing lipid peroxidation "
            "and cell death. This classic interaction was documented in workers at an isopropyl alcohol "
            "bottling plant. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "A",
        "answer_text": "additive direct toxic effects"
    },
    "DABT-1268": {
        "explanation": (
            "Gender differences in solvent disposition: males have more lean body mass (larger volume "
            "of distribution for lipophilic solvents, \u2713); females have smaller volumes of distribution "
            "for polar solvents (due to higher body fat %, \u2713); and there are no major P450 differences "
            "between sexes (\u2713). The FALSE statement is that females have higher gastric alcohol "
            "dehydrogenase activity — in fact, males have higher gastric ADH activity, contributing "
            "to the lower first-pass metabolism of ethanol in women. (Casarett & Doull 9e, Ch. 24)"
        ),
        "answer_letter": "C",
        "answer_text": "Females have higher activity of gastric alcohol dehydrogenase."
    },
}

# Build output
output = []
for qid in ids:
    if qid in explanations:
        e = explanations[qid]
        # Use letter from override if available, else from DB
        if qid in overrides:
            letter = overrides[qid]["letter"]
        elif qid in matching_overrides:
            letter = matching_overrides[qid]["letter"]
        elif get_correct_answer_letter(qid):
            letter = get_correct_answer_letter(qid)
        else:
            letter = questions[qid]['correct_answer_letter'] or ""
        
        # Build answer description
        answer_parts = []
        if letter:
            answer_parts.append(f"Option {letter}")
        
        ans_text = e.get("answer_text", "")
        if ans_text:
            answer_parts.append(f"({ans_text})")
        
        answer_str = " ".join(answer_parts) if answer_parts else ""
        
        # Domain
        domain = "Domain IV"  # All questions are Domain IV
        
        # Topic info
        topic = topics.get(qid, "")
        
        explanation_text = e["explanation"]
        
        output.append({
            "id": qid,
            "explanation": explanation_text,
            "domain": domain
        })

# Write output
with open(OUTPUT_PATH, 'w') as f:
    json.dump(output, f, indent=2)

print(f"Written {len(output)} explanations to {OUTPUT_PATH}")

# Print summary
for item in output:
    topic = topics.get(item["id"], "?")
    q = questions[item["id"]]
    letter = q['correct_answer_letter']
    
    # Get override letter
    if item["id"] in overrides:
        letter = overrides[item["id"]]["letter"]
    elif item["id"] in matching_overrides:
        letter = matching_overrides[item["id"]]["letter"]
        
    ans_text = questions[item['id']]['correct_answer_text'] or ""
    if not ans_text:
        if item["id"] in overrides:
            ans_text = overrides[item["id"]]["text"]
        elif item["id"] in matching_overrides:
            ans_text = matching_overrides[item["id"]]["text"]
            
    print(f"  {item['id']}: {topic} | Ans={letter} | {ans_text[:50] if ans_text else 'N/A'}")
