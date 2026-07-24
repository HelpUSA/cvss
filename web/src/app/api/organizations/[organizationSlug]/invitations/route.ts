import {
  mutationErrorResponse,
  mutationNotFound,
  mutationSuccess,
} from "@/lib/api-response";
import {
  createOrganizationInvitation,
} from "@/lib/invitation-lifecycle";
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

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

type RouteContext = {
  params: Promise<{
    organizationSlug: string;
  }>;
};

export async function POST(
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

    const invitation =
      await createOrganizationInvitation({
        context,

        actorUserId:
          currentSession.user.id,

        email:
          body.email,

        role:
          body.role,

        requestContext:
          getRequestAuditContext(
            request,
          ),
      });

    return mutationSuccess(
      {
        invitation,
      },
      201,
    );
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
