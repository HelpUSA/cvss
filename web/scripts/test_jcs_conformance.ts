import { jcsCanonicalize } from "../src/lib/jcs";
import crypto from "crypto";
import fs from "fs";
import path from "path";

interface TestCase {
  name: string;
  input: unknown;
  expected?: string;
  shouldThrow?: boolean;
}

const testCases: TestCase[] = [
  { name: "JCS-001 shallow key ordering", input: { b: 2, a: 1 }, expected: '{"a":1,"b":2}' },
  { name: "JCS-002 recursive key ordering", input: { z: { d: 4, c: 3 }, a: 1 }, expected: '{"a":1,"z":{"c":3,"d":4}}' },
  { name: "JCS-003 array order preserved", input: [3, 1, 2], expected: "[3,1,2]" },
  { name: "JCS-004 objects inside arrays", input: [{ y: 2, x: 1 }, { b: 4, a: 3 }], expected: '[{"x":1,"y":2},{"a":3,"b":4}]' },
  { name: "JCS-005 primitives", input: { z: null, t: true, f: false }, expected: '{"f":false,"t":true,"z":null}' },
  { name: "JCS-006 valid Unicode and surrogate pair", input: { emoji: "🛡️", greek: "αβγ" }, expected: '{"emoji":"🛡️","greek":"αβγ"}' },
  { name: "JCS-007 integer/float serialization", input: { int: 42, float: 3.14159, neg: -10 }, expected: '{"float":3.14159,"int":42,"neg":-10}' },
  { name: "JCS-008 negative zero normalizes to zero", input: { val: -0 }, expected: '{"val":0}' },
  { name: "JCS-009 reject NaN", input: { bad: Number.NaN }, shouldThrow: true },
  { name: "JCS-010 reject +Infinity", input: { bad: Number.POSITIVE_INFINITY }, shouldThrow: true },
  { name: "JCS-011 reject -Infinity", input: { bad: Number.NEGATIVE_INFINITY }, shouldThrow: true },
  { name: "JCS-012 reject lone high surrogate string", input: { bad: "\ud800" }, shouldThrow: true },
  { name: "JCS-013 reject lone low surrogate string", input: { bad: "\udc00" }, shouldThrow: true },
  { name: "JCS-014 reject lone surrogate property name", input: { ["\ud800"]: 1 }, shouldThrow: true },
  { name: "JCS-015 structural/hash invariance", input: null },
];

function sha256(value: string): string {
  return crypto.createHash("sha256").update(value, "utf8").digest("hex");
}

function runSuite() {
  const results: any[] = [];
  let passed = 0;
  let failed = 0;

  for (const tc of testCases) {
    if (tc.name.includes("structural/hash invariance")) {
      const one = { a: { b: 1, c: [{ d: 2, e: 3 }] }, f: 4 };
      const two = { f: 4, a: { c: [{ e: 3, d: 2 }], b: 1 } };
      const c1 = jcsCanonicalize(one);
      const c2 = jcsCanonicalize(two);
      const ok = c1 === c2 && sha256(c1) === sha256(c2);
      results.push({ testCase: tc.name, passed: ok, canonical: c1, hash: sha256(c1) });
      ok ? passed++ : failed++;
      continue;
    }

    if (tc.shouldThrow) {
      let threw = false;
      let error = "";
      try { jcsCanonicalize(tc.input); } catch (e: any) { threw = true; error = String(e?.message ?? e); }
      results.push({ testCase: tc.name, passed: threw, error });
      threw ? passed++ : failed++;
      continue;
    }

    let observed = "";
    let ok = false;
    try {
      observed = jcsCanonicalize(tc.input);
      ok = observed === tc.expected;
    } catch (e: any) {
      observed = `ERROR: ${e?.message ?? e}`;
    }
    results.push({ testCase: tc.name, passed: ok, expected: tc.expected, observed });
    ok ? passed++ : failed++;
  }

  const summary = {
    suite: "Local JCS contract tests (not a substitute for a pinned RFC 8785 conformance corpus)",
    timestamp: new Date().toISOString(),
    totalTests: testCases.length,
    passed,
    failed,
    formalRfc8785ConformanceClaimAllowed: false,
    results,
  };

  const outPath = path.resolve(__dirname, "../../outputs/jcs_conformance_results.json");
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(summary, null, 2), "utf8");
  console.log(JSON.stringify(summary, null, 2));
  if (failed > 0) process.exit(1);
}

runSuite();
