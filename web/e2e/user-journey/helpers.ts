import { expect, type Page } from "@playwright/test";

export const BASE_VECTOR =
  "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N";

export function requiredEnv(
  name: string,
): string {
  const value = process.env[name]?.trim();

  if (!value) {
    throw new Error(
      `Missing required environment variable: ${name}`,
    );
  }

  return value;
}

export function runSuffix(): string {
  return (
    process.env.E2E_RUN_ID?.trim() ||
    new Date()
      .toISOString()
      .replace(/[^0-9]/g, "")
      .slice(0, 14)
  );
}

export async function assertNoHorizontalOverflow(
  page: Page,
) {
  const dimensions =
    await page.evaluate(() => ({
      scrollWidth:
        document.documentElement
          .scrollWidth,
      clientWidth:
        document.documentElement
          .clientWidth,
    }));

  expect(
    dimensions.scrollWidth,
    "page should not overflow horizontally",
  ).toBeLessThanOrEqual(
    dimensions.clientWidth + 1,
  );
}

export async function assertAdvancedClosed(
  page: Page,
) {
  await expect(
    page.locator(
      ".advanced-threat-maturity[open]",
    ),
  ).toHaveCount(0);

  await expect(
    page.locator(
      ".advanced-security-requirements[open]",
    ),
  ).toHaveCount(0);

  await expect(
    page.locator(
      ".supplemental-metrics-panel[open]",
    ),
  ).toHaveCount(0);
}
