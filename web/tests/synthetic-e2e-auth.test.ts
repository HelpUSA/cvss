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

const productionAuth =
  read("src/lib/auth.ts");
const authRoute =
  read("src/app/api/auth/[...all]/route.ts");
const syntheticAuth =
  read("e2e/user-journey/synthetic-auth.ts");
const globalSetup =
  read("e2e/user-journey/global-setup.ts");
const playwrightConfig =
  read("playwright.user-journey.config.ts");

test(
  "production auth remains Google-only and does not import testUtils",
  () => {
    assert.doesNotMatch(
      productionAuth,
      /testUtils/,
    );
    assert.match(
      productionAuth,
      /socialProviders:/,
    );
    assert.match(
      productionAuth,
      /google:/,
    );
    assert.match(
      productionAuth,
      /emailAndPassword:[\s\S]*enabled:\s*false/,
    );
  },
);

test(
  "public auth route continues to expose only the production auth instance",
  () => {
    assert.match(
      authRoute,
      /import \{ auth \} from "@\/lib\/auth"/,
    );
    assert.doesNotMatch(
      authRoute,
      /synthetic|testUtils|e2e/i,
    );
  },
);

test(
  "synthetic Better Auth test utilities live only under e2e",
  () => {
    assert.match(
      syntheticAuth,
      /testUtils\(\)/,
    );
    assert.match(
      syntheticAuth,
      /127\.0\.0\.1/,
    );
    assert.match(
      syntheticAuth,
      /localhost/,
    );
  },
);

test(
  "synthetic fixture is opt-in and local-database fail-closed",
  () => {
    assert.match(
      globalSetup,
      /E2E_SYNTHETIC_AUTH !==\s*"1"/,
    );
    assert.match(
      globalSetup,
      /parsedDatabaseUrl\.hostname/,
    );
    assert.match(
      globalSetup,
      /local disposable PostgreSQL database/,
    );
    assert.match(
      globalSetup,
      /organizationSlug\.startsWith\("e2e"\)/,
    );
  },
);

test(
  "deterministic fixture provisions membership and active policy",
  () => {
    assert.match(
      globalSetup,
      /membership\.upsert/,
    );
    assert.match(
      globalSetup,
      /role:\s*"ADMIN"/,
    );
    assert.match(
      globalSetup,
      /organizationPolicyVersion/,
    );
    assert.match(
      globalSetup,
      /status:\s*"ACTIVE"/,
    );
  },
);

test(
  "Playwright wires global setup and generated storage state",
  () => {
    assert.match(
      playwrightConfig,
      /globalSetup:/,
    );
    assert.match(
      playwrightConfig,
      /E2E_SYNTHETIC_AUTH/,
    );
    assert.match(
      playwrightConfig,
      /storageState/,
    );
  },
);


test(
  "real pipeline keeps synthetic E2E non-blocking during proving period",
  () => {
    const workflow =
      read("../.github/workflows/real-pipeline.yml");

    assert.match(
      workflow,
      /synthetic-user-e2e:/,
    );
    assert.match(
      workflow,
      /continue-on-error:\s*true/,
    );
    assert.match(
      workflow,
      /Run synthetic user journeys three times/,
    );
    assert.match(
      workflow,
      /postgres:16/,
    );
  },
);
