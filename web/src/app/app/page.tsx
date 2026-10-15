import {
  roleLabel,
} from "@/lib/authorization";
import {
  listAccessibleOrganizations,
} from "@/lib/organization-context";
import { prisma } from "@/lib/prisma";
import {
  requireActiveSession,
} from "@/lib/session";

export default async function OperationalHomePage() {
  const currentSession =
    await requireActiveSession();

  const [
    organizations,
    authoritativeUser,
  ] = await Promise.all([
    listAccessibleOrganizations(
      currentSession.user.id,
    ),

    prisma.user.findUnique({
      where: {
        id:
          currentSession.user.id,
      },
      select: {
        platformRole: true,
      },
    }),
  ]);

  const isPlatformAdmin =
    authoritativeUser?.platformRole ===
      "PLATFORM_ADMIN";

  return (
    <>
      <section className="operational-hero">
        <span className="section-kicker">
          Workspace operacional
        </span>

        <h1>
          Primeiro, escolha a organização.
        </h1>

        <p>
          Cada organização mantém seus
          próprios projetos, ambientes,
          avaliações, evidências e
          histórico. Depois de entrar em
          uma organização, abra “Comece
          aqui” para seguir o roteiro
          prático.
        </p>
      </section>

      {organizations.length > 0 ? (
        <section
          className="organization-grid"
          aria-label="Organizações disponíveis"
        >
          {organizations.map((entry) => (
            <a
              className="organization-card"
              href={`/app/${entry.organization.slug}/guide`}
              key={entry.membership.id}
            >
              <span className="organization-card__mark">
                {entry.organization.name
                  .slice(0, 1)
                  .toUpperCase()}
              </span>

              <div>
                <span className="section-kicker">
                  {roleLabel(
                    entry.membership.role,
                  )}
                </span>

                <h2>
                  {entry.organization.name}
                </h2>

                <p>
                  Abrir roteiro e continuar
                  de onde parou.
                </p>
              </div>

              <strong>
                Começar / continuar →
              </strong>
            </a>
          ))}
        </section>
      ) : (
        <section className="tenant-empty-state">
          <span className="section-kicker">
            Nenhuma organização disponível
          </span>

          <h2>
            Sua conta ainda não possui
            acesso a uma organização.
          </h2>

          <p>
            Peça a um Administrador da
            organização para adicionar sua
            conta. O Platform Admin não
            recebe acesso automático aos
            dados de clientes.
          </p>
        </section>
      )}

      <section
        className="panel"
        style={{
          marginTop: "2rem",
        }}
      >
        <span className="section-kicker">
          Conta e administração
        </span>
        <h2>
          Ações fora do roteiro de avaliação
        </h2>
        <p>
          Use estas opções apenas para
          administração da plataforma ou
          segurança da sua própria sessão.
        </p>

        <div className="operational-actions">
          {isPlatformAdmin ? (
            <>
              <a
                className="button button--secondary"
                href="/app/admin/organizations/new"
              >
                Criar organização
              </a>

              <a
                className="button button--secondary"
                href="/app/admin/users"
              >
                Gerenciar usuários
              </a>
            </>
          ) : null}

          <a
            className="button button--quiet"
            href="/app/security/sessions"
          >
            Minhas sessões
          </a>
        </div>
      </section>
    </>
  );
}
