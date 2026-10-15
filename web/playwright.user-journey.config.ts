import fs from "node:fs";
import path from "node:path";
import { defineConfig, devices } from "@playwright/test";

const baseURL =
  process.env.E2E_BASE_URL ??
  "http://127.0.0.1:3000";

const storageStateCandidate =
  process.env.E2E_STORAGE_STATE ??
  path.resolve(__dirname, "playwright/.auth/user.json");

const syntheticAuth =
  process.env.E2E_SYNTHETIC_AUTH === "1";

const storageState =
  syntheticAuth ||
  fs.existsSync(storageStateCandidate)
    ? storageStateCandidate
    : undefined;

export default defineConfig({
  globalSetup:
    "./e2e/user-journey/global-setup.ts",
  testDir: "./e2e/user-journey",
  fullyParallel: false,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [
    ["list"],
    ["html", {
      outputFolder:
        "playwright-report/user-journey",
      open: "never",
    }],
  ],
  use: {
    baseURL,
    storageState,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  projects: [
    {
      name: "desktop",
      use: {
        ...devices["Desktop Chrome"],
        viewport: {
          width: 1440,
          height: 900,
        },
      },
    },
    {
      name: "tablet",
      use: {
        ...devices["iPad (gen 7)"],
      },
    },
    {
      name: "mobile",
      use: {
        ...devices["iPhone 13"],
      },
    },
  ],
});
