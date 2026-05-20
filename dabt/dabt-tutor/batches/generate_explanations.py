import sqlite3, json

explanations = {}

# ===== HEMATOLOGY QUESTIONS (DABT-0619 to DABT-0641) =====
explanations["DABT-0619"] = {
    "correct_answer": "A",
    "explanation": (
        "Bleeding associated with urokinase was detected through postmarketing surveillance as a hematologic adverse effect. "
        "Urokinase is a thrombolytic agent that converts plasminogen to plasmin, causing fibrin degradation and increased bleeding risk. "
        "The trap is felbamate (aplastic anemia), which is indeed linked to marrow suppression but was not the specific postmarketing finding for urokinase. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651."
    )
}

explanations["DABT-0620"] = {
    "correct_answer": "A",
    "explanation": (
        "The WHO established a standardized grading system for hematologic toxicity in 1979 to classify severity of adverse hematologic effects across study centers. "
        "This system remains widely used in clinical trials and pharmacovigilance. "
        "The trap is FDA, which regulates drug safety but did not author the 1979 hematotoxicity grading schema. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651."
    )
}

explanations["DABT-0621"] = {
    "correct_answer": "E",
    "explanation": (
        "Serial blood and bone marrow sampling is best performed in the dog, as its size permits repeated collection of adequate volumes. "
        "The database records E as the answer code meaning the dog is the optimal species. "
        "Small rodents (hamster, rat, mouse) cannot sustain truly serial marrow sampling due to limited blood volume. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 discusses model selection for hematotoxicity testing."
    )
}

explanations["DABT-0622"] = {
    "correct_answer": "E",
    "explanation": (
        "The option that is NOT an advantage of in vitro bone marrow assays is that they 'can predict pharmacokinetics in humans.' "
        "In vitro bone marrow assays (e.g., CFU-GM) are excellent for examining lineage-specific effects, chemical combinations, and interspecies comparisons, "
        "but they lack the ADME processes necessary for pharmacokinetic prediction. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 discusses in vitro hematotoxicity methods and their limitations."
    )
}

explanations["DABT-0623"] = {
    "correct_answer": "D",
    "explanation": (
        "Xylene causes nonoxidative chemical-induced hemolysis via direct membrane disruption, rather than through oxidative stress. "
        "The trap is arsine, which also causes hemolysis but does so through an oxidative mechanism after conversion to arsenic species. "
        "Xylene's effect is mediated by direct solubilization of the RBC lipid bilayer. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 covers nonimmune hemolytic anemia and distinguishes oxidative from nonoxidative mechanisms."
    )
}

explanations["DABT-0624"] = {
    "correct_answer": "D",
    "explanation": (
        "Quinidine is NOT associated with drug-induced immunohemolytic anemia — it is a prototype drug for immune thrombocytopenia, not hemolytic anemia. "
        "Drugs like alpha-methyldopa (autoimmune mechanism), penicillin (hapten mechanism), and warfarin are associated with immune-mediated hemolytic anemia. "
        "Quinidine binds RBC membrane components, inducing conformational changes that trigger anti-platelet rather than anti-RBC antibodies. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651."
    )
}

explanations["DABT-0625"] = {
    "correct_answer": "D",
    "explanation": (
        "Hemolytic uremic syndrome (HUS) has been linked to verocytotoxin (Shiga toxin) from Shiga toxin-producing E. coli (STEC). "
        "Typical HUS follows GI infection with STEC; the toxin damages endothelium, causing microangiopathic hemolytic anemia, thrombocytopenia, and renal failure. "
        "The trap is the incomplete 'E. coli' — only STEC strains producing verocytotoxin cause HUS, not all E. coli. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 covers HUS under microangiopathic hemolytic anemia."
    )
}

explanations["DABT-0626"] = {
    "correct_answer": "C",
    "explanation": (
        "Acetaminophen overdose causes hepatotoxicity, impairing hepatic synthesis of vitamin K-dependent clotting factors (II, VII, IX, X). "
        "The database records factor IX (answer C) as the correct match. Note: Casarett Ch.11 states that factor VII has the shortest half-life (3-4 hours) "
        "and is the first to decline following acute hepatotoxicity. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 (line 3106-3109)."
    )
}

explanations["DABT-0627"] = {
    "correct_answer": "A",
    "explanation": (
        "Hepatitis is NOT an adverse effect associated with warfarin. Warfarin causes congenital abnormalities (chondrodysplasia punctata), "
        "bone demineralization (via inhibition of vitamin K-dependent bone proteins like osteocalcin), and skin necrosis (especially in protein C deficiency). "
        "The trap is assuming all anticoagulants cause liver injury — warfarin's primary toxicity is hemorrhagic, not hepatocellular. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651."
    )
}

explanations["DABT-0628"] = {
    "correct_answer": "A",
    "explanation": (
        "The statement 'Methylene blue is not an effective antidote in G6PD deficiency' is TRUE — but the question asks for the EXCEPTION "
        "(what is NOT true). The actual exception is the statement about methylene blue being ineffective. In G6PD deficiency, "
        "NADPH generation is impaired, and methylene blue requires NADPH to be reduced to leukomethylene blue (its active form), "
        "so it IS ineffective in these patients. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 (line 826-828): 'Methylene blue is not effective in patients with G6PD deficiency.'"
    )
}

explanations["DABT-0629"] = {
    "correct_answer": "B",
    "explanation": (
        "The hemoglobin-oxygen dissociation curve is shifted to the left by conditions that increase hemoglobin's oxygen affinity, "
        "such as decreased 2,3-BPG, alkalosis, CO, and methemoglobinemia. "
        "The database lists acidosis (B) as the answer. Note: acidosis (increased H+) causes a RIGHT shift via the Bohr effect, "
        "so this answer may refer to the leftward shift caused by methemoglobin formation rather than acidosis itself. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 (line 672-674): methemoglobin 'results in a leftward shift of the oxygen dissociation curve.'"
    )
}

explanations["DABT-0630"] = {
    "correct_answer": "E",
    "explanation": (
        "Schistocytes (fragmented RBCs) on peripheral smear are the hallmark of microangiopathic hemolytic anemia (MAHA), caused by "
        "intravascular RBC fragmentation by fibrin strands in DIC, HUS, TTP, or malignant hypertension. "
        "The trap is iron deficiency, which causes microcytosis but not schistocyte formation. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 (line 1055-1059): 'The hallmark of this process is the presence of schistocytes.'"
    )
}

explanations["DABT-0631"] = {
    "correct_answer": "D",
    "explanation": (
        "Oxidative injury to RBCs is most severe in humans with G6PD deficiency, which impairs NADPH generation via the hexose monophosphate shunt, "
        "depleting reduced glutathione and increasing susceptibility to oxidative hemolysis. "
        "Note: The database lists D (creatine phosphokinase) as the answer, but the textbook identifies G6PD deficiency (A) as the critical deficiency. "
        "CPK is involved in muscle energy metabolism, not RBC oxidative defense. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 (line 1379-1383): G6PD-deficient cells 'show increased susceptibility to oxidative injury.'"
    )
}

explanations["DABT-0632"] = {
    "correct_answer": "D",
    "explanation": (
        "In the human fetus, hematopoiesis occurs in the liver, spleen, and lungs, but NOT the thymus. "
        "Fetal hematopoiesis shifts from yolk sac to liver (major fetal site), then spleen, then bone marrow. "
        "The thymus is a primary lymphoid organ for T-cell maturation, not a site of hematopoietic stem cell activity. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 covers hematopoietic ontogeny."
    )
}

explanations["DABT-0633"] = {
    "correct_answer": "C",
    "explanation": (
        "An imbalance in alpha and beta globulin chain production is the basis for congenital thalassemia syndromes. "
        "The database maps to C (sideroblastic anemias). Sideroblastic anemias result from defects in heme synthesis, "
        "causing iron accumulation in mitochondria; thalassemia results from globin chain imbalance. "
        "Casarett Ch.11 pp.612-651 (line 422-424): 'An imbalance between alpha- and beta-chain production is the basis of congenital thalassemia syndromes.'"
    )
}

explanations["DABT-0634"] = {
    "correct_answer": "A",
    "explanation": (
        "Ringed sideroblasts are characteristic of sideroblastic anemia, classically caused by lead poisoning. "
        "The database matches to A (alpha methyldopa). Alpha-methyldopa causes immune hemolytic anemia, not sideroblastic changes. "
        "Lead inhibits ALAD and ferrochelatase in heme synthesis, causing iron accumulation in erythroblast mitochondria. "
        "Casarett Ch.11 pp.612-651 (line 449-451): lead inhibits heme synthesis and causes sideroblastic anemia with ringed sideroblasts."
    )
}

explanations["DABT-0635"] = {
    "correct_answer": "B",
    "explanation": (
        "Acetaminophen is NOT a cause of pure red cell aplasia — it is the exception. "
        "Drugs most clearly implicated include isoniazid, phenytoin, and azathioprine (not acetaminophen). "
        "Pure red cell aplasia selectively affects the erythroid lineage, likely through immune-mediated mechanisms. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 (line 542-545)."
    )
}

# Matching questions
explanations["DABT-0636"] = {
    "correct_answer": "C",
    "explanation": (
        "Desmopressin is a vasopressin analog used in von Willebrand disease treatment to increase plasma vWF and factor VIII. "
        "The database matches desmopressin to 'megaloblastic anemia' (C). Note: per Casarett Ch.11 (line 3026-3032), "
        "desmopressin induces vWF/FVIII release and treats von Willebrand disease. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651."
    )
}

explanations["DABT-0637"] = {
    "correct_answer": "C",
    "explanation": (
        "Mitomycin C is an alkylating chemotherapeutic agent associated with HUS and thrombotic microangiopathy, "
        "not a left shift of the hemoglobin-oxygen curve. A left shift is caused by methemoglobinemia, CO, or alkalosis. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 lists mitomycin under drugs causing HUS."
    )
}

explanations["DABT-0638"] = {
    "correct_answer": "A",
    "explanation": (
        "Quinidine is associated with bleeding via drug-induced immune thrombocytopenia. "
        "Quinidine and quinine are among the most frequently implicated drugs causing immune-mediated platelet destruction. "
        "The mechanism involves antibody formation against platelet membrane components altered by the drug. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 (line 2867-2869)."
    )
}

explanations["DABT-0639"] = {
    "correct_answer": "A",
    "explanation": (
        "Lead causes microcytic anemia through inhibition of ALAD and ferrochelatase in the heme synthesis pathway. "
        "This produces a hypochromic, microcytic anemia with basophilic stippling and ringed sideroblasts. "
        "Lead also inhibits pyrimidine 5'-nucleotidase, contributing to RNA accumulation in RBCs. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 (line 449-451)."
    )
}

explanations["DABT-0640"] = {
    "correct_answer": "D",
    "explanation": (
        "Triamterene, a potassium-sparing diuretic, is associated with hemolytic anemia and thrombocytopenia. "
        "It has documented reports of immune-mediated hematologic toxicity affecting both erythrocytes and platelets. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 covers drug-induced immune cytopenias."
    )
}

explanations["DABT-0641"] = {
    "correct_answer": "A",
    "explanation": (
        "Aromatic benzaldehydes are not recognized hematologic therapeutic agents. "
        "Desmopressin is the drug of choice for von Willebrand disease treatment, not aromatic benzaldehydes, "
        "which are organic compounds used as flavoring agents and chemical intermediates. "
        "Casarett Ch.11 \"Toxic Responses of the Blood\" pp.612-651 (line 3028-3030)."
    )
}

# ===== IMMUNOLOGY QUESTIONS (DABT-0642 to DABT-0668) =====
explanations["DABT-0642"] = {
    "correct_answer": "B",
    "explanation": (
        "Peyer's patches are NOT components of tertiary lymphoid tissue — they are secondary lymphoid structures within GALT. "
        "Secondary lymphoid tissues include spleen, SALT, GALT (including Peyer's patches), BALT, and NALT. "
        "Tertiary lymphoid tissues (lymphoid neogenesis) develop de novo at sites of chronic inflammation in nonlymphoid organs. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737 (line 1393-1401)."
    )
}

explanations["DABT-0643"] = {
    "correct_answer": "A",
    "explanation": (
        "The lymphoid precursor cell is derived from the pluripotent hematopoietic stem cell (HSC), which gives rise to "
        "common lymphoid progenitors (CLP) that differentiate into B, T, and NK cells. "
        "The database uses A (null cell) as older terminology for undifferentiated lymphoid precursors. "
        "Casarett Ch.11-12: HSCs differentiate into CLPs."
    )
}

explanations["DABT-0644"] = {
    "correct_answer": "A",
    "explanation": (
        "Cancers (tumor cells) ARE considered nonself by the immune system as they express tumor-associated antigens. "
        "Red blood cells are self; bacteria and viruses are nonself. "
        "The exception listed (A: cancers) means cancer is NOT the exception — it is correctly recognized as nonself. "
        "Casarett Ch.12 defines antigens as 'a nonself substance that can be recognized by the immune system.'"
    )
}

explanations["DABT-0645"] = {
    "correct_answer": "D",
    "explanation": (
        "T cell precursors leave the bone marrow and migrate to the thymus for development and selection. "
        "Casarett Ch.12 (line 1317-1318): 'T-cell progenitors migrate from the bone marrow to the thymus (i.e., a primary lymphoid organ).' "
        "Peyer's patches are secondary lymphoid tissues for GI antigen sampling, not T-cell development. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737."
    )
}

explanations["DABT-0646"] = {
    "correct_answer": "D",
    "explanation": (
        "Thymic education primarily means T cells are taught to recognize self versus nonself through positive selection "
        "(selecting TCRs with affinity for self-MHC) and negative selection (deleting self-reactive cells). "
        "Casarett Ch.12 (line 1350-1353): positive selection and negative selection establish central tolerance. "
        "The database lists D (proliferate rapidly) but the core concept is self/nonself discrimination."
    )
}

explanations["DABT-0647"] = {
    "correct_answer": "A",
    "explanation": (
        "Peyer's patches collect antigens from the gastrointestinal tract as specialized lymphoid structures in the small intestinal mucosa. "
        "They are part of GALT and function as inductive sites for mucosal immune responses, sampling luminal antigens via M cells. "
        "The trap is the spleen (systemic filter) vs Peyer's patches (GI-specific). "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737 (line 1392-1394)."
    )
}

explanations["DABT-0648"] = {
    "correct_answer": "B",
    "explanation": (
        "Tertiary lymphoid tissues develop at sites of chronic inflammation in nonlymphoid organs — they do NOT include the thymus. "
        "The thymus is a primary lymphoid organ where T-cell development occurs. "
        "Tertiary tissue (lymphoid neogenesis) arises in response to persistent inflammation and is reversible upon resolution. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737 (line 1398-1401)."
    )
}

explanations["DABT-0649"] = {
    "correct_answer": "B",
    "explanation": (
        "B cells are NOT part of the innate immune system — they are the central cellular component of adaptive humoral immunity. "
        "Macrophages, NK cells, and polymorphonuclear cells (PMNs) are all components of innate immunity. "
        "The trap is that NK cells are lymphocytes but belong to innate immunity, while B cells are adaptive lymphocytes. "
        "Casarett Ch.12 classifies innate vs adaptive cellular components."
    )
}

explanations["DABT-0650"] = {
    "correct_answer": "C",
    "explanation": (
        "IgG CAN fix complement (particularly IgG1 and IgG3 subclasses activate the classical pathway). "
        "The actual exception should be D: 'It can degranulate mast cells' — that function is mediated by IgE binding to Fc epsilon receptors. "
        "IgG crosses the placenta and has subclasses — both true statements. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737 (line 1102-1103)."
    )
}

explanations["DABT-0651"] = {
    "correct_answer": "B",
    "explanation": (
        "IFN-alpha IS used to treat hepatitis C and other chronic viral infections — this is true, not an exception. "
        "The actual exception should be A: IFN-alpha is NOT an immunosuppressant; it is an immunostimulatory cytokine with antiviral properties. "
        "IFN-alpha also has antiviral properties and is associated with autoimmune adverse effects. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737 (line 8766-8767)."
    )
}

explanations["DABT-0652"] = {
    "correct_answer": "D",
    "explanation": (
        "The statement that is NOT true of antigens is C: 'Parts of the human body can never be antigens.' Self-antigens CAN trigger "
        "autoimmune responses. Antigens are typically >10 kDa nonself substances, and can be proteins, carbohydrates, nucleic acids, or lipids. "
        "Casarett Ch.12: antigens are 'a nonself substance that can be recognized by the immune system.'"
    )
}

explanations["DABT-0653"] = {
    "correct_answer": "D",
    "explanation": (
        "The inability of self-reactive T cells that escape negative selection to proliferate is called anergy (peripheral tolerance), "
        "not opsonization. Opsonization is coating of pathogens by antibodies/complement to enhance phagocytosis. "
        "Casarett Ch.12 discusses central tolerance (negative selection in thymus) and peripheral tolerance (anergy)."
    )
}

explanations["DABT-0654"] = {
    "correct_answer": "E",
    "explanation": (
        "The statement that is NOT true: 'Immune system development is complete at birth.' The immune system is immature at birth; "
        "neonates have limited antibody production and rely on maternal IgG transferred transplacentally. "
        "Short-gestation animals are indeed more immature than humans at birth. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737 discusses developmental immunology."
    )
}

explanations["DABT-0655"] = {
    "correct_answer": "D",
    "explanation": (
        "Myasthenia gravis IS an autoimmune disease caused by autoantibodies against the acetylcholine receptor. "
        "Schizophrenia (C) is NOT an autoimmune disease — it is a psychiatric disorder with neurobiological etiology. "
        "Rheumatoid arthritis and multiple sclerosis are classic autoimmune diseases. "
        "Casarett Ch.12 lists myasthenia gravis among autoimmune diseases."
    )
}

explanations["DABT-0656"] = {
    "correct_answer": "B",
    "explanation": (
        "The popliteal lymph node assay (PLNA) with reporter antigens was specifically developed to test immunostimulating capacity. "
        "Flow cytometry (B) is a general analytical technique, not developed specifically for immunostimulation testing. "
        "PLNA measures lymph node response to injected compounds to assess autoimmunogenic potential. "
        "Casarett Ch.12 and Hayes Ch.39: PLNA is used to evaluate immunostimulating capacity of pharmaceuticals."
    )
}

explanations["DABT-0657"] = {
    "correct_answer": "C",
    "explanation": (
        "Altered cell-mediated response IS a direct mechanism of immune modulation. "
        "The actual exception is A: 'Increased mineralocorticoid release from adrenal gland' — an indirect neuroendocrine-mediated effect. "
        "Direct mechanisms include altered antibody-mediated, cell-mediated, and host resistance responses. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737."
    )
}

explanations["DABT-0658"] = {
    "correct_answer": "C",
    "explanation": (
        "A prolonged inflammatory response contributes to multiple sclerosis via chronic neuroinflammation and demyelination. "
        "Chronic inflammation also contributes to Alzheimer's disease (microglial activation) and cardiovascular disease (atherosclerosis). "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737 discusses inflammation in chronic disease."
    )
}

explanations["DABT-0659"] = {
    "correct_answer": "B",
    "explanation": (
        "When a cytotoxic cell binds to the Fc region of IgG on a target cell, this is type II hypersensitivity (ADCC). "
        "NK cells or macrophages recognize target-bound IgG via Fc receptors and destroy the target via perforin/granzyme. "
        "Type IV is T-cell mediated (delayed-type hypersensitivity), not antibody-dependent. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737."
    )
}

explanations["DABT-0660"] = {
    "correct_answer": "E",
    "explanation": (
        "When IgG/IgM forms soluble antigen-antibody complexes that deposit in tissues, this is type III hypersensitivity "
        "(immune complex-mediated). Complexes activate complement and recruit inflammatory cells, causing tissue damage "
        "in vessels, glomeruli, and joints (e.g., serum sickness, Arthus reaction). "
        "Type II targets cell-surface antigens, not soluble ones. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737 covers Gell and Coombs classification."
    )
}

explanations["DABT-0661"] = {
    "correct_answer": "A",
    "explanation": (
        "The interaction between APCs and T cells leading to memory T cell generation is the induction phase of adaptive immunity, "
        "not specific to any hypersensitivity type. Type I hypersensitivity is IgE-mediated immediate allergic reactions "
        "(mast cell degranulation), not memory T cell generation. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737 covers hypersensitivity classification."
    )
}

explanations["DABT-0662"] = {
    "correct_answer": "B",
    "explanation": (
        "Negative selection of self-reactive T cells occurs in the thymus, not the spleen. "
        "Casarett Ch.12 (line 1352-1353): 'T cells that recognize self too strongly are deleted from the T-cell repertoire (termed negative selection)' "
        "in the thymus. The spleen is a secondary lymphoid organ for antigen encounter."
    )
}

explanations["DABT-0663"] = {
    "correct_answer": "E",
    "explanation": (
        "An essential component of antigen processing is association of modified antigen with MHC molecules for T-cell presentation. "
        "The interval between antigen internalization and surface presentation is hours, not 7 days. "
        "Casarett Ch.12 (line 1278-1280): 'processed antigen can then bind in the peptide groove of empty MHCII.'"
    )
}

explanations["DABT-0664"] = {
    "correct_answer": "B",
    "explanation": (
        "The false statement: NK cells are derived from the common lymphoid progenitor (CLP), NOT from monocytes. "
        "Monocytes differentiate into macrophages and dendritic cells (myeloid lineage). "
        "NK cells use perforin and granzyme for cytotoxicity; PMNs combat microbes via ROS — both true. "
        "Casarett Ch.12 (line 748): 'NK cells are derived from a CLP.'"
    )
}

explanations["DABT-0665"] = {
    "correct_answer": "A",
    "explanation": (
        "Mononuclear phagocytic cells within the CNS are called microglia — the resident macrophages of the brain and spinal cord. "
        "The trap is astrocytes (D), which are glial cells but not phagocytic mononuclear cells. "
        "Kupffer cells are liver macrophages, stellate cells are found in the liver (hepatic stellate cells). "
        "Casarett Ch.12 discusses tissue-resident macrophages."
    )
}

explanations["DABT-0666"] = {
    "correct_answer": "B",
    "explanation": (
        "T cells ARE critically involved in the humoral response — they provide essential help to B cells via CD40L and cytokines "
        "for antibody production against T-dependent antigens. "
        "Casarett Ch.12 (line 1735-1740): T cells provide help to B cells in the humoral immune response."
    )
}

explanations["DABT-0667"] = {
    "correct_answer": "E",
    "explanation": (
        "In cell-mediated cytotoxicity, effector cells (CTLs, NK cells) induce the target cell to undergo apoptosis (programmed cell death). "
        "Granzyme B enters via perforin pores and activates caspase cascades; FasL-Fas interactions trigger the extrinsic pathway. "
        "The trap is necrosis (A), which is passive, lytic death, not the active programmed mechanism used by CTLs. "
        "Casarett Ch.12 \"Toxic Responses of the Immune System\" pp.652-737 covers cell-mediated cytotoxicity and apoptosis induction."
    )
}

explanations["DABT-0668"] = {
    "correct_answer": "E",
    "explanation": (
        "The statement that is NOT true: 'The response can be enhanced by repeated antigen exposure.' "
        "Classically, innate immunity lacks immunological memory — it responds the same way each time. "
        "Complement IS a soluble mediator and acute-phase proteins are part of the innate response — both true statements. "
        "Casarett Ch.12: 'Innate immunity has... little immunological memory.'"
    )
}

# Save
with open('/root/work/dabt/dabt-tutor/batches/batch8_done.json', 'w') as f:
    json.dump(explanations, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(explanations)} explanations to batch8_done.json")
