process.env.BETTER_AUTH_SECRET = process.env.BETTER_AUTH_SECRET || "test-secret-at-least-32-chars-long-for-route-tests!";
process.env.BETTER_AUTH_URL = process.env.BETTER_AUTH_URL || "http://localhost:3000";
process.env.DATABASE_URL = process.env.DATABASE_URL || "postgresql://mock:mock@localhost:5432/mock";

import assert from "assert";
import crypto from "crypto";
import { NextRequest } from "next/server";
import fs from "fs";
import path from "path";

async function main() {
  const { prisma } = await import("../src/lib/prisma");

  // Mock prisma.user to return authoritative platformRole and status
  (prisma as any).user = {
    findUnique: async ({ where }: any) => {
      if (where.id === "admin-master-1") {
        return { id: "admin-master-1", platformRole: "PLATFORM_ADMIN", status: "ACTIVE" };
      }
      if (where.id === "admin-suspended-1") {
        return { id: "admin-suspended-1", platformRole: "PLATFORM_ADMIN", status: "SUSPENDED" };
      }
      if (where.id === "admin-disabled-1") {
        return { id: "admin-disabled-1", platformRole: "PLATFORM_ADMIN", status: "DISABLED" };
      }
      if (where.id === "admin-missing-1") {
        return null;
      }
      return { id: where.id, platformRole: "USER", status: "ACTIVE" };
    },
  };
  let revokedSessionUserId: string | null = null;
  (prisma as any).session = {
    deleteMany: async ({ where }: any) => {
      revokedSessionUserId = where?.userId || null;
      return { count: 1 };
    },
  };

  const { POST } = await import("../src/app/api/review/decision/route");
  const { auth } = await import("../src/lib/auth");

  // Track Prisma create calls for integration assertions
  let lastPersistedEvent: any = null;
  (prisma as any).securityAuditEvent = {
    create: async ({ data }: any) => {
      lastPersistedEvent = data;
      return { id: "audit_evt_123", ...data, createdAt: new Date() };
    },
  };

  // Mock auth.api.getSession to simulate authentications
  let mockSession: any = null;

  (auth.api as any).getSession = async () => {
    return mockSession;
  };
  console.log("============================================================");
  console.log("HelpUS CVSS AI — HITL Review Decision Route Security Tests");
  console.log("============================================================");

  function req(body: any) {
    return new NextRequest("http://localhost:3000/api/review/decision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  }

  const results: any[] = [];
  const check = (name: string, passed: boolean, details: any = {}) => {
    results.push({ name, passed, ...details });
    if (!passed) {
      console.error(`  [FAIL] ${name}`, details);
    } else {
      console.log(`  [PASS] ${name}`);
    }
  };

  // 1. Unauthenticated request must fail closed with HTTP 401
  mockSession = null;
  const r1 = await POST(req({ assessmentId: "asm-1", decision: "APPROVED", rationale: "Valid rationale for test" }));
  const d1 = await r1.json();
  check("1. Unauthenticated -> HTTP 401", r1.status === 401 && d1.code === "UNAUTHENTICATED");

  // 2. Authenticated user with role USER (non-PLATFORM_ADMIN) must fail closed with HTTP 403
  mockSession = {
    user: {
      id: "usr-regular-1",
      email: "analista@empresa.com",
      name: "Regular Analyst",
      platformRole: "USER",
    },
  };
  const r2 = await POST(req({ assessmentId: "asm-1", decision: "APPROVED", rationale: "Valid rationale for test" }));
  const d2 = await r2.json();
  check("2. Non-PLATFORM_ADMIN authenticated user -> HTTP 403 FORBIDDEN", r2.status === 403 && d2.code === "FORBIDDEN_NOT_PLATFORM_ADMIN");

  // 3. Authenticated PLATFORM_ADMIN with missing assessmentId -> HTTP 400
  mockSession = {
    user: {
      id: "admin-master-1",
      email: "master@helpusbr.com",
      name: "Master Platform Admin",
      platformRole: "PLATFORM_ADMIN",
    },
  };
  const r3 = await POST(req({ decision: "APPROVED", rationale: "Valid rationale for test" }));
  const d3 = await r3.json();
  check("3. Missing assessmentId -> HTTP 400", r3.status === 400 && d3.code === "INVALID_ASSESSMENT_ID");

  // 4. Authenticated PLATFORM_ADMIN with invalid decision -> HTTP 400
  const r4 = await POST(req({ assessmentId: "asm-1", decision: "MAYBE", rationale: "Valid rationale for test" }));
  const d4 = await r4.json();
  check("4. Invalid decision string -> HTTP 400", r4.status === 400 && d4.code === "INVALID_DECISION");

  // 5. Authenticated PLATFORM_ADMIN with missing/short rationale (<10 chars) -> HTTP 400
  const r5 = await POST(req({ assessmentId: "asm-1", decision: "APPROVED", rationale: "short" }));
  const d5 = await r5.json();
  check("5. Short rationale (<10 chars) -> HTTP 400", r5.status === 400 && d5.code === "INVALID_RATIONALE");

  // 6. Missing policy provenance fields must fail closed (NO silent fabricated defaults) -> HTTP 400
  const r6a = await POST(
    req({
      assessmentId: "asm-pci-prod-001",
      decision: "APPROVED",
      rationale: "Topologia verificada em conformidade com isolamento de rede PCI-DSS e regras de firewall ativas.",
    })
  );
  const d6a = await r6a.json();
  check(
    "6. Missing policy binding -> HTTP 400 (no fabricated defaults)",
    r6a.status === 400 && d6a.code === "MISSING_POLICY_BINDING"
  );

  // 7. Authenticated PLATFORM_ADMIN with valid APPROVED payload -> HTTP 200 with JCS receipt and Prisma mutation
  lastPersistedEvent = null;
  const validApprovedPayload = {
    assessmentId: "asm-pci-prod-001",
    decision: "APPROVED",
    rationale: "Topologia verificada em conformidade com isolamento de rede PCI-DSS e regras de firewall ativas.",
    organizationPolicyId: "pci-segmented-prod",
    policyVersion: "2.1.0",
    rulesetVersion: "1.0.0",
    calculatorVersion: "0.2.0-aligned-first-cvss40",
  };
  const r7 = await POST(req(validApprovedPayload));
  const d7 = await r7.json();
  const sha7 = crypto.createHash("sha256").update(d7.receiptCanonicalJcs || "", "utf8").digest("hex");
  check(
    "7. PLATFORM_ADMIN APPROVED -> HTTP 200 with valid receipt and hash",
    r7.status === 200 &&
      d7.success === true &&
      d7.decision === "APPROVED" &&
      d7.receipt?.reviewer?.role === "PLATFORM_ADMIN" &&
      d7.receipt?.policyBinding?.organizationPolicyId === "pci-segmented-prod" &&
      d7.receiptHashSha256 === sha7 &&
      lastPersistedEvent !== null &&
      lastPersistedEvent.action === "HITL_REVIEW_APPROVED" &&
      lastPersistedEvent.targetId === "asm-pci-prod-001"
  );

  // 8. Authenticated PLATFORM_ADMIN with valid REJECTED payload -> HTTP 200 with REJECTED receipt and Prisma mutation
  lastPersistedEvent = null;
  const validRejectedPayload = {
    assessmentId: "asm-pci-prod-002",
    decision: "REJECTED",
    rationale: "Evidência de firewall insuficiente para justificar atenuação de vetor ambiental MAV.",
    organizationPolicyId: "pci-segmented-prod",
    policyVersion: "2.1.0",
    rulesetVersion: "1.0.0",
    calculatorVersion: "0.2.0-aligned-first-cvss40",
  };
  const r8 = await POST(req(validRejectedPayload));
  const d8 = await r8.json();
  const sha8 = crypto.createHash("sha256").update(d8.receiptCanonicalJcs || "", "utf8").digest("hex");
  check(
    "8. PLATFORM_ADMIN REJECTED -> HTTP 200 with valid receipt and hash",
    r8.status === 200 &&
      d8.success === true &&
      d8.decision === "REJECTED" &&
      d8.receipt?.reviewer?.role === "PLATFORM_ADMIN" &&
      d8.receiptHashSha256 === sha8 &&
      lastPersistedEvent !== null &&
      lastPersistedEvent.action === "HITL_REVIEW_REJECTED" &&
      lastPersistedEvent.targetId === "asm-pci-prod-002"
  );

  // 9. Database lookup failure -> HTTP 503 fail-closed (Blocker A verification)
  (prisma as any).user.findUnique = async () => {
    throw new Error("Simulated database connection failure");
  };
  const r9 = await POST(req(validApprovedPayload));
  const d9 = await r9.json();
  check(
    "9. Database lookup failure -> HTTP 503 fail-closed",
    r9.status === 503 && d9.code === "DATABASE_LOOKUP_FAILURE"
  );

  // Restore working prisma.user.findUnique
  (prisma as any).user.findUnique = async ({ where }: any) => {
    if (where.id === "admin-master-1") {
      return { id: "admin-master-1", platformRole: "PLATFORM_ADMIN", status: "ACTIVE" };
    }
    if (where.id === "admin-suspended-1") {
      return { id: "admin-suspended-1", platformRole: "PLATFORM_ADMIN", status: "SUSPENDED" };
    }
    if (where.id === "admin-disabled-1") {
      return { id: "admin-disabled-1", platformRole: "PLATFORM_ADMIN", status: "DISABLED" };
    }
    if (where.id === "admin-missing-1") {
      return null;
    }
    return { id: where.id, platformRole: "USER", status: "ACTIVE" };
  };

  // 10. Audit event persistence failure -> HTTP 500 fail-closed (Blocker B verification)
  (prisma as any).securityAuditEvent.create = async () => {
    throw new Error("Simulated audit disk write failure");
  };
  const r10 = await POST(req(validApprovedPayload));
  const d10 = await r10.json();
  check(
    "10. Security audit event persistence failure -> HTTP 500 fail-closed",
    r10.status === 500 && d10.code === "DURABLE_PERSISTENCE_FAILED"
  );

  // Restore working securityAuditEvent.create
  (prisma as any).securityAuditEvent.create = async ({ data }: any) => {
    lastPersistedEvent = data;
    return { id: "audit_evt_123", ...data, createdAt: new Date() };
  };

  // 11. Suspended PLATFORM_ADMIN user -> HTTP 403 fail-closed (FORBIDDEN_USER_NOT_ACTIVE)
  lastPersistedEvent = null;
  revokedSessionUserId = null;
  mockSession = {
    user: {
      id: "admin-suspended-1",
      email: "suspended.admin@helpusbr.com",
      name: "Suspended Admin",
      platformRole: "PLATFORM_ADMIN",
    },
  };
  const r11 = await POST(req(validApprovedPayload));
  const d11 = await r11.json();
  check(
    "11. Suspended PLATFORM_ADMIN -> HTTP 403 fail-closed, session revoked, zero persistence",
    r11.status === 403 &&
      d11.code === "FORBIDDEN_USER_NOT_ACTIVE" &&
      d11.currentUserStatus === "SUSPENDED" &&
      revokedSessionUserId === "admin-suspended-1" &&
      lastPersistedEvent === null
  );

  // 12. Disabled PLATFORM_ADMIN user -> HTTP 403 fail-closed (FORBIDDEN_USER_NOT_ACTIVE)
  lastPersistedEvent = null;
  revokedSessionUserId = null;
  mockSession = {
    user: {
      id: "admin-disabled-1",
      email: "disabled.admin@helpusbr.com",
      name: "Disabled Admin",
      platformRole: "PLATFORM_ADMIN",
    },
  };
  const r12 = await POST(req(validApprovedPayload));
  const d12 = await r12.json();
  check(
    "12. Disabled PLATFORM_ADMIN -> HTTP 403 fail-closed, session revoked, zero persistence",
    r12.status === 403 &&
      d12.code === "FORBIDDEN_USER_NOT_ACTIVE" &&
      d12.currentUserStatus === "DISABLED" &&
      revokedSessionUserId === "admin-disabled-1" &&
      lastPersistedEvent === null
  );

  // 13. Missing authoritative user in DB -> HTTP 403 fail-closed (FORBIDDEN_USER_NOT_ACTIVE)
  lastPersistedEvent = null;
  revokedSessionUserId = null;
  mockSession = {
    user: {
      id: "admin-missing-1",
      email: "ghost.admin@helpusbr.com",
      name: "Ghost Admin",
      platformRole: "PLATFORM_ADMIN",
    },
  };
  const r13 = await POST(req(validApprovedPayload));
  const d13 = await r13.json();
  check(
    "13. Missing authoritative user in DB -> HTTP 403 fail-closed, session revoked, zero persistence",
    r13.status === 403 &&
      d13.code === "FORBIDDEN_USER_NOT_ACTIVE" &&
      d13.currentUserStatus === "NOT_FOUND" &&
      revokedSessionUserId === "admin-missing-1" &&
      lastPersistedEvent === null
  );

  const total = results.length;
  const passed = results.filter((r) => r.passed).length;
  console.log(`\nResultado: ${passed}/${total} testes de segurança aprovados.`);

  // Write machine-readable evidence
  const outDir = path.resolve(__dirname, "../../outputs");
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(
    path.join(outDir, "hitl-review-decision-security-tests.json"),
    JSON.stringify({ timestamp: new Date().toISOString(), total, passed, results }, null, 2),
    "utf8"
  );

  if (passed !== total) {
    process.exit(1);
  }
}

main().catch((err) => {
  console.error("Test execution failed:", err);
  process.exit(1);
});
