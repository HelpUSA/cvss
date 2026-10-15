import {
  expect,
  test,
} from "@playwright/test";

import {
  assertAdvancedClosed,
  assertNoHorizontalOverflow,
  BASE_VECTOR,
  hasAuthenticatedStorage,
  requiredEnv,
  runSuffix,
} from "./helpers";

test.describe.configure({
  mode: "serial",
});

test.describe(
  "advanced governed CVSS journey",
  () => {
    const organizationSlug =
      requiredEnv(
        "E2E_ORGANIZATION_SLUG",
        "e2e-org",
      );

    const activePolicyLabel =
      process.env
        .E2E_ACTIVE_POLICY_LABEL
        ?.trim() ||
      (process.env.E2E_SYNTHETIC_AUTH === "1"
        ? "E2E-CVSS-ENV · v1"
        : undefined);

    const suffix = runSuffix();

    test(
      "operator can produce a governed BTE result and preserve Supplemental context",
      async ({ page }, testInfo) => {
        test.skip(
          !hasAuthenticatedStorage(),
          "Authenticated storageState required. Generate via: npx playwright codegen --save-storage=playwright/.auth/user.json",
        );

        test.skip(
          !activePolicyLabel,
          "E2E_ACTIVE_POLICY_LABEL is required for governed CR/IR/AR",
        );

        const viewportKey =
          testInfo.project.name;

        const projectName =
          `E2E advanced ${viewportKey} ${suffix}`;

        const environmentName =
          `Advanced env ${viewportKey} ${suffix}`;

        await page.goto(
          `/app/${organizationSlug}/projects`,
        );

        await page
          .getByLabel("Nome do projeto")
          .fill(projectName);

        await page
          .getByLabel("Slug")
          .fill(
            `e2e-advanced-${viewportKey}-${suffix}`
              .toLowerCase(),
          );

        await page
          .getByRole("button", {
            name: "Criar projeto",
          })
          .click();

        await expect(
          page.getByText(
            "Projeto criado com sucesso.",
          ),
        ).toBeVisible();

        await page.goto(
          `/app/${organizationSlug}/environments`,
        );

        await page
          .getByLabel("Projeto")
          .selectOption({
            label: projectName,
          });

        await page
          .getByLabel("Nome do ambiente")
          .fill(environmentName);

        await page
          .getByLabel("Slug")
          .fill(
            `advanced-${viewportKey}-${suffix}`
              .toLowerCase(),
          );

        await page
          .getByRole("button", {
            name: "Criar ambiente",
          })
          .click();

        await expect(
          page.getByText(
            "Ambiente criado com sucesso.",
          ),
        ).toBeVisible();

        await page.goto(
          `/app/${organizationSlug}/assessments`,
        );

        await page
          .getByLabel("Ambiente")
          .selectOption({
            label:
              `${projectName} / ${environmentName}`,
          });

        await page
          .getByLabel("CVE")
          .fill("CVE-2026-54321");

        await page
          .getByLabel("Nome da avaliação")
          .fill(
            `Advanced BTE ${viewportKey} ${suffix}`,
          );

        await page
          .getByRole("button", {
            name:
              "Criar e continuar para evidências",
          })
          .click();

        await assertAdvancedClosed(page);

        await page
          .getByLabel(
            "Vetor CVSS v4.0 de origem",
          )
          .fill(BASE_VECTOR);

        await page
          .getByLabel(
            /Como o sistema vulnerável pode ser alcançado/i,
          )
          .selectOption(
            "INTERNAL_ROUTED",
          );

        await page
          .getByLabel(
            "Qualidade da evidência",
          )
          .selectOption("SUFFICIENT");

        await page
          .getByLabel(
            "Idade da evidência (dias)",
          )
          .fill("0");

        await page
          .getByText(
            "Threat — Exploit Maturity (E) (avançado)",
            { exact: true },
          )
          .click();

        await page
          .getByLabel(
            "Exploit Maturity (E)",
          )
          .selectOption("P");

        await page
          .getByLabel(
            "Referência de threat intelligence",
          )
          .fill(
            "E2E-THREAT-INTEL-POC",
          );

        const observedAt =
          new Date(
            Date.now() - 60_000,
          )
            .toISOString()
            .slice(0, 16);

        await page
          .getByLabel("Observada em")
          .fill(observedAt);

        await page
          .getByText(
            "Requisitos de Segurança do ambiente (avançado)",
            { exact: true },
          )
          .click();

        await page
          .getByLabel(
            "Política organizacional",
          )
          .selectOption({
            label:
              activePolicyLabel!,
          });

        await page
          .getByLabel(
            "Confidencialidade (CR)",
          )
          .selectOption("H");

        await page
          .getByLabel(
            "Integridade (IR)",
          )
          .selectOption("M");

        await page
          .getByLabel(
            "Disponibilidade (AR)",
          )
          .selectOption("L");

        await page
          .getByText(
            "Supplemental Metrics (não alteram o score)",
            { exact: true },
          )
          .click();

        await page
          .getByLabel("Safety (S)")
          .selectOption("P");

        await page
          .getByLabel(
            "Automatable (AU)",
          )
          .selectOption("Y");

        await page
          .getByLabel(
            "Provider Urgency (U)",
          )
          .selectOption("Amber");

        await page
          .getByRole("button", {
            name:
              "Executar e ver resultado",
          })
          .click();

        await expect(
          page.getByRole("heading", {
            name:
              "Resultado da avaliação",
          }),
        ).toBeVisible();

        await expect(
          page.getByText("CVSS-BTE"),
        ).toBeVisible();

        await expect(
          page.getByRole("heading", {
            name:
              "Supplemental Metrics",
          }),
        ).toBeVisible();

        await expect(
          page.getByText(
            /não alteram o score CVSS numérico/i,
          ),
        ).toBeVisible();

        await assertNoHorizontalOverflow(
          page,
        );
      },
    );
  },
);
