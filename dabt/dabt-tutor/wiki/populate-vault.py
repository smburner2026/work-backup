#!/usr/bin/env python3
"""
DABT Vault Populator — first wave.

Reads the curriculum topic list from dabt-config.json and writes:
- 5 MOC notes (Domain I/II/III/IV + Organ Systems)
- 81 concept notes (functioning stubs with definition, exam signal, source pointers)
- Updates backlinks in adversity-determination and mode-of-action-analysis

Stubs are intentionally concise. User pulls on a concept to expand it.
"""
import json
import os
import re
from pathlib import Path

VAULT = Path("/root/work/dabt/dabt-tutor/wiki")
CONCEPTS = VAULT / "concepts"
CONCEPTS.mkdir(parents=True, exist_ok=True)

# === Source mapping: each topic name → likely source locations ===
# Curated from the actual file list. Mappings are conservative — when in doubt,
# the stub points at the whole source, not a wrong page.
CD_CHAPTERS = {
    "General Principles & Concepts": "2-principles-of-toxicology",
    "General Toxicology": "2-principles-of-toxicology",
    "Mechanisms of Toxicity": "3-mechanisms-of-toxicity",
    "Study Design": "2-principles-of-toxicology",
    "OECD Test Guidelines": "2-principles-of-toxicology",
    "ICH S-series": "2-principles-of-toxicology",
    "GLP": "2-principles-of-toxicology",
    "Dose Selection": "2-principles-of-toxicology",
    "Study Execution": "2-principles-of-toxicology",
    "Data Collection": "2-principles-of-toxicology",
    "Quality Assurance": "2-principles-of-toxicology",
    "Histopathology": "12-pathology-principles-and-practices-for-toxicity-studies",
    "Data Interpretation": "3-mechanisms-of-toxicity",
    "NOAEL/LOAEL": "3-dose-response-a-fundamental-concept-in-toxicology",
    "Statistical Analysis": "9-statistics-and-experimental-design-for-toxicologists",
    "Adversity Determination": "3-mechanisms-of-toxicity",
    "Pathology Interpretation": "12-pathology-principles-and-practices-for-toxicity-studies",
    "Biotransformation / Metabolism": "4-metabolism-a-determinant-of-toxicity",
    "Genotoxicity / DNA Damage": "26-genetic-and-epigenetic-toxicology",
    "Carcinogenesis & Mutagenesis": "8-chemical-carcinogenesis",
    "MOA/AOP": "8-chemical-carcinogenesis",
    "Hypothesis Testing": "3-mechanisms-of-toxicity",
    "Comparative Toxicology": "11-epidemiology-for-toxicologists",
    "Extrapolation": "11-epidemiology-for-toxicologists",
    "Genetic Susceptibility": "26-genetic-and-epigenetic-toxicology",
    "Age/Sex Differences": "21-humane-care-and-use-of-laboratory-animals-in-toxicology-research",
    "Primary vs Secondary Toxicity": "3-mechanisms-of-toxicity",
    "In Vitro to In Vivo": "22-novel-approaches-and-alternative-models-validation-and-regulatory-acceptance",
    "Molecular to Organism": "3-mechanisms-of-toxicity",
    "Risk Assessment & Regulatory": "35-regulatory-toxicology",
    "Toxicokinetics / ADME": "5-toxicokinetics",
    "Dose-Response": "3-dose-response-a-fundamental-concept-in-toxicology",
    "Hazard ID": "35-regulatory-toxicology",
    "Weight of Evidence": "35-regulatory-toxicology",
    "Cancer Classification": "27-carcinogenicity-bioassays-and-related-assays-human-relevance",
    "Exposure Assessment": "10-the-practice-of-exposure-assessment",
    "Biomonitoring": "10-the-practice-of-exposure-assessment",
    "Exposure Reconstruction": "10-the-practice-of-exposure-assessment",
    "Dose-Response Modeling": "3-dose-response-a-fundamental-concept-in-toxicology",
    "BMD": "3-dose-response-a-fundamental-concept-in-toxicology",
    "NOAEL/UF/MF": "3-dose-response-a-fundamental-concept-in-toxicology",
    "POD Selection": "3-dose-response-a-fundamental-concept-in-toxicology",
    "Risk Characterization": "35-regulatory-toxicology",
    "Margin of Exposure": "3-dose-response-a-fundamental-concept-in-toxicology",
    "Risk Management": "35-regulatory-toxicology",
    "Metals & Metalloids": "23-toxic-effects-of-metals",
    "Solvents & Hydrocarbons": "24-toxic-effects-of-solvents-and-vapors",
    "Pesticides – Insecticides": "22-toxic-effects-of-pesticides",
    "Pesticides – Herbicides": "22-toxic-effects-of-pesticides",
    "Pesticides – Rodenticides": "22-toxic-effects-of-pesticides",
    "Pesticides – Fumigants": "22-toxic-effects-of-pesticides",
    "Gases – Asphyxiants & Irritants": "15-toxic-responses-of-the-respiratory-system",
    "Air Pollution & Particulates": "31-air-pollution",
    "Drugs & Therapeutics – Toxicology": "8-toxicologic-assessment-of-pharmaceutical-medical-device-and-biotechnology-prod",
    "Plant Toxins": "26-toxic-effects-of-plants-and-animals",
    "Animal & Microbial Venoms / Toxins": "26-toxic-effects-of-plants-and-animals",
    "Mycotoxins": "27-food-toxicology-fundamental-and-regulatory-aspects",
    "Food Additives, Cosmetics & GRAS": "27-food-toxicology-fundamental-and-regulatory-aspects",
    "Alcohols & Methanol/Ethanol": "33-clinical-toxicology",
    "Environmental Toxicology": "30-ecotoxicology",
    "Ecosystem Exposures": "30-ecotoxicology",
    "Emergency Response": "33-clinical-toxicology",
    "Poison Control": "33-clinical-toxicology",
    "Biomonitoring Programs": "10-the-practice-of-exposure-assessment",
    "Exposure Biomarkers": "10-the-practice-of-exposure-assessment",
    "Children": "10-the-evolving-journey-of-toxicology-a-historical-glimpse",
    "Elderly": "10-the-evolving-journey-of-toxicology-a-historical-glimpse",
    "Pregnant Women": "38-female-reproductive-and-developmental-toxicology",
    "Green Chemistry": "35-regulatory-toxicology",
    "Alternatives Assessment": "22-novel-approaches-and-alternative-models-validation-and-regulatory-acceptance",
    "Liver / Hepatotoxicity": "32-hepatotoxicology",
    "Kidney / Nephrotoxicity": "33-principles-and-methods-for-renal-toxicology",
    "Lung / Pulmonary Toxicity": "30-inhalation-toxicology",
    "Nervous System / Neurotoxicity": "35-neurotoxicology",
    "Skin / Dermatotoxicity": "29-dermatotoxicology",
    "Eye / Ocular Toxicity": "17-toxic-responses-of-the-cornea-retina-and-central-visual-system",
    "Cardiovascular Toxicity": "34-cardiovascular-toxicology-methods",
    "Hematology & Blood Toxicity": "11-toxic-responses-of-the-blood",
    "Immunotoxicology / Allergy": "39-immunotoxicology-the-immune-system-response-to-toxic-insult",
    "Endocrine Toxicology": "36-toxicology-of-the-endocrine-system",
    "Reproductive & Developmental Toxicity": "37-assessment-of-male-reproductive-toxicity",
}

HAYES_CHAPTERS = {
    # Best-effort mapping to Hayes 7e (39 chapters available)
    "General Principles & Concepts": "1-history-understanding-and-a-possible-future-of-toxicology",
    "Mechanisms of Toxicity": "23-modern-instrumental-methods-for-studying-mechanisms-of-toxicology",
    "Biotransformation / Metabolism": "4-metabolism-a-determinant-of-toxicity",
    "Genotoxicity / DNA Damage": "26-genetic-and-epigenetic-toxicology",
    "Carcinogenesis & Mutagenesis": "27-carcinogenicity-bioassays-and-related-assays-human-relevance",
    "Dose-Response": "3-dose-response-a-fundamental-concept-in-toxicology",
    "Dose-Response Modeling": "3-dose-response-a-fundamental-concept-in-toxicology",
    "BMD": "3-dose-response-a-fundamental-concept-in-toxicology",
    "NOAEL/UF/MF": "3-dose-response-a-fundamental-concept-in-toxicology",
    "POD Selection": "3-dose-response-a-fundamental-concept-in-toxicology",
    "Toxicokinetics / ADME": "5-toxicokinetics",
    "Statistical Analysis": "9-statistics-and-experimental-design-for-toxicologists",
    "Histopathology": "12-pathology-principles-and-practices-for-toxicity-studies",
    "Comparative Toxicology": "11-epidemiology-for-toxicologists",
    "Liver / Hepatotoxicity": "32-hepatotoxicology",
    "Kidney / Nephrotoxicity": "33-principles-and-methods-for-renal-toxicology",
    "Lung / Pulmonary Toxicity": "30-inhalation-toxicology",
    "Nervous System / Neurotoxicology": "35-neurotoxicology",
    "Cardiovascular Toxicity": "34-cardiovascular-toxicology-methods",
    "Endocrine Toxicology": "36-toxicology-of-the-endocrine-system",
    "Immunotoxicology / Allergy": "39-immunotoxicology-the-immune-system-response-to-toxic-insult",
    "Reproductive & Developmental Toxicity": "38-female-reproductive-and-developmental-toxicology",
    "Skin / Dermatotoxicity": "29-dermatotoxicology",
    "Metals & Metalloids": "19-metals",
    "Hazard ID": "2-use-of-toxicology-in-the-regulatory-process",
    "Risk Characterization": "2-use-of-toxicology-in-the-regulatory-process",
    "Risk Management": "2-use-of-toxicology-in-the-regulatory-process",
    "Exposure Assessment": "10-the-practice-of-exposure-assessment",
    "Biomonitoring": "10-the-practice-of-exposure-assessment",
    "Children": "38-female-reproductive-and-developmental-toxicology",
    "Pregnant Women": "38-female-reproductive-and-developmental-toxicity",
    "Adversity Determination": "3-dose-response-a-fundamental-concept-in-toxicology",
    "MOA/AOP": "3-dose-response-a-fundamental-concept-in-toxicology",
}

# Topic → exam weight from blueprint (Domain I=36, II=13, III=38, IV=13)
DOMAIN_WEIGHT = {
    "domain-i-conduct-of-studies": 36,
    "domain-ii-mechanistic-tox": 13,
    "domain-iii-risk-assessment": 38,
    "domain-iv-applied-tox": 13,
    "organ-systems": 0,  # cross-cutting
}

# Sub-domain weights for higher granularity
SUBDOMAIN_WEIGHT = {
    # Domain I
    "a-design": 11, "b-execute": 9, "c-interpret": 16,
    # Domain III
    "a-hazard-id": 12, "b-exposure": 8, "c-dose-response": 9, "d-risk-char": 9,
}

# Short definition for each topic — pragmatic, exam-oriented
DEFINITIONS = {
    "General Principles & Concepts": "Foundational toxicology: dose-response, hazard vs risk, exposure routes, individual vs population effects.",
    "General Toxicology": "Branch overview: history, scope, sub-disciplines, the three Rs (reduce/refine/replace), classification frameworks.",
    "Mechanisms of Toxicity": "How chemicals cause harm at the molecular, cellular, and tissue level — receptors, enzymes, DNA, oxidative stress.",
    "Study Design": "Hypothesis formation, control selection, dose levels, route, species, GLP compliance, statistical power.",
    "OECD Test Guidelines": "Internationally harmonised test protocols (TG 402, 403, 404, 405, 406, 426, 429, etc.) for regulatory toxicology studies.",
    "ICH S-series": "International Council for Harmonisation safety guidelines — S1 (carcinogenicity), S2 (genotox), S3 (pharmacokinetics), S5-S12 (various).",
    "GLP": "Good Laboratory Practice — 21 CFR Part 58 (FDA), 40 CFR Part 160 (EPA/FIFRA), 40 CFR Part 792 (EPA/TSCA), OECD GLP Principles.",
    "Dose Selection": "Rationale for dose levels in toxicity studies — MTD, limit dose, dose spacing, linearity with exposure.",
    "Study Execution": "In-life phase: animal husbandry, clinical observations, body weights, food/water consumption, clinical pathology.",
    "Data Collection": "Endpoints measured: clinical signs, organ weights, clinical chemistry, hematology, urinalysis, histopathology.",
    "Quality Assurance": "QA unit responsibilities, study audits, facility inspections, SOP compliance, raw data integrity.",
    "Histopathology": "Microscopic evaluation of tissues — fixation, sectioning, staining (H&E, special stains), peer review.",
    "Data Interpretation": "Drawing conclusions from study results — NOAEL/LOAEL, adversity, dose-response, relevance to humans.",
    "NOAEL/LOAEL": "No/Lowest Observed Adverse Effect Level — the foundational POD in non-cancer risk assessment.",
    "Statistical Analysis": "Methods for tox data: t-test, ANOVA, Dunnett's, trend tests, chi-square, BMD modeling, multiplicity correction.",
    "Adversity Determination": "Whether a biological effect is adaptive or adverse — the gateway skill for NOAEL, BMDL, and risk numbers.",
    "Pathology Interpretation": "Distinguishing spontaneous background lesions from treatment-related effects; adversity vs adaptation.",
    "Biotransformation / Metabolism": "Phase I (CYP450) and Phase II (conjugation) reactions — activation, detoxification, species differences.",
    "Genotoxicity / DNA Damage": "DNA-reactive agents, mutation assays (Ames, micronucleus, comet), threshold vs non-threshold.",
    "Carcinogenesis & Mutagenesis": "Initiation-promotion-progression, genotoxic vs non-genotoxic carcinogens, MoA analysis, classification.",
    "MOA/AOP": "Mode of Action / Adverse Outcome Pathway — MIE → Key Events → Adverse Outcome; framework for human-relevant risk.",
    "Hypothesis Testing": "Forming testable mechanistic hypotheses, designing experiments to discriminate between competing MoAs.",
    "Comparative Toxicology": "Cross-species differences in toxicokinetics and toxicodynamics — animal-to-human extrapolation.",
    "Extrapolation": "Animal → human, high-dose → low-dose, acute → chronic, in vitro → in vivo. Each carries uncertainty.",
    "Genetic Susceptibility": "Polymorphisms in metabolising enzymes (CYP, NAT, GST) and DNA repair that modulate individual risk.",
    "Age/Sex Differences": "Pediatric, geriatric, sex-specific differences in toxicokinetics and target organ sensitivity.",
    "Primary vs Secondary Toxicity": "Direct toxicity at the target organ vs systemic effects downstream from a different target.",
    "In Vitro to In Vivo": "Bridging cell-based assays to whole-organism responses — validation, limitations, OECD acceptance.",
    "Molecular to Organism": "From molecular initiating event to whole-organism adverse outcome — AOP framework.",
    "Risk Assessment & Regulatory": "NRC 4-step framework: Hazard ID → Exposure Assessment → Dose-Response → Risk Characterization.",
    "Toxicokinetics / ADME": "Absorption, Distribution, Metabolism, Excretion — what the body does to the chemical.",
    "Dose-Response": "Relationship between dose and the magnitude/incidence of effect — central to all of toxicology.",
    "Hazard ID": "The weight-of-evidence determination that a chemical can cause an adverse effect.",
    "Weight of Evidence": "Integrating mechanistic, animal, and human data using modified Bradford Hill criteria.",
    "Cancer Classification": "IARC (1, 2A, 2B, 3, 4), EPA (carcinogenic, likely, suggestive, inadequate, not likely), NTP RoC.",
    "Exposure Assessment": "Identifying populations exposed, routes, magnitudes, frequencies, durations — measurement or modelling.",
    "Biomonitoring": "Measuring parent compound, metabolites, or adducts in biological media (blood, urine, hair) as exposure biomarkers.",
    "Exposure Reconstruction": "Retrospective exposure estimation from biomarkers, environmental levels, and PBPK modeling.",
    "Dose-Response Modeling": "Fitting mathematical models to dose-response data — log-logistic, Weibull, Hill, quantal linear.",
    "BMD": "Benchmark Dose — dose producing a specified response level (BMR); BMDL = lower 95% confidence bound.",
    "NOAEL/UF/MF": "NOAEL divided by uncertainty factors (interspecies, intraspecies, subchronic-to-chronic, LOAEL-to-NOAEL).",
    "POD Selection": "Point of Departure choice: NOAEL, LOAEL, BMDL — depends on data quality, dose spacing, study design.",
    "Risk Characterization": "Integration of hazard, exposure, and dose-response into a quantitative or qualitative risk estimate.",
    "Margin of Exposure": "POD / human exposure — small MoE = high concern; used for genotoxic carcinogens (EFSA approach).",
    "Risk Management": "Decision-making after risk characterisation — engineering controls, PPE, exposure limits, mitigation.",
    "Metals & Metalloids": "Essential (Fe, Zn, Cu, Se) and non-essential (Pb, Hg, Cd, As) metals — speciation, chelation, target organs.",
    "Solvents & Hydrocarbons": "Organic solvents (benzene, toluene, CCl4) and fuels — CNS depression, hepatotoxicity, target organ by route.",
    "Pesticides – Insecticides": "Organophosphates, carbamates, pyrethroids, neonicotinoids — AChE inhibition, mechanism-specific tox.",
    "Pesticides – Herbicides": "Glyphosate, atrazine, 2,4-D — mechanisms, endocrine disruption controversy, IARC classification.",
    "Pesticides – Rodenticides": "Anticoagulants (warfarin), bromethalin, zinc phosphide — secondary poisoning risk to non-targets.",
    "Pesticides – Fumigants": "Methyl bromide, phosphine, sulfuryl fluoride — high acute toxicity, occupational exposure limits.",
    "Gases – Asphyxiants & Irritants": "CO, HCN, H2S, Cl2, NH3, phosgene — local vs systemic, water solubility determines site of action.",
    "Air Pollution & Particulates": "PM2.5, ozone, NOx, SO2 — cardiovascular and respiratory endpoints, IUR for cancer risk.",
    "Drugs & Therapeutics – Toxicology": "Adverse drug reactions, drug-drug interactions, idiosyncratic reactions, therapeutic index.",
    "Plant Toxins": "Pyrrolizidine alkaloids, amygdalin, ricin, abrin — hepatotoxicity, neurotoxicity, gastrointestinal.",
    "Animal & Microbial Venoms / Toxins": "Snake venom, scorpion, spider, marine toxins, botulinum — mechanism-based antivenoms.",
    "Mycotoxins": "Aflatoxins (B1 — IARC 1), ochratoxin, fumonisin, deoxynivalenol — hepatotoxic, nephrotoxic, carcinogenic.",
    "Food Additives, Cosmetics & GRAS": "FDA Generally Recognized As Safe designation, color additives, indirect food additives.",
    "Alcohols & Methanol/Ethanol": "Methanol → formate → optic nerve; ethanol → acetaldehyde → liver; ethylene glycol → oxalate → kidney.",
    "Environmental Toxicology": "Fate and transport in ecosystems — persistence, bioaccumulation, biomagnification, TEFs.",
    "Ecosystem Exposures": "Population-, community-, ecosystem-level effects — apical endpoints beyond individual organisms.",
    "Emergency Response": "Acute exposure incidents — Triage, decontamination, antidotes, incident command (HAZMAT).",
    "Poison Control": "Clinical management of poisoning exposures — supportive care, antidotes, toxidromes.",
    "Biomonitoring Programs": "NHANES, CDC Environmental Health Tracking, population-level exposure surveillance.",
    "Exposure Biomarkers": "Chemicals or metabolites in biological media indicating exposure — internal dose measurement.",
    "Children": "Pediatric toxicology — developmental vulnerabilities, milk/placenta transfer, body surface area scaling.",
    "Elderly": "Geriatric toxicology — polypharmacy, reduced renal/hepatic clearance, altered body composition.",
    "Pregnant Women": "Teratogenicity, placental transfer, fetal susceptibility windows, pregnancy prescribing.",
    "Green Chemistry": "Designing chemicals with reduced intrinsic hazard — the 12 principles of green chemistry.",
    "Alternatives Assessment": "Substituting safer chemicals — read-across, QSAR, in vitro assays to support decision-making.",
    "Liver / Hepatotoxicity": "Hepatic steatosis, necrosis, cholestasis, fibrosis, cirrhosis — by mechanism and zone (centrilobular).",
    "Kidney / Nephrotoxicity": "Tubular necrosis, glomerulonephritis, papillary necrosis, urinary biomarkers (KIM-1, NGAL).",
    "Lung / Pulmonary Toxicity": "Respiratory irritation, pulmonary edema, fibrosis, emphysema, occupational pneumoconioses.",
    "Nervous System / Neurotoxicity": "Neuronopathy, axonopathy, myelinopathy, neurotransmission effects — irreversible often.",
    "Skin / Dermatotoxicity": "Irritation, corrosion, sensitisation (LLNA, GPMT, HRIPT), phototoxicity — local vs systemic.",
    "Eye / Ocular Toxicity": "Irritation, corrosion, corneal opacity, retinopathy — Draize test and in vitro alternatives.",
    "Cardiovascular Toxicity": "Cardiotoxicity, QT prolongation (hERG), vascular injury, ICH S7A/S7B safety pharmacology.",
    "Hematology & Blood Toxicity": "Hemolysis, methemoglobinemia, aplastic anemia, leukemia, coagulation disorders.",
    "Immunotoxicology / Allergy": "Immunosuppression, sensitisation, hypersensitivity, autoimmunity — T-cell dependent.",
    "Endocrine Toxicology": "Endocrine disruption — EDCs, thyroid, estrogen/androgen, OECD and EPA screening programs.",
    "Reproductive & Developmental Toxicity": "Fertility, implantation, teratogenicity, functional deficits — ICH S5, OECD 414/415/416.",
}

# === Stub file template ===
STUB_TEMPLATE = """---
tags: [concept, {domain_tag}, weight-{weight}]
domain: {domain}
exam_weight: {weight}
status: stub
sources: [{sources}]
related: [{related}]
---

# {title}

{definition}

## Why it matters

Exam weight: **{weight}%** (Domain {domain_short}). Stub — pull on this to expand.

## Related concepts

{related}

## Source pointers

{source_block}
"""


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r'[–—/]', '-', s)  # em-dash, en-dash, and forward-slash → hyphen
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    s = s.replace('gr-as', 'gras')
    return s


def write_concept_stub(name, domain_id, domain_label, subdomain=None):
    slug = slugify(name)
    path = CONCEPTS / f"{slug}.md"
    if path.exists():
        return False

    weight = SUBDOMAIN_WEIGHT.get(subdomain, DOMAIN_WEIGHT.get(domain_id, 0))
    if domain_id == "organ-systems":
        weight = 0  # cross-cutting
    domain_tag = domain_id.replace("domain-", "").replace("-tox", "").replace("conduct-of-studies", "i")
    domain_short = domain_id.split("-")[1].upper() if "-" in domain_id else "?"

    sources = []
    if name in CD_CHAPTERS:
        cd = CD_CHAPTERS[name]
        sources.append(f"cd-{cd.split('-')[0]}")
    if name in HAYES_CHAPTERS:
        hayes = HAYES_CHAPTERS[name]
        sources.append(f"hayes-{hayes.split('-')[0]}")
    if not sources:
        sources.append("cd-2")
        sources.append("hayes-2")

    definition = DEFINITIONS.get(name, f"Toxicology concept: {name}.")

    # Related — link to a couple of plausible neighbours
    related_links = {
        "Adversity Determination": ["[[mode-of-action-analysis]]", "[[dose-response]]", "[[noael-loael]]"],
        "MOA/AOP": ["[[adversity-determination]]", "[[weight-of-evidence]]", "[[carcinogenesis-mutagenesis]]"],
        "BMD": ["[[dose-response-modeling]]", "[[noael-loael]]", "[[pod-selection]]"],
        "NOAEL/UF/MF": ["[[bmd]]", "[[pod-selection]]", "[[dose-response]]"],
        "POD Selection": ["[[noael-loael]]", "[[bmd]]", "[[adversity-determination]]"],
        "Dose-Response Modeling": ["[[bmd]]", "[[dose-response]]"],
        "Dose-Response": ["[[bmd]]", "[[noael-loael]]", "[[adversity-determination]]"],
        "Carcinogenesis & Mutagenesis": ["[[moa-aop]]", "[[cancer-classification]]", "[[genotoxicity-dna-damage]]"],
        "Genotoxicity / DNA Damage": ["[[carcinogenesis-mutagenesis]]", "[[moa-aop]]"],
        "Cancer Classification": ["[[carcinogenesis-mutagenesis]]", "[[hazard-id]]", "[[weight-of-evidence]]"],
        "Risk Characterization": ["[[margin-of-exposure]]", "[[risk-management]]", "[[hazard-id]]"],
        "Risk Management": ["[[risk-characterization]]", "[[exposure-assessment]]"],
        "Hazard ID": ["[[weight-of-evidence]]", "[[cancer-classification]]"],
        "Weight of Evidence": ["[[hazard-id]]", "[[moa-aop]]"],
        "Statistical Analysis": ["[[dose-response-modeling]]", "[[bmd]]"],
    }
    related = related_links.get(name, ["[[risk-assessment-regulatory]]", "[[adversity-determination]]"])

    source_lines = []
    if name in CD_CHAPTERS:
        cd = CD_CHAPTERS[name]
        source_lines.append(f"- Casarett & Doull 9e ch {cd.split('-')[0]} — `{cd}`")
    if name in HAYES_CHAPTERS:
        hayes = HAYES_CHAPTERS[name]
        source_lines.append(f"- Hayes 7e ch {hayes.split('-')[0]} — `{hayes}`")
    source_lines.append("- `reference/extracted/` for the raw text")
    source_block = "\n".join(source_lines)

    related_block = ", ".join(related)

    content = STUB_TEMPLATE.format(
        domain_tag=domain_tag,
        weight=weight,
        domain=domain_label,
        title=name,
        domain_short=domain_short,
        definition=definition,
        sources=", ".join(sources),
        related=related_block,
        source_block=source_block,
    )
    path.write_text(content)
    return True


# === MOC template ===
MOC_TEMPLATE = """---
tags: [moc, {domain_tag}]
type: map-of-content
domain: {domain_label}
exam_weight: {weight}
---

# {moc_title}

> {domain_label} — {weight}% of the DABT exam. Master index of concept notes, source pointers, and exam traps.

## Exam weight breakdown

{weight_breakdown}

## Concept notes (this domain)

{concept_list}

## Source pointers

- **Primary text**: Casarett & Doull's Toxicology, 9th ed. — `reference/extracted/casarett-doull-9e/`
- **Mechanistic depth**: Hayes' Principles and Methods of Toxicology, 7th ed. — `reference/extracted/hayes-7e/`
- **Regulatory anchor**: `reference/extracted/regulations/`

## Exam traps

- This domain tests both knowledge and reasoning under uncertainty. Most questions are scenario-based.
- Adaptive vs adverse effects are a recurring exam trap (see [[adversity-determination]]).
- Regulatory framework questions require knowing which agency, which guideline, which endpoint.

## Backlinks

This MOC is referenced from:
- [[learner-profile]]
- [[miss-journal|miss-journal MOC]]
- All concept notes in this domain link here
"""


def write_moc(domain_id, domain_label, weight, sub_breakdown, topics_list):
    slug = domain_id.replace("domain-", "moc-")
    path = CONCEPTS / f"{slug}.md"

    domain_short = domain_id.split("-")[1].upper() if "-" in domain_id else "?"
    domain_tag = domain_id.replace("domain-", "")

    # Sort topics by exam weight within the domain
    topic_with_weights = []
    for t in topics_list:
        if isinstance(t, tuple):
            topic_with_weights.append(t)
        else:
            topic_with_weights.append((t, None))

    bullet_lines = []
    for t, sub in topic_with_weights:
        slug_t = slugify(t)
        sub_label = f" *({sub})*" if sub else ""
        bullet_lines.append(f"- [[{slug_t}]]{sub_label}")

    weight_lines = []
    for sub_label, w in sub_breakdown.items():
        weight_lines.append(f"- **{sub_label}** — {w}%")
    if not weight_lines:
        weight_lines.append(f"- Whole domain: {weight}%")

    content = MOC_TEMPLATE.format(
        domain_tag=domain_tag,
        domain_label=domain_label,
        weight=weight,
        moc_title=f"Domain {domain_short} — {domain_label}",
        weight_breakdown="\n".join(weight_lines),
        concept_list="\n".join(bullet_lines),
    )
    path.write_text(content)
    return path


# === Main ===
def main():
    config = json.load(open("/root/work/dabt/dabt-tutor/dabt-config.json"))

    written = 0
    for d_id, d in config["curriculum"]["domains"].items():
        domain_label = d["name"]
        # Top-level topic_list
        for t in d["topic_list"]:
            if write_concept_stub(t, d_id, domain_label):
                written += 1
        # Subdomain topic_lists (catch the rest)
        for s_id, s in d.get("subdomains", {}).items():
            for t in s.get("topic_list", []):
                if write_concept_stub(t, d_id, domain_label, subdomain=s_id):
                    written += 1

    # MOC notes
    mocs = [
        ("domain-i-conduct-of-studies", "Conduct of Toxicological Studies", 36,
         {"I-A Design": 11, "I-B Execute": 9, "I-C Interpret": 16}),
        ("domain-ii-mechanistic-tox", "Mechanistic Toxicology", 13, {}),
        ("domain-iii-risk-assessment", "Risk Assessment", 38,
         {"III-A Hazard ID": 12, "III-B Exposure": 8, "III-C Dose-Response": 9, "III-D Risk Char": 9}),
        ("domain-iv-applied-tox", "Applied Toxicology", 13, {}),
    ]
    moc_files = []
    for d_id, label, w, breakdown in mocs:
        # Build topic list for the MOC: include all topic names from this domain
        topics = list(config["curriculum"]["domains"][d_id]["topic_list"])
        moc_path = write_moc(d_id, label, w, breakdown, topics)
        moc_files.append(moc_path)

    # Organ-systems MOC
    os_topics = list(config["curriculum"]["organ_systems"]["topic_list"])
    os_moc_path = CONCEPTS / "moc-organ-systems.md"
    os_moc_path.write_text(MOC_TEMPLATE.format(
        domain_tag="organ-systems",
        domain_label="Organ-System Toxicology",
        weight=0,
        moc_title="Organ Systems — Cross-Cutting Toxicology",
        weight_breakdown="- Cross-cutting: integrated with Domain I, II, III, IV by organ",
        concept_list="\n".join([f"- [[{slugify(t)}]]" for t in os_topics]),
    ))
    moc_files.append(os_moc_path)

    print(f"Wrote {written} concept stubs")
    print(f"Wrote {len(moc_files)} MOC notes:")
    for p in moc_files:
        print(f"  - {p.relative_to(VAULT)}")


if __name__ == "__main__":
    main()
