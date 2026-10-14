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
