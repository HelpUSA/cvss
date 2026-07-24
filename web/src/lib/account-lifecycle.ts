import {
  UserStatus,
  type Prisma,
} from "@prisma/client";

import {
  hashOpaqueToken,
  issueOpaqueToken,
  parseOpaqueToken,
} from "@/lib/auth-tokens";
import { DomainError } from "@/lib/domain-errors";
import {
  buildPublicUrl,
  escapeHtml,
  sendTransactionalEmail,
} from "@/lib/email-delivery";
import {
  hashCredentialPassword,
  parseNewPassword,
} from "@/lib/password-policy";
import { prisma } from "@/lib/prisma";
import type {
  RequestAuditContext,
} from "@/lib/request-security";
import {
  withSerializableRetry,
} from "@/lib/transactions";
import {
  normalizeMemberEmail,
} from "@/lib/validation";

const PASSWORD_RESET_TTL_MS =
  30 * 60 * 1000;

const CREDENTIAL_PROVIDER =
  "credential";

async function appendAnonymousAudit(
  transaction:
    Prisma.TransactionClient,

  input: {
    action: string;
    targetType?: string;
    targetId?: string;
    metadata?:
      Prisma.InputJsonObject;
    requestContext?:
      RequestAuditContext;
  },
): Promise<void> {
  await transaction
    .securityAuditEvent
    .create({
      data: {
        actorUserId: null,
        organizationId: null,

        action:
          input.action,

        targetType:
          input.targetType,

        targetId:
          input.targetId,

        ipAddress:
          input.requestContext
            ?.ipAddress,

        userAgent:
          input.requestContext
            ?.userAgent,

        metadata:
          input.metadata,
      },
    });
}

async function revokeFailedResetToken(
  input: {
    tokenId: string;
    userId: string;
    requestContext?:
      RequestAuditContext;
  },
): Promise<void> {
  await withSerializableRetry(
    async (transaction) => {
      await transaction
        .passwordResetToken
        .updateMany({
          where: {
            id: input.tokenId,
            usedAt: null,
          },

          data: {
            revokedAt:
              new Date(),
          },
        });

      await appendAnonymousAudit(
        transaction,
        {
          action:
            "password_reset.delivery_failed",

          targetType:
            "User",

          targetId:
            input.userId,

          requestContext:
            input.requestContext,
        },
      );
    },
  );
}

export async function requestPasswordReset(
  input: {
    email: unknown;
    requestContext?:
      RequestAuditContext;
  },
): Promise<{
  accepted: true;
}> {
  const email =
    normalizeMemberEmail(
      input.email,
    );

  const user =
    await prisma.user.findFirst({
      where: {
        email,
        status:
          UserStatus.ACTIVE,

        accounts: {
          some: {
            providerId:
              CREDENTIAL_PROVIDER,

            password: {
              not: null,
            },
          },
        },
      },

      select: {
        id: true,
        name: true,
        email: true,
      },
    });

  if (!user) {
    await prisma
      .securityAuditEvent
      .create({
        data: {
          actorUserId: null,

          action:
            "password_reset.request_ignored",

          ipAddress:
            input.requestContext
              ?.ipAddress,

          userAgent:
            input.requestContext
              ?.userAgent,
        },
      });

    return {
      accepted: true,
    };
  }

  const {
    token,
    tokenHash,
  } = issueOpaqueToken();

  const expiresAt =
    new Date(
      Date.now() +
        PASSWORD_RESET_TTL_MS,
    );

  const resetToken =
    await withSerializableRetry(
      async (transaction) => {
        await transaction
          .passwordResetToken
          .updateMany({
            where: {
              userId: user.id,
              usedAt: null,
              revokedAt: null,
            },

            data: {
              revokedAt:
                new Date(),
            },
          });

        const created =
          await transaction
            .passwordResetToken
            .create({
              data: {
                userId: user.id,
                tokenHash,
                expiresAt,
              },

              select: {
                id: true,
              },
            });

        await appendAnonymousAudit(
          transaction,
          {
            action:
              "password_reset.requested",

            targetType:
              "User",

            targetId:
              user.id,

            requestContext:
              input.requestContext,
          },
        );

        return created;
      },
    );

  const resetUrl =
    buildPublicUrl(
      `/reset-password?token=${encodeURIComponent(
        token,
      )}`,
    );

  try {
    await sendTransactionalEmail({
      to: user.email,

      subject:
        "Redefinição de senha — CVSS",

      text:
        `Olá, ${user.name}.\n\n` +
        `Use o endereço abaixo para redefinir sua senha. ` +
        `O link expira em 30 minutos e pode ser usado uma única vez.\n\n` +
        `${resetUrl}\n\n` +
        `Caso você não tenha solicitado a redefinição, ignore esta mensagem.`,

      html:
        `<p>Olá, ${escapeHtml(user.name)}.</p>` +
        `<p>Use o botão abaixo para redefinir sua senha. ` +
        `O link expira em 30 minutos e pode ser usado uma única vez.</p>` +
        `<p><a href="${escapeHtml(resetUrl)}">Redefinir senha</a></p>` +
        `<p>Caso você não tenha solicitado a redefinição, ignore esta mensagem.</p>`,

      idempotencyKey:
        `password-reset-${resetToken.id}`,
    });
  } catch (error) {
    await revokeFailedResetToken({
      tokenId:
        resetToken.id,

      userId:
        user.id,

      requestContext:
        input.requestContext,
    });

    console.error(
      "AUTH1E_PASSWORD_RESET_DELIVERY_FAILED",
      error instanceof Error
        ? error.name
        : "UnknownError",
    );
  }

  return {
    accepted: true,
  };
}

export async function confirmPasswordReset(
  input: {
    token: unknown;
    password: unknown;
    requestContext?:
      RequestAuditContext;
  },
): Promise<{
  sessionsRevoked: number;
}> {
  const token =
    parseOpaqueToken(
      input.token,
    );

  const password =
    parseNewPassword(
      input.password,
    );

  const tokenHash =
    hashOpaqueToken(token);

  const candidate =
    await prisma
      .passwordResetToken
      .findFirst({
        where: {
          tokenHash,
          usedAt: null,
          revokedAt: null,

          expiresAt: {
            gt: new Date(),
          },

          user: {
            status:
              UserStatus.ACTIVE,
          },
        },

        select: {
          id: true,
          userId: true,
        },
      });

  if (!candidate) {
    throw new DomainError({
      code:
        "invalid_or_expired_reset",

      message:
        "The password reset link is invalid or expired.",

      status: 400,
    });
  }

  const passwordHash =
    await hashCredentialPassword(
      password,
    );

  return withSerializableRetry(
    async (transaction) => {
      const current =
        await transaction
          .passwordResetToken
          .findFirst({
            where: {
              id: candidate.id,
              tokenHash,
              usedAt: null,
              revokedAt: null,

              expiresAt: {
                gt: new Date(),
              },

              user: {
                status:
                  UserStatus.ACTIVE,
              },
            },

            select: {
              id: true,
              userId: true,
            },
          });

      if (!current) {
        throw new DomainError({
          code:
            "invalid_or_expired_reset",

          message:
            "The password reset link is invalid or expired.",

          status: 400,
        });
      }

      const account =
        await transaction
          .account
          .findFirst({
            where: {
              userId:
                current.userId,

              providerId:
                CREDENTIAL_PROVIDER,
            },

            select: {
              id: true,
            },
          });

      if (!account) {
        throw new DomainError({
          code:
            "credential_account_not_found",

          message:
            "A credential account was not found.",

          status: 409,
        });
      }

      await transaction
        .account
        .update({
          where: {
            id: account.id,
          },

          data: {
            password:
              passwordHash,
          },
        });

      await transaction
        .passwordResetToken
        .update({
          where: {
            id: current.id,
          },

          data: {
            usedAt:
              new Date(),
          },
        });

      await transaction
        .passwordResetToken
        .updateMany({
          where: {
            userId:
              current.userId,

            id: {
              not: current.id,
            },

            usedAt: null,
            revokedAt: null,
          },

          data: {
            revokedAt:
              new Date(),
          },
        });

      const deletedSessions =
        await transaction
          .session
          .deleteMany({
            where: {
              userId:
                current.userId,
            },
          });

      await appendAnonymousAudit(
        transaction,
        {
          action:
            "password_reset.completed",

          targetType:
            "User",

          targetId:
            current.userId,

          metadata: {
            sessionsRevoked:
              deletedSessions.count,
          },

          requestContext:
            input.requestContext,
        },
      );

      return {
        sessionsRevoked:
          deletedSessions.count,
      };
    },
  );
}
