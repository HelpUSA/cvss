import assert from "node:assert/strict";
import test from "node:test";

import { jcsCanonicalize } from "../src/lib/jcs";

test("JCS preserves Unicode as-is and does not silently normalize NFC", () => {
  const composed = "é";
  const decomposed = "e\u0301";

  assert.notEqual(composed, decomposed);
  assert.notEqual(
    jcsCanonicalize({ value: composed }),
    jcsCanonicalize({ value: decomposed }),
  );
});

test("JCS canonicalization remains key-order invariant", () => {
  const one = { z: "fim", a: "início" };
  const two = { a: "início", z: "fim" };

  assert.equal(
    jcsCanonicalize(one),
    jcsCanonicalize(two),
  );
});
