# G9 — Author and Contributor Roles Charter (CRediT Taxonomy)
**Document ID:** `G9-AUTHOR-CONTRIBUTOR-ROLES-v1.0`  
**Project:** HelpUS CVSS AI Scientific Validation  
**Sponsor:** HelpUS LLC (United States)  
**Taxonomy Standard:** ANSI/NISO Z39.104-2022 (Contributor Roles Taxonomy — CRediT)  
**Status:** BINDING AUTHORSHIP CHARTER  
**Effective Date:** 2026-10-13  

---

## 1. Principles of Authorship and Scientific Integrity

HelpUS LLC adheres strictly to the International Committee of Medical Journal Editors (ICMJE) and Committee on Publication Ethics (COPE) standards for scientific authorship:
1. Substantial contributions to the conception or design of the work; or the acquisition, analysis, or interpretation of data for the work;
2. Drafting the work or reviewing it critically for important intellectual content;
3. Final approval of the version to be published;
4. Agreement to be accountable for all aspects of the work in ensuring that questions related to the accuracy or integrity of any part of the work are appropriately investigated and resolved.

Honorary, gift, or familial authorship is strictly prohibited. Co-authorship must be supported by documented, substantive intellectual or technical labor.

---

## 2. Contributor Attribution Matrix (CRediT)

### 2.1. Principal Investigator (PI) — Wagner Santos
- **Affiliation**: HelpUS LLC / Independent Cybersecurity Research Group (Brazil)
- **Role**: Primary Author & Principal Investigator
- **CRediT Allocations**:
  - **Conceptualization**: Lead (formulation of zero-shot deterministic CVSS 4.0 evaluation model and multi-source cross-entropy weighting).
  - **Methodology**: Lead (development of validation gates G1–G10, statistical power calculation, synthetic scenario curation).
  - **Software**: Lead (author of core CVSS 4.0 mathematical engine, deterministic parser, and test suite).
  - **Formal Analysis**: Lead (statistical analysis plan SAP v1.0, Gwet's AC1 and Fleiss' Kappa formulation).
  - **Investigation**: Lead (execution of benchmark tests against FIRST.org 486k corpus).
  - **Writing – Original Draft**: Lead (composition of the primary manuscript, theoretical foundations, and mathematical appendices).
  - **Project Administration**: Lead (overall coordination of research lifecycle).

### 2.2. Collaborator / Potential Coauthor — US-Resident Technical Lead (Son of PI)
- **Affiliation**: HelpUS LLC (United States)
- **Role**: Coauthor (Contingent on Substantive Technical Execution)
- **Eligible CRediT Allocations**:
  - **Software**: Supporting (architecture, maintenance, and deployment of the Web Electronic Data Capture — EDC system).
  - **Validation Infrastructure**: Lead (implementation of HMAC-SHA256 audit trails, version hashes, and zero-trust blinding controls).
  - **Data Curation**: Supporting (data pipeline automation, artifact hashing, and portable clean-room reproduction scripts).
  - **Writing – Review & Editing**: Supporting (critical revision of manuscript text, regulatory harmonization with US disclosures).
  - **Reproducibility**: Lead (Docker packaging, Vercel edge deployment, and multi-platform validation runs).
- **Absolute Boundary Rule**:
  - **`SON_AS_COAUTHOR = PERMITTED_IF_SUBSTANTIVE_CONTRIBUTION`**
  - **`SON_AS_ONE_OF_5_INDEPENDENT_EXPERTS = STRICTLY_PROHIBITED`**
  - He shall under no circumstances serve as an evaluator, reviewer, or adjudicator in the 5-expert independent panel.

---

## 3. The 5 Independent Expert Evaluators (Study Participants)

The five external cybersecurity specialists recruited for the blind adjudication panel hold a distinct, legally protected scientific role:
- **Role Classification**: Research Participants / Expert Adjudicators (NOT Co-Authors).
- **Blinding & Independence**:
  - Completely independent of HelpUS LLC corporate ownership, employment, or familial relationships.
  - Evaluate vulnerability scenarios under double-blind protocols (blind to engine scores, peer evaluations, and synthetic metadata).
- **Confidentiality & Acknowledgment**:
  - Identified in scientific publications solely via persistent pseudonyms (`EXP-01` through `EXP-05`).
  - May be acknowledged by name in the *Acknowledgements* section of published manuscripts only upon voluntary, written opt-in provided via their e-ICF / TCLE submission.
  - Zero authorial liability or financial interest in HelpUS LLC intellectual property.

---

## 4. Governance Verification

Any manuscript submission derived from this codebase must attach this charter as supplementary governance documentation to assure peer reviewers and editors that evaluator independence was rigorously maintained and all co-authors satisfied international standards.
