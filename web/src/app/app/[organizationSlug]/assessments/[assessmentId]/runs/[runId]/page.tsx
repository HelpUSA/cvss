import {
  notFound,
} from "next/navigation";

import {
  cvssNomenclatureFromVector,
} from "@/lib/cvss-presentation";
import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  getTenantOperationalRun,
} from "@/lib/tenant-data";

import {
  GuidedWorkflowStepper,
} from "@/app/components/GuidedWorkflowStepper";

import {
  RunExplanation,
} from "@/app/components/RunExplanation";

import {
  SupplementalMetricsSummary,
} from "@/app/components/SupplementalMetricsSummary";

type Params = Promise<{
  organizationSlug: string;
  assessmentId: string;
  runId: string;
}>;

function formatScore(
  score: number | null,
) {
  return score === null
    ? "—"
    : score.toFixed(1);
}

export default async function RunResultPage({
  params,
}: {
  params: Params;
}) {
  const {
    organizationSlug,
    assessmentId,
    runId,
  } = await params;

  const context =
    await requireOrganizationContext({
      organizationSlug,
      permission:
        "organization:read",
    });

  const run =
    await getTenantOperationalRun(
      context,
      assessmentId,
      runId,
    );

  if (!run) {
    notFound();
  }

  const sourceNomenclature =
    cvssNomenclatureFromVector(
      run.sourceVector,
    );

  const finalNomenclature =
    cvssNomenclatureFromVector(
      run.finalVector ??
        run.sourceVector,
    );

  const abstained =
    run.status === "ABSTAINED";

  return (
    <>
      <section className="tenant-page-heading">
        <span className="section-kicker">
          Etapa 5 de 5
        </span>
        <h1>
          Resultado da avaliação
        </h1>
        <p>
          {run.assessment.cve ??
            run.assessment
              .vulnerabilityId}
          {" · "}
          {
            run.assessment
              .environment.project.name
          }
          {" / "}
          {
            run.assessment
              .environment.name
          }
        </p>
      </section>

      <GuidedWorkflowStepper currentStep={5} />

      <div
        className="panel"
        style={{
          marginBottom: "1.25rem",
        }}
      >
        <span className="section-kicker">
          Leitura principal
        </span>
        <h2>
          {abstained
            ? "O motor se absteve de afirmar um resultado ambiental."
            : "Compare origem e contexto sem misturar os dois."}
        </h2>
        <p>
          {abstained
            ? "A evidência foi considerada insuficiente, vencida ou conflitante. O CVSS-B de origem permanece disponível, mas nenhuma métrica ambiental é forçada."
            : "A nomenclatura segue a convenção da FIRST: CVSS-B para Base, CVSS-BE quando métricas ambientais são usadas e CVSS-BTE quando também há Threat."}
        </p>
      </div>

      <RunExplanation
        status={run.status}
        sourceScore={run.sourceScore}
        finalScore={run.finalScore}
        decision={run.decision}
        candidateMetrics={run.candidateMetrics}
        abstentionReasons={run.abstentionReasons}
        sourceType={run.evidenceSnapshot.sourceType}
        sourceReference={run.evidenceSnapshot.sourceReference}
        capturedAt={run.evidenceSnapshot.capturedAt}
      />

      <SupplementalMetricsSummary
        metadata={run.evidenceSnapshot.metadata}
      />

      <section
        className="tenant-metric-grid"
        aria-label="Resumo do resultado"
      >
        <article className="tenant-metric">
          <span>
            Origem
          </span>
          <strong>
            {formatScore(
              run.sourceScore,
            )}
          </strong>
          <small>
            {sourceNomenclature}
          </small>
        </article>

        <article className="tenant-metric">
          <span>
            Contextual
          </span>
          <strong>
            {abstained
              ? "ABSTAIN"
              : formatScore(
                  run.finalScore,
                )}
          </strong>
          <small>
            {abstained
              ? "Sem score ambiental afirmado"
              : finalNomenclature}
          </small>
        </article>

        <article className="tenant-metric">
          <span>
            Estado
          </span>
          <strong>
            {run.status}
          </strong>
          <small>
            Decisão: {run.decision}
          </small>
        </article>
      </section>

      <details
        className="panel"
        style={{
          marginTop: "1.25rem",
        }}
      >
        <summary
          style={{
            cursor: "pointer",
            fontWeight: 800,
          }}
        >
          Vetores CVSS completos (origem e contextual)
        </summary>
        <p>
          Compare o vetor Base de referência com o vetor contextual enriquecido com métricas de ameaça, ambientais e suplementares.
        </p>

        <div
          style={{
            display: "grid",
            gap: "1rem",
            marginTop: "1rem",
          }}
        >
          <div>
            <strong>
              Vetor de origem — {
                sourceNomenclature
              }
            </strong>
            <pre
              style={{
                whiteSpace: "pre-wrap",
                overflowWrap: "anywhere",
              }}
            >
              {run.sourceVector}
            </pre>
          </div>

          <div>
            <strong>
              Vetor contextual — {
                abstained
                  ? "não emitido"
                  : finalNomenclature
              }
            </strong>
            <pre
              style={{
                whiteSpace: "pre-wrap",
                overflowWrap: "anywhere",
              }}
            >
              {run.finalVector ??
                "ABSTAIN — nenhuma afirmação ambiental final."}
            </pre>
          </div>
        </div>
      </details>

      {abstained ? (
        <section
          className="panel"
          style={{
            marginTop: "1.25rem",
          }}
        >
          <span className="section-kicker">
            O que falta
          </span>
          <h2>
            Corrija as evidências e execute
            novamente.
          </h2>
          <pre
            style={{
              whiteSpace: "pre-wrap",
            }}
          >
            {JSON.stringify(
              run.abstentionReasons,
              null,
              2,
            )}
          </pre>
        </section>
      ) : null}

      <details
        className="panel"
        style={{
          marginTop: "1.25rem",
        }}
      >
        <summary
          style={{
            cursor: "pointer",
            fontWeight: 800,
          }}
        >
          Rastreabilidade e auditoria (hashes e engine)
        </summary>
        <p>
          Identificadores criptográficos, recibo de auditoria e versão do motor para conformidade e reprodutibilidade.
        </p>

        <dl className="context-list">
          <div>
            <dt>Run</dt>
            <dd>{run.id}</dd>
          </div>
          <div>
            <dt>Evidence</dt>
            <dd>
              {
                run.evidenceSnapshot
                  .canonicalHash
              }
            </dd>
          </div>
          <div>
            <dt>Fonte da evidência</dt>
            <dd>
              {run.evidenceSnapshot.sourceType}
            </dd>
          </div>
          <div>
            <dt>Referência</dt>
            <dd>
              {run.evidenceSnapshot.sourceReference ??
                "Não informada"}
            </dd>
          </div>
          <div>
            <dt>Receipt</dt>
            <dd>
              {run.auditReceiptHash}
            </dd>
          </div>
          <div>
            <dt>Engine</dt>
            <dd>
              {run.engineCommit}
            </dd>
          </div>
          <div>
            <dt>Captured</dt>
            <dd>
              {run.evidenceSnapshot.capturedAt.toLocaleString(
                "pt-BR",
              )}
            </dd>
          </div>
        </dl>
      </details>

      <div
        className="operational-actions"
        style={{
          marginTop: "1.5rem",
        }}
      >
        <a
          className="button button--primary"
          href={`/app/${context.organization.slug}/assessments/${assessmentId}`}
        >
          Voltar e executar novamente
        </a>
        <a
          className="button button--secondary"
          href={`/app/${context.organization.slug}/assessments`}
        >
          Ver todas as avaliações
        </a>
        <a
          className="button button--quiet"
          href="https://www.first.org/cvss/calculator/4.0"
          target="_blank"
          rel="noreferrer"
        >
          Comparar com calculadora FIRST ↗
        </a>
      </div>
    </>
  );
}
