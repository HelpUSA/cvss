import {
  mutationNotFound,
  mutationSuccess,
} from "@/lib/api-response";
import {
  isActivePlatformAdmin,
} from "@/lib/platform-administration";
import {
  listPlatformUsers,
} from "@/lib/platform-user-administration";
import {
  getActiveSession,
} from "@/lib/session";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function GET() {
  const currentSession =
    await getActiveSession();

  if (!currentSession) {
    return mutationNotFound();
  }

  const permitted =
    await isActivePlatformAdmin(
      currentSession.user.id,
    );

  if (!permitted) {
    return mutationNotFound();
  }

  const users =
    await listPlatformUsers();

  return mutationSuccess({
    users,
  });
}
