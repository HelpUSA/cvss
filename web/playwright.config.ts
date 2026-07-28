import {
  defineConfig,
  devices,
} from "@playwright/test";

const baseURL =
  process.env.AUTH1G_BASE_URL ??
  "http://127.0.0.1:3000";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  forbidOnly: Boolean(process.env.CI),
  timeout: 120_000,
  expect: {
    timeout: 20_000,
  },
  reporter: [
    ["line"],
    [
      "html",
      {
        outputFolder:
          "playwright-report",
        open: "never",
      },
    ],
  ],
  use: {
    baseURL,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
      },
    },
  ],
  webServer: {
    command:
      "npm run start -- --hostname 127.0.0.1 --port 3000",
    url: baseURL,
    reuseExistingServer: false,
    timeout: 120_000,
    stdout: "pipe",
    stderr: "pipe",
  },
});