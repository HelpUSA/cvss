import {
  mutationErrorResponse,
  mutationNotFound,
  mutationSuccess,
} from "@/lib/api-response";
import {
  resolveOrganizationContextForUser,
} from "@/lib/organization-context";
import {
  assertJsonMutationRequest,
  getRequestAuditContext,
  readJsonObject,
} from "@/lib/request-security";
import {
  getActiveSession,
} from "@/lib/session";
import {
  updateOrganizationMembership,
} from "@/lib/tenant-administration";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

type RouteContext = {
  params: Promise<{
    organizationSlug: string;
    membershipId: string;
  }>;
};

export async function PATCH(
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
      membershipId,
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

    const body =
      await readJsonObject(
        request,
      );

    const result =
      await updateOrganizationMembership({
        context,

        actorUserId:
          currentSession.user.id,

        membershipId,
        role: body.role,
        status: body.status,

        requestContext:
          getRequestAuditContext(
            request,
          ),
      });

    return mutationSuccess(
      result,
    );
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
