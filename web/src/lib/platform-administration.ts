import {
  MembershipRole,
  MembershipStatus,
  OrganizationStatus,
  PlatformRole,
  UserStatus,
} from "@prisma/client";

import { DomainError } from "@/lib/domain-errors";
import { prisma } from "@/lib/prisma";
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
  normalizeName,
  normalizeSlug,
} from "@/lib/validation";

export async function isActivePlatformAdmin(
  userId: string,
): Promise<boolean> {
  const user =
    await prisma.user.findFirst({
      where: {
        id: userId,
        status: UserStatus.ACTIVE,
        platformRole:
          PlatformRole.PLATFORM_ADMIN,
      },

      select: {
        id: true,
      },
    });

  return Boolean(user);
}

export async function createOrganization(
  input: {
    actorUserId: string;
    name: unknown;
    slug: unknown;
    requestContext?: RequestAuditContext;
  },
) {
  const name = normalizeName(
    input.name,
    "organization name",
  );

  const slug = normalizeSlug(
    input.slug,
    "organization slug",
  );

  try {
    return await withSerializableRetry(
      async (transaction) => {
        const actor =
          await transaction
            .user
            .findFirst({
              where: {
                id: input.actorUserId,
                status:
                  UserStatus.ACTIVE,
                platformRole:
                  PlatformRole
                    .PLATFORM_ADMIN,
              },

              select: {
                id: true,
              },
            });

        if (!actor) {
          throw new DomainError({
            code:
              "platform_admin_required",
            message:
              "Platform administrator access is required.",
            status: 403,
          });
        }

        const organization =
          await transaction
            .organization
            .create({
              data: {
                name,
                slug,
                status:
                  OrganizationStatus
                    .ACTIVE,
              },

              select: {
                id: true,
                name: true,
                slug: true,
              },
            });

        const membership =
          await transaction
            .membership
            .create({
              data: {
                organizationId:
                  organization.id,

                userId:
                  input.actorUserId,

                role:
                  MembershipRole.ADMIN,

                status:
                  MembershipStatus
                    .ACTIVE,
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
              organization.id,

            actorUserId:
              input.actorUserId,

            action:
              "organization.created",

            targetType:
              "Organization",

            targetId:
              organization.id,

            metadata: {
              slug:
                organization.slug,

              firstMembershipRole:
                membership.role,
            },

            requestContext:
              input.requestContext,
          },
        );

        return {
          organization,
          membership,
        };
      },
    );
  } catch (error) {
    if (
      isUniqueConstraintError(error)
    ) {
      throw new DomainError({
        code:
          "organization_slug_conflict",
        message:
          "An organization already uses this slug.",
        status: 409,
      });
    }

    throw error;
  }
}
