import type {
  ReactNode,
} from "react";

import {
  hasTenantPermission,
  roleLabel,
} from "@/lib/authorization";
import {
  requireOrganizationContext,
} from "@/lib/organization-context";

type TenantLayoutParams = Promise<{
  organizationSlug: string;
}>;

export default async function TenantLayout({
  children,
  params,
}: {
  children: ReactNode;
  params: TenantLayoutParams;
}) {
  const {
    organizationSlug,
  } = await params;

  const context =
    await requireOrganizationContext({
      organizationSlug,
      permission: "organization:read",
    });

  const basePath =
    `/app/${context.organization.slug}`;

  const canReadMemberships =
    hasTenantPermission(
      context.membership.role,
      "membership:read",
    );

  return (
    <div className="tenant-shell">
      <aside className="tenant-sidebar">
        <a
          className="tenant-back-link"
          href="/app"
        >
          ← Trocar organização
        </a>

        <div className="tenant-identity">
          <span
            className="tenant-identity__mark"
            aria-hidden="true"
          >
            {context.organization.name
              .slice(0, 1)
              .toUpperCase()}
          </span>

          <div>
            <strong>
              {context.organization.name}
            </strong>

            <span>
              {roleLabel(
                context.membership.role,
              )}
            </span>
          </div>
        </div>

        <nav
          className="tenant-nav"
          aria-label={
            "Navegação da organização"
          }
        >
          <a href={basePath}>
            Visão geral
          </a>

          <a href={`${basePath}/guide`}>
            Comece aqui
          </a>

          <a href={`${basePath}/projects`}>
            1. Projetos
          </a>

          <a
            href={`${basePath}/environments`}
          >
            2. Ambientes
          </a>

          <a
            href={`${basePath}/assessments`}
          >
            3–5. Avaliações
          </a>

          <a href={`${basePath}/evidence`}>
            Evidence Library
          </a>

          {canReadMemberships ? (
            <a
              href={`${basePath}/members`}
            >
              Membros
            </a>
          ) : null}
        </nav>

        <div className="tenant-boundary-note">
          <strong>
            Dúvida sobre o próximo passo?
          </strong>

          <p>
            Abra “Comece aqui”. O roteiro
            mostra o que já existe e qual
            etapa deve ser concluída em
            seguida.
          </p>
        </div>
      </aside>

      <div className="tenant-content">
        {children}
      </div>
    </div>
  );
}
