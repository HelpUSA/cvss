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
  revokeAllUserSessions,
} from "@/lib/session-administration";

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

    const result =
      await revokeAllUserSessions({
        userId:
          currentSession.user.id,

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
