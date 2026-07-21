import { DomainError } from "@/lib/domain-errors";
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
import {
  normalizeId,
} from "@/lib/validation";

export async function listUserSessions(
  userId: string,
) {
  return prisma.session.findMany({
    where: {
      userId,

      expiresAt: {
        gt: new Date(),
      },
    },

    select: {
      id: true,
      createdAt: true,
      updatedAt: true,
      expiresAt: true,
      ipAddress: true,
      userAgent: true,
    },

    orderBy: [
      {
        updatedAt: "desc",
      },
      {
        id: "asc",
      },
    ],
  });
}

export async function revokeUserSession(
  input: {
    userId: string;
    currentSessionId: string;
    sessionId: unknown;
    requestContext?:
      RequestAuditContext;
  },
) {
  const sessionId =
    normalizeId(
      input.sessionId,
      "sessionId",
    );

  return withSerializableRetry(
    async (transaction) => {
      const session =
        await transaction
          .session
          .findFirst({
            where: {
              id: sessionId,
              userId:
                input.userId,
            },

            select: {
              id: true,
            },
          });

      if (!session) {
        throw new DomainError({
          code:
            "session_not_found",

          message:
            "Session was not found.",

          status: 404,
        });
      }

      await transaction
        .session
        .delete({
          where: {
            id:
              session.id,
          },
        });

      await appendSecurityAuditEvent(
        transaction,
        {
          actorUserId:
            input.userId,

          action:
            "session.revoked",

          targetType:
            "Session",

          targetId:
            session.id,

          metadata: {
            revokedCurrent:
              session.id ===
              input.currentSessionId,
          },

          requestContext:
            input.requestContext,
        },
      );

      return {
        revokedCurrent:
          session.id ===
          input.currentSessionId,
      };
    },
  );
}

export async function revokeOtherUserSessions(
  input: {
    userId: string;
    currentSessionId: string;
    requestContext?:
      RequestAuditContext;
  },
) {
  return withSerializableRetry(
    async (transaction) => {
      const deleted =
        await transaction
          .session
          .deleteMany({
            where: {
              userId:
                input.userId,

              id: {
                not:
                  input.currentSessionId,
              },
            },
          });

      await appendSecurityAuditEvent(
        transaction,
        {
          actorUserId:
            input.userId,

          action:
            "sessions.revoked_others",

          targetType:
            "User",

          targetId:
            input.userId,

          metadata: {
            revokedCount:
              deleted.count,
          },

          requestContext:
            input.requestContext,
        },
      );

      return {
        revokedCount:
          deleted.count,
      };
    },
  );
}

export async function revokeAllUserSessions(
  input: {
    userId: string;
    requestContext?:
      RequestAuditContext;
  },
) {
  return withSerializableRetry(
    async (transaction) => {
      const deleted =
        await transaction
          .session
          .deleteMany({
            where: {
              userId:
                input.userId,
            },
          });

      await appendSecurityAuditEvent(
        transaction,
        {
          actorUserId:
            input.userId,

          action:
            "sessions.revoked_all",

          targetType:
            "User",

          targetId:
            input.userId,

          metadata: {
            revokedCount:
              deleted.count,
          },

          requestContext:
            input.requestContext,
        },
      );

      return {
        revokedCount:
          deleted.count,
      };
    },
  );
}
