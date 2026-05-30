-- FIX 25 WRONG ANSWER KEYS IN dabt.db
-- Database: /root/work/dabt/dabt-tutor/reference/data/dabt.db
-- Each section: UPDATE + VERIFY
-- Corrections verified against Casarett & Doull Ch.6 (Biotransformation)

-- DABT-1820: acetaldehyde→acetic acid by ALDH2 in mitochondria (not cytosol)
UPDATE questions SET correct_answer_letter='A', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1820' AND option_letter='A') WHERE id='DABT-1820';

-- DABT-1821: aldehyde oxidase/xanthine oxidoreductase contain molybdenum (not copper)
UPDATE questions SET correct_answer_letter='B', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1821' AND option_letter='B') WHERE id='DABT-1821';

-- DABT-1823: Parkinson's elevated MAO-B in substantia nigra (not COMT)
UPDATE questions SET correct_answer_letter='D', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1823' AND option_letter='D') WHERE id='DABT-1823';

-- DABT-1824: MPO exception — induced by cyanide is FALSE
UPDATE questions SET correct_answer_letter='B', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1824' AND option_letter='B') WHERE id='DABT-1824';

-- DABT-1825: PHS exception — toxicity in high-CYP450 tissues is FALSE
UPDATE questions SET correct_answer_letter='D', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1825' AND option_letter='D') WHERE id='DABT-1825';

-- DABT-1826: FMO reactions most similar to CYP450 (not xanthine oxidase)
UPDATE questions SET correct_answer_letter='B', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1826' AND option_letter='B') WHERE id='DABT-1826';

-- DABT-1827: CYP450 highest in liver endoplasmic reticulum (not cytosol)
UPDATE questions SET correct_answer_letter='A', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1827' AND option_letter='A') WHERE id='DABT-1827';

-- DABT-1828: CYP450 exception — binds CO₂ is FALSE (binds CO, not CO₂)
UPDATE questions SET correct_answer_letter='C', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1828' AND option_letter='C') WHERE id='DABT-1828';

-- DABT-1829: Epoxidation exception — chloroform (undergoes oxidative dechlorination)
UPDATE questions SET correct_answer_letter='D', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1829' AND option_letter='D') WHERE id='DABT-1829';

-- DABT-1831: Toxic metabolite exception — ethanol→acetic acid is DETOXIFICATION
UPDATE questions SET correct_answer_letter='B', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1831' AND option_letter='B') WHERE id='DABT-1831';

-- DABT-1832: CYP450 can catalyze dehydrogenation (not peptide cleavage)
UPDATE questions SET correct_answer_letter='D', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1832' AND option_letter='D') WHERE id='DABT-1832';

-- DABT-1833: GST toxification exception — aflatoxin B1 epoxide (GSH conjugation is detoxification)
UPDATE questions SET correct_answer_letter='C', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1833' AND option_letter='C') WHERE id='DABT-1833';

-- DABT-1834: GST present in cytosol + microsomes + mitochondria (all of above)
UPDATE questions SET correct_answer_letter='D', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1834' AND option_letter='D') WHERE id='DABT-1834';

-- DABT-1836: Rhodanese detoxifies H₂S (not N₂O)
UPDATE questions SET correct_answer_letter='B', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1836' AND option_letter='B') WHERE id='DABT-1836';

-- DABT-1837: TST polymorphisms: ulcerative colitis + ALS (not dementia + MS)
UPDATE questions SET correct_answer_letter='D', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1837' AND option_letter='D') WHERE id='DABT-1837';

-- DABT-1838: Amino acid conjugation exception — Acetyl CoA (uses CoA-SH, not acetyl-CoA)
UPDATE questions SET correct_answer_letter='D', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1838' AND option_letter='D') WHERE id='DABT-1838';

-- DABT-1839: GST exception — stereoselective implies enzymatic (not non-enzymatic)
UPDATE questions SET correct_answer_letter='A', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1839' AND option_letter='A') WHERE id='DABT-1839';

-- DABT-1840: GSH displacement substrate — all of the above
UPDATE questions SET correct_answer_letter='D', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1840' AND option_letter='D') WHERE id='DABT-1840';

-- DABT-1841: GSH addition substrate — β-propiolactone (not hexane)
UPDATE questions SET correct_answer_letter='C', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1841' AND option_letter='C') WHERE id='DABT-1841';

-- DABT-1842: GSH conjugate in urine — mercapturic acid (not glutaric acids)
UPDATE questions SET correct_answer_letter='A', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1842' AND option_letter='A') WHERE id='DABT-1842';

-- DABT-1843: Methylation exception — acetone (not nicotine)
UPDATE questions SET correct_answer_letter='A', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1843' AND option_letter='A') WHERE id='DABT-1843';

-- DABT-1844: Transesterification — cocaine→ethylcocaine (not histamine N-methylation)
UPDATE questions SET correct_answer_letter='C', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1844' AND option_letter='C') WHERE id='DABT-1844';

-- DABT-1845: Acetylation exception — increases solubility is FALSE (decreases it)
UPDATE questions SET correct_answer_letter='A', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1845' AND option_letter='A') WHERE id='DABT-1845';

-- DABT-1848: Sulfonation — high-affinity, low-capacity pathway (not low-affinity, low-capacity)
UPDATE questions SET correct_answer_letter='D', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1848' AND option_letter='D') WHERE id='DABT-1848';

-- DABT-1850: Sulfonation exception — always detoxify is FALSE (can bioactivate)
UPDATE questions SET correct_answer_letter='B', correct_answer_text=(SELECT option_text FROM answer_options WHERE question_id='DABT-1850' AND option_letter='B') WHERE id='DABT-1850';

-- Verification query
SELECT '=== VERIFICATION ===' AS '';
SELECT id, correct_answer_letter, substr(correct_answer_text,1,60) AS ans_text FROM questions
WHERE id IN ('DABT-1820','DABT-1821','DABT-1823','DABT-1824','DABT-1825','DABT-1826','DABT-1827','DABT-1828','DABT-1829','DABT-1831','DABT-1832','DABT-1833','DABT-1834','DABT-1836','DABT-1837','DABT-1838','DABT-1839','DABT-1840','DABT-1841','DABT-1842','DABT-1843','DABT-1844','DABT-1845','DABT-1848','DABT-1850')
ORDER BY id;

SELECT '=== 25 corrections applied ===' AS '';
