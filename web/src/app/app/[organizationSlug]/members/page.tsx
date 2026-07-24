import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  listOrganizationInvitations,
} from "@/lib/invitation-lifecycle";
import {
  listTenantMemberships,
} from "@/lib/tenant-data";
import {
  InvitationsPanel,
} from "./InvitationsPanel";
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

  const [
    memberships,
    invitations,
  ] = await Promise.all([
    listTenantMemberships(
      context,
    ),

    listOrganizationInvitations(
      context,
    ),
  ]);

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

      <InvitationsPanel
        organizationSlug={
          context.organization.slug
        }
        initialInvitations={
          invitations.map(
            (invitation) => ({
              id:
                invitation.id,

              email:
                invitation.email,

              role:
                invitation.role,

              expiresAt:
                invitation.expiresAt
                  .toISOString(),

              createdAt:
                invitation.createdAt
                  .toISOString(),

              createdByName:
                invitation.createdBy.name,
            }),
          )
        }
      />

      <section className="direct-membership-section">
        <span className="section-kicker">
          Usuários já provisionados
        </span>

        <h2>
          Adicionar sem convite
        </h2>

        <MemberCreateForm
          organizationSlug={
            context.organization.slug
          }
        />
      </section>

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
