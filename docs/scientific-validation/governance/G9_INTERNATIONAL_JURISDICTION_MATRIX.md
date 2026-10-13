# G9 — International Legal, Ethics, and Data Protection Matrix
**Document ID:** `G9-INTERNATIONAL-JURISDICTION-MATRIX-v1.1`  
**Project:** HelpUS CVSS AI Scientific Validation  
**Sponsor:** HelpUS LLC (United States)  
**Status:** BINDING COMPLIANCE MATRIX  
**Effective Date:** 2026-10-13  

---

## 1. Operating Model

The HelpUS CVSS AI validation may operate with a U.S.-centered technical environment while the Principal Investigator remains based in Brazil.

Current governance:

- **Sponsor / operational host:** HelpUS LLC (United States)
- **PI location:** Brazil
- **Coordinating ethics review:** SINEP / competent CEP in Brazil
- **Scientific canonical language:** English
- **Participant pool:** Brazil, United States, and other countries only after jurisdiction clearance
- **Human-use status:** NOT AUTHORIZED until ethics approval
- **EDC status:** SYNTHETIC DRY-RUN ONLY until production controls are complete

---

## 2. Core Rule

**No country clearance = no recruitment.**

A participant may be invited only after:

`COUNTRY_CLEARANCE = YES`

which requires:
- ethics applicability review;
- institutional-policy review where relevant;
- privacy-law applicability review;
- consent-language package;
- data-flow approval;
- transfer/access safeguards.

---

## 3. Data-Protection Matrix

| Data/Operation | U.S.-centered target state | Brazil/LGPD impact | Required control |
|---|---|---|---|
| Name/email | U.S. identity store | Avoid access from Brazil where feasible | Segregated identity store; least privilege |
| e-ICF / signature evidence | U.S. consent store | Avoid routine Brazil access | Versioned consent artifact + server receipt |
| Authentication/security logs | U.S. security store | Avoid routine Brazil access | Short retention; security purpose only |
| Expert scientific responses | Pseudonymized U.S. research store | LGPD may apply if processed/accessed in Brazil | Minimize fields; role-based access |
| Identity-code linkage | U.S. restricted vault | Do not expose to Brazil PI by default | Separate key table |
| Analysis dataset for PI | Prefer anonymized/minimized export | If truly anonymized, LGPD personal-data rules may no longer apply to that dataset | Document anonymization method |
| Aggregate statistics | U.S. or Brazil | Low privacy exposure if non-identifying | Suppression/aggregation checks |
| Cross-border access | Explicitly logged | Can trigger LGPD territorial or transfer analysis | Data-flow map + legal basis + logging |

---

## 4. LGPD Territorial Scope

LGPD is not determined only by server location or participant nationality.

If the Brazil-based PI or another person in Brazil performs operations on personal or pseudonymous participant data, that may constitute processing in Brazilian territory.

Therefore:

**U.S. hosting does not automatically remove LGPD.**

The project's preferred architecture is to reduce Brazilian access to identifiable or linkable data and provide the PI only the minimum scientific dataset required.

This is a privacy-minimization strategy, not an attempt to bypass Brazilian law.

---

## 5. Legal-Basis Discipline

HelpUS LLC is a for-profit company and must **not** use `LGPD Art. 7, IV — studies by research body` as a blanket basis merely because the activity is scientific.

A purpose-by-purpose legal-basis matrix must be maintained for:

- recruitment/contact;
- consent evidence;
- research responses;
- security logs;
- audit trail;
- retention;
- incident response;
- international transfers/access.

Ethics consent and data-protection legal basis are separate concepts.

---

## 6. United States

For an independent U.S.-based expert:

- a U.S. IRB is not automatically required solely because the participant resides in the United States;
- first determine whether any federal, FDA, institutional, contractual, or state trigger exists;
- do not self-declare a Common Rule exemption as the project's primary legal basis;
- if no U.S. trigger is identified, document that conclusion in the participant's jurisdiction-clearance record.

Preferred status language:

`US_IRB_REQUIREMENT = NONE_IDENTIFIED_AFTER_APPLICABILITY_REVIEW`

not:

`US_EXEMPT = YES`

---

## 7. Brazil

Current ethics architecture must be described using:

- Lei 14.874/2024;
- Decreto 12.651/2025;
- SINEP;
- CEP;
- INAEP.

Older CNS/Conep materials may be referenced where still effective and compatible, but not as the primary current architecture.

Brazilian participants should receive a PT-BR consent package when required for comprehension and CEP approval, even though the scientific instrument itself may remain in English if eligibility requires sufficient English proficiency.

---

## 8. European Union / EEA

Europe is not treated as a single ethics jurisdiction.

For each country:

- assess local research-ethics requirements;
- assess GDPR territorial scope;
- define participant-facing language;
- define controller/processor roles;
- define transfer mechanism where applicable.

Do not claim blanket `GDPR compliant` status before this mapping is complete.

---

## 9. U.S. State Privacy

Do not assume that CCPA/CPRA or any other state law applies to every participant.

For each U.S. participant:

- record state of participation only if needed for compliance;
- assess whether the relevant state privacy statute applies to HelpUS LLC and the specific processing;
- document the result.

Do not claim blanket U.S. state-law compliance.

---

## 10. Consent and Withdrawal

The portal must not treat a checkbox plus browser localStorage as production e-consent.

Production consent requires:

- participant/session identity binding;
- exact document version/hash;
- authoritative server timestamp;
- evidence of acceptance/signature;
- copy made available to participant;
- withdrawal/reconsent workflow;
- immutable audit history.

Withdrawal rights and data-retention consequences must be described accurately. Do not promise automatic deletion of all research records where scientific-integrity or legal obligations require retention of non-identifying records.

---

## 11. Cross-Border Architecture

Recommended operational flow:

`Participant -> U.S. EDC -> U.S. identity/consent store -> U.S. pseudonymized research store -> anonymized/minimized scientific export -> PI in Brazil`

This is the preferred privacy architecture because it:

- keeps direct identifiers outside the scientific dataset;
- reduces unnecessary international exposure;
- reduces the amount of personal data processed from Brazil;
- preserves the ability to conduct scientific analysis from Brazil.

Any deviation must be documented in the DMP.

---

## 12. Recruitment Clearance Record

For each participant, record at minimum:

| Field | Required |
|---|---|
| Country | YES |
| State/region when relevant | YES |
| Participant type | YES |
| Institutional affiliation used for recruitment | YES |
| Local ethics trigger | YES |
| U.S. federal/FDA trigger where applicable | YES |
| Institutional-policy trigger | YES |
| Privacy-law applicability | YES |
| Consent language | YES |
| Data-hosting region | YES |
| Cross-border access path | YES |
| Evidence file | YES |
| Cleared for recruitment | YES/NO |

No participant may proceed unless `Cleared for recruitment = YES`.

---

## 13. Current Project State

- G1-G8 = PASS / CLOSED
- G9 = PENDING_EXTERNAL
- G10 = PENDING_PROCEDURAL_EXTERNAL
- SAFE_TO_FREEZE = NO
- C1/C2 = SEALED / UNOPENED / UNEXECUTED / DO_NOT_RETUNE
- HUMAN EDC USE = NOT AUTHORIZED
