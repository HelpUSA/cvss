import {
  MembershipStatus,
  OrganizationStatus,
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
import type {
  OrganizationContext,
} from "@/lib/organization-context";
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
  normalizeMemberEmail,
  parseMembershipRole,
} from "@/lib/validation";

const INVITATION_TTL_MS =
  72 * 60 * 60 * 1000;

export async function listOrganizationInvitations(
  context: OrganizationContext,
) {
  return prisma.invitation.findMany({
    where: {
      organizationId:
        context.organization.id,

      acceptedAt: null,
      revokedAt: null,

      expiresAt: {
        gt: new Date(),
      },
    },

    select: {
      id: true,
      email: true,
      role: true,
      expiresAt: true,
      createdAt: true,

      createdBy: {
        select: {
          name: true,
        },
      },
    },

    orderBy: [
      {
        createdAt: "desc",
      },
      {
        id: "asc",
      },
    ],
  });
}

async function revokeInvitationAfterDeliveryFailure(
  input: {
    invitationId: string;
    context: OrganizationContext;
    actorUserId: string;
    requestContext?:
      RequestAuditContext;
  },
): Promise<void> {
  await withSerializableRetry(
    async (transaction) => {
      await transaction
        .invitation
        .updateMany({
          where: {
            id:
              input.invitationId,

            organizationId:
              input.context
                .organization.id,

            acceptedAt: null,
          },

          data: {
            revokedAt:
              new Date(),
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
            "invitation.delivery_failed",

          targetType:
            "Invitation",

          targetId:
            input.invitationId,

          requestContext:
            input.requestContext,
        },
      );
    },
  );
}

export async function createOrganizationInvitation(
  input: {
    context: OrganizationContext;
    actorUserId: string;
    email: unknown;
    role: unknown;
    requestContext?:
      RequestAuditContext;
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

  const {
    token,
    tokenHash,
  } = issueOpaqueToken();

  const expiresAt =
    new Date(
      Date.now() +
        INVITATION_TTL_MS,
    );

  const invitation =
    await withSerializableRetry(
      async (transaction) => {
        const activeMembership =
          await transaction
            .membership
            .findFirst({
              where: {
                organizationId:
                  input.context
                    .organization.id,

                status:
                  MembershipStatus.ACTIVE,

                user: {
                  email,
                },
              },

              select: {
                id: true,
              },
            });

        if (activeMembership) {
          throw new DomainError({
            code:
              "active_membership_exists",

            message:
              "This user already has an active membership.",

            status: 409,
          });
        }

        await transaction
          .invitation
          .updateMany({
            where: {
              organizationId:
                input.context
                  .organization.id,

              email,
              acceptedAt: null,
              revokedAt: null,
            },

            data: {
              revokedAt:
                new Date(),
            },
          });

        const created =
          await transaction
            .invitation
            .create({
              data: {
                organizationId:
                  input.context
                    .organization.id,

                email,
                role,
                tokenHash,
                expiresAt,

                createdByUserId:
                  input.actorUserId,
              },

              select: {
                id: true,
                email: true,
                role: true,
                expiresAt: true,
                createdAt: true,
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
              "invitation.created",

            targetType:
              "Invitation",

            targetId:
              created.id,

            metadata: {
              role:
                created.role,
            },

            requestContext:
              input.requestContext,
          },
        );

        return created;
      },
    );

  const invitationUrl =
    buildPublicUrl(
      `/invitation?token=${encodeURIComponent(
        token,
      )}`,
    );

  try {
    await sendTransactionalEmail({
      to: invitation.email,

      subject:
        `Convite para ${input.context.organization.name}`,

      text:
        `Você recebeu um convite para acessar ` +
        `${input.context.organization.name} no CVSS.\n\n` +
        `Papel: ${invitation.role}\n` +
        `O convite expira em 72 horas.\n\n` +
        `${invitationUrl}\n\n` +
        `Entre com a conta que utiliza este endereço de e-mail.`,

      html:
        `<p>Você recebeu um convite para acessar ` +
        `<strong>${escapeHtml(input.context.organization.name)}</strong> no CVSS.</p>` +
        `<p>Papel: <strong>${escapeHtml(invitation.role)}</strong></p>` +
        `<p>O convite expira em 72 horas.</p>` +
        `<p><a href="${escapeHtml(invitationUrl)}">Aceitar convite</a></p>` +
        `<p>Entre com a conta que utiliza este endereço de e-mail.</p>`,

      idempotencyKey:
        `invitation-${invitation.id}`,
    });
  } catch (error) {
    await revokeInvitationAfterDeliveryFailure({
      invitationId:
        invitation.id,

      context:
        input.context,

      actorUserId:
        input.actorUserId,

      requestContext:
        input.requestContext,
    });

    throw error;
  }

  return invitation;
}

export async function revokeOrganizationInvitation(
  input: {
    context: OrganizationContext;
    actorUserId: string;
    invitationId: unknown;
    requestContext?:
      RequestAuditContext;
  },
) {
  const invitationId =
    normalizeId(
      input.invitationId,
      "invitationId",
    );

  return withSerializableRetry(
    async (transaction) => {
      const invitation =
        await transaction
          .invitation
          .findFirst({
            where: {
              id: invitationId,

              organizationId:
                input.context
                  .organization.id,

              acceptedAt: null,
              revokedAt: null,
            },

            select: {
              id: true,
            },
          });

      if (!invitation) {
        throw new DomainError({
          code:
            "invitation_not_found",

          message:
            "Invitation was not found.",

          status: 404,
        });
      }

      const updated =
        await transaction
          .invitation
          .update({
            where: {
              id:
                invitation.id,
            },

            data: {
              revokedAt:
                new Date(),
            },

            select: {
              id: true,
              revokedAt: true,
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
            "invitation.revoked",

          targetType:
            "Invitation",

          targetId:
            invitation.id,

          requestContext:
            input.requestContext,
        },
      );

      return updated;
    },
  );
}

export async function acceptOrganizationInvitation(
  input: {
    token: unknown;
    user: {
      id: string;
      email: string;
    };
    requestContext?:
      RequestAuditContext;
  },
) {
  const token =
    parseOpaqueToken(
      input.token,
    );

  const tokenHash =
    hashOpaqueToken(token);

  const userEmail =
    normalizeMemberEmail(
      input.user.email,
    );

  return withSerializableRetry(
    async (transaction) => {
      const invitation =
        await transaction
          .invitation
          .findFirst({
            where: {
              tokenHash,
              acceptedAt: null,
              revokedAt: null,

              expiresAt: {
                gt: new Date(),
              },

              organization: {
                status:
                  OrganizationStatus.ACTIVE,
              },
            },

            select: {
              id: true,
              organizationId: true,
              email: true,
              role: true,

              organization: {
                select: {
                  name: true,
                  slug: true,
                },
              },
            },
          });

      if (!invitation) {
        throw new DomainError({
          code:
            "invalid_or_expired_invitation",

          message:
            "The invitation is invalid or expired.",

          status: 400,
        });
      }

      if (
        normalizeMemberEmail(
          invitation.email,
        ) !== userEmail
      ) {
        throw new DomainError({
          code:
            "invitation_email_mismatch",

          message:
            "The invitation belongs to another email address.",

          status: 403,
        });
      }

      const existing =
        await transaction
          .membership
          .findUnique({
            where: {
              organizationId_userId: {
                organizationId:
                  invitation.organizationId,

                userId:
                  input.user.id,
              },
            },

            select: {
              id: true,
            },
          });

      const membership =
        existing
          ? await transaction
              .membership
              .update({
                where: {
                  id:
                    existing.id,
                },

                data: {
                  role:
                    invitation.role,

                  status:
                    MembershipStatus.ACTIVE,

                  suspendedAt: null,
                  revokedAt: null,
                },

                select: {
                  id: true,
                  role: true,
                  status: true,
                },
              })
          : await transaction
              .membership
              .create({
                data: {
                  organizationId:
                    invitation.organizationId,

                  userId:
                    input.user.id,

                  role:
                    invitation.role,

                  status:
                    MembershipStatus.ACTIVE,
                },

                select: {
                  id: true,
                  role: true,
                  status: true,
                },
              });

      await transaction
        .invitation
        .update({
          where: {
            id:
              invitation.id,
          },

          data: {
            acceptedAt:
              new Date(),

            acceptedByUserId:
              input.user.id,
          },
        });

      await transaction
        .invitation
        .updateMany({
          where: {
            organizationId:
              invitation.organizationId,

            email:
              invitation.email,

            id: {
              not:
                invitation.id,
            },

            acceptedAt: null,
            revokedAt: null,
          },

          data: {
            revokedAt:
              new Date(),
          },
        });

      await appendSecurityAuditEvent(
        transaction,
        {
          organizationId:
            invitation.organizationId,

          actorUserId:
            input.user.id,

          action:
            "invitation.accepted",

          targetType:
            "Invitation",

          targetId:
            invitation.id,

          metadata: {
            membershipId:
              membership.id,

            role:
              membership.role,
          },

          requestContext:
            input.requestContext,
        },
      );

      return {
        organization:
          invitation.organization,

        membership,
      };
    },
  );
}
