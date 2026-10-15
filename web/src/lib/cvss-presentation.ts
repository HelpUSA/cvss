const ENVIRONMENTAL_PREFIXES = [
  "CR",
  "IR",
  "AR",
  "MAV",
  "MAC",
  "MAT",
  "MPR",
  "MUI",
  "MVC",
  "MVI",
  "MVA",
  "MSC",
  "MSI",
  "MSA",
];

export function cvssNomenclatureFromVector(
  vector: string | null | undefined,
): "CVSS-B" | "CVSS-BT" | "CVSS-BE" | "CVSS-BTE" {
  if (!vector) {
    return "CVSS-B";
  }

  const metrics =
    new Map<string, string>();

  for (const part of vector.split("/").slice(1)) {
    const separator =
      part.indexOf(":");

    if (separator <= 0) {
      continue;
    }

    metrics.set(
      part.slice(0, separator),
      part.slice(separator + 1),
    );
  }

  const threatUsed =
    metrics.has("E") &&
    metrics.get("E") !== "X";

  const environmentalUsed =
    ENVIRONMENTAL_PREFIXES.some(
      (metric) =>
        metrics.has(metric) &&
        metrics.get(metric) !== "X",
    );

  if (
    threatUsed &&
    environmentalUsed
  ) {
    return "CVSS-BTE";
  }

  if (environmentalUsed) {
    return "CVSS-BE";
  }

  if (threatUsed) {
    return "CVSS-BT";
  }

  return "CVSS-B";
}
