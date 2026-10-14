import { notFound } from "next/navigation";

import {
  isActivePlatformAdmin,
} from "@/lib/platform-administration";
import {
  isCanonicalPlatformSuperAdminEmail,
} from "@/lib/platform-superadmin";
import {
  listPlatformUsers,
} from "@/lib/platform-user-administration";
import {
  requireActiveSession,
} from "@/lib/session";

import {
  PlatformUserControls,
} from "./PlatformUserControls";

export default async function PlatformUsersPage() {
  const currentSession =
    await requireActiveSession();

  const permitted =
    await isActivePlatformAdmin(
      currentSession.user.id,
    );

  if (!permitted) {
    notFound();
  }

  const users =
    await listPlatformUsers();

  const actorIsCanonical =
    isCanonicalPlatformSuperAdminEmail(
      currentSession.user.email,
    );

  return (
    <section className="tenant-page-heading">
      <span className="section-kicker">
        Administração da plataforma
      </span>

      <h1>Usuários</h1>

      <p>
        Gestão global de contas Google,
        status da conta, sessões e papéis
        de plataforma. O acesso a cada
        organização continua dependendo
        de membership ativa.
      </p>

      <div className="table-wrap" style={{ marginTop: "24px" }}>
        <table>
          <thead>
            <tr>
              <th>Usuário</th>
              <th>Provedores</th>
              <th>Status</th>
              <th>Papel plataforma</th>
              <th>Memberships</th>
              <th>Sessões</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>
                  <strong className="table-primary">
                    {user.name}
                  </strong>
                  <span className="table-secondary">
                    {user.email}
                    {isCanonicalPlatformSuperAdminEmail(user.email)
                      ? " · SuperAdmin canônico"
                      : ""}
                  </span>
                </td>
                <td>
                  {user.accounts
                    .map((account) => account.providerId)
                    .join(", ") || "—"}
                </td>
                <td>{user.status}</td>
                <td>{user.platformRole}</td>
                <td>{user._count.memberships}</td>
                <td>{user._count.sessions}</td>
                <td>
                  <PlatformUserControls
                    userId={user.id}
                    currentStatus={user.status}
                    currentPlatformRole={user.platformRole}
                    canonical={isCanonicalPlatformSuperAdminEmail(user.email)}
                    canManagePlatformRole={actorIsCanonical}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
