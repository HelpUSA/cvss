import {
  MembershipRole,
  MembershipStatus,
} from "@prisma/client";

import { DomainError } from "@/lib/domain-errors";

export type MembershipState = {
  role: MembershipRole;
  status: MembershipStatus;
};

export function isActiveAdmin(
  state: MembershipState,
): boolean {
  return (
    state.role ===
      MembershipRole.ADMIN &&
    state.status ===
      MembershipStatus.ACTIVE
  );
}

export function removesActiveAdmin(
  before: MembershipState,
  after: MembershipState,
): boolean {
  return (
    isActiveAdmin(before) &&
    !isActiveAdmin(after)
  );
}

export function assertLastActiveAdminInvariant(
  input: {
    before: MembershipState;
    after: MembershipState;
    activeAdminCount: number;
  },
): void {
  if (
    removesActiveAdmin(
      input.before,
      input.after,
    ) &&
    input.activeAdminCount <= 1
  ) {
    throw new DomainError({
      code: "last_active_admin",
      message:
        "The last active organization administrator cannot be removed, suspended, revoked or demoted.",
      status: 409,
    });
  }
}
