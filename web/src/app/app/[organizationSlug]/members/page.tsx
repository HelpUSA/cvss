import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  listTenantMemberships,
} from "@/lib/tenant-data";
import {
  MemberCreateForm,
} from "./MemberCreateForm";
import {
  MembershipControls,
} from "./MembershipControls";

type MembersPageParams = Promise<{
  organizationSlug: string;
}>;

export default async function MembersPage({
  params,
}: {
  params: MembersPageParams;
}) {
  const {
    organizationSlug,
  } = await params;

  const context =
    await requireOrganizationContext({
      organizationSlug,
      permission: "membership:read",
    });

  const memberships =
    await listTenantMemberships(
      context,
    );

  return (
    <>
      <section className="tenant-page-heading">
        <span className="section-kicker">
          Administração
        </span>

        <h1>
          Membros de{" "}
          {context.organization.name}
        </h1>

        <p>
          Somente administradores ativos
          podem criar ou alterar memberships.
          O último administrador ativo não
          pode ser removido, suspenso,
          revogado ou rebaixado.
        </p>
      </section>

      <MemberCreateForm
        organizationSlug={
          context.organization.slug
        }
      />

      <section className="membership-list">
        {memberships.map(
          (membership) => (
            <article
              className="membership-card"
              key={membership.id}
            >
              <div>
                <span className="section-kicker">
                  {membership.user.status}
                </span>

                <h2>
                  {membership.user.name}
                </h2>

                <p>
                  {membership.user.email}
                </p>
              </div>

              <MembershipControls
                organizationSlug={
                  context.organization.slug
                }
                membershipId={
                  membership.id
                }
                initialRole={
                  membership.role
                }
                initialStatus={
                  membership.status
                }
              />
            </article>
          ),
        )}
      </section>
    </>
  );
}
