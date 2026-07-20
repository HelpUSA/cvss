import {
  MembershipRole,
} from "@prisma/client";

export const TENANT_PERMISSIONS = [
  "organization:read",
  "membership:read",
  "membership:manage",
  "project:read",
  "project:manage",
  "environment:read",
  "environment:manage",
  "analysis:execute",
  "decision:review",
] as const;

export type TenantPermission =
  (typeof TENANT_PERMISSIONS)[number];

const ROLE_PERMISSIONS: Record<
  MembershipRole,
  ReadonlySet<TenantPermission>
> = {
  [MembershipRole.ADMIN]:
    new Set<TenantPermission>(
      TENANT_PERMISSIONS,
    ),

  [MembershipRole.OPERATOR]:
    new Set<TenantPermission>([
      "organization:read",
      "project:read",
      "project:manage",
      "environment:read",
      "environment:manage",
      "analysis:execute",
    ]),

  [MembershipRole.REVIEWER]:
    new Set<TenantPermission>(),

  [MembershipRole.VIEWER]:
    new Set<TenantPermission>([
      "organization:read",
      "project:read",
      "environment:read",
    ]),
};

export function permissionsForRole(
  role: MembershipRole,
): readonly TenantPermission[] {
  return Array.from(
    ROLE_PERMISSIONS[role],
  );
}

export function hasTenantPermission(
  role: MembershipRole,
  permission: TenantPermission,
): boolean {
  return ROLE_PERMISSIONS[
    role
  ].has(permission);
}

export function roleLabel(
  role: MembershipRole,
): string {
  switch (role) {
    case MembershipRole.ADMIN:
      return "Administrador";

    case MembershipRole.OPERATOR:
      return "Operador";

    case MembershipRole.REVIEWER:
      return "Revisor reservado";

    case MembershipRole.VIEWER:
      return "Visualizador";
  }
}
