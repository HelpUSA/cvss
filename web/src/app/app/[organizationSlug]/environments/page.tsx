import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  listTenantEnvironments,
} from "@/lib/tenant-data";

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

  const environments =
    await listTenantEnvironments(context);

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
          Cada ambiente é filtrado por um
          projeto pertencente à organização
          autorizada.
        </p>
      </section>

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
      ) : (
        <section className="tenant-empty-state">
          <h2>
            Nenhum ambiente ativo.
          </h2>

          <p>
            A criação de ambientes será
            conectada posteriormente com
            autorização por ação.
          </p>
        </section>
      )}
    </>
  );
}
