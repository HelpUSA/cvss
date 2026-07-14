export default function NotFound() {
  return (
    <main className="not-found-page">
      <section className="not-found-card">
        <span className="section-kicker">404</span>
        <h1>Página não encontrada.</h1>
        <p>
          O endereço solicitado não faz parte da experiência pública atual.
        </p>

        <a className="button button--primary" href="/">
          Voltar ao painel
        </a>
      </section>
    </main>
  );
}
