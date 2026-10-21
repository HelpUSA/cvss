# Antigravity handoff — advanced CR/IR/AR

Repository: HelpUSA/cvss
Branch: chatgpt/advanced-security-requirements
Base: scientific-validation

## ChatGPT already implemented

- active tenant policy lookup;
- advanced progressive-disclosure CR/IR/AR section;
- defaults X / Not Defined;
- active policy selector;
- form guard requiring active policy when any CR/IR/AR != X;
- payload wiring to organizationPolicyId, policyVersion and securityRequirements;
- responsive CSS;
- regression tests;
- no scorer/rule changes.

## Required validation

Inside web/:
1. npm ci
2. npx prisma validate
3. npx prisma generate
4. npm run typecheck
5. npm run test:saas:unit
6. npm run build

Run pytest/real pipeline as required.

## Browser/runtime cases

### A. Default path
Leave CR/IR/AR at X.
Expected:
- no policy required;
- no securityRequirements sent;
- basic flow remains unchanged;
- resulting nomenclature should not gain Environmental status solely because X values were untouched.

### B. Non-X without policy
Set CR=H with no policy.
Expected:
- client blocks submit;
- clear message asks for active organization policy.

### C. Governed CR/IR/AR
Select an ACTIVE tenant policy and values such as CR=H, IR=M, AR=L.
Expected:
- payload includes organizationPolicyId and policyVersion;
- securityRequirements contains CR/IR/AR;
- current engine accepts and records candidate metrics;
- resulting vector/nomenclature reflect Environmental metrics as appropriate.

### D. Inactive/foreign policy
Craft request or UI state using inactive/foreign tenant policy identifiers.
Confirm current server-side evidence/rule path cannot silently treat it as governed. If server-side policy existence/status validation is missing, report FIX_REQUIRED and implement the smallest tenant-scoped validation in the run route before merge.

### E. All X with policy selected
Confirm all-X behaves as Not Defined and does not invent candidate metrics.

## Semantic checks

Confirm labels/help make clear:
- these are properties of the vulnerable system/environment;
- X is the safe default;
- they are not compensating controls;
- they do not change Base metrics directly.

## Responsive/accessibility

Test 1440px, 768px, 375px, keyboard details/summary, selects, focus-visible, zoom 200%.

## Do not change

- canonical scorer;
- FIRST arithmetic;
- rule catalog semantics;
- ABSTAIN;
- TTL;
- C1/C2;
- EvidenceSnapshot history.

## Return

Create:
docs/reviews/ANTIGRAVITY_ADVANCED_SECURITY_REQUIREMENTS_REPORT.md

Include:
- tested HEAD;
- gates;
- cases A-E;
- server-side policy validation finding;
- nomenclature/vector behavior;
- responsive/accessibility;
- files changed;
- residual issues;
- MERGE or FIX_REQUIRED.
