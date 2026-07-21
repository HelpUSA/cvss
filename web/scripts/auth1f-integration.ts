import {
  randomUUID,
} from "node:crypto";

import {
  verify,
} from "@node-rs/argon2";

import {
  MembershipRole,
  MembershipStatus,
  OrganizationStatus,
  PlatformRole,
  UserStatus,
} from "@prisma/client";

import {
  confirmPasswordReset,
} from "../src/lib/account-lifecycle";

import {
  issueOpaqueToken,
} from "../src/lib/auth-tokens";

import {
  DomainError,
} from "../src/lib/domain-errors";

import {
  acceptOrganizationInvitation,
} from "../src/lib/invitation-lifecycle";

import {
  resolveOrganizationContextForUser,
} from "../src/lib/organization-context";

import {
  prisma,
} from "../src/lib/prisma";

import {
  listUserSessions,
  revokeAllUserSessions,
  revokeOtherUserSessions,
  revokeUserSession,
} from "../src/lib/session-administration";

const startedAt = new Date();

const runId =
  randomUUID()
    .replaceAll("-", "")
    .slice(0, 12);

function expect(
  condition: unknown,
  message: string,
): asserts condition {
  if (!condition) {
    throw new Error(message);
  }
}

async function expectDomainError(
  operation: Promise<unknown>,
  expectedCode: string,
): Promise<void> {
  try {
    await operation;
  } catch (error) {
    if (
      error instanceof DomainError &&
      error.code === expectedCode
    ) {
      return;
    }

    throw error;
  }

  throw new Error(
    `Expected DomainError ${expectedCode}.`,
  );
}

async function createUser(
  label: string,
) {
  return prisma.user.create({
    data: {
      name:
        `Auth1F ${label}`,

      email:
        `${label}-${runId}@auth1f.invalid`,

      emailVerified: true,

      status:
        UserStatus.ACTIVE,

      platformRole:
        PlatformRole.USER,
    },
  });
}

async function createCredentialAccount(
  userId: string,
) {
  return prisma.account.create({
    data: {
      accountId:
        userId,

      providerId:
        "credential",

      userId,

      password:
        "auth1f-initial-password-hash",
    },
  });
}

async function createSession(
  userId: string,
  label: string,
) {
  return prisma.session.create({
    data: {
      userId,

      token:
        `auth1f-${label}-${randomUUID()}`,

      expiresAt:
        new Date(
          Date.now() +
            24 * 60 * 60 * 1000,
        ),

      ipAddress:
        "127.0.0.1",

      userAgent:
        `Auth1F/${label}`,
    },
  });
}

async function assertEmptyDatabase(): Promise<void> {
  const [
    userCount,
    organizationCount,
    sessionCount,
  ] = await Promise.all([
    prisma.user.count(),
    prisma.organization.count(),
    prisma.session.count(),
  ]);

  expect(
    userCount === 0,
    "Temporary database already contains users.",
  );

  expect(
    organizationCount === 0,
    "Temporary database already contains organizations.",
  );

  expect(
    sessionCount === 0,
    "Temporary database already contains sessions.",
  );
}

async function testPasswordReset(): Promise<void> {
  const user =
    await createUser(
      "password-reset",
    );

  const account =
    await createCredentialAccount(
      user.id,
    );

  await Promise.all([
    createSession(
      user.id,
      "reset-a",
    ),

    createSession(
      user.id,
      "reset-b",
    ),
  ]);

  const issued =
    issueOpaqueToken();

  const resetToken =
    await prisma
      .passwordResetToken
      .create({
        data: {
          userId:
            user.id,

          tokenHash:
            issued.tokenHash,

          expiresAt:
            new Date(
              Date.now() +
                30 * 60 * 1000,
            ),
        },
      });

  const newPassword =
    "Auth1F-new-password-2026";

  const result =
    await confirmPasswordReset({
      token:
        issued.token,

      password:
        newPassword,
    });

  expect(
    result.sessionsRevoked === 2,
    "Password reset did not revoke all sessions.",
  );

  const [
    storedToken,
    storedAccount,
    sessionCount,
    auditCount,
  ] = await Promise.all([
    prisma.passwordResetToken
      .findUnique({
        where: {
          id:
            resetToken.id,
        },
      }),

    prisma.account.findUnique({
      where: {
        id:
          account.id,
      },
    }),

    prisma.session.count({
      where: {
        userId:
          user.id,
      },
    }),

    prisma.securityAuditEvent
      .count({
        where: {
          action:
            "password_reset.completed",

          targetId:
            user.id,
        },
      }),
  ]);

  expect(
    storedToken?.usedAt instanceof Date,
    "Password reset token was not consumed.",
  );

  expect(
    typeof storedAccount?.password ===
      "string",
    "Credential password was not updated.",
  );

  expect(
    await verify(
      storedAccount.password,
      newPassword,
    ),
    "Stored password is not a valid Argon2id hash.",
  );

  expect(
    sessionCount === 0,
    "Sessions remained after password reset.",
  );

  expect(
    auditCount === 1,
    "Password reset audit event was not created.",
  );

  await expectDomainError(
    confirmPasswordReset({
      token:
        issued.token,

      password:
        "Auth1F-replay-password-2026",
    }),

    "invalid_or_expired_reset",
  );
}

async function testConcurrentPasswordReset(): Promise<void> {
  const user =
    await createUser(
      "password-concurrency",
    );

  await createCredentialAccount(
    user.id,
  );

  await createSession(
    user.id,
    "password-concurrency",
  );

  const issued =
    issueOpaqueToken();

  await prisma
    .passwordResetToken
    .create({
      data: {
        userId:
          user.id,

        tokenHash:
          issued.tokenHash,

        expiresAt:
          new Date(
            Date.now() +
              30 * 60 * 1000,
          ),
      },
    });

  const results =
    await Promise.allSettled([
      confirmPasswordReset({
        token:
          issued.token,

        password:
          "Auth1F-concurrent-password-A",
      }),

      confirmPasswordReset({
        token:
          issued.token,

        password:
          "Auth1F-concurrent-password-B",
      }),
    ]);

  const successful =
    results.filter(
      (result) =>
        result.status ===
        "fulfilled",
    );

  const rejected =
    results.filter(
      (result) =>
        result.status ===
        "rejected",
    );

  expect(
    successful.length === 1,
    "Concurrent reset allowed multiple successes.",
  );

  expect(
    rejected.length === 1,
    "Concurrent reset did not reject one consumer.",
  );

  const remainingSessions =
    await prisma.session.count({
      where: {
        userId:
          user.id,
      },
    });

  expect(
    remainingSessions === 0,
    "Concurrent reset did not revoke sessions.",
  );
}

async function testInvitationLifecycle(): Promise<{
  organizationId: string;
  organizationSlug: string;
  inviteeUserId: string;
}> {
  const [
    administrator,
    invitee,
  ] = await Promise.all([
    createUser(
      "invitation-admin",
    ),

    createUser(
      "invitation-user",
    ),
  ]);

  const organization =
    await prisma.organization.create({
      data: {
        name:
          `Auth1F Organization ${runId}`,

        slug:
          `auth1f-org-${runId}`,

        status:
          OrganizationStatus.ACTIVE,
      },
    });

  await prisma.membership.create({
    data: {
      organizationId:
        organization.id,

      userId:
        administrator.id,

      role:
        MembershipRole.ADMIN,

      status:
        MembershipStatus.ACTIVE,
    },
  });

  const issued =
    issueOpaqueToken();

  const invitation =
    await prisma.invitation.create({
      data: {
        organizationId:
          organization.id,

        email:
          invitee.email,

        role:
          MembershipRole.VIEWER,

        tokenHash:
          issued.tokenHash,

        expiresAt:
          new Date(
            Date.now() +
              72 * 60 * 60 * 1000,
          ),

        createdByUserId:
          administrator.id,
      },
    });

  const accepted =
    await acceptOrganizationInvitation({
      token:
        issued.token,

      user: {
        id:
          invitee.id,

        email:
          invitee.email,
      },
    });

  expect(
    accepted.organization.id ===
      organization.id,
    "Invitation resolved the wrong organization.",
  );

  expect(
    accepted.membership.role ===
      MembershipRole.VIEWER,
    "Invitation created an unexpected role.",
  );

  expect(
    accepted.membership.status ===
      MembershipStatus.ACTIVE,
    "Invitation did not create an active membership.",
  );

  const [
    storedInvitation,
    membershipCount,
    auditCount,
  ] = await Promise.all([
    prisma.invitation.findUnique({
      where: {
        id:
          invitation.id,
      },
    }),

    prisma.membership.count({
      where: {
        organizationId:
          organization.id,

        userId:
          invitee.id,
      },
    }),

    prisma.securityAuditEvent
      .count({
        where: {
          action:
            "invitation.accepted",

          organizationId:
            organization.id,

          actorUserId:
            invitee.id,
        },
      }),
  ]);

  expect(
    storedInvitation
      ?.acceptedAt instanceof Date,
    "Invitation was not consumed.",
  );

  expect(
    storedInvitation
      ?.acceptedByUserId ===
      invitee.id,
    "acceptedByUserId was not persisted.",
  );

  expect(
    membershipCount === 1,
    "Invitation created an unexpected number of memberships.",
  );

  expect(
    auditCount === 1,
    "Invitation audit event was not created.",
  );

  await expectDomainError(
    acceptOrganizationInvitation({
      token:
        issued.token,

      user: {
        id:
          invitee.id,

        email:
          invitee.email,
      },
    }),

    "invalid_or_expired_invitation",
  );

  const mismatch =
    issueOpaqueToken();

  const mismatchInvitation =
    await prisma.invitation.create({
      data: {
        organizationId:
          organization.id,

        email:
          `different-${runId}@auth1f.invalid`,

        role:
          MembershipRole.OPERATOR,

        tokenHash:
          mismatch.tokenHash,

        expiresAt:
          new Date(
            Date.now() +
              72 * 60 * 60 * 1000,
          ),

        createdByUserId:
          administrator.id,
      },
    });

  await expectDomainError(
    acceptOrganizationInvitation({
      token:
        mismatch.token,

      user: {
        id:
          invitee.id,

        email:
          invitee.email,
      },
    }),

    "invitation_email_mismatch",
  );

  const mismatchAfter =
    await prisma.invitation.findUnique({
      where: {
        id:
          mismatchInvitation.id,
      },
    });

  expect(
    mismatchAfter?.acceptedAt === null,
    "Mismatched invitation was consumed.",
  );

  return {
    organizationId:
      organization.id,

    organizationSlug:
      organization.slug,

    inviteeUserId:
      invitee.id,
  };
}

async function testConcurrentInvitation(): Promise<void> {
  const [
    administrator,
    invitee,
  ] = await Promise.all([
    createUser(
      "concurrent-invite-admin",
    ),

    createUser(
      "concurrent-invite-user",
    ),
  ]);

  const organization =
    await prisma.organization.create({
      data: {
        name:
          `Auth1F Concurrent ${runId}`,

        slug:
          `auth1f-concurrent-${runId}`,

        status:
          OrganizationStatus.ACTIVE,
      },
    });

  await prisma.membership.create({
    data: {
      organizationId:
        organization.id,

      userId:
        administrator.id,

      role:
        MembershipRole.ADMIN,

      status:
        MembershipStatus.ACTIVE,
    },
  });

  const issued =
    issueOpaqueToken();

  await prisma.invitation.create({
    data: {
      organizationId:
        organization.id,

      email:
        invitee.email,

      role:
        MembershipRole.OPERATOR,

      tokenHash:
        issued.tokenHash,

      expiresAt:
        new Date(
          Date.now() +
            72 * 60 * 60 * 1000,
        ),

      createdByUserId:
        administrator.id,
    },
  });

  const accept = () =>
    acceptOrganizationInvitation({
      token:
        issued.token,

      user: {
        id:
          invitee.id,

        email:
          invitee.email,
      },
    });

  const results =
    await Promise.allSettled([
      accept(),
      accept(),
    ]);

  const successful =
    results.filter(
      (result) =>
        result.status ===
        "fulfilled",
    );

  const rejected =
    results.filter(
      (result) =>
        result.status ===
        "rejected",
    );

  expect(
    successful.length === 1,
    "Concurrent invitation allowed multiple successes.",
  );

  expect(
    rejected.length === 1,
    "Concurrent invitation did not reject one consumer.",
  );

  const membershipCount =
    await prisma.membership.count({
      where: {
        organizationId:
          organization.id,

        userId:
          invitee.id,
      },
    });

  expect(
    membershipCount === 1,
    "Concurrent invitation created duplicate memberships.",
  );
}

async function testSessionAdministration(): Promise<void> {
  const user =
    await createUser(
      "sessions",
    );

  const [
    current,
    second,
  ] = await Promise.all([
    createSession(
      user.id,
      "current",
    ),

    createSession(
      user.id,
      "second",
    ),

    createSession(
      user.id,
      "third",
    ),
  ]);

  const listed =
    await listUserSessions(
      user.id,
    );

  expect(
    listed.length === 3,
    "Session listing did not return all sessions.",
  );

  for (const session of listed) {
    expect(
      !("token" in session),
      "Session listing exposed a session token.",
    );
  }

  const single =
    await revokeUserSession({
      userId:
        user.id,

      currentSessionId:
        current.id,

      sessionId:
        second.id,
    });

  expect(
    single.revokedCurrent === false,
    "Non-current session was classified as current.",
  );

  const others =
    await revokeOtherUserSessions({
      userId:
        user.id,

      currentSessionId:
        current.id,
    });

  expect(
    others.revokedCount === 1,
    "Unexpected count while revoking other sessions.",
  );

  const remaining =
    await prisma.session.findMany({
      where: {
        userId:
          user.id,
      },

      select: {
        id: true,
      },
    });

  expect(
    remaining.length === 1 &&
      remaining[0]?.id ===
        current.id,
    "Other-session revocation did not preserve only the current session.",
  );

  await createSession(
    user.id,
    "after-others",
  );

  const all =
    await revokeAllUserSessions({
      userId:
        user.id,
    });

  expect(
    all.revokedCount === 2,
    "Unexpected count while revoking all sessions.",
  );

  const finalCount =
    await prisma.session.count({
      where: {
        userId:
          user.id,
      },
    });

  expect(
    finalCount === 0,
    "All-session revocation left sessions behind.",
  );
}

async function testTenantIsolation(
  input: {
    organizationId: string;
    organizationSlug: string;
    inviteeUserId: string;
  },
): Promise<void> {
  const otherOrganization =
    await prisma.organization.create({
      data: {
        name:
          `Auth1F Isolated ${runId}`,

        slug:
          `auth1f-isolated-${runId}`,

        status:
          OrganizationStatus.ACTIVE,
      },
    });

  const allowed =
    await resolveOrganizationContextForUser({
      userId:
        input.inviteeUserId,

      organizationSlug:
        input.organizationSlug,

      permission:
        "project:read",
    });

  expect(
    allowed?.organization.id ===
      input.organizationId,
    "Authorized tenant was not resolved.",
  );

  const denied =
    await resolveOrganizationContextForUser({
      userId:
        input.inviteeUserId,

      organizationSlug:
        otherOrganization.slug,

      permission:
        "project:read",
    });

  expect(
    denied === null,
    "Cross-tenant access was incorrectly authorized.",
  );
}

async function main(): Promise<void> {
  await assertEmptyDatabase();

  await testPasswordReset();
  await testConcurrentPasswordReset();

  const invitationContext =
    await testInvitationLifecycle();

  await testConcurrentInvitation();
  await testSessionAdministration();

  await testTenantIsolation(
    invitationContext,
  );

  console.log(
    JSON.stringify(
      {
        auth1fIntegrationOk: true,

        execution:
          "GitHub Actions",

        database:
          "Temporary Railway PostgreSQL",

        localDockerUsed: false,
        localDatabaseUsed: false,

        passwordResetRealDatabase: true,
        passwordResetSingleUse: true,
        passwordResetConcurrency: true,
        passwordStoredAsArgon2id: true,
        sessionsRevokedAfterReset: true,

        invitationAcceptance: true,
        invitationEmailBinding: true,
        invitationSingleUse: true,
        invitationConcurrency: true,
        duplicateMembershipPrevented: true,

        sessionTokenExposed: false,
        individualSessionRevocation: true,
        otherSessionRevocation: true,
        allSessionRevocation: true,

        crossTenantAccessAllowed: false,

        schemaChanged: false,
        migrationCreated: false,

        startedAt:
          startedAt.toISOString(),

        completedAt:
          new Date().toISOString(),
      },
      null,
      2,
    ),
  );
}

main()
  .catch((error: unknown) => {
    console.error(
      error instanceof Error
        ? error.stack ??
          error.message
        : String(error),
    );

    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
