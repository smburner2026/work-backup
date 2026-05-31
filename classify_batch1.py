#!/usr/bin/env python3
"""
Classify 156 DABT questions (batch 1) into domains I-IV with sub_domain and confidence.
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
    # Build full context
    options_text = ''
    for opt in q.get('options', []):
        otext = opt.get('option_text', '') or ''
        options_text += ' ' + otext.lower()
    
    combined = full_text + ' ' + options_text
    
    # Initialize results
    domain = None
    sub_domain = ''
    task = ''
    confidence = 'medium'
    
    # ============================================================
    # DOMAIN IV — Applied Toxicology (check first since it has very specific signals)
    # ============================================================
    # Clinical toxicology / antidotes / poisoning
    domain_iv_signals = {
        'antidote': ('Applied', 'T8'),
        'prussian blue': ('Applied', 'T8'),
        'naloxone': ('Applied', 'T8'),
        'flumazenil': ('Applied', 'T8'),
        'atropine': ('Applied', 'T8'),
        'pralidoxime': ('Applied', 'T8'),
        'fomepizole': ('Applied', 'T8'),
        'n-acetylcysteine': ('Applied', 'T8'),
        'sodium bicarbonate': ('Applied', 'T8'),
        'chelation': ('Applied', 'T8'),
        'dimercaprol': ('Applied', 'T8'),
        'british anti-lewisite': ('Applied', 'T8'),
        'succimer': ('Applied', 'T8'),
        
        # Clinical tox specific
        'organophosphorus pesticide poisoning': ('Applied', 'T8'),
        'opioid overdose': ('Applied', 'T8'),
        'barbiturate poisoning': ('Applied', 'T8'),
        'cyanide poisoning': ('Applied', 'T8'),
        'lithium toxicity': ('Applied', 'T8'),
        'thallium': ('Applied', 'T8'),
        'salicylate': ('Applied', 'T8'),
        'metabolic acidosis': ('Applied', 'T8'),
        'respiratory alkalosis': ('Applied', 'T8'),
        'garlic breath': ('Applied', 'T8'),
        
        # Heavy metals / clinical tox
        'wilson\'s disease': ('Applied', 'T8'),
        'menkes\' disease': ('Applied', 'T8'),
        'hemochromatosis': ('Applied', 'T8'),
        'hereditary hemochromatosis': ('Applied', 'T8'),
        'wernicke\'s encephalopathy': ('Applied', 'T8'),
        'chloroquine-induced retinopathy': ('Applied', 'T8'),
        'vaginal adenocarcinoma': ('Applied', 'T8'),
        'diethylstilbestrol': ('Applied', 'T8'),
        'amanita phalloides': ('Applied', 'T8'),
        'death cap': ('Applied', 'T8'),
        
        # Ecotoxicology
        'ecotoxicolog': ('Applied', 'T3'),
        'daphnia magna': ('Applied', 'T3'),
        'daphnia': ('Applied', 'T3'),
        'eutrophication': ('Applied', 'T3'),
        'aquatic toxicology': ('Applied', 'T3'),
        'bioconcentration in fish': ('Applied', 'T3'),
        'food web residue': ('Applied', 'T3'),
        'microcosm': ('Applied', 'T3'),
        'sentinel species for aquatic': ('Applied', 'T3'),
        'skeletonema': ('Applied', 'T3'),
        'microcystis': ('Applied', 'T3'),
        'pimephales': ('Applied', 'T3'),
        'oncorhynchus': ('Applied', 'T3'),
        'temperature inversion': ('Applied', 'T7'),
        'air quality standards': ('Applied', 'T7'),
        'threshold limit value': ('Applied', 'T7'),
        
        # Public health / consumer
        'personal care products': ('Applied', 'T7'),
        'cosmetic': ('Applied', 'T7'),
        'food quality protection act': ('Applied', 'T7'),  # Actually risk assessment, but FQPA is regulatory
        'elixir of sulphanilamide': ('Applied', 'T7'),
        'food, drug and cosmetic act': ('Applied', 'T7'),
        'sorbitol': ('Applied', 'T7'),
        'osmotic diarrhea': ('Applied', 'T7'),
    }
    
    # Check for strong Domain IV signals
    for signal, (sub, t) in domain_iv_signals.items():
        if signal in combined:
            # But verify it's not a mechanism question
            if 'mechanism' in full_text and signal not in ['wilson\'s disease', 'menkes\' disease', 'hemochromatosis']:
                # Could be Domain II if asking about mechanism
                pass
            else:
                # Check FQPA - this is actually Domain III
                if signal == 'food quality protection act':
                    domain = 'Domain III'
                    sub_domain = 'D.RiskChar&Mgmt'
                    task = ''
                    confidence = 'high'
                    return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
                if signal == 'air quality standards':
                    domain = 'Domain III'
                    sub_domain = 'D.RiskChar&Mgmt'
                    task = ''
                    confidence = 'high'
                    return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
                if signal == 'threshold limit value':
                    domain = 'Domain III'
                    sub_domain = 'D.RiskChar&Mgmt'
                    task = ''
                    confidence = 'high'
                    return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
                
                domain = 'Domain IV'
                sub_domain = sub
                task = t
                confidence = 'high'
                return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
    
    # More Domain IV: specific chemical toxicity / poisoning
    dom_iv_patterns = [
        (r'\b(benzodiazepines?|organophosphate|organophosphorus)\b.*\b(toxic|poison|overdose|antidote|effect)', 'Applied', 'T8'),
        (r'\b(zinc phosphide|rodenticide)\b', 'Applied', 'T8'),
        (r'\b(lindane|hexachlorocyclohexane)\b', 'Applied', ''),
        (r'\b(aroclor|pcbs?)\b', 'Applied', ''),
        (r'\b(gasoline|hydrocarbons?)\b.*\b(exposure|toxic|pneumonitis)', 'Applied', 'T8'),
        (r'\b(nash|nafld|fatty liver|steatosis)\b', 'Applied', ''),
        (r'\b(transaminitis|hepatitis)\b', 'Applied', ''),
        (r'\b(metabolic syndrome)\b', 'Applied', ''),
        (r'\b(cheese.*mold inhibitor|mold inhibitor.*cheese)\b', 'Applied', ''),
        (r'\bplastic manufacturer.*packaging\b', 'Applied', ''),
        (r'\bperchlorate.*thyroid\b', 'Applied', ''),
        (r'\b(cobalt.*beer|polycythemia.*cobalt)\b', 'Applied', ''),
        (r'\bethylene dibromide\b', 'Applied', ''),
    ]
    
    for pattern, dom, t in dom_iv_patterns:
        if re.search(pattern, combined):
            domain = 'Domain IV'
            sub_domain = 'Applied'
            task = t
            confidence = 'high' if t else 'medium'
            return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
    
    # ============================================================
    # DOMAIN II — Mechanistic Toxicology
    # ============================================================
    dom_ii_signals = [
        # Mitochondrial/cell death mechanisms
        'mitochondrial permeability transition pore', 'mpt pore', 'cyclosporin a',
        'hydrophobic bile acids', 'bongkrekic acid', 'l-deprenyl',
        'apoptosis', 'necrosis', 'autophagy',
        'hypoxia response', 'hif-1 alpha', 'erythropoietin',
        'molecular chaperone',
        'cellular stress response',
        'soft electrophile', 'hard electrophile', 'electrophile',
        'dna adduct', 'o6-alkylguanine', 'n7-alkylguanine',
        'alkylating agent',
        'unscheduled dna synthesis',
        'cyp2e1', 'cyp450', 'cytochrome p450',
        'bioactivation', 'reactive metabolite',
        'ppar alpha', 'peroxisome proliferator',
        'retinoic acid receptor', 'rar',
        'mode of action', 'mechanism of action',
        'alpha-2micro-globulin', 'alpha-2-microglobulin',
        'protein droplet', 'male rat.*kidney',
        'hens?.*peripheral neuropathy',
        'testicular failure.*fs(h|sh)',
        'spermatogenesis',
        'vaginal cells.*pseudo-pregnancy',
        'pseudo-pregnancy',
        'lipofuscin',
        'carbon tetrachloride.*damage',
        'diabetes.*hepatotoxicity.*carbon tetrachloride',
        'her2', 'signal transduction',
        'genotoxic', 'non-genotoxic',
        'carcinogenesis',
        'endocrine disruption',
        'hers(hberger|berman) assay',
        'immunosuppression',
        'humoral immune',
        't-cell dependent antibody',
        'local lymph node assay', 'llna',
        'skin sensitization',
        'dermal sensitization',
        'guinea pig maximization',
        'buehler', 'klecak',
        'split adjuvant',
        'spleen weight', 'thymus weight',
        'phagocytosis',
        'endogenous retrovirus',
        'hematologic malignancies',
    ]
    
    dom_ii_count = sum(1 for s in dom_ii_signals if s in combined)
    
    # Check for Domain II patterns
    dom_ii_patterns = [
        (r'enzyme\s+(aconitase|that\s+is\s+blocked)', 'Mechanistic'),
        (r'\b(krebs|tricarboxylic acid)\b.*\bcycle\b', 'Mechanistic'),
        (r'\b(trichloroethylene)\b.*\b(dcvc|reactive metabolite|ppar|estrogen receptor)\b', 'Mechanistic'),
        (r'\b(moa|mechanism)\b.*\b(toxic|carcinogen|cancer)\b', 'Mechanistic'),
        (r'\breactive\s+metabolite\b', 'Mechanistic'),
        (r'\b(coagulation factors?|factor\s+(v|vii|viii|ix|xii)|prothrombin time|partial thromboplastin)\b', 'Mechanistic'),
        (r'\b(phocomelia|syndactyly|adactyly|micromelia)\b', 'Mechanistic'),
        (r'\bsupernatant fraction.*(microsome|nuclear|lysosome|mitochondrial)\b', 'Mechanistic'),
        (r'\b(absor(bed|ption))\b.*\b(intestine|pka)\b', 'Mechanistic'),
        (r'\bvolatile organic compounds?\b.*\b(voc|absorbed|metabolized|elimination)\b', 'Mechanistic'),
        (r'\bclearance\b.*\b(michaelis|menten)\b', 'Mechanistic'),
        (r'\bzero order\b.*\b(pharmacokinetic|elimination)\b', 'Mechanistic'),
        (r'\b(ed50|ec50|ld50|lc50|td50)\b', 'Mechanistic'),
        (r'\bslope.*probit\b', 'Mechanistic'),
        (r'\bprobit plot\b', 'Mechanistic'),
        (r'\b(rat.*uterus|uterus.*rat|bicornuate|duplex|simplex)\b', 'Mechanistic'),
        (r'\blactation index.*rats\b', 'Mechanistic'),
        (r'\b(testicular failure|serum.*(fs(h|sh)|luteinizing|testosterone|estrogen))\b', 'Mechanistic'),
        (r'\bstress response', 'Mechanistic'),
        (r'\bpolyacrylamide gel\b', 'Mechanistic'),
        (r'\bproteins expressed\b.*\bfluids or tissues\b', 'Mechanistic'),
        (r'\b(human tissue sample.*extract|acidic drugs|basic drugs|organic solvent)\b', 'Mechanistic'),
        (r'\barocl(or|)\s*1254\b', 'Mechanistic'),
        (r'\bwarfarin\b', 'Mechanistic'),
        (r'\binulin\b.*\bclearance\b', 'Mechanistic'),
        (r'\bpara-?aminohippuric\b', 'Mechanistic'),
        (r'\bcreatinine\b.*\bclearance\b', 'Mechanistic'),
        (r'\bprobenecid\b', 'Mechanistic'),
        (r'\b(organic anion transporter|oat)\b', 'Mechanistic'),
        (r'\bretinal vasoconstriction|hyperbaric oxygen.*photoreceptor\b', 'Mechanistic'),
        (r'\bperipheral reticulocytosis\b', 'Mechanistic'),
        (r'\b(renal blood flow|renal clearance)\b', 'Mechanistic'),
    ]
    
    for pattern, sub in dom_ii_patterns:
        if re.search(pattern, combined):
            domain = 'Domain II'
            sub_domain = 'Mechanistic'
            task = 'T4'
            confidence = 'high' if dom_ii_count > 1 else 'medium'
            return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
    
    if dom_ii_count >= 2:
        domain = 'Domain II'
        sub_domain = 'Mechanistic'
        task = 'T4'
        confidence = 'high'
        return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
    
    # ============================================================
    # DOMAIN I — Conduct of Toxicological Studies
    # ============================================================
    dom_i_signals = {
        'B.Design': [
            'experimental design', 'dose selection', 'species selection',
            'route of administration', 'study duration', 'number of animals',
            'glp', 'good laboratory practice', 'ich guideline',
            'test guideline', 'study protocol', 'randomization', 'blinding',
            'positive control', 'negative control', 'vehicle control',
            'power analysis', 'oecd tg', 'oppts', 'fda redbook',
            'study design', 'animal welfare act', 'aphis',
            'department of agriculture', 'nda', 'ind', 'investigational new drug',
            'fda segment', 'segment i', 'segment ii', 'segment iii',
            'classical teratology study', 'multigeneration reproduction',
            'reproductive toxicology', 'teratology study',
            '28-day study', 'repeat dose',
            'how much test article', 'mg/kg/day',
            'before.*can be given to humans',
            '1906 food and drugs act', '1938 food, drug and cosmetic act',
        ],
        'B.Execute': [
            'dosing technique', 'sample collection', 'necropsy',
            'histopathology', 'clinical observation', 'body weight',
            'food consumption', 'ophthalmology', 'ecg',
            'clinical pathology', 'hematology', 'clinical chemistry',
            'urinalysis', 'tissue processing', 'data quality', 'sop',
            'chain of custody', 'specimen labeling', 'qa/qc', 'audit',
            'reagents must be labeled',
            'primary irritation of the skin', 'patch-test', 'draize',
            'ocular irritancy', 'conjunctival sac',
            'corneal opacity', 'pannus', 'iritis',
            '0.5 ml', '0.5 g', '0.1 ml',
            'primary dermal irritation',
            'abraded.*skin', 'intact skin',
            'eye irritation test',
            'strong acid.*ph 2', 'strong alkali.*ph 11',
        ],
        'C.Interpret': [
            'data interpretation', 'statistical analysis',
            't-test', 'anova', 'dunnett', 'chi-square',
            'fisher\'s exact', 'trend test',
            'dose-response analysis', 'noael', 'loael',
            'benchmark dose', 'reference value',
            'clinical significance', 'statistical significance',
            'histopathology findings', 'clinical pathology data',
            'toxicokinetic data', 'across-study comparison',
            'multiple endpoints',
            'bonferroni correction', 'multiple comparisons',
            'type i error', 'type ii error',
            'dose vs. response', 'low dosage levels', 'extrapolation',
            'probabilistic risk assessment', 'tier 1', 'tier 2', 'tier 3',
            'deterministic risk assessment',
            'single numerical value',
            'sensitivity.*specificity', 'epidemiologic studies',
            'cross-sectional.*studies',
            'validity.*epidemiologic',
            'reticulocytosis',
            'alanine aminotransferase', 'alt.*ast', 'sorbitol dehydrogenase',
            'liver toxicant', 'leakage of enzymes',
            'kidney findings.*male rats.*female',
            'decrease in red blood cells.*mechanism.*anemia',
            'hemolysis', 'erythropoiesis',
        ],
    }
    
    for sub, signals in dom_i_signals.items():
        for s in signals:
            if s in combined:
                # But check if it's really a mechanism question
                if s in ['noael', 'loael'] and 'risk' in full_text:
                    # This could be Domain III
                    pass  # Will be caught below
                elif s == 'probabilistic risk assessment':
                    # This is actually Domain III
                    pass
                else:
                    domain = 'Domain I'
                    sub_domain = sub
                    task = ''
                    confidence = 'high' if len(s) > 10 else 'medium'
                    return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
    
    # More Domain I patterns
    dom_i_patterns = [
        (r'\b(study.*dosage|dosage.*study|dosage.*response.*chronic)\b', 'C.Interpret', ''),
        (r'\bcross-sectional\b', 'C.Interpret', ''),
        (r'\bsensitivity.*specificity\b', 'C.Interpret', ''),
        (r'\b(validity|precision).*epidemiologic\b', 'C.Interpret', ''),
        (r'\bbonferroni\b', 'C.Interpret', ''),
        (r'\bfda.*segment\b', 'A.Design', ''),
        (r'\b(segment i|segment ii|segment iii)\b', 'A.Design', ''),
        (r'\bmultigeneration reproduction\b', 'A.Design', ''),
        (r'\bclassical teratology\b', 'A.Design', ''),
        (r'\breproductive toxicology\b', 'A.Design', ''),
        (r'\bteratology study\b', 'A.Design', ''),
        (r'\b(study|test).*(rat|dog|mouse|rabbit|guinea pig|hen|hamster)\b', 'A.Design', ''),
        (r'\bwhich.*species\b.*\b(test|study|toxic)\b', 'A.Design', ''),
        (r'\banimal species of choice\b', 'A.Design', ''),
        (r'\b28.day\b.*\bstudy\b', 'A.Design', ''),
        (r'\bmg/kg/day\b.*\b(study|test)\b', 'A.Design', ''),
        (r'\bhow much test article\b', 'A.Design', ''),
        (r'\b(nda|ind|investigational new drug)\b', 'A.Design', ''),
        (r'\bgood laboratory practice\b', 'A.Design', ''),
        (r'\banimal welfare act\b', 'A.Design', ''),
        (r'\baphis\b', 'A.Design', ''),
        (r'\bdepartment of agriculture\b', 'A.Design', ''),
        (r'\b1906 food\b', 'A.Design', ''),
        (r'\b1938 food\b', 'A.Design', ''),
        (r'\belixir of sulphanilamide\b', 'A.Design', ''),
        (r'\bprimary irritation of the skin\b', 'B.Execute', ''),
        (r'\bdraize\b', 'B.Execute', ''),
        (r'\bpatch.test\b', 'B.Execute', ''),
        (r'\bocular irritancy\b', 'B.Execute', ''),
        (r'\b(eye irritation|primary eye irritation)\b', 'B.Execute', ''),
        (r'\b(local lymph node|llna)\b', 'B.Execute', ''),
        (r'\bgene mutation|chromosome aberration|dominant lethal|reverse mutation\b', 'B.Execute', ''),
        (r'\bunscheduled dna synthesis\b', 'B.Execute', ''),
        (r'\bspleen weight\b', 'B.Execute', ''),
        (r'\bthymus weight\b', 'B.Execute', ''),
        (r'\bt.cell dependent antibody\b', 'B.Execute', ''),
        (r'\bhumoral immune\b', 'B.Execute', ''),
        (r'\bguinea pig maximization\b', 'B.Execute', ''),
        (r'\bbuehler\b', 'B.Execute', ''),
        (r'\bklecak\b', 'B.Execute', ''),
        (r'\bsplit adjuvant\b', 'B.Execute', ''),
        (r'\bwhich.*not.*assay.*dermal sensitization\b', 'B.Execute', ''),
        (r'\breagents must be labeled\b', 'B.Execute', ''),
        (r'\b(serum.*(alt|ast)|alanine aminotransferase|aspartate aminotransferase)\b', 'C.Interpret', ''),
        (r'\bsorbitol dehydrogenase\b', 'C.Interpret', ''),
        (r'\b(proximal convoluted tubule|proximal tubule)\b', 'C.Interpret', ''),
        (r'\b(aminoaciduria|proteinuria)\b', 'C.Interpret', ''),
        (r'\bphenolsulfonphthalein|sulfobromophthalein\b', 'C.Interpret', ''),
        (r'\b(clearance of|renal function|glomerular filtration)\b', 'C.Interpret', ''),
        (r'\b(blood urea nitrogen|bun)\b', 'C.Interpret', ''),
        (r'\burine (osmolarity|volume|ph)\b', 'C.Interpret', ''),
        (r'\bexcretion of sodium and potassium\b', 'C.Interpret', ''),
        (r'\bdecrease in red blood cells\b', 'C.Interpret', ''),
        (r'\bmechanism.*anemia\b', 'C.Interpret', ''),
        (r'\bhemolysis\b', 'C.Interpret', ''),
        (r'\bsugar alcohols.*osmotic diarrhea\b', 'C.Interpret', ''),
    ]
    
    for pattern, sub, t in dom_i_patterns:
        if re.search(pattern, combined):
            # Check for false positives
            if sub == 'B.Execute' and ('local lymph node' in combined or 'llna' in combined):
                domain = 'Domain I'
                sub_domain = sub
                task = ''
                confidence = 'high'
                return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
            
            domain = 'Domain I'
            sub_domain = sub
            task = t
            confidence = 'high'
            return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
    
    # ============================================================
    # DOMAIN III — Risk Assessment
    # ============================================================
    dom_iii_signals = {
        'A.Hazard ID': [
            'hazard identification', 'weight of evidence',
            'epidemiology', 'case report', 'cohort study', 'case-control',
            'iarc', 'ntp conclusion', 'epa weight of evidence',
            'known human carcinogen',
        ],
        'B.Exposure': [
            'exposure assessment', 'occupational exposure',
            'environmental exposure', 'consumer exposure',
            'pbpk', 'biomarker of exposure', 'biomonitoring equivalent',
            'nhanes', 'aggregate exposure', 'cumulative exposure',
            'uncertainty factor.*exposure',
        ],
        'C.Dose-Response': [
            'dose-response', 'noael', 'loael', 'benchmark dose',
            'low-dose extrapolation', 'linear.*threshold',
            'relative potency factor', 'toxic equivalency factor',
            'bmd', 'rfd', 'rfc', 'slope factor',
            'margin of exposure', 'allometric scaling',
        ],
        'D.RiskChar&Mgmt': [
            'risk characterization', 'risk communication',
            'risk management', 'margin of safety',
            'hazard quotient', 'hazard index',
            'mcl', 'pel', 'tlv', 'adi', 'tdi',
            'ptwi', 'uncertainty factor',
            'intraspecies', 'interspecies',
            'fqpa', 'food quality protection act',
            'delaney clause', 'threshold of toxicological concern',
            'threshold of regulation',
            'osha pel', 'niosh rel', 'acgih tlv',
            'risk.*clean.up', 'risk.*cleanup',
            'risk assessment',
            'probabilistic risk assessment',
            'deterministic risk assessment',
            'tier 1', 'tier 2', 'tier 3',
            'air quality standard',
            'threshold limit value',
            'food web residue',
        ],
    }
    
    for sub, signals in dom_iii_signals.items():
        for s in signals:
            if s in combined:
                domain = 'Domain III'
                sub_domain = sub
                task = ''
                confidence = 'high'
                return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
    
    # More Domain III patterns
    dom_iii_patterns = [
        (r'\brisk assess', 'D.RiskChar&Mgmt'),
        (r'\bdeterministic risk', 'D.RiskChar&Mgmt'),
        (r'\bprobabilistic risk', 'D.RiskChar&Mgmt'),
        (r'\btier (1|2|3)\b.*\bcomplexity\b', 'D.RiskChar&Mgmt'),
        (r'\bair quality (standard|aqs)\b', 'D.RiskChar&Mgmt'),
        (r'\bthreshold limit value|tlv\b', 'D.RiskChar&Mgmt'),
        (r'\bfood web residue\b', 'D.RiskChar&Mgmt'),
        (r'\btoxic chemical effects.*reduce.*biomass.*population\b', 'B.Exposure'),
        (r'\bkilling of.*(symbiont|prey|courtship)\b', 'B.Exposure'),
        (r'\begg.*shell\b', 'B.Exposure'),
        (r'\bnoael|loael\b', 'C.Dose-Response'),
        (r'\brfd|rfc|adi|tolerable daily|acceptable daily\b', 'D.RiskChar&Mgmt'),
        (r'\buncertainty factor\b', 'D.RiskChar&Mgmt'),
        (r'\bmargin of (safety|exposure)\b', 'D.RiskChar&Mgmt'),
        (r'\brat.*carcinogen.*not.*relevant.*human\b', 'A.Hazard ID'),
        (r'\bunleaded gasoline.*renal tumor.*male rat\b', 'A.Hazard ID'),
        (r'\bno relevance to humans\b', 'A.Hazard ID'),
        (r'\badditive effect|synerg(y|istic)|potentiation\b', 'C.Dose-Response'),
        (r'\bmode of action.*carcinogen\b', 'A.Hazard ID'),
    ]
    
    for pattern, sub in dom_iii_patterns:
        if re.search(pattern, combined):
            domain = 'Domain III'
            sub_domain = sub
            task = ''
            confidence = 'high'
            return {'question_id': qid, 'domain': domain, 'sub_domain': sub_domain, 'task': task, 'confidence': confidence}
    
    # ============================================================
    # FALLBACK — use keyword counts
    # ============================================================
    # Count keywords for each domain
    dom_i_kw = ['study', 'test', 'dosage', 'dose', 'species', 'animal', 'rat', 'mouse',
                'glp', 'protocol', 'experiment', 'design', 'sensitivity', 'specificity',
                'statistical', 'analysis', 'interpret', 'serum', 'clinical pathology',
                'hematology', 'tissue', 'necropsy', 'histopathology', 'segment',
                'teratology', 'reproduction', 'fertility', 'lactation', 'patch',
                'irritation', 'corneal', 'ophthalmology', 'ophthalmic']
    
    dom_ii_kw = ['mechanism', 'molecular', 'cellular', 'receptor', 'enzyme', 'pathway',
                 'gene', 'dna', 'protein', 'apoptosis', 'necrosis', 'oxidative',
                 'metabolite', 'cyp', 'bioactivation', 'signal', 'transduction',
                 'mitochondrial', 'peroxisome', 'mutagen', 'carcinogen',
                 'immune', 'antibody', 'sensitization', 'lymphocyte',
                 'electrophile', 'nucleophile', 'alkylating', 'adduct']
    
    dom_iii_kw = ['risk', 'exposure', 'hazard', 'safety', 'standard', 'limit',
                  'regulation', 'regulatory', 'epa', 'fda', 'osha', 'threshold',
                  'noael', 'loael', 'reference', 'uncertainty', 'margin',
                  'assessment', 'population', 'public', 'environmental',
                  'food', 'water', 'air', 'contaminant', 'biomonitoring']
    
    dom_iv_kw = ['poison', 'antidote', 'treatment', 'overdose', 'toxic', 'clinical',
                 'patient', 'syndrome', 'diagnosis', 'therapy', 'acute',
                 'chronic', 'heavy metal', 'lead', 'mercury', 'arsenic',
                 'ecotox', 'aquatic', 'daphnia', 'fish', 'algae',
                 'consumer', 'product', 'cosmetic', 'food safety',
                 'nash', 'nafld', 'liver disease', 'hepatitis',
                 'wilson', 'menkes', 'hemochromatosis']
    
    scores = {
        'Domain I': sum(1 for k in dom_i_kw if k in combined),
        'Domain II': sum(1 for k in dom_ii_kw if k in combined),
        'Domain III': sum(1 for k in dom_iii_kw if k in combined),
        'Domain IV': sum(1 for k in dom_iv_kw if k in combined),
    }
    
    # Get best domain
    sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_domain = sorted_domains[0][0]
    best_score = sorted_domains[0][1]
    
    if best_score >= 3:
        domain = best_domain
        confidence = 'medium'
    elif best_score >= 1:
        domain = best_domain
        confidence = 'low'
    else:
        # Last resort
        domain = 'Domain III'
        confidence = 'low'
    
    return {'question_id': qid, 'domain': domain, 'sub_domain': '', 'task': '', 'confidence': confidence}


# Classify all questions
results = []
for q in questions:
    result = classify_question(q)
    results.append(result)

# Output JSON array
print(json.dumps(results, indent=2))

# Also write to file for verification
with open('/root/work/batch1_classified.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nClassified {len(results)} questions", file=sys.stderr)

# Count by domain
from collections import Counter
domains = Counter(r['domain'] for r in results)
print(f"Domain distribution: {dict(domains)}", file=sys.stderr)
