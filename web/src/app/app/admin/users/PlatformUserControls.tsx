"use client";

import {
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

type Props = {
  userId: string;
  currentStatus:
    | "ACTIVE"
    | "SUSPENDED"
    | "DISABLED";
  currentPlatformRole:
    | "USER"
    | "PLATFORM_ADMIN";
  canonical: boolean;
};

export function PlatformUserControls({
  userId,
  currentStatus,
  currentPlatformRole,
  canonical,
}: Props) {
  const router = useRouter();
  const [pending, setPending] =
    useState(false);
  const [message, setMessage] =
    useState("");

  async function update(
    patch: Record<string, string>,
  ) {
    setPending(true);
    setMessage("");

    try {
      const response = await fetch(
        `/api/platform/users/${userId}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify(patch),
        },
      );

      const payload =
        await response
          .json()
          .catch(() => null);

      if (!response.ok) {
        throw new Error(
          payload?.message ??
            "A alteração não pôde ser aplicada.",
        );
      }

      setMessage("Atualizado");
      router.refresh();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Falha inesperada.",
      );
    } finally {
      setPending(false);
    }
  }

  return (
    <div style={{ display: "grid", gap: "8px", minWidth: "180px" }}>
      <select
        aria-label="Status do usuário"
        value={currentStatus}
        disabled={pending || canonical}
        onChange={(event) =>
          void update({
            status: event.target.value,
          })
        }
      >
        <option value="ACTIVE">ACTIVE</option>
        <option value="SUSPENDED">SUSPENDED</option>
        <option value="DISABLED">DISABLED</option>
      </select>

      <select
        aria-label="Papel de plataforma"
        value={currentPlatformRole}
        disabled={pending || canonical}
        onChange={(event) =>
          void update({
            platformRole:
              event.target.value,
          })
        }
      >
        <option value="USER">USER</option>
        <option value="PLATFORM_ADMIN">
          PLATFORM_ADMIN
        </option>
      </select>

      {canonical ? (
        <small>
          Conta canônica protegida.
        </small>
      ) : null}

      {message ? (
        <small aria-live="polite">
          {message}
        </small>
      ) : null}
    </div>
  );
}
