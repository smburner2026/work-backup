#!/usr/bin/env python3
"""
Inject "## Cross-references (vault)" sections into source chapter files.
Self-contained: inlines the chapter→concept maps.
"""
import json
import re
from pathlib import Path
from collections import defaultdict

VAULT = Path("/root/work/dabt/dabt-tutor/wiki")
EXTRACTED = Path("/root/work/dabt/dabt-tutor/reference/extracted")


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
    "Reproductive & Developmental Toxicity": "38-female-reproductive-and-developmental-toxicity",
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

DOMAIN_WEIGHT = {
    "domain-i-conduct-of-studies": 36,
    "domain-ii-mechanistic-tox": 13,
    "domain-iii-risk-assessment": 38,
    "domain-iv-applied-tox": 13,
    "organ-systems": 0,
}

SUBDOMAIN_WEIGHT = {
    "a-design": 11, "b-execute": 9, "c-interpret": 16,
    "a-hazard-id": 12, "b-exposure": 8, "c-dose-response": 9, "d-risk-char": 9,
}


# Build inverse map
chapter_to_concepts = defaultdict(list)
for concept, ch in CD_CHAPTERS.items():
    chapter_to_concepts[("cd", ch)].append(concept)
for concept, ch in HAYES_CHAPTERS.items():
    chapter_to_concepts[("hayes", ch)].append(concept)


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r'[–—/]', '-', s)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    s = s.replace('gr-as', 'gras')
    return s


def weight_of(name):
    config = json.load(open("/root/work/dabt/dabt-tutor/dabt-config.json"))
    for d_id, d in config["curriculum"]["domains"].items():
        if name in d.get("topic_list", []):
            for s_id, s in d.get("subdomains", {}).items():
                if name in s.get("topic_list", []):
                    return SUBDOMAIN_WEIGHT.get(s_id, DOMAIN_WEIGHT.get(d_id, 0))
            return DOMAIN_WEIGHT.get(d_id, 0)
    return 0


def inject(file_path: Path, source: str, chapter_slug: str):
    if not file_path.exists():
        return False
    concepts = chapter_to_concepts.get((source, chapter_slug), [])
    if not concepts:
        return False
    concepts_sorted = sorted(concepts, key=weight_of, reverse=True)
    concept_links = "\n".join(f"- [[{slugify(c)}]]" for c in concepts_sorted)
    section = f"""

---

## Cross-references (vault)

Auto-generated by `wiki/inject-wikilinks.py`. Concept notes that cite this chapter as a source, ordered by exam weight.

{concept_links}

> Backlinks from these concept notes will appear in the Obsidian backlink panel when this vault is opened. To regenerate, re-run the script.
"""
    existing = file_path.read_text()
    marker = "## Cross-references (vault)"
    if marker in existing:
        head, _, _ = existing.partition(marker)
        head = head.rstrip().rstrip("-").rstrip()
        new = head.rstrip() + "\n" + section
    else:
        new = existing.rstrip() + section
    file_path.write_text(new)
    return True


def main():
    touched = 0
    skipped = 0
    for (source, chapter_slug) in chapter_to_concepts.keys():
        if source == "cd":
            f = EXTRACTED / "casarett-doull-9e" / f"{chapter_slug}.txt"
        else:
            f = EXTRACTED / "hayes-7e" / f"{chapter_slug}.txt"
        if inject(f, source, chapter_slug):
            touched += 1
        else:
            skipped += 1
    print(f"Touched: {touched} | Skipped: {skipped}")


if __name__ == "__main__":
    main()
