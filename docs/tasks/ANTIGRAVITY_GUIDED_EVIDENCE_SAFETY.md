# Antigravity handoff — guided evidence safety

Repository: HelpUSA/cvss
Branch: chatgpt/ux-guided-evidence-safety
Base: scientific-validation

## ChatGPT already implemented

- safer evidence-entry defaults:
  - reachability UNKNOWN;
  - evidence quality UNKNOWN;
  - telemetry age blank/null instead of implicit zero;
- explicit "Ainda não avaliei" choices;
- contextual CVSS evidence guidance before the run form;
- responsive styling for the inline help;
- regression tests preventing optimistic defaults from returning;
- architecture note documenting rationale and scope.

## What Antigravity should do

Do not redesign or replace this work.

Validate the exact branch/head in a real web environment and complement only where necessary.

### Required commands

Inside web/:

1. npm ci
2. npx prisma validate
3. npx prisma generate
4. npm run typecheck
5. npm run test:saas:unit
6. npm run build

### Browser checks

Use a disposable/test tenant.

Validate at approximately:
- 375px mobile;
- 768px tablet;
- 1440px desktop.

Flow:
Login -> Organization -> Comece aqui -> Project -> Environment -> Assessment -> Evidence -> Result

On the evidence page confirm:

1. no factual environmental assertion is preselected;
2. "Ainda não avaliei" is visible for reachability and evidence quality;
3. telemetry age begins blank;
4. submitting unknown/incomplete evidence produces the expected fail-closed behavior, not an optimistic environmental score;
5. entering sufficient current evidence still produces the normal result path;
6. help details are keyboard accessible;
7. layout does not become excessively long or visually noisy on mobile;
8. back/forward navigation does not invent values.

### Specific functional cases

Case A — untouched contextual inputs:
- expect UNKNOWN/UNKNOWN/null semantics;
- expect ABSTAIN/evidence remediation as appropriate.

Case B — known internal routed + sufficient + age 0:
- explicitly choose those values;
- confirm normal engine behavior.

Case C — conflicting/insufficient:
- confirm ABSTAIN reason is clear on result page.

### Do not change

- frozen scorer;
- FIRST gate;
- environmental rule semantics;
- TTL thresholds;
- C1/C2 sealed material;
- historical expert-study artifacts.

### Optional improvements only if clearly needed after browser inspection

- CSS spacing refinements;
- clearer focus styles;
- field-level message if blank telemetry is confusing;
- wording refinements that preserve the same semantics.

Do not add CR/IR/AR advanced inputs in this PR unless there is a concrete blocker. That should be a separate increment.

## Return

Commit any necessary browser-derived fixes to this branch and add a report containing:

- tested HEAD SHA;
- commands/results;
- SaaS tests count;
- typecheck/build status;
- mobile/tablet/desktop result;
- untouched-input ABSTAIN result;
- explicit-known-input normal-result outcome;
- accessibility notes;
- files changed;
- residual issues;
- recommendation MERGE or FIX_REQUIRED.
