import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

const root = path.resolve(__dirname, "..");

function read(relativePath: string): string {
  return fs.readFileSync(
    path.join(root, relativePath),
    "utf8",
  );
}

const projects = read(
  "src/app/app/[organizationSlug]/projects/ProjectCreateForm.tsx",
);
const environments = read(
  "src/app/app/[organizationSlug]/environments/EnvironmentCreateForm.tsx",
);
const assessments = read(
  "src/app/app/[organizationSlug]/assessments/AssessmentCreateForm.tsx",
);
const runForm = read(
  "src/app/app/[organizationSlug]/assessments/[assessmentId]/AssessmentRunForm.tsx",
);

test(
  "project creation offers models and keeps generated slug editable",
  () => {
    assert.match(
      projects,
      /Começar por um modelo/,
    );
    assert.match(
      projects,
      /slugify\(nextName\)/,
    );
    assert.match(
      projects,
      /setSlugManuallyEdited\(true\)/,
    );
  },
);

test(
  "environment creation offers common environment presets",
  () => {
    assert.match(
      environments,
      /Tipo de ambiente \(atalho\)/,
    );
    assert.match(
      environments,
      /Produção/,
    );
    assert.match(
      environments,
      /Homologação/,
    );
    assert.match(
      environments,
      /Cloud \/ Nuvem/,
    );
  },
);

test(
  "assessment creation offers editable title and observation templates",
  () => {
    assert.match(
      assessments,
      /Modelo de nome \(opcional\)/,
    );
    assert.match(
      assessments,
      /CV[E|e] \+ ambiente/,
    );
    assert.match(
      assessments,
      /Observação rápida \(opcional\)/,
    );
    assert.match(
      assessments,
      /ponto de partida e deve ser ajustado aos fatos reais/,
    );
  },
);

test(
  "evidence form offers age and validity shortcuts but preserves manual numeric fields",
  () => {
    assert.match(
      runForm,
      /Idade da evidência — atalho/,
    );
    assert.match(
      runForm,
      /Validade máxima — atalho/,
    );
    assert.match(
      runForm,
      /id="telemetry-age"/,
    );
    assert.match(
      runForm,
      /id="telemetry-max-age"/,
    );
  },
);

test(
  "CVSS vector remains a required factual input rather than an auto-filled template",
  () => {
    assert.match(
      runForm,
      /Vetor CVSS v4\.0 de origem/,
    );
    assert.match(
      runForm,
      /id="base-vector"/,
    );
    assert.doesNotMatch(
      runForm,
      /setBaseVector\("CVSS:4\.0/,
    );
  },
);
