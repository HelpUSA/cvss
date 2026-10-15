import {
  roleLabel,
} from "@/lib/authorization";
import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  getTenantOverview,
} from "@/lib/tenant-data";

type Params = Promise<{
  organizationSlug: string;
}>;

export default async function TenantOverviewPage({
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

  let next = {
    title: "Criar o primeiro projeto",
    text:
      "Um projeto agrupa o sistema ou escopo que será avaliado.",
    href: `${base}/projects`,
  };

  if (overview.activeProjects > 0) {
    next = {
      title: "Criar um ambiente",
      text:
        "Defina onde o sistema está implantado: produção, homologação, DMZ ou outro contexto.",
      href: `${base}/environments`,
    };
  }

  if (overview.activeEnvironments > 0) {
    next = {
      title:
        "Registrar uma vulnerabilidade",
      text:
        "Associe uma CVE ao ambiente correto antes de informar o vetor e as evidências.",
      href: `${base}/assessments`,
    };
  }

  if (overview.activeAssessments > 0) {
    next = {
      title:
        "Continuar uma avaliação",
      text:
        "Abra uma avaliação existente para informar o CVSS-B de origem e as evidências ambientais.",
      href: `${base}/assessments`,
    };
  }

  if (overview.completedRuns > 0) {
    next = {
      title:
        "Consultar resultados ou reavaliar",
      text:
        "O histórico já possui execuções. Abra uma avaliação para revisar resultados ou registrar uma nova execução.",
      href: `${base}/assessments`,
    };
  }

  return (
    <>
      <section className="tenant-hero">
        <span className="section-kicker">
          Organização
        </span>
        <h1>
          {context.organization.name}
        </h1>
        <p>
          Você está como{" "}
          <strong>
            {roleLabel(
              context.membership.role,
            )}
          </strong>
          . Para o fluxo prático, use o
          roteiro guiado e avance uma etapa
          de cada vez.
        </p>
        <div className="operational-actions">
          <a
            className="button button--primary"
            href={`${base}/guide`}
          >
            Abrir roteiro “Comece aqui”
          </a>
        </div>
      </section>

      <section
        className="tenant-metric-grid"
        aria-label="Resumo operacional"
      >
        <article className="tenant-metric">
          <span>Projetos</span>
          <strong>
            {overview.activeProjects}
          </strong>
          <small>Etapa 1</small>
        </article>

        <article className="tenant-metric">
          <span>Ambientes</span>
          <strong>
            {overview.activeEnvironments}
          </strong>
          <small>Etapa 2</small>
        </article>

        <article className="tenant-metric">
          <span>Avaliações</span>
          <strong>
            {overview.activeAssessments}
          </strong>
          <small>Etapa 3</small>
        </article>

        <article className="tenant-metric">
          <span>Execuções</span>
          <strong>
            {overview.completedRuns}
          </strong>
          <small>Etapas 4–5</small>
        </article>
      </section>

      <section
        className="panel"
        style={{
          marginTop: "1.5rem",
        }}
      >
        <span className="section-kicker">
          Próxima ação recomendada
        </span>
        <h2>{next.title}</h2>
        <p>{next.text}</p>
        <a
          className="button button--primary"
          href={next.href}
        >
          Continuar →
        </a>
      </section>

      <section
        className="panel"
        style={{
          marginTop: "1.5rem",
        }}
      >
        <span className="section-kicker">
          Regra simples
        </span>
        <h2>
          Origem primeiro, contexto depois.
        </h2>
        <p>
          Preserve o vetor publicado pela
          fonte como CVSS-B. Depois informe
          somente fatos do ambiente. A
          HelpUS mantém o resultado
          ambiental, o histórico e a
          política operacional separados da
          origem.
        </p>
      </section>
    </>
  );
}
