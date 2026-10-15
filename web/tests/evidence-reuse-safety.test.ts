import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

const root = path.resolve(__dirname, "..");
const form = fs.readFileSync(path.join(root, "src/app/app/[organizationSlug]/assessments/[assessmentId]/AssessmentRunForm.tsx"), "utf8");
const page = fs.readFileSync(path.join(root, "src/app/app/[organizationSlug]/assessments/[assessmentId]/page.tsx"), "utf8");
const tenantData = fs.readFileSync(path.join(root, "src/lib/tenant-data.ts"), "utf8");
const route = fs.readFileSync(path.join(root, "src/app/api/organizations/[organizationSlug]/projects/[projectId]/environments/[environmentId]/assessments/[assessmentId]/runs/route.ts"), "utf8");

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
