import json

with open('/root/work/dabt/dabt-tutor/batches/synthetic/domain_i_a_batch_5.json') as f:
    data = json.load(f)

new_questions = [
    {
        "question_text": "According to Hayes Ch. 25, which of the following is NOT an objective of short-term repeated-dose toxicity studies?",
        "options": {
            "A": "Determine adverse effects at doses allowing survival of most animals",
            "B": "Determine reversibility of adverse effects after discontinuation of treatment",
            "C": "Determine carcinogenic potential for regulatory submission",
            "D": "Identify organs affected by exposure to test material"
        },
        "correct_answer": "C",
        "explanation": "Table 25.1 lists objectives of short-term studies including determining adverse effects at sublethal doses, effects over longer exposure than acute studies, reversibility, dose-response/NOAEL, target organs, species sensitivity, and data for risk assessment. Determining carcinogenic potential is not listed as a short-term study objective.",
        "source_citation": "Hayes Ch. 25, pp. 1366",
        "bloom_level": "Recall",
        "format": "EXCEPT/NOT",
        "sub_domain": "A.Design"
    },
    {
        "question_text": "According to Hayes Ch. 25, which of the following is NOT a type of negative control group used in repeated-dose toxicity studies?",
        "options": {
            "A": "Vehicle control group (receives vehicle by same route)",
            "B": "Untreated control group (receives diet without test material)",
            "C": "Sham control group (receives same physical treatment without test material)",
            "D": "Satellite control group (receives test material at a different time)"
        },
        "correct_answer": "D",
        "explanation": "The chapter describes three types of negative controls: vehicle control, untreated control (for dietary studies), and sham control (e.g., insertion of intubation tube with water). A satellite control group receiving test material at a different time is not a negative control type.",
        "source_citation": "Hayes Ch. 25, pp. 1378-1379",
        "bloom_level": "Recall",
        "format": "EXCEPT/NOT",
        "sub_domain": "A.Design"
    },
    {
        "question_text": "According to Hayes Ch. 25, which of the following is NOT listed as a selection criterion for species and strain in repeated-dose toxicity studies?",
        "options": {
            "A": "Metabolism of test material in a manner similar to humans",
            "B": "Availability of historical control data",
            "C": "Cost of the animal per unit body weight",
            "D": "Responsiveness of particular organs and tissues to specific toxicities"
        },
        "correct_answer": "C",
        "explanation": "Table 25.6 lists selection criteria: regulatory requirements, human-like metabolism, historical control data availability, most sensitive species/strain, organ responsiveness, species availability, appropriate housing/husbandry, and laboratory experience. Cost per unit body weight is not listed.",
        "source_citation": "Hayes Ch. 25, pp. 1378-1379",
        "bloom_level": "Recall",
        "format": "EXCEPT/NOT",
        "sub_domain": "A.Design"
    },
    {
        "question_text": "According to Hayes Ch. 26, which of the following is NOT a major category of direct DNA damage?",
        "options": {
            "A": "Covalent binding (DNA adduct formation)",
            "B": "Intercalation between base pairs",
            "C": "Protein phosphorylation",
            "D": "DNA strand breakage"
        },
        "correct_answer": "C",
        "explanation": "Table 26.4 lists major categories of direct DNA damage: covalent binding, intercalation, cross-linking, and DNA strand breakage. Protein phosphorylation is an epigenetic modification, not direct DNA damage.",
        "source_citation": "Hayes Ch. 26, pp. 1417-1418",
        "bloom_level": "Recall",
        "format": "EXCEPT/NOT",
        "sub_domain": "A.Design"
    },
    {
        "question_text": "According to Hayes Ch. 26, which of the following is NOT a component of the ICH S2(R1) Option 2 genetic test battery?",
        "options": {
            "A": "Bacterial reverse mutation assay (OECD 471)",
            "B": "In vivo micronucleus assay (OECD 474)",
            "C": "In vitro mouse lymphoma TK gene mutation assay (OECD 490)",
            "D": "In vivo Comet assay (OECD 489)"
        },
        "correct_answer": "C",
        "explanation": "Option 2 of ICH S2(R1) consists of bacterial reverse mutation assay (OECD 471) and in vivo assessment with two tissues (typically MN assay OECD 474 and Comet assay OECD 489). The in vitro mouse lymphoma TK assay (OECD 490) is part of Option 1, not Option 2.",
        "source_citation": "Hayes Ch. 26, pp. 1424-1425",
        "bloom_level": "Application",
        "format": "EXCEPT/NOT",
        "sub_domain": "A.Design"
    },
    {
        "question_text": "According to Hayes Ch. 26, which of the following is NOT one of the three criteria for a clearly positive genotoxicity result?",
        "options": {
            "A": "Statistically significant increase compared with concurrent negative control",
            "B": "Dose-related increase in at least one experimental condition",
            "C": "Result outside the distribution of historical negative control data",
            "D": "Confirmation by two independent laboratories"
        },
        "correct_answer": "D",
        "explanation": "The three criteria for a clearly positive result are: (1) statistically significant increase vs. concurrent negative control, (2) dose-related increase, and (3) results outside historical negative control data distribution. Confirmation by two independent laboratories is not one of these criteria.",
        "source_citation": "Hayes Ch. 26, pp. 1425-1426",
        "bloom_level": "Application",
        "format": "EXCEPT/NOT",
        "sub_domain": "A.Design"
    },
    {
        "question_text": "According to Hayes Ch. 27, which of the following is NOT a characteristic of epigenetic (non-genotoxic) carcinogens?",
        "options": {
            "A": "They are generally inactive in genotoxicity assays",
            "B": "They typically require high-level or sustained administration",
            "C": "They directly form covalent adducts with nuclear DNA",
            "D": "They often produce tumors only in a single tissue"
        },
        "correct_answer": "C",
        "explanation": "Table 27.2 describes epigenetic carcinogens as NOT being DNA reactive. They do not directly form covalent adducts with nuclear DNA. They typically require high-level/sustained exposure, are inactive in genotoxicity assays, and often affect only a single tissue.",
        "source_citation": "Hayes Ch. 27, pp. 1459",
        "bloom_level": "Recall",
        "format": "EXCEPT/NOT",
        "sub_domain": "A.Design"
    },
    {
        "question_text": "According to Hayes Ch. 27, which of the following is NOT listed as a mechanism by which epigenetic carcinogens produce tumors?",
        "options": {
            "A": "Tumor promotion through enhanced cell proliferation",
            "B": "Endocrine modulation via receptor binding",
            "C": "Direct alkylation of guanine at the O6 position",
            "D": "PPAR-alpha agonism leading to hepatocellular proliferation"
        },
        "correct_answer": "C",
        "explanation": "Direct alkylation of guanine at the O6 position is a mechanism of DNA-reactive (genotoxic) carcinogens, not epigenetic carcinogens. Epigenetic mechanisms include tumor promotion, endocrine modulation, PPAR-alpha agonism, cytotoxicity-induced regeneration, immunosuppression, and urinary pH extremes.",
        "source_citation": "Hayes Ch. 27, pp. 1459-1461",
        "bloom_level": "Application",
        "format": "EXCEPT/NOT",
        "sub_domain": "A.Design"
    },
    {
        "question_text": "A toxicologist is reviewing results from a 2-year rat bioassay. The high-dose group shows a marginal increase in pituitary gland adenomas compared to the concurrent control, but the incidence is within the range of historical control data. The concurrent control group has an unusually low incidence. According to Hayes Ch. 27, how should this finding be interpreted?",
        "options": {
            "A": "Conclude that the chemical is a pituitary carcinogen based on the high-dose increase",
            "B": "The HCD comparison suggests this may be an incidental inter-group difference rather than a treatment-related effect, since dosed animal incidences are within HCD range",
            "C": "Ignore the finding entirely because it is not statistically significant",
            "D": "Request a repeat study with more animals"
        },
        "correct_answer": "B",
        "explanation": "The chapter provides a similar example where high pituitary tumors in dosed rats had a concurrent control group with extraordinarily low incidence, and dosed animal incidences were within the range of HCD and only slightly above the mean. This was taken as evidence for an incidental inter-group difference rather than a true carcinogenic effect.",
        "source_citation": "Hayes Ch. 27, pp. 1472-1473",
        "bloom_level": "Analysis",
        "format": "vignette",
        "sub_domain": "A.Design"
    }
]

data.extend(new_questions)

with open('/root/work/dabt/dabt-tutor/batches/synthetic/domain_i_a_batch_5.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f'Total questions: {len(data)}')

formats = {}
blooms = {}
for q in data:
    fmt = q['format']
    bloom = q['bloom_level']
    formats[fmt] = formats.get(fmt, 0) + 1
    blooms[bloom] = blooms.get(bloom, 0) + 1

print('Format distribution:')
for k,v in sorted(formats.items()):
    print(f'  {k}: {v} ({v/len(data)*100:.0f}%)')

print('Bloom distribution:')
for k,v in sorted(blooms.items()):
    print(f'  {k}: {v} ({v/len(data)*100:.0f}%)')
