import {
  explainOperationalRun,
} from "@/lib/run-explanation";

type Props = {
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

export function RunExplanation({
  status,
  sourceScore,
  finalScore,
  decision,
  candidateMetrics,
  abstentionReasons,
  sourceType,
  sourceReference,
  capturedAt,
}: Props) {
  const explanation =
    explainOperationalRun({
      status,
      sourceScore,
      finalScore,
      decision,
      candidateMetrics,
      abstentionReasons,
      sourceType,
      sourceReference,
      capturedAt,
    });

  return (
    <section
      className="panel run-explanation"
      aria-labelledby="run-explanation-title"
    >
      <span className="section-kicker">
        Explicação do resultado
      </span>
      <h2 id="run-explanation-title">
        O que aconteceu nesta avaliação?
      </h2>

      <div className="run-explanation__grid">
        <article>
          <h3>O que mudou?</h3>
          <p>{explanation.whatChanged}</p>
        </article>

        <article>
          <h3>Por quê?</h3>
          <ul>
            {explanation.why.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article>
          <h3>Qual evidência sustentou?</h3>
          <ul>
            {explanation.evidence.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article>
          <h3>Próximo passo</h3>
          <p>{explanation.nextAction}</p>
        </article>
      </div>

      <p className="run-explanation__decision">
        Decisão registrada: <strong>{decision}</strong>
      </p>
    </section>
  );
}
