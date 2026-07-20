export default function OperationalHomePage() {
  return (
    <>
      <section className="operational-hero">
        <span className="section-kicker">
          Auth-1B operacional
        </span>

        <h1>
          Fundação autenticada pronta para
          os fluxos multiusuário.
        </h1>

        <p>
          Login, logout, sessão persistida,
          bloqueio de contas inativas e
          proteção autoritativa no servidor
          estão conectados ao schema
          PostgreSQL existente.
        </p>
      </section>

      <section
        className="operational-grid"
        aria-label={
          "Estado da fundação operacional"
        }
      >
        <article className="operational-card">
          <span>01</span>
          <h2>Identidade</h2>

          <p>
            Better Auth utiliza os modelos
            de identidade adicionados pela
            Auth-1A.
          </p>

          <strong>Operacional</strong>
        </article>

        <article className="operational-card">
          <span>02</span>
          <h2>Sessão</h2>

          <p>
            A sessão é recusada quando a
            conta está suspensa ou
            desabilitada.
          </p>

          <strong>Fail closed</strong>
        </article>

        <article className="operational-card">
          <span>03</span>
          <h2>Provisionamento</h2>

          <p>
            O primeiro administrador depende
            de comando explícito e variáveis
            de ambiente.
          </p>

          <strong>
            Sem registro público
          </strong>
        </article>

        <article className="operational-card">
          <span>04</span>
          <h2>Próxima fronteira</h2>

          <p>
            Organizações, memberships,
            papéis e ambientes serão
            conectados na Auth-1C.
          </p>

          <strong>Auth-1C</strong>
        </article>
      </section>

      <section className="operational-boundary">
        <div>
          <span className="section-kicker">
            Limite atual
          </span>

          <h2>
            Autenticação não equivale a
            autorização por tenant.
          </h2>
        </div>

        <p>
          A Auth-1B comprova identidade e
          estado da conta. RBAC, seleção
          organizacional e isolamento de
          dados continuam pendentes.
        </p>
      </section>
    </>
  );
}
