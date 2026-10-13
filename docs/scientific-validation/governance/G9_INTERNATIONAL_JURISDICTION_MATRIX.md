# G9 — International Legal, Ethics, and Data Protection Matrix
**Document ID:** `G9-INTERNATIONAL-JURISDICTION-MATRIX-v1.0`  
**Project:** HelpUS CVSS AI Scientific Validation  
**Sponsor:** HelpUS LLC (United States)  
**Status:** BINDING COMPLIANCE MATRIX  
**Effective Date:** 2026-10-13  

---

## 1. Multi-Jurisdictional Scope & Regulatory Harmonization

The HelpUS CVSS AI scientific validation protocol engages an international architecture:
- **Corporate Sponsor & Hosting**: HelpUS LLC (Delaware / United States)
- **Principal Investigator**: Wagner Santos (Brazil)
- **Coordinating Ethics Jurisdiction**: Brazil (SINEP / CEP)
- **Expert Adjudication Panel**: Multi-national cybersecurity specialists (Brazil, United States, European Union / UK)

This matrix establishes compliance across three major legal frameworks: Brazilian Law, United States Federal and State Law, and European Union Data Protection Regulations.

---

## 2. Comparative Compliance Matrix

| Dimension | Brazil (Coordinating) | United States | European Union (GDPR) | HelpUS CVSS AI Implementation |
|---|---|---|---|---|
| **Primary Ethics Oversight** | CONEP / CEP (Res. CNS 510/2016, CNS 466/2012) | 45 CFR 46 (Common Rule) | Declaration of Helsinki / National Ethics Bodies | Coordinated via Brazilian CEP (free of commercial bias); US Common Rule minimal risk survey exemption applied. |
| **Informed Consent** | TCLE (Termo de Consentimento Livre e Esclarecido) eletrônico | Electronic Informed Consent (e-ICF, 45 CFR § 46.116) | Informed Consent (Art. 6(1)(a) & Art. 9(2)(a) GDPR) | Trilingual e-ICF/TCLE (PT/EN/ES) presented before authentication; cryptographic timestamp and immutable audit log. |
| **Data Privacy Law** | LGPD (Lei Geral de Proteção de Dados, Lei 13.709/2018) | CCPA/CPRA, State Privacy Statutes | GDPR (Regulation EU 2016/679) | Unified zero-trust privacy policy; explicit participant rights to access, rectification, and withdrawal. |
| **Scientific Research Basis** | LGPD Art. 7, IV (Estudos por órgão de pesquisa) | Common Rule 45 CFR § 46.104(d)(2) (Exempt survey) | GDPR Art. 89(1) (Safeguards for scientific research) | Research data processed exclusively for scientific validation of vulnerability metrics. |
| **Pseudonymization Standard** | Anonimização / Pseudonimização (LGPD Art. 13) | HIPAA / De-identification best practices | GDPR Art. 4(5) & Recital 26 Pseudonymisation | Separation of participant identity tables from adjudication metrics; unique nonces `EXP-01` to `EXP-05`. |
| **Cross-Border Transfer** | LGPD Art. 33 (Transferência Internacional de Dados) | US Cross-Border Data Framework | GDPR Chapter V (Standard Contractual Clauses) | End-to-end TLS 1.3 encryption, edge deployment on Vercel US/BR nodes, zero transmission of unencrypted PII. |
| **Right to Erasure / Revocation** | LGPD Art. 18, VI (Revogação do consentimento) | 45 CFR § 46.116(b)(8) (Right to withdraw) | GDPR Art. 17 (Right to erasure) & Art. 89 exceptions | Participants may withdraw consent anytime; upon revocation, personal records are permanently expunged. |

---

## 3. Country Clearance Protocol for International Experts

Prior to formal onboarding of any non-Brazilian expert to the active adjudication phase:
1. **Jurisdiction Verification**: Verification of expert's country of tax residency and employer moonlighting/consulting policies.
2. **Clearance Check**: Confirmation that participant's home institution does not claim mandatory extraterritorial IRB ownership over independent professional survey participation.
3. **Language Selection**: Participant selects canonical language (English default, Spanish, or Brazilian Portuguese) for legal notices and user interface.
4. **Conflict of Interest Warranty**: Signing of multi-jurisdictional non-affiliation declaration confirming absence of personal, financial, or familial ties to HelpUS LLC or the authors.
