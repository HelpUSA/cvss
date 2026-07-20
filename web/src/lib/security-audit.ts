import type {
  Prisma,
} from "@prisma/client";

import type {
  RequestAuditContext,
} from "@/lib/request-security";

export type SecurityAuditInput = {
  organizationId?: string;
  actorUserId: string;
  action: string;
  targetType?: string;
  targetId?: string;
  metadata?: Prisma.InputJsonObject;
  requestContext?: RequestAuditContext;
};

export async function appendSecurityAuditEvent(
  transaction: Prisma.TransactionClient,
  input: SecurityAuditInput,
): Promise<void> {
  await transaction
    .securityAuditEvent
    .create({
      data: {
        organizationId:
          input.organizationId,

        actorUserId:
          input.actorUserId,

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
