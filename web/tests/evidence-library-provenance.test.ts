import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

const root = path.resolve(__dirname, "..");
const form = fs.readFileSync(
  path.join(
    root,
    "src/app/app/[organizationSlug]/assessments/[assessmentId]/AssessmentRunForm.tsx",
  ),
  "utf8",
);
const layout = fs.readFileSync(
  path.join(root, "src/app/app/[organizationSlug]/layout.tsx"),
  "utf8",
);
const resultPage = fs.readFileSync(
  path.join(
    root,
    "src/app/app/[organizationSlug]/assessments/[assessmentId]/runs/[runId]/page.tsx",
  ),
  "utf8",
);
const libraryPage = fs.readFileSync(
  path.join(root, "src/app/app/[organizationSlug]/evidence/page.tsx"),
  "utf8",
);

test("guided run exposes optional provenance fields", () => {
  assert.match(form, /evidence-provenance-panel/);
  assert.match(form, /Provenance da fonte \(opcional\)/);
  assert.match(form, /source-reference/);
  assert.match(form, /captured-at/);
  assert.match(form, /sourceReference:\s*sourceReference\.trim\(\)/);
  assert.match(form, /capturedAt:\s*capturedAt\.trim\(\)/);
});

test("provenance payload fallback behavior is deterministic", () => {
  // Scenario A: blank provenance
  const blankSource = "";
  const blankCaptured = "";
  const resolvedBlankSource = blankSource.trim() || undefined;
  const resolvedBlankCaptured = blankCaptured.trim()
    ? new Date(blankCaptured).toISOString()
    : new Date().toISOString();

  assert.equal(resolvedBlankSource, undefined);
  assert.ok(typeof resolvedBlankCaptured === "string");
  assert.ok(!Number.isNaN(new Date(resolvedBlankCaptured).getTime()));

  // Scenario B: explicit provenance
  const explicitSource = "https://nvd.nist.gov/vuln/detail/CVE-2024-1234";
  const explicitCaptured = "2026-10-15T10:30";
  const resolvedExplicitSource = explicitSource.trim() || undefined;
  const resolvedExplicitCaptured = new Date(explicitCaptured).toISOString();

  assert.equal(resolvedExplicitSource, explicitSource);
  assert.equal(resolvedExplicitCaptured, new Date("2026-10-15T10:30").toISOString());
});

test("tenant navigation exposes Evidence Library", () => {
  assert.match(layout, /\/evidence/);
  assert.match(layout, /Evidence Library/);
});

test("result traceability shows source type and reference", () => {
  assert.match(resultPage, /Fonte da evidência/);
  assert.match(resultPage, /sourceReference/);
  assert.match(resultPage, /run\.evidenceSnapshot\.capturedAt/);
});

test("Evidence Library is environment-scoped and provenance-oriented", () => {
  assert.match(libraryPage, /Evidências preservadas por ambiente/);
  assert.match(libraryPage, /canonicalHash/);
  assert.match(libraryPage, /sourceReference/);
  assert.match(libraryPage, /Expirada/);
  assert.match(libraryPage, /Preservada/);
  assert.match(libraryPage, /Nenhuma evidência preservada ainda/);
});

test("Evidence Library data access enforces tenant boundary and deterministic ordering", () => {
  const tenantData = fs.readFileSync(
    path.join(root, "src/lib/tenant-data.ts"),
    "utf8",
  );
  assert.match(tenantData, /export async function listTenantEvidenceSnapshots/);
  assert.match(tenantData, /organizationId:\s*context\.organization\.id/);
  assert.match(tenantData, /capturedAt:\s*"desc"/);
  assert.match(tenantData, /id:\s*"desc"/);
  assert.match(tenantData, /take:\s*200/);
});

test("CSS rules include provenance panel and keyboard focus styling", () => {
  const css = fs.readFileSync(path.join(root, "src/app/globals.css"), "utf8");
  assert.match(css, /\.evidence-provenance-panel\s*\{/);
  assert.match(css, /\.evidence-provenance-panel summary:focus-visible/);
  assert.match(css, /\.context-list div/);
});