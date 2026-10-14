import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  getTenantOverview,
} from "@/lib/tenant-data";

type Params = Promise<{
  organizationSlug: string;
}>;

export default async function GuidedStartPage({
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

  const overview =
    await getTenantOverview(context);

  const base =
    `/app/${context.organization.slug}`;

  const steps = [
    {
      number: 1,
      title: "Projeto",
      text:
        "Agrupe um sistema, produto ou escopo de trabalho. Ex.: ERP, Portal, Laboratório.",
      done:
        overview.activeProjects > 0,
      href: `${base}/projects`,
      action:
        overview.activeProjects > 0
          ? "Revisar projetos"
          : "Criar primeiro projeto",
    },
    {
      number: 2,
      title: "Ambiente",
      text:
        "Defina onde o sistema roda. Ex.: Produção, Homologação, DMZ ou filial.",
      done:
        overview.activeEnvironments > 0,
      href: `${base}/environments`,
      action:
        overview.activeEnvironments > 0
          ? "Revisar ambientes"
          : "Criar primeiro ambiente",
    },
    {
      number: 3,
      title: "Vulnerabilidade",
      text:
        "Associe uma CVE ao ambiente que realmente está exposto à vulnerabilidade.",
      done:
        overview.activeAssessments > 0,
      href: `${base}/assessments`,
      action:
        overview.activeAssessments > 0
          ? "Ver avaliações"
          : "Criar primeira avaliação",
    },
    {
      number: 4,
      title: "Origem + evidências",
      text:
        "Preserve o vetor CVSS-B publicado e informe fatos verificáveis do seu ambiente.",
      done:
        overview.completedRuns > 0,
      href: `${base}/assessments`,
      action:
        overview.activeAssessments > 0
          ? "Continuar avaliação"
          : "Concluir etapa anterior",
    },
    {
      number: 5,
      title: "Resultado e histórico",
      text:
        "Compare CVSS-B com o resultado ambiental, confira ABSTAIN quando aplicável e preserve cada execução.",
      done:
        overview.completedRuns > 0,
      href: `${base}/assessments`,
      action:
        overview.completedRuns > 0
          ? "Abrir histórico"
          : "Gerar primeiro resultado",
    },
  ];

  return (
    <>
      <section className="tenant-page-heading">
        <span className="section-kicker">
          Comece aqui
        </span>
        <h1>
          Roteiro operacional em 5 etapas
        </h1>
        <p>
          Siga a sequência abaixo. Cada
          página trata somente da etapa
          necessária e informa o próximo
          passo.
        </p>
      </section>

      <div
        className="panel"
        style={{
          marginBottom: "1.5rem",
        }}
      >
        <strong>
          Como isto se relaciona com a
          FIRST?
        </strong>
        <p>
          A FIRST separa métricas Base,
          Threat, Environmental e
          Supplemental. Neste roteiro, o
          vetor Base vem da fonte e o
          contexto da sua organização é
          adicionado depois, sem
          sobrescrever a origem.
        </p>
        <div
          style={{
            display: "flex",
            gap: ".75rem",
            flexWrap: "wrap",
          }}
        >
          <a
            className="button button--quiet"
            href="https://www.first.org/cvss/v4.0/user-guide"
            target="_blank"
            rel="noreferrer"
          >
            Guia FIRST ↗
          </a>
          <a
            className="button button--quiet"
            href="https://www.first.org/cvss/calculator/4.0"
            target="_blank"
            rel="noreferrer"
          >
            Calculadora FIRST ↗
          </a>
        </div>
      </div>

      <section
        style={{
          display: "grid",
          gap: "1rem",
        }}
      >
        {steps.map((step) => (
          <article
            className="panel"
            key={step.number}
            style={{
              display: "grid",
              gridTemplateColumns:
                "70px minmax(0, 1fr) auto",
              gap: "1rem",
              alignItems: "center",
            }}
          >
            <strong
              style={{
                fontSize: "2rem",
              }}
            >
              {String(step.number).padStart(
                2,
                "0",
              )}
            </strong>

            <div>
              <span className="section-kicker">
                {step.done
                  ? "Concluída / disponível"
                  : "Próxima etapa"}
              </span>
              <h2
                style={{
                  margin:
                    ".25rem 0 .4rem",
                }}
              >
                {step.title}
              </h2>
              <p
                style={{
                  margin: 0,
                }}
              >
                {step.text}
              </p>
            </div>

            <a
              className={
                step.done
                  ? "button button--secondary"
                  : "button button--primary"
              }
              href={step.href}
            >
              {step.action}
            </a>
          </article>
        ))}
      </section>
    </>
  );
}
