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
  "synthetic operator journey",
  () => {
    const organizationSlug =
      requiredEnv(
        "E2E_ORGANIZATION_SLUG",
        "e2e-org",
      );

    const suffix = runSuffix();

    let projectName = "";
    let environmentName = "";
    let assessmentTitle = "";
    let assessmentUrl = "";

    test.beforeEach(async ({ page }) => {
      test.skip(
        !hasAuthenticatedStorage(),
        "Authenticated storageState required. Generate via: npx playwright codegen --save-storage=playwright/.auth/user.json",
      );

      await page.goto(
        `/app/${organizationSlug}/guide`,
      );

      await expect(
        page.getByRole("heading", {
          name: /Roteiro operacional em 5 etapas/i,
        }),
      ).toBeVisible();
    });

    test(
      "new operator completes the basic 1-to-5 flow without opening advanced CVSS controls",
      async ({ page }, testInfo) => {
        const viewportKey =
          testInfo.project.name;

        const attemptSuffix =
          testInfo.retry > 0
            ? `${suffix}-r${testInfo.retry}`
            : suffix;

        projectName =
          `E2E ${viewportKey} ${attemptSuffix}`;
        environmentName =
          `Produção E2E ${viewportKey} ${attemptSuffix}`;
        assessmentTitle =
          `CVE E2E ${viewportKey} ${attemptSuffix}`;

        await test.step(
          "Step 1 — create project",
          async () => {
            await page.goto(
              `/app/${organizationSlug}/projects`,
            );

            await page
              .getByLabel("Nome do projeto")
              .fill(projectName);

            await page
              .getByLabel("Slug")
              .fill(
                `e2e-${viewportKey}-${attemptSuffix}`
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

            await expect(
              page.getByText(
                projectName,
                { exact: true },
              ),
            ).toBeVisible();

            await assertNoHorizontalOverflow(
              page,
            );
          },
        );

        await test.step(
          "Step 2 — create environment",
          async () => {
            await page.goto(
              `/app/${organizationSlug}/environments`,
            );

            await page
              .getByLabel("Projeto")
              .selectOption({
                label: projectName,
              });

            await page
              .getByLabel(
                "Nome do ambiente",
              )
              .fill(environmentName);

            await page
              .getByLabel("Slug")
              .fill(
                `prod-e2e-${viewportKey}-${attemptSuffix}`
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

            await expect(
              page.getByText(
                environmentName,
                { exact: true },
              ),
            ).toBeVisible();

            await assertNoHorizontalOverflow(
              page,
            );
          },
        );

        await test.step(
          "Step 3 — create assessment",
          async () => {
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
              .fill("CVE-2026-12345");

            await page
              .getByLabel(
                "Nome da avaliação",
              )
              .fill(assessmentTitle);

            await page
              .getByRole("button", {
                name:
                  "Criar e continuar para evidências",
              })
              .click();

            await expect(page).toHaveURL(
              /\/assessments\/[^/]+$/,
            );

            assessmentUrl = page.url();

            await assertNoHorizontalOverflow(
              page,
            );
          },
        );

        await test.step(
          "Step 4 — execute with essential fields only",
          async () => {
            await assertAdvancedClosed(
              page,
            );

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

            await expect(
              page.getByText(
                /Vetor válido/i,
              ),
            ).toBeVisible();

            await assertAdvancedClosed(
              page,
            );

            await page
              .getByRole("button", {
                name:
                  "Executar e ver resultado",
              })
              .click();
          },
        );

        await test.step(
          "Step 5 — understand result before technical details",
          async () => {
            await expect(
              page.getByRole("heading", {
                name:
                  "Resultado da avaliação",
              }),
            ).toBeVisible();

            await expect(
              page.getByText(
                "Origem",
                { exact: true },
              ),
            ).toBeVisible();

            await expect(
              page.getByText(
                "Contextual",
                { exact: true },
              ),
            ).toBeVisible();

            await expect(
              page.locator(
                "details[open]",
              ),
            ).toHaveCount(0);

            await assertNoHorizontalOverflow(
              page,
            );
          },
        );

        await test.step(
          "Evidence Library is reachable",
          async () => {
            await page
              .getByRole("link", {
                name: "Evidence Library",
              })
              .click();

            await expect(
              page.getByRole("heading", {
                name:
                  /Evidence Library/i,
              }),
            ).toBeVisible();

            await assertNoHorizontalOverflow(
              page,
            );
          },
        );
      },
    );

    test(
      "operator reuses preserved evidence and creates a new run",
      async ({ page }) => {
        test.skip(
          !assessmentUrl,
          "basic journey must run first",
        );

        await page.goto(assessmentUrl);

        await page
          .getByLabel(
            "Vetor CVSS v4.0 de origem",
          )
          .fill(BASE_VECTOR);

        const reusePanel =
          page.getByText(
            "Reutilizar evidência existente (opcional)",
            { exact: true },
          );

        await reusePanel.click();

        const reuseSelect =
          page.getByLabel(
            "Snapshot preservado",
          );

        const optionCount =
          await reuseSelect
            .locator("option")
            .count();

        expect(
          optionCount,
          "a prior run should expose at least one reusable snapshot",
        ).toBeGreaterThan(1);

        await reuseSelect.selectOption({
          index: 1,
        });

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

        await page
          .getByText(
            "Rastreabilidade e auditoria (hashes e engine)",
          )
          .click();

        await expect(
          page.getByText(
            /GUIDED_REUSE/i,
          ),
        ).toBeVisible();

        await assertNoHorizontalOverflow(
          page,
        );
      },
    );

    test(
      "ABSTAIN is understandable and recoverable",
      async ({ page }) => {
        test.skip(
          !assessmentUrl,
          "basic journey must run first",
        );

        await page.goto(assessmentUrl);

        await page
          .getByLabel(
            "Vetor CVSS v4.0 de origem",
          )
          .fill(BASE_VECTOR);

        await page
          .getByLabel(
            /Como o sistema vulnerável pode ser alcançado/i,
          )
          .selectOption("UNKNOWN");

        await page
          .getByLabel(
            "Qualidade da evidência",
          )
          .selectOption("UNKNOWN");

        await page
          .getByRole("button", {
            name:
              "Executar e ver resultado",
          })
          .click();

        await expect(
          page.getByText(
            /se absteve de afirmar um resultado ambiental/i,
          ),
        ).toBeVisible();

        await expect(
          page.getByRole("heading", {
            name:
              /Corrija as evidências e execute novamente/i,
          }),
        ).toBeVisible();

        await page
          .getByRole("link", {
            name:
              "Voltar e executar novamente",
          })
          .click();

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

        await assertNoHorizontalOverflow(
          page,
        );
      },
    );
  },
);
