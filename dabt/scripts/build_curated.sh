#!/bin/bash
set -euo pipefail

SRC="/root/dabt-materials"
DST="/root/dabt-curated"

echo "=== Creating destination directory structure ==="
mkdir -p "$DST"
mkdir -p "$DST/Textbooks"
mkdir -p "$DST/Practice_Exams/Mini-ABT_1-11"
mkdir -p "$DST/Practice_Exams/Kristen_Mini_Exams"
mkdir -p "$DST/Practice_Exams/Past_ABT_Exams"
mkdir -p "$DST/Practice_Tests_by_Topic/Kristen_Topic_Tests"
mkdir -p "$DST/Chapter_Tests/Tests"
mkdir -p "$DST/Chapter_Tests/Tests_with_Answers"
mkdir -p "$DST/2000Q_Question_Bank"
mkdir -p "$DST/ACT_Course_2018/Lectures"
mkdir -p "$DST/ACT_Course_2018/Audio"
mkdir -p "$DST/Mid-Amer_Tox_Course/Topic_Summaries"
mkdir -p "$DST/Mid-Amer_Tox_Course/Regulatory_Guidelines/ICH"
mkdir -p "$DST/Mid-Amer_Tox_Course/Regulatory_Guidelines/OECD"
mkdir -p "$DST/Mid-Amer_Tox_Course/Regulatory_Guidelines/EPA"
mkdir -p "$DST/Mid-Amer_Tox_Course/Regulatory_Guidelines/FDA"
mkdir -p "$DST/C_and_D_Chapter_Support"
mkdir -p "$DST/Study_Aids"

echo "=== Copying Textbook ==="
cp "$SRC/2021 ABT Prep/Casarett _ Doull_s 7th Edition Full Text.pdf" \
   "$DST/Textbooks/Casarett_and_Doull_7th_Ed_Full.pdf"

echo "=== Copying Mini-ABT Exams 1-11 (with answer keys) ==="
cp "$SRC/2021 ABT Prep/Mini-ABT Practice Exams/"*.docx \
   "$DST/Practice_Exams/Mini-ABT_1-11/"

echo "=== Copying Kristen Mini Exams (18 dated exams + 14 answer keys) ==="
cp "$SRC/Kristen Materials/mini exams/"*.docx \
   "$DST/Practice_Exams/Kristen_Mini_Exams/"

echo "=== Copying Kristen Topic Tests (14 topics) ==="
cp "$SRC/Kristen Materials/practice test by topic/"* \
   "$DST/Practice_Tests_by_Topic/Kristen_Topic_Tests/"

echo "=== Copying Past ABT Exams ==="
# 2012 complete board questions (from Shipkowski - unique copy)
cp "$SRC/Shipkowski Materials/DABT Study Material/Mini-ABT Exams/ABT Exam prep/Questions/2012-complete-board-questions.pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2012_complete_board_questions.pdf"

# 2013 Recert
cp "$SRC/2021 ABT Prep/Past ABT Exams/2013 - Recert Examination.pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2013_Recert_Examination.pdf"

# 2015 Recert
cp "$SRC/2021 ABT Prep/Past ABT Exams/2015 - Recert Examination.pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2015_Recert_Examination.pdf"

# 2017 Certification Parts A-D
cp "$SRC/2021 ABT Prep/Past ABT Exams/2017 ABT CERTIFICATION EXAMINATION - Part A.pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2017_Certification_Part_A.pdf"
cp "$SRC/2021 ABT Prep/Past ABT Exams/2017 ABT CERTIFICATION EXAMINATION - Part B.pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2017_Certification_Part_B.pdf"
cp "$SRC/2021 ABT Prep/Past ABT Exams/2017 ABT CERTIFICATION EXAMINATION - Part C.pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2017_Certification_Part_C.pdf"
cp "$SRC/2021 ABT Prep/Past ABT Exams/2017 ABT CERTIFICATION EXAMINATION - Part D.pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2017_Certification_Part_D.pdf"

# 2017 Certification Parts 1 & 2 (from Kristen - alternate splits)
cp "$SRC/Kristen Materials/other materials/2017 ABT CERTIFICATION EXAMINATION - Part 1 of 2.pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2017_Certification_Part_1_of_2.pdf"
cp "$SRC/Kristen Materials/other materials/2017 ABT CERTIFICATION EXAMINATION - Part 2 of 2.pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2017_Certification_Part_2_of_2.pdf"

# Also get the (day 2) variants
cp "$SRC/Kristen Materials/other materials/2017 ABT CERTIFICATION EXAMINATION - Part 1 of 2 (day 2).pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2017_Certification_Part_1_of_2_day2.pdf"
cp "$SRC/Kristen Materials/other materials/2017 ABT CERTIFICATION EXAMINATION - Part 2 of 2 (day 2).pdf" \
   "$DST/Practice_Exams/Past_ABT_Exams/2017_Certification_Part_2_of_2_day2.pdf"

# Compiled recert exams
cp "$SRC/2021 ABT Prep/Past ABT Exams/2008-2014 Compiled Recert Exams_Ramesh Kovi 2017.xlsx" \
   "$DST/Practice_Exams/Past_ABT_Exams/2008-2014_Compiled_Recert_Exams.xlsx"

# Recert exam discussion slides (valuable for answer walkthroughs)
mkdir -p "$DST/Practice_Exams/Past_ABT_Exams/Recert_Discussion_Slides"
cp -r "$SRC/2021 ABT Prep/Past ABT Exams/2013 and 2015 recert exams - with answers/"* \
   "$DST/Practice_Exams/Past_ABT_Exams/Recert_Discussion_Slides/" 2>/dev/null || true

echo "=== Copying Chapter Tests ==="
cp "$SRC/2021 ABT Prep/Chapter Tests/Tests/"*.docx \
   "$DST/Chapter_Tests/Tests/"
cp "$SRC/2021 ABT Prep/Chapter Tests/Tests with Answers/"*.docx \
   "$DST/Chapter_Tests/Tests_with_Answers/"

echo "=== Copying 2000Q Question Bank ==="
cp "$SRC/2021 ABT Prep/Tox 2000/2000Q/"*.docx \
   "$DST/2000Q_Question_Bank/"
cp "$SRC/2021 ABT Prep/Tox 2000/Tox 2000 Answers.pdf" \
   "$DST/2000Q_Question_Bank/"
cp "$SRC/2021 ABT Prep/Tox 2000/Tox 2000 NoteCards.pdf" \
   "$DST/2000Q_Question_Bank/"

echo "=== Copying ACT Course 2018 Lectures ==="
# Copy all PDFs excluding audio directory
find "$SRC/ACT Course 2018" -maxdepth 1 -name "*.pdf" -exec cp {} "$DST/ACT_Course_2018/Lectures/" \;

# Also copy the (1) variant in the ACT course (it has a clean copy too - 11_Dev_Repro_A_Hoberman.pdf without (1) doesn't exist)
# Actually let's check - the ACT course has 11_Dev_Repro_A_Hoberman (1).pdf but NOT 11_Dev_Repro_A_Hoberman.pdf without (1)
# So we should keep the (1) version here since it's the only copy
if [ -f "$SRC/ACT Course 2018/11_Dev_Repro_A_Hoberman (1).pdf" ]; then
    cp "$SRC/ACT Course 2018/11_Dev_Repro_A_Hoberman (1).pdf" \
       "$DST/ACT_Course_2018/Lectures/11_Dev_Repro_A_Hoberman.pdf"
fi

echo "=== Copying ACT Course 2018 Audio ==="
cp "$SRC/ACT Course 2018/ACT2018 audio/"*.wav \
   "$DST/ACT_Course_2018/Audio/"

echo "=== Copying Mid-Amer Tox Course Topic Summaries ==="
# All PDFs in root of Mid-Amer Tox Course (excluding DABT Regulations/)
find "$SRC/Mid-Amer Tox Course" -maxdepth 1 -name "*.pdf" -exec cp {} "$DST/Mid-Amer_Tox_Course/Topic_Summaries/" \;

echo "=== Copying Mid-Amer Tox Course Regulatory Guidelines ==="
# ICH guidelines
find "$SRC/Mid-Amer Tox Course/DABT Regulations/ICH" -name "*.pdf" -exec cp {} "$DST/Mid-Amer_Tox_Course/Regulatory_Guidelines/ICH/" \;

# OECD guidelines
find "$SRC/Mid-Amer Tox Course/DABT Regulations/OECD" -name "*.pdf" -exec cp {} "$DST/Mid-Amer_Tox_Course/Regulatory_Guidelines/OECD/" \;

# EPA
cp "$SRC/Mid-Amer Tox Course/DABT Regulations/EPA_cancer_guidelines_2005.pdf" \
   "$DST/Mid-Amer_Tox_Course/Regulatory_Guidelines/EPA/"

# FDA
cp "$SRC/Mid-Amer Tox Course/DABT Regulations/FDA Least Burdensome Provisions.pdf" \
   "$DST/Mid-Amer_Tox_Course/Regulatory_Guidelines/FDA/"
cp "$SRC/Mid-Amer Tox Course/DABT Regulations/FDA Safety Testing of Drug Metabolites.pdf" \
   "$DST/Mid-Amer_Tox_Course/Regulatory_Guidelines/FDA/"

# Silverbook
cp "$SRC/Mid-Amer Tox Course/DABT Regulations/Silverbook.pdf" \
   "$DST/Mid-Amer_Tox_Course/Regulatory_Guidelines/"

echo "=== Copying C&D Chapter Supporting Materials ==="
# Copy the entire C&D Chapter Supporting Materials directory preserving structure
cp -r "$SRC/2021 ABT Prep/C&D Chapter Supporting Materials"/* \
   "$DST/C_and_D_Chapter_Support/"

echo "=== Copying Study Aids ==="
cp "$SRC/2021 ABT Prep/ABT chemical list.xlsx" \
   "$DST/Study_Aids/ABT_chemical_list.xlsx"
cp "$SRC/2021 ABT Prep/ABT review of notes_26Sep.docx" \
   "$DST/Study_Aids/ABT_review_of_notes.docx"
cp "$SRC/2021 ABT Prep/ICH.docx" \
   "$DST/Study_Aids/ICH_notes.docx"
cp "$SRC/2021 ABT Prep/Tox Review.docx" \
   "$DST/Study_Aids/Tox_Review.docx"

# Copy Certification Manual if present
if [ -f "$SRC/2021 ABT Prep/Certification Manual 2018.pdf" ]; then
    cp "$SRC/2021 ABT Prep/Certification Manual 2018.pdf" \
       "$DST/Study_Aids/Certification_Manual_2018.pdf"
fi

# Also copy Kristen's Tox 2000 supplemental files
cp "$SRC/Kristen Materials/other materials/Tox 2000 Answers.pdf" \
   "$DST/Study_Aids/" 2>/dev/null || true
cp "$SRC/Kristen Materials/other materials/Tox 2000 NoteCards.pdf" \
   "$DST/Study_Aids/" 2>/dev/null || true

echo "=== Copying additional study notes from 2021 ABT Prep ==="
# Copy any remaining useful files at root of 2021 ABT Prep
for f in "$SRC/2021 ABT Prep/"*.docx; do
    bn=$(basename "$f")
    # Skip files already copied
    case "$bn" in
        ABT\ review\ of\ notes_26Sep.docx|ICH.docx|Tox\ Review.docx) ;;
        ABT\ chemical\ list.xlsx) ;;
        *)
            cp "$f" "$DST/Study_Aids/" 2>/dev/null || true
            ;;
    esac
done

echo ""
echo "=== COPY COMPLETE ==="
echo "Counting files in curated directory..."
find "$DST" -type f | wc -l
echo "Total size:"
du -sh "$DST" | cut -f1
