import {
  requireOrganizationContext,
} from "@/lib/organization-context";
import {
  listTenantEvidenceSnapshots,
} from "@/lib/tenant-data";

type Params = Promise<{
  organizationSlug: string;
}>;

export default async function EvidenceLibraryPage({
  params,
}: {
  params: Params;
}) {
  const { organizationSlug } = await params;

  const context =
    await requireOrganizationContext({
      organizationSlug,
      permission: "environment:read",
    });

  const snapshots =
    await listTenantEvidenceSnapshots(
      context,
    );

  const base =
    `/app/${context.organization.slug}`;

  return (
    <>
      <section className="tenant-page-heading">
        <span className="section-kicker">
          Evidence Library
        </span>
        <h1>
          Evidências preservadas por ambiente
        </h1>
        <p>
          Consulte snapshots já capturados,
          sua origem, data, validade e hash.
          Esta biblioteca não recalcula
          resultados nem altera evidências
          históricas.
        </p>
      </section>

      <div
        className="panel"
        style={{ marginBottom: "1.25rem" }}
      >
        <strong>
          Como usar esta biblioteca
        </strong>
        <p>
          Cada execução cria um snapshot
          imutável ligado ao ambiente. Use a
          biblioteca para verificar
          provenance e decidir se uma nova
          execução pode reutilizar a mesma
          fonte ou se precisa de evidência
          mais recente.
        </p>
        <a
          className="button button--secondary"
          href={`${base}/environments`}
        >
          Ver ambientes
        </a>
      </div>

      {snapshots.length > 0 ? (
        <section className="tenant-list">
          {snapshots.map((snapshot) => {
            const expired =
              snapshot.expiresAt !== null &&
              snapshot.expiresAt.getTime() <
                Date.now();

            return (
              <article
                className="tenant-list-card"
                key={snapshot.id}
              >
                <div>
                  <span className="section-kicker">
                    {
                      snapshot.environment
                        .project.name
                    }{" "}
                    / {
                      snapshot.environment
                        .name
                    }
                  </span>
                  <h2>
                    {snapshot.sourceType}
                  </h2>
                  <p className="tenant-muted-copy">
                    {snapshot.sourceReference ??
                      "Sem referência externa informada"}
                  </p>
                  <code>
                    {
                      snapshot.canonicalHash
                    }
                  </code>
                </div>

                <dl>
                  <div>
                    <dt>Capturada</dt>
                    <dd>
                      {snapshot.capturedAt.toLocaleString(
                        "pt-BR",
                      )}
                    </dd>
                  </div>
                  <div>
                    <dt>Validade</dt>
                    <dd>
                      {snapshot.expiresAt
                        ? snapshot.expiresAt.toLocaleString(
                            "pt-BR",
                          )
                        : "Não informada"}
                    </dd>
                  </div>
                  <div>
                    <dt>Estado</dt>
                    <dd>
                      {expired
                        ? "Expirada"
                        : "Preservada"}
                    </dd>
                  </div>
                  <div>
                    <dt>Execuções</dt>
                    <dd>
                      {snapshot._count.runs}
                    </dd>
                  </div>
                </dl>
              </article>
            );
          })}
        </section>
      ) : (
        <section className="tenant-empty-state">
          <h2>
            Nenhuma evidência preservada ainda.
          </h2>
          <p>
            A biblioteca será preenchida
            automaticamente à medida que
            avaliações forem executadas.
          </p>
          <a
            className="button button--primary"
            href={`${base}/assessments`}
          >
            Ir para avaliações
          </a>
        </section>
      )}
    </>
  );
}
