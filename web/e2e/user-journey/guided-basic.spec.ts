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
          `ERP Financeiro ${viewportKey} ${attemptSuffix}`;
        environmentName = "Produção";
        assessmentTitle =
          `CVE-2026-12345 — ${projectName} / ${environmentName}`;

        await test.step(
          "Step 1 — create project using model, automatic slug, and manual slug preservation",
          async () => {
            await page.goto(
              `/app/${organizationSlug}/projects`,
            );

            const templateSelect =
              page.getByLabel(
                "Começar por um modelo (opcional)",
              );
            const nameInput =
              page.getByLabel(
                "Nome do projeto",
              );
            const slugInput =
              page.getByLabel("Slug");

            await templateSelect.focus();
            await expect(
              templateSelect,
            ).toBeFocused();

            await templateSelect.selectOption(
              "ERP / Aplicação",
            );
            await expect(
              nameInput,
            ).toHaveValue(
              "ERP / Aplicação",
            );
            await expect(
              slugInput,
            ).toHaveValue(
              "erp-aplicacao",
            );

            await nameInput.fill(
              "Aplicação São Paulo",
            );
            await expect(
              slugInput,
            ).toHaveValue(
              "aplicacao-sao-paulo",
            );

            await nameInput.fill(
              "ERP Financeiro",
            );
            await expect(
              slugInput,
            ).toHaveValue(
              "erp-financeiro",
            );

            const customSlug =
              `e2e-${viewportKey}-${attemptSuffix}`.toLowerCase();
            await slugInput.fill(
              customSlug,
            );

            await nameInput.fill(
              projectName,
            );
            await expect(
              slugInput,
            ).toHaveValue(customSlug);

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
          "Step 2 — create environments using presets and automatic slugs",
          async () => {
            await page.goto(
              `/app/${organizationSlug}/environments`,
            );

            await page
              .getByLabel("Projeto")
              .selectOption({
                label: projectName,
              });

            const envTemplate =
              page.getByLabel(
                "Tipo de ambiente (atalho)",
              );
            const envName =
              page.getByLabel(
                "Nome do ambiente",
              );
            const envSlug =
              page.getByLabel("Slug");

            const expectedPresets: Array<
              [string, string]
            > = [
              [
                "Homologação",
                "homologacao",
              ],
              [
                "Desenvolvimento",
                "desenvolvimento",
              ],
              ["DMZ", "dmz"],
              [
                "Rede interna",
                "rede-interna",
              ],
              [
                "Cloud / Nuvem",
                "cloud-nuvem",
              ],
              ["Produção", "producao"],
            ];

            for (const [
              presetLabel,
              expectedSlug,
            ] of expectedPresets) {
              await envTemplate.selectOption(
                presetLabel,
              );
              await expect(
                envName,
              ).toHaveValue(presetLabel);
              await expect(
                envSlug,
              ).toHaveValue(expectedSlug);
            }

            await envName.fill(
              "Filial Nordeste",
            );
            await expect(
              envSlug,
            ).toHaveValue(
              "filial-nordeste",
            );

            await envTemplate.selectOption(
              "Homologação",
            );
            await page
              .getByRole("button", {
                name: "Criar ambiente",
              })
              .click();

            await expect(
              page.getByRole("heading", {
                name: "Homologação",
                exact: true,
              }),
            ).toBeVisible();

            await envTemplate.selectOption(
              "Produção",
            );
            await expect(
              envName,
            ).toHaveValue("Produção");
            await expect(
              envSlug,
            ).toHaveValue("producao");

            await page
              .getByRole("button", {
                name: "Criar ambiente",
              })
              .click();

            await expect(
              page.getByRole("heading", {
                name: environmentName,
                exact: true,
              }),
            ).toBeVisible();

            await assertNoHorizontalOverflow(
              page,
            );
          },
        );

        await test.step(
          "Step 3 — create assessment using title and observation templates",
          async () => {
            await page.goto(
              `/app/${organizationSlug}/assessments`,
            );

            const envSelect =
              page.getByLabel("Ambiente");
            const cveInput =
              page.getByLabel("CVE");
            const titleTemplateSelect =
              page.getByLabel(
                "Modelo de nome (opcional)",
              );
            const titleInput =
              page.getByLabel(
                "Nome da avaliação",
              );
            const obsTemplateSelect =
              page.getByLabel(
                "Observação rápida (opcional)",
              );
            const obsInput =
              page.getByLabel(
                "Observação opcional",
              );

            await expect(
              cveInput,
            ).toHaveValue("");

            await envSelect.selectOption({
              label: `${projectName} / Homologação`,
            });

            await cveInput.fill(
              "CVE-2026-12345",
            );

            await titleTemplateSelect.selectOption(
              "cve-environment",
            );
            await expect(
              titleInput,
            ).toHaveValue(
              "CVE-2026-12345 no Homologação",
            );

            await envSelect.selectOption({
              label: `${projectName} / ${environmentName}`,
            });

            await titleTemplateSelect.selectOption(
              "cve-environment",
            );
            await expect(
              titleInput,
            ).toHaveValue(
              `CVE-2026-12345 no ${environmentName}`,
            );

            await titleTemplateSelect.selectOption(
              "assessment-cve",
            );
            await expect(
              titleInput,
            ).toHaveValue(
              `Avaliação CVE-2026-12345 — ${environmentName}`,
            );

            await titleTemplateSelect.selectOption(
              "project-environment",
            );
            await expect(
              titleInput,
            ).toHaveValue(
              assessmentTitle,
            );

            await titleInput.fill(
              `${assessmentTitle} (editado)`,
            );
            await expect(
              titleInput,
            ).toHaveValue(
              `${assessmentTitle} (editado)`,
            );
            await titleInput.fill(
              assessmentTitle,
            );

            await obsTemplateSelect.selectOption(
              "internet",
            );
            await expect(
              obsInput,
            ).toHaveValue(
              /Serviço acessível pela Internet/i,
            );

            await obsTemplateSelect.selectOption(
              "internal",
            );
            await expect(
              obsInput,
            ).toHaveValue(
              /rede interna/i,
            );

            await obsInput.fill(
              "Observação ajustada manualmente pelo operador.",
            );
            await expect(
              obsInput,
            ).toHaveValue(
              "Observação ajustada manualmente pelo operador.",
            );

            await obsInput.fill("");
            await expect(
              obsInput,
            ).toHaveValue("");

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
          "Step 4 — execute with essential fields and numeric shortcuts",
          async () => {
            await assertAdvancedClosed(
              page,
            );

            const vectorInput =
              page.getByLabel(
                "Vetor CVSS v4.0 de origem",
              );
            await expect(
              vectorInput,
            ).toHaveValue("");

            await vectorInput.fill(
              BASE_VECTOR,
            );

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

            const agePreset =
              page.getByLabel(
                "Idade da evidência — atalho",
              );
            const ageInput =
              page.getByLabel(
                "Idade da evidência (dias)",
              );

            for (const presetVal of [
              "0",
              "1",
              "3",
              "7",
              "30",
            ]) {
              await agePreset.selectOption(
                presetVal,
              );
              await expect(
                ageInput,
              ).toHaveValue(presetVal);
            }

            await agePreset.selectOption(
              "7",
            );
            await ageInput.fill("7.5");
            await expect(
              ageInput,
            ).toHaveValue("7.5");

            await agePreset.selectOption(
              "0",
            );
            await expect(
              ageInput,
            ).toHaveValue("0");

            const validityPreset =
              page.getByLabel(
                "Validade máxima — atalho",
              );
            const validityInput =
              page.getByLabel(
                "Validade máxima (dias)",
              );

            for (const maxVal of [
              "1",
              "7",
              "30",
              "90",
            ]) {
              await validityPreset.selectOption(
                maxVal,
              );
              await expect(
                validityInput,
              ).toHaveValue(maxVal);
            }

            await validityInput.fill(
              "2.5",
            );
            await expect(
              validityInput,
            ).toHaveValue("2.5");

            await validityPreset.selectOption(
              "1",
            );
            await expect(
              validityInput,
            ).toHaveValue("1");

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
                  /Evidências preservadas por ambiente|Evidence Library/i,
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

        await expect(
          page.getByText(
            /Vetor válido/i,
          ),
        ).toBeVisible();

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
            "GUIDED_REUSE",
            { exact: true },
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

        await expect(
          page.getByText(
            /Vetor válido/i,
          ),
        ).toBeVisible();

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

        await expect(
          page.getByText(
            /Vetor válido/i,
          ),
        ).toBeVisible();

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
