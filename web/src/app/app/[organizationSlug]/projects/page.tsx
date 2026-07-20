import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  listTenantProjects,
} from "@/lib/tenant-data";

type TenantProjectsParams = Promise<{
  organizationSlug: string;
}>;

export default async function TenantProjectsPage({
  params,
}: {
  params: TenantProjectsParams;
}) {
  const {
    organizationSlug,
  } = await params;

  const context =
    await requireOrganizationContext({
      organizationSlug,
      permission: "project:read",
    });

  const projects =
    await listTenantProjects(context);

  return (
    <>
      <section className="tenant-page-heading">
        <span className="section-kicker">
          Projetos
        </span>

        <h1>
          Projetos de{" "}
          {context.organization.name}
        </h1>

        <p>
          A consulta usa exclusivamente o
          identificador da organização
          resolvido no servidor.
        </p>
      </section>

      {projects.length > 0 ? (
        <section className="tenant-list">
          {projects.map((project) => (
            <article
              className="tenant-list-card"
              key={project.id}
            >
              <div>
                <span className="section-kicker">
                  Projeto ativo
                </span>

                <h2>{project.name}</h2>

                <code>{project.slug}</code>
              </div>

              <dl>
                <div>
                  <dt>Ambientes</dt>
                  <dd>
                    {
                      project._count
                        .environments
                    }
                  </dd>
                </div>

                <div>
                  <dt>Status</dt>
                  <dd>{project.status}</dd>
                </div>
              </dl>
            </article>
          ))}
        </section>
      ) : (
        <section className="tenant-empty-state">
          <h2>
            Nenhum projeto ativo.
          </h2>

          <p>
            A criação de projetos será
            conectada em uma etapa posterior
            com permissão explícita.
          </p>
        </section>
      )}
    </>
  );
}
