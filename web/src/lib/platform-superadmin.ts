import { normalizeEmail } from "@/lib/normalize-email";

const DEFAULT_PLATFORM_SUPERADMIN_EMAIL =
  "helpus.ecommerce@gmail.com";

export function canonicalPlatformSuperAdminEmail(): string {
  return normalizeEmail(
    process.env.PLATFORM_SUPERADMIN_EMAIL?.trim() ||
      DEFAULT_PLATFORM_SUPERADMIN_EMAIL,
  );
}

export function isCanonicalPlatformSuperAdminEmail(
  email: string | null | undefined,
): boolean {
  if (!email) {
    return false;
  }

  return normalizeEmail(email) ===
    canonicalPlatformSuperAdminEmail();
}
