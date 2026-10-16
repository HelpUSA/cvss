import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

const workflow = fs.readFileSync(
  path.resolve(
    __dirname,
    "../../.github/workflows/real-pipeline.yml",
  ),
  "utf8",
);

test(
  "synthetic E2E isolates each viewport and stability round in its own organization",
  () => {
    assert.match(
      workflow,
      /for run in 1 2 3/,
    );
    assert.match(
      workflow,
      /for project in desktop tablet mobile/,
    );
    assert.match(
      workflow,
      /E2E_ORGANIZATION_SLUG="e2e-\$\{GITHUB_RUN_ID\}-\$\{run\}-\$\{project\}"/,
    );
    assert.match(
      workflow,
      /--project="\$\{project\}"/,
    );
  },
);

test(
  "synthetic E2E is a blocking CI gate after isolated stability proof",
  () => {
    assert.match(
      workflow,
      /synthetic-user-e2e:/,
    );
    assert.doesNotMatch(
      workflow,
      /continue-on-error:/,
    );
  },
);
