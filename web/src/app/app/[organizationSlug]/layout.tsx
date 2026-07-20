import type {
  ReactNode,
} from "react";

import {
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

          <a href={`${basePath}/projects`}>
            Projetos
          </a>

          <a
            href={`${basePath}/environments`}
          >
            Ambientes
          </a>
        </nav>

        <div className="tenant-boundary-note">
          <strong>
            Isolamento ativo
          </strong>

          <p>
            Todas as consultas desta área
            recebem o ID da organização
            resolvido pela membership no
            servidor.
          </p>
        </div>
      </aside>

      <div className="tenant-content">
        {children}
      </div>
    </div>
  );
}
