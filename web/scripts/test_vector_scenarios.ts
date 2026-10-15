import { validateCvss40VectorInput } from "../src/lib/cvss-vector-validation";

const validBase = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N";

const scenarios = [
  { id: "A", name: "Valid Base-only", input: validBase },
  { id: "B", name: "Threat (E:P)", input: validBase + "/E:P" },
  { id: "C", name: "Environmental (CR:H)", input: validBase + "/CR:H" },
  { id: "D", name: "Threat + Env (E:A/CR:H)", input: validBase + "/E:A/CR:H" },
  { id: "E", name: "Wrong prefix (CVSS:3.1)", input: validBase.replace("CVSS:4.0", "CVSS:3.1") },
  { id: "F", name: "Missing Base metric (VC)", input: validBase.replace("/VC:H", "") },
  { id: "G", name: "Duplicate metric (AV:A)", input: validBase + "/AV:A" },
  { id: "H", name: "Unknown metric (ZZ:H)", input: validBase + "/ZZ:H" },
  { id: "I", name: "Invalid value (AC:X)", input: validBase.replace("/AC:L", "/AC:X") },
  { id: "J", name: "Whitespace padding", input: "   " + validBase + "   " },
];

console.log("=== VECTOR VALIDATION SCENARIOS A through J ===");
for (const s of scenarios) {
  const res = validateCvss40VectorInput(s.input);
  console.log(`Scenario ${s.id}: ${s.name}`);
  console.log(`  Valid: ${res.valid} | Nomenclature: ${res.nomenclature}`);
  if (res.errors.length) {
    console.log(`  Errors: ${JSON.stringify(res.errors)}`);
  } else {
    console.log(`  Normalized: ${res.normalized}`);
  }
}
