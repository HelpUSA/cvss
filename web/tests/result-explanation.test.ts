import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

import { explainOperationalRun } from "../src/lib/run-explanation";

test("completed run explains score change and applied metrics", () => {
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
  assert.match(result.whatChanged, /9\.8/);
  assert.match(result.whatChanged, /9\.3/);
  assert.ok(result.why.includes("MAV: N"));
  assert.ok(result.why.includes("CR: H"));
});

test("abstained run explains unresolved evidence instead of inventing cause", () => {
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
  assert.match(result.whatChanged, /Nenhuma afirmação ambiental final/);
  assert.deepEqual(result.unresolved, ["Idade da telemetria ausente", "Reachability desconhecida"]);
  assert.match(result.nextAction, /Revise as evidências/);
});

test("result page renders explanation before technical metric grid", () => {
  const page = fs.readFileSync(
    path.resolve(__dirname, "../src/app/app/[organizationSlug]/assessments/[assessmentId]/runs/[runId]/page.tsx"),
    "utf8",
  );
  assert.ok(page.indexOf("<RunExplanation") < page.indexOf('className="tenant-metric-grid"'));
});
