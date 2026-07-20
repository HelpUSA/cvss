import { headers } from "next/headers";
import { redirect } from "next/navigation";

import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

export async function getActiveSession() {
  const currentSession = await auth.api.getSession({
    headers: await headers(),
  });

  if (!currentSession) {
    return null;
  }

  const authoritativeUser =
    await prisma.user.findUnique({
      where: {
        id: currentSession.user.id,
      },

      select: {
        status: true,
        platformRole: true,
      },
    });

  if (
    !authoritativeUser ||
    authoritativeUser.status !== "ACTIVE"
  ) {
    await prisma.session.deleteMany({
      where: {
        userId: currentSession.user.id,
      },
    });

    return null;
  }

  return {
    ...currentSession,

    user: {
      ...currentSession.user,
      status: "ACTIVE" as const,
      platformRole:
        authoritativeUser.platformRole,
    },
  };
}

export async function requireActiveSession() {
  const currentSession =
    await getActiveSession();

  if (!currentSession) {
    redirect(
      "/login?reason=session-required",
    );
  }

  return currentSession;
}
