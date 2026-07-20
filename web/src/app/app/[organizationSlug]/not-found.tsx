export default function TenantNotFound() {
  return (
    <section className="tenant-empty-state">
      <span className="section-kicker">
        Contexto indisponível
      </span>

      <h1>
        Organização não encontrada.
      </h1>

      <p>
        O endereço pode não existir ou sua
        conta pode não possuir uma membership
        operacional ativa.
      </p>

      <a
        className="button button--primary"
        href="/app"
      >
        Voltar às organizações
      </a>
    </section>
  );
}
