import {
  roleLabel,
} from "@/lib/authorization";
import {
  listAccessibleOrganizations,
} from "@/lib/organization-context";
import {
  requireActiveSession,
} from "@/lib/session";

export default async function OperationalHomePage() {
  const currentSession =
    await requireActiveSession();

  const organizations =
    await listAccessibleOrganizations(
      currentSession.user.id,
    );

  return (
    <>
      <section className="operational-hero">
        <span className="section-kicker">
          Contexto organizacional
        </span>

        <h1>
          Escolha uma organização autorizada.
        </h1>

        <p>
          A organização é resolvida no
          servidor a partir da sua membership
          ativa. IDs e papéis enviados pelo
          navegador não são considerados
          confiáveis.
        </p>
      </section>

      {organizations.length > 0 ? (
        <section
          className="organization-grid"
          aria-label={
            "Organizações disponíveis"
          }
        >
          {organizations.map((entry) => (
            <a
              className="organization-card"
              href={`/app/${entry.organization.slug}`}
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

                <code>
                  {entry.organization.slug}
                </code>
              </div>

              <strong>
                Acessar organização →
              </strong>
            </a>
          ))}
        </section>
      ) : (
        <section className="tenant-empty-state">
          <span className="section-kicker">
            Nenhum tenant disponível
          </span>

          <h2>
            Sua conta não possui uma
            membership operacional ativa.
          </h2>

          <p>
            Contas de plataforma não recebem
            acesso implícito às organizações.
            Um administrador do tenant precisa
            criar ou reativar a membership.
          </p>
        </section>
      )}

      <section className="operational-boundary">
        <div>
          <span className="section-kicker">
            Auth-1C
          </span>

          <h2>
            Autenticação e autorização
            permanecem separadas.
          </h2>
        </div>

        <p>
          A sessão identifica o usuário.
          A membership ativa determina quais
          organizações e operações podem ser
          acessadas.
        </p>
      </section>
    </>
  );
}
