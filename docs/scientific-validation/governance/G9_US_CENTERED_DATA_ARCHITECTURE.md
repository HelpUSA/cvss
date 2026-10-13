# G9 — U.S.-Centered Data Architecture and Brazil Access Minimization

**Document ID:** `G9-US-CENTERED-DATA-ARCHITECTURE-v1.0`  
**Project:** HelpUS CVSS AI Scientific Validation  
**Sponsor:** HelpUS LLC (United States)  
**Status:** GOVERNANCE DESIGN — PRE-PRODUCTION  
**Effective Date:** 2026-10-13  

## 1. Objective

Define a U.S.-centered operating model that preserves HelpUS LLC operational independence while minimizing unnecessary personal-data processing from Brazil.

This architecture does not attempt to evade Brazilian law. It separates operational custody of identifiable participant data from scientific analysis.

## 2. Target Data Zones

### Zone A — U.S. Identity Store
Contains:
- name;
- email;
- invitation status;
- authentication metadata;
- jurisdiction clearance.

Access:
- restricted operational role only;
- Brazil-based PI has no routine access.

### Zone B — U.S. Consent Store
Contains:
- e-ICF/TCLE version;
- document hash;
- authoritative consent timestamp;
- signature/acceptance evidence;
- withdrawal/reconsent events.

Access:
- restricted compliance role;
- Brazil PI receives only status and approved audit evidence when necessary.

### Zone C — U.S. Pseudonymized Research Store
Contains:
- participant code;
- scenario responses;
- rationale;
- instrument version;
- submission receipt;
- audit-chain evidence.

Contains no direct identity fields.

### Zone D — Scientific Analysis Export
Preferred export to Brazil:
- anonymized or maximally minimized;
- no name/email/IP/signature/authentication event;
- no identity-code mapping key;
- only fields required by the frozen SAP.

## 3. Default Access Rule

`BRAZIL_PI_PERSONAL_DATA_ACCESS = DENY_BY_DEFAULT`

Any exception requires:
- documented purpose;
- least-privilege authorization;
- access log;
- time limitation;
- DMP update where material.

## 4. Identity Separation

The participant-code lookup table must:
- reside separately from the response dataset;
- use stricter access control;
- never be embedded in browser-side code;
- never be included in scientific exports;
- never be stored in C1/C2.

## 5. Anonymization

Pseudonymization is not anonymization.

Before a dataset is classified as anonymous for Brazil analysis, the project must document:
- removal of direct identifiers;
- removal/generalization of quasi-identifiers;
- re-identification risk assessment;
- separation/destruction or inaccessibility of linkage keys for the receiving analysis context.

## 6. Portal Production Boundary

Current public EDC remains synthetic-only.

Live mode requires:
- server-side authenticated token flow;
- U.S. authoritative stores;
- server-side consent and submission events;
- recursive canonicalization;
- server-side HMAC/signature;
- append-only audit trail;
- immutable submission state;
- no answer-key data in expert bundle.

## 7. Regulatory Result

A U.S.-centered architecture can materially reduce LGPD exposure by minimizing personal-data processing in Brazil.

It does **not** automatically eliminate:
- Brazilian ethics review;
- LGPD applicability to any personal data actually processed in Brazil;
- international-transfer analysis;
- U.S. state/institutional requirements.

## 8. Current State

- G9 = PENDING_EXTERNAL
- HUMAN COLLECTION = NOT AUTHORIZED
- EDC = SYNTHETIC DRY-RUN ONLY
- C1/C2 = SEALED / UNOPENED / UNEXECUTED / DO_NOT_RETUNE
