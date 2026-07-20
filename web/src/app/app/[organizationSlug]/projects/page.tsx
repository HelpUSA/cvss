import {
  hasTenantPermission,
} from "@/lib/authorization";
import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  listTenantProjects,
} from "@/lib/tenant-data";
import {
  ProjectCreateForm,
} from "./ProjectCreateForm";

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
    await listTenantProjects(
      context,
    );

  const canManage =
    hasTenantPermission(
      context.membership.role,
      "project:manage",
    );

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
          A consulta e a mutação usam
          exclusivamente o identificador da
          organização resolvido no servidor.
        </p>
      </section>

      {canManage ? (
        <ProjectCreateForm
          organizationSlug={
            context.organization.slug
          }
        />
      ) : null}

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
            Administradores e operadores
            podem criar o primeiro projeto
            usando o formulário acima.
          </p>
        </section>
      )}
    </>
  );
}
