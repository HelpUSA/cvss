import {
  MembershipRole,
  MembershipStatus,
  ProjectStatus,
  EnvironmentStatus,
  UserStatus,
  type Prisma,
} from "@prisma/client";

import { DomainError } from "@/lib/domain-errors";
import {
  assertLastActiveAdminInvariant,
} from "@/lib/membership-invariants";
import type {
  OrganizationContext,
} from "@/lib/organization-context";
import type {
  RequestAuditContext,
} from "@/lib/request-security";
import {
  appendSecurityAuditEvent,
} from "@/lib/security-audit";
import {
  isUniqueConstraintError,
  withSerializableRetry,
} from "@/lib/transactions";
import {
  normalizeId,
  normalizeMemberEmail,
  normalizeName,
  normalizeSlug,
  parseMembershipRole,
  parseMembershipStatus,
} from "@/lib/validation";

export async function addOrganizationMembership(
  input: {
    context: OrganizationContext;
    actorUserId: string;
    email: unknown;
    role: unknown;
    requestContext?: RequestAuditContext;
  },
) {
  const email =
    normalizeMemberEmail(
      input.email,
    );

  const role =
    parseMembershipRole(
      input.role,
    );

  return withSerializableRetry(
    async (transaction) => {
      const user =
        await transaction.user.findFirst({
          where: {
            email,
            status: UserStatus.ACTIVE,
          },

          select: {
            id: true,
            name: true,
            email: true,
          },
        });

      if (!user) {
        throw new DomainError({
          code: "active_user_not_found",
          message:
            "No active user exists with this email.",
          status: 404,
        });
      }

      const existing =
        await transaction
          .membership
          .findUnique({
            where: {
              organizationId_userId: {
                organizationId:
                  input.context
                    .organization.id,

                userId: user.id,
              },
            },

            select: {
              id: true,
            },
          });

      if (existing) {
        throw new DomainError({
          code:
            "membership_already_exists",
          message:
            "This user already has a membership in the organization.",
          status: 409,
        });
      }

      const membership =
        await transaction
          .membership
          .create({
            data: {
              organizationId:
                input.context
                  .organization.id,

              userId: user.id,
              role,

              status:
                MembershipStatus.ACTIVE,
            },

            select: {
              id: true,
              role: true,
              status: true,
            },
          });

      await appendSecurityAuditEvent(
        transaction,
        {
          organizationId:
            input.context
              .organization.id,

          actorUserId:
            input.actorUserId,

          action:
            "membership.created",

          targetType:
            "Membership",

          targetId:
            membership.id,

          metadata: {
            targetUserId:
              user.id,

            role:
              membership.role,

            status:
              membership.status,
          },

          requestContext:
            input.requestContext,
        },
      );

      return {
        membership,
        user,
      };
    },
  );
}

export async function updateOrganizationMembership(
  input: {
    context: OrganizationContext;
    actorUserId: string;
    membershipId: unknown;
    role?: unknown;
    status?: unknown;
    requestContext?: RequestAuditContext;
  },
) {
  const membershipId = normalizeId(
    input.membershipId,
    "membershipId",
  );

  const requestedRole =
    input.role === undefined
      ? undefined
      : parseMembershipRole(
          input.role,
        );

  const requestedStatus =
    input.status === undefined
      ? undefined
      : parseMembershipStatus(
          input.status,
        );

  if (
    requestedRole === undefined &&
    requestedStatus === undefined
  ) {
    throw new DomainError({
      code: "no_membership_changes",
      message:
        "At least one membership change is required.",
      status: 400,
    });
  }

  return withSerializableRetry(
    async (transaction) => {
      const current =
        await transaction
          .membership
          .findFirst({
            where: {
              id: membershipId,

              organizationId:
                input.context
                  .organization.id,
            },

            select: {
              id: true,
              userId: true,
              role: true,
              status: true,
              suspendedAt: true,
              revokedAt: true,

              user: {
                select: {
                  id: true,
                  name: true,
                  email: true,
                  status: true,
                },
              },
            },
          });

      if (!current) {
        throw new DomainError({
          code:
            "membership_not_found",
          message:
            "Membership was not found.",
          status: 404,
        });
      }

      const nextRole =
        requestedRole ??
        current.role;

      const nextStatus =
        requestedStatus ??
        current.status;

      if (
        nextStatus ===
          MembershipStatus.ACTIVE &&
        current.user.status !==
          UserStatus.ACTIVE
      ) {
        throw new DomainError({
          code:
            "inactive_user_membership",
          message:
            "An inactive user cannot receive an active membership.",
          status: 409,
        });
      }

      const activeAdminCount =
        await transaction
          .membership
          .count({
            where: {
              organizationId:
                input.context
                  .organization.id,

              role:
                MembershipRole.ADMIN,

              status:
                MembershipStatus.ACTIVE,
            },
          });

      assertLastActiveAdminInvariant({
        before: {
          role: current.role,
          status: current.status,
        },

        after: {
          role: nextRole,
          status: nextStatus,
        },

        activeAdminCount,
      });

      const data:
        Prisma.MembershipUpdateInput = {};

      if (
        requestedRole !== undefined
      ) {
        data.role = requestedRole;
      }

      if (
        requestedStatus !== undefined
      ) {
        data.status =
          requestedStatus;

        if (
          requestedStatus ===
          MembershipStatus.ACTIVE
        ) {
          data.suspendedAt = null;
          data.revokedAt = null;
        }

        if (
          requestedStatus ===
          MembershipStatus.SUSPENDED
        ) {
          data.suspendedAt =
            new Date();

          data.revokedAt = null;
        }

        if (
          requestedStatus ===
          MembershipStatus.REVOKED
        ) {
          data.suspendedAt = null;
          data.revokedAt =
            new Date();
        }
      }

      const updated =
        await transaction
          .membership
          .update({
            where: {
              id: current.id,
            },

            data,

            select: {
              id: true,
              role: true,
              status: true,
            },
          });

      await appendSecurityAuditEvent(
        transaction,
        {
          organizationId:
            input.context
              .organization.id,

          actorUserId:
            input.actorUserId,

          action:
            "membership.updated",

          targetType:
            "Membership",

          targetId:
            updated.id,

          metadata: {
            targetUserId:
              current.userId,

            previousRole:
              current.role,

            nextRole:
              updated.role,

            previousStatus:
              current.status,

            nextStatus:
              updated.status,
          },

          requestContext:
            input.requestContext,
        },
      );

      return {
        membership: updated,
        user: current.user,
      };
    },
  );
}

export async function createTenantProject(
  input: {
    context: OrganizationContext;
    actorUserId: string;
    name: unknown;
    slug: unknown;
    requestContext?: RequestAuditContext;
  },
) {
  const name = normalizeName(
    input.name,
    "project name",
  );

  const slug = normalizeSlug(
    input.slug,
    "project slug",
  );

  try {
    return await withSerializableRetry(
      async (transaction) => {
        const project =
          await transaction
            .project
            .create({
              data: {
                organizationId:
                  input.context
                    .organization.id,

                name,
                slug,

                status:
                  ProjectStatus.ACTIVE,
              },

              select: {
                id: true,
                name: true,
                slug: true,
                status: true,
              },
            });

        await appendSecurityAuditEvent(
          transaction,
          {
            organizationId:
              input.context
                .organization.id,

            actorUserId:
              input.actorUserId,

            action:
              "project.created",

            targetType:
              "Project",

            targetId:
              project.id,

            metadata: {
              slug:
                project.slug,
            },

            requestContext:
              input.requestContext,
          },
        );

        return project;
      },
    );
  } catch (error) {
    if (
      isUniqueConstraintError(error)
    ) {
      throw new DomainError({
        code:
          "project_slug_conflict",
        message:
          "A project in this organization already uses this slug.",
        status: 409,
      });
    }

    throw error;
  }
}

export async function createTenantEnvironment(
  input: {
    context: OrganizationContext;
    actorUserId: string;
    projectId: unknown;
    name: unknown;
    slug: unknown;
    requestContext?: RequestAuditContext;
  },
) {
  const projectId = normalizeId(
    input.projectId,
    "projectId",
  );

  const name = normalizeName(
    input.name,
    "environment name",
  );

  const slug = normalizeSlug(
    input.slug,
    "environment slug",
  );

  try {
    return await withSerializableRetry(
      async (transaction) => {
        const project =
          await transaction
            .project
            .findFirst({
              where: {
                id: projectId,

                organizationId:
                  input.context
                    .organization.id,

                status:
                  ProjectStatus.ACTIVE,
              },

              select: {
                id: true,
                name: true,
              },
            });

        if (!project) {
          throw new DomainError({
            code:
              "tenant_project_not_found",
            message:
              "The project was not found in this organization.",
            status: 404,
          });
        }

        const environment =
          await transaction
            .environment
            .create({
              data: {
                projectId:
                  project.id,

                name,
                slug,

                status:
                  EnvironmentStatus.ACTIVE,
              },

              select: {
                id: true,
                name: true,
                slug: true,
                status: true,
                projectId: true,
              },
            });

        await appendSecurityAuditEvent(
          transaction,
          {
            organizationId:
              input.context
                .organization.id,

            actorUserId:
              input.actorUserId,

            action:
              "environment.created",

            targetType:
              "Environment",

            targetId:
              environment.id,

            metadata: {
              projectId:
                project.id,

              slug:
                environment.slug,
            },

            requestContext:
              input.requestContext,
          },
        );

        return {
          environment,
          project,
        };
      },
    );
  } catch (error) {
    if (
      isUniqueConstraintError(error)
    ) {
      throw new DomainError({
        code:
          "environment_slug_conflict",
        message:
          "An environment in this project already uses this slug.",
        status: 409,
      });
    }

    throw error;
  }
}
