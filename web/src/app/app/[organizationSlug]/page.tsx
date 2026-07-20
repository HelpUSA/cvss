import {
  roleLabel,
} from "@/lib/authorization";
import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  getTenantOverview,
} from "@/lib/tenant-data";

type TenantOverviewParams = Promise<{
  organizationSlug: string;
}>;

export default async function TenantOverviewPage({
  params,
}: {
  params: TenantOverviewParams;
}) {
  const {
    organizationSlug,
  } = await params;

  const context =
    await requireOrganizationContext({
      organizationSlug,
      permission: "organization:read",
    });

  const overview =
    await getTenantOverview(context);

  return (
    <>
      <section className="tenant-hero">
        <span className="section-kicker">
          Organização ativa
        </span>

        <h1>
          {context.organization.name}
        </h1>

        <p>
          Você está operando como{" "}
          <strong>
            {roleLabel(
              context.membership.role,
            )}
          </strong>
          . Nenhum papel enviado pelo cliente
          participa desta decisão.
        </p>
      </section>

      <section
        className="tenant-metric-grid"
        aria-label={
          "Resumo da organização"
        }
      >
        <article className="tenant-metric">
          <span>Projetos ativos</span>
          <strong>
            {overview.activeProjects}
          </strong>
          <small>
            Limitados a esta organização
          </small>
        </article>

        <article className="tenant-metric">
          <span>Ambientes ativos</span>
          <strong>
            {overview.activeEnvironments}
          </strong>
          <small>
            Resolvidos por projeto autorizado
          </small>
        </article>

        <article className="tenant-metric">
          <span>Membros ativos</span>
          <strong>
            {overview.activeMembers}
          </strong>
          <small>
            Memberships válidas no tenant
          </small>
        </article>
      </section>

      <section className="tenant-next-steps">
        <div>
          <span className="section-kicker">
            Fundação multiusuário
          </span>

          <h2>
            O limite organizacional está
            operacional.
          </h2>
        </div>

        <p>
          Os próximos fluxos poderão usar
          este contexto para importações,
          inventário, análises e decisões
          sem realizar consultas globais.
        </p>
      </section>
    </>
  );
}
