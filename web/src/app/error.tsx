"use client";

export default function ErrorPage({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <main className="error-page">
      <section className="error-card">
        <span className="section-kicker">Falha controlada</span>
        <h1>Não foi possível carregar o painel.</h1>
        <p>
          Os dados permanecem preservados. Tente executar novamente ou volte
          para o início.
        </p>

        <div className="error-actions">
          <button
            className="button button--primary"
            type="button"
            onClick={reset}
          >
            Tentar novamente
          </button>

          <a className="button button--secondary" href="/">
            Voltar ao início
          </a>
        </div>
      </section>
    </main>
  );
}
