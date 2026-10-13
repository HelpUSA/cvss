# G9 — U.S.-Based Human Study Data Architecture

**Document ID:** `G9-US-CENTERED-DATA-ARCHITECTURE-v2.0`  
**Project:** HelpUS CVSS AI Scientific Validation  
**Sponsor:** HelpUS LLC (United States)  
**Study Operating Jurisdiction:** United States  
**Status:** GOVERNANCE DESIGN — PRE-ACTIVATION  
**Effective Date:** 2026-10-13  

## 1. Objective

Define a U.S.-based architecture for the human validation phase so that operational control, consent, participant identity, pseudonymized responses, and custody remain within the HelpUS LLC U.S. environment.

## 2. Activation Gate

The human phase may begin only when:

- the U.S.-resident Principal Investigator is conducting the human-subjects phase from the United States;
- the U.S. EDC production controls are complete;
- the U.S. regulatory applicability review is current;
- the target participant jurisdiction has been cleared;
- all synthetic-only restrictions are lifted through the formal study-activation record.

Until then:

`HUMAN_STUDY_ACTIVATION = BLOCKED`

## 3. Data Zones

### Zone A — U.S. Identity Store
Contains:
- name;
- email;
- invitation state;
- authentication metadata;
- jurisdiction clearance.

### Zone B — U.S. Consent Store
Contains:
- e-ICF version;
- document hash;
- authoritative consent timestamp;
- acceptance/signature evidence;
- withdrawal/reconsent events.

### Zone C — U.S. Pseudonymized Research Store
Contains:
- participant code;
- scenario responses;
- rationale;
- instrument version;
- submission receipt;
- audit-chain evidence.

No direct identifiers are permitted here.

### Zone D — Scientific Analysis Store
Contains:
- pseudonymized or anonymized study dataset;
- no direct identity fields;
- no identity-to-code mapping key.

## 4. Identity Separation

The participant-code lookup table must:
- reside separately from the response dataset;
- use stricter access control;
- never be embedded in browser code;
- never be included in scientific exports;
- never be stored in C1/C2.

## 5. Expert Portal Production Boundary

Current public EDC remains synthetic-only.

Live mode requires:
- server-side one-time invitation token;
- authoritative U.S. server timestamp;
- exact consent version/hash;
- recursive canonicalization;
- server-side HMAC/signature;
- append-only audit trail;
- immutable final state;
- no answer-key data in the expert bundle;
- fail-closed completeness validation;
- token-bound expert identity.

## 6. Participant Scope

Initial live recruitment should use U.S.-based independent experts unless another country has completed jurisdiction clearance.

No participant should be enrolled merely because the portal is technically reachable from that country.

## 7. Scientific Language

The canonical study language is English.

Additional consent or participant-facing translations may be added only when required for a cleared jurisdiction.

## 8. Historical Integrity

Historical governance records are not rewritten to imply facts that were not true at the time.

The U.S.-based study configuration applies prospectively from the formal activation date.

## 9. Current State

- G1-G8 = PASS / CLOSED
- G9 = PENDING_EXTERNAL / U.S. APPLICABILITY + STUDY ACTIVATION
- G10 = PENDING_PROCEDURAL_EXTERNAL
- SAFE_TO_FREEZE = NO
- HUMAN COLLECTION = NOT AUTHORIZED
- EDC = SYNTHETIC DRY-RUN ONLY
- C1/C2 = SEALED / UNOPENED / UNEXECUTED / DO NOT RETUNE
