# Real-world CVSS implementation plan

Updated: 2026-05-28 15:35:16

## Decision

The project is moving from a prototype deterministic methodology into a real-world practical implementation path. The existing prototype remains a baseline, but the definitive path must support operational use, official CVSS semantics, real vulnerability data, reproducible validation, and defensible outputs.

## Non-negotiable requirements

1. Preserve the current static MVP and prototype results as baseline artifacts.
2. Implement or integrate official CVSS scoring semantics before making real-world scoring claims.
3. Clearly separate official CVSS metrics from additional environmental/business context signals.
4. Replace synthetic-only scenarios with real CVE-backed validation cases.
5. Keep every score explainable with traceable inputs, formula outputs, and rationale.
6. Support operational site workflows: input, calculate, explain, export, and reproduce.
7. Avoid claiming independent human expert validation until a real adjudication protocol is completed.

## Phases

### Phase 1: Foundation freeze

- Tag or document current prototype baseline.
- Keep current public deployment stable.
- Start real-world work on this branch.

### Phase 2: Official CVSS core

- Add official CVSS vector parser.
- Add official CVSS score calculation path.
- Add tests against known vectors.
- Document CVSS version support.

### Phase 3: Contextual environmental layer

- Keep contextual factors explicit and separate from official CVSS metrics.
- Support adjustment trace output.
- Make every adjustment auditable.

### Phase 4: Real-world data ingestion

- Add real CVE/NVD input structure.
- Add references to vendor advisories or NVD records.
- Add evidence source fields.

### Phase 5: Validation

- Build validation set with real vulnerabilities and realistic environments.
- Compare official score, contextual score, and expected operational priority.
- Add reviewer protocol for later human expert adjudication.

### Phase 6: Operational site

- Add multi-finding analysis.
- Add import/export of scenario packages.
- Add detailed report output.
- Add user-facing explanation of official vs contextual scoring.

### Phase 7: Article revision

- Rewrite article from prototype-only manuscript into practical system manuscript.
- Include real CVE validation if available.
- Keep limitations explicit.

## Immediate next step

Build an official-CVSS compatibility layer and tests while preserving the prototype contextual policy.
