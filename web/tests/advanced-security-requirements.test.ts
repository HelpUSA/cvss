import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

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
const page = fs.readFileSync(
  path.join(
    root,
    "src/app/app/[organizationSlug]/assessments/[assessmentId]/page.tsx",
  ),
  "utf8",
);
const tenantData = fs.readFileSync(
  path.join(root, "src/lib/tenant-data.ts"),
  "utf8",
);
const route = fs.readFileSync(
  path.join(
    root,
    "src/app/api/organizations/[organizationSlug]/projects/[projectId]/environments/[environmentId]/assessments/[assessmentId]/runs/route.ts",
  ),
  "utf8",
);
const css = fs.readFileSync(path.join(root, "src/app/globals.css"), "utf8");

test("advanced CR IR AR inputs default to X and remain optional (Case A)", () => {
  assert.match(form, /useState\("X"\)/);
  assert.match(form, /X — Não definido/);
  assert.match(form, /Requisitos de Segurança do ambiente \(avançado\)/);
});

test("non-X CR IR AR requires an active organization policy client-side (Case B)", () => {
  assert.match(form, /securityRequirementsUsed/);
  assert.match(
    form,
    /Selecione uma política organizacional ativa antes de definir CR\/IR\/AR/,
  );
});

test("payload sends security requirements only when governed by selected policy (Case C)", () => {
  assert.match(form, /organizationPolicyId:/);
  assert.match(form, /policyVersion:/);
  assert.match(form, /securityRequirements:/);
  assert.match(form, /CR: cr/);
  assert.match(form, /IR: ir/);
  assert.match(form, /AR: ar/);
});

test("active policy options are tenant-scoped and active only", () => {
  assert.match(tenantData, /listActiveTenantPolicyVersions/);
  assert.match(tenantData, /organizationId:\s*context\.organization\.id/);
  assert.match(tenantData, /status:\s*"ACTIVE"/);
  assert.match(page, /activePolicyOptions/);
});

test("server-side route validates active tenant policy and rejects inactive or foreign policies (Cases D & E)", () => {
  assert.match(route, /organizationPolicyVersion\.findFirst/);
  assert.match(route, /organizationId:\s*context\.organization\.id/);
  assert.match(route, /policyId,/);
  assert.match(route, /status:\s*"ACTIVE"/);
  assert.match(
    route,
    /Política organizacional não encontrada ou inativa para esta organização\./,
  );
  assert.match(
    route,
    /Política organizacional e versão são obrigatórias para definir requisitos de segurança\./,
  );
});

test("governed CR IR AR produces expected candidate metrics in analyzeEnvironment", () => {
  const analysis = analyzeEnvironment({
    cveId: "CVE-2024-1000",
    baseVector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    sourceAssessmentMeta: { provider: "CNA_PUBLISHED" },
    evidence: {
      reachability: "INTERNAL_ROUTED",
      evidenceQuality: "SUFFICIENT",
      telemetryAgeDays: 0.5,
      maxTelemetryAgeDays: 1.0,
      telemetryProfile: "production",
      organizationPolicyId: "pol-prod-001",
      policyVersion: "1.0",
      securityRequirements: {
        CR: "H",
        IR: "M",
        AR: "L",
      },
    },
  });

  assert.equal(analysis.inferenceAnalysis.candidateMetrics.CR, "H");
  assert.equal(analysis.inferenceAnalysis.candidateMetrics.IR, "M");
  assert.equal(analysis.inferenceAnalysis.candidateMetrics.AR, "L");

  // Environmental assessment completed
  assert.ok(!("status" in analysis.environmentalAssessment));
  const nomenclature = cvssNomenclatureFromVector(analysis.environmentalAssessment.vector);
  assert.equal(nomenclature, "CVSS-BE");
});

test("all-X with policy does not promote candidate metrics or force environmental nomenclature", () => {
  const analysis = analyzeEnvironment({
    cveId: "CVE-2024-1000",
    baseVector: "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
    sourceAssessmentMeta: { provider: "CNA_PUBLISHED" },
    evidence: {
      reachability: "UNKNOWN",
      evidenceQuality: "UNKNOWN",
      organizationPolicyId: "pol-prod-001",
      policyVersion: "1.0",
      securityRequirements: {
        CR: "X",
        IR: "X",
        AR: "X",
      },
    },
  });

  assert.equal(analysis.inferenceAnalysis.candidateMetrics.CR, undefined);
  assert.equal(analysis.inferenceAnalysis.candidateMetrics.IR, undefined);
  assert.equal(analysis.inferenceAnalysis.candidateMetrics.AR, undefined);
});

test("advanced help preserves correct semantic boundary", () => {
  assert.match(form, /criticidade\s+do sistema vulnerável/);
  assert.match(form, /não a\s+vulnerabilidade em si/);
  assert.match(form, /não\s+deve ser usada para compensar controles/);
});

test("CSS rules include responsive grid layout for security requirements", () => {
  assert.match(css, /\.advanced-security-requirements__grid/);
  assert.match(css, /grid-template-columns:\s*repeat\(3,\s*minmax\(0,\s*1fr\)\)/);
  assert.match(css, /@media\s*\(max-width:\s*760px\)/);
});