import {
  mutationErrorResponse,
  mutationNotFound,
  mutationSuccess,
} from "@/lib/api-response";
import {
  revokeOrganizationInvitation,
} from "@/lib/invitation-lifecycle";
import {
  resolveOrganizationContextForUser,
} from "@/lib/organization-context";
import {
  assertJsonMutationRequest,
  getRequestAuditContext,
} from "@/lib/request-security";
import {
  getActiveSession,
} from "@/lib/session";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

type RouteContext = {
  params: Promise<{
    organizationSlug: string;
    invitationId: string;
  }>;
};

export async function DELETE(
  request: Request,
  routeContext: RouteContext,
) {
  try {
    assertJsonMutationRequest(
      request,
    );

    const currentSession =
      await getActiveSession();

    if (!currentSession) {
      return mutationNotFound();
    }

    const {
      organizationSlug,
      invitationId,
    } = await routeContext.params;

    const context =
      await resolveOrganizationContextForUser({
        userId:
          currentSession.user.id,

        organizationSlug,

        permission:
          "membership:manage",
      });

    if (!context) {
      return mutationNotFound();
    }

    const invitation =
      await revokeOrganizationInvitation({
        context,

        actorUserId:
          currentSession.user.id,

        invitationId,

        requestContext:
          getRequestAuditContext(
            request,
          ),
      });

    return mutationSuccess({
      invitation,
    });
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
