import { NextResponse } from "next/server";

import {
  resolveOrganizationContextForUser,
} from "@/lib/organization-context";
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

function notFoundResponse() {
  return NextResponse.json(
    {
      error: "not_found",
    },
    {
      status: 404,

      headers: {
        "Cache-Control":
          "private, no-store, max-age=0",
      },
    },
  );
}

export async function GET(
  _request: Request,
  routeContext: RouteContext,
) {
  const currentSession =
    await getActiveSession();

  if (!currentSession) {
    return notFoundResponse();
  }

  const {
    organizationSlug,
  } = await routeContext.params;

  const context =
    await resolveOrganizationContextForUser({
      userId: currentSession.user.id,
      organizationSlug,
      permission: "organization:read",
    });

  if (!context) {
    return notFoundResponse();
  }

  return NextResponse.json(
    {
      organization: {
        name: context.organization.name,
        slug: context.organization.slug,
      },

      membership: {
        role: context.membership.role,
      },
    },
    {
      status: 200,

      headers: {
        "Cache-Control":
          "private, no-store, max-age=0",
      },
    },
  );
}
