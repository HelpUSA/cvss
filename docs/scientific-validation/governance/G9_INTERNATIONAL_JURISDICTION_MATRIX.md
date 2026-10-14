# G9 — International Jurisdiction and Privacy Matrix
**Document ID:** `G9-INTERNATIONAL-JURISDICTION-MATRIX-v2.0`  
**Project:** HelpUS CVSS AI Scientific Validation  
**Sponsor:** HelpUS LLC (United States)  
**Initial Study Jurisdiction:** United States  
**Status:** BINDING COMPLIANCE MATRIX  
**Effective Date:** 2026-10-13  

---

## 1. Initial Scope

The human validation phase is structured as a U.S.-based study.

Initial operating model:
- sponsor and host: HelpUS LLC, United States;
- PI conducts the human-subjects phase from the United States;
- EDC and human-study records hosted in the United States;
- canonical scientific language: English;
- initial participants: U.S.-based independent cybersecurity experts;
- expansion outside the United States only after jurisdiction-specific clearance.

---

## 2. Core Rule

**No jurisdiction clearance = no recruitment.**

A participant may be invited only after:

`COUNTRY_CLEARANCE = YES`

For the initial U.S. cohort this requires:
- federal/Common Rule applicability check;
- FDA applicability check;
- institutional-policy/FWA check where relevant;
- state-law/privacy applicability check;
- consent-package approval;
- data-flow approval.

---

## 3. U.S. Compliance Matrix

| Dimension | Current Project Position |
|---|---|
| Sponsor | HelpUS LLC (United States) |
| Human-study operations | United States |
| Common Rule | No federal trigger identified currently |
| Self-declared exemption | Not used |
| FDA | No human-subjects trigger identified currently |
| Institutional IRB | Only if an institution/policy actually triggers it |
| State privacy | Evaluate per participant/state and company applicability |
| Consent | EN-US e-ICF with authoritative server evidence |
| Identity storage | U.S. restricted identity store |
| Consent storage | U.S. restricted consent store |
| Research responses | U.S. pseudonymized research store |
| Scientific dataset | Pseudonymized/anonymized analysis dataset |
| International recruitment | Not allowed without separate clearance |

---

## 4. State-by-State U.S. Review

Before recruitment of a U.S. expert, record:
- state of participation when legally relevant;
- whether a comprehensive state privacy law applies to HelpUS LLC and the processing;
- whether any sector-specific rule applies;
- whether employer or institutional policies restrict participation;
- whether any local requirement changes consent or privacy disclosures.

Do not claim blanket CCPA/CPRA or other state-law compliance for participants outside applicable scope.

---

## 5. Consent and Privacy

Research consent and privacy-law legal basis are separate concepts.

Production e-consent requires:
- participant/session identity binding;
- exact document version/hash;
- authoritative server timestamp;
- evidence of acceptance/signature;
- participant copy;
- withdrawal/reconsent history;
- immutable audit history.

A browser checkbox or localStorage record is not sufficient for production.

---

## 6. Data Minimization

The study should not collect:
- health data;
- biometric data;
- race/ethnicity;
- political views;
- religion;
- sexual orientation;
- unrelated employment records;
- unnecessary precise location.

Collect only information needed for:
- eligibility;
- contact;
- consent;
- conflict-of-interest screening;
- technical expert evaluation;
- security/audit.

---

## 7. International Expansion

If a future expert is outside the United States, create a country-specific row before invitation covering:

| Field | Required |
|---|---|
| Country | YES |
| Participant type | YES |
| Recruitment channel | YES |
| Institutional affiliation used | YES |
| Local ethics trigger | YES |
| Privacy-law applicability | YES |
| Consent language | YES |
| Hosting country | YES |
| Transfer/access mechanism | YES |
| Evidence file | YES |
| Cleared for recruitment | YES/NO |

No non-U.S. participant may proceed while `Cleared for recruitment = NO`.

---

## 8. Human-Study Activation

The portal remains synthetic-only until:
- PI is physically conducting the human phase from the U.S.;
- production EDC controls are complete;
- the regulatory applicability memo is current;
- the initial U.S. participant route is cleared;
- formal activation is recorded.

Until then:

`HUMAN_STUDY_ACTIVATION = BLOCKED`

---

## 9. Current Project State

- G1-G8 = PASS / CLOSED
- G9 = PENDING_EXTERNAL / U.S. APPLICABILITY + STUDY ACTIVATION
- G10 = PENDING_PROCEDURAL_EXTERNAL
- SAFE_TO_FREEZE = NO
- HUMAN EDC USE = NOT AUTHORIZED
- C1/C2 = SEALED / UNOPENED / UNEXECUTED / DO NOT RETUNE
