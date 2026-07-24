import {
  requireActiveSession,
} from "@/lib/session";
import {
  listUserSessions,
} from "@/lib/session-administration";
import {
  SessionControls,
} from "./SessionControls";

export const dynamic =
  "force-dynamic";

export default async function SessionsPage() {
  const currentSession =
    await requireActiveSession();

  const sessions =
    await listUserSessions(
      currentSession.user.id,
    );

  return (
    <section className="security-sessions-page">
      <a
        className="tenant-back-link"
        href="/app"
      >
        ← Voltar
      </a>

      <span className="section-kicker">
        Segurança da conta
      </span>

      <h1>
        Sessões ativas
      </h1>

      <p>
        Encerre acessos que você não reconhece.
        A redefinição de senha encerra
        automaticamente todas as sessões.
      </p>

      <SessionControls
        sessions={sessions.map(
          (session) => ({
            id: session.id,

            createdAt:
              session.createdAt
                .toISOString(),

            updatedAt:
              session.updatedAt
                .toISOString(),

            expiresAt:
              session.expiresAt
                .toISOString(),

            ipAddress:
              session.ipAddress,

            userAgent:
              session.userAgent,

            current:
              session.id ===
              currentSession.session.id,
          }),
        )}
      />
    </section>
  );
}
