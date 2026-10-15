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
  getTenantOperationalAssessment,
} from "@/lib/tenant-data";

import {
  AssessmentRunForm,
} from "./AssessmentRunForm";
import {
  CvssEvidenceHelp,
} from "@/app/components/CvssEvidenceHelp";

type Params = Promise<{
  organizationSlug: string;
  assessmentId: string;
}>;

export default async function AssessmentDetailPage({
  params,
}: {
  params: Params;
}) {
  const {
    organizationSlug,
    assessmentId,
  } = await params;

  const context =
    await requireOrganizationContext({
      organizationSlug,
      permission:
        "organization:read",
    });

  const assessment =
    await getTenantOperationalAssessment(
      context,
      assessmentId,
    );

  if (!assessment) {
    notFound();
  }

  const canExecute =
    context.membership.role ===
      "ADMIN" ||
    context.membership.role ===
      "OPERATOR";

  return (
    <>
      <section className="tenant-page-heading">
        <span className="section-kicker">
          Etapa 4 de 5
        </span>
        <h1>{assessment.title}</h1>
        <p>
          {assessment.cve ??
            assessment.vulnerabilityId}
          {" · "}
          {
            assessment.environment
              .project.name
          }
          {" / "}
          {assessment.environment.name}
        </p>
      </section>

      <div
        className="panel"
        style={{
          marginBottom: "1rem",
        }}
      >
        <strong>
          O que acontece nesta etapa?
        </strong>
        <p>
          Você informa o vetor CVSS-B de
          origem e fatos verificáveis do
          ambiente. O motor decide se há
          evidência suficiente para métricas
          ambientais e calcula o resultado
          sem alterar o score de origem.
        </p>
        <a
          href="https://www.first.org/cvss/v4.0/user-guide"
          target="_blank"
          rel="noreferrer"
        >
          Consultar orientação oficial da
          FIRST ↗
        </a>
      </div>

      <CvssEvidenceHelp />

      {canExecute ? (
        <AssessmentRunForm
          organizationSlug={
            context.organization.slug
          }
          projectId={
            assessment.environment
              .project.id
          }
          environmentId={
            assessment.environment.id
          }
          assessmentId={
            assessment.id
          }
          cveId={
            assessment.cve ??
            assessment.vulnerabilityId
          }
        />
      ) : (
        <section className="tenant-empty-state">
          <h2>
            Perfil sem permissão de execução.
          </h2>
          <p>
            Você pode consultar o histórico
            abaixo, mas apenas Administrador
            ou Operador pode executar uma
            nova avaliação.
          </p>
        </section>
      )}

      <section
        style={{
          marginTop: "2rem",
        }}
      >
        <div className="section-heading">
          <div>
            <span className="section-kicker">
              Histórico
            </span>
            <h2>
              Execuções desta avaliação
            </h2>
          </div>
          <p>
            Cada execução é preservada.
            Reavaliar nunca sobrescreve o
            resultado anterior.
          </p>
        </div>

        {assessment.runs.length > 0 ? (
          <div className="tenant-list">
            {assessment.runs.map(
              (run) => (
                <a
                  className="tenant-list-card"
                  href={`/app/${context.organization.slug}/assessments/${assessment.id}/runs/${run.id}`}
                  key={run.id}
                >
                  <div>
                    <span className="section-kicker">
                      {
                        run.status
                      }
                    </span>
                    <h2>
                      {run.finalScore ??
                        run.sourceScore}
                      {" "}
                      {
                        cvssNomenclatureFromVector(
                          run.finalVector ??
                            run.sourceVector,
                        )
                      }
                    </h2>
                    <code>
                      {run.id}
                    </code>
                  </div>
                  <dl>
                    <div>
                      <dt>Decisão</dt>
                      <dd>
                        {run.decision}
                      </dd>
                    </div>
                    <div>
                      <dt>Data</dt>
                      <dd>
                        {run.createdAt.toLocaleString(
                          "pt-BR",
                        )}
                      </dd>
                    </div>
                  </dl>
                </a>
              ),
            )}
          </div>
        ) : (
          <div className="tenant-empty-state">
            <h2>
              Ainda não há execuções.
            </h2>
            <p>
              Preencha as evidências acima
              para gerar o primeiro
              resultado.
            </p>
          </div>
        )}
      </section>
    </>
  );
}
