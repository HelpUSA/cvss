import {
  hasTenantPermission,
} from "@/lib/authorization";
import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  listTenantEnvironments,
  listTenantProjects,
} from "@/lib/tenant-data";
import {
  EnvironmentCreateForm,
} from "./EnvironmentCreateForm";

type TenantEnvironmentsParams = Promise<{
  organizationSlug: string;
}>;

export default async function TenantEnvironmentsPage({
  params,
}: {
  params: TenantEnvironmentsParams;
}) {
  const {
    organizationSlug,
  } = await params;

  const context =
    await requireOrganizationContext({
      organizationSlug,
      permission: "environment:read",
    });

  const [
    environments,
    projects,
  ] = await Promise.all([
    listTenantEnvironments(
      context,
    ),

    listTenantProjects(
      context,
    ),
  ]);

  const canManage =
    hasTenantPermission(
      context.membership.role,
      "environment:manage",
    );

  return (
    <>
      <section className="tenant-page-heading">
        <span className="section-kicker">
          Ambientes
        </span>

        <h1>
          Ambientes de{" "}
          {context.organization.name}
        </h1>

        <p>
          Cada ambiente é verificado contra
          um projeto ativo que pertence à
          organização autorizada.
        </p>
      </section>

      {canManage &&
      projects.length > 0 ? (
        <EnvironmentCreateForm
          organizationSlug={
            context.organization.slug
          }
          projects={projects.map(
            (project) => ({
              id: project.id,
              name: project.name,
            }),
          )}
        />
      ) : null}

      {canManage &&
      projects.length === 0 ? (
        <section className="tenant-empty-state">
          <h2>
            Crie um projeto primeiro.
          </h2>

          <p>
            Um ambiente sempre pertence a um
            projeto ativo do mesmo tenant.
          </p>
        </section>
      ) : null}

      {environments.length > 0 ? (
        <section className="tenant-list">
          {environments.map(
            (environment) => (
              <article
                className="tenant-list-card"
                key={environment.id}
              >
                <div>
                  <span className="section-kicker">
                    {
                      environment.project
                        .name
                    }
                  </span>

                  <h2>
                    {environment.name}
                  </h2>

                  <code>
                    {
                      environment.project
                        .slug
                    }
                    /
                    {environment.slug}
                  </code>
                </div>

                <dl>
                  <div>
                    <dt>Projeto</dt>
                    <dd>
                      {
                        environment.project
                          .name
                      }
                    </dd>
                  </div>

                  <div>
                    <dt>Status</dt>
                    <dd>
                      {environment.status}
                    </dd>
                  </div>
                </dl>
              </article>
            ),
          )}
        </section>
      ) : null}
    </>
  );
}
