import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

const root = path.resolve(__dirname, "..");
const formPath = path.join(
  root,
  "src/app/app/[organizationSlug]/assessments/[assessmentId]/AssessmentRunForm.tsx",
);
const helpPath = path.join(
  root,
  "src/app/components/CvssEvidenceHelp.tsx",
);

test("guided evidence form defaults unknown facts to unknown", () => {
  const source = fs.readFileSync(formPath, "utf8");

  assert.match(source, /useState\("UNKNOWN"\)/);
  assert.match(source, /value="UNKNOWN">\s*Ainda não avaliei/);
  assert.doesNotMatch(
    source,
    /useState\("INTERNAL_ROUTED"\)/,
  );
  assert.doesNotMatch(
    source,
    /useState\("SUFFICIENT"\)/,
  );
});

test("telemetry age is not silently submitted as zero when unanswered", () => {
  const source = fs.readFileSync(formPath, "utf8");

  assert.match(
    source,
    /telemetryAgeDays\.trim\(\) === ""\s*\? null/,
  );
});

test("inline evidence help explicitly preserves unknown state and ABSTAIN semantics", () => {
  const source = fs.readFileSync(helpPath, "utf8");

  assert.match(
    source,
    /desconhecido deve permanecer desconhecido/i,
  );
  assert.match(source, /ABSTAIN não é erro de cálculo/i);
  assert.match(source, /Não altere o vetor Base/i);
});
