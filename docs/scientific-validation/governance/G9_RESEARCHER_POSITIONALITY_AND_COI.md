# G9 — Researcher Positionality, Professional Engagement, and Conflict of Interest (COI) Statement
**Document ID:** `G9-RESEARCHER-POSITIONALITY-AND-COI-v1.0`  
**Project:** HelpUS CVSS AI Scientific Validation  
**Sponsor:** HelpUS LLC (United States)  
**Status:** BINDING DISCLOSURE CHARTER  
**Effective Date:** 2026-10-13  

---

## 1. Purpose and Philosophical Foundation

In high-stakes computational cybersecurity and automated artificial intelligence evaluation, transparency regarding the researcher's background, institutional motivations, professional interactions, and financial relationships is foundational to reproducibility and peer-review integrity. This document sets forth a formal Researcher Positionality and Conflict of Interest statement for all academic publications, conference proceedings, and public repositories associated with HelpUS CVSS AI.

---

## 2. Institutional Affiliation & Commercial Disclosure

1. **Corporate Sponsor**: The research is sponsored and supported by HelpUS LLC, an entity incorporated in the United States.
2. **Commercial Interest**: The algorithmic technology and automated scoring pipelines developed under this project may form the basis for commercial enterprise vulnerability triage services provided by HelpUS LLC.
3. **Intellectual Property**: Wagner Santos (Principal Investigator) is the primary inventor and developer of the HelpUS CVSS AI engine and holds an equity/founder interest in HelpUS LLC.

---

## 3. Factual Characterization of FIRST / CVSS Ecosystem Engagement

### 3.1. Approved Factual Statements
The Principal Investigator regularly follows and participates in technical dialogues surrounding vulnerability scoring methodologies. Publications and biographical notices may factually declare:
- *"The Principal Investigator has actively participated in CVSS-related community meetings and technical discussions concerning vulnerability scoring practices."*
- *"The research methodology was informed by insights gained through engagement with the broader CVSS practitioner and working group discussions."*
- *"The authors actively follow and contribute technical discussions within vulnerability management communities."*

### 3.2. Prohibited Claims (Boundary Rules)
Unless verified by formal institutional membership credentials and organizational authorization, authors and project documentation shall **NOT** claim:
- "Official representative of FIRST.org";
- "FIRST-endorsed scoring engine / methodology";
- "Institutional member of FIRST Special Interest Group on behalf of HelpUS LLC";
- "Research certified or co-sponsored by FIRST".

### 3.3. Methodological and Ethics Demarcation
Participation in community discussions provides technical domain competence, but does **NOT** substitute for:
- Independent Research Ethics Committee (CEP/IRB) approval;
- Rigorous statistical hypothesis pre-registration;
- Strict double-blind separation between the PI and external expert adjudicators.

---

## 4. Methodological Safeguards Against Researcher Bias

To prevent the Principal Investigator's commercial interest and theoretical preconceptions from introducing confirmation bias into the validation results, the project enforces four objective architectural safeguards:

1. **Pre-Registration & Protocol Freezing (G9 / SAP v1.0)**:
   All statistical hypotheses, primary endpoints (Gwet's AC1 ≥ 0.80), sample size calculations, and metric formulas are cryptographically frozen in `G9_SAP_v1.0.md` prior to unsealing evaluation data.
2. **Cryptographic Sealing of Datasets C1 & C2**:
   The definitive testing datasets C1 (synthetic multi-vector benchmark) and C2 (complex edge-case corpus) are encrypted and sealed with SHA-256 commitments (`SEALED / UNOPENED / DO NOT RETUNE`). The PI has zero discretion to filter, prune, or reweight data post-execution.
3. **Architectural Blinding in Web EDC (G10 Custody)**:
   The Web EDC platform enforces cryptographic role separation. The PI has zero ability to view expert scoring in progress or modify submitted adjudications. Expert identities are segregated from rating data.
4. **Independent 5-Expert Panel**:
   Scoring is performed by five independent external cybersecurity professionals bound by non-affiliation warranties. The PI and co-authors are barred from participating in the scoring panel.
