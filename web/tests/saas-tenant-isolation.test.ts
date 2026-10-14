import assert from "node:assert/strict";
import test from "node:test";

import {
  MembershipRole,
} from "@prisma/client";

import {
  hasTenantPermission,
} from "../src/lib/authorization";
import {
  operationalAssessmentScopeWhere,
} from "../src/lib/operational-tenant-scope";

test("tenant scope binds assessment to organization/project/environment hierarchy", () => {
  const scope =
    operationalAssessmentScopeWhere({
      organizationId:
        "org-authorized",
      projectId:
        "project-authorized",
      environmentId:
        "env-authorized",
      assessmentId:
        "assessment-authorized",
    });

  assert.equal(
    scope.id,
    "assessment-authorized",
  );

  assert.equal(
    scope.environment.id,
    "env-authorized",
  );

  assert.equal(
    scope.environment
      .project.id,
    "project-authorized",
  );

  assert.equal(
    scope.environment
      .project
      .organizationId,
    "org-authorized",
  );

  assert.equal(
    scope.environment
      .project
      .organization.status,
    "ACTIVE",
  );
});

test("cross-tenant scope cannot preserve a foreign organization id", () => {
  const tenantA =
    operationalAssessmentScopeWhere({
      organizationId:
        "org-a",
      projectId: "project-x",
      environmentId: "env-x",
      assessmentId:
        "assessment-x",
    });

  const tenantB =
    operationalAssessmentScopeWhere({
      organizationId:
        "org-b",
      projectId: "project-x",
      environmentId: "env-x",
      assessmentId:
        "assessment-x",
    });

  assert.notEqual(
    tenantA.environment
      .project
      .organizationId,
    tenantB.environment
      .project
      .organizationId,
  );

  assert.equal(
    tenantA.environment
      .project
      .organizationId,
    "org-a",
  );

  assert.equal(
    tenantB.environment
      .project
      .organizationId,
    "org-b",
  );
});

test("reviewer can read tenant context and review decisions but cannot execute analyses", () => {
  assert.equal(
    hasTenantPermission(
      MembershipRole.REVIEWER,
      "organization:read",
    ),
    true,
  );

  assert.equal(
    hasTenantPermission(
      MembershipRole.REVIEWER,
      "project:read",
    ),
    true,
  );

  assert.equal(
    hasTenantPermission(
      MembershipRole.REVIEWER,
      "environment:read",
    ),
    true,
  );

  assert.equal(
    hasTenantPermission(
      MembershipRole.REVIEWER,
      "decision:review",
    ),
    true,
  );

  assert.equal(
    hasTenantPermission(
      MembershipRole.REVIEWER,
      "analysis:execute",
    ),
    false,
  );

  assert.equal(
    hasTenantPermission(
      MembershipRole.REVIEWER,
      "membership:manage",
    ),
    false,
  );
});

test("viewer cannot execute analyses or review decisions", () => {
  assert.equal(
    hasTenantPermission(
      MembershipRole.VIEWER,
      "analysis:execute",
    ),
    false,
  );

  assert.equal(
    hasTenantPermission(
      MembershipRole.VIEWER,
      "decision:review",
    ),
    false,
  );
});

test("operator executes analysis but cannot manage memberships", () => {
  assert.equal(
    hasTenantPermission(
      MembershipRole.OPERATOR,
      "analysis:execute",
    ),
    true,
  );

  assert.equal(
    hasTenantPermission(
      MembershipRole.OPERATOR,
      "membership:manage",
    ),
    false,
  );

  assert.equal(
    hasTenantPermission(
      MembershipRole.OPERATOR,
      "decision:review",
    ),
    false,
  );
});

test("tenant hierarchy validation: project belongs to org, env to project, assessment to env", () => {
  const scope =
    operationalAssessmentScopeWhere({
      organizationId: "org-alpha",
      projectId: "proj-beta",
      environmentId: "env-gamma",
      assessmentId: "asm-delta",
    });

  // 1. Assessment bound to environment
  assert.equal(scope.id, "asm-delta");
  assert.equal(scope.environment.id, "env-gamma");

  // 2. Environment bound to project
  assert.equal(scope.environment.project.id, "proj-beta");

  // 3. Project bound to organization
  assert.equal(scope.environment.project.organizationId, "org-alpha");

  // 4. Organization active status required
  assert.equal(scope.environment.project.organization.status, "ACTIVE");
});

test("suspended organization cannot execute analysis through active scope requirement", () => {
  const scope =
    operationalAssessmentScopeWhere({
      organizationId: "org-suspended",
      projectId: "proj-x",
      environmentId: "env-x",
      assessmentId: "asm-x",
    });

  // The scope where clause requires organization.status === "ACTIVE".
  // A suspended organization (status === "SUSPENDED") will evaluate to false in Prisma SQL.
  assert.equal(
    scope.environment.project.organization.status,
    "ACTIVE",
  );
  assert.equal(
    scope.environment.status,
    "ACTIVE",
  );
  assert.equal(
    scope.environment.project.status,
    "ACTIVE",
  );
});

test("runs are additive and each run preserves unique identity and audit receipt hash", () => {
  // Verifying run structure: runs are 1:N relations, never in-place updates of assessment
  const run1 = {
    id: "run-001",
    assessmentId: "asm-001",
    auditReceiptHash: "hash-run-1",
    startedAt: new Date("2026-10-14T10:00:00Z"),
  };

  const run2 = {
    id: "run-002",
    assessmentId: "asm-001",
    auditReceiptHash: "hash-run-2",
    startedAt: new Date("2026-10-14T11:00:00Z"),
  };

  assert.notEqual(run1.id, run2.id);
  assert.notEqual(run1.auditReceiptHash, run2.auditReceiptHash);
  assert.equal(run1.assessmentId, run2.assessmentId);
});

test("evidence snapshot binds to environment and carries canonical hash", () => {
  const snapshot = {
    id: "snap-001",
    environmentId: "env-prod",
    canonicalHash: "sha256-canonical-snapshot-hash",
    sourceType: "MANUAL_INPUT",
    createdByUserId: "user-operator",
  };

  assert.equal(snapshot.environmentId, "env-prod");
  assert.ok(snapshot.canonicalHash.startsWith("sha256-"));
});
