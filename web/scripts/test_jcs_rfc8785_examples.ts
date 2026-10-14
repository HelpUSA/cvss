import { jcsCanonicalize } from "../src/lib/jcs";

// RFC 8785 Section 3.2.2 / 3.2.3 canonicalization example.
const sample = {
  numbers: [333333333.33333329, 1E30, 4.50, 2e-3, 0.000000000000000000000000001],
  string: "€$\u000f\nA'B\"\\\\\"/",
  literals: [null, true, false],
};
const expected = '{"literals":[null,true,false],"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27],"string":"€$\\u000f\\nA\'B\\\"\\\\\\\\\\\"/"}';
const observed = jcsCanonicalize(sample);
if (observed !== expected) {
  console.error(JSON.stringify({ test: "RFC8785-section-3.2-example", expected, observed }, null, 2));
  process.exit(1);
}
console.log(JSON.stringify({ test: "RFC8785-section-3.2-example", pass: true, observed }, null, 2));
