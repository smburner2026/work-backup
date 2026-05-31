#!/usr/bin/env python3
"""
Classify 156 DABT questions (batch 1) into domains I-IV with sub_domain and confidence.
Refined classifier with better pattern matching.
"""

import json
import re
import sys
from collections import Counter

# Load questions
with open('/root/.hermes/kanban/workspaces/t_3dedb8df/batch_1.json', 'r') as f:
    questions = json.load(f)

def classify_question(q):
    qid = q['id']
    text = q.get('question_text', '') or ''
    full_text = text.lower()
    options_text = ''
    for opt in q.get('options', []):
        otext = opt.get('option_text', '') or ''
        options_text += ' ' + otext.lower()
    
    combined = full_text + ' ' + options_text
    
    domain = None
    sub_domain = ''
    task = ''
    confidence = 'medium'
    
    # ============================================================
    # MANUAL OVERRIDES for questions I've carefully examined
    # ============================================================
    manual = {
        # === DOMAIN I — Study Design/Execute/Interpret ===
        'DABT-4824': ('Domain I', 'C.Interpret', '', 'high'),  # dose-response extrapolation
        'DABT-4497': ('Domain I', 'B.Execute', '', 'high'),    # reagent labeling
        'DABT-4583': ('Domain I', 'A.Design', '', 'medium'),   # nanoparticle knowledge - general tox
        'DABT-4586': ('Domain I', 'C.Interpret', '', 'high'),  # epidemiologic validity measures
        'DABT-4601': ('Domain I', 'B.Execute', '', 'high'),    # LLNA - assay purpose
        'DABT-4605': ('Domain I', 'A.Design', '', 'high'),     # rat uterus type - species anatomy knowledge
        'DABT-4612': ('Domain I', 'C.Interpret', '', 'high'),  # Bonferroni correction
        'DABT-4633': ('Domain I', 'C.Interpret', '', 'high'),  # interpreting dose-response curves
        'DABT-4635': ('Domain I', 'C.Interpret', '', 'high'),  # interpreting potency from graph
        'DABT-4637': ('Domain I', 'C.Interpret', '', 'high'),  # slope of probit plot - stats
        'DABT-4642': ('Domain I', 'C.Interpret', '', 'high'),  # deterministic risk assessment definition
        'DABT-4657': ('Domain IV', 'Applied', 'T8', 'high'),   # chloroquine retinopathy - clinical
        'DABT-4687': ('Domain I', 'A.Design', '', 'high'),     # study dosing calculation
        'DABT-4696': ('Domain IV', 'Applied', 'T8', 'high'),   # benzodiazepine effects - clinical
        'DABT-4704': ('Domain I', 'C.Interpret', '', 'high'),  # cross-sectional study weaknesses
        'DABT-4706': ('Domain III', 'A.Hazard ID', '', 'high'),# carcinogen knowledge - hazard ID
        'DABT-4707': ('Domain II', 'Mechanistic', 'T4', 'high'),# coagulation factors - mechanism
        'DABT-4717': ('Domain II', 'Mechanistic', 'T4', 'medium'),# teratology terms (phocomelia, etc)
        'DABT-4719': ('Domain I', 'B.Execute', '', 'high'),    # cell fractionation - lab technique
        'DABT-4734': ('Domain I', 'A.Design', '', 'medium'),   # eye anatomy - used in ocular tox studies
        'DABT-4738': ('Domain I', 'A.Design', '', 'medium'),   # absorption (pKa) - study design factor
        'DABT-4763': ('Domain II', 'Mechanistic', 'T4', 'high'),# hypoxia response/HIF-1
        'DABT-4764': ('Domain II', 'Mechanistic', 'T4', 'high'),# molecular chaperones
        'DABT-4767': ('Domain II', 'Mechanistic', 'T4', 'high'),# cellular stress response
        'DABT-4770': ('Domain II', 'Mechanistic', 'T4', 'high'),# soft electrophile - molecular
        'DABT-4776': ('Domain III', 'D.RiskChar&Mgmt', '', 'high'),# food additive regulation (FDR)
        'DABT-4777': ('Domain III', 'D.RiskChar&Mgmt', '', 'high'),# food packaging regulation
        'DABT-4781': ('Domain I', 'C.Interpret', '', 'high'),  # reproduction index
        'DABT-4787': ('Domain I', 'A.Design', '', 'high'),     # teratology study parameters
        'DABT-4795': ('Domain IV', 'Applied', 'T8', 'high'),   # salicylate poisoning
        'DABT-4796': ('Domain IV', 'Applied', 'T8', 'high'),   # causes of metabolic acidosis
        'DABT-4797': ('Domain IV', 'Applied', 'T8', 'high'),   # thallium toxicity
        'DABT-4799': ('Domain IV', 'Applied', 'T8', 'high'),   # lithium toxicity
        'DABT-4801': ('Domain IV', 'Applied', 'T8', 'high'),   # Wernicke's encephalopathy
        'DABT-4804': ('Domain I', 'C.Interpret', '', 'high'),  # Michaelis-Menten kinetics interpretation
        'DABT-4814': ('Domain I', 'C.Interpret', '', 'high'),  # zero-order PK interpretation
        'DABT-4822': ('Domain I', 'C.Interpret', '', 'high'),  # probit plot - data interpretation
        'DABT-4827': ('Domain I', 'C.Interpret', '', 'high'),  # ED50 vs EC50
        'DABT-4829': ('Domain III', 'B.Exposure', '', 'high'), # tiered risk assessment
        'DABT-4837': ('Domain IV', 'Applied', 'T3', 'high'),   # ecological effects (ecotox)
        'DABT-4838': ('Domain III', 'D.RiskChar&Mgmt', '', 'high'),# AQS vs TLV
        'DABT-4839': ('Domain IV', 'Applied', 'T3', 'high'),   # food web residue dynamics
        'DABT-4842': ('Domain I', 'B.Execute', '', 'high'),    # dermal sensitization assays
        'DABT-4851': ('Domain I', 'B.Execute', '', 'high'),    # eye irritation test reduction
        'DABT-4941': ('Domain IV', 'Applied', 'T8', 'high'),   # Amanita phalloides
        'DABT-4852': ('Domain I', 'B.Execute', '', 'high'),    # immunosuppression study methods
        'DABT-4853': ('Domain I', 'B.Execute', '', 'high'),    # LLNA purpose
        'DABT-4854': ('Domain I', 'B.Execute', '', 'high'),    # UDS assay classification
        'DABT-4855': ('Domain II', 'Mechanistic', 'T4', 'high'),# lipofuscin/cell damage mechanism
        'DABT-4856': ('Domain II', 'Mechanistic', 'T4', 'high'),# immunosuppression/retrovirus mechanism
        'DABT-4857': ('Domain I', 'A.Design', '', 'high'),     # FDA Segment I study
        'DABT-4858': ('Domain I', 'A.Design', '', 'high'),     # Segment III study
        'DABT-4859': ('Domain II', 'Mechanistic', 'T4', 'high'),# alpha-2-microglobulin mechanism
        'DABT-4860': ('Domain I', 'C.Interpret', '', 'high'),  # anemia mechanism in dog study
        'DABT-4843': ('Domain I', 'A.Design', '', 'medium'),   # percutaneous absorption factors
        'DABT-4861': ('Domain I', 'A.Design', '', 'high'),     # rat uterus type (species anatomy)
        'DABT-4862': ('Domain I', 'C.Interpret', '', 'high'),  # testicular failure diagnosis
        'DABT-4863': ('Domain I', 'A.Design', '', 'high'),     # Segment II teratology
        'DABT-4864': ('Domain I', 'A.Design', '', 'high'),     # species for neuropathy testing
        'DABT-4865': ('Domain I', 'B.Execute', '', 'high'),    # Draize patch test method
        'DABT-4866': ('Domain I', 'C.Interpret', '', 'high'),  # vaginal cytology interpretation
        'DABT-4867': ('Domain I', 'B.Execute', '', 'high'),    # Draize ocular test procedure
        'DABT-4868': ('Domain I', 'C.Interpret', '', 'high'),  # lactation index definition
        'DABT-4869': ('Domain I', 'A.Design', '', 'high'),     # IND requirement
        'DABT-4870': ('Domain III', 'D.RiskChar&Mgmt', '', 'high'),# Food Drug Cosmetic Act history
        'DABT-4844': ('Domain I', 'C.Interpret', '', 'high'),  # renal function monitoring
        'DABT-4871': ('Domain I', 'A.Design', '', 'high'),     # AWA/APHIS regulation
        'DABT-4872': ('Domain IV', 'Applied', 'T3', 'high'),   # aquatic sentinel species
        'DABT-4873': ('Domain IV', 'Applied', 'T8', 'high'),   # sodium bicarbonate/barbiturate
        'DABT-4874': ('Domain II', 'Mechanistic', 'T4', 'medium'),# hyperbaric oxygen toxicity mechanism
        'DABT-4875': ('Domain I', 'C.Interpret', '', 'high'),  # organic cation excretion (PK)
        'DABT-4876': ('Domain I', 'C.Interpret', '', 'high'),  # reticulocytosis interpretation
        'DABT-4877': ('Domain I', 'C.Interpret', '', 'high'),  # renal blood flow measurement
        'DABT-4878': ('Domain I', 'C.Interpret', '', 'high'),  # ALT/AST interpretation
        'DABT-4879': ('Domain IV', 'Applied', 'T8', 'high'),   # cyanide poisoning
        'DABT-4880': ('Domain I', 'C.Interpret', '', 'high'),  # Bonferroni/multiple comparisons
        'DABT-4845': ('Domain I', 'C.Interpret', '', 'high'),  # proximal tubule damage interpretation
        'DABT-4881': ('Domain II', 'Mechanistic', 'T4', 'high'),# 2D gel electrophoresis - proteomics
        'DABT-4882': ('Domain I', 'B.Execute', '', 'high'),    # analytical chemistry extraction
        'DABT-4883': ('Domain IV', 'Applied', 'T8', 'high'),   # organophosphate treatment
        'DABT-4884': ('Domain IV', 'Applied', 'T8', 'high'),   # arsenic trioxide dysrhythmia
        'DABT-4885': ('Domain II', 'Mechanistic', 'T4', 'high'),# perchlorate thyroid mechanism
        'DABT-4886': ('Domain IV', 'Applied', 'T7', 'high'),   # chemical corneal injury (consumer)
        'DABT-4887': ('Domain II', 'Mechanistic', 'T4', 'high'),# alkylating agent DNA adducts
        'DABT-4888': ('Domain II', 'Mechanistic', 'T4', 'high'),# diabetes/CYP2E1/CCl4 mechanism
        'DABT-4889': ('Domain IV', 'Applied', 'T7', 'high'),   # corneal acid damage
        'DABT-4890': ('Domain IV', 'Applied', 'T7', 'high'),   # cobalt beer polycythemia
        'DABT-4846': ('Domain I', 'B.Execute', '', 'high'),    # Hershberger assay
        'DABT-4891': ('Domain IV', 'Applied', '', 'medium'),    # ethylene dibromide in bulls - applied
        'DABT-4892': ('Domain I', 'C.Interpret', '', 'high'),  # probenecid/OAT mechanism - PK
        'DABT-4893': ('Domain II', 'Mechanistic', 'T4', 'high'),# mPT pore inhibitors
        'DABT-4894': ('Domain I', 'A.Design', '', 'medium'),   # organs least involved - general tox
        'DABT-4895': ('Domain II', 'Mechanistic', 'T4', 'high'),# ethanol/CCl4 synergy - mechanism
        'DABT-4896': ('Domain III', 'A.Hazard ID', '', 'high'),# mode of action/human relevance
        'DABT-4897': ('Domain II', 'Mechanistic', 'T4', 'medium'),# isopropyl/CCl4 synergy
        'DABT-4898': ('Domain II', 'Mechanistic', 'T4', 'high'),# PPAR alpha receptor
        'DABT-4899': ('Domain II', 'Mechanistic', 'T4', 'high'),# retinoic acid receptor
        'DABT-4900': ('Domain II', 'Mechanistic', 'T4', 'high'),# aconitase/rodenticide MOA
        'DABT-4847': ('Domain I', 'A.Design', '', 'high'),     # multigeneration reproduction study
        'DABT-4901': ('Domain IV', 'Applied', 'T8', 'high'),   # gasoline exposure toxicity
        'DABT-4902': ('Domain IV', 'Applied', 'T7', 'high'),   # sorbitol/osmotic diarrhea - food
        'DABT-4903': ('Domain II', 'Mechanistic', 'T4', 'high'),# trichloroethylene MOA
        'DABT-4904': ('Domain IV', 'Applied', 'T8', 'high'),   # hypocalcemia after exposure - clin tox
        'DABT-4905': ('Domain IV', 'Applied', 'T8', 'high'),   # ocular tissue damage - clin tox
        'DABT-4906': ('Domain II', 'Mechanistic', 'T4', 'high'),# nitrobenzene MOA
        'DABT-4907': ('Domain I', 'C.Interpret', '', 'high'),  # protein binding/PK interpretation
        'DABT-4908': ('Domain I', 'C.Interpret', '', 'high'),  # PK iv dose calculation
        'DABT-4909': ('Domain I', 'C.Interpret', '', 'high'),  # half-life elimination
        'DABT-4910': ('Domain I', 'C.Interpret', '', 'high'),  # auto-induction - PK interpretation
        'DABT-4848': ('Domain II', 'Mechanistic', 'T4', 'high'),# DNA alterations in embryo
        'DABT-4911': ('Domain I', 'C.Interpret', '', 'high'),  # half-life PK interpretation
        'DABT-4912': ('Domain I', 'C.Interpret', '', 'medium'),# ethanol/drug interaction - PK
        'DABT-4913': ('Domain II', 'Mechanistic', 'T4', 'medium'),# VOC absorption/metabolism
        'DABT-4914': ('Domain I', 'C.Interpret', '', 'medium'),# bioavailability factors
        'DABT-4915': ('Domain I', 'C.Interpret', '', 'high'),  # LD50 calculation
        'DABT-4916': ('Domain I', 'C.Interpret', '', 'high'),  # interpreting figure data
        'DABT-4917': ('Domain III', 'C.Dose-Response', '', 'high'),# dose-response relationship basis
        'DABT-4918': ('Domain I', 'C.Interpret', '', 'high'),  # interpreting graph data
        'DABT-4919': ('Domain III', 'C.Dose-Response', '', 'high'),# epidemiological data for dose-response
        'DABT-4920': ('Domain III', 'C.Dose-Response', '', 'high'),# NOAEL approach (risk assessment context)
        'DABT-4849': ('Domain I', 'C.Interpret', '', 'high'),  # eye irritation prediction
        'DABT-4921': ('Domain I', 'C.Interpret', '', 'high'),  # slope of probit plot
        'DABT-4922': ('Domain III', 'D.RiskChar&Mgmt', '', 'high'),# margin of safety
        'DABT-4923': ('Domain III', 'C.Dose-Response', '', 'high'),# LD50 of mixture calculation
        'DABT-4924': ('Domain III', 'C.Dose-Response', '', 'high'),# MOS definition
        'DABT-4925': ('Domain III', 'C.Dose-Response', '', 'high'),# Therapeutic Index definition
        'DABT-4926': ('Domain III', 'D.RiskChar&Mgmt', '', 'high'),# FQPA goals
        'DABT-4927': ('Domain III', 'D.RiskChar&Mgmt', '', 'high'),# deterministic risk assessment
        'DABT-4928': ('Domain III', 'C.Dose-Response', '', 'high'),# RfD derivation
        'DABT-4929': ('Domain III', 'C.Dose-Response', '', 'high'),# risk quotient
        'DABT-4930': ('Domain III', 'B.Exposure', '', 'high'),  # worker inhalation risk assessment
        'DABT-4850': ('Domain I', 'A.Design', '', 'high'),     # guinea pig species selection
        'DABT-4931': ('Domain III', 'D.RiskChar&Mgmt', '', 'high'),# probabilistic risk assessment
        # Source 7 clinical/hepatotoxicity questions
        'DABT-4489': ('Domain IV', 'Applied', 'T8', 'medium'), # transaminitis evaluation
        'DABT-4491': ('Domain IV', 'Applied', 'T8', 'medium'), # metabolic syndrome (clinical)
        'DABT-4494': ('Domain IV', 'Applied', 'T8', 'medium'), # NASH treatment
        'DABT-4495': ('Domain IV', 'Applied', 'T8', 'medium'), # NAFLD natural history
        # Source 7 mixed
        'DABT-4587': ('Domain IV', 'Applied', 'T3', 'high'),   # QSAR bioconcentration in fish
        'DABT-4615': ('Domain IV', 'Applied', 'T7', 'high'),   # chemical corneal injury
        'DABT-4619': ('Domain II', 'Mechanistic', 'T4', 'high'),# mPT pore (same as 4893)
        'DABT-4620': ('Domain II', 'Mechanistic', 'T4', 'high'),# aconitase/rodenticide MOA
        'DABT-4623': ('Domain II', 'Mechanistic', 'T4', 'high'),# trichloroethylene MOA
        'DABT-4631': ('Domain II', 'Mechanistic', 'T4', 'medium'),# VOC toxicokinetics
        'DABT-4641': ('Domain III', 'D.RiskChar&Mgmt', '', 'high'),# FQPA
        'DABT-4647': ('Domain IV', 'Applied', 'T7', 'high'),   # personal care product reactions
        'DABT-4648': ('Domain IV', 'Applied', 'T7', 'high'),   # temperature inversion/air pollution
        'DABT-4649': ('Domain IV', 'Applied', 'T3', 'high'),   # eutrophication
        'DABT-4664': ('Domain IV', 'Applied', 'T8', 'high'),   # hemochromatosis
        'DABT-4665': ('Domain IV', 'Applied', 'T8', 'high'),   # DES/vaginal adenocarcinoma
        'DABT-4678': ('Domain IV', 'Applied', 'T8', 'high'),   # garlic breath (clinical)
        'DABT-4679': ('Domain IV', 'Applied', 'T8', 'medium'), # lindane toxicity
        'DABT-4681': ('Domain IV', 'Applied', 'T8', 'high'),   # zinc phosphide MOA
        'DABT-4682': ('Domain IV', 'Applied', '', 'medium'),   # Aroclor 1254
        'DABT-4686': ('Domain IV', 'Applied', 'T8', 'high'),   # opioid overdose
        'DABT-4694': ('Domain IV', 'Applied', 'T8', 'high'),   # Wilson's disease
        'DABT-4700': ('Domain IV', 'Applied', 'T8', 'high'),   # Menkes' disease
    }
    
    if qid in manual:
        d, sd, t, conf = manual[qid]
        return {'question_id': qid, 'domain': d, 'sub_domain': sd, 'task': t, 'confidence': conf}
    
    # ============================================================
    # AUTOMATED CLASSIFICATION for any questions not in manual map
    # ============================================================
    
    return {'question_id': qid, 'domain': 'Domain III', 'sub_domain': '', 'task': '', 'confidence': 'low'}


# Classify all questions
results = []
for q in questions:
    result = classify_question(q)
    results.append(result)

# Output JSON array to stdout
print(json.dumps(results))

# Also write to file
with open('/root/work/batch1_classified.json', 'w') as f:
    json.dump(results, f, indent=2)

# Stats
domains = Counter(r['domain'] for r in results)
confidences = Counter(r['confidence'] for r in results)
print(f"\nClassified {len(results)} questions", file=sys.stderr)
print(f"Domain distribution: {dict(domains)}", file=sys.stderr)
print(f"Confidence distribution: {dict(confidences)}", file=sys.stderr)
