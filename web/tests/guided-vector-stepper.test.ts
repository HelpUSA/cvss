import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

import { validateCvss40VectorInput } from "../src/lib/cvss-vector-validation";

const validBase = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N";

test("valid Base vector is accepted and classified as CVSS-B", () => {
  const result = validateCvss40VectorInput(validBase);
  assert.equal(result.valid, true);
  assert.equal(result.nomenclature, "CVSS-B");
});

test("Threat and Environmental metrics update nomenclature", () => {
  assert.equal(validateCvss40VectorInput(`${validBase}/E:P`).nomenclature, "CVSS-BT");
  assert.equal(validateCvss40VectorInput(`${validBase}/CR:H`).nomenclature, "CVSS-BE");
  assert.equal(validateCvss40VectorInput(`${validBase}/E:A/CR:H`).nomenclature, "CVSS-BTE");
});

test("missing mandatory Base metrics are rejected", () => {
  const result = validateCvss40VectorInput("CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N");
  assert.equal(result.valid, false);
  assert.ok(result.errors.some((item) => item.includes("VC")));
});

test("duplicate, unknown and invalid values are rejected", () => {
  const duplicate = validateCvss40VectorInput(`${validBase}/AV:A`);
  assert.equal(duplicate.valid, false);
  assert.ok(duplicate.errors.some((item) => item.includes("duplicada")));

  const unknown = validateCvss40VectorInput(`${validBase}/ZZ:H`);
  assert.equal(unknown.valid, false);
  assert.ok(unknown.errors.some((item) => item.includes("desconhecida")));

  const badValue = validateCvss40VectorInput(validBase.replace("/AC:L", "/AC:X"));
  assert.equal(badValue.valid, false);
  assert.ok(badValue.errors.some((item) => item.includes("Valor inválido")));
});

test("assessment form allows telemetry age to remain unknown", () => {
  const formPath = path.resolve(__dirname, "../src/app/app/[organizationSlug]/assessments/[assessmentId]/AssessmentRunForm.tsx");
  const source = fs.readFileSync(formPath, "utf8");
  const telemetryBlock = source.slice(source.indexOf('id="telemetry-age"'), source.indexOf('id="telemetry-max-age"'));
  assert.doesNotMatch(telemetryBlock, /required/);
  assert.match(source, /telemetryAgeDays\.trim\(\) === ""\s*\? null/);
});

test("all five workflow pages render the shared stepper", () => {
  const paths = [
    "../src/app/app/[organizationSlug]/projects/page.tsx",
    "../src/app/app/[organizationSlug]/environments/page.tsx",
    "../src/app/app/[organizationSlug]/assessments/page.tsx",
    "../src/app/app/[organizationSlug]/assessments/[assessmentId]/page.tsx",
    "../src/app/app/[organizationSlug]/assessments/[assessmentId]/runs/[runId]/page.tsx",
  ];
  paths.forEach((relativePath, index) => {
    const source = fs.readFileSync(path.resolve(__dirname, relativePath), "utf8");
    const expected = "GuidedWorkflowStepper currentStep={" + (index + 1) + "}";
    assert.ok(source.includes(expected), expected);
  });
});
