import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fromVector } from "ae-cvss-calculator";
import { analyzeEnvironment } from "../src/lib/environmental-analysis-service";
import { cvssNomenclatureFromVector } from "../src/lib/cvss-presentation";

const root = path.resolve(__dirname, "..");
const form = fs.readFileSync(
  path.join(
    root,
    "src/app/app/[organizationSlug]/assessments/[assessmentId]/AssessmentRunForm.tsx",
  ),
  "utf8",
);
const route = fs.readFileSync(
  path.join(
    root,
    "src/app/api/organizations/[organizationSlug]/projects/[projectId]/environments/[environmentId]/assessments/[assessmentId]/runs/route.ts",
  ),
  "utf8",
);
const service = fs.readFileSync(
  path.join(root, "src/lib/environmental-analysis-service.ts"),
  "utf8",
);
const summary = fs.readFileSync(
  path.join(root, "src/app/components/SupplementalMetricsSummary.tsx"),
  "utf8",
);

const BASE_VECTOR =
  "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N";

test("all six Supplemental Metrics default to X", () => {
  assert.match(form, /Supplemental Metrics \(não alteram o score\)/);
  assert.match(form, /Safety \(S\)/);
  assert.match(form, /Automatable \(AU\)/);
  assert.match(form, /Recovery \(R\)/);
  assert.match(form, /Value Density \(V\)/);
  assert.match(form, /Vulnerability Response Effort \(RE\)/);
  assert.match(form, /Provider Urgency \(U\)/);
});

test("server validates allowed Supplemental Metric values", () => {
  assert.match(route, /S: \["X", "N", "P"\]/);
  assert.match(route, /AU: \["X", "N", "Y"\]/);
  assert.match(route, /R: \["X", "A", "U", "I"\]/);
  assert.match(route, /V: \["X", "D", "C"\]/);
  assert.match(route, /RE: \["X", "L", "M", "H"\]/);
  assert.match(route, /"Clear"/);
  assert.match(route, /"Green"/);
  assert.match(route, /"Amber"/);
  assert.match(route, /"Red"/);
});

test("Supplemental Metrics are not stored in candidateMetrics", () => {
  assert.match(service, /supplementalMetrics:/);
  assert.match(service, /\.\.\.candidateMetrics,\s*\.\.\.supplementalMetrics/);
  assert.doesNotMatch(service, /candidateMetrics\.S\s*=/);
  assert.doesNotMatch(service, /candidateMetrics\.AU\s*=/);
  assert.doesNotMatch(service, /candidateMetrics\.R\s*=/);
  assert.doesNotMatch(service, /candidateMetrics\.V\s*=/);
  assert.doesNotMatch(service, /candidateMetrics\.RE\s*=/);
  assert.doesNotMatch(service, /candidateMetrics\.U\s*=/);
});

test("Supplemental Metrics participate in vector enrichment", () => {
  assert.match(service, /"S",\s*"AU",\s*"R",\s*"V",\s*"RE",\s*"U"/);
});

test("result summary explicitly says Supplemental Metrics do not alter score", () => {
  assert.match(summary, /não\s+alteram o score CVSS numérico/);
  assert.match(summary, /value !== "X"/);
});

test("Score invariance: Safety (S:P)", () => {
  const baseScore = fromVector(BASE_VECTOR).calculateOverallScore();
  const withSafety = fromVector(`${BASE_VECTOR}/S:P`).calculateOverallScore();
  assert.strictEqual(withSafety, baseScore);
});

test("Score invariance: Automatable (AU:Y)", () => {
  const baseScore = fromVector(BASE_VECTOR).calculateOverallScore();
  const withAutomatable = fromVector(
    `${BASE_VECTOR}/AU:Y`,
  ).calculateOverallScore();
  assert.strictEqual(withAutomatable, baseScore);
});

test("Score invariance: Recovery (R:I)", () => {
  const baseScore = fromVector(BASE_VECTOR).calculateOverallScore();
  const withRecovery = fromVector(`${BASE_VECTOR}/R:I`).calculateOverallScore();
  assert.strictEqual(withRecovery, baseScore);
});

test("Score invariance: Value Density (V:C)", () => {
  const baseScore = fromVector(BASE_VECTOR).calculateOverallScore();
  const withValueDensity = fromVector(
    `${BASE_VECTOR}/V:C`,
  ).calculateOverallScore();
  assert.strictEqual(withValueDensity, baseScore);
});

test("Score invariance: Response Effort (RE:H)", () => {
  const baseScore = fromVector(BASE_VECTOR).calculateOverallScore();
  const withEffort = fromVector(`${BASE_VECTOR}/RE:H`).calculateOverallScore();
  assert.strictEqual(withEffort, baseScore);
});

test("Score invariance: Provider Urgency (U:Red)", () => {
  const baseScore = fromVector(BASE_VECTOR).calculateOverallScore();
  const withUrgency = fromVector(
    `${BASE_VECTOR}/U:Red`,
  ).calculateOverallScore();
  assert.strictEqual(withUrgency, baseScore);
});

test("Score invariance: all six Supplemental Metrics together", () => {
  const baseScore = fromVector(BASE_VECTOR).calculateOverallScore();
  const fullSupplementalVector = `${BASE_VECTOR}/S:P/AU:Y/R:I/V:C/RE:H/U:Red`;
  const allScore = fromVector(fullSupplementalVector).calculateOverallScore();
  assert.strictEqual(allScore, baseScore);
  assert.notStrictEqual(fullSupplementalVector, BASE_VECTOR);
});

test("Score invariance: Threat + Environmental + Supplemental (BTE)", () => {
  const bteVector = `${BASE_VECTOR}/E:P/CR:H/IR:M/AR:L/MAV:N`;
  const bteWithSupplemental = `${bteVector}/S:P/AU:Y/R:I/V:C/RE:H/U:Red`;

  const scoreBte = fromVector(bteVector).calculateOverallScore();
  const scoreBteSupp = fromVector(bteWithSupplemental).calculateOverallScore();

  assert.strictEqual(scoreBteSupp, scoreBte);
  assert.strictEqual(
    fromVector(bteWithSupplemental).getNomenclature(),
    "CVSS-BTE",
  );
  assert.strictEqual(
    cvssNomenclatureFromVector(bteWithSupplemental),
    "CVSS-BTE",
  );
});

test("All-X Supplemental Metrics do not emit supplemental segments", () => {
  const result = analyzeEnvironment({
    cveId: "CVE-2026-9101",
    baseVector: BASE_VECTOR,
    sourceAssessmentMeta: { provider: "NVD" },
    evidence: {
      reachability: "INTERNAL_ROUTED",
      evidenceQuality: "SUFFICIENT",
      telemetryAgeDays: 0.1,
      supplementalMetrics: {
        S: "X",
        AU: "X",
        R: "X",
        V: "X",
        RE: "X",
        U: "X",
      },
    },
  });

  assert.strictEqual("status" in result.environmentalAssessment, false);
  if (!("status" in result.environmentalAssessment)) {
    assert.doesNotMatch(result.environmentalAssessment.vector, /\/S:/);
    assert.doesNotMatch(result.environmentalAssessment.vector, /\/AU:/);
    assert.doesNotMatch(result.environmentalAssessment.vector, /\/R:/);
    assert.doesNotMatch(result.environmentalAssessment.vector, /\/V:/);
    assert.doesNotMatch(result.environmentalAssessment.vector, /\/RE:/);
    assert.doesNotMatch(result.environmentalAssessment.vector, /\/U:/);
    assert.strictEqual(result.environmentalAssessment.nomenclature, "CVSS-BE");
  }
});

test("Supplemental Metrics are enriched in canonical order and excluded from candidateMetrics", () => {
  const result = analyzeEnvironment({
    cveId: "CVE-2026-9102",
    baseVector: BASE_VECTOR,
    sourceAssessmentMeta: { provider: "NVD" },
    evidence: {
      reachability: "INTERNAL_ROUTED",
      evidenceQuality: "SUFFICIENT",
      telemetryAgeDays: 0.1,
      supplementalMetrics: {
        S: "P",
        AU: "Y",
        R: "I",
        V: "C",
        RE: "H",
        U: "Red",
      },
    },
  });

  assert.strictEqual("status" in result.environmentalAssessment, false);
  if (!("status" in result.environmentalAssessment)) {
    const vector = result.environmentalAssessment.vector;
    assert.match(vector, /\/MAV:N\/S:P\/AU:Y\/R:I\/V:C\/RE:H\/U:Red/);
  }

  // Verify none of the supplemental metrics are present in candidateMetrics
  const candidates = result.inferenceAnalysis.candidateMetrics;
  assert.strictEqual(candidates.S, undefined);
  assert.strictEqual(candidates.AU, undefined);
  assert.strictEqual(candidates.R, undefined);
  assert.strictEqual(candidates.V, undefined);
  assert.strictEqual(candidates.RE, undefined);
  assert.strictEqual(candidates.U, undefined);
});

test("ABSTAIN is preserved: Supplemental Metrics do not cure environmental deficiencies", () => {
  const result = analyzeEnvironment({
    cveId: "CVE-2026-9103",
    baseVector: BASE_VECTOR,
    sourceAssessmentMeta: { provider: "NVD" },
    evidence: {
      reachability: "UNKNOWN", // Triggers ABSTAIN
      evidenceQuality: "SUFFICIENT",
      telemetryAgeDays: 0.1,
      supplementalMetrics: {
        S: "P",
        AU: "Y",
        R: "I",
      },
    },
  });

  assert.ok(
    "status" in result.environmentalAssessment &&
      result.environmentalAssessment.status === "ABSTAINED",
  );
  assert.ok(
    result.inferenceAnalysis.abstentionReasons.some((r) =>
      r.includes("Classe de reachability"),
    ),
  );
});

test("Audit receipt digest incorporates supplemental metrics", () => {
  const withoutSupp = analyzeEnvironment({
    cveId: "CVE-2026-9104",
    baseVector: BASE_VECTOR,
    sourceAssessmentMeta: { provider: "NVD" },
    evidence: {
      reachability: "INTERNAL_ROUTED",
      evidenceQuality: "SUFFICIENT",
      telemetryAgeDays: 0.1,
    },
  });

  const withSupp = analyzeEnvironment({
    cveId: "CVE-2026-9104",
    baseVector: BASE_VECTOR,
    sourceAssessmentMeta: { provider: "NVD" },
    evidence: {
      reachability: "INTERNAL_ROUTED",
      evidenceQuality: "SUFFICIENT",
      telemetryAgeDays: 0.1,
      supplementalMetrics: {
        S: "P",
      },
    },
  });

  assert.notStrictEqual(
    withoutSupp.auditReceipt.receiptDigest,
    withSupp.auditReceipt.receiptDigest,
  );
});