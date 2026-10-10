process.env.BETTER_AUTH_SECRET = process.env.BETTER_AUTH_SECRET || "test-secret-at-least-32-chars-long-for-route-tests!";
process.env.BETTER_AUTH_URL = process.env.BETTER_AUTH_URL || "http://localhost:3000";

import assert from "assert";
import crypto from "crypto";
import { NextRequest } from "next/server";
import fs from "fs";
import path from "path";

async function main() {
  const { POST } = await import("../src/app/api/review/decision/route");
  const { auth } = await import("../src/lib/auth");

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

  // 2. Authenticated user with role USER (non-superadmin) must fail closed with HTTP 403
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
  check("2. Non-SuperAdmin authenticated user -> HTTP 403 FORBIDDEN", r2.status === 403 && d2.code === "FORBIDDEN_NOT_SUPERADMIN");

  // 3. Authenticated SuperAdmin with missing assessmentId -> HTTP 400
  mockSession = {
    user: {
      id: "admin-master-1",
      email: "master@helpusbr.com",
      name: "Master SuperAdmin",
      platformRole: "SUPERADMIN",
    },
  };
  const r3 = await POST(req({ decision: "APPROVED", rationale: "Valid rationale for test" }));
  const d3 = await r3.json();
  check("3. Missing assessmentId -> HTTP 400", r3.status === 400 && d3.code === "INVALID_ASSESSMENT_ID");

  // 4. Authenticated SuperAdmin with invalid decision -> HTTP 400
  const r4 = await POST(req({ assessmentId: "asm-1", decision: "MAYBE", rationale: "Valid rationale for test" }));
  const d4 = await r4.json();
  check("4. Invalid decision string -> HTTP 400", r4.status === 400 && d4.code === "INVALID_DECISION");

  // 5. Authenticated SuperAdmin with missing/short rationale (<10 chars) -> HTTP 400
  const r5 = await POST(req({ assessmentId: "asm-1", decision: "APPROVED", rationale: "short" }));
  const d5 = await r5.json();
  check("5. Short rationale (<10 chars) -> HTTP 400", r5.status === 400 && d5.code === "INVALID_RATIONALE");

  // 6. Authenticated SuperAdmin with valid APPROVED payload -> HTTP 200 with JCS receipt
  const validApprovedPayload = {
    assessmentId: "asm-pci-prod-001",
    decision: "APPROVED",
    rationale: "Topologia verificada em conformidade com isolamento de rede PCI-DSS e regras de firewall ativas.",
    organizationPolicyId: "pci-segmented-prod",
    policyVersion: "2.1.0",
  };
  const r6 = await POST(req(validApprovedPayload));
  const d6 = await r6.json();
  const sha6 = crypto.createHash("sha256").update(d6.receiptCanonicalJcs || "", "utf8").digest("hex");
  check(
    "6. SuperAdmin APPROVED -> HTTP 200 with valid receipt and hash",
    r6.status === 200 &&
      d6.success === true &&
      d6.decision === "APPROVED" &&
      d6.receipt?.reviewer?.role === "SUPERADMIN" &&
      d6.receiptSha256 === sha6
  );

  // 7. Authenticated SuperAdmin with valid REJECTED payload -> HTTP 200 with JCS receipt
  const validRejectedPayload = {
    assessmentId: "asm-pci-prod-002",
    decision: "REJECTED",
    rationale: "Evidência de telemetria desatualizada e sem garantias de regras de borda ativas.",
    organizationPolicyId: "pci-segmented-prod",
    policyVersion: "2.1.0",
  };
  const r7 = await POST(req(validRejectedPayload));
  const d7 = await r7.json();
  const sha7 = crypto.createHash("sha256").update(d7.receiptCanonicalJcs || "", "utf8").digest("hex");
  check(
    "7. SuperAdmin REJECTED -> HTTP 200 with valid receipt and hash",
    r7.status === 200 &&
      d7.success === true &&
      d7.decision === "REJECTED" &&
      d7.receipt?.reviewer?.role === "SUPERADMIN" &&
      d7.receiptSha256 === sha7
  );

  // 8. Receipt verification: reviewer email and identity must come from server session, not request body
  const spoofAttemptPayload = {
    assessmentId: "asm-pci-prod-003",
    decision: "APPROVED",
    rationale: "Tentativa de injeção de identidade forjada no corpo da requisição.",
    reviewer: {
      email: "forged.superadmin@external.com",
      role: "ROOT_SUPERADMIN",
    },
  };
  const r8 = await POST(req(spoofAttemptPayload));
  const d8 = await r8.json();
  check(
    "8. Identity spoofing prevented: reviewer strictly loaded from authoritative server session",
    r8.status === 200 &&
      d8.receipt.reviewer.email === "master@helpusbr.com" &&
      d8.receipt.reviewer.id === "admin-master-1" &&
      d8.receipt.reviewer.role === "SUPERADMIN"
  );

  const passedCount = results.filter((r) => r.passed).length;
  console.log("------------------------------------------------------------");
  console.log(`TOTAL: ${passedCount}/${results.length} tests passed.`);

  const outputPath = path.resolve(__dirname, "../../outputs/review_decision_tests_results.json");
  fs.writeFileSync(
    outputPath,
    JSON.stringify(
      {
        suite: "Server-Side HITL Review Decision Route Security Suite",
        total: results.length,
        passed: passedCount,
        allPassed: passedCount === results.length,
        results,
      },
      null,
      2
    )
  );
  console.log(`Saved results to ${outputPath}`);

  if (passedCount !== results.length) {
    process.exit(1);
  }
}

main().catch((e) => {
  console.error("Test execution error:", e);
  process.exit(1);
});
