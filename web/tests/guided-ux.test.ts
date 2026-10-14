import assert from "node:assert/strict";
import test from "node:test";

import {
  cvssNomenclatureFromVector,
} from "../src/lib/cvss-presentation";

const base =
  "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N";

test("CVSS presentation helper reports Base-only nomenclature", () => {
  assert.equal(
    cvssNomenclatureFromVector(base),
    "CVSS-B",
  );
});

test("CVSS presentation helper reports Environmental nomenclature", () => {
  assert.equal(
    cvssNomenclatureFromVector(
      `${base}/MAV:L`,
    ),
    "CVSS-BE",
  );
});

test("CVSS presentation helper reports Threat nomenclature", () => {
  assert.equal(
    cvssNomenclatureFromVector(
      `${base}/E:P`,
    ),
    "CVSS-BT",
  );
});

test("CVSS presentation helper reports Threat plus Environmental nomenclature", () => {
  assert.equal(
    cvssNomenclatureFromVector(
      `${base}/E:A/CR:H`,
    ),
    "CVSS-BTE",
  );
});

test("Not Defined optional metrics do not change nomenclature", () => {
  assert.equal(
    cvssNomenclatureFromVector(
      `${base}/E:X/CR:X/MAV:X`,
    ),
    "CVSS-B",
  );
});
