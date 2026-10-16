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
  "project creation offers all 5 models, normalizes accents in automatic slugs, and preserves manually edited slugs",
  () => {
    assert.match(
      projects,
      /Começar por um modelo \(opcional\)/,
    );
    for (const model of [
      "ERP / Aplicação",
      "Portal / API",
      "Infraestrutura",
      "Serviço em nuvem",
      "Projeto geral",
    ]) {
      assert.ok(
        projects.includes(model),
        `Expected project model "${model}"`,
      );
    }
    assert.match(
      projects,
      /\.normalize\("NFD"\)/,
    );
    assert.match(
      projects,
      /if \(!slugManuallyEdited\)/,
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
  "environment creation offers all 6 common environment presets and automatic editable slugs",
  () => {
    assert.match(
      environments,
      /Tipo de ambiente \(atalho\)/,
    );
    for (const preset of [
      "Produção",
      "Homologação",
      "Desenvolvimento",
      "DMZ",
      "Rede interna",
      "Cloud / Nuvem",
    ]) {
      assert.ok(
        environments.includes(preset),
        `Expected environment preset "${preset}"`,
      );
    }
    assert.match(
      environments,
      /if \(!slugManuallyEdited\)/,
    );
    assert.match(
      environments,
      /setSlugManuallyEdited\(true\)/,
    );
  },
);

test(
  "assessment creation offers editable title and observation templates without inventing CVE",
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
      /“Avaliação” \+ CVE \+ ambiente/,
    );
    assert.match(
      assessments,
      /CVE \+ projeto \+ ambiente/,
    );
    assert.match(
      assessments,
      /Observação rápida \(opcional\)/,
    );
    assert.match(
      assessments,
      /Serviço acessível pela Internet/,
    );
    assert.match(
      assessments,
      /Somente rede interna/,
    );
    assert.match(
      assessments,
      /Ativo\/serviço crítico/,
    );
    assert.match(
      assessments,
      /Sem observação/,
    );
    assert.match(
      assessments,
      /ponto de partida e deve ser ajustado aos fatos reais/,
    );
    assert.doesNotMatch(
      assessments,
      /useState\("CVE-20/,
    );
  },
);

test(
  "evidence form offers age (0,1,3,7,30) and validity (1,7,30,90) shortcuts while preserving decimal manual numeric fields",
  () => {
    assert.match(
      runForm,
      /Idade da evidência — atalho/,
    );
    assert.match(
      runForm,
      /Coletada agora \/ hoje/,
    );
    for (const ageVal of [
      "0",
      "1",
      "3",
      "7",
      "30",
    ]) {
      assert.match(
        runForm,
        new RegExp(
          `<option value="${ageVal}">`,
        ),
      );
    }
    assert.match(
      runForm,
      /Validade máxima — atalho/,
    );
    for (const maxVal of [
      "1",
      "7",
      "30",
      "90",
    ]) {
      assert.match(
        runForm,
        new RegExp(
          `<option value="${maxVal}">`,
        ),
      );
    }
    assert.match(
      runForm,
      /id="telemetry-age"/,
    );
    assert.match(
      runForm,
      /id="telemetry-max-age"/,
    );
    assert.match(
      runForm,
      /step="0\.01"/,
    );
  },
);

test(
  "CVSS vector and provenance references remain required factual inputs rather than auto-filled templates",
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
    assert.doesNotMatch(
      runForm,
      /useState\("CVSS:4\.0/,
    );
  },
);
