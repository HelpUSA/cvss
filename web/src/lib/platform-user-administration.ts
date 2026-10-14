import {
  PlatformRole,
  UserStatus,
} from "@prisma/client";

import { DomainError } from "@/lib/domain-errors";
import { isCanonicalPlatformSuperAdminEmail } from "@/lib/platform-superadmin";
import { prisma } from "@/lib/prisma";
import type {
  RequestAuditContext,
} from "@/lib/request-security";
import {
  appendSecurityAuditEvent,
} from "@/lib/security-audit";
import {
  withSerializableRetry,
} from "@/lib/transactions";

function parseUserStatus(value: unknown): UserStatus | undefined {
  if (value === undefined) {
    return undefined;
  }

  if (
    typeof value !== "string" ||
    !Object.values(UserStatus).includes(value as UserStatus)
  ) {
    throw new DomainError({
      code: "invalid_user_status",
      message: "User status is invalid.",
      status: 400,
    });
  }

  return value as UserStatus;
}

function parsePlatformRole(value: unknown): PlatformRole | undefined {
  if (value === undefined) {
    return undefined;
  }

  if (
    typeof value !== "string" ||
    !Object.values(PlatformRole).includes(value as PlatformRole)
  ) {
    throw new DomainError({
      code: "invalid_platform_role",
      message: "Platform role is invalid.",
      status: 400,
    });
  }

  return value as PlatformRole;
}

export async function listPlatformUsers() {
  return prisma.user.findMany({
    select: {
      id: true,
      name: true,
      email: true,
      emailVerified: true,
      status: true,
      platformRole: true,
      image: true,
      createdAt: true,
      updatedAt: true,
      _count: {
        select: {
          sessions: true,
          memberships: true,
        },
      },
      accounts: {
        select: {
          providerId: true,
        },
        orderBy: {
          providerId: "asc",
        },
      },
    },
    orderBy: [
      {
        platformRole: "desc",
      },
      {
        email: "asc",
      },
    ],
  });
}

export async function updatePlatformUser(input: {
  actorUserId: string;
  targetUserId: string;
  status?: unknown;
  platformRole?: unknown;
  requestContext?: RequestAuditContext;
}) {
  const requestedStatus =
    parseUserStatus(input.status);

  const requestedPlatformRole =
    parsePlatformRole(input.platformRole);

  if (
    requestedStatus === undefined &&
    requestedPlatformRole === undefined
  ) {
    throw new DomainError({
      code: "no_user_changes",
      message: "At least one user change is required.",
      status: 400,
    });
  }

  return withSerializableRetry(
    async (transaction) => {
      const actor =
        await transaction.user.findFirst({
          where: {
            id: input.actorUserId,
            status: UserStatus.ACTIVE,
            platformRole:
              PlatformRole.PLATFORM_ADMIN,
          },
          select: {
            id: true,
            email: true,
          },
        });

      if (!actor) {
        throw new DomainError({
          code: "platform_admin_required",
          message:
            "Platform administrator access is required.",
          status: 403,
        });
      }

      const target =
        await transaction.user.findUnique({
          where: {
            id: input.targetUserId,
          },
          select: {
            id: true,
            email: true,
            status: true,
            platformRole: true,
          },
        });

      if (!target) {
        throw new DomainError({
          code: "user_not_found",
          message: "User was not found.",
          status: 404,
        });
      }

      const targetIsCanonical =
        isCanonicalPlatformSuperAdminEmail(
          target.email,
        );

      if (
        targetIsCanonical &&
        requestedStatus !== undefined &&
        requestedStatus !== UserStatus.ACTIVE
      ) {
        throw new DomainError({
          code:
            "canonical_superadmin_must_remain_active",
          message:
            "The canonical platform SuperAdmin account cannot be suspended or disabled.",
          status: 409,
        });
      }

      if (
        targetIsCanonical &&
        requestedPlatformRole !== undefined &&
        requestedPlatformRole !==
          PlatformRole.PLATFORM_ADMIN
      ) {
        throw new DomainError({
          code:
            "canonical_superadmin_role_protected",
          message:
            "The canonical platform SuperAdmin account cannot be demoted.",
          status: 409,
        });
      }

      if (
        requestedPlatformRole !== undefined &&
        !isCanonicalPlatformSuperAdminEmail(
          actor.email,
        )
      ) {
        throw new DomainError({
          code:
            "canonical_superadmin_required_for_role_change",
          message:
            "Only the canonical platform SuperAdmin may change platform roles.",
          status: 403,
        });
      }

      const nextStatus =
        requestedStatus ?? target.status;

      const nextPlatformRole =
        requestedPlatformRole ??
        target.platformRole;

      const updated =
        await transaction.user.update({
          where: {
            id: target.id,
          },
          data: {
            status: nextStatus,
            platformRole: nextPlatformRole,
            suspendedAt:
              nextStatus === UserStatus.SUSPENDED
                ? new Date()
                : null,
            disabledAt:
              nextStatus === UserStatus.DISABLED
                ? new Date()
                : null,
          },
          select: {
            id: true,
            name: true,
            email: true,
            status: true,
            platformRole: true,
          },
        });

      if (
        nextStatus !== UserStatus.ACTIVE
      ) {
        await transaction.session.deleteMany({
          where: {
            userId: target.id,
          },
        });
      }

      await appendSecurityAuditEvent(
        transaction,
        {
          actorUserId: actor.id,
          action: "platform.user.updated",
          targetType: "User",
          targetId: target.id,
          metadata: {
            previousStatus: target.status,
            nextStatus: updated.status,
            previousPlatformRole:
              target.platformRole,
            nextPlatformRole:
              updated.platformRole,
            sessionsRevoked:
              nextStatus !== UserStatus.ACTIVE,
          },
          requestContext:
            input.requestContext,
        },
      );

      return updated;
    },
  );
}
