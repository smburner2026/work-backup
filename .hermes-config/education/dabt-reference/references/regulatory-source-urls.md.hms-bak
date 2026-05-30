# Regulatory Source URLs for DABT Reference Library

Collection of authoritative URLs for downloading/extracting regulatory documents.
Sourced from successful batch-download session (May 2026, 11 documents).
These URLs are stable government/international sources, not ephemeral mirrors.

## EPA Statutory (epa.gov)

### TSCA
- Summary: `https://www.epa.gov/laws-regulations/summary-toxic-substances-control-act`
- Learn About: `https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/learn-about-toxic-substances-control-act-tsca`
- Section 4 Testing: `https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/industry-testing-requirements-under-tsca-section-4`
- Section 5 PMN: `https://www.epa.gov/reviewing-new-chemicals-under-toxic-substances-control-act-tsca/actions-under-tsca-section-5`
- Section 6 Risk Management: `https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/regulation-chemicals-under-section-6a-toxic-substances`
- Lautenberg 2016: `https://www.epa.gov/assessing-and-managing-chemicals-under-tsca/frank-r-lautenberg-chemical-safety-21st-century-act`

### FIFRA
- Summary: `https://www.epa.gov/laws-regulations/summary-federal-insecticide-fungicide-and-rodenticide-act`
- Registration: `https://www.epa.gov/pesticide-registration/about-pesticide-registration`
- Registration Review: `https://www.epa.gov/pesticide-reevaluation/why-we-review-pesticides`
- Enforcement: `https://www.epa.gov/enforcement/federal-insecticide-fungicide-and-rodenticide-act-fifra-and-federal-facilities`

### FQPA
- Summary: `https://www.epa.gov/laws-regulations/summary-food-quality-protection-act`
- Tolerances: `https://www.epa.gov/pesticide-tolerances`
- Risk Assessment: `https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks`

### IRIS
- Basic Info: `https://www.epa.gov/iris/basic-information-about-integrated-risk-information-system`
- IRIS Home: `https://www.epa.gov/iris`
- ORD Staff Handbook (PDF): `https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P10113JW.TXT`
- Report to Congress (PDF): `https://www.epa.gov/sites/default/files/2015-12/documents/iris_report_to_congress_nov2015.pdf`

### SDWA
- How EPA Regulates: `https://www.epa.gov/sdwa/how-epa-regulates-drinking-water-contaminants`
- Summary: `https://www.epa.gov/laws-regulations/summary-safe-drinking-water-act`
- Source Book: `https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=901F0A00.TXT`

## OSHA (osha.gov / eCFR)

### Hazard Communication (29 CFR 1910.1200)
- **Primary (works):** `https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XVII/part-1910/subpart-Z/section-1910.1200`
  - Use `/current/` path (NOT `/api/versioner/` which returns 404)
- Cornell LII mirror: `https://www.law.cornell.edu/cfr/text/29/1910.1200`
- OSHA page: `https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1200`

### Subpart Z — Air Contaminants (PELs)
- 1910.1000 text: `https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1000`
- Annotated Tables: `https://www.osha.gov/annotated-pels`
- Annotated Z-3: `https://www.osha.gov/annotated-pels/table-z-3`
- PEL update history: `https://www.osha.gov/laws-regs/federalregister/2014-10-10`

## EU REACH (echa.europa.eu)
- Legislation: `https://echa.europa.eu/regulations/reach/legislation`
- Understanding REACH: `https://echa.europa.eu/regulations/reach/understanding-reach`
- EUR-Lex consolidated: `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02006R1907-20221205`

## UN GHS (unece.org / PubChem)
- **UNECE GHS Rev 7 (sometimes unreachable):** `https://unece.org/ghs-rev7-2017`
- **Fallback (more reliable):** `https://pubchem.ncbi.nlm.nih.gov/ghs` — excellent structured GHS classification summary with H-codes, P-codes, LD50 ranges
- Individual part PDFs: follow links from UNECE GHS page

## NTP Report on Carcinogens (ntp.niehs.nih.gov)
- Completed Evaluations: `https://ntp.niehs.nih.gov/research/assessments/cancer/completed/roc`
- Introduction (15th Ed PDF): `https://ntp.niehs.nih.gov/sites/default/files/ntp/roc/content/introduction_508.pdf`
- Process (15th Ed PDF): `https://ntp.niehs.nih.gov/sites/default/files/ntp/roc/content/process_508.pdf`
- RoC Home: `https://ntp.niehs.nih.gov/go/roc`
- Listing Criteria: `https://ntp.niehs.nih.gov/go/15209`

## NRC Red Book (nap.edu)
- Full text was already present in the library at 504 KB. Original source is nap.edu.

## Batch Download Strategy (HTML content)

For HTML-based regulatory content (EPA summary pages, ECHA, OSHA):
```
1. web_extract(urls=[...]) — extract up to 5 URLs at once
2. Compile from 2-4 source pages per document for comprehensive coverage
3. write_file with:
   - # Source: <url> comments at top (one per source URL)
   - Structured markdown with sections
```

For eCFR content:
```
# Use /current/ URL path, NOT /api/versioner/
web_extract("https://www.ecfr.gov/current/title-29/...")
```

For PDF content:
```
apt-get install -y poppler-utils
pdftotext <pdf> <output.txt>
```

## File Provenance Convention
Every regulatory .txt file must start with `# Source: <url>` comments listing ALL source URLs used. This is critical for auditability — DABT exam study requires knowing the original authority.

Format:
```
# Source: https://www.epa.gov/laws-regulations/summary-...
# Source: https://www.epa.gov/assessing-and-managing-...
# Retrieved: 2026-05-29
```
