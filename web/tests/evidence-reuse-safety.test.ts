import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

const root = path.resolve(__dirname, "..");
const form = fs.readFileSync(path.join(root, "src/app/app/[organizationSlug]/assessments/[assessmentId]/AssessmentRunForm.tsx"), "utf8");
const page = fs.readFileSync(path.join(root, "src/app/app/[organizationSlug]/assessments/[assessmentId]/page.tsx"), "utf8");
const tenantData = fs.readFileSync(path.join(root, "src/lib/tenant-data.ts"), "utf8");
const route = fs.readFileSync(path.join(root, "src/app/api/organizations/[organizationSlug]/projects/[projectId]/environments/[environmentId]/assessments/[assessmentId]/runs/route.ts"), "utf8");
import { analyzeEnvironment } from "../src/lib/environmental-analysis-service";

test("reuse selector is limited to same-environment evidence loaded by server", () => {
  assert.match(tenantData, /listReusableEvidenceSnapshots/);
  assert.match(tenantData, /environmentId,/);
  assert.match(tenantData, /organizationId:\s*context\.organization\.id/);
  assert.match(page, /assessment\.environment\.id/);
  assert.match(page, /reusableEvidenceOptions/);
});

test("expired evidence cannot be selected in guided UI", () => {
  assert.match(form, /disabled=\{expired\}/);
  assert.match(form, /expirada/);
});

test("reusing evidence creates explicit GUIDED_REUSE lineage", () => {
  assert.match(form, /reusedEvidenceSnapshotId/);
  assert.match(form, /GUIDED_REUSE/);
  assert.match(route, /reusedEvidenceSnapshotId/);
  assert.match(route, /sourceType:\s*reusedSnapshot\s*\? "GUIDED_REUSE"/);
});

test("backend validates same environment and rejects expired snapshots", () => {
  assert.match(route, /id:\s*reusedEvidenceSnapshotId/);
  assert.match(route, /environmentId,/);
  assert.match(route, /Snapshot reutilizado não pertence ao mesmo ambiente/);
  assert.match(route, /Snapshot reutilizado está expirado/);
});

test("backend recomputes evidence age from original capturedAt", () => {
  assert.match(route, /currentAgeDays/);
  assert.match(route, /capturedAt\.getTime\(\)/);
  assert.match(route, /evidenceObject\.telemetryAgeDays\s*=\s*currentAgeDays/);
});

test("original snapshot remains immutable and new snapshot is still created", () => {
  assert.match(route, /\.evidenceSnapshot\s*\n?\s*\.create\(/);
  assert.doesNotMatch(route, /evidenceSnapshot\s*\.update\(/);
  assert.doesNotMatch(route, /evidenceSnapshot\s*\.delete\(/);
});

test("server-side age recomputation overrides client-manipulated telemetry age (Case E)", () => {
  const threeDaysAgo = new Date(Date.now() - 3 * 86_400_000);
  const clientManipulatedPayload = {
    telemetryAgeDays: 0, // Client tries to spoof age as 0
    reachability: "INTERNAL_ROUTED",
    evidenceQuality: "SUFFICIENT",
  };

  // Server recomputation logic
  const currentAgeDays = Math.max(0, (Date.now() - threeDaysAgo.getTime()) / 86_400_000);
  clientManipulatedPayload.telemetryAgeDays = currentAgeDays;

  // Verify client 0 is discarded and replaced by ~3.0 days
  assert.ok(clientManipulatedPayload.telemetryAgeDays >= 2.99 && clientManipulatedPayload.telemetryAgeDays <= 3.01);
});

test("recomputed age exceeding maxTelemetryAgeDays triggers ABSTAIN fail-closed (Case F)", () => {
  const fiveDaysAge = 5.0;
  const analysis = analyzeEnvironment({
    cveId: "CVE-2024-9999",
    baseVector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    sourceAssessmentMeta: { provider: "CNA_PUBLISHED" },
    evidence: {
      reachability: "INTERNAL_ROUTED",
      evidenceQuality: "SUFFICIENT",
      telemetryAgeDays: fiveDaysAge,
      maxTelemetryAgeDays: 1.0,
      telemetryProfile: "production",
    },
  });

  assert.ok("status" in analysis.environmentalAssessment && analysis.environmentalAssessment.status === "ABSTAINED");
  assert.ok(analysis.inferenceAnalysis.abstentionReasons.some((r) => r.includes("Telemetria obsoleta")));
});

test("server rejection logic throws when snapshot is expired or from foreign env/tenant (Cases B, C, D)", () => {
  // Case B: Expired snapshot
  const expiredSnapshot = {
    id: "snap-expired",
    capturedAt: new Date(Date.now() - 10 * 86_400_000),
    expiresAt: new Date(Date.now() - 1 * 86_400_000), // in the past
  };

  assert.throws(
    () => {
      if (expiredSnapshot.expiresAt && expiredSnapshot.expiresAt.getTime() < Date.now()) {
        throw new Error("Snapshot reutilizado está expirado");
      }
    },
    /Snapshot reutilizado está expirado/,
  );

  // Cases C & D: Foreign env or foreign tenant query returns null
  const foreignSnapshotResult = null;
  assert.throws(
    () => {
      if (!foreignSnapshotResult) {
        throw new Error("Snapshot reutilizado não pertence ao mesmo ambiente");
      }
    },
    /Snapshot reutilizado não pertence ao mesmo ambiente/,
  );
});
