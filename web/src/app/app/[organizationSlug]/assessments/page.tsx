import {
  hasTenantPermission,
} from "@/lib/authorization";
import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  listTenantEnvironments,
  listTenantOperationalAssessments,
} from "@/lib/tenant-data";

import {
  AssessmentCreateForm,
} from "./AssessmentCreateForm";

type Params = Promise<{
  organizationSlug: string;
}>;

export default async function AssessmentsPage({
  params,
}: {
  params: Params;
}) {
  const {
    organizationSlug,
  } = await params;

  const context =
    await requireOrganizationContext({
      organizationSlug,
      permission:
        "organization:read",
    });

  const [
    assessments,
    environments,
  ] = await Promise.all([
    listTenantOperationalAssessments(
      context,
    ),
    listTenantEnvironments(
      context,
    ),
  ]);

  const canExecute =
    hasTenantPermission(
      context.membership.role,
      "analysis:execute",
    );

  return (
    <>
      <section className="tenant-page-heading">
        <span className="section-kicker">
          Etapa 3 de 5
        </span>
        <h1>
          Avaliações de vulnerabilidade
        </h1>
        <p>
          Uma avaliação liga uma
          vulnerabilidade a um ambiente
          específico. Depois dela, você
          informa o vetor CVSS-B de origem
          e as evidências ambientais.
        </p>
      </section>

      <div
        className="panel"
        style={{
          marginBottom: "1.25rem",
        }}
      >
        <strong>
          Padrão alinhado ao fluxo do
          consumidor CVSS
        </strong>
        <p>
          A fonte publica normalmente o
          CVSS-B. A sua organização adiciona
          o contexto ambiental para produzir
          um CVSS-BE quando houver métricas
          ambientais aplicáveis.
        </p>
      </div>

      {environments.length === 0 ? (
        <section className="tenant-empty-state">
          <h2>
            Falta criar um ambiente.
          </h2>
          <p>
            Antes de registrar uma
            vulnerabilidade, crie o ambiente
            onde o sistema está implantado.
          </p>
          <a
            className="button button--primary"
            href={`/app/${context.organization.slug}/environments`}
          >
            Ir para Etapa 2 — Ambientes
          </a>
        </section>
      ) : canExecute ? (
        <AssessmentCreateForm
          organizationSlug={
            context.organization.slug
          }
          environments={
            environments.map(
              (environment) => ({
                id: environment.id,
                name: environment.name,
                project: {
                  id:
                    environment.project.id,
                  name:
                    environment.project
                      .name,
                },
              }),
            )
          }
        />
      ) : (
        <section className="tenant-empty-state">
          <h2>
            Seu perfil é somente consulta.
          </h2>
          <p>
            Você pode acompanhar avaliações
            existentes, mas não iniciar uma
            nova execução.
          </p>
        </section>
      )}

      {assessments.length > 0 ? (
        <section
          className="tenant-list"
          style={{
            marginTop: "2rem",
          }}
        >
          {assessments.map(
            (assessment) => (
              <a
                className="tenant-list-card"
                key={assessment.id}
                href={`/app/${context.organization.slug}/assessments/${assessment.id}`}
              >
                <div>
                  <span className="section-kicker">
                    {assessment.cve ??
                      assessment
                        .vulnerabilityId}
                  </span>
                  <h2>
                    {assessment.title}
                  </h2>
                  <code>
                    {
                      assessment
                        .environment
                        .project.name
                    }{" "}
                    /{" "}
                    {
                      assessment
                        .environment.name
                    }
                  </code>
                </div>
                <dl>
                  <div>
                    <dt>Execuções</dt>
                    <dd>
                      {
                        assessment._count
                          .runs
                      }
                    </dd>
                  </div>
                  <div>
                    <dt>Status</dt>
                    <dd>
                      {assessment.status}
                    </dd>
                  </div>
                </dl>
              </a>
            ),
          )}
        </section>
      ) : null}
    </>
  );
}
