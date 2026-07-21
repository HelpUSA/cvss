import {
  mutationErrorResponse,
  mutationNotFound,
  mutationSuccess,
} from "@/lib/api-response";
import {
  assertJsonMutationRequest,
  getRequestAuditContext,
} from "@/lib/request-security";
import {
  getActiveSession,
} from "@/lib/session";
import {
  revokeUserSession,
} from "@/lib/session-administration";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

type RouteContext = {
  params: Promise<{
    sessionId: string;
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
      sessionId,
    } = await routeContext.params;

    const result =
      await revokeUserSession({
        userId:
          currentSession.user.id,

        currentSessionId:
          currentSession.session.id,

        sessionId,

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
