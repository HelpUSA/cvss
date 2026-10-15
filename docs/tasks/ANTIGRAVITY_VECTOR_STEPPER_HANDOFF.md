# Antigravity handoff — vector validation + workflow stepper

Repository: HelpUSA/cvss
Branch: chatgpt/ux-vector-validation-stepper
Base: scientific-validation

## Already implemented by ChatGPT

- client-side structural CVSS v4.0 vector validation;
- inline validation state and detected nomenclature;
- submit guard for invalid non-empty vectors;
- telemetry age may remain blank/null;
- shared 5-step workflow stepper;
- stepper inserted on Projects, Environments, Assessments, Evidence and Result pages;
- responsive CSS;
- regression tests.

## Required validation

Inside web/:

1. npm ci
2. npx prisma validate
3. npx prisma generate
4. npm run typecheck
5. npm run test:saas:unit
6. npm run build

## Browser scenarios

### Vector validation

Test:
- valid Base-only vector -> accepted, CVSS-B;
- valid E metric -> CVSS-BT;
- valid environmental metric -> CVSS-BE;
- Threat + Environmental -> CVSS-BTE;
- wrong prefix -> blocked with inline error;
- missing Base metric -> blocked;
- duplicate Base metric -> blocked;
- unknown metric -> blocked;
- invalid metric value -> blocked;
- leading/trailing whitespace -> normalized safely.

Confirm server-side validation is still authoritative.

### Telemetry age

Leave age blank and confirm browser allows submission.
Expected: null reaches analysis and fail-closed behavior occurs if evidence is otherwise unresolved.

### Stepper

At 1440px, 768px and 375px confirm:
- correct current step on all five pages;
- prior steps appear completed;
- current step uses aria-current="step";
- no layout breakage;
- mobile horizontal scroll is understandable and no page-level overflow occurs.

## Accessibility

Check:
- inline error announced with role=alert;
- textarea has aria-invalid when malformed;
- stepper navigation has meaningful aria-label;
- current step exposed via aria-current;
- keyboard and zoom 200%.

## Do not change

- canonical scorer;
- FIRST semantics;
- rule catalog;
- ABSTAIN logic;
- C1/C2;
- historical expert artifacts.

## Return

Commit necessary fixes only if browser/build proves them necessary.

Create:
docs/reviews/ANTIGRAVITY_VECTOR_STEPPER_EXECUTION_REPORT.md

Return:
- tested head SHA;
- tests count;
- typecheck/build;
- vector scenarios;
- telemetry-null scenario;
- desktop/tablet/mobile;
- accessibility;
- files changed;
- residual issues;
- MERGE or FIX_REQUIRED.
