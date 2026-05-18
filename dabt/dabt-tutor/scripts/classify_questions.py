import pandas as pd
import json

DB_PATH = '/home/vthen/work/dabt-tutor/reference/Claude_import/DABT_Practice_Questions_Database.xlsx'
df = pd.read_excel(DB_PATH, sheet_name='Questions')
print(f"Loaded {len(df)} questions")

topic_to_domain = {
    'General Principles & Concepts': ('I', 'A.Design', 'T1', 'high'),
    'General Toxicology': ('I', 'C.Interpret', 'T1', 'medium'),
    'Toxicokinetics / ADME': ('I', 'B.Execute', 'T2', 'medium'),
    'Biotransformation / Metabolism': ('I', 'C.Interpret', 'T4', 'medium'),
    'Mechanisms of Toxicity': ('II', 'Mechanistic', 'T1', 'high'),
    'Carcinogenesis & Mutagenesis': ('II', 'Mechanistic', 'T4', 'high'),
    'Genotoxicity / DNA Damage': ('II', 'Mechanistic', 'T1', 'high'),
    'Risk Assessment & Regulatory': ('III', 'D.RiskChar&Mgmt', 'T1', 'medium'),
    'Metals & Metalloids': ('IV', 'Applied', 'T11', 'medium'),
    'Solvents & Hydrocarbons': ('IV', 'Applied', 'T11', 'medium'),
    'Pesticides – Insecticides': ('IV', 'Applied', 'T11', 'medium'),
    'Pesticides – Herbicides': ('IV', 'Applied', 'T11', 'medium'),
    'Pesticides – Rodenticides': ('IV', 'Applied', 'T11', 'medium'),
    'Pesticides – Fumigants': ('IV', 'Applied', 'T11', 'medium'),
    'Gases – Asphyxiants & Irritants': ('IV', 'Applied', 'T11', 'medium'),
    'Air Pollution & Particulates': ('IV', 'Applied', 'T3', 'medium'),
    'Drugs & Therapeutics – Toxicology': ('IV', 'Applied', 'T8', 'high'),
    'Plant Toxins': ('IV', 'Applied', 'T11', 'medium'),
    'Animal & Microbial Venoms / Toxins': ('IV', 'Applied', 'T11', 'medium'),
    'Mycotoxins': ('IV', 'Applied', 'T1', 'medium'),
    'Food Additives, Cosmetics & GRAS': ('IV', 'Applied', 'T7', 'medium'),
    'Alcohols & Methanol/Ethanol': ('IV', 'Applied', 'T11', 'medium'),
    'Radiation / UV / Ionizing': ('IV', 'Applied', 'T1', 'high'),
    'Liver / Hepatotoxicity': ('I', 'C.Interpret', 'T2', 'medium'),
    'Kidney / Nephrotoxicity': ('I', 'C.Interpret', 'T2', 'medium'),
    'Lung / Pulmonary Toxicity': ('I', 'C.Interpret', 'T2', 'medium'),
    'Nervous System / Neurotoxicity': ('I', 'C.Interpret', 'T2', 'medium'),
    'Skin / Dermatotoxicity': ('I', 'C.Interpret', 'T2', 'medium'),
    'Eye / Ocular Toxicity': ('I', 'C.Interpret', 'T2', 'medium'),
    'Cardiovascular Toxicity': ('I', 'C.Interpret', 'T2', 'medium'),
    'Hematology & Blood Toxicity': ('I', 'C.Interpret', 'T2', 'medium'),
    'Immunotoxicology / Allergy': ('I', 'C.Interpret', 'T2', 'medium'),
    'Endocrine Toxicology': ('I', 'C.Interpret', 'T2', 'medium'),
    'Reproductive & Developmental Toxicity': ('I', 'C.Interpret', 'T2', 'medium'),
}

def classify_bloom(question_text):
    q = str(question_text).lower()
    
    analyze_indicators = [
        'why', 'mechanism', 'explain', 'compare', 'differ', 'distinguish',
        'most likely reason', 'basis of', 'rationale', 'interpret',
        'significance', 'how does', 'relationship between',
        'best explains', 'cause of', 'due to', 'which of the following explains',
        'which statement', 'true regarding'
    ]
    
    apply_indicators = [
        'which of the following', 'most appropriate', 'best', 'first step',
        'recommend', 'select', 'choose', 'what would', 'case', 'patient',
        'worker', 'exposed', 'scenario', 'study found', 'investigation',
        'management', 'treatment', 'diagnosis', 'most likely'
    ]
    
    analyze_score = sum(1 for ind in analyze_indicators if ind in q)
    apply_score = sum(1 for ind in apply_indicators if ind in q)
    
    if analyze_score >= 2:
        return 'Analyze', 'medium'
    elif analyze_score >= 1 or apply_score >= 2:
        return 'Apply', 'medium'
    elif apply_score >= 1:
        return 'Apply', 'medium'
    else:
        return 'Remember/Understand', 'medium'

classifications = []
for idx, row in df.iterrows():
    topic = row['Topic (Primary)']
    dom, sub, task, conf = topic_to_domain.get(topic, ('?', '?', '?', 'low'))
    
    # Risk Assessment override - check All Topics AND question text for RA keywords
    all_topics = str(row.get('All Topics', ''))
    question = str(row['Question']).lower()
    
    ra_keywords = [
        # Dose-response
        'dose-response', 'dose response', 'benchmark dose', 'bmd', 'noael', 'loael',
        'reference dose', 'rfd', 'reference concentration', 'rfc',
        'point of departure', 'pod', 'safe dose', 'safety margin',
        'acceptable daily intake', 'adi', 'tolerable daily intake', 'tdi',
        'therapeutic index', 'ed50', 'ld50', 'lc50', 'ec50',
        'no observed', 'lowest observed', 'median lethal', 'median effective',
        'hormesis', 'dose-response curve', 'cumulative dose',
        # Exposure assessment
        'exposure assessment', 'margin of exposure', 'margin of safety', 'moe',
        'hazard quotient', 'hazard index', 'uncertainty factor',
        'exposure limit', 'threshold limit value', 'tlv', 'pel', 'permissible exposure',
        'short-term exposure', 'st el', 'time-weighted average', 'twa',
        'biomonitoring', 'exposure reconstruction', 'exposure scenario',
        'exposure route', 'route of exposure', 'exposure pathway',
        'body weight', 'inhalation rate', 'surface area', 'exposure duration',
        # Hazard identification
        'hazard identification', 'weight of evidence', 'woe',
        'cancer classification', 'iarc', 'epa cancer', 'carcinogen classification',
        'group 1', 'group 2a', 'group 2b', 'group 2',
        'known human carcinogen', 'probable human carcinogen', 'possible human carcinogen',
        # Risk characterization / management
        'risk assessment', 'risk characterization', 'risk management',
        'risk communication', 'precautionary', 'safe level',
        'health-based', 'provisional advisory', 'aegl', 'acute exposure guideline',
        'cleanup', 'remediation', 'acceptable risk', 'de minimis',
        # Regulatory / standards
        'osha standard', 'epa guideline', 'fifra', 'tsca', 'reach',
        'regulatory limit', 'maximum contaminant', 'mcl', 'action level',
        # Uncertainty / extrapolation
        'interspecies', 'intraspecies', 'extrapolation',
        'chemical-specific adjustment', 'data-derived', 'ddef', 'csaf',
        'allometric scaling', 'safety factor', 'assessment factor',
        'linear extrapolation', 'non-threshold', 'threshold',
        # Mode of action / AOP (connects to risk)
        'mode of action', 'adverse outcome pathway', 'aop', 'key event',
        # Sentinel phrases
        'for risk assessment', 'in risk assessment', 'risk assessor',
        'in the risk', 'characterize risk', 'evaluating risk',
        'estimated daily intake', 'edi',
    ]
    
    ra_score = sum(1 for kw in ra_keywords if kw in question)
    
    if ra_score >= 1 or 'Risk Assessment' in all_topics or 'Dose-Response' in all_topics:
        if dom in ('I', 'IV', '?'):
            dom, sub, task = ('III', 'D.RiskChar&Mgmt', 'T1')
            conf = 'medium' if ra_score >= 3 else 'low'  # High overlap = more confident
    
    bloom, bloom_conf = classify_bloom(row['Question'])
    
    classifications.append({
        'ID': row['ID'],
        'Source Exam': int(row['Source Exam']),
        'Question #': int(row['Question #']),
        'Topic (Primary)': topic,
        'All Topics': all_topics,
        'Domain': f'Domain {dom}' if dom != '?' else '?',
        'Sub-Domain': sub,
        'Task': task,
        'Bloom Level': bloom,
        'Domain Confidence': conf,
        'Bloom Confidence': bloom_conf
    })

cls_df = pd.DataFrame(classifications)

print(f"Domain distribution:")
print(cls_df['Domain'].value_counts().to_string())
print(f"\nBloom distribution:")
print(cls_df['Bloom Level'].value_counts().to_string())
print(f"\nDomain confidence:")
print(cls_df['Domain Confidence'].value_counts().to_string())

# Check unclassified
unclassified = cls_df[cls_df['Domain'] == '?']
if len(unclassified):
    print(f"\nUNCLASSIFIED ({len(unclassified)}):")
    for _, r in unclassified.iterrows():
        print(f"  {r['ID']}: {r['Topic (Primary)']}")

cls_df.to_csv('/home/vthen/work/dabt-tutor/reference/question_classifications.csv', index=False)
cls_df.to_json('/home/vthen/work/dabt-tutor/reference/question_classifications.json', orient='records', indent=2)
print(f"\nSaved classification files.")
