"use client";

import {
  useState,
} from "react";
import {
  useRouter,
} from "next/navigation";

const ROLES = [
  "ADMIN",
  "OPERATOR",
  "REVIEWER",
  "VIEWER",
] as const;

const STATUSES = [
  "ACTIVE",
  "SUSPENDED",
  "REVOKED",
] as const;

type Role =
  (typeof ROLES)[number];

type Status =
  (typeof STATUSES)[number];

export function MembershipControls({
  organizationSlug,
  membershipId,
  initialRole,
  initialStatus,
}: {
  organizationSlug: string;
  membershipId: string;
  initialRole: Role;
  initialStatus: Status;
}) {
  const router = useRouter();

  const [role, setRole] =
    useState<Role>(
      initialRole,
    );

  const [status, setStatus] =
    useState<Status>(
      initialStatus,
    );

  const [pending, setPending] =
    useState(false);

  const [message, setMessage] =
    useState("");

  async function save() {
    setPending(true);
    setMessage("");

    try {
      const response = await fetch(
        `/api/organizations/${encodeURIComponent(
          organizationSlug,
        )}/memberships/${encodeURIComponent(
          membershipId,
        )}`,
        {
          method: "PATCH",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            role,
            status,
          }),
        },
      );

      const payload =
        await response
          .json()
          .catch(() => null);

      if (!response.ok) {
        throw new Error(
          payload?.message ??
            "A membership não pôde ser atualizada.",
        );
      }

      setMessage(
        "Membership atualizada.",
      );

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
    <div className="membership-controls">
      <div className="field">
        <label
          htmlFor={`role-${membershipId}`}
        >
          Papel
        </label>

        <select
          id={`role-${membershipId}`}
          value={role}
          onChange={(event) =>
            setRole(
              event.target.value as Role,
            )
          }
        >
          {ROLES.map((value) => (
            <option
              value={value}
              key={value}
            >
              {value}
            </option>
          ))}
        </select>
      </div>

      <div className="field">
        <label
          htmlFor={`status-${membershipId}`}
        >
          Status
        </label>

        <select
          id={`status-${membershipId}`}
          value={status}
          onChange={(event) =>
            setStatus(
              event.target.value as Status,
            )
          }
        >
          {STATUSES.map((value) => (
            <option
              value={value}
              key={value}
            >
              {value}
            </option>
          ))}
        </select>
      </div>

      <button
        className="button button--secondary"
        type="button"
        disabled={pending}
        onClick={save}
      >
        {pending
          ? "Salvando..."
          : "Salvar"}
      </button>

      {message ? (
        <p
          className="management-feedback"
          role="status"
        >
          {message}
        </p>
      ) : null}
    </div>
  );
}
