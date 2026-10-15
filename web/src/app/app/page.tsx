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
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "8px", marginBottom: "8px" }}>
          <span className="section-kicker" style={{ margin: 0 }}>
            Workspace operacional
          </span>
          {isPlatformAdmin ? (
            <span
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                fontSize: "12px",
                fontWeight: 700,
                color: "#f59e0b",
                background: "rgba(245, 158, 11, 0.15)",
                border: "1px solid rgba(245, 158, 11, 0.4)",
                padding: "4px 12px",
                borderRadius: "999px",
              }}
            >
              👑 Platform SuperAdmin ({currentSession.user.email})
            </span>
          ) : (
            <span
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                fontSize: "12px",
                fontWeight: 600,
                color: "#94a3b8",
                background: "rgba(255, 255, 255, 0.05)",
                border: "1px solid rgba(255, 255, 255, 0.1)",
                padding: "4px 12px",
                borderRadius: "999px",
              }}
            >
              👤 Usuário ({currentSession.user.email})
            </span>
          )}
        </div>

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
