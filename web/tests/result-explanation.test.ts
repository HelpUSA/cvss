import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

import { explainOperationalRun } from "../src/lib/run-explanation";

test("completed run explains score change and applied metrics (Case A)", () => {
  const result = explainOperationalRun({
    status: "COMPLETED",
    sourceScore: 9.8,
    finalScore: 9.3,
    decision: "changed",
    candidateMetrics: { MAV: "N", CR: "H" },
    abstentionReasons: null,
    sourceType: "GUIDED_MANUAL_INPUT",
    sourceReference: "ADV-2026-001",
    capturedAt: new Date("2026-10-15T12:00:00Z"),
  });
  assert.equal(result.abstained, false);
  assert.match(result.whatChanged, /O score contextual mudou de 9\.8 para 9\.3\./);
  assert.ok(result.why.includes("MAV: N"));
  assert.ok(result.why.includes("CR: H"));
  assert.ok(result.evidence.some((e) => e.includes("Referência: ADV-2026-001")));
  assert.match(result.nextAction, /Use este resultado junto com o vetor/);
});

test("completed run explains unchanged numeric score while preserving candidate metrics (Case B)", () => {
  const resultWithMetrics = explainOperationalRun({
    status: "COMPLETED",
    sourceScore: 8.5,
    finalScore: 8.5,
    decision: "unchanged",
    candidateMetrics: { MAV: "N" },
    abstentionReasons: null,
    sourceType: "GUIDED_MANUAL_INPUT",
    sourceReference: "https://example.com/advisory",
    capturedAt: new Date("2026-10-15T12:00:00Z"),
  });
  assert.equal(resultWithMetrics.abstained, false);
  assert.equal(resultWithMetrics.whatChanged, "O contexto analisado não alterou o score numérico de origem.");
  assert.ok(resultWithMetrics.why.includes("MAV: N"));

  const resultWithoutMetrics = explainOperationalRun({
    status: "COMPLETED",
    sourceScore: 8.5,
    finalScore: 8.5,
    decision: "unchanged",
    candidateMetrics: {},
    abstentionReasons: null,
    sourceType: "GUIDED_MANUAL_INPUT",
    sourceReference: "https://example.com/advisory",
    capturedAt: new Date("2026-10-15T12:00:00Z"),
  });
  assert.ok(resultWithoutMetrics.why.includes("Nenhuma métrica contextual adicional foi aplicada."));
});

test("abstained run explains unresolved evidence and prevents invented environmental claims (Case C)", () => {
  const result = explainOperationalRun({
    status: "ABSTAINED",
    sourceScore: 7.5,
    finalScore: null,
    decision: "abstained",
    candidateMetrics: {},
    abstentionReasons: ["Idade da telemetria ausente", "Reachability desconhecida"],
    sourceType: "GUIDED_MANUAL_INPUT",
    sourceReference: null,
    capturedAt: new Date("2026-10-15T12:00:00Z"),
  });
  assert.equal(result.abstained, true);
  assert.equal(result.whatChanged, "Nenhuma afirmação ambiental final foi emitida.");
  assert.deepEqual(result.unresolved, ["Idade da telemetria ausente", "Reachability desconhecida"]);
  assert.deepEqual(result.why, ["Idade da telemetria ausente", "Reachability desconhecida"]);
  assert.match(result.nextAction, /Revise as evidências/);
  assert.match(result.nextAction, /execute uma nova avaliação sem sobrescrever este histórico/);
});

test("abstained run parses structured reason objects defensively (Case C2)", () => {
  const result = explainOperationalRun({
    status: "ABSTAINED",
    sourceScore: 6.0,
    finalScore: null,
    decision: "abstained",
    candidateMetrics: null,
    abstentionReasons: [
      { reason: "Qualidade da evidência não suficiente (INSUFFICIENT)" },
      { message: "Conflito explícito de evidência" },
      "Idade da telemetria ausente",
    ],
    sourceType: "API_SUBMISSION",
    sourceReference: null,
    capturedAt: new Date("2026-10-15T12:00:00Z"),
  });
  assert.equal(result.abstained, true);
  assert.deepEqual(result.why, [
    "Qualidade da evidência não suficiente (INSUFFICIENT)",
    "Conflito explícito de evidência",
    "Idade da telemetria ausente",
  ]);
});

test("null source reference displays fallback text safely without crashing (Case D)", () => {
  const result = explainOperationalRun({
    status: "COMPLETED",
    sourceScore: 9.0,
    finalScore: 8.8,
    decision: "changed",
    candidateMetrics: { MAV: "A" },
    abstentionReasons: null,
    sourceType: "GUIDED_MANUAL_INPUT",
    sourceReference: null,
    capturedAt: new Date("2026-10-15T12:00:00Z"),
  });
  assert.ok(result.evidence.includes("Referência externa: não informada"));
  assert.ok(!result.evidence.some((e) => e.includes("null") || e.includes("undefined")));
});

test("candidate metrics filters non-primitive types safely", () => {
  const result = explainOperationalRun({
    status: "COMPLETED",
    sourceScore: 9.0,
    finalScore: 9.0,
    decision: "unchanged",
    candidateMetrics: {
      MAV: "L",
      CR: "H",
      nested: { invalid: true },
      empty: null,
    },
    abstentionReasons: null,
    sourceType: "GUIDED_MANUAL_INPUT",
    sourceReference: null,
    capturedAt: new Date("2026-10-15T12:00:00Z"),
  });
  assert.deepEqual(result.appliedMetrics, [
    ["MAV", "L"],
    ["CR", "H"],
  ]);
  assert.deepEqual(result.why, ["MAV: L", "CR: H"]);
});

test("result page renders explanation before technical metric grid", () => {
  const page = fs.readFileSync(
    path.resolve(__dirname, "../src/app/app/[organizationSlug]/assessments/[assessmentId]/runs/[runId]/page.tsx"),
    "utf8",
  );
  assert.ok(page.indexOf("<RunExplanation") < page.indexOf('className="tenant-metric-grid"'));
});

test("RunExplanation component preserves accessibility attributes and responsive styles", () => {
  const component = fs.readFileSync(
    path.resolve(__dirname, "../src/app/components/RunExplanation.tsx"),
    "utf8",
  );
  assert.match(component, /aria-labelledby="run-explanation-title"/);
  assert.match(component, /id="run-explanation-title"/);
  assert.match(component, /className="run-explanation__grid"/);

  const css = fs.readFileSync(
    path.resolve(__dirname, "../src/app/globals.css"),
    "utf8",
  );
  assert.match(css, /\.run-explanation__grid/);
  assert.match(css, /@media \(max-width: 720px\)/);
});
