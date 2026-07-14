export default function Loading() {
  return (
    <main className="loading-page" aria-busy="true" aria-label="Carregando painel">
      <div className="loading-shell">
        <div className="skeleton skeleton--title" />
        <div className="skeleton skeleton--text" />

        <div className="skeleton-grid">
          <div className="skeleton skeleton--card" />
          <div className="skeleton skeleton--card" />
          <div className="skeleton skeleton--card" />
        </div>
      </div>
    </main>
  );
}
