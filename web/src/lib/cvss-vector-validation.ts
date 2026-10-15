const BASE_METRICS: Record<string, readonly string[]> = {
  AV: ["N", "A", "L", "P"],
  AC: ["L", "H"],
  AT: ["N", "P"],
  PR: ["N", "L", "H"],
  UI: ["N", "P", "A"],
  VC: ["H", "L", "N"],
  VI: ["H", "L", "N"],
  VA: ["H", "L", "N"],
  SC: ["H", "L", "N"],
  SI: ["H", "L", "N"],
  SA: ["H", "L", "N"],
};

const OPTIONAL_METRICS: Record<string, readonly string[]> = {
  E: ["X", "A", "P", "U"],
  CR: ["X", "H", "M", "L"],
  IR: ["X", "H", "M", "L"],
  AR: ["X", "H", "M", "L"],
  MAV: ["X", "N", "A", "L", "P"],
  MAC: ["X", "L", "H"],
  MAT: ["X", "N", "P"],
  MPR: ["X", "N", "L", "H"],
  MUI: ["X", "N", "P", "A"],
  MVC: ["X", "H", "L", "N"],
  MVI: ["X", "H", "L", "N"],
  MVA: ["X", "H", "L", "N"],
  MSC: ["X", "H", "L", "N"],
  MSI: ["X", "S", "H", "L", "N"],
  MSA: ["X", "S", "H", "L", "N"],
  S: ["X", "N", "P"],
  AU: ["X", "N", "Y"],
  R: ["X", "A", "U", "I"],
  V: ["X", "D", "C"],
  RE: ["X", "L", "M", "H"],
  U: ["X", "Clear", "Green", "Amber", "Red"],
};

const ALL_METRICS = {
  ...BASE_METRICS,
  ...OPTIONAL_METRICS,
};

export type CvssVectorValidation = {
  valid: boolean;
  normalized: string;
  errors: string[];
  nomenclature:
    | "CVSS-B"
    | "CVSS-BT"
    | "CVSS-BE"
    | "CVSS-BTE";
};

export function validateCvss40VectorInput(
  input: string,
): CvssVectorValidation {
  const normalized = input.trim();
  const errors: string[] = [];

  if (!normalized) {
    return {
      valid: false,
      normalized,
      errors: ["Informe o vetor CVSS v4.0 publicado pela fonte."],
      nomenclature: "CVSS-B",
    };
  }

  const parts = normalized.split("/");
  if (parts[0] !== "CVSS:4.0") {
    errors.push("O vetor deve começar com CVSS:4.0.");
  }

  const seen = new Map<string, string>();

  for (const segment of parts.slice(1)) {
    const separator = segment.indexOf(":");
    if (separator <= 0) {
      errors.push(`Segmento inválido: ${segment || "(vazio)"}.`);
      continue;
    }

    const metric = segment.slice(0, separator);
    const value = segment.slice(separator + 1);
    const allowed = ALL_METRICS[metric];

    if (!allowed) {
      errors.push(`Métrica desconhecida: ${metric}.`);
      continue;
    }

    if (seen.has(metric)) {
      errors.push(`Métrica duplicada: ${metric}.`);
      continue;
    }

    if (!allowed.includes(value)) {
      errors.push(`Valor inválido para ${metric}: ${value || "(vazio)"}.`);
      continue;
    }

    seen.set(metric, value);
  }

  for (const metric of Object.keys(BASE_METRICS)) {
    if (!seen.has(metric)) {
      errors.push(`Métrica Base obrigatória ausente: ${metric}.`);
    }
  }

  const threatUsed =
    seen.has("E") && seen.get("E") !== "X";

  const environmentalUsed =
    Object.keys(OPTIONAL_METRICS)
      .filter((metric) => metric !== "E" && !["S", "AU", "R", "V", "RE", "U"].includes(metric))
      .some((metric) => seen.has(metric) && seen.get(metric) !== "X");

  const nomenclature = threatUsed
    ? environmentalUsed
      ? "CVSS-BTE"
      : "CVSS-BT"
    : environmentalUsed
      ? "CVSS-BE"
      : "CVSS-B";

  return {
    valid: errors.length === 0,
    normalized,
    errors,
    nomenclature,
  };
}
