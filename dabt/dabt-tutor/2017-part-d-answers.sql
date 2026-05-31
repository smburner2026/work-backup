-- 2017 ABT Certification Exam Part D (Questions 1-100)
-- Answers determined from Casarett & Doull 9e and Hayes 7e reference texts
-- and standard toxicology knowledge

-- D_1: Acute toxicity study provides all of the above (lethal dose, target organs, dose selection)
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5143';

-- D_2: High variability in plasma concentration likely due to CYP2D6 polymorphism
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5144';

-- D_3: Cheese wrapper mold inhibitor - must demonstrate no migration AND toxicity data
-- For food contact substances, must show safety and that it doesn't migrate into food
UPDATE questions SET correct_answer_letter = 'F' WHERE id = 'DABT-5145';

-- D_4: Plastic packaging additive - all of the above required
-- Indirect food additive requires efficacy, migration data, lowest effective level, toxicity data
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5146';

-- D_5: Non-GRAS food additive safety testing - A, B, and C are true
-- D is false because Delaney Clause prohibits carcinogens in food additives
UPDATE questions SET correct_answer_letter = 'F' WHERE id = 'DABT-5147';

-- D_6: High casein diet reduces spontaneous hepatoma incidence in mice
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5148';

-- D_7: Most important in pesticide development = selective toxicity
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5149';

-- D_8: Relative potency is least important in drug selection
-- Efficacy, safety, duration, and elimination route are more clinically relevant
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5150';

-- D_9: Fertility index = (pregnancies / successful matings) × 100
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5151';

-- D_10: Dominant lethal - positive indicates reduced fertility/implantations AND increased post-implantation death
-- Both B and C are indicators of dominant lethal effects
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5152';

-- D_11: Fertility depressed first 7 days then recovers - affects spermatozoa (mature sperm)
-- Spermatogonia damage would affect later weeks
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5153';

-- D_12: Most mutagenicity assays are NOT accurate predictors of in vivo potency
-- Short-term assays are screening tools
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5154';

-- D_13: Ames test is a widely used screening test (A is true)
-- Not host-mediated assay (B false); uses his- strains needing histidine (C true per wording)
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5155';

-- D_14: Guinea pig is species of choice for skin contact allergen testing (GPMT, Buehler)
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5156';

-- D_15: Fertility index is not monitored in rat teratology study
-- Teratology studies assess fetuses, not mating success
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5157';

-- D_16: Teratogenic potential best assessed by malformations and embryolethality
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5158';

-- D_17: Best teratology testing regimen = exposure during organogenesis, 3 dose levels, negative control
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5159';

-- D_18: Rat at 20 months - chronic progressive glomerulonephrosis (common spontaneous finding in aging rats)
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5160';

-- D_19: Multigeneration study best assesses chronic low-level effects on reproduction, growth, survival
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5161';

-- D_20: Corneal damage gives highest Draize scores (cornea weighted most heavily in scoring)
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5162';

-- D_21: Clastogenesis detection - micronucleus test and chromosomal observation (B and D)
-- Ames = gene mutation; fungal aneuploidization = aneuploidy
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5163';

-- D_22: TA1535 is sensitive to base-pair substitution mutagens
-- TA1537/TA1538 detect frameshifts
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5164';

-- D_23: Minute volume = RR × TV = 100 breaths/min × 1.3 mL = 130 mL/min = 0.13 L/min
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5165';

-- D_24: Elevated alkaline phosphatase in BAL indicates type I pneumocyte damage
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5166';

-- D_25: Nominal concentration = 120,000 mg / (10 L/min × 60 min) = 200 mg/L
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5167';

-- D_26: T99 = chamber volume and airflow rate needed (A and C)
-- T99 = (chamber volume / airflow rate) × constant
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5168';

-- D_27: Micronuclei = membrane-bounded structures containing chromosomal fragments/whole chromosomes
-- C&D 9e Ch9 confirms: "membrane-bound micronucleus that resides in the cytoplasm"
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5169';

-- D_28: Mouse Lymphoma assay measures both mutagenic and clastogenic endpoints
-- tk locus detects gene mutations (large colonies) and chromosomal damage (small colonies)
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5170';

-- D_29: Hy's Law = >3× ALT/AST (not ALP) + >2× total bilirubin
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5171';

-- D_30: FSH and LH regulate germ cell development after puberty in both humans and rats
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5172';

-- D_31: Ames test - TA1535/TA100 detect base-pair (A true); TA1537/TA1538/TA98 detect frameshift (C true)
-- B false: PKM101 not in TA98/TA1537; D false: strains have uvrB deletion
UPDATE questions SET correct_answer_letter = 'F' WHERE id = 'DABT-5173';

-- D_32: Initial salicylate poisoning = respiratory alkalosis (stimulates respiratory center)
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5174';

-- D_33: Diuretics cause metabolic alkalosis, not acidosis
-- Renal failure, salicylates, methanol, diarrhea all cause metabolic acidosis
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5175';

-- D_34: Thallium mimics POTASSIUM, not sodium (confirmed in C&D 9e Ch23)
-- "The thallium ion has a similar charge and ion radius as the potassium ion"
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5176';

-- D_35: Cyanide inhibits cytochrome oxidase (cytochrome c oxidase, Complex IV)
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5177';

-- D_36: Lithium toxicity includes tremor, diabetes insipidus, renal failure - NOT liver necrosis
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5178';

-- D_37: Sodium thiosulfate facilitates thiocyanate formation via rhodanese
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5179';

-- D_38: Wernicke's encephalopathy = thiamine (B1) deficiency
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5180';

-- D_39: Anhydroecgonine methyl ester = pyrolytic product from smoking cocaine (crack)
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5181';

-- D_40: Cytochalasin B blocks cytokinesis in micronucleus assay
-- C&D 9e Ch9: "cytokinesis-block technique in which cell division is inhibited with cytochalasin B"
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5182';

-- D_41: Glycolic acid is the toxic metabolite of ethylene glycol causing anion-gap acidosis
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5183';

-- D_42: Rumack-Matthew nomogram is for acetaminophen poisoning
-- Confirmed in C&D 9e Ch33
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5184';

-- D_43: Ionic organic compound movement influenced by lipid solubility AND pH partitioning (B and C)
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5185';

-- D_44: Hydroxyl radical is NOT enzymatically detoxified (too reactive)
-- Catalase detoxifies H2O2; GPx detoxifies H2O2 and lipid peroxides
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5186';

-- D_45: Michaelis-Menten: first order when C < Km (A is correct)
-- At low concentrations relative to Km, elimination follows first-order kinetics
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5187';

-- D_46: Peanut allergy = Type 1 (IgE-mediated immediate) hypersensitivity
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5188';

-- D_47: n-hexane does NOT form radicals via redox cycling
-- Paraquat, doxorubicin, nitrofurantoin undergo redox cycling to form radicals
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5189';

-- D_48: High Vd means extensive tissue distribution, NOT remaining in plasma
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5190';

-- D_49: Lead inhibits ALAD (d-aminolevulinate dehydrogenase) and ferrochelatase
-- Confirmed in C&D 9e Ch23
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5191';

-- D_50: Normal anion/osmo gaps + elevated transaminases + NAC treatment = acetaminophen
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5192';

-- D_51: Rapid resistance over hours = tachyphylaxis
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5193';

-- D_52: Primary target organ of toluene = CNS (neurotoxicant/CNS depressant)
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5194';

-- D_53: Photoallergic reactions = immunologic basis (D) and elicited by smaller doses (B)
-- A = phototoxic; C false (can be systemic too)
UPDATE questions SET correct_answer_letter = 'G' WHERE id = 'DABT-5195';

-- D_54: Type IV allergens - epoxy monomers and mercaptobenzothiazole (B and D)
-- These are known contact sensitizers
UPDATE questions SET correct_answer_letter = 'G' WHERE id = 'DABT-5196';

-- D_55: Minocycline/nicardipine/spironolactone = microsomal induction → dec T3/T4 → inc TSH → thyroid tumors
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5197';

-- D_56: Vitamin A accumulates in hepatic stellate cells (Ito cells)
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5198';

-- D_57: Iron causes ROS via Fenton chemistry; zone I (periportal) has higher oxygen tension
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5199';

-- D_58: Isopropyl alcohol → acetone → induces CYP2E1 → potentiates CCl4 bioactivation
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5200';

-- D_59: DDT delays inactivation of sodium channels (prolonged Na+ influx)
-- Confirmed in C&D 9e Ch22
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5201';

-- D_60: Sodium chlorate inhibits NIS (sodium-iodide symporter)
-- Perchlorate/chlorate/bromate inhibit iodide uptake (C&D 9e Ch20)
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5202';

-- D_61: Sulfamethazine = thyroperoxidase inhibitor, antibacterial in food animals
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5203';

-- D_62: Vitamin B12 deficiency → megaloblastic anemia
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5204';

-- D_63: Phosphorus produces liver injury via lipid peroxidation
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5205';

-- D_64: MPP+ damages dopaminergic neurons in substantia nigra (Parkinson-like)
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5206';

-- D_65: Microsomal induction → inc T4 glucuronidation → dec T4 → inc TSH → follicular hyperplasia/hypertrophy → adenoma
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5207';

-- D_66: At steady-state during inhalation, uptake depends primarily on tissue solubility (blood:air PC)
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5208';

-- D_67: Zero-order elimination: half-life increases with increasing dose
-- First-order has constant half-life regardless of dose
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5209';

-- D_68: 90% of steady-state ≈ 3.3 half-lives. 3.3 × 35 min = 115.5 min ≈ 2.0 hours
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5210';

-- D_69: k = 0.693 / t1/2. Given t1/2 = 2.31 hr? Actually k = 0.693/2.31 = 0.3 hr-1
-- Or if question meant k = 2.31 hr-1, then fractional rate = k = same as given... 
-- Half-life of 2.31 hours gives k = 0.3, answer C
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5211';

-- D_70: Half-life determined by plotting log Cp vs time (first-order kinetics)
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5212';

-- D_71: Fraction remaining = e^(-0.3×1) = 0.741. Eliminated = 1 - 0.741 = 0.259 ≈ 26%
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5213';

-- D_72: Intake rate = CL × Css = 100 mL/min × 0.4 mg/L = 0.04 mg/min
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5214';

-- D_73: Total amount = Cp × Vd = 0.03 mg/L × 6 L = 0.18 mg
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5215';

-- D_74: No consistent relationship between LD50 and chronic toxicity
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5216';

-- D_75: Slope of dose-response = sensitivity of response to dose
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5217';

-- D_76: Probit plot provides reliable estimate of any % response, e.g., dose killing 30%
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5218';

-- D_77: Hazard index combines intrinsic toxicity and intensity of exposure
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5219';

-- D_78: Extrapolation from high to low dose is highly uncertain
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5220';

-- D_79: POD for workers = 100 × (6/8) = 75 mg/m3 (adjusting for exposure duration)
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5221';

-- D_80: Drug A has lowest EC50 (10 nM) = most potent
-- Drug B has highest efficacy (100%)
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5222';

-- D_81: ED50 = quantal population measure; EC50 = graded concentration measure
-- Also ED50 used for TI calculation, EC50 for potency comparison
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5223';

-- D_82: Drug B has smaller TI (2 vs 3) = narrower safety margin, more care needed
UPDATE questions SET correct_answer_letter = 'B' WHERE id = 'DABT-5224';

-- D_83: Tier 3 = high complexity, probabilistic (C correct)
-- Tier 1 = screening, Tier 2 = moderate (A and B swapped/wrong)
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5225';

-- D_84: Probabilistic risk assessment provides distributions, not point estimates
-- Of the options, mode of action is not a probabilistic endpoint
UPDATE questions SET correct_answer_letter = 'F' WHERE id = 'DABT-5226';

-- D_85: Conceptual model includes sources, stressors, pathways/routes, receptors/endpoints (A,B,C,D)
UPDATE questions SET correct_answer_letter = 'G' WHERE id = 'DABT-5227';

-- D_86: MOE = NOAEL / Exposure = 100 / 0.1 = 1000
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5228';

-- D_87: ADI based on animal and human NOAELs
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5229';

-- D_88: Adjustment: 100 × (6/24) × (5/7) = 100 × 0.25 × 0.714 = 17.86 ≈ 18
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5230';

-- D_89: Slope factor = BMR / HED = 0.10 / 100 = 0.001 (mg/kg/day)^-1
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5231';

-- D_90: Risk = 10 × 0.001 = 0.01 = 10^-2 > 10^-6. NOT acceptable.
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5232';

-- D_91: Probability depends on ALL: absorption, potency, concentration, biotransformation
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5233';

-- D_92: All listed effects can indirectly reduce biomass of non-target species
UPDATE questions SET correct_answer_letter = 'E' WHERE id = 'DABT-5234';

-- D_93: AQS protect general population/environment (A and C), not based on 40hr/week (B = TLV)
UPDATE questions SET correct_answer_letter = 'F' WHERE id = 'DABT-5235';

-- D_94: Microcosm experiments best study food web residue dynamics
UPDATE questions SET correct_answer_letter = 'C' WHERE id = 'DABT-5236';

-- D_95: Process change/solvent elimination = best approach (hierarchy of controls)
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5237';

-- D_96: Biggest concern from low-level lead = cognitive delays/behavioral changes in children
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5238';

-- D_97: Small NPs (<50nm) enter by passive diffusion? Actually endocytosis...
-- SWCNTs puncture cells (B correct); small NPs up to 50nm enter by passive diffusion (A debatable)
-- Rigid long NPs frustrate phagocytosis (C = what happens AFTER entry)
-- Best answer: G (A and B) - both are entry mechanisms
UPDATE questions SET correct_answer_letter = 'G' WHERE id = 'DABT-5239';

-- D_98: Only inhalation is acceptable for quantitative risk assessment
-- Instillation/aspiration are bolus doses, not physiologically realistic
UPDATE questions SET correct_answer_letter = 'D' WHERE id = 'DABT-5240';

-- D_99: Section 112(b) of Clean Air Act lists 188 HAPs
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5241';

-- D_100: C = A/Vd = 0.72 mg / 6 L = 0.12 mg/L
UPDATE questions SET correct_answer_letter = 'A' WHERE id = 'DABT-5242';
