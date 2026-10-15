# Antigravity Execution Report — PR #34: Explain Assessment Results from Persisted Facts

- **Repository**: HelpUSA/cvss
- **PR**: #34 — UX: explain assessment results from persisted facts
- **Branch**: `chatgpt/result-explanation`
- **Base**: `scientific-validation`
- **Tested HEAD**: `073715e7104e35fa39e65fbe308c4025a473e4c0` (with defensive parser enhancement and expanded tests)
- **Status**: **MERGE READY (PASSED ALL GATES)**

---

## 1. Quality Gates & Validation Summary

| Gate | Target / Tool | Result | Details |
|---|---|---|---|
| **Prisma Schema Validation** | `npx prisma validate` | **PASS** | Valid schema, zero changes needed. |
| **Prisma Client Generation** | `npx prisma generate` | **PASS** | v6.19.0 client successfully generated. |
| **TypeScript Typecheck** | `npm run typecheck` (`tsc --noEmit`) | **PASS** | 0 compilation errors across entire web app. |
| **SaaS & UX Unit Tests** | `npm run test:saas:unit` | **PASS** | 40/40 tests passed (including 8 comprehensive explanation tests). |
| **Python Core Suite** | `pytest tests/` | **PASS** | 166/166 passed in 2.66s. Scorer sealed. |
| **Next.js Production Build** | `npm run build` | **PASS** | 46 routes built cleanly with zero compilation errors. |
| **GitHub Actions Pipeline** | PR #34 Checks | **PASS** | AI Exchange Validation: PASS, validate: PASS, Vercel: PASS. |

---

## 2. Functional Scenario Verification

### Case A: Completed run with changed score
- **Inputs**: `sourceScore: 9.8`, `finalScore: 9.3`, `candidateMetrics: { MAV: "N", CR: "H" }`, `sourceReference: "ADV-2026-001"`.
- **Result Output**:
  - What changed: `"O score contextual mudou de 9.8 para 9.3."`
  - Why: Lists exact applied candidate metrics (`"MAV: N"`, `"CR: H"`).
  - Evidence: Provenance details displayed (`Fonte: GUIDED_MANUAL_INPUT`, `Referência: ADV-2026-001`).
  - Next Action: Recommends using the result with preserved vector & evidence, and rerunning if environment changes.
- **Verification**: Verified via `test("completed run explains score change and applied metrics (Case A)")`.

### Case B: Completed run with unchanged score
- **Inputs**: `sourceScore: 8.5`, `finalScore: 8.5`, `candidateMetrics: { MAV: "N" }`.
- **Result Output**:
  - What changed: `"O contexto analisado não alterou o score numérico de origem."`
  - Why: Still presents candidate metrics applied (`"MAV: N"`), without falsely claiming "no changes applied" unless empty.
- **Verification**: Verified via `test("completed run explains unchanged numeric score while preserving candidate metrics (Case B)")`.

### Case C: ABSTAIN run (No invented environmental claims)
- **Inputs**: `status: "ABSTAINED"`, `finalScore: null`, `abstentionReasons: ["Idade da telemetria ausente", "Reachability desconhecida"]`.
- **Result Output**:
  - What changed: `"Nenhuma afirmação ambiental final foi emitida."`
  - Why: Lists exact persisted abstention reasons without hallucinating environmental scores.
  - Next Action: Guides user to correct missing/stale/conflicting evidence and execute a new run without editing history.
  - Base Score: CVSS-B remains available and unaltered below the explanation.
- **Verification**: Verified via `test("abstained run explains unresolved evidence and prevents invented environmental claims (Case C)")`.

### Case C2: Defensive parsing of structured reason objects
- **Inputs**: `abstentionReasons` containing mixture of strings, `{ reason: "..." }`, and `{ message: "..." }`.
- **Result Output**: Extracts plain-text strings cleanly without rendering `[object Object]`.
- **Verification**: Verified via `test("abstained run parses structured reason objects defensively (Case C2)")`.

### Case D: Null or empty source reference
- **Inputs**: `sourceReference: null`.
- **Result Output**: Renders `"Referência externa: não informada"` without crash or undefined text.
- **Verification**: Verified via `test("null source reference displays fallback text safely without crashing (Case D)")`.

---

## 3. Placement & Semantic Safety

- **Page Order**: `<RunExplanation>` renders directly before `<section className="tenant-metric-grid">`. The user reads "What happened" first, followed by auditability metrics, vectors, hashes, and engine commit metadata.
- **Zero AI / External Calls**: Operates strictly on persisted run facts in PostgreSQL. No LLM, no external fetch, no recalculation.
- **Semantic Neutrality**: States what was recorded (e.g. `"MAV: N foi uma métrica contextual aplicada"`) without inventing unverified causal claims.

---

## 4. Usability, Responsive Layout & Accessibility

- **Breakpoints Tested**:
  - Desktop (1440px): 2-column grid (`.run-explanation__grid`) with clear spacing and structured articles.
  - Tablet (768px): 2-column grid adapts cleanly without layout disruption.
  - Mobile (375px): Stacks into 1 column (`@media (max-width: 720px) { grid-template-columns: 1fr; }`).
- **Accessibility Verification**:
  - Semantic section with `aria-labelledby="run-explanation-title"`.
  - Accessible heading hierarchy: `<h2>` section title, followed by `<h3>` for each card ("O que mudou?", "Por quê?", "Qual evidência sustentou?", "Próximo passo").
  - Lists formatted with standard `<ul>` and `<li>`.
  - Contrast compliant with WCAG AA. Zoom at 200% displays cleanly without horizontal clipping.

---

## 5. Architectural Boundaries Preserved

- Canonical CVSS v4.0 Scorer (`core/cvss40.py`): FROZEN / UNTOUCHED.
- Rule catalog & TTL thresholds: UNTOUCHED.
- FIRST Reference Calculator Corpus G1: UNTOUCHED.
- Sealed datasets C1/C2: UNTOUCHED.
- Zero Prisma database migrations added.

---

## 6. Recommendation

**MERGE**: PR #34 satisfies all user requirements, preserves technical auditability, enforces semantic safety, and passes 100% of local and CI quality gates.
