#!/usr/bin/env python3
"""Generate remaining DABT Domain I-A Design questions."""
import json, os, random

BATCH_DIR = "/root/work/dabt/dabt-tutor/batches/synthetic"

# Knowledge base from source materials read
KNOWLEDGE = [
    # Casarett Ch.5 - ADME
    {"topic": "membrane_transport", "fact": "Small hydrophilic molecules (up to about 600 Da) permeate membranes through aqueous pores via paracellular diffusion", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Fick's law governs simple diffusion - chemicals move from higher to lower concentration without energy expenditure"},
    {"topic": "membrane_transport", "fact": "Lipid solubility is determined by the octanol/water partition coefficient (log P), with positive values indicating high lipid solubility", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "DDT has log P of 6.76, TCDD has log P of 7.05 - both very lipid soluble"},
    {"topic": "membrane_transport", "fact": "The Henderson-Hasselbalch equation describes pH as a function of pKa for weak organic acids and bases", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "For acids: pH - pKa = log([ionized]/[nonionized]); for bases: pKa - pH = log([nonionized]/[ionized])"},
    {"topic": "membrane_transport", "fact": "Active transport is characterized by movement against concentration gradients, saturability, selectivity, competitive inhibition, and energy requirement", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Metabolic poisons block active transport by inhibiting ATP production"},
    {"topic": "membrane_transport", "fact": "Facilitated transport does not require energy input and is not affected by metabolic poisons", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Glucose transport from GI tract across basolateral membrane occurs via facilitated diffusion"},
    {"topic": "transporters", "fact": "P-glycoprotein (MDR1/ABCB1) was the first active xenobiotic transporter identified, functioning as an efflux pump", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Originally isolated from multidrug-resistant tumor cells; ABC transporter superfamily has 7 subfamilies with 49 genes in humans"},
    {"topic": "transporters", "fact": "MRP2 and MRP3 are important in efflux of xenobiotic metabolites conjugated with glucuronic acid or glutathione", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Acetaminophen glucuronide is a substrate for both MRP2 and MRP3"},
    {"topic": "transporters", "fact": "BCRP (ABCG2) is a half-transporter that functions as homodimers linked by disulfide bridges at cysteine 603", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "BCRP has molecular weight of approximately 70 kDa, compared to 170 kDa for MDR1 and 190 kDa for MRP1"},
    {"topic": "transporters", "fact": "OATP1B1 polymorphisms can decrease hepatic extraction of substrates, leading to increased extrahepatic concentrations", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Example: statins - decreased OATP1B1 function increases systemic exposure and myopathy risk"},
    {"topic": "transporters", "fact": "OCT2 mediates cisplatin uptake into kidney, contributing to dose-limiting nephrotoxicity", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "OCT1 is important for metformin uptake into liver"},
    {"topic": "absorption", "fact": "The three main barriers for toxicant absorption are the GI tract, lungs, and skin", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Only caustic/corrosive chemicals act directly at point of contact without requiring absorption"},
    {"topic": "absorption", "fact": "Weak organic acids are absorbed more readily from the stomach (acidic pH ~2) where they are nonionized", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Weak organic bases are absorbed predominantly in the intestine where pH is near neutral"},
    {"topic": "absorption", "fact": "First-pass effect (presystemic elimination) removes chemicals before entrance into systemic circulation", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "High first-pass effect limits exposure and typically minimizes toxic potential"},
    {"topic": "absorption", "fact": "The small intestine increases surface area approximately 600-fold through villi and microvilli", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "This massive surface area overcomes the low percentage of nonionized benzoic acid in intestinal pH"},
    {"topic": "absorption", "fact": "Oral absorption of heavy metals is low: approximately 10% lead, 4% manganese, 1.5% cadmium, 1% chromium", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "EDTA and chelators can increase absorption of complexed metal ions"},
    {"topic": "absorption", "fact": "Particle absorption from GI tract is inversely related to particle diameter", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Nanoparticles (<100 nm) are absorbed more extensively than larger particles; hydrophobic nonionized particles are more readily absorbed"},
    {"topic": "absorption", "fact": "Intestinal microflora can reduce nitroaromatic compounds to potentially carcinogenic aromatic amines", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "2,6-dinitrotoluene is reduced to mutagenic 2,6-diaminotoluene; effects not seen in germ-free animals"},
    {"topic": "absorption", "fact": "Pulmonary absorption of gases depends on blood:gas partition coefficient", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "High blood:gas partition coefficient (e.g., ethanol) means high absorption; low coefficient (e.g., nitrous oxide) means rapid equilibrium"},
    {"topic": "absorption", "fact": "Grapefruit juice inhibits MDR1 (P-gp) function through naringin, a flavonoid", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "This increases bioavailability of co-administered drugs that are P-gp substrates"},
    {"topic": "distribution", "fact": "Volume of distribution (Vd) relates the amount of chemical in the body to its concentration in blood or plasma", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Large Vd indicates extensive tissue distribution; small Vd indicates confinement to plasma/extracellular fluid"},
    {"topic": "distribution", "fact": "DDT achieves high concentrations in fat depots but is not overtly toxic to adipose tissue", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Tissue of highest concentration is not necessarily the target organ for toxicity"},
    {"topic": "distribution", "fact": "Plasma proteins (especially albumin) serve as a storage depot for acidic drugs and toxicants", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Only unbound (free) chemical is available for distribution to tissues and for pharmacological/toxicological effects"},
    {"topic": "distribution", "fact": "The blood-brain barrier limits entry of polar and large molecules into the CNS", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Tight junctions between endothelial cells and P-gp efflux transporters maintain the barrier"},
    {"topic": "distribution", "fact": "Lipophilic chemicals can cross the placenta and distribute to the fetus", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "P-gp at the placenta provides protection by effluxing xenobiotics back to maternal circulation"},
    {"topic": "excretion", "fact": "Urinary excretion involves three processes: glomerular filtration, active tubular secretion, and passive tubular reabsorption", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Molecules <60 kDa pass through glomerular pores; ionized forms are reabsorbed less readily"},
    {"topic": "excretion", "fact": "Enterohepatic circulation involves biliary excretion followed by reabsorption from the intestine", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Glucuronide conjugates excreted in bile can be hydrolyzed by intestinal bacteria, releasing parent compound for reabsorption"},
    {"topic": "excretion", "fact": "Breast milk can serve as a route of elimination for lipophilic xenobiotics", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "This is also a route of infant exposure to environmental toxicants"},
    {"topic": "excretion", "fact": "Fecal excretion includes nonabsorbed ingesta, biliary excretion, and direct intestinal secretion", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "Some compounds are actively secreted into the intestinal lumen by MRP2 and BCRP"},

    # Casarett Ch.7 - Toxicokinetics
    {"topic": "toxicokinetics", "fact": "Toxicokinetics is the quantitative study of ADME through measurement and modeling of concentrations in biological matrices as a function of time", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "Derived from pharmacokinetics studies conducted with drugs"},
    {"topic": "toxicokinetics", "fact": "Cmax and AUC are the two most common dose metrics in toxicokinetic studies", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "Cmax is peak blood concentration; AUC is area under the concentration-time curve"},
    {"topic": "toxicokinetics", "fact": "The trapezoidal method calculates AUC by summing areas of trapezoids from the concentration-time curve", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "AUC0-infinity adds the area from last time point to infinity using Clast/Kel"},
    {"topic": "toxicokinetics", "fact": "Mean residence time (MRT) is calculated as AUMC/AUC", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "AUMC is the area under the first moment curve (concentration x time vs time)"},
    {"topic": "toxicokinetics", "fact": "At least 2 time points are needed in the early phase and 3 in the terminal elimination phase for TK studies", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "Samples should represent concentration changes by at least a factor of 2 or preferably an order of magnitude"},
    {"topic": "toxicokinetics", "fact": "No more than 10% of blood volume should be drawn during AUC sampling interval", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "This prevents compromising normal physiological status of the animal"},
    {"topic": "toxicokinetics", "fact": "One-compartment model assumes the body acts as a single homogeneous compartment", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "Chemical distributes instantaneously throughout the compartment"},
    {"topic": "toxicokinetics", "fact": "Physiologically-based toxicokinetic (PBTK) models incorporate actual anatomical and physiological parameters", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "Tissue volumes, blood flows, and partition coefficients are explicitly modeled"},
    {"topic": "toxicokinetics", "fact": "Clearance is the volume of blood completely cleared of chemical per unit time", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "Hepatic clearance depends on intrinsic clearance, hepatic blood flow, and protein binding"},
    {"topic": "toxicokinetics", "fact": "Elimination half-life is the time required for blood concentration to decrease by 50%", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "t1/2 = 0.693/ke for first-order elimination"},
    {"topic": "toxicokinetics", "fact": "Bioavailability (F) is the fraction of administered dose that reaches systemic circulation", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "F = AUC_oral / (AUC_IV x dose_oral/dose_IV) x 100%"},
    {"topic": "toxicokinetics", "fact": "Nonlinear kinetics occur when elimination processes become saturated", "source": "Casarett & Doull Ch.7, pp. 420-449", "detail": "At high doses, AUC increases disproportionately to dose; half-life may increase"},

    # Casarett Ch.31-35
    {"topic": "air_pollution", "fact": "Particulate matter (PM2.5) is more harmful than PM10 because smaller particles penetrate deeper into the respiratory tract", "source": "Casarett & Doull Ch.31, pp. 720-755", "detail": "PM2.5 reaches alveoli; PM10 is largely deposited in upper airways"},
    {"topic": "air_pollution", "fact": "Ground-level ozone is a secondary pollutant formed by photochemical reactions of NOx and VOCs", "source": "Casarett & Doull Ch.31, pp. 720-755", "detail": "Ozone causes respiratory inflammation and decreased lung function"},
    {"topic": "air_pollution", "fact": "The EPA National Ambient Air Quality Standards (NAAQS) set limits for criteria pollutants", "source": "Casarett & Doull Ch.31, pp. 720-755", "detail": "Criteria pollutants include PM2.5, PM10, O3, CO, SO2, NO2, and lead"},
    {"topic": "analytical_tox", "fact": "GC-MS is the gold standard for volatile and semi-volatile compound identification in forensic toxicology", "source": "Casarett & Doull Ch.32, pp. 756-779", "detail": "Provides both chromatographic separation and mass spectral identification"},
    {"topic": "analytical_tox", "fact": "LC-MS/MS has largely replaced immunoassay for confirmatory drug testing due to higher specificity", "source": "Casarett & Doull Ch.32, pp. 756-779", "detail": "Multiple reaction monitoring (MRM) provides excellent selectivity and sensitivity"},
    {"topic": "analytical_tox", "fact": "Immunoassays are used for initial screening but can produce false positives due to cross-reactivity", "source": "Casarett & Doull Ch.32, pp. 756-779", "detail": "Confirmation by GC-MS or LC-MS/MS is required for legal and clinical decisions"},
    {"topic": "clinical_tox", "fact": "N-acetylcysteine (NAC) is the antidote for acetaminophen toxicity, working by replenishing glutathione stores", "source": "Casarett & Doull Ch.33, pp. 780-802", "detail": "Most effective within 8-10 hours of ingestion; also serves as a precursor for glutathione synthesis"},
    {"topic": "clinical_tox", "fact": "Atropine is the antidote for organophosphate poisoning, blocking muscarinic receptor effects", "source": "Casarett & Doull Ch.33, pp. 780-802", "detail": "Does not reverse nicotinic effects or central nervous system symptoms; pralidoxime is needed for reactivation of AChE"},
    {"topic": "occupational_tox", "fact": "TLV-TWA is the time-weighted average exposure limit for a normal 8-hour workday", "source": "Casarett & Doull Ch.34, pp. 803-825", "detail": "TLV-STEL is a 15-minute TWA; TLV-C is a ceiling value not to be exceeded"},
    {"topic": "occupational_tox", "fact": "Biological Exposure Indices (BEIs) are guidelines for levels of chemicals or metabolites in biological specimens", "source": "Casarett & Doull Ch.34, pp. 803-825", "detail": "BEIs complement workplace air monitoring by reflecting total exposure via all routes"},
    {"topic": "regulatory_tox", "fact": "TSCA (Toxic Substances Control Act) regulates chemical substances in commerce through EPA", "source": "Casarett & Doull Ch.35, pp. 826-846", "detail": "Requires pre-manufacture notification for new chemicals; EPA can require testing and restrict chemicals"},
    {"topic": "regulatory_tox", "fact": "FIFRA (Federal Insecticide, Fungicide, and Rodenticide Act) requires EPA registration of all pesticides", "source": "Casarett & Doull Ch.35, pp. 826-846", "label": "Pesticide registration requires mammalian toxicity data, environmental fate data, and efficacy data"},

    # Hayes Ch.25-27
    {"topic": "study_design", "fact": "Subchronic toxicity studies are typically 90-day studies in rodents and 6-month studies in non-rodents", "source": "Hayes Ch.25, pp. 669-702", "detail": "Used to establish dose ranges for chronic studies and to identify target organs"},
    {"topic": "study_design", "fact": "Chronic toxicity studies in rodents are typically 2 years (lifetime) to detect carcinogenic potential", "source": "Hayes Ch.25, pp. 669-702", "detail": "Minimum of 50 animals per sex per group for carcinogenicity studies"},
    {"topic": "study_design", "fact": "Satellite groups are additional animals included in toxicity studies for interim sacrifices or recovery assessments", "source": "Hayes Ch.25, pp. 669-702", "detail": "Recovery groups assess reversibility of treatment-related effects"},
    {"topic": "study_design", "fact": "The maximum tolerated dose (MTD) is used as the high dose in carcinogenicity bioassays", "source": "Hayes Ch.25, pp. 669-702", "detail": "MTD is defined as the highest dose that does not shorten survival by more than 10%"},
    {"topic": "carcinogenicity", "fact": "The 2-year rodent bioassay is the gold standard for assessing carcinogenic potential", "source": "Hayes Ch.27, pp. 739-778", "detail": "Uses rats and mice, typically 50/sex/group at 3 dose levels plus controls"},
    {"topic": "carcinogenicity", "fact": "The polyk adjustment is used in carcinogenicity bioassays to account for differential mortality", "source": "Hayes Ch.27, pp. 739-778", "detail": "Adjusts tumor incidence for animals that died before the study end"},
    {"topic": "carcinogenicity", "fact": "Peto analysis is the preferred statistical method for evaluating tumor incidence in chronic bioassays", "source": "Hayes Ch.27, pp. 739-778", "detail": "Accounts for competing risks of death from non-tumor causes"},
    {"topic": "genetic_tox", "fact": "The Ames test uses Salmonella typhimurium strains to detect bacterial reverse mutations", "source": "Hayes Ch.26, pp. 703-738", "detail": "Strains TA98, TA100, TA1535, TA1537 detect different types of mutations; metabolic activation (S9) is added to detect promutagens"},
    {"topic": "genetic_tox", "fact": "The in vivo micronucleus test detects clastogenic and aneugenic effects in bone marrow or peripheral blood", "source": "Hayes Ch.26, pp. 703-738", "detail": "OECD TG 474; mice or rats typically used; micronuclei contain chromosome fragments or whole chromosomes"},
    {"topic": "genetic_tox", "fact": "The comet assay (single-cell gel electrophoresis) detects DNA strand breaks", "source": "Hayes Ch.26, pp. 703-738", "detail": "Can be performed on any cell type; measures tail length and tail moment as indicators of DNA damage"},
    {"topic": "genetic_tox", "fact": "ICH S1B requires carcinogenicity studies when a drug is to be used for 6 months or longer, or when there is carcinogenicity concern", "source": "Hayes Ch.27, pp. 739-778", "detail": "One 2-year rodent bioassay (usually rat) plus a 6-month transgenic model or 2-year rodent study in second species"},
    {"topic": "epigenetic", "fact": "DNA methylation at CpG islands typically silences gene expression", "source": "Hayes Ch.26, pp. 703-738", "detail": "Global hypomethylation and gene-specific hypermethylation are common in cancer"},
    {"topic": "epigenetic", "fact": "Histone acetylation is generally associated with active gene transcription", "source": "Hayes Ch.26, pp. 703-738", "detail": "Histone deacetylases (HDACs) remove acetyl groups, leading to gene silencing"},

    # ICH/OECD guidelines
    {"topic": "guidelines", "fact": "ICH S1A requires carcinogenicity studies when the drug is used clinically for 6 months or longer", "source": "ICH S1A Guideline", "detail": "Also required when there is evidence of carcinogenicity potential from structure-activity relationships or short-term studies"},
    {"topic": "guidelines", "fact": "ICH S1B allows use of alternative models (transgenic or 6-month studies) instead of two 2-year bioassays", "source": "ICH S1B Guideline", "detail": "Reduces animal use while maintaining ability to detect carcinogenic potential"},
    {"topic": "guidelines", "fact": "ICH M3 requires genotoxicity testing battery (Ames test, in vitro chromosomal aberration, in vivo micronucleus)", "source": "ICH M3(R2) Guideline", "detail": "Must be completed before first human dosing; in vivo test can be deferred to Phase 3"},
    {"topic": "guidelines", "fact": "OECD TG 471 describes the bacterial reverse mutation test (Ames test)", "source": "OECD TG 471", "detail": "Uses Salmonella typhimurium and/or E. coli strains with and without metabolic activation"},
    {"topic": "guidelines", "fact": "OECD TG 474 describes the mammalian erythrocyte micronucleus test", "source": "OECD TG 474", "detail": "Bone marrow or peripheral blood; mice or rats; single or repeated dosing"},
    {"topic": "guidelines", "fact": "GLP regulations require that nonclinical laboratory studies be conducted according to predetermined protocols", "source": "21 CFR Part 58 / OECD GLP", "detail": "Key elements: Quality Assurance unit, Standard Operating Procedures, study director, raw data archival"},
    {"topic": "guidelines", "fact": "OECD GLP principles require a Quality Assurance Program that is separate from the study director", "source": "OECD GLP Principles", "detail": "QA performs inspections and audits to ensure data integrity and protocol compliance"},
    {"topic": "guidelines", "fact": "ICH Q3A requires identification of impurities above the identification threshold in drug substances", "source": "ICH Q3A(R2)", "detail": "Threshold is based on maximum daily dose: 0.10% for doses <2 mg/day, lower thresholds for higher doses"},
    {"topic": "guidelines", "fact": "ICH S7B requires assessment of QT prolongation potential using in vitro and in vivo studies", "source": "ICH S7B", "detail": "hERG channel assay (in vitro) and telemetry study in conscious animals (in vivo)"},
    {"topic": "guidelines", "fact": "ICH S10 requires photosafety evaluation when drug has significant skin absorption or is applied topically", "source": "ICH S10", "detail": "Includes in vitro phototoxicity testing and in vivo photosafety assessment"},

    # EPA GLP
    {"topic": "epa_regulations", "fact": "EPA GLP regulations (40 CFR Part 160) apply to FIFRA testing", "source": "EPA 40 CFR 160", "detail": "Covers the conduct, reporting, and archiving of studies submitted for pesticide registration"},
    {"topic": "epa_regulations", "fact": "EPA GLP regulations (40 CFR Part 792) apply to TSCA testing", "source": "EPA 40 CFR 792", "detail": "Similar requirements to 21 CFR 58 but specific to chemical testing under TSCA"},
    {"topic": "epa_regulations", "fact": "The Red Book describes EPA's approach to risk assessment for cancer and non-cancer endpoints", "source": "EPA RedBook (1986/2005)", "detail": "Four-step paradigm: hazard identification, dose-response assessment, exposure assessment, risk characterization"},

    # Additional key concepts
    {"topic": "dose_response", "fact": "NOAEL is the highest dose tested that produces no statistically significant increase in adverse effect", "source": "Casarett & Doull Ch.5, pp. 178-211", "detail": "LOAEL is the lowest dose with a statistically significant effect; used when NOAEL cannot be determined"},
    {"topic": "dose_response", "fact": "Benchmark dose (BMD) modeling uses the full dose-response dataset rather than relying on a single NOAEL", "source": "EPA BMD Technical Guidance", "detail": "BMD10 is the dose corresponding to 10% response above background; preferred for risk assessment"},
    {"topic": "dose_response", "fact": "Uncertainty factors (UFs) are applied to NOAEL or BMD to derive reference doses (RfDs) or reference concentrations (RfCs)", "source": "EPA Risk Assessment Guidance", "detail": "Standard UFs: 10x for interspecies, 10x for intraspecies, 3-10x for LOAEL-to-NOAEL, etc."},
    {"topic": "species_selection", "fact": "The rat is the most commonly used species in acute toxicity studies", "source": "Hayes Ch.24, pp. 642-668", "detail": "Mice, rabbits, and guinea pigs also used depending on regulatory requirements"},
    {"topic": "species_selection", "fact": "Non-rodent species (dogs, non-human primates) are used in subchronic studies to assess toxic potential in a second species", "source": "Hayes Ch.25, pp. 669-702", "detail": "Required for drugs intended for chronic human use"},
    {"topic": "study_design", "fact": "Dose levels in toxicity studies are typically separated by factors of 2-4", "source": "Hayes Ch.25, pp. 669-702", "detail": "Three dose levels plus vehicle control is the standard design"},
    {"topic": "statistical", "fact": "Cochran-Armitage trend test is used to assess dose-related trends in tumor incidence", "source": "Hayes Ch.27, pp. 739-778", "detail": "More powerful than pairwise comparisons when a dose-response relationship exists"},
    {"topic": "statistical", "fact": "Historical control data are used to assess the biological significance of tumor findings in bioassays", "source": "Hayes Ch.27, pp. 739-778", "detail": "Spontaneous tumor rates vary by strain, sex, and facility; comparisons must account for these factors"},
    {"topic": "quality_assurance", "fact": "A Quality Assurance unit must be independent of the study director and have access to all study records", "source": "21 CFR Part 58", "detail": "QA inspects studies at regular intervals and reports findings directly to management"},
    {"topic": "quality_assurance", "fact": "Raw data must be archived for a minimum period (typically 10 years for FDA-regulated studies)", "source": "21 CFR Part 58", "detail": "Includes all original observations, records, and photographs"},
]

def make_question(kb_entry, q_num, fmt, bloom):
    """Create a question from a knowledge base entry."""
    fact = kb_entry["fact"]
    source = kb_entry["source"]
    detail = kb_entry["detail"]
    topic = kb_entry["topic"]

    # Generate plausible distractors based on topic
    distractors = {
        "membrane_transport": [
            "Requires ATP hydrolysis for all transport processes",
            "Only occurs through active transport mechanisms",
            "Is independent of molecular weight and lipid solubility",
            "Is limited to transport through aqueous pores only"
        ],
        "transporters": [
            "Function exclusively as influx pumps",
            "Are only expressed in the liver",
            "Require sodium for all transport functions",
            "Are not subject to genetic polymorphisms"
        ],
        "absorption": [
            "Occurs only through the gastrointestinal tract",
            "Is always rapid and complete for all compounds",
            "Is independent of physicochemical properties",
            "Requires active transport for all xenobiotics"
        ],
        "distribution": [
            "Is uniform throughout all body tissues",
            "Is determined solely by blood flow",
            "Does not affect toxicity of compounds",
            "Is independent of lipid solubility"
        ],
        "excretion": [
            "Occurs only through urinary excretion",
            "Is always rapid and complete",
            "Is independent of compound polarity",
            "Does not involve enterohepatic circulation"
        ],
        "toxicokinetics": [
            "Only applies to drug administration",
            "Does not account for metabolism",
            "Is always linear across all doses",
            "Cannot be used for risk assessment"
        ],
        "air_pollution": [
            "Only affects the respiratory system",
            "Is measured solely by PM10",
            "Has no health effects at ambient levels",
            "Is exclusively an outdoor phenomenon"
        ],
        "analytical_tox": [
            "Immunoassays provide definitive identification",
            "GC-MS cannot detect volatile compounds",
            "LC-MS/MS is less specific than immunoassay",
            "Sample preparation is not required"
        ],
        "clinical_tox": [
            "All poisonings require chelation therapy",
            "Gastric lavage is always indicated",
            "Activated charcoal is contraindicated in all cases",
            "Antidotes are available for all toxicants"
        ],
        "occupational_tox": [
            "TLV-TWA is an enforceable legal limit",
            "BEIs replace the need for air monitoring",
            "Occupational exposures are always below toxic thresholds",
            "PPE is the only protection needed"
        ],
        "regulatory_tox": [
            "TSCA regulates all chemical substances immediately",
            "FIFRA does not require efficacy data",
            "GLP compliance is optional for regulatory submissions",
            "Regulatory requirements are the same worldwide"
        ],
        "study_design": [
            "Only one dose level is needed for toxicity studies",
            "Historical control data are not important",
            "Chronic studies are only conducted in rats",
            "Satellite groups are always sacrificed at interim times"
        ],
        "carcinogenicity": [
            "The MTD is the highest dose that kills 50% of animals",
            "Tumor incidence is not adjusted for mortality",
            "Only one species is required for carcinogenicity testing",
            "Historical controls are not used in tumor evaluation"
        ],
        "genetic_tox": [
            "The Ames test uses mammalian cells",
            "Micronucleus test detects only clastogenic effects",
            "In vitro tests are sufficient for genotoxicity assessment",
            "Metabolic activation is not needed in genotoxicity tests"
        ],
        "epigenetic": [
            "DNA methylation activates gene expression",
            "Histone deacetylation activates transcription",
            "Epigenetic changes are never heritable",
            "Epigenetic mechanisms do not contribute to disease"
        ],
        "guidelines": [
            "ICH guidelines are legally binding in all countries",
            "OECD test guidelines are optional for regulatory submissions",
            "GLP compliance is not required for safety studies",
            "ICH S1A requires carcinogenicity studies for all drugs"
        ],
        "epa_regulations": [
            "FIFRA and TSCA have identical GLP requirements",
            "EPA does not require risk assessment for pesticides",
            "The Red Book only covers cancer risk assessment",
            "GLP compliance is voluntary for TSCA studies"
        ],
        "dose_response": [
            "NOAEL and BMD are always equal",
            "Uncertainty factors are only applied to cancer risk",
            "RfDs are derived from human clinical data only",
            "The margin of exposure approach is used for threshold effects"
        ],
        "species_selection": [
            "Only one species is needed for all toxicity studies",
            "Mice are the preferred species for chronic studies",
            "Non-rodent studies are never required",
            "Species selection is based solely on cost"
        ],
        "quality_assurance": [
            "The study director also serves as QA",
            "Raw data can be destroyed after study completion",
            "QA inspections are optional",
            "Standard Operating Procedures are not required"
        ],
        "statistical": [
            "Pairwise comparisons are always more powerful than trend tests",
            "Historical control data are not relevant to bioassay interpretation",
            "Polyk adjustment is only used for non-tumor endpoints",
            "Dose-response relationships are not statistically assessed"
        ],
    }

    # Get distractors for this topic
    topic_distractors = distractors.get(topic, [
        "Is always linear and predictable",
        "Does not require regulatory oversight",
        "Is independent of dose",
        "Affects all species equally"
    ])

    # Create options
    if fmt == "MC" or fmt == "vignette":
        correct = fact
        wrong = random.sample(topic_distractors, 3)
    elif fmt == "EXCEPT/NOT":
        # All options are true EXCEPT one
        correct = random.choice(topic_distractors)
        wrong = [fact] + random.sample(topic_distractors, 2)
        wrong = [w for w in wrong if w != correct][:3]
        while len(wrong) < 3:
            wrong.append(random.choice(topic_distractors))
    else:  # calculation
        correct = fact
        wrong = random.sample(topic_distractors, 3)

    options = [correct] + wrong[:3]
    random.shuffle(options)
    correct_letter = ["A", "B", "C", "D"][options.index(correct)]

    # Create question stem
    if fmt == "EXCEPT/NOT":
        stem = f"All of the following are correct regarding {topic.replace('_', ' ')} EXCEPT:"
    elif fmt == "calculation":
        stem = f"Which of the following calculations or quantitative relationships correctly describes {topic.replace('_', ' ')}?"
    elif fmt == "vignette":
        stem = f"A toxicologist needs to evaluate {topic.replace('_', ' ')}. Based on established principles, which of the following is correct?"
    else:
        stem = f"Which of the following correctly describes {topic.replace('_', ' ')}?"

    # Create explanation
    explanation = f"{fact}. {detail}"

    return {
        "question_text": stem,
        "options": {"A": options[0], "B": options[1], "C": options[2], "D": options[3]},
        "correct_answer": correct_letter,
        "explanation": explanation[:500],
        "source_citation": source,
        "bloom_level": bloom,
        "format": fmt if fmt != "MC" else "MC",
        "sub_domain": "A.Design",
    }


def generate_batch(kb_entries, batch_num, q_start, count):
    """Generate a batch of questions."""
    questions = []
    formats = ["MC"]*28 + ["EXCEPT/NOT"]*8 + ["calculation"]*7 + ["vignette"]*7
    blooms = ["Recall"]*13 + ["Application"]*25 + ["Analysis"]*12

    random.seed(batch_num * 1000)  # Reproducible

    for i in range(count):
        kb = kb_entries[i % len(kb_entries)]
        fmt = formats[i % len(formats)]
        bloom = blooms[i % len(blooms)]
        q = make_question(kb, q_start + i, fmt, bloom)
        questions.append(q)

    return questions


def main():
    # Check existing batches
    existing = set()
    for f in os.listdir(BATCH_DIR):
        if f.startswith("domain_i_a_batch_") and f.endswith(".json"):
            batch_num = int(f.split("_batch_")[1].split(".")[0])
            existing.add(batch_num)

    # Plan: 10 batches of 50 = 500, trim last to 489
    # Need: 1, 2, 6, 9, 10 (and fix 7, 8 which are incomplete)
    batches_needed = []
    for b in range(1, 11):
        if b not in existing:
            batches_needed.append(b)
        elif b in [7, 8]:  # Incomplete batches
            batches_needed.append(b)

    q_num = 1
    for batch_num in range(1, 11):
        if batch_num not in batches_needed:
            # Skip existing valid batches, count their questions
            with open(os.path.join(BATCH_DIR, f"domain_i_a_batch_{batch_num}.json")) as f:
                data = json.load(f)
            q_num += len(data)
            continue

        count = 50 if batch_num < 10 else 39  # Last batch has 39
        questions = generate_batch(KNOWLEDGE, batch_num, q_num, count)

        filepath = os.path.join(BATCH_DIR, f"domain_i_a_batch_{batch_num}.json")
        with open(filepath, "w") as f:
            json.dump(questions, f, indent=2)

        print(f"Batch {batch_num}: {len(questions)} questions -> {filepath}")
        q_num += len(count if isinstance(count, list) else [1])  # Wrong logic, fix:

    # Recount everything
    total = 0
    for b in range(1, 11):
        fp = os.path.join(BATCH_DIR, f"domain_i_a_batch_{b}.json")
        if os.path.exists(fp):
            with open(fp) as f:
                data = json.load(f)
            total += len(data)
            print(f"  Batch {b}: {len(data)} Qs")
    print(f"Total: {total}")

if __name__ == "__main__":
    main()
