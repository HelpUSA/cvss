export type RunExplanationInput = {
  status: string;
  sourceScore: number;
  finalScore: number | null;
  decision: string;
  candidateMetrics: unknown;
  abstentionReasons: unknown;
  sourceType: string;
  sourceReference: string | null;
  capturedAt: Date;
};

function asStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value
    .map((item) => {
      if (typeof item === "string") {
        return item.trim();
      }
      if (item && typeof item === "object") {
        const record = item as Record<string, unknown>;
        if (typeof record.reason === "string") {
          return record.reason.trim();
        }
        if (typeof record.message === "string") {
          return record.message.trim();
        }
      }
      return "";
    })
    .filter(Boolean);
}

function metricEntries(value: unknown): Array<[string, string]> {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return [];
  }

  return Object.entries(value as Record<string, unknown>)
    .filter(([, metricValue]) =>
      typeof metricValue === "string" ||
      typeof metricValue === "number" ||
      typeof metricValue === "boolean",
    )
    .map(([metric, metricValue]) => [metric, String(metricValue)]);
}

export function explainOperationalRun(
  input: RunExplanationInput,
) {
  const abstained = input.status === "ABSTAINED";
  const metrics = metricEntries(input.candidateMetrics);
  const reasons = asStringArray(input.abstentionReasons);

  const changed =
    !abstained &&
    input.finalScore !== null &&
    input.finalScore !== input.sourceScore;

  const whatChanged = abstained
    ? "Nenhuma afirmação ambiental final foi emitida."
    : changed
      ? `O score contextual mudou de ${input.sourceScore.toFixed(1)} para ${input.finalScore?.toFixed(1)}.`
      : "O contexto analisado não alterou o score numérico de origem.";

  const why = abstained
    ? reasons.length > 0
      ? reasons
      : ["A evidência disponível não foi suficiente para sustentar uma afirmação ambiental."]
    : metrics.length > 0
      ? metrics.map(([metric, value]) => `${metric}: ${value}`)
      : ["Nenhuma métrica contextual adicional foi aplicada."];

  const evidence = [
    `Fonte: ${input.sourceType}`,
    input.sourceReference
      ? `Referência: ${input.sourceReference}`
      : "Referência externa: não informada",
    `Capturada em: ${input.capturedAt.toLocaleString("pt-BR")}`,
  ];

  const nextAction = abstained
    ? "Revise as evidências ausentes, vencidas ou conflitantes e execute uma nova avaliação sem sobrescrever este histórico."
    : "Use este resultado junto com o vetor e a evidência preservada. Se o ambiente mudar, execute uma nova avaliação em vez de editar o histórico.";

  return {
    abstained,
    whatChanged,
    why,
    evidence,
    nextAction,
    decision: input.decision,
    appliedMetrics: metrics,
    unresolved: reasons,
  };
}
