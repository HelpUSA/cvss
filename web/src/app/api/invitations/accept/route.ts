import {
  mutationErrorResponse,
  mutationNotFound,
  mutationSuccess,
} from "@/lib/api-response";
import {
  acceptOrganizationInvitation,
} from "@/lib/invitation-lifecycle";
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

export async function POST(
  request: Request,
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

    const body =
      await readJsonObject(
        request,
      );

    const result =
      await acceptOrganizationInvitation({
        token:
          body.token,

        user: {
          id:
            currentSession.user.id,

          email:
            currentSession.user.email,
        },

        requestContext:
          getRequestAuditContext(
            request,
          ),
      });

    return mutationSuccess({
      accepted: true,
      organization:
        result.organization,
      membership:
        result.membership,
    });
  } catch (error) {
    return mutationErrorResponse(
      error,
    );
  }
}
