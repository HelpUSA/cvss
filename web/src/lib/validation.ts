import {
  MembershipRole,
  MembershipStatus,
} from "@prisma/client";

import { DomainError } from "@/lib/domain-errors";
import {
  normalizeEmail,
} from "@/lib/normalize-email";

function requireString(
  value: unknown,
  field: string,
): string {
  if (typeof value !== "string") {
    throw new DomainError({
      code: "invalid_input",
      message: `${field} must be a string.`,
      status: 400,
    });
  }

  return value;
}

export function normalizeName(
  value: unknown,
  field = "name",
): string {
  const normalized = requireString(
    value,
    field,
  )
    .trim()
    .replace(/\s+/g, " ");

  if (
    normalized.length < 2 ||
    normalized.length > 120
  ) {
    throw new DomainError({
      code: "invalid_name",
      message:
        `${field} must contain between 2 and 120 characters.`,
      status: 400,
    });
  }

  return normalized;
}

export function normalizeSlug(
  value: unknown,
  field = "slug",
): string {
  const normalized = requireString(
    value,
    field,
  )
    .trim()
    .toLowerCase();

  if (
    normalized.length < 2 ||
    normalized.length > 80 ||
    !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(
      normalized,
    )
  ) {
    throw new DomainError({
      code: "invalid_slug",
      message:
        `${field} must use lowercase letters, numbers and internal hyphens.`,
      status: 400,
    });
  }

  return normalized;
}

export function normalizeId(
  value: unknown,
  field: string,
): string {
  const normalized = requireString(
    value,
    field,
  ).trim();

  if (
    normalized.length < 1 ||
    normalized.length > 128 ||
    !/^[A-Za-z0-9_-]+$/.test(normalized)
  ) {
    throw new DomainError({
      code: "invalid_identifier",
      message: `${field} is invalid.`,
      status: 400,
    });
  }

  return normalized;
}

export function normalizeMemberEmail(
  value: unknown,
): string {
  const normalized = normalizeEmail(
    requireString(value, "email"),
  );

  if (
    normalized.length < 3 ||
    normalized.length > 320 ||
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
      normalized,
    )
  ) {
    throw new DomainError({
      code: "invalid_email",
      message: "A valid email is required.",
      status: 400,
    });
  }

  return normalized;
}

export function parseMembershipRole(
  value: unknown,
): MembershipRole {
  if (
    typeof value !== "string" ||
    !Object.values(
      MembershipRole,
    ).includes(
      value as MembershipRole,
    )
  ) {
    throw new DomainError({
      code: "invalid_membership_role",
      message: "Membership role is invalid.",
      status: 400,
    });
  }

  return value as MembershipRole;
}

export function parseMembershipStatus(
  value: unknown,
): MembershipStatus {
  if (
    typeof value !== "string" ||
    !Object.values(
      MembershipStatus,
    ).includes(
      value as MembershipStatus,
    )
  ) {
    throw new DomainError({
      code: "invalid_membership_status",
      message: "Membership status is invalid.",
      status: 400,
    });
  }

  return value as MembershipStatus;
}
