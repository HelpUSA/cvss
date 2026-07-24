import { notFound } from "next/navigation";

import {
  isActivePlatformAdmin,
} from "@/lib/platform-administration";
import {
  requireActiveSession,
} from "@/lib/session";
import {
  OrganizationCreateForm,
} from "./OrganizationCreateForm";

export default async function NewOrganizationPage() {
  const currentSession =
    await requireActiveSession();

  const permitted =
    await isActivePlatformAdmin(
      currentSession.user.id,
    );

  if (!permitted) {
    notFound();
  }

  return (
    <section className="admin-form-page">
      <a
        className="tenant-back-link"
        href="/app"
      >
        ← Voltar às organizações
      </a>

      <span className="section-kicker">
        Administração da plataforma
      </span>

      <h1>
        Criar organização
      </h1>

      <p>
        A organização será criada com você
        como primeiro administrador ativo.
        Isso não concede acesso a qualquer
        outra organização.
      </p>

      <OrganizationCreateForm />
    </section>
  );
}
